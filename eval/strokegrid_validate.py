# /// script
# requires-python = ">=3.10"
# dependencies = ["pdf-inspector==0.2.6", "pymupdf==1.28.0"]
# ///
"""Apply the candidate stroke_grid rule to a corpus and render what it drops.

The rule, designed against eval/strokegrid/labels.tsv:

    drop a stroke_grid firing when the page has EXACTLY TWO distinct vertical
    stroke positions (a frame: left edge, right edge, nothing between) AND the
    same fingerprint appears on at least two other pages of the document
    (a real table appears once; a box template repeats).

In-sample that is 35 of 72 wasted calls removed, 2 real items lost, 95%
precision, stable at 92%/96% under a document-level split. Those numbers are
in-sample by construction, which is why this script exists: point it at a
corpus the rule was NOT designed on, label what it drops, and see whether the
precision survives.

`bills` and the olmOCR corpora cannot serve - between them they produce 17
firings and the rule fires on none, because single-page extracts and short
bills have no page template to repeat. corpus/arxiv_holdout is fetched fresh
for this purpose from a different month (2608.*) than corpus/arxiv (2607.*).

    uv run eval/strokegrid_validate.py corpus/arxiv_holdout
"""
import json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills" / "doc-extract"))
import fitz
from harvest import harvest_batch

OUT = ROOT / "eval" / "strokegrid" / "holdout"
TOL = 2.0
DPI = 130


def _xy(p):
    return (p[0], p[1]) if isinstance(p, (tuple, list)) else (p.x, p.y)


def fingerprint(page, tol=TOL):
    """Rounded distinct x-positions of vertical strokes on this page."""
    vx = []
    for d in page.get_cdrawings():
        for it in d.get("items", ()):
            if it[0] != "l":
                continue
            (x0, y0), (x1, y1) = _xy(it[1]), _xy(it[2])
            if abs(x0 - x1) <= 1 and abs(y0 - y1) > 3:
                vx.append((x0 + x1) / 2)
    out = []
    for x in sorted(vx):
        if not out or x - out[-1] > tol:
            out.append(x)
    return tuple(round(x) for x in out)


def main(corpus):
    paths = sorted(pathlib.Path(corpus).glob("*.pdf"))
    res = harvest_batch([str(p) for p in paths])
    fire = [(p, it["page"]) for p, r in zip(paths, res) if r.get("status") == "ok"
            for it in (r.get("items") or []) if it["reason"] == "stroke_grid"]

    cache, hits = {}, []
    for p, pg in fire:
        if p not in cache:
            try:
                with fitz.open(str(p)) as d:
                    cache[p] = [fingerprint(x) for x in d]
            except Exception:
                cache[p] = None
        pages = cache[p]
        if not pages:
            continue
        me = pages[pg - 1]
        same = sum(1 for j, f in enumerate(pages) if j != pg - 1 and f == me and me)
        if len(me) == 2 and same >= 2:
            hits.append((p, pg))

    (OUT / "pages").mkdir(parents=True, exist_ok=True)
    recs = []
    for i, (p, pg) in enumerate(hits):
        tag = f"h{i+1:03d}"
        with fitz.open(str(p)) as d:
            d[pg - 1].get_pixmap(dpi=DPI).save(str(OUT / "pages" / f"{tag}.png"))
        recs.append({"tag": tag, "file": p.name, "page": pg})

    (OUT / "index.json").write_text(json.dumps(
        {"rule": "vx==2 and same fingerprint on >=2 other pages",
         "corpus": corpus, "n_docs": len(paths), "n_firings": len(fire),
         "n_dropped": len(hits), "candidates": recs}, indent=1))

    print(f"documents        : {len(paths)}")
    print(f"stroke_grid fires: {len(fire)}")
    print(f"rule drops       : {len(hits)}")
    print(f"rendered to {OUT/'pages'} for labelling")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "corpus/arxiv_holdout")
