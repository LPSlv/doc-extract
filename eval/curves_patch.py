# /// script
# requires-python = ">=3.10"
# dependencies = ["pdf-inspector==0.2.6", "pymupdf==1.28.0"]
# ///
"""The proposed `vendor_curves` patch, applied to harvest.py's source at import.

The rule cannot be committed to `skills/doc-extract/harvest.py` from this
session, but the cascade question - does dropping a `curves` page render
un-subsume a raster and put the call back? - can only be answered by running
the WHOLE pipeline with the rule in it. So this module reads harvest.py,
applies the exact textual patch proposed in the report, and execs the result
as a module named `harvest_patched`.

Two properties are worth having explicitly:

  * applying it is a test. Every anchor string is asserted, so if harvest.py
    moves under this file the import fails loudly instead of measuring the
    unpatched pipeline and reporting a flattering "no cascade".
  * `PATCH` below IS the diff in the report. There is no second copy to drift.

    uv run eval/curves_patch.py            # print the unified diff and exit
"""
import difflib
import pathlib
import sys
import types

ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ROOT / "skills" / "doc-extract" / "harvest.py"

# ---------------------------------------------------------------- the patch
IMPORT_OLD = "import sys, json, hashlib, collections\n"
IMPORT_NEW = "import sys, json, re, hashlib, collections\n"

CONST_OLD = ('TEXTONLY_PATHS = 2     # drawing paths a page may have and still '
             'carry no picture\n')
CONST_NEW = CONST_OLD + """CURVES_CLUSTER = 0.05  # largest connected stroke cluster a `curves` page may
                       # cover and still be branding rather than a figure
CLUSTER_GAP   = 24.0   # pt; stroke rects further apart are separate clusters
CLUSTER_CAP   = 2000   # stroke paths above which the test is abandoned (keep)
CAPTION = re.compile(r"\\b(Fig(?:ure)?\\.?|Table|Chart|Scheme|Plate)\\s*\\.?\\s*\\d",
                     re.I)
"""

FUNC_ANCHOR = "def _plot_shaped(g):"
FUNC_NEW = '''def vendor_curves(pg):
    """A `curves` firing that is a vendor logo on a text page, not a figure.

    `_plot_shaped` gates the branch on `stroke_frac`, the union bounding box
    of EVERY stroke path on the page. A logo in the header and a rule in the
    footer put that box across the whole page - the median stroke_frac over
    120 labelled `curves` firings is 0.72 - which is why the 2% floor that
    separates logos from charts in eval/tds-corpus.md does not fire here.

    The largest SPATIALLY CONNECTED stroke cluster does not have that defect.
    On its own it is still not enough (eval/rejected-signals.md: it scores
    0.0372 on the TI header and 0.0372 on a real thermal chart), so it is
    combined with the one gate known to prove content: a figure caption in the
    page text. 175 of 328 content images carry one and 0 of 49 branding
    images do (eval/tds-corpus.md), so as a KEEP-gate it is one-sided in the
    safe direction.

    Cost: the cluster test is single-link on stroke-path bounding boxes, which
    is quadratic, and `curves` pages reach 7,771 paths. Two exact escapes keep
    it off the hot path. Clusters only ever grow, so the moment any partial
    cluster exceeds the threshold the answer is already `False` - a dense
    chart bails within its first few dozen paths. And a page carrying more
    than CLUSTER_CAP stroke paths is not a logo; it is kept untested.
    """
    parea = max(1.0, pg.rect.width * pg.rect.height)
    lim = parea * CURVES_CLUSTER
    rects = []
    for path in pg.get_cdrawings():
        x0, y0, x1, y1 = path["rect"]
        if (x1 - x0) * (y1 - y0) > parea * FULLPAGE_FRAC:
            continue                                   # background tint
        if any(it[0] in ("c", "l") for it in path["items"]):
            rects.append([x0, y0, x1, y1])
            if len(rects) > CLUSTER_CAP:
                return False
    # single-link union-find, each set carrying its bounding box
    parent, box = list(range(len(rects))), [list(r) for r in rects]

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    for i in range(len(rects)):
        a = rects[i]
        for j in range(i):
            b = rects[j]
            if (a[0] - CLUSTER_GAP <= b[2] and b[0] - CLUSTER_GAP <= a[2]
                    and a[1] - CLUSTER_GAP <= b[3] and b[1] - CLUSTER_GAP <= a[3]):
                ra, rb = find(i), find(j)
                if ra == rb:
                    continue
                parent[ra] = rb
                bb, ba = box[rb], box[ra]
                bb[0] = min(bb[0], ba[0]); bb[1] = min(bb[1], ba[1])
                bb[2] = max(bb[2], ba[2]); bb[3] = max(bb[3], ba[3])
                if (bb[2] - bb[0]) * (bb[3] - bb[1]) > lim:
                    return False                        # only ever grows
    for i in range(len(rects)):
        if find(i) == i:
            b = box[i]
            if (b[2] - b[0]) * (b[3] - b[1]) > lim:
                return False
    return not CAPTION.search(pg.get_text())


'''

CALL_OLD = """        if why == "stroke_grid" and g["vx_pos"] in boxes:
            dropped.append({"page": i + 1, "why": "boxed_text"})
            continue
"""
CALL_NEW = CALL_OLD + """        if why == "curves" and vendor_curves(pg):
            dropped.append({"page": i + 1, "why": "vendor_curves"})
            continue
"""


def patched_source():
    src = SRC.read_text()
    for old, new in ((IMPORT_OLD, IMPORT_NEW), (CONST_OLD, CONST_NEW),
                     (FUNC_ANCHOR, FUNC_NEW + FUNC_ANCHOR), (CALL_OLD, CALL_NEW)):
        if src.count(old) != 1:
            raise SystemExit(f"anchor not unique in harvest.py: {old[:60]!r}")
        src = src.replace(old, new, 1)
    return src


def load():
    """Import the patched harvest as its own module (the shipped one is
    untouched and can be imported alongside it, which is how the diff runs)."""
    sys.path.insert(0, str(ROOT / "skills" / "doc-extract"))
    mod = types.ModuleType("harvest_patched")
    mod.__file__ = str(SRC)
    exec(compile(patched_source(), str(SRC) + " [patched]", "exec"), mod.__dict__)
    sys.modules["harvest_patched"] = mod
    return mod


if __name__ == "__main__":
    print("".join(difflib.unified_diff(
        SRC.read_text().splitlines(keepends=True),
        patched_source().splitlines(keepends=True),
        "skills/doc-extract/harvest.py", "skills/doc-extract/harvest.py")))
