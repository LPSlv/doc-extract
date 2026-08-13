# /// script
# requires-python = ">=3.10"
# dependencies = ["pdf-inspector==0.2.6", "pymupdf==1.28.0"]
# ///
"""Canonical visual-harvest block for the doc-extract skill.

This is the single source of truth for every routing decision. The numbers in
the design spec and README are regenerated from THIS file; never the reverse.

Usage:
    uv run harvest.py <pdf> [--json]

Emits a manifest describing what would be sent to a vision pass, and why --
including what was dropped, since false negatives are the dangerous direction.
"""
import sys, json, hashlib, collections
import fitz
import pdf_inspector as pi
from filters import (MIN_DIM, MAX_ASPECT, MIN_AREA, UBIQUITY, MAX_EDGE_PX,
                     SCALE_GUARD, furniture_reason, _tok)

# ---------------------------------------------------------------- definitions
EDGE_TOL      = 3.0    # pt; two rect edges within this are the "same" gridline
FULLPAGE_FRAC = 0.90   # a rect covering more than this is background, not ink
INK_MIN       = 0.15   # filled non-background area / page area
STROKE_MIN_FRAC   = 0.02  # stroke bbox must cover this much of the page
STROKE_MAX_ASPECT = 5.0   # ...and not be an edge-hugging sliver
RASTER_GRID   = 6      # more rasters than this on one page: render the page
VSTROKE_TOL   = 2.0    # pt; two vertical strokes within this are the same edge
VSTROKE_MIN   = 3.0    # pt; shorter than this is a tick or a glyph, not an edge
BOX_REPEATS   = 3      # occurrences of a 2-edge signature that make it a template
TEXTONLY_PATHS = 2     # drawing paths a page may have and still carry no picture


def _cluster(vals, tol=EDGE_TOL):
    """Distinct coordinates, merging anything within tol."""
    out = []
    for v in sorted(vals):
        if not out or v - out[-1] > tol:
            out.append(v)
    return out


def page_geometry(pg):
    """Vector signature of one page. All terms defined here, nowhere else.

    ink  = sum of areas of FILLED paths, excluding any path covering more than
           FULLPAGE_FRAC of the page (background tint), divided by page area.
           Unfilled/stroke-only paths contribute zero ink.

    paths = how many drawing paths the page contains at all, filtered by
           nothing. A page with no raster and at most TEXTONLY_PATHS of these
           has no picture on it: a border and a header rule are two paths.
           Used only by the whole_document filter; see drop_textonly().

    vx_pos = the distinct x-positions of the page's vertical strokes, clustered
           at VSTROKE_TOL. Counting POSITIONS rather than strokes is what tells
           a frame (two positions: a left edge and a right edge) apart from a
           ruled table (3-4) or a plot (10+). Background paths are included
           deliberately: a frame drawn as a full-width path is still a frame.

    Reads get_cdrawings(), not get_drawings(): identical data, but as plain
    tuples. The wrapper spends more time constructing Point/Rect objects than
    MuPDF spends walking the page (measured 2.4x on 632 datasheet pages), and
    this function only ever looks at coordinates.
    """
    pw, ph = pg.rect.width, pg.rect.height
    parea = max(1.0, pw * ph)
    curves = diagonals = axis_h = axis_v = rects = paths = 0
    xs, ys, ink = [], [], 0.0
    vx = []
    sx0 = sy0 = float("inf"); sx1 = sy1 = float("-inf")   # stroke bounding box

    for path in pg.get_cdrawings():
        paths += 1
        rx0, ry0, rx1, ry1 = path["rect"]
        rw, rh = rx1 - rx0, ry1 - ry0
        is_background = rw * rh > parea * FULLPAGE_FRAC
        has_stroke = False
        for it in path["items"]:
            kind = it[0]
            if kind == "c":
                curves += 1; has_stroke = True
            elif kind == "re":
                rects += 1
                if not is_background:
                    x0, y0, x1, y1 = it[1]
                    xs += (x0, x1)
                    ys += (y0, y1)
            elif kind == "l":
                (p1x, p1y), (p2x, p2y) = it[1], it[2]
                dx, dy = abs(p2x - p1x), abs(p2y - p1y)
                if dx > 1.0 and dy > 1.0:
                    diagonals += 1
                elif dx >= dy:
                    axis_h += 1
                else:
                    axis_v += 1
                if dx <= 1.0 and dy > VSTROKE_MIN:
                    vx.append((p1x + p2x) / 2)
                has_stroke = True
        if has_stroke and not is_background:
            sx0 = min(sx0, rx0); sy0 = min(sy0, ry0)
            sx1 = max(sx1, rx1); sy1 = max(sy1, ry1)
        if path.get("fill") and not is_background:
            ink += rw * rh

    if sx1 > sx0 and sy1 > sy0:
        sw, sh = sx1 - sx0, sy1 - sy0
        stroke_frac = (sw * sh) / parea
        stroke_aspect = max(sw, sh) / max(1.0, min(sw, sh))
    else:
        stroke_frac, stroke_aspect = 0.0, 99.0

    return {
        "curves": curves, "diagonals": diagonals,
        "axis_h": axis_h, "axis_v": axis_v, "axis_lines": axis_h + axis_v,
        "rects": rects, "x_edges": len(_cluster(xs)), "y_edges": len(_cluster(ys)),
        "ink": round(ink / parea, 4),
        "stroke_frac": round(stroke_frac, 4), "stroke_aspect": round(stroke_aspect, 2),
        "vx_pos": tuple(round(v) for v in _cluster(vx, VSTROKE_TOL)),
        "paths": paths,
    }


def box_templates(geoms):
    """Frame signatures that repeat within this document.

    Boxed text is the largest false positive in `stroke_grid`: a frame drawn
    around a prompt listing, an algorithm or a proof puts strokes in both
    orientations and reads as a ruled table. Two facts separate it from a real
    table and neither is sufficient alone.

    A frame has exactly TWO distinct vertical stroke positions -- a left edge
    and a right edge, nothing between. Alone that cut 41 wasted calls out of
    170 firings but destroyed 13 real items, because a two-column ruled table
    also has two verticals.

    A template REPEATS, while a real table's geometry differs page to page. So
    the signature must also appear on BOX_REPEATS pages, counting this one.
    Composed, the two measured 95% precision in-sample, and then 100% (17
    drops, 0 real items lost, 95% CI 82-100%) on 348 arXiv papers fetched
    afterwards for the purpose. See eval/strokegrid.md.
    """
    n = collections.Counter(g["vx_pos"] for g in geoms if len(g["vx_pos"]) == 2)
    return {sig for sig, c in n.items() if c >= BOX_REPEATS}


def _plot_shaped(g):
    """Do the strokes occupy a substantial, blobby region?

    A chart's marks span a sizeable central area with a moderate aspect ratio.
    Decorative margin artwork (background line patterns, edge flourishes) is a
    thin sliver hugging one edge, and page furniture is tiny. Without this,
    a slide with a wallpaper line-pattern reads as a scatter plot.
    """
    return g["stroke_frac"] >= STROKE_MIN_FRAC and g["stroke_aspect"] <= STROKE_MAX_ASPECT


def render_reason(g):
    """Why this page needs eyes -- or None. Four branches, each self-gated.

    Ordered most- to least-specific. Each branch carries its own minimum so a
    near-empty page (e.g. a tinted cover with 2 drawing ops) cannot trip any.
    """
    # Vendor logos are bezier artwork too. A real figure occupies a meaningful
    # part of the page; a logo is a fraction of a percent and repeats on every
    # page of the document. Measured on 23 datasheets: 176 curve-pages sit at
    # >=5% stroke area, 10 at <2%, nothing between -- and all 10 were logos on
    # otherwise text-only pages (one verified by eye as a legal disclaimer).
    if g["curves"] >= 8 and _plot_shaped(g):
        return "curves"                      # bezier artwork: real vector figure
    # The area floor was originally lifted here so a chart tucked into a page
    # corner would still fire. Measured: a corner chart covers ~3.3% of the page
    # and a vendor logo 0.4-0.6%, so the 2% floor separates them cleanly and the
    # corner case is kept. Verified by the synthetic corner-chart fixture.
    if g["diagonals"] >= 4 and _plot_shaped(g):
        return "diagonals"                   # line chart / connected series
    # Axis-aligned strokes alone are ambiguous: plot spines and ticks look like
    # underlined headings. A plot has strokes in BOTH orientations; underlines
    # and rules are horizontal only. Requiring both kills the false positive
    # without losing marker-based scatter plots.
    if g["axis_h"] >= 3 and g["axis_v"] >= 3 \
            and g["axis_lines"] + g["diagonals"] >= 10 and g["rects"] <= 20 \
            and _plot_shaped(g):
        # Both orientations present: either a marker/tick-based plot or a ruled
        # table the extractor failed to turn into Markdown (filter 3 already
        # removed the ones it handled). One label -- the action is identical and
        # distinguishing them reliably is not worth false precision.
        return "stroke_grid"
    if g["x_edges"] >= 4 and g["y_edges"] >= 4 and g["rects"] >= 8 \
            and g["ink"] >= INK_MIN:
        return "dense_grid"                  # shaded table the extractor missed
    return None


MIN_EDGE_PX = 800        # below this small print starts to go
TARGET_EM_PX = 8.0       # px of em-height needed to read a glyph reliably
NO_TEXT_EDGE_PX = 1100   # scans carry no font info; handwriting needs more

# Only span sizes are read below, but "dict" also decodes and base64-wraps
# every raster on the page unless told otherwise. Dropping images returns the
# exact same spans (verified on 632 pages) at ~2.7x the speed.
SPAN_FLAGS = fitz.TEXTFLAGS_DICT & ~fitz.TEXT_PRESERVE_IMAGES


def render_edge(pg):
    """Long edge in px this page needs, from the size of its smallest text.

    Computed here rather than in convert.py because this function already has
    the page open and parsed; doing it separately doubled render wall-time.
    """
    sizes = []
    try:
        for b in pg.get_text("dict", flags=SPAN_FLAGS)["blocks"]:
            for ln in b.get("lines", []):
                for sp in ln.get("spans", []):
                    if sp.get("text", "").strip() and sp["size"] >= 3.0:
                        sizes.append(sp["size"])
    except Exception:
        pass
    if not sizes:
        return NO_TEXT_EDGE_PX
    sizes.sort()
    small = sizes[max(0, len(sizes) // 20)]   # 5th pct: the true min is usually
    long_pt = max(pg.rect.width, pg.rect.height)   # legal boilerplate, not content
    return int(max(MIN_EDGE_PX, min(MAX_EDGE_PX, long_pt * (TARGET_EM_PX / small))))


def _is_blank(pg, thresh=0.999):
    """Near-uniform white page: a scanned separator sheet, not content."""
    try:
        pm = pg.get_pixmap(dpi=20, colorspace=fitz.csGRAY)
        data = pm.samples
        return sum(1 for b in data if b >= 250) / max(1, len(data)) >= thresh
    except Exception:
        return False


def grid_pages(page_sets, renders):
    """Pages tiled with more than RASTER_GRID rasters not already covered.

    A composite figure -- an inpainting comparison, a 12-panel results grid, a
    robot-rollout strip -- is often stored as one XObject per tile, and each
    tile would otherwise cost its own vision call while only making sense as a
    whole. Checked by rendering every page carrying >=7 standalone rasters in
    corpus/papers + corpus/tds + 14 more datasheets: all were a single
    composite figure, or worse, ONE photo stored as horizontal strips
    (bq24074 p49: 12 "images" that are slices of one package render, nonsense
    individually). ai_latent-diffusion alone wanted 301 calls for 45 pages --
    one page holds 48 tiles -- where one ~849-token page render reads better.

    The threshold is 6, not lower, because pages holding 5-6 rasters are
    sometimes several genuinely distinct figures whose tiles carry more
    resolution than a page render can (tps62840 p25: six oscilloscope shots,
    each with fine on-screen text). Measured on papers+tds: collapsing at >6
    cuts vision calls 1024 -> 533 and image tokens 21%; >4 saves only 2
    points more while starting to eat those distinct-figure pages.

    `page_sets` is an iterable of per-raster placement-page sets; `renders`
    the pages already being rendered for another reason. Rasters every one of
    whose pages is already rendered are ignored -- subsumption will drop them
    regardless -- and placements on rendered pages do not count toward the
    tile total of an unrendered one.
    """
    placed = collections.Counter()
    for pages in page_sets:
        if not all(p in renders for p in pages):
            for p in pages:
                if p not in renders:
                    placed[p] += 1
    return {p for p, n in placed.items() if n > RASTER_GRID}


def batch_furniture(results, min_docs=3, frac=0.5):
    """Signatures that recur across DIFFERENT documents are template emblems.

    The intra-document ubiquity rule cannot see these: a US bill is 2-4 pages
    and the GPO seal sits on page 1 only, so it never reaches 50% *within* one
    file -- but it is byte-identical across all 230 bills. Geometry cannot tell
    an emblem from a small chart (max-path, fill-ratio and spatial-cluster
    measures were all tested and all failed: the 4N25 disclaimer page scores
    higher than a real ina226 chart page on every one). Recurrence across
    documents is the signal that actually works.
    """
    import collections as _c
    docs = _c.defaultdict(set)
    for r in results:
        if r.get("status") != "ok":
            continue
        for sig in (r.get("page_sigs") or {}).values():
            docs[tuple(sig)].add(r["path"])
    n = len({r["path"] for r in results if r.get("status") == "ok"})
    if n < min_docs:
        return set()
    return {sig for sig, seen in docs.items() if len(seen) / n > frac}


def drop_batch_furniture(results, template):
    """Remove items whose page signature is a cross-document emblem."""
    if not template:
        return results
    for r in results:
        if r.get("status") != "ok":
            continue
        sigs = r.get("page_sigs") or {}
        keep, removed = [], 0
        for it in r["items"]:
            sig = sigs.get(str(it["page"])) or sigs.get(it["page"])
            if it["kind"] == "page_render" and sig and tuple(sig) in template:
                r["dropped"].append({"page": it["page"], "why": "batch_furniture"})
                removed += 1
            else:
                keep.append(it)
        if removed:
            r["items"] = keep
            r["vision_calls"] = len(keep)
            r["over_scale_guard"] = len(keep) > SCALE_GUARD
    return results


def cost_guard(items, doc, edges):
    """Never cost more than just looking at the whole document.

    On short documents the routed set can exceed the price of rendering every
    page: measured on olmOCR single-page corpora, 99 files cost MORE than full
    optical (long_tiny_text as a class was +61%). When that happens the routed
    set is not a saving, so fall back to one render per page -- which also
    captures strictly more.
    """
    if not items:
        return items, None
    ours = 0
    for it in items:
        if it["kind"] == "raster":
            ours += _tok(*it["px"])
        else:
            pg = doc[it["page"] - 1]
            e = it.get("edge") or edges.get(it["page"] - 1) or NO_TEXT_EDGE_PX
            sc = e / max(pg.rect.width, pg.rect.height)
            ours += _tok(int(pg.rect.width * sc), int(pg.rect.height * sc))
    whole = 0
    for i, pg in enumerate(doc):
        e = render_edge(pg)
        sc = e / max(pg.rect.width, pg.rect.height)
        whole += _tok(int(pg.rect.width * sc), int(pg.rect.height * sc))
    if ours <= whole:
        return items, None
    out = []
    for i, pg in enumerate(doc):
        out.append({"id": f"p{i+1:03d}-render", "page": i + 1,
                    "kind": "page_render", "reason": "whole_document",
                    "edge": render_edge(pg), "description": None})
    return out, {"why": "cost_guard", "routed_tokens": ours, "whole_tokens": whole}


def drop_textonly(items, geoms, img_pages, ocr_pages):
    """Pages a whole-document collapse renders although they carry no picture.

    `cost_guard` replaces the routed set with one render per page whenever the
    routed set costs more than reading the whole document. That bound is on
    cost, not on content: it renders the references, the acknowledgements and
    the two-column prose along with everything else. Labelling 120 sampled
    `whole_document` calls found 34% of them carry nothing to look at
    (eval/nofigure.md), which is the largest single block of waste measured in
    this router.

    Most of it is not reachable - a prose page under a journal masthead is
    branding, and branding is separable from a figure only by reading it
    (eval/tds-corpus.md, twelve signals, eleven rejected). This takes the part
    that needs no judgement at all: a page with NO raster placed on it and at
    most TEXTONLY_PATHS drawing paths has nothing pictorial on it. A page
    border and a header rule are two paths.

    Measured blind on two corpora fetched after the rule was written -
    corpus/pmc_holdout (250 journal PDFs, disjoint from corpus/pmc by content
    hash) and corpus/arxiv_holdout - by three independent labellers per page:
    **203 drops labelled, 0 real items, 100% precision**, 95% Wilson 97-100%
    and 96-100%. 113 of 546 whole_document calls on the first, 320 of 1,011 on
    the second.

    It cannot cascade the way the reverted QR filter did (eval/tds-corpus.md).
    That filter removed IMAGES before `grid_pages`, so pages fell below
    RASTER_GRID and re-expanded into crops. This removes a page render only
    when the page carries no raster at all, and runs after cost_guard, so
    there is nothing left on the page to un-subsume.

    Text is unaffected either way: `process_pdf` runs over the whole document
    independently of routing, so a dropped page keeps its extracted text.
    """
    keep, gone = [], []
    for it in items:
        i = it["page"] - 1
        if (it["reason"] == "whole_document" and it["page"] not in ocr_pages
                and i not in img_pages and i < len(geoms)
                and geoms[i]["paths"] <= TEXTONLY_PATHS):
            gone.append({"page": it["page"], "why": "textonly_page"})
        else:
            keep.append(it)
    return keep, gone


def harvest_batch(paths):
    """Harvest several documents and apply the cross-document furniture rule.

    Use this rather than mapping harvest() yourself: an emblem repeated across
    documents is only visible at batch scope, and callers that skip this step
    pay a vision call per document for a publisher mark (230 US bills = 227
    wasted calls before this existed).
    """
    results = [harvest(p) for p in paths]
    return drop_batch_furniture(results, batch_furniture(results))


def harvest(path):
    # -- phase 1: classify, and refuse to cache a silent failure -------------
    try:
        doc = fitz.open(path)
    except Exception as e:                      # corrupt/unreadable: structured
        return {"status": "error", "error": "unreadable",
                "detail": type(e).__name__, "path": path}
    if doc.needs_pass or doc.is_encrypted:
        doc.close()
        return {"status": "error", "error": "encrypted", "path": path}

    # MuPDF opens .txt/.epub/.svg/images happily, so fitz.open() succeeding is
    # not proof this is a PDF. pdf_inspector is stricter and raises; catch it
    # here or one bad file in a folder aborts every remaining document.
    try:
        det = pi.detect_pdf(path)
        pdf_type = str(getattr(det, "pdf_type", "unknown"))
        ocr_pages = set(getattr(det, "pages_needing_ocr", []) or [])

        # -- phase 2: authoritative text from process_pdf, NOT per-page ------
        # (extract_pages_markdown scores 0.860 vs 0.875 and returns nothing at
        #  all on some documents; used ONLY for the table cross-check below.)
        res = pi.process_pdf(path)
        doc_md = getattr(res, "markdown", None)
    except Exception as e:
        doc.close()
        return {"status": "error", "error": "unreadable",
                "detail": f"{type(e).__name__}: {e}", "path": path}
    if not (doc_md or "").strip():
        # No text. That is legitimate for a scan or a figure-only page -- but if
        # there is no visual content either, extraction genuinely failed and we
        # must NOT cache an empty artifact as a success.
        has_visual = any(pg.get_images(full=True) or pg.get_cdrawings() for pg in doc)
        if not has_visual and not ocr_pages:
            doc.close()
            return {"status": "error", "error": "empty_extraction", "path": path}

    try:
        page_mds = [getattr(p, "markdown", "") or ""
                    for p in getattr(pi.extract_pages_markdown(path), "pages", [])]
    except Exception:
        page_mds = []

    npages = len(doc)
    kept, dropped = {}, []

    # -- filter 1: furniture -------------------------------------------------
    seen = collections.defaultdict(lambda: {"n": 0, "w": 0, "h": 0, "pages": set()})
    for i, pg in enumerate(doc):
        for im in pg.get_images(full=True):
            e = seen[im[0]]
            e["n"] += 1; e["w"], e["h"] = im[2], im[3]; e["pages"].add(i)
    for xref, e in seen.items():
        why = furniture_reason(e["w"], e["h"], e["n"], npages)
        if why:
            dropped.append({"xref": xref, "px": [e["w"], e["h"]], "why": why})
        else:
            kept[xref] = e

    # -- filter 2: pixel-hash dedup ------------------------------------------
    # Zero hits on the five design documents (spec 3.4 called it "unproven;
    # insurance"), but wider corpora vindicated it: 132 duplicate drops across
    # 11 of 277 documents (papers, datasheets, opendataloader), 40 in one
    # Wurth datasheet alone -- each a vision call that would have re-described
    # identical pixels.
    # Hashing via doc.extract_image re-encodes every image (PNG) and dominated
    # this filter's cost. Two cheap facts shrink the work with the same result:
    # images whose pixel dimensions differ can never be byte-identical, and
    # images whose raw streams plus image-dict entries are identical decode
    # identically -- so only dimension-groups with MIXED raw streams still need
    # the full decode-and-hash. Verified byte-identical dedup on every corpus.
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
    ident = {}                     # xref -> dedup identity; absent means unique
    for dim, group in by_dim.items():
        if len(group) == 1:
            continue
        raws = [_raw_key(x) for x in group]
        if None not in raws and len(set(raws)) == 1:
            h = _img_hash(group[0])    # identical inputs decode identically...
            if h == f"xref{group[0]}":
                continue               # ...and fail identically: all unique
            for x in group:
                ident[x] = (dim, h)
        else:
            for x in group:
                ident[x] = (dim, _img_hash(x))

    by_hash, uniq = {}, {}
    for xref, e in kept.items():
        h = ident.get(xref, ("uniq", xref))
        if h in by_hash:
            dropped.append({"xref": xref, "px": [e["w"], e["h"]],
                            "why": f"duplicate_of({by_hash[h]})"})
        else:
            by_hash[h] = xref; uniq[xref] = e

    # -- filters 3 + 4: which pages need eyes --------------------------------
    # Vector page furniture: a vendor logo is bezier artwork that repeats with
    # an identical signature on every page, exactly as a raster logo does. The
    # raster filter already drops those by ubiquity; do the same for drawings,
    # or a logo on a text page reads as a figure. Measured on 23 datasheets:
    # ti_ucc27517 carries the same 143-curve/20-diagonal signature on 6 pages.
    geoms = [page_geometry(pg) for pg in doc]
    sig = lambda g: (g["curves"], g["diagonals"], g["axis_h"], g["axis_v"])
    counts = collections.Counter(sig(g) for g in geoms)
    template = {k for k, n in counts.items()
                if npages > 2 and n / npages > UBIQUITY}

    boxes = box_templates(geoms)
    # Every page carrying a raster at all, before filters 1 and 2 have their
    # say. Read by filter 3's audit entry below and by drop_textonly after the
    # collapse -- both want images the furniture filter is about to discard.
    raster_pages = {p for e in seen.values() for p in e["pages"]}

    renders, edges, page_sigs = {}, {}, {}
    for i, pg in enumerate(doc):
        if (i + 1) in ocr_pages:
            if _is_blank(pg):
                dropped.append({"page": i + 1, "why": "blank_page"})
            else:
                renders[i] = "no_text_layer"      # unambiguous: nothing to lose
                edges[i] = render_edge(pg)
            continue
        pm = page_mds[i] if i < len(page_mds) else ""
        if pm.count("\n|") >= 3:
            # Filter 3: the extractor parsed a table, so the page is treated as
            # captured. Record what that costs instead of skipping in silence.
            #
            # This was the only filter here that `continue`d without an audit
            # entry, and that is precisely why nobody could see it: a filter
            # which suppresses a call leaves no artifact, and every eval in this
            # repo samples the ROUTED set. 4,065 pages carrying figure signal
            # and no raster were discarded this way across 711 documents, 66%
            # of them carrying a real figure, and the loss went uncounted for
            # three sessions (eval/filter3.md).
            #
            # Free: `geoms` is already computed for every page, so the reason is
            # arithmetic over it rather than another get_cdrawings() walk.
            # Routing is unchanged -- this only ever appends to `dropped`.
            wanted = render_reason(geoms[i])
            if wanted:
                dropped.append({"page": i + 1, "why": "parsed_table",
                                "wanted": wanted,
                                "raster": i in raster_pages})
            continue
        g = geoms[i]
        # ...but only when the page carries nothing else. A shaded table has
        # filled rects and no strokes at all, so it matches the empty-stroke
        # template by accident; the ink test keeps those.
        if (sig(g) in template and g["stroke_frac"] < STROKE_MIN_FRAC
                and g["ink"] < INK_MIN and g["rects"] < 8):
            dropped.append({"page": i + 1, "why": "vector_furniture"})
            continue
        why = render_reason(g)
        if why == "stroke_grid" and g["vx_pos"] in boxes:
            dropped.append({"page": i + 1, "why": "boxed_text"})
            continue
        if why:
            renders[i] = why
            edges[i] = render_edge(pg)
            page_sigs[str(i + 1)] = sig(g)

    # -- raster grids: a page tiled with many images is one figure -----------
    for p in grid_pages((e["pages"] for e in uniq.values()), renders):
        renders[p] = "raster_grid"
        edges[p] = render_edge(doc[p])

    # -- subsumption: a rendered page covers the rasters it contains ---------
    standalone = []
    for xref, e in uniq.items():
        if all(p in renders for p in e["pages"]):
            dropped.append({"xref": xref, "px": [e["w"], e["h"]],
                            "why": "subsumed_by_page_render"})
        else:
            standalone.append((xref, e))

    items = [{"id": f"p{min(e['pages'])+1:03d}-x{xref}", "page": min(e["pages"]) + 1,
              "kind": "raster", "reason": "standalone_raster", "xref": xref,
              "px": [e["w"], e["h"]], "description": None}
             for xref, e in standalone]
    items += [{"id": f"p{i+1:03d}-render", "page": i + 1, "kind": "page_render",
               "reason": why, "edge": edges.get(i), "description": None}
              for i, why in sorted(renders.items())]
    items, guard = cost_guard(items, doc, edges)
    if guard:
        dropped.append(guard)
        # Only ever after the collapse: before it, a page that looks bare here
        # may still be carrying a raster the routed set would have emitted.
        items, gone = drop_textonly(items, geoms, raster_pages, ocr_pages)
        dropped += gone
    doc.close()

    return {
        "status": "ok", "path": path, "pdf_type": pdf_type, "pages": npages,
        "markdown": doc_md or "", "page_markdown": page_mds,
        "page_sigs": page_sigs,
        "engine": "pdf-inspector==0.2.6",
        "text_chars": len((doc_md or "")),
        "vision_calls": len(items), "over_scale_guard": len(items) > SCALE_GUARD,
        "items": items, "dropped": dropped,
    }


def _harvest_all(paths):
    """One result per path, in input order. Documents are independent, so
    multi-file runs fan out across processes; each result is deterministic and
    map() preserves order, so output is byte-identical to the serial loop.
    Falls back to serial if the platform refuses to fork."""
    if len(paths) > 1:
        try:
            import os, concurrent.futures as cf
            with cf.ProcessPoolExecutor(
                    max_workers=min(len(paths), os.cpu_count() or 1)) as ex:
                return list(ex.map(harvest, paths))
        except Exception:
            pass
    return [harvest(p) for p in paths]


if __name__ == "__main__":
    flags = {a for a in sys.argv[1:] if a.startswith("--")}
    args = [a for a in sys.argv[1:] if a not in flags]
    if not args:
        print("usage: uv run harvest.py <pdf> [...] [--json]", file=sys.stderr)
        raise SystemExit(2)
    bad = 0
    results = _harvest_all(args)
    # Cross-document furniture: only visible at batch scope (see harvest_batch).
    results = drop_batch_furniture(results, batch_furniture(results))
    for p, r in zip(args, results):
        if r["status"] != "ok":
            bad += 1
        if "--json" in flags:
            # JSONL: one document per line, so many files stay parseable.
            slim = {k: v for k, v in r.items()
                    if k not in ("markdown", "page_markdown", "page_sigs")}
            print(json.dumps(slim))
        else:
            name = p.split("/")[-1][:44]
            if r["status"] != "ok":
                print(f"{name:<46} ERROR {r['error']}")
            else:
                kinds = collections.Counter(i["reason"] for i in r["items"])
                print(f"{name:<46} {r['pdf_type']:<11} pp={r['pages']:<3} "
                      f"calls={r['vision_calls']:<3} {dict(kinds)}")
    raise SystemExit(1 if bad else 0)
