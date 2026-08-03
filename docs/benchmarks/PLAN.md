# Benchmark suite plan

The routing thresholds in `harvest.py` were fitted on ~5 documents and
regression-tested on ~250. This suite measures whether they generalise to
thousands of unseen pages across genuinely different document classes, and
records cost (input tokens, vision calls, wall time) in a reproducible,
third-party-verifiable way.

**Scope boundary:** this suite *measures*. It does not tune thresholds — that
is deliberate, because tuning on the measurement set would invalidate it.
Negative results are reported as-is, with named files.

## Datasets

Every source below was probed live before this plan was written (HTTP 200 on
sample files, directory listings enumerated). No dataset is assumed.

| dataset | class | files (target) | source | license | what it uniquely tests |
|---|---|---|---|---|---|
| `arxiv` | born-digital LaTeX papers, full documents | 200 | `export.arxiv.org/pdf/<id><vN>`, IDs pinned with version | arXiv licenses (no redistribution) | vector figures/plots at document scale; the tile-grid pathology (`ai_latent-diffusion`); math that must NOT route |
| `pmc` | publisher-typeset biomedical journal articles | 220 | `ftp.ncbi.nlm.nih.gov/pub/pmc/deprecated/oa_pdf/xx/yy/`, paths pinned | PMC OA subset (mixed CC) | two-column publisher layouts, mixed raster/vector figures, many publishers' PDF generators |
| `bills` | US legislative text (GPO typesetting) | 220 | `govinfo.gov/content/pkg/BILLS-118hr<n>ih/pdf/…`, enumerated from public bulkdata JSON | US public domain | the zero-figure class: any vision call here is a false positive; line-numbered text, no figures at all |
| `olmocr_multi_column` | single pages, dense multi-column | 231 (all) | HF `allenai/olmOCR-bench` resolve URLs, sha256 pinned from HF LFS metadata | ODC-BY 1.0 | column layouts that stress text extraction; routing should stay quiet |
| `olmocr_headers_footers` | single pages, heavy furniture | 267 (all) | same | ODC-BY 1.0 | furniture filters (rules, letterheads) vs real content |
| `olmocr_arxiv_math` | single pages, dense display math | 522 (all) | same | ODC-BY 1.0 | equations are bézier-adjacent vector content that must NOT fire `curves`/`diagonals` |
| `olmocr_tables` | single pages, real tables | 188 (all) | same | ODC-BY 1.0 | `dense_grid`/`stroke_grid` branches; extractor-vs-vision table split |
| `olmocr_scans` | scanned pages (old_scans + old_scans_math) | 134 (all) | same | ODC-BY 1.0 | `no_text_layer` branch must fire on ~100% |
| `olmocr_long_tiny_text` | single pages, very small fonts | 62 (all) | same | ODC-BY 1.0 | adaptive-resolution edge (5th-percentile font sizing) |
| `datasheets` | electronics datasheets, many parts | ~200 attempted | TI `ti.com/lit/ds/symlink/<part>.pdf` + Diodes + Nexperia known-good URLs, curated part list | vendor copyright | the figure-dense case: curves, pinouts, schematics; extends the fitted 23-file `corpus/tds` |

Existing small corpora (`corpus/tds` 23, `corpus/papers` 25) are kept and
benchmarked with the same runner for continuity, but are not counted toward
the ≥200 goal.

Categories below 200 files are below 200 because the upstream source has no
more (olmOCR ships 134 scans, 62 tiny-text, 188 tables — we take all of
them); this is stated rather than padded. The datasheet corpus depends on
vendor URL hit-rate (ST/Microchip/onsemi block bots — verified 403); the
achieved count will be reported honestly.

Rejected candidates, with reasons:

- **OmniDocBench** — ships JPEGs, not PDFs. Useless here.
- **DocLayNet** — ships page images + COCO annotations, not the source PDFs.
- **PubLayNet** — ships images; the underlying PDFs are PMC anyway, which we
  take directly.
- **SEC EDGAR** — modern filings are HTML/XBRL, not PDF; PDF exhibits are
  unsystematic to enumerate. govinfo covers the government-document class
  with clean, enumerable, public-domain PDFs.
- **onsemi, ST, Microchip datasheets** — automated fetch blocked (403,
  verified live).

## Reproducibility mechanics

Corpora stay out of git (`corpus/` is already gitignored — copyright). What
is committed instead pins them exactly:

1. **URL lists** — `eval/manifests/<dataset>.urls.tsv` (filename, URL).
   Produced once by `eval/discover.py <dataset>` (also committed), which
   documents *how* the list was derived (API queries, directory listings,
   curated part lists). The lists are frozen; discovery is not re-run on
   fetch.
2. **Fetch** — `uv run eval/fetch.py <dataset>` downloads exactly the pinned
   list into `corpus/<dataset>/`, rejects anything that is not `%PDF`, and
   verifies sha256 against the manifest when one exists. Idempotent;
   parallel with polite per-host limits.
3. **Manifests** — `eval/manifest.py corpus/<dataset>` writes
   `eval/manifests/<dataset>.json`: per-file sha256, bytes, pages, plus
   summary (file count, page count, total bytes, page-count distribution
   min/p25/median/p75/p95/max). Committed, so every result is pinned to
   exact inputs. Files that upstream later removes or changes will fail the
   sha256 check loudly rather than drift silently.

A third party reproduces any number with:

```bash
uv run eval/fetch.py <dataset>            # rebuild corpus, sha256-verified
uv run eval/bench.py corpus/<dataset>     # -> docs/benchmarks/results/<dataset>.json
uv run eval/report.py                     # -> docs/benchmarks/RESULTS.md
```

## Metrics

`eval/bench.py` generalises `eval/tds-bench.py` (which remains for the README
workflow) and keeps its token model unchanged:

- **image tokens** = `(w*h)/750` after fitting inside 1568 px on the long
  edge, computed from actual rendered pixels;
- **text tokens** = `chars/3.5`;
- **full optical** renders every page at 140 dpi (streamed, not held in
  memory — the old runner kept all pixmaps in a list, which breaks on
  1,000-page bills).

Per file, recorded to JSON: pages, bytes, vision calls, calls-per-page,
reason histogram, `over_scale_guard`, tokens for (a) full optical,
(b) pdf-inspector text only, (c) pdf-extract, wall time per stage (optical
render / text extraction / routing / routed-page render), and an
independent raster proxy (count of image placements ≥300 px min-dim, for
the zero-call cross-check below). Per dataset: totals, medians, and the
outlier lists. `eval/report.py` renders all JSONs into
`docs/benchmarks/RESULTS.md` — one machine-readable JSON per dataset plus
one human-readable Markdown report, both committed.

## Generalisation questions, and how each is answered

1. **Distribution of vision-calls-per-page by document class** — histogram +
   mean/median/p95/max per dataset. If the fitted thresholds generalise,
   figure-dense classes (datasheets, arxiv) sit well above text classes
   (bills, multi_column), and bills sit at ~0.
2. **Pathological tails** — every file where `calls > pages` (tile-grid
   pathology; `ai_latent-diffusion` wants 301 calls for 45 pages), every
   file over the scale guard (15), top-10 by calls/page per dataset — all
   *named*, with reason breakdown, so the other agent can reproduce each
   case with `harvest.py <file> --json`.
3. **False negatives (zero calls on a document with figures)** — files with
   0 calls but ≥1 large raster placement (independent of harvest's own
   filters). Honest limitation: for *vector-only* figures there is no cheap
   independent detector that is not itself harvest's logic, so the
   vector-figure false-negative rate on text PDFs is not measurable here
   and is stated as unmeasured.
4. **False positives on pure text** — the bills dataset is the control: it
   has no figures by construction, so its total call count is a direct
   false-positive measurement. olmocr_arxiv_math similarly bounds the
   equations-misrouted-as-charts failure.
5. **Scans** — olmocr_scans: fraction of files routed `no_text_layer`
   (should be ~100%); any file NOT routed is a named false negative.
6. **Cost regression at scale** — files where pdf-extract costs *more* than
   full optical (`ours_tok > opt_tok`, like `lm2596` at −1%), counted and
   named per dataset.

## What is NOT measured, and why

- **Figure-description accuracy on text-bearing PDFs** — no public benchmark
  scores it; inventing a proxy would be dishonest. The only accuracy
  measurement remains `eval/oldscans.md` (olmOCR scoring of scanned pages).
- **Extraction quality on the new corpora** — no ground truth exists for
  arbitrary arXiv/PMC/bill text. Quality claims stay pinned to the existing
  gated benchmarks (opendataloader-bench 0.875, byte-identity gate).
  `eval/gate.py` is additionally run on a 10-file random sample per new
  dataset as a smoke check that the pipeline round-trips, not as a score.
- **Vector-figure false negatives on text pages** — see point 3 above.
- **Threshold sensitivity** — measuring how results move as thresholds vary
  is tuning's twin; out of scope here by design.

## Budget

~1,600 downloaded PDFs, ~1.5 GB total (66 GB free, checked). arXiv is fetched
at ≤1 request/3 s per their robots policy (~12 min); HF, PMC, govinfo and TI
tolerate modest parallelism. Bench runtime is dominated by routing at
~35 ms/page — an estimated ~15,000 pages ≈ 10–15 min local compute, run
per-dataset so a failure loses nothing.
