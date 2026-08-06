"""Standalone images, and the dimension sniffing the Office path shares.

An image file is the degenerate document: one unit, no text layer, exactly one
thing to look at. It gets an artifact anyway, because the value is in the
citation and cache contract rather than in the routing -- a described image
answers follow-up questions for free, like every other converted document.

Dimensions are read from file headers rather than through PyMuPDF. The Office
path needs them for the furniture filter, and making office.py import the PDF
engine to measure a PNG would drag the whole PDF dependency set into a path
that has no use for it.
"""
import struct

ENGINE = "image==1"

# What the host agent can actually look at. The Office path filters assets
# against this: anydoc faithfully retains EMF, WMF and OLE payloads, and
# routing one to `pending` would create an item no agent can complete, because
# there is no rasterizer here and LibreOffice is not a dependency.
VIEWABLE = {"image/png", "image/jpeg", "image/gif", "image/webp",
            "image/bmp", "image/tiff"}

EXT_MEDIA = {
    ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
    ".gif": "image/gif", ".webp": "image/webp", ".bmp": "image/bmp",
    ".tif": "image/tiff", ".tiff": "image/tiff",
}


def media_type(data):
    """MIME type from magic bytes, or None. Extension is never consulted."""
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        return "image/png"
    if data[:2] == b"\xff\xd8":
        return "image/jpeg"
    if data[:6] in (b"GIF87a", b"GIF89a"):
        return "image/gif"
    if data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        return "image/webp"
    if data[:2] == b"BM":
        return "image/bmp"
    if data[:4] in (b"II*\x00", b"MM\x00*"):
        return "image/tiff"
    return None


def dimensions(data):
    """(width, height) in px, or (0, 0) when the header cannot be read.

    (0, 0) is deliberately a value the furniture filter rejects as `small`:
    an image whose size cannot be established is not one to spend a vision
    call on sight-unseen.
    """
    try:
        kind = media_type(data)
        if kind == "image/png":
            return struct.unpack(">II", data[16:24])
        if kind == "image/gif":
            return struct.unpack("<HH", data[6:10])
        if kind == "image/bmp":
            w, h = struct.unpack("<ii", data[18:26])
            return abs(w), abs(h)
        if kind == "image/jpeg":
            return _jpeg_dims(data)
        if kind == "image/webp":
            return _webp_dims(data)
        if kind == "image/tiff":
            return _tiff_dims(data)
    except Exception:
        pass
    return (0, 0)


def _jpeg_dims(data):
    # Walk the segment chain to the first frame header. JPEG carries its size
    # in SOFn, and which n varies with the encoding (baseline, progressive,
    # arithmetic), so the whole SOF range is accepted except the four markers
    # in it that are not frame headers.
    i = 2
    while i + 9 < len(data):
        if data[i] != 0xFF:
            i += 1
            continue
        marker = data[i + 1]
        if 0xC0 <= marker <= 0xCF and marker not in (0xC4, 0xC8, 0xCC, 0xD8):
            h, w = struct.unpack(">HH", data[i + 5:i + 9])
            return w, h
        if marker in (0xD8, 0x01) or 0xD0 <= marker <= 0xD7:
            i += 2
            continue
        i += 2 + struct.unpack(">H", data[i + 2:i + 4])[0]
    return (0, 0)


def _webp_dims(data):
    fmt = data[12:16]
    if fmt == b"VP8 ":
        return struct.unpack("<HH", data[26:30])
    if fmt == b"VP8L":
        b = int.from_bytes(data[21:25], "little")
        return (b & 0x3FFF) + 1, ((b >> 14) & 0x3FFF) + 1
    if fmt == b"VP8X":
        w = int.from_bytes(data[24:27], "little") + 1
        h = int.from_bytes(data[27:30], "little") + 1
        return w, h
    return (0, 0)


def _tiff_dims(data):
    little = data[:2] == b"II"
    e = "<" if little else ">"
    offset = struct.unpack(e + "I", data[4:8])[0]
    count = struct.unpack(e + "H", data[offset:offset + 2])[0]
    w = h = 0
    for i in range(count):
        p = offset + 2 + i * 12
        tag, typ = struct.unpack(e + "HH", data[p:p + 4])
        if tag in (256, 257):
            # SHORT and LONG are both legal for these tags, and both are left
            # aligned in the value field.
            val = struct.unpack(e + "H", data[p + 8:p + 10])[0] if typ == 3 \
                else struct.unpack(e + "I", data[p + 8:p + 12])[0]
            if tag == 256:
                w = val
            else:
                h = val
    return w, h


def harvest_image(path):
    """The harvest() contract for a single image file."""
    data = open(path, "rb").read()
    kind = media_type(data)
    if kind is None:
        return {"status": "error", "error": "unreadable", "path": str(path),
                "detail": "not a recognised image format"}
    w, h = dimensions(data)
    item = {"id": "img", "page": "img", "kind": "raster",
            "reason": "no_text_layer", "px": [w, h], "media_type": kind,
            "description": None, "_bytes": data}
    # No furniture filter here, deliberately. A standalone file is what the
    # user chose to hand over; a 90x90 icon they asked about is the content,
    # not a logo on somebody else's page.
    return {
        "status": "ok", "path": str(path), "pdf_type": None, "pages": 1,
        "markdown": "", "page_markdown": [""], "page_sigs": {},
        "engine": "image", "text_chars": 0,
        "vision_calls": 1, "over_scale_guard": False,
        "items": [item], "dropped": [],
    }
