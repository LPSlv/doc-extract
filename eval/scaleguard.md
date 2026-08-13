# `over_scale_guard` after `textonly_page`

`SCALE_GUARD = 15` is the number of vision calls above which the skill stops
and asks the user before proceeding — the only routing decision a user sees
*before* the calls happen. `drop_textonly` (`eval/nofigure.md`) removed 272
page renders across the design corpora, so some documents necessarily crossed
that threshold. `docs/NEXT.md` §2 recorded the flips as uncounted. This counts
them.

## Result

**10 documents of 2,342 flip from `over_scale_guard: true` to `false`.** No
document flips the other way, and none can: `drop_textonly` only ever removes
items, so the routed set is monotone non-increasing.

| | documents |
|---|--:|
| PDFs in the twelve corpora | 2,342 (2 unreadable, skipped) |
| touched by `drop_textonly` at all | 76 |
| `over_scale_guard` before the rule | 145 |
| `over_scale_guard` today | 135 |
| **flipped true → false** | **10** |

0.43% of all documents; **6.9% of the 145 that used to stop and ask**; 13% of
the 76 the rule touches. 119 vision calls that would have been announced are
now made silently — the ten documents' post-rule call counts, which run from 7
to 15.

| document | pages | calls before → after |
|---|--:|--:|
| `pmc/gkae711.PMC11417360.pdf` | 16 | 16 → 7 |
| `pmc/13287_2025_Article_4518.PMC12296610.pdf` | 16 | 16 → 9 |
| `papers/rob_diffusion-policy.pdf` | 18 | 18 → 11 |
| `arxiv/2607.28965v1.pdf` | 23 | 23 → 12 |
| `arxiv/2607.28736v1.pdf` | 17 | 17 → 12 |
| `papers/rob_pi0.pdf` | 17 | 17 → 12 |
| `arxiv/2607.29510v1.pdf` | 19 | 19 → 13 |
| `arxiv/2607.29568v1.pdf` | 21 | 21 → 14 |
| `arxiv/2607.29500v1.pdf` | 17 | 17 → 14 |
| `pmc/main.PMC11292527.pdf` | 21 | 21 → 15 |

All ten are `cost_guard` collapses — every remaining call is a
`whole_document` render — which is the only place `drop_textonly` runs, so
"calls before" is exactly the page count in each case.

## Is the new behaviour better?

**Better, and the labels say so on these specific documents.** A document that
no longer stops to ask is a document the user is no longer warned about, so the
question is what the ten now spend silently.

`eval/nofigure/labels.tsv` already carries 16 blind labels on
`whole_document` pages of these ten files. Split by what the rule did with
them:

| | figure | table | branding | none |
|---|--:|--:|--:|--:|
| dropped as `textonly_page` | 0 | 0 | 0 | **4** |
| still routed | 8 | 3 | 1 | 0 |

Every labelled page the rule removed was labelled `none` (references lists,
plain prose), and every labelled figure and table survived. The one surviving
waste page is `13287_2025_Article_4518` p1, a BMC title page — `branding`,
which `eval/nofigure.md` already records as unreachable by geometry.

So the calls these documents still make are, as far as the existing labels
reach, calls a user would have approved; the ones they no longer make are the
ones a user would have wished away. The routed set only shrank, and it shrank
by removing the junk, so no document approves anything today that it would not
have approved before — the change is that ten documents stop asking about a
smaller and better set.

The honest counterweight: `SCALE_GUARD` is a cost-consent threshold, not a
content check, and 15 is arbitrary. A user who wanted to be consulted about 16
calls plausibly wanted to be consulted about 15. This did not move the
threshold, but it moved ten documents across it without anyone deciding to, and
the guard now fires on 6.9% fewer documents than the README's behaviour
description implies it did.

## Provenance

Every number here comes from `eval/scaleguard.py`, which harvests each PDF and
reads two facts off the result: `vision_calls`, and how many entries in
`dropped` carry `why == "textonly_page"`. `drop_textonly` is the last mutation
`harvest()` makes to `items`, so *calls before* is `calls_after + n_textonly`
exactly, not a model.

Checks run, because this repo's measurement code is where its defects have
been:

- **The counterfactual was re-run, not assumed.** `--recheck` monkeypatches
  `harvest.drop_textonly` to a no-op and re-harvests all 76 touched documents:
  **0 mismatches** against `calls_after + n_textonly`.
- **Cross-checked against `eval/bench.py`.** Per-corpus document counts, call
  totals and `over_scale_guard` counts agree exactly for ten of the twelve
  corpora. The two that differ, `bills` (227 vs 9) and `datasheets` (3,303 vs
  3,191), are exactly the two where `batch_furniture` fires: `bench.py` mirrors
  `harvest_batch`, while `convert.py` — the path a user runs — harvests one
  document at a time and never applies it. Re-running both corpora at batch
  scope (`--batch`) gives **0 flips** in either, so the count is 10 under both
  conventions.
- **Reproduces the published totals from independent code**: 272 renders
  removed from 76 of 96 collapsed documents across the five design corpora,
  matching `docs/NEXT.md` §2 and `eval/nofigure.md`; 2,342 documents and the
  same two unreadable files `bench.py` skips.

Artifacts: `eval/scaleguard/flips.json` — one row per document with `pages`,
`calls_after`, `n_textonly`, `collapsed`.

## What is not measured here

- **The other 135.** Documents still over the guard were not re-examined; the
  rule changed their call counts too, just not their answer.
- **Whether 15 is the right number.** Unchanged and untested; the threshold has
  never been validated against anything.
- **Only 16 of the 119 remaining calls carry a label.** The judgement above
  rests on those 16 plus `eval/nofigure.md`'s branch-level rates, not on a
  labelling of the flipped documents' full routed sets.
