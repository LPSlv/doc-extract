# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "pdf-inspector==0.2.6",
#   "pymupdf==1.28.0",
#   "pillow==11.3.0",
# ]
# ///
"""Price the multi-figure fix, and render its trigger set for labelling.

`eval/rejected-signals.md` records that 54.1% of routed rasters sit on pages
carrying more than one raster, and that a further 10.0% -- 134 items -- are a
lone raster on a page that ALSO shows vector figure signal. The one genuine
figure-QA v3 miss (w18b) lives in that second group. The obvious fix is to
render the whole page whenever a raster fires on a page with vector figure
signal, turning 134 crops into 134 page renders. Nobody had priced it.

This script prices it, on both sides.

    uv run eval/multifigure.py measure     # harvest, split, cost, cost_guard
    uv run eval/multifigure.py render      # PNGs for blind labelling
    uv run eval/multifigure.py batches     # split them for labellers
    uv run eval/multifigure.py score       # merge labels, rate, Wilson CI, triggers
    uv run eval/multifigure.py resolution  # what the swap costs the crop it drops
    uv run eval/multifigure.py shipped     # the same delta from the real PNGs
    uv run eval/multifigure.py variants    # swap vs. render-and-keep

`measure` re-harvests 688 PDFs (~10 min) and writes eval/multifigure/index.json.

DEFINITIONS, stated because every number below depends on them.

  routed raster       an item with kind == "raster" in harvest()'s post-
                      cost_guard item list, i.e. what convert.py actually
                      crops and ships.
  lone raster         the only routed raster whose item page is this page.
                      Item page is min(placement pages), which is how the
                      published 728/134/483 split counted them.
  vector figure       render_reason(page_geometry(pg)) is not None. This is
  signal              the same predicate the router itself uses to decide a
                      page needs eyes; it reproduces the published 134 exactly.

Corpora are datasheets, pmc, arxiv and papers -- the four the published split
came from -- harvested per corpus with batch_furniture applied per corpus,
which is what eval/bench.py does and therefore what the README's token totals
describe. (The published split's own run did not apply batch_furniture: it
reports 4,726 page renders where this reports 4,577. batch_furniture only ever
drops page renders, so every raster count is identical either way.)
"""
import collections, json, math, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills" / "doc-extract"))
import fitz
from harvest import (_harvest_all, batch_furniture, drop_batch_furniture,
                     page_geometry, render_reason, render_edge, NO_TEXT_EDGE_PX,
                     MAX_EDGE_PX)
from filters import _tok
from convert import _raster_pixmap

CORPORA = ("datasheets", "pmc", "arxiv", "papers")
OUT = ROOT / "eval" / "multifigure"
DPI = 130                      # mirrors eval/strokegrid_render.py


# --------------------------------------------------------------- token models
def render_tok(pg, edge):
    """cost_guard's price for a page render. int() truncation and all.

    This is deliberately the SHIPPED PREDICTION, not the shipped output:
    convert.py builds the pixmap with fitz.Matrix(scale, scale), whose width
    is a rounded product rather than a truncated one. The two differ by at
    most a pixel per side. eval/rejected-signals.md documents the far larger
    drift on the raster side; `--shipped` below measures both directly.
    """
    sc = edge / max(pg.rect.width, pg.rect.height)
    return _tok(int(pg.rect.width * sc), int(pg.rect.height * sc))


def item_tok(it, doc, edges):
    if it["kind"] == "raster":
        return _tok(*it["px"])
    pg = doc[it["page"] - 1]
    e = it.get("edge") or edges.get(it["page"] - 1) or NO_TEXT_EDGE_PX
    return render_tok(pg, e)


def whole_tok(doc):
    return sum(render_tok(pg, render_edge(pg)) for pg in doc)


def shipped_raster_tok(doc, it):
    """What convert.py's PNG really costs, mirroring _write_image."""
    pix = _raster_pixmap(doc, it)
    if pix.n - pix.alpha >= 4:
        pix = fitz.Pixmap(fitz.csRGB, pix)
    while max(pix.width, pix.height) > MAX_EDGE_PX * 2:
        pix.shrink(1)
    return _tok(pix.width, pix.height), (pix.width, pix.height)


def shipped_render_tok(pg, edge):
    sc = edge / max(pg.rect.width, pg.rect.height)
    pm = pg.get_pixmap(matrix=fitz.Matrix(sc, sc))
    return _tok(pm.width, pm.height), (pm.width, pm.height)


def crop_bbox(pg, xref):
    """The region _raster_pixmap clips, or None when it falls back to samples."""
    places = [i for i in pg.get_image_info(xrefs=True) if i.get("xref") == xref]
    if not places:
        return None
    info = max(places, key=lambda i: fitz.Rect(i["bbox"]).get_area())
    bbox = (fitz.Rect(info["bbox"]) * pg.rotation_matrix) & pg.rect
    if bbox.is_empty or bbox.width < 4 or bbox.height < 4:
        return None
    return bbox


# ------------------------------------------------------------------- measure
def measure():
    docs, totals = [], collections.Counter()
    for c in CORPORA:
        paths = sorted((ROOT / "corpus" / c).glob("*.pdf"))
        res = _harvest_all([str(p) for p in paths])
        res = drop_batch_furniture(res, batch_furniture(res))
        for p, r in zip(paths, res):
            totals["files"] += 1
            if r.get("status") != "ok":
                totals["skipped"] += 1
                continue
            docs.append((c, p, r))
        print(f"  harvested {c}: {len(paths)} files", file=sys.stderr)

    rows, per_doc = [], []
    for c, p, r in docs:
        with fitz.open(str(p)) as d:
            geoms = [page_geometry(pg) for pg in d]
            edges = {it["page"] - 1: it.get("edge")
                     for it in r["items"] if it["kind"] == "page_render"}
            rendered = {it["page"] for it in r["items"] if it["kind"] == "page_render"}
            # An xref can be drawn on several pages; an item's `page` is the
            # smallest of them. So "the item's page" and "the pages this crop
            # comes from" are not the same set, and the difference decides
            # whether rendering the page would subsume the crop at all.
            xref_pages = collections.defaultdict(set)
            for i, pg in enumerate(d):
                for im in pg.get_images(full=True):
                    xref_pages[im[0]].add(i + 1)
            toks = [item_tok(it, d, edges) for it in r["items"]]
            rasters = [it for it in r["items"] if it["kind"] == "raster"]
            bypage = collections.Counter(it["page"] for it in rasters)
            totals["pages"] += len(d)
            totals["calls"] += len(r["items"])
            totals["rasters"] += len(rasters)
            totals["renders"] += len(r["items"]) - len(rasters)
            totals["img_tok"] += sum(toks)
            collapsed = all(it["reason"] == "whole_document" for it in r["items"]) \
                and bool(r["items"])
            hits, seen_multi = [], set()
            for it, t in zip(r["items"], toks):
                if it["kind"] != "raster":
                    continue
                pg = d[it["page"] - 1]
                g = geoms[it["page"] - 1]
                sig = render_reason(g)
                lone = bypage[it["page"]] == 1
                if lone and sig:
                    totals["lone_signal"] += 1
                elif lone:
                    totals["lone_only"] += 1
                else:
                    totals["multi"] += 1
                    if sig:
                        # The rule as WORDED ("a raster fires on a page that
                        # also shows vector figure signal") covers these too.
                        # There the swap collapses N crops into ONE render, so
                        # its sign is not obvious in advance; price it.
                        totals["multi_signal"] += 1
                        totals["multi_crop_tok"] += t
                        if it["page"] not in seen_multi:
                            seen_multi.add(it["page"])
                            totals["multi_pages"] += 1
                            totals["multi_render_tok"] += render_tok(pg, render_edge(pg))
                if not (lone and sig):
                    continue
                pm = (r.get("page_markdown") or [""] * len(d))[it["page"] - 1] or ""
                e = render_edge(pg)
                bb = crop_bbox(pg, it["xref"])
                hits.append({
                    "corpus": c, "file": p.name, "path": str(p),
                    "page": it["page"], "id": it["id"], "xref": it["xref"],
                    "px": it["px"], "signal": sig,
                    "npages": len(d), "doc_calls": len(r["items"]),
                    "crop_tok": t, "render_tok": render_tok(pg, e), "edge": e,
                    "page_pt": [round(pg.rect.width, 1), round(pg.rect.height, 1)],
                    "bbox": [round(v, 1) for v in bb] if bb else None,
                    "bbox_frac": round(bb.get_area() / pg.rect.get_area(), 4) if bb else None,
                    "filter3": pm.count("\n|") >= 3,
                    "page_rendered": it["page"] in rendered,
                    "placed_on": sorted(xref_pages.get(it["xref"], {it["page"]})),
                    "co_rasters": sum(
                        1 for o in rasters if o is not it
                        and it["page"] in xref_pages.get(o["xref"], {o["page"]})),
                })
            if hits:
                per_doc.append({"path": str(p), "corpus": c, "calls": len(r["items"]),
                                "ours": sum(toks), "whole": whole_tok(d),
                                "npages": len(d), "collapsed": collapsed,
                                "pages": sorted({h["page"] for h in hits})})
            rows += hits

    rows.sort(key=lambda x: (x["corpus"], x["file"], x["page"]))
    for i, h in enumerate(rows):
        h["tag"] = f"m{i+1:03d}"

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "index.json").write_text(json.dumps(
        {"corpora": list(CORPORA), "dpi": DPI,
         "definition": "lone routed raster on a page where render_reason fires",
         "totals": dict(totals), "docs": per_doc, "rows": rows}, indent=1) + "\n")
    _report(dict(totals), rows, per_doc)


def _report(t, rows, per_doc):
    n = t["rasters"]
    print(f"\ndocuments harvested : {t['files']} ({t['skipped']} unreadable)")
    print(f"pages               : {t['pages']:,}")
    print(f"vision calls        : {t['calls']:,}  "
          f"({t['renders']:,} renders + {t['rasters']:,} rasters)")
    print(f"routed image tokens : {t['img_tok']:,}   [_tok model, native raster px]")
    print(f"\nrouted rasters      : {n}")
    print(f"  on pages with >1  : {t['multi']} ({t['multi']/n*100:.1f}%)")
    print(f"  lone + signal     : {t['lone_signal']} ({t['lone_signal']/n*100:.1f}%)")
    print(f"  lone, no signal   : {t['lone_only']} ({t['lone_only']/n*100:.1f}%)")
    # The proposal as worded -- "a raster fires on a page that also shows vector
    # figure signal" -- does not say "lone". Read literally it also fires on the
    # multi-raster half, which is a much larger set nobody has costed.
    print(f"  (multi-raster pages that ALSO show vector signal: "
          f"{t['multi_signal']} items on {t['multi_pages']} pages, out of scope "
          f"of the 134 but inside the rule as worded --")
    print(f"   collapsing those into one render per page: "
          f"{t['multi_crop_tok']:,} -> {t['multi_render_tok']:,} tokens, "
          f"{t['multi_render_tok']-t['multi_crop_tok']:+,}; "
          f"vision calls {t['multi_signal']-t['multi_pages']:+})")

    # An item whose own page is ALREADY rendered is not a multi-figure loss and
    # the fix would change nothing for it: the crop survives subsumption only
    # because the same xref is drawn on a second, unrendered page. The published
    # 134 counts those; the effective trigger set is smaller.
    stale = [r for r in rows if r["page_rendered"]]
    eff = [r for r in rows if not r["page_rendered"]]
    print(f"\n-- the trigger set --")
    print(f"  lone raster + vector signal        : {len(rows)}  (published 134)")
    print(f"  ...whose page is already rendered  : {len(stale)}")
    print(f"  EFFECTIVE trigger set              : {len(eff)}")
    print(f"  crop drawn on >1 page              : "
          f"{sum(1 for r in eff if len(r['placed_on']) > 1)}")
    print(f"  another routed raster is drawn on the same page : "
          f"{sum(1 for r in eff if r['co_rasters'])}")

    crop = sum(r["crop_tok"] for r in eff)
    rend = sum(r["render_tok"] for r in eff)
    print(f"\n-- first-order cost of the swap ({len(eff)} items) --")
    print(f"  crops today       : {crop:,}")
    print(f"  page renders      : {rend:,}")
    print(f"  delta             : {rend-crop:+,}  "
          f"({(rend-crop)/t['img_tok']*100:+.2f}% of routed image tokens)")

    print(f"\n-- cost_guard second order --")
    flip = []
    by_path = collections.defaultdict(list)
    for r in eff:
        by_path[r["path"]].append(r)
    for d in per_doc:
        hs = by_path.get(d["path"], [])
        new = d["ours"] + sum(h["render_tok"] - h["crop_tok"] for h in hs)
        d["ours_new"] = new
        if d["ours"] > d["whole"]:
            print(f"  !! already over whole: {d['path']}")
        if new > d["whole"]:
            flip.append(d)
    print(f"  documents holding a trigger : {len(per_doc)}")
    print(f"  documents that flip to whole_document : {len(flip)}")
    for d in flip:
        print(f"    {pathlib.Path(d['path']).name}  {d['npages']}pp  "
              f"ours {d['ours']:,} -> {d['ours_new']:,}  whole {d['whole']:,}"
              f"   calls {d['calls']} -> {d['npages']}")
    # cost_guard is a CEILING, not an amplifier: a document it collapses pays
    # `whole`, which is by definition less than the routed set that tripped it.
    # So this term is negative -- the opposite sign to the soft-mask case, where
    # RASTER_GRID un-collapsed pages and cancelled the saving.
    second = sum(d["whole"] - d["ours_new"] for d in flip)
    print(f"  token effect of collapse    : {second:+,}")
    print(f"  vision calls                : {sum(d['npages']-d['calls'] for d in flip):+}")
    print(f"  TOTAL delta                 : {rend-crop+second:+,}  "
          f"({(rend-crop+second)/t['img_tok']*100:+.2f}%)")

    print(f"\n-- composition of the {len(eff)} effective triggers --")
    print("  signal :", dict(collections.Counter(r["signal"] for r in eff)))
    print("  corpus :", dict(collections.Counter(r["corpus"] for r in eff)))
    print("  filter3 ('the extractor won') suppressed the render :",
          sum(r["filter3"] for r in eff), "of", len(eff))
    fr = sorted(r["bbox_frac"] for r in eff if r["bbox_frac"] is not None)
    if fr:
        print(f"  crop as a share of its page: median {fr[len(fr)//2]:.1%}, "
              f"90th pct {fr[int(len(fr)*0.9)]:.1%}")


# -------------------------------------------------------------------- render
def render():
    """One PNG per trigger: the whole page, with the shipped crop outlined.

    A labeller cannot judge 'does the crop lose figure content' from the crop
    alone -- the question is about what surrounds it. Drawing the crop's own
    rectangle on the page render puts both facts in one image, which halves
    what each labeller has to hold and removes any chance of mispairing a crop
    with the wrong page.
    """
    from PIL import Image, ImageDraw
    import io
    idx = json.loads((OUT / "index.json").read_text())
    idx["rows"] = [r for r in idx["rows"] if not r["page_rendered"]]
    (OUT / "pages").mkdir(parents=True, exist_ok=True)
    z = DPI / 72.0
    cur, d = None, None
    for r in idx["rows"]:
        if r["path"] != cur:                 # rows are grouped by file already
            if d is not None:
                d.close()
            d, cur = fitz.open(r["path"]), r["path"]
        pg = d[r["page"] - 1]
        pm = pg.get_pixmap(dpi=DPI)
        im = Image.open(io.BytesIO(pm.tobytes("png"))).convert("RGB")
        if r["bbox"]:
            x0, y0, x1, y1 = [v * z for v in r["bbox"]]
            dr = ImageDraw.Draw(im)
            for w in range(4):
                dr.rectangle([x0 - w, y0 - w, x1 + w, y1 + w], outline=(220, 20, 30))
        im.save(OUT / "pages" / f"{r['tag']}.png")
    if d is not None:
        d.close()
    n_bb = sum(1 for r in idx["rows"] if r["bbox"])
    print(f"rendered {len(idx['rows'])} pages at {DPI} dpi -> {OUT/'pages'}")
    print(f"  crop rectangle drawn on {n_bb}; "
          f"{len(idx['rows'])-n_bb} have no page placement (whole-image fallback)")


# ------------------------------------------------------------------- batches
NBATCH = 4


def batches():
    """Split the trigger set into labelling batches. Tag and PNG path only.

    Deliberately no file name, corpus or page number: a labeller who can see
    that a page came from a TI datasheet can guess what the rest of the page
    holds without looking, and this repo has already published one number that
    a labeller's prior knowledge would have moved.
    """
    idx = json.loads((OUT / "index.json").read_text())
    idx["rows"] = [r for r in idx["rows"] if not r["page_rendered"]]
    tags = [r["tag"] for r in idx["rows"]]
    per = -(-len(tags) // NBATCH)
    for b in range(NBATCH):
        chunk = tags[b * per:(b + 1) * per]
        (OUT / f"batch{b+1}.tsv").write_text(
            "tag\tpng\n" + "".join(
                f"{t}\t{OUT/'pages'/(t+'.png')}\n" for t in chunk))
        print(f"batch{b+1}.tsv: {len(chunk)} pages ({chunk[0]}..{chunk[-1]})")


# --------------------------------------------------------------------- score
def wilson(k, n, z=1.96):
    if not n:
        return float("nan"), float("nan")
    p, d = k / n, 1 + z * z / n
    c = p + z * z / (2 * n)
    s = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return (c - s) / d, (c + s) / d


def _read_labels(p, want="label"):
    """Read a labeller's TSV BY COLUMN NAME.

    eval/strokegrid_holdout_score.py read it positionally the first time and
    picked up `page` as the label, reporting 0% on a set that was unanimously
    clean. Not repeating that.
    """
    lines = p.read_text().strip().splitlines()
    head = lines[0].split("\t")
    ti, li = head.index("tag"), head.index(want)
    out = {}
    for l in lines[1:]:
        f = l.split("\t")
        if len(f) > li and f[ti].strip():
            out[f[ti].strip()] = f[li].strip()
    return out


def score():
    idx = json.loads((OUT / "index.json").read_text())
    idx["rows"] = [r for r in idx["rows"] if not r["page_rendered"]]
    rows = {r["tag"]: r for r in idx["rows"]}
    files = sorted(OUT.glob("labels-*.tsv"))
    if not files:
        sys.exit("no eval/multifigure/labels-*.tsv yet")
    per = {f.name: _read_labels(f) for f in files}
    notes = {f.name: _read_labels(f, "note") for f in files}
    tags = sorted(rows)
    missing = [t for t in tags if not all(t in p for p in per.values())]
    if missing:
        print(f"WARNING unlabelled by some labeller: {' '.join(missing)}", file=sys.stderr)

    merged = []
    for t in tags:
        votes = [p[t] for p in per.values() if t in p]
        if not votes:
            continue
        c = collections.Counter(votes)
        top, k = c.most_common(1)[0]
        # Ties break AGAINST the change: a page is only a loss when a majority
        # of labellers say so. With an even split, `sufficient` wins.
        if k * 2 <= len(votes) and top == "loses":
            top = "sufficient"
        note = next((notes[f][t] for f in sorted(per)
                     if per[f].get(t) == top and notes[f].get(t)), "")
        merged.append({"tag": t, "label": top, "agree": f"{k}/{len(votes)}",
                       "note": note,
                       **{k2: rows[t][k2] for k2 in
                          ("corpus", "file", "page", "signal", "bbox_frac")}})

    # Where _raster_pixmap finds no page placement it falls back to the stored
    # samples, `render` draws no rectangle, and there is no region on the page
    # to reason about. Those pages are unjudgeable BY CONSTRUCTION, and are
    # excluded on that fact rather than on the label: on m015 one labeller
    # answered `norect` and two answered from the figure's own red ink, which
    # is a judgement about nothing. Dropping them by label would have kept it.
    nore = [m["tag"] for m in merged if not rows[m["tag"]]["bbox"]]
    # `judgeable` is the column that stops a reader counting 66 losses out of
    # 131.
    for m in merged:
        m["judgeable"] = m["tag"] not in nore
    cols = ["tag", "corpus", "file", "page", "signal", "bbox_frac",
            "judgeable", "label", "agree", "note"]
    (OUT / "labels.tsv").write_text(
        "\t".join(cols) + "\n" +
        "".join("\t".join(str(m[c]) for c in cols) + "\n" for m in merged))

    lab = {m["tag"]: m["label"] for m in merged if m["tag"] not in nore}
    n = len(lab)
    loses = sum(1 for v in lab.values() if v == "loses")
    lo, hi = wilson(loses, n)
    print(f"labellers        : {len(per)} ({', '.join(sorted(per))})")
    print(f"labelled         : {len(merged)} of {len(tags)}"
          f"   ({len(nore)} unjudgeable, no page placement: "
          f"{' '.join(nore) or '-'})")
    una = sum(1 for m in merged if m["agree"].split('/')[0] == m["agree"].split('/')[1])
    print(f"unanimous        : {una}/{len(merged)} ({una/len(merged)*100:.0f}%)"
          f"   -- see the caveat: three runs of one model are not three labellers")
    print(f"documents        : {len({rows[t]['file'] for t in lab})} in the trigger set,"
          f" {len({rows[t]['file'] for t in lab if lab[t]=='loses'})} with a loss")
    print(f"LOSES figure content outside the crop : {loses}/{n} = {loses/n*100:.1f}%"
          f"   (95% Wilson {lo*100:.0f}-{hi*100:.0f}%)")

    print("\nby signal:")
    for s in sorted({r["signal"] for r in rows.values()}):
        ts = [t for t in lab if rows[t]["signal"] == s]
        if ts:
            k = sum(1 for t in ts if lab[t] == "loses")
            print(f"  {s:<12} {k}/{len(ts)}")
    print("by corpus:")
    for c in CORPORA:
        ts = [t for t in lab if rows[t]["corpus"] == c]
        if ts:
            k = sum(1 for t in ts if lab[t] == "loses")
            print(f"  {c:<12} {k}/{len(ts)}")

    print("\n-- narrower triggers, scored against the same labels --")
    print("   tokens include cost_guard: a trigger set is re-tested against each")
    print("   document's whole-render price, and a document that flips pays that")
    print("   instead, which is a CEILING and so damps the increase.")
    print(f"\n{'trigger':<42}{'fires':>6}{'gets':>6}{'recall':>8}{'prec':>6}"
          f"{'tokens':>10}{'per fig':>9}")
    for name, fn in TRIGGERS.items():
        fire = [t for t in lab if fn(rows[t])]
        if not fire:
            continue
        k = sum(1 for t in fire if lab[t] == "loses")
        dt = _delta_with_guard(idx, rows, fire)
        print(f"{name:<42}{len(fire):>6}{k:>6}{k/max(1,loses)*100:>7.0f}%"
              f"{k/len(fire)*100:>5.0f}%{dt:>+10,}{dt/max(1,k):>+9,.0f}")


def variants():
    """The three things "render the page" can mean, priced.

    The proposal says render the page INSTEAD of cropping. `resolution` shows
    what that costs the raster you already had. Keeping both is the version
    that loses nothing -- and it is a different, larger bill, so it should not
    be quoted as if it were the proposal's.
    """
    idx = json.loads((OUT / "index.json").read_text())
    rows = {r["tag"]: r for r in idx["rows"] if not r["page_rendered"]}
    tags = list(rows)
    img = idx["totals"]["img_tok"]
    calls = idx["totals"]["calls"]
    swap = _delta_with_guard(idx, rows, tags)
    add = _delta_with_guard(idx, rows, tags, keep_crop=True)
    print(f"routed image tokens      : {img:,}   vision calls: {calls:,}")
    print(f"{'variant':<46}{'tokens':>10}{'share':>8}{'calls':>8}")
    print(f"{'swap: render instead of crop':<46}{swap:>+10,}"
          f"{swap/img*100:>7.2f}%{'+10':>8}")
    print(f"{'additive: render AND keep the crop':<46}{add:>+10,}"
          f"{add/img*100:>7.2f}%{'+'+str(len(tags)):>8}")
    print(f"\n(the +10 calls in the swap row are cost_guard collapses, not new "
          f"items:\n the swap is call-neutral by construction.)")


def _delta_with_guard(idx, rows, fire, keep_crop=False):
    """Token delta of swapping exactly `fire`, cost_guard re-applied per document."""
    by_path = collections.defaultdict(list)
    for t in fire:
        by_path[rows[t]["path"]].append(t)
    total = 0
    for d in idx["docs"]:
        ts = by_path.get(d["path"])
        if not ts:
            continue
        raw = sum(rows[t]["render_tok"] - (0 if keep_crop else rows[t]["crop_tok"])
                  for t in ts)
        total += min(raw, d["whole"] - d["ours"])   # cost_guard caps at `whole`
    return total


TRIGGERS = {
    "any vector figure signal (the proposal)": lambda r: True,
    "signal is curves or diagonals": lambda r: r["signal"] in ("curves", "diagonals"),
    "crop covers <30% of the page": lambda r: (r["bbox_frac"] or 1.0) < 0.30,
    "curves/diagonals AND crop <30%": lambda r: r["signal"] in ("curves", "diagonals")
        and (r["bbox_frac"] or 1.0) < 0.30,
    "render costs no more than the crop": lambda r: r["render_tok"] <= r["crop_tok"],
    "render costs at most 1.5x the crop": lambda r: r["render_tok"] <= 1.5 * r["crop_tok"],
    "render at most 1.5x AND curves/diagonals": lambda r: r["render_tok"] <= 1.5 * r["crop_tok"]
        and r["signal"] in ("curves", "diagonals"),
}


# ----------------------------------------------------------------- resolution
def resolution():
    """What the swap does to the raster that is ALREADY being read.

    The labelling asks what a page render would ADD. It cannot see what the
    same render takes away, and _raster_pixmap exists precisely because that
    is not nothing: it scales a crop to the image's own pixel count rather
    than the placement's, with the comment "capping this at a fixed multiple
    of the placement silently degrades a high-resolution image that happens to
    be placed small, which is common for schematics and scope captures".

    A page render caps at the placement by construction. So for every trigger
    this measures the linear scale factor the routed raster suffers:

        (placement width in the page render) / (crop width shipped today)
    """
    idx = json.loads((OUT / "index.json").read_text())
    idx["rows"] = [r for r in idx["rows"] if not r["page_rendered"]]
    ratios = []
    for r in idx["rows"]:
        if not r["bbox"]:
            continue
        with fitz.open(r["path"]) as d:
            _, (cw, ch) = shipped_raster_tok(
                d, {"page": r["page"], "xref": r["xref"], "kind": "raster"})
        pw, ph = r["page_pt"]
        sc = r["edge"] / max(pw, ph)
        x0, y0, x1, y1 = r["bbox"]
        ratios.append((r["tag"], ((x1 - x0) * sc) / cw))
    ratios.sort(key=lambda x: x[1])
    v = [x[1] for x in ratios]
    print(f"routed rasters measured : {len(v)}")
    print(f"linear resolution of the raster after the swap, as a fraction of today's crop")
    for q in (0, 10, 25, 50, 75, 90, 100):
        print(f"  p{q:<3} {v[min(len(v)-1, int(len(v)*q/100))]:.2f}x")
    for th in (1.0, 0.75, 0.5, 0.25):
        k = sum(1 for x in v if x < th)
        print(f"  below {th:.2f}x : {k} ({k/len(v)*100:.0f}%)")
    print(f"\nworst 6: " + ", ".join(f"{t} {x:.2f}x" for t, x in ratios[:6]))


# -------------------------------------------------------------------- shipped
def shipped():
    """The same delta priced from the PNGs convert.py really writes.

    rejected-signals.md records that cost_guard's `_tok(*it["px"])` underprices
    the shipped raster by 0.6% in aggregate and up to 58% per item, because
    _raster_pixmap clip-renders the placement isotropically. The swap REMOVES
    raster tokens, so that bias inflates the modelled cost of the change; this
    measures how much.
    """
    idx = json.loads((OUT / "index.json").read_text())
    idx["rows"] = [r for r in idx["rows"] if not r["page_rendered"]]
    mc = mr = sc = sr = 0
    for r in idx["rows"]:
        with fitz.open(r["path"]) as d:
            it = {"page": r["page"], "xref": r["xref"], "kind": "raster"}
            st, dim = shipped_raster_tok(d, it)
            rt, rdim = shipped_render_tok(d[r["page"] - 1], r["edge"])
        mc += r["crop_tok"]; mr += r["render_tok"]; sc += st; sr += rt
    print(f"{'':<22}{'crops':>12}{'renders':>12}{'delta':>12}")
    print(f"{'modelled (_tok/px)':<22}{mc:>12,}{mr:>12,}{mr-mc:>+12,}")
    print(f"{'shipped (real PNGs)':<22}{sc:>12,}{sr:>12,}{sr-sc:>+12,}")
    print(f"{'model error':<22}{(sc-mc)/mc*100:>11.1f}%{(sr-mr)/mr*100:>11.1f}%")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "measure"
    {"measure": measure, "render": render, "batches": batches,
     "score": score, "shipped": shipped,
     "resolution": resolution, "variants": variants}[cmd]()
