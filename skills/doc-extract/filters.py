"""Format-agnostic filters shared by the PDF and Office paths.

These four thresholds and the two functions over them are the only routing
logic that means the same thing regardless of where an image came from: a logo
is small, thin, or repeated on every unit whether the unit is a PDF page, a
slide, or a worksheet. Everything else in harvest.py reads PDF vector geometry
and has no Office analogue -- see the design spec, section 4.3.

Deliberately NOT here: the pixel-hash dedup. harvest.py's version is entangled
with xref and raw-stream shortcuts that exist to avoid re-encoding every image
(harvest.py:417-449, worth a measured speedup on datasheet corpora), and the
Office analogue is three lines of sha256 over bytes anydoc already decoded.
Sharing them would mean generalising the fast path into something neither side
wants, for no measured gain.

The numbers are fitted, not learned. Every one is justified in the design spec
and regenerated into the README; change one and the benchmark tables move.
"""

MIN_DIM       = 120    # px; smaller on either side => furniture
MAX_ASPECT    = 8.0    # w:h beyond this => rule/stripe, not a figure
MIN_AREA      = 40_000 # px^2
UBIQUITY      = 0.50   # placed on more than this fraction of pages => furniture

MAX_EDGE_PX = 1568       # above this the model downsamples anyway


def furniture_reason(w, h, placements, npages):
    """Why this image is page furniture rather than content -- or None.

    `placements` is how many units carry the image and `npages` how many units
    exist, so ubiquity means the same thing for a slide deck as for a PDF. The
    two-unit floor keeps a cover image in a one- or two-page document from
    reading as a repeated emblem.
    """
    if npages > 2 and placements / npages > UBIQUITY:
        return f"ubiquitous({placements}/{npages}pp)"
    if w < MIN_DIM or h < MIN_DIM:
        return f"small({w}x{h})"
    if max(w, h) / max(1, min(w, h)) > MAX_ASPECT:
        return "sliver"
    if w * h < MIN_AREA:
        return "low_area"
    return None


def _tok(w, h, cap=MAX_EDGE_PX):
    """Image tokens an w x h image costs after the model's own downscale."""
    s = min(1.0, cap / max(w, h))
    return int((w * s) * (h * s) / 750)
