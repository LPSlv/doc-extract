**Page furniture (p20).** Left header "TLC555" and "SLFS043K – AUGUST 1983 – REVISED JANUARY 2026"; Texas Instruments logo top right with "www.ti.com". Footer: page number 20, "Submit Document Feedback", "Copyright © 2026 Texas Instruments Incorporated", "Product Folder Links: TLC555".

Two figures on the page.

---

## Figure 7-4. Pulse-Width-Modulation vs Control Voltage — Clock Duty Cycle 98%, V<sub>DD</sub> = 5 V

(Section heading above it: "7.2.2.3 Application Curve".)

**Type.** Line plot, two smooth monotonically rising curves, plain box frame with no gridlines.

**Axes.**
- X: "Control Voltage (V)", linear, 0.5 to 4.5, ticks every 0.5 (0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5).
- Y: "Output Duty Cycle (%)", linear, 0 to 100, ticks every 20 (0, 20, 40, 60, 80, 100).

**Legend (box at top left inside plot).**
- "Clock period = 1 RC" — black trace
- "Clock period = 2.5 RC" — red trace

**Curve values (all read from axis).**
- Black, clock period = 1 RC: ~13% at 0.5 V; ~20% at 1.0 V; ~30% at 1.5 V; ~42% at 2.0 V; ~58% at 2.5 V; ~78% at 3.0 V; reaches 100% at about 3.2 V and leaves the top of the plot — the trace is drawn only up to about 3.2 V, so no data is shown for this curve above ~3.2 V.
- Red, clock period = 2.5 RC: ~5% at 0.5 V; ~10% at 1.0 V; ~17% at 1.5 V; ~25% at 2.0 V; ~34% at 2.5 V; ~45% at 3.0 V; ~57% at 3.5 V; ~72% at 4.0 V; ~92% at 4.5 V (right edge, still below 100%).

Both curves are convex upward (accelerating with control voltage), matching the "non linear relationship" the body text describes.

**Other in-plot string.** A small plot ID at the lower-right corner of the frame, rendered as "D015" (low-resolution; last characters marginal).

---

## Figure 7-5 (schematic under section 7.2.3 Pulse-Position Modulation)

The drawing itself carries no printed caption on this page; the body text refers to it as Figure 7-5.

**Type.** Block/schematic diagram of a TLC555 timer wired as a pulse-position modulator (free-running astable with modulation into CONT).

**Central block.** A rectangle representing the timer, with pin numbers outside and pin names inside:
- Pin 4 — RESET (top left of block, tied up to the V<sub>DD</sub> rail)
- Pin 8 — V<sub>DD</sub> (top right of block, tied to the V<sub>DD</sub> rail)
- Pin 2 — TRIG (left side)
- Pin 5 — CONT (left side, lower)
- Pin 3 — OUT (right side)
- Pin 7 — DISCH (right side)
- Pin 6 — THRES (right side, lower)
- GND (bottom of block, pin number not legible at this resolution)

**Connections.**
- Top rail labelled "V<sub>DD</sub> (5 V to 15 V)" runs across the top, feeding both pin 4 (RESET) and pin 8 (V<sub>DD</sub>), and also the top of resistor R<sub>A</sub> on the right.
- R<sub>A</sub> runs from the V<sub>DD</sub> rail down to the node joined to pin 7 (DISCH).
- R<sub>B</sub> runs from that DISCH node down to the node joined to pin 6 (THRES).
- Capacitor C runs from the THRES node down to the ground rail at the bottom.
- Pin 2 (TRIG) is tied by a wire on the left to the THRES/timing node (the standard astable tie).
- Pin 3 (OUT) goes right to a terminal labelled "Output".
- Pin 5 (CONT) is driven from the left by a line labelled "Modulation Input (see Note A)".
- The block's GND pin connects to the bottom ground rail, shared with C.

**Component callouts.** R<sub>A</sub>, R<sub>B</sub>, C, V<sub>DD</sub> (5 V to 15 V), Output, Modulation Input (see Note A).

**Figure note below the drawing.** "A. The modulating signal can be direct or capacitively coupled to CONT. For direct coupling, consider the effects of modulation source voltage and impedance on the bias of the timer."
