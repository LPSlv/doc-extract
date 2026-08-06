"""OOXML package reading, for the parts anydoc does not give us.

Standard library only, deliberately: this is the whole reason the Office path
costs no dependency beyond the anydoc wheel.

Two jobs, and only two. Anything anydoc already does correctly is NOT done
here -- duplicating its output was the single largest error in the first draft
of this design.

  pptx   sldIdLst surgery, so one slide at a time can be handed to anydoc.
         That is how unit boundaries AND per-slide asset placement are
         obtained; anydoc's own model exposes neither.

  xlsx   sheet names, charts and images. anydoc's spreadsheet path is pure
         cell extraction -- measured on tests/fixtures/book.xlsx, it returns
         zero assets and no chart while the package plainly holds
         xl/media/image1.png and xl/charts/chart1.xml. For docx and pptx it
         handles both, so neither is read here.

The pptx surgery is textual rather than an xml.etree round-trip. ElementTree
rewrites namespace prefixes on write, which changes the bytes anydoc parses
for no reason; and the only edit needed is deleting sibling elements from one
list. Both the self-closing and element forms of sldId are legal, and the
prefix is not guaranteed to be `p`, so the patterns match either.
"""
import io
import re
import zipfile
import xml.etree.ElementTree as ET

# Namespaces, spelled out once. OOXML files in the wild bind these to varying
# prefixes, so every lookup goes through a qualified name rather than a prefix.
NS = {
    "pkg":   "http://schemas.openxmlformats.org/package/2006/relationships",
    "rel":   "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "ss":    "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
    "chart": "http://schemas.openxmlformats.org/drawingml/2006/chart",
    "xdr":   "http://schemas.openxmlformats.org/drawingml/2006/spreadsheetDrawing",
    "a":     "http://schemas.openxmlformats.org/drawingml/2006/main",
}
OFFICE_DOC_REL = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument"
IMAGE_REL = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/image"

# Prefix-agnostic: `<p:sldId .../>`, `<sldId .../>` and `<x:sldId>...</x:sldId>`
# are all legal spellings of the same thing.
_SLDIDLST = re.compile(r"<(?:\w+:)?sldIdLst\s*>(.*?)</(?:\w+:)?sldIdLst\s*>", re.S)
_SLDID = re.compile(r"<(?:\w+:)?sldId\b[^>]*?(?:/>|>.*?</(?:\w+:)?sldId\s*>)", re.S)
# `id` and `r:id` are different attributes on sldId; only the prefixed one is
# the relationship. Matching bare `id=` here would address the wrong slide.
_RID = re.compile(r'\s\w+:id\s*=\s*"([^"]+)"')


def _q(ns, tag):
    return f"{{{NS[ns]}}}{tag}"


def _resolve(base_part, target):
    """Resolve a relationship target against the part that declared it."""
    if target.startswith("/"):
        return target.lstrip("/")
    segs = base_part.rsplit("/", 1)[0].split("/") if "/" in base_part else []
    for seg in target.split("/"):
        if seg == "..":
            if segs:
                segs.pop()
        elif seg not in (".", ""):
            segs.append(seg)
    return "/".join(segs)


def rels_for(zf, part):
    """{rId: (type, resolved-target-part)} for one part. Empty if it has none."""
    name = f"{part.rsplit('/', 1)[0]}/_rels/{part.rsplit('/', 1)[-1]}.rels" if "/" in part \
        else f"_rels/{part}.rels"
    try:
        root = ET.fromstring(zf.read(name))
    except (KeyError, ET.ParseError):
        return {}
    out = {}
    for r in root.findall(_q("pkg", "Relationship")):
        rid, typ, tgt = r.get("Id"), r.get("Type", ""), r.get("Target", "")
        if r.get("TargetMode") == "External":
            continue
        out[rid] = (typ, _resolve(part, tgt))
    return out


def main_part(zf):
    """The package's officeDocument part, from the root relationships.

    anydoc discovers it the same way rather than assuming a conventional path,
    and a package that has been through some producers does not use one.
    """
    try:
        root = ET.fromstring(zf.read("_rels/.rels"))
    except (KeyError, ET.ParseError):
        return None
    for r in root.findall(_q("pkg", "Relationship")):
        if r.get("Type") == OFFICE_DOC_REL:
            return _resolve("", r.get("Target", ""))
    return None


# ------------------------------------------------------------------ pptx
def slide_rids(data):
    """Relationship ids of every slide, in sldIdLst order.

    That order is what PowerPoint's sidebar shows, including hidden slides,
    so the index into this list is the number a citation should carry.
    """
    with zipfile.ZipFile(io.BytesIO(data)) as zf:
        part = main_part(zf) or "ppt/presentation.xml"
        pres = zf.read(part).decode("utf8", "replace")
    lst = _SLDIDLST.search(pres)
    if not lst:
        return []
    out = []
    for entry in _SLDID.findall(lst.group(1)):
        m = _RID.search(entry)
        if m:
            out.append(m.group(1))
    return out


def repack_single(data, rid):
    """The package with sldIdLst reduced to `rid` alone.

    Every layout, master, notes and media part stays, so anydoc's
    slide -> layout -> master -> presentation-default text cascade still
    resolves and the extraction is exactly what a whole-deck run would give
    for that slide. Verified byte-identical on the committed fixtures; see
    tests/test_anydoc_invariants.py.
    """
    with zipfile.ZipFile(io.BytesIO(data)) as zf:
        names = zf.namelist()
        parts = {n: zf.read(n) for n in names}
    part = _main_part_name(parts) or "ppt/presentation.xml"
    pres = parts[part].decode("utf8", "replace")
    lst = _SLDIDLST.search(pres)
    if not lst:
        return data
    keep = [e for e in _SLDID.findall(lst.group(1))
            if (m := _RID.search(e)) and m.group(1) == rid]
    parts[part] = pres.replace(lst.group(1), "".join(keep), 1).encode("utf8")

    buf = io.BytesIO()
    # Deflate rather than store: the repack happens once per slide and the
    # bytes are handed straight to anydoc, so size matters more than the
    # microseconds compression costs.
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as out:
        for n in names:
            out.writestr(n, parts[n])
    return buf.getvalue()


def _main_part_name(parts):
    try:
        root = ET.fromstring(parts["_rels/.rels"])
    except (KeyError, ET.ParseError):
        return None
    for r in root.findall(_q("pkg", "Relationship")):
        if r.get("Type") == OFFICE_DOC_REL:
            return _resolve("", r.get("Target", ""))
    return None


# ------------------------------------------------------------------ xlsx
def sheet_names(zf):
    """Worksheet names in workbook order.

    Only used for the single-sheet case: anydoc gates its `## <name>` heading
    on a multi-sheet workbook, so with one sheet there is no heading to read
    the name from. For multi-sheet workbooks the names MUST come from the
    emitted headings instead -- empty and unreadable sheets emit nothing, so
    this list and anydoc's tables do not correspond positionally. Measured on
    tests/fixtures/book.xlsx: [Data, Empty, Notes] yields two tables.
    """
    part = main_part(zf) or "xl/workbook.xml"
    try:
        root = ET.fromstring(zf.read(part))
    except (KeyError, ET.ParseError):
        return []
    return [s.get("name", "") for s in root.iter(_q("ss", "sheet"))]


def _shared_strings(zf):
    try:
        root = ET.fromstring(zf.read("xl/sharedStrings.xml"))
    except (KeyError, ET.ParseError):
        return []
    return ["".join(t.text or "" for t in si.iter(_q("ss", "t")))
            for si in root.findall(_q("ss", "si"))]


_CELL = re.compile(r"([A-Z]+)(\d+)")


def _col_index(letters):
    n = 0
    for ch in letters:
        n = n * 26 + (ord(ch) - 64)
    return n


def sheet_cells(zf, sheet_part, shared=None):
    """{'B2': 'value'} for one worksheet, shared strings already resolved."""
    shared = _shared_strings(zf) if shared is None else shared
    try:
        root = ET.fromstring(zf.read(sheet_part))
    except (KeyError, ET.ParseError):
        return {}
    out = {}
    for c in root.iter(_q("ss", "c")):
        ref, typ = c.get("r"), c.get("t")
        if not ref:
            continue
        if typ == "inlineStr":
            val = "".join(t.text or "" for t in c.iter(_q("ss", "t")))
        else:
            v = c.find(_q("ss", "v"))
            val = v.text if v is not None else None
            if val is None:
                continue
            if typ == "s":
                try:
                    val = shared[int(val)]
                except (ValueError, IndexError):
                    pass
        out[ref] = val
    return out


def _expand(ref):
    """'Data!$B$2:$B$4' -> (sheet, ['B2','B3','B4']). Single cells too."""
    sheet, _, rng = ref.rpartition("!")
    sheet = sheet.strip("'").replace("''", "'")
    rng = rng.replace("$", "")
    start, _, end = rng.partition(":")
    ms, me = _CELL.fullmatch(start), _CELL.fullmatch(end or start)
    if not (ms and me):
        return sheet, []
    c0, r0 = _col_index(ms.group(1)), int(ms.group(2))
    c1, r1 = _col_index(me.group(1)), int(me.group(2))
    cells = []
    for col in range(min(c0, c1), max(c0, c1) + 1):
        letters = ""
        n = col
        while n:
            n, rem = divmod(n - 1, 26)
            letters = chr(65 + rem) + letters
        for row in range(min(r0, r1), max(r0, r1) + 1):
            cells.append(f"{letters}{row}")
    return sheet, cells


def _cached(node, zf, sheet_map, shared):
    """Values for one c:cat / c:val node: cache first, then resolve the range.

    Producers disagree about caches. Excel writes them; openpyxl writes only
    the c:f reference and no cache at all (measured on the committed
    book.xlsx). Reading the reference against the workbook's own sheets covers
    that second population exactly, because the data is in the same file.
    """
    if node is None:
        return []
    vals = [(int(pt.get("idx", i)), (pt.find(_q("chart", "v")).text or ""))
            for i, pt in enumerate(node.iter(_q("chart", "pt")))
            if pt.find(_q("chart", "v")) is not None]
    if vals:
        return [v for _, v in sorted(vals)]
    f = node.find(f".//{_q('chart', 'f')}")
    if f is None or not f.text:
        return []
    sheet, cells = _expand(f.text)
    part = sheet_map.get(sheet)
    if not part:
        return []
    got = sheet_cells(zf, part, shared)
    return [got.get(c, "") for c in cells]


def _first(parent, *tags):
    """First present child among `tags`, by identity rather than truthiness."""
    for t in tags:
        el = parent.find(_q("chart", t))
        if el is not None:
            return el
    return None


def _sheet_part_map(zf):
    part = main_part(zf) or "xl/workbook.xml"
    try:
        root = ET.fromstring(zf.read(part))
    except (KeyError, ET.ParseError):
        return {}
    rels = rels_for(zf, part)
    out = {}
    for s in root.iter(_q("ss", "sheet")):
        rid = s.get(_q("rel", "id"))
        if rid in rels:
            out[s.get("name", "")] = rels[rid][1]
    return out


def charts(zf):
    """Every chart in a workbook as {title, headers, rows, part, complete}.

    `complete` is False when a series carried neither cached points nor a
    resolvable reference -- scatter and bubble charts use c:xVal/c:yVal, which
    this reads, but a chart referencing an external workbook resolves to
    nothing. Those are reported, never silently dropped.
    """
    shared = _shared_strings(zf)
    sheet_map = _sheet_part_map(zf)
    out = []
    for name in sorted(n for n in zf.namelist()
                       if re.fullmatch(r"xl/charts/chart\d+\.xml", n)):
        try:
            root = ET.fromstring(zf.read(name))
        except ET.ParseError:
            out.append({"part": name, "title": "", "headers": [], "rows": [],
                        "complete": False})
            continue
        title_el = root.find(f".//{_q('chart', 'title')}")
        title = " ".join(t.text.strip() for t in title_el.iter(_q("a", "t"))
                         if t.text) if title_el is not None else ""
        cats, series, complete = [], [], True
        for ser in root.iter(_q("chart", "ser")):
            tx = ser.find(_q("chart", "tx"))
            label = ""
            if tx is not None:
                label = " ".join(_cached(tx, zf, sheet_map, shared)) or ""
            # `or` would be wrong here: an Element with no children is falsy,
            # so an empty <c:cat> would silently fall through to <c:xVal> and
            # read a scatter chart's X values as categories.
            cat_node = _first(ser, "cat", "xVal")
            val_node = _first(ser, "val", "yVal")
            got = _cached(cat_node, zf, sheet_map, shared)
            if got and not cats:
                cats = got
            vals = _cached(val_node, zf, sheet_map, shared)
            if not vals:
                complete = False
            series.append((label, vals))
        rows = []
        for i, cat in enumerate(cats):
            rows.append([cat] + [(v[i] if i < len(v) else "") for _, v in series])
        out.append({"part": name, "title": title,
                    "headers": [""] + [lab for lab, _ in series],
                    "rows": rows,
                    "complete": bool(complete and cats and series)})
    return out


CHART_REL = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/chart"


def chart_sheets(zf):
    """{chart-part: sheet-name} for charts anchored in a worksheet.

    A citation that names the wrong sheet is worse than no citation, and a
    workbook's charts are rarely all on its first sheet.
    """
    out = {}
    for sheet, part in _sheet_part_map(zf).items():
        for _, target in rels_for(zf, part).items():
            if not target[1].startswith("xl/drawings/"):
                continue
            for dtyp, dtarget in rels_for(zf, target[1]).values():
                if dtyp == CHART_REL:
                    out[dtarget] = sheet
    return out


def images(zf):
    """[(media-part, sheet-name)] for every image anchored in a worksheet.

    Attribution matters: an image on one sheet of a twelve-sheet workbook is
    content, and the same logo on all twelve is furniture. Without the sheet
    it came from there is no placement count to make that call.
    """
    sheet_map = _sheet_part_map(zf)
    out = []
    for sheet, part in sheet_map.items():
        for typ, target in rels_for(zf, part).values():
            if not target.startswith("xl/drawings/"):
                continue
            for dtyp, dtarget in rels_for(zf, target).values():
                if dtyp == IMAGE_REL:
                    out.append((dtarget, sheet))
    return out
