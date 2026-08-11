<div align="center">

# doc-extract

**Read documents properly. Fast local text extraction, plus vision only on what text extraction provably missed.**

[![CI](https://github.com/LPSlv/doc-extract/actions/workflows/ci.yml/badge.svg)](https://github.com/LPSlv/doc-extract/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-black.svg)](LICENSE)
[![Agent skill](https://img.shields.io/badge/agent-skill-b3261e.svg)](https://skills.sh/)

</div>

Text extraction handles most documents on its own — and silently drops every
chart, pinout diagram, scanned page and merged-header table. Looking at every
page instead catches all of it, and costs 2.4× more.

`doc-extract` does neither. It extracts text with [pdf-inspector](https://github.com/firecrawl/pdf-inspector)
and [anydoc](https://github.com/firecrawl/anydoc), works out which pages the
extractor actually failed on, and sends only those to your agent's eyes.

Reads **PDF, Word, Excel, PowerPoint and images**. No API key, no per-page bill,
no upload — the vision is the subscription you already pay for.

| across 2,342 PDFs, 20,375 pages | read every page | text only | **doc-extract** |
|---|--:|--:|--:|
| input tokens | 48.9M | 13.6M | **20.1M** |
| vision calls per page | 1.00 | 0 | **0.34** |
| figures it can see | all | **none** | the ones text missed |

<sub>Text alone is cheapest because it is blind — a floor, not an option. Once
converted, follow-up questions read the cached text and cost 99% less again.</sub>

## Quick start

```bash
npx skills add LPSlv/doc-extract@doc-extract
```

Then ask your agent: *"read this datasheet and tell me the Q3 variance."*
Or point it at a folder of mixed `.pdf`, `.docx`, `.xlsx` and `.pptx`.

Requires [`uv`](https://docs.astral.sh/uv/). No API key, no Rust toolchain, no
global installs — dependencies resolve on first run.

### Try it without installing

```bash
git clone https://github.com/LPSlv/doc-extract && cd doc-extract
uv run skills/doc-extract/convert.py example/sample-report.pdf
```

```json
{"status":"ok","artifact":"~/.cache/doc-extract/d2176c41…","cached":false,
 "pending":[{"id":"p001-x38","page":1,"kind":"raster","reason":"standalone_raster",
             "path":"…/images/p001-x38.png"}],
 "dropped":0,"over_scale_guard":false,"scale_guard":15}
```

All the text is already extracted — including the budget table, as real Markdown.
Exactly one item needs eyes. The finished output is committed at
[`example/sample-report.expected.md`](example/sample-report.expected.md), so you
can see what you get before installing anything.

### What the one vision call buys

Ask *"how big is the Q4 gap?"* of that page:

| text extraction alone | with doc-extract |
|---|---|
| `***Figure 1: spend against plan***` <br><br> `Actual spend tracked plan closely` <br> `through Q2 but diverged in Q3 as` <br> `equipment procurement slipped.` | `**[p1] p001-x38** — Line chart, two series.` <br> `X: Quarter 2026 (Q1–Q4). Y: Spend (k EUR).` <br> `Planned: Q1 12, Q2 19, Q3 24, Q4 31.` <br> `Actual: Q1 11, Q2 17, Q3 18, Q4 22.` <br> `…the Q4 gap is about 9k EUR.` |
| **no answer** — the chart is a vector drawing, so there is nothing to extract | **≈ 9k EUR**, with a `[p1]` citation |

The text path is untouched: strip the added block and you get pdf-inspector's
output back byte for byte. The visual layer only ever adds.

## How it works

```
file ──► classify ──► extract text ─────► route visuals ──► agent looks ──► answer
         by content   pdf-inspector/      the interesting   describe.py    [p12]
         10-50 ms     anydoc              part                             citations
```

### 1. Convert

Everything deterministic happens in one command:

```bash
uv run skills/doc-extract/convert.py FILE [MORE ...]
```

Prints one JSON object per document. Exit code is non-zero if any document
failed, and a bad file never aborts the batch. Re-running returns
`cached: true` instantly and costs nothing.

### 2. Describe

For each entry in `pending`, read the image file and write back what you saw:

```bash
uv run skills/doc-extract/describe.py <artifact> <id> "Line chart, two series…"
uv run skills/doc-extract/describe.py <artifact> <id> -   # long text from stdin
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
~/.cache/doc-extract/<sha256>-<engine+schema>/
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

## Extracting the images does not give you the figures

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
| Twelve signals tried for branding, one kept | Mastheads and logos are separable from charts only by reading them ([`eval/tds-corpus.md`](eval/tds-corpus.md)) |
| Ink threshold on the dense-grid branch | Separates a shaded table the extractor missed from decorative banners |

Pages render at the resolution their *own smallest text* needs rather than a
flat dpi, measured from the 5th-percentile font on each page. That alone cut
image tokens 54% with identical content capture.

## Reading 20,375 pages costs 2.4× less than looking at them

Twelve corpora, chosen to be unlike each other: electronics datasheets, arXiv and
PMC papers, US legislation, and six olmOCR-bench page classes. Each has a fetch
script and a sha256 manifest, so a result pins to exact inputs.
Full tables: [`docs/benchmarks/RESULTS.md`](docs/benchmarks/RESULTS.md).

<!-- benchmarks:begin -->
Reading every page of these 2,342 PDFs costs 48.9M input tokens. doc-extract reads the same 20,375 pages for 20.1M — **2.4× less** — because it looks at one page in three (6,834 vision calls over 20,375 pages) instead of all of them.

Extracting text alone is cheaper still, at 13.6M, and captures no figure, scan or unparsed table whatsoever. It is the floor, not an option.

| corpus | files | pages | cheaper by | vision calls per page |
|---|--:|--:|--:|--:|
| `bills` | 230 | 2,736 | **7.0×** | 0.00 |
| `datasheets` | 204 | 7,641 | 2.9× | 0.42 |
| `tds` | 23 | 632 | 2.8× | 0.40 |
| `olmocr_arxiv_math` | 522 | 522 | 2.5× | 0.12 |
| `olmocr_tables` | 188 | 188 | 2.4× | 0.45 |
| `olmocr_headers_footers` | 266 | 266 | 2.1× | 0.50 |
| `arxiv` | 238 | 5,336 | 2.0× | 0.27 |
| `papers` | 24 | 704 | 1.9× | 0.39 |
| `olmocr_scans` | 134 | 134 | 1.8× | 1.00 |
| `olmocr_multi_column` | 231 | 231 | 1.5× | 0.58 |
| `pmc` | 220 | 1,923 | 1.3× | 0.56 |
| `olmocr_long_tiny_text` | 62 | 62 | 0.9× | 1.05 |

`olmocr_long_tiny_text` sits last because it **loses**: 62 single-page documents where text plus one figure render costs more than the page itself. Single pages have nothing to amortise. It stays in the table.
<!-- benchmarks:end -->

## On scans it recovers what text extraction cannot reach

pdf-inspector extracts **zero characters** from these pages. The vision pass recovers most of the content:

| olmOCR-bench `old_scans` | pdf-inspector | doc-extract |
|---|---|---|
| `present` — is the text there? | 0.0% | **61.5%** |
| `order` — correct reading order? | 0.0% | **59.4%** |
| overall | 18.4% | **60.9%** |

<sub>n=11 documents, 87 tests. The baseline's 18.4% is hollow — it passes <code>absent</code> tests by producing nothing at all.</sub>

### On native-text PDFs it changes nothing, deliberately

Through opendataloader-bench's official evaluator it scores **0.875 overall /
0.915 NID / 0.814 TEDS** — identical to the engine it delegates to, because the
text path is byte-identical and every addition is strippable.

> [!NOTE]
> That 0.875 is pdf-inspector's number, not an improvement. Against the
> benchmark's *full* engine set it ranks 5th of 15 — `opendataloader-hybrid`
> 0.907, `nutrient` 0.885 and `docling` 0.882 all score higher. The equality is
> enforced, not asserted: `eval/gate.py` runs the real pipeline and requires the
> stripped output to equal raw engine output byte for byte.

### Only the first question pays

The artifact is cached, so follow-ups read text instead of pixels.

![Cumulative tokens across repeated questions](docs/img/datasheet-cost.svg)

## On figures, a description recovers what rendering the page recovers

Cost is easy to measure and easy to game. The claim that matters is whether the
description actually carries the figure's content — so it is now measured, on
questions built so that **only** the visual can answer them.

| 12 visual-only questions | correct |
|---|--:|
| no document at all | 0/12 |
| text extraction only | 0/12 |
| **doc-extract** | **12/12** |
| read the whole page | **12/12** |

Questions are admitted by a gate, not by judgement: a candidate survives only if
reading the page answers it (ground truth is sound), a closed-book agent fails
it under **two** option orderings (it isn't reachable by convention), and a
text-only agent cannot ground it in the markdown. 30 candidates in, 12 out,
none lost to a bad answer key. Four agents ran the arms, none of them able to
see the ground truth or each other.

Text extraction's raw score on the same set is 7/12, and all of it is guessing:
eleven of its twelve answers were ungrounded, and the one it claimed to ground
was wrong. On Fig. 4 of one paper it is worse than blind — the markdown gives
526 nm for curve *a* and nothing for curve *b*, walking a text-only reader
straight into the wrong answer, while the description carries curve *b*'s own
530 nm.

> [!NOTE]
> This says the routing loses nothing **on pages it selects**. It says nothing
> about pages it skips, and for most of these figures the routed item is a
> whole-page render — so on that page doc-extract and full optical are looking
> at much the same thing. The 2.4× comes from the two-thirds of pages never
> rendered, and the price of that is in Limitations.
> Method, per-question results and the two artifacts that nearly broke it:
> [`eval/figqa.md`](eval/figqa.md).

## On Office documents the routing barely helps, and the numbers say so

Word, Excel and PowerPoint go through [anydoc](https://github.com/firecrawl/anydoc)
for text and through the same furniture filters, citation contract, cache and
describe rubric as PDFs. Measured on 236 government and NASA documents
(govdocs1 and NTRS, pinned in `eval/manifests/office.urls.tsv`):

<!-- office:begin -->
Across 236 documents (1,335 units), the filters cut 1,647 embedded images down to **1,316** worth looking at — 0.986 vision calls per unit. 19 spreadsheet charts were recovered as exact tables at no vision cost at all.

| format | files | units | images found | sent to vision | calls per unit |
|---|--:|--:|--:|--:|--:|
| Word (headings) | 162 | 484 | 415 | 331 | 0.684 |
| Excel (sheets) | 35 | 77 | 26 | 1 | 0.013 |
| PowerPoint (slides) | 39 | 774 | 1,206 | 984 | 1.271 |

<sub>Baseline is describe every extracted asset, before furniture filters and dedup — not a page render, which Office documents do not have. Residue, counted not hidden: 1 chart unreadable, 108 assets in formats no agent can view.</sub>
<!-- office:end -->

**The 2.4× does not transfer, and it was never going to.** PDF routing wins by
avoiding page renders — the expensive baseline it beats is looking at every
page optically. An Office document has no render to avoid, so the only lever
left is filtering embedded images, and most embedded images in a real deck are
content. The filters drop a fifth of the assets but under two percent of the
tokens, because what they catch is small by definition: logos, icons, rules.

So a slide deck costs roughly one vision call per slide. A 79-slide NASA deck
is 86 calls, and `over_scale_guard` will fire and ask you first. That is the
honest shape of it.

What Office documents genuinely gain:

| | |
|---|---|
| **Spreadsheet charts** | Read from the chart definition — **exact numbers, zero vision calls**. 19 of 20 recovered across 35 workbooks |
| Citations and cache | `[s07]`, `[Sheet2]`, `[Budget assumptions]`; follow-up questions read text, not pixels |
| Byte-identity | Stripped output equals raw anydoc output, enforced by `eval/gate.py` on every format |
| No per-page bill | The vision is your own agent's, not a metered service |

Excel is the outlier that pays: anydoc's spreadsheet path is pure cell
extraction, returning zero assets and no chart for a workbook that plainly
contains both, so everything visual there is recovered here or nowhere. It
reads Word and PowerPoint charts perfectly well, and those are left alone —
extracting them twice was the largest error caught during design.

## Not a reimplementation of Firecrawl Parse

Firecrawl's hosted Parse routes on the same open-source `pdf-inspector`
classifier this skill already calls, and bills 1 credit per page whether or not
a page needed OCR. Two differences matter:

- **It routes on text presence alone.** A chart on a page full of text passes
  straight through as text, and the figure is gone. This skill also routes on
  vector geometry, which is what catches those.
- **The vision is yours.** Parse's OCR layer is [GLM-OCR](https://github.com/THUDM), MIT-licensed and
  not Firecrawl's own model, served on their GPUs and billed per page. Here it
  is the agent's own eyes, inside the seat you already pay for.

Selective routing is what makes that practical rather than merely possible: at
1.00 vision calls per page a subscription-funded agent exhausts its budget on
the first document; at the measured 0.34 it does not.

> [!IMPORTANT]
> This is a billing-model comparison, not a quality one. Parse's OCR on a
> scanned page may well read better than a general agent's — that is unmeasured
> here and is not claimed either way.

## Limitations

> [!WARNING]
> - Thresholds are fitted, not learned: ~21 numbers tuned on a handful of real
>   documents, then exercised for regression across 2,342 more. That exercise
>   found two failures the small set could not — see below — so treat the
>   constants as calibrated to the corpora here, not as universal.
> - **Single-page documents can lose.** Nothing amortises; see `olmocr_long_tiny_text`.
> - **Emblems need a batch.** A publisher mark is only distinguishable from a
>   small chart by recurring across documents — twelve signals were measured and
>   eleven rejected ([`eval/tds-corpus.md`](eval/tds-corpus.md)). Convert one
>   government PDF alone and its seal still costs one call.
> - **Branding still costs calls, and zero false positives is not reachable.**
>   Journal mastheads, society logos, conference banners and cover art fire as
>   figures. On a 382-item labelled set ([`tests/raster-labels.tsv`](tests/raster-labels.tsv),
>   every raster firing across four journal corpora, classified by eye) that is
>   **49 cases — 12.8% of raster firings, 3.4% of vision calls, 2.8% of raster
>   tokens**. Twelve signals have been measured and none removes them safely:
>   branding is separable from a figure only by reading what it says, which is
>   the call being avoided. The two best candidates were flawless on the set they
>   were fitted to and then lost real content on the corpora they had not seen —
>   a top-of-page rule dropped a tile of arXiv 2607.29107 Figure 1, and a QR
>   detector dropped robot-manipulation photographs. Cheap handling, not
>   detection, is the mitigation: a branding image costs a median 140 tokens
>   against 878 for a figure, and the describe rubric dismisses one in a line.
> - **Two routed pages in five have nothing on them.** On 30 routed pages
>   sampled one-per-document across arxiv, pmc, datasheets and papers, 11 carry
>   no figure at all — mastheads, references pages, plain prose, an ESD icon, a
>   QR box — and one more duplicates a table the extractor already recovered.
>   `stroke_grid` was wrong on all 3 of its firings there; `standalone_raster`
>   on none of 6. Those calls are wasted, and they are inside the 0.34
>   calls-per-page figure above, not additional to it.
> - **A raster can hide the figure next to it.** When a page holds both an
>   embedded bitmap and vector artwork, firing `standalone_raster` emits the
>   bitmap and suppresses the page render — so the vector figure is never seen.
>   Measured once directly: a 519×457 fluorescence inset was routed while the
>   optical-setup schematic around it was skipped entirely.
> - A table with **no rules and no shading** is invisible to every branch. If the
>   extractor also drops it, the content is lost silently.
> - `stroke_grid` conflates marker-based plots with ruled tables — one label, two causes.
> - Text quality is bounded by pdf-inspector. If it misreads a page, so does this.
> - Figure-description accuracy rests on **12 questions from 8 figures** — enough
>   to separate a working visual layer from an absent one, not enough to
>   separate a good one from a better one. No public benchmark scores this task,
>   so the set is built here and its construction is the thing to audit
>   ([`eval/figqa.md`](eval/figqa.md)).
> - **On Office documents the routing saves very little.** 1.9% of vision
>   tokens across the 236-document corpus, against 2.4× on PDFs. There is no
>   page render to avoid, so the only lever is filtering embedded images, and
>   most of those are content. Slide decks cost more than one call per slide.
>   The cache, citations and chart extraction are the reasons to use it there —
>   not the routing.
> - **Office figure counts come from one corpus.** 236 government and NASA
>   documents, skewed to what those bodies publish. A corporate deck template
>   with a logo on every master would behave differently, and inherited
>   furniture is invisible to the text engine entirely, so the ubiquity filter
>   has less to catch than it does on PDFs.
> - **EMF, WMF and embedded OLE objects cannot be read.** The text engine
>   retains them faithfully and there is no rasterizer here, so they are dropped
>   and counted rather than sent to an agent that cannot open them. Pasted Excel
>   charts and clipart in older decks are frequently EMF, so on legacy documents
>   this content is neither extracted nor viewable. Frequency unmeasured.
> - **Spreadsheet charts can be unreadable.** Scatter and bubble series use a
>   different XML shape than the extractor reads, and a chart referencing an
>   external workbook resolves to nothing. An OOXML chart has no rendered image,
>   so unlike a PDF figure there is no vision fallback — the content is simply
>   unavailable. Counted in `dropped` as `native_chart_unread`.
> - **Word citations need Word headings.** A contract written as numbered prose
>   rather than Heading styles yields one whole-document unit, so `pages/` greps
>   degrade to reading everything.

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
| [`tests/raster-labels.tsv`](tests/raster-labels.tsv) | 382 raster firings labelled by eye — content, branding or portrait |
| [`docs/benchmarks/results/office.json`](docs/benchmarks/results/office.json) | **236 Office documents** — govdocs1 and NASA NTRS, per-file rows |

```bash
uv run --with pytest --with firecrawl-anydoc==0.1.6 \
  python -m pytest tests/ -q                      # splice/strip, cache, anydoc invariants
python3 tests/check_sync.py                       # verbatim block matches harvest.py
uv run eval/gate.py example/                      # byte-identity, real pipeline
uv run eval/fetch.py bills && uv run eval/bench.py corpus/bills   # any PDF corpus
uv run eval/fetch.py office && uv run eval/office_bench.py corpus/office
uv run eval/report.py                             # regenerate RESULTS.md
python3 eval/readme_tables.py --write             # regenerate this README's tables
```

> [!TIP]
> `harvest.py` is the single source of truth for every routing decision, and
> every number in this README is regenerated from it — none is hand-carried. To
> see routing on your own file without converting anything:
> `uv run skills/doc-extract/harvest.py FILE.pdf`
