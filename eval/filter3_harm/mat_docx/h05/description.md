Page from the Texas Instruments OPA192 / OPA2192 / OPA4192 data sheet (SBOS620E), section 8.3.1 "Input Protection Circuitry". Three figures.

## Figure 54 — schematic pair

Title beneath: "**Figure 54. OPA192 Input Protection Does Not Limit Differential Input Capability**". Two op-amp schematics side by side, each a large triangle pointing right.

**Left schematic.** Triangle labelled inside "**OPA192**". Supply pin `V+` enters the top of the triangle from above; `V−` leaves the bottom. Two inputs on the left: `V_IN+` (upper) and `V_IN−` (lower). Output on the right: `V_OUT`. A vertical double-headed arrow spans between the two input nodes, annotated "**36 V**". No protection devices are drawn across the inputs. Caption under this half: "OPA192 Provides Full 36-V Differential Input Range".

**Right schematic.** Unlabelled triangle, same pinning: `V+` top, `V−` bottom, inputs `V_IN+` (upper) and `V_IN−` (lower), output `V_OUT`. Across the two input nodes sit two anti-parallel (back-to-back) diodes drawn as a pair of solid triangles with bars, connected between the same two rails. A vertical double-headed arrow between the input nodes is annotated "**~0.7 V**". Caption under this half: "Conventional Input Protection Limits Differential Input Range".

## Figure 55 — three-block circuit diagram

Title beneath: "**Figure 55. Back-to-Back Diodes Create Settling Issues**". Three sections, each with a bold italic label underneath: "*Input Low Pass Filter*" (dashed enclosure), "*Simplified Mux Model*" (solid enclosure), "*Buffer Amplifier*".

**Input Low Pass Filter (dashed box, left).** Two identical RC branches.
- Upper branch: source labelled in green "**V_n = +10 V**" feeds a series resistor `R_FILT`; the node after it is labelled in green "**+10 V**"; a shunt capacitor `C_FILT` runs from that node to ground.
- Lower branch: source labelled in red "**V_n+1 = −10 V**" feeds a series resistor `R_FILT`; the node after it is labelled in red "**−10 V**"; a shunt capacitor `C_FILT` to ground. A red dashed arrow points downward through this branch's ground return.

**Simplified Mux Model (solid box, centre).** Two switch channels sharing a common drain.
- Upper channel: input terminal drawn as an open circle labelled `S_n`; a shunt capacitor `C_S` to ground; a series resistor `R_on_mux`; then a switch drawn *open*, annotated with an upward arrow and a circled "**1**".
- Lower channel: input terminal `S_n+1` (open circle); shunt `C_S` to ground; series `R_on_mux`; then a switch, annotated with a downward arrow and a circled "**2**".
- Both channels join at the right at a node marked with an open circle labelled `D`, which has a shunt capacitor `C_D` to ground.
- A red dashed current path runs from the lower filter branch, through the mux, up to node `D`; it is labelled in red "**I_diode_transient**".

**Buffer Amplifier (right).** Above the amplifier, a circled "**1**" over a green "**+10 V**", a dotted arrow pointing right, then a circled "**2**" over a red "**~−9.3 V**" — i.e. the state-1 → state-2 transition of the buffer input node. The amplifier is a right-pointing triangle with inputs `Vin−` (upper) and `Vin+` (lower) and output `Vout` at the apex; the output is tied back to `Vin−` (unity-gain buffer). Between `Vin−` and `Vin+` sit two anti-parallel diodes, with a vertical double-headed arrow annotated "**~0.7 V**". The `Vin+` node is additionally labelled in red "**−10 V**". The red dashed `I_diode_transient` path from node `D` enters at this input pair.

## Figure 56 — line chart

Title beneath: "**Figure 56. OPA192 Protection Circuit Maintains Fast-Settling Transient Response**".

- X-axis: "Time (µs)", 0 to 60, major ticks and gridlines every 5 (0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60).
- Y-axis: "Output Delta From Final Value (mV)", −100 to 100, ticks and gridlines every 20 (100, 80, 60, 40, 20, 0, −20, −40, −60, −80, −100).
- Two heavy black dashed horizontal lines at **+10 mV** and **−10 mV**, annotated in-plot "0.1% Settling = ±10 mV".

**Red trace** ("Standard Input Diode Structure Extends Settling Time", annotation with an arrow pointing to the trace at about t ≈ 14 µs): a near-vertical spike out of the top of the plot at t ≈ 3–4 µs, then a fall to a minimum of ≈ −92 mV at t ≈ 5 µs (read from axis); it recovers, crosses zero at t ≈ 12 µs (read from axis), overshoots to a peak of ≈ +29 mV at t ≈ 18–19 µs (read from axis), then decays slowly — re-entering the ±10 mV band at t ≈ 37 µs (read from axis) and approaching 0 by t ≈ 55–60 µs.

**Green trace** ("OPA192 Input Structure Offers Fast Settling", annotation with an arrow pointing to the trace at about t ≈ 21 µs): rises steeply from below −100 mV at t ≈ 2 µs, spikes to ≈ +12 mV at t ≈ 3.5 µs (read from axis), dips to ≈ −10 mV at t ≈ 4.5 µs, and from about t ≈ 5 µs onward stays inside the ±10 mV band, flattening to a small positive value near +2 mV and converging to 0.

Page furniture: header "OPA192, OPA2192, OPA4192" / "SBOS620E − DECEMBER 2013 − REVISED NOVEMBER 2015" / "www.ti.com" / Texas Instruments logo; footer "24", "Submit Documentation Feedback", "Copyright © 2013–2015, Texas Instruments Incorporated", "Product Folder Links: OPA192 OPA2192 OPA4192".
