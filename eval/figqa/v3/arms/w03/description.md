**Figure (block diagram / system architecture, p2).** A two-part wireless-power-and-communication link, drawn as two rounded dash-dot enclosures side by side, coupled through an inductive (transformer) link across the middle of the figure.

Top of figure, centred above the gap between the two enclosures: the label `NFC ISO 15693`, with a blue double-headed horizontal arrow directly beneath it spanning the gap between the two enclosures.

**Left enclosure — caption (blue text, inside the box at bottom left): `External WPT & Two-way C&C link Transceiver`.**
Signal chain, left to right:

- A blue double-headed arrow entering from outside on the far left, labelled `I/O`.
- An orange/yellow block labelled `MCU`.
- A blue double-headed arrow labelled `SPI`.
- A blue block labelled `NFC Reader` (text on two lines).
- To the right of the NFC Reader, a resonant tank drawn in black line art: a vertical capacitor symbol in parallel with a coil (inductor drawn as a multi-turn spiral), connected top and bottom by wires with junction dots.

**Coupling:** the left-hand coil faces a mirror-image coil at the left edge of the right enclosure, with an air gap between them (the two dash-dot enclosure borders pass between the coils).

**Right enclosure — caption (blue text, inside the box at bottom right): `Implanted Side WPT & Two-way C&C link Transceiver`.**
Contents, left to right:

- A mirrored resonant tank: coil in parallel with a vertical capacitor symbol, junction dots top and bottom.
- A dashed-outline rectangle grouping two stacked memory blocks: a blue block labelled `SRAM` (upper) and a green block labelled `EEPROM` (lower).
- A green double-headed arrow labelled `I2C` leaving the dashed group to the right.
- A light-blue/pale block labelled `MCU`.
- A blue double-headed arrow leaving the pale MCU to the right, exiting the enclosure (unlabelled).

**Faded/greyed sub-layer in the lower part of the right enclosure** (drawn in low-contrast grey and teal, all legible):

- A wide horizontal double-headed gradient arrow (blue on the left fading to teal on the right) spanning nearly the full width of the right enclosure, with the reversed-out label `TRANSPARENT I²C MASTER CHANNEL` running along it.
- Beneath the arrow, a bracket/leader line dropping from the dashed memory group to two teal labels, each followed by a small grey right-pointing arrow: `(Energy Harvesting)` (upper) and `Event Detection` (lower).
- Two identical grey label pairs flank these, one on the left side and one on the right side of the enclosure; each pair reads `Data` above a small grey double-headed arrow, and `(Energy)` above a small grey right-pointing arrow.

No numeric values, units, part numbers, axes or legend are present in the figure; the only alphanumeric strings are those transcribed above.
