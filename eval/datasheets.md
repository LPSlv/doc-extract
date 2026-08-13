# Electronics datasheets — what it costs to understand one

14 real datasheets (TI, Diodes Inc), **668 pages**, downloaded from the
manufacturers. Datasheets are the hard case: pinout diagrams, characteristic
curves and schematics that text extraction cannot touch, mixed with dense
parameter tables it handles perfectly.

Reproduce with `uv run eval/datasheet-cost.py` (expects `datasheets/*.pdf`).

> [!NOTE]
> **These are pre-adaptive-resolution numbers.** Every total below describes the
> flat-140-dpi renderer that this repo replaced; the shipped pipeline sizes each
> page from its own smallest text (`harvest.py:render_edge()`). On this same set
> that took the first question from **1,084,905 to 668,054 tokens — 59% below
> reading every page, not the 33% quoted here** — and turned `lm2596_ti` from 1%
> worse into 34% better. `eval/resolution.md` has the current figures.
>
> One line already carried the new number while the headline did not: line 79
> below says "1,626,152 → 668,054", which is the post-resolution comparison
> sitting in a pre-resolution document. That looked like a self-contradiction
> and is really a half-applied update. The stale totals are kept as the
> historical record rather than rewritten, since the resolution work is only
> meaningful against what it improved on.

## Token model

Images are charged at `(w x h)/750` after fitting inside 1568px on the long
edge, per Anthropic's documented rule, computed from the **actual rendered
pixels**. Text is charged at `chars/3.5`, conservative for technical English.

## Per document

| datasheet | pages | vision calls | read-every-page | doc-extract | saving |
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

| | read every page | doc-extract |
|---|---|---|
| first question | 1,626,152 | 1,084,905 (33% less) |
| each one after | 1,626,152 | **13,126 (99% less)** |

| questions | naive | doc-extract | ratio |
|---|---|---|---|
| 1 | 1,626,152 | 1,084,905 | 1.5x |
| 3 | 4,878,456 | 1,111,157 | 4.4x |
| 5 | 8,130,760 | 1,137,409 | 7.1x |
| 10 | 16,261,520 | 1,203,039 | **13.5x** |

The underlying reason is per-page: the median datasheet page is **478 tokens**
of extracted text but about **2,400 tokens** to look at as an image. If you only
need the text and not the figures, the whole corpus is 81% cheaper.

## Wall time, per stage

Median of 3 runs, 14 datasheets, 668 pages. `uv run eval/datasheet-time.py`.

| stage | total | per page |
|---|---|---|
| classify (`detect_pdf`) | 0.36 s | 0.5 ms |
| extract text (`process_pdf`) | 4.66 s | 7 ms |
| route (`harvest`, incl. page sizing) | **18.22 s** | 27 ms |
| render the selected images | 3.11 s | 4.7 ms |
| **doc-extract total** | **26.4 s** | **39 ms** |
| naive: render every page | 6.74 s | 10 ms |

**Routing is the expensive stage**, not rendering — `get_drawings()` on every
page dominates. And the honest comparison: the skill spends about **20 s more
local CPU** across 668 pages than simply rasterising everything.

That 20 s of CPU removes 958,098 tokens of model input (1,626,152 → 668,054) and
292 round trips (668 page reads → 376 image reads, then zero on follow-ups). At
any plausible prefill rate that is a large net time win, but the local pipeline
itself is slower and it would be dishonest to imply otherwise.

Moving the page-sizing computation into `harvest` — where the page is already
parsed — was worth doing: computing it separately in `convert` made rendering
54% slower. Rendering is now 3.11 s against 3.74 s for the old fixed-dpi path,
17% faster *and* producing images that cost 54% fewer tokens.

## What this does not measure

Whether the figure descriptions are *correct*. This is a cost measurement, not
an accuracy one. No public benchmark scores figure comprehension in PDFs; see
`oldscans.md` for the one place accuracy is measurable.
