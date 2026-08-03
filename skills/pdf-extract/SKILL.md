---
name: pdf-extract
description: Use when given one or more PDFs to read, summarise, extract from, or answer questions about - converts them to citable Markdown, and separately extracts and visually reads the charts, diagrams, scanned pages and ruled tables that text extraction silently drops. Triggers on "read this PDF", "extract from these PDFs", "what does this report say", "parse this scan", "pull the figures out of".
---

# pdf-extract

Text extraction gets ~54% of PDFs right on its own. This skill uses a fast local
engine for that half, then spends vision calls **only** on the parts it provably
missed — figures, scans, and tables it failed to structure.

Two modes: **convert** once into a cached artifact, then **answer** against it
cheaply, as many times as needed.

## When NOT to use this

- Merging, splitting, form filling, encryption → `anthropics/skills@pdf`.
- A PDF you only need one number from and already know the page of → just read it.

## Requirements

`uv` only. Dependencies resolve on first run; nothing is installed globally.
`pdftoppm` (poppler) is used for rendering when present, PyMuPDF otherwise.

## Workflow

### 1. Harvest

```bash
uv run <skill-dir>/harvest.py <file.pdf> --json
```

This does everything deterministic: classifies the PDF, extracts authoritative
Markdown, pulls embedded images, drops furniture, and decides which pages need
eyes. It returns a manifest with `description: null` on every item needing a
vision pass, plus a `dropped` list recording what was filtered and why.

**Check `status` first.** `encrypted` and `unreadable` are terminal — report and
stop, do not cache. `empty_extraction` means the file has neither text nor
visual content.

**Check `over_scale_guard`.** If true (>15 vision calls), report the count to the
user and get agreement before continuing. An 84-page scan is 84 calls.

### 2. Look at each item

For every manifest item with `description: null`, read the image file and write
what you see. Two modes, detailed in `reference/describing-visuals.md`:

- `kind: "raster"` or a chart page → **describe the figure**: what type, what it
  shows, axes and units, notable values, and every piece of legible text.
- `reason: "no_text_layer"` → **transcribe the page verbatim**. This is the OCR
  path; the page has no text at all. Reconstruct tables as Markdown.
- `reason: "dense_grid"` or `"stroke_grid"` → a table the extractor could not
  structure. Reproduce it as a Markdown table, exactly.

Write each description back into the manifest.

### 3. Assemble

```python
from artifact import splice
doc = splice(raw_markdown, [(offset, description), ...])
```

**Never edit the engine's Markdown directly.** Everything you add goes through
`splice`, which wraps it in delimiters so it can be removed again. This is what
lets the benchmark prove the skill does not degrade text extraction. Editing the
text in place breaks that guarantee silently.

### 4. Answer

Read `pages/pNNN.md` for the pages a question touches rather than the whole
document. Cite as `[p12]`, or `[report.pdf:p12]` across multiple documents.

## Why the filters are what they are

Do not "simplify" these. Each exists because the obvious alternative was tested
and failed on real documents:

| Filter | Why |
|---|---|
| Drop images on >50% of pages, <120px, aspect >8:1 | One 14-page grant PDF had 69 image placements: 7 distinct objects, of which 6 were logos, rules and a sidebar stripe. One was real. |
| Skip pages that already yielded a Markdown table | The extractor is better at tables it can parse than vision is. Only intervene where it produced nothing. |
| Require strokes in **both** orientations | Underlines and rules are horizontal only. Counting all axis-aligned strokes fired on bibliography pages and on contract pages with underlined headings. |
| Exempt `diagonals` from the area floor | 4+ diagonal segments do not occur in body text, and the floor was vetoing real charts placed in a page corner. |
| Ink threshold on the dense-grid branch | Distinguishes a shaded table the extractor missed from decorative section banners. |

## Canonical block

`harvest.py` is the single source of truth for every routing decision. If you
cannot execute a file, its full contents are reproduced verbatim in
`reference/harvest-block.md` — paste and run that instead. `tests/check_sync.py`
asserts the two are identical.

Numbers in the README and design spec are regenerated from `harvest.py`. Never
edit a number by hand.
