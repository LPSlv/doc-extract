# /// script
# requires-python = ">=3.10"
# dependencies = ["firecrawl-anydoc==0.1.6", "pytest"]
# ///
"""Pin the anydoc behaviours the Office design depends on.

anydoc is pinned exactly and its version is in the cache key, so an upgrade
cannot serve stale artifacts. What that does NOT contain is the maintenance
risk: this design couples to several behaviours anydoc never documented, and a
0.2.0 could change any of them silently. Each test below asserts one such
behaviour against a committed fixture, so an upgrade that breaks one fails
loudly here instead of emitting wrong citations or duplicated charts.

Every assertion corresponds to a numbered claim in the design spec. When one
fails, read the spec section before "fixing" the test -- the test is the
evidence the section rests on.

Run:  uv run --with pytest python -m pytest tests/test_anydoc_invariants.py -q
"""
import io
import re
import zipfile
from pathlib import Path

import anydoc
import pytest

FIX = Path(__file__).resolve().parent / "fixtures"


# --------------------------------------------------------------- helpers
def _slide_rids(data):
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        pres = z.read("ppt/presentation.xml").decode()
    lst = re.search(r"<p:sldIdLst>(.*?)</p:sldIdLst>", pres, re.S).group(1)
    return re.findall(r'r:id="([^"]+)"', lst)


def _repack(data, rid):
    """One-slide package: sldIdLst reduced to `rid`, everything else intact."""
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        names = z.namelist()
        parts = {n: z.read(n) for n in names}
    pres = parts["ppt/presentation.xml"].decode()
    lst = re.search(r"<p:sldIdLst>(.*?)</p:sldIdLst>", pres, re.S).group(1)
    keep = [e for e in re.findall(r"<p:sldId\b[^>]*/>", lst) if f'r:id="{rid}"' in e]
    parts["ppt/presentation.xml"] = pres.replace(lst, "".join(keep)).encode()
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        for n in names:
            z.writestr(n, parts[n])
    return buf.getvalue()


def _headings(doc):
    return [(b.level, b.content[0].text) for b in doc.blocks
            if b.kind == "heading" and b.content]


def _image_inlines(blocks):
    for b in blocks:
        for i in (b.content or []):
            if i.kind == "image":
                yield i
        if b.blocks:
            yield from _image_inlines(b.blocks)


# ------------------------------------------------------- spec section 3.4
def test_repack_concatenation_equals_whole_deck():
    """Per-slide conversion is the whole deck, split. The unit boundaries the
    citation scheme needs cost nothing in text fidelity."""
    data = (FIX / "deck.pptx").read_bytes()
    whole = anydoc.to_markdown_bytes(data, "pptx").strip()
    parts = [anydoc.to_markdown_bytes(_repack(data, r), "pptx").strip()
             for r in _slide_rids(data)]
    assert "\n\n".join(p for p in parts if p) == whole


def test_repack_follows_sldidlst_not_part_names():
    """Slide order comes from the presentation part's list, so repacking by
    rId addresses the slide the user sees in PowerPoint's sidebar."""
    data = (FIX / "deck.pptx").read_bytes()
    rids = _slide_rids(data)
    first = anydoc.to_markdown_bytes(_repack(data, rids[0]), "pptx")
    last = anydoc.to_markdown_bytes(_repack(data, rids[-1]), "pptx")
    assert "Quarterly Review" in first
    assert "Revenue and Cost" in last


def test_repack_gives_per_slide_asset_placement():
    """Each repacked package gets a fresh asset sink, so per-slide assets ARE
    the placement counts UBIQUITY needs -- no rels walking required.

    The logo is on every slide (ubiquitous, furniture); the photo on one.
    """
    data = (FIX / "deck.pptx").read_bytes()
    per_slide = [{a.origin_part for a in anydoc.to_document(_repack(data, r), "pptx").assets}
                 for r in _slide_rids(data)]
    counts = {}
    for parts in per_slide:
        for p in parts:
            counts[p] = counts.get(p, 0) + 1
    assert counts["ppt/media/image1.png"] == len(per_slide)   # logo, every slide
    assert counts["ppt/media/image2.png"] == 1                # photo, one slide


# ------------------------------------------------------- spec section 4.4
def test_anydoc_already_extracts_pptx_charts():
    """The reason chart extraction is xlsx-only. Extracting these ourselves
    would emit every chart twice -- once here, once in a delimited block."""
    md = anydoc.to_markdown_bytes((FIX / "deck.pptx").read_bytes(), "pptx")
    assert "| Q1 | 1240 | 890 |" in md


def test_anydoc_surfaces_nothing_visual_for_xlsx():
    """The reason ooxml.py owns images AND charts for xlsx alone: the sheet
    path is pure cell extraction, and the package demonstrably holds both."""
    data = (FIX / "book.xlsx").read_bytes()
    names = zipfile.ZipFile(io.BytesIO(data)).namelist()
    assert "xl/media/image1.png" in names and "xl/charts/chart1.xml" in names

    doc = anydoc.to_document(data, "xlsx")
    assert doc.assets == []
    assert "Revenue by region" not in anydoc.to_markdown_bytes(data, "xlsx")


# ------------------------------------------------------- spec section 3.5
def test_empty_sheets_emit_nothing_so_names_come_from_headings():
    """book.xlsx is [Data, Empty, Notes]. anydoc emits two heading+table pairs,
    so zipping package sheet names positionally would cite Notes' table as
    'Empty' -- a confidently wrong citation, the one sin this project forbids.
    """
    doc = anydoc.to_document((FIX / "book.xlsx").read_bytes(), "xlsx")
    names = [t for _, t in _headings(doc)]
    tables = [b for b in doc.blocks if b.kind == "table"]
    assert names == ["Data", "Notes"]
    assert len(tables) == len(names)


def test_single_sheet_workbook_emits_no_heading():
    """The multi_sheet gate. The one case where the name must come from the
    package rather than from an emitted heading."""
    doc = anydoc.to_document((FIX / "single.xlsx").read_bytes(), "xlsx")
    assert _headings(doc) == []
    assert sum(1 for b in doc.blocks if b.kind == "table") == 1


# ------------------------------------------------------- spec section 3.3/3.6
def test_docx_placements_come_from_image_inlines_not_assets():
    """Asset dedup collapses bytes, not references. doc.docx places the same
    image twice: one asset, two inlines, both pointing at it. That is where a
    docx placement count comes from."""
    doc = anydoc.to_document((FIX / "doc.docx").read_bytes(), "docx")
    inlines = list(_image_inlines(doc.blocks))
    assert len(doc.assets) == 1
    assert len(inlines) == 2
    assert [i.source.asset_id for i in inlines] == [0, 0]


def test_docx_headings_are_unconditional_with_levels():
    """docx citations key off heading blocks, which -- unlike anchors -- are
    always emitted."""
    doc = anydoc.to_document((FIX / "doc.docx").read_bytes(), "docx")
    assert _headings(doc) == [(1, "Introduction"), (2, "Budget assumptions"),
                              (1, "Results")]


def test_heading_less_docx_has_no_units():
    """The citation-granularity fallback: a contract written as prose yields
    no headings at all, so it must cite as a whole document."""
    doc = anydoc.to_document((FIX / "headless.docx").read_bytes(), "docx")
    assert _headings(doc) == []
    assert list(_image_inlines(doc.blocks))


# ------------------------------------------------------- spec section 4.7
def test_error_taxonomy_classes_exist():
    """§4.7's mapping names these; a rename would silently fall through to a
    bare except and mislabel a document's terminal status."""
    for name in ("ConvertError", "UnsupportedError", "MalformedError",
                 "EncryptedError", "ResourceLimitError", "MissingPartError"):
        assert issubclass(getattr(anydoc, name), Exception)
    assert issubclass(anydoc.UnsupportedError, anydoc.ConvertError)


def test_format_detection_is_by_content():
    """Dispatch reads bytes, not extensions -- a .doc that is really a .docx
    must route correctly."""
    assert anydoc.format_from_bytes((FIX / "deck.pptx").read_bytes()) == "pptx"
    assert anydoc.format_from_bytes((FIX / "book.xlsx").read_bytes()) == "xlsx"
    assert anydoc.format_from_bytes((FIX / "doc.docx").read_bytes()) == "docx"


def test_to_document_rejects_pdf():
    """PDF has no document-model form, which is why the PDF path keeps using
    pdf-inspector and PyMuPDF directly rather than routing through anydoc."""
    pdf = (Path(__file__).resolve().parents[1] / "example" / "sample-report.pdf")
    with pytest.raises(Exception):
        anydoc.to_document(pdf.read_bytes(), "pdf")
