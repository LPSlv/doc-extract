**Figure set (two oscilloscope screen captures, p11).** Two monochrome oscilloscope-style waveform captures of a single rectangular pulse, black trace on a white background, each enclosed in a solid black rectangular border and overlaid with a **dotted graticule**.

**Neither image contains any legible text.** There are no axis labels, no volts/div or time/div readouts, no channel markers, no trigger or cursor annotations, no title and no printed numbers of any kind in either capture. All quantities below are therefore expressed in **graticule divisions**, measured from the pixels.

Both panels share the same graticule: **10 horizontal divisions x 8 vertical divisions**, drawn as dotted lines, with the panel border as the outer edge. Horizontal division width ~59.3 px, vertical division height ~50.1 px. The vertical centre of the screen is the 4th horizontal dotted line from the top. In both captures the low (baseline) level sits **2 divisions below screen centre** and the high level sits **2 divisions above screen centre**, so both pulses have an amplitude of **exactly 4.0 divisions peak-to-peak**, using the full central half of the screen height.

The two differ in edge speed: `p011-x473.png` has near-vertical edges with pronounced overshoot/undershoot, while `p011-x486.png` has visibly sloped (ramped) edges with much smaller overshoot.

---

## p011-x473.png

**Oscilloscope trace, 596 x 403 px.** Single positive rectangular pulse, black trace, dotted graticule, solid black border.

Graticule (pixel positions): vertical dotted lines at x = 60, 120, 180, 239, 298, 357, 417, 476, 535 (9 interior lines -> 10 horizontal divisions); horizontal dotted lines at y = 50, 100, 150, 200, 250, 301, 351 (7 interior lines -> 8 vertical divisions). Plot interior runs x ~2-594, y ~1-402.

Levels:
- **Low / baseline level: y = 302 px**, sitting exactly on the 6th horizontal dotted line from the top, i.e. **2.0 divisions below screen centre**. The trace is flat at this level from the left edge to the rising edge, and again from the settled part of the falling edge to the right edge.
- **High level: y = 100 px**, sitting exactly on the 2nd horizontal dotted line from the top, i.e. **2.0 divisions above screen centre**.
- **Amplitude: 4.0 divisions.**

Rising edge:
- Located at x ~59-62 px, i.e. essentially **on the 1st vertical dotted line, 1.0 division from the left edge**.
- Effectively vertical — the transition occupies under 4 px (~0.07 division).
- **Overshoot spike** reaching y = 69 px, i.e. **0.62 division above the flat top** (about 15 % overshoot relative to the 4-division amplitude). The spike is narrow, only a few pixels wide.
- Damped ringing immediately after: the trace dips and recovers over x ~63-73 (roughly 0.17 division of time), touching about y = 107 (0.14 division below the flat top) before settling on the 100 px level.

Flat top:
- Held perfectly flat at y = 99-101 px from about x = 65 to x = 428, i.e. across roughly **6.1 divisions**.

Falling edge:
- Located at x ~429-435 px, i.e. **7.25 divisions from the left edge** (between the 7th vertical line at x = 417 and the 8th at x = 476).
- Also near-vertical, the transition spanning ~6 px (~0.1 division).
- **Undershoot** to y = 338 px, i.e. **0.72 division below the baseline** (about 18 % of amplitude), the deepest point at about x = 434.
- Damped ringing over x ~435-445: the trace comes back up to about y = 293 (slightly above baseline) at x = 438, then dips again to y = 305 near x = 443, and is settled on the 302 px baseline by about x = 446.

Pulse width measured between the two edges: **~6.25 divisions** (x = 60.5 to x = 431).

After settling, the baseline runs flat at y = 302 to the right-hand border. Nothing else is drawn in the frame.

## p011-x486.png

**Oscilloscope trace, 599 x 405 px.** Single positive pulse with sloped (trapezoidal) edges, black trace, dotted graticule, solid black border.

Graticule (pixel positions): vertical dotted lines at x = 60, 120, 180, 239, 299, 358, 418, 477, 537 (9 interior lines -> 10 horizontal divisions); horizontal dotted lines at y = 52, 102, 152, 202, 252, 302, 353 (7 interior lines -> 8 vertical divisions). Plot interior runs x ~2-596, y ~2-402.

Levels:
- **Low / baseline level: y = 299 px**, about 3 px above the 6th horizontal dotted line, i.e. **~2.05 divisions below screen centre**.
- **High level: y = 98 px**, about 4 px above the 2nd horizontal dotted line, i.e. **~2.08 divisions above screen centre**.
- **Amplitude: 201 px = 4.0 divisions.**

Left baseline:
- Flat at y = 298-300 from the left border to about x = 50 (~0.8 division of time).

Rising edge:
- A clean **linear ramp** from (x ~50, y ~299) up to (x ~97, y ~90). Rise duration ~47 px = **~0.79 division**, starting just before the 1st vertical dotted line and finishing about 0.6 division past it.
- Small **overshoot** at the top of the ramp: the trace peaks at y = 87 px, i.e. **~0.22 division above the flat top** (about 5 % of amplitude).
- Brief ringing between x ~93 and x ~110 (two small wiggles, y oscillating between about 87 and 105), settled on the 98 px level by about x = 109.

Flat top:
- Held flat at y = 97-99 px from about x = 100 to x = 418, i.e. across roughly **5.3 divisions**, reaching exactly to the 7th vertical dotted line.

Falling edge:
- A **linear ramp** starting at about (x = 419, y = 99), on the 7th vertical dotted line, and descending to the baseline at about (x = 452, y = 297). Fall duration ~33 px = **~0.56 division**, i.e. noticeably faster than the rise.
- **Undershoot** below the baseline to y = 323 px at about x = 458-460, i.e. **~0.48 division below baseline** (about 12 % of amplitude).
- Recovery: the trace rises back through the baseline around x = 464-467 and is settled at y = 298-300 by about x = 470.

Pulse width measured at the mid-points of the two ramps: **~6.1 divisions** (x ~73.5 to x ~436).

After settling, the baseline runs flat at y = 299 to the right-hand border. Nothing else is drawn in the frame.
