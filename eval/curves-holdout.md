# A datasheet holdout, and the `curves` branding rule tested on it

`eval/nofigure.md` measured the `curves` branch at **25% waste** and found that
21 of its 30 labelled wasted calls were one thing: a Texas Instruments
datasheet page whose only vector content is the 143-curve header logo. Four
signals were measured against it and three were rejected on merit
(`eval/rejected-signals.md`). The fourth — **small largest-stroke-cluster AND
no figure caption** — scored 17 cut, 17 `branding`, 0 real items lost, and was
still not shipped, for three stated reasons. One of them was fixable:

> it is read off the set it would be validated on, and it targets **vendor**
> boilerplate, so `arxiv_holdout` and `pmc_holdout` are both the wrong holdout.
> A datasheet holdout does not exist.

This file builds that holdout and reports what the rule does on it.

## `corpus/datasheet_holdout`

**295 component datasheets, 9,449 pages, eleven vendors**, pinned in
`eval/manifests/datasheet_holdout.urls.tsv`, fetched with
`uv run eval/discover.py datasheet_holdout && uv run eval/fetch.py datasheet_holdout`.

The design corpus `corpus/datasheets` is 153 TI + 27 Nexperia + 16 Diodes + 9
assorted — **75% one vendor**, and the rule under test was designed on that
vendor's logo. A holdout that is also TI-dominated would prove very little, so
the three vendors whose catalogues can be **enumerated** rather than guessed
carry the bulk, and TI is held to a tenth of the files.

| vendor | files | share | pages | median pages |
|---|--:|--:|--:|--:|
| Renesas | 55 | 18.6% | 1,238 | 18 |
| Vishay | 55 | 18.6% | 421 | 7 |
| Alpha & Omega | 48 | 16.3% | 360 | 6 |
| Texas Instruments | 27 | 9.2% | 1,299 | 46 |
| Nexperia | 23 | 7.8% | 298 | 13 |
| Melexis | 20 | 6.8% | 1,034 | 55 |
| Silicon Labs | 17 | 5.8% | 1,412 | 65 |
| Espressif | 15 | 5.1% | 935 | 60 |
| Raspberry Pi | 14 | 4.7% | 2,295 | 25 |
| Würth | 14 | 4.7% | 105 | 7 |
| Omron | 7 | 2.4% | 52 | 8 |

By **pages** — which is what routing actually sees — the mix is Raspberry Pi
24%, Silicon Labs 15%, TI 14%, Renesas 13%, Melexis 11%, Espressif 10%, the
rest 13%.

### How it was fetched, and who refused

Every host was checked against its `robots.txt` first, and every request used
`discover.py`'s plain `doc-extract-bench/1.0 (mailto:…)` User-Agent. **Nothing
here spoofs a browser, and no refusal was worked around**; a vendor that says
no is simply absent, which is the same rule `eval/tds-corpus.md` recorded for
ST, Microchip, TME and LCSC.

- **Refused with 403** to the bench agent: onsemi, ROHM, Toshiba, Bourns,
  Littelfuse, TDK, TE Connectivity.
- **`robots.txt` says no, although the file is served**: `ww1.microchip.com`
  (`User-agent: * / Disallow: /` — it answers 200 to a datasheet request, and
  is excluded anyway) and `www.winbond.com` (`Disallow: /resource-files`,
  which is where the PDFs live). Worth recording because
  `docs/NEXT.md` lists Microchip as blocking automated fetches: the block is
  in its robots policy, not in its server.
- **No response at all from this network**: `www.analog.com` — robots.txt and
  every datasheet time out. That is not a refusal, and ADI would be the single
  best remaining source of vendor-diverse datasheets if it is reachable
  elsewhere.

The three enumerable sources are all the vendor's own sitemap:

- **Vishay** — `sitemap1.xml.gz` lists 3,607 `/en/product/<id>/` pages, and
  `https://www.vishay.com/doc?<id>` 302s to that product's datasheet. The
  redirect is resolved at discovery time so the manifest pins the real
  `/docs/<id>/<part>.pdf` URL.
- **Renesas** — `sitemap.xml` paginates 232k URLs; walking it in order to the
  first 3,000 `/en/document/dst/` (datasheet) entries and sampling from those.
  Renesas also aggregates the Intersil, IDT, Dialog and NEC back catalogues,
  so the page templates inside it are not one house style.
- **Alpha & Omega** — `sitemap.xml` lists 1,969 product pages; the datasheet
  is `/res/data_sheets/<PART>.pdf`.

Sampling is `random.Random(20260813).sample` over the sorted candidate list.
The rest are curated part lists in the style of `discover.py`'s `datasheets()`;
21 of 317 candidates 404'd or came back as HTML and `fetch.py` dropped them.

### Disjointness from `corpus/datasheets`, checked both ways

- **by filename: 0 of 295 overlap** (the manifest is generated with the
  `datasheets` filename and URL sets subtracted, and the check is re-run
  against the fetched directory).
- **by sha256: 1 overlap, found and removed.** `ti_tlv9004.pdf` came back
  byte-identical to `corpus/datasheets/ti_tlv9002.pdf` — TI publishes one
  document for both part numbers. Filename disjointness did not catch it. The
  file was deleted and the row removed from the manifest, leaving **295 files,
  0 filename overlaps, 0 sha256 overlaps**, and no duplicate hashes inside the
  holdout either.

## The rule, and where every number comes from

    drop a `curves` firing whose largest SPATIALLY CONNECTED stroke cluster
    covers at most 0.05 of the page and whose page text carries no figure
    caption.

The threshold is the one the in-sample table was read at: on the 120 labelled
`curves` firings the drop set is identical for any cut in (0.0399, 0.0527], and
0.05 is the round number inside it. `eval/curves_validate.py` reimplements the
cluster measure from `fitz` primitives and **reproduces `eval/nofigure`'s
recorded in-sample result exactly** — same `cluster_frac` to four decimals on
all 120 firings, same `has_caption`, **17 drops, 17 `branding`, 0 real, 2
carrying rasters**. That check is why the holdout numbers below can be compared
with the in-sample ones at all.

- **2,957 vision calls / 1,392 `curves` firings** — `eval/curves_holdout/index-datasheet_holdout.json`,
  written by `eval/curves_validate.py`, which harvests all 295 documents with
  the shipped `harvest()` and then applies `drop_batch_furniture` **at corpus
  scope**, the same batch scope `eval/nofigure_render.py` used. One document
  is excluded because `harvest()` refuses it — `aos_AON6792.pdf`, "PDF parsing
  error: couldn't parse input: invalid content stream", which is the router
  behaving correctly on a malformed file — so the denominator is 294.
  Independently of `eval/nofigure.md`, `curves` is **47% of every vision call**
  on this corpus, against 45% there.
- **222 drops over 91 documents** — the same file. This is the set of `curves`
  page renders the rule removes *after* `cost_guard`, i.e. calls that really
  would have been made. The bare predicate fires more often than that — on
  **466 of the 3,511 pages** that reach it (`eval/curves_cost.py`) — but the
  rest sit in documents `cost_guard` collapses, where the page is rendered
  anyway and nothing is saved.
- **the precision** — `eval/curves_holdout/labels.tsv`, merged by
  `eval/curves_score.py` from 12 per-labeller TSVs, every column read by name,
  with the merge refusing to proceed unless every tag carries exactly three
  labels.
- **the cascade** — the same 295 documents harvested a **second** time through
  `eval/curves_patch.py`, which applies the proposed patch to `harvest.py`'s
  source and execs it. Not a model of the pipeline: the pipeline.

## Blind labelling

**120 of the 222 drops** (budget; sampled with seed 20260813, population and
seed in `eval/curves_holdout/sample.json`, 102 not labelled), split into four
batches of 30 and given to **three independent labellers each — twelve in
all**. Every labeller saw the 130-dpi PNG and nothing else: not the rule, not
the hypothesis, not the filename, not which answer would be convenient. The
instruction is reproduced verbatim in `eval/curves_holdout/LABELLING.md`, and
it told every one of them to **break every tie towards `figure`/`table`**, i.e.
against the rule.

| | figure | table | branding | none | n | precision |
|---|--:|--:|--:|--:|--:|--:|
| **all drops** | **24** | 0 | 96 | 0 | 120 | **80%** (95% Wilson 72–86) |

**120 of 120 unanimous 3/3.** As `eval/multifigure.md` says, that measures
determinism, not reliability: these are three runs of one model on one prompt,
independent of each other's answers and not of each other's blind spots.

The aggregate is not the finding. The split is — counts are of the **120
labelled** drops, not of all 222:

| vendor | figure | branding | labelled | precision |
|---|--:|--:|--:|--:|
| Texas Instruments | 1 | 52 | 53 | **98%** (90–100) |
| Renesas | 5 | 11 | 16 | 69% (44–86) |
| Alpha & Omega | 9 | 3 | 12 | **25%** (9–53) |
| Espressif | 0 | 11 | 11 | 100% (74–100) |
| Raspberry Pi | 0 | 10 | 10 | 100% (72–100) |
| Silicon Labs | 3 | 6 | 9 | 67% (35–88) |
| Vishay | 4 | 1 | 5 | **20%** (4–62) |
| Omron | 1 | 1 | 2 | 50% |
| Melexis | 1 | 0 | 1 | 0% |
| Nexperia | 0 | 1 | 1 | 100% |

**TI 98% (52 of 53), everything else 66% (44 of 67, 95% Wilson 54–76).** The
rule is not a branding detector. It is a TI-header detector, and this is the
first corpus that could tell the difference.

### Why it fails, in one number

The median `cluster_frac` of the drops labelled `branding` is **0.0372** — the
TI header logo, the constant the threshold was fitted around. The median of the
drops labelled `figure` is **0.0283**, *below* it. The two distributions are
not merely overlapping; they are interleaved, so **no threshold on this measure
separates them**. `eval/rejected-signals.md` already recorded the same
collision in-sample (0.0372 on the TI header and 0.0372 on `ti_lm317` p25, a
thermal chart). The holdout shows it is not an unlucky pair.

What the rule threw away, with `cluster_frac`:

- **`vishay_ilhb.pdf` p5 (0.0498)** — a page whose entire content is one
  impedance-vs-frequency plot under the heading *TYPICAL CURVES*. Rendered and
  checked by eye. Small real plots are exactly what this measure cannot see,
  and the caption gate does not rescue them because vendors head a figure
  *TYPICAL CURVES* or *Typical Characteristics*, not *Figure 3*.
- **`renesas_isl23415-datasheet.pdf` p18 (0.0397)**, `isl60002` p39 (0.0214),
  `isl8016` p22 (0.0249) — full-page **package outline drawings**: top view,
  two side views, detail and land pattern. A multi-view mechanical drawing is
  many small clusters, so "largest connected cluster" reports a small number
  for a page that is nothing but drawing. This is a structural defect of the
  measure, not a threshold that is set wrong.
- **Alpha & Omega part-marking and test-circuit pages** (0.0084–0.0472) — nine
  of twelve AOS drops. `aos_AOD6B60M1.pdf` p9 (0.0294) is six schematics and
  waveform plots and nothing else, and it is captioned — *Figure A: Gate Charge
  Test Circuit & Waveforms*, *Figure B*, *Figure C*. The caption gate misses it
  because the regex is `Fig(ure)?\s*\.?\s*\d`: it wants a **digit**, and this
  vendor letters its figures. A keep-gate that a vendor's own house style
  defeats is not a keep-gate.
- **cover pages carrying a simplified block diagram** — `ti_ina228.pdf` p1
  (0.0272, the *only* TI loss), `renesas_zsc31050` p1, `aos_AOZ1360DIL` p1.
- three Silicon Labs marketing back covers (photograph plus icon row) that two
  labellers flagged as arguably furniture. Counting all three as `branding`
  moves precision from 80% to **82% (74–88)**, which changes nothing.

## The cascade, measured rather than argued

`drop_textonly` could not cascade: it removes a page render only when the page
carries no raster, so nothing is left to un-subsume. **This rule can.** A
`curves` page render subsumes the rasters placed on it, and dropping the render
hands them back as standalone calls — the mechanism that forced the QR-code
filter's revert (`eval/tds-corpus.md`). In-sample, 2 of the 17 drops carried a
raster; here **35 of 222 do**.

Harvesting the corpus with the patch actually in the pipeline:

| | calls |
|---|--:|
| shipped | 2,957 |
| with the rule | 2,767 |
| **net** | **−190** |

222 drops buy 190 calls. The arithmetic is worth spelling out, because it does
not reduce to one effect: −222 drops, **+46 standalone rasters handed back**,
+3 drops in already-collapsed documents that were never going to save anything,
and −10 from the single document whose collapse the rule undid. And **four
documents finish with MORE vision calls than before**: `aos_AOD6B60M1.pdf`
7→11, `vishay_sip12107.pdf` 20→24, `renesas_845252` and `renesas_85104i` +1
each. Eight more churn without a net change. So a fifth of the benefit is
returned at the till, and the QR-filter pathology reappears on real documents —
in a rule whose precision already fails.

Two smaller pipeline effects, both real:

- `rpi_pico-datasheet.pdf` goes **31 → 21** calls, because dropping three
  `curves` firings takes the routed set back under the `cost_guard` bound and
  the document stops collapsing to `whole_document`. It is the only collapse
  flip in 294 documents, and it is a saving — but the rule does change *which*
  documents collapse, and `docs/NEXT.md` already flags that a changed collapse
  set moves `over_scale_guard`, i.e. when the skill stops to ask.
- Conversely, three drops in already-collapsed documents (`ti_lm5117.pdf` p3
  and p39, `aos_AOK75B60D1.pdf` p9) are recorded but save nothing at all — the
  page is rendered anyway as `whole_document`.

### No variant rescues it

The obvious repairs were scored on the same labels before writing the rule
off. None reaches the bar the last two shipped rules set (100%, 82–100 and
96–100):

| variant | clean / labelled | precision |
|---|--:|--:|
| the rule as measured | 96/120 | 80% (72–86) |
| **+ require no raster on the page** (which would also kill the cascade) | 86/98 | 88% (80–93) |
| `cluster_frac <= 0.04` | 87/104 | 84% (75–90) |
| `cluster_frac <= 0.02` | 32/39 | 82% (67–91) |
| `cluster_frac <= 0.01` | 23/25 | 92% (75–98) |

Tightening the threshold by a factor of five still leaves roughly one real
figure in twelve, because what it is cutting out is *small figures*, and the
smallest ones are as small as a logo.

## The diff, which this time found nine pages

`eval/curves_validate.py --diff` compares the analysis script's drop set with
what the patched pipeline really drops: **222 vs 225, 3 only in the script, 6
only in the pipeline.** Every one was chased down.

- **3 only in the script** — `omron_en-g5q` p4, `renesas_isl23415` p18,
  `renesas_x93154` p8, all with 2,894–2,958 stroke paths. The patch abandons
  the test above `CLUSTER_CAP` (2,000 paths) because the quadratic clustering
  is otherwise unaffordable there; the analysis script has no cap. The cap
  therefore changes 3 answers in 222, always towards **keeping** the page —
  and by luck one of the three is the ISL23415 package drawing, a real figure.
- **6 only in the pipeline** — the rule sits before `cost_guard`, so it also
  fires on `curves` pages in documents that then collapse (or that stop
  collapsing). Three are the phantom drops described above and three are the
  `rpi_pico-datasheet` pages that un-collapsed the document.

Neither direction is a bug in the measurement; both are facts about where the
rule sits. They are recorded because the `boxed_text` failure mode surfaced
from exactly this comparison, and a clean diff here would have been a sign the
two sides were not independent.

## Verdict: does not ship

- **80% precision, 95% Wilson 72–86%**, against 100% (82–100) for `boxed_text`
  and 100% (96–100 / 97–100) for `textonly_page`. One drop in five is a real
  figure.
- **98% on TI, 66% on everything else.** A rule that is near-perfect on the
  vendor it was fitted to and loses a third of its drops elsewhere is the exact
  failure `eval/tds-corpus.md` recorded for the top-band rule: *perfect on 382
  hand-checked items, then dropped a real arXiv figure.*
- **It cascades.** 46 rasters returned, four documents made worse.
- **And it is not free.** `eval/curves_cost.py` times `vendor_curves()` on its
  own, against a warm harvest, in one process with no ordering to bias it:
  over the 295 documents it runs on **3,511 `curves` pages and costs 62.4 s
  against 385.4 s of harvest — 16.2%, or 212 ms per document**. Per tested page
  the median is 4.7 ms and the p90 32 ms, but the tail reaches **608 ms**: the
  cluster test re-walks `get_cdrawings()` and is quadratic, and the early exit
  only saves the pages that are obviously charts. For scale, soft-mask
  suppression was rejected in `eval/rejected-signals.md` for **~40 ms per
  document**. This is five times that, in the routing hot path, to lose
  figures.

The honest conclusion is the one `eval/nofigure.md` already reached and this
corpus now supports out-of-sample: **a vendor logo is separable from a small
figure only by reading it**, and reading it is the vision call being avoided.
The `curves` branch stays as it is.

## What this leaves behind

The corpus is the durable part. `corpus/datasheet_holdout` is the first
vendor-diverse datasheet holdout in this repo, and it is the right instrument
for any future `curves` or vendor-boilerplate candidate — the wrong-holdout
objection that blocked the signature-ubiquity rule
(`eval/rejected-signals.md`) can now be answered for datasheets as
`corpus/pmc_holdout` answered it for journals.

Also worth carrying forward: **the labelled set says where the waste actually
is.** Of the 120 blind labels, 96 are `branding` and 0 are `none` — on a
datasheet, every wasted `curves` call is a page with a logo on it, and none is
a bare page. The `textonly_page` shape of fix (a page with *nothing* on it) has
no purchase here at all.

## Provenance

- `eval/manifests/datasheet_holdout.urls.tsv` — the 316 pinned URLs
- `eval/discover.py datasheet_holdout` — how they were found, and who refused
- `eval/curves_validate.py` — the rule, the drop set, the renders, `--diff`
- `eval/curves_patch.py` — the proposed patch as a textual diff against
  `harvest.py`, exec'd for the cascade measurement; `uv run` it to print the diff
- `eval/curves_cost.py` — what the test costs in the routing path
- `eval/curves_score.py` — the merge and the Wilson intervals
- `eval/curves_holdout/index-datasheet_holdout.json` — 222 drops, 1,170 kept
  `curves` firings, every added item, every changed document
- `eval/curves_holdout/labels-{1..4}{a,b,c}.tsv` — the twelve labellers
- `eval/curves_holdout/labels.tsv` — the 120 merged labels with agreement
- `eval/curves_holdout/LABELLING.md` — what they were told, verbatim
- `eval/curves_holdout/pages/` — the renders, gitignored; rebuild with
  `uv run eval/curves_validate.py corpus/datasheet_holdout`
