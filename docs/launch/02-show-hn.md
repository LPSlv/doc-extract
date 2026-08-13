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

Across two sessions I found three defects in the skill and six in the code that
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
doc-extract costs 20.1M at 0.33 vision calls per page. That is 2.4x cheaper than
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
1.9% of vision tokens rather than 2.4x — there is no page render to avoid, so
the only lever is filtering embedded images and most of those are content. A
slide deck costs roughly one vision call per slide. The cache, the citations and
the spreadsheet-chart extraction are the reasons to use it there; the routing
is not.

Every number above is regenerable. `eval/readme_tables.py --write` rebuilds the
cost tables in the README from the raw JSON and the README is not hand-edited
between the markers. Corpus manifests are in `eval/manifests/`, and the pinning
is uneven in a way that is documented: the six olmOCR corpora are sha256-pinned
per file, arxiv/bills/datasheets/pmc ship URLs without hashes, and one corpus has
no manifest at all.

https://github.com/LPSlv/doc-extract

Two things I would especially like: someone to point out where the figure-QA set
is selected toward what my describer happens to capture, and a boilerplate-heavy
holdout corpus, because the half of the routing waste that comes from vendor
title blocks and legal pages has no working rule and I could not find a corpus to
test one against.
