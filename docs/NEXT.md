# Where this was left

State at the end of the 2026-08-11 session. Everything below is pushed, CI
green, 85 tests, `eval/gate.py` 7/7 byte-identical.

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

What is left from it, in order:

- **A free win, unimplemented.** Dropping a `stroke_grid` page whose signature
  covers more than the existing `UBIQUITY` (0.50) share of its document removes
  6 wasted calls and loses nothing — 100% precision on the labelled set, and no
  new constant. Small (8% of the waste) but strictly positive.
- **Do not ship the 0.20 threshold** from that table. It is read off the set it
  would be validated against. It needs a held-out corpus first.
- **A rule for the LaTeX half now exists and measures well**: count *distinct*
  vertical stroke positions instead of strokes, and drop a firing where there
  are exactly 2 (the box signature — left edge, right edge, nothing between)
  AND the same fingerprint appears on ≥2 other pages of the document. 35 of 72
  wasted calls removed, 2 real items lost, **95% precision**, stable under a
  document-level split (92% / 96%).
  **Not shipped — it needs a true holdout, and the holdout now exists.**

  `corpus/arxiv_holdout` was fetched for exactly this: 348 papers from `2608.*`,
  disjoint from `corpus/arxiv` (`2607.*`), sha256-pinned in
  `eval/manifests/arxiv_holdout.urls.tsv`. Rebuild with
  `uv run eval/fetch.py arxiv_holdout` (arXiv allows one request per 3 s, so
  budget ~20 minutes).

  **RESUME HERE — three steps, in order:**

  1. `uv run eval/strokegrid_validate.py corpus/arxiv_holdout`
     Applies the rule and renders every page it would drop to
     `eval/strokegrid/holdout/pages/`. On the first 59 papers this was 19
     firings and 4 drops, so expect roughly 100 firings and 25 drops at full
     size — enough to test 95% precision, not enough to refine it.
  2. Label those drops **blind**, the way `eval/strokegrid/labels.tsv` was built:
     one agent per batch, sees only the PNGs, assigns
     `table` / `plot` / `figure` / `none`. Anything not `none` is a real item
     the rule would have destroyed.
  3. Decide on the number. If precision holds near 95%, implement in
     `harvest.py` (and update `reference/harvest-block.md`, which
     `tests/check_sync.py` enforces), add a test naming this incident, re-run
     `eval/bench.py` over the affected corpora, and regenerate the README block
     with `uv run eval/readme_tables.py --write`. If precision drops below
     ~90%, record it in `eval/rejected-signals.md` and stop — that is a result,
     not a failure.

  Do not skip step 2 in favour of eyeballing a few. The whole reason this rule
  is unshipped is that its numbers came from the set that designed it.
- It is blind to the vendor-boilerplate half (Würth title blocks, Nexperia
  legal pages) — those are real multi-column grids. Recurrence, not lattice
  shape, is the lever there.
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
