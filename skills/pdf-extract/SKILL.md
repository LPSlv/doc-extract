---
name: pdf-extract
description: Use when given one or more PDFs to read, summarise, extract from, or answer questions about - converts them to citable Markdown and visually reads the charts, diagrams, scanned pages and ruled tables that text extraction silently drops. Triggers on "read this PDF", "extract from these PDFs", "what does this report say", "parse this scan", "pull the figures out of", "summarise this contract".
---

# pdf-extract

Text extraction handles most PDFs on its own. This skill uses a fast local
engine for that, then spends vision calls **only** on what it provably missed —
figures, scanned pages, and tables it failed to structure.

## When NOT to use this

- Merging, splitting, form filling, encryption → `anthropics/skills@pdf`.
- A PDF you need one number from and already know the page of → just read it.

Requires `uv`. Nothing else; dependencies resolve on first run.

## 1. Convert

```bash
uv run <skill-dir>/convert.py FILE.pdf [MORE.pdf ...]
```

One JSON object per document, on stdout. Everything deterministic is now done:
text extracted, images written, artifact cached. Exit code is non-zero if any
document failed.

```json
{"status":"ok","artifact":"/home/…/<sha>-<tag>","cached":false,
 "doc_md":"…/doc.md","pages_dir":"…/pages","manifest":"…/manifest.json",
 "pending":[{"id":"p007-render","page":7,"kind":"page_render",
             "reason":"dense_grid","path":"…/images/p007-render.png"}],
 "dropped":6,"over_scale_guard":false,"scale_guard":15}
```

Check `status` first. `encrypted` and `unreadable` are terminal — report and
move on; the batch continues. Re-running the same PDF returns `cached: true`
instantly and costs nothing.

**If `over_scale_guard` is true**, tell the user how many calls it wants and get
agreement before continuing. An 84-page scan is 84 calls.

## 2. Look at each pending item

`pending` is empty → you are done, go to step 3.

Otherwise, for each entry: read the file at `path`, then write what you saw:

```bash
uv run <skill-dir>/describe.py <artifact> <id> "your description"
# or pipe a long one:  … describe.py <artifact> <id> -
```

How to write the description depends on `reason` — see
`reference/describing-visuals.md`:

| `reason` | What to write |
|---|---|
| `standalone_raster`, `curves`, `diagonals` | Describe the figure: type, what it shows, axes and units, notable values, all legible text. |
| `no_text_layer` | **Transcribe the page verbatim.** This is the OCR path; there is no text at all. |
| `dense_grid`, `stroke_grid` | A table the extractor could not structure. Reproduce it as a Markdown table. |

`describe.py` is safe to re-run — it replaces rather than duplicates, so a vision
pass that dies halfway can just be resumed.

## 3. Answer

- Whole document: `doc.md`.
- A specific question: grep `pages/pNNN.md` and read only the pages you need.
- Cite as `[p12]`, or `[report.pdf:p12]` across several documents.

## The one rule

**Never edit `doc.md` by hand.** Everything you add goes through `describe.py`,
which wraps it in delimiters. That is what lets the benchmark strip the additions
and prove the skill does not degrade text extraction. Editing in place breaks
that guarantee silently.

## Why the filters are what they are

Do not "simplify" these — each exists because the obvious alternative was tested
and failed on real documents:

| Filter | Why |
|---|---|
| Drop images on >50% of pages, <120px, aspect >8:1 | One 14-page grant PDF had 69 image placements: 7 distinct objects, six of them logos, rules and a sidebar stripe. |
| Skip pages that already yielded a Markdown table | The extractor is better at tables it can parse than vision is. Only intervene where it produced nothing. |
| Require strokes in **both** orientations | Underlines and rules are horizontal only. Counting all axis-aligned strokes fired on bibliography pages and on contracts with underlined headings. |
| Exempt `diagonals` from the area floor | 4+ diagonal segments do not occur in body text, and the floor was vetoing charts placed in a page corner. |
| Ink threshold on the dense-grid branch | Separates a shaded table the extractor missed from decorative section banners. |

`harvest.py` is the single source of truth for routing. Every number in the
README and design spec is regenerated from it; never edit a number by hand. If
you cannot execute a file, `reference/harvest-block.md` is a verbatim copy to
paste and run.
