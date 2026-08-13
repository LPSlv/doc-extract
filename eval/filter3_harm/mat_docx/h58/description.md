**Figure (functional block diagram, MAX232 datasheet p9).** The page's only drawn
artwork, sitting under the heading "**7.2 Functional Block Diagram**". Simple black
line art, no border, no caption line of its own.

**Elements, top to bottom:**

1. **Power rail row.** Label "**5V**" at the left, a short horizontal wire running
   right into a plain rectangular box labelled "**POWER**". Nothing leaves the box on
   the drawing — it represents the on-chip charge-pump / voltage generator block.

2. **Transmit path (middle row).** Label "**TIN**" at the left. A horizontal wire runs
   right; part-way along it is a **diagonal slash tick with the numeral "2" above it**
   (bus-width marker: two identical channels). The wire enters the flat left edge of a
   **triangle pointing right** labelled "**TX**" (buffer/driver symbol). From the
   triangle's right-hand apex a wire continues right, again crossed by a **slash with
   "2"**, ending at the two-line label "**TOUT / RS232**".

3. **Receive path (bottom row).** Label "**ROUT**" at the left. A horizontal wire runs
   right from that label, crossed by a **slash with "2"**, into the **apex of a
   triangle pointing left** labelled "**RX**" (buffer/receiver symbol). The triangle's
   flat right-hand edge continues right as a wire, crossed by another **slash with
   "2"**, ending at the two-line label "**RIN / RS232**". Signal flow on this row is
   therefore right-to-left: RS232 in at RIN, logic out at ROUT.

**Every legible string inside the figure:** "5V", "POWER", "TIN", "2" (x4, one on each
slashed wire), "TX", "TOUT", "RS232" (x2), "ROUT", "RX", "RIN".

The "2" markers encode that the device contains two drivers and two receivers — the
dual driver/receiver described in section 7.1 Overview.

No chart, no other figure on the page. The rest of the page is body prose
(sections 7.1 Overview, 7.2, 7.3 Feature Description with 7.3.1 Power / 7.3.2 RS232
Driver / 7.3.3 RS232 Receiver, 7.4 Device Functional Modes, 7.4.3 Function Tables) and
"Table 7-1. Each Driver", all of which is extractable text.

Page furniture: TI logo, "www.ti.com", "MAX232", "SLLS047N − FEBRUARY 1989 − REVISED
FEBRUARY 2024"; footer "Copyright © 2024 Texas Instruments Incorporated", "Submit
Document Feedback", page 9, "Product Folder Links: MAX232".
