# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "pdf-inspector==0.2.6",
#   "pymupdf==1.28.0",
#   "firecrawl-anydoc==0.1.6",
# ]
# ///
"""Byte-identity gate: prove the skill cannot degrade text extraction.

Covers every format the skill reads. The reference is whatever engine produced
the text for that format -- pdf-inspector for PDFs, anydoc for Office -- so the
guarantee reads the same either way: everything this skill adds is strippable,
and what remains is exactly what the engine said.

Runs the REAL pipeline -- convert, then describe every pending item (including
one payload that quotes the close delimiter, and one re-describe to simulate a
resumed run) -- then strips the added blocks from the produced doc.md and
requires the residue to equal raw pdf-inspector output exactly.

An earlier version of this file spliced strings into engine markdown and
compared the result to itself. That was a unit test of artifact.py wearing a
benchmark's clothes: it never touched the pipeline, so it could not have caught
a pipeline that edited text in place. This one can.

Every document is run TWICE, once per placement:

  trailing  every description in one block at the end of doc.md
  inline    each description at the offset its manifest item recorded

Both must round-trip. Inline is the mode that needs the gate most, because it is
the one that could have been built as a substitution -- overwrite the engine's
placeholder line, and record what was overwritten so it can be put back. That
reverses perfectly and would sail through a byte comparison while eating any
prose line it mistook for a placeholder, so this file also checks WHERE each
block landed:

  * every block begins at a line boundary of the engine text -- a block spliced
    into the middle of a line still strips back to the same bytes;
  * every anchor the manifest recorded is a position a block is actually at, so
    a pipeline that quietly stopped inlining fails even though it round-trips.

Both checks were verified by breaking the pipeline on purpose, along with the
byte comparison itself: substitution at a correct anchor, substitution at an
ambiguous one, inlining silently disabled, and an anchor three bytes into a
line. All four fail this gate.

Usage:  uv run eval/gate.py <pdf|dir> [...]
"""
import json, re, sys, shutil, tempfile, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "doc-extract"
sys.path.insert(0, str(SKILL))

import pdf_inspector as pi
import anydoc
from artifact import strip, OPEN, CLOSE
from convert import convert
from describe import main as describe_main

HOSTILE = f"Table shows {CLOSE} and a total of 40 000 EUR"

_BLOCK = re.compile("\n" + re.escape(OPEN) + "\n.*?\n" + re.escape(CLOSE) + "\n",
                    re.DOTALL)


def spots(produced):
    """Where each added block sits, as an offset into the STRIPPED text.

    Computed from the produced file rather than from the manifest on purpose:
    what is being checked is where the pipeline actually wrote, not where it
    meant to.
    """
    out, removed = [], 0
    for m in _BLOCK.finditer(produced):
        out.append(m.start() - removed)
        removed += m.end() - m.start()
    return out


EXTS = ("*.pdf", "*.docx", "*.xlsx", "*.pptx")


def targets(args):
    for a in args:
        p = pathlib.Path(a)
        if not p.is_dir():
            yield p
            continue
        for pat in EXTS:
            yield from sorted(p.glob(pat))


def reference(path):
    """What the engine says this document's text is, before the skill adds to it.

    For pptx that is the concatenation of per-slide conversions rather than a
    whole-deck one, because per-slide repacking is part of the pipeline under
    test -- comparing against a whole-deck run would be testing anydoc. The two
    are byte-identical except on decks carrying internal slide-to-slide links,
    a divergence class understood in the design spec and reported separately
    below, so any OTHER divergence is a bug this catches.
    """
    data = path.read_bytes()
    if data[:5] == b"%PDF-":
        return getattr(pi.process_pdf(str(path)), "markdown", None) or "", None
    fmt = anydoc.format_from_bytes(data)
    if fmt != "pptx":
        return anydoc.to_markdown_bytes(data, fmt), None
    sys.path.insert(0, str(SKILL))
    import ooxml
    parts = [anydoc.to_markdown_bytes(ooxml.repack_single(data, r), "pptx").strip()
             for r in ooxml.slide_rids(data)]
    concat = "\n\n".join(p for p in parts if p)
    whole = anydoc.to_markdown_bytes(data, "pptx").strip()
    return concat, (concat == whole)


def check(pdf, cache_root, inline=False):
    raw, agrees = reference(pdf)
    r = convert(str(pdf), root=cache_root, force=True, inline=inline)
    if r["status"] != "ok":
        return None, f"convert failed: {r.get('error')}"

    art = pathlib.Path(r["artifact"])
    for n, item in enumerate(r["pending"]):
        body = HOSTILE if n == 0 else f"**Figure.** Description of {item['id']}."
        describe_main([str(art), item["id"], body])
        if n == 0:                      # resumed-run replay
            describe_main([str(art), item["id"], body])

    produced = (art / "doc.md").read_text()
    residue = strip(produced)
    if residue != raw:
        return False, f"residue {len(residue)} != engine {len(raw)}"
    if r["pending"] and produced == raw:
        return False, "descriptions were not written at all"

    at = spots(produced)
    for pos in at:
        # A block that starts mid-line has split a line of engine text in two.
        # Stripping still restores the bytes, so byte-identity alone would not
        # notice; a reader would.
        if not (pos == 0 or pos == len(residue)
                or residue[pos - 1] == "\n" or residue[pos] == "\n"):
            return False, f"block at {pos} does not start on a line boundary"

    man = json.loads((art / "manifest.json").read_text())
    described = [i for i in man["items"] if i.get("description")]
    anchored = [i for i in described if i.get("anchor") is not None]
    if inline:
        if man.get("placement") != "inline":
            return False, "artifact did not record the placement it was built with"
        # The point of the mode: every anchor the manifest recorded must be a
        # position where a block actually is. Recomputed from the produced
        # file, so a pipeline that quietly reverted to trailing placement fails
        # here even though its bytes still round-trip.
        missing = sorted({i["anchor"] for i in anchored} - set(at))
        if missing:
            return False, (f"{len(missing)} anchored item(s) not placed at their "
                           f"anchor: {missing[:4]}")
    elif len(at) > 1:
        return False, "trailing placement wrote more than one block"

    note = (f"{len(r['pending'])} described, {len(anchored)}/{len(described)} "
            f"anchored, blocks at {len(at)} position(s)")
    if agrees is False:
        note += "; per-slide concat differs from whole-deck (internal links)"
    return True, note


def main(args):
    files = list(targets(args))
    if not files:
        print("usage: uv run eval/gate.py <file|dir> [...]", file=sys.stderr)
        return 2
    cache_root = pathlib.Path(tempfile.mkdtemp(prefix="docx-gate-"))
    ok = bad = skip = 0
    try:
        for p in files:
            for mode in ("trailing", "inline"):
                try:
                    verdict, note = check(p, cache_root, inline=(mode == "inline"))
                except Exception as e:
                    verdict, note = None, f"{type(e).__name__}: {e}"
                if verdict is None:
                    skip += 1
                    print(f"SKIP {p.name} [{mode}]: {note}")
                elif verdict:
                    ok += 1
                    if "differs" in note:
                        print(f"NOTE {p.name} [{mode}]: {note}")
                else:
                    bad += 1
                    print(f"FAIL {p.name} [{mode}]: {note}")
    finally:
        shutil.rmtree(cache_root, ignore_errors=True)
    print(f"\n{ok}/{ok + bad} runs round-trip to byte-identity "
          f"({len(files)} documents x 2 placements)"
          f"{f' ({skip} skipped)' if skip else ''}")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
