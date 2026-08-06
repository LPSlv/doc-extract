# Local fixtures

Expected routing for the five documents the thresholds were derived from.
The PDFs are **not** committed: they contain Optonics budget figures, named
individuals and contract detail. Regenerate with:

    uv run skills/doc-extract/harvest.py <file>

| Document | Pages | Unfiltered | Expected | Composition |
|---|---|---|---|---|
| ESA_BIC_LV funding guidelines 03.26 | 14 | 7 | 1 | 1 standalone_raster |
| ESA_ERAF_Metodika_v3 | 9 | 5 | 0 | — |
| ESA_BIC_Latvia_MTR_Optonics | 16 | 20 | 10 | 8 raster + 2 dense_grid (p9, p11) |
| Lenards_Msc_Thesis_VLAs | 46 | 33 | 13 | 7 raster + 6 curves |
| example/sample-report.pdf (committed) | 1 | 1 | 1 | 1 standalone_raster |
| housing_VSZ (CAD) | 1 | 3 | 1 | 1 no_text_layer |

Synthetic controls (reproducible, no private data):

| Case | Expected |
|---|---|
| matplotlib line plot, no legend | fires `diagonals` |
| line plot in the corner of a text page | fires `diagonals` |
| scatter, square markers | fires `stroke_grid` |
| page of 14 underlined links | fires **nothing** |
| truncated/corrupt file | `status: error, unreadable`, batch continues |
