# Benchmark results

Generated 2026-08-03 at commit `8740da8` by `uv run eval/report.py` from the per-dataset JSONs in `docs/benchmarks/results/`.
Reproduce any dataset with `uv run eval/fetch.py <dataset>` then `uv run eval/bench.py corpus/<dataset>`; inputs are pinned by sha256 in `eval/manifests/<dataset>.json`.
Token model: image `(w*h)/750` after fitting inside 1568 px; text `chars/3.5`; optical baseline renders every page at 140 dpi. Wall time is the deterministic local pipeline only — model inference is excluded.

## Cost: three ways to read each corpus

| dataset | files | pages | MB | full optical | text only | **pdf-extract** | vs optical | vision calls | local s |
|---|---|---|---|---|---|---|---|---|---|
| tds | 23 | 632 | 31 | 1,513,884 | 282,933 | **546,969** | +64% | 253 | 20 |
| datasheets | 204 | 7,641 | 398 | 18,511,075 | 3,362,899 | **6,395,087** | +65% | 3,197 | 300 |
| papers | 24 | 704 | 172 | 1,705,760 | 622,992 | **913,606** | +46% | 277 | 25 |
| arxiv | 238 | 5,336 | 859 | 12,856,721 | 5,031,436 | **6,446,136** | +50% | 1,415 | 251 |
| pmc | 220 | 1,923 | 460 | 4,450,900 | 2,270,193 | **3,310,381** | +26% | 1,070 | 115 |
| bills | 230 | 2,736 | 57 | 6,684,048 | 948,046 | **953,986** | +86% | 9 | 16 |
| olmocr_multi_column | 231 | 231 | 64 | 532,845 | 255,624 | **348,597** | +35% | 135 | 8 |
| olmocr_headers_footers | 266 | 266 | 65 | 597,036 | 190,402 | **278,653** | +53% | 133 | 10 |
| olmocr_arxiv_math | 522 | 522 | 95 | 1,249,499 | 443,449 | **492,855** | +61% | 61 | 17 |
| olmocr_tables | 188 | 188 | 39 | 435,331 | 118,278 | **179,907** | +59% | 85 | 8 |
| olmocr_long_tiny_text | 62 | 62 | 24 | 103,450 | 55,737 | **110,929** | -7% | 65 | 11 |
| olmocr_scans | 134 | 134 | 68 | 273,172 | 1,810 | **151,274** | +45% | 134 | 10 |

`text only` is always cheapest and always misses every figure, scan and unparsed table; it is a floor, not an option. `vs optical` is pdf-extract's token saving against rendering every page.

## What routing fired, by class

| dataset | standalone_raster | no_text_layer | curves | diagonals | dense_grid | stroke_grid | raster_grid | whole_document | total |
|---|---|---|---|---|---|---|---|---|---|
| tds | 44 | 0 | 176 | 20 | 0 | 10 | 3 | 0 | 253 |
| datasheets | 519 | 19 | 2056 | 279 | 8 | 25 | 46 | 245 | 3197 |
| papers | 102 | 7 | 33 | 13 | 8 | 23 | 11 | 80 | 277 |
| arxiv | 453 | 2 | 353 | 43 | 19 | 71 | 49 | 425 | 1415 |
| pmc | 271 | 0 | 152 | 6 | 13 | 41 | 1 | 586 | 1070 |
| bills | 0 | 0 | 9 | 0 | 0 | 0 | 0 | 0 | 9 |
| olmocr_multi_column | 42 | 15 | 28 | 7 | 0 | 4 | 1 | 38 | 135 |
| olmocr_headers_footers | 44 | 24 | 12 | 4 | 4 | 3 | 2 | 40 | 133 |
| olmocr_arxiv_math | 11 | 1 | 22 | 1 | 0 | 4 | 0 | 22 | 61 |
| olmocr_tables | 25 | 15 | 9 | 1 | 4 | 6 | 1 | 24 | 85 |
| olmocr_long_tiny_text | 13 | 23 | 6 | 0 | 0 | 0 | 0 | 23 | 65 |
| olmocr_scans | 0 | 119 | 0 | 0 | 0 | 0 | 0 | 15 | 134 |

## Calls-per-page distribution (per file)

| dataset | mean | median | p90 | p99 | max | zero-call files | over guard (15) | calls>pages |
|---|---|---|---|---|---|---|---|---|
| tds | 0.38 | 0.35 | 0.71 | 1.33 | 1.33 | 2/23 | 7 | 1 |
| datasheets | 0.39 | 0.40 | 0.59 | 0.98 | 1.33 | 5/204 | 101 | 1 |
| papers | 0.40 | 0.33 | 1.00 | 1.00 | 1.00 | 1/24 | 8 | 0 |
| arxiv | 0.36 | 0.25 | 1.00 | 1.25 | 2.00 | 45/238 | 18 | 4 |
| pmc | 0.54 | 0.50 | 1.00 | 1.00 | 1.50 | 27/220 | 7 | 2 |
| bills | 0.00 | 0.00 | 0.00 | 0.08 | 0.17 | 221/230 | 0 | 0 |
| olmocr_multi_column | 0.58 | 1.00 | 1.00 | 2.00 | 2.00 | 106/231 | 0 | 10 |
| olmocr_headers_footers | 0.50 | 0.00 | 1.00 | 2.00 | 3.00 | 143/266 | 0 | 8 |
| olmocr_arxiv_math | 0.12 | 0.00 | 1.00 | 1.00 | 2.00 | 462/522 | 0 | 1 |
| olmocr_tables | 0.45 | 0.00 | 1.00 | 2.00 | 3.00 | 109/188 | 0 | 5 |
| olmocr_long_tiny_text | 1.05 | 1.00 | 1.00 | 2.00 | 6.00 | 5/62 | 0 | 4 |
| olmocr_scans | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0/134 | 0 | 0 |

## Outliers, named

### tds

**calls > pages** (1 files):
- `led_wurth.pdf` — 12 calls / 9 pages (mostly `standalone_raster`)

**most vision calls:** `ti_tlv9061.pdf` (41/99p), `ti_tps54331.pdf` (26/41p), `ti_tca9548a.pdf` (25/42p), `ti_lmv321.pdf` (24/53p), `ti_tps61023.pdf` (20/28p)

### datasheets

**calls > pages** (1 files):
- `led_wurth.pdf` — 12 calls / 9 pages (mostly `standalone_raster`)

**most vision calls:** `ti_lf356.pdf` (46/47p), `ti_lm2596.pdf` (46/47p), `ti_lm1117.pdf` (45/46p), `ti_dac8562.pdf` (44/63p), `ti_lm4562.pdf` (42/43p)

**skipped** (1): `ti_sn74ls138.pdf` (ValueError: PDF parsing error: couldn't parse input: invalid content stream)

### papers


**most vision calls:** `ai_latent-diffusion.pdf` (45/45p), `ai_gpt3.pdf` (26/75p), `ai_ddpm.pdf` (22/25p), `cs_umap.pdf` (21/63p), `rob_diffusion-policy.pdf` (18/18p)

**skipped** (1): `rob_palm-e.pdf` (ValueError: Invalid PDF structure)

### arxiv

**calls > pages** (4 files):
- `2607.29150v1.pdf` — 6 calls / 3 pages (mostly `standalone_raster`)
- `2607.29582v1.pdf` — 8 calls / 6 pages (mostly `standalone_raster`)
- `2607.28941v1.pdf` — 15 calls / 12 pages (mostly `standalone_raster`)
- `2607.29187v1.pdf` — 6 calls / 5 pages (mostly `standalone_raster`)

**pdf-extract costs MORE than full optical** (4 files): `2607.29341v1.pdf` (+650), `2607.29414v1.pdf` (+66), `2607.29500v1.pdf` (+5,229), `2607.29513v1.pdf` (+58)

**most vision calls:** `2607.29029v1.pdf` (51/51p), `2607.28594v1.pdf` (27/27p), `2607.29679v1.pdf` (27/61p), `2607.29427v1.pdf` (25/53p), `2607.29476v1.pdf` (24/36p)

### pmc

**calls > pages** (2 files):
- `AJPS-20-243.PMC10450116.pdf` — 3 calls / 2 pages (mostly `standalone_raster`)
- `1809-4406-aob-30-spe1-e245692.PMC9270044.pdf` — 5 calls / 4 pages (mostly `standalone_raster`)

**pdf-extract costs MORE than full optical** (17 files): `1052071.PMC7395265.pdf` (+1,408), `1809-4406-aob-30-spe1-e245692.PMC9270044.pdf` (+794), `41467_2025_Article_65996.PMC12678810.pdf` (+2,299), `JEM_20131560.PMC3949572.pdf` (+4,094), `LM054059Han.PMC11801479.pdf` (+255), `MGR-10-30.PMC7871936.pdf` (+2,369), `edinbmedj75066-0001.PMC5306817.pdf` (+1,606), `fncel-06-00025.PMC3357636.pdf` (+442), `main.PMC10973653.pdf` (+559), `main.PMC11782883.pdf` (+8,495) …

**most vision calls:** `edinbmedj75066-0001.PMC5306817.pdf` (40/40p), `main.PMC11292527.pdf` (21/21p), `41586_2025_Article_9767.PMC12657213.pdf` (18/19p), `KCAM_20_2674357.PMC13185462.pdf` (17/17p), `13287_2025_Article_4518.PMC12296610.pdf` (16/16p)

### bills


**most vision calls:** `BILLS-118hr12ih.pdf` (1/33p), `BILLS-118hr14ih.pdf` (1/76p), `BILLS-118hr15ih.pdf` (1/31p), `BILLS-118hr17ih.pdf` (1/28p), `BILLS-118hr20ih.pdf` (1/56p)

### olmocr_multi_column

**calls > pages** (10 files):
- `multi_column__00945e98ea0970dcffb8f548336df3a0137f_page_3_pg1.pdf` — 2 calls / 1 pages (mostly `standalone_raster`)
- `multi_column__02ef468d6658a2cc7878397e68640fe0357f_page_5_pg1.pdf` — 2 calls / 1 pages (mostly `standalone_raster`)
- `multi_column__081875a1035e34dee439b9a2a3a55e319405_page_4_pg1.pdf` — 2 calls / 1 pages (mostly `standalone_raster`)
- `multi_column__08c9eac4149a44cf8eed7cf1466ce8afa6b7_page_1_pg1.pdf` — 2 calls / 1 pages (mostly `standalone_raster`)
- `multi_column__0b045ab838c05c4ff1ac844caf826f8f368d_page_12_pg1.pdf` — 2 calls / 1 pages (mostly `standalone_raster`)
- `multi_column__0b045ab838c05c4ff1ac844caf826f8f368d_page_18_pg1.pdf` — 2 calls / 1 pages (mostly `standalone_raster`)
- `multi_column__0b045ab838c05c4ff1ac844caf826f8f368d_page_26_pg1.pdf` — 2 calls / 1 pages (mostly `standalone_raster`)
- `multi_column__0b045ab838c05c4ff1ac844caf826f8f368d_page_27_pg1.pdf` — 2 calls / 1 pages (mostly `standalone_raster`)
- `multi_column__0b045ab838c05c4ff1ac844caf826f8f368d_page_30_pg1.pdf` — 2 calls / 1 pages (mostly `standalone_raster`)
- `multi_column__0b045ab838c05c4ff1ac844caf826f8f368d_page_32_pg1.pdf` — 2 calls / 1 pages (mostly `standalone_raster`)

**pdf-extract costs MORE than full optical** (19 files): `multi_column__00187fe0533b1e8ddc748adab4924b6f7099_page_10_pg1.pdf` (+103), `multi_column__0097571b436308f563a5808d45d0232255a2_page_6_pg1.pdf` (+93), `multi_column__0097571b436308f563a5808d45d0232255a2_page_7_pg1.pdf` (+582), `multi_column__01ed6dcc6a3d0237daa88b293d0c0667df1a_page_12_pg1.pdf` (+371), `multi_column__01ed6dcc6a3d0237daa88b293d0c0667df1a_page_49_pg1.pdf` (+1,941), `multi_column__01ed6dcc6a3d0237daa88b293d0c0667df1a_page_66_pg1.pdf` (+770), `multi_column__01ed6dcc6a3d0237daa88b293d0c0667df1a_page_67_pg1.pdf` (+1,890), `multi_column__05aa71fa77e07bccb443ef4fd28dde3ecfd6_page_12_pg1.pdf` (+690), `multi_column__05eac72b90295dbb76786d1fe5e2fe0db27d_page_6_pg1.pdf` (+1,758), `multi_column__0621a0090414e4681e90a4e1ea543acca910_page_11_pg1.pdf` (+432) …

**most vision calls:** `multi_column__00945e98ea0970dcffb8f548336df3a0137f_page_3_pg1.pdf` (2/1p), `multi_column__02ef468d6658a2cc7878397e68640fe0357f_page_5_pg1.pdf` (2/1p), `multi_column__081875a1035e34dee439b9a2a3a55e319405_page_4_pg1.pdf` (2/1p), `multi_column__08c9eac4149a44cf8eed7cf1466ce8afa6b7_page_1_pg1.pdf` (2/1p), `multi_column__0b045ab838c05c4ff1ac844caf826f8f368d_page_12_pg1.pdf` (2/1p)

### olmocr_headers_footers

**calls > pages** (8 files):
- `headers_footers__0b09e4c7b49b3b4a4451ac9de5609db2d53feb8e_page_4_processed.pdf` — 3 calls / 1 pages (mostly `standalone_raster`)
- `headers_footers__7901d119ed91a89f8fbabf0eef7174d75a7656e3_page_1.pdf` — 3 calls / 1 pages (mostly `standalone_raster`)
- `headers_footers__0678963a20825044fed5401fedb69bc7a3e54de6_page_2_processed.pdf` — 2 calls / 1 pages (mostly `standalone_raster`)
- `headers_footers__74094decfc2f4504fb7e14a3969e2abe71d5eaf9_page_3.pdf` — 2 calls / 1 pages (mostly `standalone_raster`)
- `headers_footers__9530001da9e19b67bb7cb784a1ab109c233685cc_page_1.pdf` — 2 calls / 1 pages (mostly `standalone_raster`)
- `headers_footers__b79ccdcb9871dce02d3873bdf9690d9f6dd58cb4_page_19.pdf` — 2 calls / 1 pages (mostly `standalone_raster`)
- `headers_footers__d93aa3ed6cf33401e7427cff9f1feada5bae46e7_page_4.pdf` — 2 calls / 1 pages (mostly `standalone_raster`)
- `headers_footers__ed107236f9863d65c41f29cd8e8091ba76cc61d8_page_2.pdf` — 2 calls / 1 pages (mostly `standalone_raster`)

**pdf-extract costs MORE than full optical** (9 files): `headers_footers__04cea54b5e3d95140c36cfa315a41be27b2434f9_page_1_processed.pdf` (+133), `headers_footers__09c8a46e9cf449d41f48a2a69f4f54f05286e1b5_page_6.pdf` (+1,293), `headers_footers__0f692b1bde8c3e04d1ec47ae43d616fc5c2ff2a9_page_23_processed.pdf` (+538), `headers_footers__5b419ca6365ed67292e9c4f5a46d733efce69b75_page_1.pdf` (+248), `headers_footers__661e8e921def996b7775d17e3e2537092db1dbf3_page_65.pdf` (+512), `headers_footers__75bb3db067b653a432ac93c10c1b20a06811fb71_page_1.pdf` (+652), `headers_footers__9530001da9e19b67bb7cb784a1ab109c233685cc_page_1.pdf` (+167), `headers_footers__a2704890a3a4ced534778be695db36d8c203331b_page_4.pdf` (+342), `headers_footers__e83afed6342a82de99744c654ba0d1158124bfa8_page_1.pdf` (+21)

**most vision calls:** `headers_footers__0b09e4c7b49b3b4a4451ac9de5609db2d53feb8e_page_4_processed.pdf` (3/1p), `headers_footers__7901d119ed91a89f8fbabf0eef7174d75a7656e3_page_1.pdf` (3/1p), `headers_footers__0678963a20825044fed5401fedb69bc7a3e54de6_page_2_processed.pdf` (2/1p), `headers_footers__74094decfc2f4504fb7e14a3969e2abe71d5eaf9_page_3.pdf` (2/1p), `headers_footers__9530001da9e19b67bb7cb784a1ab109c233685cc_page_1.pdf` (2/1p)

### olmocr_arxiv_math

**calls > pages** (1 files):
- `arxiv_math__2503.07090_pg2.pdf` — 2 calls / 1 pages (mostly `standalone_raster`)

**pdf-extract costs MORE than full optical** (6 files): `arxiv_math__2503.03948_pg3.pdf` (+34), `arxiv_math__2503.04486_pg21.pdf` (+359), `arxiv_math__2503.05104_pg18.pdf` (+508), `arxiv_math__2503.06000_pg17.pdf` (+171), `arxiv_math__2503.06725_pg7.pdf` (+14), `arxiv_math__2503.08118_pg5.pdf` (+391)

**most vision calls:** `arxiv_math__2503.07090_pg2.pdf` (2/1p), `arxiv_math__2503.02004_pg9.pdf` (1/1p), `arxiv_math__2503.03847_pg30.pdf` (1/1p), `arxiv_math__2503.03879_pg4.pdf` (1/1p), `arxiv_math__2503.03903_pg9.pdf` (1/1p)

### olmocr_tables

**calls > pages** (5 files):
- `tables__92f758debb936f4c750694f03bc41db861ad_pg1_pg1.pdf` — 3 calls / 1 pages (mostly `standalone_raster`)
- `tables__11d982c1d2faa79c3ea4c05c707b84a72b8e_pg3_pg1.pdf` — 2 calls / 1 pages (mostly `standalone_raster`)
- `tables__587a1f5a89db9e04752baea0b4f94a364b7a_pg7_pg1.pdf` — 2 calls / 1 pages (mostly `standalone_raster`)
- `tables__a534e72afcecc225a6b2896ddf7290003c9c_pg6.pdf` — 2 calls / 1 pages (mostly `standalone_raster`)
- `tables__b74ef859a1584b4900e3d9daca7f536100e9_pg4_pg1.pdf` — 2 calls / 1 pages (mostly `standalone_raster`)

**pdf-extract costs MORE than full optical** (8 files): `tables__008d1dbe3c5a5fd2bac6e4f29acc45e711aa_pg8_pg1.pdf` (+49), `tables__144a1fd7a9b78d65270092a5b84792c59ceb_pg2_pg1.pdf` (+151), `tables__7b9b73157809310ba970693297b7b998ee1c_pg19.pdf` (+88), `tables__7e850300cc7a63925214ffea6856992511f5_pg7_pg1.pdf` (+377), `tables__981f5f245a1c3dcbafc67603d942144df82e_pg7.pdf` (+422), `tables__a45ce384707785ce86e301682e1bae0e34b5_pg7_pg1.pdf` (+114), `tables__e247cacc054302c938c36a4357f861b56ce7_pg2_pg1.pdf` (+111), `tables__fa18a15c1dbbfcb71b1f1ea1b8f116e24b8a_pg2_pg1.pdf` (+491)

**most vision calls:** `tables__92f758debb936f4c750694f03bc41db861ad_pg1_pg1.pdf` (3/1p), `tables__11d982c1d2faa79c3ea4c05c707b84a72b8e_pg3_pg1.pdf` (2/1p), `tables__587a1f5a89db9e04752baea0b4f94a364b7a_pg7_pg1.pdf` (2/1p), `tables__a534e72afcecc225a6b2896ddf7290003c9c_pg6.pdf` (2/1p), `tables__b74ef859a1584b4900e3d9daca7f536100e9_pg4_pg1.pdf` (2/1p)

### olmocr_long_tiny_text

**calls > pages** (4 files):
- `long_tiny_text__20_pg33_pg1.pdf` — 6 calls / 1 pages (mostly `standalone_raster`)
- `long_tiny_text__20_pg18_pg1.pdf` — 2 calls / 1 pages (mostly `standalone_raster`)
- `long_tiny_text__20_pg40_pg1.pdf` — 2 calls / 1 pages (mostly `standalone_raster`)
- `long_tiny_text__20_pg48_pg1.pdf` — 2 calls / 1 pages (mostly `standalone_raster`)

**pdf-extract costs MORE than full optical** (34 files): `long_tiny_text__11_pg145_pg1.pdf` (+1,396), `long_tiny_text__11_pg146_pg1.pdf` (+1,455), `long_tiny_text__11_pg161_pg1.pdf` (+1,302), `long_tiny_text__11_pg186_pg1.pdf` (+1,417), `long_tiny_text__11_pg252_pg1.pdf` (+1,368), `long_tiny_text__11_pg36_pg1.pdf` (+1,401), `long_tiny_text__11_pg375_pg1.pdf` (+1,580), `long_tiny_text__11_pg377_pg1.pdf` (+1,369), `long_tiny_text__11_pg418_pg1.pdf` (+1,318), `long_tiny_text__11_pg421_pg1.pdf` (+1,242) …

**most vision calls:** `long_tiny_text__20_pg33_pg1.pdf` (6/1p), `long_tiny_text__20_pg18_pg1.pdf` (2/1p), `long_tiny_text__20_pg40_pg1.pdf` (2/1p), `long_tiny_text__20_pg48_pg1.pdf` (2/1p), `long_tiny_text__10a_pg1.pdf` (1/1p)

### olmocr_scans


**pdf-extract costs MORE than full optical** (17 files): `old_scans_math__1_pg10.pdf` (+244), `old_scans_math__1_pg113.pdf` (+244), `old_scans_math__1_pg125.pdf` (+244), `old_scans_math__1_pg131.pdf` (+244), `old_scans_math__1_pg19.pdf` (+244), `old_scans_math__1_pg40.pdf` (+244), `old_scans_math__1_pg61.pdf` (+244), `old_scans_math__1_pg63.pdf` (+244), `old_scans_math__1_pg72.pdf` (+244), `old_scans_math__2_pg189.pdf` (+142) …

**most vision calls:** `old_scans__1.pdf` (1/1p), `old_scans__10.pdf` (1/1p), `old_scans__11.pdf` (1/1p), `old_scans__12.pdf` (1/1p), `old_scans__13.pdf` (1/1p)

## What this does not measure

- **Figure-description accuracy on text-bearing PDFs.** No public benchmark scores it; the only accuracy measurement in this repo remains `eval/oldscans.md` (scanned pages, olmOCR ground truth).
- **Vector-figure false negatives.** The zero-call cross-check above uses embedded rasters ≥300×300 px as an independent figure detector; a chart drawn purely with vector strokes has no such witness, so a text page whose vector chart was missed is invisible to this suite.
- **Extraction quality on the new corpora.** No ground truth exists for arbitrary arXiv/PMC/bill text; quality claims stay pinned to opendataloader-bench and the byte-identity gate (`eval/gate.py`).
- **Threshold sensitivity.** Deliberately out of scope: tuning on the measurement set would invalidate it.
