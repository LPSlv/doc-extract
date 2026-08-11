## p007-render.png

Full page render of a Texas Instruments datasheet page. Body content is section 7,
"Parameter Measurement Information", containing four timing/circuit figures and
four lettered notes. Roughly the bottom half of the page is blank.

**Section heading:** "7 Parameter Measurement Information"

**Line under the heading:** "t_pd is the maximum between t_PLH and t_PHL"

### Figure 7-1. Load Circuit

**Figure (schematic).** A horizontal wire enters from the left, labelled at its
origin **"From Output Under Test"**, and terminates at a solid black dot labelled
**"Test Point"**. From that node a vertical wire runs down to a capacitor symbol,
and below the capacitor to a ground symbol. The capacitor is annotated
**C_L = 50 pF (see Note A)**.

Caption: "Figure 7-1. Load Circuit"

### Figure 7-2. Voltage Waveforms — Pulse Durations

**Figure (timing/waveform diagram, two traces).** Reference levels are drawn as
dashed lines at the right: **V_CC** (upper) and **0 V** (lower) for each trace.

- Upper trace, labelled **High-Level Pulse**: starts low at 0 V, ramps up to V_CC,
  holds, then ramps back down to 0 V. The **50%** point is marked with a tick on
  both the rising and the falling edge.
- Lower trace, labelled **Low-Level Pulse**: starts high at V_CC, ramps down to
  0 V, holds, then ramps back up to V_CC. The **50%** point is marked with a tick
  on both the falling and the rising edge.

A double-headed horizontal arrow between the two traces, spanning between the
vertical dashed reference lines dropped from the 50% crossings, is labelled
**t_W** (pulse duration).

Caption: "Figure 7-2. Voltage Waveforms Pulse Durations"

### Figure 7-3. Voltage Waveforms — Setup and Hold and Input Rise and Fall Times

**Figure (timing/waveform diagram, two traces).** Reference levels **V_CC**
(dashed) and **0 V** at the right of each trace.

- Upper trace, labelled **Reference Input**: low at 0 V, rises to V_CC, holds, then
  falls back to 0 V at the right. The **50%** point is ticked on the rising edge; a
  vertical dashed line drops from it.
- Lower trace, labelled **Data Input**: low, rises to V_CC, holds a plateau, then
  falls. On the rising edge the **10%**, **50%** and **90%** points are marked; on
  the falling edge **90%**, **50%** and **10%** are marked.

Between the two traces a pair of back-to-back double-headed arrows meeting at the
Reference Input 50% dashed line measures **t_su** (setup time, to the left of that
line, measured from the Data Input rising-edge 50% reference) and **t_h** (hold
time, to the right of that line, extending to the Data Input falling-edge 50%
reference).

Below the Data Input trace, two more double-headed arrows measure **t_r** (rise
time, between the 10% and 90% points of the rising edge) and **t_f** (fall time,
between the 90% and 10% points of the falling edge). Short arrows mark the 10%–50%
intervals at each edge.

Caption: "Figure 7-3. Voltage Waveforms Setup and Hold and Input Rise and Fall
Times"

### Figure 7-4. Voltage Waveforms — Propagation Delay and Output Transition Times

**Figure (timing/waveform diagram, three traces).**

- Top trace, labelled **Input**: rises from 0 V to **V_CC**, holds, then falls back
  to 0 V. **50%** is ticked on both the rising and falling edges, with vertical
  dashed lines dropped from each.
- Middle trace, labelled **In-Phase Output**: swings between **V_OL** (low
  reference, dashed) and **V_OH** (high reference, dashed). It starts at V_OL,
  rises to V_OH, holds, then falls back to V_OL. On its rising edge the **10%**,
  **50%** and **90%** points are marked; on its falling edge **90%**, **50%** and
  **10%** are marked.
- Bottom trace, labelled **Out-of-Phase Output**: also swings between **V_OL** and
  **V_OH** but inverted — starts at V_OH, falls to V_OL, holds, then rises back to
  V_OH. **90%**, **50%**, **10%** marked on the falling edge and **10%**, **50%**,
  **90%** on the rising edge.

Propagation-delay arrows, all referenced to the Input 50% crossings:

- Between Input and In-Phase Output: **t_PLH** measured from the Input rising-edge
  50% to the In-Phase Output's transition, and **t_PHL** measured from the Input
  falling-edge 50% to the In-Phase Output's transition.
- Between In-Phase Output and Out-of-Phase Output: **t_PHL** measured from the
  Input rising-edge 50%, and **t_PLH** measured from the Input falling-edge 50%
  (i.e. the labels are swapped relative to the in-phase output, because the output
  is inverted).

Transition-time arrows below each output trace: on the In-Phase Output, **t_r** on
the rising edge (10%–90%) and **t_f** on the falling edge (90%–10%); on the
Out-of-Phase Output, **t_f** on the falling edge and **t_r** on the rising edge.

Caption: "Figure 7-4. Voltage Waveforms Propagation Delay and Output Transition
Times"

### Notes below the figures

A. C_L includes probe and jig capacitance.

B. Phase relationships between waveforms were chosen arbitrarily. All input pulses
are supplied by generators having the following charactersitics: PRR ≤ 1 MHz,
Z_O = 50 Ω, t_r = 6 ns, t_f = 6 ns. (Printed as "charactersitics".)

C. For clock inputs, f_max is measured when the input duty cycle is 50%

D. The outputs are measured one at a time with one input transition per
measurement.

Page furniture: Texas Instruments logo and "www.ti.com" at top left; top-right
header "SN54HC174, SN74HC174" over "SCLS119E – DECEMBER 1982 – REVISED FEBRUARY
2022"; footer "Copyright © 2022 Texas Instruments Incorporated", "Submit Document
Feedback", page number 7, and "Product Folder Links: SN54HC174 SN74HC174".
