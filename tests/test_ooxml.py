# /// script
# requires-python = ">=3.10"
# dependencies = ["pytest"]
# ///
"""Package-reader tests. Standard library only, like the module under test.

Expected values are written out in full rather than derived, because the point
of these tests is to catch a reader that silently returns something plausible.
A test that computes its own expectation the same way the code does proves
nothing.
"""
import sys
import zipfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills" / "doc-extract"))
FIX = Path(__file__).resolve().parent / "fixtures"

import ooxml


# ------------------------------------------------------------------ pptx
def test_slide_rids_in_presentation_order():
    rids = ooxml.slide_rids((FIX / "deck.pptx").read_bytes())
    assert len(rids) == 3
    assert len(set(rids)) == 3           # distinct: not the same slide thrice


def test_repack_keeps_one_slide_and_every_other_part():
    data = (FIX / "deck.pptx").read_bytes()
    rids = ooxml.slide_rids(data)
    before = set(zipfile.ZipFile(__import__("io").BytesIO(data)).namelist())

    one = ooxml.repack_single(data, rids[1])
    after = set(zipfile.ZipFile(__import__("io").BytesIO(one)).namelist())

    # Only the presentation part changes; media, layouts and masters survive,
    # which is what keeps anydoc's text cascade resolvable.
    assert before == after
    assert ooxml.slide_rids(one) == [rids[1]]


def test_repack_is_idempotent_on_an_already_single_slide_package():
    data = (FIX / "deck.pptx").read_bytes()
    rid = ooxml.slide_rids(data)[0]
    once = ooxml.repack_single(data, rid)
    assert ooxml.slide_rids(ooxml.repack_single(once, rid)) == [rid]


def test_main_part_comes_from_root_rels():
    with zipfile.ZipFile(FIX / "deck.pptx") as zf:
        assert ooxml.main_part(zf) == "ppt/presentation.xml"


# ------------------------------------------------------------------ xlsx
def test_sheet_names_includes_the_empty_sheet():
    """The package knows about Empty; anydoc's output does not. That mismatch
    is exactly why multi-sheet names come from headings instead."""
    with zipfile.ZipFile(FIX / "book.xlsx") as zf:
        assert ooxml.sheet_names(zf) == ["Data", "Empty", "Notes"]


def test_single_sheet_name_available_for_the_no_heading_case():
    with zipfile.ZipFile(FIX / "single.xlsx") as zf:
        assert ooxml.sheet_names(zf) == ["Budget"]


def test_chart_resolves_ranges_when_the_producer_wrote_no_cache():
    """openpyxl writes c:f references and no numCache at all. Reading the
    reference against the workbook's own sheets recovers the exact values --
    which is strictly better than a vision call, since these are the numbers
    rather than an estimate read off pixels."""
    with zipfile.ZipFile(FIX / "book.xlsx") as zf:
        got = ooxml.charts(zf)

    assert len(got) == 1
    chart = got[0]
    assert chart["title"] == "Revenue by region"
    assert chart["complete"] is True
    assert chart["headers"] == ["", "revenue"]
    assert chart["rows"] == [["North", "1240"], ["South", "1310"], ["East", "1180"]]


def test_images_are_attributed_to_their_sheet():
    """Without the sheet, there is no placement count, and a logo repeated on
    every sheet cannot be told from a chart image on one."""
    with zipfile.ZipFile(FIX / "book.xlsx") as zf:
        assert ooxml.images(zf) == [("xl/media/image1.png", "Data")]


def test_workbook_with_no_charts_returns_empty_not_error():
    with zipfile.ZipFile(FIX / "single.xlsx") as zf:
        assert ooxml.charts(zf) == []
        assert ooxml.images(zf) == []


# ------------------------------------------------------------------ helpers
@pytest.mark.parametrize("ref,expect", [
    ("Data!$B$2:$B$4", ("Data", ["B2", "B3", "B4"])),
    ("Data!$A$1", ("Data", ["A1"])),
    ("'My Sheet'!$A$1:$B$1", ("My Sheet", ["A1", "B1"])),
    ("Sheet1!$Z$1:$AA$1", ("Sheet1", ["Z1", "AA1"])),
])
def test_range_expansion(ref, expect):
    assert ooxml._expand(ref) == expect


def test_column_index_crosses_the_26_boundary():
    assert ooxml._col_index("A") == 1
    assert ooxml._col_index("Z") == 26
    assert ooxml._col_index("AA") == 27
