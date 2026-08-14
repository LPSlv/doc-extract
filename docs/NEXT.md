# Where this was left

State at the end of the **2026-08-14** session. Everything below is pushed, CI
green, **146 tests**, `eval/gate.py` **16/16** byte-identical (8 documents ×
2 description placements), and **nothing is publicly posted** — one venue went up
on 2026-08-14 and was withdrawn the same day.

This header said "2026-08-12, 93 tests, 7/7" until the moment it was rewritten,
which is the same rot the cost bullet below documents. If you finish a session
here, the last edit is this line.

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
- **`textonly_page` ships** — inside a `cost_guard` collapse, drop a page with no
  raster and ≤2 drawing paths. 203 blind drops across two holdouts fetched
  afterwards, 0 real items lost. The largest routing saving here: 6,175 → 5,903
  calls on the design corpora. [`eval/nofigure.md`](../eval/nofigure.md).
- **Descriptions can be placed inline** — `convert.py --inline`, Office only,
  opt-in, default unchanged. By *insertion* beside the engine's line, never
  substitution for it, which is what keeps byte-identity enforceable; the gate
  runs both placements over every format.
- **Filter 3 now records what it suppresses** (`why: "parsed_table"`, with
  `wanted` and `raster`). Behaviour-neutral — zero routing drift across all
  twelve corpora — but it means the largest measured loss here is finally
  visible in `manifest.json` rather than invisible to every eval.
- **Three corpora exist for validating vendor and journal rules**, each fetched
  after the rule it tested and each verified disjoint by content hash:
  `corpus/arxiv_holdout` (348), `corpus/pmc_holdout` (250 journals),
  `corpus/datasheet_holdout` (295 datasheets, 11 vendors, TI held to 9%). The
  last one is new and is the durable asset from a rule that failed on it.
- **Four routing candidates were examined on 2026-08-13 and none shipped**: the
  `curves` small-cluster rule (80% precision out of sample, cascades, and costs
  5× the compute that sank soft-mask), the multi-figure swap and its
  multi-raster half (both trade resolution for coverage), `boxed_text`
  consecutiveness (the premise is backwards), and `FILTER3_ROWS = 4` (selects a
  smaller population, not a better one). Every one is written up.

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
  the untested idea was *consecutiveness*, since a continued table's pages are
  adjacent and a prompt-box template's usually are not. **Measured, and dead**
  (`eval/rejected-signals.md`). The premise is backwards: over all 188 labelled
  firings it marks waste rather than tables — 63% of `none` sit on
  consecutive-fingerprint pages against 15% of `table` — and on the 55 drops the
  difference is 41/52 against 2/3, Fisher p = 0.53. The candidate is dominated
  by the containment refinement that was itself rejected as dominated. The
  failure mode stands unfixed; a signal identifying *continuation* directly (a
  repeated column header, a "continued" caption) is what is left.
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

- ~~**`curves` is 45% of all vision calls and a quarter of that is branding**~~ —
  **the datasheet holdout now exists and the rule is rejected on it.**
  `corpus/datasheet_holdout` — 295 datasheets, 9,449 pages, eleven vendors, no
  vendor above 19% of files (TI is 9%, against 75% in `corpus/datasheets`),
  disjoint by filename and by sha256 with one collision found and removed — was
  fetched for exactly this. 222 drops, 120 labelled blind by three labellers
  each: **80% precision (95% Wilson 72–86), 24 real figures lost**; 98% on TI,
  **66% on every other vendor**. It also cascades: 46 subsumed rasters return and
  four documents finish with *more* calls than before.
  [`eval/curves-holdout.md`](../eval/curves-holdout.md). Nothing measured now
  reaches the 2,770 `curves` firings — but **the corpus is the durable asset**,
  and it is the right holdout for any future vendor-boilerplate candidate, as
  `pmc_holdout` was for journals.
- **Correction, made while fetching:** Microchip does *not* block automated
  fetches at the server — `ww1.microchip.com` answers 200 to a datasheet
  request. Its `robots.txt` is `Disallow: /`, so the corpus omits it by policy,
  not by refusal. Winbond is the same shape (`Disallow: /resource-files`). ST,
  TME and LCSC are unchanged. `analog.com` is simply unreachable from this
  network, and would be the best remaining diversity source if reached
  elsewhere. Actually refusing with 403: onsemi, ROHM, Toshiba, Bourns,
  Littelfuse, TDK, TE Connectivity.
- **The unreachable 16** of `whole_document`'s 41 wasted calls: BMC/RSC title
  pages, TI tables of contents, and old scanned journal pages where the page
  *is* one image, so no geometric test can see it is only prose.
- `TEXTONLY_PATHS = 2` is a floor, not a tuned threshold. 6 cuts one more and
  starts losing real items (87%). Moving it needs a fresh holdout.
- **Estimates, not a census.** Unlike `strokegrid.md`'s 170, these branch rates
  come from 240 of 4,106 firings with CIs stated. `datasheets` is 74% of
  `curves` firings and TI-dominated; the pmc and tds cells are 7 and 8
  observations.
- ~~**`over_scale_guard` flips were not counted.**~~ — counted, see
  [`eval/scaleguard.md`](../eval/scaleguard.md). **10 documents of 2,342** flip
  true → false, 145 → 135 over the guard; none flips the other way and none can,
  since `drop_textonly` only removes items. All ten are `cost_guard` collapses in
  arxiv, pmc and papers, landing at 7–15 calls. On the 16 pages of those ten that
  `eval/nofigure` already labels, the rule dropped 4 of 4 `none` pages and kept 8
  figures, 3 tables and 1 branding page: the guard now fires on 6.9% fewer
  documents, and what it stopped announcing is the part with nothing on it. 119
  calls across the ten now happen without a prompt, and `SCALE_GUARD = 15`
  remains an arbitrary number nobody has validated.
- **Fixed while measuring the above:** `office.py` returned a hardcoded
  `"over_scale_guard": False`. Invisible because `convert.py` recomputes the flag
  from `pending`, so the user path was always right and no test read
  `harvest_office()` directly — a deck routing thirty items reported `False`.
  `SCALE_GUARD` now lives in `filters.py`, which the Office path can import
  without dragging PyMuPDF in, and
  `tests/test_anydoc_invariants.py` pins both directions.

### 3. ~~Multi-figure pages~~ — DONE, rejected, see [`eval/multifigure.md`](../eval/multifigure.md)

Priced on both sides. **+0.99% tokens** to recover a real figure on **50.4% of
129 blind-labelled pages** (95% CI 42–59%, 59 of 91 documents) — and it pays by
shrinking the raster it already reads to a **median 0.27× linear resolution**,
100% of them below 1.0×. Rejected: it buys a second figure by half-blinding the
first, and half the time there is no second figure. The non-degrading variant —
render *and* keep the crop — is +2.13% and +131 vision calls.

What is left from it:

- ~~**All 131 triggers are filter 3**~~ — **counted, see
  [`eval/filter3.md`](../eval/filter3.md), and it is the largest content loss
  measured in this repo.** Filter 3 skips **8,295** pages; on **5,137**
  `render_reason` would have fired, and on **4,065** the page carries no raster
  at all, so nothing about it is ever routed *or counted*. **65.6% of 250
  blind-labelled pages carry a real figure** (95% CI 60–71), ≈2,668 of the
  population, across 409 documents. The comparison that makes it a defect rather
  than a trade-off: the `curves` pages filter 3 **discards** carry figures at
  70%; the `curves` pages the router **pays for** carry them at 73%. The only
  difference is whether a table was parsed somewhere on the page.

  Fixing it in full is **+3,911 calls and +64% image tokens**, 2.25× → 1.85× —
  rejected on price (`eval/rejected-signals.md`). **`FILTER3_ROWS = 4` is
  proposed and deliberately NOT applied**: three pipe lines is a header, a rule
  and *one data row*, so requiring two takes 400 pages at 87% in-sample and 73%
  (62–82) across 71 blind holdout labels, for +386 calls and +2.3% of prompt
  tokens. Patch and test at `eval/filter3/proposed.patch`.

  **Validated on `corpus/datasheet_holdout`, and rejected as written.** 144
  renders added over 294 datasheets, all labelled blind by three labellers each:
  **63% carry a figure (95% Wilson 55–71)**, against 87% in-sample. Pooled over
  all three holdouts it is **143/215 = 66.5% (60–72)** — the same rate as the
  entire 4,065-page blind spot (65.6%, 60–71). `T = 4` selects a **smaller**
  population, not a better one, and `eval/rejected-signals.md` already rejected
  routing that population on price.

  **The branch-gated version is what survives, and `eval/filter3.md` predicted
  it before this corpus existed.** `stroke_grid` and `dense_grid` *mean* "a ruled
  table the extractor missed", which is exactly what filter 3 establishes — they
  were 0 of 11 and 1 of 7 in-sample, and on the datasheet holdout they are
  **0 of 36, all `table`, unanimously**, a quarter of all firings there against
  14 of 400 in-sample. Gated to `curves`/`diagonals`: **139/164 = 84.8% (78–89)**
  across three holdouts, for **+374 calls** against the proposal's +386 — 97% of
  the cost. It is **not** a vendor rule: ungated the holdout reads TI 78% /
  others 53%, gated it inverts to TI 78% / others **92%**.

  **Two things the holdout did not fix.** Journals genuinely fail — `pmc_holdout`
  is a **census, not a sample** (the rule fires exactly 9 times on 250
  documents), and adding the 12 never-labelled `corpus/pmc` firings gives **4 of
  21, 19% (8–40)**, almost all publisher front matter. And the gate does not help
  `SCALE_GUARD`: **10 documents newly stop to ask**, all TI, all one direction.

  **Harm was then measured, and it is far below exposure — see
  [`eval/filter3_harm.md`](../eval/filter3_harm.md).** 65 screened questions on
  65 discarded pages, four arms. The optical control answers 65/65. **The status
  quo — the page suppressed, as it ships today — answers 61/65 (94%).** The fix
  answers 64/65, so it recovers **3 of the 4 lost answers**, 4.6% (95% 2–13).
  Grounding is where the real loss sits: the status quo can *quote the line* for
  only 41/65 against the fix's 62/65, **32.3% (22–44)**.

  The mechanism is the predicted one, and it is why this population is the
  cheapest loss in the router: **`printed` facts — legends, axis labels,
  callouts — are 0 of 30 lost**, because a vector figure's own text survives
  into `doc.md` regardless of routing. All four outright losses are `geometry`
  (4 of 35): readings taken off a plotted curve. What filter 3 discards is
  *shape*, not *words*.

  So against the 4,065-page blind spot the full branch-gated fix buys roughly
  **154 recovered answers for +60% image tokens** — one per 25 pages rendered —
  and the rationed rule buys about **22 answers, or ~137 recovered citations**.
  **Priced in harm rather than exposure, the case for spending is an order of
  magnitude weaker than the 65.6% figure suggests**, and the rationed rule's
  honest justification is citation recovery, not answer recovery.

  Two caveats that cut the other way and are in the writeup: **closed-book
  scores 72%**, so multiple choice flatters the status quo and 4.6% is a floor
  while 32.3% is closer to a ceiling — free text would sit nearer the ceiling.
  And the authoring-bias control ran *opposite* to the fear: questions written
  from the page's text first were ungrounded 45% of the time against 28% for
  questions written from the image, because looking at a figure draws you toward
  its printed labels.

  **Not applied.** The gated patch and its test still need writing —
  `eval/filter3_patch.py --narrow` is the exact source that was measured. It
  would be the first cost increase this repo has accepted (+2.3% of prompt
  tokens, 2.25× → 2.20×), which is a product judgement rather than a measurement
  one. The argument for it: it adds pages carrying a figure at **85%**, while the
  `curves` pages the router **already pays for** carry one at **73%**
  (`eval/nofigure.md`) — it buys content at a better rate than existing spend.
- **Correction:** the `over_scale_guard` flip count for this rule is **10**, not
  the 13 first reported here or the 12 in `eval/filter3/cost.json`.
  `filter3.py cost_run()` reads the flag from before `drop_batch_furniture` while
  reading calls and tokens from after it; `ti_ne556.pdf` and `ti_sn74hc125.pdf`
  land at exactly 15 calls and so do not cross. Eleventh and twelfth measurement
  defects here — and **the first two that made a result look worse rather than
  better.**
- Still uncounted: **769 filter-3 pages carrying a raster that filters 1–2
  dropped**. Nothing on them is routed either, but a rule there interacts with
  the furniture and dedup filters, which is a different argument.
- ~~**The multi-raster half is the cheap one and nobody costed it.**~~ —
  labelled and **rejected**, see [`eval/multiraster.md`](../eval/multiraster.md).
  The four stored components reproduce exactly (308 / 96 / 150,934 / 116,890);
  the accounting built on them does not survive. The hypothesis was that the
  resolution argument which killed the lone half might not apply when a page
  already carries several small crops. **It applies — the crops are the same
  size, there are just more of them.** 91 pages labelled: the swap recovers a
  real graphic on **61.5%** (95% 51–71) and destroys resolvable detail *inside*
  crops the router already reads on **39.6%** (30–50). 26 strictly better, 6
  strictly worse, 30 a trade, 29 only cheaper. Against `textonly_page` (−4.0% of
  calls, **zero** real items lost over 203 blind drops) it is not close.
  `batch_furniture` was checked as a second-order term and is **zero of 94**.
- Corrected in passing: `eval/rejected-signals.md` said these corpora hold
  **1,014** documents. They hold **686**. Every count downstream of it was right,
  which is exactly why it survived.
- The labellers were three runs of one model on one prompt. 129/131 unanimity
  measures determinism, not reliability — and the same caveat applies to
  `eval/strokegrid`'s holdout, where it is not currently stated.

## The launch — posted to one venue, then withdrawn

**Nothing is live.** [firecrawl/firecrawl
#4307](https://github.com/firecrawl/firecrawl/discussions/4307) was posted to Show
and tell on 2026-08-14 and withdrawn the same day at the author's request, after a
matter of minutes, with zero comments and zero reactions. It is now titled
"Withdrawn by author", its body is a one-line withdrawal notice, and it is closed
as outdated.

**It could not be hard-deleted, and that is worth knowing before posting to
anyone else's repository.** GitHub lets only repo maintainers delete a
discussion — for the author of a discussion in somebody else's repo,
`viewerCanDelete` is `false` and `deleteDiscussion` returns `FORBIDDEN`. Editing
is all that is available, and **GitHub keeps public edit history**, so the
original text remains reachable to anyone who opens it. Full removal would need a
Firecrawl maintainer. A discussion on somebody else's repo is effectively
one-way; treat posting there as unrecallable.

**Unposted, and each needs its own yes:** Show HN, r/LocalLLaMA, the X thread.
They go out under LPSlv's social identities, from a logged-in browser session,
which is why none of them can be done unattended. The drafts are current against
`87570d6` either way.

The three pre-conditions are settled:

- ~~**The `extract_pages_markdown` claim that justified posting to Firecrawl
  first was ours, and it was wrong.**~~ Settled. `eval/figqa.md` said the
  per-page API returns nothing on 3 of 30 documents; re-running both APIs gives
  **1**. The post leads with a named repro (`irlz44n_infineon.pdf`, pages 1–2
  return 0 chars against 7,559 from `process_pdf`) instead of the aggregate, and
  the whole observation was re-run at the pinned 0.2.6 on the morning it went
  out: 1 of 30, 8 of 30, 20 of 624, reproduced exactly. The staging strategy
  worked as intended — the error surfaced at the cheapest possible audience,
  which was us. **`eval/figqa.md:43` and `eval/figqa_text.py:11` still carry the
  unreproduced 3, and should be corrected.**
- ~~**The opendataloader comparison scores exist only in a design spec.**~~
  **Cut before posting.** The published text says the comparison was made, says
  the numbers are not being printed because nothing in the repo regenerates
  them, and offers to re-run it properly and post the artifact. A repo whose
  pitch is published negative results should not lead with a figure it cannot
  reproduce.
- ~~**The cost figures move whenever routing does.**~~ They moved a third time,
  and the drafts were stale for a day before anyone noticed: `textonly_page`
  shipped after they were written, so 20.1M / 2.4× / 0.33 became **19.9M / 2.5×
  / 0.32**. Found by re-running `eval/readme_tables.py` against the drafts rather
  than trusting them. **The same pass found `README.md:198` — the section
  *heading* — still reading "costs 2.4× less" three lines above a generated table
  saying 2.5×.** Re-check `00-claims.md` against
  `docs/benchmarks/results/*.json` immediately before each remaining post; the
  addendum at the bottom of that file is the template.

What the remaining drafts gained on 2026-08-14, since it is stronger than what it
replaced: filter 3 as the fourth skill defect and the largest content loss here,
priced in harm (4.6% of answers, 32% of citations) rather than exposure (65.6%);
the `curves` rule dying on a purpose-built vendor-diverse holdout at 80%
precision and 24 real figures lost; `textonly_page`'s 203 blind drops with zero
real items. All three closing asks used to request a boilerplate-heavy holdout
corpus — that corpus now exists and killed the rule it was built for, so the asks
point at the two failure modes that are actually open.

## A caution for whoever picks this up

Across three sessions, **four** defects were found in the skill and six in the
measurement code. The fourth skill defect is **filter 3**, and it is the one
nobody was looking for: it surfaced as a side effect of `eval/multifigure.md`
and had never been counted, because **a filter that suppresses a call produces
no artifact to audit**. Every eval here samples the routed set —
`figqa_select.py` draws its candidates from `res["items"]` — so anything the
router silently drops is invisible to all of them by construction, figure-QA
included. If you add a filter, add a way to see what it removed.

The measurement defects were: withheld routed items, a circular gate, a contaminated
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

Four more earned theirs on 2026-08-13, when four candidates were examined and
none shipped:

- **Build the holdout before trusting the number, and check what the holdout is
  made of.** The `curves` rule read 17/17 in-sample and 80% on 295 vendor-diverse
  datasheets — 98% on TI, 66% on everyone else. `FILTER3_ROWS = 4` read 87%
  in-sample and 63% on the corpus carrying four fifths of its firings. Both were
  fitted to a corpus that was 75% one vendor. A holdout of the wrong *kind* is
  not a holdout.
- **Precision is not the only axis, and usually not the deciding one.** The
  `curves` rule failed three ways independently: precision, cascade (46
  suppressed rasters returned and four documents got *more* expensive), and
  compute (5× the per-document overhead that sank soft-mask suppression). The
  multi-figure swap passed on cost and failed on resolution, which nobody had
  thought to measure.
- **Check whether the claim survives changing the denominator.** "2.25× → 1.87×"
  was true of the five-corpus figure and wrong about the published headline,
  which is 2.5× → ~2.05×. Same arithmetic, different question.
- **Separate exposure from harm.** Every routing number here — 65.6%, 70%, 85% —
  says a figure *exists*, never that an answer was *lost*, while cost is measured
  in exact tokens. Pricing benefit in a proxy and cost in currency
  systematically favours doing nothing. `eval/figqa.md` is still the only
  measurement here that crosses the gap, at n=23.
