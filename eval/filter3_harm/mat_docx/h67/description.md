**Page furniture (p17).** Texas Instruments logo top left with "www.ti.com"; right header "TL431, TL432" and "SLVS543S – AUGUST 2004 – REVISED MAY 2024". Footer: "Copyright © 2024 Texas Instruments Incorporated", "Submit Document Feedback", page number 17, "Product Folder Links: TL431 TL432".

The page holds six figures in a two-column, three-row grid (graphs left, test circuits right).

---

## Figure 6-12. Reference Impedance vs Frequency

**Type.** Log-log line plot, single curve, on a full log grid.

**Axes.**
- X: "f – Frequency – Hz", logarithmic, decade ticks labelled 1 k, 10 k, 100 k, 1 M, 10 M.
- Y: "|z<sub>KA</sub>| – Reference Impedance – Ω", logarithmic, decade ticks labelled 0.1, 1, 10, 100.

**In-plot annotations (top-left corner).** "I<sub>KA</sub> = 10 mA", "T<sub>A</sub> = 25°C".

**Curve.** Flat and low across the low-frequency decades, sitting near the bottom of the grid at roughly 0.2 Ω (read from axis) from 1 kHz to about 100 kHz, then rising steeply and monotonically from about 200 kHz onward: passing ~1 Ω near 700 kHz (read from axis), ~10 Ω near 5 MHz (read from axis), and flattening to a slight plateau of ~12–15 Ω (read from axis) at the 10 MHz end of the sweep. No legend; only the one trace.

---

## Figure 6-13. Test Circuit for Reference Impedance

**Type.** Schematic (test circuit).

**Topology.** An AC source symbol (circle with sine wave) on the left drives, through a series 50 Ω resistor drawn in the vertical leg, a node that feeds a horizontal 1 kΩ resistor. The right end of the 1 kΩ resistor is the node labelled "Output" at the top right. From that node the current I<sub>KA</sub> (downward arrow, labelled "I<sub>KA</sub>") flows into the shunt-regulator symbol (a boxed triangle/zener-reference device, the TL431 symbol). Below the device is an adjustable/variable zener element in series, with a "+" sign marked beside it, returning to the bottom rail. The bottom rail runs left to the source and right to the node labelled "GND", which carries an earth-ground symbol.

**Component callouts.** 1 kΩ (series to Output), 50 Ω (source series resistor), I<sub>KA</sub>. Node labels: Output, GND.

---

## Figure 6-14. Pulse Response

**Type.** Time-domain line plot with two traces (input drawn dashed, output drawn solid).

**Axes.**
- X: "t – Time – µs", linear, ticks −1, 0, 1, 2, 3, 4, 5, 6, 7.
- Y: "Input and Output Voltage – V", linear, 0 to 6, ticks every 1 V.

**In-plot annotations.** "T<sub>A</sub> = 25°C" at top left; the dashed trace labelled "Input"; the solid trace labelled "Output".

**Traces.**
- Input (dashed): 0 V before t = 0, steps up vertically at t = 0 to 5 V, holds flat at 5 V until t = 5 µs, then steps back down vertically to 0 V.
- Output (solid): starts near 2.0 V (read from axis) at the left edge, rises with a short ramp/rounded edge between t ≈ 0 and t ≈ 0.5 µs to about 2.5 V (read from axis), holds flat at ~2.5 V until t = 5 µs, then falls vertically to 0 V at t = 5 µs, coincident with the input's falling edge.

The output swing is small (≈2.0 → 2.5 V) compared with the 0–5 V input.

---

## Figure 6-15. Test Circuit for Pulse Response

**Type.** Schematic (test circuit).

**Topology.** A box labelled "Pulse Generator / f = 100 kHz" on the left drives a node. From that node a shunt 50 Ω resistor goes down to the bottom rail, and the same node feeds a horizontal 220 Ω resistor whose right end is the "Output" node at top right. From the Output node the shunt-regulator device symbol (boxed triangle, TL431) connects down to the bottom rail. The bottom rail runs to the "GND" label at the right and carries an earth-ground symbol.

**Component callouts.** 220 Ω (series to Output), 50 Ω (shunt), "Pulse Generator f = 100 kHz". Node labels: Output, GND.

---

## Figure 6-16. Stability Boundary Conditions for All TL431 and TL431A Devices (Except for SOT23-3, SC-70, and Q-Temp Devices)

**Type.** Semi-log line plot, four labelled curves (A, B, C, D) enclosing regions of instability.

**Axes.**
- X: "C<sub>L</sub> – Load Capacitance – µF", logarithmic, decade ticks 0.001, 0.01, 0.1, 1, 10.
- Y: "I<sub>KA</sub> – Cathode Current – mA", linear, 0 to 100, ticks every 10 mA.

**In-plot legend block (top left).**
- A V<sub>KA</sub> = V<sub>ref</sub>
- B V<sub>KA</sub> = 5 V
- C V<sub>KA</sub> = 10 V
- D V<sub>KA</sub> = 15 V

Also in-plot: "T<sub>A</sub> = 25°C" at top right. The word "Stable" appears twice as a region label — once at left, around C<sub>L</sub> ≈ 0.01 µF / I<sub>KA</sub> ≈ 55 mA, and once at right, around C<sub>L</sub> ≈ 2 µF / I<sub>KA</sub> ≈ 70 mA. Curve letter labels A, B, C, D are placed on the traces: A at lower left (~C<sub>L</sub> = 0.01 µF, I<sub>KA</sub> ≈ 48 mA), B near the top (~C<sub>L</sub> = 0.1 µF, I<sub>KA</sub> ≈ 73 mA), C in the middle (~C<sub>L</sub> = 0.3 µF, I<sub>KA</sub> ≈ 52 mA), D lower centre (~C<sub>L</sub> = 0.3 µF, I<sub>KA</sub> ≈ 24 mA).

**Curve shapes (all read from axis).** Each curve is a closed/valley-shaped lobe: it comes down steeply from 100 mA at the left, reaches a minimum, and rises steeply back to 100 mA at the right, so the area under/inside each curve is the unstable region.
- Curve A: leftmost lobe, descending from 100 mA near C<sub>L</sub> ≈ 0.002 µF, minimum roughly 15–20 mA around C<sub>L</sub> ≈ 0.05–0.1 µF, rising back to 100 mA near C<sub>L</sub> ≈ 0.4 µF.
- Curve B: the widest and highest lobe, from 100 mA near C<sub>L</sub> ≈ 0.004 µF, minimum roughly 10 mA near C<sub>L</sub> ≈ 0.2 µF, back to 100 mA near C<sub>L</sub> ≈ 3 µF.
- Curve C: peak-shaped trace reaching about 52 mA at C<sub>L</sub> ≈ 0.3 µF, narrower than B.
- Curve D: smallest/lowest lobe, peaking at about 22 mA near C<sub>L</sub> ≈ 0.3 µF.

Note: the D legend entry reads "D V<sub>KA</sub> = 15 V" but the rendered glyph after 15 is ambiguous at this resolution (appears as "15 V<sub>f</sub>" or "15 V"); the trailing subscript is illegible.

**Caption text beneath the plot (inside the figure block).** "The areas under the curves represent conditions that can cause the device to oscillate. For curves B, C, and D, R2 and V+ are adjusted to establish the initial V<sub>KA</sub> and I<sub>KA</sub> conditions, with C<sub>L</sub> = 0. VBATT and C<sub>L</sub> then are adjusted to determine the ranges of stability."

---

## Figure 6-17. Test Circuits for Stability Boundary Conditions

**Type.** Two schematics stacked vertically, each with its own sub-caption.

**Upper schematic — sub-caption "TEST CIRCUIT FOR CURVE A".** A horizontal 150 Ω resistor at the top connects the supply node to the device node. On the left branch a capacitor C<sub>L</sub> is connected from the device node down to the bottom rail. The shunt-regulator device symbol (boxed triangle, TL431) sits in the centre with the cathode current arrow labelled "I<sub>KA</sub>" pointing down into it. On the right is a battery symbol labelled "V<sub>BATT</sub>" with "+" at its top terminal and "−" at its bottom, returning to the bottom rail. The bottom rail carries an earth-ground symbol. In this circuit the device's reference is tied so that V<sub>KA</sub> = V<sub>ref</sub> (curve A condition).

**Lower schematic — sub-caption "TEST CIRCUIT FOR CURVES B, C, AND D".** Same skeleton with a resistive divider added. From the device node, a resistor "R1 = 10 kΩ" runs down, and below it an adjustable resistor "R2" (drawn with an arrow through it, i.e. a potentiometer) continues to the bottom rail; the divider tap feeds the device reference. A capacitor C<sub>L</sub> is on the far left from the top node to the bottom rail. A 150 Ω resistor is in the right-hand branch, in series with the battery "V<sub>BATT</sub>" (again "+" top, "−" bottom, drawn as an adjustable source). The cathode current arrow labelled "I<sub>KA</sub>" points into the device. Bottom rail carries an earth-ground symbol.

**Component callouts across both.** 150 Ω (both circuits), C<sub>L</sub> (both), I<sub>KA</sub> (both), V<sub>BATT</sub> (both), R1 = 10 kΩ and R2 (lower only).
