# Adaptive resolution — same capture, half the tokens

Vision cost scales with image **area**, so resolution is the dominant lever:
halving an image's long edge quarters its token cost. The first version rendered
every page at a flat 140 dpi (~2,443 tokens for A4), which pays for detail most
pages do not contain.

## The rule

`harvest.py:render_edge()` sizes each page from the size of its own smallest
meaningful text (this document said `convert.py:_render_edge()` until
2026-08-13; the function lives in `harvest.py` and has no leading underscore —
`convert.py:40` imports it):

    edge_px = page_long_edge_pt x (8.0 / fifth_percentile_font_pt)
    clamped to [800, 1568] px;  pages with no text layer get 1100 px

The 5th percentile rather than the true minimum: the absolute smallest glyph on
a datasheet is almost always legal boilerplate, not content. 1568 px is the
ceiling because the model downsamples above it anyway.

## Calibration

Across 272 rendered datasheet pages the smallest text is median 6.8 pt
(p10 4.5 pt). A dense TI characteristic-curves page was rendered at 1568 / 1120
/ 896 / 784 px and inspected: axis labels, tick values, curve annotations and
figure captions all remained legible at **784 px (633 tokens, 25% of the 1568 px
cost)**.

## Effect on cost — 14 datasheets, 668 pages

| | read every page | before | after |
|---|---|---|---|
| first question | 1,626,152 | 1,084,905 (33% less) | **668,054 (59% less)** |
| images alone | — | 774,926 | **358,075 (54% less)** |
| 10 questions | 16,261,520 | 1,203,039 (13.5x) | **786,242 (20.7x)** |

Every one of the 14 improved. `lm2596_ti`, which was 1% *worse* than reading
every page, is now 34% better.

## Does it still capture the same? Controlled test

Three olmOCR-bench `old_scans` documents (typed letter, handwritten cursive,
small-print contents page), transcribed twice — once from the old ~2,570 tok/page
renders, once from the new ~1,266 tok/page renders — and scored against the
benchmark's own tests:

| | pdf-inspector | high-res | low-res (51% fewer tokens) |
|---|---|---|---|
| `present` | 0/10 — 0% | 6/10 — **60.0%** | 6/10 — **60.0%** |
| `order` | 0/9 — 0% | 6/9 — **66.7%** | 6/9 — **66.7%** |
| `absent` | 4/4 | 3/4 | 2/4 |
| TOTAL | 4/23 — 17.4% | 15/23 — 65.2% | 14/23 — 60.9% |

**Content capture is identical.** Both content test types score exactly the same
at half the tokens.

The single difference is one `absent` test (`'ack 5/27/14'`, an archival note I
included in the low-res transcription's furniture line and not the high-res
one). That is a transcription choice, not a legibility loss — verified by
diffing the two outputs test by test.

## Limits

- n=3 for the controlled comparison. Small.
- Scans get a fixed 1100 px because they carry no font metadata to measure. A
  scan of genuinely tiny print would be under-rendered; `--edge` overrides it.
- Calibration used TI/Diodes datasheets and 1914-era correspondence. Other
  document classes are unmeasured.
