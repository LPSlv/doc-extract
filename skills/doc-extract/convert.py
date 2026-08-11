# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "pdf-inspector==0.2.6",
#   "pymupdf==1.28.0",
#   "firecrawl-anydoc==0.1.6",
# ]
# ///
"""Turn documents into a cached, citable artifact. The orchestrator.

    uv run convert.py <file> [...] [--out DIR] [--force] [--edge PX]

PDFs, Word, Excel, PowerPoint and standalone images. Format is decided by
content rather than by extension, because a .doc that is really a .docx is
common enough to matter and mis-dispatching it produces confident nonsense.

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
import image as image_adapter


def route(src):
    """(harvester, engine) for this file, decided by content.

    Engines are per format on purpose. The cache key hashes the engine string,
    so a single combined one would invalidate every cached PDF artifact the
    moment Office support shipped -- re-billing vision calls already paid for,
    on a path whose behaviour is guaranteed unchanged.
    """
    with open(src, "rb") as fh:
        head = fh.read(64)
    if head[:5] == b"%PDF-":
        return harvest, ENGINE
    if image_adapter.media_type(head):
        return image_adapter.harvest_image, image_adapter.ENGINE
    # Office packages are zips, and a zip's directory lives at the END of the
    # file, so detection needs the whole thing rather than a prefix.
    import office
    with open(src, "rb") as fh:
        if office.detect(fh.read()):
            return office.harvest_office, office.ENGINE
    return harvest, ENGINE          # let the PDF path report why it is not one


def _raster_pixmap(doc, item):
    """The routed raster, oriented the way the page draws it.

    fitz.Pixmap(doc, xref) decodes the image XObject's own samples and applies
    nothing else. When a PDF draws that image flipped - and TI datasheets do;
    ti_drv8825.pdf p11 ships its motor-control block diagram upside down - the
    PNG handed to the vision model is upside down too, silently, and every
    label in it is unreadable. Nothing in the suite looks at image pixels, so
    CI never saw it.

    Rendering the image's own rectangle off the page applies the placement
    matrix by construction, whatever the mechanism (flipped CTM, /Decode
    array, bottom-up sample order). Scale is chosen to keep the image's native
    detail rather than the page's.
    """
    page = doc[item["page"] - 1]
    places = [i for i in page.get_image_info(xrefs=True)
              if i.get("xref") == item["xref"]]
    if places:
        # An xref can be drawn more than once on a page; the largest placement
        # is the one worth reading.
        info = max(places, key=lambda i: fitz.Rect(i["bbox"]).get_area())

        # get_image_info() reports bbox in UNROTATED page space, while clip=
        # and page.rect live in rotated space. Skipping this on a /Rotate 270
        # page turns a full-width figure into a wrong square crop, and on some
        # pages into pure white - worse than the flip this function exists to
        # fix. arxiv 2607.29183v1 pp.4,6 are the corpus cases.
        bbox = (fitz.Rect(info["bbox"]) * page.rotation_matrix) & page.rect
        if not bbox.is_empty and bbox.width >= 4 and bbox.height >= 4:
            # Preserve the image's own resolution: scale so the rendered region
            # is about its native pixel count. Capping this at a fixed multiple
            # of the *placement* silently degrades a high-resolution image that
            # happens to be placed small, which is common for schematics and
            # scope captures.
            s = max(info["width"] / bbox.width, info["height"] / bbox.height)
            s = min(s, (MAX_EDGE_PX * 2) / max(bbox.width, bbox.height))
            pix = page.get_pixmap(matrix=fitz.Matrix(s, s), clip=bbox)
            # Rendering the region captures whatever the page draws there, so
            # an image fully covered by an opaque overlay comes out blank. That
            # is a silent total loss; the stored samples are worth more.
            if not pix.is_unicolor:
                return pix
    return fitz.Pixmap(doc, item["xref"])   # unplaced, degenerate, or occluded


def _write_image(doc, item, images_dir, edge_override=None):
    """Materialise one manifest item to a PNG. Returns the filename."""
    name = f"{item['id']}.png"
    dest = images_dir / name
    if item["kind"] == "raster":
        try:
            pix = _raster_pixmap(doc, item)
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
    harvester, engine = route(src)
    dest = cache_dir(src, root=root, engine=engine)

    if dest.exists() and not force:
        man = json.loads((dest / "manifest.json").read_text())
        return _report(src, dest, man, cached=True, out=out)

    h = harvester(str(src))
    if h["status"] != "ok":
        return {"status": "error", "error": h["error"], "path": str(src),
                "detail": h.get("detail")}

    is_pdf = harvester is harvest

    def build(staging):
        (staging / "images").mkdir()
        (staging / "pages").mkdir()
        if is_pdf:
            doc = fitz.open(str(src))
            try:
                for item in h["items"]:
                    item["path"] = f"images/{_write_image(doc, item, staging / 'images', edge)}"
            finally:
                doc.close()
        else:
            # Office and image adapters carry the decoded bytes on the item,
            # because there is no document handle to re-read them from. The
            # key is stripped before the manifest is written: it is transport,
            # not a record.
            for item in h["items"]:
                blob = item.pop("_bytes", None)
                if blob is None:
                    continue
                name = f"{item['id']}.png" if item.get("media_type") == "image/png" \
                    else f"{item['id']}{_suffix(item.get('media_type'))}"
                (staging / "images" / name).write_bytes(blob)
                item["path"] = f"images/{name}"

        (staging / "doc.md").write_text(h["markdown"])
        labels = h.get("unit_labels")
        for i, pm in enumerate(h.get("page_markdown") or [], start=1):
            # PDF units are pages and keep their p001.md names, which the
            # example artifact and the gate corpus depend on. Office units are
            # named things, and a sheet called "Q1 P&L / draft" is not a
            # filename -- so those are positional, with the label in the
            # manifest where a citation can find it.
            stem = f"p{i:03d}" if is_pdf else f"u{i:03d}"
            (staging / "pages" / f"{stem}.md").write_text(pm or "")
        (staging / "manifest.json").write_text(json.dumps(
            {"items": h["items"], "dropped": h["dropped"],
             **({"units": labels} if labels else {})}, indent=2))
        (staging / "source.json").write_text(json.dumps({
            "path": str(src.resolve()), "sha256": sha256_file(src),
            "bytes": src.stat().st_size, "pdf_type": h["pdf_type"],
            "pages": h["pages"], "engine": engine, "schema": SCHEMA,
            "status": "ok",
        }, indent=2))

    publish(dest, build)
    man = json.loads((dest / "manifest.json").read_text())
    return _report(src, dest, man, cached=False, out=out)


_SUFFIX = {"image/png": ".png", "image/jpeg": ".jpg", "image/gif": ".gif",
           "image/webp": ".webp", "image/bmp": ".bmp", "image/tiff": ".tif"}


def _suffix(media):
    """Keep the real extension: an agent reading the file needs to decode it."""
    return _SUFFIX.get(media, ".bin")


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
