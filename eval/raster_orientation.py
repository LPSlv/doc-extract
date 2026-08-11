# /// script
# requires-python = ">=3.10"
# dependencies = ["pdf-inspector==0.2.6", "pymupdf==1.28.0"]
# ///
"""How many routed rasters does convert.py write out mis-oriented?

convert.py materialises a raster item with `fitz.Pixmap(doc, xref)`, which
decodes the image XObject's own samples and never applies the placement matrix
the page draws it with. When a PDF places an image flipped or rotated, the PNG
handed to the vision model is flipped or rotated too - silently. Nothing in the
test suite looks at image *pixels*, so this is invisible to CI.

This measures it: for every routed raster, decode the raw stream the way
convert.py does, render the same region off the page (which applies the
matrix, and is by definition what a reader sees), and compare. If the raw
matches better after a vertical flip, the shipped PNG is upside down.

    uv run eval/raster_orientation.py corpus/datasheets [corpus/... ]

Comparison is on a 64x64 grayscale thumbnail, so it is robust to the small
resolution difference between the two paths.
"""
import json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills" / "doc-extract"))
import fitz
from harvest import harvest_batch

N = 64


def thumb(pix):
    """64x64 grayscale byte string, via PyMuPDF only (no numpy/PIL)."""
    if pix.n - pix.alpha >= 4:
        pix = fitz.Pixmap(fitz.csRGB, pix)
    if pix.alpha:
        pix = fitz.Pixmap(pix, 0)
    g = fitz.Pixmap(fitz.csGRAY, pix)
    # shrink() halves; get close to N then sample the rest
    while min(g.width, g.height) >= N * 2:
        g.shrink(1)
    w, h, s = g.width, g.height, g.samples
    out = bytearray(N * N)
    for y in range(N):
        sy = min(h - 1, y * h // N)
        for x in range(N):
            sx = min(w - 1, x * w // N)
            out[y * N + x] = s[sy * w + sx]
    return bytes(out)


def mse(a, b):
    return sum((p - q) * (p - q) for p, q in zip(a, b)) / len(a)


def flipv(t):
    return b"".join(t[(N - 1 - y) * N:(N - 1 - y) * N + N] for y in range(N))


def fliph(t):
    return b"".join(bytes(reversed(t[y * N:y * N + N])) for y in range(N))


def main(dirs):
    paths = []
    for d in dirs:
        paths += sorted(pathlib.Path(d).glob("*.pdf"))
    results = harvest_batch([str(p) for p in paths])

    tot = ok = flipped = rot = skipped = 0
    bad = []
    for path, res in zip(paths, results):
        if res.get("status") != "ok":
            continue
        rasters = [i for i in (res.get("items") or []) if i.get("kind") == "raster"]
        if not rasters:
            continue
        try:
            doc = fitz.open(str(path))
        except Exception:
            continue
        for it in rasters:
            tot += 1
            try:
                page = doc[it["page"] - 1]
                info = next((i for i in page.get_image_info(xrefs=True)
                             if i.get("xref") == it["xref"]), None)
                if info is None:
                    skipped += 1
                    continue
                bbox = fitz.Rect(info["bbox"])
                if bbox.is_empty or bbox.width < 4 or bbox.height < 4:
                    skipped += 1
                    continue
                raw = thumb(fitz.Pixmap(doc, it["xref"]))
                s = max(info["width"] / bbox.width, info["height"] / bbox.height)
                s = min(s, 4.0)
                ref = thumb(page.get_pixmap(matrix=fitz.Matrix(s, s), clip=bbox))
            except Exception:
                skipped += 1
                continue

            d_id, d_v, d_h = mse(raw, ref), mse(flipv(raw), ref), mse(fliph(raw), ref)
            best = min(d_id, d_v, d_h)
            # require a clear margin, else call it upright and move on
            if best == d_id or best > 0.75 * d_id:
                ok += 1
            elif best == d_v:
                flipped += 1
                bad.append({"file": path.name, "id": it["id"], "kind": "vflip",
                            "mse_as_is": round(d_id, 1), "mse_flipped": round(d_v, 1)})
            else:
                rot += 1
                bad.append({"file": path.name, "id": it["id"], "kind": "hflip",
                            "mse_as_is": round(d_id, 1), "mse_flipped": round(d_h, 1)})
        doc.close()

    print(f"routed rasters checked : {tot}")
    print(f"  upright              : {ok}")
    print(f"  VERTICALLY FLIPPED   : {flipped}")
    print(f"  horizontally flipped : {rot}")
    print(f"  not comparable       : {skipped}")
    if tot - skipped:
        print(f"\nmis-oriented share: {(flipped+rot)/(tot-skipped)*100:.1f}% "
              f"of comparable routed rasters")
    for b in bad[:40]:
        print(f"  {b['kind']}  {b['file'][:44]:44s} {b['id']:14s} "
              f"as-is {b['mse_as_is']:8.1f}  fixed {b['mse_flipped']:8.1f}")
    (ROOT / "eval" / "raster-orientation.json").write_text(json.dumps(
        {"checked": tot, "upright": ok, "vflip": flipped, "hflip": rot,
         "skipped": skipped, "cases": bad}, indent=1))


if __name__ == "__main__":
    main([a for a in sys.argv[1:] if not a.startswith("-")] or ["corpus/datasheets"])
