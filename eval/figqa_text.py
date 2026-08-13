# /// script
# requires-python = ">=3.10"
# dependencies = ["pdf-inspector==0.2.6", "pymupdf==1.28.0"]
# ///
"""Dump what the text-only arm actually recovers, plus a per-page authoring view.

Two different things, deliberately kept apart:

  text/<id>.md   the WHOLE-DOCUMENT markdown from process_pdf. This is the
                 text-only arm as graded, because it is what the skill ships;
                 extract_pages_markdown loses text this API recovers -- 1 of
                 these 30 documents comes back entirely empty, 8 of 30 have at
                 least one empty page, 20 of 624 pages (3.2%) overall -- and
                 grading against it would handicap the baseline into a
                 walkover. (This docstring said "3 of these 30 documents"
                 until 2026-08-13; re-running both APIs gives 1. See the
                 correction note in eval/figqa.md.)

  view/<id>.txt  the candidate page's raw text via PyMuPDF, for authoring only.
                 Never graded. It exists so a question can be checked to be
                 genuinely figure-only before it enters the set.

Without this step you end up "proving" the visual layer wins on facts the text
extractor already had.
"""
import json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills" / "doc-extract"))
import fitz, pdf_inspector as pi

OUT = ROOT / "eval" / "figqa"


def main():
    meta = json.loads((OUT / "candidates.json").read_text())
    (OUT / "text").mkdir(exist_ok=True)
    (OUT / "view").mkdir(exist_ok=True)
    cache = {}
    for c in meta["selected"]:
        doc = c["doc"]
        if doc not in cache:
            cache[doc] = pi.process_pdf(doc).markdown or ""
        (OUT / "text" / f"{c['id']}.md").write_text(cache[doc])
        with fitz.open(doc) as d:
            page_txt = d[c["page"] - 1].get_text()
        (OUT / "view" / f"{c['id']}.txt").write_text(page_txt)
        print(f"{c['id']}  {c['name'][:36]:36s} p{c['page']:<4d} "
              f"doc {len(cache[doc]):7d}  page {len(page_txt):6d}")


if __name__ == "__main__":
    main()
