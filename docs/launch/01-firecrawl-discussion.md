# Draft 1 — Firecrawl GitHub Discussions

**Status: POSTED 2026-08-14** —
https://github.com/firecrawl/firecrawl/discussions/4307 (Show and tell, #4307).

Posted as written below, with two changes made immediately beforehand: the
opendataloader comparison table was cut (it existed only in a design note and
nothing regenerates it — `00-claims.md` C-15), and the `extract_pages_markdown`
observation was re-run at the pinned 0.2.6 on the day of posting rather than
quoted from the day before. It reproduced exactly: 1 of 30, 8 of 30, 20 of 624,
`[0, 0, 801, 759]` against 7,559.

**Venue:** `https://github.com/firecrawl/firecrawl/discussions`, category
**Show and tell**. Checked 2026-08-13: that Discussions board exists and is
active. `firecrawl/pdf-inspector` and `firecrawl/anydoc` do **not** have
Discussions enabled, so the post goes on the main repo and links out to the two
libraries it is actually about.

**Why this one goes first:** smallest audience, and it carries the one factual
claim in the launch set that is about somebody else's code. If the claim is
wrong, it is wrong in front of ~dozens of people rather than ~thousands.

---

## Title

Show and tell: doc-extract — an agent skill that layers a selective vision pass on pdf-inspector and anydoc

## Body

I built an agent skill on top of `pdf-inspector` and `anydoc` and wanted to
share it here, partly because it is a straightforward "built with your stuff"
post and partly because measuring it turned up two small things about the
`pdf-inspector` Python API that you may want to know.

Repo: https://github.com/LPSlv/doc-extract (MIT)

### What it does, and what it deliberately does not do

`anydoc` and `pdf-inspector` do text. They are explicit that they do not do
OCR or vision, and that is the right call for a Rust extraction library — it
keeps them fast and dependency-free. But it means a chart, a pinout diagram, a
scanned page or a ruled table the parser could not structure comes out as a
caption and a silence.

doc-extract fills exactly that gap and nothing else:

1. `pdf_inspector.process_pdf()` / `anydoc` for text. Authoritative, untouched.
2. A local routing pass over the page's drawing operators works out which pages
   the extractor plausibly lost something on.
3. Only those pages/images go to the vision of whatever agent is running the
   skill — Claude Code, Codex, whatever. No OCR service, no API key, no
   per-page bill on our side.

The text path is byte-identical. Every visual description is wrapped in
strippable delimiters, and `eval/gate.py` runs the real pipeline and asserts
that the stripped output equals raw `process_pdf().markdown` byte for byte.
Through opendataloader-bench's official evaluator the skill scores 0.875
overall / 0.915 NID / 0.814 TEDS — which is *pdf-inspector's* number, not an
improvement, and it is stated that way in the README on purpose.

So this composes with your tools rather than competing with them. To be
explicit about the one place it looks adjacent to a product: hosted Firecrawl
Parse also routes work, and the README's comparison there is a **billing-model**
comparison, not a quality one. Parse's OCR on a scanned page may well read
better than a general agent's; that is unmeasured and not claimed either way.

### The part worth leading with: what didn't work

The reason I am comfortable posting this is not the cost number. It is that
the repo publishes the evals that failed, and there are a lot of them.

- **The weakest routing branch is 42% waste, measured exhaustively.** All 170
  firings of the `stroke_grid` branch across 711 documents were rendered and
  labelled by eye: 38% ruled tables, 6% plots, 14% other real figures, **42%
  nothing at all**. Its second stated purpose — marker-based plots — accounts
  for 10 firings in 170.
- **Twelve branding-detection signals were measured; eleven were not kept.**
  Two of them were *flawless* on the 382-item labelled set they were fitted to
  and then lost real content on corpora they had not seen. A top-of-page rule
  scored precision 1.00 on 382 items, then dropped a tile of arXiv 2607.29107's
  Figure 1. A QR-code detector selected 5 of 5 QR codes and nothing else across
  1,524 raster firings, shipped, and was then reverted when the before/after
  diff showed two arXiv documents going *up* in vision calls — it had matched
  19 images the sweep never saw because page renders subsumed them.
- **A "free win" turned out to be one document.** A rule advertised in our own
  notes as "6 wasted calls removed, 100% precision, no new constant" sat there
  as a recommendation for two sessions. All six cuts were pages 2–7 of a single
  file.
- **Six defects were found in the measurement code**, against four in the
  skill itself. Every one flattered or distorted a published number, and none
  was caught by tests. The fourth skill defect is the largest content loss in
  the thing and nobody was looking for it: a filter that skips a page when a
  pipe table parsed anywhere on it, which suppresses 8,295 pages and leaves no
  artifact behind to audit, so every eval here was blind to it by construction.
  Measured in harm rather than exposure it costs 4.6% of answers and 32% of
  groundable citations on a 65-question set, and the write-up says why it is
  cheaper to leave than to fix.

Full write-ups: [`eval/strokegrid.md`](https://github.com/LPSlv/doc-extract/blob/main/eval/strokegrid.md),
[`eval/rejected-signals.md`](https://github.com/LPSlv/doc-extract/blob/main/eval/rejected-signals.md),
[`eval/tds-corpus.md`](https://github.com/LPSlv/doc-extract/blob/main/eval/tds-corpus.md),
[`eval/figqa.md`](https://github.com/LPSlv/doc-extract/blob/main/eval/figqa.md).

### Two notes on `extract_pages_markdown` vs `process_pdf`

Not a bug report and possibly all working as designed — I may well be holding it
wrong, in which case tell me and I will correct the docs on my side. Both
observations are on **pdf-inspector 0.2.6**, Python bindings.

**1. `extract_pages_markdown` returns empty markdown for pages that
`process_pdf` clearly extracts.** Re-measured on 2026-08-14 across the 30
documents in our figure-QA candidate set (arXiv, PMC, TI/Diodes datasheets;
`eval/figqa/candidates.json`):

| | |
|---|--:|
| pages where `extract_pages_markdown` returns empty markdown | **20 of 624 (3.2%)** |
| documents with ≥1 such page | **8 of 30** |
| documents where *every* page comes back empty | **1 of 30** |

The all-empty document is `main.PMC9937890.pdf` — 4 of 4 pages empty, while
`process_pdf` on the same file returns 18,398 characters.

The cleanest single repro is a datasheet, `irlz44n_infineon.pdf` (Infineon
IRLZ44N):

```python
import pdf_inspector as pi
pages = pi.extract_pages_markdown("irlz44n_infineon.pdf").pages
[len(p.markdown or "") for p in pages[:4]]   # -> [0, 0, 801, 759]
len(pi.process_pdf("irlz44n_infineon.pdf").markdown)   # -> 7559, incl. ~100 table rows
```

Pages 1 and 2 are where that datasheet's parameter tables live. This one has
been stable for us across sessions, so it is probably the best starting point if
anyone wants to look.

**2. A second observation I am deliberately *not* going to give you numbers
for.** When choosing between the two APIs during design I recorded that joined
`extract_pages_markdown` output scored lower than `process_pdf().markdown`
through opendataloader-bench's evaluator, on all three of overall, reading order
and tables. I still have the three-decimal table in a design note.

I am not printing it, because I cannot re-run it: the raw evaluator output was
not kept and nothing in the repo regenerates those numbers. A repo whose whole
pitch is publishing the evals that failed should not lead with a figure it cannot
reproduce. The direction is at least consistent with observation 1 — dropped
pages would depress reading order and tables first — but consistency is not
evidence and I am not presenting it as such. If it would be useful, I will re-run
the comparison properly and post the artifact.

Net effect on our side: `process_pdf().markdown` is the authoritative text path,
and `extract_pages_markdown` is used only for a per-page table cross-check,
where an occasional empty page costs a redundant render rather than lost
content.

### If you want to try it

```bash
git clone https://github.com/LPSlv/doc-extract && cd doc-extract
uv run skills/doc-extract/convert.py example/sample-report.pdf
```

Happy to move any of this to an issue on the right repo if that is more useful
than a discussion thread, and happy to be told that observation 1 is expected
behaviour for a page-oriented API.
