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
| 0.50 (current `UBIQUITY`) — all 6 from one document, see below | 6 | 0 | **100%** | 8% |
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

The 0.50 variant looked like a different case: strictly free, no content lost,
no new constant because `UBIQUITY` already exists. **It was measured properly
afterwards and rejected.** Its 6 cuts are pages 2–7 of a single document, and
`boxed_text` now drops all six — that file routes zero vision calls today. On
the holdout it fires on 0 of the 77 firings that survive `boxed_text`. The
write-up is in `eval/rejected-signals.md`; the lesson is that "100% precision"
over one document formats identically to a real number.

## So how do you make it work? A rule that measures well, and what it still needs

The branch asks *are there strokes in both orientations?* A ruled table, a box
around a prompt listing, and a page of fraction bars all answer yes. What
separates them is whether the strokes form a **lattice**.

Counting *distinct* vertical stroke positions (clustered at 2 pt) instead of
counting strokes:

| distinct vertical positions | table | plot | figure | none |
|---|--:|--:|--:|--:|
| 0–1 | 16 | 1 | 0 | 3 |
| **exactly 2** | 8 | 1 | 4 | **41** |
| 3–4 | 29 | 1 | 2 | 10 |
| 5–9 | 7 | 0 | 5 | 14 |
| 10+ | 4 | 7 | 13 | 4 |

**Exactly two is the box signature** — a frame has a left edge and a right edge
and nothing between. Tables sit at 0–1 (booktabs, no verticals at all) or 3–4
(ruled columns); plots and figures at 10+.

Alone it is not good enough: 41 cut, **13 real items lost**, 76% precision.
Dropping a table costs content silently while a wasted call only costs tokens,
so this codebase should not take that trade — it has already reverted two
signals that lost content out-of-sample.

Composing it with the repetition finding fixes that. A real table appears once;
a box template repeats.

| rule | cut | lost | precision | recall |
|---|--:|--:|--:|--:|
| `vx == 2` | 41 | 13 | 76% | 57% |
| `vx == 2` and fingerprint on ≥1 other page | 37 | 5 | 88% | 51% |
| **`vx == 2` and fingerprint on ≥2 other pages** | **35** | **2** | **95%** | **49%** |
| `vx == 2` and on ≥3 other pages | 24 | 2 | 92% | 33% |

where *fingerprint* is the tuple of rounded distinct vertical positions, so
"the same box in the same place on another page".

**Half the waste, 95% precision, and it is stable.** A document-level split
gives 92% on one fold and 96% on the other, and the 35 drops come from 18
distinct documents rather than one pathological file.

### What it does not do

Recall is entirely corpus-dependent:

| corpus | cut | lost | precision | recall |
|---|--:|--:|--:|--:|
| arxiv | 26 | 1 | 96% | 79% |
| pmc | 7 | 1 | 88% | 30% |
| papers | 2 | 0 | 100% | 50% |
| datasheets | 0 | 0 | — | **0%** |
| tds | 0 | 0 | — | **0%** |

It solves the LaTeX families — prompt boxes, pseudocode frames, proof pages —
and is completely blind to the vendor-boilerplate family, because a Würth title
block or a Nexperia legal table is a real multi-column grid with more than two
vertical positions. Those need a recurrence rule instead, and no working one
exists — the `UBIQUITY = 0.50` variant that looked like the start of it turned
out to fire only on pages `boxed_text` already takes.

### Validated out-of-sample, and shipped

The rule was designed by looking at the labels above, so those numbers are
in-sample and the document split showed stability, not generalisation. The
obvious holdouts could not serve: `bills` and the six olmOCR corpora produce
only **17** `stroke_grid` firings between them and the rule fires on **none**
— olmOCR extracts are single pages and bills are short, so no page template
can recur.

So a corpus was fetched for the purpose. **`corpus/arxiv_holdout`: 348 papers
from `2608.*`**, sha256-pinned in `eval/manifests/arxiv_holdout.urls.tsv`,
**disjoint from `corpus/arxiv` by content hash** (14 of the IDs are late-July
`2607.*` that appear in the August listing; none is a file the design set
contains). Rebuild with `uv run eval/fetch.py arxiv_holdout`.

94 `stroke_grid` firings. The rule dropped **18** of them. Every drop was
rendered and labelled **blind** by three independent labellers who saw the PNG
and nothing else — not the rule, not the hypothesis, not which answer would be
convenient — and who were instructed to break every tie *against* `none`.

| | drops | `none` | real | precision |
|---|--:|--:|--:|--:|
| effective (change what ships) | 17 | 17 | 0 | **100%** |
| all firings of the rule | 18 | 17 | 1 | 94% |
| **combined with the 170 in-sample** | **55** | **52** | **3** | **95%** |

The three labellers agreed unanimously on all 17 effective drops, with
near-identical descriptions: proof pages, boxed prompt listings, framed JSON
examples. 95% Wilson interval on 17/17 is 82–100%.

> **Read that unanimity carefully.** The "three independent labellers" are three
> runs of one model on one prompt. They are independent of each other's answers,
> not of each other's blind spots, and near-identical descriptions are as
> consistent with shared bias as with correctness. Unanimity here is evidence of
> **determinism, not reliability**, and the Wilson interval prices sampling error
> only — it cannot price a systematic misread all three share. The same caveat
> applies to `eval/multifigure`'s 129/131 unanimity. A genuinely independent
> check would need a different model, a different prompt, or a human.

Effect on the corpus: **2,473 vision calls → 2,456**, a 0.69% reduction, with
no `cost_guard` cascades. It costs nothing to compute — `page_geometry`
already walks `get_cdrawings()` once per page, so `vx_pos` is collected in the
loop that was already running.

Shipped in `harvest.py` as the `boxed_text` drop, with `box_templates()`
carrying the reasoning and `tests/test_boxed_text.py` pinning both halves of
the rule and the fact that the frame fixture really does trip the branch.

### The one failure mode, named

The 18th drop is why this section can be specific. `2608.07734v1` p19 is
**Table 2, a booktabs table continued across pages** — two interior rules
separating three column groups, in the same place on every continuation page.
It satisfies the rule perfectly: two vertical positions, repeated. The rule's
premise, *a real table's geometry differs page to page*, is simply false for
continued tables.

That page is safe only by accident: `cost_guard` collapses that document into
24 whole-page renders, so it is described anyway. In a document that does not
collapse, the rule would silently degrade a table.

**All three real items lost across 188 labelled firings are this same case**
(`pi-13-473.PMC5067340` p5, `2607.29378v1` p7, `2608.07734v1` p19). One
observation would be a fluke; three of three is a class.

Two things bound the damage. A dropped page still keeps its extracted text —
`process_pdf` runs over the whole document independently of routing, so what
is lost is the *vision description* of a table the text extractor rendered
without structure, not the table's content. And the exchange rate is 52
wasted calls avoided for 3 degraded tables.

A refinement that targets exactly this case was measured and rejected; see
`eval/rejected-signals.md`.

### How the 18th drop was found

Not by the validation script. That script scores the rule against
`harvest_batch`'s *item* list, which is post-`cost_guard`, so it never saw a
firing inside a collapsed document. The discrepancy surfaced only because the
shipped implementation was diffed against the script's 17 candidates and
returned 18. Had the rule been implemented from the script's output alone, a
real table in the drop set would have gone unrecorded.

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
- `eval/strokegrid/holdout/index.json` — what the rule drops on the holdout
- `eval/strokegrid/holdout/labels.tsv` — the 17 blind labels and their 3/3 agreement
- `eval/strokegrid_validate.py` — applies the rule to a corpus, renders the drops
- `eval/strokegrid_holdout_score.py` — precision and its Wilson interval
- `eval/strokegrid_frame_test.py` — scores plain vs framed over all 188 firings

Two measurement bugs found and fixed while scoring the holdout, recorded
because this file's whole argument is that measurement code is where the
errors are. `strokegrid_holdout_score.py` first read the label by column
*index* and picked up `page` instead, reporting 0% precision on a set that is
unanimously `none`; it now reads by column name. And the validation script's
blindness to `cost_guard` is described above — it under-reported the drop set
by one, and the one it missed was the only real item.

One correction worth recording: an earlier pass reported that 26% of firings
were on pages whose markdown already contained a table, implying filter 3 was
broken. That was a bug in the render script, which matched 1-based item pages
against `pdf_inspector`'s 0-based `PageMarkdown.page` and read the following
page. Corrected, the figure is 1% and **no** firing trips filter 3's threshold.
Filter 3 does exactly what it claims.
