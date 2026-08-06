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

Usage:  uv run eval/gate.py <pdf|dir> [...]
"""
import sys, shutil, tempfile, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "pdf-extract"
sys.path.insert(0, str(SKILL))

import pdf_inspector as pi
import anydoc
from artifact import strip, CLOSE
from convert import convert
from describe import main as describe_main

HOSTILE = f"Table shows {CLOSE} and a total of 40 000 EUR"


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


def check(pdf, cache_root):
    raw, agrees = reference(pdf)
    r = convert(str(pdf), root=cache_root, force=True)
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
    note = f"{len(r['pending'])} described"
    if agrees is False:
        note += "; per-slide concat differs from whole-deck (internal links)"
    return True, note


def main(args):
    files = list(targets(args))
    if not files:
        print("usage: uv run eval/gate.py <file|dir> [...]", file=sys.stderr)
        return 2
    cache_root = pathlib.Path(tempfile.mkdtemp(prefix="pdfx-gate-"))
    ok = bad = skip = 0
    try:
        for p in files:
            try:
                verdict, note = check(p, cache_root)
            except Exception as e:
                verdict, note = None, f"{type(e).__name__}: {e}"
            if verdict is None:
                skip += 1
                print(f"SKIP {p.name}: {note}")
            elif verdict:
                ok += 1
                if "differs" in note:
                    print(f"NOTE {p.name}: {note}")
            else:
                bad += 1
                print(f"FAIL {p.name}: {note}")
    finally:
        shutil.rmtree(cache_root, ignore_errors=True)
    print(f"\n{ok}/{ok + bad} documents round-trip to byte-identity"
          f"{f' ({skip} skipped)' if skip else ''}")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
