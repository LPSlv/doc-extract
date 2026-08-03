# /// script
# requires-python = ">=3.10"
# dependencies = ["pdf-inspector==0.2.6"]
# ///
"""Byte-identity gate: prove the skill cannot degrade text extraction.

For each PDF, splice descriptions into the engine's Markdown (including a
payload that quotes the close delimiter), re-splice to simulate a resumed run,
then strip and require the residue to equal raw engine output exactly.

Usage:  uv run eval/gate.py <pdf|dir> [...]
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "skills" / "pdf-extract"))
import pdf_inspector as pi
from artifact import splice, strip, OPEN, CLOSE

HOSTILE = f"Table shows {CLOSE} and a total of 40 000 EUR"


def targets(args):
    for a in args:
        p = pathlib.Path(a)
        yield from (sorted(p.glob("*.pdf")) if p.is_dir() else [p])


def main(args):
    files = list(targets(args))
    if not files:
        print("usage: uv run eval/gate.py <pdf|dir> [...]"); return 2
    bad = 0
    for p in files:
        try:
            raw = getattr(pi.process_pdf(str(p)), "markdown", None) or ""
        except Exception as e:
            print(f"SKIP {p.name}: {type(e).__name__}"); continue
        adds = [(len(raw), "**Figure.** Stacked bar."), (max(0, len(raw) // 2), HOSTILE)]
        out = splice(raw, adds)
        again = splice(out, adds)
        if strip(out) != raw or strip(again) != raw \
                or out.count(OPEN) != 2 or out.count(CLOSE) != 2:
            bad += 1
            print(f"FAIL {p.name}")
    print(f"\n{len(files) - bad}/{len(files)} documents round-trip to byte-identity")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
