**Masthead (top of page).** Texas Instruments logo; devices TPS63020, TPS63021;
document SLVS916I – JULY 2010 – REVISED OCTOBER 2019; www.ti.com.

Six line charts in a 2 × 3 ruled grid of typical-characteristics plots. All six
share a `Efficiency (%)` Y axis running 0 to 100 with labelled gridlines every
10. The four upper charts use a logarithmic `Output Current (A)` X axis with
labelled decades `100µ, 1m, 10m, 100m, 1, 4`; the two lower charts use a linear
`Input Voltage (V)` X axis labelled `1.8, 2.2, 2.6, 3, 3.4, 3.8, 4.2, 4.6, 5,
5.4`. Each chart carries a boxed condition label in its lower right corner. All
curve values below are read from the axes.

**Figure 8. Efficiency Versus Output Current, TPS63020, Power Save Enabled**
(top left). Boxed condition: `TPS63020, Power Save Enabled`. Legend (four
traces): `V_IN = 1.8V, V_OUT = 2.5V` (blue); `V_IN = 3.6V, V_OUT = 2.5V`
(black); `V_IN = 2.4V, V_OUT = 4.5V` (tan/yellow); `V_IN = 3.6V, V_OUT = 4.5V`
(teal).
- Blue (1.8 V → 2.5 V): ~69 % at 100 µA, ~82 % at 1 mA, flat ~84–85 % from
  10 mA to ~200 mA, peak ~86 % near 400 mA, falling to ~77 % where the trace
  ends at about 1 A.
- Black (3.6 V → 2.5 V): ~55 % at 100 µA, ~80 % at 1 mA, ~88–90 % from 10 mA to
  100 mA, peak ~93 % near 400 mA, ~90 % at 1 A, ~81 % at 4 A.
- Tan (2.4 V → 4.5 V): ~62 % at 100 µA, ~80 % at 1 mA, ~85–87 % mid-range, peak
  ~88 % near 300 mA, falling to ~72 % where the trace ends near 1.5 A.
- Teal (3.6 V → 4.5 V): ~66 % at 100 µA, ~82 % at 1 mA, ~90 % from 10 mA to
  100 mA, peak ~91–92 % near 500 mA, falling to ~80 % near 2 A where it ends.
- Only the black trace runs to the full 4 A; the other three stop short.

**Figure 9. Efficiency Versus Output Current, TPS63020, Power Save Disabled**
(top right). Boxed condition: `TPS63020, Power Save Disabled`. Same four-entry
legend as Figure 8.
- All four traces start near 1–2 % at 100 µA and rise monotonically in an
  S-curve: ~8–10 % at 1 mA, ~45–55 % at 10 mA, ~85–90 % at 100 mA.
- Peak ~93 % between roughly 500 mA and 1 A for the black and teal traces.
- Blue (1.8 V → 2.5 V) tops out at ~86 % near 200 mA and falls to ~73 % where it
  ends near 1 A; tan (2.4 V → 4.5 V) reaches ~92 % then falls to ~72 % near
  1.5 A; black runs to 4 A ending at ~82 %.

**Figure 10. Efficiency Versus Output Current, TPS63021, Power Save Enabled**
(middle left). Boxed condition: `TPS63021, Power Save Enabled`. Legend (two
traces): `V_IN = 2.4V` (blue); `V_IN = 3.6V` (black).
- Blue (2.4 V): ~67 % at 100 µA, ~82 % at 300 µA, ~87 % at 1 mA, flat
  ~89–90 % from 10 mA to ~200 mA, peak ~91 % near 500 mA, falling to ~72 %
  where it ends near 2 A.
- Black (3.6 V): ~68 % at 100 µA, ~85 % at 300 µA, ~90 % at 1 mA, ~93–95 % from
  10 mA to 200 mA with a small notch dip to ~92 % near 200 mA, peak ~95 % near
  700 mA, then falling to ~81 % at 4 A.

**Figure 11. Efficiency Versus Output Current, TPS63021, Power Save Disabled**
(middle right). Boxed condition: `TPS63021, Power Save Disabled`. Legend:
`V_IN = 2.4V` (blue); `V_IN = 3.6V` (black).
- Both start ~1–2 % at 100 µA. Blue rises earlier: ~8 % at 1 mA, ~45 % at
  10 mA, ~88 % at 100 mA, peak ~92 % near 300 mA, then falls to ~72 % where it
  ends near 2 A.
- Black: ~5 % at 1 mA, ~35 % at 10 mA, ~85 % at 100 mA, peak ~95 % between
  700 mA and 1 A, ~82 % at 4 A.

**Figure 12. Efficiency Versus Input Voltage, TPS63020, V_OUT = 2.5 V, Power
Save Enabled** (bottom left). X axis `Input Voltage (V)` 1.8–5.4. Boxed
condition: `TPS63020, V_OUT = 2.5V, Power Save Enabled`. Legend (four traces):
`I_OUT = 10mA` (blue); `I_OUT = 500mA` (black); `I_OUT = 1A` (tan);
`I_OUT = 2A` (teal).
- Blue (10 mA): ~84 % at 1.8 V, ~85–86 % to ~2.1 V, then a sharp notch — down to
  ~63 % at ~2.25 V, back up to ~78 % at ~2.35 V, down to a minimum ~57 % at
  ~2.6 V — then a steep climb to ~90 % at 2.9 V and ~92 % at 3.4 V, followed by
  a steady decline to ~73 % at 5.4 V.
- Black (500 mA): ~80 % at 1.8 V, ~85 % at 2.2 V, ~90 % at 2.9 V, peak ~93 % at
  ~3.4 V, then essentially flat ~91–92 % out to 5.4 V.
- Tan (1 A): trace begins near 2.0 V at ~80 %, dips to ~78 % at ~2.2 V, rises
  through ~88 % at 2.7 V with a small spike to ~90 %, then flat ~90–91 % from
  3 V to 5.4 V.
- Teal (2 A): trace begins near 2.35 V at ~78 %, rises to ~88 % at ~3.2 V, then
  slowly declines to ~86–87 % at 5.4 V.
- The 1 A and 2 A traces have no data below ~2.0 V and ~2.35 V respectively.

**Figure 13. Efficiency Versus Input Voltage, TPS63020, V_OUT = 4.5 V, Power
Save Enabled** (bottom right). Boxed condition: `TPS63020, V_OUT = 4.5V, Power
Save Enabled`. Same four-entry legend as Figure 12.
- Blue (10 mA): ~79 % at 1.8 V, ~88 % at 2.2 V, ~91 % at 3.4 V, ~93–95 % between
  4.6 V and 5 V, ~93 % at 5.4 V.
- Black (500 mA): ~70 % at 1.8 V, ~88 % at 2.2 V, ~91 % at 3.4 V, peak ~95–96 %
  near 4.8–5 V, ~93 % at 5.4 V.
- Tan (1 A): begins near 2.0 V at ~74 %, ~85 % at 3 V, ~90 % at 3.8 V, ~93 % at
  4.6 V, ~95 % at 5–5.4 V.
- Teal (2 A): begins near 3.7 V at ~84 %, rising with visible ripple to ~90 % at
  4.4 V, ~93 % at 5 V, ~94 % at 5.4 V.

Page footer: page 18, "Submit Documentation Feedback",
"Copyright © 2010–2019, Texas Instruments Incorporated",
"Product Folder Links: TPS63020 TPS63021".
