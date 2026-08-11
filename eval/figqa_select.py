# /// script
# requires-python = ">=3.10"
# dependencies = ["pdf-inspector==0.2.6", "pymupdf==1.28.0"]
# ///
"""Select figure-QA candidates mechanically, so the question set is not cherry-picked.

A candidate is a (document, page) where BOTH hold:

  1. the page carries real extractable text — so the text-only arm is not
     trivially empty, which is the failure mode that made `old_scans` a
     walkover (see eval/oldscans.md);
  2. harvest.py routes something on that page — so doc-extract has a figure
     to describe and the three arms actually differ.

Everything eligible is enumerated, then sampled with a fixed seed. The point
is that nobody chose which figures to be graded on.

    uv run eval/figqa_select.py corpus/datasheets corpus/papers --n 30

Writes eval/figqa/candidates.json and renders each page to
eval/figqa/pages/<id>.png at RENDER_DPI for ground-truth authoring.
"""
import json, pathlib, random, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills" / "doc-extract"))
import fitz, pdf_inspector as pi
from harvest import harvest_batch

OUT = ROOT / "eval" / "figqa"
RENDER_DPI = 200            # ground-truth authoring only; higher than the
                            # pipeline's own render, so the oracle is never
                            # worse-informed than the system under test
MIN_PAGE_CHARS = 400        # "real extractable text" on the figure's own page
SEED = 20260811


def eligible(paths):
    """Enumerate every (doc, page) meeting both conditions. No judgement."""
    out = []
    results = harvest_batch([str(p) for p in paths])
    for path, res in zip(paths, results):
        if res.get("status") != "ok":
            continue
        # harvest() calls them "items"; convert.py renames them "pending" for
        # its CLI output. Read the library's key, not the CLI's.
        pending = res.get("items") or []
        if not pending:
            continue
        try:
            with fitz.open(str(path)) as d:
                chars = {i + 1: len(pg.get_text().strip()) for i, pg in enumerate(d)}
                npages = len(d)
        except Exception:
            continue
        seen = set()
        for item in pending:
            pno = item.get("page")
            if not pno or pno in seen:
                continue
            if chars.get(pno, 0) < MIN_PAGE_CHARS:
                continue          # scanned/blank page: old_scans covers that case
            seen.add(pno)
            out.append({"doc": str(path), "name": path.name, "page": pno,
                        "pages": npages, "reason": item.get("reason"),
                        "kind": item.get("kind"), "page_chars": chars[pno]})
    return out


def main(dirs, n):
    paths = []
    for d in dirs:
        paths += sorted(pathlib.Path(d).glob("*.pdf"))
    print(f"scanning {len(paths)} documents…", file=sys.stderr)
    cands = eligible(paths)
    print(f"{len(cands)} eligible (doc,page) pairs", file=sys.stderr)

    # One question per document: 30 figures from 30 files generalises further
    # than 30 figures from 5 files, and stops a single figure-dense datasheet
    # from dominating the score.
    by_doc = {}
    for c in cands:
        by_doc.setdefault(c["doc"], []).append(c)
    rng = random.Random(SEED)
    docs = sorted(by_doc)
    rng.shuffle(docs)
    picked = [rng.choice(by_doc[d]) for d in docs[:n]]
    for i, c in enumerate(picked):
        c["id"] = f"q{i+1:02d}"

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "pages").mkdir(exist_ok=True)
    for c in picked:
        with fitz.open(c["doc"]) as d:
            pm = d[c["page"] - 1].get_pixmap(dpi=RENDER_DPI)
            pm.save(str(OUT / "pages" / f"{c['id']}.png"))
    meta = {"seed": SEED, "render_dpi": RENDER_DPI,
            "min_page_chars": MIN_PAGE_CHARS, "dirs": [str(d) for d in dirs],
            "documents_scanned": len(paths), "eligible_pairs": len(cands),
            "eligible_documents": len(by_doc), "selected": picked}
    (OUT / "candidates.json").write_text(json.dumps(meta, indent=1))
    print(f"wrote {len(picked)} candidates -> {OUT/'candidates.json'}")


if __name__ == "__main__":
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    n = int(sys.argv[sys.argv.index("--n") + 1]) if "--n" in sys.argv else 30
    main(a, n)
