## p009-render.png — full page render (two-column IEEE-style paper page with three figures)

The page carries three figures stacked across the full page width (Fig. 9, Fig. 10,
Fig. 11), then two columns of body text.

---

### Fig. 9 — three line charts side by side

Figure caption (centred beneath the row): **Fig. 9: The target domain
classification accuracy for different schemes trained in AWGN channel with fixed
CSNR.**

All three panels share the same six-entry legend, drawn inside the lower-right of
each panel, with a coloured line + marker per entry:

| Legend entry | Colour | Marker |
|---|---|---|
| Proposed | red | filled circle |
| Proposed w/o PCL | blue | filled circle |
| DANN JSCC | orange | filled square |
| MDAN | magenta/purple | filled triangle |
| KJDM | cyan/teal | filled diamond |
| Deep JSCC | dark green | filled circle |

Each curve carries a translucent shaded band of the same colour around it
(±1 standard deviation across seeds, per the body text).

**Fig. 9(a) — subcaption "(a) Trained CSNR = 10 dB".** Panel title above the
axes: "AWGN channel". Y axis "Target Domain Accuracy(%)", range 40–100, labelled
ticks at 40, 50, 60, 70, 80, 90, 100. X axis "CSNR(dB)", labelled ticks at −5, 0,
5, 10, 15, 20; data points at each of those six values. A vertical dashed grey
reference line is drawn at x = 10 (the trained CSNR). Values read from the axis
(estimates):

| Series | −5 | 0 | 5 | 10 | 15 | 20 |
|---|---|---|---|---|---|---|
| Proposed | ~73.3 | ~94.6 | ~97.4 | ~97.8 | ~97.8 | ~97.9 |
| Proposed w/o PCL | ~72 | ~87.5 | ~90.3 | ~90.8 | ~91.1 | ~91.2 |
| DANN JSCC | ~70.5 | ~83.2 | ~84.5 | ~85 | ~85 | ~84.8 |
| MDAN | ~64 | ~80.1 | ~83.8 | ~85 | ~85.5 | ~85.7 |
| KJDM | ~67.3 | ~82 | ~85.3 | ~86.5 | ~86.8 | ~86.9 |
| Deep JSCC | ~53.8 | ~67 | ~71 | ~72.1 | ~72.4 | ~72.6 |

Ordering at the right-hand end (best to worst): Proposed > Proposed w/o PCL >
KJDM > MDAN ≈ DANN JSCC > Deep JSCC.

**Fig. 9(b) — subcaption "(b) Trained CSNR = 15 dB".** Panel title "AWGN
channel". Same axes: Y "Target Domain Accuracy(%)" 40–100 (ticks 40, 50, 60, 70,
80, 90, 100); X "CSNR(dB)" ticks −5, 0, 5, 10, 15, 20. The vertical dashed grey
reference line is at x = 15. Values (estimates):

| Series | −5 | 0 | 5 | 10 | 15 | 20 |
|---|---|---|---|---|---|---|
| Proposed | ~65.9 | ~89.5 | ~95.9 | ~96.3 | ~96.6 | ~96.6 |
| Proposed w/o PCL | ~66.8 | ~83.9 | ~86.7 | ~86.8 | ~86.8 | ~87.1 |
| DANN JSCC | ~64.4 | ~78.4 | ~80.4 | ~81.6 | ~82.1 | ~82.2 |
| MDAN | ~62 | ~77.2 | ~82.5 | ~84.4 | ~84.7 | ~84.8 |
| KJDM | ~61.2 | ~79.4 | ~84.2 | ~84.9 | ~85.2 | ~85.5 |
| Deep JSCC | ~49.1 | ~63.9 | ~70.2 | ~72.2 | ~72.7 | ~72.8 |

Note: at x = −5 the Proposed curve (~65.9) is slightly *below* Proposed w/o PCL
(~66.8) — the only crossing in this panel; from x = 0 onward Proposed is highest.

**Fig. 9(c) — subcaption "(c) Trained CSNR = 10 dB."** Panel title "AWGN channel".
Y axis "Target Domain Accuracy(%)", range 55–100, labelled ticks at 55, 60, 65,
70, 75, 80, 85, 90, 95, 100. X axis is **m** (not CSNR), labelled ticks at 16, 18,
20, 22, 24, 26, 28, 30, 32; data points at m = 16, 20, 24, 28, 32. No vertical
dashed reference line. Values (estimates):

| Series | m=16 | m=20 | m=24 | m=28 | m=32 |
|---|---|---|---|---|---|
| Proposed | ~93.8 | ~95.9 | ~96.8 | ~97.3 | ~97.5 |
| Proposed w/o PCL | ~89.3 | ~89.7 | ~90.2 | ~90.8 | ~90.8 |
| DANN JSCC | ~84.5 | ~84.3 | ~84.7 | ~84.3 | ~84.7 |
| MDAN | ~84.1 | ~83.8 | ~83.3 | ~85.0 | ~85.0 |
| KJDM | ~83.0 | ~84.2 | ~86.8 | ~86.0 | ~86.5 |
| Deep JSCC | ~69.4 | ~70.2 | ~71.3 | ~71.8 (partly hidden behind the legend box) | ~72.1 |

The Deep JSCC curve passes behind the legend box between m ≈ 27 and m ≈ 32.

---

### Fig. 10 — three line charts side by side

Figure caption (centred beneath the row): **Fig. 10: The target domain
classification accuracy for different schemes trained in Rayleigh channel with
fixed CSNR.**

Same six-series legend as Fig. 9 (Proposed, Proposed w/o PCL, DANN JSCC, MDAN,
KJDM, Deep JSCC), same colours and markers, legend box in the lower right of each
panel, same shaded ±1 std bands. Panel titles read "Rayleigh fading channel".

**Fig. 10(a) — subcaption "(a) Trained CSNR = 10 dB".** Y "Target Domain
Accuracy(%)" 30–90, labelled ticks 30, 40, 50, 60, 70, 80, 90. X "CSNR(dB)" ticks
−5, 0, 5, 10, 15, 20. Vertical dashed grey line at x = 10. Values (estimates):

| Series | −5 | 0 | 5 | 10 | 15 | 20 |
|---|---|---|---|---|---|---|
| Proposed | ~44.4 | ~70.2 | ~79.3 | ~82.8 | ~84.6 | ~85.2 |
| MDAN | ~41.5 | ~62.0 | ~73.8 | ~79.2 | ~81.1 | ~82.1 |
| Proposed w/o PCL | ~41.3 | ~59.8 | ~71.2 | ~76.4 | ~78.2 | ~78.7 |
| KJDM | ~40.6 | ~58.9 | ~70.3 | ~74.9 | ~76.8 | ~77.4 |
| DANN JSCC | ~39.4 | ~55.6 | ~63.1 | ~71.5 | ~72.8 | ~73.3 |
| Deep JSCC | ~35.7 | ~50.7 | ~61.0 | ~65.8 | ~68.1 | ~68.7 |

Here MDAN is the second-best series (unlike the AWGN panels, where Proposed w/o
PCL was second).

**Fig. 10(b) — subcaption "(b) Trained CSNR = 15 dB".** Y "Target Domain
Accuracy(%)" 30–90, labelled ticks 30, 40, 50, 60, 70, 80, 90. X "CSNR(dB)" ticks
−5, 0, 5, 10, 15, 20. Vertical dashed grey line at x = 15. Values (estimates):

| Series | −5 | 0 | 5 | 10 | 15 | 20 |
|---|---|---|---|---|---|---|
| Proposed | ~40.5 | ~67.3 | ~80.5 | ~86.7 | ~89.4 | ~89.8 |
| MDAN | ~37.8 | ~57.5 | ~72.4 | ~78.9 | ~81.2 | ~82.1 |
| Proposed w/o PCL | ~41.8 | ~60.4 | ~72.6 | ~78.2 | ~79.5 | ~79.9 |
| KJDM | ~39.9 | ~59.4 | ~71.1 | ~77.4 | ~79.2 | ~79.9 |
| DANN JSCC | ~36.9 | ~56.6 | ~68.9 | ~76.7 | ~77.5 | ~78.4 |
| Deep JSCC | ~33.7 | ~48.1 | ~58.4 | ~65.1 | ~68.2 | ~69.5 |

At x = −5 the four middle curves are tightly bunched between ~36.9 and ~41.8; the
Proposed curve separates clearly from x = 0 onward.

**Fig. 10(c) — subcaption "(c) Trained CSNR = 10 dB."** Y "Target Domain
Accuracy(%)" 50–90, labelled ticks 50, 55, 60, 65, 70, 75, 80, 85, 90. X axis is
**m**, labelled ticks at 24, 26, 28, 30, 32, 34, 36, 38, 40; data points at
m = 24, 28, 32, 36, 40. No vertical dashed reference line. Values (estimates):

| Series | m=24 | m=28 | m=32 | m=36 | m=40 |
|---|---|---|---|---|---|
| Proposed | ~75.7 | ~77.6 | ~82.9 | ~84.5 | ~86.0 |
| MDAN | ~76.0 | ~77.0 | ~79.4 | ~79.8 | ~79.5 |
| Proposed w/o PCL | ~72.0 | ~74.1 | ~76.4 | ~76.6 | ~79.1 |
| KJDM | ~70.3 | ~72.1 | ~74.9 | ~76.6 | ~77.2 |
| DANN JSCC | ~71.7 | ~72.0 | ~71.8 | ~73.6 | ~76.1 |
| Deep JSCC | ~65.4 | ~65.6 | ~65.9 | ~68.1 | ~68.5 |

Note the crossing at the left: at m = 24 MDAN (~76.0) is marginally above
Proposed (~75.7); Proposed overtakes MDAN from m ≈ 28 and the gap widens to m = 40.

---

### Fig. 11 — three t-SNE scatter plots side by side

Figure caption (centred beneath the row): **Fig. 11: The tSNE visualization of
different schemes.**

Subcaptions, left to right: **(a) Deep JSCC**, **(b) DANN JSCC**, **(c) Proposed**.

Each panel is a dense 2-D scatter of points in two colours, with a small legend
in the upper right listing two entries: **MNIST** (dark blue) and **SVHN**
(cyan/turquoise). Axes are unlabelled numeric t-SNE coordinates; the tick labels
run roughly from −60 to 60 on both axes in all three panels (panel (c)'s vertical
ticks read approximately −60, −40, −20, 0, 20, 40, 60).

- **(a) Deep JSCC** — roughly ten diffuse blobs that overlap heavily and bleed
  into each other; large numbers of dark-blue MNIST points sit separated from the
  cyan SVHN mass inside and between clusters, so the two domains are visibly not
  aligned and the cluster boundaries are ragged.
- **(b) DANN JSCC** — about ten clusters that are more compact and more clearly
  separated than in (a); the cyan and dark-blue points are largely superimposed,
  with only scattered dark-blue points still visible at cluster edges. Some
  clusters still touch or merge.
- **(c) Proposed** — about ten small, round, well-separated clusters with clear
  white space between them; the dark-blue MNIST points are almost entirely
  covered by the cyan SVHN points, i.e. the two domains overlap most completely
  here.

---

### Body text (two columns, below the figures)

**Left column (continuing from the previous page):**

an additional StarGAN module during inference. We also compare our method with
DANN-based domain-adaptive JSCC [28], which performs global feature-level domain
alignment through adversarial learning. In addition, KJDM [32] is adopted as a
recent domain adaptation baseline. Unlike global marginal feature alignment, KJDM
matches the source feature-label joint distribution with the pseudo-labeled target
joint distribution, thereby introducing class-aware distribution alignment.

*B. Experimental Results on Digits*

We first conduct the experiments in digits datasets. We utilize the target domain
classification accuracy as the metric to assess and compare the performance of
various methods. According to Section III, the channel capacity is determined by
the physical channel configuration, including the transmitted dimension and CSNR.
We therefore vary *m* and CSNR and examine whether the qualitative behavior
predicted by the CCI analysis persists in practical Deep JSCC models. The value of
*λ* in the loss function is set to 0.001. All experiments are repeated with
multiple random seeds. The curves show the mean performance, and the

**Right column:**

shaded bands represent ±1 standard deviation across seeds.

In Fig. 9, we present the results of different methods across various test CSNRs
under the AWGN channel. The models are trained at fixed CSNRs of 10 and 15 dB and
evaluated over a wider CSNR range, while the channel-output dimension is fixed at
*m* = 32. The Deep JSCC, which does not employ any domain adaptation operation,
generally exhibits the lowest target domain accuracy because it cannot mitigate
the distribution discrepancy between the source and target domains. DANN JSCC
improves the target domain generalization performance through global feature
alignment, but its global discriminator cannot explicitly capture class-dependent
domain discrepancies. KJDM further reduces the domain gap by matching the joint
distributions of the source and target representations and generally performs
better than vanilla Deep JSCC and DANN JSCC in several settings. Nevertheless, it
remains inferior to the proposed method. MDAN also improves upon the conventional
baselines, but its performance remains substantially below that of the proposed
method. Benefiting from class-level feature alignment and pseudo-label supervised
contrastive learning,

*(the right column is cut off at the bottom of the page and continues on the next
page)*

---

Page furniture: none visible — the page render shows no running head, page number
or footer.
