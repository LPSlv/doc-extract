# /// script
# requires-python = ">=3.10"
# ///
"""Merge the blind labels for the datasheet-holdout run and score them.

Same shape as `eval/filter3.py score` / `eval/curves_score.py`, and the same
two refusals, because both have caught something here before:

  * every column is read BY NAME, never by position. A scorer that read the
    `page` column as the label once reported 0% on a set that was unanimously
    clean (`docs/NEXT.md`).
  * the merge refuses to proceed unless every tag carries exactly three labels
    from three distinct labellers, and unless every label is in the vocabulary.

Precision here is "the rule was RIGHT to route this page", i.e. the page
carries a real `figure`. That is the same direction `eval/filter3.md` scores
its holdout in, so the numbers are directly comparable.

    uv run eval/filter3_ds_score.py
"""
import collections
import csv
import json
import math
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "eval" / "filter3" / "datasheet_holdout"
RAW = OUT / "raw"
LABELS = {"figure", "table", "branding", "none"}
NLAB = 3


def wilson(k, n, z=1.96):
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - h), min(1.0, c + h))


def read_tsv(path):
    with open(path, newline="") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def merge():
    sample = json.loads((OUT / "sample.json").read_text())
    facts = {r["tag"]: r for r in sample["rows"]}
    byl = {}
    for n in (1, 2, 3):
        rows = []
        for f in sorted(RAW.glob(f"L{n}-b*.tsv")):
            for r in read_tsv(f):
                tag = (r.get("tag") or "").strip()
                lab = (r.get("label") or "").strip().lower()
                if not tag:
                    continue
                if lab not in LABELS:
                    raise SystemExit(f"{f}: tag {tag} label {lab!r} not in "
                                     f"{sorted(LABELS)}")
                rows.append({"tag": tag, "label": lab,
                             "note": (r.get("note") or "").strip()})
        seen = collections.Counter(r["tag"] for r in rows)
        dup = [t for t, c in seen.items() if c > 1]
        if dup:
            raise SystemExit(f"labeller {n}: duplicate tags {dup[:10]}")
        byl[n] = {r["tag"]: r for r in rows}
        (OUT / f"labels-{n}.tsv").write_text(
            "tag\tlabel\tnote\n"
            + "".join(f"{r['tag']}\t{r['label']}\t{r['note']}\n"
                      for r in sorted(rows, key=lambda r: r["tag"])))

    tags = sorted(facts)
    missing = [t for t in tags for n in (1, 2, 3) if t not in byl[n]]
    if missing:
        raise SystemExit(f"{len(missing)} tag/labeller cells missing: "
                         f"{sorted(set(missing))[:10]}")
    extra = sorted(set().union(*(set(byl[n]) for n in (1, 2, 3))) - set(tags))
    if extra:
        raise SystemExit(f"labels for tags not in the sample: {extra[:10]}")

    merged = []
    for t in tags:
        votes = [byl[n][t]["label"] for n in (1, 2, 3)]
        if len(votes) != NLAB:
            raise SystemExit(f"{t}: {len(votes)} labels, want {NLAB}")
        c = collections.Counter(votes)
        lab, k = c.most_common(1)[0]
        f = facts[t]
        merged.append({"tag": t, "corpus": f.get("corpus", "datasheet_holdout"),
                       "vendor": f["vendor"], "file": f["file"],
                       "page": f["page"], "branch": f["reason"],
                       "pipe_rows": f.get("pipe_rows"),
                       "label": lab, "agree": f"{k}/{NLAB}",
                       "votes": "|".join(votes),
                       "note": byl[1][t]["note"]})
    hdr = ("tag\tcorpus\tvendor\tfile\tpage\tbranch\tpipe_rows\tlabel\tagree\t"
           "votes\tnote\n")
    (OUT / "labels.tsv").write_text(hdr + "".join(
        "\t".join(str(m[k]) for k in ("tag", "corpus", "vendor", "file", "page",
                                      "branch", "pipe_rows", "label", "agree",
                                      "votes", "note")) + "\n"
        for m in merged))
    return merged


def pct(k, n):
    if n == 0:
        return "     -"
    lo, hi = wilson(k, n)
    return f"{k/n*100:3.0f}% ({lo*100:.0f}-{hi*100:.0f})"


def table(rows, key, title):
    print(f"\n{title}")
    print(f"{'':<16}{'none':>6}{'brand':>6}{'table':>6}{'figure':>7}{'n':>5}"
          f"   carries a figure")
    groups = collections.defaultdict(list)
    for r in rows:
        groups[r[key]].append(r)
    for g in sorted(groups, key=lambda g: -len(groups[g])):
        rs = groups[g]
        c = collections.Counter(r["label"] for r in rs)
        k = c["figure"]
        print(f"{str(g):<16}{c['none']:>6}{c['branding']:>6}{c['table']:>6}"
              f"{k:>7}{len(rs):>5}   {pct(k, len(rs))}")


def main():
    merged = merge()
    n = len(merged)
    c = collections.Counter(r["label"] for r in merged)
    k = c["figure"]
    unan = sum(1 for r in merged if r["agree"] == f"{NLAB}/{NLAB}")
    print(f"labelled            : {n}")
    print(f"unanimous {NLAB}/{NLAB}       : {unan}  "
          f"({n - unan} split)")
    print(f"label counts        : {dict(c.most_common())}")
    print(f"PRECISION (figure)  : {pct(k, n)}")
    table(merged, "vendor", "By vendor")
    table(merged, "branch", "By branch")
    table(merged, "corpus", "By corpus")
    if any(r["agree"] != f"{NLAB}/{NLAB}" for r in merged):
        print("\nSplits:")
        for r in merged:
            if r["agree"] != f"{NLAB}/{NLAB}":
                print(f"  {r['tag']} {r['file']} p{r['page']} "
                      f"{r['votes']} -> {r['label']}  {r['note']}")
    print(f"\nwrote {OUT/'labels.tsv'} and labels-1..3.tsv")


if __name__ == "__main__":
    sys.exit(main())
