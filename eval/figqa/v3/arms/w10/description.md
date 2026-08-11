# Visual descriptions — w10 (2 images, both from page 8)

Two grouped bar charts with error bars, drawn in the same style: white
background, no chart title, no x-axis title, no gridlines in the vertical
direction, light grey horizontal gridlines at each labelled y tick, a black
left spine and a black bottom spine, and black error bars with short horizontal
caps on top of every bar. Both use the same five x-axis categories, in this
left-to-right order: **Cov4, Cov6, Cov9, Cov12, Full**. Colours encode the
series and are given in the legend of each chart (blue = Total, green = ID,
orange/salmon = OOD).

Bar values below are read off the axis from the pixel geometry and are accurate
to roughly ±0.2 percentage points; error-bar limits are the positions of the cap
lines. Values are stated as "value (lower–upper)".

---

## p008-x663.png

**Figure (grouped bar chart with error bars).** 807 × 565 px.

- **Y axis title:** "Success rate (%)" (rotated, on the left).
- **Y axis:** labelled ticks at **0, 10, 20, 30, 40, 50**, with a light grey
  horizontal gridline at each. The axis line runs above the last label — the
  plotted range extends to about **56** at the top of the spine. Zero is the
  bottom spine; no bar is clipped.
- **X axis:** five category labels — **Cov4, Cov6, Cov9, Cov12, Full**. No
  x-axis title.
- **Legend** (upper right, inside the plot area, no frame), three entries in
  this order: **Total** (blue), **ID** (green), **OOD** (orange/salmon).
- Each group has **three bars, in the order Total, ID, OOD** (left to right).

| Group | Total (blue) | ID (green) | OOD (orange) |
|---|---|---|---|
| Cov4  | **14.0** (13.4–14.6) | **39.5** (36.2–42.6) | **1.1** (0.3–2.5) |
| Cov6  | **16.1** (13.0–19.4) | **33.4** (24.7–42.6) | **7.4** (5.4–9.5) |
| Cov9  | **22.2** (21.5–22.8) | **34.3** (33.4–35.4) | **16.0** (15.6–16.5) |
| Cov12 | **22.8** (20.2–25.5) | **31.5** (29.2–34.0) | **18.4** (15.5–21.3) |
| Full  | **37.3** (36.3–38.5) | **37.3** (36.3–38.5) | **37.3** (36.4–38.5) |

Points readable from the geometry:

- In the **Full** group all three bars are the **same height (≈37.3)** with the
  same error bars — they form a flat block, and this is the tallest Total bar
  and the tallest OOD bar in the chart.
- **ID is higher than Total, and Total higher than OOD, in every one of Cov4,
  Cov6, Cov9 and Cov12.**
- The **tallest bar in the chart is ID at Cov4 (≈39.5)**; the **shortest bar is
  OOD at Cov4 (≈1.1)**, barely above the axis. Cov4 therefore has the largest
  ID–OOD gap (≈38.4 points).
- The **largest error bars are on ID at Cov6** (24.7–42.6, a span of ≈17.9
  points) and on Total at Cov6 (13.0–19.4). The **smallest error bars are in the
  Cov9 group** (Total 21.5–22.8, ID 33.4–35.4, OOD 15.6–16.5).
- Total rises monotonically across Cov4 → Cov6 → Cov9 → Cov12 → Full
  (14.0, 16.1, 22.2, 22.8, 37.3). OOD also rises monotonically (1.1, 7.4, 16.0,
  18.4, 37.3). ID does **not** rise monotonically: it falls from 39.5 at Cov4 to
  33.4 at Cov6, recovers slightly to 34.3 at Cov9, falls to 31.5 at Cov12, then
  rises to 37.3 at Full.
- No bar reaches 50; nothing in the chart exceeds ≈42.6 including error bars.

---

## p008-x664.png

**Figure (grouped bar chart with error bars).** 809 × 565 px.

- **Y axis title:** "Wrong container rate (%)" (rotated, on the left).
- **Y axis:** labelled ticks at **0, 10, 20, 30, 40**, with a light grey
  horizontal gridline at each. The axis spine extends above the 40 label to
  about **50**.
- **X axis:** the same five category labels — **Cov4, Cov6, Cov9, Cov12,
  Full**. No x-axis title.
- **Legend** (upper right, inside the plot area, no frame), two entries in this
  order: **ID** (green), **OOD** (orange/salmon). **There is no "Total" series
  in this chart** — unlike p008-x663 it has only two bars per group, and the
  bars are correspondingly wider.
- Each group has **two bars, in the order ID, OOD** (left to right).

| Group | ID (green) | OOD (orange) |
|---|---|---|
| Cov4  | **4.4** (4.0–5.1) | **36.0** (34.2–37.5) |
| Cov6  | **6.2** (4.5–8.1) | **26.8** (24.8–29.0) |
| Cov9  | **3.2** (1.9–4.5) | **17.2** (15.7–18.9) |
| Cov12 | **8.4** (6.6–10.3) | **15.6** (10.9–20.4) |
| Full  | **8.3** (7.7–9.0) | **8.3** (7.7–9.0) |

Points readable from the geometry:

- **OOD exceeds ID in every group.** In the **Full** group the two bars are
  **equal (≈8.3 each)** with identical error bars, so the gap closes to zero
  there.
- **OOD falls monotonically** across the five groups: 36.0 → 26.8 → 17.2 →
  15.6 → 8.3. The **tallest bar in the chart is OOD at Cov4 (≈36.0)**.
- **ID does not fall monotonically**: 4.4 → 6.2 → 3.2 → 8.4 → 8.3. The
  **shortest bar in the chart is ID at Cov9 (≈3.2)**; the tallest ID bar is at
  Cov12 (≈8.4), essentially tied with Full (≈8.3).
- The **largest error bar is on OOD at Cov12** (10.9–20.4, a span of ≈9.5
  points); the **smallest is on ID at Cov4** (4.0–5.1, ≈1.1 points).
- The ID–OOD gap shrinks steadily: ≈31.6 at Cov4, ≈20.6 at Cov6, ≈14.0 at Cov9,
  ≈7.2 at Cov12, ≈0 at Full. At Cov12 the ID and OOD error bars overlap
  (ID upper 10.3 vs OOD lower 10.9 — just short of touching).
- No bar reaches 40.
