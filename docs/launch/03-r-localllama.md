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

That 42% is the branch as measured, before I did anything about it. One rule since
shipped against it, and over all 188 labelled firings it cuts 52 and costs 3 real
items — so the residual waste is lower than the headline, and the three items it
destroyed are all the same failure mode, named in the README rather than left for
a user to trip over.

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

**Six of the ten defects I found were in the measurement code, not the tool.**
An answer key with the correct option at C fourteen times in thirty. A scorer
reading the wrong column, reporting 0% precision on a set that was unanimously
clean. A harness that withheld a whole page render from the arm under test and
then counted its absence against the router — that one cost me a published
22/23 that I had already written up as 20/23 and blamed on routing.

**The fourth defect in the tool is the one nobody was looking for, and it is the
largest content loss here.** If the text extractor parses a pipe table anywhere
on a page, the page is skipped entirely — 8,295 pages, 4,065 of them with no
image on them at all, so nothing about them is routed *or counted*. A filter that
suppresses a call leaves no artifact to audit, and every eval in the repo samples
the routed set, so all of them were blind to it by construction. 65.6% of 250
blind-labelled skipped pages carry a real figure (95% CI 60–71). The comparison
that makes it a defect rather than a trade-off: the pages this filter discards
carry figures at 70%, and the pages the router pays for carry them at 73%. The
only difference between them is whether a table got parsed somewhere on the page.

Then I priced it in **harm instead of exposure**, which is the methodological
mistake underneath every routing number in this repo: 65 screened questions on 65
of those discarded pages, four arms. Optical control 65/65. The pipeline as it
ships, 61/65. So the fix recovers 3 of the 4 answers it loses — 4.6% (95% 2–13),
nothing like what 65.6% implies. The mechanism is the interesting part: a vector
figure's own text survives into the markdown regardless of routing, so **0 of 30
questions about printed labels, legends and axes were lost**, and all four real
losses were readings taken off a plotted curve. What the filter throws away is
shape, not words. Grounding is where the loss actually sits — 41 of 65 pages can
quote the line against the fix's 62 — so the honest case for spending is citation
recovery, not answer recovery. It costs +3,911 vision calls and +64% of routed
image tokens, taking 2.5x to about 2.05x, and it is therefore unfixed and written
up rather than quietly omitted. Two caveats in the writeup cut the other way:
closed-book scores 72% on that question set, so multiple choice flatters the
status quo, and 4.6% is a floor while 32.3% is nearer a ceiling.

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
| **routed** | **19.9M** |

2.5x cheaper than reading everything, at 0.32 vision calls per page. Per corpus
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
and the three holdout corpora are sha256-pinned per file, so those reproduce
exactly. `arxiv`, `bills`, `datasheets` and `pmc` ship URLs without hashes, and
`papers` has no manifest at all — re-fetching those may not give you
byte-identical inputs.

Two routing rules shipped, both validated the way I think these things should be:
a corpus fetched *after* the rule was designed, sha256-pinned, verified disjoint
from the design set by content hash, and every drop labelled blind by three
independent labellers who saw the PNG and nothing else — not the rule, not the
hypothesis, not which answer would be convenient. 348 arXiv papers for the first
(17 effective drops, 17 correct) and 250 journal PDFs plus those papers for the
second (203 drops, 0 real items, Wilson 97–100). The write-up for the first leads
with its one failure mode — a booktabs table continued across pages is
indistinguishable from a repeated template — and with the fact that the 18th drop
was found by diffing the shipped implementation against the analysis script, not
by the script.

**The third corpus exists because it killed a rule, and that is the more useful
result.** The biggest saving available was a rule to stop the busiest branch
firing on vendor boilerplate; in-sample it read 17 of 17. The corpus it was
fitted to is 75% Texas Instruments, so I fetched 295 datasheets across eleven
vendors with none above 19%. It scored 80% (95% Wilson 72–86) and lost 24 real
figures — 98% on TI, 66% on every other vendor. It also cascaded: 46 previously
subsumed rasters came back and four documents finished *more* expensive than
before. A holdout of the wrong kind is not a holdout, and precision is usually
not the axis that decides.

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
236-document corpus, against 2.5x on PDFs, and the README says that in the
heading rather than the footnotes. There is no page render to avoid, so the only
lever is filtering embedded images, and most embedded images in a real deck are
content. A slide deck costs roughly one vision call per slide. Spreadsheet
charts are the exception that genuinely pays — they are read from the chart XML
as exact numbers at zero vision cost, 19 of 20 recovered across 35 workbooks.

MIT. https://github.com/LPSlv/doc-extract

What I would most like back: a discriminator for the two failure modes I could
not solve. Vendor boilerplate — Würth title blocks, Nexperia legal pages — is
half the routing waste and is a real multi-column grid, so lattice shape cannot
see it; recurrence across documents is the only lever I can think of, and the one
rule I built for it died on its holdout. And a table continued across pages
repeats its geometry, which is exactly what a template does; frame containment
and page-consecutiveness were both measured and both dead, the second with its
premise backwards. The three holdout corpora are in the repo, so a candidate can
be scored on something it was not fitted to.
