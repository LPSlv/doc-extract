# `stroke_grid`, labelled exhaustively

`docs/NEXT.md` had this as the first queued experiment, on the strength of a
three-observation sample in figure-QA v1 where the branch fired three times and
was wrong three times. Three observations cannot condemn a branch, so this
labels every firing instead.

**170 firings across 110 documents**, from 711 documents in datasheets, pmc,
arxiv, papers and tds. Every one rendered at 130 dpi and classified by eye
(`eval/strokegrid/labels.tsv`), by six labellers each told to break ties in the
branch's favour.

## What it fires on

| label | n | share |
|---|--:|--:|
| `table` — a ruled table the extractor did not parse | 64 | 37.6% |
| `plot` — marker/tick-based plot, the branch's other purpose | 10 | 5.9% |
| `figure` — some other real figure; wrong branch, real content | 24 | 14.1% |
| **`none` — no table, no plot, no figure** | **72** | **42.4%** |

Its stated purpose is met 44% of the time. It buys *something* 58% of the time.
**42% is waste.** The v1 sample's 3-for-3 was unlucky, not representative — but
the branch is still the weakest in the router.

By corpus, and the spread is the story:

| corpus | table | plot | figure | none | waste |
|---|--:|--:|--:|--:|--:|
| papers | 11 | 5 | 3 | 4 | **17%** |
| datasheets | 19 | 0 | 0 | 6 | 24% |
| arxiv | 17 | 2 | 19 | 33 | 46% |
| pmc | 13 | 3 | 2 | 23 | 56% |
| tds | 4 | 0 | 0 | 6 | 60% |

## The second purpose barely exists

`render_reason` justifies this branch as catching "either a marker/tick-based
plot or a ruled table". Across 170 firings, **10 were plots** — and 5 of those
are in one corpus. Whatever the branch is worth, it is worth it as a
table-catcher; the plot rationale is close to dead weight and should not be
used to defend the threshold.

## Three distinct false-positive families

Not one cause, three, and they need different answers.

**1. Recurring boilerplate (largest).** Vendor legal pages and CAD title
blocks. Würth's drawing title block — a ruled metadata grid in the footer —
fires on 6 pages of `led_wurth.pdf` and 6 of `wurth_7447709100.pdf`. Medknow's
"Access this article online" QR box accounts for 6 of one batch's 18. One PMC
review, `MGR-10-30`, burned 6 consecutive calls on prose pages whose only
strokes were the header rule and footer bar.

Related, and not counted as waste above: **22 of the 64 `table` hits are the
same table** — Nexperia's "Data sheet status" legal boilerplate, repeated
across datasheets. Literally a ruled table the extractor missed, so the label
is right, but it is identical text every time. Precision understates the
problem; the branch's real defect is repetition.

**2. LaTeX math furniture.** Fraction bars, matrix delimiters, underbraces and
QED squares supply axis-aligned strokes in both orientations. Ten of one
batch's fourteen `none`s were theorem/proof pages; four consecutive pages of
`2607.29020v1` fired on plain proof text.

**3. Framed verbatim text.** Boxed LLM prompt listings, algorithm pseudocode
with loop bars, boxed labelling instructions. `2607.29679v1` alone contributed
five. This family barely existed in the corpora the thresholds were tuned on
and is now everywhere in ML papers.

## A rule that works, and does not work well enough

60% of the waste is in documents that waste more than once, so within-document
repetition is the obvious lever. `harvest.py` already computes a page signature
and an intra-document template set, but only drops a page when it *also* has
low ink, low stroke fraction and fewer than 8 rects — conditions a ruled title
block fails by design. `batch_furniture` cannot help either: it needs a
signature in >50% of *documents*, and a Würth datasheet is a handful of files.

Tested against the labels: **drop a `stroke_grid` page whose signature covers
more than X of its document's pages**, on the reasoning that a real table's
geometry differs page to page while furniture repeats.

| threshold | wasted cut | useful lost | precision | recall |
|---|--:|--:|--:|--:|
| 0.50 (current `UBIQUITY`) | 6 | 0 | **100%** | 8% |
| 0.30 | 13 | 2 | 87% | 18% |
| 0.25 | 17 | 2 | 89% | 24% |
| **0.20** | **21** | **2** | **91%** | **29%** |
| 0.15 | 26 | 6 | 81% | 36% |
| 0.10 | 32 | 17 | 65% | 44% |

At the existing 0.50 the rule is free — 6 wasted calls removed, nothing lost —
and at 0.20 it removes 21 and costs 2 real figures.

**Not implemented, deliberately.** Two reasons:

- 0.20 is read off the set it would be validated against. `docs/benchmarks/RESULTS.md`
  puts threshold sensitivity out of scope precisely because tuning on the
  measurement set invalidates it. A threshold chosen here needs a held-out
  corpus before it ships.
- The size does not obviously clear the bar. 21 calls is 0.3% of the 6,405
  across these corpora, and it loses 2 real figures. Soft-mask suppression was
  rejected in `rejected-signals.md` at 0.013% for costing 40 ms/document; this
  is larger but not free, since it trades content for cost rather than saving
  both.

The 0.50 variant is a different case: strictly free, no content lost, and it
needs no new constant because `UBIQUITY` already exists. That one is worth
implementing if anyone wants a small, safe win. It fixes 8% of the problem.

## What would actually move the number

Families 2 and 3 — math furniture and framed verbatim — are together roughly
half the waste and share a property the current geometry misses: **the strokes
enclose text rather than bounding a data region.** A signal along those lines
(text coverage inside the stroke bounding box, say) is the thing worth trying
next. It is a new measurement, not a threshold tweak, and it should be built
against this labelled set and then validated on a corpus this set does not
contain.

## Provenance

- `eval/strokegrid/firings.json` — every firing, enumerated mechanically
- `eval/strokegrid/index.json` — per-firing page facts
- `eval/strokegrid/labels.tsv` — the 170 labels, tag / corpus / file / page / label / note
- `eval/strokegrid/pages/` — the renders, gitignored, rebuild with
  `uv run eval/strokegrid_render.py`

One correction worth recording: an earlier pass reported that 26% of firings
were on pages whose markdown already contained a table, implying filter 3 was
broken. That was a bug in the render script, which matched 1-based item pages
against `pdf_inspector`'s 0-based `PageMarkdown.page` and read the following
page. Corrected, the figure is 1% and **no** firing trips filter 3's threshold.
Filter 3 does exactly what it claims.
