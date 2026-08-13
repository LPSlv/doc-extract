# /// script
# requires-python = ">=3.10"
# dependencies = ["pdf-inspector==0.2.6", "pymupdf==1.28.0"]
# ///
"""The proposed `FILTER3_ROWS = 4` patch, applied to harvest.py's source at import.

Same technique and same reasoning as `eval/curves_patch.py`: the rule is not
this session's to commit, but the questions that matter -- what does it do to
`cost_guard`, to `SCALE_GUARD`, to subsumption -- can only be answered by
running the WHOLE pipeline with the rule in it. So this module reads
`skills/doc-extract/harvest.py`, applies the exact textual patch recorded in
`eval/filter3/proposed.patch`, and execs the result as `harvest_f3`.

`skills/doc-extract/harvest.py` is never written to.

Two properties worth having explicitly:

  * applying it is a test. Every anchor string must occur exactly once, so if
    harvest.py moves under this file the import fails loudly instead of
    silently measuring the unpatched pipeline and reporting "no change".
  * `uv run eval/filter3_patch.py --verify` diffs the result against
    `eval/filter3/proposed.patch` applied by `patch(1)`, so the text below is
    checkably the same rule the report proposes, not a paraphrase of it.

    uv run eval/filter3_patch.py            # print the unified diff and exit
    uv run eval/filter3_patch.py --verify   # ...and check it against the .patch
"""
import difflib
import pathlib
import subprocess
import sys
import tempfile
import types

ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ROOT / "skills" / "doc-extract" / "harvest.py"
PATCHFILE = ROOT / "eval" / "filter3" / "proposed.patch"

# ---------------------------------------------------------------- the patch
CONST_OLD = ("TEXTONLY_PATHS = 2     # drawing paths a page may have and still "
             "carry no picture\n")
CONST_NEW = CONST_OLD + """FILTER3_ROWS  = 4      # pipe rows a parsed table needs before it speaks for
                       # a page that carries no raster; see filter 3
"""

BOXES_OLD = "    boxes = box_templates(geoms)\n"
BOXES_NEW = BOXES_OLD + """    # Every page carrying a raster at all, before filters 1 and 2 have their
    # say. Read by filter 3 below and by drop_textonly after the collapse.
    raster_pages = {p for e in seen.values() for p in e["pages"]}
"""

FILT_OLD = '''        pm = page_mds[i] if i < len(page_mds) else ""
        if pm.count("\\n|") >= 3:
            continue                              # filter 3: extractor won
'''
FILT_NEW = '''        pm = page_mds[i] if i < len(page_mds) else ""
        # -- filter 3: the extractor won -- but only over what it can see, and
        # a table with a header, a rule and ONE data row counts three pipe
        # lines. Where the page also carries a raster, that raster is routed
        # by another path and the page is not lost; rendering it instead is
        # the swap eval/multifigure.md priced and rejected, because a page
        # render caps the raster at its placement (median 0.27x linear
        # resolution). Where the page carries NO raster, this skip is the
        # whole decision and nothing else on the page is ever looked at.
        # Measured over 711 documents: 4,065 such pages are discarded, and of
        # 250 sampled and labelled blind by three labellers, 66% carry a real
        # figure -- the same rate at which the `curves` pages the router DOES
        # route carry one. Requiring two data rows takes the 400 pages whose
        # "table" is a single row: 87% carry a figure in-sample, 73% (95% CI
        # 62-82) on 71 blind labels across two holdouts. eval/filter3.md.
        if pm.count("\\n|") >= (3 if i in raster_pages else FILTER3_ROWS):
            continue
'''

TEXT_OLD = '''        # Only ever after the collapse: before it, `seen` covers images the
        # furniture filter is about to drop, and a page that looks bare here
        # may still be carrying a raster the routed set would have emitted.
        img_pages = {p for e in seen.values() for p in e["pages"]}
        items, gone = drop_textonly(items, geoms, img_pages, ocr_pages)
'''
TEXT_NEW = '''        # Only ever after the collapse: before it, a page that looks bare
        # here may still be carrying a raster the routed set would have
        # emitted, and `raster_pages` deliberately counts images the furniture
        # filter is about to drop.
        items, gone = drop_textonly(items, geoms, raster_pages, ocr_pages)
'''

HUNKS = ((CONST_OLD, CONST_NEW), (BOXES_OLD, BOXES_NEW),
         (FILT_OLD, FILT_NEW), (TEXT_OLD, TEXT_NEW))

# ------------------------------------------------------- the narrowed variant
# NOT the proposed patch. `eval/filter3.md`'s own in-sample branch table --
# written before `corpus/datasheet_holdout` existed -- records `stroke_grid` at
# 0 of 11 and `dense_grid` at 1 of 7 for figures, and says why: those two
# branches MEAN "a ruled table the extractor missed", which is exactly the
# claim filter 3's premise rebuts. This variant therefore leaves filter 3
# untouched on those two branches and relaxes it only on `curves`/`diagonals`.
# `render_reason` is pure and reads only `geoms[i]`, which the loop already
# has, so calling it here costs nothing.
NARROW_CONST_NEW = CONST_NEW + """FILTER3_BRANCHES = ("curves", "diagonals")   # branches the relaxation applies
                       # to; stroke_grid/dense_grid mean "a table the extractor
                       # missed", which is what filter 3 already establishes
"""

NARROW_FILT_NEW = FILT_NEW.replace(
    '        if pm.count("\\n|") >= (3 if i in raster_pages else FILTER3_ROWS):\n'
    '            continue\n',
    '        if pm.count("\\n|") >= (\n'
    '                FILTER3_ROWS if (i not in raster_pages\n'
    '                                 and render_reason(geoms[i])\n'
    '                                 in FILTER3_BRANCHES) else 3):\n'
    '            continue\n')

NARROW_HUNKS = ((CONST_OLD, NARROW_CONST_NEW), (BOXES_OLD, BOXES_NEW),
                (FILT_OLD, NARROW_FILT_NEW), (TEXT_OLD, TEXT_NEW))


def patched_source(narrow=False):
    src = SRC.read_text()
    for old, new in (NARROW_HUNKS if narrow else HUNKS):
        if src.count(old) != 1:
            raise SystemExit(f"anchor not unique in harvest.py: {old[:60]!r}")
        src = src.replace(old, new, 1)
    return src


def load(narrow=False):
    """Import the patched harvest as its own module. The shipped one is
    untouched on disk and can be imported alongside it, which is how the
    before/after comparison runs in one process."""
    sys.path.insert(0, str(ROOT / "skills" / "doc-extract"))
    name = "harvest_f3_narrow" if narrow else "harvest_f3"
    mod = types.ModuleType(name)
    mod.__file__ = str(SRC)
    exec(compile(patched_source(narrow), str(SRC) + " [patched]", "exec"),
         mod.__dict__)
    sys.modules[name] = mod
    return mod


def verify():
    """Apply eval/filter3/proposed.patch with patch(1) and diff the results.

    The point is that nothing here is trusted to be "the same rule" by eye:
    the report's .patch file is the artifact under consideration, and this
    asserts that exec'ing the source built above is exec'ing that patch.
    """
    with tempfile.TemporaryDirectory() as td:
        d = pathlib.Path(td)
        (d / "harvest.py").write_text(SRC.read_text())
        r = subprocess.run(["patch", "-p3", "-s", "-i", str(PATCHFILE),
                            str(d / "harvest.py")],
                           capture_output=True, text=True)
        if r.returncode != 0:
            print(f"patch(1) failed: {r.stdout}{r.stderr}", file=sys.stderr)
            return 2
        want = (d / "harvest.py").read_text()
    got = patched_source()
    if want == got:
        print("VERIFIED: exec'd source is byte-identical to "
              "eval/filter3/proposed.patch applied by patch(1)")
        return 0
    print("".join(difflib.unified_diff(want.splitlines(keepends=True),
                                       got.splitlines(keepends=True),
                                       "patch(1)", "filter3_patch.py")))
    return 1


if __name__ == "__main__":
    if "--verify" in sys.argv:
        raise SystemExit(verify())
    print("".join(difflib.unified_diff(
        SRC.read_text().splitlines(keepends=True),
        patched_source("--narrow" in sys.argv).splitlines(keepends=True),
        "skills/doc-extract/harvest.py", "skills/doc-extract/harvest.py")))
