# Draft 2 — Show HN

**Status: DRAFT. Not posted.**

**Venue:** news.ycombinator.com/submit, "Show HN". URL field:
`https://github.com/LPSlv/doc-extract`. The body goes in as the first comment.

**Format note:** HN renders no Markdown. The body below is plain text —
blank-line-separated paragraphs, no bold, no tables, no headers. Keep it that
way when pasting. Bare URLs autolink.

**Title** (76 chars, under HN's 80):

```
Show HN: Doc-extract – vision only on the pages text extraction provably lost
```

---

## Body (paste as the first comment, plain text)

I want to lead with the parts that didn't work, because the parts that did are
the same claim every tool in this space makes.

The weakest routing branch in this thing is 42% waste. I know that because I
rendered all 170 of its firings across 711 documents and labelled every one by
eye: 38% were ruled tables it was supposed to catch, 6% were plots, 14% were
some other real figure it caught by accident, and 42% were nothing at all — a
QR box, a page of LaTeX fraction bars, a Würth title block, four consecutive
pages of a proof. The branch's second stated purpose, marker-based plots,
accounts for 10 firings out of 170. It should not be defended on that basis and
the README says so.

Twelve signals were measured to try to stop the router firing on journal
mastheads and vendor logos. One shipped. Two of the eleven that didn't were
perfect on the labelled set they were fitted to, and then lost real content on
corpora they had not seen — a top-of-page rule scored precision 1.00 on 382
hand-checked items and then dropped a tile of a real arXiv figure; a QR detector
selected 5 of 5 QR codes and nothing else, shipped, and was reverted a day later
when the diff showed two documents going up in cost because it had matched 19
images the audit never saw. Zero false positives is not reachable here, for a
structural reason: a masthead is separable from a chart only by reading it, and
reading it is the call being avoided.

A rule sat in my notes for two sessions as "6 wasted calls removed, 100%
precision, no new constant." Every word was true. All six cuts were pages 2-7 of
one document. "100% precision" over n=1 formats identically to "95% precision"
over n=55 in a summary table, which is the whole danger.

The cure for that is a holdout you build before you trust the number, and it has
to be a holdout of the right kind. The biggest single saving on the table was a
rule to stop the busiest branch firing on vendor boilerplate. In-sample it read
17 of 17. So I fetched 295 datasheets across eleven vendors, none above 19% of
the corpus, because the corpus it was fitted to was 75% Texas Instruments. It
scored 80% — 98% on TI, 66% on everyone else — and lost 24 real figures. Two
rules did survive that treatment, on corpora fetched after they were designed
and labelled blind by three people each who saw only a PNG: 17 drops and 203
drops, zero real items between them.

The largest content loss in this thing is not a routing branch at all. If the
text extractor manages to parse a pipe table anywhere on a page, the page is
skipped — and 8,295 pages hit that, 4,065 of them carrying no image, so nothing
about them was ever routed *or counted*. A filter that suppresses a call
produces no artifact to audit, and every eval I had samples the routed set, so
all of them were blind to it by construction. 65.6% of 250 blind-labelled skipped
pages carry a real figure. The damning comparison is not that number, it is that
the pages this filter discards carry figures at 70% while the pages the router
happily pays for carry them at 73%.

Then I measured what it actually costs in answers rather than in exposure, which
is the mistake I had been making everywhere: 65 screened questions on 65 of those
discarded pages. An optical control answers 65. The pipeline as it ships answers
61. The fix recovers 3 of the 4 it loses — 4.6% of the sample, not the disaster
the 65.6% implies — because a vector figure's own text survives extraction, and
0 of 30 questions about printed labels were lost. All four real losses were
readings taken off a plotted curve. What it discards is shape, not words. The
honest case for fixing it is citation recovery — 41 of 65 groundable against 62 —
and it is an order of magnitude weaker than the exposure figure suggests. Fixing
it in full costs +3,911 vision calls and +64% of routed image tokens, which takes
the 2.5x headline to about 2.05x, so it has not been fixed, and the reasoning is
in the repo rather than in my head. Every
benefit number in this repo was in a proxy while every cost number was in exact
tokens, and that asymmetry silently favours doing nothing.

Across three sessions I found four defects in the skill and six in the code that
measures it: a harness that withheld routed items from the arm under test, a
circular gate, a contaminated question, an answer key with the correct option at
C fourteen times in thirty, a scorer that read the wrong column and reported 0%
on a set that was unanimously clean, and a validation script blind to a code
path, which under-reported a drop set by exactly the one item that mattered.
Every one of those flattered or distorted a number I had already written down.
None was caught by tests.

So: what it is. Text extraction handles most documents fine and silently drops
every chart, scanned page and merged-header table. Looking at every page with a
vision model catches all of it and costs 3.6x what text extraction does.
Doc-extract extracts text with pdf-inspector and anydoc, works out which pages
the extractor actually failed on by looking at the page's drawing operators, and
sends only those to the vision of whatever agent is already running it. There is
no OCR service in the loop and no per-page bill.

Across 2,342 PDFs and 20,375 pages in twelve deliberately dissimilar corpora
(datasheets, arXiv, PMC, US legislation, six olmOCR-bench page classes): reading
every page costs 48.9M input tokens, text alone costs 13.6M and is blind,
doc-extract costs 19.9M at 0.32 vision calls per page. That is 2.5x cheaper than
reading everything. One corpus, 62 single-page documents, comes out 0.9x — it
loses, because a single page has nothing to amortise, and it stays in the table
in sort position.

Accuracy is the harder claim and the eval for it is the thing I would most like
torn apart. There is no public benchmark for figure-description accuracy on
text-bearing PDFs, so I built one: 40 candidate questions, admitted only if
rendering the whole page answers it, a closed-book model fails it under two
different option orderings, and a text-only model cannot ground it in the
extracted markdown. 23 survived. Doc-extract got 22. The full-page-render arm
got 23/23 and the closed-book arm 0/23 — but both of those are forced by the
admission rule, so three of the four rows in that table are gate calibration and
only one measures anything. The first run of it scored 20/23 and I wrote up the
routing as the cause. Two of the three misses were a bug in my harness: it
handed the arm one routed item per page when the pipeline routes several, and on
one page it withheld an entire page render and then counted its absence against
the router.

Where it genuinely wins is scanned pages, where the text extractor produces zero
characters: 0% to 61.5% on olmOCR-bench old_scans "present" tests. That is n=11
documents. On native-text PDFs it changes nothing on purpose — through
opendataloader-bench's evaluator it scores 0.875, which is pdf-inspector's own
number, and against that benchmark's full engine set it ranks 5th of 15.

Known and documented: single-page documents can lose. A page can hold more
figures than the router emits, which is the one genuine miss above. Branding
still costs about 3.4% of vision calls. On Office documents the routing saves
1.9% of vision tokens rather than 2.5x — there is no page render to avoid, so
the only lever is filtering embedded images and most of those are content. A
slide deck costs roughly one vision call per slide. The cache, the citations and
the spreadsheet-chart extraction are the reasons to use it there; the routing
is not.

Every number above is regenerable. `eval/readme_tables.py --write` rebuilds the
cost tables in the README from the raw JSON and the README is not hand-edited
between the markers. Corpus manifests are in `eval/manifests/`, and the pinning
is uneven in a way that is documented: the six olmOCR corpora and the three
holdouts are sha256-pinned per file, arxiv/bills/datasheets/pmc ship URLs without
hashes, and one corpus has no manifest at all.

https://github.com/LPSlv/doc-extract

Two things I would especially like. Someone to point out where the figure-QA set
is selected toward what my own describer happens to capture — it is 23 questions
from 16 pages and I built both sides of it, which is exactly the position from
which you cannot see your own selection. And an idea for the failure mode I could
not solve: a table continued across pages repeats its geometry page after page,
which is indistinguishable from a template, and the two obvious discriminators
(does the frame contain the strokes, are the pages consecutive) were both measured
and both dead — the second one had its premise backwards.
