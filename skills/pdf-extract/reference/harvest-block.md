# harvest-block

Verbatim copy of `harvest.py`, for agents that cannot execute a file. Generated
by `tests/check_sync.py --fix`; do not edit by hand.

```python
# /// script
# requires-python = ">=3.10"
# dependencies = ["pdf-inspector==0.2.6", "pymupdf==1.28.0"]
# ///
"""Canonical visual-harvest block for the pdf-extract skill.

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

# ---------------------------------------------------------------- definitions
EDGE_TOL      = 3.0    # pt; two rect edges within this are the "same" gridline
FULLPAGE_FRAC = 0.90   # a rect covering more than this is background, not ink
MIN_DIM       = 120    # px; smaller on either side => furniture
MAX_ASPECT    = 8.0    # w:h beyond this => rule/stripe, not a figure
MIN_AREA      = 40_000 # px^2
UBIQUITY      = 0.50   # placed on more than this fraction of pages => furniture
INK_MIN       = 0.15   # filled non-background area / page area
STROKE_MIN_FRAC   = 0.02  # stroke bbox must cover this much of the page
STROKE_MAX_ASPECT = 5.0   # ...and not be an edge-hugging sliver
SCALE_GUARD   = 15     # vision calls above which we stop and ask


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
    """
    pw, ph = pg.rect.width, pg.rect.height
    parea = max(1.0, pw * ph)
    curves = diagonals = axis_h = axis_v = rects = 0
    xs, ys, ink = [], [], 0.0
    sx0 = sy0 = float("inf"); sx1 = sy1 = float("-inf")   # stroke bounding box

    for path in pg.get_drawings():
        r = path["rect"]
        is_background = r.width * r.height > parea * FULLPAGE_FRAC
        has_stroke = False
        for it in path["items"]:
            kind = it[0]
            if kind == "c":
                curves += 1; has_stroke = True
            elif kind == "re":
                rects += 1
                if not is_background:
                    xs += [it[1].x0, it[1].x1]
                    ys += [it[1].y0, it[1].y1]
            elif kind == "l":
                p1, p2 = it[1], it[2]
                dx, dy = abs(p2.x - p1.x), abs(p2.y - p1.y)
                if dx > 1.0 and dy > 1.0:
                    diagonals += 1
                elif dx >= dy:
                    axis_h += 1
                else:
                    axis_v += 1
                has_stroke = True
        if has_stroke and not is_background:
            sx0 = min(sx0, r.x0); sy0 = min(sy0, r.y0)
            sx1 = max(sx1, r.x1); sy1 = max(sy1, r.y1)
        if path.get("fill") and not is_background:
            ink += r.width * r.height

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
    }


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


MAX_EDGE_PX = 1568       # above this the model downsamples anyway
MIN_EDGE_PX = 800        # below this small print starts to go
TARGET_EM_PX = 8.0       # px of em-height needed to read a glyph reliably
NO_TEXT_EDGE_PX = 1100   # scans carry no font info; handwriting needs more


def render_edge(pg):
    """Long edge in px this page needs, from the size of its smallest text.

    Computed here rather than in convert.py because this function already has
    the page open and parsed; doing it separately doubled render wall-time.
    """
    sizes = []
    try:
        for b in pg.get_text("dict")["blocks"]:
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


def furniture_reason(w, h, placements, npages):
    if npages > 2 and placements / npages > UBIQUITY:
        return f"ubiquitous({placements}/{npages}pp)"
    if w < MIN_DIM or h < MIN_DIM:
        return f"small({w}x{h})"
    if max(w, h) / max(1, min(w, h)) > MAX_ASPECT:
        return "sliver"
    if w * h < MIN_AREA:
        return "low_area"
    return None


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
        has_visual = any(pg.get_images(full=True) or pg.get_drawings() for pg in doc)
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

    # -- filter 2: pixel-hash dedup (unproven; cheap insurance) --------------
    by_hash, uniq = {}, {}
    for xref, e in kept.items():
        try:
            h = hashlib.sha256(doc.extract_image(xref)["image"]).hexdigest()
        except Exception:
            h = f"xref{xref}"
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

    renders, edges = {}, {}
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
            continue                              # filter 3: extractor won
        g = geoms[i]
        # ...but only when the page carries nothing else. A shaded table has
        # filled rects and no strokes at all, so it matches the empty-stroke
        # template by accident; the ink test keeps those.
        if (sig(g) in template and g["stroke_frac"] < STROKE_MIN_FRAC
                and g["ink"] < INK_MIN and g["rects"] < 8):
            dropped.append({"page": i + 1, "why": "vector_furniture"})
            continue
        why = render_reason(g)
        if why:
            renders[i] = why
            edges[i] = render_edge(pg)

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
    doc.close()

    return {
        "status": "ok", "path": path, "pdf_type": pdf_type, "pages": npages,
        "markdown": doc_md or "", "page_markdown": page_mds,
        "engine": "pdf-inspector==0.2.6",
        "text_chars": len((doc_md or "")),
        "vision_calls": len(items), "over_scale_guard": len(items) > SCALE_GUARD,
        "items": items, "dropped": dropped,
    }


if __name__ == "__main__":
    flags = {a for a in sys.argv[1:] if a.startswith("--")}
    args = [a for a in sys.argv[1:] if a not in flags]
    if not args:
        print("usage: uv run harvest.py <pdf> [...] [--json]", file=sys.stderr)
        raise SystemExit(2)
    bad = 0
    for p in args:
        r = harvest(p)
        if r["status"] != "ok":
            bad += 1
        if "--json" in flags:
            # JSONL: one document per line, so many files stay parseable.
            slim = {k: v for k, v in r.items() if k not in ("markdown", "page_markdown")}
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
```
