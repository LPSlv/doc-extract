**Figure set (three rasters, p2).** Two of the three rasters (`p002-x32.png` and `p002-x33.png`) are the same composite figure: `x33` is the colour artwork and `x32` is its black-and-white transparency mask, at effectively the same size (563-564 x 366-367 px). The third (`p002-x34.png`, 594 x 312 px) is an unrelated electronic block diagram.

---

## p002-x32.png

**Alpha/transparency mask (binary stencil), 563 x 366 px.** Not a chart. Pure black-and-white: white marks the opaque areas of the composite figure in `p002-x33.png`, black marks the transparent areas. About 57 % of the frame is white. There is no data, no axis, no plot.

Geometry, as fractions of the frame (x from left, y from top):

- A small isolated white rectangle at approximately x 0.10-0.20, y 0.09-0.18 — the footprint of the "Supporting electronics" callout box in the colour version.
- A large white block in the left third, roughly x 0.04-0.29 spanning y 0.18 down to about y 0.68, with a wider shelf x 0.04-0.38 across y 0.18-0.36 — the skull panel.
- A white block in the top centre, roughly x 0.38-0.71, y 0.04-0.45 — the prosthetic-arm illustration panel.
- A white block in the lower right, roughly x 0.45-0.82, y 0.45-0.90, cut by a thin vertical black line at about x 0.52 — the head-in-profile line-drawing panel and the adjacent rendered-head panel.
- A white block low centre-left, roughly x 0.22-0.52, y 0.68-0.90 — the rendered flesh-coloured head panel.
- The right-hand strip (x > 0.82) and the bottom band (y > 0.90) are black.

Text does render in the mask, white-on-black, and is legible:

- "BMI connectivity to" — top centre, clipped by the upper edge of the frame (the second line, "prosthetic arm", falls inside a white block and so is not visible in the mask).
- "Exte…" / "Unit" — left edge, at about y 0.20-0.24; the tail of "External Unit".
- "…it" — at about x 0.55, y 0.20; the tail of "Implant Unit".
- "Reader/Powering" — right side, at about y 0.45, preceded by a short white dash (the leader line).
- "Implant unit" — right side, at about y 0.59.
- "Microelectrode array" (two lines) — right side, at about y 0.71-0.77, preceded by a short white dash.

## p002-x33.png

**Composite illustration (four sub-panels, photographic renders plus line art), 564 x 367 px.** Subject: an implanted brain-machine-interface (BMI) device. White background, no frame, no axes, no numbers anywhere in the image.

**Sub-panel 1 — top left (roughly x 0.02-0.38, y 0.05-0.68): 3-D CT-style render of a human skull**, grey/bone coloured, seen in three-quarter profile facing right, with the mandible and teeth visible. On the crown of the skull sits a disc-shaped implanted device: a dark ring with a gold/bronze concentric patterned face on top, and a blue cylindrical body below it seated into the bone.
Labels on this panel:
- A blue-filled rectangular callout box at the top reading **"Supporting electronics"** in white text, with a **blue double-headed vertical arrow** running from the box down to the device on the skull.
- **"External Unit"** (two lines, black text) at the far left, with a thin blue curved arrow pointing right to the upper, gold/dark ring part of the disc.
- **"Implant Unit"** (black text) at the upper right of the panel, with a thin blue curved arrow pointing left/down to the blue lower part of the disc.

**Sub-panel 2 — lower centre (roughly x 0.24-0.52, y 0.46-0.90): 3-D render of the same head with the skin surface on**, flesh/tan coloured, bald, seen in right profile facing right, ear and facial features visible, neck cut off at the base. The same dark disc device is visible on the top of the head, partly protruding through the scalp. No labels on this panel.

**Sub-panel 3 — top right (roughly x 0.38-0.72, y 0.02-0.45): colour anatomical illustration** titled in bold black text above it, **"BMI connectivity to prosthetic arm"** (two lines). It shows a human torso and head from behind/three-quarter rear. A grey metallic **robotic prosthetic arm** is attached at the left shoulder, bent at the elbow, hand and fingers drawn at the upper left. The head is cut away to expose the **pink brain**; teal/green and beige segmented shell pieces sit over the skull; two small black connector/electrode blocks sit on the brain surface. **Red and blue wire pathways** (drawn as zig-zag red and smooth blue lines with small arrowheads) run from the connectors at the back of the head, down the neck, along the exposed **red spinal column**, and forward across the shoulder into the prosthetic arm.

**Sub-panel 4 — lower right (roughly x 0.52-0.82, y 0.46-0.90): black-and-white line drawing** of a human head in left profile (facing left), with the outline of the brain and its gyri drawn inside. Across the top of the skull lies a **black-and-white segmented band** (alternating black and white blocks, like a coil/antenna strip) with a small black arrowhead at each end. Inside the brain are two **orange rectangular blocks** near the top and two **yellow/gold rectangular blocks** slightly deeper and lower. Three black dashed leader lines run from the drawing to labels at the right:
- **"Reader/Powering"** — points to the segmented band on the scalp.
- **"Implant unit"** — points to the orange block just under the skull.
- **"Microelectrode array"** (two lines) — points to the deeper yellow/orange elements inside the brain.

## p002-x34.png

**Block diagram (system architecture), 594 x 312 px.** White background. Two large rounded rectangles drawn in **black dash-dot outline** sit side by side and represent the two halves of a wireless link; a labelled arrow across the gap between them represents the wireless channel.

**Top / channel:** bold black text **"NFC ISO 15693"** centred at the top of the figure ("NFC" in heavy bold, "ISO 15693" slightly lighter). Directly beneath it a **blue horizontal double-headed arrow** spans the gap between the two dash-dot boxes.

**Left box** — caption in blue bold text at the bottom of the box, two lines: **"External WPT & Two-way C&C link Transceiver"**. Contents, left to right:
- Black label **"I/O"** at the far left, with a **blue double-headed horizontal arrow** entering the box.
- An **orange/amber filled square block labelled "MCU"** (bold black text).
- A **blue double-headed horizontal arrow** labelled **"SPI"** (bold black text above it).
- A tall **dark-blue filled rectangle labelled "NFC Reader"** (white text, two lines).
- To the right of that, a black-line resonant circuit: a **capacitor** (two parallel plates) drawn in parallel with a **coil / inductor** (a solenoid of about four loops) — the reader antenna.

**Right box** — caption in blue bold text at the bottom, two lines: **"Implanted Side WPT & Two-way C&C link Transceiver"**. Contents, left to right:
- A matching **coil / inductor** (about four loops) in parallel with a **capacitor** — the implant antenna, facing the left box's coil across the gap.
- A **black dashed rectangle** enclosing two stacked blocks: a **dark-blue rectangle labelled "SRAM"** (white bold text) on top, and a **green rectangle labelled "EEPROM"** (black bold text) below it.
- A **green double-headed horizontal arrow** labelled **"I2C"** (bold black text above it).
- A **light-blue filled rectangle labelled "MCU"** (bold black text), with a **blue double-headed arrow** exiting to the right, out of the box.

**Lower half of the right box** (drawn faint/greyed, beneath the blocks above):
- A wide **horizontal double-headed arrow with a left-to-right colour gradient** (blue at the left end, teal/green at the right end), running almost the full width of the box, with faint white capitals inside reading **"TRANSPARENT I2C MASTER CHANNEL"**.
- Below the arrow, at the left: grey text **"Data"** over a grey double-headed horizontal arrow, and beneath it grey text **"(Energy)"** over a grey single-headed arrow pointing right.
- The same pair repeated at the right of the box: **"Data"** with a grey double-headed arrow, and **"(Energy)"** with a grey right-pointing arrow.
- In the centre, two teal/green bold labels, each followed by a short grey right-pointing arrow: **"(Energy Harvesting)"** (upper) and **"Event Detection"** (lower). A thin grey bracket/L-shaped line links these two labels up to the dashed SRAM/EEPROM box above.

No numbers, axes, scales or units appear anywhere in the diagram; the only numeric string is the standard number "15693" in the title.
