# /// script
# requires-python = ">=3.10"
# dependencies = ["pytest"]
# ///
"""Tests for harvest.py's routing decisions -- the single source of truth.

Every case here encodes a documented failure from the design spec (docs/
superpowers/specs/2026-08-03-pdf-extract-skill-design.md) or git history, so a
"simplification" that re-breaks one fails with the original incident named.

render_reason, furniture_reason, grid_pages and _cluster are pure functions of
plain data; they are tested everywhere. harvest.py's module imports (fitz,
pdf_inspector) are stubbed when absent so those pure tests still run under the
bare pytest environment; the end-to-end tests on synthetic PDFs skip unless
the real dependencies are installed.
"""
import sys, types, pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "skills" / "pdf-extract"))

import pytest

try:
    import fitz
    HAVE_FITZ = True
except ImportError:                      # pure tests never touch fitz; stub the
    HAVE_FITZ = False                    # two constants harvest reads at import
    stub = types.ModuleType("fitz")
    stub.TEXTFLAGS_DICT, stub.TEXT_PRESERVE_IMAGES = 0xFFFF, 8
    sys.modules["fitz"] = stub
try:
    import pdf_inspector
    HAVE_PI = True
except ImportError:
    HAVE_PI = False
    sys.modules["pdf_inspector"] = types.ModuleType("pdf_inspector")

from harvest import (render_reason, furniture_reason, grid_pages, _cluster,
                     RASTER_GRID, harvest)

needs_real_deps = pytest.mark.skipif(
    not (HAVE_FITZ and HAVE_PI),
    reason="needs pymupdf + pdf-inspector (run: uv run --with pytest "
           "--with pdf-inspector==0.2.6 --with pymupdf==1.28.0 "
           "python -m pytest tests/)")


def g(**kw):
    """A page_geometry dict with everything zeroed unless overridden."""
    base = dict(curves=0, diagonals=0, axis_h=0, axis_v=0, rects=0,
                x_edges=0, y_edges=0, ink=0.0, stroke_frac=0.0,
                stroke_aspect=99.0)
    base.update(kw)
    base.setdefault("axis_lines", base["axis_h"] + base["axis_v"])
    return base


# --------------------------------------------------------------- render_reason
def test_bezier_figure_fires_curves():
    """Thesis figures: legend boxes and plot artwork emit bezier ops."""
    assert render_reason(g(curves=20, stroke_frac=0.08, stroke_aspect=1.4)) == "curves"


def test_vendor_logo_is_not_a_figure():
    """ti_ucc27517: 143-curve logo at ~0.5% stroke area on a text page."""
    assert render_reason(g(curves=143, diagonals=20,
                           stroke_frac=0.005, stroke_aspect=1.2)) is None


def test_corner_chart_fires_diagonals_despite_small_area():
    """corner_chart_only.pdf: ~3.3% of the page; the 2% floor must keep it."""
    assert render_reason(g(diagonals=5, axis_h=2, axis_v=2,
                           stroke_frac=0.033, stroke_aspect=1.5)) == "diagonals"


def test_underlined_links_do_not_fire():
    """underlines.pdf + thesis bibliography: horizontal strokes only."""
    assert render_reason(g(axis_h=14, stroke_frac=0.5, stroke_aspect=1.3)) is None


def test_marker_scatter_fires_stroke_grid():
    """chart_scatter.pdf: no curves, no diagonals, strokes both ways."""
    assert render_reason(g(axis_h=6, axis_v=6, rects=4,
                           stroke_frac=0.30, stroke_aspect=1.3)) == "stroke_grid"


def test_wallpaper_line_pattern_does_not_fire():
    """guidelines p13: 40 axis strokes in a thin margin sliver, ink 0.008."""
    assert render_reason(g(axis_h=20, axis_v=20,
                           stroke_frac=0.30, stroke_aspect=9.0)) is None


def test_shaded_table_the_extractor_missed_fires_dense_grid():
    """MTR p9: merged-header cost table, filled cells, no strokes."""
    assert render_reason(g(rects=40, x_edges=6, y_edges=12, ink=0.30)) == "dense_grid"


def test_decorative_banners_do_not_fire():
    """Metodika p2: section banners, ink 0.03-0.07, below the 0.15 floor."""
    assert render_reason(g(rects=12, x_edges=5, y_edges=6, ink=0.06)) is None


def test_tinted_cover_page_does_not_fire():
    """A full-bleed tint reaches ink 1.0 with 2 drawing ops; per-branch
    minimums must keep it out."""
    assert render_reason(g(rects=2, ink=1.0)) is None


def test_curves_outranks_stroke_grid():
    """Branch order is most- to least-specific."""
    assert render_reason(g(curves=9, axis_h=5, axis_v=5,
                           stroke_frac=0.2, stroke_aspect=1.2)) == "curves"


# ------------------------------------------------------------ furniture_reason
def test_ubiquitous_image_is_furniture():
    """guidelines: a sidebar stripe placed on 14/14 pages."""
    assert furniture_reason(400, 400, 14, 14).startswith("ubiquitous")


def test_ubiquity_needs_more_than_two_pages():
    """A figure on both pages of a 2-pager is content, not furniture."""
    assert furniture_reason(400, 400, 2, 2) is None


def test_small_sliver_and_low_area_are_furniture():
    assert furniture_reason(80, 400, 1, 10).startswith("small")
    assert furniture_reason(1200, 130, 1, 10) == "sliver"
    assert furniture_reason(150, 150, 1, 10) == "low_area"


def test_real_figure_survives():
    """guidelines: the one real 1347x758 graphic out of 69 placements."""
    assert furniture_reason(1347, 758, 1, 14) is None


# ------------------------------------------------------------------ grid_pages
def test_page_tiled_with_many_rasters_collapses():
    """ai_latent-diffusion p32: 48 tiles of one inpainting comparison."""
    assert grid_pages([{31}] * 48, renders={}) == {31}


def test_a_few_distinct_figures_do_not_collapse():
    """tps62840 p25: six oscilloscope shots, better sent as tiles."""
    assert grid_pages([{24}] * RASTER_GRID, renders={}) == set()


def test_rasters_on_an_already_rendered_page_do_not_count():
    """Subsumption already covers them; no double render."""
    assert grid_pages([{3}] * 10, renders={3: "curves"}) == set()


def test_multi_page_raster_counts_only_unrendered_placements():
    sets = [{3, 7}] * 10
    assert grid_pages(sets, renders={3: "curves"}) == {7}


def test_cluster_merges_within_tolerance():
    assert _cluster([0.0, 1.0, 2.0, 100.0, 101.0]) == [0.0, 100.0]


# ------------------------------------------------- end-to-end, synthetic PDFs
def _make_pdf(path, n_images, w=300, h=300):
    """One text page carrying n distinct (differently coloured) images."""
    doc = fitz.open()
    page = doc.new_page(width=595, height=842)
    # Enough prose that pdf-inspector classifies the page text_based rather
    # than flagging it for OCR (a caption-sized line is not enough).
    for ln in range(18):
        page.insert_text((72, 60 + 14 * ln),
                         f"Line {ln}: prose so this page is text_based and "
                         "is not routed down the no_text_layer path.",
                         fontsize=11)
    for i in range(n_images):
        pm = fitz.Pixmap(fitz.csRGB, fitz.IRect(0, 0, w, h))
        pm.clear_with((i * 29) % 255)          # distinct pixels: survives dedup
        x, y = 60 + (i % 4) * 125, 340 + (i // 4) * 125
        page.insert_image(fitz.Rect(x, y, x + 110, y + 110), pixmap=pm)
    doc.save(str(path))
    doc.close()


@needs_real_deps
def test_grid_page_yields_one_render_not_n_calls(tmp_path):
    pdf = tmp_path / "grid.pdf"
    _make_pdf(pdf, RASTER_GRID + 2)
    r = harvest(str(pdf))
    assert r["status"] == "ok"
    reasons = [i["reason"] for i in r["items"]]
    assert reasons == ["raster_grid"], reasons
    assert r["items"][0]["kind"] == "page_render"
    assert r["items"][0]["edge"], "a collapsed page must carry a pixel budget"
    subsumed = [d for d in r["dropped"] if d.get("why") == "subsumed_by_page_render"]
    assert len(subsumed) == RASTER_GRID + 2


@needs_real_deps
def test_few_images_stay_standalone(tmp_path):
    pdf = tmp_path / "few.pdf"
    _make_pdf(pdf, 3)
    r = harvest(str(pdf))
    assert r["status"] == "ok"
    assert [i["reason"] for i in r["items"]] == ["standalone_raster"] * 3


@needs_real_deps
def test_duplicate_images_are_deduped(tmp_path):
    """Same pixels stored as distinct XObjects must cost one call, not N.
    (132 real cases across the measured corpora; 40 in wurth_7447709100.)"""
    pdf = tmp_path / "dup.pdf"
    doc = fitz.open()
    page = doc.new_page(width=595, height=842)
    page.insert_text((72, 60), "Prose so this is text_based.", fontsize=11)
    pm = fitz.Pixmap(fitz.csRGB, fitz.IRect(0, 0, 300, 300))
    pm.clear_with(90)
    for i in range(3):                     # same pixels, three insertions
        x = 60 + i * 130
        page.insert_image(fitz.Rect(x, 100, x + 110, 210), pixmap=pm)
    doc.save(str(pdf))
    doc.close()
    r = harvest(str(pdf))
    assert r["status"] == "ok"
    rasters = [i for i in r["items"] if i["kind"] == "raster"]
    assert len(rasters) <= 1
