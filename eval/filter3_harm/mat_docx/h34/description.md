**Figure 3.2 (memory map, p20).** "EFR32MG24 Memory Map — Core Peripherals and Code Space". Page section heading: "3.13 Memory Map". One tall vertical address-map column on the left (address space grows upward), with two dashed-line callouts expanding regions of it into detail columns on the right. Named regions are drawn white; unnamed (reserved/unpopulated) gaps are drawn grey and carry no block name. Addresses are printed to the right of each block boundary in a monospace font.

**Left column — full 32-bit address map (top to bottom; the address printed at a boundary is the top or bottom of the adjacent block):**

| Block | Top address | Bottom address |
|---|---|---|
| (unnamed grey band, top of map) | 0xfffffffe | 0xe0100000 |
| M33 Peripherals | 0xe00fffff | 0xe0000000 |
| (unnamed grey band) | 0xdfffffff | 0xb0005000 |
| FRCRAM (non-secure) | 0xb0004fff | 0xb0004000 |
| SEQRAM (non-secure) | 0xb0003fff | 0xb0000000 |
| (unnamed grey band) | 0xafffffff | 0xa0005000 |
| FRCRAM (secure) | 0xa0004fff | 0xa0004000 |
| SEQRAM (secure) | 0xa0003fff | 0xa0000000 |
| (unnamed grey band) | 0x9fffffff | 0x60000000 |
| Peripherals (non-secure) | 0x5fffffff | 0x50000000 |
| Peripherals (secure) | 0x4fffffff | 0x40000000 |
| (unnamed grey band) | 0x3fffffff | 0x20040000 |
| RAM (DMEM) | 0x2003ffff | 0x20000000 |
| Flash | 0x1fffffff | 0x08000000 |
| (unnamed grey band, bottom of map) | 0x07FFFFFF | 0x00000000 |

Notes on legibility: the very top address renders as `0xfffffffe` at this resolution (the final glyph is round, unlike the seven preceding `f`s); reported as printed. `0x07FFFFFF` is printed with upper-case hex digits, unlike the rest of the map.

**Callout 1 — "M33 Peripherals" expanded (dashed lines from the 0xe00fffff…0xe0000000 block to a detail column at upper right).** Boundary addresses are printed to the right of the detail column, top to bottom:

| Block | Top address | Bottom address |
|---|---|---|
| (unnamed grey band, above M33 ROM Table) | — (extends above 0xe0100000) | 0xe0100000 |
| M33 ROM Table | 0xe0100000 | 0xe00ff000 |
| (unnamed grey band) | 0xe00ff000 | 0xe0042000 |
| Embedded Trace Macrocell (ETM) | 0xe0042000 | 0xe0041000 |
| Trace Port Interface Unit (TPIU) | 0xe0041000 | 0xe0040000 |
| (unnamed grey band) | 0xe0040000 | 0xe000f000 |
| System Control Space | 0xe000f000 | 0xe000e000 |
| (unnamed grey band) | 0xe000e000 | 0xe0003000 |
| Flash Patch and Breakpoint (FPB) | 0xe0003000 | 0xe0002000 |
| Data Watchpoint and Trace (DWT) | 0xe0002000 | 0xe0001000 |
| Instrumentation Trace Macrocell (ITM) | 0xe0001000 | 0xe0000000 |

Legibility note: the address at the base of System Control Space is a 5-pixel glyph that is ambiguous between `e` and `c` at this render resolution — it reads `0xe000e000` (could be `0xe000c000`).

**Callout 2 — "Flash" expanded (dashed lines from the 0x1fffffff…0x08000000 block to a detail column at lower right).** Boundary addresses, top to bottom:

| Block | Top address | Bottom address |
|---|---|---|
| (unnamed grey band, top of detail) | — | 0x0fe08a00 |
| FLASH_CHIPCONFIG | 0x0fe08a00 | 0x0fe08400 |
| FLASH_DEVINFO | 0x0fe08400 | 0x0fe08000 |
| (unnamed grey band) | 0x0fe08000 | 0x0fe00400 |
| FLASH_USERDATA | 0x0fe00400 | 0x0fe00000 |
| (unnamed grey band) | 0x0fe00000 | 0x08180000 |
| FLASH | 0x08180000 | 0x08000000 |

Nothing on the page separates the two detail columns other than the dashed leader lines; no legend, scale bar or footnote accompanies the figure. The map is not drawn to scale (the grey reserved bands span far larger address ranges than their drawn height suggests).

Page furniture: running head "EFR32MG24 Wireless SoC Family Data Sheet" with section label "System Overview" in green beneath it; footer "silabs.com | Building a more connected world." and "Rev. 1.2 | 20".
