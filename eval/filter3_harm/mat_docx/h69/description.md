**Page furniture (p21).** Texas Instruments logo top left with "www.ti.com"; right header "TLV2370, TLV2371, TLV2372 / TLV2373, TLV2374, TLV2375" and "SLOS270F – MARCH 2001 – REVISED AUGUST 2016". Footer: "Copyright © 2001–2016, Texas Instruments Incorporated", "Submit Documentation Feedback", page number 21, "Product Folder Links: TLV2370 TLV2371 TLV2372 TLV2373 TLV2374 TLV2375".

Two figures, side by side, at the top of the page; the rest of the page is blank.

---

## Figure 32. Shutdown Supply Current and Output Voltage vs Time

**Type.** Stacked time-domain oscilloscope-style plot — three panels sharing one X axis, on a fine square grid. Axis-break marks (double-tick "≈" symbols) appear on the vertical axes between panels.

**Shared X axis.** "Time (µs)", linear, −40 to 180, ticks every 20 (−40, −20, 0, 20, 40, 60, 80, 100, 120, 140, 160, 180).

**Test conditions (text block inside the top panel).**
- V<sub>DD</sub> = 15 V
- A<sub>V</sub> = 1
- R<sub>L</sub> = 2 kΩ
- C<sub>L</sub> = 10 pF
- V<sub>I</sub> = V<sub>DD</sub>/2
- T<sub>A</sub> = 25°C

**Panel 1 — Y: "Shutdown Pulse (V)", linear, 0 to 10, ticks every 2 (0, 2, 4, 6, 8, 10).** Trace labelled "SHDN" (with overbar, i.e. active-low shutdown). It sits flat at ~8 V (read from axis) from the left edge to t = 0, drops vertically to 0 V at t = 0, stays at 0 V until t ≈ 120 µs, then steps back up to ~8 V and holds to the right edge.

**Panel 2 — Y: "Output Voltage (V)", linear, −1.5 to 7.5, ticks every 1.5 (−1.5, 0, 1.5, 3, 4.5, 6, 7.5).** Trace labelled "V<sub>O</sub>" at its left end. Flat at ~7.2 V (read from axis, just below the 7.5 gridline) from the left edge until roughly t = 15 µs, then falls steeply to 0 V by about t = 20 µs; holds at 0 V until t ≈ 120 µs; then rises steeply back to ~7.2 V by about t = 125 µs and stays flat to the right edge.

**Panel 3 — Y: "Supply Current (mA/Ch)", linear, −0.25 to 1, ticks −0.25, 0, 0.25, 0.5, 0.75, 1.** Trace annotated "I<sub>DD(SHDN = 0)</sub>" (SHDN overbarred) with a leader arrow pointing at the trace near t ≈ 35 µs. Flat at ~0.8 mA/Ch (read from axis) from the left edge to t = 0; drops abruptly at t = 0 to ~0.5 mA/Ch; then decays gradually along a shallow downward slope to ~0.35 mA/Ch by t ≈ 33 µs; a small step down at t ≈ 35–38 µs to ~0.15 mA/Ch, where it stays flat until t ≈ 120 µs; then steps back up to ~0.8 mA/Ch (with a slight overshoot bump) and holds to the right edge.

---

## Figure 33. Shutdown Supply Current/output Voltage vs Time

**Type.** Same three-panel stacked time-domain plot on a fine grid, with axis-break marks between panels. This is the 5 V counterpart of Figure 32 on a much shorter time base.

**Shared X axis.** "Time (µs)", linear, −2 to 10, ticks every 1 (−2, −1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10).

**Test conditions (text block inside the top panel, right-hand side).**
- V<sub>DD</sub> = 5 V
- A<sub>V</sub> = 1
- R<sub>L</sub> = 2 kΩ
- C<sub>L</sub> = 10 pF
- V<sub>I</sub> = V<sub>DD</sub>/2
- T<sub>A</sub> = 25°C

**Panel 1 — Y: "Shutdown Pulse (V)", linear, 0 to 6, ticks every 1 (0, 1, 2, 3, 4, 5, 6).** Trace labelled "SHDN" (overbarred) at the top left. Flat at ~4.2 V (read from axis) from the left edge to t = 0, falls vertically to 0 V at t = 0, holds at 0 V until t ≈ 5.2 µs, then steps back to ~4.2 V and holds to the right edge.

**Panel 2 — Y: "Output Voltage (V)", linear, −1 to 3, ticks −1, −0.5, 0, 0.5, 1, 1.5, 2, 2.5.** Trace labelled "V<sub>O</sub>". Flat at ~2.5 V from the left edge until t ≈ 0.3 µs, then falls steeply, with a slightly rounded knee at the bottom, to about 0.05–0.1 V (read from axis) by t ≈ 1.3 µs; stays flat near 0 V until t ≈ 5.5 µs; then rises steeply back to ~2.5 V by about t ≈ 6.5 µs and holds flat to the right edge.

**Panel 3 — Y: "Supply Current (mA/Ch)", linear, −0.25 to 1, ticks −0.25, 0, 0.25, 0.5, 0.75, 1.** Trace annotated "I<sub>DD(SHDN = 0)</sub>" (SHDN overbarred) with a leader arrow pointing at the trace around t ≈ 1.5 µs. Flat at ~0.75 mA/Ch from the left edge to t = 0; drops sharply at t ≈ 0.3–0.6 µs to a shallow minimum of about 0.18 mA/Ch (read from axis); settles at ~0.22 mA/Ch and stays flat until t ≈ 5.5 µs; then rises back to ~0.75 mA/Ch by t ≈ 6 µs and holds flat to the right edge.
