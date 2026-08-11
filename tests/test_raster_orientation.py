"""A routed raster must be handed over the way the page draws it.

The incident: ti_drv8825.pdf p11 draws its motor-control block diagram with a
flipped placement matrix. convert.py extracted the image XObject's own samples
with fitz.Pixmap(doc, xref), which ignores that matrix, and shipped the
diagram upside down. Every label in it was unreadable, and the vision pass
described a mirrored image without ever signalling a problem.

Nothing caught it because nothing in this suite looks at image *pixels* - the
byte-identity gate compares markdown, and the harvest tests compare routing
decisions. This file is the missing check.
"""
import pathlib
import sys

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "skills" / "doc-extract"))

# These tests build real PDFs, so unlike the pure routing tests there is
# nothing meaningful to stub: skip when PyMuPDF is absent, as test_harvest.py
# does for its end-to-end cases.
fitz = pytest.importorskip("fitz", reason="needs PyMuPDF to build a test PDF")
from convert import _raster_pixmap


BLACK, WHITE = 0, 255


def _half_and_half():
    """A pixmap whose top half is black and bottom half white - asymmetric on
    the one axis that matters, so a vertical flip cannot hide."""
    pm = fitz.Pixmap(fitz.csGRAY, fitz.IRect(0, 0, 40, 40), False)
    pm.set_rect(fitz.IRect(0, 0, 40, 20), (BLACK,))
    pm.set_rect(fitz.IRect(0, 20, 40, 40), (WHITE,))
    return pm


def _top_row_mean(pm):
    g = pm if pm.n == 1 else fitz.Pixmap(fitz.csGRAY, pm)
    row = g.samples[: g.width]
    return sum(row) / len(row)


def _bottom_row_mean(pm):
    g = pm if pm.n == 1 else fitz.Pixmap(fitz.csGRAY, pm)
    row = g.samples[(g.height - 1) * g.width: g.height * g.width]
    return sum(row) / len(row)


def _doc_with_image(rotate):
    doc = fitz.open()
    page = doc.new_page(width=200, height=200)
    page.insert_image(fitz.Rect(20, 20, 180, 180), pixmap=_half_and_half(),
                      rotate=rotate)
    xref = page.get_images(full=True)[0][0]
    return doc, {"page": 1, "xref": xref, "kind": "raster"}


def test_unrotated_placement_is_unchanged():
    """The common case must not regress: no placement transform, no surprise."""
    doc, item = _doc_with_image(0)
    pm = _raster_pixmap(doc, item)
    assert _top_row_mean(pm) < 64, "top of an unrotated image should stay dark"
    assert _bottom_row_mean(pm) > 191, "bottom should stay light"
    doc.close()


def test_rotated_placement_follows_the_page_not_the_stored_samples():
    """The incident, in miniature.

    The stored samples are dark-on-top. Drawn at 180 degrees the page shows
    light-on-top. What we hand the model must match the page.
    """
    doc, item = _doc_with_image(180)
    pm = _raster_pixmap(doc, item)
    assert _top_row_mean(pm) > 191, (
        "raster was handed over in stored-sample order, ignoring the page's "
        "placement matrix - this is the ti_drv8825 p11 upside-down bug")
    assert _bottom_row_mean(pm) < 64
    doc.close()


def test_raw_extraction_would_have_failed_this():
    """Pins the mechanism, so the test cannot quietly stop testing anything.

    If a future PyMuPDF makes Pixmap(doc, xref) matrix-aware on its own, this
    fails and the guard above becomes redundant - worth knowing either way.
    """
    doc, item = _doc_with_image(180)
    raw = fitz.Pixmap(doc, item["xref"])
    assert _top_row_mean(raw) < 64, (
        "raw xref extraction no longer ignores the placement matrix; "
        "re-evaluate whether _raster_pixmap still needs to clip-render")
    doc.close()


def test_unplaced_xref_still_yields_something():
    """An xref the page does not draw has no bbox; fall back, do not crash."""
    doc, item = _doc_with_image(0)
    pm = _raster_pixmap(doc, {**item, "xref": item["xref"], "page": 1})
    assert pm.width > 0 and pm.height > 0
    doc.close()
