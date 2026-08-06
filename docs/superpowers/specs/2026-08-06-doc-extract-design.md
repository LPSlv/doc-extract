# doc-extract — design

Extends `doc-extract` to Office formats and standalone images. Supersedes
nothing: the PDF path in `2026-08-03-doc-extract-skill-design.md` is unchanged,
and every claim it makes still holds byte-for-byte.

Status: design approved, not implemented. Revision 2 — §3 and §4 were rewritten
after running the pinned wheel refuted three claims of revision 1. Those
refutations are kept in place rather than edited out, because a design that
hides what it got wrong teaches nothing.

## 1. Purpose

A user with a folder of mixed documents should get one interface. Today the
skill reads `report.pdf` and refuses `report.docx`, `model.xlsx`, `deck.pptx`
and `scan.png` — formats that arrive in the same email as the PDF.

The pitch stays what it was: extract text cheaply and locally, then spend vision
calls only on what text extraction provably missed. The vision is the host
agent's own — see §8.

## 2. Non-goals

- **Not a rewrite of the PDF path.** `harvest.py`'s routing is untouched. All
  12 corpora and every fitted threshold keep their current meaning, and the
  benchmark numbers must be bit-identical after the refactor in §4.1.
- **No LibreOffice, no pandoc, no system packages at runtime.** `uv` and
  nothing else. Both are installed on the author's machine and both are
  legitimate *fixture-generation* tools; neither may enter the skill's
  dependency set.
- **No layout model and no OCR model of our own.**
- **Not HTML, EPUB, RTF, CSV, ODF, email or archives.** Dispatch whitelists
  exactly `{pdf, docx, xlsx, pptx}` plus image types and returns `unsupported`
  otherwise. `anydoc.format_from_bytes` also returns `doc`, `ppt`, `xls`, `odt`
  and more, and anydoc converts several of them — but `ooxml.py` uses `zipfile`
  and cannot read the legacy OLE containers, so citations and assets would
  degrade silently. The whitelist is what keeps this non-goal from leaking.
- **No page-render analogue for Office.** See §4.3.

## 3. Evidence base

Everything here was verified against `firecrawl_anydoc==0.1.6` — the wheel
actually depended on — by executing it, not by reading the design. Source
citations are to the anydoc clone; where source and wheel could disagree, the
wheel wins and is marked **[run]**.

### 3.1 anydoc is the right text engine

MIT, Rust, converts Word/PowerPoint/Excel/ODF/RTF/EPUB/CSV to GFM. Prebuilt
`abi3` wheels for manylinux, musllinux, macOS and Windows at
`requires-python >=3.10`, matching `convert.py`'s existing floor. **[run]**
`uv run --with firecrawl-anydoc==0.1.6 python -c "import anydoc"` succeeds and
`format_from_bytes` detects by content. No Rust toolchain, no system
dependency.

The alternatives lose on merit, not effort. `python-docx`/`openpyxl`/
`python-pptx` are object-model libraries, not converters — choosing them means
owning list numbering, style cascades, merged-cell grids, footnotes and the
pptx layout→master text cascade, with no benchmark to prove parity. They remain
the right tools for generating fixtures. `markitdown` converts but exposes no
document model, no asset bytes and no typed errors, so the package reader would
still be needed and the text engine would be a second unpinned quality surface.

One watch item: anydoc's Rust `pdf-inspector` is 0.1.7 while this skill's Python
path pins 0.2.6. Irrelevant while anydoc's PDF path is never used, and §2 keeps
it that way.

### 3.2 anydoc has no visual layer, deliberately

`src/render/markdown/inline.rs` emits alt text for `ImageSource::Asset(_) |
Unavailable` and nothing when alt is empty. Scanned PDFs raise
`UnsupportedError`. That capability is reserved for Firecrawl's paid hosted
Parse, so the gap anydoc leaves open is exactly what this skill already fills.

### 3.3 Placement counts, and where they actually come from

`src/shared/assets.rs:16,33` dedups assets by package part — repeated
placements of one part collapse to a single `Asset`. Revision 1 concluded from
this that a custom rels-walking reader was required to restore `UBIQUITY`. That
conclusion was wrong in both directions:

- **pptx** — the per-slide repack of §3.4 is run anyway for unit boundaries,
  and each repacked package gets a fresh asset sink. **[run]** the shared logo
  in a 3-slide fixture appears in all three slides' asset lists as
  `ppt/media/image1.png`. So `UBIQUITY` is `len(units containing part) /
  len(units)` with no rels walking at all. A useful side effect: the 128 MiB
  asset cap applies per slide rather than per deck.
- **docx** — dedup collapses `Asset` entries, not `Inline::Image` references.
  Every placement produces its own image inline carrying the shared `asset_id`.
  **[run]** `handmade-rich.docx` → `assets=2, image inlines=2, asset_ids=[0,1]`.
- **xlsx** — see §3.5. anydoc surfaces no assets at all, so `ooxml.py` owns
  extraction outright.

**Inherited furniture never enters the count, in either direction.** anydoc's
`load_layout`/`load_master` read placeholders and `txStyles` only, never
`p:pic`; the docx frontend reads no header or footer parts. A master logo or a
letterhead is therefore invisible to anydoc and costs zero vision calls by
omission. This matters for §4.3: if asset extraction is ever moved into
`ooxml.py` for a format, it must count only unit-level parts, or every
inherited logo enters with placement count 1, sails under the `UBIQUITY`
threshold, and buys a vision call each — precisely the failure the filter
exists to prevent.

### 3.4 Slide boundaries by repacking — verified end to end

`src/formats/pptx/mod.rs:73` derives `slide_paths` from `sldIdLst` in the
presentation part. Rewriting that part to hold one `sldId` and re-zipping in
memory yields a package anydoc reads as a one-slide deck, with every layout,
master, notes and media part intact so the text cascade still resolves.

**[run]** across anydoc's own fixtures, per-slide output concatenated with
`"\n\n"` is **byte-identical** to whole-deck output for `handmade-order.pptx`,
`handmade-inherit.pptx` and `pres.pptx`. **[run]** reversing `sldIdLst` in
`pres.pptx` reverses anydoc's output, confirming it follows the list and not
part names, so repacking by `rId` is correct.

Two hazards, both found by running it:

- The surgery must be **textual and prefix-agnostic**, handling both
  self-closing and element forms of `sldId`. Round-tripping through
  `xml.etree` rewrites prefixes and perturbs anydoc's input.
- The presentation part path must come from `_rels/.rels`' `officeDocument`
  relationship, as `pptx/mod.rs:61-66` does, not a hardcoded
  `ppt/presentation.xml`.

One known divergence class: decks with internal slide-to-slide links.
**[run]** `handmade-links.pptx` full-deck emits a resolved anchor where a
repacked slide emits the raw relative path `slides/slide2.xml`, because
`slide_anchors` holds one entry. Text content is identical; only link rendering
differs. Cross-slide link targets are therefore rewritten to `[sNN]` citations
using the `sldIdLst` index map — which suits our citation scheme better than
anydoc's anchors would.

Cost is O(slides × package bytes), not the trivial figure revision 1 implied:
a 30 MB 150-slide deck copies ~4.5 GB. Entries are copied raw and other slides'
parts pruned via the rels walk to contain it.

### 3.5 xlsx: names from headings, never positional

`src/formats/sheet/mod.rs:104-111` pushes `Block::heading(2, name)` — when
multi-sheet — then one `Block::Table` per sheet. Revision 1 specified zipping
package-reader `sheet_names` against `Table` blocks positionally. **That
produces confidently wrong citations**, the one sin this project defines itself
against.

Empty sheets (`:42`), unreadable sheets (`:36-40`) and empty grids (`:104-106`)
all emit nothing. **[run]** a workbook `[Data, Empty, Summary]` yields exactly
`heading(Data), table, heading(Summary), table` — positional zipping would cite
Summary's table as `[Empty]`.

The rule is therefore inverted: **take names from the emitted heading blocks**,
which pair 1:1 with tables after every skip path. Use the package reader's name
only in the single-sheet case, where no heading exists. Excel enforces unique
sheet names and forbids `[ ] : * ? / \`, so the citation syntax is safe. If
heading count ever fails to match table count, fall back to whole-document
citation rather than emit a misaligned one.

### 3.6 docx needs no repacking

Headings are unconditional `Block.kind == "heading"` entries carrying `level`;
only `anchor` is conditional. **[run]** `doc.docx` → `# Intro` / `# Results`
with the body image captured as an asset.

### 3.7 Parse adds nothing this skill needs

Firecrawl's hosted Parse is `pdf-inspector` classification, a layout model and
GLM-OCR — Zhipu's MIT 0.9B model, not a Firecrawl model. Its selectivity claim
("only the scanned ones reach a GPU") is `harvest.py`'s `no_text_layer` branch,
routed on the same classifier this skill already calls at `harvest.py:363`.

Parse routes on text presence alone. `render_reason()` also routes on vector
geometry, catching pages that carry plenty of text but whose *content* is
visual. Parse passes those through and drops the figure silently.

anydoc ships its own agent skill, which is text-only and points scanned files at
paid Parse. That is the competing baseline, and it sharpens the positioning in
§8: everything they route to a paid API, this routes to the seat already paid
for.

The one idea worth taking is per-region prompting, including LaTeX for
formulas — §4.5. Region-level prompting generally, and a `fast|auto|ocr` mode
switch, are logged as follow-up work.

## 4. Architecture

```
                   ┌─ pdf ──────────────► harvest.py         routing UNCHANGED
                   │                       pdf-inspector + PyMuPDF geometry
input ─► detect ───┼─ docx / xlsx / pptx ─► office.py + ooxml.py
   format_from_    │                       text, units, assets, charts
   bytes, not ext  └─ png/jpg/tiff/webp ──► image.py
                                                    │
                             all paths converge ────┴──► filters.py
                                                          furniture · dedup
                                                                │
                                                artifact.py · cache.py
                                                     describe.py (labels)
```

### 4.1 Module boundaries

| Module | Responsibility | Depends on |
|---|---|---|
| `harvest.py` | PDF routing. Behaviour unchanged; imports shared filters instead of defining them | `pdf-inspector`, `pymupdf`, `filters` |
| `filters.py` | **New.** `furniture_reason`, `_tok`, and the constants they read. Nothing else | stdlib only |
| `ooxml.py` | **New.** pptx: presentation-part discovery, `sldIdLst` surgery, re-zip. xlsx: sheet names, charts, media. Nothing for docx | stdlib only |
| `office.py` | **New.** Orchestrates anydoc + `ooxml`, emits the `harvest()` contract | `firecrawl-anydoc`, `ooxml`, `filters` |
| `image.py` | **New.** One image → one item | stdlib only |
| `convert.py` | Format dispatch, then unchanged | all adapters |
| `describe.py` | **Changed** — unit labels, see below | `artifact` |
| `artifact.py`, `cache.py` | Unchanged except a second engine constant (§5) | — |

**The pixel-hash dedup does not move.** Revision 1 proposed lifting it into
`filters.py`. `harvest.py:417-449` is deliberately entangled with xref and
raw-stream shortcuts that exist to avoid re-encoding every image, and moving it
risks perturbing measured routing for no gain. The Office analogue is three
lines of `sha256(asset.data)` and lives in `office.py` with a comment saying
exactly why it is not shared.

**`describe.py` does change, and carefully.** `describe.py:41-42` sorts by
`(x["page"], x["id"])` and formats `**[p{i['page']}] …**`. Office units are
strings, so a mixed batch raises `TypeError` and a sheet renders as
`[pSheet2]`. It needs a unit-label-aware line that keeps `[p{n}]` byte-exact
for integer pages — `example/sample-report.expected.md` and the gate corpus
depend on it — and a sort key tolerant of both. The gate compares stripped
text, so it would not catch a label regression; an expected-output assertion
must.

**The `filters.py` lift breaks a promise that must be repaired in the same
commit.** `reference/harvest-block.md` is a verbatim copy of `harvest.py` whose
stated purpose is that an agent unable to execute a file can paste it and get
identical routing. Once `harvest.py` imports from `filters.py`, the pasted
block fails. `tests/check_sync.py` must render the block as `filters.py`
followed by `harvest.py` with the import line elided, and assert that import
line matches an exact literal so the elision cannot silently drift. Its HEADER
text and `SKILL.md`'s repetition of the promise both change with it.

### 4.2 The adapter contract

Every adapter returns the dict `harvest()` returns, so `convert.py` and
everything downstream stay ignorant of format. Office and image adapters return
`pdf_type: null`, and `page` carries a unit label rather than an integer.

### 4.3 Routing is thin for Office, and that is the honest outcome

`render_reason`, `grid_pages` and `cost_guard` are PDF-only. All three exist
because a PDF page is a program of drawing commands that hides its figures;
OOXML declares its images in the package. There is also no slide or sheet render
to fall back to without LibreOffice, which §2 rules out.

Office routing is: extract assets → `furniture_reason` → byte-hash dedup →
describe. This asymmetry belongs in the README plainly. The selective-routing
advantage is a PDF phenomenon; what Office inherits is the furniture filters,
the artifact and citation contract, and the describe rubric.

`UBIQUITY` is close to vestigial here — §3.3 shows inherited furniture never
enters the count, and a genuinely repeated pasted image is already collapsed by
dedup. It stays because it costs nothing and the residual case is real, but no
claim rests on it.

### 4.4 Native charts — xlsx only

Revision 1 claimed anydoc drops charts in all three formats. **That was wrong**,
and running the wheel caught it. `shared/drawingml.rs:11-70` implements
`chart_blocks()`, emitting a bold title plus a categories × series table from
`c:numCache`/`c:strCache`, called from `pptx/mod.rs:584` and
`docx/content.rs:527`. Implementing our own for those formats would have emitted
every chart **twice** — once in anydoc's base text, once in a delimited block.

It is **not** called from the sheet path, and the gap there is wider than
charts. **[run]** on a workbook containing `xl/media/image1.png` and
`xl/drawings/drawing1.xml`:

```
anydoc assets for xlsx: 0 []
markdown: '| value |\n| --- |\n| 7 |'
```

The xlsx path is pure calamine cell extraction — drawings, images, charts and
chart sheets are dropped with no trace. So `ooxml.py` owns images and charts for
xlsx alone, and neither for docx or pptx.

**Caches are producer-dependent, so extraction must not depend on them.**
**[run]** python-pptx writes caches; openpyxl writes none. For xlsx this is
recoverable by construction: the referenced ranges are in the same workbook, so
the extractor resolves `c:f` ranges against sheet data when caches are absent.
Coverage is therefore cache-hit ∪ reference-resolution.

Two residues to count in `dropped`, never to paper over:

- Scatter and bubble charts. `drawingml.rs:36-46` reads `c:cat`/`c:val` only, so
  `c:xVal`/`c:yVal` series yield a title and no data *even on the paths anydoc
  handles*. Detect and count as `native_chart_unread`; do not out-extract
  anydoc inside the delimited region for pptx/docx, which would break §6.1.
- Charts recoverable by neither cache nor reference. An OOXML chart has no
  rendered image, so there is no vision fallback and the content is simply
  unavailable. Limitations, not a promise.

`numCache` being "stale" relative to live data is not a defect here: the cache
is what the chart *displays*, so matching it is document fidelity.

### 4.5 Formula guidance in the describe rubric

`reference/describing-visuals.md` gains a Formulas section: transcribe as LaTeX,
preserve equation numbering, mark unreadable subscripts rather than guessing.
Parse budgets formulas separately for this reason, and `olmocr_arxiv_math` is
522 of the 2,342 benchmarked files. A rubric change, not a routing change,
applying to both paths.

### 4.6 Citations

| Format | Unit | Citation | Derived from |
|---|---|---|---|
| pdf | page | `[p12]` | unchanged |
| pptx | slide | `[s07]` | `sldIdLst` order, via repacking |
| xlsx | sheet | `[Sheet2]` | emitted heading blocks (§3.5) |
| docx | heading | `[§Budget assumptions]` | the document's own label |
| image | whole | `[img]` | — |

**docx citations use the document's own heading label, never a synthesized
number.** Revision 1 proposed deriving `[§3.2]` by counting heading levels.
Real documents have unnumbered headings, appendices and restarts, so a counted
number would not match what the user sees in Word — which defeats the point of a
citation. anydoc already prepends the visible number of a numbered heading
(`docx/content.rs:86-92`); use that verbatim when present, fall back to heading
text, then to positional `[h07]`. Duplicate heading texts get positional
disambiguation.

`pages/` keeps its name and holds units under positional filenames
(`u001.md`), because sheet names and heading text contain characters hostile to
filenames. The human label goes in the file's first line and in the manifest;
citations use the label, greps find either.

### 4.7 Errors

| anydoc | status |
|---|---|
| `EncryptedError` | `encrypted` |
| `MalformedError`, `MissingPartError` | `unreadable` |
| `UnsupportedError` | `unsupported` (new; terminal, reported, batch continues) |
| `ResourceLimitError` | `unreadable`, with `limit` in `detail` |
| `OSError` | `unreadable` — the binding raises this, not `ConvertError`, for a file it cannot read |

**Unit-level failures must not be document-terminal.** Whole-deck conversion
skips a corrupt slide (`pptx/mod.rs:120-127`); a repacked single slide instead
hits `failed == len(slide_paths)` and raises `MalformedError`
(`pptx/mod.rs:210-212`). Mapped naively that kills a 60-slide deck for one bad
slide. A per-unit failure is recorded in `dropped` and the remaining 59 units
are produced.

`ResourceLimitError` is **not** an image-count ceiling. **[run]** it fires as
`max_entry_bytes` — `word/media/image1.png declares 201326592 decompressed
bytes` — a zip-bomb guard at a deliberately non-configurable 128 MiB
(`package/limits.rs:35`). Ordinary image-heavy documents do not trip it, and
crafted bombs should. Per-slide repacking makes the cap per slide for pptx.

### 4.8 Unviewable media

anydoc retains `image/emf`, `image/wmf` and OLE payloads
(`application/vnd.ms-ole-object`). Without a rasterizer the host agent cannot
view them, so routing one to `pending` creates an item no agent can complete.
Assets are filtered to media types the agent can actually read; SVG is passed as
text; everything else is dropped as `unviewable_media(<type>)` and **counted**.

This is a real content-loss path — for EMF content the material is neither
extracted nor viewable — and legacy-era documents are full of WMF. It belongs
in Limitations with a measured frequency, not a footnote.

## 5. Cache and versioning

**Engine strings are per format.** `cache.py:31` hashes the engine into every
artifact key, so a single combined `ENGINE` would invalidate every cached *PDF*
artifact the moment Office support ships — re-billing every vision call already
paid for, on a path §2 promises is unchanged. `cache_dir()` already accepts
`engine=`: PDF keeps `"pdf-inspector==0.2.6"`, Office passes
`"anydoc==0.1.6"`. Future anydoc bumps then cost nothing on the PDF side.

`SCHEMA` stays at 1; the artifact layout does not change.

anydoc is days old and its API stability is unproven. The exact pin and the
cache key contain the correctness risk, but not the maintenance risk: this
design couples to several undocumented internals — `sldIdLst` driving
`slide_paths`, per-slide concat equalling whole-deck, one table block per
non-empty sheet, asset dedup by part, chart table shape. `tests/test_anydoc_
invariants.py` asserts each against committed fixtures, so an upgrade that
breaks one fails loudly instead of corrupting output quietly.

## 6. Validation

**No Office ground-truth extraction benchmark exists.** OmniDocBench,
olmOCR-bench and the rest are PDF/page-image based; VLM-SlideEval measures VLM
comprehension of slides, not extraction fidelity. Validation is therefore
self-referential and construction-based.

### 6.1 Byte-identity gate, extended

`eval/gate.py` proves stripped `doc.md` equals raw engine output exactly. For
docx and xlsx the reference is `anydoc.to_markdown_bytes(file)`; for pptx it is
the per-slide repack concatenation, because repacking is part of the pipeline
under test and comparing against a whole-deck run would test anydoc instead.
The hostile-payload and re-describe legs port unchanged.

The concat-vs-whole-deck agreement rate is recorded as a corpus statistic. The
one divergence class is source-understood (§3.4), so any *other* divergence is a
bug detector.

xlsx chart tables and unit labels are the two things the gate cannot see —
chart output is inside delimiters and labels are stripped — so both need
expected-output assertions of their own.

### 6.2 Chart validation is unusually strong

Ground truth is in the XML being parsed. Three tests, all exact string
equality, no judge and no tolerance: a hand-built zip fixture with caches, where
output must equal the table the test wrote; an openpyxl fixture without caches,
where the extractor must resolve `c:f` ranges to the values the test wrote; and
a corpus-level self-consistency check re-deriving each chart's table from the
workbook's own sheet data.

### 6.3 Office corpus

A 13th corpus pinned as the existing 12 are. Sources verified reachable:

- **xlsx — SEC EDGAR `Financial_Report.xlsx`**, per-filing stable URLs, public
  domain. `fetch.py` needs a per-host User-Agent override — SEC returns an HTML
  block page to a bare UA and the file to a contact-bearing one — plus their
  10 req/s limit alongside the existing `SLOW_HOSTS` mechanism.
- **pptx — NASA NTRS**, per-file stable URLs, public domain.
- **docx and legacy-era all three — Digital Corpora govdocs1**, explicitly
  redistributable. Distributed as per-type zips rather than per-file URLs, so
  manifests gain a member form pinning both zip and member sha256, and the
  magic-byte check becomes format-aware (`PK\x03\x04` plus
  `[Content_Types].xml`) instead of `%PDF-`. Its own documentation warns that
  extensions lie — validate by content and expect malformed members, which are
  good input for the error taxonomy.

**Paired-format documents are the only external quality signal available.**
Institutions often publish the same document as both docx and PDF. On such
pairs the already-benchmarked PDF path is a trusted reference: convert both and
compare content coverage. The two paths' failure modes are independent, so
divergences localize bugs. Worth 20–30 pairs even if collected by hand.

### 6.4 What may and may not be claimed

**"Cheaper by N×" cannot be claimed for Office and must not appear in the
existing table.** That column is `opt_tok / ours_tok` where `opt_tok` is a
140-dpi page render (`bench.py:42-57`). Office has no render, so the
denominator would silently mean something different in the same table — exactly
the unmeasured claim §2 forbids. Office gets its own table with its baseline
stated, and "vision calls per page" becomes per *unit*, labelled as such.

`office_bench.py` can honestly measure: text tokens; assets extracted versus
sent to vision, which is the Office descendant of "69 placements → 1"; vision
calls per unit; chart tables recovered at zero vision cost with residue counts;
and unviewable-media counts.

May be claimed on measurement: those numbers, and byte-identity with anydoc's
text — stated as the opendataloader note states pdf-inspector equality,
"anydoc's number, enforced not asserted". May **not** be claimed: any Office
"cheaper by" ratio, any OCR-quality comparison with Parse, any figure-description
accuracy, or EMF/WMF coverage.

Limitations gains: the §4.3 routing asymmetry, unviewable legacy media with
measured frequency, the scatter and cacheless chart residue, and heading-less
docx citation granularity.

## 7. Open questions

Revision 1 listed four. Two are retired by measurement, recorded in §4.7 and
§3.4. The remainder, plus what running the wheel raised:

1. **docx heading-less fallback.** Decision rule: measure the fraction of
   corpus docx with zero headings. Above 20%, whole-document citation is a
   first-class path in SKILL.md rather than a footnote. Contracts structured as
   numbered lists rather than Heading styles are the population at risk.
2. **Repack robustness on real decks.** §3.4 is verified on anydoc's fixtures
   and constructed decks, not on a corpus. Falsified if any deck converts
   whole-deck but fails per-slide, if element-form or exotic-prefix `sldIdLst`
   breaks the surgery, or if `.pptm` fails.
3. **Unviewable-media frequency.** §4.8's handling is decided; its cost is not
   measured. Determines whether it is a Limitations line or a headline caveat.
4. **Unit-file naming.** §4.6 chooses positional `u001.md`. This is the one
   decision that would force `SCHEMA = 2` if it turns out wrong, so it is
   settled before implementation, not after.

## 8. Positioning

The vision layer is the agent's own eyes. That is the entire commercial
argument, and it is why this is a skill rather than a library or a service.

Firecrawl Parse bills 1 credit per page, flat, whether or not a page needed
OCR — roughly $0.83–3.20 per 1,000 pages depending on plan, on top of an
account, an API key and an upload of the documents to a third party. This skill
spends the subscription the user already pays for. No second bill, no key, and
no document leaves the machine.

Selective routing is what makes that practical rather than merely possible. At
1.00 vision calls per page a subscription-funded agent burns its budget on the
first document; at the measured 0.34 it does not. The routing is not only a cost
optimisation — it is what lets the vision layer live inside a seat licence at
all. `SCALE_GUARD` continues to work for Office unchanged, because it gates on
`len(pending)` regardless of format.

Two honesty constraints:

- The comparison against a per-page service is **a billing-model claim, not a
  quality claim.** Parse's OCR on a scanned page may well read better than a
  general agent's. That is unmeasured here and must not be implied.
- **Local execution is a feature to state, not to overclaim.** Nothing in the
  pipeline makes a network call — anydoc, pdf-inspector and PyMuPDF are all
  local. Whether the agent's own vision calls leave the machine depends on the
  host, which this skill does not control and must not make promises about.

### Public claim

> Reads PDFs, Word, Excel, PowerPoint and images. Extracts text locally and
> exactly, then spends your agent's own eyes only on what text extraction
> provably missed — no API key, no per-page bill, no upload.

Everything beyond that is measured or is not claimed.
