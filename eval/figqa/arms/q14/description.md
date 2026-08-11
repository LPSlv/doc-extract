**Figure (block / schematic diagram, from `p011-x250.png`).** Functional block diagram of a two-channel (A and B) bipolar stepper-motor driver IC connected to a stepper motor. The raster as stored is mirrored top-to-bottom (all text reads upside-down / reversed); the description below is of the image after correcting that flip.

A single thick vertical black line runs the full height of the diagram: it is the device boundary. Everything to the left of it is on-chip; the labelled grey squares sitting on the line are the package pins; everything to the right of it is external.

Layout: two identical channel blocks stacked vertically. The upper block is the **A channel**; the lower block is the **B channel**. The caption fragment **"From Indexer Logic"** appears once, at the top left of the A-channel block, above the incoming control lines.

**A channel (upper block), left to right:**

- Three horizontal input arrows entering a tall rectangular block labelled **PWM**, labelled from top to bottom: **AENBL**, **APHASE**, **ADECAY**.
- Below them, a bus arrow labelled **AI[4:0]** runs into a pentagon-shaped block labelled **DAC**. The bus is drawn with a diagonal slash tick annotated **5**.
- A further input line labelled **AVREF** runs from the left edge, turns upward, and enters the bottom of the **DAC** block (its reference input).
- The **DAC** output goes to the **+** input of a comparator (triangle with **−** on the upper input and **+** on the lower input). The comparator output feeds back into the right-hand side of the **PWM** block.
- The **−** input of the comparator is driven by a second triangle (amplifier) annotated **A = 5**, whose input comes from the sense node.
- The **PWM** block drives, via two arrows, a rectangular block labelled **Pre-drive** (drawn as "Pre-" over "drive").
- **Pre-drive** also receives an arrow from the left labelled **VCP, VGD**, and two arrows labelled **OCP** — one entering near its top, one entering near its bottom. Each **OCP** line originates at a small open circle (current-sense symbol) placed in series with the power path.
- The output stage is drawn as four MOSFET symbols, each with an antiparallel body diode, arranged as an H-bridge (two high-side, two low-side), with their gates driven by lines coming from **Pre-drive**.

**A-channel pins on the boundary line (top to bottom):** **VM**, **AOUT1**, **AOUT2**, **AISEN**.

**A-channel external connections (right of the boundary):**

- **VM** pin connects to a filled blue up-arrow supply symbol labelled **VM**.
- **AOUT1** and **AOUT2** run to the two ends of a coil (winding) symbol drawn immediately to the left of a circle labelled **Step Motor**; this is the A-phase winding.
- **AISEN** connects to a resistor (zigzag symbol) whose lower end goes to a ground (open triangle) symbol — the sense resistor.
- A second coil symbol is drawn just below/right of the Step Motor circle; its two leads run down the right side of the page to the B-channel outputs.

**B channel (lower block):** identical topology, with the labels changed:

- Inputs to the **PWM** block, top to bottom: **BENBL**, **BPHASE**, **BDECAY**.
- Bus input **BI[4:0]** into the **DAC**, with the diagonal bus tick annotated **4** (as printed; the A-channel equivalent tick is annotated **5**).
- Reference input **BVREF** into the bottom of the **DAC**.
- Comparator with **−** and **+** inputs, sense amplifier annotated **A = 5**, feedback into **PWM**.
- **Pre-drive** block with **VCP, VGD** input and two **OCP** inputs from the two current-sense circles.
- Four MOSFETs with body diodes forming the second H-bridge.

**B-channel pins on the boundary line (top to bottom):** **VM**, **BOUT1**, **BOUT2**, **BISEN**.

**B-channel external connections:** **VM** to a blue up-arrow **VM** supply symbol; **BOUT1** and **BOUT2** route via long wires up the right-hand side to the two ends of the second motor winding (the one drawn under the Step Motor circle); **BISEN** to a resistor to ground (open triangle).

There is no title block, axis, legend or numeric data in the graphic other than the bus-width ticks (**5** on AI[4:0], **4** on BI[4:0]) and the amplifier gain annotations (**A = 5** in both channels). No figure number or caption text is visible within the raster.
