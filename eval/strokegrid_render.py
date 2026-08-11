# /// script
# requires-python = ">=3.10"
# dependencies = ["pdf-inspector==0.2.6", "pymupdf==1.28.0"]
# ///
"""Render every stroke_grid firing for labelling, with the facts a label needs.

`stroke_grid` exists to catch two things the text extractor misses: a ruled
table it could not parse, and a marker-based plot whose strokes are the
markers. In the v1 figure-QA sample it fired three times and was wrong three
times - boxed display equations, publisher front matter, a QR box - but three
observations cannot justify retuning a threshold, and tuning on the
measurement set would invalidate it.

So this builds the artifact instead: one PNG per firing plus the two facts a
labeller should not have to judge by eye.

  has_md_table   the page's own markdown already contains a pipe table, so the
                 extractor DID parse it and the render is redundant
  page_chars     how much text the page carries

    uv run eval/strokegrid_render.py
"""
import json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills" / "doc-extract"))
import fitz, pdf_inspector as pi

OUT = ROOT / "eval" / "strokegrid"
DPI = 130


def main():
    firings = json.loads((OUT / "firings.json").read_text())["firings"]
    (OUT / "pages").mkdir(exist_ok=True)
    cache = {}
    rows = []
    for i, f in enumerate(firings):
        doc = f["doc"]
        if doc not in cache:
            try:
                cache[doc] = pi.extract_pages_markdown(doc).pages
            except Exception:
                cache[doc] = []
        # pdf_inspector's PageMarkdown.page is 0-BASED, while harvest's item
        # pages are 1-based. Matching them directly reads the following page
        # and quietly reports its table as this one's.
        md = next((p.markdown for p in cache[doc]
                   if p.page == f["page"] - 1), "") or ""

        tag = f"s{i+1:03d}"
        try:
            with fitz.open(doc) as d:
                pg = d[f["page"] - 1]
                pg.get_pixmap(dpi=DPI).save(str(OUT / "pages" / f"{tag}.png"))
                chars = len(pg.get_text().strip())
        except Exception:
            continue

        rows.append({"tag": tag, "name": f["name"], "page": f["page"],
                     "id": f["id"], "corpus": f["doc"].split("/")[1],
                     "has_md_table": "|---" in md or "| ---" in md,
                     "page_chars": chars})
        if (i + 1) % 40 == 0:
            print(f"  {i+1}/{len(firings)}", file=sys.stderr)

    (OUT / "index.json").write_text(json.dumps({"dpi": DPI, "rows": rows}, indent=1))
    n_tab = sum(r["has_md_table"] for r in rows)
    print(f"rendered {len(rows)} firings")
    print(f"  pages whose markdown ALREADY has a table: {n_tab} "
          f"({n_tab/len(rows)*100:.0f}%)")


if __name__ == "__main__":
    main()
