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
| cost | 1.0× | 0.28× | **0.41× — 2.4× cheaper** |
| vision calls | 1 per page | none | **1 per 3 pages** |
| sees figures | everything | **nothing** | what the extractor missed |

<sub>2,342 PDFs · 20,375 pages · 12 corpora. <code>pdf-inspector only</code> is cheapest because it captures no figure, scan or unparsed table at all — a floor, not an option.</sub>

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
| Drop emblems repeated across *documents* | The GPO seal fired on 227 of 230 US bills — documents with no figures at all |
| Collapse pages with >6 rasters | A 48-tile inpainting figure is one figure; one TI package photo arrives as 12 strips |
| Never cost more than reading everything | On single-page documents the routed set can lose; the guard caps it |
| Ink threshold on the dense-grid branch | Separates a shaded table the extractor missed from decorative banners |

Pages render at the resolution their *own smallest text* needs rather than a
flat dpi, measured from the 5th-percentile font on each page. That alone cut
image tokens 54% with identical content capture.

## Measured on 2,342 PDFs

Twelve corpora, 20,375 pages, chosen to be genuinely different from each other —
electronics datasheets, arXiv and PMC papers, US legislation, and six olmOCR-bench
page classes. Every corpus has a fetch script and a sha256 manifest, so results
pin to exact inputs. Full tables: [`docs/benchmarks/RESULTS.md`](docs/benchmarks/RESULTS.md).

| corpus | files | pages | cheaper than reading every page | calls/page |
|---|---|---|---|---|
| `bills` | 230 | 2,736 | **7.0×** | 0.00 |
| `datasheets` | 204 | 7,641 | **2.9×** | 0.42 |
| `olmocr_arxiv_math` | 522 | 522 | **2.5×** | 0.12 |
| `tds` | 23 | 632 | **2.8×** | 0.40 |
| `olmocr_tables` | 188 | 188 | **2.4×** | 0.45 |
| `olmocr_headers_footers` | 266 | 266 | **2.1×** | 0.50 |
| `arxiv` | 238 | 5,336 | **2.0×** | 0.27 |
| `papers` | 24 | 704 | **1.9×** | 0.39 |
| `olmocr_scans` | 134 | 134 | **1.8×** | 1.00 |
| `olmocr_multi_column` | 231 | 231 | **1.5×** | 0.58 |
| `pmc` | 220 | 1,923 | **1.3×** | 0.56 |
| `olmocr_long_tiny_text` | 62 | 62 | **0.9×** | 1.05 |

**Overall: 2.4× cheaper than reading every page** (48.9M → 20.1M tokens), at one
vision call per three pages instead of one per page.

> [!NOTE]
> `olmocr_long_tiny_text` is the one class where this **loses** — 62 single-page
> documents of very small print, where text plus a figure render costs 7% more
> than simply rendering the page. Single-page documents have nothing to amortise.
> A cost guard caps the damage (it was +61% before), but it does not turn the
> case into a win, and the table says so.

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
> - Thresholds are fitted, not learned: ~21 numbers tuned on a handful of real
>   documents, then exercised for regression across 2,342 more. That exercise
>   found two failures the small set could not — see below — so treat the
>   constants as calibrated to the corpora here, not as universal.
> - **Single-page documents can lose.** Nothing amortises; see `olmocr_long_tiny_text`.
> - **Emblems need a batch.** A publisher mark is only distinguishable from a
>   small chart by recurring across documents — six signals were measured and
>   five rejected ([`eval/tds-corpus.md`](eval/tds-corpus.md)). Convert one
>   government PDF alone and its seal still costs one call.
> - **Branding still costs calls.** Journal mastheads, conference banners, QR
>   codes and cover art fire as figures; in a sampled audit that was 7 of 18
>   raster firings on journal-page corpora. Extending the recurrence rule to
>   individual images was implemented, then reverted — it discarded a reused TI
>   application schematic, so it trades content for cost.
> - A table with **no rules and no shading** is invisible to every branch. If the
>   extractor also drops it, the content is lost silently.
> - `stroke_grid` conflates marker-based plots with ruled tables — one label, two causes.
> - Text quality is bounded by pdf-inspector. If it misreads a page, so does this.
> - Figure description *accuracy* is unmeasured in text-bearing PDFs. No public
>   benchmark scores it; `eval/oldscans.md` is the only place it is measured at all.

## Benchmarks

| Document | What it covers |
|---|---|
| [`docs/benchmarks/RESULTS.md`](docs/benchmarks/RESULTS.md) | **All 12 corpora, 2,342 files, 20,375 pages** |
| [`docs/benchmarks/PLAN.md`](docs/benchmarks/PLAN.md) | How each corpus was chosen, sourced and pinned |
| [`eval/tds-corpus.md`](eval/tds-corpus.md) | 23 datasheets — the original three-way comparison |
| [`eval/datasheets.md`](eval/datasheets.md) | Token model and per-stage wall time |
| [`eval/resolution.md`](eval/resolution.md) | Adaptive resolution and the controlled capture test |
| [`eval/oldscans.md`](eval/oldscans.md) | olmOCR-bench scanned-document accuracy |
| [`eval/opendataloader.md`](eval/opendataloader.md) | Regression gate procedure |

```bash
uv run --with pytest python -m pytest tests/ -q   # splice/strip + cache contracts
python3 tests/check_sync.py                       # verbatim block matches harvest.py
uv run eval/gate.py example/                      # byte-identity, real pipeline
uv run eval/fetch.py bills && uv run eval/bench.py corpus/bills   # any corpus
uv run eval/report.py                             # regenerate RESULTS.md
```

> [!TIP]
> `harvest.py` is the single source of truth for every routing decision, and
> every number in this README is regenerated from it — none is hand-carried. To
> see routing on your own file without converting anything:
> `uv run skills/pdf-extract/harvest.py FILE.pdf`
