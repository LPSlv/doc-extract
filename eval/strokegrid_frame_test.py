# /// script
# requires-python = ">=3.10"
# dependencies = ["pymupdf==1.28.0"]
# ///
"""Does requiring the verticals to BE the frame's edges beat the plain rule?

The plain rule drops a `stroke_grid` firing whose page has exactly two distinct
vertical stroke positions repeated on >=BOX_REPEATS pages. On the holdout it
dropped 18 pages; 17 were waste and the 18th was Table 2 of 2608.07734v1 - a
booktabs table CONTINUED across pages, whose two interior rules repeat exactly
as a template does. That page survives only because cost_guard renders its
whole document anyway.

The proposed refinement is not a new threshold, it is the definition of a
frame: a box's two verticals are the LEFT AND RIGHT EXTREMES of the page's
horizontal strokes, because the rules run from one edge to the other. A
continued table's interior rules sit strictly inside its horizontal rules.

This scores both rules against every labelled firing - 170 in-sample from
eval/strokegrid/labels.tsv, 18 out-of-sample from the holdout - so the
refinement is accepted or rejected on 188 observations rather than on the one
that suggested it.

    uv run eval/strokegrid_frame_test.py
"""
import collections, json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
SG = ROOT / "eval" / "strokegrid"
import fitz

TOL = 2.0
VMIN = 3.0
HMIN = 3.0
REPEATS = 3


def strokes(page):
    """(distinct vertical x-positions, x-extent of horizontal strokes)."""
    vx, hx = [], []
    for d in page.get_cdrawings():
        for it in d.get("items", ()):
            if it[0] != "l":
                continue
            (x0, y0), (x1, y1) = _xy(it[1]), _xy(it[2])
            dx, dy = abs(x0 - x1), abs(y0 - y1)
            if dx <= 1 and dy > VMIN:
                vx.append((x0 + x1) / 2)
            elif dy <= 1 and dx > HMIN:
                hx += [x0, x1]
    out = []
    for x in sorted(vx):
        if not out or x - out[-1] > TOL:
            out.append(x)
    span = (min(hx), max(hx)) if hx else None
    return tuple(round(x) for x in out), span


def _xy(p):
    return (p[0], p[1]) if isinstance(p, (tuple, list)) else (p.x, p.y)


def page_facts(path):
    with fitz.open(str(path)) as d:
        return [strokes(p) for p in d]


def evaluate(doc_pages, page_no):
    """(plain rule drops?, framed rule drops?) for a 1-based page."""
    fps = [f for f, _ in doc_pages]
    me, span = doc_pages[page_no - 1]
    if len(me) != 2:
        return False, False
    if sum(1 for f in fps if f == me) < REPEATS:
        return False, False
    if span is None:
        return True, False
    framed = abs(me[0] - span[0]) <= TOL and abs(me[1] - span[1]) <= TOL
    return True, framed


def main():
    cases = []          # (label, path, page)

    for line in (SG / "labels.tsv").read_text().strip().splitlines()[1:]:
        c = line.split("\t")
        cases.append((c[4].strip(), ROOT / "corpus" / c[1] / c[2], int(c[3])))

    hold = json.loads((SG / "holdout" / "index.json").read_text())["candidates"]
    hl = {}
    for line in (SG / "holdout" / "labels.tsv").read_text().strip().splitlines()[1:]:
        c = line.split("\t")
        hl[c[0]] = c[4].strip()
    hl["h018"] = "table"     # 2608.07734v1 p19, labelled blind after the fact
    for c in hold:
        cases.append((hl[c["tag"]], ROOT / "corpus" / "arxiv_holdout" / c["file"],
                      c["page"]))
    cases.append(("table", ROOT / "corpus" / "arxiv_holdout" / "2608.07734v1.pdf", 19))

    cache, tally = {}, collections.defaultdict(collections.Counter)
    for label, path, page in cases:
        if not path.exists():
            print(f"missing {path}", file=sys.stderr)
            continue
        if path not in cache:
            cache[path] = page_facts(path)
        plain, framed = evaluate(cache[path], page)
        waste = label == "none"
        if plain:
            tally["plain"]["cut" if waste else "lost"] += 1
        if framed:
            tally["framed"]["cut" if waste else "lost"] += 1
        if plain and not waste:
            print(f"  LOST by plain  : {path.name} p{page} ({label})"
                  f"{'  [rescued by framed]' if not framed else ''}")

    print(f"{'rule':<10}{'wasted cut':>12}{'real lost':>11}{'precision':>11}")
    for k in ("plain", "framed"):
        cut, lost = tally[k]["cut"], tally[k]["lost"]
        p = cut / (cut + lost) * 100 if cut + lost else float("nan")
        print(f"{k:<10}{cut:>12}{lost:>11}{p:>10.0f}%")


if __name__ == "__main__":
    main()
