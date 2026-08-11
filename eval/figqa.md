# Figure QA — v1, a calibration run that failed to discriminate

`docs/benchmarks/RESULTS.md` lists, first among the things this repo does not
measure:

> **Figure-description accuracy on text-bearing PDFs.** No public benchmark
> scores it.

Every other number here is a cost number — tokens, vision calls, seconds —
plus a byte-identity gate. This was the attempt to measure whether the visual
layer recovers information that text extraction loses. **It did not succeed,
and the honest result is the instrument, not a score.**

## Method

Candidates were selected mechanically (`eval/figqa_select.py`, seed 20260811):
one routed page per document, sampled from every (document, page) where
harvest.py routes something *and* the page carries ≥400 characters of
extractable text. The text condition matters — without it the set collapses
into `old_scans`, where the baseline scores zero by producing nothing at all
(see `oldscans.md`). 5,088 eligible pairs across 626 of 711 documents; 30
sampled, one per document, spanning arxiv, pmc, datasheets and papers.

Each page was rendered at 200 dpi for ground-truth authoring — deliberately
higher than the pipeline's own render, so the oracle is never better-informed
than the system under test.

Four arms, each run by a **separate agent that never saw this analysis, the
ground truth, or the other arms**:

| arm | sees |
|---|---|
| closed-book | the question and its four options, nothing else |
| text only | `process_pdf` whole-document markdown |
| doc-extract | that markdown, plus a description of the routed visual written by another agent from the pipeline's own PNG |
| full optical | the page rendered at 140 dpi |

Multiple choice, four options, because short free-text answers would be graded
by string match and stray tokens in the extracted text — the bare letters
`C E B` on q03 — would falsely credit the text arm. Random baseline 25%.

The whole-document markdown comes from `process_pdf`, not
`extract_pages_markdown`: the per-page API returns nothing at all on 3 of these
30 documents, and grading against it would have handed the baseline a loss it
had not earned.

## Half the routed pages have nothing on them

Before any scoring, authoring ground truth required looking at all 30 pages.
Only 15 yielded a fact that a question could be built on:

| outcome | n |
|---|--:|
| figure-only fact exists | 15 |
| **no figure on the page at all** | **11** |
| caption already conveys the figure | 3 |
| duplicates text that extraction already recovered | 1 |

The eleven are not borderline: a journal masthead, two references pages, four
pages of plain two-column prose, an ESD warning icon, Elsevier front matter,
and a references page whose only graphic is an "Access this article online" QR
box.

By routing branch:

| branch | fired | no figure |
|---|--:|--:|
| `stroke_grid` | 3 | **3** |
| `whole_document` | 9 | 4 |
| `curves` | 11 | 4 |
| `standalone_raster` | 6 | **0** |
| `dense_grid` | 1 | 0 |

`stroke_grid` was wrong every time it fired — boxed display equations, Elsevier
front matter, a QR box. `standalone_raster` was right every time. Three
firings is far too few to retune a threshold on, and tuning on the measurement
set would invalidate it, but it names where to look.

## The scores, and why they mean nothing

| arm | correct | |
|---|--:|--:|
| closed-book | 8/15 | 53% |
| text only | 13/15 | 87% |
| full optical | 15/15 | 100% |

Full optical answering 15/15 is the control working: every question really is
answerable from the page, so a miss elsewhere is information loss rather than a
bad question.

Everything else is contamination. **Exactly one question, q07, is failed by
both the closed-book and the text-only arm.** A one-question measurement
surface cannot support a claim.

Three leakage paths, all mine:

1. **Convention.** A SOT-23's lone pin is the collector on every SOT-23 ever
   made. Lateral-flow strips always run sample → conjugate → test → control →
   absorbent. A weight-4 stabilizer takes four CX gates by definition. The
   closed-book arm got eight without opening anything.
2. **Prose restates the figure.** q17's PRISMA count appears as "After removing
   640 duplicates"; q14's amplifier gain appears in a pin table as "5 V/V".
3. **Figure labels survive extraction as loose tokens.** Fig. 10(c)'s axis came
   through as `24 26 28 30 m 32 34 36 38 40`.

Paths 2 and 3 slipped past because questions were checked against the *page's*
text (`view/<id>.txt`) while the arm is graded against the *whole document's*
markdown.

The underlying mistake is conceptual. A question isolates visual information
only if its answer is **arbitrary** — a value that could have been otherwise.
q07 asks for a plotted MSE at a specific clip multiplier, with distractors
spaced closely enough that convention cannot reach it. q03 asks something true
of an entire package family. Both sit on a figure; only one needs it.

## Two bugs the arms found on the way past

Neither needed a score. Both came from making an agent actually look at what
the pipeline hands over — something no existing check does.

### Routed rasters were shipped in the wrong orientation

`convert.py` materialised a raster with `fitz.Pixmap(doc, xref)`, which decodes
the image XObject's own samples and applies nothing else. `ti_drv8825.pdf` p11
draws its motor-control block diagram with a flipped placement, so the PNG went
out **upside down** — `PWM` reading as `ᴡWq`, every pin label inverted. The
describing agent noticed only because it thought to flip the crop.

The byte-identity gate compares markdown and the harvest tests compare routing
decisions, so nothing in the suite had ever looked at an image's pixels.

Fixed in `_raster_pixmap()`: render the image's own rectangle off the page,
which applies the placement matrix by construction — whatever the mechanism
(flipped CTM, `/Decode` array, bottom-up sample order). Guarded by
`tests/test_raster_orientation.py`, and CI now installs PyMuPDF so those tests
actually run; it previously did not, which also left three existing end-to-end
tests silently skipping.

**Prevalence is unmeasured.** `eval/raster_orientation.py` compares each raw
extraction against a page render and flagged 51 of 453 routed rasters, but it
misses the one case confirmed by eye (ratio 0.86, under its threshold): sparse
line art on white looks much the same flipped once thumbnailed. Its output is
biased toward photographs and dense images and should not be quoted as a rate.
The fix does not depend on the rate.

### `standalone_raster` can mask a vector figure on the same page

q21's page carries FIG. 1(a), a large vector schematic of an optical setup, and
a small embedded bitmap — a false-colour fluorescence inset inside the trap.
Routing fired `standalone_raster` on the 519x457 bitmap and emitted it as a
cropped image. Because the item is a raster rather than a page render, the
schematic around it was never rendered, and the only informative figure on the
page is invisible to the pipeline.

This is the failure mode `docs/benchmarks/RESULTS.md` lists as unmeasurable:

> a chart drawn purely with vector strokes has no such witness, so a text page
> whose vector chart was missed is invisible to this suite

The suite's large-raster proxy cannot see it, because the proxy *is* the raster
that fired. Note this pulls against the presence result above: `standalone_raster`
never fired on an empty page (0/6), yet firing can still cost you the figure.
"Precision 6/6" is the wrong summary of that branch.

## What v2 must do

Make the screening a measured property rather than a judgement call. A question
is admitted only if:

- the closed-book arm gets it **wrong** (not reachable by convention), and
- the text-only arm gets it **wrong** (not in the markdown, in prose or as
  loose tokens)

What survives is visual-only by construction. Over-generate — on v1's rates
roughly a third survive, so ~30 candidates yields ~10 admitted questions.

Question style: arbitrary readings with near-miss distractors drawn from the
same figure.

---

# v2 — the screened set, and the number

30 candidates, all arbitrary-value readings with near-miss distractors drawn
from the same figure, over the 15 figures v1 identified. Screened by code, not
judgement (`eval/figqa_v2_screen.py`):

| filter | candidates failing it |
|---|--:|
| ground truth unsound (full optical got it wrong) | **0** |
| reachable by convention (closed-book correct under *both* orderings) | 10 |
| recoverable from the extracted markdown | 12 |
| *(overlap: candidates failing both of the above)* | *4* |
| withdrawn for author contamination | 1 |
| **admitted** | **11** |

These are **not a cascade** — 30 − 10 − 12 ≠ 11, because four candidates fail
both filters. An earlier version of this table implied subtraction and was
wrong.

Full optical scored 30/30 on the candidates, so no question died from a bad
answer key; every drop is a real leakage path.

**v25 was withdrawn after scoring.** Its answer — a bus tick printed `4` where
the datasheet's own convention says `5` — had been volunteered to the question
author in a describer's status report *before* the question was written. The
author learned it from the arm under test. It is recorded in
`figqa_v2_screen.py` with its reason rather than quietly deleted.

## Result

**Descriptions written before these questions existed contained and correctly
grounded 11 of 11 admitted answers**, each quoting the line it came from.

That is the finding. The arm table below is mostly *not*:

| arm | letter score | status |
|---|--:|---|
| full optical | 11/11 | **forced** — admission requires it |
| closed-book, per ordering | 4/12 and 1/12 | **forced** — admission requires failing both |
| text only | 7/12, 0 grounded-correct | grounded-correct is **forced**; the 7 is guessing |
| **doc-extract** | **11/11**, all grounded | the only unconstrained arm |

An earlier draft of this file said doc-extract "matches rendering the page."
That claim is circular: the page-render arm could not have scored anything but
11/11, because scoring 11/11 is how a question got in. Three of four rows
calibrate the gate; one measures something.

Text-only's 7/12 is not recovery either. Eleven of its twelve answers were
ungrounded guesses and the one it claimed to ground was wrong. The 58% is an
artifact of the answer key (below).

### Two discounts on the one real number

**For 9 of the 11, the routed item is a whole-page render** (`p*-render.png`),
so the describer looked at nearly the same pixels as the full-optical arm. The
sharp test — whether describing a *cropped* raster captures the figure — is
n=2 (v10, v29). A blind re-run targeting cropped rasters specifically is the
obvious next step.

**Eleven questions from 8 pages are not 11 independent trials.** v04 and v06
read the x-tick and the y-label of the *same graph*; v13–v15 all come from one
page. Five of eleven are axis-tick or label reads, which one describer habit
answers at once. Effective independent units ≈ 8. That rules out a describer
that misses things; it cannot bound how much a good one misses.

The clearest single case is v30. `text.md` states 526 nm for curve *a* of Fig. 4
and nothing for curve *b*; a text-only reader is not merely uninformed but
actively misled toward the wrong option. The description carried curve *b*'s own
annotation, 530 nm.

## What this does and does not license

It licenses: on a page the router selects, describing what it routes loses
nothing measurable against rendering that page.

It does not license a claim about the whole document. For most of these figures
the routed item *is* a whole-page render, so on those pages doc-extract and
full optical see nearly the same thing at nearly the same cost. The saving is
in the two-thirds of pages never rendered — and v1 measured that saving's
price: 11 routed pages in 30 with no figure at all, plus the vector figure
`standalone_raster` masked on q21.

## Two artifacts that nearly produced a wrong answer

**Answer-position bias.** Of 30 candidates I placed the correct option at C in
14. A guessing arm picks middle options, so closed-book "scored" 8/10 on the
group whose key was 7xC. Defeated by re-running closed-book under a second
deterministic permutation (`v2-perm.json`) and treating a question as
convention-reachable only if it is answered correctly under both. That rescued
10 questions that a single pass would have disqualified.

**Guessing counted as recovery.** The same bias inflated the text arm: its
ungrounded answers ran 11/17 correct against ~4.2 expected. Scoring "in the
text" as *correct **and** grounded* — the arm quotes a snippet — moved the
admitted set from 5 to 12. Grounded claims are trustworthy at 12/13.

Both artifacts pushed in the same direction: throwing away good questions. Had
they gone unnoticed the reported set would have been 5 questions instead of 12,
with no sign anything was wrong.

## Limits of this measurement

- n=30 pages; 15 questions in v1, 12 admitted in v2. Small, and 12 questions
  cannot separate a good visual layer from a very good one — only from an
  absent one.
- The admitted set is drawn from 8 figures, so questions are not independent:
  three come from one page's two bar charts.
- doc-extract scoring 11/11 means the descriptions held every admitted answer
  *on pages the router selected*. Pages the router skips are out of frame by
  construction, and that is where its risk lives.
- **The question author had already seen the describers' output.** v25 was
  withdrawn for a demonstrable instance, but the general risk is unresolved:
  the same agent designed the eval, read the describers' status reports, and
  then wrote the candidates. The question genre — printed ticks, axis labels,
  annotations — is exactly what a systematic describer transcribes, so the set
  may be selected toward what this describer happens to capture. Only a
  re-authoring by an agent that has seen the page renders and nothing else
  settles it. That is running.
- The descriptions are committed (`eval/figqa/arms/*/description.md`) so the
  headline's key input is auditable; the page renders and per-arm text are not,
  being regenerable from `eval/figqa_select.py` and `eval/figqa_artifacts.py`.
- Ground truth was authored by the same agent that designed the eval, though
  the arms were run by agents with no access to it and grading is a letter
  match with no judgement at scoring time.
- The routed item for several pages is a whole-page render, so for those pages
  doc-extract and full optical see nearly the same thing; the saving is in the
  pages that are never rendered, not in cheaper looks at the ones that are.
- Selection is one routed page per document, so these rates describe *routed
  pages*, not all pages. Most pages are never routed at all.
