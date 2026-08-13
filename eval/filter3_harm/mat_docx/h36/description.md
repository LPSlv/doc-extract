**Figure 6-10 (schematic / system block diagram, p13, CD4066B datasheet SCHS051J).** Caption below the drawing: "Figure 6-10. Four-Channel PAM Multiplex System Diagram". Copyright line printed inside the figure area, above the caption: "Copyright © 2016, Texas Instruments Incorporated".

**Type:** logic schematic in two halves — the multiplexer (transmit) circuit on the left of the page and the demultiplexer (receive) circuit on the right. Every device pin is drawn as a small circled number next to the block; blocks are labelled with the CMOS part number. The two halves are drawn as separate circuits (no wire crosses between them on the page); the PAM line and the clock/reset lines are the implied link.

## Left half — multiplexer (transmit)

**CD4018B (presettable divide-by-N counter), top-left block.**
- Left-side inputs: "Clock" → pin (14); "Reset" → pin (15). Both come in from open-circle terminals at the far left.
- Top edge, jam/preset inputs left to right: pin (10) = P_E, pin (2) = J1, pin (3) = J2, pin (7) = J3, pin (9) = J4, pin (12) = J5. The J5 line (pin 12) runs right to a ground symbol.
- Bottom edge: pin (1) at the left, and two outputs labelled with overbars, "Q̄1" and "Q̄2", carried on pins (5) and (4) respectively.

**1/3 CD4049B (inverters), lower left.** Two inverter triangles with bubbles: input pin (3) → output pin (2); input pin (5) → output pin (4). Block caption "1/3 CD4049B".

**CD4001B (quad NOR), centre.** Drawn as a package outline containing two gate symbols with a dashed line between them (the other two gates implied). Input pins along the left/top: (1), (2), (5), (6), (8), (9), (12), (13); output pins on the right/bottom: (3), (4), (10), (11). The gate inputs are fed from the CD4018B outputs (pins 5 and 4) and from the CD4049B inverter outputs (pins 2 and 4), so each NOR decodes one time slot.

**1/4 CD4066B (single switch), upper right of this half.** Control pin (13) on top, signal pin (1) on the left, signal pin (2) on the right. Its control line is tapped from the clock/counter node; its output (pin 2) feeds the outgoing PAM line — this is the sync/marker switch.

**CD4066B (quad bilateral switch), bottom centre.** Labelled "CD4066B" inside the block.
- Control inputs entering the top/left of the block: pins (12), (6), (5), (13) — driven by the four CD4001B outputs (11), (10), (4), (3).
- Signal inputs on the left, from four open-circle terminals under the heading "Signal Inputs", each on its own labelled wire: "Channel 1" → pin (1), "Channel 2" → pin (4), "Channel 3" → pin (8), "Channel 4" → pin (11). The four input terminals are joined by a vertical line at the far left of the drawing.
- Signal outputs on the right: pins (2), (3), (9), (10) are all tied to one common node (solid junction dots), which goes to a resistor labelled "10 kΩ" to ground and out as the multiplexed PAM signal.

## Right half — demultiplexer (receive)

**CD4018B, top block.** Same arrangement as the left: "Clock" line → pin (14); an open-circle terminal labelled "External Reset" → pin (15); top jam inputs pin (10) = P_E, (2) = J1, (3) = J2, (7) = J3, (9) = J4, (12) = J5, with J5 taken to ground; bottom pin (1); outputs "Q̄1" on pin (5) and "Q̄2" on pin (4).

**1/3 CD4049B (inverters).** Input pin (7) → output pin (6); input pin (9) → output pin (10). Caption "1/3 CD4049B".

**CD4001B (quad NOR), centre right.** Package outline with two gate symbols and a dashed continuation line, labelled "CD4001B". Input pins across the top, left to right: (13), (12), (9), (8), (6), (5), (2), (1). Output pins along the bottom: (11), (10), (4), (3). The four outputs run down and left/right to the control pins of the receiving CD4066B, ending at circled pins (12), (6), (5) and (11) respectively.

**1/6 CD4049B (inverter), left of the receive switch.** Input pin (11) → output pin (12); caption "1/6 CD4049B". Its output drives control pin (5) of the "1/4 CD4066B" block below it.

**1/4 CD4066B (single switch).** Control pin (5) on top, signal pin (4) on the left (fed from the incoming line, which also carries the clock recovery tap), signal pin (3) on the right, which feeds the demultiplexer switch inputs.

**CD4066B (quad bilateral switch), tall block at centre right.** Labelled "CD4066B".
- Control pins entering the top: (12), (6), (5), (11) as printed. (At this render resolution the last of these and the left-side pin (11) below cannot both be right; one of the two circled "11" labels may be a "13" — reported as drawn.)
- Left side, signal pins (1), (4), (8), (11), all commoned onto one vertical bus fed from the "1/4 CD4066B" output pin (3), i.e. the received PAM line is applied to all four switches.
- Right side, signal pins (2), (3), (9), (10). Each output node has a "10 kΩ" resistor to ground (four of them, each labelled "10 kΩ" with a ground symbol) and then feeds a small box labelled "LPF".
- The four LPF outputs are labelled, top to bottom, "Channel 1", "Channel 2", "Channel 3", "Channel 4", ending in open-circle terminals joined by a vertical line at the far right, under the heading "Signal Outputs".

**All legible strings in the figure:** "Clock", "Reset", "External Reset", "CD4018B", "P_E", "J1", "J2", "J3", "J4", "J5", "Q̄1", "Q̄2", "1/3 CD4049B", "1/6 CD4049B", "CD4001B", "CD4066B", "1/4 CD4066B", "LPF", "10 kΩ", "Signal Inputs", "Signal Outputs", "Channel 1", "Channel 2", "Channel 3", "Channel 4", and the pin numbers listed above.

Page furniture: Texas Instruments logo, "www.ti.com", "CD4066B", "SCHS051J – NOVEMBER 1998 – REVISED AUGUST 2024"; footer "Copyright © 2024 Texas Instruments Incorporated", "Submit Document Feedback", page number 13, "Product Folder Links: CD4066B".
