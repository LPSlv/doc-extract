**Figure (grouped bar chart with error bars).** Success rate by coverage
setting, three series per group. No title.

Axes. Y: **"Success rate (%)"**, from 0 to just above 50; labelled ticks and
faint horizontal gridlines at **0, 10, 20, 30, 40, 50**. X: five categorical
groups, labelled left to right **Cov4, Cov6, Cov9, Cov12, Full** (no x-axis
title). Legend, upper right, three entries: **Total** (blue), **ID** (green),
**OOD** (orange). Each group has the three bars in that order, left to right.
Every bar carries a symmetric black error bar with horizontal caps.

Values read from the axis (no numbers are printed on the chart); error-bar
extents given as low–high:

| Group | Total (%) | Total err | ID (%) | ID err | OOD (%) | OOD err |
|---|---|---|---|---|---|---|
| Cov4 | ~14.0 | ~13.4–14.6 | ~39.5 | ~36.3–43.2 | ~1.1 | ~0.6–2.5 |
| Cov6 | ~16.1 | ~13.0–19.4 | ~33.5 | ~24.7–42.6 | ~7.4 | ~5.4–9.5 |
| Cov9 | ~22.2 | ~21.5–22.8 | ~34.4 | ~33.4–35.4 | ~16.0 | ~15.6–16.5 |
| Cov12 | ~22.8 | ~20.2–25.5 | ~31.5 | ~29.2–34.0 | ~18.4 | ~15.5–21.3 |
| Full | ~37.3 | ~36.4–38.5 | ~37.3 | ~36.4–38.5 | ~37.3 | ~36.4–38.5 |

Points visible in the drawing: in the **Full** group all three bars are the same
height (~37.3%) with essentially identical error bars — Total, ID and OOD
coincide. In every Cov group ID is the tallest bar and OOD the shortest, with
Total in between. **Cov4 OOD is close to zero (~1%)**, the smallest bar in the
chart, and its error bar nearly reaches the axis. **Cov6 has by far the widest
error bars** (ID spans roughly 25–42%, Total roughly 13–19%), while **Cov9 has
the tightest** (all three whiskers about ±0.5). ID falls monotonically across
Cov4 → Cov12 (~39.5 → ~33.5 → ~34.4 → ~31.5, with Cov9 slightly above Cov6),
whereas Total and OOD rise monotonically across the same sequence. No bar
reaches 40% except Cov4 ID, and no series is missing from any group.
