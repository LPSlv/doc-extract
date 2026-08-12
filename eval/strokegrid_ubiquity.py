# /// script
# requires-python = ">=3.10"
# dependencies = ["pdf-inspector==0.2.6", "pymupdf==1.28.0"]
# ///
"""The second stroke_grid candidate: drop a firing whose signature is ubiquitous.

`harvest.py` already computes a per-document set of page signatures covering
more than UBIQUITY (0.50) of the pages, and already drops such a page as
`vector_furniture` -- but only when it ALSO has low ink, low stroke fraction
and fewer than 8 rects, conditions a ruled vendor title block fails by design.

The candidate is to drop a `stroke_grid` firing on signature ubiquity alone.
On the 170 labelled firings that removed 6 wasted calls and lost nothing, and
it needs no new constant. Both halves of that sentence are in-sample, which is
what sank the last rule's first draft, so this scores it the same way
`boxed_text` was finally scored:

  in-sample   against eval/strokegrid/labels.tsv
  holdout     applied to a corpus the candidate never saw, drops rendered to
              eval/strokegrid/ubiquity/pages/ for blind labelling

Run after boxed_text ships, so what it measures is the MARGINAL effect: the
firings it would remove that boxed_text does not already take.

    uv run eval/strokegrid_ubiquity.py corpus/arxiv_holdout
"""
import collections, json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills" / "doc-extract"))
import fitz
from filters import UBIQUITY
from harvest import harvest_batch, page_geometry

OUT = ROOT / "eval" / "strokegrid" / "ubiquity"
DPI = 130


def sig(g):
    return (g["curves"], g["diagonals"], g["axis_h"], g["axis_v"])


def ubiquitous_pages(path):
    """1-based pages whose signature covers more than UBIQUITY of the document."""
    with fitz.open(str(path)) as d:
        n = len(d)
        geoms = [page_geometry(p) for p in d]
    if n <= 2:
        return set()
    c = collections.Counter(sig(g) for g in geoms)
    tpl = {k for k, v in c.items() if v / n > UBIQUITY}
    return {i + 1 for i, g in enumerate(geoms) if sig(g) in tpl}


def in_sample():
    """Score the candidate against the 170 labels, marginal to boxed_text."""
    rows = [l.split("\t") for l in
            (ROOT / "eval" / "strokegrid" / "labels.tsv")
            .read_text().strip().splitlines()[1:]]
    by_doc = collections.defaultdict(list)
    for r in rows:
        by_doc[ROOT / "corpus" / r[1] / r[2]].append((int(r[3]), r[4].strip()))

    cut = lost = 0
    for path, pages in sorted(by_doc.items()):
        if not path.exists():
            print(f"missing {path}", file=sys.stderr)
            continue
        ub = ubiquitous_pages(path)
        for page, label in pages:
            if page in ub:
                if label == "none":
                    cut += 1
                else:
                    lost += 1
                    print(f"  LOST in-sample: {path.name} p{page} ({label})")
    tot = cut + lost
    print(f"in-sample: {cut} wasted cut, {lost} real lost, "
          f"{cut/tot*100:.0f}% precision" if tot else "in-sample: fires on nothing")
    return cut, lost


def holdout(corpus):
    """Apply to a fresh corpus and render what it would additionally drop."""
    paths = sorted(pathlib.Path(corpus).glob("*.pdf"))
    res = harvest_batch([str(p) for p in paths])
    fire = [(p, it["page"]) for p, r in zip(paths, res) if r.get("status") == "ok"
            for it in (r.get("items") or []) if it["reason"] == "stroke_grid"]

    hits, cache = [], {}
    for p, pg in fire:
        if p not in cache:
            cache[p] = ubiquitous_pages(p)
        if pg in cache[p]:
            hits.append((p, pg))

    (OUT / "pages").mkdir(parents=True, exist_ok=True)
    recs = []
    for i, (p, pg) in enumerate(hits):
        tag = f"u{i+1:03d}"
        with fitz.open(str(p)) as d:
            d[pg - 1].get_pixmap(dpi=DPI).save(str(OUT / "pages" / f"{tag}.png"))
        recs.append({"tag": tag, "file": p.name, "page": pg})

    (OUT / "index.json").write_text(json.dumps(
        {"rule": f"stroke_grid page whose signature covers >{UBIQUITY} of the document",
         "note": "marginal to boxed_text, which is already shipped",
         "corpus": corpus, "n_docs": len(paths),
         "n_firings_after_boxed_text": len(fire), "n_dropped": len(hits),
         "candidates": recs}, indent=1))

    print(f"holdout: {len(paths)} documents, {len(fire)} firings remain after "
          f"boxed_text, this rule drops {len(hits)}")
    if hits:
        print(f"rendered to {OUT/'pages'} for blind labelling")


if __name__ == "__main__":
    in_sample()
    holdout(sys.argv[1] if len(sys.argv) > 1 else "corpus/arxiv_holdout")
