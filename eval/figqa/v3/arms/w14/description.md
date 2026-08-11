# Visual description — w14 (page 6)

Two images: a full-page render of page 6 of a Texas Instruments LM386 datasheet,
and a cropped high-resolution version of the first figure on that page.

---

## p006-render.png

Full page render. Body content first, page furniture last.

### Body

**6.6 Typical Characteristics**

The section contains eight small graphs laid out in a two-column, four-row grid.
All eight are monochrome line graphs reproduced from an older datasheet (coarse,
photocopied appearance with heavy black curves on a ruled grid). Each is
followed by a bold caption below it. Transcribed in reading order:

---

**Figure 6-1 (line graph).** Supply current versus supply voltage.
X axis: **SUPPLY VOLTAGE (VOLTS)**, linear, ticks at 4, 5, 6, 7, 8, 9, 10, 11,
12 (grid line at every tick).
Y axis: **SUPPLY CURRENT (mA)**, linear, ticks at 1, 2, 3, 4, 5, 6.
A single straight, slightly rising line: **≈3.5 mA at 4 V**, ≈3.65 mA at 5 V,
≈3.8 mA at 6 V, **≈4.0 mA at 7 V**, ≈4.1 mA at 8 V, ≈4.3 mA at 9 V, ≈4.45 mA at
10 V, ≈4.6 mA at 11 V, **≈4.75 mA at 12 V** (values read from the axis). No
legend, no in-plot annotations.
Caption: **Figure 6-1. Supply Current vs Supply Voltage**

---

**Figure 6-2 (line graph, log X).** Power supply rejection versus frequency.
X axis: **FREQUENCY (Hz)**, logarithmic, decade labels **10, 100, 1k, 10k,
100k** with log minor grid lines between decades.
Y axis: **POWER SUPPLY REJECTION (dB)**, linear, ticks 0, 10, 20, 30, 40, 50,
60.
In-plot conditions box (right of centre): **V_S = 6V**, **A_V = 26 dB**.
Five curves, each labelled in-plot by its bypass capacitor value:
- **C_B = 50 µF** — starts ≈35 dB at 10 Hz, rises to the **50 dB** plateau by
  ≈60–70 Hz and stays at 50 dB to 100 kHz.
- **10 µF** — starts ≈20 dB at 10 Hz, reaches the 50 dB plateau at ≈300 Hz.
- **1 µF** — starts ≈6 dB, rises through ≈30 dB at ≈600 Hz, reaching 50 dB at
  ≈3–4 kHz.
- **0.5 µF** — starts ≈6 dB, the right-most rolling curve, reaching 50 dB at
  ≈6–8 kHz.
- **NO BYPASS CAPACITOR** — a flat horizontal line at **≈6 dB** across the whole
  frequency range (labelled with that text in-plot at about the 10 dB gridline
  height).
All four capacitor curves converge on the same **50 dB** ceiling.
Caption: **Figure 6-2. Power Supply Rejection vs Frequency**

---

**Figure 6-3 (line graph).** Output voltage versus supply voltage.
X axis: **SUPPLY VOLTAGE (VOLTS)**, linear, ticks 4, 5, 6, 7, 8, 9, 10, 11, 12.
Y axis: **OUTPUT VOLTAGE (VOLTS PEAK-TO-PEAK)**, linear, ticks 0, 2, 4, 6, 8,
10.
Four curves, labelled in-plot by load resistance:
- **R_L = ∞** (label written "R_L = ∞" near the top of the steepest pair) —
  straight line from ≈2.8 V p-p at 4 V supply to **10 V p-p at 12 V** (it runs
  off the top of the plot at 12 V).
- **16** — just below R_L = ∞, from ≈2.6 V p-p at 4 V to ≈10 V p-p at 12 V.
- **8** — from ≈2.3 V p-p at 4 V, rising to ≈6.0 V p-p at 9 V and saturating at
  a plateau of **≈6.6 V p-p** from about 10.5 V supply onward.
- **4** — from ≈2.1 V p-p at 4 V, saturating early at a plateau of **≈3.6 V
  p-p** from about 9 V supply onward.
All four curves originate from roughly the same point (≈2.1–2.8 V p-p) at 4 V.
Caption: **Figure 6-3. Output Voltage vs Supply Voltage**

---

**Figure 6-4 (line graph, log X).** Voltage gain versus frequency.
X axis: **FREQUENCY (Hz)**, logarithmic, decade labels **100, 1k, 10k, 100k,
1M** with log minor grid lines.
Y axis: **VOLTAGE GAIN (dB)**, linear, ticks 0, 10, 20, 30, 40, 50, 60.
Two curves, labelled in-plot:
- **C_1–8 = 10 µF** — flat at **≈46 dB** from 100 Hz to ≈30 kHz, then rolls off,
  crossing ≈30 dB at ≈300 kHz and ending at **≈11–12 dB at 1 MHz**.
- **C_1–8 = 0** — flat at **≈26–27 dB** from 100 Hz to ≈100 kHz, then rolls off,
  ending at ≈11–12 dB at 1 MHz.
The two curves converge at ≈700 kHz–1 MHz. The 20 dB difference between the
plateaus corresponds to the gain-setting capacitor between pins 1 and 8.
Caption: **Figure 6-4. Voltage Gain vs Frequency**

---

**Figure 6-5 (line graph, log X).** Total harmonic distortion versus frequency.
X axis: **FREQUENCY (Hz)**, logarithmic, tick labels **20, 50, 100, 200, 500,
1k, 2k, 5k, 10k, 20k**.
Y axis: **TOTAL HARMONIC DISTORTION (%)**, linear, ticks 0, 0.2, 0.4, 0.6, 0.8,
1.0, 1.2, 1.4, 1.6, 1.8, 2.0.
In-plot conditions block (top left): **V_S = 6V**, **R_L = 8 Ω**, **P_OUT =
125 mW**, **A_V = 26 dB (C_1–8 = 0)**.
Single U-shaped curve: **≈0.5 % at 20 Hz**, ≈0.4 % at 50 Hz, ≈0.32 % at 100 Hz,
falling to a broad **minimum of ≈0.2 % between about 400 Hz and 1 kHz**, then
rising — ≈0.3 % at 2 kHz, ≈0.6 % at 5 kHz, ≈0.9–1.0 % at 10 kHz, and steeply to
**≈1.45–1.5 % at 20 kHz**.
Caption: **Figure 6-5. Total Harmonic Distortion vs Frequency**

---

**Figure 6-6 (line graph, log X).** Total harmonic distortion versus output
power.
X axis: **POWER OUT (WATTS)**, logarithmic, decade labels **0.001, 0.01, 0.1,
1.0** with log minor grid lines.
Y axis: **TOTAL HARMONIC DISTORTION (%)**, linear, ticks 0 through 10 in steps
of 1.
In-plot conditions block (top left): **V_S = 6V**, **R_L = 8 Ω**, **f = 1 kHz**.
Single curve: starts at **≈0.6 % at 0.001 W**, dips to a flat floor of
**≈0.25–0.3 %** from about 0.005 W to 0.15 W, then rises almost vertically —
crossing 1 % at ≈0.2 W, 3 % at ≈0.25 W, 5 % at ≈0.28 W — and hitting the top of
the plot (**10 %**) at **≈0.32–0.35 W**. Nothing is plotted beyond that point;
the curve terminates against the 10 % ceiling well short of the 1.0 W axis end.
Caption: **Figure 6-6. Total Harmonic Distortion vs Power Out**

---

**Figure 6-7 (line graph).** Device dissipation versus output power, low-supply
set.
X axis: **OUTPUT POWER (W)**, linear, ticks 0, 0.1, 0.2, 0.3, 0.4, 0.5.
Y axis: **DEVICE DISSIPATION (W)**, linear, ticks 0, 0.2, 0.4, 0.6, 0.8, 1.0,
1.2, 1.4, 1.6, 1.8, 2.0.
Three solid curves, each labelled in-plot with a leader line:
- **V_S = 12V** — the top curve; from ≈0.2 W dissipation at zero output, rising
  to ≈0.9 W at 0.1 W out, ≈1.1 W at 0.2 W out, and peaking at **≈1.25 W at
  ≈0.35 W output**, where it terminates in a dashed vertical drop.
- **V_S = 9V** — middle curve; from ≈0.15 W at zero output to ≈0.6 W at 0.1 W
  out, flattening to **≈0.82 W at ≈0.3 W output**, terminating in a dashed
  vertical drop.
- **V_S = 6V** — bottom curve; from ≈0.1 W at zero output, flattening to
  **≈0.42 W** from about 0.15 W output onward, terminating at ≈0.3 W output.
Two dashed lines cut across the family and are labelled at the right:
**3% THD LEVEL** (the left-hand dashed boundary, at roughly 0.30–0.36 W output)
and **10% THD LEVEL** (the right-hand dashed boundary, slightly further right).
Nothing is plotted beyond ≈0.4 W output even though the axis runs to 0.5 W.
Caption: **Figure 6-7. Device Dissipation vs Output Power**

---

**Figure 6-8 (line graph).** Device dissipation versus output power,
high-supply set (same quantity as 6-7 but a wider power range and an extra
supply curve).
X axis: **OUTPUT POWER (W)**, linear, ticks 0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6,
0.7, 0.8, 0.9, 1.0.
Y axis: **DEVICE DISSIPATION (W)**, linear, ticks 0, 0.2, 0.4, 0.6, 0.8, 1.0,
1.2, 1.4, 1.6, 1.8, 2.0.
Four solid curves, each labelled in-plot:
- **V_S = 16V** — top curve; rises steeply from ≈0.1 W at zero output through
  ≈0.9 W at 0.15 W out and ≈1.2 W at 0.35 W out, to a maximum of **≈1.49 W at
  ≈0.84 W output**, then a dashed vertical drop.
- **V_S = 12V** — from ≈0.1 W at zero output, flattening to a plateau of
  **≈0.84 W** across roughly 0.4–0.85 W output, then a dashed vertical drop at
  ≈0.85 W.
- **V_S = 9V** — flattening to **≈0.52–0.55 W**, running to ≈0.7 W output.
- **V_S = 6V** — the lowest curve, flattening to **≈0.22 W**.
Two long dashed lines run diagonally across the family and are labelled at the
right: **3% THD LEVEL** (lower/left label with a leader arrow pointing to the
lower dashed line) and **10% THD LEVEL** (upper/right label). The dashed
boundaries terminate each solid curve.
Caption: **Figure 6-8. Device Dissipation vs Output Power**

---

Page furniture: header — part number **LM386** (blue), document number
**SNAS545D – MAY 2004 – REVISED AUGUST 2023**, Texas Instruments logo (red state
outline mark) top right with **www.ti.com** beneath it, and a horizontal rule
under the header block. Footer — page number **6**, link text *Submit Document
Feedback* (blue italic), **Copyright © 2023 Texas Instruments Incorporated**,
and a centred line **Product Folder Links: LM386** (LM386 in blue).

---

## p006-x252.png

**Figure (line graph).** A cropped, enlarged rendering of Figure 6-1 from the
same page — the graph only, without its "Figure 6-1." caption. Same content as
described above, legible at higher resolution:

- X axis: **SUPPLY VOLTAGE (VOLTS)**, linear, labelled ticks at **4, 5, 6, 7, 8,
  9, 10, 11, 12**, one vertical grid line per tick.
- Y axis: **SUPPLY CURRENT (mA)**, linear, labelled ticks at **1, 2, 3, 4, 5,
  6**, one horizontal grid line per tick. The Y axis is truncated at the bottom
  — it starts at 1 mA, not 0.
- A single thick straight line, monotonically increasing with constant slope,
  spanning the full plot width: **≈3.5 mA at 4 V** on the left to **≈4.75 mA at
  12 V** on the right; it passes almost exactly through **4.0 mA at 7 V**.
  Slope ≈0.155 mA per volt over the range.
- No legend, no curve label, no conditions box, no title, no data-point markers.
  The curve occupies only the middle band of the plot (roughly 3.5–4.8 mA of a
  1–6 mA axis).
