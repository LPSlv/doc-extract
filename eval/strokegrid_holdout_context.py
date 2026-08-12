# /// script
# requires-python = ">=3.10"
# dependencies = ["pdf-inspector==0.2.6", "pymupdf==1.28.0"]
# ///
"""How many vision calls does the holdout make, and what share would the rule cut?

A precision number decides whether a rule is SAFE. It does not decide whether
the rule is WORTH SHIPPING - that needs the denominator. This prints the
routed-item histogram for a corpus so the drop count can be read as a share of
total calls rather than as a bare integer.

    uv run eval/strokegrid_holdout_context.py corpus/arxiv_holdout
"""
import collections, json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills" / "doc-extract"))
from harvest import harvest_batch


def main(corpus):
    paths = sorted(pathlib.Path(corpus).glob("*.pdf"))
    res = harvest_batch([str(p) for p in paths])
    hist = collections.Counter()
    pages = 0
    for p, r in zip(paths, res):
        if r.get("status") != "ok":
            continue
        pages += r.get("pages") or 0
        for it in (r.get("items") or []):
            hist[it["reason"]] += 1

    total = sum(hist.values())
    print(f"documents   : {len(paths)}")
    print(f"pages       : {pages}")
    print(f"vision calls: {total}")
    for k, v in hist.most_common():
        print(f"  {k:<18}: {v:>5}  ({v/total*100:.1f}%)")

    (ROOT / "eval" / "strokegrid" / "holdout" / "context.json").write_text(
        json.dumps({"corpus": corpus, "docs": len(paths), "pages": pages,
                    "calls": total, "by_reason": dict(hist)}, indent=1))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "corpus/arxiv_holdout")
