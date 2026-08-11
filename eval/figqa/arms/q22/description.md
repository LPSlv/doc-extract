## p010-render.png — full page render (Texas Instruments datasheet, page 10)

**Page transcription.**

(Continuation of a bulleted layout-guidelines list from the previous page. The
first item is a sub-bullet, indented under an item that begins on the previous
page.)

- – Connect low-ESR, 0.1µF ceramic bypass capacitors between each supply pin and
  ground, placed as close to the device as possible. A single bypass capacitor
  from V+ to ground is applicable for single supply applications.
- Separate grounding for analog and digital portions of circuitry is one of the
  simplest and most-effective methods of noise suppression. One or more layers on
  multilayer PCB are typically devoted to ground planes. A ground plane helps
  distribute heat and reduces EMI noise pickup. Make sure to physically separate
  digital and analog grounds, paying attention to the flow of the ground current.
  For more detailed information, refer to Circuit Board Layout Techniques,
  SLOA089. *(SLOA089 is a blue hyperlink.)*
- To reduce parasitic coupling, run the input traces as far away from the supply
  or output traces as possible. If not possible to keep them separate, better to
  cross the sensitive trace perpendicular as opposed to in parallel with the
  noisy trace.
- Place the external components as close to the device as possible. Keeping RF
  and RG close to the inverting input minimizes parasitic capacitance, as shown
  in *Section 7.3.2* . *(Section 7.3.2 is a blue italic cross-reference link.)*
- Keep the length of input traces as short as possible. Always remember that the
  input traces are the most sensitive part of the circuit.
- Consider a driven, low-impedance guard ring around the critical traces. A guard
  ring can significantly reduce leakage currents from nearby traces that are at
  different potentials.

### *7.3.2 Layout Example*

---

### Figure 7-5 (circuit schematic, upper figure)

Caption below the drawing: **Figure 7-5. Operational Amplifier Schematic for
Noninverting Configuration**

Line-art schematic of a single op amp drawn as a triangle pointing right, with no
component values printed — every element is labelled by reference designator
only.

Connections, as drawn:

- **VIN** enters at the upper left on a horizontal wire, passes through resistor
  **RIN** (zig-zag resistor symbol), and continues to the op amp's **+**
  (noninverting) input, which is the upper of the two inputs on the triangle's
  left edge.
- A **ground symbol** (three-bar earth symbol) at the lower left connects up and
  right through resistor **RG** to a junction dot; that junction connects to the
  op amp's **−** (inverting) input, the lower input on the triangle's left edge.
- From the same **−**-input junction dot, a wire runs down and right through
  feedback resistor **RF** and back up to the op amp output node.
- The op amp **output** (triangle apex, right) has a junction dot and continues
  right to the terminal labelled **VOUT**; the RF feedback path ties to this
  output node.

So: RIN in series with the + input, RG from ground to the − input, RF from output
back to the − input, output = VOUT. No supply pins are shown in this schematic.

### Figure 7-6 (board-layout diagram, lower figure, enclosed in a thin rectangular border)

Caption below the drawing: **Figure 7-6. Operational Amplifier Board Layout for
Noninverting Configuration**

A PCB-layout style drawing: a large empty rectangle in the centre represents the
device package, with eight rectangular pin pads attached, four on the left edge
and four on the right edge.

**Pin pads on the left edge, top to bottom:**
1. **OUT1**
2. **IN1−**
3. **IN1+**
4. **VCC−**

**Pin pads on the right edge, top to bottom:**
1. **VCC+**
2. **OUT2**
3. **IN2−**
4. **IN2+**

**Left-hand external circuitry:**

- A dashed rectangle at the far left encloses two resistors and their two round
  terminal pads. The upper pad is labelled **GND** and connects through a
  zig-zag resistor labelled **RG** (label sits above/inside the dashed box) to a
  trace running right.
- The lower pad is labelled **VIN** and connects through a zig-zag resistor
  labelled **RIN** (label below it, inside the dashed box) to a trace running
  right into the **IN1+** pad.
- The RG trace runs right, turns up at a vertical trace, and joins the left end
  of resistor **RF**; the RG/RF node also feeds the **IN1−** pad. **RF**'s right
  end connects to the **OUT1** pad.
- An arrow points into the dashed input-resistor box from the callout
  **"Run the input traces as far away from the supply lines as possible"**
  (upper left).
- A callout **"Place components close to device and to each other to reduce
  parasitic errors"** (top centre) has two arrowheads: one pointing down-left at
  the RG resistor / dashed box, one pointing down at the **RF** resistor.

**Bottom-left external circuitry:**

- A small dashed box below the RIN box contains a capacitor symbol (two parallel
  plates) above a round pad labelled **GND**. The capacitor's top plate connects
  up to a horizontal trace that runs right into the **VCC−** pad.
- A second round pad on that same trace, to the right of the dashed capacitor
  box, is labelled **VS−** with the sub-label **"(or GND for single supply)"**.
- A callout at the lower left, **"Only needed for dual-supply operation"**, has
  an arrow pointing right at that dashed capacitor box.

**Right-hand external circuitry:**

- A round pad labelled **VS+** at the top right connects down and left into the
  **VCC+** pad.
- Below the VS+ node, a dashed box contains a capacitor symbol above a round pad
  labelled **GND**, connected in series from the VCC+/VS+ trace to GND (the
  bypass capacitor).
- A callout at the lower right, **"Use low-ESR, ceramic bypass capacitor"**, has
  an arrow pointing up-left at that dashed capacitor box.
- Text at the bottom right inside the border: **"Ground (GND) plane on another
  layer"**.

No component values, dimensions or numeric annotations appear in Figure 7-6 —
all labels are pin names, net names, reference designators (RF, RG, RIN) and the
callout sentences transcribed above.

---

Page furniture: header — part numbers **"NE5532, NE5532A, SA5532, SA5532A"**
(blue bold) with document number and date **"SLOS075K – NOVEMBER 1979 – REVISED
DECEMBER 2025"** beneath; Texas Instruments logo at top right with **www.ti.com**
under it; a horizontal rule below the header. Footer — page number **10** at
bottom left, italic blue link **"Submit Document Feedback"**, right-aligned
**"Copyright © 2025 Texas Instruments Incorporated"**, and a centred line
**"Product Folder Links: NE5532 NE5532A SA5532 SA5532A"** (the part numbers in
blue italic as links).
