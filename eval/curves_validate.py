# /// script
# requires-python = ">=3.10"
# dependencies = ["pdf-inspector==0.2.6", "pymupdf==1.28.0"]
# ///
"""Apply the candidate `curves` rule to a corpus, render its drops, price it.

The rule, read off `eval/nofigure/labels.tsv` and therefore in-sample there:

    drop a `curves` firing whose largest SPATIALLY CONNECTED stroke cluster
    covers at most CURVES_CLUSTER (0.05) of the page and whose page text
    carries no figure caption.

In-sample: 17 firings cut, all 17 labelled `branding`, 0 real items lost.
`eval/rejected-signals.md` declined to ship it on three counts, one of which -
"it is read off the set it would be validated on, and the two holdouts are the
wrong kind because it targets VENDOR boilerplate" - is what this script and
`corpus/datasheet_holdout` exist to answer.

    uv run eval/curves_validate.py                      # corpus/datasheet_holdout
    uv run eval/curves_validate.py corpus/datasheets    # in-sample re-check
    uv run eval/curves_validate.py --diff               # vs the patched pipeline

Two things this deliberately does NOT share with the proposed patch:

  * the cluster measure is reimplemented here from `fitz` primitives, in the
    plain quadratic form `eval/nofigure_features.py` used, with no early exit
    and no path cap. The patch needs those to stay off the hot path; if they
    ever changed an answer, `--diff` is what says so. The `boxed_text` rule's
    only known failure mode surfaced from exactly this comparison.
  * the firing set is counted AFTER `drop_batch_furniture` at corpus scope,
    the same batch scope `eval/nofigure_render.py` used, so the denominator
    here is comparable with the 2,770 in `eval/nofigure.md`.

The cascade question is the one a precision number cannot answer. Dropping a
`curves` page render un-subsumes any raster on that page, which comes back as
its own vision call - the cascade that forced the QR-code filter's revert
(`eval/tds-corpus.md`), and 2 of the 17 in-sample drops carry rasters. So each
document is harvested TWICE, shipped and patched, and the report is the real
per-document call delta with every added item named.
"""
import collections
import json
import pathlib
import re
import subprocess
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills" / "doc-extract"))
sys.path.insert(0, str(ROOT / "eval"))
import fitz                                                   # noqa: E402
from harvest import batch_furniture, drop_batch_furniture, harvest   # noqa: E402
import curves_patch                                           # noqa: E402

OUT = ROOT / "eval" / "curves_holdout"
PARTS = OUT / "parts"
DPI = 130
SHARDS = 6
CLUSTER_MAX = 0.05     # largest connected stroke cluster / page area
GAP = 24.0             # pt; stroke rects further apart are separate clusters
CAPTION = re.compile(r"\b(Fig(?:ure)?\.?|Table|Chart|Scheme|Plate)\s*\.?\s*\d",
                     re.I)


def cluster_frac(pg):
    """Largest connected group of stroke-path bounding boxes, over page area.

    Single-link on rect proximity, exactly as eval/nofigure_features.py
    computed it for the labelled set - written out again rather than imported
    so that this file and the patch are two independent statements of the same
    rule.
    """
    parea = max(1.0, pg.rect.width * pg.rect.height)
    rects = []
    for path in pg.get_cdrawings():
        x0, y0, x1, y1 = path["rect"]
        if (x1 - x0) * (y1 - y0) > parea * 0.90:
            continue                                # background tint
        if any(it[0] in ("c", "l") for it in path["items"]):
            rects.append([x0, y0, x1, y1])
    if not rects:
        return 0.0
    parent = list(range(len(rects)))

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    for i in range(len(rects)):
        for j in range(i + 1, len(rects)):
            a, b = rects[i], rects[j]
            if (a[0] - GAP <= b[2] and b[0] - GAP <= a[2]
                    and a[1] - GAP <= b[3] and b[1] - GAP <= a[3]):
                ra, rb = find(i), find(j)
                if ra != rb:
                    parent[ra] = rb
    groups = collections.defaultdict(list)
    for i in range(len(rects)):
        groups[find(i)].append(rects[i])
    best = 0.0
    for g in groups.values():
        x0 = min(r[0] for r in g); y0 = min(r[1] for r in g)
        x1 = max(r[2] for r in g); y1 = max(r[3] for r in g)
        best = max(best, (x1 - x0) * (y1 - y0) / parea)
    return round(best, 4)


# --------------------------------------------------------------------- shards
def run_shard(corpus, i, n):
    PARTS.mkdir(parents=True, exist_ok=True)
    patched = curves_patch.load()
    paths = sorted(pathlib.Path(corpus).glob("*.pdf"))[i::n]
    recs = []
    for p in paths:
        t0 = time.perf_counter()
        try:
            r = harvest(str(p))
        except Exception as e:
            recs.append({"file": p.name, "status": f"error {type(e).__name__}"})
            continue
        t1 = time.perf_counter()
        try:
            q = patched.harvest(str(p))
        except Exception as e:
            q = {"status": f"error {type(e).__name__}"}
        t2 = time.perf_counter()
        if r.get("status") != "ok":
            recs.append({"file": p.name, "status": r.get("status")})
            continue
        # per-page facts for every curves firing this document produces
        facts = {}
        curves = [it["page"] for it in r["items"] if it["reason"] == "curves"]
        if curves:
            with fitz.open(str(p)) as d:
                for pg_no in curves:
                    pg = d[pg_no - 1]
                    facts[str(pg_no)] = {
                        "cluster_frac": cluster_frac(pg),
                        "has_caption": bool(CAPTION.search(pg.get_text())),
                        "n_images": len(pg.get_images(full=True)),
                        "n_drawings": len(pg.get_cdrawings()),
                        "page_chars": len(pg.get_text().strip())}
        recs.append({
            "file": p.name, "status": "ok", "pages": r["pages"],
            "items": [{k: it[k] for k in ("id", "page", "kind", "reason")}
                      for it in r["items"]],
            "dropped": r["dropped"], "page_sigs": r["page_sigs"],
            "facts": facts,
            "patched_status": q.get("status"),
            "patched_sigs": q.get("page_sigs") or {},
            "patched_items": [{k: it[k] for k in ("id", "page", "kind", "reason")}
                              for it in (q.get("items") or [])],
            "patched_dropped": [d for d in (q.get("dropped") or [])
                                if d.get("why") == "vendor_curves"],
            "t_shipped": round(t1 - t0, 3), "t_patched": round(t2 - t1, 3)})
    (PARTS / f"shard{i}.json").write_text(json.dumps(recs))


def read_parts():
    recs = []
    for i in range(SHARDS):
        recs += json.loads((PARTS / f"shard{i}.json").read_text())
    recs.sort(key=lambda r: r["file"])
    return recs


def load_recs(corpus):
    PARTS.mkdir(parents=True, exist_ok=True)
    for f in PARTS.glob("shard*.json"):
        f.unlink()
    procs = [subprocess.Popen(
        [sys.executable, str(pathlib.Path(__file__).resolve()), corpus,
         "--shard", f"{i}/{SHARDS}"]) for i in range(SHARDS)]
    bad = [i for i, p in enumerate(procs) if p.wait() != 0]
    if bad:
        raise SystemExit(f"shards failed: {bad}")
    recs = []
    for i in range(SHARDS):
        recs += json.loads((PARTS / f"shard{i}.json").read_text())
    recs.sort(key=lambda r: r["file"])
    return recs


def batch_scope(recs, key_items, key_sigs="page_sigs"):
    """Apply the cross-document furniture rule at corpus scope, in place.

    Without this the `curves` denominator is not the one eval/nofigure.md
    reports, and on a single-vendor corpus it is the filter most likely to
    have taken the drop already.
    """
    shaped = [{"status": "ok", "path": r["file"], "items": r[key_items],
               "dropped": [], "page_sigs": r.get(key_sigs, {})}
              for r in recs if r["status"] == "ok"]
    drop_batch_furniture(shaped, batch_furniture(shaped))
    out = {}
    for s in shaped:
        out[s["path"]] = (s["items"], [d["page"] for d in s["dropped"]])
    return out


# ----------------------------------------------------------------------- main
def main(corpus):
    recs = load_recs(corpus)
    ok = [r for r in recs if r["status"] == "ok"]
    name = pathlib.Path(corpus).name
    OUT.mkdir(parents=True, exist_ok=True)

    ship = batch_scope(ok, "items")
    hits, kept = [], []
    for r in ok:
        items, bf = ship[r["file"]]
        for it in items:
            if it["reason"] != "curves":
                continue
            f = r["facts"].get(str(it["page"]))
            if f is None:
                continue
            row = {"file": r["file"], "page": it["page"], **f}
            (hits if (f["cluster_frac"] <= CLUSTER_MAX
                      and not f["has_caption"]) else kept).append(row)

    calls = sum(len(ship[r["file"]][0]) for r in ok)
    n_curves = len(hits) + len(kept)

    tag_of = {}
    (OUT / "pages").mkdir(parents=True, exist_ok=True)
    for i, h in enumerate(sorted(hits, key=lambda h: (h["file"], h["page"]))):
        tag = f"c{i + 1:03d}"
        tag_of[(h["file"], h["page"])] = tag
        with fitz.open(str(pathlib.Path(corpus) / h["file"])) as d:
            d[h["page"] - 1].get_pixmap(dpi=DPI).save(
                str(OUT / "pages" / f"{tag}.png"))

    # ---- cascade: the same corpus harvested with the rule actually in place
    pat = batch_scope([r for r in ok if r["patched_status"] == "ok"],
                      "patched_items", "patched_sigs")
    deltas, added = [], collections.Counter()
    added_rows = []
    for r in ok:
        if r["patched_status"] != "ok":
            continue
        a = {it["id"]: it for it in ship[r["file"]][0]}
        b = {it["id"]: it for it in pat[r["file"]][0]}
        d = len(b) - len(a)
        new = [b[k] for k in b.keys() - a.keys()]
        for it in new:
            added[it["reason"]] += 1
            added_rows.append({"file": r["file"], **it})
        if d or new:
            deltas.append({"file": r["file"], "before": len(a), "after": len(b),
                           "delta": d, "added": [it["id"] for it in new]})

    index = {
        "rule": f"curves firing with largest stroke cluster <= {CLUSTER_MAX} "
                "of the page and no figure caption in the page text",
        "corpus": corpus, "dpi": DPI,
        "documents": len(recs), "ok": len(ok),
        "vision_calls": calls, "curves_firings": n_curves,
        "n_dropped": len(hits),
        "documents_hit": len({h["file"] for h in hits}),
        "drops_with_raster": sum(1 for h in hits if h["n_images"]),
        "patched_ok": sum(1 for r in ok if r["patched_status"] == "ok"),
        "calls_after_patch": sum(len(pat[r["file"]][0]) for r in ok
                                 if r["patched_status"] == "ok"),
        "calls_before_patch": sum(len(ship[r["file"]][0]) for r in ok
                                  if r["patched_status"] == "ok"),
        "added_items": dict(added), "added_rows": added_rows,
        "documents_changed": deltas,
        "t_shipped": round(sum(r["t_shipped"] for r in ok), 1),
        "t_patched": round(sum(r["t_patched"] for r in ok), 1),
        "candidates": [{"tag": tag_of[(h["file"], h["page"])], **h}
                       for h in sorted(hits, key=lambda h: (h["file"], h["page"]))],
        "kept": kept,
    }
    (OUT / f"index-{name}.json").write_text(json.dumps(index, indent=1))

    print(f"corpus            : {corpus}")
    print(f"documents ok      : {len(ok)}/{len(recs)}")
    print(f"vision calls      : {calls}")
    print(f"curves firings    : {n_curves}")
    print(f"rule drops        : {len(hits)}  "
          f"({index['documents_hit']} documents, "
          f"{index['drops_with_raster']} carrying a raster)")
    print(f"calls with rule   : {index['calls_before_patch']} -> "
          f"{index['calls_after_patch']}  "
          f"({index['calls_after_patch'] - index['calls_before_patch']:+d})")
    print(f"items ADDED       : {dict(added) or 'none'}")
    print(f"harvest wall      : shipped {index['t_shipped']}s  "
          f"patched {index['t_patched']}s")
    print(f"rendered to {OUT / 'pages'} for labelling")


def sample(corpus, budget=120, seed=20260813):
    """Draw the labelling batch, and say what is NOT in it.

    Every drop is labelled when the drop set fits the budget; above it the
    population is SAMPLED, never truncated, with a fixed seed - the same
    convention as `eval/nofigure/holdout/arxiv-sample.json`, which sampled 90
    of 320.
    """
    import random
    name = pathlib.Path(corpus).name
    idx = json.loads((OUT / f"index-{name}.json").read_text())
    tags = [c["tag"] for c in idx["candidates"]]
    drawn = (sorted(tags) if len(tags) <= budget
             else sorted(random.Random(seed).sample(sorted(tags), budget)))
    (OUT / "sample.json").write_text(json.dumps(
        {"corpus": corpus, "population": len(tags), "budget": budget,
         "seed": seed, "not_labelled": len(tags) - len(drawn),
         "tags": drawn}, indent=1))
    # split into batches of BATCH so no labeller has to hold 120 pages at once
    BATCH = 30
    n = 0
    for n, i in enumerate(range(0, len(drawn), BATCH), start=1):
        (OUT / f"batch{n}.tsv").write_text(
            "tag\n" + "\n".join(drawn[i:i + BATCH]) + "\n")
    print(f"population {len(tags)}  drawn {len(drawn)}  "
          f"not labelled {len(tags) - len(drawn)}")
    print(f"wrote {n} batch files to {OUT}")


def diff(corpus):
    """This script's drop set against what the patched pipeline really drops."""
    name = pathlib.Path(corpus).name
    idx = json.loads((OUT / f"index-{name}.json").read_text())
    want = {(c["file"], c["page"]) for c in idx["candidates"]}
    got = set()
    for r in read_parts():
        if r["status"] != "ok":
            continue
        for d in r.get("patched_dropped", []):
            got.add((r["file"], d["page"]))
    only_script = sorted(want - got)
    only_ship = sorted(got - want)
    print(f"analysis script : {len(want)}")
    print(f"patched harvest : {len(got)}")
    print(f"only in script  : {len(only_script)} {only_script[:10]}")
    print(f"only in patched : {len(only_ship)} {only_ship[:10]}")
    return 1 if (only_script or only_ship) else 0


if __name__ == "__main__":
    argv = sys.argv[1:]
    target = next((a for a in argv if not a.startswith("--")),
                  "corpus/datasheet_holdout")
    if "--shard" in argv:
        i, n = argv[argv.index("--shard") + 1].split("/")
        run_shard(target, int(i), int(n))
    elif "--diff" in argv:
        raise SystemExit(diff(target))
    elif "--sample" in argv:
        sample(target)
    else:
        main(target)
