Front page of the Texas Instruments SN65HVD230 / SN65HVD231 / SN65HVD232 data sheet (SLOS346O). One substantive figure plus branding.

**Masthead / navigation strip (p1).** Texas Instruments logo, and a row of five link buttons with icons: "Product Folder", "Order Now", "Technical Documents", "Tools & Software", "Support & Community". Bottom-of-page warning triangle icon beside the IMPORTANT NOTICE paragraph.

## Figure — "Equivalent Input and Output Schematic Diagrams"

Heading printed above the drawing: "**Equivalent Input and Output Schematic Diagrams**". It is a transistor-level / mixed block schematic of one CAN transceiver, drawn inside a heavy rectangular device boundary. No figure number is printed.

**Pins entering the boundary on the left edge, top to bottom:** `D`, `R_S`, `NC`, `R`.
**Pins entering the top edge:** `V_CC` and `V_REF`.
**Pin at the bottom edge:** `GND`.
The two output nets leave the right-hand part of the schematic and run to the device boundary; **no pin names are printed on those two right-hand nets** in this rendering (they are the bus outputs, drawn as two horizontal rails with junction dots).

**Blocks and devices, as drawn:**

- A box labelled "**V_CC / 2**" near the top centre, fed from `V_CC` and from `V_REF` above it — i.e. `V_REF` is generated as half the supply.
- Both the `D` and `R_S` input pins carry a small current-source / pull-up symbol to `V_CC` (an arrow into a circle-with-bar) immediately inside the boundary.
- A box labelled "**Thermal Shutdown**" (upper left of centre), whose output drops into the block below it.
- A large box labelled "**SLOPE CONTROL and MODE LOGIC**", fed from `R_S` on the left, connected upward to the Thermal Shutdown block, and driving lines to the right.
- A right-pointing triangle (driver / amplifier) fed from the `D` path and from the SLOPE CONTROL block; a small rectangle symbol sits inside the triangle on its input line.
- The triangle's two outputs drive a high-side and a low-side output transistor. Each transistor is drawn as a MOSFET with a series diode to its supply: the high-side device has a diode from `V_CC` (labelled `V_CC` above it) into its drain; the low-side device has a diode arrangement and its source returns to the bottom rail.
- A tall narrow box on the right labelled "**BIAS UNIT**" (text rotated 90°), fed from `V_CC` at its top; it contains a series string drawn as bar–resistor–resistor–bar between the two bus rails, i.e. a split termination/bias network tapped between the two outputs.
- The two bus rails leave the transistor stage and the BIAS UNIT to the right, each with a junction dot, and run to the device boundary.
- At the bottom right, a left-pointing triangle containing a **hysteresis (Schmitt-trigger) symbol** — the receiver comparator. Its output has a small inversion bubble on the left and drives the `R` pin. Its two inputs are tied back to the two bus rails (one from each rail, routed down the right side).
- The SLOPE CONTROL and MODE LOGIC block also drives a line to the receiver stage at the bottom.
- `NC` on the left edge terminates in a short unconnected stub.
- The bottom edge of the boundary is the ground rail, brought out as `GND`.

Everything else on the page (Features, Applications, Description, the Device Information table) is ordinary body text and a plain table.

Page furniture: "SN65HVD230, SN65HVD231, SN65HVD232"; "SLOS346O − MARCH 2001 − REVISED APRIL 2018"; document title "SN65HVD23x 3.3-V CAN Bus Transceivers".
