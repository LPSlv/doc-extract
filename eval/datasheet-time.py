# /// script
# dependencies = ["pdf-inspector==0.2.6", "pymupdf==1.28.0"]
# ///
"""Wall-clock, per stage, on 14 datasheets. Median of 3 runs per document."""
import sys, time, json, pathlib, statistics
sys.path.insert(0,"/home/lps/pdf-extract/skills/pdf-extract")
import fitz, pdf_inspector as pi
from harvest import harvest
from convert import _render_edge

def med(f, n=3):
    ts=[]
    for _ in range(n):
        t=time.perf_counter(); r=f(); ts.append(time.perf_counter()-t)
    return statistics.median(ts), r

rows=[]
for f in sorted(pathlib.Path("datasheets").glob("*.pdf")):
    p=str(f)
    t_cls,_   = med(lambda: pi.detect_pdf(p))
    t_txt,_   = med(lambda: pi.process_pdf(p))
    t_har,h   = med(lambda: harvest(p), n=1)
    if h["status"]!="ok": continue
    n=h["pages"]

    def render_all(dpi=140):
        d=fitz.open(p)
        for pg in d: pg.get_pixmap(dpi=dpi)
        d.close()
    def render_sel():
        d=fitz.open(p)
        for it in h["items"]:
            if it["kind"]=="raster": fitz.Pixmap(d, it["xref"])
            else:
                pg=d[it["page"]-1]; e=it.get("edge") or _render_edge(pg)
                s=e/max(pg.rect.width,pg.rect.height)
                pg.get_pixmap(matrix=fitz.Matrix(s,s))
        d.close()
    def render_sel_old():
        d=fitz.open(p)
        for it in h["items"]:
            if it["kind"]=="raster": fitz.Pixmap(d, it["xref"])
            else: d[it["page"]-1].get_pixmap(dpi=140)
        d.close()

    t_all,_ = med(render_all)
    t_sel,_ = med(render_sel)
    t_old,_ = med(render_sel_old)
    rows.append(dict(name=f.stem,pages=n,calls=h["vision_calls"],
                     cls=t_cls,txt=t_txt,har=t_har,
                     naive_render=t_all,sel_render=t_sel,sel_render_old=t_old))

print(f"{'datasheet':<16}{'pp':>4}{'classify':>9}{'extract':>9}{'route':>8}{'render sel':>11}{'render all':>11}")
print("-"*68)
for r in sorted(rows,key=lambda r:-r["pages"]):
    print(f"{r['name'][:15]:<16}{r['pages']:>4}{r['cls']*1000:>8.0f}m{r['txt']*1000:>8.0f}m"
          f"{r['har']*1000:>7.0f}m{r['sel_render']*1000:>10.0f}m{r['naive_render']*1000:>10.0f}m")
S=lambda k: sum(r[k] for r in rows)
print("-"*68)
print(f"{'TOTAL (s)':<16}{sum(r['pages'] for r in rows):>4}{S('cls'):>8.2f} {S('txt'):>8.2f} "
      f"{S('har'):>7.2f} {S('sel_render'):>9.2f}  {S('naive_render'):>9.2f}")
print()
print(f"pdf-extract deterministic total : {S('cls')+S('txt')+S('har')+S('sel_render'):.1f}s "
      f"for {sum(r['pages'] for r in rows)} pages "
      f"({(S('cls')+S('txt')+S('har')+S('sel_render'))/sum(r['pages'] for r in rows)*1000:.0f} ms/page)")
print(f"naive render-every-page only    : {S('naive_render'):.1f}s")
print(f"adaptive vs fixed-dpi rendering : {S('sel_render_old'):.1f}s -> {S('sel_render'):.1f}s "
      f"({1-S('sel_render')/S('sel_render_old'):.0%} faster)")
json.dump(rows, open("timebench.json","w"), indent=1)
