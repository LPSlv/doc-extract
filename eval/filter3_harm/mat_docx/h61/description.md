Page of *Typical Characteristics (continued)* for the TI OPA192 / OPA2192 / OPA4192
(SBOS620E). Six plots in a 2 × 3 grid. Conditions stated above the grid apply to all:
T_A = 25 °C, V_S = ±18 V, V_CM = V_S / 2, R_LOAD = 10 kΩ connected to V_S / 2,
C_L = 100 pF, unless otherwise noted.

**Figure 43 (line plot). Settling Time (5-V Negative Step).**
X: Time (µs), 0 to 1.8, ticks every 0.2. Y: Output Delta from Final Value (mV),
−4 to 4, gridlines every 1. Single blue trace plus two horizontal black dashed
lines at +0.5 mV and −0.5 mV.
In-plot annotations: "G = +1" (top right); "0.01% Settling = ±500 µV" (labelling the
dashed pair); "Step Applied at t = 0" (bottom right).
Trace: flat/off-scale until ≈0.2 µs, then two full-height vertical excursions that
run off both the top and bottom of the frame between ≈0.22 µs and ≈0.30 µs
(the step and its overshoot, clipped by the ±4 mV window); re-enters the frame from
the top at ≈0.38 µs, falls to a local minimum ≈1.65 mV at ≈0.42 µs, rises to a local
peak ≈2.0 mV at ≈0.47 µs, then decays monotonically: ≈1.2 mV at 0.6 µs,
≈0.75 mV at 0.8 µs, crossing the +0.5 mV band at ≈0.95–1.0 µs, ≈0.25 mV at 1.2 µs,
≈0.1 mV at 1.5 µs, ≈0.03 mV at 1.8 µs (all read from axis).

**Figure 44 (line plot). Short-Circuit Current vs Temperature.**
X: Temperature (°C), −75 to 150, ticks every 25. Y: I_SC (mA), 0 to 80, gridlines
every 20. Two red curves. Text inside the plot: "I_SC, Source" (upper-middle area)
and "I_SC, Sink" (left, near 60 mA). Neither label has a leader line; by proximity
"I_SC, Source" belongs to the upper curve and "I_SC, Sink" to the lower one.
Both curves start at ≈−55 °C (left of the plotted data; no data below −55 °C).
Upper curve: ≈78 mA at −55 °C, ≈73 at −25, ≈71 at 0, ≈69 at 25, ≈66 at 50,
≈65 at 75, then bends steeply down — ≈52 at 100, crossing the other curve at
≈107 °C / ≈47 mA, ≈25 at 125, reaching 0 mA at ≈138 °C.
Lower curve: ≈74 mA at −55 °C, ≈68 at −25, ≈65 at 0, ≈62 at 25, ≈58 at 50,
≈54 at 75, ≈48 at 100, ≈41 at 125, ≈25 at 150 °C (all read from axis).

**Figure 45 (line plot, log X). Maximum Output Voltage vs Frequency.**
X: Frequency (Hz), logarithmic, 10k to ≈20M, labelled decades 10k, 100k, 1M, 10M.
Y: Output Voltage (V_PP), 0 to 30, gridlines every 5. Three curves, each labelled
in-plot by supply rather than by a legend box:
- "V_S = ±15 V" — flat at 30 V_PP up to ≈200 kHz, then rolls off.
- "V_S = ±5 V" — flat at 10 V_PP up to ≈600 kHz, then rolls off.
- "V_S = ±2.25 V" — flat at 5 V_PP up to ≈1.2 MHz, then rolls off.
All three merge onto a common slew-rate-limited asymptote above ≈1.5 MHz and decay
together to ≈0.3 V_PP at the right edge (≈20 MHz). Callout with arrow pointing at the
knee of the ±15 V curve: "Maximum output voltage without slew-rate induced distortion."
(breakpoints read from axis).

**Figure 46 (oscilloscope-style trace). Propagation Delay Rising Edge.**
X: Time (200 ns/div), no numeric labels — 10 horizontal divisions.
Y: Output Voltage (5 V/div), no numeric labels — 8 vertical divisions; a heavy
horizontal centre line and a heavy vertical centre line mark the graticule origin.
Two traces: a red input trace that steps up sharply near the left of the frame and
stays high, and a blue V_OUT trace that stays low, begins to rise ≈2 divisions later
and ramps up to the same high level near the right of the frame.
Annotations: "Overdrive = 100 mV" with an arrow to the red rising edge;
"V_OUT Voltage" with an arrow to the blue ramp; a double-headed horizontal dimension
arrow spanning from the red edge to the blue trace's crossing of the centre line,
labelled "t_pLH = 0.97 µs".

**Figure 47 (oscilloscope-style trace). Propagation Delay Falling Edge.**
X: Time (200 ns/div), no numeric labels. Y: Output Voltage (1 V/div), no numeric
labels; heavy horizontal and vertical centre lines as above.
Two traces: a red input trace that steps sharply down near the left of the frame and
stays low, and a blue V_OUT trace that stays high, then falls with an S-shaped
transition and settles low near the right of the frame.
Annotations: "V_OUT Voltage" with an arrow to the blue falling edge;
"Overdrive = 100 mV" with an arrow to the red falling edge; a double-headed
horizontal dimension arrow from the red edge to the blue trace's crossing of the
centre line, labelled "t_pLH = 1.1 µs" (label reads t_pLH, not t_pHL, as printed).

**Figure 48 (line plot, log X). Crosstalk vs Frequency.**
X: Frequency (Hz), logarithmic, 1k to 1M, labelled decades 1k, 10k, 100k, 1M.
Y: Crosstalk (db) — axis caption printed with a lower-case "db" — −180 to −80,
gridlines every 20. Single noisy black trace, no legend, no test-condition box.
Values (read from axis): ≈−145 dB at 1 kHz; minimum ≈−149 dB at ≈1.8 kHz;
rising to ≈−138 dB at 10 kHz; a shallow plateau ≈−136 dB from ≈15 kHz to ≈30 kHz;
≈−134 dB at 40–60 kHz; ≈−130 dB at 100 kHz; then a steady rise to ≈−108 dB at 1 MHz.

Page furniture (not part of the figures): running head "OPA192, OPA2192, OPA4192",
"SBOS620E – DECEMBER 2013 – REVISED NOVEMBER 2015", Texas Instruments logo,
"www.ti.com"; footer page number 20, "Submit Documentation Feedback",
"Copyright © 2013–2015, Texas Instruments Incorporated",
"Product Folder Links: OPA192 OPA2192 OPA4192".
