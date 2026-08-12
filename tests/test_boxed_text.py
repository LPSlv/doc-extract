"""A frame drawn around text is not a ruled table.

The incident: `stroke_grid` fires when a page carries axis-aligned strokes in
both orientations, on the reasoning that a plot has spines and ticks and a
ruled table has gridlines. A box drawn around a prompt listing, an algorithm,
or a proof answers yes to exactly that question. Labelling all 170 firings
across 711 documents found 72 (42%) bought nothing, and boxed text was the
largest single family - `2607.29679v1` alone burned five vision calls on
framed prompt listings.

The rule that fixed it needs BOTH halves, and this file pins both:

  - a frame has exactly TWO distinct vertical stroke POSITIONS, a left edge
    and a right edge with nothing between. Counting strokes instead of
    positions cannot see this, because a tcolorbox draws each edge as several
    segments.
  - a template REPEATS. On its own the two-position test cut 41 wasted calls
    but destroyed 13 real items, because a two-column ruled table also has two
    verticals. Requiring the same signature at the same x-positions elsewhere
    in the document took precision from 76% to 95%.

Measured 95% in-sample, then 100% (17 drops, 0 real items lost, 95% CI
82-100%) on 348 arXiv papers fetched afterwards for the purpose. Full method
and the labels: eval/strokegrid.md.
"""
import pathlib
import sys
import types

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "skills" / "doc-extract"))

try:
    import pdf_inspector                                        # noqa: F401
    HAVE_PI = True
except ImportError:
    HAVE_PI = False
    sys.modules["pdf_inspector"] = types.ModuleType("pdf_inspector")

fitz = pytest.importorskip("fitz", reason="needs PyMuPDF to build a test PDF")
from harvest import (BOX_REPEATS, box_templates, harvest, page_geometry,
                     render_reason)

needs_pi = pytest.mark.skipif(
    not HAVE_PI, reason="needs pdf-inspector (see test_harvest.py for the cmd)")

W, H = 612, 792
LEFT, RIGHT = 56.0, 556.0


def _framed_page(pg, left=LEFT, right=RIGHT):
    """A tcolorbox-style frame: each edge in three segments, plus separators.

    Segmented deliberately. Six vertical strokes at two positions is the shape
    the rule has to recognise; a naive stroke count sees six and a naive
    "distinct verticals" count that forgot to cluster sees six too.
    """
    for x in (left, right):
        for y0, y1 in ((90, 300), (300, 500), (500, 700)):
            pg.draw_line((x, y0), (x, y1))
    for y in (90, 140, 300, 500, 700):
        pg.draw_line((left, y), (right, y))
    pg.insert_text((70, 120), "Prompt template", fontsize=11)
    for i, y in enumerate(range(160, 690, 24)):
        pg.insert_text((70, y), f"line {i}: you are a helpful assistant.", fontsize=9)


def _ruled_table_page(pg):
    """A real five-column ruled table: five distinct vertical positions."""
    cols = [56.0, 156.0, 256.0, 356.0, 456.0, 556.0]
    for x in cols:
        pg.draw_line((x, 90), (x, 700))
    for y in range(90, 701, 40):
        pg.draw_line((cols[0], y), (cols[-1], y))
    for r, y in enumerate(range(110, 700, 40)):
        for c, x in enumerate(cols[:-1]):
            pg.insert_text((x + 6, y), f"{r}.{c}", fontsize=9)


def _plain_page(pg, n):
    pg.insert_text((70, 100), f"Section {n}", fontsize=13)
    for i, y in enumerate(range(140, 700, 22)):
        pg.insert_text((70, y), f"Body text line {i} on page {n}.", fontsize=10)


def _build(tmp_path, name, painters):
    doc = fitz.open()
    for paint in painters:
        paint(doc.new_page(width=W, height=H))
    p = tmp_path / name
    doc.save(str(p))
    doc.close()
    return p


def _reasons(path):
    r = harvest(str(path))
    assert r["status"] == "ok", r
    return ([it["reason"] for it in r["items"]],
            [d.get("why") for d in r["dropped"]])


# ------------------------------------------------------------- the geometry
def test_a_segmented_frame_has_two_vertical_positions():
    """Six strokes, two positions. Clustering is what makes that true."""
    doc = fitz.open()
    _framed_page(doc.new_page(width=W, height=H))
    g = page_geometry(doc[0])
    assert g["axis_v"] == 6, "six vertical segments were drawn"
    assert len(g["vx_pos"]) == 2, g["vx_pos"]
    doc.close()


def test_a_ruled_table_has_more_than_two_vertical_positions():
    doc = fitz.open()
    _ruled_table_page(doc.new_page(width=W, height=H))
    assert len(page_geometry(doc[0])["vx_pos"]) == 6
    doc.close()


def test_the_frame_would_fire_stroke_grid_without_the_rule():
    """Guards against the test going vacuous: if the frame stopped tripping
    the branch, every assertion below would pass for the wrong reason."""
    doc = fitz.open()
    _framed_page(doc.new_page(width=W, height=H))
    assert render_reason(page_geometry(doc[0])) == "stroke_grid"
    doc.close()


# ------------------------------------------------------------- the routing
@needs_pi
def test_a_repeated_frame_is_dropped_as_boxed_text(tmp_path):
    path = _build(tmp_path, "framed.pdf",
                  [lambda p: _plain_page(p, 1)] + [_framed_page] * 4)
    reasons, why = _reasons(path)
    assert "stroke_grid" not in reasons, reasons
    assert why.count("boxed_text") == 4, why


def test_a_repeated_ruled_table_is_not_a_box_template():
    """The half of the rule that stops it eating tables.

    Tested against `box_templates` rather than through `harvest`, because a
    ruled table this clean never reaches the branch: pdf-inspector parses it
    into Markdown and filter 3 drops the page first. That ordering is real and
    is what `test_a_parsed_table_never_reaches_the_branch` pins. It also means
    routing cannot demonstrate this half of the rule - the page would survive
    whether the rule were right or wrong."""
    doc = fitz.open()
    for _ in range(4):
        _ruled_table_page(doc.new_page(width=W, height=H))
    geoms = [page_geometry(p) for p in doc]
    assert box_templates(geoms) == set(), "six positions is not a frame"
    assert all(g["vx_pos"] not in box_templates(geoms) for g in geoms)
    doc.close()


@needs_pi
def test_a_parsed_table_never_reaches_the_branch(tmp_path):
    """Filter 3 runs first: what the extractor turned into Markdown needs no
    eyes. Pinned so a later reordering cannot quietly hand these pages to the
    box rule, where they would look exactly like the thing it drops."""
    path = _build(tmp_path, "tables.pdf",
                  [lambda p: _plain_page(p, 1)] + [_ruled_table_page] * 4)
    reasons, why = _reasons(path)
    assert "boxed_text" not in why, why
    assert reasons == [], reasons


@needs_pi
def test_a_frame_that_does_not_repeat_enough_is_kept(tmp_path):
    """BOX_REPEATS occurrences, self included. Two is a coincidence; a real
    two-column table appearing twice must not be destroyed by it."""
    assert BOX_REPEATS == 3
    path = _build(tmp_path, "twice.pdf",
                  [lambda p: _plain_page(p, 1)] + [_framed_page] * 2)
    reasons, why = _reasons(path)
    assert "boxed_text" not in why, why
    assert reasons.count("stroke_grid") == 2, reasons


@needs_pi
def test_frames_at_different_positions_are_not_the_same_template(tmp_path):
    """The signature is WHERE the edges are, not how many. Three unrelated
    boxes at three different widths are three figures, not a repeat."""
    path = _build(tmp_path, "shifted.pdf", [
        lambda p: _plain_page(p, 1),
        lambda p: _framed_page(p, 56.0, 556.0),
        lambda p: _framed_page(p, 96.0, 516.0),
        lambda p: _framed_page(p, 136.0, 476.0),
    ])
    reasons, why = _reasons(path)
    assert "boxed_text" not in why, why
    assert reasons.count("stroke_grid") == 3, reasons
