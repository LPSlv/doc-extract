# /// script
# dependencies = ["pdf-inspector==0.2.6", "pymupdf==1.28.0"]
# ///
"""Cost with adaptive resolution vs the previous fixed 140dpi render."""
import sys, time, json, pathlib, statistics
sys.path.insert(0,"/home/lps/doc-extract/skills/doc-extract")
import fitz
from harvest import harvest
from convert import _render_edge, MAX_EDGE_PX

def tok(w,h,cap=MAX_EDGE_PX):
    s=min(1.0,cap/max(w,h)); return int((w*s)*(h*s)/750)

rows=[]
for f in sorted(pathlib.Path("datasheets").glob("*.pdf")):
    doc=fitz.open(str(f)); n=len(doc)
    naive=sum(tok(*(lambda pm:(pm.width,pm.height))(pg.get_pixmap(dpi=140))) for pg in doc)
    doc.close()
    t0=time.perf_counter()
    h=harvest(str(f))
    if h["status"]!="ok": continue
    text=int(len(h["markdown"])/3.5)
    d=fitz.open(str(f)); old=new=0
    for it in h["items"]:
        if it["kind"]=="raster":
            w,hh=it["px"]; old+=tok(w,hh); new+=tok(w,hh)
        else:
            pg=d[it["page"]-1]
            pm=pg.get_pixmap(dpi=140); old+=tok(pm.width,pm.height)
            e=_render_edge(pg); s=e/max(pg.rect.width,pg.rect.height)
            pm2=pg.get_pixmap(matrix=fitz.Matrix(s,s)); new+=tok(pm2.width,pm2.height)
    d.close(); el=time.perf_counter()-t0
    rows.append(dict(name=f.stem,pages=n,calls=h["vision_calls"],naive=naive,
                     text=text,old=text+old,new=text+new,s=el))

rows.sort(key=lambda r:-r["pages"])
print(f"{'datasheet':<18}{'pp':>4}{'calls':>6}{'read-all':>10}{'was':>10}{'now':>10}{'vs read-all':>12}")
print("-"*70)
for r in rows:
    print(f"{r['name'][:17]:<18}{r['pages']:>4}{r['calls']:>6}{r['naive']:>10,}{r['old']:>10,}{r['new']:>10,}"
          f"{1-r['new']/r['naive']:>11.0%}")
N=sum(r['naive'] for r in rows); O=sum(r['old'] for r in rows); W=sum(r['new'] for r in rows)
print("-"*70)
print(f"{'TOTAL':<18}{sum(r['pages'] for r in rows):>4}{sum(r['calls'] for r in rows):>6}{N:>10,}{O:>10,}{W:>10,}{1-W/N:>11.0%}")
print()
print(f"first question : {N:,} -> {W:,}  ({1-W/N:.0%} less; was {1-O/N:.0%})")
print(f"images alone   : {O-sum(r['text'] for r in rows):,} -> {W-sum(r['text'] for r in rows):,} "
      f"({1-(W-sum(r['text'] for r in rows))/(O-sum(r['text'] for r in rows)):.0%} less)")
follow=int(sum(r['text']/r['pages']*2 for r in rows))
for q in (1,3,10):
    print(f"  {q:>2} q: read-all {N*q:>11,}   doc-extract {W+follow*(q-1):>9,}   {N*q/(W+follow*(q-1)):>5.1f}x")
json.dump(rows, open("costbench2.json","w"), indent=1)
