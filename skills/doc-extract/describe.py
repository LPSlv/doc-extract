# /// script
# requires-python = ">=3.10"
# ///
"""Write a visual description back into an artifact.

    uv run describe.py <artifact-dir> <item-id> "the description"
    uv run describe.py <artifact-dir> <item-id> -      # read from stdin

Updates manifest.json and rebuilds doc.md. Rebuilding always strips every
existing added block first and re-appends from the manifest, so running this
twice on the same item replaces rather than duplicates -- which is what makes a
half-finished vision pass safe to resume.

Where descriptions land, and why there are two answers:

`trailing` (the default) appends everything at the end of doc.md under one
heading, each entry labelled with its page. For a PDF that is the only honest
option: pdf-inspector's Markdown carries no page offsets -- its per-page text
comes from a different extractor and is often not even a substring of the
document text -- so "insert at the figure's position" is not knowable, and
pretending otherwise would put text in the wrong place.

`inline` (opt in with `convert.py --inline`) puts each description at the
position its manifest item recorded, which Office documents can supply and
PDFs cannot. It is an INSERTION at that offset, never a substitution: the
engine's own line stays exactly where it was. That distinction is the whole
reason the byte-identity guarantee survives the change -- see eval/gate.py,
which fails the moment anything is edited in place instead.

What inline does NOT promise is that the position is right. Byte-identity
cannot check placement: an insertion round-trips wherever it lands. office.py
only emits an image's own line as the anchor when the count of candidate lines
matches the count of image inlines exactly, and falls back to the end of the
unit otherwise -- so the position is either provably that image's, or a unit
boundary, never a guess between two lines that look alike.
"""
import sys, json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from artifact import splice, strip

HEADING = "## Figures and scanned pages"


def _label(unit):
    """`p12` for a PDF page; an Office unit is already its own label.

    PDF pages MUST keep the bare `p{n}` form: example/sample-report.expected.md
    and every gate corpus artifact carry it, and the byte-identity gate strips
    the block rather than reading it, so a change here would go unnoticed.
    """
    return f"p{unit}" if isinstance(unit, int) else str(unit)


def _order(pair):
    """Numeric for PDF pages, manifest order for Office units.

    Sorting Office units as strings would put a sheet named "10" before "2",
    and sorting mixed types raises outright. The manifest is already in
    reading order for those, so position is the honest key.
    """
    n, i = pair
    unit = i["page"]
    if isinstance(unit, int):
        return (0, unit, 0, i["id"])
    return (1, 0, n, "")


def _entry(item):
    return (f"**[{_label(item['page'])}] {item['id']}** "
            f"({item['reason']}) — {item['description']}")


def _anchor(item, base, inline):
    """Where this item's block goes, as an offset into the stripped text.

    None means "with the trailing block". An anchor that is missing, not an
    integer, or outside the engine text is treated as absent rather than
    trusted: manifests outlive the code that wrote them, and a stale offset
    must degrade to the end of the document, never into the middle of a word.
    """
    if not inline:
        return None
    a = item.get("anchor")
    if not isinstance(a, int) or isinstance(a, bool) or not 0 <= a <= len(base):
        return None
    return a


def rebuild(artifact):
    """Regenerate doc.md from the engine text plus every described item.

    Offsets in the manifest are offsets into the ENGINE's text, and `base` is
    the engine's text -- strip() has just removed every block this function
    previously added. That is what makes a resumed run land in the same place
    as the first one instead of drifting by the length of what it already
    wrote.
    """
    artifact = Path(artifact)
    man = json.loads((artifact / "manifest.json").read_text())
    base = strip((artifact / "doc.md").read_text())
    inline = man.get("placement") == "inline"

    described = [(n, i) for n, i in enumerate(man["items"]) if i.get("description")]
    if not described:
        (artifact / "doc.md").write_text(base)
        return 0

    groups, trailing = {}, []
    for _, i in sorted(described, key=_order):
        pos = _anchor(i, base, inline)
        if pos is None:
            trailing.append(_entry(i))
        else:
            groups.setdefault(pos, []).append(_entry(i))

    # Blocks in document order, so equal offsets keep reading order and the
    # trailing block -- which sits at the very end -- comes last.
    additions = [(pos, "\n\n".join(entries)) for pos, entries in sorted(groups.items())]
    if trailing:
        additions.append((len(base), "\n\n".join([HEADING] + trailing)))

    (artifact / "doc.md").write_text(splice(base, additions))
    return len(described)


def main(argv):
    if len(argv) < 3:
        print("usage: describe.py <artifact-dir> <item-id> <text|->", file=sys.stderr)
        return 2
    artifact, item_id, text = Path(argv[0]), argv[1], argv[2]
    if text == "-":
        text = sys.stdin.read()
    text = text.strip()
    if not text:
        print("refusing to write an empty description", file=sys.stderr)
        return 2

    mf = artifact / "manifest.json"
    if not mf.exists():
        print(f"no manifest at {mf}", file=sys.stderr)
        return 2
    man = json.loads(mf.read_text())

    hit = next((i for i in man["items"] if i["id"] == item_id), None)
    if hit is None:
        ids = ", ".join(i["id"] for i in man["items"]) or "(none)"
        print(f"no item {item_id!r}. known: {ids}", file=sys.stderr)
        return 2

    hit["description"] = text
    mf.write_text(json.dumps(man, indent=2))
    n = rebuild(artifact)
    remaining = sum(1 for i in man["items"] if not i.get("description"))
    print(json.dumps({"status": "ok", "id": item_id, "described": n,
                      "remaining": remaining, "doc_md": str(artifact / "doc.md")}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
