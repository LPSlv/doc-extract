**Figure 16 (p341, RP2350 Datasheet) — block diagram of the flash execute-in-place (XIP) subsystem.**

Caption in the left margin: "Figure 16. Flash execute-in-place (XIP) subsystem. The cache is split into two banks for performance, but behaves as a single 16 kB cache. XIP accesses first query the cache. If a cache entry is not found, the QMI generates an external serial access, adds the resulting data to the cache, and forwards it on to the system bus (for reads) or merges it with the AHB write data (for writes)."

The diagram sits on a light grey panel. Three block styles are used: yellow/tan boxes for bus ports and the arbiter, blue boxes for XIP-internal logic and storage, one purple box for the QMI.

**Top row — five yellow bus-port boxes, left to right:**
1. "APB: XIP_CTRL"
2. "AHB: XIP (Even cache lines)"
3. "AHB: XIP (Odd cache lines)"
4. "AHB: AUX (Streaming DMA)"
5. "APB: QMI_CTRL"

**Second row — four blue boxes, left to right:**
1. "XIP/Cache Control Registers"
2. "Cache Bank 0 — 8 kB 2-way"
3. "Cache Bank 1 — 8 kB 2-way"
4. "Streaming FIFO"

**Third row:** a wide yellow trapezoid (multiplexer/arbiter shape) labelled "AHB Arbiter", spanning from under Cache Bank 0 across to under Streaming FIFO.

**Bottom:** a purple box labelled "QSPI Memory Interface".

**Connections (arrowheads as drawn):**
- "APB: XIP_CTRL" ↕ "XIP/Cache Control Registers" — double-headed vertical arrow.
- "AHB: XIP (Even cache lines)" ↕ "Cache Bank 0" — double-headed.
- "AHB: XIP (Odd cache lines)" ↕ "Cache Bank 1" — double-headed.
- "AHB: AUX (Streaming DMA)" ← "Streaming FIFO" — single arrow pointing up, from the FIFO to the AUX port.
- "XIP/Cache Control Registers" → "Cache Bank 0" — three short dashed arrows pointing right (control/configuration fan-out).
- "Cache Bank 0" ↕ "AHB Arbiter" and "Cache Bank 1" ↕ "AHB Arbiter" — double-headed vertical arrows.
- "Streaming FIFO" ← "AHB Arbiter" — single arrow pointing up from the arbiter into the FIFO.
- "AHB Arbiter" ↕ "QSPI Memory Interface" — double-headed vertical arrow, annotated "Data".
- "APB: QMI_CTRL" runs down the right-hand side, then left along a line annotated "Configuration", turning down into the top of the "QSPI Memory Interface" box (single arrow, into the QMI).
- Three signal stubs leave the bottom of the "QSPI Memory Interface", each drawn with arrowheads at both ends (bidirectional pins), labelled left to right: "SCK", "CSn[1:0]", "SD[3:0]".

No axes, scales or numeric values other than the block labels above.

Page furniture: header "RP2350 Datasheet"; footer "4.4. External flash and PSRAM (XIP)" and page number 341.
