# pdf-extract

An agent skill for reading PDFs properly: fast local text extraction, plus
vision **only** on the parts text extraction provably missed — charts, scanned
pages, and tables it failed to structure.

```bash
npx skills add LPSlv/pdf-extract@pdf-extract
```

Requires [`uv`](https://docs.astral.sh/uv/). Nothing else — no API key, no Rust
toolchain, no global installs. Dependencies resolve on first run.

## The problem

"Extract the images from a PDF" is a well-defined operation that every tool
performs correctly, and it does not do what people expect.

![Filter cascade: 69 image placements reduce to 1 worth reading](docs/img/filter-cascade.svg)

A PDF page is a program of drawing commands. Only *image XObjects* are stored
bitmaps; a chart pasted from Excel is a few hundred rectangle-and-line
operations with no image object to extract. On one ESA BIC funding document,
naive extraction yields 69 images — 7 distinct objects, six of them logos, rules
and a sidebar stripe. Meanwhile a sibling document returns **zero** images while
containing several pages of drawn content.

So both mechanisms are needed, and both need filtering.

## What it does

1. **Classify** the PDF (~10–50 ms) — text-based, scanned, image-based or mixed.
2. **Extract** authoritative Markdown with [pdf-inspector](https://github.com/firecrawl/pdf-inspector).
3. **Harvest** visuals: pull embedded images, drop furniture, detect pages whose
   drawn content the extractor did not capture, render those.
4. **Read** each survivor with the host agent's own vision — no separate API.
5. **Answer** questions against the cached artifact with `[p12]` citations.

Everything through step 3 is deterministic and free.

![Vision calls before and after filtering, five documents](docs/img/vision-calls.svg)

## Benchmark

The text path is delegated entirely to pdf-inspector, and everything this skill
adds sits inside strippable delimiters. The gate strips them and asserts the
residue is **byte-identical** to raw engine output — so the score below is
inherited, and verified rather than assumed.

![Engine scores on opendataloader-bench across three metrics](docs/img/benchmark.svg)

**0.875 overall on opendataloader-bench** (200 PDFs), the top score in
Firecrawl's published comparison against LiteParse, OpenDataLoader, PyMuPDF4LLM
and MarkItDown.

This is not a claim that pdf-extract's own extraction beats anything. It is a
claim that it does not degrade a strong engine while adding a visual layer —
and that claim is enforced by a test that can fail.

Across the same 200 PDFs the visual layer costs **0.66 vision calls per
document**: 95 of 200 need none at all.

## What no benchmark measures

opendataloader-bench, olmOCR-bench and OmniDocBench all score text fidelity —
reading order, tables, headings. None scores whether a chart was understood.
The feature this skill exists for is unmeasured by the available instruments,
which is stated plainly rather than papered over.

The one place it can be shown: olmOCR-bench's `old_scans` (134 PDFs). Every
sampled file classifies `scanned` with **zero extractable characters** —
pdf-inspector alone scores ~0. Rendering and reading recovers them, including
handwritten cursive that Tesseract also fails.

## Known limitations

- Thresholds are fitted to a small sample: nine numbers tuned on five real
  documents plus ~20 synthetic controls, then exercised for regression across
  200 more.
- A table with no rules and no shading is invisible to every branch. If the
  extractor also drops it, the content is lost silently.
- `stroke_grid` conflates marker-based plots with ruled tables. One label, two
  causes — deliberate, but it makes that manifest `reason` less diagnostic.
- Text quality is bounded by pdf-inspector. If it misreads a page, so does this.

## Development

```bash
uv run --with pytest python -m pytest tests/ -q   # splice/strip and cache contracts
python3 tests/check_sync.py                       # verbatim block matches harvest.py
uv run skills/pdf-extract/harvest.py FILE.pdf     # routing decisions for one file
```

`harvest.py` is the single source of truth for routing. Every number in this
README and in `docs/superpowers/specs/` is regenerated from it; none is
hand-carried.

## Licence

MIT.
