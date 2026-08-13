Page heading: "Typical Application". Two application schematics on this page, each with its own sub-heading.

## Figure 1 — IMON 3rd Order Thermal Compensation Application

Sub-heading above the figure: "IMON 3rd Order Thermal Compensation Application" / "(Thermal Compensation only IMON Function)".

**Type:** electronic schematic (application circuit) built around a grey rectangular IC block labelled **AOZ23655QI** in blue.

**IC pins as drawn.** Left side of the block, top to bottom: TON, VID0, VID1, VCC, AGND, PGOOD, EN/PFM, IMON, LL. Right side, top to bottom: IN, VOUT, BST, LX, ISEN_P, ISEN_N, RGND, PGND.

**Connections and components:**

- **RTON** — resistor from the TON pin up and over to the IN net (the wire loops over the top of the IC and ties to the IN/INPUT rail).
- **IN** — connects to the right-hand rail labelled "INPUT / 4V TO 28V" (drawn with an input arrow terminal). **C2, 44µF** from that rail to power ground.
- **VID0** and **VID1** — each driven from an input arrow terminal on the left. **R1, 100kΩ** pulls VID0's node to analog ground; **R2, 100kΩ** pulls VID1's node to analog ground.
- **VCC** — fed from a "5V" input arrow terminal. **R3, 100kΩ** and **C1, 4.7µF** are on this node; C1 returns to analog ground and R3's lower end goes to the PGOOD net.
- **AGND** — to analog ground.
- **PGOOD** — output arrow terminal labelled "POWER GOOD"; pulled up through R3 to the 5V/VCC node.
- **EN/PFM** — driven from an input arrow terminal.
- **BST** — **C4, 0.1µF** from BST to the LX node.
- **VOUT** — sense line routed right and then down to the OUTPUT node.
- **LX** — through **L1, 0.22µH** to the output node labelled "OUTPUT / 1.8V, 18A". **C3, 800µF** from the output to power ground.
- **Snubber / current-sense network across L1:** **R_SN** in series with **C_SN** connected from the LX side of the inductor to the output side. The junction between R_SN and C_SN feeds **ISEN_P**. **ISEN_N** connects through **R_CSN** to the output side of the inductor.
- **RGND** and **PGND** — both routed to the power-ground symbol at the output capacitor return.
- **IMON thermal-compensation network (this is what makes it "3rd order"):** from the IMON pin, **C5** to analog ground; **R_S** from the IMON node down to a junction; from that junction a parallel arrangement of **R_C** on one branch and, on the other branch, **R_S1** in series with **R_NTC(T)**; the network bottoms out at analog ground.
- **LL** — **R_LL** from the LL pin to analog ground, with **C6** in parallel across it.

**Legend inside the figure (ground symbol key):**

- ⏚ (bar/T symbol) = "POWER GROUND"
- ▽ (triangle symbol) = "ANALOG GROUND"

A pair of unlabelled ground symbols (one triangle, one bar) is also drawn below the IC block.

## Figure 2 — IMON 2nd Order Thermal Compensation Application

Sub-heading above the figure: "IMON 2nd Order Thermal Compensation Application" / "(Thermal Compensation both LL and IMON Function)".

**Type:** electronic schematic, same IC block **AOZ23655QI** with the same pin arrangement (left: TON, VID0, VID1, VCC, AGND, PGOOD, EN/PFM, IMON, LL; right: IN, VOUT, BST, LX, ISEN_P, ISEN_N, RGND, PGND).

Identical to Figure 1 in the following respects: RTON from TON to IN; "INPUT / 4V TO 28V" rail with **C2, 44µF**; **R1, 100kΩ** and **R2, 100kΩ** on VID0/VID1 (R1 and R2 are printed as "100k Ω" with a space in this second schematic); "5V" into VCC with **R3, 100kΩ** and **C1, 4.7µF**; "POWER GOOD" from PGOOD; EN/PFM input; **C4, 0.1µF** from BST to LX; **L1, 0.22µH** from LX to "OUTPUT / 1.8V, 18A"; **C3, 800µF** at the output; RGND/PGND to power ground; the same POWER GROUND / ANALOG GROUND legend.

**Differences from Figure 1:**

- **Simplified IMON network:** from the IMON pin, **C5** to analog ground with **R_S** in parallel, R_S returning to analog ground. There is no R_C / R_S1 / R_NTC(T) branch on IMON.
- **LL network:** **R_LL** from LL to analog ground with **C6** in parallel — same as Figure 1.
- **Thermal compensation moved into the current-sense network:** across the inductor, **R_SN** in series with **C_SN** as before, but the ISEN_P branch now runs through **R_CSP** in series with **R_NTC(T)**, with **R_CSX** as an additional element between that node and the output side; **ISEN_N** connects via **R_CSN** into the same network. (The NTC thermistor sits in the ISEN divider here rather than on IMON.)

Page furniture: Alpha & Omega Semiconductor logo; header "AOZ23655QI"; footer "Rev. 1.1 May 2023", "www.aosmd.com", "Page 2 of 21".
