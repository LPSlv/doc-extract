## p084-render.png

Full page render from the appendix of a differential-privacy paper. The top third
is a two-part figure (Figure 15); the rest is running text.

### Figure 15, panel (a) — line chart with error bars

**Figure (line chart, four series, symmetric error bars).** Panel title:
**"MSE vs C\* across n for 5-Modal Bivariate t-Mixture"**.

- X axis: **"Clip Multiplier (C\* scaling)"**, linear, tick labels 0.4, 0.5, 0.6,
  0.7, 0.8, 0.9, 1.0.
- Y axis: **"MSE"**, linear, tick labels 0.0, 0.1, 0.2, 0.3, 0.4, 0.5, with faint
  horizontal gridlines at each tick.
- Legend, inside the axes at top left, four entries with round markers:
  **n=700** (green), **n=1000** (orange), **n=2000** (blue/slate),
  **n=5000** (pink/magenta).

Data points are plotted at clip multiplier **0.4, 0.5, 0.6, 0.8 and 1.0 only** —
there is no marker at 0.7 or 0.9, though the axis ticks those values. All four
series rise monotonically with the clip multiplier. Values read from the axis
(approximate):

| Clip multiplier | n=700 | n=1000 | n=2000 | n=5000 |
| --- | --- | --- | --- | --- |
| 0.4 | ~0.135 | ~0.096 | ~0.040 | ~0.014 |
| 0.5 | ~0.157 | ~0.109 | ~0.050 | ~0.018 |
| 0.6 | ~0.262 | ~0.170 | ~0.056 | ~0.020 |
| 0.8 | ~0.347 | ~0.184 | ~0.082 | ~0.029 |
| 1.0 | ~0.491 | ~0.321 | ~0.101 | ~0.038 |

Error bars are visible on every point. They are widest for n=700 (at clip
multiplier 1.0 the bar spans roughly 0.45 to 0.53; at 0.8 roughly 0.31 to 0.385; at
0.6 roughly 0.24 to 0.285) and for n=1000 (at 1.0 roughly 0.29 to 0.35). The n=2000
and n=5000 bars are small enough to be barely wider than the markers. Ordering is
strict throughout: n=700 highest, then n=1000, then n=2000, then n=5000 lowest.

Sub-caption: **"(a) MSE vs. clipping multiplier `clip_multiplier`."**

### Figure 15, panel (b) — 2×2 grid of small-multiple line charts

**Figure (small multiples, four log-x line charts).** Overall title above the grid:
**"MSE vs m across n for 5-Modal Bivariate t-Mixture"**.

Grid layout and subplot titles: top-left **"n = 700"**, top-right **"n = 1000"**,
bottom-left **"n = 2000"**, bottom-right **"n = 5000"**. Each panel uses one colour
matching panel (a)'s legend: n=700 green, n=1000 orange, n=2000 blue, n=5000 pink.

- Y axis: **"MSE"** (labelled on the left column only), linear, tick labels 0.0,
  0.5, 1.0, 1.5 on all four panels, so all four share the same vertical scale.
- X axis: **"Minibatch size m"** (labelled on the bottom row only), logarithmic.
  Tick labels differ per panel: n=700 shows 10¹ and 10²; n=1000 shows 10¹, 10² and
  10³; n=2000 shows 10² and 10³; n=5000 shows 10² and 10³.

Every panel shows MSE falling steeply from the smallest minibatch and then
flattening. Five markers per panel. Values read from the axes (approximate):

- **n = 700** (green): starts at ~1.34 at the smallest m (≈7), with a visible error
  bar spanning roughly 1.15 to 1.55 — the only conspicuous error bar in the grid.
  Then drops to ~0.31, ~0.23, ~0.19 and ~0.15 at successively larger m.
- **n = 1000** (orange): starts ~0.72 at m ≈ 10 (small error bar, roughly 0.66 to
  0.79), then ~0.20, ~0.13, ~0.10, and ~0.08 at m ≈ 10³.
- **n = 2000** (blue): starts ~0.26 at the smallest m, then ~0.09, ~0.07, ~0.055,
  and ~0.045 at the largest m (beyond 10³).
- **n = 5000** (pink): starts ~0.13, then ~0.04, ~0.03, ~0.025, and ~0.02 at the
  largest m.

Curves for n=2000 and n=5000 sit near the bottom of their panels and are nearly
flat across the whole range on this shared 0–1.5 scale.

Sub-caption: **"(b) MSE vs. minibatch size m."**

### Figure 15 caption (verbatim)

"Figure 15: **Hyperparameter sensitivity for DP-GRAMS on the 5-modal *t*-mixture.**
(a) Effect of clipping multiplier `clip_multiplier` on MSE for
n ∈ {700, 1000, 2000, 5000} at fixed ε = 1. (b) Effect of minibatch size m on MSE
across the same sample sizes. The sweeps do not show sharp degradation near the
selected defaults, despite the heavier tails and heterogeneous component scales."

### Body text below the figure

Table 5 summarizes oracle DP-MSE, PMS-MSE, and runtime across the sinusoidal
privacy–utility grid. The table supports the main trend in Figure 4: the largest
DP-MSE reductions occur between the smallest privacy budgets and moderate ε, while
for larger n further privacy-budget increases yield smaller improvements and the
private error moves closer to the PMS-MSE scale. Figure 19 shows that the
sinusoidal experiment is not sharply sensitive to moderate changes in the clipping
multiplier or minibatch size near the selected defaults.

Together, the piecewise-constant and sinusoidal designs show that DP-PMS can
recover both support-limited branches and smooth nonlinear modal curves under the
fixed-design response-privacy setup. The two examples differ in difficulty: the
three-component design shows a sharper drop in DP-MSE at larger n and ε, while the
sinusoidal design retains a visible gap from PMS-MSE even at the largest privacy
budgets. In both cases, the clipping and minibatch sweeps indicate that the
reported results are not driven by a narrow tuning choice.

**B.3  Private Clustering on Simulated Data**

This subsection complements the blobs clustering experiment in Section 5.5.1 by
providing additional numerical summaries and hyperparameter sweeps for DP-GRAMS-C.
Figure 6 reports privacy–utility curves in ARI, NMI, and centroid MSE versus ε
across n ∈ {700, 1000, 2000, 5000}. Table 6 shows that DP-GRAMS-C improves sharply
from ε = 0.1 to moderate privacy budgets and then largely stabilizes in ARI and
NMI, while centroid MSE remains small once ε is moderate. DP-k-Means also improves
with ε, but is generally weaker in ARI and NMI except at the loosest [text
continues off the page]

Cross-reference numbers in the body text (5, 4, 19, 5.5.1, 6) are rendered as
coloured hyperlinks.

Page furniture: page number 84, centred at the foot of the page.
