**Figure (line chart, two curves, cumulative-distribution style).** Title:
**"deep1b_10m - recall@100=90%"**.

Axes. X: **"Amount of Data Accessed (MB)"**, from about 5 at the left spine to
about 250 at the right edge; labelled ticks and vertical gridlines at **50, 100,
150, 200, 250** (no tick label at the left spine). Y: **"Queries (%)"**, range
**60 to 100** (axis truncated at 60, not 0); labelled ticks and horizontal
gridlines at **60, 70, 80, 90, 100**. Grey gridlines on white.

Legend (lower right, boxed): **"Fixed nprobe"** (pink line) and **"QASP"**
(dark yellow / olive line).

Curves. Both rise monotonically from the bottom-left. Values read off the axes:

| Data accessed (MB) | Fixed nprobe (%) | QASP (%) |
|---|---|---|
| 20 | ~62 | ~61 |
| 25 | ~69 | ~72 |
| 30 | ~75 | ~82 |
| 35 | ~81 | ~89 |
| 40 | ~85 | ~96 |
| 45 | ~87 | ~98.5 |
| 50 | ~89 | ~99 |
| 60 | ~91 | (curve ended) |
| 70 | ~94 | — |
| 80 | ~96.5 | — |
| 100 | ~97.5 | — |
| 120 | ~97.6 | — |
| 130 | ~98.3 | — |
| 135 | ~99 | — |
| 150–200 | ~99 (flat) | — |
| 225–248 | ~99.5 (flat) | — |

The two curves cross at roughly 22 MB / ~65%; below that Fixed nprobe is
marginally above QASP, above it QASP is above Fixed nprobe everywhere. The
**QASP curve stops at about 52 MB**, where it has reached ~99.5% — it does not
extend across the rest of the x-range. The Fixed nprobe curve continues to the
right edge, with a visible step up near 130–133 MB (from ~98.3% to ~99%) and a
further step to ~99.5% at about 223 MB, then flat to the right edge.

Annotations. Three horizontal double-headed black arrows, each with a filled
black dot at both ends, comparing the x-position of the two curves at a fixed
y-level:

- **"4.3 X"** (label above the arrow, near the top of the plot): dots at
  **~52 MB** (QASP) and **~223 MB** (Fixed nprobe), both at y ≈ 99.5%.
- **"1.8 X"** (label above the arrow): dots at **~40 MB** (QASP) and **~70 MB**
  (Fixed nprobe), both at y = 95%.
- **"1.3 X"** (label above the arrow): dots at **~37 MB** (QASP) and **~49 MB**
  (Fixed nprobe), both at y = 90%.

All MB readings are estimated from the axis gridlines. No error bars, no
additional annotations or footnotes.
