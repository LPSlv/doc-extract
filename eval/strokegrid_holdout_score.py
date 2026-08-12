# /// script
# requires-python = ">=3.10"
# ///
"""Score blind holdout labels against the in-sample claim of 95% precision.

Reads eval/strokegrid/holdout/index.json (what the rule dropped) and
eval/strokegrid/holdout/labels.tsv (what those pages actually were, labelled
blind from the PNGs alone). A drop is CORRECT when the page carries no table,
no plot and no figure; anything else is a real item the rule destroyed.

Precision here is the only number that decides shipping. Recall cannot be
computed on the holdout without labelling every firing, which is not the
question - the question is whether the drops are safe.

    uv run eval/strokegrid_holdout_score.py
"""
import collections, json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
H = ROOT / "eval" / "strokegrid" / "holdout"


def main():
    idx = json.loads((H / "index.json").read_text())
    # Read the label by COLUMN NAME. Positional indexing read `page` as the
    # label the first time this ran and reported 0% precision on a set that is
    # unanimously `none`.
    lines = (H / "labels.tsv").read_text().strip().splitlines()
    head = lines[0].split("\t")
    ti, li = head.index("tag"), head.index("label")
    rows = [l.split("\t") for l in lines[1:]]
    labels = {r[ti]: r[li].strip() for r in rows if len(r) > li}

    drops = idx["candidates"]
    missing = [d["tag"] for d in drops if d["tag"] not in labels]
    if missing:
        sys.exit(f"unlabelled: {' '.join(missing)}")

    print(f"corpus            : {idx['corpus']} ({idx['n_docs']} documents)")
    print(f"stroke_grid fires : {idx['n_firings']}")

    # Two populations, and the difference matters. index.json holds the drops
    # this script found by scoring harvest's ITEM list, which is post-
    # cost_guard - so a firing inside a document that cost_guard collapses into
    # whole-page renders never appears there. Those pages are dropped by the
    # shipped rule and then rendered anyway, so they change nothing; but one of
    # them was a real table, and reporting only the effective set would hide it.
    eff = {d["tag"] for d in drops}
    for title, tags in (("effective (change what ships)", eff),
                        ("all firings of the rule", set(labels))):
        n = collections.Counter(labels[t] for t in tags)
        good, tot = n["none"], len(tags)
        lo, hi = _wilson(good, tot)
        detail = ", ".join(f"{k} {n[k]}" for k in ("none", "table", "plot", "figure")
                           if n[k])
        print(f"\n{title}: {tot} drops   [{detail}]")
        print(f"  real items lost : {tot - good}")
        print(f"  PRECISION       : {good/tot*100:.0f}%"
              f"   (95% CI {lo*100:.0f}-{hi*100:.0f}%; in-sample claim 95%)")


def _wilson(k, n, z=1.96):
    if not n:
        return (float("nan"), float("nan"))
    p, d = k / n, 1 + z * z / n
    c = p + z * z / (2 * n)
    s = z * ((p * (1 - p) / n + z * z / (4 * n * n)) ** 0.5)
    return ((c - s) / d, (c + s) / d)


if __name__ == "__main__":
    main()
