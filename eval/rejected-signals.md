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

## cost_guard's token model drifts from what ships — measured, tolerated

`cost_guard()` decides whether the routed set is cheaper than rendering every
page, and prices a raster with `_tok(*it["px"])` — the xref's **native**
dimensions. Since `_raster_pixmap()` began clip-rendering the placement, that
is no longer what `convert.py` emits: the render targets the native pixel
count but scales isotropically, so an anisotropic placement comes out larger.

Measured over 892 routed rasters (datasheets, pmc, papers), mirroring
`_write_image`'s shrink loop:

| | tokens |
|---|--:|
| `cost_guard` predicts | 858,616 |
| `convert.py` emits | 863,763 |
| **error** | **+0.60%** |

Per item the disagreement reaches **58%** — `ti_tps54331.pdf` p24 predicts 583
tokens and ships 920, four times over.

**Tolerated, not fixed.** `cost_guard` is a threshold, so a 0.6% aggregate
under-estimate only changes an outcome for a document sitting within 0.6% of
the boundary. Pricing the true output would mean a `get_image_info()` pass per
raster inside `harvest()`, which is the same ~40 ms/document overhead that
sank soft-mask suppression above — and this repo should not pay that twice for
sub-percent corrections.

Two consequences worth stating plainly rather than burying:

- the token figures in `docs/benchmarks/results/*.json` describe the **modelled**
  raster path, not the shipped one, and are ~0.6% low on rasters (rasters are a
  minority of calls, so the effect on the headline 20.1M is far smaller);
- a document within a hair of the `cost_guard` boundary can route the wrong way.
  No such document has been observed; nothing looks for one.

Revisit if `_raster_pixmap` ever changes scale policy again, since the error is
entirely a function of that policy.

## Signature ubiquity for `stroke_grid` — rejected, subsumed and never replicated

**The idea.** `harvest.py` already computes the set of page signatures covering
more than `UBIQUITY` (0.50) of a document, and already drops such a page as
`vector_furniture` — but only when it also has low ink, low stroke fraction and
fewer than 8 rects, which a ruled vendor title block fails by design. So: drop
a `stroke_grid` firing on signature ubiquity alone.

This sat in `docs/NEXT.md` for a while as *the free win* — "6 wasted calls
removed, nothing lost, 100% precision, and no new constant". Every word was
true and the recommendation was still wrong, for two reasons that only appear
when you ask where the 6 came from.

**All six are pages 2–7 of one document** (`MGR-10-30.PMC7871936.pdf`, the PMC
review that burned six consecutive calls on prose pages whose only strokes were
a header rule and a footer bar). A rule measured on one document is an
anecdote with a percentage attached. "100% precision" over n=1 reads exactly
like "95% precision" over 55 in a summary table, which is the whole danger.

**And `boxed_text` already takes them.** That document now routes **zero**
vision calls; all six pages are dropped as `boxed_text`. The marginal benefit
of the ubiquity rule, on top of what ships, is nothing.

**Measured out-of-sample too, for completeness**: on `corpus/arxiv_holdout` it
fires on **0 of the 77** `stroke_grid` firings that survive `boxed_text`. That
is not evidence against it so much as the wrong holdout — the rule targets
vendor and publisher boilerplate, and 348 arXiv papers contain none. Testing it
properly would need a datasheet or journal holdout, which does not exist here.

**Verdict: rejected, and removed from the queue.** `eval/strokegrid_ubiquity.py`
keeps the measurement. If a boilerplate-heavy holdout is ever fetched, that
script scores the candidate in one command — but it would first have to find a
case `boxed_text` does not already handle.

## Frame containment for `boxed_text` — rejected, dominated

**The idea.** The `boxed_text` rule that shipped (see `eval/strokegrid.md`)
drops a `stroke_grid` firing whose page has exactly two distinct vertical
stroke positions repeated on three or more pages. Its one known failure is a
**booktabs table continued across pages**: two interior rules, same place
every page, indistinguishable from a template.

There is a principled way to tell them apart, and it is not a threshold. In a
real frame the two verticals **are** the box's edges, so the horizontal rules
run from one to the other and the three coincide. A continued table's interior
rules sit strictly inside its horizontal rules. So: drop only when both
vertical positions match the x-extent of the page's horizontal strokes.

**Measured** over all 188 labelled firings — 170 in-sample, 18 from the
holdout — by `eval/strokegrid_frame_test.py`:

| rule | wasted cut | real lost | precision |
|---|--:|--:|--:|
| shipped (`vx == 2`, repeated) | 52 | 3 | 95% |
| + frame containment | 20 | 1 | 95% |

**Verdict: rejected, and the reason is not precision.** Both rules sit at 95%.
Containment gives up **32 of the 52** wasted calls — 62% of the entire benefit
— to rescue **2 of the 3** tables, and does not fix the third
(`2607.29378v1` p7). It buys one table back per sixteen wasted calls
surrendered, and still leaves the failure mode present.

What kills the recall is that the containment test is not specific to boxes:
any unrelated horizontal rule wider than the frame — a header rule, a footer
bar, a full-width `\hrule` above a caption — pushes the x-extent past the
frame's edges and rescues a page that was genuinely waste.

Worth revisiting only with a signal that identifies *continuation* directly
(a repeated column header, a "continued" caption, the same fingerprint on
consecutive pages rather than scattered ones). Consecutiveness is the cheapest
of those and was not tested; the three known losses are too few to fit it on
without repeating the mistake this whole exercise was about.

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
