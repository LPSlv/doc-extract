# Where this was left

State at the end of the 2026-08-12 session. Everything below is pushed, CI
green, 93 tests, `eval/gate.py` 7/7 byte-identical.

## What is true right now

- **Figure-QA v3: doc-extract 22/23**, full optical 23/23, on questions
  screened so only the visual can answer them. One genuine miss (w18b), a page
  carrying two drawings where only the upper is routed. Method and every
  correction: [`eval/figqa.md`](../eval/figqa.md).
- **Cost: regenerated 2026-08-13 against the shipped router.** 48.9M / 13.6M /
  **19.9M** tokens, **2.5×**, **0.32** vision calls per page (6,525 / 20,375),
  2,342 PDFs, 20,375 pages. All twelve results JSONs re-run after
  `textonly_page` shipped; both README marker blocks regenerate byte-identically
  from `eval/readme_tables.py --write`.

  **This number has now gone stale twice in one day, the same way both times.**
  It was 0.34 in this file and three places in the README — the pre-`boxed_text`
  rate — then 0.33 for the few hours between fixing that and shipping
  `textonly_page`. Both times the *generated* block was right and the
  hand-carried prose around it was wrong. Anything quoted outside a marker block
  is unmanaged by definition. If you change routing, `eval/bench.py` over all
  twelve corpora and `eval/readme_tables.py --write` are part of the change, not
  follow-up work — and then grep the README for the old figures, because the
  generator will not touch them.
- Routed rasters follow the page's placement matrix, on rotated pages too;
  guarded by `tests/test_raster_orientation.py`, and CI installs PyMuPDF so
  those tests actually run.
- **`boxed_text` ships**, the first routing rule here validated on a corpus
  fetched after it was designed. 6,834 → 6,797 vision calls, one known failure
  mode, documented in the README's limitations rather than left for a user to
  find. [`eval/strokegrid.md`](../eval/strokegrid.md).
- `eval/report.py` can regenerate `RESULTS.md` again — it had been crashing on
  `office.json` since that file landed in the results directory.

## Next, in the order I would do it

### 1. ~~Label `stroke_grid`~~ — DONE, see [`eval/strokegrid.md`](../eval/strokegrid.md)

All 170 firings labelled. **42% waste**, not the 100% the three-observation v1
sample implied, and the waste has three distinct causes rather than one.

**The `boxed_text` rule is now validated and shipped.** Count *distinct*
vertical stroke positions instead of strokes; drop a `stroke_grid` firing with
exactly 2 (the frame signature — left edge, right edge, nothing between) whose
fingerprint repeats on ≥2 other pages. In `harvest.py` as `box_templates()`,
pinned by `tests/test_boxed_text.py`.

Validated on `corpus/arxiv_holdout` — 348 papers fetched for the purpose,
disjoint from `corpus/arxiv` by content hash — with all drops labelled blind by
three independent labellers. **17 effective drops, 17 `none`, 100% precision**
(95% CI 82–100%); 95% over all 188 labelled firings, matching the in-sample
claim exactly. 2,473 → 2,456 calls on that corpus, at no compute cost.

What is left from it, in order:

- ~~**A free win**, dropping a `stroke_grid` page whose signature covers more
  than `UBIQUITY` (0.50) of its document~~ — **rejected**, and worth reading as
  a cautionary tale. Its "6 wasted calls removed, 100% precision" was six pages
  of *one* document, and `boxed_text` now drops all six anyway: that file routes
  zero calls today. Marginal benefit nil, and 0 firings on the holdout.
  `eval/rejected-signals.md`.
- **Do not ship the 0.20 threshold** from `strokegrid.md`'s table. It is read
  off the set it would be validated against. It needs its own holdout.
- **The known failure mode is booktabs tables continued across pages** — two
  interior rules in the same place on every continuation page. All three real
  items lost across 188 firings are this case. A containment refinement that
  targets it was measured and rejected as dominated (`rejected-signals.md`);
  the untested idea is *consecutiveness*, since a continued table's pages are
  adjacent and a prompt-box template's usually are not. Three observations is
  too few to fit that on.
- `boxed_text` is blind to the vendor-boilerplate half (Würth title blocks,
  Nexperia legal pages) — those are real multi-column grids. Recurrence, not
  lattice shape, is the lever there.
- Worth knowing: the branch's second stated purpose, marker-based plots, fired
  **10 times in 170**. Do not defend the threshold on that basis.

### 2. ~~Routed pages carrying no figure~~ — DONE, see [`eval/nofigure.md`](../eval/nofigure.md)

4,106 `curves` and `whole_document` firings enumerated, 240 labelled by three
independent labellers each. **`curves` wastes 25% (CI 18–33), `whole_document`
34% (CI 26–43)** — reweighted, 28% of firings and 19% of every vision call these
corpora make. The figure-QA sample's 37% was close in aggregate and wrong on the
branch split.

**`textonly_page` ships**, and it is the largest routing saving measured here.
Inside a `cost_guard` collapse, drop a page with no raster and at most
`TEXTONLY_PATHS` (2) drawing paths. Validated on two corpora fetched
afterwards — `corpus/pmc_holdout` (250 journal PDFs, disjoint from `corpus/pmc`
by content hash, `uv run eval/discover.py pmc_holdout && uv run eval/fetch.py
pmc_holdout`) and `corpus/arxiv_holdout` — **203 blind drops labelled by three
labellers each, 0 real items, 100% precision** (Wilson 97–100 / 96–100).
6,175 → 5,903 calls on the design corpora, from 76 of 96 collapsed documents.
In `harvest.py` as `drop_textonly()`, pinned by `tests/test_textonly_page.py`.
For scale, `boxed_text` was 0.69%.

What is left from it:

- **`curves` is 45% of all vision calls and a quarter of that is branding** —
  2,770 firings, and nothing measured reaches it. Four signals tried, all in
  `eval/rejected-signals.md`. The one that separates cleanly (small stroke
  cluster, no caption: 17 cut, 0 lost) needs a *datasheet* holdout, which does
  not exist and is hard to build: ST, Microchip, TME and LCSC block automated
  fetches.
- **The unreachable 16** of `whole_document`'s 41 wasted calls: BMC/RSC title
  pages, TI tables of contents, and old scanned journal pages where the page
  *is* one image, so no geometric test can see it is only prose.
- `TEXTONLY_PATHS = 2` is a floor, not a tuned threshold. 6 cuts one more and
  starts losing real items (87%). Moving it needs a fresh holdout.
- **Estimates, not a census.** Unlike `strokegrid.md`'s 170, these branch rates
  come from 240 of 4,106 firings with CIs stated. `datasheets` is 74% of
  `curves` firings and TI-dominated; the pmc and tds cells are 7 and 8
  observations.
- **`over_scale_guard` flips were not counted.** Removing 272 renders takes some
  documents below `SCALE_GUARD = 15`, changing when the skill stops to ask.

### 3. ~~Multi-figure pages~~ — DONE, rejected, see [`eval/multifigure.md`](../eval/multifigure.md)

Priced on both sides. **+0.99% tokens** to recover a real figure on **50.4% of
129 blind-labelled pages** (95% CI 42–59%, 59 of 91 documents) — and it pays by
shrinking the raster it already reads to a **median 0.27× linear resolution**,
100% of them below 1.0×. Rejected: it buys a second figure by half-blinding the
first, and half the time there is no second figure. The non-degrading variant —
render *and* keep the crop — is +2.13% and +131 vision calls.

What is left from it:

- **All 131 triggers are filter 3.** `pm.count("\n|") >= 3` skips a page for its
  table before `render_reason` ever runs. So filter 3 discards a page for one
  reason while ignoring another reason to keep it — and filter-3 pages with
  figure signal and *no* raster are the same defect, entirely uncounted.
- **The multi-raster half is the cheap one and nobody costed it.** The rule as
  worded does not say *lone*: 308 rasters on 96 pages, where collapsing to one
  render per page is **−34,044 tokens and −212 calls**. Cost measured, benefit
  unlabelled. That is the one worth labelling next.
- Corrected in passing: `eval/rejected-signals.md` said these corpora hold
  **1,014** documents. They hold **686**. Every count downstream of it was right,
  which is exactly why it survived.
- The labellers were three runs of one model on one prompt. 129/131 unanimity
  measures determinism, not reliability — and the same caveat applies to
  `eval/strokegrid`'s holdout, where it is not currently stated.

## Not done, and waiting on a human

**The launch.** Drafts exist but were written to a scratchpad that does not
survive the session; regenerate them from `eval/figqa.md` and the README. Four
pieces were planned: a Firecrawl Discussions post (smallest audience, and it
carries a factual claim about `extract_pages_markdown` scoring worse than
`process_pdf` — post it first so an error surfaces cheaply), Show HN,
r/LocalLLaMA, and an X thread.

Lead with the measurement failures, not the multiplier. Every tool in this
space claims a multiplier; almost none publishes the eval that didn't work.

Nothing has been posted anywhere. Posting to Firecrawl's repo happens under
LPSlv's GitHub identity and needs an explicit yes.

## A caution for whoever picks this up

Across two sessions, three defects were found in the skill and **six in the
measurement code**: withheld routed items, a circular gate, a contaminated
question, an answer key with the correct option at C fourteen times in thirty,
a scorer that read the `page` column as the label and reported 0% on a set that
was unanimously clean, and a validation script blind to `cost_guard` that
under-reported a drop set by exactly the one item that mattered. Every one
flattered or distorted a published number, and none was caught by tests.

Prefer building durable labelled artifacts over running fresh end-to-end evals.
An artifact can be re-checked by someone else; an eval mostly re-discovers the
mistakes of whoever wrote it.

Two habits earned their keep on the `boxed_text` work and are worth repeating:

- **Diff the shipped implementation against the analysis script.** They
  disagreed by one page. That page was the only real table in the drop set and
  the entire known failure mode of the rule.
- **Ask where a percentage came from before believing it.** "100% precision, 6
  calls saved" was one document. It sat in this file as a recommendation for
  two sessions.
