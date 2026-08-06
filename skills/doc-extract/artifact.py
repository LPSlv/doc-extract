"""Splice and strip for doc-extract artifacts.

The design spec's byte-identity guarantee (§5) lives here. Everything the skill
adds to pdf-inspector's output sits inside a delimited block; the benchmark gate
strips those blocks and asserts the residue equals raw engine output exactly.

The insertion template and strip pattern are a matched pair and must stay that
way -- of nine plausible pairings tried during review, only one round-tripped to
byte-identity. Do not "tidy" the newlines in either without re-running
tests/test_artifact.py.
"""
import re

OPEN = "<!-- doc-extract:add -->"
CLOSE = "<!-- /doc-extract:add -->"

_BLOCK = re.compile(
    "\n" + re.escape(OPEN) + "\n.*?\n" + re.escape(CLOSE) + "\n",
    re.DOTALL,
)


def _escape(body: str) -> str:
    """Neutralise comment delimiters inside a description.

    A vision transcription of a page that discusses HTML -- or a PDF crafted to
    contain the close delimiter -- would otherwise terminate the block early and
    leave fragments behind after stripping.
    """
    return body.replace("<!--", "&lt;!--").replace("-->", "--&gt;")


def strip(text: str) -> str:
    """Remove every added block. A no-op on text that has none."""
    return _BLOCK.sub("", text)


def splice(text: str, additions):
    """Insert `additions` as delimited blocks. `additions` is [(offset, body)].

    Strips first, so a resumed run replaces rather than stacks duplicates.
    Offsets refer to the stripped text and are applied back-to-front so that
    earlier ones stay valid.
    """
    base = strip(text)
    for pos, body in sorted(additions, key=lambda a: -a[0]):
        block = "\n" + OPEN + "\n" + _escape(body) + "\n" + CLOSE + "\n"
        base = base[:pos] + block + base[pos:]
    return base
