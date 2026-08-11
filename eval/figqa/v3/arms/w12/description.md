**Figure (oscilloscope screen capture, p25).** A Teledyne LeCroy scope screenshot showing a hot-swap / e-fuse power-up sequence: six annotated traces on a single 10 × 8 division grid, with the instrument's menu bar across the top and the channel/timebase/trigger readouts across the bottom.

**Menu bar (top, left to right):** File · Vertical · Timebase · Trigger · Display · Cursors · Measure · Math · Analysis · Utilities · Support.

**Grid.** 10 horizontal divisions × 8 vertical divisions. Horizontal scale 2.00 ms/div with the trigger/centre at 0.00 ms, so the visible window spans roughly −10 ms to +10 ms. Centre crosshairs are drawn at the middle vertical and horizontal division lines. No numeric axis tick labels are printed on the grid itself; scaling comes only from the readout boxes below. A small green trigger-position marker sits on the bottom edge at the centre (0 ms).

**Ground/zero-reference markers on the left edge of the grid** (channel tags in their trace colours), from top to bottom: **C3** (blue) at ~4.0 div from the top, **M3** (light violet) at ~6.0 div, **M2** (dark red) at ~6.8 div, **C4** (green) at ~8.0 div, i.e. on the bottom grid line. Positions below are given in divisions: x measured from the centre (0 ms) in divisions of 2.00 ms, y measured downward from the top grid line.

**Labelled traces** (each label is printed on the plot with a short leader line to its trace):

- **VIN** — dark yellow/olive (C1, 10.0 V/div). A flat horizontal line at y ≈ 1.56 div for the whole sweep; no transition anywhere in the window. Label sits left of centre at about x ≈ −2.5 div.
- **GATE** — magenta/pink (C2, 10.0 V/div). Flat on the low baseline at y ≈ 4.02 div until about x ≈ −1.2 div, then a slow ramp that steepens; crosses the VIN level at roughly x ≈ +0.6 div and keeps climbing, ending at y ≈ 0.38 div at the right edge — i.e. GATE finishes about 1.2 div (≈ 12 V at 10 V/div) *above* VIN. Label at upper right, about x ≈ +2.0 div.
- **VOUT** — blue (C3, FLT DC1M, 10.0 V/div). Flat on the same low baseline y ≈ 4.04 div, starts rising later than GATE at about x ≈ −0.5 div, rises in an S-shape, and flattens at y ≈ 1.57 div — exactly the VIN level — by about x ≈ +1.0 div, then runs coincident with VIN to the right edge. Label just left of centre, about x ≈ −0.5 div.
- **PGD** — light violet (M3, 20.0 V/div). Flat low at y ≈ 6.02 div until a fast rising step at x ≈ +0.7 div, then flat high at y ≈ 4.80 div to the right edge. Step height ≈ 1.2 div (≈ 24 V at the stated 20.0 V/div). Label at about x ≈ −1.8 div, on the low section.
- **TIMER** — dark red (M2, 5.00 V/div). Starts flat high at y ≈ 6.23 div, falls at about x ≈ −1.7 div to a low of y ≈ 6.96 div, holds briefly, then recovers slightly from about x ≈ −0.3 div to y ≈ 6.78 div and stays essentially flat (drifting very slowly to y ≈ 6.80 div) to the right edge. Label at about x ≈ +1.3 div.
- **CURRENT_IIN** — bright green (C4, BwL DC, 5.00 A/div, offset −20.000 A). Sits at the bottom grid line (y ≈ 7.99 div) for the whole left half, then a small step up at about x ≈ −0.5 div, a gradual rise, a sharp triangular peak at **x ≈ +0.48 div, y ≈ 7.01 div** — about 1.0 div, i.e. ≈ 5 A above the baseline — then a fall back to the baseline by about x ≈ +1.1 div and flat at zero for the rest of the sweep. Label at about x ≈ −0.9 div, below the trace.

Ordering of events left to right: TIMER falls → CURRENT_IIN begins to rise / GATE begins to ramp → VOUT begins to rise → inrush current peaks → GATE crosses VIN → PGD asserts high → VOUT reaches VIN → inrush current returns to zero while GATE continues climbing above VIN.

**Bottom readout boxes, left to right (verbatim):**

| Box | Line 1 | Line 2 | Line 3 |
|---|---|---|---|
| **C1** (yellow tag) | DC1M | 10.0 V/div | 0 mV offset |
| **C2** (magenta tag) | DC1M | 10.0 V/div | 0 mV offset |
| **C3** (blue tag, label low-contrast dark-on-blue) | FLT DC1M | 10.0 V/div | 0.0 mV ofst |
| **C4** (green tag) | BwL DC | 5.00 A/div | −20.000 A |
| **M2** (red tag) | — | 5.00 V/div | 2.00 ms/div |
| **M3** (violet tag) | — | 20.0 V/div | 2.00 ms/div |

**Timebase box:** "Timebase 0.00 ms / 2.00 ms/div / 100 kS 5 MS/s".
**Trigger box:** "Trigger C4 DC / Stop 750 mA / Edge Positive".

**Page furniture:** bottom-left brand mark "TELEDYNE LECROY"; bottom-right timestamp "8/15/2016 3:40:07 PM".

No title, legend box, cursors or measurement-parameter table are shown on the capture.
