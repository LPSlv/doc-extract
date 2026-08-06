# Describing what you see

The description replaces the image for every downstream reader. Someone
answering a question from the Markdown alone must not be at a disadvantage.

## Figures

Lead with the type, then the content, then the numbers. Do not editorialise
about what the figure "shows us" or "highlights" — report it.

```
**Figure (grouped bar, p7).** Planned versus actual spend by work package,
2024–2026. X: WP1–WP4. Y: EUR, 0–45 000, gridlines every 10 000.
WP1 planned 40 000 / actual 38 100; WP2 30 000 / 31 500; WP3 22 000 / 9 800;
WP4 12 000 / 0. Legend: planned (light), actual (dark). Note: WP4 has no
actual spend recorded.
```

Include:

- **Type** — bar, grouped bar, line, scatter, flow diagram, org chart, screenshot, photo, map, signature, stamp.
- **Axes** with units and range, for anything quantitative.
- **Values** you can read. If a bar is unlabelled, estimate and say so: "~9 800 (read from axis)".
- **Every legible string** — titles, labels, legends, footnotes, axis captions.
- **What is absent** when it carries meaning: a missing series, an empty category, a truncated axis.

Do not:

- Guess values you cannot see. Write "illegible" instead.
- Summarise a table as prose. Reproduce it (below).
- Describe styling — colours matter only when they encode a variable.

### Publisher branding: one line, then move on

Some routed rasters are not figures. Journal mastheads, society and university
logos, conference banners, book covers and decorative section icons fire as
figures because nothing short of reading them can tell them apart from a small
chart — six geometric signals were measured against that and five failed
(`eval/tds-corpus.md`). They are 3.4% of vision calls, and the cheap handling
below is the fix, because the detection is not available.

When the image turns out to be branding, name it and stop:

```
**Masthead (p1).** *Circulation: Cardiovascular Interventions*, Journal of the
American Heart Association.
```

Do not describe the typography, the crest, the colour of the rule beneath it, or
the ribbon the emblem sits on. One line. The exception is a mark that carries a
fact the text does not state — an ISSN, a version number, a date stamp, a
certification number inside the logo — which goes in the line.

## Page transcriptions (`reason: "no_text_layer"`)

The page has no text layer at all. You are the OCR.

Transcribe **verbatim**, preserving reading order, headings and structure. Do not
paraphrase, summarise, correct spelling, or modernise. For handwriting,
transcribe what is written; mark genuinely unreadable words `[illegible]` rather
than guessing.

### Body first. Furniture last, and separately.

**Start with the document's actual content.** Running heads, footers, page
numbers, letterhead blocks, archival stamps and marginal annotations are *not*
body text. Put them last, under a plain label:

```
<body text, in reading order>

Page furniture: letterhead "BUTLER & VALE, Attorneys at Law, Southern
Building, Washington D.C."; telephone Main 3928; archival note "ack 5/26/14";
page number 10.
```

Do **not** write `<!-- doc-extract:add -->` markers yourself. `describe.py`
adds them, and it escapes any that appear in your text — writing them by hand
turns them into visible `&lt;!--` garbage in `doc.md`.

This is not cosmetic. Interleaving furniture with body text means a repeated
letterhead lands in every chunk of a 40-page contract, poisoning retrieval and
burying the sentence that actually answers the question. Keep it, but keep it
out of the way — and inside delimiters, so it strips cleanly.

Signature blocks *are* body content: keep them inline. So are dates and
reference numbers that appear in the body of a letter rather than in its
letterhead.

## Tables (`reason: "dense_grid"` or `"stroke_grid"`)

The extractor saw the page but could not turn its table into Markdown, usually
because of merged or spanning headers. Reproduce it exactly as a Markdown table.

For merged headers, flatten into unambiguous column names rather than dropping
the grouping:

```
| Sub-task | Type of expense | Planned incentive | Planned other | Actual incentive | Actual other |
```

Preserve totals rows and their labels. Keep numbers exactly as printed —
thousands separators, decimal commas, currency symbols. Do not normalise
`2 746,00` into `2746.0`; downstream reconciliation depends on the original form.

If part of the table is genuinely unreadable, reproduce what you can and mark the
gap. A partial table with a stated gap is useful; a silently incomplete one is
worse than none.

## Formulas

Transcribe mathematics as LaTeX, inline with `$…$` and displayed with `$$…$$`.
Prose descriptions of an equation are not recoverable — "the gradient of the
loss with respect to theta" could be any of a dozen expressions, and a reader
answering from the Markdown alone cannot reconstruct which.

```
$$\mathcal{L}(\theta) = -\frac{1}{N}\sum_{i=1}^{N} y_i \log \hat{y}_i \quad (3)$$
```

- **Keep the equation number** exactly as printed, in the form the document
  uses — `(3)`, `(3.1)`, `(A.2)`. Later text refers back to it by that number.
- **Preserve the symbols the author chose.** Do not normalise `σ` to `s`, or
  rewrite a summation as a loop. Distinguish visually similar characters where
  you can: `\ell` and `1`, `\nu` and `v`, `\epsilon` and `\in`.
- **Mark what you cannot read** as `[illegible]` inside the expression rather
  than guessing a plausible subscript. A wrong subscript is worse than a gap,
  because it looks correct.
- **Inline maths stays inline.** Do not promote every symbol in running prose
  to a display equation; it destroys the paragraph.

Where an equation is part of a page transcription (`no_text_layer`), it goes in
reading order with the rest of the body, not collected at the end.

## Length

Match the content. A logo needs a line. A dense financial table needs however
many rows it has. Do not pad, and do not truncate a table to keep it short.
