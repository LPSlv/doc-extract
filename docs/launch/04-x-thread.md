# Draft 4 — X thread

**Status: DRAFT. Not posted.**

**Format:** 13 posts. Every post is under 280 characters as counted below.
X counts any URL as 23 characters regardless of its real length; post 13 is
under the limit either way, so no post depends on that concession.

Attach `docs/img/filter-cascade.png` to post 8 and `docs/img/benchmark.png` to
post 9 if images are wanted. Neither is required for the text to make sense.

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

Running tally, two sessions:

3 defects found in the tool.
6 found in the code that measures the tool.

An answer key with the right option at C 14 times in 30. A scorer reading the
wrong column. A harness that hid a page render from the arm under test.

None caught by tests.

---

**8/**

OK, what it is.

Text extraction handles most documents and silently drops every chart, scan and
merged-header table.

Looking at every page catches all of it at 3.6x the cost.

doc-extract extracts text locally, then sends only the pages extraction
provably lost.

---

**9/**

2,342 PDFs. 20,375 pages. 12 corpora chosen to be unlike each other.

read every page: 48.9M input tokens
text only (blind): 13.6M
routed: 20.1M

2.4x cheaper than looking at everything, at 0.33 vision calls per page.

No OCR API. No per-page bill. Nothing uploaded.

---

**10/**

Per corpus it runs 7.0x down to 0.9x.

0.9x means it LOSES: 62 single-page documents where text plus one figure render
costs more than the page itself. Nothing amortises.

That row stays in the table, in sort position. Not a footnote.

---

**11/**

Does the description carry the figure? No public benchmark scores this, so I
built one. 40 questions, admitted only if the page answers it and both blind
arms fail it. 23 admitted, 22 correct.

Discount it: 3 of the 4 arms are forced by the gate. Only one measures anything.

---

**12/**

And where it doesn't work.

On Word/Excel/PowerPoint the routing saves 1.9% of vision tokens. Not 2.4x.

There's no page render to avoid, so the only lever is filtering embedded
images, and most of those are content.

That's in the README's heading, not its footnotes.

---

**13/**

MIT. No API key. Uses whatever vision your agent already has.

github.com/LPSlv/doc-extract

If you have a boilerplate-heavy PDF corpus — vendor datasheets, journal
back-issues — I want one. Half my routing waste has no working rule and no
holdout to test one on.
