# /// script
# requires-python = ">=3.10"
# dependencies = ["pdf-inspector==0.2.6", "pymupdf"]
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
STROKE_MIN_FRAC   = 0.05  # stroke bbox must cover this much of the page
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
    curves = diagonals = axis_lines = rects = 0
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
                if abs(p2.x - p1.x) > 1.0 and abs(p2.y - p1.y) > 1.0:
                    diagonals += 1
                else:
                    axis_lines += 1
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
        "curves": curves, "diagonals": diagonals, "axis_lines": axis_lines,
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
    if g["curves"] >= 8 and _plot_shaped(g):
        return "curves"                      # bezier artwork: real vector figure
    if g["diagonals"] >= 4 and _plot_shaped(g):
        return "diagonals"                   # line chart / connected series
    if g["axis_lines"] + g["diagonals"] >= 10 and g["rects"] <= 20 \
            and _plot_shaped(g):
        return "sparse_plot"                 # axes+ticks+markers, few rects
    if g["x_edges"] >= 4 and g["y_edges"] >= 4 and g["rects"] >= 8 \
            and g["ink"] >= INK_MIN:
        return "dense_grid"                  # shaded table the extractor missed
    return None


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
    doc = fitz.open(path)
    if doc.needs_pass or doc.is_encrypted:
        doc.close()
        return {"status": "error", "error": "encrypted", "path": path}

    det = pi.detect_pdf(path)
    pdf_type = str(getattr(det, "pdf_type", "unknown"))
    ocr_pages = set(getattr(det, "pages_needing_ocr", []) or [])

    # -- phase 2: authoritative text comes from process_pdf, NOT per-page ----
    # (extract_pages_markdown scores 0.860 vs 0.875 and returns nothing at all
    #  on some documents; it is used ONLY for the table cross-check below.)
    res = pi.process_pdf(path)
    doc_md = getattr(res, "markdown", None)
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
    renders = {}
    for i, pg in enumerate(doc):
        if (i + 1) in ocr_pages:
            renders[i] = "no_text_layer"          # unambiguous: nothing to lose
            continue
        pm = page_mds[i] if i < len(page_mds) else ""
        if pm.count("\n|") >= 3:
            continue                              # filter 3: extractor won
        why = render_reason(page_geometry(pg))
        if why:
            renders[i] = why

    # -- subsumption: a rendered page covers the rasters it contains ---------
    standalone = []
    for xref, e in uniq.items():
        if all(p in renders for p in e["pages"]):
            dropped.append({"xref": xref, "px": [e["w"], e["h"]],
                            "why": "subsumed_by_page_render"})
        else:
            standalone.append((xref, e))

    items = [{"id": f"p{min(e['pages'])+1:03d}-x{xref}", "page": min(e["pages"]) + 1,
              "kind": "raster", "reason": "standalone_raster",
              "px": [e["w"], e["h"]], "description": None}
             for xref, e in standalone]
    items += [{"id": f"p{i+1:03d}-render", "page": i + 1, "kind": "page_render",
               "reason": why, "description": None}
              for i, why in sorted(renders.items())]
    doc.close()

    return {
        "status": "ok", "path": path, "pdf_type": pdf_type, "pages": npages,
        "engine": "pdf-inspector==0.2.6",
        "text_chars": len((doc_md or "")),
        "vision_calls": len(items), "over_scale_guard": len(items) > SCALE_GUARD,
        "items": items, "dropped": dropped,
    }


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    for p in args:
        r = harvest(p)
        if "--json" in sys.argv:
            print(json.dumps(r, indent=2))
        else:
            name = p.split("/")[-1][:44]
            if r["status"] != "ok":
                print(f"{name:<46} ERROR {r['error']}")
            else:
                kinds = collections.Counter(i["reason"] for i in r["items"])
                print(f"{name:<46} {r['pdf_type']:<11} pp={r['pages']:<3} "
                      f"calls={r['vision_calls']:<3} {dict(kinds)}")
