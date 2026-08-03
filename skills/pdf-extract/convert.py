# /// script
# requires-python = ">=3.10"
# dependencies = ["pdf-inspector==0.2.6", "pymupdf==1.28.0"]
# ///
"""Turn PDFs into a cached, citable artifact. The orchestrator.

    uv run convert.py <pdf> [...] [--out DIR] [--force] [--edge PX]

Runs everything deterministic and writes a complete artifact, then prints one
JSON object per document telling the agent exactly which image files still need
a description. That is the whole handoff: the agent reads `pending`, looks at
each `path`, and calls `describe.py` to write the answer back.

Artifact layout:

    <cache>/<sha256>-<tag>/
      source.json     provenance + status
      doc.md          authoritative text (pdf-inspector), plus delimited additions
      pages/p001.md   per-page text, for citation and cheap answering
      images/*.png    extracted rasters and rendered pages
      manifest.json   every kept item, and everything dropped with the reason
"""
import sys, json, argparse, shutil
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fitz
# Vision cost scales with image AREA, so resolution is the dominant lever:
# halving the long edge quarters the token bill. render_edge and the pixel
# bounds live in harvest.py, which already computes a budget for every page it
# routes to a render; this module holds no second copy of that arithmetic.
from harvest import harvest, render_edge, MAX_EDGE_PX, SCALE_GUARD
from artifact import splice, strip
from cache import cache_dir, publish, sha256_file, ENGINE, SCHEMA


def _write_image(doc, item, images_dir, edge_override=None):
    """Materialise one manifest item to a PNG. Returns the filename."""
    name = f"{item['id']}.png"
    dest = images_dir / name
    if item["kind"] == "raster":
        try:
            pix = fitz.Pixmap(doc, item["xref"])
            if pix.n - pix.alpha >= 4:
                pix = fitz.Pixmap(fitz.csRGB, pix)
            # Downscale oversized rasters: a 3000px screenshot costs 4x a
            # 1500px one and carries no more readable detail. shrink(n) halves
            # each dimension n times, which is all the precision needed here.
            while max(pix.width, pix.height) > MAX_EDGE_PX * 2:
                pix.shrink(1)
            pix.save(dest)
            return name
        except Exception:
            pass                       # fall through to a page render
    page = doc[item["page"] - 1]
    edge = edge_override or item.get("edge") or render_edge(page)
    scale = edge / max(page.rect.width, page.rect.height)
    page.get_pixmap(matrix=fitz.Matrix(scale, scale)).save(dest)
    return name


def convert(path, out=None, edge=None, force=False, root=None):
    src = Path(path)
    dest = cache_dir(src, root=root)

    if dest.exists() and not force:
        man = json.loads((dest / "manifest.json").read_text())
        return _report(src, dest, man, cached=True, out=out)

    h = harvest(str(src))
    if h["status"] != "ok":
        return {"status": "error", "error": h["error"], "path": str(src),
                "detail": h.get("detail")}

    def build(staging):
        (staging / "images").mkdir()
        (staging / "pages").mkdir()
        doc = fitz.open(str(src))
        try:
            for item in h["items"]:
                item["path"] = f"images/{_write_image(doc, item, staging / 'images', edge)}"
        finally:
            doc.close()

        (staging / "doc.md").write_text(h["markdown"])
        for i, pm in enumerate(h.get("page_markdown") or [], start=1):
            (staging / "pages" / f"p{i:03d}.md").write_text(pm or "")
        (staging / "manifest.json").write_text(json.dumps(
            {"items": h["items"], "dropped": h["dropped"]}, indent=2))
        (staging / "source.json").write_text(json.dumps({
            "path": str(src.resolve()), "sha256": sha256_file(src),
            "bytes": src.stat().st_size, "pdf_type": h["pdf_type"],
            "pages": h["pages"], "engine": ENGINE, "schema": SCHEMA,
            "status": "ok",
        }, indent=2))

    publish(dest, build)
    man = json.loads((dest / "manifest.json").read_text())
    return _report(src, dest, man, cached=False, out=out)


def _report(src, dest, man, cached, out):
    pending = [{"id": i["id"], "page": i["page"], "kind": i["kind"],
                "reason": i["reason"], "path": str(dest / i["path"])}
               for i in man["items"] if i.get("description") is None]
    if out:
        outp = Path(out); outp.mkdir(parents=True, exist_ok=True)
        shutil.copy2(dest / "doc.md", outp / f"{src.stem}.md")
        if (dest / "images").exists():
            shutil.copytree(dest / "images", outp / f"{src.stem}.images",
                            dirs_exist_ok=True)
    return {
        "status": "ok", "path": str(src), "artifact": str(dest), "cached": cached,
        "doc_md": str(dest / "doc.md"), "pages_dir": str(dest / "pages"),
        "manifest": str(dest / "manifest.json"),
        "pending": pending, "dropped": len(man["dropped"]),
        "over_scale_guard": len(pending) > SCALE_GUARD, "scale_guard": SCALE_GUARD,
    }


def main(argv=None):
    ap = argparse.ArgumentParser(description="Convert PDFs to a citable artifact")
    ap.add_argument("pdfs", nargs="+")
    ap.add_argument("--out", help="also copy doc.md and images here")
    ap.add_argument("--edge", type=int, default=None,
                    help="force a long-edge pixel budget instead of the adaptive one")
    ap.add_argument("--force", action="store_true", help="ignore any cached artifact")
    ap.add_argument("--cache-root", default=None)
    a = ap.parse_args(argv)

    bad = 0
    for p in a.pdfs:
        try:
            r = convert(p, out=a.out, edge=a.edge, force=a.force, root=a.cache_root)
        except Exception as e:
            r = {"status": "error", "error": "convert_failed",
                 "detail": f"{type(e).__name__}: {e}", "path": p}
        if r["status"] != "ok":
            bad += 1
        print(json.dumps(r))
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
