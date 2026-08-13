# /// script
# requires-python = ">=3.10"
# dependencies = ["pymupdf==1.28.0"]
# ///
"""Enlarge the journal evidence for the proposed rule, and say what it is.

`eval/filter3.md` reports the rule at **1 of 9** on `corpus/pmc_holdout`. Nine
is not a sample of that corpus: at T = 4 the rule fires exactly nine times
there and all nine were labelled, so it is a CENSUS and 11% cannot be enlarged
by drawing more pages of the same rule from the same corpus. The only cheap
enlargement available is the other journal corpus.

`corpus/pmc` carries **12** firings of the same rule and **none of them is in
`eval/filter3/labels.tsv`**: the 250-page in-sample draw sampled 4 `pmc`
`curves` pages and none happened to have exactly three pipe rows, so the
in-sample labelling says nothing about the journal cell of this rule at all.

Labelling those 12 doubles the journal evidence, 9 -> 21. It is in-sample by
corpus, and that is stated wherever the number is used: `corpus/pmc` is one of
the five corpora the rule was designed on. Pooled into the datasheet-holdout
batches under the same opaque tags so no labeller can tell the two apart.

    uv run eval/filter3_pmc_more.py
"""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills" / "doc-extract"))
import fitz                                                      # noqa: E402

OUT = ROOT / "eval" / "filter3" / "datasheet_holdout"
DPI = 130


def firings():
    """The proposed rule's page set on `corpus/pmc`, read off the enumeration
    `eval/filter3.py measure` wrote. The predicate is spelled out here rather
    than imported so it can be checked against filter3.md's own definition:
    filter 3 fires (>= 3 pipe rows), the page carries NO raster,
    `render_reason` returns a reason, neither `vector_furniture` nor
    `boxed_text` would have taken the page anyway, and the table is a single
    data row (fewer than 4 pipe lines)."""
    b = json.loads((ROOT / "eval" / "filter3" / "firings.json").read_text())
    return [r for r in b["firings"]
            if r["corpus"] == "pmc" and r["raw_rasters"] == 0
            and r["reason"] and not r["vector_furniture"]
            and not r["boxed_text"] and r["pipe_rows"] < 4]


def main():
    rows = sorted(firings(), key=lambda r: (r["name"], r["page"]))
    s = json.loads((OUT / "sample.json").read_text())
    have = {(r["file"], r["page"]) for r in s["rows"]}
    n0 = max(int(r["tag"][1:]) for r in s["rows"])
    add = []
    for i, r in enumerate(rows, start=n0 + 1):
        if (r["name"], r["page"]) in have:
            continue
        tag = f"d{i:03d}"
        with fitz.open(str(ROOT / r["doc"])) as doc:
            doc[r["page"] - 1].get_pixmap(dpi=DPI).save(
                str(OUT / "pages" / f"{tag}.png"))
        add.append({"tag": tag, "corpus": "pmc", "vendor": "pmc(journal)",
                    "file": r["name"], "page": r["page"], "reason": r["reason"],
                    "pipe_rows": r["pipe_rows"], "curves": r["curves"],
                    "diagonals": r["diagonals"], "collapsed": None,
                    "kind": "page_render", "predicate": True})
    for r in s["rows"]:
        r.setdefault("corpus", "datasheet_holdout")
    s["rows"] += add
    s["pmc_pooled"] = {
        "corpus": "corpus/pmc", "population": len(rows), "added": len(add),
        "why": "in-sample by corpus; the only cheap enlargement of the journal "
               "cell, whose holdout n=9 is a census not a sample"}
    (OUT / "sample.json").write_text(json.dumps(s, indent=1))
    print(f"corpus/pmc firings at T=4: {len(rows)}")
    print(f"pooled into the batch     : {len(add)} "
          f"({', '.join(a['tag'] for a in add)})")
    print(f"batch total               : {len(s['rows'])}")


if __name__ == "__main__":
    main()
