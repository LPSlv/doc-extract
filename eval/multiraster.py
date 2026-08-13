# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "pdf-inspector==0.2.6",
#   "pymupdf==1.28.0",
#   "pillow==11.3.0",
# ]
# ///
"""The multi-raster half of the multi-figure rule, priced and labelled.

`eval/multifigure.md` rejected "render the whole page when a raster fires on a
page that also shows vector figure signal" -- but it only measured the LONE
half (131 items, +0.99% tokens, and a median 0.27x linear resolution loss on
the raster already being read). The rule as worded does not say *lone*. Its
other half is 308 routed rasters on 96 pages where collapsing to one render per
page is, per `eval/multifigure/index.json`, -34,044 tokens and -212 calls.

Cheaper AND fewer calls is the opposite sign to the half that was rejected, so
the benefit was never labelled. This script does that, and re-derives the cost
from scratch rather than trusting the number in index.json.

    uv run eval/multiraster.py measure     # harvest, split, first-order cost
    uv run eval/multiraster.py variant     # end-to-end re-harvest with the rule
    uv run eval/multiraster.py resolution  # what the collapse costs each crop
    uv run eval/multiraster.py render      # PNGs for blind labelling
    uv run eval/multiraster.py batches
    uv run eval/multiraster.py score

DEFINITIONS. Two of them, because the published 308/96 uses the first and only
the second can be implemented:

  by-item-page    a routed raster's `page` is min(its placement pages). The
                  published split counted "rasters on this page" that way.
  by-placement    the rasters actually DRAWN on this page. A page render
                  subsumes a raster only when EVERY page the raster is drawn on
                  is rendered (harvest.py's subsumption rule), so this is the
                  set that decides what a collapse really removes.

Reuses eval/multifigure.py's measurement code rather than restating it.
"""
import collections, json, math, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills" / "doc-extract"))
sys.path.insert(0, str(ROOT / "eval"))
import fitz
from harvest import (_harvest_all, batch_furniture, drop_batch_furniture,
                     page_geometry, render_reason, render_edge, box_templates,
                     cost_guard, UBIQUITY, STROKE_MIN_FRAC, INK_MIN)
from filters import _tok
from multifigure import (render_tok, item_tok, whole_tok, crop_bbox,
                         shipped_raster_tok, wilson, _read_labels)

CORPORA = ("datasheets", "pmc", "arxiv", "papers")
OUT = ROOT / "eval" / "multiraster"
DPI = 130                      # mirrors eval/strokegrid_render.py


def _sig(g):
    return (g["curves"], g["diagonals"], g["axis_h"], g["axis_v"])


def measure():
    """Re-derive the multi-raster split and its first-order price.

    Nothing here reads eval/multifigure/index.json: the point is to reproduce
    308 / 96 / 150,934 / 116,890 independently, and then to ask what those
    numbers left out.
    """
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

    pages, per_doc = [], []
    for c, p, r in docs:
        with fitz.open(str(p)) as d:
            geoms = [page_geometry(pg) for pg in d]
            edges = {it["page"] - 1: it.get("edge")
                     for it in r["items"] if it["kind"] == "page_render"}
            rendered = {it["page"] for it in r["items"] if it["kind"] == "page_render"}
            xref_pages = collections.defaultdict(set)
            for i, pg in enumerate(d):
                for im in pg.get_images(full=True):
                    xref_pages[im[0]].add(i + 1)
            toks = [item_tok(it, d, edges) for it in r["items"]]
            rasters = [it for it in r["items"] if it["kind"] == "raster"]
            tok_of = {it["id"]: t for it, t in zip(r["items"], toks)
                      if it["kind"] == "raster"}
            byitem = collections.Counter(it["page"] for it in rasters)
            byplace = collections.Counter(
                q for it in rasters for q in xref_pages.get(it["xref"], {it["page"]}))
            totals["pages"] += len(d)
            totals["calls"] += len(r["items"])
            totals["rasters"] += len(rasters)
            totals["img_tok"] += sum(toks)

            # ---- the published definition, reproduced exactly ---------------
            for it in rasters:
                if byitem[it["page"]] > 1 and render_reason(geoms[it["page"] - 1]):
                    totals["multi_signal"] += 1
                    totals["multi_crop_tok"] += tok_of[it["id"]]
            for q in sorted({it["page"] for it in rasters}):
                if byitem[q] > 1 and render_reason(geoms[q - 1]):
                    totals["multi_pages"] += 1
                    totals["multi_render_tok"] += render_tok(d[q - 1], render_edge(d[q - 1]))

            # ---- the same set, per page, with what it leaves out -------------
            counts = collections.Counter(_sig(gg) for gg in geoms)
            templ = {k for k, n in counts.items()
                     if len(d) > 2 and n / len(d) > UBIQUITY}
            boxes = box_templates(geoms)
            hits = []
            for q in sorted({it["page"] for it in rasters}):
                g = geoms[q - 1]
                sigl = render_reason(g)
                if byitem[q] <= 1 or not sigl:
                    continue
                pg = d[q - 1]
                pm = (r.get("page_markdown") or [""] * len(d))[q - 1] or ""
                # which suppressor stopped this page being rendered already
                why_not = None
                if q in rendered:
                    why_not = "already_rendered"
                elif pm.count("\n|") >= 3:
                    why_not = "filter3"
                elif (_sig(g) in templ and g["stroke_frac"] < STROKE_MIN_FRAC
                        and g["ink"] < INK_MIN and g["rects"] < 8):
                    why_not = "vector_furniture"
                elif sigl == "stroke_grid" and g["vx_pos"] in boxes:
                    why_not = "boxed_text"
                else:
                    why_not = "unknown"
                on_item = [it for it in rasters if it["page"] == q]
                on_place = [it for it in rasters
                            if q in xref_pages.get(it["xref"], {it["page"]})]
                # what a render of THIS page really subsumes: a raster whose
                # every placement page is rendered (harvest.py's own rule)
                newr = rendered | {q}
                gone = [it for it in on_place
                        if all(x in newr for x in xref_pages.get(it["xref"], {it["page"]}))]
                bbs = []
                for it in on_place:
                    bb = crop_bbox(pg, it["xref"])
                    bbs.append({"id": it["id"], "xref": it["xref"], "px": it["px"],
                                "tok": tok_of[it["id"]],
                                "bbox": [round(v, 1) for v in bb] if bb else None,
                                "bbox_frac": round(bb.get_area() / pg.rect.get_area(), 4)
                                if bb else None,
                                "subsumed": it in gone,
                                "placed_on": sorted(xref_pages.get(it["xref"], {it["page"]}))})
                hits.append({
                    "corpus": c, "file": p.name, "path": str(p), "page": q,
                    "signal": sigl, "why_not_rendered": why_not,
                    "npages": len(d), "doc_calls": len(r["items"]),
                    "n_item": len(on_item), "n_placed": len(on_place),
                    "n_subsumed": len(gone),
                    "crop_tok_item": sum(tok_of[it["id"]] for it in on_item),
                    "crop_tok_gone": sum(tok_of[it["id"]] for it in gone),
                    "render_tok": render_tok(pg, render_edge(pg)),
                    "edge": render_edge(pg),
                    "page_pt": [round(pg.rect.width, 1), round(pg.rect.height, 1)],
                    "rasters": bbs,
                })
            if hits:
                per_doc.append({"path": str(p), "corpus": c, "calls": len(r["items"]),
                                "ours": sum(toks), "whole": whole_tok(d),
                                "npages": len(d),
                                "pages": sorted(h["page"] for h in hits)})
            pages += hits

    pages.sort(key=lambda x: (x["corpus"], x["file"], x["page"]))
    for i, h in enumerate(pages):
        h["tag"] = f"r{i+1:03d}"

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "index.json").write_text(json.dumps(
        {"corpora": list(CORPORA), "dpi": DPI,
         "definition": "pages with >1 routed raster (by item page) where render_reason fires",
         "totals": dict(totals), "docs": per_doc, "pages": pages}, indent=1) + "\n")
    _report(dict(totals), pages)


def report():
    """Re-print `measure`'s report from the artifact, without re-harvesting."""
    idx = json.loads((OUT / "index.json").read_text())
    _report(idx["totals"], idx["pages"])


def _report(t, pages):
    print(f"\ndocuments harvested : {t['files']} ({t.get('skipped', 0)} unreadable)")
    print(f"pages               : {t['pages']:,}")
    print(f"vision calls        : {t['calls']:,}")
    print(f"routed rasters      : {t['rasters']:,}")
    print(f"routed image tokens : {t['img_tok']:,}")
    print("\n-- reproducing eval/multifigure/index.json's multi-raster totals --")
    print(f"  multi_signal      : {t['multi_signal']}   (published 308)")
    print(f"  multi_pages       : {t['multi_pages']}   (published 96)")
    print(f"  multi_crop_tok    : {t['multi_crop_tok']:,}   (published 150,934)")
    print(f"  multi_render_tok  : {t['multi_render_tok']:,}   (published 116,890)")
    print(f"  delta             : {t['multi_render_tok']-t['multi_crop_tok']:+,}"
          f"   (published -34,044)")
    print(f"  calls             : {t['multi_pages']-t['multi_signal']:+}"
          f"   (published -212)")

    wn = collections.Counter(p["why_not_rendered"] for p in pages)
    print(f"\n-- why these pages are not rendered already --")
    for k, v in wn.most_common():
        print(f"  {k:<18} {v}")
    eff = [p for p in pages if p["why_not_rendered"] != "already_rendered"]
    print(f"\n-- effective set (dropping pages that already carry a render) --")
    print(f"  pages                 : {len(eff)}")
    print(f"  rasters by item page  : {sum(p['n_item'] for p in eff)}")
    print(f"  rasters placed here   : {sum(p['n_placed'] for p in eff)}")
    print(f"  rasters really subsumed by the collapse : {sum(p['n_subsumed'] for p in eff)}")
    ci = sum(p["crop_tok_item"] for p in eff)
    cg = sum(p["crop_tok_gone"] for p in eff)
    rt = sum(p["render_tok"] for p in eff)
    print(f"\n  crops removed, by item page   : {ci:,}")
    print(f"  crops removed, really subsumed: {cg:,}")
    print(f"  page renders added            : {rt:,}")
    print(f"  FIRST ORDER (honest)          : {rt-cg:+,}"
          f"  ({(rt-cg)/t['img_tok']*100:+.2f}% of routed image tokens)")
    print(f"  vision calls (honest)         : {len(eff)-sum(p['n_subsumed'] for p in eff):+}")
    print(f"\n  signal :", dict(collections.Counter(p["signal"] for p in eff)))
    print(f"  corpus :", dict(collections.Counter(p["corpus"] for p in eff)))
    n = collections.Counter(p["n_placed"] for p in eff)
    print(f"  rasters per page :", dict(sorted(n.items())))


# ---------------------------------------------------------------- cost_guard
def guard():
    """Second-order cost, by DRIVING cost_guard() rather than re-deriving it.

    The first-order term is arithmetic on one page at a time. cost_guard is a
    per-document threshold, so removing crops and adding renders can move a
    document across it in either direction. On the lone half the term was
    -1,051 (a document that trips the guard pays `whole`, a ceiling). Here the
    change is token-NEGATIVE, so it can only ever pull a document back from the
    boundary -- but "can only" is an argument, and this measures it.

    A document that is ALREADY collapsed contributes no routed raster, so it
    cannot be in the candidate set at all; the only documents that can move are
    ones currently routing, and they can only move by getting cheaper.
    """
    idx = json.loads((OUT / "index.json").read_text())
    eff = [p for p in idx["pages"] if p["why_not_rendered"] != "already_rendered"]
    bypath = collections.defaultdict(list)
    for p in eff:
        bypath[p["path"]].append(p)

    first = second = 0
    flips_in = flips_out = 0
    dcalls = 0
    for path, ps in sorted(bypath.items()):
        # rebuild this document's routed item list, then apply the rule to it
        res = _harvest_all([path])[0]
        assert res["status"] == "ok", path
        with fitz.open(path) as d:
            edges = {it["page"] - 1: it.get("edge")
                     for it in res["items"] if it["kind"] == "page_render"}
            drop = {b["id"] for p in ps for b in p["rasters"] if b["subsumed"]}
            add = {p["page"]: p["edge"] for p in ps}
            new = [it for it in res["items"] if it["id"] not in drop]
            new += [{"id": f"p{q:03d}-render", "page": q, "kind": "page_render",
                     "reason": "multi_raster_figure", "edge": e, "description": None}
                    for q, e in sorted(add.items())]
            new.sort(key=lambda it: (it["page"], it["id"]))
            nedges = dict(edges)
            for q, e in add.items():
                nedges[q - 1] = e
            # cost_guard itself, on both item lists, with the real document
            old_items, old_g = cost_guard(list(res["items"]), d, edges)
            new_items, new_g = cost_guard(new, d, nedges)
            ot = sum(item_tok(it, d, edges) for it in old_items)
            nt = sum(item_tok(it, d, nedges) for it in new_items)
        raw = sum(p["render_tok"] for p in ps) - sum(p["crop_tok_gone"] for p in ps)
        first += raw
        second += (nt - ot) - raw
        dcalls += len(new_items) - len(old_items)
        if new_g and not old_g:
            flips_in += 1
            print(f"  FLIPS INTO whole_document: {pathlib.Path(path).name} {new_g}")
        if old_g and not new_g:
            flips_out += 1
            print(f"  flips OUT of whole_document: {pathlib.Path(path).name} {old_g}")
        if old_g:
            print(f"  (already collapsed: {pathlib.Path(path).name})")
    img = idx["totals"]["img_tok"]
    calls = idx["totals"]["calls"]
    print(f"\ndocuments holding a candidate page : {len(bypath)}")
    print(f"  flip INTO whole_document  : {flips_in}")
    print(f"  flip OUT of whole_document: {flips_out}")
    print(f"  first order   : {first:+,}")
    print(f"  second order  : {second:+,}")
    print(f"  TOTAL         : {first+second:+,}  "
          f"({(first+second)/img*100:+.2f}% of {img:,} routed image tokens)")
    print(f"  vision calls  : {dcalls:+}  (of {calls:,})")


# ----------------------------------------------------------------- resolution
def resolution():
    """What the collapse does to each raster it removes.

    Identical arithmetic to eval/multifigure.py's `resolution`, so the two
    halves are directly comparable:

        (placement width in the page render) / (crop width shipped today)
    """
    idx = json.loads((OUT / "index.json").read_text())
    eff = [p for p in idx["pages"] if p["why_not_rendered"] != "already_rendered"]
    ratios, perpage = [], []
    for p in eff:
        pw, ph = p["page_pt"]
        sc = p["edge"] / max(pw, ph)
        with fitz.open(p["path"]) as d:
            for b in p["rasters"]:
                if not b["subsumed"] or not b["bbox"]:
                    continue
                _, (cw, ch) = shipped_raster_tok(
                    d, {"page": p["page"], "xref": b["xref"], "kind": "raster"})
                x0, y0, x1, y1 = b["bbox"]
                ratios.append((f"{p['tag']}/{b['id']}", ((x1 - x0) * sc) / cw))
        perpage.append(p)
    ratios.sort(key=lambda x: x[1])
    (OUT / "ratios.json").write_text(json.dumps(dict(ratios), indent=1) + "\n")
    v = [x[1] for x in ratios]
    print(f"rasters measured : {len(v)}  (subsumed, with a page placement)")
    print("linear resolution after the collapse, as a fraction of today's crop")
    for q in (0, 10, 25, 50, 75, 90, 100):
        print(f"  p{q:<3} {v[min(len(v)-1, int(len(v)*q/100))]:.2f}x")
    for th in (1.0, 0.75, 0.5, 0.25):
        k = sum(1 for x in v if x < th)
        print(f"  below {th:.2f}x : {k} ({k/len(v)*100:.0f}%)")
    print("\nworst 6: " + ", ".join(f"{t} {x:.2f}x" for t, x in ratios[:6]))
    print("best  6: " + ", ".join(f"{t} {x:.2f}x" for t, x in ratios[-6:]))
    fr = sorted(b["bbox_frac"] for p in eff for b in p["rasters"]
                if b["subsumed"] and b["bbox_frac"] is not None)
    print(f"\ncrop as a share of its page: median {fr[len(fr)//2]:.1%}, "
          f"p90 {fr[int(len(fr)*0.9)]:.1%}")
    tot = sorted(sum(b["bbox_frac"] or 0 for b in p["rasters"] if b["subsumed"])
                 for p in eff)
    print(f"all crops on a page, share of the page: median {tot[len(tot)//2]:.1%}, "
          f"p90 {tot[int(len(tot)*0.9)]:.1%}")


# -------------------------------------------------------------------- render
def render():
    """One PNG per candidate page, every shipped crop outlined in red.

    NOT at 130 dpi, and the deviation from eval/strokegrid_render.py and
    eval/multifigure.py is the point. Those two asked only what lies OUTSIDE
    the box, a question the page's own resolution does not bear on. Half the
    question here is whether the replacement image still RESOLVES what is
    inside the boxes, and the replacement is a render at `render_edge(pg)` --
    which on 81 of these 94 pages is SMALLER than a 130 dpi render, median
    0.71x linear, about half the pixels. Labelling a 130 dpi image would have
    asked "is this legible" of a picture sharper than the one that ships, in
    the direction that flatters the change.

    So each PNG is exactly the pixmap convert.py would emit for this page,
    plus the rectangles. What the labeller sees is what the model would see.
    """
    from PIL import Image, ImageDraw
    import io
    idx = json.loads((OUT / "index.json").read_text())
    eff = [p for p in idx["pages"] if p["why_not_rendered"] != "already_rendered"]
    (OUT / "pages").mkdir(parents=True, exist_ok=True)
    cur, d, nb = None, None, 0
    for p in eff:
        if p["path"] != cur:
            if d is not None:
                d.close()
            d, cur = fitz.open(p["path"]), p["path"]
        pg = d[p["page"] - 1]
        z = p["edge"] / max(pg.rect.width, pg.rect.height)
        pm = pg.get_pixmap(matrix=fitz.Matrix(z, z))
        im = Image.open(io.BytesIO(pm.tobytes("png"))).convert("RGB")
        dr = ImageDraw.Draw(im)
        for b in p["rasters"]:
            if not b["bbox"] or not b["subsumed"]:
                continue
            nb += 1
            x0, y0, x1, y1 = [v * z for v in b["bbox"]]
            for w in range(2):
                dr.rectangle([x0 - w, y0 - w, x1 + w, y1 + w], outline=(220, 20, 30))
        im.save(OUT / "pages" / f"{p['tag']}.png")
    if d is not None:
        d.close()
    print(f"rendered {len(eff)} pages at their shipped render_edge -> "
          f"{OUT/'pages'}  ({nb} rectangles)")


NBATCH = 4


def batches():
    idx = json.loads((OUT / "index.json").read_text())
    eff = [p for p in idx["pages"] if p["why_not_rendered"] != "already_rendered"]
    tags = [p["tag"] for p in eff]
    per = -(-len(tags) // NBATCH)
    for b in range(NBATCH):
        chunk = tags[b * per:(b + 1) * per]
        (OUT / f"batch{b+1}.tsv").write_text(
            "tag\tpng\n" + "".join(
                f"{t}\t{OUT/'pages'/(t+'.png')}\n" for t in chunk))
        print(f"batch{b+1}.tsv: {len(chunk)} pages ({chunk[0]}..{chunk[-1]})")


def score():
    """Merge the labellers, both questions, and price what the labels imply.

    Two columns, not one, because the two halves of this rule pull opposite
    ways: `outside` is what a page render RECOVERS and `detail` is what it
    DESTROYS. A single verdict column would have hidden whichever of the two
    the reader was not looking for -- which is exactly how the lone half's
    resolution cost went unnoticed through a whole labelling round.
    """
    idx = json.loads((OUT / "index.json").read_text())
    eff = {p["tag"]: p for p in idx["pages"]
           if p["why_not_rendered"] != "already_rendered"}
    files = sorted(OUT.glob("labels-*.tsv"))
    if not files:
        sys.exit("no eval/multiraster/labels-*.tsv yet")
    out_v = {f.name: _read_labels(f, "outside") for f in files}
    det_v = {f.name: _read_labels(f, "detail") for f in files}
    notes = {f.name: _read_labels(f, "note") for f in files}
    tags = sorted(eff)
    missing = [t for t in tags if not all(t in p for p in out_v.values())]
    if missing:
        print(f"WARNING unlabelled by some labeller: {' '.join(missing)}",
              file=sys.stderr)

    def merge(votes, against):
        """Majority, with any non-majority resolved AGAINST the change."""
        c = collections.Counter(votes)
        top, k = c.most_common(1)[0]
        if k * 2 <= len(votes) and top != against:
            top = against
        return top, k

    merged = []
    for t in tags:
        ov = [p[t] for p in out_v.values() if t in p]
        dv = [p[t] for p in det_v.values() if t in p]
        if not ov:
            continue
        o, ok = merge(ov, "no")
        dd, dk = merge(dv, "lost")
        # Labeller 1's note verbatim, whether or not labeller 1 is in the
        # majority. Two label columns make "the majority's note" ambiguous, so
        # the column is named for its source instead of being merged.
        note = notes[sorted(notes)[0]].get(t, "")
        p = eff[t]
        nrect = sum(1 for b in p["rasters"] if b["bbox"] and b["subsumed"])
        nsub = sum(1 for b in p["rasters"] if b["subsumed"])
        # Two separate reasons a page cannot be judged, kept apart on purpose.
        # nrect == 0 is the CODE's fact: _raster_pixmap found no page placement
        # for any raster here, so no region was drawn and there is nothing on
        # the page to reason about (eval/multifigure.py excludes on the same
        # fact rather than on the label, and that is what kept a
        # judgement-about-nothing out of its numerator). `norect` from a
        # majority of labellers on a page that provably HAS a rectangle is the
        # LABELLER's failure -- both of them are 24x27pt CAD callouts -- and is
        # excluded too, but counted separately so neither hides the other.
        merged.append({"tag": t, "corpus": p["corpus"], "file": p["file"],
                       "page": p["page"], "signal": p["signal"],
                       "subsumed": nsub, "rects": nrect, "edge": p["edge"],
                       "judgeable": nrect > 0 and o != "norect" and dd != "norect",
                       "outside": o, "outside_agree": f"{ok}/{len(ov)}",
                       "detail": dd, "detail_agree": f"{dk}/{len(dv)}",
                       "note_l1": note})
    cols = ["tag", "corpus", "file", "page", "signal", "edge",
            "subsumed", "rects", "judgeable", "outside", "outside_agree",
            "detail", "detail_agree",
            "note_l1"]
    (OUT / "labels.tsv").write_text(
        "\t".join(cols) + "\n" +
        "".join("\t".join(str(m[c]) for c in cols) + "\n" for m in merged))

    jud = [m for m in merged if m["judgeable"]]
    n = len(jud)
    add = sum(1 for m in jud if m["outside"] == "yes")
    lost = sum(1 for m in jud if m["detail"] == "lost")
    both = sum(1 for m in jud if m["outside"] == "yes" and m["detail"] == "lost")
    safe_add = sum(1 for m in jud if m["outside"] == "yes" and m["detail"] == "legible")
    pure_harm = sum(1 for m in jud if m["outside"] == "no" and m["detail"] == "lost")
    print(f"labellers   : {len(out_v)} ({', '.join(sorted(out_v))})")
    print(f"labelled    : {len(merged)} of {len(tags)}   "
          f"({len(merged)-n} unjudgeable: no rectangle drawn)")
    for k in ("outside", "detail"):
        una = sum(1 for m in merged
                  if m[k + "_agree"].split("/")[0] == m[k + "_agree"].split("/")[1])
        print(f"unanimous on {k:<8}: {una}/{len(merged)} "
              f"({una/len(merged)*100:.0f}%)  -- three runs of one model, see the caveat")
    for name, k in (("RECOVERS a graphic outside the crops", add),
                    ("DESTROYS detail inside the crops", lost)):
        lo, hi = wilson(k, n)
        print(f"{name:<40}: {k}/{n} = {k/n*100:.1f}%  "
              f"(95% Wilson {lo*100:.0f}-{hi*100:.0f}%)")
    print(f"\n  both (recovers and destroys) : {both}/{n}")
    print(f"  recovers, nothing destroyed  : {safe_add}/{n}")
    print(f"  destroys, recovers nothing   : {pure_harm}/{n}")
    print(f"  neither                      : {n-both-safe_add-pure_harm}/{n}")
    print(f"\ndocuments   : {len({m['file'] for m in jud})} judged, "
          f"{len({m['file'] for m in jud if m['outside']=='yes'})} with a recovery, "
          f"{len({m['file'] for m in jud if m['detail']=='lost'})} with a loss")
    for key in ("corpus", "signal", "subsumed"):
        print(f"\nby {key}:")
        for v in sorted({m[key] for m in jud}, key=str):
            g = [m for m in jud if m[key] == v]
            print(f"  {str(v):<12} n={len(g):<4} outside "
                  f"{sum(1 for m in g if m['outside']=='yes')}/{len(g)}"
                  f"   detail lost {sum(1 for m in g if m['detail']=='lost')}/{len(g)}")


TRIGGERS = {
    "any vector figure signal (the rule as worded)": lambda p, n: True,
    "signal is curves or diagonals": lambda p, n: p["signal"] in ("curves", "diagonals"),
    "at least 3 rasters on the page": lambda p, n: n >= 3,
    "at least 4 rasters on the page": lambda p, n: n >= 4,
    "at least 5 rasters (RASTER_GRID 6 -> 4)": lambda p, n: n >= 5,
    "the collapse is token-negative on this page": lambda p, n: None,   # filled below
}


def variants():
    """Every subset of the trigger, priced and scored against the labels.

    The point of the table is the same one eval/multifigure.py's made: check
    whether any narrowing isolates the benefit cheaply, or whether the bill is
    just the price of a page render and does not care why the page was picked.
    """
    idx = json.loads((OUT / "index.json").read_text())
    eff = {p["tag"]: p for p in idx["pages"]
           if p["why_not_rendered"] != "already_rendered"}
    lab, lp = {}, OUT / "labels.tsv"
    if lp.exists():
        o = _read_labels(lp, "outside")
        dt = _read_labels(lp, "detail")
        ju = _read_labels(lp, "judgeable")
        lab = {t: (o[t], dt[t]) for t in o if ju.get(t) == "True"}
    rat, rp = {}, OUT / "ratios.json"
    if rp.exists():
        for k, v in json.loads(rp.read_text()).items():
            rat.setdefault(k.split("/")[0], []).append(v)
    print(f"{'trigger':<46}{'pages':>6}{'crops':>7}{'tokens':>10}{'calls':>7}"
          f"{'recovers':>10}{'degrades':>10}{'p50 res':>9}")
    for name, fn in TRIGGERS.items():
        fire = []
        for t, p in eff.items():
            g = [b for b in p["rasters"] if b["subsumed"]]
            n = len(g)
            hit = (p["render_tok"] - sum(b["tok"] for b in g) < 0
                   if fn(p, n) is None else fn(p, n))
            if hit:
                fire.append((t, p, g))
        if not fire:
            continue
        tok = sum(p["render_tok"] - sum(b["tok"] for b in g) for _, p, g in fire)
        calls = sum(1 - len(g) for _, _, g in fire)
        jud = [t for t, p, g in fire if g and t in lab]
        rec = sum(1 for t in jud if lab[t][0] == "yes")
        deg = sum(1 for t in jud if lab[t][1] == "lost")
        rs = sorted(v for t, _, _ in fire for v in rat.get(t, []))
        print(f"{name:<46}{len(fire):>6}{sum(len(g) for _,_,g in fire):>7}"
              f"{tok:>+10,}{calls:>+7}"
              f"{f'{rec}/{len(jud)}':>10}{f'{deg}/{len(jud)}':>10}"
              f"{(f'{rs[len(rs)//2]:.2f}x' if rs else '-'):>9}")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "measure"
    if len(sys.argv) > 2:            # e.g. `measure arxiv_holdout,pmc_holdout out=holdout`
        CORPORA = tuple(sys.argv[2].split(","))
    if len(sys.argv) > 3:
        OUT = ROOT / "eval" / "multiraster" / sys.argv[3]
    {"measure": measure, "report": report, "guard": guard,
     "resolution": resolution, "render": render, "batches": batches,
     "score": score, "variants": variants}[cmd]()
