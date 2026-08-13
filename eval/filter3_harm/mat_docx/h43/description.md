**Masthead (top of page).** Texas Instruments logo, www.ti.com; device TCA9534,
document SCPS197D – SEPTEMBER 2014 – REVISED OCTOBER 2017.

**Equations (drawn/typeset objects in the body, in reading order).**

$$T_J = T_A + (\theta_{JA} \times P_d) \quad (1)$$

$$P_d \approx \left(I_{CC\_STATIC} \times V_{CC}\right) + \sum P_{d\_PORT\_L} + \sum P_{d\_PORT\_H} \quad (2)$$

$$P_{d\_PORT\_L} = \left(I_{OL} \times V_{OL}\right) \quad (3)$$

$$P_{d\_PORT\_H} = \left(I_{OH} \times \left(V_{CC} - V_{OH}\right)\right) \quad (4)$$

**Figure 34. High-Value Resistor in Parallel with LED** (circuit schematic,
bottom of page).

- A rectangular block on the left represents the TCA9534; two pin labels are
  printed inside it along its right edge: `V_CC` (upper) and `LEDx` (lower).
- A vertical wire runs from the top of the device block up to a horizontal
  supply rail. The rail ends at the right with a node dot and the label `V_CC`.
- From the `LEDx` pin a horizontal wire runs right to a lower node.
- Between the supply rail and that lower node, two components sit in parallel:
  - An LED, drawn as a diode symbol with two emission arrows, labelled `LED`;
    anode at the top (supply rail), cathode at the bottom (LEDx node).
  - A resistor, drawn as a zigzag, labelled `100 k`, connected from the same
    supply rail down to the same LEDx node.
- So the LED and the 100 kΩ resistor are in parallel, both from V_CC to the
  LEDx port pin, which sinks the LED current.

No axes or numeric scales; the only value on the drawing is `100 k`.

Page footer: "Copyright © 2014–2017, Texas Instruments Incorporated",
"Submit Documentation Feedback", page 25, "Product Folder Links: TCA9534".
