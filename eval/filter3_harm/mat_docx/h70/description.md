**Page furniture (p16).** Left header "TLV271, TLV272, TLV274" and "SLOS351E – FEBRUARY 2004 – REVISED NOVEMBER 2016"; Texas Instruments logo top right with "www.ti.com". Footer: page number 16, "Submit Documentation Feedback", "Copyright © 2004–2016, Texas Instruments Incorporated", "Product Folder Links: TLV271 TLV272 TLV274".

One figure on the page (under heading "8.2 Functional Block Diagram"); the lower two-thirds of the page is blank.

---

## Functional Block Diagram (section 8.2)

**Type.** Transistor-level functional block diagram of the op-amp. It carries no numbered figure caption — only the section heading "8.2 Functional Block Diagram" above it and a copyright line below it.

**Terminals (open-circle pins).**
- "V<sub>DD</sub>" at the top centre, feeding a horizontal supply rail.
- "GND" at the bottom centre, on the bottom rail.
- "IN+" on the left, upper of the two input pins.
- "IN−" on the left, lower of the two input pins.
- "OUT" on the right.

**Structure and connections (left to right).**
1. From the V<sub>DD</sub> pin a vertical line drops to a horizontal rail. That rail feeds, on the left, the top ends of two load resistors (drawn as zigzags side by side), and on the right the "Bias" block.
2. Input differential pair: two MOSFET symbols (each drawn as a MOS transistor with the arrow on the body/substrate lead) sit below the resistors. The gate of the left transistor connects out to the "IN+" pin; the gate of the right transistor connects out to the "IN−" pin (its lead runs left and down to the lower input pin). The two transistors' drains go up to the two load resistors — the left transistor to the left resistor, the right transistor to the right resistor.
3. The common source node of the pair connects downward to a current-source symbol (circle with a downward arrow inside), whose bottom connects to the ground rail — the tail current source.
4. The signal is taken from the differential pair's right-hand drain/load node and runs right into a triangle (gain stage / amplifier symbol), whose output feeds a second triangle (output buffer stage), whose output runs right to the "OUT" pin.
5. A rectangular block labelled "Bias" sits above the two triangles, fed from the V<sub>DD</sub> rail; a vertical line runs from the Bias block down the right-hand side of the diagram to the bottom ground rail, and the two triangular stages sit inside that Bias-fed column, i.e. the bias block supplies the gain and output stages.
6. The bottom rail joins the tail current source, the right-hand bias column and the "GND" pin.

**Every legible string in the drawing.** V<sub>DD</sub>, GND, IN+, IN−, OUT, "Bias". No component values, no dimension callouts.

**Line beneath the drawing.** "Copyright © 2016, Texas Instruments Incorporated".
