Two figures on this page. The section text (13.2.3 "4-Pts LNR Parameters") is extractable text and is not reproduced here.

## Figure 10 — Discontinuity point positioning (for CW=0)

Caption below the figure, in teal italic: "Figure 10 - Discontinuity point positioning (for CW=0)".

**Type:** angular / polar orientation diagram.

Elements as drawn:

- A pair of black Cartesian axes with arrowheads (horizontal axis pointing right, vertical axis pointing up), crossing at the origin.
- A teal circle centred on the origin.
- Two teal straight lines through the origin, each drawn with small arrowheads where they cross the circle, dividing the circle into four labelled sectors. Their end labels, in teal, are:
  - **0°** — lower-left end of the steeper line (below and left of the origin)
  - **90°** — lower-right end of the shallower line
  - **180°** — upper-right end of the steeper line (above and right of the origin)
  - **270°** — upper-left end of the shallower line
- An orange curved arrow sweeping clockwise from just right of the origin, over the top, round to a point at lower-left where it terminates in a solid orange arrowhead. Labelled in bold orange: **DP** (discontinuity point). The arrowhead lands on the 0° direction.

The layout as drawn: with CW=0 the angle labels run 0°, 90°, 180°, 270° counter-clockwise from the lower-left direction, and DP marks the 0° / discontinuity position.

## Figure 11 — 4pts linearization parameters description

Caption below the figure, in teal italic: "Figure 11 - 4pts linearization parameters description".

**Type:** piecewise-linear transfer-function plot (line chart with labelled breakpoints).

- **X axis:** "Angle [°]", drawn as an arrow to the right. Tick labels along the axis, left to right: **DP(0,0)** (origin, bold), **LNR_A_X**, **LNR_B_X**, **LNR_C_X**, **LNR_D_X**, and **360** (bold) at the right end. No numeric values are printed for the LNR_*_X positions — they are symbolic.
- **Y axis:** "Output [%]", drawn as an arrow upwards. Tick labels bottom to top: **CLAMPLOW** (teal italic), **LNR_A_Y**, **LNR_B_Y**, **LNR_C_Y**, **LNR_D_Y**, **CLAMPHIGH** (teal italic), **100%** (bold, the topmost label, above CLAMPHIGH). Again symbolic — no numbers except "100%".

**The curve** is a teal polyline running left to right, monotonically increasing, with grey/black "×" markers at each knee:

1. A flat segment at the **CLAMPLOW** level from the origin out to the first grey × marker (unlabelled marker where the curve leaves the low clamp).
2. Rising segment to point **A** at (LNR_A_X, LNR_A_Y) — marked with a bold black ×, labelled **A** above it.
3. Segment to point **B** at (LNR_B_X, LNR_B_Y) — bold black ×, labelled **B**.
4. Segment to point **C** at (LNR_C_X, LNR_C_Y) — bold black ×, labelled **C**.
5. Segment to point **D** at (LNR_D_X, LNR_D_Y) — bold black ×, labelled **D**.
6. Rising segment to a final grey × where the curve reaches **CLAMPHIGH**, then flat at CLAMPHIGH out to the right edge (x = 360).

Dashed grey construction lines drop from each marker to its X label and run across to its Y label. A dashed box also marks the 100% level across the top of the plot.

**Slope callouts**, each a small curved arrow pointing at the segment it names:

- **Slope LNR_S0** — the first rising segment (from CLAMPLOW up to point A).
- **Slope LNR_A_S** — the segment from A to B.
- **Slope LNR_B_S** — the segment from B to C.
- **Slope LNR_C_S** — the segment from C to D.
- **Slope LNR_D_S** — the segment from D up to CLAMPHIGH.

The plot shows seven segments in total (low clamp, five sloped segments, high clamp), matching the text's "Seven segments can be programmed but the clamping levels are necessarily flat."

Page furniture: header "MLX90421", "Triaxis® Position Sensor IC", Melexis logo with the strapline "INNOVATION WITH HEART"; footer "REVISION 004 - 31 March 2026", "Page 29 of 61", "3901090421".
