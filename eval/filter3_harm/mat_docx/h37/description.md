**Masthead (top of page).** Texas Instruments logo, www.ti.com.

**Figure 8-11. Independent PWM High-Side and Low-Side Drivers** (schematic / block
diagram, upper half of page).

Device side (left): two input pins drawn as small square pads, `INHx` (upper) and
`INLx` (lower), each feeding a triangular buffer inside a rectangular block
captioned `Gate Driver`. The upper buffer is labelled `HS` and sits under the
supply label `VCP`; the lower buffer is labelled `LS` and sits under the supply
label `VGLS`. A ground symbol is drawn inside the block below the LS buffer.

Device pins on the right edge, top to bottom, each a square pad on a vertical
bus: `VDRAIN`, `GHx`, `SHx`, `GLx`, `SLx/SPx`.

Two V_DS overcurrent comparators are drawn as triangles with `+` and `−` inputs
and the label `V_DS` inside; one above the gate-driver block and one below it.
Each has its output arrow pointing left, and each output is annotated
`Disable` in red — i.e. both V_DS overcurrent monitors are disabled in this
configuration. The upper comparator's inputs tap the `VDRAIN` and `SHx` nets;
the lower comparator's inputs tap the `SHx` and `SLx/SPx` nets.

External circuit (right): a vertical supply rail labelled `VM` at the top right.
`VDRAIN` connects to the `VM` rail. Two N-channel MOSFETs with body diodes are
drawn inside grey boxes:

- High-side FET: gate from `GHx`, drain to the `VM`/`VDRAIN` node, source to
  `SHx`; from the source a vertical line runs down through a circle labelled
  `Load` to the `SLx/SPx` net and on to a ground symbol.
- Low-side FET: gate from `GLx`, drain fed from the `VM` rail through a second
  circle labelled `Load`, source down to the `SLx/SPx` net and to the same
  ground symbol.

So each half of the bridge drives its own load: high-side FET sourcing into a
load returned to ground, low-side FET sinking a load returned to VM.

**Figure 8-12. One High-Side Driver** (schematic, lower left).

Same device drawing as Figure 8-11: `INHx` and `INLx` input pads into `HS`
(under `VCP`) and `LS` (under `VGLS`) buffers inside the `Gate Driver` block with
its internal ground symbol; right-hand pads `VDRAIN`, `GHx`, `SHx`, `GLx`,
`SLx/SPx`; upper and lower `V_DS` comparators with `+`/`−` inputs and outputs
arrowed to the left. Here the comparator outputs carry **no** "Disable"
annotation — the V_DS monitors are in use.

A ground symbol at the far left is tied to the unused `INLx` input line.

External: `VM` rail at top right tied to `VDRAIN`. A single N-channel MOSFET
(body diode shown) in a grey box has its drain on the `VM`/`VDRAIN` node, gate
on `GHx`, source on `SHx`; the source runs down through a circle labelled `Load`
to the `SLx/SPx` net and to a ground symbol. `GLx` has no external connection.

**Figure 8-13. One Low-Side Driver** (schematic, lower right).

Identical device drawing and pin set to Figure 8-12 (`INHx`, `INLx`, `VCP`/`HS`,
`VGLS`/`LS`, `Gate Driver`, `VDRAIN`, `GHx`, `SHx`, `GLx`, `SLx/SPx`, two
un-annotated `V_DS` comparators). A ground symbol at the far left is tied to the
unused `INHx` input line.

External: `VM` rail at top right tied to `VDRAIN`. From the `VM` rail a circle
labelled `Load` feeds the drain of a single N-channel MOSFET (body diode shown,
grey box); its gate is on `GLx` and its source runs to the `SLx/SPx` net and down
to a ground symbol. `GHx` and `SHx` have no external connection.
