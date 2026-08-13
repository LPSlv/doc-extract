**Masthead (top of page).** Texas Instruments logo, www.ti.com; devices OPA189,
OPA2189, OPA4189; document SBOS830I – SEPTEMBER 2017 – REVISED OCTOBER 2021.

**Figure 8-5. Noise Performance of the OPAx189 and OPA211 in Unity-Gain Buffer
Configuration** (log–log line chart, single figure on the page).

- X axis: `Source Resistance, R_S (Ω)`, logarithmic, decade ticks labelled
  1, 10, 100, 1k, 10k, 100k, 1M, 10M; vertical gridlines at each decade.
- Y axis: `Voltage Noise Spectral Density, E_O (V/Hz^1/2)`, logarithmic, decade
  ticks labelled 0.1n, 1n, 10n, 100n, 1µ, 10µ; horizontal gridlines at each
  decade.
- Three traces:
  - `OPAx189` (red, labelled with a leader arrow at the left of the plot):
    flat at about 10 n up to roughly 1 kΩ, then rising along the resistor-noise
    asymptote, reaching roughly 100 n at ~100 kΩ and about 1–2 µ at 10 MΩ
    (read from axis).
  - `OPA211` (blue, labelled with a leader arrow at the top right): flat at
    about 1 n from 1 Ω to roughly 100 Ω, rising from about 1 kΩ, crossing the
    red OPAx189 curve at roughly 2–4 kΩ near 10 n, and reaching the top of the
    plot at about 10 µ at 10 MΩ (read from axis).
  - `Resistor Noise` (black dashed, labelled with a leader arrow at the lower
    centre): straight line of slope ½ on the log–log grid, from about 0.13 n at
    1 Ω through about 13 n at 10 kΩ to roughly 0.4–1 µ at 10 MΩ (read from
    axis). It forms the lower asymptote that both amplifier curves merge into.
- A vertical dotted line is drawn at about 3.6 kΩ, labelled `R_S = 3.6 kΩ` with
  a leader; this is the crossing point of the OPAx189 and OPA211 curves.
- Credit line beneath the plot: `Copyright © 2017, Texas Instruments
  Incorporated`.
- Note under the figure (text): R_S = 3.6 kΩ is the source impedance above which
  OPAx189 is a lower noise option than the OPA211.

No other figure appears on this page (Figure 8-6 is referenced in the text but
is not printed here).
