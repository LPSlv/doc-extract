"""A routed raster must be handed over the way the page draws it.

The incident: ti_drv8825.pdf p11 draws its motor-control block diagram with a
flipped placement matrix. convert.py extracted the image XObject's own samples
with fitz.Pixmap(doc, xref), which ignores that matrix, and shipped the
diagram upside down. Every label in it was unreadable, and the vision pass
described a mirrored image without ever signalling a problem.

Nothing caught it because nothing in this suite looks at image *pixels* - the
byte-identity gate compares markdown, and the harvest tests compare routing
decisions. This file is the missing check.

The first fix then broke worse things, all pinned here: on a /Rotate page it
cropped a full-width figure to a square (arxiv 2607.29183v1 pp.4,6) or shipped
pure white, and capping the render scale at a multiple of the *placement*
silently downsampled high-resolution images that happen to be placed small.
"""
import pathlib
import sys
import types

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "skills" / "doc-extract"))

# convert -> harvest -> pdf_inspector, which the bare pytest environment does
# not have. test_harvest.py stubs it for the same reason; without this the
# whole module ERRORs at collection instead of skipping, which is how it went
# unnoticed that CI was not running these at all.
try:
    import pdf_inspector                                        # noqa: F401
except ImportError:
    sys.modules["pdf_inspector"] = types.ModuleType("pdf_inspector")

fitz = pytest.importorskip("fitz", reason="needs PyMuPDF to build a test PDF")
from convert import _raster_pixmap, MAX_EDGE_PX

BLACK, WHITE = 0, 255


def _half_and_half(n=40):
    """Top half black, bottom half white - asymmetric on the one axis a
    vertical flip would hide."""
    pm = fitz.Pixmap(fitz.csGRAY, fitz.IRect(0, 0, n, n), False)
    pm.set_rect(fitz.IRect(0, 0, n, n // 2), (BLACK,))
    pm.set_rect(fitz.IRect(0, n // 2, n, n), (WHITE,))
    return pm


def _row_mean(pm, y):
    g = pm if pm.n == 1 else fitz.Pixmap(fitz.csGRAY, pm)
    row = g.samples[y * g.width: (y + 1) * g.width]
    return sum(row) / len(row)


def _top(pm):
    return _row_mean(pm, 0)


def _bottom(pm):
    g = pm if pm.n == 1 else fitz.Pixmap(fitz.csGRAY, pm)
    return _row_mean(pm, g.height - 1)


def _doc(rotate=0, page_rotation=0, native=40, rect=(20, 20, 180, 180)):
    doc = fitz.open()
    page = doc.new_page(width=200, height=200)
    page.insert_image(fitz.Rect(*rect), pixmap=_half_and_half(native), rotate=rotate)
    if page_rotation:
        page.set_rotation(page_rotation)
    xref = page.get_images(full=True)[0][0]
    return doc, {"page": 1, "xref": xref, "kind": "raster"}


def test_unrotated_placement_is_unchanged():
    """The common case must not regress."""
    doc, item = _doc()
    pm = _raster_pixmap(doc, item)
    assert _top(pm) < 64 and _bottom(pm) > 191
    doc.close()


def test_rotated_placement_follows_the_page_not_the_stored_samples():
    """The original incident, in miniature: samples are dark-on-top, the page
    draws them light-on-top, and what we hand over must match the page."""
    doc, item = _doc(rotate=180)
    pm = _raster_pixmap(doc, item)
    assert _top(pm) > 191, (
        "raster handed over in stored-sample order, ignoring the placement "
        "matrix - the ti_drv8825 p11 upside-down bug")
    assert _bottom(pm) < 64
    doc.close()


def test_raw_extraction_would_have_failed_this():
    """Pins the mechanism so the guard above cannot go vacuous."""
    doc, item = _doc(rotate=180)
    raw = fitz.Pixmap(doc, item["xref"])
    assert _top(raw) < 64, (
        "raw xref extraction no longer ignores the placement matrix; "
        "re-evaluate whether _raster_pixmap still needs to clip-render")
    doc.close()


@pytest.mark.parametrize("rotation", [90, 180, 270])
def test_page_rotation_does_not_crop_or_blank_the_image(rotation):
    """get_image_info() reports bbox in unrotated space; clip= expects rotated.

    Without page.rotation_matrix this shipped a wrong square crop on
    arxiv 2607.29183v1 pp.4,6 and pure white on a synthetic 200x400 page.
    """
    doc = fitz.open()
    page = doc.new_page(width=200, height=400)
    page.insert_image(fitz.Rect(20, 20, 180, 380), pixmap=_half_and_half())
    page.set_rotation(rotation)
    xref = page.get_images(full=True)[0][0]

    pm = _raster_pixmap(doc, {"page": 1, "xref": xref, "kind": "raster"})
    assert not pm.is_unicolor, f"/Rotate {rotation} produced a blank image"
    # the image is half dark and half light whatever way the page is turned
    g = pm if pm.n == 1 else fitz.Pixmap(fitz.csGRAY, pm)
    mean = sum(g.samples) / len(g.samples)
    assert 64 < mean < 191, f"/Rotate {rotation} lost most of the image (mean {mean:.0f})"
    doc.close()


def test_high_resolution_image_placed_small_keeps_its_detail():
    """A 1200px image drawn into a 60pt box must not ship at 60-ish pixels.

    Schematics and scope captures are routinely placed small; capping the
    render at a fixed multiple of the placement threw away the detail that
    made them worth a vision call.
    """
    doc = fitz.open()
    page = doc.new_page(width=200, height=200)
    page.insert_image(fitz.Rect(20, 20, 80, 80), pixmap=_half_and_half(1200))
    xref = page.get_images(full=True)[0][0]

    pm = _raster_pixmap(doc, {"page": 1, "xref": xref, "kind": "raster"})
    assert max(pm.width, pm.height) >= 1000, (
        f"native 1200px image placed in a 60pt box emitted only "
        f"{pm.width}x{pm.height}")
    doc.close()


def test_render_stays_within_the_downstream_pixel_budget():
    """Preserving detail must not become unbounded: _write_image only halves,
    so the scale cap is what keeps a huge placement from exploding."""
    doc = fitz.open()
    page = doc.new_page(width=2000, height=2000)
    page.insert_image(fitz.Rect(0, 0, 2000, 2000), pixmap=_half_and_half(9000))
    xref = page.get_images(full=True)[0][0]

    pm = _raster_pixmap(doc, {"page": 1, "xref": xref, "kind": "raster"})
    assert max(pm.width, pm.height) <= MAX_EDGE_PX * 2 + 2
    doc.close()


def test_fully_occluded_image_falls_back_instead_of_shipping_blank():
    """Rendering the region captures whatever the page draws there. An image
    hidden under an opaque rectangle would otherwise ship as pure white with
    no error at all - a silent total loss."""
    doc = fitz.open()
    page = doc.new_page(width=200, height=200)
    page.insert_image(fitz.Rect(20, 20, 180, 180), pixmap=_half_and_half())
    page.draw_rect(fitz.Rect(0, 0, 200, 200), color=(1, 1, 1), fill=(1, 1, 1))
    xref = page.get_images(full=True)[0][0]

    pm = _raster_pixmap(doc, {"page": 1, "xref": xref, "kind": "raster"})
    assert not pm.is_unicolor, "occluded image shipped blank instead of falling back"
    doc.close()


def test_xref_present_in_resources_but_never_drawn_falls_back():
    """harvest builds item['page'] from get_images(), which lists a page's
    resources rather than what it draws. An xref that is listed but never
    painted has no placement, and the stored samples are all there is."""
    doc = fitz.open()
    drawn = doc.new_page(width=200, height=200)
    drawn.insert_image(fitz.Rect(20, 20, 180, 180), pixmap=_half_and_half())
    xref = drawn.get_images(full=True)[0][0]

    blank = doc.new_page(width=200, height=200)
    assert not [i for i in blank.get_image_info(xrefs=True) if i.get("xref") == xref]

    pm = _raster_pixmap(doc, {"page": 2, "xref": xref, "kind": "raster"})
    assert pm.width > 0 and pm.height > 0
    assert _top(pm) < 64, "fallback should return the stored samples verbatim"
    doc.close()
