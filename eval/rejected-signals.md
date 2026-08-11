# Signals measured and rejected

Filters that looked obviously right, were implemented and measured on real
corpora, and did not earn their place. Recorded so the same idea is not
re-implemented from first principles later.

`eval/tds-corpus.md` holds the twelve branding-detection signals, eleven of
which were rejected the same way. This file collects the rest.

---

## Soft-mask suppression — rejected, cost-neutral and slow

**The idea.** An xref another image names as its `/SMask` or `/Mask` is that
image's transparency channel, not a figure. It renders as white-on-black
shapes. Describing one is pure waste, and a v3 describer met exactly this: it
reported `p002-x32` as "the binary alpha mask of `p002-x33`", having spent a
vision call on it.

**Implemented as filter 0** in `harvest()`: scan every xref for `SMask`/`Mask`
keys, collect the referenced xrefs, drop them before the furniture filter.

**Measured** on 1,014 documents across datasheets, pmc, arxiv and papers:

| | before | after |
|---|--:|--:|
| routed rasters | 1,345 | 1,350 |
| page renders | 4,726 | 4,717 |
| vision calls | 6,071 | 6,067 |
| **vision tokens** | **5,886,199** | **5,885,431** |

**−768 tokens. −0.013%.** Seventeen mask items really do disappear, and the
change is correct in the sense that a mask is never a figure. But dropping
them takes some pages below the `RASTER_GRID = 6` threshold, so a page that
had collapsed into one render un-collapses into several crops. Rasters go
*up* by five, renders down by nine, and the two effects cancel.

**Cost:** the xref scan is ~40 ms per document — comparable to the entire
classify step the README advertises at 10–50 ms.

**Verdict: rejected.** Doubling per-document overhead for a 0.013% token
change fails the same bar the branding signals were held to. Worth
reconsidering only if `RASTER_GRID` is ever reworked so that mask suppression
stops un-collapsing pages — the two interact, and the interaction is the whole
reason the saving vanishes.

Prevalence, if useful later: 17 of 1,345 routed rasters (1.3%), concentrated
entirely in datasheets (16 of 519, 3.1%) and essentially absent from pmc,
arxiv and papers (1 of 826).

---

## Multi-figure pages — measured, not yet actioned

Not a rejected signal; an open one, recorded because the measurement exists.

The one genuine miss in figure-QA v3 (w18b) is a page carrying two drawings
where the router emits only the upper. Across the same four corpora:

| routed raster items | share |
|---|--:|
| on pages with >1 raster | 728 (54.1%) |
| lone raster, page also has vector figure signal | 134 (10.0%) |
| genuinely the only figure on the page | 483 (35.9%) |

So multi-figure pages are the common case, not the edge case. The measured
loss is nonetheless small (1 of 23 admitted questions), because when several
rasters exist the router usually emits all of them — the failure needs a page
where the *other* figure is vector artwork or was filtered out.

An obvious fix — render the whole page whenever a raster fires on a page that
also shows vector figure signal — would convert 134 crops into 134 page
renders. That is a cost increase for a defect measured at 1 in 23, and it has
not been justified. It should be measured properly before anyone implements it.
