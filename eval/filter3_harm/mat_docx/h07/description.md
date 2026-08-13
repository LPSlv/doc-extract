Page from the Texas Instruments SN74HC126 / SN54HC126 data sheet (SCLS103F), section 8.3.3 "Clamp Diode Structure". One figure.

## Figure 8-1 — clamp diode schematic

Caption: "**Figure 8-1. Electrical Placement of Clamping Diodes for Each Input and Output**".

A schematic enclosed in a dashed rectangle whose top-left corner is labelled "**Device**".

- At the top of the dashed box, an open-circle terminal labelled "**V_CC**", feeding a horizontal top rail inside the box (junction dot where it meets the rail).
- At the bottom, an open-circle terminal labelled "**GND**", tied to the bottom rail.
- On the left edge, an open-circle terminal labelled "**Input**"; on the right edge, an open-circle terminal labelled "**Output**". Both connect horizontally to a central rectangular block labelled "**Logic**".
- Four clamp diodes, one pair on the input node and one pair on the output node, each drawn as a solid triangle-and-bar symbol:
  - Upper-left diode, from the Input node up to the V_CC rail, labelled "**+I_IK**" with an upward arrow beside it.
  - Lower-left diode, between the Input node and the GND rail, labelled "**−I_IK**" with a downward arrow.
  - Upper-right diode, from the Output node up to the V_CC rail, labelled "**+I_OK**" with an upward arrow.
  - Lower-right diode, between the Output node and the GND rail, labelled "**−I_OK**" with a downward arrow.
- Junction dots mark where the diode pairs tap the Input and Output nets and where the diodes meet the V_CC and GND rails.

The arrow directions encode current sense: `+I_IK` / `+I_OK` current flowing into the part toward V_CC, `−I_IK` / `−I_OK` current flowing out toward GND.

Everything else on the page — the CAUTION box, section headings 8.3.3 / 8.4, and Table 8-1 "Function Table" — is plain extractable text.

Page furniture: Texas Instruments logo, "www.ti.com", "SN74HC126, SN54HC126", "SCLS103F – MARCH 1984 – REVISED APRIL 2021"; footer "Copyright © 2021 Texas Instruments Incorporated", "Submit Document Feedback", "11", "Product Folder Links: SN74HC126 SN54HC126".
