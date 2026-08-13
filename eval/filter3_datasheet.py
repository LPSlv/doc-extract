# /// script
# requires-python = ">=3.10"
# dependencies = ["pdf-inspector==0.2.6", "pymupdf==1.28.0"]
# ///
"""The proposed `FILTER3_ROWS = 4` rule, run on `corpus/datasheet_holdout`.

`eval/filter3.md` ships its rule on two holdouts, `arxiv_holdout` (82%) and
`pmc_holdout` (11%), and says the weakness out loud: **324 of the 400
in-sample firings are datasheets and neither holdout is a datasheet corpus.**
`eval/curves-holdout.md` built the missing corpus afterwards -- 295 datasheets,
9,449 pages, eleven vendors, TI held to 9% of files, disjoint from
`corpus/datasheets` by filename and sha256. This runs the rule on it.

Method, deliberately the more expensive of the two available:

  * every document is harvested TWICE, shipped and patched, through
    `harvest()` itself -- not through a re-implementation of its page loop.
    `eval/filter3_patch.py` applies the exact text of
    `eval/filter3/proposed.patch` to `harvest.py`'s source and execs it, and
    `--verify` there asserts byte-identity with `patch(1)`'s output. So
    `cost_guard`, `grid_pages`, subsumption and `drop_textonly` are the real
    ones and their cascades are observed rather than argued.
  * `drop_batch_furniture` is then applied at CORPUS scope to both sides, the
    scope `harvest_batch` uses and the scope `eval/curves_validate.py` and
    `eval/filter3.py cost` both used, so the call counts are comparable with
    `eval/curves-holdout.md`'s 2,957.
  * the page-loop predicate is ALSO computed independently, from
    `eval/filter3.py`'s own `prefix()`, so `--diff` can say where the two
    disagree. `eval/curves-holdout.md` found nine such pages and both
    directions were facts about the pipeline rather than bugs; a clean diff
    would be a sign the two sides are not independent.

    uv run eval/filter3_datasheet.py                          # the holdout
    uv run eval/filter3_datasheet.py corpus/datasheets        # in-sample anchor
    uv run eval/filter3_datasheet.py --diff [corpus]
    uv run eval/filter3_datasheet.py --sample [corpus]        # draw + render
"""
import collections
import json
import pathlib
import subprocess
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills" / "doc-extract"))
sys.path.insert(0, str(ROOT / "eval"))
import fitz                                                        # noqa: E402
from harvest import (SCALE_GUARD, STROKE_MIN_FRAC, INK_MIN,        # noqa: E402
                     batch_furniture, drop_batch_furniture, harvest,
                     render_reason)
import filter3 as F3                                               # noqa: E402
import filter3_patch                                               # noqa: E402

OUT = ROOT / "eval" / "filter3" / "datasheet_holdout"
DPI = 130
SHARDS = 6
SEED = 20260813
LABEL_BUDGET = 150


NARROW = False          # set by --narrow; see filter3_patch.NARROW_HUNKS


def suffix():
    return "-narrow" if NARROW else ""


def parts_dir(corpus):
    return OUT / "parts" / (pathlib.Path(corpus).name + suffix())


def vendor_of(name):
    return name.split("_", 1)[0]


# --------------------------------------------------------------------- shard
def predicate_rows(ctx):
    """The pages the proposed rule newly exposes, at page-loop level.

    Written against `eval/filter3.py`'s `prefix()` so it is the same statement
    of the rule that produced `eval/filter3.md`'s 400 / 324, and independent of
    the patched module exec'd alongside it.
    """
    doc, geoms = ctx["doc"], ctx["geoms"]
    raster_pages = {p for e in ctx["seen"].values() for p in e["pages"]}
    rows = []
    for i, pg in enumerate(doc):
        if (i + 1) in ctx["ocr_pages"]:
            continue
        pm = ctx["page_mds"][i] if i < len(ctx["page_mds"]) else ""
        n = pm.count("\n|")
        if n < 3:
            continue                          # filter 3 does not fire at all
        g = geoms[i]
        why = render_reason(g)
        row = {
            "page": i + 1, "pipe_rows": n, "reason": why,
            "has_raster": i in raster_pages,
            "vector_furniture": bool(
                F3.SIG(g) in ctx["template"] and g["stroke_frac"] < STROKE_MIN_FRAC
                and g["ink"] < INK_MIN and g["rects"] < 8),
            "boxed_text": bool(why == "stroke_grid" and g["vx_pos"] in ctx["boxes"]),
            "curves": g["curves"], "diagonals": g["diagonals"],
            "paths": g["paths"],
            "page_chars": len(pg.get_text().strip()),
        }
        rows.append(row)
    return rows


def fires(row, T=4):
    """Does the proposed rule newly route this page? (page-loop level)"""
    return (not row["has_raster"] and row["reason"] is not None
            and not row["vector_furniture"] and not row["boxed_text"]
            and row["pipe_rows"] < T)


def toks(items, doc):
    """Per-item image tokens, by cost_guard's own model (F3.price)."""
    return [F3.price([it], doc) for it in items]


def shape(r, doc):
    return {"items": [{"id": it["id"], "page": it["page"], "kind": it["kind"],
                       "reason": it["reason"], "tok": t}
                      for it, t in zip(r["items"], toks(r["items"], doc))],
            "page_sigs": r.get("page_sigs") or {},
            "collapsed": any(d.get("why") == "cost_guard"
                             for d in r.get("dropped", [])),
            "textonly": sum(1 for d in r.get("dropped", [])
                            if d.get("why") == "textonly_page")}


def run_shard(corpus, i, n):
    d = parts_dir(corpus)
    d.mkdir(parents=True, exist_ok=True)
    patched = filter3_patch.load(NARROW)
    paths = sorted((ROOT / corpus).glob("*.pdf"))[i::n]
    recs = []
    for k, p in enumerate(paths):
        t0 = time.perf_counter()
        try:
            a = harvest(str(p))
        except Exception as e:
            recs.append({"file": p.name, "status": f"raise {type(e).__name__}"})
            continue
        t1 = time.perf_counter()
        try:
            b = patched.harvest(str(p))
        except Exception as e:
            b = {"status": f"raise {type(e).__name__}"}
        t2 = time.perf_counter()
        if a.get("status") != "ok" or b.get("status") != "ok":
            recs.append({"file": p.name, "status": a.get("status"),
                         "patched_status": b.get("status")})
            continue
        ctx = F3.prefix(str(p))
        rows = predicate_rows(ctx) if ctx else []
        with fitz.open(str(p)) as doc:
            rec = {"file": p.name, "status": "ok", "pages": a["pages"],
                   "vendor": vendor_of(p.name),
                   "ship": shape(a, doc), "pat": shape(b, doc),
                   "rows": rows,
                   "t_ship": round(t1 - t0, 2), "t_pat": round(t2 - t1, 2)}
        if ctx:
            ctx["doc"].close()
        recs.append(rec)
        if (k + 1) % 10 == 0:
            print(f"shard {i}: {k+1}/{len(paths)}", file=sys.stderr, flush=True)
    (d / f"shard{i}.json").write_text(json.dumps(recs))
    print(f"shard {i}: done {len(recs)}", file=sys.stderr, flush=True)


def read_parts(corpus):
    recs = []
    for i in range(SHARDS):
        recs += json.loads((parts_dir(corpus) / f"shard{i}.json").read_text())
    recs.sort(key=lambda r: r["file"])
    return recs


def load_recs(corpus, reuse=False):
    d = parts_dir(corpus)
    if not reuse:
        d.mkdir(parents=True, exist_ok=True)
        for f in d.glob("shard*.json"):
            f.unlink()
        me = str(pathlib.Path(__file__).resolve())
        extra = ["--narrow"] if NARROW else []
        procs = [subprocess.Popen([sys.executable, me, corpus, "--shard",
                                   f"{i}/{SHARDS}"] + extra)
                 for i in range(SHARDS)]
        bad = [i for i, p in enumerate(procs) if p.wait() != 0]
        if bad:
            raise SystemExit(f"shards failed: {bad}")
    return read_parts(corpus)


# --------------------------------------------------------------- batch scope
def batch_scope(recs, side):
    """drop_batch_furniture at corpus scope, in place. Returns file -> items."""
    shaped = [{"status": "ok", "path": r["file"],
               "items": [dict(it) for it in r[side]["items"]],
               "dropped": [], "page_sigs": r[side]["page_sigs"]}
              for r in recs if r["status"] == "ok"]
    drop_batch_furniture(shaped, batch_furniture(shaped))
    return {s["path"]: s["items"] for s in shaped}


# ----------------------------------------------------------------------- main
def main(corpus, reuse=False):
    recs = load_recs(corpus, reuse)
    ok = [r for r in recs if r["status"] == "ok"]
    OUT.mkdir(parents=True, exist_ok=True)
    ship = batch_scope(ok, "ship")
    pat = batch_scope(ok, "pat")

    # ---- (a) the page-loop predicate, comparable with eval/filter3.md's 400
    pred = [{"file": r["file"], "vendor": r["vendor"], **row}
            for r in ok for row in r["rows"] if fires(row)]
    f3_pages = sum(len(r["rows"]) for r in ok)
    blind = sum(1 for r in ok for row in r["rows"]
                if not row["has_raster"] and row["reason"]
                and not row["vector_furniture"] and not row["boxed_text"])

    # ---- (b) what the pipeline actually adds, after cost_guard + batch scope
    added, docs_changed, flips, sg_flips = [], [], [], []
    calls_b = calls_a = tok_b = tok_a = 0
    for r in ok:
        A, B = ship[r["file"]], pat[r["file"]]
        calls_b += len(A); calls_a += len(B)
        tok_b += sum(it["tok"] for it in A); tok_a += sum(it["tok"] for it in B)
        aid = {it["id"] for it in A}
        new = [it for it in B if it["id"] not in aid]
        lost = [it for it in A if it["id"] not in {i["id"] for i in B}]
        prow = {row["page"]: row for row in r["rows"]}
        for it in new:
            added.append({"file": r["file"], "vendor": r["vendor"],
                          "page": it["page"], "reason": it["reason"],
                          "kind": it["kind"],
                          "collapsed": r["pat"]["collapsed"],
                          "pipe_rows": prow.get(it["page"], {}).get("pipe_rows"),
                          "curves": prow.get(it["page"], {}).get("curves"),
                          "diagonals": prow.get(it["page"], {}).get("diagonals"),
                          "predicate": bool(fires(prow[it["page"]]))
                          if it["page"] in prow else False})
        if len(A) != len(B) or new or lost:
            docs_changed.append({"file": r["file"], "before": len(A),
                                 "after": len(B), "added": [i["id"] for i in new],
                                 "lost": [i["id"] for i in lost]})
        if r["ship"]["collapsed"] != r["pat"]["collapsed"]:
            flips.append({"file": r["file"], "before": r["ship"]["collapsed"],
                          "after": r["pat"]["collapsed"],
                          "calls": [len(A), len(B)],
                          "tok": [sum(i["tok"] for i in A),
                                  sum(i["tok"] for i in B)]})
        if (len(A) > SCALE_GUARD) != (len(B) > SCALE_GUARD):
            sg_flips.append({"file": r["file"], "calls": [len(A), len(B)],
                             "dir": "over" if len(B) > SCALE_GUARD else "under"})

    sel = [a for a in added if a["reason"] != "whole_document"
           and a["kind"] == "page_render"]
    coll = [a for a in added if a["reason"] == "whole_document"]
    ras = [a for a in added if a["kind"] == "raster"]

    idx = {
        "corpus": corpus,
        "rule": ("FILTER3_ROWS = 4 where the page carries no raster"
                 + (" AND render_reason is curves/diagonals" if NARROW else "")),
        "documents": len(recs), "ok": len(ok),
        "errors": [{"file": r["file"], "status": r.get("status"),
                    "patched": r.get("patched_status")}
                   for r in recs if r["status"] != "ok"],
        "filter3_pages": f3_pages, "blind_spot_pages": blind,
        "predicate_firings": len(pred),
        "predicate_documents": len({p["file"] for p in pred}),
        "predicate_by_vendor": dict(collections.Counter(
            p["vendor"] for p in pred).most_common()),
        "predicate_by_branch": dict(collections.Counter(
            p["reason"] for p in pred).most_common()),
        "calls_before": calls_b, "calls_after": calls_a,
        "tokens_before": tok_b, "tokens_after": tok_a,
        "renders_added": len(sel),
        "renders_added_documents": len({a["file"] for a in sel}),
        "whole_document_side_effects": len(coll),
        "rasters_handed_back": len(ras),
        "documents_changed": docs_changed,
        "collapse_flips": flips, "scale_guard_flips": sg_flips,
        "over_scale_guard_before": sum(1 for r in ok if len(ship[r["file"]]) > SCALE_GUARD),
        "over_scale_guard_after": sum(1 for r in ok if len(pat[r["file"]]) > SCALE_GUARD),
        "t_ship": round(sum(r["t_ship"] for r in ok), 1),
        "t_pat": round(sum(r["t_pat"] for r in ok), 1),
        "predicate_rows": pred,
        "added_rows": sorted(sel, key=lambda a: (a["file"], a["page"])),
    }
    name = pathlib.Path(corpus).name
    (OUT / f"index-{name}{suffix()}.json").write_text(json.dumps(idx, indent=1))

    print(f"corpus                 : {corpus}")
    print(f"documents ok           : {len(ok)}/{len(recs)}  "
          f"errors={[e['file'] for e in idx['errors']]}")
    print(f"filter-3 pages         : {f3_pages}  (blind spot: {blind})")
    print(f"PREDICATE firings      : {len(pred)} pages in "
          f"{idx['predicate_documents']} documents")
    print(f"  by branch            : {idx['predicate_by_branch']}")
    print(f"  by vendor            : {idx['predicate_by_vendor']}")
    print(f"vision calls           : {calls_b} -> {calls_a} "
          f"({calls_a - calls_b:+d}, {(calls_a-calls_b)/max(1,calls_b)*100:+.1f}%)")
    print(f"image tokens           : {tok_b:,} -> {tok_a:,} "
          f"({tok_a - tok_b:+,}, {(tok_a-tok_b)/max(1,tok_b)*100:+.1f}%)")
    print(f"page renders ADDED     : {len(sel)} in "
          f"{idx['renders_added_documents']} documents")
    print(f"  whole_document side effects: {len(coll)}   "
          f"rasters handed back: {len(ras)}")
    print(f"documents changed      : {len(docs_changed)}")
    print(f"cost_guard flips       : {len(flips)}  {flips}")
    print(f"over SCALE_GUARD       : {idx['over_scale_guard_before']} -> "
          f"{idx['over_scale_guard_after']}   flips={len(sg_flips)} {sg_flips}")
    print(f"harvest wall           : shipped {idx['t_ship']}s  "
          f"patched {idx['t_pat']}s")


def diff(corpus):
    """The page-loop predicate against what the patched pipeline really adds."""
    name = pathlib.Path(corpus).name
    idx = json.loads((OUT / f"index-{name}{suffix()}.json").read_text())
    want = {(p["file"], p["page"]) for p in idx["predicate_rows"]}
    got = {(a["file"], a["page"]) for a in idx["added_rows"]}
    only_p = sorted(want - got)
    only_r = sorted(got - want)
    print(f"predicate      : {len(want)}")
    print(f"pipeline adds  : {len(got)}")
    print(f"only predicate : {len(only_p)} {only_p[:12]}")
    print(f"only pipeline  : {len(only_r)} {only_r[:12]}")
    return 1 if (only_p or only_r) else 0


def sample(corpus, budget=LABEL_BUDGET, seed=SEED):
    """Draw the labelling set, stratified by vendor, and SAY what is excluded."""
    import random
    name = pathlib.Path(corpus).name
    idx = json.loads((OUT / f"index-{name}.json").read_text())
    rows = sorted(idx["added_rows"], key=lambda a: (a["file"], a["page"]))
    byv = collections.defaultdict(list)
    for r in rows:
        byv[r["vendor"]].append(r)
    N = len(rows)
    if N <= budget:
        drawn, quota = list(rows), {v: len(g) for v, g in byv.items()}
    else:
        # largest-remainder proportional allocation, floor of 1 per vendor
        quota, rem = {}, {}
        for v, g in byv.items():
            exact = len(g) * budget / N
            quota[v] = max(1, int(exact))
            rem[v] = exact - int(exact)
        while sum(quota.values()) > budget:                 # floors overshot
            v = min((v for v in quota if quota[v] > 1), key=lambda v: rem[v])
            quota[v] -= 1
        for v in sorted(byv, key=lambda v: -rem[v]):
            if sum(quota.values()) >= budget:
                break
            if quota[v] < len(byv[v]):
                quota[v] += 1
        rng = random.Random(seed)
        drawn = []
        for v in sorted(byv):
            g = sorted(byv[v], key=lambda a: (a["file"], a["page"]))
            drawn += g if quota[v] >= len(g) else rng.sample(g, quota[v])
        drawn.sort(key=lambda a: (a["file"], a["page"]))

    (OUT / "pages").mkdir(parents=True, exist_ok=True)
    tagged = []
    for i, a in enumerate(drawn, start=1):
        tag = f"d{i:03d}"
        with fitz.open(str(ROOT / corpus / a["file"])) as doc:
            doc[a["page"] - 1].get_pixmap(dpi=DPI).save(
                str(OUT / "pages" / f"{tag}.png"))
        tagged.append(dict(a, tag=tag))
    strata = [{"vendor": v, "population": len(byv[v]),
               "sampled": sum(1 for t in tagged if t["vendor"] == v),
               "not_labelled": len(byv[v]) - sum(1 for t in tagged
                                                 if t["vendor"] == v)}
              for v in sorted(byv, key=lambda v: -len(byv[v]))]
    (OUT / "sample.json").write_text(json.dumps(
        {"corpus": corpus, "population": N, "budget": budget, "seed": seed,
         "sampled": len(tagged), "not_labelled": N - len(tagged),
         "dpi": DPI, "strata": strata, "rows": tagged}, indent=1))
    print(f"population {N}  drawn {len(tagged)}  not labelled {N - len(tagged)}"
          f"  seed {seed}")
    print(f"{'vendor':<12}{'population':>11}{'sampled':>9}{'not labelled':>14}")
    for s in strata:
        print(f"{s['vendor']:<12}{s['population']:>11}{s['sampled']:>9}"
              f"{s['not_labelled']:>14}")
    print(f"rendered {len(tagged)} pages at {DPI} dpi -> {OUT/'pages'}")


if __name__ == "__main__":
    argv = sys.argv[1:]
    NARROW = "--narrow" in argv
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
        main(target, reuse="--reuse" in argv)
