# /// script
# requires-python = ">=3.10"
# dependencies = ["pdf-inspector==0.2.6", "pymupdf==1.28.0"]
# ///
"""Collect, per question, exactly what each arm is allowed to see.

  arms/<id>/text.md        whole-document markdown  (text-only arm, and the
                           base for the doc-extract arm)
  arms/<id>/visual/*.png   what the PIPELINE routed for that page - the real
                           convert.py output, not the 200-dpi authoring render
  arms/<id>/optical.png    the page rendered whole (full-optical arm)

Keeping these on disk is what lets the arms be run by agents that never see
this conversation, the ground truth, or each other's material.
"""
import json, pathlib, shutil, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills" / "doc-extract"))
import fitz
from cache import cache_dir

OUT = ROOT / "eval" / "figqa"
OPT_DPI = 140          # the same dpi eval/bench.py charges the optical arm for


def main():
    qs = json.loads((OUT / "questions.json").read_text())["questions"]
    (OUT / "arms").mkdir(exist_ok=True)
    for q in qs:
        d = OUT / "arms" / q["id"]
        (d / "visual").mkdir(parents=True, exist_ok=True)
        art = pathlib.Path(cache_dir(q["doc"]))
        man = json.loads((art / "manifest.json").read_text())

        shutil.copy(art / "doc.md", d / "text.md")

        n = 0
        for item in man.get("items", []):
            if item.get("page") != q["page"]:
                continue
            src = art / "images" / f"{item['id']}.png"
            if src.exists():
                shutil.copy(src, d / "visual" / f"{item['id']}.png")
                n += 1

        with fitz.open(q["doc"]) as doc:
            doc[q["page"] - 1].get_pixmap(dpi=OPT_DPI).save(str(d / "optical.png"))

        print(f"{q['id']}  text {(d/'text.md').stat().st_size:7d}B  "
              f"routed {n} image(s)  page {q['page']}")


if __name__ == "__main__":
    main()
