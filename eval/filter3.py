# /// script
# requires-python = ">=3.10"
# dependencies = ["pdf-inspector==0.2.6", "pymupdf==1.28.0"]
# ///
"""Filter 3 -- the `pm.count("\\n|") >= 3` shortcut -- enumerated and priced.

`eval/multifigure.md` established that all 131 of its triggers were filter-3
pages that also carried a raster: the raster survived only because a different
path routes it. The pages nobody has ever looked at are the ones where filter 3
skips a page that carries figure signal and NO raster at all. Nothing routes
them, no counter exists, no eval has rendered one.

    uv run eval/filter3.py measure --check      # harvest 711 docs -> firings.json
    uv run eval/filter3.py measure --reuse      # re-aggregate the shard parts
    uv run eval/filter3.py report               # re-print the cross-tab
    uv run eval/filter3.py render               # sample + render the population
    uv run eval/filter3.py batches [n]          # write the blind batch files
    uv run eval/filter3.py score                # merge labels, score, CIs
    uv run eval/filter3.py features             # score candidate narrowings
    uv run eval/filter3.py variants             # price the coarse variants
    uv run eval/filter3.py cost                 # price the proposed patch for real
    uv run eval/filter3.py validate <corpus> [rule]   # run a rule on a holdout
    uv run eval/filter3.py holdout              # merge + score the blind labels

WHAT FILTER 3 ACTUALLY DOES, which is narrower than it looks.

    pm = page_mds[i] ...
    if pm.count("\\n|") >= 3:
        continue                              # filter 3: extractor won

The `continue` skips the vector_furniture drop, `render_reason`, the
`boxed_text` drop and the `renders[i] = why` assignment. Of those, only the
last changes what ships: `vector_furniture`/`boxed_text` only append to the
`dropped` audit list, and every downstream consumer (`grid_pages`,
subsumption, `cost_guard`, `page_sigs`) reads `renders`, which is written ONLY
when `render_reason` returns a reason. So filter 3's entire functional
footprint is exactly the pages this script enumerates: pages where
`render_reason` would have fired. On every other page it is a no-op.

That is why the "narrow condition" this was asked to consider -- apply filter 3
only when the page has no figure signal -- is not a narrowing at all. It is
deleting filter 3.

HOW THE COUNTERFACTUAL IS COMPUTED. `route()` below is harvest()'s page loop
with the filter-3 test behind a policy callback, and every other phase --
filter 1, filter 2, the template/box sets, grid_pages, subsumption,
`cost_guard`, `drop_textonly` -- called from harvest.py itself, not
re-derived. `measure --check` asserts that the baseline policy reproduces
harvest()'s own `items` list byte-for-byte on every document; run it, because
the last two rules shipped here were saved by exactly that diff.
"""
import collections
import json
import math
import pathlib
import random
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills" / "doc-extract"))
import fitz                                                     # noqa: E402
import pdf_inspector as pi                                      # noqa: E402
from filters import UBIQUITY, _tok, furniture_reason            # noqa: E402
import harvest as H                                             # noqa: E402
from harvest import (RASTER_GRID, SCALE_GUARD, STROKE_MIN_FRAC,  # noqa: E402
                     INK_MIN, NO_TEXT_EDGE_PX, batch_furniture,
                     box_templates, cost_guard, drop_batch_furniture,
                     drop_textonly, grid_pages, harvest, page_geometry,
                     render_edge, render_reason, _is_blank)

OUT = ROOT / "eval" / "filter3"
PARTS = OUT / "parts"
CORPORA = ["datasheets", "pmc", "arxiv", "papers", "tds"]
DPI = 130
SHARDS = 6

SAMPLE_MAX = 250
SEED = 20260813

CAPTION = re.compile(r"\b(Fig(?:ure)?\.?|Table|Chart|Scheme|Plate)\s*\.?\s*\d",
                     re.I)

SIG = lambda g: (g["curves"], g["diagonals"], g["axis_h"], g["axis_v"])
TABLEISH = {"stroke_grid", "dense_grid"}    # branches that mean "a table the
                                            # extractor missed" -- the only
                                            # branches filter 3's premise rebuts


def corpus_paths():
    out = []
    for c in CORPORA:
        out += [(c, p) for p in sorted((ROOT / "corpus" / c).glob("*.pdf"))]
    return out


def wilson(k, n, z=1.96):
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - h), min(1.0, c + h))


# ------------------------------------------------------------------- routing
def prefix(path):
    """Everything harvest() does before the page loop. Returns None on error."""
    try:
        doc = fitz.open(path)
    except Exception:
        return None
    if doc.needs_pass or doc.is_encrypted:
        doc.close()
        return None
    try:
        det = pi.detect_pdf(path)
        ocr_pages = set(getattr(det, "pages_needing_ocr", []) or [])
        res = pi.process_pdf(path)
        doc_md = getattr(res, "markdown", None)
    except Exception:
        doc.close()
        return None
    if not (doc_md or "").strip():
        has_visual = any(pg.get_images(full=True) or pg.get_cdrawings()
                         for pg in doc)
        if not has_visual and not ocr_pages:
            doc.close()
            return None
    try:
        page_mds = [getattr(p, "markdown", "") or ""
                    for p in getattr(pi.extract_pages_markdown(path), "pages", [])]
    except Exception:
        page_mds = []

    npages = len(doc)
    seen = collections.defaultdict(lambda: {"n": 0, "w": 0, "h": 0, "pages": set()})
    for i, pg in enumerate(doc):
        for im in pg.get_images(full=True):
            e = seen[im[0]]
            e["n"] += 1
            e["w"], e["h"] = im[2], im[3]
            e["pages"].add(i)
    kept = {x: e for x, e in seen.items()
            if not furniture_reason(e["w"], e["h"], e["n"], npages)}

    # filter 2, verbatim from harvest() (it closes over `doc`)
    import hashlib

    def _img_hash(xref):
        try:
            return hashlib.sha256(doc.extract_image(xref)["image"]).hexdigest()
        except Exception:
            return f"xref{xref}"

    def _raw_key(xref):
        try:
            meta = "|".join(str(doc.xref_get_key(xref, k)) for k in
                            ("Filter", "DecodeParms", "ColorSpace",
                             "BitsPerComponent", "SMask"))
            return hashlib.sha256((doc.xref_stream_raw(xref) or b"")
                                  + meta.encode()).hexdigest()
        except Exception:
            return None

    by_dim = collections.defaultdict(list)
    for xref, e in kept.items():
        by_dim[(e["w"], e["h"])].append(xref)
    ident = {}
    for dim, group in by_dim.items():
        if len(group) == 1:
            continue
        raws = [_raw_key(x) for x in group]
        if None not in raws and len(set(raws)) == 1:
            h = _img_hash(group[0])
            if h == f"xref{group[0]}":
                continue
            for x in group:
                ident[x] = (dim, h)
        else:
            for x in group:
                ident[x] = (dim, _img_hash(x))
    by_hash, uniq = {}, {}
    for xref, e in kept.items():
        h = ident.get(xref, ("uniq", xref))
        if h not in by_hash:
            by_hash[h] = xref
            uniq[xref] = e

    geoms = [page_geometry(pg) for pg in doc]
    counts = collections.Counter(SIG(g) for g in geoms)
    template = {k for k, n in counts.items() if npages > 2 and n / npages > UBIQUITY}
    boxes = box_templates(geoms)
    return dict(doc=doc, npages=npages, ocr_pages=ocr_pages, page_mds=page_mds,
                geoms=geoms, template=template, boxes=boxes, seen=dict(seen),
                uniq=uniq)


def route(ctx, policy):
    """harvest()'s page loop onward, with filter 3 behind `policy`.

    `policy(i, g, why) -> True` means "filter 3 applies, skip this page".
    The baseline is `lambda i, g, why: True`, which is the shipped code.
    """
    doc, geoms = ctx["doc"], ctx["geoms"]
    renders, edges, page_sigs = {}, {}, {}
    for i, pg in enumerate(doc):
        if (i + 1) in ctx["ocr_pages"]:
            if not _is_blank(pg):
                renders[i] = "no_text_layer"
                edges[i] = render_edge(pg)
            continue
        pm = ctx["page_mds"][i] if i < len(ctx["page_mds"]) else ""
        g = geoms[i]
        why = render_reason(g)
        if policy(i, g, why, pm):
            continue                                      # filter 3
        if (SIG(g) in ctx["template"] and g["stroke_frac"] < STROKE_MIN_FRAC
                and g["ink"] < INK_MIN and g["rects"] < 8):
            continue                                      # vector_furniture
        if why == "stroke_grid" and g["vx_pos"] in ctx["boxes"]:
            continue                                      # boxed_text
        if why:
            renders[i] = why
            edges[i] = render_edge(pg)
            page_sigs[str(i + 1)] = SIG(g)

    for p in grid_pages((e["pages"] for e in ctx["uniq"].values()), renders):
        renders[p] = "raster_grid"
        edges[p] = render_edge(doc[p])

    standalone = [(x, e) for x, e in ctx["uniq"].items()
                  if not all(p in renders for p in e["pages"])]
    items = [{"id": f"p{min(e['pages'])+1:03d}-x{x}", "page": min(e["pages"]) + 1,
              "kind": "raster", "reason": "standalone_raster", "xref": x,
              "px": [e["w"], e["h"]], "description": None}
             for x, e in standalone]
    items += [{"id": f"p{i+1:03d}-render", "page": i + 1, "kind": "page_render",
               "reason": why, "edge": edges.get(i), "description": None}
              for i, why in sorted(renders.items())]
    items, guard = cost_guard(items, doc, edges)
    gone = []
    if guard:
        img_pages = {p for e in ctx["seen"].values() for p in e["pages"]}
        items, gone = drop_textonly(items, geoms, img_pages, ctx["ocr_pages"])
    return {"items": items, "guard": guard, "page_sigs": page_sigs,
            "textonly": len(gone), "standalone": {x for x, _ in standalone}}


def price(items, doc):
    """Token cost of a routed set, by exactly cost_guard()'s own model."""
    t = 0
    for it in items:
        if it["kind"] == "raster":
            t += _tok(*it["px"])
        else:
            pg = doc[it["page"] - 1]
            e = it.get("edge") or NO_TEXT_EDGE_PX
            sc = e / max(pg.rect.width, pg.rect.height)
            t += _tok(int(pg.rect.width * sc), int(pg.rect.height * sc))
    return t


def slim(items, doc):
    out = []
    for it in items:
        d = {"id": it["id"], "page": it["page"], "kind": it["kind"],
             "reason": it["reason"]}
        d["tok"] = price([it], doc)
        out.append(d)
    return out


# ------------------------------------------------------------------ policies
def _rows(pm):
    return pm.count("\n|")


POLICIES = {
    "baseline":    lambda i, g, why, pm: _rows(pm) >= 3,     # ships today
    "delete":      lambda i, g, why, pm: False,              # no filter 3
    "tablebranch": lambda i, g, why, pm: _rows(pm) >= 3 and (
        why in TABLEISH or why is None),
}

# The proposed patch. Filter 3 stands whenever the page carries a raster --
# rendering those pages is the swap `eval/multifigure.md` rejected, because a
# page render caps the raster at its placement and costs it a median 0.27x
# linear resolution. On a page with no raster there is nothing to degrade, so
# the only question is whether a table of fewer than T pipe rows is evidence
# the extractor captured the page. T = 4 means "a header, a separator and at
# least two data rows"; T = 3, which ships, accepts a ONE-ROW table.
FILTER3_ROWS = 4


def variant_policies(raster_pages, T=FILTER3_ROWS):
    """Policies that need per-page raster facts. `raster_pages` is 0-based."""
    p = dict(POLICIES)
    p["noraster"] = lambda i, g, why, pm: _rows(pm) >= 3 and (
        (i in raster_pages) or why is None)
    p["tablebranch_noraster"] = lambda i, g, why, pm: _rows(pm) >= 3 and (
        why in TABLEISH or why is None or i in raster_pages)
    p["proposed"] = lambda i, g, why, pm: (
        _rows(pm) >= T or (_rows(pm) >= 3 and i in raster_pages))
    return p


# ------------------------------------------------------------------- measure
ALL_POLICIES = ["baseline", "delete", "tablebranch", "noraster",
                "tablebranch_noraster", "proposed"]


def analyse(corpus, path, check=False, policies=None, rows_wanted=True):
    ctx = prefix(str(path))
    if ctx is None:
        return {"corpus": corpus, "name": path.name,
                "path": str(path.relative_to(ROOT)), "status": "error"}
    doc, geoms = ctx["doc"], ctx["geoms"]
    base = route(ctx, POLICIES["baseline"])

    raw_pages = {p for e in ctx["seen"].values() for p in e["pages"]}
    uniq_pages = collections.Counter()
    for e in ctx["uniq"].values():
        for p in e["pages"]:
            uniq_pages[p] += 1
    routed_pages = collections.Counter()
    for x in base["standalone"]:
        for p in ctx["uniq"][x]["pages"]:
            routed_pages[p] += 1

    rows = []
    for i, pg in enumerate(doc if rows_wanted else []):
        if (i + 1) in ctx["ocr_pages"]:
            continue
        pm = ctx["page_mds"][i] if i < len(ctx["page_mds"]) else ""
        if pm.count("\n|") < 3:
            continue
        g = geoms[i]
        why = render_reason(g)
        vf = (SIG(g) in ctx["template"] and g["stroke_frac"] < STROKE_MIN_FRAC
              and g["ink"] < INK_MIN and g["rects"] < 8)
        boxed = (why == "stroke_grid" and g["vx_pos"] in ctx["boxes"])
        text = pg.get_text()
        e = render_edge(pg)
        sc = e / max(pg.rect.width, pg.rect.height)
        rows.append({
            "corpus": corpus, "doc": str(path.relative_to(ROOT)),
            "name": path.name, "page": i + 1, "npages": ctx["npages"],
            "reason": why, "vector_furniture": vf, "boxed_text": boxed,
            "raw_rasters": len([1 for e2 in ctx["seen"].values() if i in e2["pages"]]),
            "uniq_rasters": uniq_pages.get(i, 0),
            "routed_rasters": routed_pages.get(i, 0),
            "pipe_rows": pm.count("\n|"), "md_chars": len(pm.strip()),
            "page_chars": len(text.strip()), "has_caption": bool(CAPTION.search(text)),
            "edge": e, "render_tok": _tok(int(pg.rect.width * sc),
                                          int(pg.rect.height * sc)),
            "curves": g["curves"], "diagonals": g["diagonals"],
            "axis_h": g["axis_h"], "axis_v": g["axis_v"], "rects": g["rects"],
            "paths": g["paths"], "ink": g["ink"],
            "stroke_frac": g["stroke_frac"], "stroke_aspect": g["stroke_aspect"],
            "x_edges": g["x_edges"], "y_edges": g["y_edges"],
            "vx_pos": len(g["vx_pos"])})

    pols = variant_policies(raw_pages)
    variants = {}
    for name in (policies or ALL_POLICIES):
        pol = pols[name]
        r = base if name == "baseline" else route(ctx, pol)
        variants[name] = {
            "calls": len(r["items"]), "tokens": price(r["items"], doc),
            "collapsed": bool(r["guard"]), "textonly": r["textonly"],
            "over_scale_guard": len(r["items"]) > SCALE_GUARD,
            "items": slim(r["items"], doc), "page_sigs": r["page_sigs"]}

    mismatch = None
    if check:
        real = harvest(str(path))
        got = [(i["id"], i["kind"], i["reason"]) for i in real.get("items", [])]
        mine = [(i["id"], i["kind"], i["reason"]) for i in base["items"]]
        if got != mine:
            mismatch = {"harvest": got, "replica": mine}
    doc.close()
    return {"corpus": corpus, "name": path.name,
            "path": str(path.relative_to(ROOT)), "status": "ok",
            "pages": ctx["npages"], "rows": rows, "variants": variants,
            "mismatch": mismatch}


def run_shard(i, n, check=False, parts=None, policies=None, rows_wanted=True):
    parts = parts or PARTS
    parts.mkdir(parents=True, exist_ok=True)
    todo = corpus_paths()[i::n]
    recs = []
    for k, (c, p) in enumerate(todo):
        try:
            recs.append(analyse(c, p, check, policies, rows_wanted))
        except Exception as e:
            recs.append({"corpus": c, "name": p.name,
                         "path": str(p.relative_to(ROOT)), "status": "error",
                         "error": f"{type(e).__name__}: {e}"})
        if (k + 1) % 25 == 0:
            print(f"shard {i}: {k+1}/{len(todo)}", file=sys.stderr, flush=True)
    (parts / f"shard{i}.json").write_text(json.dumps(recs))
    print(f"shard {i}: done {len(recs)}", file=sys.stderr, flush=True)


COSTPARTS = OUT / "costparts"


def cost_run():
    """Baseline vs the proposed patch over the design corpora, cost_guard and
    drop_batch_furniture both driven for real. Two policies, no per-page rows,
    so it is far cheaper than a full `measure`."""
    COSTPARTS.mkdir(parents=True, exist_ok=True)
    for f in COSTPARTS.glob("shard*.json"):
        f.unlink()
    argv = [sys.executable, str(pathlib.Path(__file__).resolve()), "costshard"]
    procs = [subprocess.Popen(argv + [f"{i}/{SHARDS}"]) for i in range(SHARDS)]
    bad = [i for i, p in enumerate(procs) if p.wait() != 0]
    if bad:
        raise SystemExit(f"shards failed: {bad}")
    recs = []
    for i in range(SHARDS):
        recs += json.loads((COSTPARTS / f"shard{i}.json").read_text())
    recs = [r for r in recs if r["status"] == "ok"]
    out = {}
    for nm in ("baseline", "proposed"):
        calls = tok = 0
        for c in CORPORA:
            rs = [{"status": "ok", "path": r["path"],
                   "page_sigs": r["variants"][nm]["page_sigs"],
                   "items": [dict(i) for i in r["variants"][nm]["items"]],
                   "dropped": []}
                  for r in recs if r["corpus"] == c]
            drop_batch_furniture(rs, batch_furniture(rs))
            calls += sum(len(r["items"]) for r in rs)
            tok += sum(i["tok"] for r in rs for i in r["items"])
        out[nm] = (calls, tok)
    b, p = out["baseline"], out["proposed"]
    print(f"documents            : {len(recs)}")
    print(f"baseline             : {b[0]:,} calls, {b[1]:,} image tokens")
    print(f"proposed (T={FILTER3_ROWS}, no raster): {p[0]:,} calls, "
          f"{p[1]:,} image tokens")
    print(f"delta                : {p[0]-b[0]:+,} calls ({(p[0]-b[0])/b[0]*100:+.1f}%), "
          f"{p[1]-b[1]:+,} tokens ({(p[1]-b[1])/b[1]*100:+.1f}%)")
    flips = [(r["path"], r["variants"]["baseline"]["collapsed"],
              r["variants"]["proposed"]["collapsed"],
              r["variants"]["baseline"]["calls"], r["variants"]["proposed"]["calls"],
              r["variants"]["baseline"]["tokens"], r["variants"]["proposed"]["tokens"])
             for r in recs
             if r["variants"]["baseline"]["collapsed"]
             != r["variants"]["proposed"]["collapsed"]]
    print(f"cost_guard collapse flips: {len(flips)}")
    for f in flips:
        print(f"  {f[0]} {f[1]}->{f[2]} calls {f[3]}->{f[4]} tok {f[5]:,}->{f[6]:,}")
    sg = [r["path"] for r in recs
          if r["variants"]["baseline"]["over_scale_guard"]
          != r["variants"]["proposed"]["over_scale_guard"]]
    print(f"over_scale_guard flips   : {len(sg)}")
    docs = sum(1 for r in recs
               if r["variants"]["proposed"]["calls"]
               != r["variants"]["baseline"]["calls"])
    print(f"documents whose call count changes: {docs}")
    (OUT / "cost.json").write_text(json.dumps(
        {"baseline_calls": b[0], "baseline_tokens": b[1],
         "proposed_calls": p[0], "proposed_tokens": p[1],
         "filter3_rows": FILTER3_ROWS, "collapse_flips": flips,
         "scale_guard_flips": sg, "documents_changed": docs}, indent=1))


def measure(reuse=False, check=False):
    OUT.mkdir(parents=True, exist_ok=True)
    PARTS.mkdir(parents=True, exist_ok=True)
    if not reuse:
        for f in PARTS.glob("shard*.json"):
            f.unlink()
        argv = [sys.executable, str(pathlib.Path(__file__).resolve()), "shard"]
        procs = [subprocess.Popen(argv + [f"{i}/{SHARDS}"]
                                  + (["--check"] if check else []))
                 for i in range(SHARDS)]
        bad = [i for i, p in enumerate(procs) if p.wait() != 0]
        if bad:
            raise SystemExit(f"shards failed: {bad}")
    recs = []
    for i in range(SHARDS):
        recs += json.loads((PARTS / f"shard{i}.json").read_text())

    # cross-document furniture, per corpus, exactly as nofigure_render.py does
    bf = {}
    for name in ALL_POLICIES:
        removed = 0
        for c in CORPORA:
            rs = [{"status": r["status"], "path": r["path"],
                   "page_sigs": r["variants"][name]["page_sigs"],
                   "items": [dict(i) for i in r["variants"][name]["items"]],
                   "dropped": []}
                  for r in recs if r["corpus"] == c and r["status"] == "ok"]
            before = sum(len(r["items"]) for r in rs)
            drop_batch_furniture(rs, batch_furniture(rs))
            removed += before - sum(len(r["items"]) for r in rs)
        bf[name] = removed

    mism = [r for r in recs if r.get("mismatch")]
    ok = [r for r in recs if r["status"] == "ok"]
    rows = [row for r in ok for row in r["rows"]]

    blob = {
        "corpora": CORPORA,
        "documents": len(recs), "ok": len(ok),
        "errors": [r["path"] for r in recs if r["status"] != "ok"],
        "replica_mismatches": [r["path"] for r in mism],
        "batch_furniture_removed": bf,
        "n_filter3_pages": len(rows),
        "firings": rows,
        "docs": [{"corpus": r["corpus"], "path": r["path"], "pages": r["pages"],
                  "variants": {k: {kk: vv for kk, vv in v.items()
                                   if kk not in ("items", "page_sigs")}
                               for k, v in r["variants"].items()}}
                 for r in ok],
    }
    (OUT / "firings.json").write_text(json.dumps(blob, indent=1))
    report(blob)


def cells(rows):
    """The cross-tab. `eff` = the render filter 3 actually suppresses."""
    def bucket(r):
        if r["reason"] is None:
            return "no_reason"
        if r["vector_furniture"]:
            return "vector_furniture"
        if r["boxed_text"]:
            return "boxed_text"
        return "would_render"

    def rast(r):
        if r["raw_rasters"] == 0:
            return "no_raster"
        return "routed_raster" if r["routed_rasters"] else "raster_not_routed"

    t = collections.Counter((bucket(r), rast(r)) for r in rows)
    return t, bucket, rast


def report(blob):
    rows = blob["firings"]
    t, bucket, rast = cells(rows)
    print(f"documents            : {blob['ok']} ok, {len(blob['errors'])} error")
    print(f"replica mismatches   : {len(blob['replica_mismatches'])}")
    print(f"batch_furniture drops: {blob['batch_furniture_removed']}")
    print(f"filter-3 pages       : {len(rows)}\n")
    cols = ["no_raster", "raster_not_routed", "routed_raster"]
    order = ["would_render", "boxed_text", "vector_furniture", "no_reason"]
    print(f"{'':<18}" + "".join(f"{c:>20}" for c in cols) + f"{'total':>10}")
    for b in order:
        n = [t[(b, c)] for c in cols]
        print(f"{b:<18}" + "".join(f"{x:>20}" for x in n) + f"{sum(n):>10}")
    n = [sum(t[(b, c)] for b in order) for c in cols]
    print(f"{'total':<18}" + "".join(f"{x:>20}" for x in n) + f"{sum(n):>10}")

    pop = [r for r in rows if bucket(r) == "would_render" and rast(r) == "no_raster"]
    print(f"\nPOPULATION (would render, no raster at all): {len(pop)} pages, "
          f"{len({r['doc'] for r in pop})} documents")
    print("  by corpus : " + str(dict(collections.Counter(
        r["corpus"] for r in pop))))
    print("  by branch : " + str(dict(collections.Counter(
        r["reason"] for r in pop))))
    print("  by corpus x branch:")
    for k, v in sorted(collections.Counter(
            (r["corpus"], r["reason"]) for r in pop).items()):
        print(f"    {k[0]:<12} {k[1]:<12} {v:>5}")


# -------------------------------------------------------------------- render
def population(blob=None):
    blob = blob or json.loads((OUT / "firings.json").read_text())
    _, bucket, rast = cells(blob["firings"])
    return [r for r in blob["firings"]
            if bucket(r) == "would_render" and rast(r) == "no_raster"]


def stratified(pop, cap=SAMPLE_MAX, seed=SEED):
    """Proportional by (corpus, branch), with a floor of one per non-empty cell.

    Stratifying on the corpus alone would have been enough for the headline,
    but the candidate rule turns on the BRANCH (`curves`/`diagonals` versus
    `stroke_grid`/`dense_grid`), and 93% of the population is
    `curves`+`diagonals`, so a corpus-only draw would leave the other two
    branches at a handful of observations by accident rather than by choice.
    Allocation stays proportional, so the pooled rate is still a population
    rate up to the floors; `score()` prints the cell-reweighted estimate
    alongside it so the difference is visible rather than assumed.
    """
    if len(pop) <= cap:
        return list(pop), []
    cells_ = collections.defaultdict(list)
    for r in pop:
        cells_[(r["corpus"], r["reason"])].append(r)
    exact = {c: len(v) * cap / len(pop) for c, v in cells_.items()}
    take = {c: max(1, int(exact[c])) for c in cells_}
    while sum(take.values()) > cap:
        c = max((c for c in take if take[c] > 1), key=lambda c: take[c])
        take[c] -= 1
    for c in sorted(cells_, key=lambda c: exact[c] - int(exact[c]), reverse=True):
        if sum(take.values()) >= cap:
            break
        if take[c] < len(cells_[c]):
            take[c] += 1
    rng = random.Random(seed)
    sample, report_ = [], []
    for c in sorted(cells_):
        pool = sorted(cells_[c], key=lambda r: (r["doc"], r["page"]))
        n = min(take[c], len(pool))
        sample += rng.sample(pool, n)
        report_.append({"corpus": c[0], "branch": c[1], "population": len(pool),
                        "sampled": n, "not_labelled": len(pool) - n})
    sample.sort(key=lambda r: (r["corpus"], r["reason"], r["doc"], r["page"]))
    return sample, report_


def render():
    (OUT / "pages").mkdir(parents=True, exist_ok=True)
    pop = population()
    sample, rep = stratified(pop)
    if rep:
        print(f"population {len(pop)} > cap {SAMPLE_MAX}: drawing {len(sample)} "
              f"with seed {SEED}", file=sys.stderr)
        print(f"NOT LABELLED: {sum(r['not_labelled'] for r in rep)}, by cell:",
              file=sys.stderr)
        for r in sorted(rep, key=lambda r: -r["not_labelled"]):
            print(f"  {r['corpus']:<12} {r['branch']:<12} pop {r['population']:>5} "
                  f"sampled {r['sampled']:>4} unlabelled {r['not_labelled']:>5}",
                  file=sys.stderr)
    rows, skipped = [], []
    for i, f in enumerate(sample):
        tag = f"f{i+1:03d}"
        try:
            with fitz.open(str(ROOT / f["doc"])) as d:
                d[f["page"] - 1].get_pixmap(dpi=DPI).save(
                    str(OUT / "pages" / f"{tag}.png"))
        except Exception as e:
            skipped.append({"tag": tag, "doc": f["doc"], "page": f["page"],
                            "why": f"{type(e).__name__}: {e}"})
            continue
        rows.append(dict(f, tag=tag))
        if (i + 1) % 50 == 0:
            print(f"  rendered {i+1}/{len(sample)}", file=sys.stderr)
    (OUT / "index.json").write_text(json.dumps(
        {"dpi": DPI, "seed": SEED, "cap": SAMPLE_MAX, "population": len(pop),
         "sampled": len(sample), "rendered": len(rows), "strata": rep,
         "render_failures": skipped, "rows": rows}, indent=1))
    print(f"rendered {len(rows)} of {len(sample)} -> {OUT/'pages'}")
    if skipped:
        print(f"RENDER FAILURES (excluded, and why): {skipped}")


def batches(n=5):
    idx = json.loads((OUT / "index.json").read_text())["rows"]
    per = math.ceil(len(idx) / n)
    for b in range(n):
        chunk = idx[b * per:(b + 1) * per]
        if not chunk:
            continue
        lines = ["tag\timage"] + [
            f"{r['tag']}\teval/filter3/pages/{r['tag']}.png" for r in chunk]
        (OUT / f"batch{b+1}.tsv").write_text("\n".join(lines) + "\n")
        print(f"batch{b+1}.tsv: {len(chunk)} rows")


# --------------------------------------------------------------------- score
ORDER = ["none", "branding", "table", "figure"]   # ties break for filter 3
REAL = {"figure"}
PANEL = 3


def read_tsv(path):
    lines = [l for l in path.read_text().splitlines() if l.strip()]
    head = lines[0].split("\t")
    return [dict(zip(head, l.split("\t"))) for l in lines[1:]]


def score(merge=True):
    idx = {r["tag"]: r for r in json.loads((OUT / "index.json").read_text())["rows"]}
    if merge:
        votes, notes = collections.defaultdict(list), collections.defaultdict(list)
        files = sorted(OUT.glob("labels-*.tsv"))
        if not files:
            raise SystemExit("no eval/filter3/labels-*.tsv")
        for f in files:
            for r in read_tsv(f):
                lab = r["label"].strip()
                if lab not in ORDER:
                    raise SystemExit(f"{f.name}: {r['tag']} bad label {lab!r}")
                votes[r["tag"]].append(lab)
                notes[r["tag"]].append(r.get("note", "").strip())
        missing = sorted(set(idx) - set(votes))
        extra = sorted(set(votes) - set(idx))
        if missing:
            raise SystemExit(f"{len(missing)} tags unlabelled: {missing[:8]}")
        if extra:
            raise SystemExit(f"{len(extra)} tags not in index: {extra[:8]}")
        short = {t: len(v) for t, v in votes.items() if len(v) != PANEL}
        if short:
            raise SystemExit(f"{len(short)} tags without exactly {PANEL} labels: "
                             f"{sorted(short.items())[:10]}")
        out = ["\t".join(["tag", "corpus", "file", "page", "branch", "label",
                          "agree", "note"])]
        for tag in sorted(votes):
            c = collections.Counter(votes[tag])
            top = max(c.values())
            lab = min((l for l in c if c[l] == top), key=ORDER.index)
            note = next((n for l, n in zip(votes[tag], notes[tag])
                         if l == lab and n), "")
            i = idx[tag]
            out.append("\t".join([tag, i["corpus"], i["name"], str(i["page"]),
                                  str(i["reason"]), lab, f"{top}/{len(votes[tag])}",
                                  note]))
        (OUT / "labels.tsv").write_text("\n".join(out) + "\n")
        print(f"merged {len(files)} labeller files -> {OUT/'labels.tsv'} "
              f"({len(votes)} tags)")

    lab = {r["tag"]: r for r in read_tsv(OUT / "labels.tsv")}
    print("\nagreement: " + str(dict(collections.Counter(
        r["agree"] for r in lab.values()))))

    def tab(key, title, getter):
        print(f"\n{title}")
        print(f"| {key} | " + " | ".join(ORDER) + " | n | real figure |")
        print("|---|" + "--:|" * (len(ORDER) + 2))
        g = collections.defaultdict(list)
        for t, r in lab.items():
            g[getter(t, r)].append(t)
        for k in sorted(g, key=str):
            c = collections.Counter(lab[t]["label"] for t in g[k])
            n = len(g[k])
            f = sum(c[l] for l in REAL)
            lo, hi = wilson(f, n)
            print(f"| {k} | " + " | ".join(str(c[l]) for l in ORDER)
                  + f" | {n} | {f/n*100:.0f}% ({lo*100:.0f}-{hi*100:.0f}) |")

    n = len(lab)
    f = sum(1 for r in lab.values() if r["label"] in REAL)
    lo, hi = wilson(f, n)
    print(f"\nOVERALL: {f} of {n} carry a real figure = {f/n*100:.1f}% "
          f"(95% Wilson {lo*100:.0f}-{hi*100:.0f})")
    tab("corpus", "By corpus", lambda t, r: r["corpus"])
    tab("branch", "By render_reason branch", lambda t, r: r["branch"])
    print(f"\ndistinct documents in the labelled set: "
          f"{len({r['file'] for r in lab.values()})}; "
          f"documents carrying a real figure: "
          f"{len({r['file'] for r in lab.values() if r['label'] in REAL})}")

    # The draw is proportional except for the floors, so the pooled rate is
    # close to but not identical to the population rate. Both are printed;
    # quoting one without the other is how a sampling artefact gets published.
    pop = population()
    idx = {r["tag"]: r for r in json.loads((OUT / "index.json").read_text())["rows"]}
    cellpop = collections.Counter((r["corpus"], r["reason"]) for r in pop)
    hits = collections.defaultdict(lambda: [0, 0])
    for t, r in lab.items():
        k = (idx[t]["corpus"], idx[t]["reason"])
        hits[k][0] += 1
        hits[k][1] += 1 if r["label"] in REAL else 0
    est = sum(cellpop[k] * (v[1] / v[0]) for k, v in hits.items())
    print(f"cell-reweighted estimate: {est:.0f} of {len(pop)} population pages "
          f"carry a real figure = {est/len(pop)*100:.1f}% "
          f"(pooled sample rate {f/n*100:.1f}%)")
    print("cells where the sample is thin (n < 5), which the reweighting leans on:")
    for k, v in sorted(hits.items()):
        if v[0] < 5:
            print(f"  {k[0]:<12} {k[1]:<12} n={v[0]} figures={v[1]} "
                  f"population={cellpop[k]}")


def holdout_score(rule="proposed"):
    """Merge the blind holdout labels and print precision with Wilson bounds.

    Both holdouts are labelled as ONE batch under opaque `v###` tags, so a
    labeller cannot tell the corpora apart, let alone which corpus the rule was
    designed on. `vmap.json` is the only thing that maps a tag back.
    """
    d = OUT / "holdout"
    vmap = {m["vtag"]: m for m in json.loads((d / "vmap.json").read_text())}
    idx = {}
    for c in ("pmc_holdout", "arxiv_holdout"):
        f = d / f"index-{c}-{rule}.json"
        if f.exists():
            blob = json.loads(f.read_text())
            for r in blob["candidates"]:
                idx[(c, r["tag"])] = dict(r, _meta=blob)
    votes, notes = collections.defaultdict(list), collections.defaultdict(list)
    files = sorted(d.glob("labels-[0-9]*.tsv"))
    if not files:
        raise SystemExit("no eval/filter3/holdout/labels-*.tsv")
    for f in files:
        for r in read_tsv(f):
            lab = r["label"].strip()
            if lab not in ORDER:
                raise SystemExit(f"{f.name}: {r['tag']} bad label {lab!r}")
            votes[r["tag"]].append(lab)
            notes[r["tag"]].append(r.get("note", "").strip())
    if set(votes) != set(vmap):
        raise SystemExit(f"tag mismatch: {sorted(set(vmap) ^ set(votes))[:8]}")
    short = {t: len(v) for t, v in votes.items() if len(v) != PANEL}
    if short:
        raise SystemExit(f"{len(short)} tags without {PANEL} labels: "
                         f"{sorted(short.items())[:8]}")
    out = ["\t".join(["tag", "corpus", "file", "page", "branch", "pipe_rows",
                      "label", "agree", "note"])]
    per = collections.defaultdict(lambda: [0, 0])
    for t in sorted(votes):
        c = collections.Counter(votes[t])
        top = max(c.values())
        lab = min((l for l in c if c[l] == top), key=ORDER.index)
        m = vmap[t]
        r = idx[(m["corpus"], m["tag"])]
        note = next((n for l, n in zip(votes[t], notes[t]) if l == lab and n), "")
        out.append("\t".join([t, m["corpus"], r["file"], str(r["page"]),
                              str(r["reason"]), str(r["pipe_rows"]), lab,
                              f"{top}/{len(votes[t])}", note]))
        per[m["corpus"]][0] += 1
        per[m["corpus"]][1] += 1 if lab in REAL else 0
    (d / "labels.tsv").write_text("\n".join(out) + "\n")
    print(f"wrote {d/'labels.tsv'} ({len(votes)} rows)\n")
    tot = [0, 0]
    for c, (n, f) in sorted(per.items()):
        blob = json.loads((d / f"index-{c}-{rule}.json").read_text())
        lo, hi = wilson(f, n)
        print(f"{c}: {blob['documents']} docs, {blob['baseline_calls']} -> "
              f"{blob['variant_calls']} vision calls")
        print(f"  rule adds {blob['added_selected']} renders "
              f"({blob['added_collapse_side_effects']} more arrive via a "
              f"collapse and are excluded); {n} labelled")
        print(f"  carry a real figure: {f}/{n} = {f/n*100:.0f}% "
              f"(95% Wilson {lo*100:.0f}-{hi*100:.0f})")
        tot[0] += n
        tot[1] += f
    lo, hi = wilson(tot[1], tot[0])
    print(f"\nboth holdouts: {tot[1]}/{tot[0]} = {tot[1]/tot[0]*100:.0f}% "
          f"(95% Wilson {lo*100:.0f}-{hi*100:.0f})")
    print("agreement: " + str(dict(collections.Counter(
        f"{max(collections.Counter(v).values())}/{len(v)}"
        for v in votes.values()))))
    lab = {r["tag"]: r for r in read_tsv(d / "labels.tsv")}
    print("by label: " + str(dict(collections.Counter(
        r["label"] for r in lab.values()))))


# ------------------------------------------------------------------ features
def features():
    """Score candidate narrowings against the labels, then price them.

    Computed AFTER labelling, from `firings.json`, so no labeller could see
    any of these numbers. Precision is the share of pages a rule would route
    that a labeller called `figure`; the population columns apply the same
    predicate to all 4,065 pages and price them first-order (sum of the page's
    own `render_tok`). First order only -- `cost_guard` is re-driven for real
    in `variants` for the rules that survive.
    """
    lab = {r["tag"]: r for r in read_tsv(OUT / "labels.tsv")}
    idx = {r["tag"]: r for r in json.loads((OUT / "index.json").read_text())["rows"]}
    pop = population()

    def ratio(r):
        return r["md_chars"] / max(1, r["page_chars"])

    rules = {
        "everything (delete filter 3)": lambda r: True,
        "branch is curves/diagonals": lambda r: r["reason"] in ("curves", "diagonals"),
        "branch is diagonals": lambda r: r["reason"] == "diagonals",
        "branch is curves": lambda r: r["reason"] == "curves",
        "curves/diagonals and caption on page": lambda r: (
            r["reason"] in ("curves", "diagonals") and r["has_caption"]),
        "curves/diagonals and the table is short (<=6 pipe rows)": lambda r: (
            r["reason"] in ("curves", "diagonals") and r["pipe_rows"] <= 6),
        "curves/diagonals and the table is long (>=20 pipe rows)": lambda r: (
            r["reason"] in ("curves", "diagonals") and r["pipe_rows"] >= 20),
        "curves/diagonals and caption and >=4 diagonals": lambda r: (
            r["reason"] in ("curves", "diagonals") and r["has_caption"]
            and r["diagonals"] >= 4),
        "curves/diagonals and ink >= 0.02": lambda r: (
            r["reason"] in ("curves", "diagonals") and r["ink"] >= 0.02),
        "curves/diagonals and diagonals >= 4": lambda r: (
            r["reason"] in ("curves", "diagonals") and r["diagonals"] >= 4),
        "curves/diagonals and stroke_frac >= 0.30": lambda r: (
            r["reason"] in ("curves", "diagonals") and r["stroke_frac"] >= 0.30),
        "curves/diagonals and curves >= 40": lambda r: (
            r["reason"] in ("curves", "diagonals") and r["curves"] >= 40),
        "curves/diagonals and rects >= 8": lambda r: (
            r["reason"] in ("curves", "diagonals") and r["rects"] >= 8),
    }
    print("Sweep of filter 3's OWN constant. Today the test is "
          "`pm.count(chr(10)+'|') >= 3`; raising it to T renders the "
          "figure-signal pages whose table has fewer than T pipe rows.")
    print("| T | fires (labelled) | figure | precision | recall | population "
          "| pop. tokens | % of routed |")
    print("|---|--:|--:|--:|--:|--:|--:|--:|")
    base_tok = 5_812_236          # baseline routed image tokens, post-batch-furniture
    for T in (3, 4, 5, 6, 7, 8, 10, 12, 16, 20, 10**9):
        sel = [t for t in lab if idx[t]["pipe_rows"] < T]
        fig = sum(1 for t in sel if lab[t]["label"] in REAL)
        n = len(sel)
        lo, hi = wilson(fig, n) if n else (0, 0)
        ps = [r for r in pop if r["pipe_rows"] < T]
        tk = sum(r["render_tok"] for r in ps)
        nf = sum(1 for r in lab.values() if r["label"] in REAL)
        print(f"| {T if T < 10**8 else 'inf'} | {n} | {fig} | "
              f"{(fig/n*100 if n else 0):.0f}% ({lo*100:.0f}-{hi*100:.0f}) | "
              f"{fig/nf*100:.0f}% | {len(ps)} | {tk:,} | {tk/base_tok*100:+.1f}% |")
    print()

    tot_tok = sum(r["render_tok"] for r in pop)
    print(f"labelled {len(lab)}; population {len(pop)} pages, "
          f"{tot_tok:,} tokens first-order if all were rendered\n")
    print("| rule | fires (labelled) | figure | precision | recall | "
          "population | pop. tokens |")
    print("|---|--:|--:|--:|--:|--:|--:|")
    nfig = sum(1 for r in lab.values() if r["label"] in REAL)
    for name, f in rules.items():
        sel = [t for t in lab if f(idx[t])]
        fig = sum(1 for t in sel if lab[t]["label"] in REAL)
        n = len(sel)
        lo, hi = wilson(fig, n) if n else (0, 0)
        ps = [r for r in pop if f(r)]
        print(f"| {name} | {n} | {fig} | "
              f"{(fig/n*100 if n else 0):.0f}% ({lo*100:.0f}-{hi*100:.0f}) | "
              f"{fig/nfig*100:.0f}% | {len(ps)} | {sum(r['render_tok'] for r in ps):,} |")


# ------------------------------------------------------------------ variants
def variants():
    blob = json.loads((OUT / "firings.json").read_text())
    docs = blob["docs"]
    names = [n for n in ALL_POLICIES if n in docs[0]["variants"]]
    base = {"calls": sum(d["variants"]["baseline"]["calls"] for d in docs),
            "tokens": sum(d["variants"]["baseline"]["tokens"] for d in docs)}
    print(f"baseline over {len(docs)} documents: {base['calls']} vision calls, "
          f"{base['tokens']:,} routed image tokens\n")
    print("| variant | calls | Δcalls | tokens | Δtokens | Δ% | docs changed | "
          "collapse flips | scale-guard flips |")
    print("|---|--:|--:|--:|--:|--:|--:|--:|--:|")
    for nm in names:
        c = sum(d["variants"][nm]["calls"] for d in docs)
        t = sum(d["variants"][nm]["tokens"] for d in docs)
        ch = sum(1 for d in docs
                 if d["variants"][nm]["calls"] != d["variants"]["baseline"]["calls"]
                 or d["variants"][nm]["tokens"] != d["variants"]["baseline"]["tokens"])
        col = sum(1 for d in docs if d["variants"][nm]["collapsed"]
                  != d["variants"]["baseline"]["collapsed"])
        sg = sum(1 for d in docs if d["variants"][nm]["over_scale_guard"]
                 != d["variants"]["baseline"]["over_scale_guard"])
        print(f"| {nm} | {c} | {c-base['calls']:+} | {t:,} | "
              f"{t-base['tokens']:+,} | {(t-base['tokens'])/base['tokens']*100:+.2f}% "
              f"| {ch} | {col} | {sg} |")

    # The shipped pipeline also runs drop_batch_furniture at batch scope, which
    # `harvest()` alone never applies. Without this the baseline is 6,015 and
    # eval/nofigure.md's independently-derived 5,903 does not reproduce.
    print("\nafter drop_batch_furniture, per corpus (what a batch run really costs):")
    recs = []
    for i in range(SHARDS):
        recs += json.loads((PARTS / f"shard{i}.json").read_text())
    recs = [r for r in recs if r["status"] == "ok"]
    post = {}
    for nm in names:
        calls = tok = 0
        for c in CORPORA:
            rs = [{"status": "ok", "path": r["path"],
                   "page_sigs": r["variants"][nm]["page_sigs"],
                   "items": [dict(i) for i in r["variants"][nm]["items"]],
                   "dropped": []}
                  for r in recs if r["corpus"] == c]
            drop_batch_furniture(rs, batch_furniture(rs))
            calls += sum(len(r["items"]) for r in rs)
            tok += sum(i["tok"] for r in rs for i in r["items"])
        post[nm] = (calls, tok)
    b = post["baseline"]
    print("| variant | calls | Δcalls | tokens | Δtokens | Δ% |")
    print("|---|--:|--:|--:|--:|--:|")
    for nm in names:
        c, t = post[nm]
        print(f"| {nm} | {c} | {c-b[0]:+} | {t:,} | {t-b[1]:+,} | "
              f"{(t-b[1])/b[1]*100:+.2f}% |")

    print("\ncollapse (cost_guard) flips, per variant:")
    for nm in names[1:]:
        fl = [(d["path"], d["variants"]["baseline"]["collapsed"],
               d["variants"][nm]["collapsed"],
               d["variants"]["baseline"]["calls"], d["variants"][nm]["calls"],
               d["variants"]["baseline"]["tokens"], d["variants"][nm]["tokens"])
              for d in docs
              if d["variants"][nm]["collapsed"] != d["variants"]["baseline"]["collapsed"]]
        print(f"  {nm}: {len(fl)}")
        for f in fl:
            print(f"    {f[0]}  collapsed {f[1]}->{f[2]}  "
                  f"calls {f[3]}->{f[4]}  tok {f[5]:,}->{f[6]:,}")


# ------------------------------------------------------------------ validate
def validate(corpus, rule="proposed", cap=SAMPLE_MAX, seed=SEED):
    """Run a candidate rule over a holdout corpus and render every drop.

    "Drop" here means the OPPOSITE direction from strokegrid/nofigure: this
    rule ADDS renders, so what needs labelling is the added set, and a wasted
    add is a page with no real figure on it.
    """
    d = OUT / "holdout"
    (d / "pages" / rule / corpus).mkdir(parents=True, exist_ok=True)
    paths = sorted((ROOT / "corpus" / corpus).glob("*.pdf"))
    added, base_calls, cf_calls, nerr = [], 0, 0, 0
    for k, p in enumerate(paths):
        ctx = prefix(str(p))
        if ctx is None:
            nerr += 1
            continue
        raw_pages = {pp for e in ctx["seen"].values() for pp in e["pages"]}
        pol = variant_policies(raw_pages)[rule]
        b = route(ctx, POLICIES["baseline"])
        c = route(ctx, pol)
        base_calls += len(b["items"])
        cf_calls += len(c["items"])
        bset = {i["id"] for i in b["items"]}
        for it in c["items"]:
            if it["id"] not in bset and it["kind"] == "page_render":
                pg = ctx["doc"][it["page"] - 1]
                g = ctx["geoms"][it["page"] - 1]
                pm = (ctx["page_mds"][it["page"] - 1]
                      if it["page"] - 1 < len(ctx["page_mds"]) else "")
                added.append({"corpus": corpus, "doc": str(p.relative_to(ROOT)),
                              "file": p.name, "page": it["page"],
                              "reason": it["reason"],
                              "collapsed": bool(c["guard"]),
                              "pipe_rows": pm.count("\n|"),
                              "curves": g["curves"], "diagonals": g["diagonals"],
                              "paths": g["paths"]})
        ctx["doc"].close()
        if (k + 1) % 50 == 0:
            print(f"  {k+1}/{len(paths)}", file=sys.stderr, flush=True)

    # Only the pages the rule itself selects are of interest; a collapse can
    # add unrelated whole_document renders, so drop those from the drop set and
    # SAY SO rather than letting them dilute precision.
    sel = [a for a in added if a["reason"] not in ("whole_document",)]
    coll = len(added) - len(sel)
    rng = random.Random(seed)
    sample = sel if len(sel) <= cap else sorted(
        rng.sample(sorted(sel, key=lambda a: (a["doc"], a["page"])), cap),
        key=lambda a: (a["doc"], a["page"]))
    rows = []
    for i, a in enumerate(sample):
        tag = f"h{i+1:03d}"
        with fitz.open(str(ROOT / a["doc"])) as doc:
            doc[a["page"] - 1].get_pixmap(dpi=DPI).save(
                str(d / "pages" / rule / corpus / f"{tag}.png"))
        rows.append(dict(a, tag=tag))
    (d / f"index-{corpus}-{rule}.json").write_text(json.dumps(
        {"corpus": corpus, "rule": rule, "documents": len(paths),
         "unreadable": nerr, "baseline_calls": base_calls,
         "variant_calls": cf_calls, "added_total": len(added),
         "added_collapse_side_effects": coll, "added_selected": len(sel),
         "sampled": len(sample), "seed": seed, "candidates": rows}, indent=1))
    print(f"{corpus}: {len(paths)} docs ({nerr} unreadable), "
          f"{base_calls} -> {cf_calls} vision calls")
    print(f"  rule adds {len(sel)} renders ({coll} further pages arrive as "
          f"whole_document via a collapse and are excluded)")
    print(f"  rendered {len(rows)} -> {d/'pages'/rule/corpus}")


if __name__ == "__main__":
    a = sys.argv[1:]
    cmd = a[0] if a else ""
    if cmd == "shard":
        i, n = a[1].split("/")
        run_shard(int(i), int(n), "--check" in a)
    elif cmd == "costshard":
        i, n = a[1].split("/")
        run_shard(int(i), int(n), False, COSTPARTS, ["baseline", "proposed"],
                  False)
    elif cmd == "cost":
        cost_run()
    elif cmd == "measure":
        measure(reuse="--reuse" in a, check="--check" in a)
    elif cmd == "report":
        report(json.loads((OUT / "firings.json").read_text()))
    elif cmd == "render":
        render()
    elif cmd == "batches":
        batches(int(a[1]) if len(a) > 1 else 5)
    elif cmd == "score":
        score(merge="--no-merge" not in a)
    elif cmd == "holdout":
        holdout_score(*(a[1:2] or []))
    elif cmd == "features":
        features()
    elif cmd == "variants":
        variants()
    elif cmd == "validate":
        validate(a[1], *(a[2:3] or []))
    else:
        raise SystemExit(__doc__)
