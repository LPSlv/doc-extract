<u>Preprint</u>

## EVIDENCE-TYPECOMPETITION: WHENCAN INTERVENTIONALDATATEACHLANGUAGE

## MODELSCAUSALDIRECTION?

#### Xining Xun

Tsingjiao Information Science (Beijing) Co., Ltd.

### ABSTRACT

Interventional data is widely regarded as the gold standard for teaching models causal reasoning. We test this assumption in a fully controlled synthetic envi- ronment pitting observational correlation against causal effect, and find it fails instructively. In Simpson’s-paradox worlds—where the two have systematically opposite signs—increasing the fraction of interventional samples in pretraining (*α*) does*not*improve causal direction: the magnitude of the model’s *do*()-response grows monotonically with *α*, yet its sign is copied from the observational context. What governs whether interventional evidence is used is not the training mixture but the*evidence type present in the context at inference time*. Under an identical training recipe, a purely observational context induces systematic sign reversal in 29/50 worlds, a mixed context in 19/50, while aligned interventional probes alone yield 41/50 correct, with reversals at the measurement noise floor. Inference-time interventions localize the phenomenon: doubling the probe dose does not lift the suppression, whereas*erasing observational evidence from the context immediately* *releases the suppressed causal interpolation ability*(ratio true = +0*.*56, match- ing a model trained on probes alone); a four-state content manipulation shows the switch is content-mediated and graded. The suppression is stable across training seeds—every measurable strong reversal (11/11) persists on a matched-protocol second seed—and robust as a rate at 0.93B parameters (31.8% vs. 6% reversals in the matched probe-only arm), even as absolute interventional gains shrink four-fold. An external audit on CLadder further exposes a learned positive-effect prior with a two-layer structure: sign-randomized retraining removes it in-distribution but not out-of-distribution, where a positive default persists. We summarize: *the capability* *lives in the weights; the switch lives in the context*—activation patching local- izes the switch to the middle layers’ observational rows. We further quantify the sampling noise floor of probe-based causal evaluation and an evidence-averaging protocol that cuts sign errors from 26% to 9%.

**Keywords:** causal direction, language models, interventional data, Simpson’s paradox, evidence-type competi- tion, activation patching

### 1 INTRODUCTION

**The interventional-data hypothesis.**The ladder of causation (Pearl,2009) places intervention above observation: identifying causal effects from correlation requires, in principle, data from

# arXiv:2607.29484v1 [cs.CL] 31 Jul 2026

interventional distributions. This hierarchy has shaped data-curation intuitions in the LLM era. A natural hypothesis—which we denote**H1**—holds that*increasing the proportion of interventional* *data in pretraining should improve a model’s causal reasoning*. H1 is implicit in much data-mixture practice, yet to our knowledge has never been tested under fully controlled conditions: known confounding structure, computable causal ground truth, a leak-free protocol.

**A negative result that is more informative than “false”.**We test H1 on a family of Simpson’s- paradox worlds in which Corr*obs*(*X,Y*)*<*0 while the true causal effect eff(*X→Y*)*>*0, with opposite signs by construction. A six-level sweep of the interventional fraction *α∈{,.,...,.}* shows no monotone trend in corrected sign accuracy (0.5/0.3/0.2/0.4/0.4/0.4): **H1 is falsified**. The

<u>Preprint</u>

Figure 1: Overview (schematic).**A:** a hidden confounder makes observational correlation negative

while the true effect of *X* on *Y* is positive (sampled world, *ρ*= 0*.*9; full tour in AppendixA).**B:** with observational records in context, the answer follows the observational sign (19/50 reversed); erasing them*at inference time*releases the suppressed interpolation (E1b: ratio true = +0*.*56); doubling the probe dose alone does not (E1a).

manner of failure contains the real discovery: the*magnitude*of the model’s Simpson-slope grows monotonically with *α* (0.169 *→* 0.384), while its*sign*stays wrong throughout. The model learns something from interventional data—the magnitude—but copies the direction from the observational context: a**magnitude–direction duality**.

**The evidence-type factor.**If the mixture ratio is not the operative variable, what is? We isolate a one-dimensional factor—the*evidence type in the context*—holding training fixed at *α*= 1*.*0. Under a 50-world, evidence-averaged protocol, the four-way comparison (Table1) reveals a**contextual** **dose gradient**: the more observational evidence in the context, the stronger the suppression of causal direction (mean ratio true: pure obs *−*0*.*288*→* mixed *−*0*.*092*→* pure probes +0*.*418; paired McNemar*p*down to1*.*1e*−*9).

**Mechanism: the switch is in the context**(Figure1). Three zero-training-cost, inference-time interventions (E1) decide whether the suppression lives in training or at inference time. (i) Doubling the probe dose does not lift it. (ii)*Erasing the observational evidence immediately releases the* *suppressed interpolation ability*(ratio true rises from *−*0*.*09 to +0*.*56, matching the probe-only model). (iii) Dose titration and content manipulation (E5) show the switch is*content-mediated and* *graded*: one observational record barely suppresses, two dilute, four capture—*first dilution, then* *capture*—and removing observational*content*releases suppression even when observational-*format* tokens remain. The interpolation circuit was in the weights all along; the context had switched it off.

#### Contributions.

1. **A motivating negative result.**H1 is falsified under controlled conditions, revealing the magnitude– direction duality (§5.1).
2. **Main result.**The evidence-type factor and the contextual dose gradient: a 50-world four-arm comparison with paired statistics (§5.2, Table1).
3. **Mechanism contribution.**Inference-time decision matrices (E1, E5) localizing suppression as an inference-time, content-mediated, graded phenomenon (§5.3, §5.6).
4. **Methodology.**Quantification of the sampling noise floor of probe-based causal evaluation: a perfect interpolator commits 26% sign errors single-shot; evidence averaging repairs this (§4).
5. **Robustness and boundary conditions.**Rate-level persistence of the suppression at 0.93B scale (§5.5); a CLadder audit exposing a learned positive-effect prior and its two-layer structure under sign randomization (§5.7, §5.8).
### 2 RELATEDWORK

**Causal reasoning of LLMs.**CLadder (Jin et al.,2023) systematically evaluates LLMs across the three rungs of the causal ladder, finding degraded accuracy on formal causal queries; Corr2Cause (Jin et al.,2024) finds near-chance performance at inferring causation from correlational statements; CausalPitfalls (Du et al.,2025) audits statistical pitfalls including Simpson’s paradox;Kıcıman et al. (2023) report strong performance of GPT-family models on causal commonsense tasks. Unlike these studies, which*evaluate existing models*, we*control the training distribution itself*.

<u>Preprint</u>

**Amortized causal inference.**A complementary line pretrains transformers on synthetic causal data to estimate effects in-context: Do-PFN (Robertson et al.,2025) predicts interventional outcomes from observational context with prior-fitted networks; CausalPFN (Balazadeh et al.,2025) amortizes ATE estimation under ignorability;Liang et al.(2025) show that transformers emulate 2SLS when facing endogeneity in in-context linear regression. These works ask*whether*a transformer can amortize causal estimation; we ask*which evidence type*in a mixed observational–interventional pretraining stream drives the interventional answer, and what arbiters—dose, content, and sign priors—decide the competition.

**Teaching causal competence through training data.**Closest to our interventional stance,Vashishtha et al.(2024) train transformers from scratch on symbolic demonstrations of causal axioms (transitivity, *d*-separation) and show generalization to more complex graph structures, whileLampinen et al.(2023) show that agents can acquire active causal strategies from purely passive data—provided they may *intervene at test time*, with natural-language explanations enabling generalization even from perfectly confounded training data. Neither, however, mixes competing evidence types: the first teaches explicit symbolic rules; the second assumes an active experimentation channel at deployment. We isolate the corner they leave open—purely passive inference over contexts where observational and interventional evidence coexist and contradict—and find that an observational prior, not missing capability, decides the answer (§5.2, §5.6).

**In-context learning as function learning.**Garg et al.(2022) show that Transformers can learn linear and nonlinear function classes from in-context examples (our least-squares-interpolator baseline is of this kind);Akyurek et al. ¨ (2023) relate ICL to gradient-descent-like algorithms. Our probe protocol is the causal version of this paradigm: probes supply (*X,*responses of other variables) under intervention, and the query asks for interpolation over a *do*(*X*) grid. Our negative result also delineates a boundary for this paradigm: when observational evidence is mixed into the context, ICL selects the wrong function class—not a failure to learn, but a failure of evidence selection.

**Knowledge conflicts.**Longpre et al.(2021) andXie et al.(2024), among others, study LLM behavior when parametric knowledge conflicts with contextual knowledge, finding that reliance on context varies with prior strength. Ours is a sharper causal instance: the conflicting parties are two*statistical* *evidence types*rather than factual memories. To our knowledge, the specific form “interventional evidence suppressed at inference time by an observational prior” has not been reported.

**Simpson’s paradox.**A classical statistical problem (Pearl,2009); in NLP it has appeared mainly in bias auditing. We repurpose it as a jointly controlled train–evaluation instrument: a world family in which observational correlation and causal effect have opposite signs makes “copying observation” and “true causation” mechanically distinguishable at the level of signs.

### 3 SETUP

**Synthetic world generator.**Each world is a parametric structural causal model (SCM): *n* nodes (*n∈*[5*,*12]; the novel-topology domain uses [13*,*16]), Erdos–R ˝ enyi or scale-free graph structure ´ (equal probability), and mixed linear–nonlinear mechanisms. A confounding-strength parameter *ρ∈ {*0*,.*3*,.*6*,.*9*}* controls unobserved confounding paths (*Z→X*, *Z→Y*). The evaluation family (SEED TEST domain) uses *ρ*= 0*.*9 and selects confounded triples (*Z,X,Y*) such that observational correlation and causal effect have opposite signs (a*Simpson trap*): in 50/50 worlds, Corr*obs*(*X,Y*)*<*0 while eff(*X→Y*)*>*0 (mean *≈*+0*.*57; a sampled world is visualized end to end in Figure5, AppendixA). Training data are generated online and are infinitely fresh, eliminating fixed-corpus memorization.

**Evidence formats.**Each training/evaluation sample = a context (*k*= 4 evidence records) + one query. Five evidence types: **OBS**(observational samples);**NONE**(no context);**INT**(intervention records on *random*nodes);**PROBE**(intervention records on the*query*node *X*—*do*(*X*=*v*)*→* responses of all variables, *v* sampled 50/50 from a two-sided range);**OBS PROBE**(half obs, half probes). Queries take the form*do*(*X*=*x₀*)*→Y*=?, over the grid*x₀ ∈X*=*{−*1*,−*0*.*5*,*0*,*0*.*5*,*1*}*.

**Model and training.**A 25.7M-parameter GPT-style decoder (8 layers, na¨ıve attention), vocabulary 41, block size 640. Training: 20,000 steps, batch 64, lr 6e*−*4 (warmup 500). *α*-mixture sampling: each sample is independently drawn from the interventional distribution with probability *α* (strict binomial mixture). Seed domains are disjoint across train/val/test/novel.

<u>Preprint</u>

**Formal statement.**A world is an SCM *W*= (*G,F,PU*) over variables *V*=*{V₁,...,Vn}* with mechanisms *Vi*=*fi*(pa(*Vi*)*,Ui*) and an unobserved confounder *Z* for a designated triple (*Z,X,Y*), with the Simpson-trap condition enforced in the evaluation family:

Corr*obs*(*X,Y*)*·*eff(*X→Y*)*<*0*,*eff(*X→Y*) = 2 <u>1</u> E[*Y|do*(*X*=1)]*−*E[*Y|do*(*X*=*−*1)]*.*

(1)
A context is a multiset of *k* evidence records *C*=*{r₁,...,rk}*, each either*observational r* *obs* = (*v₁,...,vn*)*∼PW*(*V*)or*interventional*

||r =|do(V =v),(v₁,...,v||)∼P (V|do(V||=v)) .(2)||
|---|---|---|---|---|---|---|---|
||jint|j||n W|j|||
||OBS|||||||
||x|||||||
|||||2||||
|w|b|a x₀∈X|x||w|w|w|
||w|||||||

Evidence type *τ*(*C*)*∈ {,*NONE*,*INT*,*PROBE*,*OBS PROBE*}* fixes which records appear. Per world*w*, predictions *Y*ˆ0over the grid are regressed by least squares, X slope = arg min min *Y*ˆ0*−*(*a*+*bx₀*)*,*t = slope */*slope true*,*(3)

where slope true is the oracle grid-regression slope from E[*Y|do*(*X*=*x₀*)] estimated by large- sample Monte Carlo. ratio true*≈*1: correct magnitude; *≈*0: blind; *<*0: reversed. The hit criterion applies a magnitude gate*τ₀* = 0*.*05:

#### hitw=⊮ |slopew|> τ₀ ∧sign(slopew) = sign(effw).(4)

We also track the interventional point-prediction advantage ∆ = mse*obs−*mse*do*over held-out *do*()-queries (∆*>*0: interventional semantics learned).

### 4 EVALUATIONMETHODOLOGY

**Hit criterion.**Per-world three-way classification: **hit**(*|*slope*|>*0*.*05, sign consistent with eff) /**flat** (*|*slope*|≤*0*.*05) /**reversed**(slope*<−*0*.*05; eff is always positive in the evaluation family). The magnitude gate eliminates false positives in which a numerically flat line is counted as a hit.

**The sampling noise floor of probe-based evaluation.**Even if the model were a*perfect least-* *squares interpolator*, probe evidence is itself a single-draw random variable (4 probes, one sample each), and its regression slope carries an intrinsic sign-error rate. Writing the oracle grid response as *µ*(*x₀*) =E[*Y|do*(*X*=*x₀*)], single-shot evaluation estimates ˜*µ*(*x₀*) =*µ*(*x₀*) +*ε*(*x₀*) with heteroscedastic*ε*inherited from*PW*, so that

*p*err= Pr sign slope(˜*µ*) *̸*= sign slope(*µ*) *>*0*even for a perfect model.*(5)

Offline simulation (20 repetitions): under single-shot sampling (*nrep*=1), a perfect interpolator commits sign errors at a rate of**2.6/10 (26%)**—per-world sign statistics that do not control for this floor can manufacture “attractor camps” out of noise. The repair is**evidence averaging**(*nrep*): for each query, draw *nrep*independent context-evidence sets, average the predictions, then regress, reducing Var[˜*µ*] by a factor *≈*1*/nrep*; *nrep*= 8 reduces the floor to**0.9/10 (9%)**. All final results are obtained at*nrep*= 8; reversal counts are tested one-sidedly against the floor,

#### Pr Bin(50, p₀=0.09)≥k ,(6)

to separate mechanistic signal from measurement noise (Figure3).

**Statistics.**Arms are compared on identical world sets: exact McNemar test on hit discordance, Wilcoxon signed-rank onratio true, and the binomial test of equation6.

**Reproducibility.**The generator’s intervention-value cache persists across calls: offline replay of the evaluation stream must explicitly re-seed the cache, otherwise identical protocols drift. Code fingerprints (md5) and seeds for all final results are registered in AppendixB.

### 5 RESULTS

5.1 H1FALSIFIED:THE MAGNITUDE–DIRECTION DUALITY Fixing *ρ*= 0*.*9 withOBScontexts, we sweep *α∈{.,.,.,.,.,.}* (20,000 steps each). **H1 is falsified**: corrected sign accuracy across the six levels is 0.5/0.3/0.2/0.4/0.4/0.4—no monotone

Preprint

trend (the 0.5 at *α*= 0 is blind sign-hitting).**Duality**: the*magnitude*of the Simpson slope grows monotonically with *α* (0.169 *→* 0.384) while the*sign*stays negative throughout: *magnitude is learned* *from interventions; direction is copied from context*.**Loss decouples from causal competence**: all six runs converge with similar losses, yet causal metrics diverge.**The shortcut deepens with** **training**: at *α*= 1*.*0, ∆ decays from +0*.*20 (step 2k) to *−*0*.*19 (step 20k)—interventional semantics is learned first, then overwritten (replayed within a single run, §5.4).

**The dual role of context (ablations).**Training*without*context (NONE) removes the contamination source (reversals 0/10) but collapses the slope magnitude to 0.018—the model loses its world- identification channel and falls near-blind. Random probes (INT) are worse than baseline (reversals 7/10), rejecting the “target-node confusion” hypothesis. Context is simultaneously a*contamination* *source*and a*world-identification channel*.

5.2 MAIN RESULT:THE FOUR-ARM EVIDENCE-TYPE COMPARISON
Table 1: Four-arm comparison over 50 worlds (*α*= 1*.*0, *ρ*= 0*.*9, *nrep*= 8, identical world set,
 paired; curr. = curriculum).

|Arm|Context evidence|Hit|Flat|Reversed|meanratio true|∆|
|---|---|---|---|---|---|---|
|Baseline|pure OBS 7/50||14|29 −|0. 288|− 0. 100|
|C1 OBS|+ probes|18/50|13|19 −|0. 092|+0. 041|
|C2 pure probes|41/50||5|4+0|. 418+0|. 262|
|C2-curr2|pure probes (harder curr.)|40/50|6|4+0|. 482|+0. 373|

Table1and Figure2show the**contextual dose gradient**: as the observational dose in the context decreases (pure obs *→* mixed *→* pure probes), mean ratio true rises monotonically (*−*0*.*288*→* *−*0*.*092*→*+0*.*418), with ∆ in lockstep (*−*0*.*100*→*+0*.*041*→*+0*.*262). Paired exact McNemar tests (hit criterion): C2 vs. baseline *b*=35*/c*=1, *p*= 1*.*1e*−*9; C2 vs. C1 *b*=25*/c*=2, *p*= 5*.*7e*−*6; C1 vs. baseline *b*=14*/c*=3, *p*= 1*.*3e*−*2. Paired Wilcoxon on ratio true: *p*= 7*.*6e*−*9/2*.*9e*−*7 /

5*.*8e*−*3. C2’s slope exceeds C1’s in 43/50 worlds (paired*t*,*p*= 5*.*6e*−*8).
Figure 2: Main result. (a) Hit/flat/reversed counts over 50 worlds; (b) per-world ratio true
 distributions—the contextual dose gradient. Figure3closes the noise-floor methodology empirically (one-sided binomial against *p₀* = 0*.*09): baseline (29/50, *p*= 4*.*7e*−*18) and C1 (19/50, *p*= 2*.*6e*−*8) lie deep in the mechanistic regime, while C2 and C2-curr2 (4/50 each,*p*= 0*.*67) sit on the null—the residual reversals on the C2 side*are*the measurement noise.
5.3 MECHANISM LOCALIZATION:THEE1INFERENCE-TIME DECISION MATRIX Three zero-training-cost, inference-time interventions decide the locus of suppression. Doubling the probe dose (E1a: C1 with 4 probes instead of 2) does not lift it (4/8 hit, 2 reversed);**erasing** **the observational evidence immediately releases the suppressed interpolation ability**(E1b: 7/9 hit, ratio true from *−*0*.*09 to +0*.*56, matching C2 at +0*.*418 same protocol / +0*.*55 same world set); injecting observational records into C2 (E1c) collapses parsing to zero (out-of-distribution), an invalid arm set aside.*The suppression of interventional evidence by the observational prior is an* *inference-time phenomenon*—the capability is not missing; it is switched off by context.

Preprint

Figure 3: Reversal counts vs. the noise floor: Binomial(50, 0.09) null with the four arms’ reversal

counts marked. Baseline (29) and C1 (19) lie deep in the mechanistic regime; C2 and C2-curr2 (4) sit on the null.

5.4 ROBUSTNESS:SEEDS,CURRICULUM,CONFOUNDING,TOPOLOGY **Seed replication; suppression is a world property.**C1 closes on three seeds with nearly identical profiles (s0: 18/13/19; s1: 18/13/18; s2: 18/13/19) and C2 on two (s0: 41/5/4; s1: 44/3/3; McNemar *p*= 0*.*549). A matched-protocol second C1 seed (identical evaluation code, the same 50 worlds, *nrep*= 8) replicates the per-world structure: per-world slopes correlate at *r*= +0*.*825, the reversed sets overlap in 14 of 18 (hypergeometric *p*= 8*.*7e*−*6), and*every*measurable strong reversal persists (11/11 at slope *<−*0*.*15; one world lost to a parse failure), while the worlds flowing in or out of the reversed set all sit within *|*slope*|<*0*.*15 of the threshold—boundary noise at the measurement floor, not structural drift (s0*↔*s2:+0*.*872, 15/19; AppendixD). **Curriculum and confounding-strength transfer.**C2-curr2 (harder curriculum) is indistinguishable from C2 (hits 40 vs. 41, McNemar *p*= 1*.*00; *r*= +0*.*775), and C2-rho06—trained entirely at the milder *ρ*= 0*.*6, evaluated at *ρ*= 0*.*9—achieves 39/8/3, mean ratio true +0*.*348 (McNemar *p*= 0*.*727;*r*= +0*.*684). **Within-run degradation.**The C1-s2 trajectory replays§5.1within a single run: the slope ratio falls from+0*.*172to*−*0*.*266over the four evaluations after step 12k while∆stays positive. **Novel topology.**On the unseen 13–16-node domain (C2 checkpoint), 16 of 20 worlds parse, yielding 12 hit / 2 flat / 2 reversed, ∆ = +0*.*381; the 2 reversals are floor-consistent (*p*= 0*.*43): causal- direction interpolation**transfers to larger novel topologies**.
5.5 SCALING TO1B:THE SUPPRESSION PERSISTS AS A RATE
Table 2: Scale comparison on the identical 50-world protocol (in-distribution context length; C2 25M
 as in Table1). Absolute gains shrink globally at 1B, yet the arm contrast in reversals survives. parse = fraction of syntactically valid responses.

|Arm|Scale|Hit|Flat|Reversed|meanratio true|∆parse|
|---|---|---|---|---|---|---|
|C2|1B|14/50|33|3+0|. 072|+0. 1621.00|
|C1|25M|18/50|13|19 −|0. 092|+0. 0411.00|
|C1|1B|12/44|18|14+0|. 008|− 0. 0030.88|

We retrain both arms at 0.93B (same recipe, lr 3e*−*4, 20k steps) and evaluate on the identical 50-world set (Table2).**(i) The arm contrast is scale-robust.**At 1B the mixed-context arm still reverses 14/44 worlds (31.8%) against 3/50 (6%) in the matched probe-only arm (Fisher exact *p*= 1*.*2e*−*3).**(ii)** **Absolute magnitudes shrink globally and cannot measure the suppression.**Mean *|*ratio true*|* drops from 0.464 to 0.105 on C2 (4*.*4*×*) and from 0.372 to 0.160 on C1 (2*.*3*×*)—a global gain contraction that hits the control arm*harder*(its origin open,§7); only scale-free measures (reversal rates, the arm contrast) are meaningful cross-scale, and they show persistence.**(iii) The identity** **of suppressed worlds does not transfer across scale.**Of the 17 worlds reversed by C1 at 25M, only 6 remain reversed at 1B (base rate 5.4), and per-world slopes are rank-uncorrelated across scale (Spearman *r*= +0*.*08, *n*= 44 paired)—against *r*= +0*.*87 across seeds*within*25M (§5.4): at 1B the suppression is a diffuse,*reshuffled*rate elevation rather than stable per-world capture (Table3).

<u>Preprint</u>

5.6 MECHANISM DISCRIMINATION:A GRADED,CONTENT-MEDIATED SWITCH(E5) Two inference-time probe batteries on the C1 checkpoint (*nprobe*= 4, *nrep*= 8, 50 worlds; paired on commonly parsed subsets). **Dose titration**(OBSrecords *nobs*= 1*/*2*/*4; paired *n*= 37): hits 31 *→* 22 *→* 17 and mean ratio true +0*.*472*→*+0*.*204*→*+0*.*037 as the observational dose grows (McNemar n1 vs. n2 *p*= 3*.*9e*−*3; n1 vs. n4 *p*= 1*.*3e*−*3; Wilcoxon n1 vs. n4 *p*= 1*.*0e*−*5). The*shape*is informative: at *nobs*= 2 the model mostly goes**flat**(12 flat / 3 reversed); at *nobs*= 4 it**reverses**(11 reversed, binomial *p*= 3e*−*4)—a singleOBSrecord barely suppresses (39/50 hits, *≈* the probe-only level), two dilute the signal, four capture it: *first dilution, then capture*. (The *nobs*= 8 arm was lost to a parse-rate collapse, 0.16; §7.) **Four-state content manipulation**(*nobs*= 4; paired *n*= 33): hits—**SAME**(this world’s true obs) 16 *<* **SCRAMBLE**(marginals intact, correlations destroyed) 20 *≈* **CROSS**(a foreign world’s intact obs) 21 *<* **ZERO**(all-zero placeholders) 25; mean ratio true +0*.*059*/*+ 0*.*203*/*+ 0*.*192*/*+ 0*.*378. The decisive contrast is**SAMEvs.ZERO**(McNemar *p*= 0*.*023; Wilcoxon *p*= 2e*−*4): removing observational*content*releases suppression even when obs-*format*tokens remain—the pure format- dilution hypothesis is rejected.CROSSandSCRAMBLEare indistinguishable (Wilcoxon *p*= 0*.*87): real-valued observational content suppresses partially*regardless of correlational coherence*with the current world;SAMEadds the largest increment (vs. cross/scramble: Wilcoxon *p≈*0*.*07–0*.*08, marginal at*n*= 33). OnlySAMEshows mechanistic reversals (9/33; the rest noise-compatible). **Verdict.**The switch is*content-mediated and graded*, not a binary format gate: format without content (ZERO) *≈* full release; plausible observational numerics alone (CROSS *≈* SCRAMBLE) yield partial, correlation-agnostic suppression; the world’s own correlation contributes the decisive increment. Each observational record shifts the evidence mixture toward the observational attractor, and coherent this-world correlations shift it most.
5.7 EXTERNAL AUDIT ONCLADDER:A SIGN PRIOR AND ONE-SIDED READING To stress-test external validity we structurally transplant CLadder v1 (Jin et al.,2023) into our symbolic channel: its binary Bernoulli SCMs (10 textbook graph families, 3–4 nodes, fully observed CPTs) are instantiated as our worlds and evaluated with the*identical*probe protocol (*nprobe*= 4, *nrep*= 8; *x₀ ∈ {*0*,*1*}*, so the two-point slope is the ATE). Ground truth, recomputed by exact enumeration of the released CPTs, agrees on 9/10 families (*<*10
*−*9; exception in Appendix). Two suites:ALL(5 worlds per family, 45) andCONF(50*confounding*-family worlds—the direct analog of our*ρ*= 0*.*9Simpson design).

Three findings.**(i) Format transfer is perfect**: 285/285 worlds parse across arms and suites—binary values, unseen graph families, and smaller graphs pose no format problem.**(ii) Both interventional** **arms carry a positive response offset**while the observational baseline is flat (*a≈*0*.*03, *b≈*0, and 47–72% of its predictions are negative): regressing predicted on true effects, ∆ = b *a·*ATE +*b*, gives *b*= +0*.*233 for C2 (95% CI [+0*.*195*,*+0*.*269]) and *b*= +0*.*386 for C1 ([+0*.*341*,*+0*.*431]). The offset is therefore*learned from interventional training with single-signed effects*, not a property of the evaluation pipeline. Because every training world had a positive causal effect by construction, the models answer “do(*X*) raises *Y* ” regardless of evidence: on sign-balanced CLadder this yields *∼*50% hit / *∼*50% reversal (96.3% of negative-ATE predictions remain positive). This is a genuine prior, not a measurement limit: an oracle reader of the same evidence misreads the sign only 19–45% of the time at these effect sizes (sign-information floor, Appendix).**(iii) Both arms read*one-sidedly*** (Figure4): within positive-ATE worlds (*n*= 23) both track magnitude (within-subset correlations +0*.*53 C1 / +0*.*48 C2, C1 at *∼*2*×* the amplitude, mean prediction +0*.*58 vs. +0*.*28); on negative-ATE worlds (*n*= 27)*both*collapse onto the positive default (within-subset correlations *−*0*.*08 / *−*0*.*10; reversals 25/27 and 24/27). C1’s larger pooled slope (*a*= 0*.*76 vs. 0*.*21) is thus an*amplitude*effect on positive worlds, not sign competence: only 2–4% of all predictions are negative at all. The mixed context—suppressed in-distribution—amplifies magnitude tracking out-of-distribution, but neither arm reads the sign. A matched-protocol second C1 seed replicates the asymmetry but not its amplitude (positive-world correlation +0*.*19; negative-world reversals 13/27): the one-sided*structure* is seed-robust, the magnitude is not (§5.8).

<u>Preprint</u>

The audit thus exposes a boundary condition invisible to our main experiments (single-signed effects by design), quantified as an offset–gain decomposition rather than an accuracy score; it motivates the sign-randomized retraining (confounding path co-flipped, so the Simpson property holds for both signs) whose falsifiable prediction—*b→*0with*a*intact—is tested in §5.8.

Figure 4: One-sided reading on the 50 CLadder confounding worlds. Blue circles: positive-ATE

worlds (*n*= 23)—both arms track magnitude (within-subset slopes +0*.*62 / +0*.*48). Red squares: negative-ATE worlds (*n*= 27)—predictions collapse onto a positive default (slopes *≈*0; reversals 25/27 C1, 24/27 C2). The pooled-slope difference (*a*= 0*.*76 vs. 0*.*21) is positive-world amplitude, not sign reading: only 2–4% of predictions are negative.

5.8 SIGN-RANDOMIZED RETRAINING:THE POSITIVE PRIOR IS TWO-LAYERED The audit of§5.7motivates a direct repair: retrain with the causal-effect sign randomized per world (*s∈{±*1*}* multiplying*both*the causal and the confounding path, so the Simpson property holds for both signs and “always positive” is no longer learnable). Two arms (C1-sr, C2-sr), same 25M recipe, then the identical CLadder re-test. The pre-registered prediction was*b→*0with*a*intact. **In-distribution, the repair works—for the probe-only arm.**C2-sr reaches slope ratio +0*.*74 on the training-distribution probe battery (vs. +0*.*18 non-sr): forced to read the sign from interventional evidence, the model does. C1-sr flatlines at *−*0*.*06: with observational records present, probe learning is*diluted to nothing*—the dilution endpoint of the E5 dose curve (§5.6), not capture, since no gain ever materializes to be captured. **Out-of-distribution, the prediction is falsified.**On CLadder the offset does not move: *b*= +0*.*21*±*0*.*02 across all four arm*×*suite cells, indistinguishable from the non-sr arms (+0*.*233). The gain tells a split story. C2-sr carries genuine ATE signal that the*flip-the-observation*heuristic cannot explain: partial Corr(∆b*,*ATE*|*obs) = +0*.*37 against the heuristic’s ceiling of +0*.*17 on this suite (Corr(ATE*,*obs) =*−*0*.*17); the offset is no query-grid artifact either—on a symmetric grid *{−*1*,*+1*}* it persists (*b*= +0*.*36 C2-sr / +0*.*33 C2; mean ratio +0*.*616 / *−*0*.*184)—while the apparent negative-world sign-reading gain (11%*→*30% at grid*{*0*,*1*}*) does not (negative predictions vanish), so we do not claim it. C1-sr collapses onto the observational sign (partial Corr(∆b*,*obs*|*ATE) = +0*.*66; meanratio true*−*0*.*66). **Verdict: the prior is two-layered.**An*in-distribution layer*(“effects are positive”) is removed by sign randomization, though the unmasked sign competence transfers only partially; an*out-of-distribution* *default*(“answer positive when the evidence machinery fails to engage”) is immune to the same fix. Since the pure-observational baseline shows no offset on the identical pipeline (*b≈*0;§5.7), the default is induced by interventional training itself; its micro-mechanism remains open (§7).
### 6 DISCUSSION

**Mechanism statement.**(1) Interventional evidence is*sufficient*to teach causal-direction interpolation (C2: 41/50, true reversal rate *≈*0). (2) The observational-correlation prior*suppresses*the use of interventional evidence at inference time (C1: 18/50, 19 reversed), independently of probe dose (E1a). (3) The suppression is an*inference-time*phenomenon: erasing observational evidence immediately releases the suppressed ability (E1b: +0*.*56). (4) The shortcut is*distributionally* *rational*—the observational correlation is correct for most random queries (confounded pairs are only *∼ /n*)—and deepens with training. (5) Training-distribution priors are*two-layered*: the learnable in-distribution regularity (“effects are positive”) can be removed by sign randomization, but an

<u>Preprint</u>

out-of-distribution default persists underneath it (§5.8)—repairing training statistics does not repair deployment-time fallback. (6) Activation patching localizes the switch to the observational-record (obs) rows: transplanting zero-context activations at the obs rows of layers 2–3 releases the suppressed slope (*R≈*+1*.*0; +0*.*96 on a second seed), non-obs rows and the final layer release little, and the effect resists sparse head-level decomposition (AppendixH). In one sentence: *the capability lives in* *the weights; the switch lives in the context.*

**Implications for pretraining data practice.**Mixture-ratio optimization assumes capability scales with its signal; we show the bottleneck lies instead in the*evidence ecology of the inference-time* *context*: interventional data remains necessary (C2 proves sufficiency), yet observational content at deployment can switch the learned ability off (E5)—motivating context engineering and evidence-type gating.

### 7 LIMITATIONS

(1)**Fully synthetic**: a single SCM family; the CLadder audit (§5.7) covers binary textbook graphs, not natural language. (2)**Gain contraction at scale**: absolute interventional gains shrink 2–4*×* at 1B in both arms; the suppression survives only as a reversal-rate elevation, its cause (budget vs. recipe) unseparated (§5.5); the 1B checkpoint retains format fragility (parse 0.88). (3)**The OOD** **positive default is mechanism-unknown**(§5.8): sign randomization removes the in-distribution prior layer but not the out-of-distribution default; why it is*positive*is unidentified, and C2-sr’s apparent negative-world improvement is grid-fragile. (4)**Cross-scale identity of suppressed worlds**: stable across seeds at 25M (*r*= +0*.*83, matched protocol; strong reversals 11/11) but not across scale (§5.5). (5)**Dose–effect unconfirmed**: the 10-world “suppression *∝|*observational correlation*|*” did not replicate at 50 (*p*= 0*.*14). (6)**Format stress and seed variance**: parsing degrades at extended contexts (*nobs*= 8: 0.16; four-state: 0.74–0.86); C1’s ∆ varies *∼*0*.*5 across seeds—per-world claims defer to the multi-seed table.
### AI USESTATEMENT

A large-language-model assistant was used to help draft and copy-edit the manuscript, to adversarially proof-check its claims against the underlying experimental data, and to develop and debug the evalua- tion and patching code. All scientific claims, experimental design, data, analyses, and conclusions were made and verified by the authors, who take full responsibility for the content of this paper.

### REPRODUCIBILITYSTATEMENT

All evaluation artifacts, code fingerprints (md5), and protocol notes are documented in AppendixB; the activation-patching experiments follow preregistered protocols and decision logs summarized in AppendixH.

### REFERENCES

Ekin Akyurek, Dale Schuurmans, Jacob Andreas, Tengyu Ma, and Denny Zhou. ¨ What learning algorithm is in-context learning? investigations with linear models. In*The Eleventh International* *Conference on Learning Representations (ICLR 2023)*, 2023.

Vahid Balazadeh, Hamidreza Kamkari, Valentin Thomas, Benson Li, Junwei Ma, Jesse C. Cresswell, and Rahul G. Krishnan. Amortized causal effect estimation via in-context learning. In*Advances in* *Neural Information Processing Systems 38 (NeurIPS 2025)*, 2025.

Jin Du, Li Chen, Xun Xian, An Luo, Fangqiao Tian, Ganghua Wang, Charles Doss, Xiaotong Shen, and Jie Ding. Ice cream doesn’t cause drowning: Benchmarking LLMs against statistical pitfalls in causal inference.*arXiv preprint arXiv:2505.13770*, 2025.

Shivam Garg, Dimitris Tsipras, Percy Liang, and Gregory Valiant. What can transformers learn in-context? a case study of simple function classes. In*Advances in Neural Information Processing* *Systems 35 (NeurIPS 2022)*, 2022.

<u>Preprint</u>

Zhijing Jin, Yuen Chen, Felix Leeb, Luigi Gresele, Ojas Kamal, Zhiheng Lyu, Kevin Blin, Fernando Gonzalez Adauto, Max Kleiman-Weiner, Mrinmaya Sachan, and Bernhard Scholkopf. CLadder: ¨ Assessing causal reasoning in language models. In*Advances in Neural Information Processing* *Systems 36 (NeurIPS 2023), Datasets and Benchmarks Track*, 2023.

Zhijing Jin, Jiarui Liu, Zhiheng Lyu, Spencer Poff, Mrinmaya Sachan, Rada Mihalcea, Mona Diab, and Bernhard Scholkopf. ¨ Can large language models infer causation from correlation? In*The* *Twelfth International Conference on Learning Representations (ICLR 2024)*, 2024.

Emre Kıcıman, Robert Ness, Amit Sharma, and Chenhao Tan. Causal reasoning and large language models: Opening a new frontier for causality.*arXiv preprint arXiv:2305.00050*, 2023.

Andrew Lampinen, Stephanie Chan, Ishita Dasgupta, Andrew Nam, and Jane Wang. Passive learning of active causal strategies in agents and language models. In*Advances in Neural Information* *Processing Systems 36 (NeurIPS 2023)*, 2023.

Haodong Liang, Krishnakumar Balasubramanian, and Lifeng Lai. Transformers handle endogeneity in in-context linear regression. In*The Thirteenth International Conference on Learning Represen-* *tations (ICLR 2025)*, 2025.

Shayne Longpre, Kartik Perisetla, Anthony Chen, Nikhil Ramesh, Chris DuBois, and Sameer Singh. Entity-based knowledge conflicts in question answering. In*Proceedings of the 2021 Conference* *on Empirical Methods in Natural Language Processing (EMNLP 2021)*, 2021.

Judea Pearl.*Causality: Models, Reasoning, and Inference*. Cambridge University Press, 2 edition,

2009.
Jake Robertson, Arik Reuter, Siyuan Guo, Noah Hollmann, Frank Hutter, and Bernhard Scholkopf. ¨ Do-PFN: In-context learning for causal effect estimation. In*Advances in Neural Information* *Processing Systems 38 (NeurIPS 2025)*, 2025.

Aniket Vashishtha, Abhinav Kumar, Atharva Pandey, Abbavaram Gowtham Reddy, Kabir Ahuja, Vineeth N Balasubramanian, and Amit Sharma. Teaching transformers causal reasoning through axiomatic training.*arXiv preprint arXiv:2407.07612*, 2024.

Jian Xie, Kai Zhang, Jiangjie Chen, Renze Lou, and Yu Su. Adaptive chameleon or stubborn sloth: Revealing the behavior of large language models in knowledge conflicts. In*The Twelfth* *International Conference on Learning Representations (ICLR 2024)*, 2024.

### A A VISUALTOUR OF THESIMPSONCONSTRUCTION

### B REPRODUCIBILITYCHECKLIST

**Code fingerprints (md5).** eval.py = e9c347704ef8ddf9524c63ddb06bf094; eval ckpt.py = f877ac2b3e7a02c3d910f29b7df69bde; mech patch.py = 542e2dd7d0e88081c6b8758bb63cb8c0 (AppendixH). All final evaluations use these versions with*nrep*= 8(*nrep*= 4for patching).

**Seed domains.**Train/val/test/novel-topology world seeds are pairwise disjoint. The 50 test worlds are make world(SEED TEST + i,*ρ*= 0.9, curriculum = 1,*n∈*[5*,*12]) for *i*= 0*,...,*49; world identities (hashes) are logged in each evaluation artifact.

**Cache caveat.**The generator’s intervention-value cache persists across calls; offline replay of the evaluation stream must re-seed it explicitly, otherwise identical protocols drift between runs.

**Evaluation artifacts.**Every number in this paper traces to a logged evaluation file con- taining the checkpoint path, protocol flags, the corrected hit summary, and the per-world eff/slope/ratio/ratio truelines (50 worlds*×*8 final arms, plus E1/E5 and novel-topology).

Preprint

Figure 5: One sampled evaluation world (*ρ*= 0*.*9), end to end.

p

<u>(a)</u>Structure: the generator injects
a confounded triple (*Z,X,Y*) with *X*=*ρA*tanh(*Z*) + 1*−ρ² U* and *Y*=*−ρB*tanh(*Z*) + *C*tanh(*X*) + 0*.*3*U*; red dashed edges are the confounding paths, the green edge is the causal path.

**(b)**An observational sample from the*same*world shows a strong negative trend (corr =*−*0*.*86).**(c)** Interventional probes *do*(*X*) on the same world reveal the positive causal effect (two-point estimate +0*.*53). The sign conflict between (b) and (c) is the Simpson trap of equation1: a reader that copies observation answers “does*X*raise*Y*?” backwards.
### C NOISE-FLOORSIMULATION

Simulating a perfect least-squares interpolator against the oracle generator (4 aligned probe records per query *x₀*, 5-point regression grid; 20 repetitions of the 10-world protocol) gives a single-shot sign-error rate of 2.6/10 (26%). Evidence averaging over *nrep∈{*1*,*2*,*4*,*8*}* draws reduces Var[˜*µ*] by*≈*1*/nrep*(floors 26% / 17% / 12% / 9%); we adopt*nrep*= 8(floor 0.9/10) for all final results.

### D CROSS-SEEDREVERSED-WORLDOVERLAP

Across C1 seeds the reversed-world sets overlap far beyond chance: s0*↔*s2 in 15/19 (hypergeometric *p*= 4*.*2e*−*6; per-world ratio true Pearson *r*= +0*.*872, *p*= 1*.*8e*−*16). The matched-protocol s0*↔*s1 overlap (14/18; strong reversals 11/11; boundary flow within *|*slope*|<*0*.*15) is reported in §5.4.

**Cross-scale turnover**(25M *→* 1B; Table3). The reversed set turns over symmetrically (11 out / 8 in; McNemar *p*= 0*.*65), per-world slopes are rank-uncorrelated (Spearman *r*= +0*.*084, *p*= 0*.*59, *n*= 44; cross-seed *r*= +0*.*87), and survival is non-monotone in 25M strength—reshuffling, not attenuation under gain contraction.

Table 3: Cross-scale turnover of the C1 reversed set (25M *→* 1B, identical 50-world protocol; classes

by the*±*0*.*05slope dead zone).

|Fate of the 19 reversed-at-25M worlds|n|Detail|
|---|---|---|
|Survived (rev → rev)||6 strength-scattered (ranks 2–19/19); weakest ( − 0. 057) persists|
|Lost to flat||7 incl. − 0. 564 → +0. 027, − 0. 398 →− 0. 026|
|Flipped to hit||4 incl. − 0. 398 → +0. 172, − 0. 069 → +0. 337|
|Lost to parse failure||2 incl. strongest reversal ( − 0. 681); Fisher p = 1. 0|
|New reversals at 1B (from non-rev)||8 4 from flat, 4 from hit (incl.+0. 293 / + 0. 318 → rev)|

### E E5 PAIREDTABLES

### F PROTOCOL-TRANSPARENCYNOTE: CONTEXT-LENGTHMISMATCH IN THE C1 ARM

The C1 training pipeline constructsOBS PROBEcontexts from 4 observational records + 2 probe records (*nprobe*defaults to 2), i.e. an 8-line format; our initial battery queried with *nprobe*= 4 (12

<u>Preprint</u>

Table 4:**(a)**E5 dose titration on the C1 checkpoint (paired *n*= 37; *nprobe*= 4, *nrep*= 8).**(b)**E5

four-state content manipulation (paired*n*= 33;*nobs*= 4; states as defined in §5.6).

|State|Hit|Flat|Rev|meanratio true|
|---|---|---|---|---|
|SAME 16||8|9+0|. 059|
|CROSS 21||6|6+0|. 192|
|SCRAMBLE|20|8|5+0|. 203|
|ZERO 25||7|1+0|. 378|

|n obs|Hit|Flat|Rev|meanratio true|
|---|---|---|---|---|
|1|31|5|1+0|. 472|
|2|22|12|3+0|. 204|
|4|17|9|11+0|. 037|

lines)—an out-of-distribution extrapolation for C1 (C2 is unaffected: its probe branch always uses the training context length); we therefore report C1 under the in-distribution *nprobe*= 2 protocol throughout (§5.2, §5.5).

Two consequences.**(i) The main result is protocol-robust**: re-evaluating C1 at 25M under *nprobe*= 2 reproduces the out-of-distribution battery exactly (18/13/19, mean ratio true*−*0*.*092, ∆ +0*.*041)— the 12-line evaluation did not inflate suppression, and probe-dose doubling 2*→*4 provides zero rescue under observational evidence (a dose dual to§5.6).**(ii) Scale-dependent format fragility**: the 1B C1 checkpoint fails to extrapolate to 12 lines (parse 0.32; missing variables, mis-closed tags) and stays fragile even in-distribution (parse 0.88), while 25M parses perfectly under both—a scale-by-recipe robustness issue (lr 3e*−*4 vs. 6e*−*4), not a causal finding; all 1B conclusions use the in-distribution protocol.

### G NEGATIVE-RESULTREGISTRY

**E1c (C2 + obs injection)**: parse rate 0 (obs format out-of-distribution for a probe-only model); arm invalid, set aside.**Dose–effect non-replication**: “suppression *∝|*Corr*obs|*” (10 worlds) fails at 50 (*|r|* 0.770 rev vs. 0.729 hit, *p*= 0*.*14;§7).**Ablation-A target-node confusion**: rejected (*|*eff(*Z→Y*)*|/|*eff(*X→Y*)*| lower*in the reversed group). *nobs*= 8 **titration arm**: lost to parse-rate collapse (0.16; long-context format stress).

### H MECHANISMREPORT: ACTIVATION-PATCHINGLOCALIZATION

**Protocol**(preregistered; each stage’s gates were fixed before that stage’s data, with one documented revision after the engine self-test and before any downstream data). For each reversed world we measure paired baselines—the *do*()-slope under the same-world obs context (*s*same, suppressed) and under zeroed obs (*s*zero, released)—then transplant activations from the zero-condition run into the same-condition run at a candidate site and score the release ratio *R*= (*s*p*−s*same)*/*(*s*zero*−s*same) (*R*=1: full release; worlds with *s*zero*−s*same*≤*0*.*05 excluded by guard). Sites: residual-stream obs-record vs. non-obs positions per layer (G1); individual heads/MLPs selected on dev, verified on holdout (G2). *nrep*= 4; reversed worlds from the formal 50-world archive (s0: 19, deterministic dev/holdout split; s1: all 18, no split).

**Gate results**(two seeds; Figure6a).**G1 layer scan**(s0 dev, *n*= 8*/*10): obs rows L0–L3 *R*= +1*.*01– +1*.*04, L4–L6 0*.*81–0*.*92, L7 exactly 0*.*000; non-obs rows *≤*+0*.*21 at L0–L3 (+0*.*36 max) *⇒* PASS.**G2 component circuit**(s0 holdout, *n*= 8*/*9): dev-selected top-8 union *R*= +0*.*20 (CI95 [*−*0*.*43*,*+0*.*67]; vs. random ∆ = +0*.*25, permutation *p*= 0*.*19); reverse patch *R*rev= +0*.*14 *⇒* FAIL: no sparse circuit isolated under this search.**G1-s1 cross-seed confirm**(s1 all rev, *n*= 17*/*18): L2/L3 obs *R*= +0*.*98*/*+ 0*.*94 (L0–L6 obs rows all +0*.*94 to +1*.*04); obs *−* non-obs ∆ = +1*.*20*/*+ 1*.*13; non-obs all negative (*−*0*.*13to*−*0*.*26); L7 exactly0*.*000*⇒*PASS.

**Controls and reading.**Component-stage patches are surgically clean (KL sentinel max 2*.*9e*−*7 nats) and leave hit worlds intact (4/5 signs, mean *|*∆slope*|*= 0*.*15); a random 3-head baseline at L3 obs reaches *|R|≈*0*.*4, calibrating the G2 null. Obs-directed attention mass is U-shaped (L0 0*.*484*→* L2/L3 0*.*064*/*0*.*072*→* L7 0*.*560) but leverage is not: it saturates from L0 through the barely-reading middle layers and vanishes exactly at L7, where reading peaks (Figure6b). We therefore claim a *row-level, distributed*switch and*sufficiency only*—these data do not speak to necessity.

<u>Preprint</u>

Figure 6:**(a)**Release ratio *R* of zero-condition activation transplants, by layer and row type (s0

dev / s1 all-reversed; *nrep*= 4). The switch travels with the obs rows (*R≈*+1*.*0 from L0 through L6, both seeds) and vanishes exactly at L7; black boxes mark the preregistered L2/L3 obs cells.

**(b)**Obs-directed attention mass by layer (s0): reading peaks at L7, where *R*= 0*.*00—reading *̸*= leverage.
