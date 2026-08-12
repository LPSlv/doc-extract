# Where this was left

State at the end of the 2026-08-12 session. Everything below is pushed, CI
green, 93 tests, `eval/gate.py` 7/7 byte-identical.

## What is true right now

- **Figure-QA v3: doc-extract 22/23**, full optical 23/23, on questions
  screened so only the visual can answer them. One genuine miss (w18b), a page
  carrying two drawings where only the upper is routed. Method and every
  correction: [`eval/figqa.md`](../eval/figqa.md).
- **Cost: unchanged and reproducible.** 48.9M / 13.6M / 20.1M tokens, 0.34
  vision calls per page, 2,342 PDFs, 20,375 pages. Both README marker blocks
  regenerate byte-identically from `eval/readme_tables.py --write`.
- Routed rasters follow the page's placement matrix, on rotated pages too;
  guarded by `tests/test_raster_orientation.py`, and CI installs PyMuPDF so
  those tests actually run.

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

### 2. Routed pages carrying no figure — 11 of 30

The largest measured waste, concentrated in `whole_document` (4 of 9) and
`curves` (4 of 11): references pages, prose, mastheads, an ESD icon.

Expect this to end in `eval/rejected-signals.md`. Twelve branding signals were
already measured and eleven rejected, for the reason recorded in
`eval/tds-corpus.md`: branding is separable from a figure only by reading it,
which is the call being avoided. Run it anyway — a documented negative is worth
more than an untested intuition.

### 3. Multi-figure pages — measured, deliberately not actioned

54% of routed rasters sit on pages with more than one raster; 10% are lone
rasters on pages that also show vector figure signal. Broad exposure, small
measured loss (1 in 23). The obvious fix turns 134 crops into page renders.
Measure that trade before implementing it. See `eval/rejected-signals.md`.

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

Over one session, three defects were found in the skill and **four in the
measurement code**: withheld routed items, a circular gate, a contaminated
question, and an answer key with the correct option at C fourteen times in
thirty. Every one of them flattered or distorted a published number, and none
was caught by tests.

Prefer building durable labelled artifacts over running fresh end-to-end evals.
An artifact can be re-checked by someone else; an eval mostly re-discovers the
mistakes of whoever wrote it.
