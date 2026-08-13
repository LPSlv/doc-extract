Two figures on this page. Section text (2.5.3 "Chip Power-up and Reset") and Table 2-9 are extractable text and are not reproduced here.

## Figure 2-2 — ESP32-H2 Power Scheme

Caption below the figure: "Figure 2-2. ESP32-H2 Power Scheme".

**Type:** block diagram. A large outer rectangle represents the chip. Power-supply pins are drawn as small filled black squares sitting on the top edge of that rectangle; power rails are drawn as thin pink/red lines running from the pins down to the blocks they supply.

**Supply pins along the top edge, left to right, with their labels above the chip boundary:**

- **VDDPST1/VDDPST2** (one pad symbol, shared label)
- **VDD3P3**
- **VBAT**
- **VDDA_PMU**

**Inner sub-block, upper area, labelled "Analog"** (a rectangle whose label sits at its lower left). It contains two boxes:

- **"LP Voltage Regulator"**
- **"Digital Voltage Regulator"**

The Analog rectangle also spans an empty right-hand region through which the VBAT rail passes to a small switch symbol (a short diagonal line between two contacts), drawn at the right inside the Analog block.

**Bottom row of consumer blocks, left to right:**

- **"LP IO"**
- **"LP System"**
- **"Digital System"**
- **"Digital IO"**
- **"GPIO12 / XTAL_32K_N / XTAL_32K_P"** (three lines of text in one box)

**Rail routing as drawn:**

- VDDPST1/VDDPST2 feeds, via a horizontal distribution line just under the chip's top edge, the **LP IO** block, the **LP Voltage Regulator**, the **Digital Voltage Regulator**, and **Digital IO**.
- The **LP Voltage Regulator** output runs down to **LP System**.
- The **Digital Voltage Regulator** output runs down to **Digital System**.
- **VDD3P3** runs down to the same distribution line feeding **Digital IO**.
- **VBAT** runs down and across to the switch symbol inside the Analog block.
- **VDDA_PMU** runs down to the **GPIO12 / XTAL_32K_N / XTAL_32K_P** block.

## Figure 2-3 — Visualization of Timing Parameters for Power-up and Reset

Caption below the figure: "Figure 2-3. Visualization of Timing Parameters for Power-up and Reset".

**Type:** timing/waveform diagram, two traces, no numeric axes.

**Row labels at the left (the signal names):**

- Upper trace: "VDDPST1/2, VDD3P3, VDDA_PMU, VBAT"
- Lower trace: "CHIP_EN"

**Level annotations on the traces:**

- "2.8 V" with a horizontal dashed reference line across the upper trace, marking the level at which the power rails are considered stable.
- "V_IL_nRST" (rendered small; reads as V with subscript "IL_nRST") with a horizontal dashed reference line across the lower trace, marking the CHIP_EN low-input threshold.

**Interval annotations, both drawn as horizontal double-headed arrows between vertical dashed cursors at the top of the figure:**

- **t_STBL** — the earlier interval. Its left cursor sits where the rising power-rail waveform crosses 2.8 V; its right cursor sits where the rising CHIP_EN waveform crosses V_IL_nRST.
- **t_RST** — the later interval. It spans the period during which CHIP_EN dips back below V_IL_nRST and returns above it.

**Waveform shapes:** the power-rail trace starts low, ramps up through 2.8 V, and stays high flat for the remainder of the diagram. The CHIP_EN trace starts low, ramps up after the rails are stable, holds a high plateau, then dips down through V_IL_nRST to a low plateau (the reset pulse), and finally ramps back up to a high plateau.

Page furniture: running head "2  Pins"; footer "Espressif Systems", page number "21", "ESP32-H2 Series Datasheet v1.3", link "Submit Documentation Feedback".
