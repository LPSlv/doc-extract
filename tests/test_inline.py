# /// script
# requires-python = ">=3.10"
# dependencies = ["pytest", "firecrawl-anydoc==0.1.6", "pymupdf==1.28.0",
#                 "pdf-inspector==0.2.6"]
# ///
"""Tests for inline placement: where a description lands, and what it may not do.

Inline placement puts each description at its image's position instead of in
one block at the end. The byte-identity guarantee survives that only because
the block is INSERTED beside the engine's own line, never substituted for it --
`eval/gate.py` fails the moment anything is edited in place.

What byte-identity cannot check is whether the position is the right one: an
insertion round-trips wherever it lands. So the anchor rule has to be provable
on its own, and these tests are that proof. The rule is: an image's own line is
used only when the number of whole-line matches for its alt text equals the
number of image inlines carrying that alt text; otherwise the description goes
to the end of the unit, a position that is computed rather than matched.

Every case below is a real collision, measured against a committed fixture:

  deck.pptx        two placeholders on one slide, one of them furniture --
                   the description must land on the photo's line, not the logo's
  imageheavy.pptx  three adjacent identical placeholders per slide
  collide.pptx     prose that renders byte-identically to a placeholder
  doc.docx         a format that emits no placeholder at all
  book.xlsx        images and charts anydoc never renders
  sample-report.pdf  no anchor is knowable at all

Run:  uv run --with pytest --with firecrawl-anydoc==0.1.6 --with pymupdf==1.28.0
      --with pdf-inspector==0.2.6 python -m pytest tests/test_inline.py -q
"""
import json
import pathlib
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills" / "doc-extract"))

import anydoc                                             # noqa: E402
import office                                             # noqa: E402
from artifact import OPEN, strip                          # noqa: E402
from cache import cache_dir                               # noqa: E402
from convert import convert                               # noqa: E402
from describe import main as describe_main, rebuild       # noqa: E402

FIX = ROOT / "tests" / "fixtures"
PDF = ROOT / "example" / "sample-report.pdf"
OFFICE = ["deck.pptx", "imageheavy.pptx", "collide.pptx",
          "doc.docx", "headless.docx", "book.xlsx", "single.xlsx"]


def engine_markdown(path):
    """What the text engine says, by the same route the pipeline takes."""
    data = pathlib.Path(path).read_bytes()
    fmt = anydoc.format_from_bytes(data)
    if fmt != "pptx":
        return anydoc.to_markdown_bytes(data, fmt)
    import ooxml
    parts = [anydoc.to_markdown_bytes(ooxml.repack_single(data, r), "pptx").strip()
             for r in ooxml.slide_rids(data)]
    return "\n\n".join(p for p in parts if p)


def run(path, tmp_path, inline=True, twice=False):
    """Convert, describe everything pending, return (report, manifest, doc.md)."""
    r = convert(str(path), root=tmp_path, force=True, inline=inline)
    assert r["status"] == "ok", r
    for item in r["pending"]:
        describe_main([r["artifact"], item["id"], f"Description of {item['id']}."])
        if twice:
            describe_main([r["artifact"], item["id"], f"Description of {item['id']}."])
    art = pathlib.Path(r["artifact"])
    man = json.loads((art / "manifest.json").read_text())
    return r, man, (art / "doc.md").read_text()


def items_by_id(man):
    return {i["id"]: i for i in man["items"]}


def block_positions(produced):
    """Offsets into the stripped text where blocks were inserted."""
    import re
    from artifact import CLOSE
    pat = re.compile("\n" + re.escape(OPEN) + "\n.*?\n" + re.escape(CLOSE) + "\n",
                     re.DOTALL)
    out, removed = [], 0
    for m in pat.finditer(produced):
        out.append(m.start() - removed)
        removed += m.end() - m.start()
    return out


# --------------------------------------------------------------- the split
@pytest.mark.parametrize("name", OFFICE)
@pytest.mark.parametrize("level", [1, 2])
def test_span_split_agrees_with_the_split_citations_use(name, level):
    """`_split_spans` is a second implementation of `_split_markdown`, kept
    separate because the citation split is load-bearing and pinned elsewhere.
    Two implementations that disagree would anchor into the wrong unit."""
    md = engine_markdown(FIX / name)
    assert [(lab, md[s:e].strip()) for lab, s, e in office._split_spans(md, level)] \
        == office._split_markdown(md, level)


# ------------------------------------------------------- the anchor itself
def test_the_photos_line_is_the_anchor_not_the_logos():
    """deck.pptx slide 2 emits two identical placeholders: the logo (dropped as
    furniture) and the photo (the one item). Anchoring on "the first
    placeholder in the unit" would describe the photo at the logo's position."""
    md = engine_markdown(FIX / "deck.pptx")
    man = json.loads(_manifest_only(FIX / "deck.pptx"))
    anchor = items_by_id(man)["image2-png"]["anchor"]
    # Second of the two placeholder lines on slide 2, not the first.
    slide2 = md.index("## Site Photograph")
    first = md.index("image.png", slide2) + len("image.png")
    assert anchor > first
    assert md[anchor - len("image.png"):anchor] == "image.png"
    assert md[anchor:anchor + 2] == "\n\n"


def test_adjacent_placeholders_get_distinct_anchors_in_reading_order():
    """imageheavy.pptx puts three placeholders in a row on every slide. They
    are byte-identical to each other, so the mapping can only come from
    position -- and three items must not collapse onto one."""
    man = json.loads(_manifest_only(FIX / "imageheavy.pptx"))
    anchors = [i["anchor"] for i in man["items"]]
    assert len(anchors) == 30
    assert len(set(anchors)) == 30, "adjacent placeholders shared an anchor"
    assert anchors == sorted(anchors), "anchors are not in reading order"


def test_prose_identical_to_the_placeholder_disables_the_anchor():
    """collide.pptx s01 is a text box reading `image.png` above a picture: two
    candidate lines, one picture. The count check must reject BOTH rather than
    describe the picture at the sentence about it."""
    md = engine_markdown(FIX / "collide.pptx")
    man = json.loads(_manifest_only(FIX / "collide.pptx"))
    anchor = items_by_id(man)["image1-png"]["anchor"]
    unit_end = md.index("\n\n## File table")
    assert anchor == unit_end, "fell back to something other than the unit end"


def test_placeholder_inside_a_table_row_is_not_a_candidate_line():
    """collide.pptx s02 hides the same string in a table cell. Whole-line
    matching means the row is not a candidate, so the picture keeps its own
    anchor instead of being disabled by a false collision."""
    md = engine_markdown(FIX / "collide.pptx")
    man = json.loads(_manifest_only(FIX / "collide.pptx"))
    anchor = items_by_id(man)["image2-png"]["anchor"]
    assert md[anchor - len("image.png"):anchor] == "image.png"
    assert md[:anchor].count("| asset | image.png |") == 1, "anchored on the row"


def test_a_caption_repeating_the_alt_text_disables_the_anchor():
    """collide.pptx s03: two pictures with author alt text "Site plan", plus a
    caption paragraph of the same words. Three lines, two pictures -- the
    placeholder is whatever the author wrote, so this is not a corner case."""
    md = engine_markdown(FIX / "collide.pptx")
    man = json.loads(_manifest_only(FIX / "collide.pptx"))
    end = len(md)
    for item_id in ("image3-png", "image4-png"):
        assert items_by_id(man)[item_id]["anchor"] == end


def test_docx_pictures_emit_no_placeholder_so_they_anchor_to_the_section():
    """The empirical fact the docx path rests on: anydoc renders a picture as
    its alt text, and Word writes none unless the author typed one, so
    doc.docx's markdown contains no trace of either picture. Section end is
    then the closest position that is computed rather than guessed."""
    md = engine_markdown(FIX / "doc.docx")
    assert "image" not in md and "!" not in md
    man = json.loads(_manifest_only(FIX / "doc.docx"))
    item = items_by_id(man)["image1-png"]
    assert item["page"] == "Introduction"
    assert item["anchor"] == md.index("\n# Results")


def test_xlsx_chart_anchors_to_the_end_of_its_own_sheet():
    """xlsx images and charts come from the package, not from anydoc, so there
    is nothing rendered to anchor to. The sheet's block end still is."""
    md = engine_markdown(FIX / "book.xlsx")
    man = json.loads(_manifest_only(FIX / "book.xlsx"))
    chart = items_by_id(man)["chart01"]
    assert chart["page"] == "Data"
    # The sheet's chunk ends after its blank last line, one character past the
    # start of the separator before the next heading. Both sides are a line
    # boundary; what matters is that the chart lands inside Data, not at the
    # end of the workbook.
    assert md[:chart["anchor"]].endswith("| East | 1180 | 951 |\n")
    assert md[chart["anchor"]:].startswith("\n## Notes")


def test_pdf_items_carry_no_anchor_at_all(tmp_path):
    """pdf-inspector's per-page text comes from a different extractor and is
    often not even a substring of the document text, so no position in doc.md
    is knowable. --inline must therefore change nothing for a PDF."""
    r, man, produced = run(PDF, tmp_path, inline=True)
    assert man["items"], "the sample PDF should route at least one item"
    assert all(i.get("anchor") is None for i in man["items"])
    assert produced.count(OPEN) == 1
    assert block_positions(produced) == [len(strip(produced))]


def test_standalone_image_has_no_anchor_either(tmp_path):
    """An image file's engine text is empty; there is no position to hold."""
    png = tmp_path / "shot.png"
    png.write_bytes((FIX / "collide.pptx").read_bytes()[:0] + _tiny_png())
    r, man, produced = run(png, tmp_path / "cache", inline=True)
    assert [i.get("anchor") for i in man["items"]] == [None]


# ------------------------------------------------------- end to end, real
@pytest.mark.parametrize("name", OFFICE)
def test_inline_output_still_strips_to_the_engines_bytes(name, tmp_path):
    """The guarantee, through the real pipeline, in the new mode."""
    r, man, produced = run(FIX / name, tmp_path, inline=True)
    assert strip(produced) == engine_markdown(FIX / name)
    # single.xlsx routes nothing at all -- no images, no charts -- so there is
    # legitimately nothing to add. Everything else must have written.
    if any(i.get("description") for i in man["items"]):
        assert produced != strip(produced), "nothing was written at all"


@pytest.mark.parametrize("name", OFFICE)
def test_every_block_starts_on_a_line_boundary(name, tmp_path):
    """Stripping restores the bytes even from a block spliced into the middle
    of a word, so byte-identity would not catch it -- a reader would."""
    r, man, produced = run(FIX / name, tmp_path, inline=True)
    residue = strip(produced)
    for pos in block_positions(produced):
        assert pos in (0, len(residue)) \
            or residue[pos - 1] == "\n" or residue[pos] == "\n"


def test_blocks_land_exactly_where_the_manifest_said(tmp_path):
    r, man, produced = run(FIX / "collide.pptx", tmp_path, inline=True)
    described = [i for i in man["items"] if i.get("description")]
    assert described
    assert {i["anchor"] for i in described} <= set(block_positions(produced))


def test_a_resumed_run_neither_duplicates_nor_drifts(tmp_path):
    """Offsets are into the ENGINE text and rebuild strips before splicing, so
    describing the same item twice must reproduce the same file."""
    _, man_once, once = run(FIX / "deck.pptx", tmp_path / "a", inline=True)
    _, man_twice, twice = run(FIX / "deck.pptx", tmp_path / "b", inline=True,
                              twice=True)
    assert once == twice
    assert twice.count(OPEN) == 1
    assert strip(twice) == engine_markdown(FIX / "deck.pptx")


def test_trailing_placement_ignores_anchors_entirely(tmp_path):
    """The default is unchanged: one block, at the end, whatever the manifest
    knows about positions."""
    r, man, produced = run(FIX / "collide.pptx", tmp_path, inline=False)
    assert man["placement"] == "trailing"
    assert any(i.get("anchor") is not None for i in man["items"])
    assert produced.count(OPEN) == 1
    assert block_positions(produced) == [len(strip(produced))]
    assert "## Figures and scanned pages" in produced


def test_the_two_placements_do_not_share_a_cache_directory(tmp_path):
    """An artifact built inline and served to a run that asked for trailing
    would be silently the wrong shape -- the two differ only in layout."""
    assert cache_dir(FIX / "deck.pptx", root=tmp_path, placement="inline") \
        != cache_dir(FIX / "deck.pptx", root=tmp_path, placement="trailing")


def test_a_stale_anchor_is_ignored_rather_than_trusted(tmp_path):
    """Manifests outlive the code that wrote them. An offset past the end of
    the engine text must degrade to the trailing block, not raise and not land
    inside a word."""
    art = tmp_path / "art"
    art.mkdir()
    base = "# Title\n\nBody text.\n"
    (art / "doc.md").write_text(base)
    (art / "manifest.json").write_text(json.dumps({
        "placement": "inline",
        "items": [{"id": "x", "page": "doc", "kind": "raster",
                   "reason": "standalone_raster", "anchor": 9999,
                   "description": "A photo."},
                  {"id": "y", "page": "doc", "kind": "raster",
                   "reason": "standalone_raster", "anchor": "5",
                   "description": "Another."}],
        "dropped": []}))
    assert rebuild(art) == 2
    produced = (art / "doc.md").read_text()
    assert strip(produced) == base
    assert block_positions(produced) == [len(base)]


# ------------------------------------------------------------------ helpers
def _manifest_only(path):
    """The manifest a convert of `path` produces, without keeping the artifact.

    Anchors are computed by the harvester, so this exercises the real code
    rather than a re-implementation of it.
    """
    import tempfile
    with tempfile.TemporaryDirectory() as root:
        r = convert(str(path), root=root, force=True, inline=True)
        return (pathlib.Path(r["artifact"]) / "manifest.json").read_text()


def _tiny_png():
    import base64
    return base64.b64decode(
        "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmM"
        "IQAAAABJRU5ErkJggg==")
