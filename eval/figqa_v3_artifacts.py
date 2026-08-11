# /// script
# requires-python = ">=3.10"
# dependencies = ["pdf-inspector==0.2.6", "pymupdf==1.28.0"]
# ///
"""Assemble per-arm materials for v3.

v3 differs from v2 in two ways that matter:

  - every selected page's routed item is a CROPPED RASTER, not a whole-page
    render. In v2, 9 of 11 admitted questions sat on pages the router rendered
    whole, so the describer saw nearly the same pixels as the full-optical arm
    and the comparison was close to trivial. Here it never is.
  - the questions were authored by agents that saw only the page renders, with
    no access to any description. In v2 the author had already read the
    describers' status reports, and one question had to be withdrawn for it.

    uv run eval/figqa_v3_artifacts.py
"""
import json, pathlib, shutil, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills" / "doc-extract"))
import fitz
from cache import cache_dir

V3 = ROOT / "eval" / "figqa" / "v3"
OPT_DPI = 140


def main():
    sel = json.loads((V3 / "selection.json").read_text())["selected"]
    for s in sel:
        d = V3 / "arms" / s["qid"]
        (d / "visual").mkdir(parents=True, exist_ok=True)
        art = pathlib.Path(cache_dir(s["doc"]))
        man = json.loads((art / "manifest.json").read_text())

        shutil.copy(art / "doc.md", d / "text.md")

        n = 0
        for item in man.get("items", []):
            # only the routed item this page was selected for; a page can carry
            # several, and the question is about the figure, not the furniture
            if item.get("id") != s["id"]:
                continue
            src = art / "images" / f"{item['id']}.png"
            if src.exists():
                shutil.copy(src, d / "visual" / f"{item['id']}.png")
                n += 1

        with fitz.open(s["doc"]) as doc:
            doc[s["page"] - 1].get_pixmap(dpi=OPT_DPI).save(str(d / "optical.png"))

        print(f"{s['qid']}  {s['name'][:34]:34s} p{s['page']:<4d} "
              f"raster {n}  {s['px'][0]}x{s['px'][1]}")


if __name__ == "__main__":
    main()
