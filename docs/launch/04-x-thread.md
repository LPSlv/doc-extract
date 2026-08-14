# Draft 4 — X thread

**Status: DRAFT. Not posted.**

**Format:** 18 posts. Every post is under 280 characters as counted below.
X counts any URL as 23 characters regardless of its real length; post 18 is
under the limit either way, so no post depends on that concession.

Attach `docs/img/filter-cascade.png` to post 13 and `docs/img/benchmark.png` to
post 14 if images are wanted. Neither is required for the text to make sense.

Posts 8–11 are the strongest material here and the thread can be cut to eight by
keeping 1, 2, 6, 8, 10, 13, 14, 18 if 18 reads as too long.

---

**1/**

Every document-extraction tool claims a multiplier.

Almost none publishes the eval that didn't work.

So here is mine first: the weakest branch of my PDF router is 42% waste, and I
know the number because I labelled all 170 of its firings by hand.

🧵

---

**2/**

The branch fires when a page has straight strokes running both ways — meant to
catch ruled tables and marker plots.

170 firings, 711 documents, every one rendered and classified by eye:

38% tables
6% plots
14% other real figures
42% nothing at all

---

**3/**

The 6% deserves its own post.

That branch is justified in the code as catching "either a marker/tick-based
plot or a ruled table."

Plots: 10 firings out of 170. Five of them in one corpus.

It's a table-catcher. The plot rationale is dead weight and the README says so.

---

**4/**

Then there's branding. Mastheads, society logos, conference banners fire as
figures.

Twelve signals measured to stop it. One shipped.

The two best were flawless on the 382-item set they were fitted to, then lost
real content on corpora they hadn't seen.

---

**5/**

My favourite: a QR-code detector.

Selected 5 of 5 QR codes and nothing else across 1,524 firings. Every drop
checked by eye. Shipped.

Reverted when the diff showed two documents going UP in cost. It had matched 19
images the audit never saw, hidden behind page renders.

---

**6/**

A rule sat in my notes for two sessions as:

"6 wasted calls removed. 100% precision. No new constant."

Every word true.

All six were pages 2-7 of ONE document.

"100% precision" over n=1 formats identically to "95% over n=55" in a summary
table. That's the danger.

---

**7/**

The cure is a holdout built before you trust the number — and it has to be the
right kind of holdout.

A rule read 17/17 in-sample. That corpus was 75% one vendor.

So: 295 datasheets, 11 vendors, none over 19%.

80%. 24 real figures lost. 98% on TI, 66% on everyone else.

---

**8/**

The largest loss here was never a routing rule. It was a filter.

Parse a pipe table anywhere on a page → skip the page. 8,295 pages. 4,065 with
no image at all, so nothing about them was routed OR counted.

A suppressed call leaves no artifact to audit.

---

**9/**

Every eval I had samples the routed set. So all of them were blind to this by
construction.

65.6% of 250 blind-labelled skipped pages carry a real figure.

Pages the filter discards: figures at 70%.
Pages the router pays for: 73%.

The only difference is whether a table parsed.

---

**10/**

Then I measured harm instead of exposure.

65 questions on those pages. Optical control 65/65. Pipeline as it ships, 61/65.

The fix recovers 3 answers. Not what 65.6% implies.

A vector figure's own text survives extraction: 0 of 30 printed-label questions
lost.

---

**11/**

What it discards is shape, not words. All 4 real losses were readings taken off a
plotted curve.

Every benefit here was measured in a proxy. Every cost in exact tokens.

That asymmetry always favours doing nothing. Fixing it costs +64% image tokens.
Unfixed, and written up.

---

**12/**

Running tally, three sessions:

4 defects found in the tool.
6 found in the code that measures the tool.

An answer key with the right option at C 14 times in 30. A scorer reading the
wrong column. A harness that hid a page render from the arm under test.

None caught by tests.

---

**13/**

OK, what it is.

Text extraction handles most documents and silently drops every chart, scan and
merged-header table.

Looking at every page catches all of it at 3.6x the cost.

doc-extract extracts text locally, then sends only the pages extraction
provably lost.

---

**14/**

2,342 PDFs. 20,375 pages. 12 corpora chosen to be unlike each other.

read every page: 48.9M input tokens
text only (blind): 13.6M
routed: 19.9M

2.5x cheaper than looking at everything, at 0.32 vision calls per page.

No OCR API. No per-page bill. Nothing uploaded.

---

**15/**

Per corpus it runs 7.0x down to 0.9x.

0.9x means it LOSES: 62 single-page documents where text plus one figure render
costs more than the page itself. Nothing amortises.

That row stays in the table, in sort position. Not a footnote.

---

**16/**

Does the description carry the figure? No public benchmark scores this, so I
built one. 40 questions, admitted only if the page answers it and both blind
arms fail it. 23 admitted, 22 correct.

Discount it: 3 of the 4 arms are forced by the gate. Only one measures anything.

---

**17/**

And where it doesn't work.

On Word/Excel/PowerPoint the routing saves 1.9% of vision tokens. Not 2.5x.

There's no page render to avoid, so the only lever is filtering embedded
images, and most of those are content.

That's in the README's heading, not its footnotes.

---

**18/**

MIT. No API key. Uses the vision your agent already runs.

github.com/LPSlv/doc-extract

The one I couldn't crack: a table continued across pages repeats its geometry,
same as a template. Containment and consecutiveness both dead.

Three holdout corpora in the repo if you want a go.
