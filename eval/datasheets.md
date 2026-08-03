# Electronics datasheets — what it costs to understand one

14 real datasheets (TI, Diodes Inc), **668 pages**, downloaded from the
manufacturers. Datasheets are the hard case: pinout diagrams, characteristic
curves and schematics that text extraction cannot touch, mixed with dense
parameter tables it handles perfectly.

Reproduce with `uv run eval/datasheet-cost.py` (expects `datasheets/*.pdf`).

## Token model

Images are charged at `(w x h)/750` after fitting inside 1568px on the long
edge, per Anthropic's documented rule, computed from the **actual rendered
pixels**. Text is charged at `chars/3.5`, conservative for technical English.

## Per document

| datasheet | pages | vision calls | read-every-page | pdf-extract | saving |
|---|---|---|---|---|---|
| tl072_ti | 89 | 48 | 216,453 | 122,158 | 44% |
| lm358_ti | 68 | 31 | 164,902 | 108,198 | 34% |
| ads1115_ti | 57 | 30 | 138,877 | 104,501 | 25% |
| bq24074_ti | 53 | 42 | 129,105 | 103,570 | 20% |
| tmp117_ti | 50 | 29 | 121,902 | 96,558 | 21% |
| opa2333_ti | 49 | 21 | 119,337 | 66,186 | 45% |
| lm2596_ti | 47 | 43 | 114,449 | 115,472 | -1% |
| tps62840_ti | 45 | 34 | 109,687 | 76,264 | 30% |
| lm317_ti | 44 | 26 | 107,246 | 73,308 | 32% |
| sn74hc595_ti | 41 | 15 | 99,791 | 50,811 | 49% |
| ne555_ti | 39 | 20 | 94,801 | 64,920 | 32% |
| ina219_ti | 38 | 13 | 92,586 | 54,444 | 41% |
| drv8833_ti | 30 | 20 | 73,042 | 37,251 | 49% |
| ap2112_diodes | 18 | 4 | 43,974 | 11,264 | 74% |

**Total: 668 pages, 376 vision calls, 1,626,152 → 1,084,905 tokens (33% less).**

## The first pass is only 33% cheaper

That is the honest headline for a single question, and one datasheet
(`lm2596_ti`) comes out 1% *worse*. Datasheets are figure-dense, so the filter
keeps a lot: 376 calls across 668 pages. Wall time is also higher on the first
pass — 19.0 s versus 6.7 s — because extraction runs.

## The cache is where it wins

| | read every page | pdf-extract |
|---|---|---|
| first question | 1,626,152 | 1,084,905 (33% less) |
| each one after | 1,626,152 | **13,126 (99% less)** |

| questions | naive | pdf-extract | ratio |
|---|---|---|---|
| 1 | 1,626,152 | 1,084,905 | 1.5x |
| 3 | 4,878,456 | 1,111,157 | 4.4x |
| 5 | 8,130,760 | 1,137,409 | 7.1x |
| 10 | 16,261,520 | 1,203,039 | **13.5x** |

The underlying reason is per-page: the median datasheet page is **478 tokens**
of extracted text but about **2,400 tokens** to look at as an image. If you only
need the text and not the figures, the whole corpus is 81% cheaper.

## What this does not measure

Whether the figure descriptions are *correct*. This is a cost measurement, not
an accuracy one. No public benchmark scores figure comprehension in PDFs; see
`oldscans.md` for the one place accuracy is measurable.
