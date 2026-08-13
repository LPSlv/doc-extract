---
name: doc-extract
description: Use when given one or more documents to read, summarise, extract from, or answer questions about - PDFs, Word, Excel, PowerPoint or images. Converts them to citable Markdown and visually reads the charts, diagrams, scanned pages and ruled tables that text extraction silently drops. Triggers on "read this PDF", "extract from these documents", "what does this report say", "parse this scan", "pull the figures out of", "summarise this contract", "read this deck", "what's in this spreadsheet".
---

# doc-extract

Text extraction handles most documents on its own. This skill uses fast local
engines for that, then spends vision calls **only** on what it provably missed —
figures, scanned pages, and tables it failed to structure.

Reads `.pdf`, `.docx`, `.xlsx`, `.pptx`, and image files. Format is decided by
content, not by extension.

## When NOT to use this

- Merging, splitting, form filling, encryption → `anthropics/skills@pdf`.
- A document you need one number from and already know the page of → just read it.

Requires `uv`. Nothing else; dependencies resolve on first run.

## 1. Convert

```bash
uv run <skill-dir>/convert.py FILE [MORE ...]
uv run <skill-dir>/convert.py FILE --inline    # descriptions at the image's position
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

Check `status` first. `encrypted`, `unreadable` and `unsupported` are terminal —
report and move on; the batch continues. Re-running the same file returns
`cached: true` instantly and costs nothing.

**If `over_scale_guard` is true**, tell the user how many calls it wants and get
agreement before continuing. An 84-page scan is 84 calls, and so is a 40-image
slide deck.

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
| `raster_grid` | A page tiled with many images — a composite figure, or one photo stored as strips. Describe what the panels show **together**, then anything notable per panel. |

`describe.py` is safe to re-run — it replaces rather than duplicates, so a vision
pass that dies halfway can just be resumed.

Items with `kind: "native_chart"` never appear in `pending`. Those are
spreadsheet charts whose series were read from the chart definition, so their
numbers are exact rather than estimated from pixels.

## 3. Answer

- Whole document: `doc.md`.
- A specific question: grep the per-unit files and read only the ones you need.
- Cite by unit, or prefix the filename across several documents
  (`[report.pdf:p12]`).

| Format | Unit | Cite as | Per-unit file |
|---|---|---|---|
| PDF | page | `[p12]` | `pages/p012.md` |
| PowerPoint | slide | `[s07]` | `pages/u007.md` |
| Excel | sheet | `[Sheet2]` | `pages/u002.md` |
| Word | level-1 heading | `[Budget assumptions]` | `pages/u003.md` |
| image | whole file | `[img]` | `pages/u001.md` |

Office unit files are numbered rather than named, because a sheet called
`Q1 P&L / draft` is not a filename. `manifest.json` carries a `units` list
mapping each file to its label, in order.

## The one rule

**Never edit `doc.md` by hand.** Everything you add goes through `describe.py`,
which wraps it in delimiters. That is what lets the benchmark strip the additions
and prove the skill does not degrade text extraction. Editing in place breaks
that guarantee silently.

## Where descriptions land, and the one thing `--inline` does not promise

By default every description is appended in one block at the end of `doc.md`,
labelled `[s02]`, `[p12]` or `[Sheet2]`. `--inline` instead places each block at
its image's position. Pass it at **convert** time, not to `describe.py`: the
placement is recorded in the artifact (and in its cache key), so a resumed
vision pass cannot mix the two.

| Format | What `--inline` can anchor to |
|---|---|
| PowerPoint | the picture's own line, when that line is provably the picture's; otherwise the end of the slide |
| Word | the end of the section the picture sits in — anydoc renders a picture as its alt text, and Word writes none unless the author typed one, so there is usually no line to anchor to |
| Excel | the end of the sheet — images and charts come from the package, and anydoc renders neither |
| PDF, image | nothing. `--inline` changes nothing for a PDF |

The block is **inserted** beside the engine's line, never substituted for it,
which is why byte-identity survives — `eval/gate.py` runs both placements and
fails on any in-place edit.

What inline does *not* promise is that the position is right; byte-identity
cannot check placement, because an insertion round-trips wherever it lands. The
anchor is anydoc's alt text, which is ordinary prose: a slide about a file
called `image.png` renders the same line a picture does. So an image's own line
is used only when the number of candidate lines in that unit equals the number
of pictures in it, and the description falls back to the unit boundary
otherwise. Positions are either provably that picture's, or a unit boundary —
never a guess between two lines that look alike.

## Why the filters are what they are

Do not "simplify" these — each exists because the obvious alternative was tested
and failed on real documents:

| Filter | Why |
|---|---|
| Drop images on >50% of units, <120px, aspect >8:1 | One 14-page grant PDF had 69 image placements: 7 distinct objects, six of them logos, rules and a sidebar stripe. |
| Skip pages that already yielded a Markdown table | The extractor is better at tables it can parse than vision is. Only intervene where it produced nothing. |
| Require strokes in **both** orientations | Underlines and rules are horizontal only. Counting all axis-aligned strokes fired on bibliography pages and on contracts with underlined headings. |
| Exempt `diagonals` from the area floor | 4+ diagonal segments do not occur in body text, and the floor was vetoing charts placed in a page corner. |
| Ink threshold on the dense-grid branch | Separates a shaded table the extractor missed from decorative section banners. |
| Collapse pages with >6 rasters into one render | A 48-tile inpainting comparison is one figure, and one TI package photo arrives as 12 strips; per-tile calls cost ~2× the tokens and lose the composition. Pages with 5–6 rasters are sometimes distinct figures, so the line sits at 6. |
| Drop EMF, WMF and OLE payloads | Retained faithfully by the text engine, and unreadable without a rasterizer — routing one to `pending` would create an item no agent can complete. Counted in `dropped`, never silently discarded. |

`harvest.py` is the single source of truth for PDF routing, and `filters.py` for
the parts that apply to every format. Every number in the README and design spec
is regenerated from them; never edit a number by hand. If you cannot execute a
file, `reference/harvest-block.md` is a self-contained copy to paste and run.

## Office routing is deliberately thinner, and that is honest

A PDF page is a program of drawing commands that hides its figures, which is why
`harvest.py` infers them from vector geometry. OOXML declares its images in the
package, so there is nothing to infer. Office documents get the furniture
filters, the citation and cache contract, and this rubric — but no
`render_reason`, no `raster_grid` and no `cost_guard`, because without a
rendering engine there is no slide or sheet to render.
