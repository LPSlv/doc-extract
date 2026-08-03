# /// script
# requires-python = ">=3.10"
# dependencies = ["pdf-inspector==0.2.6", "pymupdf==1.28.0"]
# ///
"""Three-way benchmark on the TDS corpus: full optical, pdf-inspector, pdf-extract.

  full optical    every page rendered and read as an image
  pdf-inspector   text extraction only, no vision at all
  pdf-extract     text + only the pages/images routing flags

Reports dataset size, wall time per stage, and input-token cost.
Usage: uv run eval/tds-bench.py corpus/tds
"""
import sys, time, json, statistics, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills" / "pdf-extract"))
import fitz, pdf_inspector as pi
from harvest import harvest

MAXPX = 1568
def tok(w, h):
    s = min(1.0, MAXPX / max(w, h)); return int((w * s) * (h * s) / 750)

def med(fn, n=3):
    ts = []
    for _ in range(n):
        t = time.perf_counter(); r = fn(); ts.append(time.perf_counter() - t)
    return statistics.median(ts), r

def main(folder):
    files = sorted(pathlib.Path(folder).glob("*.pdf"))
    rows = []
    for f in files:
        p = str(f)
        d = fitz.open(p); pages = len(d)
        # --- A: full optical -------------------------------------------
        t_opt, _ = med(lambda: [pg.get_pixmap(dpi=140) for pg in fitz.open(p)], n=1)
        opt_tok = 0
        for pg in d:
            pm = pg.get_pixmap(dpi=140); opt_tok += tok(pm.width, pm.height)
        d.close()
        # --- B: pdf-inspector only -------------------------------------
        try:
            t_txt, res = med(lambda: pi.process_pdf(p))
        except Exception as e:
            print(f"SKIP {f.name}: {type(e).__name__}"); d.close() if not d.is_closed else None
            continue
        md = getattr(res, "markdown", None) or ""
        txt_tok = int(len(md) / 3.5)
        # --- C: pdf-extract --------------------------------------------
        t_har, h = med(lambda: harvest(p), n=1)
        if h["status"] != "ok":
            print(f"SKIP {f.name}: {h['error']}"); continue
        d2 = fitz.open(p); ours_img = 0
        t0 = time.perf_counter()
        for it in h["items"]:
            if it["kind"] == "raster":
                ours_img += tok(*it["px"])
            else:
                pg = d2[it["page"] - 1]
                e = it.get("edge") or 1100
                s = e / max(pg.rect.width, pg.rect.height)
                pm = pg.get_pixmap(matrix=fitz.Matrix(s, s))
                ours_img += tok(pm.width, pm.height)
        t_render = time.perf_counter() - t0
        d2.close()
        rows.append(dict(name=f.stem, pages=pages, bytes=f.stat().st_size,
                         calls=h["vision_calls"],
                         opt_tok=opt_tok, txt_tok=txt_tok, ours_tok=txt_tok + ours_img,
                         t_opt=t_opt, t_txt=t_txt, t_ours=t_txt + t_har + t_render))
    return rows

if __name__ == "__main__":
    rows = main(sys.argv[1] if len(sys.argv) > 1 else "corpus/tds")
    P = sum(r["pages"] for r in rows); B = sum(r["bytes"] for r in rows)
    print(f"DATASET  {len(rows)} files   {P} pages   {B/1024/1024:.1f} MB   "
          f"median {statistics.median([r['pages'] for r in rows]):.0f} pages/file, "
          f"max {max(r['pages'] for r in rows)}")
    print()
    print(f"{'':<18}{'tokens':>14}{'vs optical':>12}{'time (s)':>11}{'vision calls':>14}")
    print("-" * 69)
    for label, tk, tm, calls in (
        ("full optical",  sum(r["opt_tok"] for r in rows),  sum(r["t_opt"] for r in rows),  P),
        ("pdf-inspector", sum(r["txt_tok"] for r in rows),  sum(r["t_txt"] for r in rows),  0),
        ("pdf-extract",   sum(r["ours_tok"] for r in rows), sum(r["t_ours"] for r in rows), sum(r["calls"] for r in rows)),
    ):
        base = sum(r["opt_tok"] for r in rows)
        print(f"{label:<18}{tk:>14,}{1-tk/base:>11.0%}{tm:>11.1f}{calls:>14,}")
    json.dump(rows, open(ROOT / "eval" / "tds-bench.json", "w"), indent=1)
