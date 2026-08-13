# Draft 3 — r/LocalLLaMA

**Status: DRAFT. Not posted.**

**Venue:** r/LocalLLaMA, self-post (text post, not a link post — the subreddit
treats bare GitHub links as promo). Markdown renders. Flair: `Resources` if
available, otherwise `Tutorial | Guide`.

**Title:**

```
I labelled every firing of my PDF router by hand and 42% of them were waste. Here's the tool and all the evals that failed.
```

*(122 chars; Reddit's limit is 300.)*

---

## Body

Posting the negative results first because they are the only part of this that
is unusual.

**The weakest branch of my router is 42% waste and I can prove it.** It fires
when a page has axis-aligned strokes in both orientations, on the theory that
that means a ruled table or a marker-based plot. I rendered all 170 firings
across 711 documents at 130 dpi and had six labellers classify every one, each
told to break ties *in the branch's favour*:

| label | n | share |
|---|--:|--:|
| ruled table the extractor missed | 64 | 37.6% |
| marker/tick-based plot | 10 | 5.9% |
| some other real figure | 24 | 14.1% |
| **nothing at all** | **72** | **42.4%** |

The branch's second stated purpose — plots — is 10 firings in 170. Whatever
that branch is worth, it is worth it as a table-catcher, and the README says so
instead of quoting the 58% hit rate.

**Twelve signals were measured to fix the branding false positives. One
shipped.** The two best candidates were flawless on the 382-item set they were
fitted to and then lost real content on corpora they had not seen. One was a
QR-code detector that selected 5 of 5 QR codes and nothing else across 1,524
raster firings; it shipped, and was reverted when the before/after diff showed
two arXiv documents going *up* in cost — the rule had matched 19 more images the
audit never saw, because page renders had subsumed them, and dropping them broke
a grid-collapse threshold. The general result is that a masthead is separable
from a chart only by reading it, and reading it is exactly the call being
avoided.

**Six of the nine defects I found were in the measurement code, not the tool.**
An answer key with the correct option at C fourteen times in thirty. A scorer
reading the wrong column, reporting 0% precision on a set that was unanimously
clean. A harness that withheld a whole page render from the arm under test and
then counted its absence against the router — that one cost me a published
22/23 that I had already written up as 20/23 and blamed on routing.

---

## What the thing actually is

Text extraction handles most documents and silently drops every chart, pinout
diagram, scanned page and merged-header table. Feeding every page to a VLM
catches all of it and costs 3.6x more.

This is an agent skill that does neither. It extracts text locally with
`pdf-inspector` and `anydoc` (both Rust, MIT, no OCR, no network), works out
which pages the extractor provably failed on by reading the page's drawing
operators, and routes **only those** to whatever vision model is running the
agent. Reads PDF, Word, Excel, PowerPoint and images.

The relevant part for this sub: **there is no OCR API in the loop and nothing is
uploaded.** The vision call goes to whatever model your agent already runs. If
that is a local VLM behind a skills-capable harness, the entire pipeline is
local. Text extraction, routing, rendering and caching are all deterministic
local CPU — the only model call in the whole design is the description of a
routed image.

```bash
git clone https://github.com/LPSlv/doc-extract && cd doc-extract
uv run skills/doc-extract/convert.py example/sample-report.pdf
```

That prints one JSON object with the artifact path and a `pending` list of what
needs eyes. Nothing else in the pipeline touches a model.

## The cost numbers, and their caveats

2,342 PDFs / 20,375 pages, twelve corpora picked to be unlike each other —
electronics datasheets, arXiv, PMC, US legislation, six olmOCR-bench page
classes:

| | input tokens |
|---|--:|
| read every page optically | 48.9M |
| text only (blind) | 13.6M |
| **routed** | **20.1M** |

2.4x cheaper than reading everything, at 0.33 vision calls per page. Per corpus
it ranges from 7.0x (US bills — almost no figures, and the GPO seal is filtered
as a cross-document emblem) down to **0.9x on 62 single-page documents, where it
loses.** That row stays in the table in sort position rather than in a footnote.

Caveats that matter if you are going to reproduce this:

- **The token model is Anthropic's image rule** — `(w × h) / 750` after fitting
  the long edge to 1568 px, computed from the actual rendered pixels — and text
  at `chars / 3.5`. If you are costing this against a Qwen-VL or an InternVL
  tokenizer the absolute numbers will not transfer. The *ratio* is mostly a
  function of how many pages get looked at, which is model-independent.
- **The published token figures are about 0.6% low on rasters**, for a
  documented reason: the cost model prices a raster at its native xref
  dimensions while the renderer scales isotropically from the placement, so an
  anisotropic placement ships larger than predicted. Measured over 892 routed
  rasters; per item the disagreement reaches 58%. It is written up and
  deliberately not fixed, because fixing it costs ~40 ms per document. Do not
  quote these numbers to three significant figures; the underlying model does
  not support it.
- **Thresholds are fitted, not learned.** About 21 constants tuned on a handful
  of real documents, then exercised across 2,342 more. Treat them as calibrated
  to these corpora.

## Reproducibility

Everything is a script, and the README's cost tables are regenerated from raw
JSON rather than hand-typed:

```bash
uv run eval/fetch.py bills && uv run eval/bench.py corpus/bills
uv run eval/report.py                  # regenerate RESULTS.md
python3 eval/readme_tables.py --write  # regenerate the README tables
uv run eval/gate.py example/           # byte-identity, real pipeline
```

**Pinning is uneven and it is documented as uneven.** The six olmOCR corpora
and the arXiv holdout are sha256-pinned per file, so those reproduce exactly.
`arxiv`, `bills`, `datasheets` and `pmc` ship URLs without hashes, and `papers`
has no manifest at all — re-fetching those may not give you byte-identical
inputs.

The one routing rule I shipped this month was validated the way I think these
things should be: 348 arXiv papers fetched *after* the rule was designed,
sha256-pinned, disjoint from the design corpus by content hash, every drop
labelled blind by three independent labellers who saw the PNG and nothing else —
not the rule, not the hypothesis, not which answer would be convenient. 17
effective drops, 17 correct, and the write-up leads with the one failure mode it
has (a booktabs table continued across pages looks exactly like a template) plus
the fact that the 18th drop was found by diffing the implementation against the
analysis script, not by the script.

## Does the description actually carry the figure?

No public benchmark scores this, so there is a hand-built one: 40 questions
built so only the visual can answer them, admitted only if the full-page-render
arm gets it right, a closed-book arm gets it wrong under **two** option
orderings, and a text-only arm cannot ground it in the markdown. 23 admitted;
routed descriptions answered 22.

Read that with the discount attached: three of the four arms are *forced* by the
admission rule, so only the routed arm measures anything. It is 23 questions
from 16 pages. That separates a working visual layer from an absent one and
cannot separate a good one from a better one.

On scanned pages, where the extractor returns zero characters, it goes 0% →
61.5% on olmOCR-bench `old_scans` presence tests (n=11 documents).

## Where it does not help

Office documents. The routing saves **1.9%** of vision tokens across a
236-document corpus, against 2.4x on PDFs, and the README says that in the
heading rather than the footnotes. There is no page render to avoid, so the only
lever is filtering embedded images, and most embedded images in a real deck are
content. A slide deck costs roughly one vision call per slide. Spreadsheet
charts are the exception that genuinely pays — they are read from the chart XML
as exact numbers at zero vision cost, 19 of 20 recovered across 35 workbooks.

MIT. https://github.com/LPSlv/doc-extract

If anyone has a boilerplate-heavy holdout corpus — vendor datasheets or journal
PDFs, a few hundred files — I would like one. Half the routing waste is Würth
title blocks and Nexperia legal pages, there is no working rule for it, and I
could not find a corpus to validate a candidate against without fitting it on
the set I would then score it on.
