# /// script
# requires-python = ">=3.10"
# ///
"""Merge the per-labeller TSVs and score them. No PDF work; pure arithmetic.

    uv run eval/nofigure_score.py --merge     # write eval/nofigure/labels.tsv
    uv run eval/nofigure_score.py             # print the tables

Every column is read by NAME, never by index. `strokegrid_holdout_score.py`
read the label by position, picked up `page` instead, and reported 0%
precision on a set that is unanimously `none`; that bug is the reason this
file exists as its own script rather than as a paragraph of pandas somewhere.

Merge rule: majority of the three independent labels. A three-way split
cannot happen with four labels and three labellers unless all three differ,
in which case the tie is broken IN THE BRANCH'S FAVOUR - `figure` over
`table` over `branding` over `none` - which is the same instruction the
labellers were given, so the merge cannot manufacture waste that no labeller
saw.

`agree` is how many of the three labellers gave the merged label.
"""
import collections
import json
import math
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "eval" / "nofigure"
# most generous first: a tie is broken towards the branch being right
ORDER = ["figure", "table", "branding", "none"]
REAL = {"figure", "table"}
PANEL = 3          # independent labellers per tag; enforced, not assumed


def read_tsv(path):
    lines = [l for l in path.read_text().splitlines() if l.strip()]
    head = lines[0].split("\t")
    return [dict(zip(head, l.split("\t"))) for l in lines[1:]]


def wilson(k, n, z=1.96):
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - h), min(1.0, c + h))


def merge():
    index = {r["tag"]: r for r in json.loads((OUT / "index.json").read_text())["rows"]}
    files = sorted(OUT.glob("labels-*.tsv"))
    if not files:
        raise SystemExit("no eval/nofigure/labels-*.tsv to merge")
    votes = collections.defaultdict(list)
    notes = collections.defaultdict(list)
    for f in files:
        for r in read_tsv(f):
            lab = r["label"].strip()
            if lab not in ORDER:
                raise SystemExit(f"{f.name}: tag {r['tag']} has bad label {lab!r}")
            votes[r["tag"]].append(lab)
            notes[r["tag"]].append(r.get("note", "").strip())
    missing = sorted(set(index) - set(votes))
    if missing:
        raise SystemExit(f"{len(missing)} tags unlabelled: {missing[:8]}")
    extra = sorted(set(votes) - set(index))
    if extra:
        raise SystemExit(f"{len(extra)} tags not in index.json: {extra[:8]}")
    # Every tag must carry the full panel. A labeller wrote 28 rows for a
    # 30-row batch and REPORTED 30; without this the two short tags merged on
    # two votes and the only trace was a `2/2` in the agreement column, which
    # reads like a design choice rather than a defect.
    short = {t: v for t, v in votes.items() if len(v) != PANEL}
    if short:
        raise SystemExit(
            f"{len(short)} tags do not have exactly {PANEL} labels: "
            + ", ".join(f"{t}={len(v)}" for t, v in sorted(short.items())[:10]))

    rows = ["\t".join(["tag", "corpus", "file", "page", "branch", "label",
                       "agree", "note"])]
    for tag in sorted(votes):
        v = votes[tag]
        c = collections.Counter(v)
        top = max(c.values())
        lab = min((l for l in c if c[l] == top), key=ORDER.index)
        i = index[tag]
        note = next((n for l, n in zip(v, notes[tag]) if l == lab and n), "")
        rows.append("\t".join([tag, i["corpus"], i["file"], str(i["page"]),
                               i["branch"], lab, f"{top}/{len(v)}", note]))
    (OUT / "labels.tsv").write_text("\n".join(rows) + "\n")
    print(f"merged {len(files)} labeller files -> {OUT / 'labels.tsv'} "
          f"({len(votes)} tags)")


def score():
    labels = {r["tag"]: r for r in read_tsv(OUT / "labels.tsv")}
    index = {r["tag"]: r for r in json.loads((OUT / "index.json").read_text())["rows"]}
    pop = json.loads((OUT / "firings.json").read_text())

    def table(rows, key, title):
        print(f"\n{title}")
        print(f"| {key} | " + " | ".join(ORDER) + " | n | waste |")
        print("|---|" + "--:|" * (len(ORDER) + 2))
        groups = collections.defaultdict(list)
        for t, r in rows:
            groups[r[key] if key in r else index[t][key]].append(t)
        for g in sorted(groups):
            c = collections.Counter(labels[t]["label"] for t in groups[g])
            n = len(groups[g])
            w = sum(c[l] for l in ORDER if l not in REAL)
            lo, hi = wilson(w, n)
            print(f"| {g} | " + " | ".join(str(c[l]) for l in ORDER)
                  + f" | {n} | {w / n * 100:.0f}% ({lo * 100:.0f}-{hi * 100:.0f}) |")

    rows = [(t, labels[t]) for t in sorted(labels)]
    print(f"labelled: {len(rows)}  of population {pop['n_firings']}")
    print("agreement: " + str(dict(collections.Counter(
        r["agree"] for _, r in rows))))
    table(rows, "branch", "By branch")
    for b in sorted({r["branch"] for _, r in rows}):
        table([(t, r) for t, r in rows if r["branch"] == b], "corpus",
              f"By corpus, branch={b}")

    print("\nPopulation-weighted waste (branch rates x population shares):")
    tot = pop["n_firings"]
    acc = 0.0
    for b in sorted({r["branch"] for _, r in rows}):
        sub = [t for t, r in rows if r["branch"] == b]
        w = sum(1 for t in sub if labels[t]["label"] not in REAL) / len(sub)
        share = sum(n for k, n in pop["by_branch_corpus"].items()
                    if k.startswith(b + "/")) / tot
        acc += w * share
        print(f"  {b:<15} rate {w * 100:5.1f}%  share {share * 100:5.1f}%")
    print(f"  weighted total waste: {acc * 100:.1f}% of "
          f"{tot} firings = {acc * tot:.0f} calls")


def holdout():
    """Merge and score the blind holdout labels, and print Wilson intervals.

    Each page was labelled by three labellers who saw the PNG and nothing
    else - not the rule, not the hypothesis, not which answer is convenient -
    and were told to break every tie AGAINST `none`.
    """
    H = OUT / "holdout"
    groups = {"pmc_holdout": sorted(H.glob("labels-[0-9]*.tsv")),
              "arxiv_holdout": sorted(H.glob("labels-[abc][0-9]*.tsv"))}
    merged = ["\t".join(["tag", "corpus", "file", "page", "label", "agree",
                         "note"])]
    for corpus, files in groups.items():
        if not files:
            continue
        idx = {c["tag"]: c for c in
               json.loads((H / f"index-{corpus}.json").read_text())["candidates"]}
        votes, notes = collections.defaultdict(list), collections.defaultdict(list)
        for f in files:
            for r in read_tsv(f):
                lab = r["label"].strip()
                if lab not in ORDER:
                    raise SystemExit(f"{f.name}: {r['tag']} bad label {lab!r}")
                votes[r["tag"]].append(lab)
                notes[r["tag"]].append(r.get("note", "").strip())
        short = {t: len(v) for t, v in votes.items() if len(v) != PANEL}
        if short:
            raise SystemExit(f"{corpus}: {len(short)} tags not labelled "
                             f"{PANEL} times: {sorted(short.items())[:8]}")
        real = 0
        for tag in sorted(votes):
            c = collections.Counter(votes[tag])
            top = max(c.values())
            lab = min((l for l in c if c[l] == top), key=ORDER.index)
            if lab in REAL:
                real += 1
            note = next((n for l, n in zip(votes[tag], notes[tag])
                         if l == lab and n), "")
            i = idx[tag]
            merged.append("\t".join([tag, corpus, i["file"], str(i["page"]),
                                     lab, f"{top}/{len(votes[tag])}", note]))
        n = len(votes)
        lo, hi = wilson(n - real, n)
        pop = json.loads((H / f"index-{corpus}.json").read_text())
        print(f"\n{corpus}: rule dropped {pop['n_dropped']} of "
              f"{pop['whole_document_calls']} whole_document calls "
              f"({pop['vision_calls']} total)")
        print(f"  labelled {n}"
              + ("" if n == pop["n_dropped"] else f" (sampled from {pop['n_dropped']})"))
        print(f"  real items in the drop set: {real}")
        print(f"  precision {100 * (n - real) / n:.0f}%  "
              f"95% Wilson {100 * lo:.0f}-{100 * hi:.0f}%")
        print("  agreement " + str(dict(collections.Counter(
            f"{max(collections.Counter(v).values())}/{len(v)}"
            for v in votes.values()))))
    (H / "labels.tsv").write_text("\n".join(merged) + "\n")
    print(f"\nwrote {H / 'labels.tsv'} ({len(merged) - 1} rows)")


if __name__ == "__main__":
    if "--merge" in sys.argv[1:]:
        merge()
    elif "--holdout" in sys.argv[1:]:
        holdout()
    else:
        score()
