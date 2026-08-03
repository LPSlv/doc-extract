# pdf-extract — design

**Date:** 2026-08-03 (rev 2, after adversarial review)
**Status:** approved design, pending implementation plan
**Repo:** `LPSlv/pdf-extract` (MIT)

## 1. Purpose

An agent skill that turns one or many PDFs into a durable, citable Markdown artifact —
including the content that text extraction silently drops (charts, diagrams, scanned
pages, tables the extractor failed on) — and then answers questions against that
artifact cheaply.

1. **Convert** — Markdown + extracted images + manifest, cached by content hash.
2. **Answer** — questions against the cached artifact, with `[p12]` page citations.

Must work identically under Claude Code and Codex, need no API key, and need no
installation step beyond `uv`.

## 2. Non-goals

- Not a general PDF toolkit (merge/split/forms/encryption). `anthropics/skills@pdf`
  covers those.
- Not an OCR engine. It routes to a vision model instead of shipping Tesseract.
- Not a competitor on raw text extraction. It delegates that to pdf-inspector and is
  bounded by pdf-inspector's quality.

## 3. Evidence base

Every threshold was measured. All numbers in this document are regenerated from
`skills/pdf-extract/harvest.py`, which is the single source of truth; the SKILL.md
prose embeds that file verbatim (§7). **Numbers are never hand-carried into the spec.**

Corpora: five real local documents (ESA BIC grant paperwork, an MSc thesis, a CAD
drawing), the 200-PDF `opendataloader-bench`, and synthetic matplotlib figures.

### 3.1 Embedded-image extraction is necessary but not sufficient

PyMuPDF `get_images()` — the equivalent of Photoshop's "open PDF images separately" —
returns only image XObjects. Vector artwork has no image object to extract.

| Document | Pages | Raster XObjects | Vector ops |
|---|---|---|---|
| ESA_BIC_LV funding guidelines | 14 | 69 | 20 |
| **ESA_ERAF_Metodika_v3** | 9 | **0** | 237 |
| ESA_BIC_Latvia_MTR_Optonics | 16 | 23 | 1450 |
| Lenards_Msc_Thesis_VLAs | 46 | 25 | 1280 |
| housing_VSZ (CAD) | 1 | 2 | 370 |

### 3.2 Raster extraction is dominated by furniture

The 69 "images" in the guidelines PDF are **7 distinct** objects: a sidebar stripe (14
placements), two rules (26), three logos (27), and **one** real 1347×758 graphic.

### 3.3 Vector ops are dominated by tables and decoration, not figures

Every vector page in the grant corpus is 100% rectangles with **zero curves** — shaded
table cells (MTR, ink 0.29–0.46) and section banners (Metodika, ink 0.03–0.07). Ground
truth was established by rendering and looking:

- **Metodika p2** — prose with decorative banners. Nothing visual. Skip.
- **MTR p9** — cost tables with merged spanning headers that pdf-inspector failed to
  extract (0 table rows). Render.
- **guidelines p13** — a dark presentation slide whose left margin carries a decorative
  line pattern (40 axis-aligned strokes, ink 0.008). Skip.

### 3.4 Two hypotheses that did not survive

**Pixel-hash dedup** was designed to collapse eleven distinct 929×929 thesis images
inferred to be one bitmap stored repeatedly. Measured: **zero** collapses across all five
documents. They are different plots. Retained as cheap insurance, explicitly **unproven**.

**"Curves or grid+ink" missed stroke-based charts.** A matplotlib line plot without a
legend has `curves=0` and non-white ink `0.000`; a scatter with square markers has
`curves=0, diagonals=0`. Both were invisible to the original rule. The thesis figures
passed only because legend boxes have rounded corners emitting bezier ops. Fixed by two
added signals (§4, Phase 3) — diagonal segments, and sparse-rect-with-many-strokes —
each gated by a stroke-bounding-box test so that margin wallpaper (guidelines p13) does
not read as a scatter plot.

### 3.5 Filter results, regenerated from `harvest.py`

| Document | Unfiltered | Final | Composition |
|---|---|---|---|
| guidelines | 7 | **1** | 1 raster |
| Metodika_v3 | 5 | **0** | — |
| MTR_Optonics | 20 | **10** | 8 rasters + 2 dense_grid (p9, p11) |
| Thesis | 33 | **17** | 7 rasters + 5 curves + 5 sparse_plot |
| housing (CAD) | 3 | **1** | 1 no_text_layer |

68 → 29. Synthetic controls: `chart_line` fires `diagonals`, `chart_scatter` fires
`sparse_plot`, both previously missed.

Across `opendataloader-bench` (200 PDFs): **0 errors, 106 documents touched, 133 calls**
— `standalone_raster` 109, `curves` 13, `dense_grid` 7, `sparse_plot` 3, `no_text_layer` 1.

## 4. Architecture

```
PDF ──0── sha256+versions → cache dir ──(hit)──────────────► phase 5
           1── detect_pdf → type + pages_needing_ocr
           2── process_pdf → doc.md        (authoritative text)
           3── visual harvest → images/ + manifest.json
           4── agent describes images, splices DELIMITED blocks
           5── answers with [pN] citations
```

### Phase 0 — Resolve and cache

Cache key is `sha256(pdf) + engine version + skill schema version`. A hash-only key would
serve stale artifacts forever after a threshold or engine change while the README
advertises new numbers. `--out <dir>` additionally materializes `doc.md` + `images/`.

### Phase 1 — Classify, and refuse to cache a silent failure

`detect_pdf` → `pdf_type` and `pages_needing_ocr`.

**Encrypted PDFs do not raise.** A password-protected file returns `pdf_type="scanned"`,
`pages_needing_ocr=[]`, and `process_pdf().markdown == ""` — which the naive design would
cache as a successful, empty conversion. Grant contracts are exactly the files that
arrive encrypted. Phase 1 checks `needs_pass`/`is_encrypted` and fails loudly.

Empty extraction is an error **only if there is also no visual content**; a figure-only
page legitimately has no text and must still be processed.

### Phase 2 — Text

`process_pdf().markdown` is authoritative. This is not interchangeable with
`extract_pages_markdown`, which was the original choice and is measurably worse:

| API | Overall | Reading order | Tables |
|---|---|---|---|
| `extract_pages_markdown`, pages joined | 0.860 | 0.903 | **0.772** |
| `process_pdf().markdown` | **0.875** | **0.915** | **0.814** |

Independently confirmed: on 60 corpus documents the two disagree on 6, and on one
document `extract_pages_markdown` returns **nothing at all** while `process_pdf` returns
1601 characters. `extract_pages_markdown` is used **only** for the per-page table
cross-check in filter 3, never for output.

### Phase 3 — Visual harvest

Four filters, then subsumption, then the scale guard. All terms are defined numerically
in `harvest.py` and nowhere else — "ink fraction" and "distinct edges" left informal
produced two good-faith implementations that fired on 43/200 and 100/200 documents
respectively.

1. **Furniture** — drop if on >50% of pages (doc >2pp), or <120px per side, or aspect
   >8:1, or area <40 000px².
2. **Pixel-hash dedup** — sha256 of decompressed bytes. Unproven; insurance.
3. **Table cross-check** — page already yields ≥3 Markdown table rows → skip.
4. **Render if any branch fires**, each self-gated so a near-empty page cannot trip it:
   - `curves ≥ 8` — bezier artwork
   - `diagonals ≥ 4` — line chart / connected series
   - `axis_lines + diagonals ≥ 10 AND rects ≤ 20` — sparse plot (axes, ticks, markers)
   - `x_edges ≥ 4 AND y_edges ≥ 4 AND rects ≥ 8 AND ink ≥ 0.15` — shaded grid the
     extractor missed
   - the first three additionally require **plot-shaped strokes**: stroke bounding box
     ≥5% of page area and aspect ≤5:1

   Pages in `pages_needing_ocr` bypass all of this — there is no text to regress.

   The per-branch minimums matter: a tinted cover page with 2–6 drawing ops reaches
   ink 1.0 and would otherwise render under a bare `ink ≥ 0.15` rule.

Then **subsumption** (a rendered page replaces the rasters it contains), then the
**scale guard** at >15 calls.

### Phase 4 — Vision pass (the agent)

The agent iterates manifest entries with `description: null`, reads each image with its
own native capability, and writes back. No API key; identical in Claude Code and Codex.

Modes per `reference/describing-visuals.md`: **figure** (type, what it shows, axes and
units, notable values, legible text) and **page transcription** (verbatim, tables as
Markdown) for `pages_needing_ocr` and rendered pages.

### Phase 5 — Answer

Per-page files plus the manifest let the agent read only what a question needs, citing
`[p12]`. For multi-document runs citations are `[doc:p12]`.

## 5. The additive-only rule, and how it is enforced

**Where pdf-inspector produced text for a page, its Markdown is authoritative. Vision
output is appended and never replaces it. Only where it produced nothing does vision
become the page content.**

The original spec claimed this made benchmark output "byte-identical." It does not, on
its own — the evaluator scores the whole string with edit distance, and measurements show
even invisible additions cost points:

| Prediction variant | NID | TEDS | MHS |
|---|---|---|---|
| raw pdf-inspector | 0.887 | 0.918 | 0.854 |
| + one figure description | 0.488 | — | — |
| + one table transcription | 0.495 | 0.692 | — |
| + an HTML-comment page anchor only | 0.855 | — | 0.712 |

So the rule needs a mechanism, not a promise. **Every byte the skill adds — page
anchors, placeholders, descriptions — sits inside machine-strippable delimiters:**

```
<!-- pdf-extract:add -->
**Figure (chart, p7).** Stacked bar, 2024–2026, WP1–WP4 spend…
<!-- /pdf-extract:add -->
```

The benchmark harness runs the **full** pipeline, strips delimited blocks, and asserts
the residue is byte-identical to raw engine output. That converts §8.1 from an assertion
into a test that can fail. Without it the gate would benchmark the dependency and prove
nothing about the skill.

## 6. Output contract

```
~/.cache/pdf-inspect/<sha256>-<engine>-<schema>/
  source.json      {path, sha256, bytes, converted_at, pdf_type, pages, engine, schema, status}
  doc.md           authoritative text + delimited additions
  pages/p001.md    per-page, for navigation and citation
  images/…         rasters and page renders
  manifest.json
```

Manifest entries record **kept and dropped**:

```json
{
  "items":   [{"id":"p007-render","page":7,"kind":"page_render",
               "reason":"dense_grid","px":[1240,1754],"description":null}],
  "dropped": [{"xref":6,"px":[76,756],"why":"sliver"}]
}
```

Dropped candidates are recorded because **false negatives are the dangerous direction** —
a wrongly-skipped figure otherwise leaves no trace at all.

## 7. Packaging

Prose skill, no bundled executable dependency at runtime. `harvest.py` is the testable
canonical source; `SKILL.md` embeds its contents verbatim in a fenced block, and a CI
check asserts the two are identical. This keeps determinism without asking the agent to
reconstruct arithmetic from prose.

Robustness measures that survive the prose form:

- The harvest is **one code block**, not four steps to sequence. Sequencing — not
  arithmetic — is what gets dropped under context pressure, and filter 3 plus subsumption
  are the likeliest omissions since both join two data sources.
- A committed one-page fixture PDF with expected filter output, so an agent that mangled
  a paste finds out immediately.

```
LPSlv/pdf-extract
  README.md · LICENSE (MIT)
  skills/pdf-extract/SKILL.md · harvest.py · reference/describing-visuals.md
  eval/opendataloader.md · eval/oldscans.md · eval/local-fixtures.md
  docs/img/*.svg
```

Install: `npx skills add LPSlv/pdf-extract@pdf-extract`. Locally, symlink
`~/.agents/skills/pdf-extract` → repo, preserving the existing Claude/Codex pattern.

Runtime requirement is **`uv` only** — deps are declared inline (PEP 723), resolved on
first run, nothing installed globally. `pdftoppm` is used for rendering with PyMuPDF as
fallback. Engine is pinned: `pdf-inspector==0.2.6`. The published score belongs to a
version, not a name.

## 8. Validation

### 8.1 opendataloader-bench — regression gate

200 PDFs, Apache-2.0, official NID/TEDS/MHS evaluators in-repo. Firecrawl's published
result:

| Engine | Overall | Reading order | Tables | Run |
|---|---|---|---|---|
| **pdf-inspector** | **0.875** | **0.915** | **0.814** | 2.8s |
| LiteParse | 0.870 | 0.908 | 0.693 | 13.9s |
| OpenDataLoader | 0.843 | 0.912 | 0.489 | 9.8s |
| PyMuPDF4LLM | 0.735 | 0.886 | 0.401 | 15.5s |
| MarkItDown | 0.583 | 0.879 | 0.000 | 6.7s |

**Target: equal, not better.** Headroom on this corpus is effectively zero:

- 42/200 documents have ground-truth tables; pdf-inspector extracts one in **40**.
- Its 0.814 comes from TEDS structure error on merged cells and **11 spurious tables**,
  not from misses; neither is addressable by a visual layer.
- Of the 2 genuine misses, no render branch fires.
- The corpus is 200 pages across 200 PDFs — all single-page — and 199/200 `text_based`.
- The skill nonetheless fires on 106/200 documents. With no upside available, that is
  pure regression risk, which is exactly what the strip-and-compare gate contains.

Gate: strip delimited blocks, assert byte-identity with raw `process_pdf` output, and
assert **overall ≥ 0.875, reading order ≥ 0.915, tables ≥ 0.814**.

### 8.2 olmOCR-bench `old_scans` — where the visual layer wins

134 PDFs (98 + 36 math), 984 unit tests, ODC-BY. Verified on a sample: every one
classifies `scanned` with `pages_needing_ocr=[1]` and **`text_chars=0`**. pdf-inspector
alone scores ~0. Rendering at 140 dpi and reading recovers the content — confirmed end to
end on a handwritten 1914 letter, a case Tesseract also fails.

This is the only official benchmark that can measure what this skill adds.

### 8.3 Local fixtures — smoke test

The five design documents with expected counts from §3.5. PDFs **not** committed: they
contain Optonics budget figures, named individuals and contract detail.

## 9. Known limitations

- **Thresholds are fitted to a small sample.** Seven numbers tuned on five documents plus
  synthetic controls, three verified by eye. §8.1 exercises them on 200 more, but only
  for regression, not routing correctness.
- **Unshaded merged-header tables remain a blind spot.** Low ink skips them; if the
  extractor also dropped them, the content is lost silently.
- **Quality is bounded by pdf-inspector** for all text.
- **No benchmark scores figure comprehension.** opendataloader-bench, olmOCR-bench and
  OmniDocBench all measure text fidelity. The core value-add is unmeasured; §8.3 is the
  only check on it.
- **OmniDocBench is unusable** — it ships rendered JPGs plus JSON, not PDFs, so the
  vector discriminator cannot run.
- **Vision cost is real.** 0.67 calls/document on the benchmark corpus, but 17 on a
  46-page thesis. Hence the scale guard.
- **The scale guard conflicts with large scanned documents.** An 84-page scan needs 84
  mandatory renders and will always trip it. Behaviour on override, and what half-state
  the cache holds, must be defined in the plan.

## 10. Public claim

Defensible, and to be worded this way:

> Text is delegated to pdf-inspector 0.2.6 and verified byte-identical to it after
> stripping additions — **0.875 overall on opendataloader-bench**, the top score in
> Firecrawl's published comparison. Requires `uv`, nothing else. Adds figure and scan
> understanding that these benchmarks do not measure.

Not: "SOTA" (this is Firecrawl's own benchmark, on a 200-single-page corpus; rankings
differ on OmniDocBench). Not "zero setup" (`uv` is required). Not a claim that
pdf-extract's own extraction beats anything.

## 11. Open questions

- Resume semantics if phase 4 dies halfway: re-splice risks duplicate blocks. Delimiters
  make blocks idempotently replaceable, but the splice **position** is unspecified — the
  manifest has no bbox, so "at the figure's location" is not currently knowable. Either
  add bbox or define splice as end-of-page.
- Concurrency: two agents converting the same PDF race on the cache directory. Needs
  atomic rename or a lock.
- Whether answer mode needs an index beyond per-page files and grep. Deferred.
