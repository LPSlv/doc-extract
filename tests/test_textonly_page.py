"""A whole-document collapse still renders the references page.

The incident: `cost_guard` guarantees the routed set never costs more than
reading every page, and when the routed set loses that comparison it replaces
itself with one render per page. The guarantee is about COST. Nothing in it
says the pages it then renders have anything on them, and 120 sampled
`whole_document` calls labelled by three independent labellers each found 34%
carry no figure, no table and no picture of any kind - bibliographies,
acknowledgements, two-column prose (eval/nofigure.md).

Most of that is unreachable: a prose page under a journal masthead is
branding, and twelve branding signals have already been measured with eleven
rejected (eval/tds-corpus.md). The part this file pins needs no judgement:

  - a page with NO raster placed on it and at most TEXTONLY_PATHS drawing
    paths has nothing pictorial on it. A page border and a header rule are
    two paths;
  - the drop applies ONLY inside a cost_guard collapse. Outside one, a page
    that bare never routed anything in the first place, and the routed set is
    already the cheaper of the two;
  - it runs AFTER the collapse, so it cannot un-subsume a raster and re-expand
    a page into crops. That cascade is what forced the QR-code filter to be
    reverted (eval/tds-corpus.md), and it is the reason for the ordering.

Measured blind on two corpora fetched afterwards for the purpose,
corpus/pmc_holdout and corpus/arxiv_holdout: 203 drops labelled by three
labellers each, 0 real items, 100% precision. Full method: eval/nofigure.md.
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
from harvest import (TEXTONLY_PATHS, drop_textonly, harvest,  # noqa: E402
                     page_geometry)

needs_pi = pytest.mark.skipif(
    not HAVE_PI, reason="needs pdf-inspector (see test_harvest.py for the cmd)")

W, H = 612, 792


def _prose(pg, n, rules=0):
    """A page of running text, optionally under `rules` header/footer rules."""
    pg.insert_text((70, 100), f"Section {n}", fontsize=13)
    for i, y in enumerate(range(140, 700, 22)):
        pg.insert_text((70, y), f"Body text line {i} on page {n}.", fontsize=10)
    for k in range(rules):
        y = 90 + k * 620
        pg.draw_line((56, y), (556, y))


def _raster_page(pg, seed):
    """One large raster: how a document is actually made to lose to cost_guard.

    The collapse fires when the ROUTED set outprices reading everything, and
    page renders alone can never do that - they are a subset of the same
    pages at the same edge. Only rasters can, because `cost_guard` prices
    them at their native pixel count. A 2000x2000 xref is ~3,278 tokens
    against ~659 for a letter page render, so three of them outweigh nine
    pages. Each is tinted differently so the pixel-hash dedup keeps all three.
    """
    pm = fitz.Pixmap(fitz.csRGB, fitz.IRect(0, 0, 2000, 2000), False)
    pm.set_rect(pm.irect, (40 * seed % 255, 90, 200))
    pg.insert_image(fitz.Rect(80, 120, 500, 540), pixmap=pm)
    pg.insert_text((80, 570), f"Figure {seed}. Measured response", fontsize=10)


def _chart(pg):
    """Enough vector marks to route, and enough paths to fail the drop."""
    pg.draw_line((80, 700), (540, 700))
    pg.draw_line((80, 700), (80, 120))
    for i in range(14):
        x = 90 + i * 32
        pg.draw_line((x, 700), (x, 694))
        pg.draw_line((80, 690 - i * 40), (86, 690 - i * 40))
        pg.draw_bezier((x, 660 - i * 8), (x + 10, 600), (x + 20, 500),
                       (x + 30, 420 - i * 6))
    pg.insert_text((200, 90), "Figure 1. Throughput", fontsize=10)


# ------------------------------------------------------------- the geometry
def test_a_bare_prose_page_has_no_paths():
    doc = fitz.open()
    _prose(doc.new_page(width=W, height=H), 1)
    assert page_geometry(doc[0])["paths"] == 0
    doc.close()


def test_a_header_and_footer_rule_are_two_paths():
    """The threshold's whole justification: furniture is one path per rule."""
    assert TEXTONLY_PATHS == 2
    doc = fitz.open()
    _prose(doc.new_page(width=W, height=H), 1, rules=2)
    assert page_geometry(doc[0])["paths"] == 2
    doc.close()


def test_a_chart_page_is_far_above_the_threshold():
    """Guards against the test going vacuous: if the chart fixture stopped
    having paths, every keep assertion below would pass for the wrong
    reason."""
    doc = fitz.open()
    _chart(doc.new_page(width=W, height=H))
    assert page_geometry(doc[0])["paths"] > TEXTONLY_PATHS
    doc.close()


# ---------------------------------------------------------------- the rule
def _items(pages):
    return [{"id": f"p{p:03d}-render", "page": p, "kind": "page_render",
             "reason": "whole_document"} for p in pages]


def test_a_page_carrying_a_raster_is_never_dropped():
    """`img_pages` is 0-based page indices; the items are 1-based. Getting
    that wrong drops the neighbour of every image page, silently."""
    doc = fitz.open()
    for i in range(3):
        _prose(doc.new_page(width=W, height=H), i)
    geoms = [page_geometry(p) for p in doc]
    keep, gone = drop_textonly(_items([1, 2, 3]), geoms, {1}, set())
    assert [g["page"] for g in gone] == [1, 3]
    assert [k["page"] for k in keep] == [2]
    doc.close()


def test_a_page_needing_ocr_is_never_dropped():
    """A scan usually carries an image, but a page MuPDF reports as needing
    OCR is exactly the page whose text we cannot trust, so it keeps its
    render whatever the geometry says."""
    doc = fitz.open()
    _prose(doc.new_page(width=W, height=H), 1)
    geoms = [page_geometry(doc[0])]
    keep, gone = drop_textonly(_items([1]), geoms, set(), {1})
    assert gone == [] and len(keep) == 1
    doc.close()


def test_only_whole_document_items_are_considered():
    """A `curves` or `standalone_raster` item must pass through untouched:
    outside a collapse this filter has no mandate, and the reason field is
    the only thing marking the difference."""
    doc = fitz.open()
    _prose(doc.new_page(width=W, height=H), 1)
    geoms = [page_geometry(doc[0])]
    it = _items([1])
    it[0]["reason"] = "curves"
    keep, gone = drop_textonly(it, geoms, set(), set())
    assert gone == [] and len(keep) == 1
    doc.close()


# ------------------------------------------------------------- the routing
@needs_pi
def test_a_collapsed_document_drops_its_prose_pages(tmp_path):
    """End to end. Three costly rasters make the routed set lose to the whole
    document, cost_guard collapses, and the prose pages then go."""
    doc = fitz.open()
    for i in range(3):
        _raster_page(doc.new_page(width=W, height=H), i + 1)
    for i in range(6):
        _prose(doc.new_page(width=W, height=H), i, rules=2)
    p = tmp_path / "collapsed.pdf"
    doc.save(str(p)); doc.close()

    r = harvest(str(p))
    assert r["status"] == "ok", r
    why = [d.get("why") for d in r["dropped"]]
    assert "cost_guard" in why, "fixture must actually collapse"
    assert why.count("textonly_page") == 6, why
    # the three pages that really carry something keep their render
    assert {i["page"] for i in r["items"]} == {1, 2, 3}
    assert all(i["reason"] == "whole_document" for i in r["items"])


@needs_pi
def test_an_uncollapsed_document_keeps_everything(tmp_path):
    """The same prose pages in a document that does NOT collapse are not
    dropped - they were never routed, so there is nothing to drop, and the
    filter must not reach outside cost_guard to find them."""
    doc = fitz.open()
    _chart(doc.new_page(width=W, height=H))
    for i in range(6):
        _prose(doc.new_page(width=W, height=H), i, rules=2)
    p = tmp_path / "plain.pdf"
    doc.save(str(p)); doc.close()

    r = harvest(str(p))
    assert r["status"] == "ok", r
    why = [d.get("why") for d in r["dropped"]]
    assert "cost_guard" not in why, why
    assert "textonly_page" not in why, why
