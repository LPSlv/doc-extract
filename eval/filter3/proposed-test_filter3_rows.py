"""Filter 3 stops speaking for a page on the strength of a one-row table.

The incident: `if pm.count("\\n|") >= 3: continue` skips a page because the
extractor produced a pipe table for it. Three pipe lines is a header, a
separator rule and ONE data row. The skip happens before `render_reason` ever
runs, so a page carrying a chart and a one-row table is discarded for the
table and the chart goes with it - and on a page with no raster nothing else
on that page is routed either, so nothing downstream can recover it.

Measured over the 711-document base (eval/filter3.md): 4,065 pages are
discarded this way, in 409 documents, and 164 of 250 sampled and labelled
blind by three labellers each carry a real figure - 66%, which is the same
rate at which the `curves` pages the router DOES route carry one
(eval/nofigure.md). Requiring `FILTER3_ROWS` pipe lines takes the 400 pages
whose table is a single row: 87% carry a figure in-sample, 73% (95% CI 62-82)
across 71 blind labels on corpus/arxiv_holdout and corpus/pmc_holdout.

Three things are pinned here, and the third is the one that keeps this from
re-importing a rejected change:

  - a page with figure signal, no raster and a one-row table is now rendered;
  - a page with figure signal, no raster and a real table is still skipped;
  - a page that CARRIES a raster keeps the old threshold. Rendering those is
    the swap eval/multifigure.md priced and rejected: a page render caps the
    raster at its placement, costing the figure that is already being read a
    median 0.27x linear resolution.

`pdf_inspector` is stubbed rather than run, because this test is about the
routing decision and not about the extractor: the markdown each page gets is
the input under test.
"""
import pathlib
import sys
import types

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "skills" / "doc-extract"))

try:
    import pdf_inspector                                        # noqa: F401
except ImportError:
    sys.modules["pdf_inspector"] = types.ModuleType("pdf_inspector")

fitz = pytest.importorskip("fitz", reason="needs PyMuPDF to build a test PDF")
import harvest                                                  # noqa: E402
from harvest import FILTER3_ROWS                                # noqa: E402

W, H = 612, 792


def _chart(pg, n):
    """`curves` figure signal: bezier artwork over a substantial region.

    `n` varies per page so no two pages share a signature; identical
    signatures on every page would trip the vector_furniture template.
    """
    for k in range(n):
        x = 80 + k * 7
        pg.draw_bezier((x, 600), (x + 30, 400), (x + 60, 600), (x + 90, 300))
    pg.draw_rect(fitz.Rect(70, 280, 540, 620))


def _table_md(rows):
    """Markdown for a table with `rows` data rows: 2 + rows pipe lines."""
    out = ["", "| a | b |", "| --- | --- |"]
    out += [f"| {i} | {i} |" for i in range(rows)]
    return "\n".join(out)


def _doc(tmp_path, with_raster_on=()):
    doc = fitz.open()
    for i in range(3):
        pg = doc.new_page(width=W, height=H)
        pg.insert_text((70, 100), f"Page {i + 1}", fontsize=11)
        _chart(pg, 10 + i)
        if i in with_raster_on:
            pm = fitz.Pixmap(fitz.csRGB, fitz.IRect(0, 0, 300, 300))
            pm.set_rect(pm.irect, (200, 30, 90))
            pg.insert_image(fitz.Rect(300, 80, 520, 260), pixmap=pm)
    p = tmp_path / "f3.pdf"
    doc.save(str(p))
    doc.close()
    return str(p)


def _stub_pi(monkeypatch, mds):
    """Make pdf_inspector return exactly `mds` as the per-page markdown."""
    ns = types.SimpleNamespace(
        detect_pdf=lambda p: types.SimpleNamespace(
            pdf_type="digital", pages_needing_ocr=[]),
        process_pdf=lambda p: types.SimpleNamespace(
            markdown="body text\n" + "\n".join(mds)),
        extract_pages_markdown=lambda p: types.SimpleNamespace(
            pages=[types.SimpleNamespace(page=i, markdown=m)
                   for i, m in enumerate(mds)]))
    monkeypatch.setattr(harvest, "pi", ns)


def _rendered(res):
    return {it["page"] for it in res["items"] if it["kind"] == "page_render"}


def test_one_row_table_no_longer_silences_a_figure(tmp_path, monkeypatch):
    mds = [_table_md(1), _table_md(FILTER3_ROWS - 1), "just prose"]
    _stub_pi(monkeypatch, mds)
    res = harvest.harvest(_doc(tmp_path))
    assert res["status"] == "ok"
    # page 1: one data row -> 3 pipe lines -> below FILTER3_ROWS -> rendered
    assert 1 in _rendered(res)
    # page 2: enough rows to reach FILTER3_ROWS -> still skipped
    assert 2 not in _rendered(res)
    # page 3: no table at all -> rendered, exactly as before
    assert 3 in _rendered(res)


def test_a_real_table_still_wins(tmp_path, monkeypatch):
    _stub_pi(monkeypatch, [_table_md(8)] * 3)
    res = harvest.harvest(_doc(tmp_path))
    assert _rendered(res) == set()
    assert res["vision_calls"] == 0


def test_a_page_carrying_a_raster_keeps_the_old_threshold(tmp_path, monkeypatch):
    """The multifigure swap must not sneak in through this door."""
    _stub_pi(monkeypatch, [_table_md(1)] * 3)
    res = harvest.harvest(_doc(tmp_path, with_raster_on=(0,)))
    # page 1 carries a raster: 3 pipe lines still silences it, and the raster
    # is routed on its own, at its own resolution.
    assert 1 not in _rendered(res)
    assert any(it["kind"] == "raster" and it["page"] == 1 for it in res["items"])
    # its neighbours carry no raster, so the one-row table no longer speaks
    assert {2, 3} <= _rendered(res)


def test_the_constant_is_two_data_rows():
    """A header, a separator and two data rows. Moving it needs a holdout:
    eval/filter3.md sweeps 3..20 and the precision falls monotonically."""
    assert FILTER3_ROWS == 4
