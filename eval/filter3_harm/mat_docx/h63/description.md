Page from the TI OPA365 / OPA2365 datasheet (SBOS365G), section 8.3.5 *Active
Filtering* / 8.4 *Device Functional Modes*. Two schematic figures.

**Figure 8-5 (circuit schematic). Second-Order Butterworth, 500-kHz Low-Pass Filter.**
Multiple-feedback (MFB) topology built around one op amp drawn as a triangle labelled
**OPA365**, inverting input "−" on top, non-inverting input "+" below, supply pins
"V+" (above the body) and "V−" (below the body).

Connections, left to right:
- Input terminal "V_IN" (open circle) → **R₁ 549Ω** → node A.
- From node A, **C₁ 1nF** goes down to ground (ground symbol).
- From node A, **R₂ 1.24kΩ** → node B, which is the inverting (−) input of the OPA365.
- **R₃ 549Ω**, drawn along the top of the schematic, connects node A to the amplifier
  output node.
- **C₂ 150pF**, drawn below R₃, connects node B (the inverting input) to the amplifier
  output node.
- The non-inverting (+) input is tied to ground (ground symbol).
- The V− supply pin is tied to ground (ground symbol); the V+ supply pin ends in an
  open-circle terminal.
- The amplifier output goes right to an open-circle terminal labelled "V_OUT".

Component labels as printed: R₁ 549Ω, R₂ 1.24kΩ, R₃ 549Ω, C₁ 1nF, C₂ 150pF.
Note under the drawing: "Copyright © 2016, Texas Instruments Incorporated".

**Figure 8-6 (circuit schematic). Configured as a Three-Pole, 20-kHz, Sallen-Key
Filter.**
Unity-gain Sallen-Key stage preceded by a passive RC pole, around one op amp triangle
labelled **OPA365** with the non-inverting input "+" on top and the inverting input
"−" below.

Connections, left to right:
- Input terminal labelled "V_IN = 1V_RMS" (open circle) → **R₁ 1.8kΩ** → node A.
- **C₁ 3.3nF** from node A to ground (first, passive pole).
- Node A → **R₂ 19.5kΩ** → node B.
- Node B → **R₃ 150kΩ** → node C, which drives the non-inverting (+) input.
- **C₂ 47pF** from node C to ground.
- **C₃ 220pF**, drawn along the top, connects node B back to the amplifier output node
  (positive feedback around R₃).
- The inverting (−) input is wired straight back to the output (unity-gain follower):
  a wire leaves the "−" pin, runs down and right, and joins the output net.
- The output node goes right to an open-circle terminal labelled "V_OUT".

Component labels as printed: R₁ 1.8kΩ, R₂ 19.5kΩ, R₃ 150kΩ, C₁ 3.3nF, C₂ 47pF,
C₃ 220pF.
Note under the drawing: "Copyright © 2016, Texas Instruments Incorporated".

Page furniture (not part of the figures): running head "OPA365, OPA2365",
"SBOS365G – MAY 2006 – REVISED MAY 2023", Texas Instruments logo, "www.ti.com";
footer page 16, "Submit Document Feedback",
"Copyright © 2023 Texas Instruments Incorporated",
"Product Folder Links: OPA365 OPA2365".
