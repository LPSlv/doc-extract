# doc-extract — design

Extends `pdf-extract` to Office formats and standalone images. Supersedes
nothing: the PDF path in `2026-08-03-pdf-extract-skill-design.md` is unchanged,
and every claim it makes still holds byte-for-byte.

Status: design approved, not implemented.

## 1. Purpose

A user with a folder of mixed documents should get one interface. Today the
skill reads `report.pdf` and refuses `report.docx`, `model.xlsx`, `deck.pptx`
and `scan.png` — formats that arrive in the same email as the PDF.

The pitch stays what it was: extract text cheaply and locally, then spend vision
calls only on what text extraction provably missed.

## 2. Non-goals

- **Not a rewrite of the PDF path.** `harvest.py` is untouched. All 12 corpora,
  the byte-identity gate and every fitted threshold keep their current meaning.
- **No LibreOffice, no pandoc, no system packages.** `uv` and nothing else,
  as advertised.
- **No layout model and no OCR model of our own.** The agent's own eyes are the
  vision layer, as they already are for PDFs.
- **Not HTML, EPUB, RTF, CSV, ODF, email or archives.** `anydoc` handles several
  of these and adding them later is cheap, but none is measured here and this
  project does not ship unmeasured claims.
- **Not a `raster_grid`, `cost_guard` or page-render analogue for Office.**
  See §4.3 — those solve a problem OOXML does not have.

## 3. Evidence base

Everything in this section was verified against `firecrawl/anydoc` at commit
depth 1 on 2026-08-06 and against `firecrawl_anydoc==0.1.6` on PyPI. Source
line references are to the cloned repository.

### 3.1 anydoc is the right text engine, and its PDF path proves it

`anydoc` (MIT, Rust, ~5.7k stars, created 2026-08-03) converts Word,
PowerPoint, Excel, OpenDocument, RTF, EPUB and CSV to GFM. Its own PDF path
delegates to `pdf-inspector` — the exact engine `harvest.py` already uses. The
two projects are already in the same family; this makes the relationship
explicit.

Prebuilt `abi3` wheels exist for manylinux, musllinux, macOS and Windows at
`requires-python >=3.10`, matching `convert.py`'s existing floor. Verified on
this machine:

```
uv run --with firecrawl-anydoc==0.1.6 python -c "import anydoc"   # OK
anydoc.format_from_bytes(pdf_header)                              # -> 'pdf'
```

No Rust toolchain, no system dependency. The packaging promise survives.

### 3.2 anydoc has no visual layer, deliberately

Quoting the README: images "render as their alt text in the Markdown, and the
raw bytes stay available on the document model." Confirmed in
`src/render/markdown/inline.rs`: `ImageSource::Asset(_) | Unavailable` emits
alt text as plain text, and nothing at all when alt is empty. Scanned PDFs
raise `UnsupportedError` with "OCR is required".

That capability is reserved for Firecrawl's paid hosted Parse. The gap anydoc
leaves open is precisely what this skill already does, so the two compose
without overlap.

### 3.3 anydoc's document model cannot carry citations or furniture filtering

Three findings, each verified in source, each of which would have broken an
implementation that assumed otherwise:

| Finding | Source | Consequence |
|---|---|---|
| Slide anchors are emitted only on slides another slide links to | `src/formats/pptx/mod.rs:165` — `if targeted.contains(slide_path)` | `slide-N` anchors are absent from a typical deck; slide boundaries are not recoverable from the model |
| Sheet headings are gated on a multi-sheet workbook | `src/formats/sheet/mod.rs:28,108` — `multi_sheet = sheet_names.len() > 1` | A single-sheet workbook carries no sheet marker |
| Assets are deduplicated by package part | `src/shared/assets.rs:33` — `by_part`, "repeated origin parts share one asset" | Placement counts are collapsed, so `UBIQUITY` has nothing to count |

The third is the load-bearing one. `UBIQUITY` — drop an image placed on more
than 50% of units — is the filter that kills logos, and the original design
measured it as the difference between 69 image placements and 1 worth reading.
`anydoc` reports one asset with one `origin_part`, so placement counts must
come from elsewhere.

**Conclusion: `anydoc` supplies text and asset bytes. Structure comes from our
own OOXML package reader.** That reader is `zipfile` + `xml.etree`, both
standard library, so it costs no dependency — and it is the same reader that
yields chart XML in §4.4.

### 3.4 Slide boundaries are recoverable by repacking

`src/formats/pptx/mod.rs:73` derives `slide_paths` from `sldIdLst` in
`ppt/presentation.xml`. Rewriting that single part to hold one `sldId` and
re-zipping in memory therefore yields a package `anydoc` reads as a one-slide
deck. Every layout, master, notes and media part stays in place, so the
slide → layout → master → presentation-default text cascade still resolves and
the extraction quality is exactly `anydoc`'s.

Cost is one `anydoc` call per slide at a ~4.7 ms median, so a 50-slide deck
costs ~240 ms. This is the mechanism for pptx unit boundaries.

### 3.5 xlsx needs no repacking

`src/formats/sheet/mod.rs:104-111` pushes `Block::heading(2, name)` — when
multi-sheet — then exactly one `Block::Table` per sheet, in `sheet_names`
order. Sheets therefore split by walking the block list and taking each `Table`
block in order, which is reliable in the single-sheet case too. Sheet names
come from the package reader, not from the conditional headings.

### 3.6 docx needs no repacking either

Headings are unconditional `Block.kind == "heading"` entries carrying `level`.
Only the `anchor` field is conditional, and citations are built from heading
text and level rather than anchors.

### 3.7 Parse adds nothing this skill needs

Firecrawl's hosted Parse is `pdf-inspector` classification, a layout model and
GLM-OCR — Zhipu's MIT-licensed 0.9B model, not a Firecrawl model. Its
selectivity claim ("only the scanned ones reach a GPU") is `harvest.py`'s
`no_text_layer` branch, routed on the same `pdf_inspector` classifier this
skill already calls at `harvest.py:363`.

Parse routes on text presence alone. `render_reason()` also routes on vector
geometry, so it catches pages that carry plenty of text but whose *content* is
visual — charts, pinout diagrams, unstructured tables. Parse passes those
through as text and drops the figure silently.

One idea is worth taking: Parse assigns task-specific prompts and budgets per
layout region, including LaTeX-specific prompting for formulas. The describe
rubric has no formula guidance at all, which §4.5 fixes. Region-level prompting
and a `fast|auto|ocr` mode switch are logged as follow-up work, not built here.

## 4. Architecture

```
                   ┌─ pdf ──────────────► harvest.py            UNCHANGED
                   │                       pdf-inspector + PyMuPDF geometry
input ─► detect ───┼─ docx / xlsx / pptx ─► office.py + ooxml.py
   format_from_    │                       text, units, assets, charts
   bytes, not ext  └─ png/jpg/tiff/webp ──► image.py
                                                    │
                             all paths converge ────┴──► filters.py
                                                          furniture · dedup
                                                                │
                                          artifact.py · cache.py · describe.py
                                                          UNCHANGED
```

### 4.1 Module boundaries

| Module | Responsibility | Depends on |
|---|---|---|
| `harvest.py` | PDF routing. **No change** beyond having shared filters imported rather than defined | `pdf-inspector`, `pymupdf`, `filters` |
| `filters.py` | **New.** `furniture_reason`, pixel-hash dedup, `_tok`. Format-agnostic, lifted verbatim from `harvest.py` | stdlib only |
| `ooxml.py` | **New.** Package reader: unit boundaries, asset→unit placement counts, chart series, slide repacking | stdlib only (`zipfile`, `xml.etree`) |
| `office.py` | **New.** Orchestrates `anydoc` + `ooxml`, emits the `harvest()` contract | `firecrawl-anydoc`, `ooxml`, `filters` |
| `image.py` | **New.** One image → one item, no text layer | stdlib only |
| `convert.py` | Format dispatch, then unchanged | all adapters |
| `artifact.py`, `cache.py`, `describe.py` | **No change** except `ENGINE` | — |

Lifting the shared filters out of `harvest.py` is the one change to existing
code. They are format-agnostic today but entangled with PyMuPDF calls; both
paths need them, and `harvest.py` is 577 lines and does not need to grow.

That lift has a consequence worth naming, because it is easy to miss.
`reference/harvest-block.md` is a verbatim copy of `harvest.py` whose stated
promise is that an agent unable to execute a file can paste the block and get
identical routing. Once `harvest.py` imports from `filters.py`, a pasted block
fails on the import and the promise is false. `tests/check_sync.py` must
therefore render the block as `filters.py` followed by `harvest.py` with the
import line elided, and keep asserting the two stay in step. The alternative —
duplicating the filters into `office.py` — is rejected: the README states
`harvest.py` is the single source of truth for routing, and two copies of a
fitted threshold is exactly the drift that claim exists to prevent.

### 4.2 The adapter contract

Every adapter returns the dict `harvest()` already returns. `convert.py` and
everything downstream stay ignorant of format. Office and image adapters return
`pdf_type: null` and set `kind` to `"raster"` on every item, since no adapter
but the PDF one can render a unit.

### 4.3 Routing is thin for Office, and that is the honest outcome

`render_reason`, `grid_pages` and `cost_guard` are PDF-only and get no
analogue. All three exist because a PDF page is a program of drawing commands
that hides its figures; OOXML declares its images in the package. There is also
no slide or sheet render to fall back to without LibreOffice, which §2 rules
out.

Office routing is therefore: extract assets → `furniture_reason` → pixel-hash
dedup → describe. Placement counts for `UBIQUITY` come from `ooxml.py` walking
per-unit relationship parts.

This asymmetry must be stated plainly in the README rather than glossed. The
selective-routing advantage is a PDF phenomenon; what Office formats inherit is
the furniture filters, the artifact and citation contract, and the describe
rubric.

### 4.4 Native charts

A chart in pptx/xlsx/docx is `<c:chart>` XML, not an image. `anydoc` drops it
entirely — not even alt text, because it is not an image inline. That is silent
content loss, the exact failure mode this project exists to catch.

Chart XML carries `<c:numCache>` and `<c:strCache>` holding the plotted series
values, so `ooxml.py` extracts them as a Markdown table. Extraction is
deterministic, so `convert.py` writes it during the build rather than leaving
it pending for the agent — but it goes in through `artifact.splice()`, inside
the same delimiters every addition uses. That placement is required, not
stylistic: `anydoc` emits no chart content at all, so a chart table outside the
delimiters would fail the byte-identity gate in §6.1.

```
**Chart (bar, slide 4).** Revenue and cost by quarter. Series from c:numCache.

| Quarter | Revenue | Cost |
|---|--:|--:|
| Q1 | 1240 | 890 |
| Q2 | 1310 | 902 |
```

This is strictly better than a vision call: the numbers are exact rather than
read from pixels, and it costs nothing. Charts whose caches are absent or
unparseable are recorded in `dropped` with `why: "native_chart_unread"` and
counted, so the residue is visible rather than silent.

### 4.5 Formula guidance in the describe rubric

`reference/describing-visuals.md` gains a Formulas section: transcribe as
LaTeX, preserve equation numbering, mark unreadable subscripts rather than
guessing. Parse budgets formulas separately for this reason, and the
`olmocr_arxiv_math` corpus is 522 of the 2,342 benchmarked files. Applies to
both paths — it is a rubric change, not a routing change.

### 4.6 Citations

| Format | Unit | Citation | Derived from |
|---|---|---|---|
| pdf | page | `[p12]` | unchanged |
| pptx | slide | `[s07]` | `sldIdLst` order, via repacking |
| xlsx | sheet | `[Sheet2]` | `sheet_names` zipped with `Table` blocks |
| docx | heading | `[§3.2]` | heading blocks and levels |
| image | whole | `[img]` | — |

The `pages/` directory keeps its name and holds these units. Renaming it to
`units/` would force a schema bump that invalidates every cached artifact and
buy nothing functional.

### 4.7 Errors

`anydoc`'s typed taxonomy maps onto the existing terminal statuses, so a bad
file still never aborts a batch:

| anydoc | status |
|---|---|
| `EncryptedError` | `encrypted` |
| `MalformedError`, `MissingPartError` | `unreadable` |
| `UnsupportedError` | `unsupported` (new; terminal, reported, batch continues) |
| `ResourceLimitError` | `unreadable`, with `limit` in `detail` |

`ResourceLimitError` on `max_asset_total_bytes` is a live risk for image-heavy
decks. The Python binding does not expose the limit — §7 resolves this.

## 5. Cache and versioning

`ENGINE` becomes `"pdf-inspector==0.2.6+anydoc==0.1.6"`. The cache key already
hashes `ENGINE` and `SCHEMA`, so the version bump invalidates stale artifacts
through machinery that exists. `SCHEMA` stays at 1: the artifact layout does
not change.

`anydoc` is three days old and its API stability is unproven, which the exact
pin and the cache key together contain.

## 6. Validation

### 6.1 Byte-identity gate, extended

`eval/gate.py` currently proves stripped `doc.md` equals raw
`pi.process_pdf()` output exactly. The Office analogue substitutes
`anydoc.to_markdown_bytes()` as the reference, including the hostile payload
that quotes the close delimiter and the re-describe that simulates a resumed
run.

For pptx the reference is the concatenation of per-slide repacked conversions,
not a whole-deck conversion — repacking is part of the pipeline under test, so
comparing against a whole-deck run would test `anydoc` rather than this skill.
Whether the two agree is itself worth recording.

### 6.2 Office corpus

A 13th corpus, pinned exactly as the existing 12 are: `eval/fetch.py office`
reading `eval/manifests/office.urls.tsv` as `filename<TAB>url<TAB>sha256`, with
magic-byte validation. Candidate sources must be stably hosted and
redistributable by URL; government and institutional publications are the
likeliest fit, as they were for `bills`. Selection is part of implementation,
not settled here.

`eval/bench.py` needs Office token accounting: no page renders exist, so the
"read every page" baseline has no meaning. The comparison is instead against
describing every extracted asset, before furniture filtering and dedup.

### 6.3 What the README may claim

Nothing until §6.2 produces numbers. The existing table gains a row when it is
measured, and not before. The Office asymmetry from §4.3 and the chart residue
from §4.4 both belong in Limitations.

## 7. Open questions, to resolve in the first implementation task

1. **`max_asset_total_bytes`.** The Python binding exposes no configuration.
   If image-heavy decks trip `ResourceLimitError`, either assets come from
   `ooxml.py` instead of `anydoc` — which the package reader can already do —
   or the limit needs raising upstream.
2. **Repacking robustness.** §3.4 is verified by reading `anydoc`'s source, not
   by running it. Needs validation against real decks, including a deck whose
   `sldIdLst` order differs from part-name order, and one with `.pptm` macros.
3. **docx unit granularity.** Heading-level citations are only useful if a
   document has headings. The fallback for a heading-less docx is undecided;
   whole-document citation is the likely answer.
4. **Chart coverage.** Which chart types carry usable caches, and how often
   `numCache` is absent in real files. Determines whether §4.4 is a feature or
   a footnote.

## 8. Positioning

The vision layer is the agent's own eyes. That is the entire commercial
argument, and it is why this is a skill rather than a library or a service.

Firecrawl Parse bills 1 credit per page, flat, whether or not a page needed
OCR — roughly $0.83–3.20 per 1,000 pages depending on plan, on top of an
account, an API key and a 50 MB-per-file upload of documents to a third party.
This skill spends the subscription the user already pays for. There is no
second bill, no key to manage, and no document leaves the machine.

Selective routing is what makes that practical rather than merely possible. At
1.00 vision calls per page a subscription-funded agent burns its budget on the
first document; at the measured 0.34 it does not. The routing is not only a
cost optimisation — it is the thing that lets the vision layer live inside a
seat licence at all.

Two consequences follow for the Office work:

- The comparison the README should draw against a per-page service is
  **honest and favourable**, but it must be stated as what it is: a different
  billing model, not a quality claim. Parse's OCR on a scanned page may well
  read better than a general agent's; that has not been measured here and must
  not be implied.
- **Local execution is a feature to state, not to overclaim.** Documents stay
  on the machine because nothing in the pipeline makes a network call —
  `anydoc`, `pdf-inspector` and PyMuPDF are all local. Whether the agent's own
  vision calls leave the machine depends on the host, which this skill does not
  control and must not make promises about.

### Public claim

> Reads PDFs, Word, Excel, PowerPoint and images. Extracts text locally and
> exactly, then spends your agent's own eyes only on what text extraction
> provably missed — no API key, no per-page bill, no upload.

Everything beyond that is measured or is not claimed.
