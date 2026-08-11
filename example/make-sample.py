# /// script
# requires-python = ">=3.10"
# dependencies = ["pymupdf==1.28.0"]
# ///
"""Regenerate example/sample-report.pdf.

The sample used to have no provenance - it was built by hand, which meant its
body text still called the project by an old name long after the rename, and
nobody could regenerate it without guessing. This script is that provenance.

The document is deliberately shaped to exercise one routing decision each way:

  - ordinary body text            extracted, no vision
  - a ruled table                 extracted as Markdown, no vision (already handled)
  - one embedded chart raster     routed -> exactly one vision call

Keep that shape. If the table stops extracting or a second image appears, the
quick-start output in README.md stops matching what a new user sees.

    uv run example/make-sample.py && uv run eval/gate.py example/
"""
import pathlib
import fitz

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "sample-report.pdf"
FIGURE = HERE / "sample-report.figure.png"

BODY = """This is a synthetic document used as the runnable example for the
doc-extract skill. It contains ordinary body text, a table that a text
extractor can parse on its own, and a chart that it cannot. Running the skill
over it should extract all the text, skip the table (already handled), and send
exactly one image to a vision pass."""

ROWS = [("Category", "Planned", "Actual"),
        ("Personnel", "48,000", "45,200"),
        ("Equipment", "22,000", "24,800"),
        ("Travel", "6,000", "3,100"),
        ("Total", "76,000", "73,100")]

TAIL = """Actual spend tracked plan closely through Q2 but diverged in Q3 as
equipment procurement slipped. The variance is expected to close in Q1 of the
following year."""


def main():
    doc = fitz.open()
    page = doc.new_page(width=595, height=842)      # A4
    x0, y = 57, 70

    page.insert_text((x0, y), "Sample Project Report", fontname="hebo", fontsize=18)
    y += 32
    page.insert_text((x0, y), "Work package 3 - quarterly summary",
                     fontname="hebo", fontsize=13)
    y += 24
    page.insert_textbox(fitz.Rect(x0, y, 538, y + 90), " ".join(BODY.split()),
                        fontname="helv", fontsize=10.5, lineheight=1.35)
    y += 96

    page.insert_text((x0, y), "Budget by category", fontname="hebo", fontsize=12)
    y += 16

    # A ruled table: pdf-inspector recovers this as Markdown, so it must NOT
    # cost a vision call. The rules are what make it a table rather than
    # columns of loose text.
    col, rowh = [x0, x0 + 190, x0 + 300, x0 + 410], 20
    top = y
    for r, row in enumerate(ROWS):
        for c, cell in enumerate(row):
            page.insert_text((col[c] + 6, y + 14), cell,
                             fontname="hebo" if r == 0 else "helv", fontsize=10)
        y += rowh
        page.draw_line(fitz.Point(x0, y), fitz.Point(col[3], y),
                       color=(0.6, 0.6, 0.6), width=0.6)
    page.draw_line(fitz.Point(x0, top), fitz.Point(col[3], top),
                   color=(0.6, 0.6, 0.6), width=0.6)
    for cx in (col[0], col[1], col[2], col[3]):
        page.draw_line(fitz.Point(cx, top), fitz.Point(cx, y),
                       color=(0.6, 0.6, 0.6), width=0.6)

    y += 26
    page.insert_text((x0, y), "Figure 1: spend against plan",
                     fontname="hebi", fontsize=10.5)
    y += 10
    page.insert_image(fitz.Rect(x0, y, x0 + 330, y + 210), filename=str(FIGURE))
    y += 226

    page.insert_textbox(fitz.Rect(x0, y, 538, y + 70), " ".join(TAIL.split()),
                        fontname="helv", fontsize=10.5, lineheight=1.35)

    doc.save(str(OUT), garbage=4, deflate=True)
    doc.close()
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
