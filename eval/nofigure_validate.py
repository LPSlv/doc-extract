# /// script
# requires-python = ">=3.10"
# dependencies = ["pdf-inspector==0.2.6", "pymupdf==1.28.0"]
# ///
"""Apply the candidate `whole_document` rule to a corpus and render its drops.

The rule, designed against eval/nofigure/labels.tsv:

    when cost_guard has collapsed a document into one render per page, drop
    the pages that carry NO raster and AT MOST TWO vector drawing paths.
    Such a page has nothing pictorial on it; a page border and a header rule
    are two paths.

In-sample that is 25 of the 41 wasted `whole_document` calls removed, 0 real
items lost, over 22 distinct documents. Those numbers are in-sample by
construction, which is why this script exists: point it at a corpus the rule
was NOT designed on, render what it drops, label them blind, and see whether
the precision survives.

    uv run eval/nofigure_validate.py corpus/arxiv_holdout
    uv run eval/nofigure_validate.py corpus/pmc_holdout

Deliberately reimplemented here from `fitz` primitives rather than importing
the shipped predicate. The `boxed_text` work found its one real failure mode
only because the analysis script and the shipped implementation were diffed
and disagreed by one page; that diff is impossible if both sides are the same
code. `--diff` performs it.

The rule cannot cascade the way the reverted QR-code filter did. That filter
dropped IMAGES, which pushed pages below `RASTER_GRID` and un-collapsed page
renders into crops. This drops a page render only when the page carries no
raster at all, so there is nothing on it left to un-subsume - and it runs
after cost_guard, never before.
"""
import collections
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills" / "doc-extract"))
import fitz                                                   # noqa: E402
from harvest import harvest                                   # noqa: E402

OUT = ROOT / "eval" / "nofigure" / "holdout"
DPI = 130
SHARDS = 6
MAX_PATHS = 2


def nothing_to_see(pg):
    """No raster placed on this page and at most MAX_PATHS vector paths."""
    if pg.get_images(full=True):
        return False
    return len(pg.get_cdrawings()) <= MAX_PATHS


def run_shard(corpus, i, n):
    parts = OUT / "parts"
    parts.mkdir(parents=True, exist_ok=True)
    paths = sorted(pathlib.Path(corpus).glob("*.pdf"))[i::n]
    recs = []
    for p in paths:
        try:
            r = harvest(str(p))
        except Exception as e:
            recs.append({"file": p.name, "status": f"error {type(e).__name__}"})
            continue
        if r.get("status") != "ok":
            recs.append({"file": p.name, "status": r.get("status")})
            continue
        collapsed = any(d.get("why") == "cost_guard" for d in r["dropped"])
        # The pre-rule whole_document set. Once the rule ships, harvest() has
        # already removed its drops from `items`, so reading `items` alone
        # would make the script report zero and look like a passing result.
        # Adding the recorded drops back reconstructs what it scored against
        # before the ship, so the numbers here stay reproducible.
        wd = ([it["page"] for it in r["items"] if it["reason"] == "whole_document"]
              + [d["page"] for d in r["dropped"] if d.get("why") == "textonly_page"])
        hits = []
        if wd:
            try:
                with fitz.open(str(p)) as d:
                    hits = [pg for pg in wd if nothing_to_see(d[pg - 1])]
            except Exception:
                hits = []
        recs.append({"file": p.name, "status": "ok", "pages": r["pages"],
                     "calls": len(r["items"]), "collapsed": collapsed,
                     "whole_document": wd, "drops": hits})
    (parts / f"shard{i}.json").write_text(json.dumps(recs))


def main(corpus):
    parts = OUT / "parts"
    parts.mkdir(parents=True, exist_ok=True)
    for f in parts.glob("shard*.json"):
        f.unlink()
    procs = [subprocess.Popen(
        [sys.executable, str(pathlib.Path(__file__).resolve()), corpus,
         "--shard", f"{i}/{SHARDS}"]) for i in range(SHARDS)]
    bad = [i for i, p in enumerate(procs) if p.wait() != 0]
    if bad:
        raise SystemExit(f"shards failed: {bad}")
    recs = []
    for i in range(SHARDS):
        recs += json.loads((parts / f"shard{i}.json").read_text())
    recs.sort(key=lambda r: r["file"])

    ok = [r for r in recs if r["status"] == "ok"]
    calls = sum(r["calls"] for r in ok)
    wd = sum(len(r["whole_document"]) for r in ok)
    hits = [(r["file"], p) for r in ok for p in r["drops"]]

    tag_of = {}
    (OUT / "pages").mkdir(parents=True, exist_ok=True)
    name = pathlib.Path(corpus).name
    for i, (f, pg) in enumerate(hits):
        tag = f"{name[:3]}{i + 1:03d}"
        tag_of[(f, pg)] = tag
        with fitz.open(str(pathlib.Path(corpus) / f)) as d:
            d[pg - 1].get_pixmap(dpi=DPI).save(str(OUT / "pages" / f"{tag}.png"))

    (OUT / f"index-{name}.json").write_text(json.dumps({
        "rule": f"whole_document page with 0 rasters and <= {MAX_PATHS} paths",
        "corpus": corpus, "dpi": DPI,
        "documents": len(recs), "ok": len(ok),
        "collapsed_documents": sum(1 for r in ok if r["collapsed"]),
        "vision_calls": calls, "whole_document_calls": wd,
        "n_dropped": len(hits),
        "candidates": [{"tag": tag_of[(f, p)], "file": f, "page": p}
                       for f, p in hits]}, indent=1))

    print(f"corpus              : {corpus}")
    print(f"documents ok        : {len(ok)}/{len(recs)}")
    print(f"collapsed documents : {sum(1 for r in ok if r['collapsed'])}")
    print(f"vision calls        : {calls}")
    print(f"whole_document      : {wd}")
    print(f"rule drops          : {len(hits)}  "
          f"({len({f for f, _ in hits})} documents)")
    print(f"rendered to {OUT / 'pages'} for labelling")


def diff(corpus):
    """Diff this script's drop set against what harvest.py actually drops.

    The `boxed_text` rule's only known failure mode surfaced from exactly this
    comparison and from nothing else.
    """
    name = pathlib.Path(corpus).name
    mine = json.loads((OUT / f"index-{name}.json").read_text())
    want = {(c["file"], c["page"]) for c in mine["candidates"]}
    got = set()
    for p in sorted(pathlib.Path(corpus).glob("*.pdf")):
        r = harvest(str(p))
        if r.get("status") != "ok":
            continue
        for d in r["dropped"]:
            if d.get("why") == "textonly_page":
                got.add((p.name, d["page"]))
    print(f"analysis script : {len(want)}")
    print(f"shipped harvest : {len(got)}")
    only_script = sorted(want - got)
    only_ship = sorted(got - want)
    print(f"only in script  : {len(only_script)} {only_script[:10]}")
    print(f"only in shipped : {len(only_ship)} {only_ship[:10]}")
    return 1 if (only_script or only_ship) else 0


if __name__ == "__main__":
    argv = sys.argv[1:]
    target = next((a for a in argv if not a.startswith("--")), "corpus/pmc_holdout")
    if "--shard" in argv:
        i, n = argv[argv.index("--shard") + 1].split("/")
        run_shard(target, int(i), int(n))
    elif "--diff" in argv:
        raise SystemExit(diff(target))
    else:
        main(target)
