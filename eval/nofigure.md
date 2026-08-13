# Routed pages with no figure on them, labelled

`docs/NEXT.md` had this queued on the strength of figure-QA v3, where 11 of 30
routed pages carried no figure at all, concentrated in `whole_document` (4 of
9) and `curves` (4 of 11). Thirty observations cannot condemn two branches —
`stroke_grid` was 3-for-3 wrong in a **three**-observation sample and turned
out to be 42% waste, not 100%, once every firing was labelled. So this labels
a real sample of the real population instead.

**4,106 firings across 482 documents**, from the same 711 documents in
datasheets, pmc, arxiv, papers and tds that `eval/strokegrid.md` used, so the
two artifacts are directly comparable. 240 sampled, rendered at 130 dpi, and
classified by **three independent labellers each** — 24 labellers over 8
batches — every one told to break ties in the branch's favour.

## Where the numbers come from

Stated first, because six defects have been found in this repo's measurement
code and every one flattered a published number.

- **4,106 / 6,175** — `eval/nofigure/firings.json`, written by
  `eval/nofigure_render.py`. It harvests all 711 documents and applies
  `drop_batch_furniture` **per corpus**, the same batch scope
  `strokegrid_validate.py` uses; pooling five corpora into one batch would
  silently disable the >50%-of-documents test. Cross-checked against the
  existing artifact: this run's `stroke_grid` count (**133**) plus its
  `boxed_text` drops (**37**) is **170**, exactly the firing count
  `eval/strokegrid.md` labelled over the same documents.
- **the waste rates** — numerator is the merged label being `branding` or
  `none`, denominator is 120 per branch, from `eval/nofigure/labels.tsv` via
  `eval/nofigure_score.py`. That script reads every column **by name**
  (reading the label by index is the bug that made `strokegrid_holdout_score.py`
  report 0% on a unanimously-`none` set) and refuses to merge unless every tag
  carries exactly three labels.
- **the holdout precisions** — `eval/nofigure/holdout/labels.tsv`, blind, on
  two corpora fetched *after* the rule was written.

`nofigure_render.py` does its harvesting in six subprocess shards rather than
through `harvest._harvest_all`. That function's `ProcessPoolExecutor`
deadlocked on this corpus — every worker parked in `futex_do_wait`, the parent
blocked, no exception, no progress — and its `except` clause cannot catch a
hang.

## The sample, and what is not in it

4,106 firings is far too many to label, so the budget is 240, drawn with
**seed 20260813**. Nothing was truncated silently; `nofigure_render.py` prints
the full strata table, reproduced here:

| branch | corpus | population | sampled | **not labelled** |
|---|---|--:|--:|--:|
| curves | datasheets | 2,056 | 89 | 1,967 |
| curves | arxiv | 353 | 15 | 338 |
| curves | tds | 176 | 8 | 168 |
| curves | pmc | 152 | 7 | 145 |
| curves | papers | 33 | 1 | 32 |
| whole_document | pmc | 586 | 53 | 533 |
| whole_document | arxiv | 425 | 38 | 387 |
| whole_document | datasheets | 245 | 22 | 223 |
| whole_document | papers | 80 | 7 | 73 |

The budget is split **equally between the branches** and only then
proportionally by corpus. They are separate routing decisions with separate
answers, and a flat proportional draw would have given `curves` almost
everything: one collapsed 96-page paper contributes 96 `whole_document`
firings while a `curves` page contributes one. **The consequence is that no
pooled percentage here is a population rate unless it is reweighted**, and
every pooled figure below states its weights.

## What they fire on

| branch | figure | table | branding | none | n | **waste** |
|---|--:|--:|--:|--:|--:|--:|
| `curves` | 88 | 2 | 29 | 1 | 120 | **25%** (95% CI 18–33) |
| `whole_document` | 60 | 19 | 8 | 33 | 120 | **34%** (95% CI 26–43) |

Labellers agreed unanimously on 235 of 240; the other five split 2/3.

Reweighted by the population shares — `curves` 2,770 of 4,106, `whole_document`
1,336 — the two branches together waste **28% of 4,106 firings, about 1,149
vision calls**, which is 19% of the 6,175 the router makes across these
corpora. That is much the largest block of waste measured in this router:
`stroke_grid`'s entire 42% is 72 calls.

By corpus:

| branch | corpus | figure | table | branding | none | n | waste |
|---|---|--:|--:|--:|--:|--:|--:|
| `curves` | datasheets | 66 | 2 | 21 | 0 | 89 | 24% |
| `curves` | pmc | 3 | 0 | 4 | 0 | 7 | 57% |
| `curves` | tds | 5 | 0 | 3 | 0 | 8 | 38% |
| `curves` | arxiv | 13 | 0 | 1 | 1 | 15 | 13% |
| `curves` | papers | 1 | 0 | 0 | 0 | 1 | — |
| `whole_document` | pmc | 23 | 7 | 5 | 18 | 53 | 43% |
| `whole_document` | arxiv | 19 | 6 | 0 | 13 | 38 | 34% |
| `whole_document` | papers | 5 | 0 | 0 | 2 | 7 | 29% |
| `whole_document` | datasheets | 13 | 6 | 3 | 0 | 22 | 14% |

## The 11-of-30 was roughly right, and its reasons were wrong

37% against a reweighted 28% is close enough that the small sample was not
misleading in aggregate. Its **branch split** was: it implied 44% for
`whole_document` against 34%, and 36% for `curves` against 25%.

Two selection effects were worth checking rather than assuming.
`figqa_select.py` admits only pages carrying ≥400 characters of extractable
text, which sounds like it should bias hard towards prose. Measured on this
sample it barely moves anything — restricting to `page_chars ≥ 400` takes
`curves` from 25% to 27% and `whole_document` from 34% to 35%. The real
distortion is the other one: figure-QA sampled **one page per document and one
document per draw**, so a 40-page `whole_document` collapse and a lone `curves`
page counted the same. That is why it saw 9 `whole_document` firings in 30
when only 96 of 711 documents collapse at all.

## Two branches, two completely different failures

### `whole_document` is not a detector, and that is the point

`whole_document` is not a routing branch. It is the label `cost_guard` puts on
every page of a document when the routed set outprices reading the whole
thing, and the guarantee it makes is about **cost**, not content: it renders
the bibliography, the acknowledgements and the two-column prose along with
everything else. A `whole_document` page with no figure is therefore not a
misfire in the sense a `curves` misfire is — the branch never claimed the page
had a figure.

That reframing is what makes the waste reachable. Filtering the collapsed set
only lowers cost, so it cannot violate the bound cost_guard exists to enforce.
And the waste is largely **structural rather than judgemental**: of the 41
wasted `whole_document` calls, 25 are on pages carrying no raster and at most
two vector paths. There is no branding to distinguish from a figure on those
pages, because there is nothing on them at all.

### `curves` fires on the Texas Instruments logo

Of the 30 wasted `curves` calls, **21 are pages whose only vector content is
the 143-curve TI datasheet header**, and 23 of 30 are TI files. `ti_bq25895`
p15, `ti_cd4051b` p21, `ti_sn74hc157` p12 and p15, `ti_tl072` p35,
`ti_tps54331` p2 and p21, `ti_lp2985` p19 — all the same page: a logo, a
header rule, a footer rule, and prose.

The reason the existing defences miss it is worth writing down. The branch
gates on `_plot_shaped`, whose `stroke_frac` is the **union bounding box of
every stroke path on the page**. A logo at the top and a rule at the bottom
put that box across the whole page: the median `stroke_frac` over these 120
firings is **0.72**. The 2% floor that `eval/tds-corpus.md` measured as
cleanly separating logos from charts separates them only when the logo is the
*sole* stroke on the page.

The remaining four are journal front matter —
`10.1177_17151635251352537.PMC12361176` p1, `41598_2025_Article_28505.PMC12...`
p5 (a Nature banner over a pseudocode listing), `IJA-64-403.PMC7286399` p1 (a
cover with a QR code), `jbm-14-329.PMC10132291` p1.

## The rule that ships

**Inside a `cost_guard` collapse, drop a page that has no raster placed on it
and at most `TEXTONLY_PATHS` (2) drawing paths.** A page border and a header
rule are two paths.

In-sample: 25 of the 41 wasted `whole_document` calls, **0 real items lost**,
spread over **22 distinct documents** — not one pathological file, which is
the failure mode that sank the `stroke_grid` ubiquity "free win"
(`eval/rejected-signals.md`).

### Validated out-of-sample, twice

The rule was designed by reading the labels above, so those numbers are
in-sample. Two holdouts were fetched afterwards for the purpose, because the
waste is half journal boilerplate and 348 arXiv papers contain none of that —
the exact mismatch that made `arxiv_holdout` the wrong holdout for the
ubiquity rule.

- **`corpus/pmc_holdout`: 250 journal PDFs**, pinned in
  `eval/manifests/pmc_holdout.urls.tsv`, discovered by
  `uv run eval/discover.py pmc_holdout` from the `01/xx` prefix of the PMC
  `oa_pdf` tree that `pmc` never reaches, with everything `pmc.urls.tsv` pins
  excluded by name. **Zero overlap with `corpus/pmc` by sha256 and by
  filename**, checked.
- **`corpus/arxiv_holdout`: 348 papers**, already disjoint from `corpus/arxiv`
  by content hash.

Every drop was rendered and labelled **blind** by three independent labellers
who saw the PNG and nothing else — not the rule, not the hypothesis, not which
answer would be convenient — and who were told to break every tie *against*
`none`.

| holdout | whole_document calls | rule drops | labelled | real items | precision |
|---|--:|--:|--:|--:|--:|
| `pmc_holdout` | 546 | 113 | 113 (all) | **0** | **100%** (95% CI 97–100) |
| `arxiv_holdout` | 1,011 | 320 | 90 (seed 20260813) | **0** | **100%** (95% CI 96–100) |

203 blind labels, 195 unanimous, **not one `figure` and not one `table` from
any labeller**. The arXiv drop set was sampled because 320 is more than the
labelling budget; the seed and the population are in
`eval/nofigure/holdout/arxiv-sample.json`.

### Checked against figure-QA, which nobody involved could edit

The rule drops **none of the 20 pages figure-QA v3 selected** and none of the
16 that carry an admitted question, so **22/23 is unaffected**.

The v1 candidate set is a better test, because its ground truth was authored
in an earlier session by an agent that had never heard of this rule. It drops
**4 of those 30 pages — q05, q09, q13, q29 — and all four are in
`eval/figqa/questions.json`'s `no_figure` list**: "references page",
"two-column prose appendix", "two-column prose", "two-column prose". It
touches none of the 15 pages that yielded a question. That is an independent
confirmation of the drop set by a judgement made before the rule existed.

### Effect on the design corpora

**6,175 vision calls → 5,903, a 4.4% reduction**: 272 page renders removed
across **76 of the 96 collapsed documents** (pmc 142, arxiv 104, papers 20,
datasheets 6). In tokens, 17.7% of the whole-document render budget over these
corpora — 192,532 of 1,089,332. For scale, `boxed_text` was 0.69% of calls.

It costs nothing to compute. `page_geometry` already walks `get_cdrawings()`
once per page, so `paths` is counted in the loop that was already running, and
the raster-placement map is the `seen` dict filter 1 already built.

### Why it cannot cascade

The reverted QR-code filter (`eval/tds-corpus.md`) *raised* the call count on
two documents, because it dropped **images** before `grid_pages`, pushing
pages below `RASTER_GRID` so a page render un-collapsed into crops. This drops
a **page render**, only when the page carries no raster at all, and only after
`cost_guard` — so there is nothing left on the page to un-subsume. Pinned by
`tests/test_textonly_page.py`, which also pins that the filter does nothing
outside a collapse and nothing to a page needing OCR.

Text is unaffected in every case: `process_pdf` runs over the whole document
independently of routing, so a dropped page keeps its extracted text.

### The diff, which this time found nothing

`eval/nofigure_validate.py --diff` compares the analysis script's drop set
against what `harvest.py` actually drops. On `boxed_text` that comparison
disagreed by one page and that page was the rule's entire known failure mode.
Here it agrees exactly — **113 vs 113 and 320 vs 320, zero either way** — and
the reason is worth stating rather than celebrating: both sides read the same
two facts (`get_images`, `get_cdrawings`) with no thresholds in between, so
there is little for them to disagree about. The check is cheap and was worth
running; it is not evidence of much.

## `curves`: measured, and nothing ships

Four candidates were measured against the 120 labelled `curves` firings.

**Signature ubiquity — 0 firings.** `harvest.py` already computes the set of
`(curves, diagonals, axis_h, axis_v)` signatures covering more than `UBIQUITY`
of a document and already drops such pages as `vector_furniture`. The obvious
thought is that the `stroke_frac < 0.02` gate on that drop is what lets the TI
header pages through. It is not: **not one of the 120 firings has a signature
covering even 30% of its document.** The logo's curve count repeats, but the
full four-tuple does not, because the underlines and rules elsewhere on the
page vary. This differs from the rejected `strokegrid_ubiquity` signal in
branch and in outcome — that one fired six times on one document; this one
fires zero times on 120.

**Repeated curve count.** Dropping the four-tuple and keeping only "the same
`curves` count on ≥10 pages" does select the TI header, but it selects real
figures with it: 41 firings, **20 real items lost, 51% precision**. TI
rasterises many of its block diagrams, so a page with a real figure on it has
*exactly the same vector content* as a prose page — the logo.

**Largest connected stroke cluster** (`eval/nofigure_features.py`), as opposed
to the union bounding box. It scores **0.0372 on the TI header pages and
0.0372 on `ti_lm317` p25 (a thermal-derating chart), `ti_lm317` p27 (a PCB
layout) and `ti_lp2985` p15 (a block diagram)** — same reason. This measure was
already rejected once in `eval/tds-corpus.md` ("largest spatial stroke cluster
— 4N25 disclaimer 0.0056 above a real chart 0.0045"); it fails here for a new
reason and the same underlying one.

**Small cluster and no caption** is the only combination that separates
cleanly: 17 cut, 17 `branding`, 0 real lost. It is not shipped:

- 17 of 120 is 14% of the branch's firings against the 21% the
  `whole_document` rule reaches, from 13 documents, and 2 of the 17 carry
  rasters — dropping those un-subsumes an image, which is the cascade that
  forced the QR filter's revert;
- it is read off the set it would be validated on, and it targets **vendor**
  boilerplate, so `arxiv_holdout` and `pmc_holdout` are both the wrong
  holdout. A datasheet holdout does not exist, and ST, Microchip, TME and LCSC
  block automated fetches (`eval/tds-corpus.md`), so building one large enough
  is not a small job;
- the caption half is a keep-gate on a signal already known to be one-sided
  (`eval/tds-corpus.md`: 175 of 328 content images have a caption, 0 of 49
  branding images do — it proves content, never branding).

So the honest position on `curves` is the one `eval/tds-corpus.md` reached
about branding twelve signals ago: **a vendor logo is separable from a figure
only by reading it**, and reading it is the vision call being avoided. The
difference from the raster case is that the exposure is not small — 29 of the
30 wasted `curves` calls are branding, and the branch fires 2,770 times.
Recorded in `eval/rejected-signals.md`.

## What is left

- **The 16 unreachable `whole_document` wasted calls**, which are the same
  problem in a different place: BMC and RSC article title pages (a logo, a
  check-for-updates badge, an abstract box), TI tables of contents, and — a
  class worth naming — **old scanned journal pages**, `137.PMC2132290` p5 and
  p9, `427.PMC2136578` p2, `jc773627.PMC2110141` p8, where the page *is* one
  image, so no geometric test can see that the image is only prose.
- **`TEXTONLY_PATHS = 2` is a floor, not a tuned threshold.** Loosening it to
  6 cuts 26 rather than 25 and starts losing real items (4 of 30 firings,
  87%). The value ships at the point where the rule needs no judgement; there
  is no case for moving it without a fresh holdout.
- The `curves` branch is **45% of all vision calls** these corpora produce
  (2,770 of 6,175). A quarter of that is branding. Nothing measured here
  reaches it.

## Provenance

- `eval/nofigure/firings.json` — all 4,106 firings, enumerated mechanically,
  plus every branch's count for cross-checking
- `eval/nofigure/index.json` — the 240 sampled firings and their page facts
- `eval/nofigure/batch1..8.tsv` — what each labeller saw
- `eval/nofigure/labels-01..24.tsv` — the 24 labellers, 30 pages each
- `eval/nofigure/labels.tsv` — the 240 merged labels with their agreement
- `eval/nofigure/features.json` — the candidate signals, computed after
  labelling so no labeller could see them
- `eval/nofigure/holdout/index-*.json`, `labels-*.tsv`, `labels.tsv` — the two
  holdouts, their drops and the 203 blind labels
- `eval/nofigure/pages/`, `eval/nofigure/holdout/pages/` — the renders,
  gitignored; rebuild with `uv run eval/nofigure_render.py` and
  `uv run eval/nofigure_validate.py <corpus>`
- `eval/nofigure_score.py` — merges, scores, and its Wilson intervals

One measurement defect found and fixed while merging, recorded because this
file's whole argument is that measurement code is where the errors are. A
labeller wrote **28 rows for a 30-row batch and reported 30**. The merge
absorbed it silently: the two affected tags simply merged on two votes, and
the only trace was a `2/2` in an agreement column where every other row said
`3/3` — which reads like a design choice, not a defect. `nofigure_score.py`
now refuses to merge unless every tag carries exactly three labels.
