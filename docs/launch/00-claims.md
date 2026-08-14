# Claims audit for the launch drafts

Every factual claim that appears in `01-firecrawl-discussion.md`,
`02-show-hn.md`, `03-r-localllama.md` and `04-x-thread.md`, with the file and
line it came from, so the set can be checked in one pass without re-deriving
anything.

Compiled 2026-08-13 against the repo at commit `97869f7`. **Re-verified
2026-08-14 against `87570d6`; see the addendum at the bottom — four published
figures had moved, and the drafts now carry the newer ones.**

**Verdicts used:**

| | |
|---|---|
| ✅ **checks out** | the source says this, and where it was cheap to re-derive, it re-derived |
| ⚠️ **weakened** | the repo states something stronger than the evidence supports; the drafts state the weaker version |
| ❓ **unsourced** | traceable only to a design note with no artifact behind it; the drafts flag it as such |

**Three things a human should look at before anything is posted.** They are the
only places the drafts knowingly diverge from what the repo says about itself:

1. **C-14** — the `extract_pages_markdown` "3 of 30" claim does not reproduce.
   Measured today it is 1 of 30. The drafts use the smaller number and a
   page-level statistic instead. `eval/figqa.md:43` and `eval/figqa_text.py:11`
   both carry the unreproduced figure and are **not** corrected by this work
   (the brief was drafts only, no edits to existing files).
2. **C-05** — vision calls per page. Superseded twice; see the addendum. The
   drafts now say **0.32** (6,525 ÷ 20,375), the README's generated blocks agree,
   and the one place the README disagreed — the section *heading* at line 198,
   which still said 2.4× — has been corrected. This entry stays as written
   because the number going stale twice in two days is the point.
3. **C-15** — the opendataloader scores for `extract_pages_markdown` (0.860 /
   0.903 / 0.772) exist only in a design spec. No artifact in the repo backs
   them. **Settled 2026-08-14: cut.** The draft now states that the comparison
   was made and that the numbers are not being printed because nothing
   regenerates them, and offers to re-run it properly. `docs/NEXT.md:322-325`
   already judged cutting the safer call; a repo whose pitch is published
   negative results should not lead with a figure it cannot reproduce.

---

## A. Cost and scale

Recomputed today by summing `docs/benchmarks/results/*.json` with the same logic
as `eval/readme_tables.py:21-36,84-93`, and by running `uv run
eval/readme_tables.py` (read-only, no `--write`) and diffing against the README
block. The block regenerates byte-identically.

| # | claim | drafts | source | verdict |
|---|---|---|---|---|
| C-01 | 2,342 PDFs, 20,375 pages, 12 corpora | 2, 3, 4 | `docs/benchmarks/results/*.json`; `README.md:183,187-200`; recomputed: files 2342, pages 20375 | ✅ |
| C-02 | read every page = 48.9M input tokens | 2, 3, 4 | same; exact 48,913,721 | ✅ |
| C-03 | text only = 13.6M | 2, 3, 4 | same; exact 13,583,799 | ✅ |
| C-04 | routed = 20.1M | 2, 3, 4 | same; exact 20,096,373 | ✅ |
| C-05 | **0.33 vision calls per page** | 2, 3, 4 | 6,797 calls ÷ 20,375 pages = **0.3336** | ⚠️ **weakened** — `README.md:27,349` and `docs/NEXT.md:12` both say **0.34**. That is the pre-`boxed_text` count (6,834 ÷ 20,375 = 0.3354, rounds to 0.34); after `boxed_text` shipped at 6,797 calls (`docs/NEXT.md:19-20`) the correct rounding is 0.33. Hand-carried prose, outside the regenerated markers. Drafts say 0.33 |
| C-06 | 2.4× cheaper than reading everything | 2, 3, 4 | 48,913,721 ÷ 20,096,373 = 2.434; `README.md:183` | ✅ |
| C-07 | reading every page costs 3.6× text extraction | 2, 3, 4 | 48,913,721 ÷ 13,583,799 = 3.601; `README.md:15` | ✅ |
| C-08 | per-corpus range 7.0× (`bills`) down to 0.9× | 2, 3, 4 | `README.md:189,200`; regenerated table matches | ✅ |
| C-09 | the 0.9× corpus is 62 single-page documents and it loses | 2, 3, 4 | `README.md:200,202`; `docs/benchmarks/results/olmocr_long_tiny_text.json` | ✅ |
| C-10 | corpora are datasheets, arXiv, PMC, US legislation, six olmOCR-bench classes | 2, 3 | `README.md:171-173,187-200` | ✅ |
| C-11 | published token figures are ~0.6% low on rasters; per item up to 58%; measured over 892 routed rasters; not fixed because the fix costs ~40 ms/document | 3 | `eval/rejected-signals.md:53-89`, esp. `:62-70,83-84` | ✅ |
| C-12 | token model is Anthropic's image rule, `(w×h)/750` after fitting to 1568 px, text at `chars/3.5` | 3 | `eval/datasheets.md:10-14`; `eval/resolution.md:17-18` | ✅ |
| C-13 | ~21 constants fitted, not learned | 3 | `README.md:359-362` | ✅ |

## B. The Firecrawl claim — `extract_pages_markdown` vs `process_pdf`

This is the claim `docs/NEXT.md:90-92` sends to Firecrawl first "so an error
surfaces cheaply." It did.

| # | claim | drafts | source | verdict |
|---|---|---|---|---|
| C-14 | `extract_pages_markdown` returns nothing while `process_pdf` returns a full document | 1 | see below | ⚠️ **weakened** |
| C-15 | joined `extract_pages_markdown` scores 0.860 / 0.903 / 0.772 vs `process_pdf` 0.875 / 0.915 / 0.814 on opendataloader-bench | 1 | `docs/superpowers/specs/2026-08-03-doc-extract-skill-design.md:151-162` | ❓ **unsourced** |
| C-16 | `irlz44n_infineon.pdf` pages 1–2 return 0 chars from the per-page API while `process_pdf` gets ~100 table rows | 1 | `eval/tds-corpus.md:65-68`; **re-derived today** | ✅ |

### C-14 in detail

**What the repo says.** `eval/figqa.md:43-45`: "the per-page API returns nothing
at all on 3 of these 30 documents." Same figure in `eval/figqa_text.py:11-14`.

**What I measured.** Re-ran both APIs at **pdf-inspector 0.2.6** — the version
`skills/doc-extract/harvest.py:3` pins and the version `eval/figqa_text.py:3`
pins — over all 30 documents named in `eval/figqa/candidates.json`, all of which
are present under `corpus/`:

| | measured 2026-08-13 |
|---|--:|
| documents where `extract_pages_markdown` returns nothing at all | **1 of 30** |
| documents with ≥1 page returning empty markdown | 8 of 30 |
| pages returning empty markdown | 20 of 624 (3.2%) |
| documents where `process_pdf` returns nothing | 0 of 30 |

The one all-empty document is `corpus/pmc/main.PMC9937890.pdf` — 4 of 4 pages
empty, against 18,398 characters from `process_pdf`.

**Verdict: 1 of 30, not 3 of 30.** I could not reconstruct a reading of the data
that yields 3 at document level. The nearest defensible restatements are "8 of
30 documents have at least one page come back empty" or "20 of 624 pages," and
the Firecrawl draft uses both of those plus the 1-of-30 total-loss case, since a
page-level statistic with a named repro is a more useful bug report anyway.

Supporting, and consistent with 1 in 30: the design spec's independent check
(`...skill-design.md:159-161`) reports "on 60 corpus documents the two disagree
on 6, and on one document `extract_pages_markdown` returns **nothing at all**."
That is 1 in 60.

### C-15 in detail

The three-decimal table at `...skill-design.md:154-157` is the only place these
numbers appear. There is no evaluator output, no results JSON and no script in
the repo that produces them; `eval/opendataloader.md` documents the gate
procedure for the *shipped* engine only, and its gate minima (`:18-22`) are the
`process_pdf` column of that table, not the `extract_pages_markdown` column.
Re-running would need the external opendataloader-bench corpus and was out of
scope here.

**Settled 2026-08-14: the table is cut.** The draft now says the comparison was
made, says the numbers are not being printed because nothing in the repo
regenerates them, and offers to re-run it properly and post the artifact. It
still explicitly declines to use observation C-14 as evidence for it.

## C. Negative results — routing

| # | claim | drafts | source | verdict |
|---|---|---|---|---|
| C-17 | 170 `stroke_grid` firings across 110 documents, from 711 documents | 1, 2, 3, 4 | `eval/strokegrid.md:8-12` | ✅ |
| C-18 | labelled 37.6% table / 5.9% plot / 14.1% figure / **42.4% none** | 1, 2, 3, 4 | `eval/strokegrid.md:17-20`; `README.md:388-391` | ✅ |
| C-19 | rendered at 130 dpi, six labellers, told to break ties in the branch's favour | 3 | `eval/strokegrid.md:10-12` | ✅ |
| C-20 | the branch's second purpose (marker plots) is 10 firings in 170, 5 of them in one corpus | 1, 2, 3, 4 | `eval/strokegrid.md:36-42` | ✅ |
| C-21 | false positives include QR boxes, LaTeX fraction bars, Würth title blocks, consecutive proof pages | 2 | `eval/strokegrid.md:46-69` | ✅ |
| C-22 | `boxed_text` validated on 348 arXiv papers fetched **after** the rule was designed, sha256-pinned, disjoint by content hash | 3 | `eval/strokegrid.md:186-191`; `docs/NEXT.md:38-42` | ✅ |
| C-23 | 17 effective drops, 17 correct, labelled blind by 3 independent labellers who saw only the PNG | 3 | `eval/strokegrid.md:193-206`; `docs/NEXT.md:40-41` | ✅ |
| C-24 | known failure mode: a booktabs table continued across pages is indistinguishable from a template | 3 | `eval/strokegrid.md:217-233` | ✅ |
| C-25 | the 18th drop was found by diffing the implementation against the analysis script, not by the script | 3 | `eval/strokegrid.md:243-250`; `docs/NEXT.md:116-118` | ✅ |
| C-26 | the "free win" — "6 wasted calls, 100% precision, no new constant" — was six pages of one document | 1, 2, 3(implied), 4 | `eval/rejected-signals.md:91-123`, esp. `:100-107`; `docs/NEXT.md:45-50,119-121` | ✅ |
| C-27 | it sat in the notes as a recommendation for two sessions | 1, 2, 4 | `docs/NEXT.md:120-121` ("It sat in this file as a recommendation for two sessions") | ✅ |
| C-28 | 54.1% of routed rasters sit on pages with more than one raster | not used in final drafts | `eval/rejected-signals.md:171-175` | ✅ (available if a draft is expanded) |

## D. Negative results — branding

| # | claim | drafts | source | verdict |
|---|---|---|---|---|
| C-29 | twelve branding signals measured, one shipped, eleven not kept | 1, 2, 3, 4 | `eval/tds-corpus.md:207-211`; `README.md:162,366-368`. Precisely: ten rejected outright, one shipped, one shipped-then-reverted. Drafts say "one shipped" / "eleven were not kept", which matches | ✅ |
| C-30 | the labelled set is 382 raster firings — 49 branding, 5 portrait, 328 content — classified by eye | 1, 2, 3 | `eval/tds-corpus.md:89-92`; `tests/raster-labels.tsv` | ✅ |
| C-31 | two signals were flawless on the set they were fitted to, then lost real content out of sample | 1, 2, 3 | `eval/tds-corpus.md:124-125,144-160`; `README.md:374-378` | ✅ |
| C-32 | the top-of-page rule scored 17 hits / 17 branding / precision 1.00 on 382 items, then dropped a tile of arXiv `2607.29107v1` Figure 1 | 1, 2 | `eval/tds-corpus.md:144-157` | ✅ |
| C-33 | the QR detector selected 5 of 5 QR codes and nothing else across 1,524 raster firings, shipped, then was reverted | 1, 2, 3, 4 | `eval/tds-corpus.md:171-198` | ✅ |
| C-34 | it was reverted because two arXiv documents went **up**, 4→8 and 4→9 calls, having matched 19 further images the sweep never saw because page renders subsumed them | 1, 2, 3, 4 | `eval/tds-corpus.md:179-184` | ✅ |
| C-35 | branding is separable from a figure only by reading it, which is the call being avoided | 1, 2, 3 | `eval/tds-corpus.md:212-217`; `README.md:374-376` | ✅ |
| C-36 | residual branding is 3.4% of vision calls (12.8% of raster firings, 2.8% of raster tokens), median 140 tokens against 878 | 2 | `eval/tds-corpus.md:102-105,220-222`; `README.md:372-373` | ✅ |
| C-37 | soft-mask suppression rejected at −0.013% for ~40 ms/document | not used in final drafts | `eval/rejected-signals.md:12-49` | ✅ (available) |

## E. Defects found in the measurement code

| # | claim | drafts | source | verdict |
|---|---|---|---|---|
| C-38 | three defects in the skill, six in the measurement code, across two sessions | 1, 2, 3, 4 | `docs/NEXT.md:100-108` | ✅ |
| C-39 | none was caught by tests; every one flattered or distorted a published number | 1, 2, 4 | `docs/NEXT.md:107-108` | ✅ |
| C-40 | answer key had the correct option at C fourteen times in thirty | 2, 3, 4 | `docs/NEXT.md:105`; `eval/figqa.md:266-271` | ✅ |
| C-41 | a scorer read the wrong column and reported 0% on a set that was unanimously clean | 2, 3, 4 | `docs/NEXT.md:105-107`; `eval/strokegrid.md:274-279` | ✅ |
| C-42 | a harness handed the arm one routed item per page when the pipeline routes several, and on one page withheld an entire page render | 2, 3, 4 | `eval/figqa.md:304-322`; `README.md:279-283` | ✅ |
| C-43 | the first run scored 20/23 and the write-up blamed the routing; two of the three misses were that bug | 2, 3 | `eval/figqa.md:306-320`; `README.md:279-282` | ✅ |
| C-44 | a validation script blind to a code path under-reported a drop set by exactly the one item that mattered | 2 | `docs/NEXT.md:106-107`; `eval/strokegrid.md:243-250,279-281` | ✅ |

## F. Accuracy

| # | claim | drafts | source | verdict |
|---|---|---|---|---|
| C-45 | 40 candidates, 23 admitted, doc-extract 22/23 | 2, 3, 4 | `eval/figqa.md:326-337`; `README.md:245-256,260`; re-derived from `eval/figqa/v3/admitted.json` (`n_candidates` 40, `n_admitted` 23) | ✅ |
| C-46 | admission requires: full page render answers it, closed-book fails under **two** orderings, text-only cannot ground it | 2, 3, 4 | `eval/figqa.md:172-177`, `:288-296`; `README.md:258-261` | ✅ |
| C-47 | three of the four arms are forced by the gate; only the routed arm measures anything | 2, 3, 4 | `eval/figqa.md:326-337`; `README.md:263-266` | ✅ |
| C-48 | full optical answered 40/40 of the candidates, all grounded | 2(implied), 3 | `eval/figqa.md:332-335`; `README.md:260-261` | ✅ |
| C-49 | closed-book 0/23, text-only 9/23 with 0 grounded | 2 | `eval/figqa.md:327-330` | ✅ |
| C-50 | 23 questions from 16 pages | 3 | `README.md:423-427`; re-derived: `eval/figqa/v3/admitted.json` has 23 entries over 16 distinct `page_img` values | ✅ |
| C-51 | the one genuine miss is a page holding two drawings where only the upper is routed | 2(implied), 3(implied) | `eval/figqa.md:339-347`; `README.md:252-255` | ✅ |
| C-52 | on scanned pages the extractor returns zero characters; 0% → 61.5% on olmOCR `old_scans` presence tests | 2, 3 | `eval/oldscans.md:6-22`; `README.md:207-215` | ✅ |
| C-53 | that result is n=11 documents | 2, 3 | `eval/oldscans.md:11,41`; `README.md:215` | ✅ |
| C-54 | opendataloader-bench 0.875 overall / 0.915 NID / 0.814 TEDS, identical to pdf-inspector, not an improvement | 1, 2 | `README.md:219-231`; `eval/opendataloader.md:16-27` | ✅ |
| C-55 | ranks 5th of 15 against the benchmark's full engine set | 2 | `README.md:224-230`. Note the README's own caveat: the competitor figures come from the published leaderboard, not a run in this repo. Draft 2 states the rank without attributing the competitors' numbers to this repo | ✅ |
| C-56 | the text path is byte-identical; `eval/gate.py` runs the real pipeline and asserts stripped output equals raw `process_pdf` output | 1, 3 | `README.md:130-133,230-231`; `eval/opendataloader.md:9-13` | ✅ |

## G. Office documents

| # | claim | drafts | source | verdict |
|---|---|---|---|---|
| C-57 | routing saves 1.9% of vision tokens on Office, against 2.4× on PDFs | 2, 3, 4 | `README.md:428-433`; re-derived from `docs/benchmarks/results/office.json`: `unfiltered_tok` 1,037,713 → `ours_tok` 1,017,845 = **1.915%** | ✅ |
| C-58 | 236-document corpus | 2, 3 | `README.md:293-297`; `office.json` `files_ok` 236 | ✅ |
| C-59 | no page render to avoid, so the only lever is filtering embedded images, most of which are content | 2, 3, 4 | `README.md:308-313,428-433` | ✅ |
| C-60 | a slide deck costs roughly one vision call per slide | 2, 3 | `README.md:303,316-318`; `office.json` pptx `calls_per_unit` 1.271 | ✅ |
| C-61 | spreadsheet charts are read from the chart definition at zero vision cost, 19 of 20 recovered across 35 workbooks | 3 | `README.md:323`; `office.json` xlsx `charts_ok` 19, `charts_unread` 1, `files` 35 | ✅ |

## H. Product description and mechanics

| # | claim | drafts | source | verdict |
|---|---|---|---|---|
| C-62 | extracts text with `pdf-inspector` and `anydoc`; routes only failed pages to the agent's own vision | 1, 2, 3, 4 | `README.md:17-22`; `skills/doc-extract/SKILL.md:7-13` | ✅ |
| C-63 | no API key, no per-page bill, no upload | 1, 2, 3, 4 | `README.md:21-22` | ✅ |
| C-64 | reads PDF, Word, Excel, PowerPoint and images | 1, 3 | `README.md:21`; `SKILL.md:11-13` | ✅ |
| C-65 | routing reads the page's drawing operators (vector geometry), not just text presence | 1, 2, 3 | `README.md:141-146,340-342`; `skills/doc-extract/harvest.py` | ✅ |
| C-66 | MIT licence | 1, 3, 4 | `LICENSE`; `README.md:8` | ✅ |
| C-67 | repo URL is `github.com/LPSlv/doc-extract` | 1, 2, 3, 4 | fetched 2026-08-13, resolves to `LPSlv/doc-extract`, description matches. Repo was renamed from `pdf-extract`; the drafts use the current name only | ✅ |
| C-68 | `pdf-inspector` and `anydoc` are Rust, MIT, and do no OCR/vision | 1, 3 | fetched 2026-08-13: pdf-inspector describes itself as "Fast Rust library … all without OCR"; anydoc as a "Fast Rust library that converts documents … into clean GFM" with no OCR in the library | ✅ |
| C-69 | Firecrawl Parse comparison is a billing-model comparison, not a quality one | 1 | `README.md:351-354` | ✅ |
| C-70 | quick-start command runs and prints an artifact plus a `pending` list | 1, 3 | `README.md:47-56`; `SKILL.md:24-40` | ✅ |
| C-71 | `eval/readme_tables.py --write` regenerates the README cost tables, which are not hand-edited | 2, 3 | `README.md:475,478-482`; `eval/readme_tables.py:4-7,117-127`; re-ran without `--write` and the output matches `README.md:183-202` and `:297-305` | ✅ |
| C-72 | pinning is uneven: six olmOCR corpora sha256-pinned per file; arxiv/bills/datasheets/pmc URLs without hashes; `papers` has no manifest | 2, 3 | `README.md:175-179`; arXiv holdout pinning at `eval/strokegrid.md:187-191` | ✅ |
| C-73 | Firecrawl Discussions exist on `firecrawl/firecrawl` with a "Show and tell" category; `pdf-inspector` and `anydoc` have no Discussions tab | 1 (venue note) | fetched 2026-08-13 | ✅ |

---

## Incidental findings, not used in any draft

Recorded because they were noticed while checking the above, and someone should
decide what to do with them. **No existing file was edited by this work.**

1. **`README.md:27` and `:349`, `docs/NEXT.md:12` — "0.34 vision calls per
   page" is stale.** See C-05. The value is 0.33 after `boxed_text` shipped.
   This is hand-carried prose sitting outside the `benchmarks:` markers, which
   is exactly the class of number `README.md:478-482` warns is carried by hand.
2. **`eval/figqa.md:43` and `eval/figqa_text.py:11-14` — "3 of these 30
   documents" does not reproduce.** See C-14. Measured 1 of 30 today at the
   pinned engine version.
3. **`eval/datasheets.md` contradicts itself on one figure.** Line 35 and line
   48 give doc-extract's total as **1,084,905** tokens (33% less than
   1,626,152); line 79 gives the same comparison as "1,626,152 → **668,054**"
   removing 958,098 tokens. Both cannot be right. No draft cites either number.
4. **`docs/superpowers/specs/2026-08-03-doc-extract-skill-design.md:154-157`**
   is load-bearing for a public claim and has no artifact behind it. See C-15.

## How the re-derivations were done

Read-only. No file outside `docs/launch/` was created or modified, nothing was
posted, published or sent anywhere.

- Aggregates in section A: summed `docs/benchmarks/results/*.json` directly, and
  separately ran `uv run eval/readme_tables.py` (no `--write`) and compared its
  output against the README's marker blocks.
- C-14 and C-16: a throwaway script in the session scratchpad ran
  `pdf_inspector.process_pdf()` and `pdf_inspector.extract_pages_markdown()` at
  version 0.2.6 over the 30 documents listed in `eval/figqa/candidates.json` and
  over `corpus/tds/irlz44n_infineon.pdf`, reading from `corpus/` only.
- C-45, C-50: read `eval/figqa/v3/admitted.json` and counted.
- C-57, C-58, C-60, C-61: read `docs/benchmarks/results/office.json`.
- C-67, C-68, C-73: read-only web fetches of the three GitHub repos and the
  Firecrawl discussions index.

---

## Addendum — re-verified 2026-08-14 at `87570d6`, before posting

The drafts were written at `687818a`. `textonly_page` shipped after that and all
twelve results JSONs were re-run, so the cost figures moved. Nothing was posted
in the interim, which is the only reason this is a correction to a draft rather
than a correction to a public claim.

**Cost figures, re-derived by running `uv run eval/readme_tables.py` (read-only)
and diffing against the README's marker blocks — they regenerate
byte-identically:**

| # | was in the drafts | is now | note |
|---|---|---|---|
| C-04 | routed 20.1M | **19.9M** | after `textonly_page` |
| C-05 | 0.33 calls/page | **0.32** | 6,525 ÷ 20,375 = 0.3202 |
| C-06 | 2.4× cheaper | **2.5×** | 48.9M ÷ 19.9M |
| C-57 | Office 1.9% "against 2.4× on PDFs" | against **2.5×** | the 1.9% itself is unchanged |

C-01, C-02, C-03, C-08, C-09 are unchanged. Per corpus the range is still 7.0×
(`bills`) down to 0.9× (`olmocr_long_tiny_text`), and that row is still last.

**One stale figure was found in the README while checking this and fixed:**
`README.md:198`, the *heading* of the cost section, still read "costs 2.4× less"
while the generated table three lines below it read 2.5×. Same class as the
0.34 → 0.33 → 0.32 rot `docs/NEXT.md:22-30` documents: hand-carried prose
outside a marker block, in this instance the most visible line in the section.

**The defect tally moved, in the direction that matters:** three sessions, **four**
defects in the skill and six in the measurement code, not three and six
(`docs/NEXT.md:333-341`). The fourth is filter 3, and the reason it went uncounted
is worth the space the drafts now give it — a filter that suppresses a call
produces no artifact, and every eval here samples the routed set.

**Material that landed after the drafts and is now in them:**

| claim | drafts | source |
|---|---|---|
| `textonly_page` shipped: 203 blind drops over two after-the-fact holdouts, 0 real items, Wilson 97–100 | 2, 3 | `eval/nofigure.md`; `docs/NEXT.md:126-137` |
| the `curves` rule died on a purpose-built holdout: 295 datasheets, 11 vendors, none above 19%, 80% precision (Wilson 72–86), 24 real figures lost, 98% TI / 66% others, plus a cascade of 46 returning rasters | 2, 3, 4 | `eval/curves-holdout.md`; `docs/NEXT.md:139-146` |
| filter 3 skips 8,295 pages, 4,065 with no raster; 65.6% of 250 blind labels carry a figure (60–71); discarded `curves` pages 70% vs paid-for 73% | 2, 3, 4 | `eval/filter3.md`; `docs/NEXT.md:195-201` |
| harm, not exposure: 65 questions, optical 65/65, status quo 61/65, fix 64/65 → 4.6% of answers (2–13); grounding 41/65 vs 62/65 → 32.3% (22–44); `printed` facts 0 of 30 lost, all four losses `geometry` | 2, 3, 4 | `eval/filter3_harm.md`; `docs/NEXT.md:242-258` |
| full fix costs +3,911 calls and +64% routed image tokens, taking 2.5× to ≈2.05× | 2, 3 | `eval/filter3.md:13-14,262`; `docs/NEXT.md:379` (the corrected denominator — 2.25× → 1.85× is the five-corpus figure, not the headline) |
| closed-book scores 72% on that question set, so 4.6% is a floor and 32.3% nearer a ceiling | 2, 3 | `eval/filter3_harm.md`; `docs/NEXT.md:259-262` |
| three holdout corpora exist, each fetched after the rule it tested, each verified disjoint by content hash | 2, 3, 4 | `docs/NEXT.md:51-56` |
| the 42% is the branch as measured *before* `boxed_text`; over 188 labelled firings the rule cuts 52 and costs 3 | 3 | `eval/strokegrid.md`; `docs/NEXT.md:71-83` |

**Stale asks removed.** Drafts 2, 3 and 4 all closed by asking for a
boilerplate-heavy holdout corpus. That corpus now exists — it is
`corpus/datasheet_holdout`, and it killed the rule it was built for. The asks now
point at the two failure modes that are genuinely open: vendor boilerplate, where
recurrence rather than lattice shape is the only lever anyone has proposed, and
tables continued across pages, where both obvious discriminators were measured
and both failed.

**Re-run today, unchanged, because it is the one claim in the set about somebody
else's code:** at pdf-inspector 0.2.6 over the 30 documents in
`eval/figqa/candidates.json` — 1 of 30 all-empty, 8 of 30 with at least one empty
page, 20 of 624 pages (3.2%), `process_pdf` empty on 0 of 30, `main.PMC9937890.pdf`
4 of 4 pages empty against 18,398 characters, and `irlz44n_infineon.pdf` giving
`[0, 0, 801, 759]` against 7,559. Every figure in draft 1 reproduces exactly.

**Verification state at `87570d6`:** 146 tests pass, `eval/gate.py` 16/16
byte-identical over 8 documents × 2 description placements, `tests/check_sync.py`
in sync, both README marker blocks regenerate byte-identically.
