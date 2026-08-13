**Page 22, "3. Application Circuit Examples"** (ZSC31050 Datasheet, Renesas). Four application schematics, each in its own bordered frame, laid out two-by-two. All four use the same 16-pin ZSC31050 IC symbol, drawn as a tall DIP-style body with the part name "ZSC31050" set vertically inside it and a notch at the bottom edge. In every instance the pins are labelled identically:

- Left side, top to bottom: 9 FBN, 10 OUT, 11 FBP, 12 IR_TEMP, 13 VBR, 14 VINP, 15 VSS, 16 VINN.
- Right side, top to bottom: 8 VDD, 7 SDA, 6 SCL, 5 IO2, 4 IO1, 3 VGATE, 2 IN3, 1 VDDA.

Pins that leave the board are drawn as small crossed squares (test/solder pads); supply and signal terminations are drawn as flag/arrow-shaped connector symbols (V_SUPP, GND, Out / OWI, etc.).

---

## Figure 3. Application Example 1

**Type:** circuit schematic. Caption text above the frame: "Typical ratiometric measurement with voltage output, temperature compensation via external diode, internal VDD regulator, and active sensor connection check (bridge must not be at VDDA)".

Strings inside the frame: "+2.7V to +5.5V", "V_SUPP", "C2 0.1µF", "C1 0.1µF", "ZSC31050", pin names as listed above, "SDA", "SCL", "IO2", "IO1" (external pad labels beside pins 7, 6, 5, 4 respectively), "Serial Interface", "Flexible I/Os", "Sensor Bridge", "C2 < 15nF", "Out / OWI", "GND".

Connections as drawn:
- Top rail "+2.7V to +5.5V" runs from the V_SUPP connector across the top. C1 (0.1µF) sits from that rail to the GND rail. C2 (0.1µF) is in the wire from VDD (pin 8) to the same supply rail.
- VDDA (pin 1) is wired to the right up to the supply rail.
- An external diode (triangle pointing downward, i.e. anode on the upper wire) hangs from the supply-side vertical wire on the left; its lower end feeds IR_TEMP (pin 12) — this is the external temperature-compensation diode named in the caption.
- FBN (pin 9) and OUT (pin 10) are tied to the same vertical node, which continues down to the "Out / OWI" connector. C2 (< 15nF) is from that output line to GND.
- FBP (pin 11) runs down to the GND rail.
- Sensor bridge (a four-resistor diamond inside a light box labelled "Sensor Bridge") has four square pads connected to VBR (pin 13), VINP (pin 14), VSS (pin 15) and VINN (pin 16); the VSS node also ties to the GND rail.
- IN3 (pin 2) runs down to the GND rail.
- Pins 7 (SDA) and 6 (SCL) go to external pads "SDA"/"SCL"; a double-headed arrow to their right is captioned "Serial Interface". Pins 5 (IO2) and 4 (IO1) go to external pads "IO2"/"IO1"; a second double-headed arrow is captioned "Flexible I/Os".

## Figure 4. Application Example 2

**Type:** circuit schematic. Caption above the frame: "0V to 10V output configuration with supply regulator (external JFET), temperature compensation via internal diode, and bridge in voltage mode".

Strings inside the frame: "VDDA = 5V", "+7V to +48V", "V_SUPP", "R3 390Ω", "Out: 0 to 10V", "R1 2.2kΩ", "C1 0.1µF", "R4 1kΩ", "R2 2kΩ", "C2 0.1µF", "C3 0.1µF", "ZD 6.8V", "ZSC31050", pin names, external pad labels "SDA" (pin 7), "SCL" (pin 6), "IO1" (beside pin 5, which is named IO2), "IO2" (beside pin 4, which is named IO1) — the external labels are printed crossed relative to the pin names, as drawn. Also "Sensor Bridge", "GND".

Connections as drawn:
- Supply enters at V_SUPP, "+7V to +48V". A JFET (depletion-FET symbol with gate arrow) sits in the top rail between V_SUPP and the regulated node labelled "VDDA = 5V"; its gate is driven from VGATE (pin 3).
- C2 (0.1µF) and C3 (0.1µF) hang from the VDDA rail down to the bottom GND rail on the left.
- ZD, a 6.8V zener, is in the left-hand branch between the vertical rail that feeds the sensor bridge and the node shared by the C2/C3 tops and the FBP (pin 11) wire.
- VDDA (pin 1) is wired out to the right and up to the "VDDA = 5V" node.
- Output stage on the right: R3 (390Ω) from the V_SUPP rail down to the base of an NPN transistor whose collector goes to V_SUPP; the emitter is the "Out: 0 to 10V" terminal. From that output node R1 (2.2kΩ) runs down to a node that carries R2 (2kΩ) to GND and connects horizontally to the top plate of C1 (0.1µF). The bottom of C1 joins the base of a second NPN transistor, whose collector goes up to the R3/base node and whose emitter goes through R4 (1kΩ) to GND. The base node of this lower transistor is also carried back left by a long wire to the OUT (pin 10) side of the IC.
- Sensor bridge (four-resistor diamond, box labelled "Sensor Bridge") wired through four square pads to VBR (13), VINP (14), VSS (15), VINN (16).
- IN3 (pin 2) runs down to the GND rail.

## Figure 5. Application Example 3

**Type:** circuit schematic. Caption above the frame: "Absolute voltage output, supply regulator (external JFET), constant current excitation of the sensor bridge, temperature compensation by bridge voltage drop measurement, internal VDD regulator without external capacitor".

Strings inside the frame: "VDDA = 5V", "+7V to +48V", "V_SUPP", "C1 0.1µF", "C2 0.1µF", "ZD 6.8V", "R_BR_REF" (subscript BR_REF, on a resistor at the far left), "ZSC31050", pin names, external pads "SDA" (pin 7), "SCL" (pin 6), "IO1" (beside pin 5 IO2), "IO2" (beside pin 4 IO1), "Serial Interface", "Flexible I/Os", "Sensor Bridge", "C2 < 15nF", "Out / OWI", "GND".

Connections as drawn:
- V_SUPP ("+7V to +48V") feeds a JFET in the top rail; the regulated node is labelled "VDDA = 5V". VGATE (pin 3) runs right and up to the JFET gate.
- C1 (0.1µF) from the VDDA rail to the GND rail. C2 (0.1µF) is in series from VDD (pin 8) to the VDDA rail node, and the zener ZD (6.8V) is drawn from that rail across to the V_SUPP side (cathode toward the supply).
- R_BR_REF, a resistor at the far left, connects the top rail down to the wire that runs to IR_TEMP (pin 12) — the reference resistor for constant-current bridge excitation / bridge-drop temperature measurement.
- FBN (pin 9) and OUT (pin 10) are on the same node, which runs down to the "Out / OWI" connector; C2 (< 15nF) from that line to GND.
- FBP (pin 11) runs down to the GND rail.
- Sensor bridge (four-resistor diamond in a box labelled "Sensor Bridge") wired via four square pads to VBR (13), VINP (14), VSS (15), VINN (16); the VSS node also goes to GND.
- IN3 (pin 2) and VDDA (pin 1) run right to the VDDA rail node.
- Double-headed arrows on the right captioned "Serial Interface" (level with SDA/SCL) and "Flexible I/Os" (level with the IO pads).

## Figure 6. Application Example 4

**Type:** circuit schematic. Caption above the frame: "Ratiometric bridge differential signal measurement, 3–wire connection for end-of-line calibration at OUT pin (ZACwire™), additional temperature measurement with external thermistor, and PWM output at IO1 pin".

Strings inside the frame: "+2.7V to +5.5V", "V_SUPP", "C1 0.1µF", "C2 0.1µF", "R_T" (subscript T), "PTC", "ZSC31050", pin names, external pads "SDA" (pin 7) and "SCL" (pin 6) only, "PWM OUT" (connector at pin 4, IO1), "Sensor Bridge", "C2 < 15nF", "Out / OWI", "GND".

Connections as drawn:
- Supply rail "+2.7V to +5.5V" from V_SUPP across the top; C1 (0.1µF) from that rail to GND; C2 (0.1µF) in series from VDD (pin 8) to the supply rail.
- External temperature branch at the far left: R_T from the supply rail down to a node, and from that node a PTC thermistor (resistor with a diagonal arrow through it, labelled "PTC") continues down to the bottom GND rail. The mid node between R_T and the PTC feeds IR_TEMP (pin 12).
- FBN (pin 9) and OUT (pin 10) share a node that runs down to the "Out / OWI" connector; C2 (< 15nF) from that line to GND. FBP (pin 11) runs down to the GND rail.
- IO1 (pin 4) runs straight out to the connector labelled "PWM OUT". IO2 (pin 5) and VGATE (pin 3) are left unconnected (no external pads, unlike Figures 3–5).
- Sensor bridge (four-resistor diamond, box labelled "Sensor Bridge") wired via four square pads to VBR (13), VINP (14), VSS (15), VINN (16); the VBR node also ties up to the supply rail and the VSS node to GND.
- IN3 (pin 2) and VDDA (pin 1) run right and down/up to GND and the supply rail respectively.

---

Page furniture: header "ZSC31050 Datasheet" with Renesas logo; footer "© 2022 Renesas Electronics Corporation", page number 22, "January 14, 2022".
