# /// script
# requires-python = ">=3.10"
# dependencies = ["pdf-inspector==0.2.6", "pymupdf==1.28.0"]
# ///
"""How many documents did `drop_textonly` push below SCALE_GUARD?

`over_scale_guard` is the only routing number a user ever sees before the
vision calls happen: when it is true the skill stops and asks. `drop_textonly`
removed 272 page renders across the design corpora, and nobody counted how many
documents that moved across the threshold.

For every PDF in the twelve corpora this records, per document:

    calls_after   what harvest() ships today
    n_textonly    page renders drop_textonly removed from THIS document
    calls_before  calls_after + n_textonly, i.e. the pre-rule routed set

`drop_textonly` is the last mutation harvest() makes to `items` -- it runs
after `cost_guard` and nothing follows it -- so `calls_before` is exact, not
modelled. `--recheck` proves that independently by monkeypatching
`harvest.drop_textonly` to a no-op and re-harvesting, which must reproduce
`calls_before` for every document.

    uv run eval/scaleguard.py            # measure, write eval/scaleguard/flips.json
    uv run eval/scaleguard.py --recheck  # re-harvest with the rule disabled
    uv run eval/scaleguard.py --batch    # same question at harvest_batch scope
    uv run eval/scaleguard.py --detail   # what the flipped documents still route

`convert.py` -- the path a user actually runs -- calls `harvest()` on one
document, never `harvest_batch()`, so the per-document numbers are the ones a
user sees. `--batch` re-does the count with `drop_batch_furniture` applied, as
`eval/bench.py` does; the two differ only where a cross-document emblem exists
(bills, datasheets).
"""
import collections, concurrent.futures as cf, json, os, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills" / "doc-extract"))
import harvest as H

CORPORA = ["arxiv", "bills", "datasheets", "olmocr_arxiv_math",
           "olmocr_headers_footers", "olmocr_long_tiny_text",
           "olmocr_multi_column", "olmocr_scans", "olmocr_tables",
           "papers", "pmc", "tds"]
OUT = ROOT / "eval" / "scaleguard"


def _row(args):
    corpus, path = args
    r = H.harvest(str(path))
    if r["status"] != "ok":
        return {"corpus": corpus, "name": path.name, "skip": r.get("error")}
    n_to = sum(1 for d in r["dropped"] if d.get("why") == "textonly_page")
    return {"corpus": corpus, "name": path.name, "pages": r["pages"],
            "calls_after": r["vision_calls"], "n_textonly": n_to,
            "collapsed": any(d.get("why") == "cost_guard" for d in r["dropped"]),
            "guard_after": r["over_scale_guard"]}


def _row_nodrop(args):
    corpus, path = args
    H.drop_textonly = lambda items, *a, **k: (items, [])
    r = H.harvest(str(path))
    if r["status"] != "ok":
        return {"corpus": corpus, "name": path.name, "skip": r.get("error")}
    return {"corpus": corpus, "name": path.name, "calls_nodrop": r["vision_calls"]}


def _full(args):
    """Whole harvest result, minus the text, for batch-scope re-scoring."""
    corpus, path, nodrop = args
    if nodrop:
        H.drop_textonly = lambda items, *a, **k: (items, [])
    r = H.harvest(str(path))
    for k in ("markdown", "page_markdown"):
        r.pop(k, None)
    r["corpus"] = corpus
    r["name"] = path.name
    return r


def _detail(args):
    corpus, path = args
    r = H.harvest(str(path))
    return {"corpus": corpus, "name": path.name, "pages": r["pages"],
            "gone": [d["page"] for d in r["dropped"]
                     if d.get("why") == "textonly_page"],
            "kept": sorted((it["page"], it["reason"], it["kind"])
                           for it in r["items"])}


def run(fn, jobs):
    with cf.ProcessPoolExecutor(max_workers=os.cpu_count()) as ex:
        return list(ex.map(fn, jobs, chunksize=4))


def main(argv):
    jobs = [(c, p) for c in CORPORA
            for p in sorted((ROOT / "corpus" / c).glob("*.pdf"))]
    print(f"{len(jobs)} PDFs across {len(CORPORA)} corpora", file=sys.stderr)

    if "--recheck" in argv:
        rows = {r["name"]: r for r in json.loads(
            (OUT / "flips.json").read_text())["rows"]}
        # only documents the rule touched can disagree; check every one of them
        todo = [(c, p) for c, p in jobs
                if rows.get(p.name, {}).get("n_textonly", 0)]
        print(f"re-harvesting {len(todo)} documents with drop_textonly disabled",
              file=sys.stderr)
        bad = 0
        for r in run(_row_nodrop, todo):
            want = rows[r["name"]]["calls_after"] + rows[r["name"]]["n_textonly"]
            if r.get("calls_nodrop") != want:
                bad += 1
                print(f"  MISMATCH {r['name']}: {r.get('calls_nodrop')} != {want}")
        print(f"recheck: {len(todo)} documents, {bad} mismatches")
        return

    if "--batch" in argv:
        # batch_furniture only ever fires where an emblem recurs across >50% of
        # a corpus's documents; everywhere else harvest_batch == harvest, and
        # eval/bench.py's per-corpus totals confirm which those are.
        for corpus in ("bills", "datasheets"):
            paths = sorted((ROOT / "corpus" / corpus).glob("*.pdf"))
            out = {}
            for nodrop in (False, True):
                res = run(_full, [(corpus, p, nodrop) for p in paths])
                res = H.drop_batch_furniture(res, H.batch_furniture(res))
                out[nodrop] = {r["name"]: r for r in res if r["status"] == "ok"}
            names = sorted(out[False])
            flips = [n for n in names
                     if out[True][n]["over_scale_guard"]
                     and not out[False][n]["over_scale_guard"]]
            print(f"{corpus}: {len(names)} documents, "
                  f"over guard {sum(1 for n in names if out[True][n]['over_scale_guard'])}"
                  f" -> {sum(1 for n in names if out[False][n]['over_scale_guard'])}, "
                  f"FLIPPED {len(flips)}")
            for n in flips:
                print(f"  {n}: {out[True][n]['vision_calls']} -> "
                      f"{out[False][n]['vision_calls']}")
        return

    if "--detail" in argv:
        rows = {r["name"]: r for r in json.loads(
            (OUT / "flips.json").read_text())["rows"]}
        G = H.SCALE_GUARD
        flip = {n for n, r in rows.items() if "skip" not in r
                and r["calls_after"] + r["n_textonly"] > G and r["calls_after"] <= G}
        for r in run(_detail, [(c, p) for c, p in jobs if p.name in flip]):
            kinds = collections.Counter(k[1] for k in r["kept"])
            print(f"{r['corpus']}/{r['name']}  pages={r['pages']}  "
                  f"now {len(r['kept'])} calls {dict(kinds)}")
            print(f"   dropped as text-only: {r['gone']}")
            print(f"   still routed        : {[k[0] for k in r['kept']]}")
        return

    rows = run(_row, jobs)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "flips.json").write_text(json.dumps(
        {"scale_guard": H.SCALE_GUARD, "corpora": CORPORA, "rows": rows},
        indent=1) + "\n")

    ok = [r for r in rows if "skip" not in r]
    G = H.SCALE_GUARD
    flips = [r for r in ok
             if r["calls_after"] + r["n_textonly"] > G and r["calls_after"] <= G]
    print(f"documents           {len(ok)} ({len(rows) - len(ok)} skipped)")
    print(f"renders removed     {sum(r['n_textonly'] for r in ok)}")
    print(f"touched by the rule {sum(1 for r in ok if r['n_textonly'])}")
    print(f"over guard before   {sum(1 for r in ok if r['calls_after'] + r['n_textonly'] > G)}")
    print(f"over guard after    {sum(1 for r in ok if r['calls_after'] > G)}")
    print(f"FLIPPED             {len(flips)}")
    for r in sorted(flips, key=lambda r: -r["n_textonly"]):
        print(f"  {r['corpus']}/{r['name']}  pages={r['pages']} "
              f"{r['calls_after'] + r['n_textonly']} -> {r['calls_after']}")
    by = collections.Counter(r["corpus"] for r in flips)
    print("by corpus:", dict(by))


if __name__ == "__main__":
    main(sys.argv)
