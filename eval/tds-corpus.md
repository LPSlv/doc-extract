# TDS corpus — three-way benchmark

## Dataset

**23 datasheets · 632 pages · 29.3 MB** — `corpus/tds/`
Median 20 pages per file, largest 99. Eight vendors, deliberately spread across
component classes rather than one manufacturer's ICs:

| vendor | files | parts |
|---|---|---|
| Texas Instruments | 8 | op-amps, current sense, I2C mux, buck/boost, gate driver |
| Nexperia | 7 | BJTs, Schottky, ESD, logic, shift register, diodes |
| Diodes Inc | 2 | LDO, MOSFET |
| Würth | 2 | LED, power inductor |
| Infineon | 1 | IRLZ44N MOSFET |
| Bosch | 1 | BME280 environmental sensor |
| Vishay | 1 | 4N25 optocoupler |
| onsemi/other | 1 | — |

Not committed to git (vendor copyright); `corpus/` is gitignored. The download
list is in `eval/tds-fetch.sh` so the corpus is reproducible.

ST, Microchip, TME and LCSC block automated fetches; those vendors are absent
for that reason, not by choice.

## Results

| approach | input tokens | vs optical | wall time | vision calls |
|---|---|---|---|---|
| **full optical** (read every page) | 1,513,884 | — | 5.9 s | 632 |
| **pdf-inspector only** (text) | 282,933 | **81% less** | 4.0 s | 0 |
| **pdf-extract** (text + routed figures) | 549,176 | **64% less** | 21.5 s | 279 |

Wall time is the deterministic local pipeline only — it excludes model inference,
which is where the token difference is actually paid. pdf-extract is the slowest
locally (routing calls `get_drawings()` on every page) and removes 964,708
tokens and 353 round trips relative to full optical.

## Quality

**This table is a cost measurement. Quality is not measured here**, and the
three approaches are not interchangeable:

- **full optical** sees everything on every page. It is the ceiling.
- **pdf-inspector** captures text and tables well (0.875 on opendataloader-bench)
  and captures **nothing** from a characteristic curve, pinout diagram or
  schematic. On the 632 pages here it produced no figure content at all.
- **pdf-extract** is pdf-inspector's text plus 279 routed figures — 44% of the
  pages optical would read.

The one place figure comprehension is measured against public ground truth is
`oldscans.md` (0% → 61.5% on `present` tests where there is no text layer).
No public benchmark scores figure comprehension in text-bearing PDFs.

## What this corpus caught

Running it found three routing defects, all now fixed:

1. **Vendor logos read as figures.** A bezier logo on a text page fired `curves`.
   4N25's *only* vision call was its legal disclaimer page. 176 curve-pages sit
   at ≥5% stroke area, 10 at <2% — the gap is clean, and all 10 were logos.
2. **Repeated vector furniture.** `ti_ucc27517` carries the same
   143-curve/20-diagonal signature on 6 pages. The raster filter already dropped
   ubiquitous images; drawings now get the same treatment.
3. **Filter 3 is unreliable.** It skips pages whose table `extract_pages_markdown`
   already produced — but that API returns **0 chars** for pages 1–2 of
   `irlz44n_infineon` while `process_pdf` extracts 100 table rows from the
   document. Those pages are re-rendered needlessly. **Not fixed**: see below.

## Two optimisations tested and rejected

`find_tables()` detects a table on 67 of 216 rendered pages (31%) that filter 3
missed — a tempting saving. Both ways of using it would have lost real content:

- **Skip pages whose drawings sit inside table bboxes.** Separation looked
  perfectly bimodal (0.0x vs 1.0). But INA226 p7 — a page of *six characteristic
  curves* — scored 0.01 and would have been skipped: `find_tables()` reads chart
  gridlines as a table. Verified by rendering the page and looking at it.
- **Require table cells to contain text.** INA226 p7 scores 1.00, identical to a
  real parameter table.

The 31% is not safely reachable with these signals. Recorded here so it is not
re-attempted blind.
