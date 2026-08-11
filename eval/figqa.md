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

## Limits of this measurement

- n=30 pages, 15 questions. Small.
- Ground truth was authored by the same agent that designed the eval, though
  the arms were run by agents with no access to it and grading is a letter
  match with no judgement at scoring time.
- The routed item for several pages is a whole-page render, so for those pages
  doc-extract and full optical see nearly the same thing; the saving is in the
  pages that are never rendered, not in cheaper looks at the ones that are.
- Selection is one routed page per document, so these rates describe *routed
  pages*, not all pages. Most pages are never routed at all.
