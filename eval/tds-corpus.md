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

ST, Microchip, TME and LCSC are absent, not by choice — but the reasons differ,
and this line said "block automated fetches" for all four until 2026-08-13.
Building `corpus/datasheet_holdout` checked each one: **Microchip's server
answers 200**; it is `robots.txt` that says `Disallow: /`, so the omission is
policy-compliance rather than refusal. ST, TME and LCSC do refuse. The
distinction matters because a robots policy can be revisited with the
publisher's permission and a 403 cannot.

## Results

| approach | input tokens | vs optical | wall time | vision calls |
|---|---|---|---|---|
| **full optical** (read every page) | 1,513,884 | — | 5.9 s | 632 |
| **pdf-inspector only** (text) | 282,933 | **81% less** | 4.0 s | 0 |
| **doc-extract** (text + routed figures) | 549,176 | **64% less** | 21.5 s | 279 |

Wall time is the deterministic local pipeline only — it excludes model inference,
which is where the token difference is actually paid. doc-extract is the slowest
locally (routing calls `get_drawings()` on every page) and removes 964,708
tokens and 353 round trips relative to full optical.

## Quality

**This table is a cost measurement. Quality is not measured here**, and the
three approaches are not interchangeable:

- **full optical** sees everything on every page. It is the ceiling.
- **pdf-inspector** captures text and tables well (0.875 on opendataloader-bench)
  and captures **nothing** from a characteristic curve, pinout diagram or
  schematic. On the 632 pages here it produced no figure content at all.
- **doc-extract** is pdf-inspector's text plus 279 routed figures — 44% of the
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

## False positives: what is and is not reachable

### The labelled set

`tests/raster-labels.tsv` — **382 raster firings, 49 branding, 5 portrait, 328
content**. Every `standalone_raster` the router fired across
`olmocr_headers_footers`, `olmocr_multi_column`, `olmocr_tables` and `pmc`,
extracted, rendered onto contact sheets and classified by eye. It replaces the
18-item sample the first audit used.

- **branding** = publisher furniture: masthead, society logo, conference banner,
  QR code, cover art, decorative section icon. Carries nothing the text lacks.
- **portrait** = author or staff headshot. Genuinely debatable — a face is
  information the text lacks, just not information anyone wants — so it is
  labelled separately and never counted as branding in the numbers below.
- **content** = a figure, chart, photo, scan, diagram or table image.

Branding is **12.8% of raster firings, 3.4% of all vision calls, and 2.8% of
raster image tokens**. The gap between those numbers is the whole story: a
branding image has a median cost of 140 tokens against 878 for a content
figure. The residual false positives are frequent but cheap.

### Signals measured

Each was implemented and scored against pages or images whose correct verdict
was established by rendering and looking. Recorded so none is re-attempted blind.

| signal | outcome |
|---|---|
| max single stroke-path area | rejected — GPO seal 0.0014 vs a real chart 0.0028 |
| stroke fill-ratio | rejected — seal 0.0078 *above* a real chart page 0.0050 |
| largest spatial stroke cluster | rejected — 4N25 disclaimer 0.0056 *above* a real chart 0.0045 |
| image colour complexity | rejected — a masthead and a multi-panel plot both score 0.003 |
| image position in page margins | rejected — catches 2 of 7 branding cases, and flags a real spectrogram |
| **page signature recurring across documents** | **shipped** — 227 → 9 false positives on US bills |
| image recurring across documents | rejected after implementation — dropped the LM2576 typical-application schematic |
| image recurrence *gated* on area and caption | **rejected — the gate does not save the case that caused the revert** (below) |
| text inside/around the image vs `doc.metadata` | **rejected — the overlap is 0.000 for branding and for content alike** (below) |
| image aspect ratio | rejected — branding p90 5.9 against content max 5.3; no cut exists |
| top-of-page band + no figure caption | **rejected — perfect on 382 labelled items, then dropped a real arXiv figure** (below) |
| QR finder patterns (1:1:3:1:1 run ratio) | **implemented, then reverted — it dropped robot-manipulation photos** (below) |

### Why the metadata idea fails

Reading text inside the image rect and in the 55pt band around it, then
comparing it against `doc.metadata` title/author/subject, was the one untested
proposal. Measured: **`inside_meta_overlap` and `near_meta_overlap` are 0.000 at
the median, the 10th and the 90th percentile for branding and content alike**.
Two reasons, both fatal. Only 147 of 382 documents carry a metadata title at
all. And a masthead's words live in the *pixels*, not the text layer — the
median branding image has **zero** extractable words inside it. There is nothing
to compare.

The inverse — a figure caption directly beneath the image — is real but
one-sided: 175 of 328 content images have one and **0 of 49 branding images do**.
It proves content, never branding, so it can only ever be a keep-gate on some
other rule.

### Why the top-band rule fails

The strongest combination found: image centre inside the top 10% of the page,
no figure caption in the strip beneath it. On the labelled set it scores
**17 hits, 17 branding, 0 content — precision 1.00, recall 0.35**.

Run against all twelve corpora it drops 36 of 1,524 firings, and rendering
those 36 shows why it cannot ship:

- `arxiv/2607.29107v1` p2 — a 50×30pt satellite inset that is **part of Figure
  1**, "Illustration of the cooperative calibration platform". The caption gate
  cannot rescue it: the text under the tile reads `tellite / Earth`, because the
  real caption belongs to the composite figure and sits far below.
- Fifteen TI and Nexperia **package-outline renders** heading mechanical-drawing
  pages — the photograph of the physical part, dropped as if it were a logo.

A rule that is perfect on 382 hand-checked items and still loses figure tiles on
the 1,142 it had not seen is exactly the failure mode this file exists to record.

### Why gating the recurrence rule does not rescue it

The reverted cross-document image rule was re-tested with the obvious gate —
drop only if the image is small *and* has no caption. Measured on
`corpus/datasheets`: the LM2576 typical-application schematic is `xref 29`,
**area 0.0609 of the page, caption `False`** (TI titles it above, not below). It
passes the gate and is still discarded. The gate does not address the failure;
it just makes it rarer. Rejected again, this time with the number.

### Why even the QR code is not reachable

A QR symbol looked like the one branding class with a structural signature: the
format mandates three finder patterns whose scanline run-lengths are 1:1:3:1:1.
Requiring square + binary + finder runs was implemented, tested, and selected
**5 of 5 QR codes and nothing else across the 1,524 raster firings** the router
produces — every drop rendered and checked. It shipped.

Then the before/after diff across corpora showed two arXiv documents going *up*,
4 → 8 and 4 → 9 calls. The rule had matched **19 further images that the sweep
never saw, because they are subsumed by page renders rather than fired as
standalone rasters** — six robot-manipulation photographs, nine UI icon glyphs,
and four SLAM map panels. Dropping them pushed a page below the `RASTER_GRID`
collapse threshold, and the cost guard then fell back to rendering every page.

The false hits cannot be tuned away:

| | real QR codes | robot photos / icons |
|---|---|---|
| dark pixel fraction | 0.30 – 0.51 | 0.35 – 0.48 |
| finder-run score | 0.56 – 0.85 | **1.00** |

The dark fraction overlaps completely, and the false positives score *higher* on
the finder test than the true QR codes — a 1:1:3:1:1 run at 60% tolerance is a
noise detector, not a QR detector. Separating them needs finder patterns
localised to three corners with a consistent module pitch, i.e. a real QR
decoder in the routing hot path, for a measured **5 calls in 5,504 (0.09%)**.
Reverted.

Two lessons worth keeping. Validating a drop rule only against what the router
*fires* on misses every image it currently subsumes — the sweep must run over
all images. And a filter placed before `grid_pages` can *raise* the call count
by breaking a raster grid, so a drop rule is only safe applied after subsumption.

### The answer

**Zero false positives is not reachable.** Twelve signals have now been measured.
Ten were rejected outright, one shipped (page signatures recurring across
documents), and one — the QR detector — shipped and was then reverted on evidence. Every rule
that closed the gap further was measured losing real content, including the two
that were flawless on the set they were fitted to.

The reason is structural, not a failure of tuning. A masthead, a society logo, a
conference banner and a cover are separable from a content figure only by reading
what they say, and reading them is exactly the vision call being avoided. The one
class with a format-level signature turned out to need a full decoder to
recognise, for 0.09% of calls.

**44 of 49 branding cases are therefore permanent**, and the right response is
cheaper handling rather than detection. That is defensible on the numbers: they
are 3.4% of vision calls and **2.8% of raster tokens**, with a median cost of 140
tokens against 878 for a content figure.
`reference/describing-visuals.md` now tells the agent to dismiss a recognised
publisher mark in one line rather than describe it — which is where the cost
actually lives, since the round trip is already paid by the time it is seen.
