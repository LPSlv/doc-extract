**Figure (schematic timing diagram, three stacked panels).** Sensor current and
sampling activity over time for three operating modes. Each panel has its own
horizontal time axis, drawn as a black arrow pointing right and labelled `t` at
its right-hand end. There is no vertical axis, no numeric scale on either axis,
no title and no legend; all quantities are qualitative.

Panel 1 (top) — row label **"Low Power Mode"** at the left. A red trace labelled
**"current"** (red text sitting just above the trace at the left, before the
first pulse) runs along a low flat baseline and rises into **four** tall,
narrow, bell-shaped pulses. The trace returns to the same low baseline between
pulses and ends flat at the right edge. The four pulses are evenly spaced. Each
pulse coincides with a pair of adjacent vertical blocks: a **grey block labelled
"settling"** immediately followed by a **blue block labelled "sampling"** (both
labels are rotated 90°, reading bottom-to-top inside the block). There are four
settling+sampling pairs. The blocks run from the time axis upward; the current
pulse peaks reach approximately the top of the blocks.

Panel 2 (middle) — row label **"Normal Mode"**. The red trace here is a
**flat, constant horizontal line** spanning the full width of the panel (it
extends a little to the left of the first block and a little to the right of the
last block); it has no pulses. There are **four blue "sampling" blocks**, at the
same four horizontal positions and the same spacing and width as the sampling
blocks in panel 1. **No grey "settling" blocks appear in this panel.** The
constant red line crosses each block partway up.

Panel 3 (bottom) — row label **"Normal Mode – higher ODR"** (two lines). The red
trace is again a **flat constant horizontal line** at the same relative height,
spanning the full panel width. Here the blue "sampling" blocks are **contiguous:
23 blocks of the same individual width as in panels 1 and 2, separated only by
thin white hairlines**, forming an unbroken band. Every block carries the
rotated label "sampling". The band begins at the same horizontal position as the
first sampling block of the panels above and continues to just past the position
of the last sampling block above. **No grey "settling" blocks appear in this
panel either.**

Contrast encoded by the drawing: current is pulsed (low baseline with peaks) only
in Low Power Mode, and constant in both Normal Mode panels; a settling interval
precedes every sample only in Low Power Mode; sample spacing goes from four
widely separated samples (panels 1 and 2) to back-to-back sampling (panel 3,
higher ODR), with sample duration unchanged.
