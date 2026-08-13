**Masthead (top of page).** Texas Instruments logo, www.ti.com; device LMT01,
document SNIS189D – JUNE 2015 – REVISED JUNE 2018.

**Figure 23. LMT01 Output Transfer Function** (line chart, upper third of page).

- X axis: `LMT01 Junction Temperature (°C)`, −50 to 225, labelled ticks at
  −50, −25, 0, 25, 50, 75, 100, 125, 150, 175, 200, 225; vertical gridlines at
  every labelled tick.
- Y axis: `Pulse Count`, 0 to 4096, labelled ticks 0, 512, 1024, 1536, 2048,
  2560, 3072, 3584, 4096 (steps of 512); horizontal gridlines at every tick.
- Two straight, essentially coincident traces, no in-plot legend. Per the body
  text the blue line is the output transfer function from Equation 1 and the red
  line is the look-up table (LUT).
  - Red (LUT) trace: from about (−50 °C, ~25 counts) rising linearly to about
    (200 °C, ~3700 counts) where it stops (read from axis).
  - Blue (Equation 1) trace: same line, continuing to about (225 °C, 4096
    counts) at the top right corner (read from axis).
  - Slope is roughly 15 counts per °C (read from axis). The two lines are not
    separable at this scale; the surrounding text notes the LUT function is
    "truly not linear" although it appears linear here.

**Figure 24. LMT01 Typical Accuracy When Using First Order Equation
Equation 1 – 92 Typical Units Plotted at (VP – VN) = 2.15 V** (multi-trace line
chart / spaghetti plot, lower left).

- X axis: `LMT01 Junction Temperature (°C)`, −50 to 150, labelled ticks −50,
  −25, 0, 25, 50, 75, 100, 125, 150; vertical gridlines at each.
- Y axis: `Temperature Accuracy (°C)`, −1.0 to 3.0 in steps of 0.5 (−1.0, −0.5,
  0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0).
- About 92 overlapping traces in assorted colours forming a single narrow band,
  U-shaped: at −50 °C the band spans roughly +1.1 to +1.6 °C; it falls to a
  minimum of roughly +0.2 to +0.6 °C between about 25 °C and 75 °C; it rises
  again to roughly +0.9 to +1.4 °C at 150 °C (all read from axis). No trace
  crosses below 0 °C and none reaches 2.0 °C. No legend, no limit lines.

**Figure 25. LMT01 Accuracy Using Linear Interpolation of LUT Found In
Electrical Characteristics - TO-92/LPG Pulse Count to Temperature LUT – 92
typical units plotted at (VP – VN) = 2.15 V** (multi-trace line chart with limit
lines, lower right).

- X axis: `LMT01 Junction Temperature (°C)`, −50 to 150, labelled ticks −50,
  −25, 0, 25, 50, 75, 100, 125, 150.
- Y axis: `Temperature Accuracy (°C)`, −1.0 to 1.0 in steps of 0.2 (−1.0, −0.8,
  −0.6, −0.4, −0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0).
- Two heavy red step-like curves are annotated with arrows and text:
  `Max Limit` (upper) at about +0.7 °C at −50 °C, stepping down to about +0.6 °C
  across most of the range and to roughly +0.55…+0.6 °C at 125–150 °C; and
  `Min Limit` (lower), the mirror image, about −0.7 °C at −50 °C and about
  −0.6 °C over the mid range, easing to roughly −0.55 °C at the high end (read
  from axis).
- Between the limits, ~92 thin multicoloured traces form a band confined to
  roughly −0.3 to +0.3 °C, densest between −0.2 and +0.2 °C; all units lie
  inside the limit lines (read from axis).

Page footer: "Copyright © 2015–2018, Texas Instruments Incorporated",
"Submit Documentation Feedback", page 15, "Product Folder Links: LMT01".
