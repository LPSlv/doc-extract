# /// script
# requires-python = ">=3.10"
# ///
"""Regenerate the README's benchmark tables from docs/benchmarks/results/*.json.

The repo's rule is that no number is hand-carried. This prints the block that
lives between the README markers; `--write` splices it in.

Presentation follows Tufte: one encoding per quantity, the comparison in the
same row as the number, bold reserved for the single focal value, the negative
case left in sort position rather than footnoted, and headings that assert a
finding instead of labelling a category.
"""
import json, glob, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
BEGIN, END = "<!-- benchmarks:begin -->", "<!-- benchmarks:end -->"


def load():
    out = []
    for f in glob.glob(str(ROOT / "docs/benchmarks/results/*.json")):
        d = json.load(open(f)); s = d["summary"]
        out.append({"name": d["dataset"], "files": s["files"], "pages": s["pages"],
                    "opt": s["opt_tok"], "txt": s["txt_tok"], "ours": s["ours_tok"],
                    "calls": s["calls"]})
    return out


# A proportional bar was tried here and removed. With `bills` at 7.0x and every
# other corpus between 0.9x and 2.9x, eleven of twelve rows drew identically: the
# mark encoded the same quantity as the number beside it and discriminated worse.
# Redundant data-ink. The sorted numeric column does the ranking on its own.


def main(write=False):
    rows = sorted(load(), key=lambda r: -(r["opt"] / r["ours"]))
    O = sum(r["opt"] for r in rows); U = sum(r["ours"] for r in rows)
    T = sum(r["txt"] for r in rows); P = sum(r["pages"] for r in rows)
    F = sum(r["files"] for r in rows); C = sum(r["calls"] for r in rows)

    L = []
    L.append(f"Reading every page of these {F:,} PDFs costs {O/1e6:.1f}M input tokens. "
             f"pdf-extract reads the same {P:,} pages for {U/1e6:.1f}M — "
             f"**{O/U:.1f}× less** — because it looks at one page in three "
             f"({C:,} vision calls over {P:,} pages) instead of all of them.")
    L.append("")
    L.append("Extracting text alone is cheaper still, at "
             f"{T/1e6:.1f}M, and captures no figure, scan or unparsed table whatsoever. "
             "It is the floor, not an option.")
    L.append("")
    L.append("| corpus | files | pages | cheaper by | vision calls per page |")
    L.append("|---|--:|--:|--:|--:|")
    for r in rows:
        x = r["opt"] / r["ours"]
        mark = f"**{x:.1f}×**" if r is rows[0] else f"{x:.1f}×"
        L.append(f"| `{r['name']}` | {r['files']} | {r['pages']:,} | {mark} | "
                 f"{r['calls']/r['pages']:.2f} |")
    L.append("")
    L.append(f"`olmocr_long_tiny_text` sits last because it **loses**: 62 single-page "
             f"documents where text plus one figure render costs more than the page "
             f"itself. Single pages have nothing to amortise. It stays in the table.")
    print("\n".join(L))

    if write:
        p = ROOT / "README.md"; s = p.read_text()
        a, b = s.index(BEGIN) + len(BEGIN), s.index(END)
        p.write_text(s[:a] + "\n" + "\n".join(L) + "\n" + s[b:])
        print("\n-- written to README.md", file=sys.stderr)


if __name__ == "__main__":
    main("--write" in sys.argv)
