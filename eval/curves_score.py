# /// script
# requires-python = ">=3.10"
# ///
"""Merge the blind labels for the `curves` holdout and score them.

    uv run eval/curves_score.py --merge    # write eval/curves_holdout/labels.tsv
    uv run eval/curves_score.py            # print the tables

Pure arithmetic; no PDF work. Every column is read by NAME. Reading the label
by position is the defect that made `strokegrid_holdout_score.py` report 0%
precision on a unanimously clean set, and it is the reason this is a script of
its own rather than a paragraph somewhere.

Merge rule: majority of three independent labels, ties broken IN THE BRANCH'S
FAVOUR - `figure` over `table` over `branding` over `none` - the same
instruction the labellers were given, so the merge cannot manufacture waste
that no labeller saw. A tag that does not carry exactly PANEL labels aborts
the merge; a labeller once wrote 28 rows for a 30-row batch and reported 30.

Precision here is (drops that are NOT a real item) / (drops labelled), i.e.
the fraction of the rule's drops that threw away nothing. `figure` and `table`
are real items; `branding` and `none` are not.
"""
import collections
import json
import math
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "eval" / "curves_holdout"
ORDER = ["figure", "table", "branding", "none"]     # most generous first
REAL = {"figure", "table"}
PANEL = 3


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


def index(corpus="datasheet_holdout"):
    return json.loads((OUT / f"index-{corpus}.json").read_text())


def merge(corpus="datasheet_holdout"):
    idx = {c["tag"]: c for c in index(corpus)["candidates"]}
    smp = OUT / "sample.json"
    if smp.exists():                     # labelling budget: sampled, not truncated
        want = set(json.loads(smp.read_text())["tags"])
        idx = {t: c for t, c in idx.items() if t in want}
    files = sorted(OUT.glob("labels-*.tsv"))
    if not files:
        raise SystemExit("no eval/curves_holdout/labels-*.tsv to merge")
    votes, notes = collections.defaultdict(list), collections.defaultdict(list)
    for f in files:
        for r in read_tsv(f):
            lab = r["label"].strip()
            if lab not in ORDER:
                raise SystemExit(f"{f.name}: tag {r['tag']} bad label {lab!r}")
            votes[r["tag"]].append(lab)
            notes[r["tag"]].append(r.get("note", "").strip())
    missing = sorted(set(idx) - set(votes))
    if missing:
        raise SystemExit(f"{len(missing)} tags unlabelled: {missing[:8]}")
    extra = sorted(set(votes) - set(idx))
    if extra:
        raise SystemExit(f"{len(extra)} tags not in the index: {extra[:8]}")
    short = {t: len(v) for t, v in votes.items() if len(v) != PANEL}
    if short:
        raise SystemExit(f"{len(short)} tags without exactly {PANEL} labels: "
                         f"{sorted(short.items())[:10]}")
    rows = ["\t".join(["tag", "corpus", "file", "page", "vendor", "label",
                       "agree", "note"])]
    for tag in sorted(votes):
        v = votes[tag]
        c = collections.Counter(v)
        top = max(c.values())
        lab = min((l for l in c if c[l] == top), key=ORDER.index)
        note = next((n for l, n in zip(v, notes[tag]) if l == lab and n), "")
        i = idx[tag]
        rows.append("\t".join([tag, corpus, i["file"], str(i["page"]),
                               i["file"].split("_")[0], lab, f"{top}/{len(v)}",
                               note]))
    (OUT / "labels.tsv").write_text("\n".join(rows) + "\n")
    print(f"merged {len(files)} labeller files -> {OUT / 'labels.tsv'} "
          f"({len(votes)} tags)")


def score(corpus="datasheet_holdout"):
    rows = read_tsv(OUT / "labels.tsv")
    idx = index(corpus)
    n = len(rows)
    real = [r for r in rows if r["label"] in REAL]
    lo, hi = wilson(n - len(real), n)
    print(f"corpus            : {corpus}  ({idx['ok']} documents)")
    print(f"vision calls      : {idx['vision_calls']}")
    print(f"curves firings    : {idx['curves_firings']}")
    print(f"rule drops        : {idx['n_dropped']} "
          f"({idx['documents_hit']} documents)")
    smp = OUT / "sample.json"
    extra = ""
    if smp.exists():
        s = json.loads(smp.read_text())
        extra = (f" (sampled from {s['population']}, seed {s['seed']}, "
                 f"{s['not_labelled']} not labelled)")
    print(f"labelled          : {n}{extra}")
    print(f"real items lost   : {len(real)} "
          + (", ".join(f"{r['tag']}:{r['label']}" for r in real) if real else ""))
    print(f"precision         : {100 * (n - len(real)) / n:.0f}%  "
          f"95% Wilson {100 * lo:.0f}-{100 * hi:.0f}%")
    print("agreement         : " + str(dict(collections.Counter(
        r["agree"] for r in rows))))
    print("labels            : " + str(dict(collections.Counter(
        r["label"] for r in rows))))

    print("\nBy vendor (drops / label mix / precision):")
    print("| vendor | " + " | ".join(ORDER) + " | drops | precision |")
    print("|---|" + "--:|" * (len(ORDER) + 2))
    g = collections.defaultdict(list)
    for r in rows:
        g[r["vendor"]].append(r)
    for v in sorted(g, key=lambda v: -len(g[v])):
        c = collections.Counter(r["label"] for r in g[v])
        k = len(g[v]); bad = sum(c[l] for l in REAL)
        p_lo, p_hi = wilson(k - bad, k)
        print(f"| {v} | " + " | ".join(str(c[l]) for l in ORDER)
              + f" | {k} | {100 * (k - bad) / k:.0f}% "
                f"({100 * p_lo:.0f}-{100 * p_hi:.0f}) |")

    ti = [r for r in rows if r["vendor"] == "ti"]
    non = [r for r in rows if r["vendor"] != "ti"]
    for name, sub in (("TI only", ti), ("everything but TI", non)):
        if not sub:
            continue
        bad = sum(1 for r in sub if r["label"] in REAL)
        a, b = wilson(len(sub) - bad, len(sub))
        print(f"{name:<20} {len(sub) - bad}/{len(sub)} clean, precision "
              f"{100 * (len(sub) - bad) / len(sub):.0f}% "
              f"(95% Wilson {100 * a:.0f}-{100 * b:.0f})")

    print(f"\nCascade: {idx['calls_before_patch']} -> {idx['calls_after_patch']} "
          f"vision calls with the rule in the pipeline "
          f"({idx['calls_after_patch'] - idx['calls_before_patch']:+d})")
    print(f"  drops carrying a raster : {idx['drops_with_raster']}")
    print(f"  items ADDED by the rule : {idx['added_items'] or 'none'}")
    print(f"  harvest wall            : shipped {idx['t_shipped']}s -> "
          f"patched {idx['t_patched']}s")


if __name__ == "__main__":
    c = next((a for a in sys.argv[1:] if not a.startswith("--")),
             "datasheet_holdout")
    if "--merge" in sys.argv:
        merge(c)
    score(c)
