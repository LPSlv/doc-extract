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

Do **not** write `<!-- pdf-extract:add -->` markers yourself. `describe.py`
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

## Length

Match the content. A logo needs a line. A dense financial table needs however
many rows it has. Do not pad, and do not truncate a table to keep it short.
