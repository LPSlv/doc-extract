# pdf-extract — design

**Date:** 2026-08-03
**Status:** approved design, pending implementation plan
**Repo:** `LPSlv/pdf-extract` (MIT)

## 1. Purpose

An agent skill that turns one or many PDFs into a durable, citable Markdown artifact —
including the content that text extraction silently drops (charts, diagrams, scanned
pages, tables the extractor failed on) — and then answers questions against that
artifact cheaply.

Two modes, in order:

1. **Convert** — produce Markdown + extracted images + a manifest, cached by content hash.
2. **Answer** — respond to questions against the cached artifact with `[p12]` page citations.

The skill must work identically under Claude Code and Codex, require no API key, and
require no installation step from the user.

## 2. Non-goals

- Not a general PDF toolkit. No merging, splitting, form filling, watermarking, encryption.
  `anthropics/skills@pdf` already covers those; this skill is about faithful ingestion.
- Not an OCR engine. It routes to a vision model rather than shipping Tesseract.
- Not a competitor to Marker/MinerU/Docling on raw text extraction. It delegates that
  to pdf-inspector and is bounded by pdf-inspector's quality (see §9).

## 3. Evidence base

Every threshold in this design was measured, not guessed. Two corpora were used during
design: five real local documents (ESA BIC grant paperwork, an MSc thesis, a CAD drawing)
and the 200-PDF `opendataloader-bench`.

### 3.1 Embedded-image extraction is necessary but not sufficient

PyMuPDF `get_images()` — equivalent to Photoshop's "open PDF images separately" — returns
only image XObjects. Vector artwork (charts drawn by Excel/Word/matplotlib) is path
operators with no image object to extract.

| Document | Pages | Raster XObjects | Vector ops |
|---|---|---|---|
| ESA_BIC_LV funding guidelines | 14 | 69 | 20 |
| **ESA_ERAF_Metodika_v3** | 9 | **0** | 237 |
| ESA_BIC_Latvia_MTR_Optonics | 16 | 23 | 1450 |
| Lenards_Msc_Thesis_VLAs | 46 | 25 | 1280 |
| housing_VSZ (CAD) | 1 | 2 | 370 |

Metodika returns an empty image list. Both mechanisms are required.

### 3.2 Raster extraction is dominated by furniture

The 69 "images" in the guidelines PDF are **7 distinct** objects: a sidebar stripe placed
14×, two thin rules placed 26× total, three logos placed 27× total, and **one** real
1347×758 graphic. Naive extraction pays 69 vision calls for 1 unit of content.

### 3.3 Vector ops are dominated by tables, not figures

Every "vector page" in the grant corpus is 100% rectangles with **zero curves** — shaded
table cells (MTR, ink fraction 0.29–0.46) and decorative section banners (Metodika, ink
0.03–0.07). Naive "render pages with drawing ops" would render 16 pages of tables the
text extractor already handled.

Ground truth was established by rendering and visually inspecting two ambiguous pages:

- **Metodika p2** — prose with decorative header banners. Nothing visual. Must skip.
- **MTR p9** — cost tables with merged spanning headers that pdf-inspector failed to
  extract (0 Markdown table rows). Must render.

Identical signatures (0 curves, no extracted table); opposite correct verdicts. Ink
fraction separates them cleanly (0.07 vs 0.33).

### 3.4 Filter results

| Document | Naive calls | Final | Correct |
|---|---|---|---|
| guidelines | 7 | **1** | the one real graphic |
| Metodika_v3 | 5 | **0** | matches ground truth |
| MTR_Optonics | 20 | **10** | renders exactly p9, p11 |
| Thesis | 33 | **12** | 8 figures + 4 chart pages |
| housing (CAD) | 3 | **1** | — |

68 → 24 vision calls, verified correct on both hand-inspected pages.

### 3.5 A hypothesis that did not survive

Pixel-hash dedup was designed to collapse the eleven distinct 929×929 images in the
thesis, inferred to be one bitmap stored repeatedly. Measured: **zero** collapses across
all five documents. They are genuinely different plots. The check is retained as cheap
insurance but is **unproven** and must not be described as fixing an observed problem.

## 4. Architecture

Five phases. Phases 0–3 are deterministic; phase 4 needs a model; phase 5 is querying.

```
PDF ──0── sha256 → cache dir ──(hit)──────────────────────────► phase 5
           │
           1── detect_pdf → type + pages_needing_ocr
           │
           2── extract_pages_markdown → pages/pNNN.md + doc.md
           │
           3── visual harvest ──► images/*.png + manifest.json (description: null)
           │
           4── agent reads each image, writes description back, splices into Markdown
           │
           5── answer questions with [pN] citations
```

### Phase 0 — Resolve and cache

`sha256(pdf)` → `~/.cache/pdf-inspect/<sha>/`. If `manifest.json` exists with no null
descriptions, it is a cache hit; skip to phase 5. Same PDF under any path, in any
project, is never converted or vision-parsed twice. `--out <dir>` additionally
materializes `doc.md` + `images/` into a chosen location (e.g. a Grantflow vault).

### Phase 1 — Classify

`pdf_inspector.detect_pdf` → `pdf_type` ∈ {text_based, scanned, image_based, mixed} and
`pages_needing_ocr`. The library reports which pages have no text layer, so scanned-page
routing needs no heuristic at all.

### Phase 2 — Text

`pdf_inspector.extract_pages_markdown` → one file per page plus a concatenated `doc.md`.
Pages in `pages_needing_ocr` get a placeholder to be filled in phase 4.

### Phase 3 — Visual harvest

Four filters in sequence:

1. **Furniture** — drop an image if placed on >50% of pages (and doc >2 pages), or
   <120px on either side, or aspect ratio >8:1, or area <40 000px².
   *Effect: 69 placements → 1 on the guidelines.*
2. **Pixel-hash dedup** — sha256 of the decompressed image bytes; keep one representative
   per hash. *Unproven on the design corpus; retained as insurance.*
3. **Table cross-check** — if the page's extracted Markdown already contains ≥3 table
   rows, skip it. The extractor won; do not second-guess it.
   *Effect: MTR 11 vector pages → 2.*
4. **Curves-or-grid-and-ink** — render the page if `curves > 0` **OR**
   (`≥4 distinct x-edges` AND `≥4 distinct y-edges` AND `ink fraction ≥ 0.15`).
   *Effect: drops Metodika's banners, keeps MTR's merged-header cost tables.*

Then **page-level subsumption**: if a page is being rendered, drop the individual rasters
it contains — the page render already covers them. *Effect: thesis 23 images → 8.*

Then the **scale guard**: if kept images + render pages > 15, report the count and stop
for confirmation before spending vision calls.

Renders are 150 dpi PNG via `pdftoppm`.

### Phase 4 — Vision pass (the agent)

The agent iterates manifest entries with `description: null`, reads each image with its
own native image capability, and writes the result back. No API key, no separate model
call, identical under Claude Code and Codex.

Two description modes, per `reference/describing-visuals.md`:

- **Figure** — type, what it shows, axes and units, notable values, all legible text.
- **Page transcription** (for `pages_needing_ocr` and rendered pages) — verbatim content,
  tables reconstructed as Markdown.

### Phase 5 — Answer

Per-page files plus the manifest let the agent grep and read only what a question needs,
citing `[p12]`. This is why conversion is worth caching.

## 5. The additive-only rule

**Where pdf-inspector produced text for a page, its Markdown is authoritative. Vision
output is appended as figure descriptions and never replaces it. Only where pdf-inspector
produced nothing does vision become the page content.**

This is not a style preference — it is what makes the benchmark guarantee in §8 hold by
construction rather than by hope. It also bounds the blast radius: the skill cannot make
text extraction worse than the engine it delegates to.

## 6. Output contract

```
~/.cache/pdf-inspect/<sha256>/
  source.json      {path, sha256, bytes, converted_at, pdf_type, page_count}
  doc.md           full document, page-anchored
  pages/p001.md    per-page Markdown
  images/p07-1.png extracted rasters and page renders
  manifest.json
```

`manifest.json` entries:

```json
{
  "id": "p07-1",
  "page": 7,
  "kind": "raster | page_render",
  "path": "images/p07-1.png",
  "reason": "curves>0 | grid+ink | pages_needing_ocr | standalone_raster",
  "px": [1347, 758],
  "description": null
}
```

`reason` is recorded so a wrong routing decision can be diagnosed without re-running.

## 7. Packaging

Prose skill, no bundled executable code. Heuristics appear in `SKILL.md` as **verbatim
runnable blocks** the agent pastes and runs, not as prose to reinterpret — this keeps the
determinism that matters while leaving nothing to maintain separately.

```
LPSlv/pdf-extract
  README.md            benchmark numbers, install, examples
  LICENSE              MIT
  skills/pdf-extract/
    SKILL.md
    reference/describing-visuals.md
  eval/
    opendataloader.md  regression gate procedure + results
    oldscans.md        olmOCR-bench old_scans procedure + results
    local-fixtures.md  expected counts for the 5 private documents (no PDFs committed)
```

Install: `npx skills add LPSlv/pdf-extract@pdf-extract`.
Locally: symlink `~/.agents/skills/pdf-extract` → repo, preserving the existing
`~/.claude/skills` and `~/.codex/skills` symlink pattern.

Runtime dependency is `uv` only. Scripts declare deps inline (PEP 723), so
`uv run` resolves `pdf-inspector` and `pymupdf` on first use with nothing installed
globally and no virtualenv to manage. Verified working. `pdftoppm` (poppler) is used for
rendering; PyMuPDF is the fallback if poppler is absent.

## 8. Validation

### 8.1 opendataloader-bench — regression gate

The benchmark Firecrawl themselves publish against (200 PDFs, Apache-2.0, official
NID/TEDS/MHS evaluators in-repo). Their published result:

| Engine | Overall | Reading order | Tables | Run |
|---|---|---|---|---|
| **pdf-inspector** | **0.875** | **0.915** | **0.814** | 2.8s |
| LiteParse | 0.870 | 0.908 | 0.693 | 13.9s |
| OpenDataLoader | 0.843 | 0.912 | 0.489 | 9.8s |
| PyMuPDF4LLM | 0.735 | 0.886 | 0.401 | 15.5s |
| MarkItDown | 0.583 | 0.879 | 0.000 | 6.7s |

**Target: equal, not better.** Measured headroom on this corpus is effectively zero:

- 42/200 documents have ground-truth tables; pdf-inspector extracts one in **40**.
- Its 0.814 comes from TEDS structure error on merged cells and **11 spurious tables**,
  not from misses. Neither is addressable by a visual layer.
- Of the 2 genuine misses, filter 4 flags **neither**.
- The corpus is 200 pages across 200 PDFs — all single-page — and 199/200 are
  `text_based`. One image-based document in the entire set.
- The skill would nonetheless fire on 100/200 documents (128 vision calls). With no
  upside available, that is pure regression risk.

Under the §5 additive-only rule, scored output is byte-identical to pdf-inspector's, so
0.875 / 0.915 / 0.814 is guaranteed structurally. Integration is via
`src/engine_registry.py` + a `pdf_parser_pdfextract.py` **in a local checkout of the
benchmark repo** — eval harness glue, not part of the published skill (§7) — then
`uv run src/evaluator.py --engine pdf-extract`.

Gate: **overall ≥ 0.875, reading order ≥ 0.915, tables ≥ 0.814.** Any drop is a bug.

### 8.2 olmOCR-bench `old_scans` — where the visual layer wins

134 PDFs (`old_scans` 98 + `old_scans_math` 36), 984 unit tests, ODC-BY.

Verified on a 6-PDF sample: every one classifies as `scanned` with
`pages_needing_ocr=[1]` and **`text_chars=0`**. pdf-inspector alone scores ~0 because
there is no text layer to extract. Rendering at 140 dpi and reading the page recovers the
content in full — confirmed end to end on a handwritten 1914 letter, a case Tesseract
also fails.

This is the one place an official benchmark can measure what this skill adds.

### 8.3 Local fixtures — smoke test

The five design documents, with expected counts from §3.4 committed to
`eval/local-fixtures.md`. The PDFs are **not** committed: they contain Optonics budget
figures, named individuals and contract detail.

## 9. Known limitations

State these in the README; do not let them be discovered by users.

- **Thresholds are tuned on a small sample.** Four numbers (50%, 120px, 8:1, 0.15 ink)
  fitted to five documents, two verified by eye. §8.1 exercises them against 200 more,
  but only for regression, not correctness of routing.
- **Unshaded merged-header tables are a blind spot.** Low ink would skip them, and if the
  extractor also dropped them the content is lost silently. Filter 3 catches the easy
  cases and shading catches the hard ones, but the intersection is a real gap.
- **Quality is bounded by pdf-inspector** for all text. If it misreads a page, so do we.
- **No benchmark scores figure comprehension.** opendataloader-bench, olmOCR-bench and
  OmniDocBench all measure text fidelity. The core value-add is unmeasured by available
  instruments, and §8.3 is the only check on it.
- **OmniDocBench is unusable here** — it ships rendered JPGs plus JSON, not PDFs, so the
  vector discriminator cannot run at all.
- **Vision cost is real.** 0.6 calls/document on business PDFs, but 12 on a 46-page
  thesis. The scale guard exists for this.

## 10. Open questions

- Should `--visual` be opt-out rather than default for very large batches? Current
  decision: default on, scale guard at 15.
- Does the answer mode need an index beyond per-page files and grep for documents in the
  hundreds of pages? Deferred until a real document demands it.
