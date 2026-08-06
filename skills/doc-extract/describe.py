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

Where descriptions land: appended at the end of doc.md under one heading, each
labelled with its page. pdf-inspector's Markdown carries no page offsets, so
"insert at the figure's position" is not knowable from its output; pretending
otherwise would put text in the wrong place. End-of-document with an explicit
[pN] label is honest and keeps citations working.
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


def rebuild(artifact):
    """Regenerate doc.md from the engine text plus every described item."""
    artifact = Path(artifact)
    man = json.loads((artifact / "manifest.json").read_text())
    base = strip((artifact / "doc.md").read_text())

    described = [(n, i) for n, i in enumerate(man["items"]) if i.get("description")]
    if not described:
        (artifact / "doc.md").write_text(base)
        return 0

    lines = [HEADING, ""]
    for _, i in sorted(described, key=_order):
        lines.append(f"**[{_label(i['page'])}] {i['id']}** ({i['reason']}) — {i['description']}")
        lines.append("")
    body = "\n".join(lines).rstrip()

    (artifact / "doc.md").write_text(splice(base, [(len(base), body)]))
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
