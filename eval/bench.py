# /// script
# requires-python = ">=3.10"
# dependencies = ["pdf-inspector==0.2.6", "pymupdf==1.28.0"]
# ///
"""Three-way cost benchmark, one dataset at a time, machine-readable output.

  full optical    every page rendered at 140 dpi and read as an image
  pdf-inspector   text extraction only, no vision at all
  pdf-extract     text + only the pages/images harvest.py routes

Generalises eval/tds-bench.py (kept for the README workflow) to arbitrary
corpora and records everything needed for the routing-generalisation
analysis: per-file vision calls, reason histograms, scale-guard hits, and an
independent large-raster proxy for the zero-call cross-check.

    uv run eval/bench.py corpus/<dataset> [--name N] [--limit K]

Writes docs/benchmarks/results/<dataset>.json. Token model (unchanged from
tds-bench.py): image = (w*h)/750 after fitting inside 1568 px long edge,
from actual rendered pixels; text = chars/3.5. Timings are single-run wall
times of the deterministic local pipeline; model inference is excluded.
"""
import collections, datetime, hashlib, json, pathlib, sys, time
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills" / "pdf-extract"))
import fitz, pdf_inspector as pi
from harvest import harvest, batch_furniture, drop_batch_furniture

MAXPX = 1568
OPT_DPI = 140
BIG_RASTER_PX = 300      # min w AND h for the independent "has a figure" proxy


def tok(w, h):
    s = min(1.0, MAXPX / max(w, h))
    return int((w * s) * (h * s) / 750)


def bench_file(path: pathlib.Path):
    row = {"name": path.name, "bytes": path.stat().st_size}

    # --- A: full optical ----------------------------------------------------
    t0 = time.perf_counter()
    opt_tok = 0
    with fitz.open(str(path)) as d:
        row["pages"] = len(d)
        big = set()
        for pg in d:
            pm = pg.get_pixmap(dpi=OPT_DPI)
            opt_tok += tok(pm.width, pm.height)
            pm = None                                  # stream, don't hold
            for img in pg.get_images(full=True):
                xref, w, h = img[0], img[2], img[3]
                if w >= BIG_RASTER_PX and h >= BIG_RASTER_PX:
                    big.add(xref)
    row["opt_tok"] = opt_tok
    row["t_opt"] = time.perf_counter() - t0
    row["big_rasters"] = len(big)

    # --- B: pdf-inspector only ----------------------------------------------
    t0 = time.perf_counter()
    res = pi.process_pdf(str(path))
    row["t_txt"] = time.perf_counter() - t0
    md = getattr(res, "markdown", None) or ""
    row["txt_chars"] = len(md)
    row["txt_tok"] = int(len(md) / 3.5)

    # --- C: pdf-extract -----------------------------------------------------
    t0 = time.perf_counter()
    h = harvest(str(path))
    row["t_har"] = time.perf_counter() - t0
    if h["status"] != "ok":
        row["skip"] = h.get("error", "harvest_failed")
        return row
    row["pdf_type"] = h["pdf_type"]
    row["calls"] = h["vision_calls"]
    row["over_scale_guard"] = h["over_scale_guard"]
    row["reasons"] = dict(collections.Counter(it["reason"] for it in h["items"]))
    row["dropped"] = len(h["dropped"])
    row["_sigs"] = {str(k): tuple(v) for k, v in (h.get("page_sigs") or {}).items()}
    row["_items"] = []

    t0 = time.perf_counter()
    ours_img = 0
    with fitz.open(str(path)) as d2:
        for it in h["items"]:
            if it["kind"] == "raster":
                t = tok(*it["px"])
            else:
                pg = d2[it["page"] - 1]
                e = it.get("edge") or 1100
                s = e / max(pg.rect.width, pg.rect.height)
                pm = pg.get_pixmap(matrix=fitz.Matrix(s, s))
                t = tok(pm.width, pm.height)
            ours_img += t
            row["_items"].append({"page": it["page"], "kind": it["kind"],
                                  "reason": it["reason"], "tok": t})
    row["t_render"] = time.perf_counter() - t0
    row["ours_tok"] = row["txt_tok"] + ours_img
    return row



def apply_batch_furniture(rows):
    """Cross-document emblem removal, mirroring harvest.batch_furniture.

    bench.py harvests file-by-file, so the batch rule has to be re-applied here
    or the benchmark reports false positives the shipped CLI does not make.
    """
    ok = [r for r in rows if not r.get("skip")]
    if len(ok) < 3:
        return rows
    seen = collections.defaultdict(set)
    for r in ok:
        for sig in (r.get("_sigs") or {}).values():
            seen[sig].add(r.get("file") or r.get("name") or r.get("path") or id(r))
    template = {sig for sig, files in seen.items() if len(files) / len(ok) > 0.5}
    if not template:
        return rows
    for r in ok:
        sigs = r.get("_sigs") or {}
        keep, freed = [], 0
        for it in r.get("_items", []):
            if it["kind"] == "page_render" and sigs.get(str(it["page"])) in template:
                freed += it["tok"]; r["dropped"] += 1
            else:
                keep.append(it)
        if freed:
            r["_items"] = keep
            r["ours_tok"] -= freed
            r["calls"] = len(keep)
            r["reasons"] = dict(collections.Counter(i["reason"] for i in keep))
            r["over_scale_guard"] = len(keep) > 15
    return rows

def main(argv):
    folder = pathlib.Path(argv[1]).resolve()
    name = folder.name
    limit = None
    if "--name" in argv:
        name = argv[argv.index("--name") + 1]
    if "--limit" in argv:
        limit = int(argv[argv.index("--limit") + 1])
    files = sorted(folder.glob("*.pdf"))[:limit]
    if not files:
        sys.exit(f"no PDFs in {folder} — fetch the corpus first")
    rows, skips = [], []
    t_start = time.perf_counter()
    for i, f in enumerate(files, 1):
        try:
            row = bench_file(f)
        except Exception as e:
            row = {"name": f.name, "skip": f"{type(e).__name__}: {e}"}
        (skips if "skip" in row else rows).append(row)
        if i % 20 == 0 or i == len(files):
            print(f"  [{i}/{len(files)}] {f.name}"
                  + (f"  SKIP {row['skip']}" if "skip" in row else ""),
                  file=sys.stderr)

    rows = apply_batch_furniture(rows)
    for r in rows:                       # drop bookkeeping before serialising
        r.pop("_sigs", None); r.pop("_items", None)
    P = sum(r["pages"] for r in rows)
    summary = {
        "files": len(rows), "skipped": len(skips), "pages": P,
        "bytes": sum(r["bytes"] for r in rows),
        "opt_tok": sum(r["opt_tok"] for r in rows),
        "txt_tok": sum(r["txt_tok"] for r in rows),
        "ours_tok": sum(r["ours_tok"] for r in rows),
        "calls": sum(r["calls"] for r in rows),
        "reasons": dict(sum((collections.Counter(r["reasons"]) for r in rows),
                            collections.Counter())),
        "t_opt": round(sum(r["t_opt"] for r in rows), 2),
        "t_txt": round(sum(r["t_txt"] for r in rows), 2),
        "t_ours": round(sum(r["t_txt"] + r["t_har"] + r["t_render"]
                            for r in rows), 2),
        "wall_total": round(time.perf_counter() - t_start, 2),
    }
    harvest_src = (ROOT / "skills" / "pdf-extract" / "harvest.py").read_bytes()
    out = {"dataset": name, "generated": datetime.date.today().isoformat(),
           "harvest_sha256": hashlib.sha256(harvest_src).hexdigest()[:16],
           "token_model": {"image": "(w*h)/750 fit 1568px", "text": "chars/3.5",
                           "optical_dpi": OPT_DPI},
           "summary": summary, "rows": rows, "skips": skips}
    dest = ROOT / "docs" / "benchmarks" / "results" / f"{name}.json"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(out, indent=1) + "\n")
    print(f"{name}: {summary['files']} files {P} pages  "
          f"opt {summary['opt_tok']:,}  txt {summary['txt_tok']:,}  "
          f"ours {summary['ours_tok']:,}  calls {summary['calls']:,}  "
          f"-> {dest.relative_to(ROOT)}")


if __name__ == "__main__":
    main(sys.argv)
