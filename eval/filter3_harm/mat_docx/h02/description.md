**Figure 1 (three line charts side by side, shared legend below).** Optimization trajectories of eight methods on three counterexample instances. All three panels share the x-axis caption "iteration", range 0–60 with ticks at 0, 20, 40, 60; trajectories run to about iteration 58. Light grey gridlines.

Caption, verbatim:

> Figure 1: All eight methods on the three counterexample instances; the ascending method is drawn heavy and named in each panel. *Left:* SignMuon, 4 × 4 (Theorem 1). *Centre:* MuonUSign and MuonSign on their shared 5 × 5 instance (Theorems 2–3); both panels plot (8). *Right:* EF21-SignMuon, 2 × 2 (Theorem 4), normalized units at η = 1. Trajectories are momentum-free without loss (Proposition 1; Lemma 4 for EF21-SignMuon).

**Left panel.** Y-axis caption $f(\mathbf{W}) = \mathrm{Tr}(\mathbf{G}^{\top}\mathbf{W})$; ticks 0, −50, −100, −150, −200 (no unit given). In-plot annotation in blue italic: "*SignMuon* ↑".
- SignMuon (heavy solid blue, triangle markers) is the only ascending curve: starts at 0 and rises roughly linearly to ≈ +25 at iteration 58 (read from axis).
- A bundle of several series (red-diamond, purple-square, cyan, orange, green — mutually overlapping) descends roughly linearly from 0 to ≈ −55 … −60 at iteration 58 (read from axis).
- A steeper pair (brown dash-dot and a green/olive dashed line, essentially superimposed) descends from 0 to ≈ −210 at iteration 58 (read from axis).

**Centre panel.** Y-axis unlabelled; ticks 20, 10, 0, −10, −20, −30. Two in-plot annotations: "*MuonSign* ↑" (cyan, upper left) and "*MuonUSign* ↑" (purple, just below the zero line).
- MuonSign (heavy cyan, triangle markers) ascends from 0 to ≈ +22 at iteration 58 (read from axis).
- MuonUSign (heavy purple, square markers) ascends from 0 to ≈ +4 at iteration 58 (read from axis).
- The remaining six series descend roughly linearly to a band of ≈ −30 … −35 at iteration 58 (read from axis).

**Right panel.** Y-axis caption $f(\mathbf{X}_t)$; ticks 0, 2, 4, 6. In-plot annotation in red italic: "*EF21-SignMuon* ↑".
- EF21-SignMuon (heavy red, diamond markers) is a visible saw-tooth / period-two zig-zag whose envelope rises roughly linearly from 0 to ≈ +6.1 at iteration 58 (read from axis).
- All other series collapse into a noisy flat band between roughly 0 and −0.8 (read from axis) for the whole run; several are flat lines just below 0, with small oscillations visible near iterations 45–58.

**Legend** (single row beneath the three panels, eight entries, colour/dash encodes method):

| Series | Style |
|---|---|
| SignMuon | solid blue, triangle markers |
| EF21-SignMuon | red dashed, diamond markers |
| MuonUSign | purple dash-dot, square markers |
| MuonSign | cyan dashed, triangle markers |
| EF21-MuonUSign | orange/red dash-dot |
| EF21-MuonSign | orange dotted |
| SignSGD | brown dash-dot |
| Muon | green dashed |

No individual data-point values are printed anywhere in the figure; every number above is read from the axis.
