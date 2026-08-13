Texas Instruments **LM317** datasheet page 19. Two schematic figures plus five
displayed equations rendered as artwork.

## Figure 8-10. 1.25V to 20V Regulator Circuit With Minimum Program Current

**Type.** Circuit schematic (line art, black on white). Section 8.3.5.

**Topology.** Left to right:

- Terminal **V$_I$** at the far left feeds a horizontal wire into the **INPUT** pin on
  the left side of a rectangular block labelled "**LM317**" (label at the top inside
  the block). The block has three labelled pins: **INPUT** (left), **OUTPUT** (right),
  **ADJUST** (lower area of the block, wire leaving downward/leftward).
- **OUTPUT** runs right to a junction dot, and continues right to the output terminal
  **V$_O$**.
- From that junction a wire drops vertically into **R1**, a zig-zag resistor labelled
  "**R1 / 1.2 kΩ**".
- Below R1 is a junction dot. From this junction a wire runs left and up to the
  **ADJUST** pin — so ADJUST taps the R1/R2 divider node.
- Below the junction the divider continues through **R2**, drawn as a **potentiometer**
  (zig-zag resistor with a diagonal wiper arrow across it), labelled "**R2 / 20 kΩ**".
- The bottom of R2 goes to a **ground symbol** (three-bar earth).

**Equations on this page (rendered artwork), with the numbers as printed:**

$$V_{OUT} = V_{REF}\left(1 + \frac{R_2}{R_1}\right) \quad (4)$$

$$(R_1 + R_2)_{min} = V_O / I_{reg(min)} \quad (5)$$

(Equation (5) is set in a small italic face; the right-hand side renders as
"Vol$_{reg(min)}$" and is transcribed above as the engineering reading
$V_O/I_{reg(min)}$ — the slash and the "I" are not separately resolvable at this
render size.)

Cross-references in the preceding prose: "Equation 4, Equation 5, and Figure 8-10
illustrate this relationship."

## Figure 8-11. Battery-Charger Circuit

**Type.** Circuit schematic (line art). Section 8.3.6.

**Topology.** Left to right:

- Terminal **V$_I$** at the far left into the **INPUT** pin of the "**LM317**" block
  (same three-pin block: INPUT left, OUTPUT right, ADJUST below).
- **OUTPUT** runs right into a series resistor **R$_S$**, drawn horizontally at the
  top and labelled "**R$_S$ / 0.2 Ω**" (label above the symbol).
- After R$_S$ the wire continues right to a junction, then drops vertically.
- From that vertical drop, **R1** (zig-zag, labelled "**R1 / 240 Ω**") goes down to a
  junction dot; a wire from that junction runs left to the **ADJUST** pin.
- Below the junction, **R2** (zig-zag, labelled "**R2 / 2.4 kΩ**") continues down to a
  **ground symbol**.
- A further branch runs from the node after R$_S$ to the **right-hand side** of the
  schematic, where a **battery/cell symbol** (long-and-short parallel plates) sits in
  series to a ground symbol at the bottom — the cell being charged. A second
  plate-pair symbol appears on this right-hand branch at the level between R1 and R2;
  the two right-hand symbols are drawn small and their exact form (multi-cell battery
  versus battery plus capacitor) is not fully resolvable at this render size.

**Equations for this circuit (rendered artwork), numbers as printed:**

$$V_{OUT} = 1.25\ \mathrm{V} \times \left(1 + \frac{R2}{R1}\right) \quad (6)$$

$$I_{OUT}(\text{short}) = \frac{1.25\mathrm{V}}{RS} \quad (7)$$

$$\text{Output Impedance} = RS \times \left(1 + \frac{R2}{R1}\right) \quad (8)$$

Page furniture: TI logo, "www.ti.com", "LM317", "SLVS044Z − SEPTEMBER 1997 − REVISED
APRIL 2025"; footer "Copyright © 2025 Texas Instruments Incorporated", "Submit
Document Feedback", page 19, "Product Folder Links: LM317".
