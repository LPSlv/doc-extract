# Visual description — w12 (page 25)

Two oscilloscope screen captures from the same instrument and session. Both are
Teledyne LeCroy screenshots, 10 × 8 division graticule, white background, with
the same menu bar across the top: **File | Vertical | Timebase | Trigger |
Display | Cursors | Measure | Math | Analysis | Utilities | Support**. Both
carry the **TELEDYNE LECROY** wordmark in the bottom-left corner and a date/time
stamp in the bottom-right corner. Neither has a title or caption inside the
image.

Waveform-to-channel mapping is given by the colour of the on-screen annotation
labels, which match the trace colours.

---

## p025-x1133.png

**Figure (oscilloscope screenshot, 6 traces).** Turn-on / inrush waveform
capture. Date stamp: **8/15/2016 3:40:07 PM**.

### Setup boxes along the bottom

| Box | Coupling / mode | Scale | Offset or time base |
| --- | --- | --- | --- |
| C1 | DC1M | 10.0 V/div | 0 mV offset |
| C2 | DC1M | 10.0 V/div | 0 mV offset |
| C3 | FLT DC1M | 10.0 V/div | 0.0 mV ofst |
| C4 | BwL DC | 5.00 A/div | −20.000 A |
| M2 | (math/memory) | 5.00 V/div | 2.00 ms/div |
| M3 | (math/memory) | 20.0 V/div | 2.00 ms/div |

- **Timebase**: 0.00 ms; **2.00 ms/div**; 100 kS; 5 MS/s.
- **Trigger**: C4, DC; **Stop**; Edge; Positive; **750 mA**.
- Trigger-position marker (green triangle) sits at the centre of the screen, so
  screen centre = t = 0 and the window spans roughly −10 ms to +10 ms.

### Ground-reference markers (left edge)

C2 and C3 coincident at screen centre (0 div); **M3** at −2 div; **M2** at
−3 div; **C4** at −4 div. C1 has 0 mV offset, so its zero is also at centre.

### On-screen trace labels (with leader lines)

**VIN** (yellow/olive, C1), **GATE** (magenta, C2), **VOUT** (blue, C3),
**PGD** (pale lilac, M3), **TIMER** (dark red, M2), **CURRENT_IIN** (green, C4).

### Trace behaviour (values read off the graticule, so approximate)

- **VIN** (yellow, 10 V/div): perfectly flat at **+2.44 div ≈ 24.4 V** across
  the entire 20 ms window. No transition.
- **VOUT** (blue, 10 V/div): flat at 0 V until ≈ **−0.9 ms**, then an S-shaped
  rise — ≈0.2 V at −1 ms, ≈7.2 V at t = 0, ≈18.3 V at +1 ms — flattening at
  **≈24.2 V** from ≈ **+1.5 ms** onward. Final VOUT sits just below VIN.
- **GATE** (magenta, 10 V/div): 0 V until ≈ **−2.1 ms**, then a slow rise that
  is still climbing at the right edge: ≈1.2 V at −2 ms, ≈3.5 V at −1 ms,
  ≈10.6 V at t = 0, ≈22.0 V at +1 ms, ≈28.3 V at +2 ms, ≈29.5 V at +3 ms,
  ≈30.6 V at +4 ms, ≈32.9 V at +6 ms, ≈35.1 V at +8 ms, **≈36.4 V at the right
  edge**. GATE ends roughly 12 V above VIN (charge-pump gate drive).
- **CURRENT_IIN** (green, 5.00 A/div, −20.000 A offset → zero at −4 div):
  baseline ≈0.1 A. Steps up at ≈ **−1.1 ms** to ≈1.6 A, ≈2.35 A at t = 0,
  rising to a **peak of ≈5.0 A at ≈ +0.9 ms**, then falling back to ≈0.25 A by
  +2 ms and flat at baseline for the rest of the sweep. Single triangular
  inrush pulse; no second pulse.
- **TIMER** (dark red, M2, 5.00 V/div, zero at −3 div): starts **high at
  ≈3.9 V**, falls at ≈ **−3.2 ms** to ≈0.2–0.35 V, stays low through t = 0,
  then rises slightly to **≈1.1–1.2 V** by +1 ms and holds that level flat to
  the right edge.
- **PGD** (pale lilac, M3, 20.0 V/div, zero at −2 div): held **low at 0 V**
  until a single clean step at ≈ **+1.4 ms**, after which it is flat at
  **≈24.2 V** (i.e. pulled up to VOUT) to the right edge. PGD asserts *after*
  VOUT has finished rising.

---

## p025-x1139.png

**Figure (oscilloscope screenshot, 6 traces).** Same six signals, slower
timebase, capturing the whole start-up delay including the timer ramp. Date
stamp: **8/15/2016 3:59:55 PM**. A red **"Waiting for Trigger"** status flag is
shown at the bottom, left of the date.

### Setup boxes along the bottom

| Box | Coupling / mode | Scale | Offset or time base |
| --- | --- | --- | --- |
| C1 | DC1M | 10.0 V/div | 0 mV offset |
| C2 | DC1M | 5.00 V/div | −15.000 V |
| C3 | FLT DC1M | 10.0 V/div | 0.0 mV ofst |
| C4 | BwL DC | 5.00 A/div | −19.950 A |
| M2 | (math/memory) | 10.0 V/div | 20.0 ms/div |
| M3 | (math/memory) | 20.0 V/div | 20.0 ms/div |

- **Timebase**: 60.0 ms; **20.0 ms/div**; 100 kS; 500 kS/s.
- **Trigger**: C4, DC; **Norm.**; Edge; Positive; **750 mA**.
- Trigger-position marker (green triangle) sits **+3 divisions right of centre**
  (≈ +60 ms of pre-trigger view), so the window spans roughly −160 ms to +40 ms
  relative to the trigger. Times below are quoted relative to that marker.

### Ground-reference markers (left edge)

C1, C3 and M2 coincident at screen centre (0 div); **M3** at −2 div; **C2** at
−3 div (matching its −15.000 V offset at 5.00 V/div); **C4** at −4 div
(matching −19.950 A at 5.00 A/div).

### On-screen trace labels (with leader lines)

**GATE** (dark red, M2), **VIN** (yellow/olive, C1), **VOUT** (blue, C3),
**PGD** (pale lilac, M3), **TIMER** (magenta, C2), **CURRENT_IIN** (green, C4).
Note that GATE and TIMER have swapped colours/channels relative to the other
screenshot.

### Trace behaviour

- **VIN** (yellow, 10 V/div): 0 V for the first division of the sweep, then a
  fast step at ≈ **−138 ms** to **≈24.5 V**, flat for the remainder of the
  capture. This is the input supply being applied.
- **TIMER** (magenta, C2, 5.00 V/div, zero at −3 div): begins at 0 V, and from
  the moment VIN appears it ramps **linearly** upward for ≈145 ms:
  ≈0.75 V at −120 ms, ≈1.35 V at −100 ms, ≈1.85 V at −80 ms, ≈2.45 V at −60 ms,
  ≈2.95 V at −40 ms, ≈3.55 V at −20 ms, reaching a **peak of ≈4.0 V at ≈
  −5.6 ms**. It then **drops abruptly** to a minimum of ≈0.33 V at ≈ −2 ms,
  recovers to ≈1.24 V at ≈ +1 ms, and decays slowly to ≈0.7 V at the right
  edge. The ramp-and-dump is the dominant feature of this screenshot.
- **VOUT** (blue, 10 V/div): flat at 0 V for essentially the whole sweep, then a
  near-vertical rise starting ≈ **−1 ms** and reaching **≈24.2 V** by ≈ +2 ms,
  flat thereafter. Much faster than the VOUT rise in p025-x1133.
- **GATE** (dark red, M2, 10.0 V/div, zero at centre): 0 V for the whole sweep
  until ≈ **−2 ms**, then a ramp up to **≈36.0 V** by ≈ **+9 ms**, flat at
  36.0 V to the right edge.
- **CURRENT_IIN** (green, 5.00 A/div): flat at ≈0.1 A for the whole sweep except
  a single **narrow spike peaking at ≈3.8 A at ≈ +1 ms**, coincident with the
  VOUT edge. No sustained inrush plateau.
- **PGD** (pale lilac, M3, 20.0 V/div, zero at −2 div): low at 0 V for the whole
  sweep, single step up at ≈ **+1 ms** to **≈24.2 V**, flat to the right edge.

### Comparison of the two captures

Same signal set, two timescales. p025-x1133 (2 ms/div) shows a controlled,
slow VOUT ramp with a ≈5 A inrush pulse and a TIMER line that starts high and
falls; p025-x1139 (20 ms/div) shows VIN being applied first, a ≈145 ms linear
TIMER ramp to ≈4 V that then collapses, and only then a fast VOUT edge with a
narrow ≈3.8 A current spike. GATE reaches ≈36 V in both. PGD asserts to ≈24 V
after VOUT in both.
