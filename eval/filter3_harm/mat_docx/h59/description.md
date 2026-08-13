Texas Instruments **NA556, NE556, SA556, SE556** datasheet page 11. Two figures.

## Figure 7-2. Pulse-Width-Modulation vs Control Voltage — Clock Duty Cycle 98%, V$_{CC}$ = 5V

Under heading "**7.2.1.3 Application Curve**".

**Type.** Two-series line chart, gridded plot box, no markers.

- **Y axis:** "Output Duty Cycle (%)", 0 to 100, ticks and horizontal gridlines at 0,
  20, 40, 60, 80, 100.
- **X axis:** "Control Voltage (V)", 0.5 to 4.5, ticks and vertical gridlines at 0.5,
  1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5.
- **Legend** (boxed, upper left inside the plot): "**Clock period = 1 RC**" — black
  line; "**Clock period = 2.5 RC**" — red line.
- **Plot ID:** "**D001**" in the lower-right corner inside the plot box.

**Black curve (1 RC).** Rises steeply and convexly, reaching the top of the axis well
before the right edge. Approximate values (read from axis): the curve begins at the
left edge with a short near-vertical segment around 0.5 V spanning roughly 5–15%; then
≈20% at 1.0 V, ≈28% at 1.5 V, ≈40% at 2.0 V, ≈57% at 2.5 V, ≈80% at 2.8 V, and
**100% at about 3.0 V**, after which it leaves the plot — no black data is drawn for
control voltages above ≈3.0 V.

**Red curve (2.5 RC).** Lower and much flatter, rising convexly across the whole axis.
Approximate values (read from axis): ≈5% at 0.5 V, ≈10% at 1.0 V, ≈17% at 1.5 V, ≈24%
at 2.0 V, ≈33% at 2.5 V, ≈43% at 3.0 V, ≈55% at 3.5 V, ≈70% at 4.0 V, ≈93% at 4.5 V.

**Caption as printed (two lines, centred):** "Figure 7-2. Pulse-Width-Modulation vs
Control Voltage / Clock Duty Cycle 98%, V$_{CC}$ = 5V".

## Figure 7-3. Circuit for Pulse-Position Modulation

Under heading "**7.2.2 Pulse-Position Modulation**".

**Type.** Circuit schematic (black line art) of a 555/556-style timer wired as an
astable whose threshold is modulated.

**Topology.**

- A large rectangular **timer block** in the centre with its pins labelled inside along
  the edges: **RESET** and **V$_{CC}$** on the top-left/top-inside, **TRIG** on the
  left, **CONT** on the lower left, **OUT** on the right, **DISCH** on the right below
  OUT, **THRES** on the right below DISCH, and **GND** at the bottom.
- **V$_{CC}$** is labelled at the top of the drawing on a horizontal supply rail. From
  that rail a wire drops (via a junction dot) to the block's **V$_{CC}$** pin, and a
  second wire from the same rail runs right and down through **R$_A$** (zig-zag
  resistor, labelled "**R$_A$**") to a node.
- That node connects to the **DISCH** pin (junction dot) and continues down through
  **R$_B$** (zig-zag resistor, labelled "**R$_B$**") to a lower node.
- The lower node connects to the **THRES** pin (junction dot) and continues down
  through **C$_T$** (capacitor, two parallel plates, labelled "**C$_T$**") to a
  **ground symbol**.
- The **RESET** pin is tied by a wire running left and up to the same top rail /
  V$_{CC}$ (the wire leaves the block's left side and turns upward).
- **OUT** goes right to a terminal labelled "**Output**".
- **CONT** on the left is driven by an input labelled, in three stacked lines to the
  left of the block, "**Modulation Input (see Note A)**".
- **GND** at the bottom of the block goes down to its own **ground symbol**.
- **TRIG** on the left has a short stub wire running left then up (tied into the
  RESET/supply-side wiring).

**Note below the figure, as printed:** "A. The modulating signal can be direct or
capacitively coupled to CONT. For direct coupling, consider the effects of modulation
source voltage and impedance on the bias of the timer."

**Caption as printed:** "Figure 7-3. Circuit for Pulse-Position Modulation".

Page furniture: TI logo, "www.ti.com", "NA556, NE556, SA556, SE556", "SLFS023I − APRIL
1978 − REVISED MARCH 2025"; footer "Copyright © 2025 Texas Instruments Incorporated",
"Submit Document Feedback", page 11, "Product Folder Links: NA556 NE556 SA556 SE556".
