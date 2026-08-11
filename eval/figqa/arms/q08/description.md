## p006-render.png

Full page render of a Diodes Incorporated datasheet page for the ZXCT1009
high-side current monitor. Body content is the tail of the "Application
Information" section (text, one graph, one PCB layout drawing) followed by the
"Ordering Information" table.

### Section: Application Information (cont.)

**Sub-heading:** "PCB trace shunt resistor for low cost solution"

Paragraph 1: "The figure below shows output characteristics of the device when
using a PCB resistive trace for a low cost solution in replacement for a
conventional shunt resistor. The graph shows the linear rise in voltage across the
resistor due to the PTC of the material and demonstrates how this rise in
resistance value over temperature compensates for the NTCof the device." (Printed
as "NTCof", no space.)

Paragraph 2: "The figure opposite shows a PCB layout suggestion. The resistor
section is 25mm x 0.25mm giving approximately 150mΩ using 1oz copper. The data for
the normalised graph was obtained using a 1A load current and a 100Ω output
resistor. An electronic version of the PCB layout is available through Diodes
applications group."

### Figure — PCB layout drawing (top right of the page)

**Figure (PCB layout / artwork drawing, tall rectangular board outline).** The
board silkscreen carries the part name **ZXCT1009** at the top. Four round
through-hole pads sit at the corners, each with its own label:

- **Vout** — upper left pad (label above the pad)
- **Vin** — upper right pad (label to the right of the pad)
- **GND** — lower left pad (label below the pad)
- **Load** — lower right pad (label to the right of the pad)

A straight vertical trace runs from the Vout pad down to the GND pad; part-way down
it passes through a two-terminal component footprint labelled **R_out** (label
printed vertically alongside it). A second straight vertical trace runs from the
Vin pad down to the Load pad. Between the two vertical traces, at mid height, is a
small three-terminal SOT23 device footprint (the ZXCT1009 itself). To the right of
the SOT23, connected into the Vin/Load trace, is the shunt resistor: a serpentine
(meandering, comb-like) copper trace of roughly six folds. At the bottom of the
board is the **ZETEX** logo.

Caption below the drawing: "Layout shows area of shunt resistor compared to SOT23
package. Not actual size."

### Figure — line graph (left of the page)

**Figure (line chart, three curves, no legend — curves labelled in place with
leader lines).**

- X axis: **"Temperature (°C)"**, linear, tick labels −40, −20, 0, 20, 40, 60, 80,
  100, 120, 140. Vertical gridlines at every tick and at the intermediate
  ten-degree points.
- Y axis: **"Normalised Voltage"** (rotated, on the left), tick labels **0.8, 1.0,
  1.2, 1.4**. Horizontal gridlines are drawn at each labelled value and at the
  intermediate 0.9, 1.1 and 1.3 levels. The plot box extends a little below 0.8 and
  a little above 1.4.

Three curves, all passing through Normalised Voltage = 1.0 at approximately 25 °C
(the normalisation point):

1. **"Voltage across Copper Sense Resistor"** — label at the top centre of the plot
   area, leader line running down-right to the curve at roughly 60–70 °C. This is
   the steepest, near-linear rising curve: ~0.76 at −40 °C, ~1.0 at 25 °C, ~1.10 at
   60 °C, ~1.24 at 100 °C, and ~1.42 at 140 °C (all read from the axis).
2. **"V_OUT with Copper Sense Resistor"** — label at the middle right of the plot
   area, leader line running up-left to the curve at about 100 °C. Rises less
   steeply, and is essentially coincident with curve 1 below about 25 °C: ~0.75 at
   −40 °C, ~1.0 at 25 °C, ~1.09 at 60 °C, ~1.16 at 100 °C, ~1.25 at 140 °C. The gap
   between curves 1 and 2 opens up progressively above room temperature.
3. **"V_OUT with Ideal Sense Resistor"** — label at the lower centre of the plot
   area, leader line running up-left to the curve at about 60 °C. This is the only
   falling curve: ~1.01 at −40 °C, essentially flat (~1.01) from −40 °C to about
   0 °C, then declining through 1.0 at 25 °C to ~0.95 at 60 °C, ~0.90 at 100 °C and
   ~0.82 at 140 °C.

Graph title, printed inside the figure below the x axis: **"Effect of Sense
Resistor Material on Temperature Performance"**. The same wording is repeated in
bold as a caption line beneath the figure: **"Effect of Sense Resistor Material on
Temperature Performance"**.

No numeric values are printed on the curves themselves; all readings above are
estimated from the gridlines.

### Section: Ordering Information

**Table (7 columns × 3 data rows).**

| Device | AEC-Q100 level | Reel Size | Tape Width | Quantity per Reel | Part Marking | Package |
| --- | --- | --- | --- | --- | --- | --- |
| ZXCT1009FTA | Grade 3 | 7" | 8mm | 3000 Units | 109 | SOT23 |
| ZXCT1009F-7 | None | 7" | 8mm | 3000 Units | 109 | SOT23 |
| ZXCT1009T8TA | None | 7" | 12mm | 1000 Units | ZXCT1009 | SM8 |

Page furniture: DIODES INCORPORATED logo at top left; top-right header "ZXCT1009"
over "HIGH-SIDE CURRENT MONITOR"; footer left "ZXCT1009 / Document number: DS33441
Rev. 12 - 2"; footer centre "6 of 8" over "www.diodes.com"; footer right "April
2011 / © Diodes Incorporated".
