# /// script
# requires-python = ">=3.10"
# dependencies = ["pdf-inspector==0.2.6", "pymupdf==1.28.0"]
# ///
"""Candidate signals for the labelled `curves` / `whole_document` firings.

Run AFTER `nofigure_render.py` and the labelling. Adds, for each sampled
firing, document-level facts that the render script does not carry because a
labeller must not see them - they encode the hypotheses:

  sig_pages     how many pages of the document share this page's vector
                signature (curves, diagonals, axis_h, axis_v)
  sig_frac      that, over the document's page count. `harvest.py` already
                computes exactly this set as `template` and already calls it
                furniture - but only DROPS the page when it also has
                stroke_frac < 0.02, ink < 0.15 and rects < 8. The interest is
                in how many firings the existing rule identifies as furniture
                and then declines to act on.
  cluster_frac  area of the LARGEST spatially-connected stroke cluster over
                page area, as opposed to `stroke_frac`, which is the union
                bounding box of every stroke path on the page and therefore
                spans the page whenever furniture sits at both top and bottom.
  curves_repeat pages of the document with an identical `curves` count

    uv run eval/nofigure_features.py
"""
import collections
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills" / "doc-extract"))
import fitz                                                   # noqa: E402
from filters import UBIQUITY                                  # noqa: E402
from harvest import page_geometry                             # noqa: E402

OUT = ROOT / "eval" / "nofigure"
GAP = 24.0     # pt; stroke rects further apart than this are separate clusters


def clusters(pg):
    """Largest connected group of stroke path bounding boxes, over page area.

    Single-link on rect proximity. A vendor logo in the header and a rule in
    the footer are two clusters; the marks of one chart are one.
    """
    pw, ph = pg.rect.width, pg.rect.height
    parea = max(1.0, pw * ph)
    rects = []
    for path in pg.get_cdrawings():
        x0, y0, x1, y1 = path["rect"]
        if (x1 - x0) * (y1 - y0) > parea * 0.90:
            continue                                # background tint
        if any(it[0] in ("c", "l") for it in path["items"]):
            rects.append([x0, y0, x1, y1])
    if not rects:
        return 0.0, 0
    parent = list(range(len(rects)))

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    for i in range(len(rects)):
        for j in range(i + 1, len(rects)):
            a, b = rects[i], rects[j]
            if (a[0] - GAP <= b[2] and b[0] - GAP <= a[2]
                    and a[1] - GAP <= b[3] and b[1] - GAP <= a[3]):
                ra, rb = find(i), find(j)
                if ra != rb:
                    parent[ra] = rb
    groups = collections.defaultdict(list)
    for i in range(len(rects)):
        groups[find(i)].append(rects[i])
    best = 0.0
    for g in groups.values():
        x0 = min(r[0] for r in g); y0 = min(r[1] for r in g)
        x1 = max(r[2] for r in g); y1 = max(r[3] for r in g)
        best = max(best, (x1 - x0) * (y1 - y0) / parea)
    return round(best, 4), len(groups)


def main():
    rows = json.loads((OUT / "index.json").read_text())["rows"]
    by_doc = collections.defaultdict(list)
    corpus_of = {}
    for r in rows:
        by_doc[(r["corpus"], r["file"])].append(r)
        corpus_of[r["file"]] = r["corpus"]

    out = []
    for (corpus, name), rs in sorted(by_doc.items()):
        path = ROOT / "corpus" / corpus / name
        try:
            doc = fitz.open(str(path))
        except Exception as e:
            print(f"  SKIP {name}: {e}", file=sys.stderr)
            continue
        geoms = [page_geometry(p) for p in doc]
        npages = len(doc)
        sig = lambda g: (g["curves"], g["diagonals"], g["axis_h"], g["axis_v"])
        counts = collections.Counter(sig(g) for g in geoms)
        curve_counts = collections.Counter(g["curves"] for g in geoms)
        for r in rs:
            g = geoms[r["page"] - 1]
            cf, ng = clusters(doc[r["page"] - 1])
            n = counts[sig(g)]
            out.append({**r, "sig_pages": n, "sig_frac": round(n / npages, 3),
                        "is_template": npages > 2 and n / npages > UBIQUITY,
                        "curves_repeat": curve_counts[g["curves"]],
                        "cluster_frac": cf, "n_clusters": ng})
        doc.close()
    out.sort(key=lambda r: r["tag"])
    (OUT / "features.json").write_text(json.dumps(out, indent=1))
    print(f"features for {len(out)} firings -> {OUT / 'features.json'}")


if __name__ == "__main__":
    main()
