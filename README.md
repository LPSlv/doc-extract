<div align="center">

# pdf-extract

**Read PDFs properly. Fast local text extraction, plus vision only on what text extraction provably missed.**

[![CI](https://github.com/LPSlv/pdf-extract/actions/workflows/ci.yml/badge.svg)](https://github.com/LPSlv/pdf-extract/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-black.svg)](LICENSE)
[![Agent skill](https://img.shields.io/badge/agent-skill-b3261e.svg)](https://skills.sh/)

</div>

Text extraction handles most PDFs on its own — and silently drops every chart,
pinout diagram, scanned page and merged-header table. Reading every page as an
image catches all of it and costs 20× more.

`pdf-extract` does neither. It extracts text with [pdf-inspector](https://github.com/firecrawl/pdf-inspector),
works out which pages the extractor actually failed on, and sends only those to
your agent's eyes.

| | read every page | pdf-inspector only | **pdf-extract** |
|---|---|---|---|
| input tokens | 1,513,884 | 282,933 | **549,176** |
| figure content | everything | **none** | 279 figures |
| local time | 6.0 s | 4.2 s | **5.3 s** |

<sub>23 datasheets, 632 pages. <code>pdf-inspector only</code> is cheapest because it captures no figures at all.</sub>

## Quick start

```bash
npx skills add LPSlv/pdf-extract@pdf-extract
```

Then ask your agent: *"read this datasheet and tell me the Q3 variance."*

Requires [`uv`](https://docs.astral.sh/uv/). No API key, no Rust toolchain, no
global installs — dependencies resolve on first run.

### Try it without installing

```bash
git clone https://github.com/LPSlv/pdf-extract && cd pdf-extract
uv run skills/pdf-extract/convert.py example/sample-report.pdf
```

```json
{"status":"ok","artifact":"~/.cache/pdf-inspect/0559ee3a…","cached":false,
 "pending":[{"id":"p001-x5","page":1,"kind":"raster","reason":"standalone_raster",
             "path":"…/images/p001-x5.png"}],
 "dropped":0,"over_scale_guard":false,"scale_guard":15}
```

All the text is already extracted — including the budget table, as real Markdown.
Exactly one item needs eyes. The finished output is committed at
[`example/sample-report.expected.md`](example/sample-report.expected.md), so you
can see what you get before installing anything.

## How it works

```
PDF ──► classify ──► extract text ──► route visuals ──► agent looks ──► answer
        10-50 ms     pdf-inspector    the interesting   describe.py     [p12]
                                      part                              citations
```

### 1. Convert

Everything deterministic happens in one command:

```bash
uv run skills/pdf-extract/convert.py FILE.pdf [MORE.pdf ...]
```

Prints one JSON object per document. Exit code is non-zero if any document
failed, and a bad file never aborts the batch. Re-running returns
`cached: true` instantly and costs nothing.

### 2. Describe

For each entry in `pending`, read the image file and write back what you saw:

```bash
uv run skills/pdf-extract/describe.py <artifact> <id> "Line chart, two series…"
uv run skills/pdf-extract/describe.py <artifact> <id> -   # long text from stdin
```

Safe to re-run — it replaces rather than duplicates, so a vision pass that dies
halfway just resumes. What to write depends on `reason`:

| `reason` | Write |
|---|---|
| `standalone_raster`, `curves`, `diagonals` | The figure: type, axes and units, notable values, all legible text |
| `no_text_layer` | A **verbatim transcription** — this is the OCR path |
| `dense_grid`, `stroke_grid` | The table, reproduced as Markdown |

### 3. Answer

Read `doc.md` for the whole document, or grep `pages/pNNN.md` and read only the
pages a question touches. Cite as `[p12]`, or `[report.pdf:p12]` across documents.

### Artifact layout

```
~/.cache/pdf-inspect/<sha256>-<engine+schema>/
  source.json     provenance and status
  doc.md          authoritative text, plus delimited descriptions
  pages/p001.md   per-page text, for citation and cheap answering
  images/*.png    extracted rasters and rendered pages
  manifest.json   every kept item, and everything dropped with its reason
```

> [!IMPORTANT]
> Never edit `doc.md` by hand. Everything you add goes through `describe.py`,
> which wraps it in strippable delimiters. That is what lets the benchmark strip
> the additions and prove the skill does not degrade text extraction.

## Why it only looks at some pages

"Extract the images from a PDF" is a well-defined operation that every tool
performs correctly, and it does not do what people expect.

![Filter cascade: 69 image placements reduce to 1 worth reading](docs/img/filter-cascade.svg)

A PDF page is a program of drawing commands. Only *image XObjects* are stored
bitmaps — a chart pasted from Excel is a few hundred rectangle-and-line
operations with no image object to extract. One 14-page grant document yields 69
"images", of which 7 are distinct and 6 are logos and rules. A sibling document
returns **zero** images while containing pages of drawn content.

So both mechanisms are needed, and both need filtering. Every filter exists
because the obvious alternative was tested and failed on a real document:

| Filter | Why it exists |
|---|---|
| Drop images on >50% of pages, <120 px, aspect >8:1 | 69 placements collapse to 1 real graphic |
| Skip pages that already yielded a Markdown table | The extractor beats vision on tables it can parse |
| Require strokes in **both** orientations | Underlines are horizontal only; counting all strokes fired on bibliography pages |
| Stroke-area floor on curves and diagonals | A vendor logo is bézier artwork too — 4N25's only call was its legal disclaimer |
| Drop repeated vector signatures | `ti_ucc27517` carries the same 143-curve logo on six pages |
| Ink threshold on the dense-grid branch | Separates a shaded table the extractor missed from decorative banners |

Pages render at the resolution their *own smallest text* needs rather than a
flat dpi, measured from the 5th-percentile font on each page. That alone cut
image tokens 54% with identical content capture.

## Where it wins, and where it does not

**Scanned documents.** pdf-inspector extracts zero characters; this recovers most of it.

| olmOCR-bench `old_scans` | pdf-inspector | pdf-extract |
|---|---|---|
| `present` — is the text there? | 0.0% | **61.5%** |
| `order` — correct reading order? | 0.0% | **59.4%** |
| overall | 18.4% | **60.9%** |

<sub>n=11 documents, 87 tests. The baseline's 18.4% is hollow — it passes <code>absent</code> tests by producing nothing at all.</sub>

**Native-text PDFs.** It scores exactly what pdf-inspector scores, by design.
Through opendataloader-bench's official evaluator: **0.875 overall / 0.915 NID /
0.814 TEDS**, identical to the engine it delegates to.

> [!NOTE]
> That 0.875 is pdf-inspector's number, not an improvement. Against the
> benchmark's *full* engine set it ranks 5th of 15 — `opendataloader-hybrid`
> 0.907, `nutrient` 0.885 and `docling` 0.882 all score higher. The equality is
> enforced, not asserted: `eval/gate.py` runs the real pipeline and requires the
> stripped output to equal raw engine output byte for byte.

**Repeated questions.** The artifact is cached, so only the first one pays.

![Cumulative tokens across repeated questions](docs/img/datasheet-cost.svg)

## Limitations

> [!WARNING]
> - Thresholds are fitted, not learned: ~21 numbers tuned on five real documents
>   plus synthetic controls, then exercised for regression across 200 more.
> - A table with **no rules and no shading** is invisible to every branch. If the
>   extractor also drops it, the content is lost silently.
> - `stroke_grid` conflates marker-based plots with ruled tables — one label, two causes.
> - Text quality is bounded by pdf-inspector. If it misreads a page, so does this.
> - Figure description *accuracy* is unmeasured in text-bearing PDFs. No public
>   benchmark scores it; `eval/oldscans.md` is the only place it is measured at all.

## Benchmarks

| Document | What it covers |
|---|---|
| [`eval/tds-corpus.md`](eval/tds-corpus.md) | 23 datasheets, 632 pages — three-way cost comparison |
| [`eval/datasheets.md`](eval/datasheets.md) | Token model and per-stage wall time |
| [`eval/resolution.md`](eval/resolution.md) | Adaptive resolution and the controlled capture test |
| [`eval/oldscans.md`](eval/oldscans.md) | olmOCR-bench scanned-document accuracy |
| [`eval/opendataloader.md`](eval/opendataloader.md) | Regression gate procedure |

```bash
uv run --with pytest python -m pytest tests/ -q   # splice/strip + cache contracts
python3 tests/check_sync.py                       # verbatim block matches harvest.py
uv run eval/gate.py example/                      # byte-identity, real pipeline
uv run eval/tds-bench.py corpus/tds               # three-way cost benchmark
```

> [!TIP]
> `harvest.py` is the single source of truth for every routing decision, and
> every number in this README is regenerated from it — none is hand-carried. To
> see routing on your own file without converting anything:
> `uv run skills/pdf-extract/harvest.py FILE.pdf`
