"""Office documents to the harvest() contract, via anydoc plus ooxml.

Division of labour, every line of it measured rather than assumed (see
tests/test_anydoc_invariants.py):

              text            images                  charts
    docx      anydoc          anydoc (image inlines)  anydoc
    pptx      anydoc/slice    anydoc/slice            anydoc
    xlsx      anydoc          ooxml.py                ooxml.py

"anydoc/slice" is the per-slide repack: anydoc has no per-slide anything, so
one slide at a time is handed to it. That single mechanism yields the unit
boundaries citations need AND the per-slide asset lists the furniture filter
needs, which is why no relationship walking happens for pptx.

xlsx is the outlier because anydoc's spreadsheet path is pure cell extraction:
it returns zero assets and no chart for a workbook that demonstrably contains
both. Nothing here re-extracts what anydoc already handles -- doing that for
docx and pptx charts would have emitted every chart twice.

Routing is thin compared to the PDF path, and that is the honest outcome. A
PDF page hides its figures inside drawing commands, so harvest.py has to infer
them from vector geometry; OOXML declares its images in the package. What
carries over is the furniture filters, and what does not is render_reason,
raster_grid and cost_guard -- none of which has an Office analogue, since
without LibreOffice there is no slide or sheet to render.
"""
import hashlib
import io
import re
import zipfile

import anydoc

import ooxml
from filters import furniture_reason
from image import VIEWABLE, dimensions

ENGINE = "anydoc==0.1.6"
SUPPORTED = {"docx", "xlsx", "pptx"}

# anydoc detects formats this module cannot serve: `doc`, `ppt`, `xls`, `odt`
# and more are legacy OLE or ODF containers that zipfile cannot read, so
# ooxml.py would silently contribute nothing and citations would degrade
# without saying so. Dispatch whitelists rather than blacklists.
_FENCE = re.compile(r"^\s*(```|~~~)")


def detect(data):
    """Format name if this module can serve it, else None."""
    try:
        fmt = anydoc.format_from_bytes(data)
    except Exception:
        return None
    return fmt if fmt in SUPPORTED else None


def _split_markdown(md, level):
    """[(heading-text, chunk)] split at ATX headings of exactly `level`.

    Fence-aware: a `# ` inside a code block is content, not a heading, and a
    spreadsheet of shell commands would otherwise shatter into nonsense units.
    Text before the first heading is attached to a leading None-labelled
    chunk, so nothing is dropped.
    """
    marker = "#" * level + " "
    out, label, buf, fence = [], None, [], None
    for line in md.splitlines():
        f = _FENCE.match(line)
        if f:
            fence = None if fence else f.group(1)
        if fence is None and line.startswith(marker):
            if buf or label is not None:
                out.append((label, "\n".join(buf).strip()))
            label, buf = line[len(marker):].strip(), []
            continue
        buf.append(line)
    if buf or label is not None:
        out.append((label, "\n".join(buf).strip()))
    return out


def _image_inlines(blocks):
    """Every image inline, depth first, in document order."""
    for b in blocks:
        for i in (b.content or []):
            if i.kind == "image":
                yield i
        for sub in (b.blocks or []):
            yield from _image_inlines([sub])
        if b.list:
            for item in b.list.items:
                yield from _image_inlines(item.blocks)
        if b.table:
            for row in b.table.grid:
                for slot in row:
                    if slot.cell:
                        yield from _image_inlines(slot.cell.blocks)


# --------------------------------------------------------------- per format
def _pptx(data):
    """Units and placements from one repack per slide."""
    rids = ooxml.slide_rids(data)
    if not rids:
        raise anydoc.MalformedError("presentation has no slide list")
    units, placements, failed = [], {}, []
    for i, rid in enumerate(rids, start=1):
        label = f"s{i:02d}"
        try:
            one = ooxml.repack_single(data, rid)
            md = anydoc.to_markdown_bytes(one, "pptx")
            doc = anydoc.to_document(one, "pptx")
        except Exception as e:
            # A corrupt slide must not kill the deck. Whole-deck conversion
            # skips it; a one-slide repack of it instead reports "no slide
            # could be read", so the per-unit tier has to be restored here.
            failed.append({"unit": label, "why": f"unit_failed({type(e).__name__})"})
            units.append((label, ""))
            continue
        units.append((label, md.strip()))
        for a in doc.assets:
            e = placements.setdefault(a.origin_part,
                                      {"data": a.data, "media": a.media_type,
                                       "units": set()})
            e["units"].add(label)
    # The concatenation IS the engine output for a deck: it is byte-identical
    # to a whole-deck conversion (tests/test_anydoc_invariants.py), and it is
    # what this pipeline actually produced, so it is what the gate must hold
    # the artifact against.
    raw = "\n\n".join(b for _, b in units if b)
    return units, placements, failed, [], raw


def _docx(data):
    doc = anydoc.to_document(data, "docx")
    md = anydoc.to_markdown_bytes(data, "docx")

    # Level-1 headings are the unit boundary. Deeper ones would shred a
    # well-structured report into fragments too small to cite usefully, and a
    # document with no headings at all cites as a whole -- the honest answer
    # for a contract written as numbered prose rather than Heading styles.
    chunks = _split_markdown(md, 1)
    labels, seen = [], {}
    for lab, _ in chunks:
        name = lab or "doc"
        seen[name] = seen.get(name, 0) + 1
        # Real documents repeat heading text. Positional disambiguation keeps
        # two "Overview" sections from citing to the same place.
        labels.append(f"{name}#{seen[name]}" if seen[name] > 1 else name)
    units = [(labels[i], body) for i, (_, body) in enumerate(chunks)] \
        if chunks else [("doc", md.strip())]

    # Walk blocks in the same order the renderer did, so an image is credited
    # to the section it actually sits in. Placements are counted from image
    # inlines, not assets: anydoc dedups assets by package part, so two
    # placements of one image share an asset but keep their own inlines.
    placements = {}
    # The i-th level-1 heading opens the i-th unit -- unless the document
    # begins with content before any heading, in which case that leading
    # chunk is unit 0 and the headings start at 1. Getting this off by one
    # credits every image to the following section.
    has_lead = bool(chunks) and chunks[0][0] is None
    cursor = 0 if has_lead else -1
    current = units[0][0] if units else "doc"
    for b in doc.blocks:
        if b.kind == "heading" and b.level == 1:
            cursor += 1
            if 0 <= cursor < len(units):
                current = units[cursor][0]
        for inline in _image_inlines([b]):
            src = inline.source
            if not src or src.kind != "asset" or src.asset_id is None:
                continue
            if not 0 <= src.asset_id < len(doc.assets):
                continue
            a = doc.assets[src.asset_id]
            e = placements.setdefault(a.origin_part,
                                      {"data": a.data, "media": a.media_type,
                                       "units": set()})
            e["units"].add(current)
    return units, placements, [], [], md


def _xlsx(data):
    doc = anydoc.to_document(data, "xlsx")
    md = anydoc.to_markdown_bytes(data, "xlsx")
    with zipfile.ZipFile(io.BytesIO(data)) as zf:
        names = ooxml.sheet_names(zf)
        media = ooxml.images(zf)
        charts = ooxml.charts(zf)
        chart_sheet = ooxml.chart_sheets(zf)
        blobs = {part: zf.read(part) for part, _ in media if part in zf.namelist()}

    heads = [b.content[0].text for b in doc.blocks
             if b.kind == "heading" and b.content]
    tables = sum(1 for b in doc.blocks if b.kind == "table")
    if heads:
        # Names come from the emitted headings, never from zipping the
        # package's sheet list positionally: empty and unreadable sheets emit
        # nothing, so [Data, Empty, Notes] yields two tables and positional
        # zipping would cite Notes' table as "Empty".
        chunks = _split_markdown(md, 2)
        bodies = {lab: body for lab, body in chunks if lab}
        units = [(h, bodies.get(h, "")) for h in heads]
    elif tables == 1 and names:
        units = [(names[0], md.strip())]          # single sheet: no heading
    else:
        units = [("doc", md.strip())]

    known = {u for u, _ in units}
    placements = {}
    for part, sheet in media:
        if part not in blobs:
            continue
        e = placements.setdefault(part, {"data": blobs[part],
                                         "media": None, "units": set()})
        e["units"].add(sheet if sheet in known else "doc")

    chart_items, dropped = [], []
    for n, ch in enumerate(charts, start=1):
        sheet = chart_sheet.get(ch["part"])
        unit = sheet if sheet in known else (units[0][0] if units else "doc")
        if not ch["complete"]:
            dropped.append({"part": ch["part"], "why": "native_chart_unread"})
            continue
        chart_items.append({
            "id": f"chart{n:02d}", "page": unit, "kind": "native_chart",
            "reason": "native_chart", "px": [0, 0],
            "description": _chart_markdown(ch),
        })
    return units, placements, dropped, chart_items, md


def _chart_markdown(ch):
    """A chart as its own numbers, which beats describing it from pixels.

    Emitted as a description rather than a pending item, so it flows through
    the same delimited-splice machinery as everything the agent writes and
    the byte-identity gate keeps working unchanged.
    """
    head = ch["headers"]
    lines = []
    if ch["title"]:
        lines.append(f"**Chart.** {ch['title']}")
        lines.append("")
    lines.append("| " + " | ".join(h or " " for h in head) + " |")
    lines.append("|" + "|".join(["---"] * len(head)) + "|")
    for row in ch["rows"]:
        cells = list(row) + [""] * (len(head) - len(row))
        lines.append("| " + " | ".join(cells) + " |")
    lines.append("")
    lines.append("<sub>Series read from the chart definition, not from pixels.</sub>")
    return "\n".join(lines)


# ------------------------------------------------------------------ public
def harvest_office(path):
    """The harvest() contract for one Office document."""
    data = open(path, "rb").read()
    fmt = detect(data)
    if fmt is None:
        return {"status": "error", "error": "unsupported", "path": str(path),
                "detail": "not a docx, xlsx or pptx package"}
    try:
        units, placements, dropped, extra, raw_md = {
            "pptx": _pptx, "docx": _docx, "xlsx": _xlsx}[fmt](data)
    except anydoc.EncryptedError:
        return {"status": "error", "error": "encrypted", "path": str(path)}
    except anydoc.UnsupportedError as e:
        return {"status": "error", "error": "unsupported", "path": str(path),
                "detail": str(e)}
    except anydoc.ResourceLimitError as e:
        return {"status": "error", "error": "unreadable", "path": str(path),
                "detail": f"resource limit: {getattr(e, 'limit', '?')}"}
    except (anydoc.ConvertError, OSError) as e:
        return {"status": "error", "error": "unreadable", "path": str(path),
                "detail": f"{type(e).__name__}: {e}"}

    n_units = max(1, len(units))
    items, seen_hash = list(extra), {}
    for part, e in sorted(placements.items()):
        media = e["media"] or _sniff(e["data"])
        if media not in VIEWABLE:
            # anydoc faithfully retains EMF, WMF and OLE payloads. Routing one
            # to `pending` would create an item no agent can complete -- there
            # is no rasterizer here. Counted, never silently discarded.
            dropped.append({"part": part, "why": f"unviewable_media({media})"})
            continue
        w, h = dimensions(e["data"])
        why = furniture_reason(w, h, len(e["units"]), n_units)
        if why:
            dropped.append({"part": part, "px": [w, h], "why": why})
            continue
        digest = hashlib.sha256(e["data"]).hexdigest()
        if digest in seen_hash:
            dropped.append({"part": part, "px": [w, h],
                            "why": f"duplicate_of({seen_hash[digest]})"})
            continue
        seen_hash[digest] = part
        unit = sorted(e["units"])[0]
        items.append({
            "id": _item_id(part), "page": unit, "kind": "raster",
            "reason": "standalone_raster", "px": [w, h], "media_type": media,
            "description": None, "_bytes": e["data"],
        })

    # Present items in reading order: unit first, then id. Sorting by package
    # part instead puts image10 before image2, which reads as scrambled to
    # anyone stepping through `pending`.
    order = {u: n for n, (u, _) in enumerate(units)}
    items.sort(key=lambda i: (order.get(i["page"], len(order)), _natural(i["id"])))

    pending = [i for i in items if i.get("description") is None]
    # Verbatim engine output, exactly as the PDF path uses process_pdf's. The
    # unit split is a separate, lossy view for citation and cheap grepping --
    # reassembling doc.md from it would drop the heading lines the split
    # consumed, and the byte-identity gate would fail for the right reason.
    # NOT stripped. anydoc ends its output with a newline and the PDF path
    # writes process_pdf's text verbatim, so stripping here would put the
    # artifact one byte away from the engine and fail the gate for a reason
    # that has nothing to do with what the skill added.
    doc_md = raw_md
    return {
        "status": "ok", "path": str(path), "pdf_type": None, "pages": len(units),
        "markdown": doc_md,
        "page_markdown": [b for _, b in units],
        "unit_labels": [u for u, _ in units],
        "page_sigs": {}, "engine": ENGINE, "text_chars": len(doc_md),
        "vision_calls": len(pending), "over_scale_guard": False,
        "items": items, "dropped": dropped,
    }


def _sniff(data):
    from image import media_type
    return media_type(data)


def _natural(s):
    """Sort key where the 10 in image10 follows the 2 in image2."""
    return [int(t) if t.isdigit() else t for t in re.split(r"(\d+)", s)]


def _item_id(part):
    """A filesystem-safe id derived from the package part it came from."""
    return re.sub(r"[^A-Za-z0-9]+", "-", part.rsplit("/", 1)[-1]).strip("-")
