Texas Instruments **OPA192, OPA2192, OPA4192** datasheet page 14. Six characterisation
plots in a 2-column x 3-row grid inside a single ruled box, under the heading
"**Typical Characteristics (continued)**" with the conditions line "At T$_A$ = 25°C,
V$_S$ = ±18 V, V$_{CM}$ = V$_S$ / 2, R$_{LOAD}$ = 10 kΩ connected to V$_S$ / 2, and
C$_L$ = 100 pF, unless otherwise noted."

A general note on the four histograms: they are drawn with bins narrower than the
axis-label spacing, and at this render resolution only the modal bar height can be read
with confidence. Non-modal heights below are approximations from the gridlines and
should be treated as ±3–5 percentage points.

## Figure 7. Offset Voltage Drift Distribution from −40°C to +125°C

Vertical bar histogram, solid blue bars, gridded plot box.
Y: "Amplifiers (%)", 0 to 70, ticks every 10.
X: "Offset Voltage Drift (µV/°C)", −0.8 to 0.8, rotated tick labels every 0.1
(−0.8, −0.7, −0.6, −0.5, −0.4, −0.3, −0.2, −0.1, 0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6,
0.7, 0.8).
In-plot annotation, upper left: "**Distribution Taken From 120 Amplifiers / SOIC,
T$_A$ = −40°C to +125°C**".
Sub-caption between plot and figure title: "**OPA192ID and OPA2192ID**".
Distribution: a single narrow cluster of roughly seven or eight bars spanning about
−0.25 to +0.3 µV/°C, with nothing outside that range. The modal bar reaches **≈50%**
just above 0 µV/°C (read from axis); the bar adjacent to it on the left ≈30%, further
bars ≈20–23%, and the outermost bars ≈3–5%.

## Figure 8. Offset Voltage Drift Distribution from −40°C to +125°C

Vertical bar histogram, solid blue bars.
Y: "Amplifiers (%)", 0 to 50, ticks every 10.
X: "Offset Voltage Drift (µV/°C)", −1.1 to 1.1, rotated tick labels every 0.2
(−1.1, −0.9, −0.7, −0.5, −0.3, −0.1, 0.1, 0.3, 0.5, 0.7, 0.9, 1.1).
In-plot annotation, upper left: "**Distribution Taken From 75 Amplifiers / SOT and
VSSOP, T$_A$ = −40°C to +125°C**".
Sub-caption: "**OPA192IDBV, OPA192IDGK, OPA2192IDGK, and OPA4192IPW**".
Distribution: cluster spanning roughly −0.5 to +0.6 µV/°C. Modal bar **≈40%** near
−0.1 µV/°C (read from axis), with the next bar ≈32%, then ≈20%, ≈10%, and tail bars
≈2–4%. Wider than Figure 7, consistent with the smaller sample and the SOT/VSSOP
packages.

## Figure 9. Offset Voltage Drift Distribution from 0°C to 85°C

Vertical bar histogram, solid blue bars.
Y: "Amplifiers (%)", 0 to 70, ticks every 10.
X: "Offset Voltage Drift (µV/°C)", −0.5 to 0.5, rotated tick labels every 0.1
(−0.5, −0.4, −0.3, −0.2, −0.1, 0, 0.1, 0.2, 0.3, 0.4, 0.5).
In-plot annotation, upper left: "**Distribution Taken From 120 Amplifiers / SOIC,
T$_A$ = 0°C to 85°C**".
Sub-caption: "**OPA192ID and OPA2192ID**".
Distribution: cluster spanning roughly −0.25 to +0.35 µV/°C, modal bar **≈48%** near
+0.1 µV/°C (read from axis), flanked by bars of ≈30–35% and then ≈10–19%, with small
tail bars ≈3%.

## Figure 10. Offset Voltage Drift Distribution from 0°C to 85°C

Vertical bar histogram, solid blue bars.
Y: "Amplifiers (%)", 0 to 30, ticks every 5.
X: "Offset Voltage Drift (µV/°C)", −0.8 to 0.8, rotated tick labels every 0.2
(−0.8, −0.6, −0.4, −0.2, 0, 0.2, 0.4, 0.6, 0.8; intermediate 0.1-step labels are also
present but not individually resolvable).
In-plot annotation, upper left: "**Distribution Taken From 75 Amplifiers / SOT and
VSSOP, T$_A$ = 0°C to 85°C**".
Sub-caption: "**OPA192IDBV, OPA192IDGK, OPA2192IDGK, and OPA4192IPW**".
Distribution: broader and flatter than the others; roughly a dozen bars spanning about
−0.45 to +0.5 µV/°C. Two bars share the mode at **≈20%** around 0 to +0.1 µV/°C (read
from axis), with neighbours ≈12–15% and tails ≈4–8%.

## Figure 11. Offset Voltage vs Temperature

Multi-trace line chart (spaghetti plot), many overlaid coloured traces (black, red,
green, blue, magenta and others — colour here identifies individual units, not a
variable).
Y: "V$_{OS}$ (µV)", −100 to 100, ticks every 25 (−100, −75, −50, −25, 0, 25, 50, 75,
100).
X: "Temperature (°C)", −75 to 150, ticks every 25 (−75, −50, −25, 0, 25, 50, 75, 100,
125, 150).
In-plot annotation, upper left: "**190 Typical Units Shown**".
Shape: all traces are pinched into a narrow waist near room temperature (roughly
+25 °C to +30 °C, where the spread is only about ±10 µV) and fan out symmetrically in
both directions, forming a bow-tie. At the extremes of the plotted data (about −50 °C
and about +125 °C) the envelope reaches roughly ±50 µV, with the widest individual
traces touching about −60 µV and +55 µV (read from axis). No data is drawn beyond
about −55 °C or +130 °C, although the axis extends to −75 °C and 150 °C.

## Figure 12. Offset Voltage vs Common-Mode Voltage

Multi-trace line chart, five overlaid coloured traces (cyan, red, magenta, blue,
black — colour identifies individual units).
Y: "V$_{OS}$ (µV)", −50 to 50, ticks every 25 (−50, −25, 0, 25, 50).
X: "V$_{CM}$ (V)", −20 to 20, ticks every 5 (−20, −15, −10, −5, 0, 5, 10, 15, 20).
In-plot annotation, upper right: "**5 Typical Units Shown**".
Callout with an arrow pointing down-left to the left end of the traces, at about
V$_{CM}$ = −18 V: "**V$_{CM}$ = −18.1 V**".
Shape: all five traces are essentially flat and tightly bunched within about ±5 µV
across the range roughly −18 V to +15 V, with a small upturn/downturn at the extreme
left end near −18 V where the callout points, and a slight rise at the right-hand end
near +15 V (read from axis). No data is drawn beyond about ±16–18 V even though the
axis runs to ±20 V.

Page furniture: TI logo, "OPA192, OPA2192, OPA4192", "SBOS620E − DECEMBER 2013 −
REVISED NOVEMBER 2015", "www.ti.com"; footer page 14, "Submit Documentation Feedback",
"Copyright © 2013–2015, Texas Instruments Incorporated", "Product Folder Links: OPA192
OPA2192 OPA4192".
