# /// script
# requires-python = ">=3.10"
# dependencies = ["pdf-inspector==0.2.6", "pymupdf==1.28.0"]
# ///
"""Cost to UNDERSTAND a datasheet: read every page as an image, vs pdf-extract.

Token model follows Anthropic's documented rule: an image costs about
(width x height)/750 tokens after being fitted inside 1568px on the long edge.
Text is charged at chars/3.5, which is conservative for dense technical English.
Both numbers are computed from the actual rendered pixels, not guessed.
"""
import sys, time, json, pathlib, io
sys.path.insert(0, "/home/lps/pdf-extract/skills/pdf-extract")
import fitz
import pdf_inspector as pi
from harvest import harvest

MAXPX, DPI = 1568, 140

def img_tokens(w, h):
    scale = min(1.0, MAXPX / max(w, h))
    return int((w * scale) * (h * scale) / 750)

rows = []
for f in sorted(pathlib.Path("datasheets").glob("*.pdf")):
    doc = fitz.open(str(f)); n = len(doc)

    # --- naive: render EVERY page and look at it -------------------------
    t0 = time.perf_counter()
    naive_tok = 0
    for pg in doc:
        pm = pg.get_pixmap(dpi=DPI)
        naive_tok += img_tokens(pm.width, pm.height)
    naive_s = time.perf_counter() - t0
    doc.close()

    # --- pdf-extract: text + only the flagged images ---------------------
    t0 = time.perf_counter()
    h = harvest(str(f))
    if h["status"] != "ok":
        print(f"SKIP {f.name}: {h['error']}"); continue
    text_tok = int(len(h["markdown"]) / 3.5)
    d2 = fitz.open(str(f)); vis_tok = 0
    for it in h["items"]:
        if it["kind"] == "raster":
            vis_tok += img_tokens(*it["px"])
        else:
            pm = d2[it["page"] - 1].get_pixmap(dpi=DPI)
            vis_tok += img_tokens(pm.width, pm.height)
    d2.close()
    skill_s = time.perf_counter() - t0
    skill_tok = text_tok + vis_tok

    rows.append(dict(name=f.stem, pages=n, calls=h["vision_calls"],
                     naive_tok=naive_tok, text_tok=text_tok, vis_tok=vis_tok,
                     skill_tok=skill_tok, naive_s=naive_s, skill_s=skill_s,
                     ratio=naive_tok / max(1, skill_tok)))

rows.sort(key=lambda r: -r["pages"])
print(f"{'datasheet':<20}{'pp':>4}{'calls':>6}{'naive tok':>11}{'skill tok':>11}{'saving':>9}{'naive s':>9}{'skill s':>9}")
print("-" * 79)
for r in rows:
    print(f"{r['name'][:19]:<20}{r['pages']:>4}{r['calls']:>6}{r['naive_tok']:>11,}{r['skill_tok']:>11,}"
          f"{1 - r['skill_tok']/r['naive_tok']:>8.0%}{r['naive_s']:>9.1f}{r['skill_s']:>9.1f}")
tn = sum(r["naive_tok"] for r in rows); ts = sum(r["skill_tok"] for r in rows)
pp = sum(r["pages"] for r in rows); cc = sum(r["calls"] for r in rows)
print("-" * 79)
print(f"{'TOTAL':<20}{pp:>4}{cc:>6}{tn:>11,}{ts:>11,}{1-ts/tn:>8.0%}"
      f"{sum(r['naive_s'] for r in rows):>9.1f}{sum(r['skill_s'] for r in rows):>9.1f}")
print(f"\nmedian per-doc saving: {sorted(1-r['skill_tok']/r['naive_tok'] for r in rows)[len(rows)//2]:.0%}")
print(f"text tokens are {sum(r['text_tok'] for r in rows)/ts:.0%} of the skill's total; images {sum(r['vis_tok'] for r in rows)/ts:.0%}")
json.dump(rows, open("costbench.json","w"), indent=1)
