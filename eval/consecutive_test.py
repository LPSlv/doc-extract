# /// script
# requires-python = ">=3.10"
# dependencies = ["pdf-inspector==0.2.6", "pymupdf==1.28.0"]
# ///
"""Does *consecutiveness* separate a continued table from a box template?

`boxed_text` (eval/strokegrid.md) drops a `stroke_grid` firing whose page has
exactly two distinct vertical stroke positions repeating on >=BOX_REPEATS
pages. Its one known failure is a booktabs table continued across pages: two
interior rules, same place every page. `docs/NEXT.md` records the untested
idea -- a continued table's pages are ADJACENT, a prompt-box or title-block
template's usually are not -- and records, correctly, that three known losses
are too few to fit a rule on.

So this does not fit a rule. It measures how the signal DISTRIBUTES over every
labelled firing (170 in-sample + 18 holdout drops = 188), and only then prices
the candidate against the shipped rule and against the rejected containment
refinement.

Definitions, all page-level and 1-based:

    fp          the page's fingerprint: rounded distinct vertical stroke
                x-positions, exactly as harvest.page_geometry computes vx_pos
    fp_pages    every page of the document carrying the identical fp
    adjacent    fp_pages contains page-1 or page+1  (this page sits in a run)
    max_run     longest consecutive stretch inside fp_pages (document-level)

    uv run eval/consecutive_test.py
"""
import collections, json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
SG = ROOT / "eval" / "strokegrid"
OUT = ROOT / "eval" / "consecutive"
sys.path.insert(0, str(ROOT / "skills" / "doc-extract"))
import fitz
from harvest import page_geometry, BOX_REPEATS

TOL, VMIN = 2.0, 3.0


def fp_independent(page):
    """vx fingerprint, recomputed without harvest.py.

    Same definition, different code: this file's whole argument is that the
    measurement code is where the errors are, so both are computed and any
    disagreement is fatal (see check below).
    """
    vx = []
    for d in page.get_cdrawings():
        for it in d.get("items", ()):
            if it[0] != "l":
                continue
            (x0, y0), (x1, y1) = _xy(it[1]), _xy(it[2])
            if abs(x0 - x1) <= 1.0 and abs(y0 - y1) > VMIN:
                vx.append((x0 + x1) / 2)
    out = []
    for x in sorted(vx):
        if not out or x - out[-1] > TOL:
            out.append(x)
    return tuple(round(x) for x in out)


def _xy(p):
    return (p[0], p[1]) if isinstance(p, (tuple, list)) else (p.x, p.y)


def doc_fps(path):
    with fitz.open(str(path)) as d:
        a = [tuple(page_geometry(p)["vx_pos"]) for p in d]
        b = [fp_independent(p) for p in d]
    if a != b:
        raise SystemExit(f"fingerprint mismatch in {path}: {a} != {b}")
    return a


def runs(pages):
    """Longest consecutive stretch in a sorted page list."""
    best = cur = 1
    for i in range(1, len(pages)):
        cur = cur + 1 if pages[i] == pages[i - 1] + 1 else 1
        best = max(best, cur)
    return best if pages else 0


def facts(fps, page):
    me = fps[page - 1]
    fp_pages = [i + 1 for i, f in enumerate(fps) if f == me]
    run_here = 1
    for p in (page - 1, page + 1):
        if p in fp_pages:
            run_here = 2
    # length of the consecutive run this page belongs to
    lo = hi = page
    s = set(fp_pages)
    while lo - 1 in s:
        lo -= 1
    while hi + 1 in s:
        hi += 1
    return {"fp": list(me), "n_vx": len(me), "n_rep": len(fp_pages),
            "fp_pages": fp_pages, "adjacent": run_here == 2,
            "run_here": hi - lo + 1, "max_run": runs(fp_pages),
            "drops": len(me) == 2 and len(fp_pages) >= BOX_REPEATS}


def cases():
    out = []
    for line in (SG / "labels.tsv").read_text().strip().splitlines()[1:]:
        c = line.split("\t")
        out.append(("in", c[0], c[4].strip(), ROOT / "corpus" / c[1] / c[2],
                    int(c[3])))
    hl = {}
    for line in (SG / "holdout" / "labels.tsv").read_text().strip().splitlines()[1:]:
        c = line.split("\t")
        hl[c[0]] = (c[4].strip(), c[2], int(c[3]))
    for tag in sorted(hl):                     # h001..h017 + h018, 18 rows
        label, name, page = hl[tag]
        out.append(("hold", tag, label, ROOT / "corpus" / "arxiv_holdout" / name,
                    page))
    return out


def pct(a, b):
    return f"{a}/{b} = {100 * a / b:.0f}%" if b else f"{a}/0 = --"


def main():
    cache, rows = {}, []
    for src, tag, label, path, page in cases():
        if not path.exists():
            sys.exit(f"missing {path}")
        if path not in cache:
            cache[path] = doc_fps(path)
        f = facts(cache[path], page)
        f.update({"src": src, "tag": tag, "label": label, "file": path.name,
                  "page": page})
        rows.append(f)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "facts.json").write_text(json.dumps(rows, indent=1) + "\n")
    print(f"{len(rows)} labelled firings "
          f"({sum(1 for r in rows if r['src'] == 'in')} in-sample, "
          f"{sum(1 for r in rows if r['src'] == 'hold')} holdout)\n")

    # ---- 1. distribution over every labelled firing ------------------------
    print("all 188 firings, by label x adjacency (same fingerprint on page +-1)")
    print(f"{'label':<8}{'n':>5}{'adjacent':>10}{'share':>8}")
    for label in ("table", "plot", "figure", "none"):
        g = [r for r in rows if r["label"] == label]
        a = sum(1 for r in g if r["adjacent"])
        print(f"{label:<8}{len(g):>5}{a:>10}{(100*a/len(g) if g else 0):>7.0f}%")

    # the population the rule can act on at all: fp repeats >= BOX_REPEATS
    print("\nrestricted to what `boxed_text` actually drops (vx==2, repeated)")
    print(f"{'label':<8}{'drops':>7}{'adjacent':>10}{'share':>8}{'max_run>=2':>12}")
    for label in ("table", "plot", "figure", "none"):
        g = [r for r in rows if r["label"] == label and r["drops"]]
        a = sum(1 for r in g if r["adjacent"])
        m = sum(1 for r in g if r["max_run"] >= 2)
        print(f"{label:<8}{len(g):>7}{a:>10}{(100*a/len(g) if g else 0):>7.0f}%{m:>12}")

    # ---- 2. price the candidate -------------------------------------------
    drops = [r for r in rows if r["drops"]]
    waste = [r for r in drops if r["label"] == "none"]
    real = [r for r in drops if r["label"] != "none"]
    print(f"\nshipped rule: {len(waste)} wasted cut, {len(real)} real lost, "
          f"precision {pct(len(waste), len(drops))}")
    for name, keep in (("A: page adjacent to a same-fp page",
                        lambda r: not r["adjacent"]),
                       ("B: any two same-fp pages consecutive",
                        lambda r: r["max_run"] < 2),
                       ("C: run containing this page >= 3",
                        lambda r: r["run_here"] < 3)):
        w = sum(1 for r in waste if keep(r))
        l = sum(1 for r in real if keep(r))
        p = 100 * w / (w + l) if w + l else float("nan")
        print(f"  + {name:<40} cut {w:>3} (gives back {len(waste)-w:>2}), "
              f"lost {l} of {len(real)}, precision {p:.0f}%")

    print("\nthe three real items, in detail")
    for r in real:
        print(f"  {r['file']:<28} p{r['page']:<4} {r['label']:<7} "
              f"fp={tuple(r['fp'])} on {r['fp_pages']} "
              f"adjacent={r['adjacent']} run_here={r['run_here']} "
              f"max_run={r['max_run']}")

    print("\nwasted drops that consecutiveness would give back, by document")
    give = collections.Counter(r["file"] for r in waste if r["adjacent"])
    for f, n in give.most_common():
        print(f"  {n:>3}  {f}")


if __name__ == "__main__":
    main()
