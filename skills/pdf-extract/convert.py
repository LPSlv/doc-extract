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
from harvest import harvest, SCALE_GUARD
from artifact import splice, strip
from cache import cache_dir, publish, sha256_file, ENGINE, SCHEMA

# Vision cost scales with image AREA, so resolution is the dominant lever:
# halving the long edge quarters the token bill. Rendering every page at a fixed
# high dpi pays for detail most pages do not contain. These bounds were set by
# rendering dense datasheet pages at each size and checking legibility, then
# validated against olmOCR-bench ground truth (see eval/resolution.md).
MAX_EDGE_PX = 1568        # above this the model downsamples anyway - never exceed
MIN_EDGE_PX = 800         # below this small print starts to go
TARGET_EM_PX = 8.0        # pixels of em-height needed to read a glyph reliably
NO_TEXT_EDGE_PX = 1100    # scans carry no font info; handwriting needs more


def _render_edge(page):
    """Long edge in pixels for this page, from the size of its smallest text.

    A page whose smallest meaningful glyph is 12pt needs far fewer pixels than
    one set in 5pt. Pages with no text layer at all (scans) get a fixed budget
    because there is no font size to measure.
    """
    sizes = []
    try:
        # Spans only: without this flag "dict" also decodes and base64-wraps
        # every raster on the page. Same spans, ~2.7x faster (see harvest.py).
        flags = fitz.TEXTFLAGS_DICT & ~fitz.TEXT_PRESERVE_IMAGES
        for b in page.get_text("dict", flags=flags)["blocks"]:
            for ln in b.get("lines", []):
                for sp in ln.get("spans", []):
                    if sp.get("text", "").strip() and sp["size"] >= 3.0:
                        sizes.append(sp["size"])
    except Exception:
        pass
    if not sizes:
        return NO_TEXT_EDGE_PX
    sizes.sort()
    small = sizes[max(0, len(sizes) // 20)]        # 5th percentile, not the min:
    # the absolute smallest glyph on a datasheet is usually legal boilerplate.
    long_pt = max(page.rect.width, page.rect.height)
    edge = long_pt * (TARGET_EM_PX / small)
    return int(max(MIN_EDGE_PX, min(MAX_EDGE_PX, edge)))


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
    edge = edge_override or item.get("edge") or _render_edge(page)
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
