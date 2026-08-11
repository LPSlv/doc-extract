# Effect of wind on prey-predator dynamics with group defense and additional food strategy

1 2 ∗1

#### Anushree Hazra, Aniket Banerjee, and Debaldev Jana

1 Department of Mathematics, Ramakrishna Mission Vivekananda Educational and Research Institute, Belur Math, West Bengal 711202, India

#### Sorbonne Université, CNRS, Laboratoire Jacques-Louis Lions (LJLL), 75005 Paris, France

**Abstract**

Wind plays a crucial role in changing prey defense strategy and predation efficiency. We develop and analyze a prey-predator model that incorporates wind-driven environmental effects, prey group defense, and an additional food strategy for the predator. Wind intensity is assumed to modulate predation efficiency, while prey aggregation reduces predation pressure at high densities, and supplementary food alters predator growth independent of prey abundance. We investigate the existence and stability of biologically feasible equilibrium points. The analysis reveals that wind strength and additional food supply can induce stability switches, oscillatory dynamics via Hopf bifurcation, and more complex behaviors including saddle–node and Bogdanov–Takens bifurcations. Our results demonstrate that environmental forcing and resource supplementation jointly shape predator persistence and population fluctuations, providing theoretical insights into ecological management strategies involving food enrichment under variable environmental conditions.

### 1 Introduction

Prey–predator interactions are fundamental components of ecological systems and play a key role in shaping population dynamics and ecosystem structure [34, 18, 4]. In natural ecosystems, however, population dynamics are strongly influenced by environmental factors [30, 9, 25, 19] that are often neglected in basic models. Among these factors, wind plays a significant role in shaping ecological interactions, particularly in open terrestrial and aquatic environments [2]. Wind can affect prey– predator dynamics by altering movement patterns, dispersal rates, encounter frequencies, and foraging efficiency. For instance, wind-driven transport may facilitate or hinder predator–prey encounters,

## arXiv:2607.24285v1 [q-bio.PE] 27 Jul 2026

modify spatial distribution, and influence the energetic cost of movement for both species. Motivated by these ecological considerations, several studies have emphasized the importance of incorporating environmental forcing into population models [7, 10, 3, 31]. In this context, wind can be modeled as an external factor that modifies interaction terms, movement behavior, or species growth

∗ Corresponding author: debaldevjana.jana@gmail.com

rates. Such modifications lead to nonlinear dynamical systems whose qualitative behavior may differ significantly from that of classical prey–predator models. The role of additional food for predators has received considerable attention, particularly in bio- logical control theory [28, 27, 29]. The provision of supplementary food, either naturally occurring or artificially supplied, modifies both the predator’s numerical response and the functional response [23, 13]. Several studies have demonstrated that the quality and quantity of additional food can either stabilize or destabilize predator-prey interactions [26, 27]. It has also been shown that supplementary food may lead to counterintuitive outcomes such as prey extinction or the emergence of complex bi- furcation structures depending on parameter regimes [21, 33]. However, most of these studies assume constant environmental conditions and do not explicitly incorporate adaptive prey defense mechanisms within the same modeling framework. Although substantial progress has been made in modeling additional food, group defense, and nonlinear functional responses independently, an integrated framework combining these mechanisms with wind-modulated predation remains largely unexplored. In particular, the interaction between wind-dependent olfactory efficiency and supplementary food may generate novel stability thresholds and higher codimension bifurcations that cannot be captured by models lacking environmental mod- ulation. We develop a prey-predator model to understand the dynamical change in the species population when the prey adopts a group defense strategy as an anti-predator response in the presence of an additional food source for the predator. The effect of wind is studied and is important to understand its implications for population dynamics. We assume the prey population follows logistic growth in the absence of the predator. The ecosys- tem has a carrying capacity *k*, which takes into account that there is a limit to the amount of resources for the populations in the ecosystem, which stops the unbounded growth of the prey population in the absence of a predator. The intrinsic growth rate of the prey population is assumed to be the positive constant *r*. The logistic growth of the prey population simplifies and takes into account the growth, natural mortality, and intraspecific competition of the prey population. 8 > > <u>dx</u> = *rx* 1 *−* <u>x</u> *− yp*(*x*)*,* > <*k* *dt* <u>dy</u>

(1)
> > = *q*(*x*)*y − dy,* > : *dt* *x*(0) *>* 0*, y*(0) *>* 0*.*

We assume the group defense strategy to be modeled as Holling type IV or Monod-Haldane type functional response([11, 24]). The functional response to observe the study of group defense can be <u>βx</u> stated as *p*(*x*) = 2 where *β* is the rate of predation of the prey, *b* is the rate of group defense *a* + *bx* + *x* by the prey population. As *b* increases, *p*(*x*) decreases, thereby reducing predation. So, group defense as an anti-predator response sensitivity is studied through the parameter *b*. The additional food for the predator is assumed to exist or maybe be provided externally with the quantity *ξ* and quality *α* <u>1</u>. The additional food source decreases the predation function response, i.e., *p*(*x*) decreases with an increase in *ξ*, as the predator has an alternate food source for predation, while it increases the predator growth by providing nutrients, i.e., *q*(*x*) increases with the increase of *ξ*. Such models have been studied extensively in the literature [26, 27, 21]. Thus, a developed model with the effect of group defense and the presence of additional food can be given by,

> *dx xy* >*x* > = *rx − −,* >*k* < *dt* 1 + *αξ* + *bx* + *x* <u>dy β(x + ξ)y</u>

(2)
> = *− dy,* >2 > *dt* 1 + *αξ* + *bx* + *x* > : *x*(0) *>* 0*, y*(0) *>* 0*.*

Beyond biotic interactions, abiotic environmental factors play a crucial role in shaping predator- prey encounters. Wind, in particular, influences olfactory communication [1, 14], dispersal patterns [8, 20], and encounter rates in terrestrial and aerial ecosystems [32]. Empirical studies suggest that wind speed affects the transmission of chemical cues in a non-monotonic manner. At very low wind speeds, odor plumes disperse poorly, limiting detection, while at very high speeds, turbulence disrupts odor gradients and reduces signal reliability. Consequently, olfactory efficiency often exhibits an optimal intermediate wind speed. Despite such biological evidence, wind effects are rarely mechanistically incorporated into deterministic prey-predator models. Environmental variability is often modeled as stochastic noise or periodic forcing, without an explicit functional dependence between wind speed and predation efficiency. Motivated by these considerations, we propose and analyze a prey-predator model that incorpo- rates logistic prey growth, group defense represented via a Monod-Haldane type functional response, additional food of specified quality and quantity for the predator, and a wind-dependent modulation of predation efficiency described through a biologically motivated function. The wind function reflects the empirically observed relationship between wind speed and olfactory signal reception and directly modifies both predation and predator growth terms. In addition, a density-dependent mortality term associated with supplementary food consumption is included to capture potential ecological costs. Thus, after modification, our model for the study is given as follows: 8 > *dx ϕ*(*w*)*xy* >*x* > = *rx* 1 *− −,* > *k* 2 < *dt* 1 + *αξ* + *bx* + *x* <u>dy βϕ(w)(x + ξ)y</u> (3) 2 > = *− dy − cξϕ*(*w*)*y ,* >2 > *dt* 1 + *αξ* + *bx* + *x* > : *x*(0) *>* 0*, y*(0) *>* 0*.*

The main objective of this work is to provide a rigorous analytical and numerical investigation of the resulting dynamical system. We establish positivity and uniform boundedness of solutions to ensure ecological feasibility. We determine the existence and local stability conditions of all equilib- ria, including trivial, boundary, and interior steady states. We further investigate local bifurcations, including transcritical, saddle-node, and Hopf bifurcations, with respect to biologically relevant pa- rameters. Moreover, we analyze higher-codimension global bifurcations, including cusp singularities and Bogdanov–Takens bifurcations, thereby revealing the possible emergence of unstable limit cycles and homoclinic loops. Numerical simulations are performed to illustrate how different wind-dependent functional forms influence extinction, coexistence, and oscillatory dynamics. The paper is organized as follows. Section 8.1 establishes positivity and uniform boundedness of solutions. Section 2 analyzes the existence and local stability of equilibria. Section 3 is devoted to local bifurcation analysis, while Section 4 investigates global bifurcation phenomena including cusp and Bogdanov–Takens bifurcations. Numerical simulations are presented in Section 5, followed by an ecological interpretation of wind effects in Section 6. Finally, Section 7 concludes the paper with discussion and future perspectives.

### The existence and local stability of the equilibria of the system (3)

The existence and local stability of the equilibrium points of the system (3) are established under the appropriate parametric conditions described in Table 1.

### 3 Analysis of local bifurcation

#### 3.1 Transcritical bifurcation

**Theorem 3.1.** *The model* (3) *experiences a transcritical bifurcation near the axial/ prey only equi-* 2 <u>rcξ(1 + αξ + bk + k²)</u>

|d(1+αξ+bk+k)|3|
|---|---|
|β(k+ξ)|2|

(*T C*) *librium point E₂*(*K,*0) *in ϕ*(*w*) = *ϕ₂* (*w*) = *with ϕ*(*w*) *̸*= *βk*(*−*1 *− αξ* + *bξ* + 2*kξ* + *k*) *and* (*−*1 *− αξ* + *bξ* + 2*kξ* + *k²*) *̸*= 0*.*

*Proof.* A transcritical bifurcation occurs between the coexistence/interior equilibrium point *E* *∗* and the prey only/axial equilibrium point *E₂* with respect to the bifurcation parameter *ϕ*(*w*) and these (*T C*) two equilibrium points exchange their stability at that point *ϕ*(*w*) = *ϕ₂* (*w*). Now we calculate the Jacobian matrix *J₂* in *E₂* of model (3), that is,

0 1 *ϕ*(*w*)*k* *−r −* 2 B 1 + *αξ* + *bk* + *k* C *J₂* = @ A*.* <u>βϕ(w)(k + ξ)</u> 0 *−d* + 2 1 + *αξ* + *bk* + *k*

From the above it is clear that one eigenvalue of the above Jacobian matrix is negative and the other <u>d(1 + αξ + bk + k²)</u> <u>βϕ(w)(k+ξ)</u> *T C* zero iff *−d* + 1+*αξ*+*bk*+*k*2 = 0, that is, iff *ϕ*(*w*) =, which gives *ϕ*(*w*) = *ϕ₂* (*w*) = *β*(*k* + *ξ*) 2 *T* <u>d(1 + αξ + bk + k)</u> *T* <u>−ϕ(w)k</u>. We obtain *W* = (0*,*1) and *V* = 2 *,*1, where W and V *β*(*k* + *ξ*) *r*(1 + *αξ* + *bk* + *k*) *T* represent the eigenvectors related to the zero eigenvalue of the matrices *J₂* and *J₂*, respectively. Now,

|T|(T C)|||
|---|---|---|---|
|ϕ(w)||||
|T|(T C)|||
|ϕ(w)|X|2||
|T 2|(T C) X||2 3|
|||3||
|||2||

*W f* (*E₂, ϕ₂* (*w*)) = 0*,* <u>β(k + ξ)</u> *W* [*Df* (*E, ϕ₂* (*w*))*V*] = *̸*= 0*,* 1 + *αξ* + *bk* + *k* <u>2βkϕ(w) (1 +</u> 2 <u>αξ − bξ − 2kξ − k²)</u> *W* [*D f* (*E, ϕ₂* (*w*))(*V, V*)] = *−*2*cξϕ*(*w*) *− ̸*= 0*,* *r*(1 + *αξ* + *bk* + *k*) <u>rcξ(1 + αξ + bk + k²)</u> 2 *that is if f ϕ*(*w*) *̸*= *and* (*−*1 *− αξ* + *bξ* + 2*kξ* + *k*) *̸*= 0*.* *βk*(*−*1 *− αξ* + *bξ* + 2*kξ* + *k*)

Now we can say that the system(3) experiences a transcritical bifurcation around *ϕ*(*w*) at *ϕ*(*w*) = *ϕ* *T C* 2(*w*) according to Sotomayor’s Theorem ([22]).

**Theorem 3.2.** *The model* (3) *transcritical bifurcation is experienced near the axial/ prey only equi-* (*T C*) <u>(1+αξ)(d+rcξ(1+αξ))βϕ(w)ξ</u> *librium point E₁*(0*, y₁*) *at ϕ*(*w*) = *ϕ₁* (*w*) = *βξ* *with* 1 + *αξ − bξ ̸*= 0 *and > d* 1 + *αξ* <u>(1 + αξ)[bdk − rcξ(1 + αξ)</u> 2 <u>]</u> *and ϕ*(*w*) *̸*= *and* (1 + *αξ −* 2*bξ*) *̸*= 0*.* *βk*(1 + *αξ −* 2*bξ*)

##### Proof. Similar to the theorem 3.2.

#### 3.2 Saddle-node bifurcation

Now, the system(3) can be represented as, 8 > > *dx* *x* *ϕ*(*w*)*xy* > > = *rx* 1 *−* *k* *−* 2 = *p*(*x*) *F* (*x*) *− y,* < *dt* 1 + *αξ* + *bx* + *x* <u>dy βϕ(w)(x + ξ)y</u> 2(4) > > = 2 *− dy − cξϕ*(*w*)*y* = *y h*(*x*) *− cξϕ*(*w*)*y,* > > *dt* 1 + *αξ* + *bx* + *x* : *x*(0) *>* 0*, y*(0) *>* 0*.*

*ϕ*(*w*)*x r x* 2 *βϕ*(*w*)(*x* + *ξ*) where *p*(*x*) = 2, *F* (*x*) = 1*−* (1+*αξ*+*bx*+*x*), *h*(*x*) = 2 *−d*. 1 + *αξ* + *bx* + *x ϕ*(*w*) *k* 1 + *αξ* + *bx* + *x*

The corresponding Jacobian matrix is

*p* *′*

(*x*)(*F* (*x*) *− y*) + *F*
*′*

(*x*)*p*(*x*) *−p*(*x*)
*J* =*′.* *h* (*x*)*y* (*h*(*x*) *− cξϕ*(*w*)*y*) *− cξϕ*(*w*)*y*

For interior *E* *∗* = (*x* *∗* *, y* *∗* ) with *y* *∗* = *F* (*x* *∗* ), we have that the Jacobian matrix becomes

*∗F* *′* (*x* *∗* )*p*(*x* *∗* ) *−p*(*x* *∗* ) *J* =*′ ∗ ∗ ∗.* *h* (*x*)*F* (*x*) *−cξϕ*(*w*)*F* (*x*)

Hence, *tr*(*J* *∗* ) = *F* *′* (*x* *∗* )*p*(*x* *∗* ) *− cξϕ*(*w*)*F* (*x* *∗*

)*,* (5)
*det*(*J* *∗* ) = *p*(*x* *∗* )*F* (*x* *∗* ) *h* *′* (*x* *∗* ) *− cξϕ*(*w*)*F* *′* (*x* *∗*

)*.* (6)
**Theorem 3.3.** *The model* (3) *has a saddle-node bifurcation at interior equilibrium E* *∗* (*x* *∗* *, y* *∗* ) *when* *∗ ∗ ∗ ∗*2 *−*1 *SN* <u>rcξ</u> *cξ*(*b* + 2*x*)*y* <u>β(1 + αξ − bξ − 2ξx − x)</u> *ϕ*(*w*) = *ϕ∗*(*w*) = *∗ ∗*2 2 *−* *∗ ∗*2 3 *and* *k* (1 + *αξ* + *bx* + *x*) (1 + *αξ* + *bx* + *x*) *∗ ∗ ∗ −*1 *x* (*b* + 2*x*

|rx|)||||||||
|---|---|---|---|---|---|---|---|---|
||||∗|∗ 2||∗|∗2|∗|
|∗|∗ ∗ ∗ 2|∗2 2|∗ ∗ ∗2|3 ∗|||||

*∗ ∗* 2 *∗ ∗*2 *∗* *ϕ*(*w*) *̸*= *− cξ −,* (*x* + *ξ*)(*b* + 2*x*) *̸*= (1 + *αξ* + *bx* + *x*)(*b* + 3*x* + *ξ*) *ky* (1 + *αξ* + *bx* + *x*) <u>rcξ(k − b − 3x)(1 + αξ + bx + x</u> *∗*2 <u>)</u> *and ϕ*(*w*) *̸*= *∗* *.* *βk*[(*x* + *ξ*)(*b* + 2*x*) *−* (1 + *αξ* + *bx* + *x*)(*b* + 3*x* + *ξ*)]

*Proof.* For the system (4) to undergo a saddle-node bifurcation at the interior equilibrium point *E* *∗* (*x* *∗* *, y* *∗* ), the Jacobian matrix *J* *∗* at (*x* *∗* *, y* *∗* ) must have one zero eigenvalue and one nonzero (positive *∗ ∗*

|or negative) eigenvalue. Therefore, det(J|||) = 0 and tr(J|) ̸= 0.||
|---|---|---|---|---|---|
|||′ ∗ T||∗ ∗|∗ T ∗T|

Now we obtain *V* = (1*, F* (*x*)) and *W* = (*cξϕ*(*w*)*F* (*x*)*, −p*(*x*)), where V and W represent the eigenvectors related to the zero eigenvalue of the matrices *J* and *J* respectively. Now

*T ∗ SN ∗ ∗* 2 <u>dp(x</u> *∗* <u>)F (x</u> *∗* <u>)</u> *W fϕ*(*w*)(*x, ϕ∗*(*w*)) = *−cξp*(*x*)*F* (*x*) *−* *SN* *̸*= 0*,* *ϕ∗*(*w*)

|T|∗ SN|∗ ∗|SN|′′ ∗|′′ ∗||SN|′′ ∗|′′ ∗|
|---|---|---|---|---|---|---|---|---|---|
||∗||∗ ∗|∗|∗2 3||∗|||
|∗|SN ∗ ∗ 2|∗ 2 ∗ ∗2|∗|∗|∗2|∗||||
|||SN||||||||
|||∗||||||||

*W* [*Df²*(*x, ϕ* (*w*))(*V, V*)] = *p*(*x*)*F* (*x*) *cξϕ* (*w*)*F* (*x*) *− h* (*x*) *̸*= 0 *if f cξϕ* (*w*)*F* (*x*) *̸*= *h* (*x*)*,*

<u>rcξ(k − b − 3x)(1 + αξ + bx + x)</u> that is iff *ϕ* (*w*) *̸*= *∗* and *βk*[(*x* + *ξ*)(*b* + 2*x*) *−* (1 + *αξ* + *bx* + *x*)(*b* + 3*x* + *ξ*)] (*x* + *ξ*)(*b* + 2*x*) *̸*= (1 + *αξ* + *bx* + *x*)(*b* + 3*x* + *ξ*)*.* As it satisfies the condition of Sotomayor’s Theorem ([22]), system (4) experiences a saddle-node bifurcation around *ϕ*(*w*) at *ϕ*(*w*) = *ϕ* (*w*).

#### 3.3 Hopf bifurcation

For the system (4) to undergo a Hopf bifurcation at the interior point *E* *∗* = (*x* *∗* *, y* *∗* ), the Jacobian *J* *∗*

at (*x* *∗* *, y* *∗* ) must have a pair of purely imaginary eigenvalues *±iδ₀*. This implies that the determinant of the Jacobian matrix *J* *∗* is positive and the trace of the Jacobian matrix *J* *∗* vanishes. That is, *det*(*J* *∗* ) = *δ₀₂ >* 0 and *tr*(*J* *∗*

) = 0.
##### 3.3.1 Direction of Hopf bifurcation and stability of bifurcating periodic solutions

Under the condition of Hopf bifurcation, *tr*(*J* *∗*

) = 0 and *det*(*J*
*∗*

) *>* 0, which implies as follows:
*F* *′* (*x* *∗* )*p*(*x* *∗* ) = *cξϕ*(*w*)*F* (*x* *∗*

)*.* (7)
We begin by shifting coordinates via the affine transformation *X₁* = *x − x* *∗* and *Y₁* = *y − F*(*x* *∗* ), which brings equilibrium *E* *∗* = (*x* *∗* *, F*(*x* *∗* )). Expanding the system in a Taylor series around *E* *∗*, we obtain the following reduced system: 8 *∗ ′′ ∗* > > ˙*∗ ′ ∗ ∗ ′ ∗ ′ ∗* <u>p(x)F (x)</u> 2 *′ ∗* > > *X₁* = *p*(*x*)*F* (*x*)*X₁ − p*(*x*)*Y₁* + *p* (*x*)*F* (*x*) + *X₁ − p* (*x*)*X₁Y₁*+ > > 2 > >*′′′ ∗ ∗ ′′ ∗ ′ ∗ ′ ∗ ′′ ∗ ′′ ∗*

|F (x )p(x )|F|(x )p (x )|F (x )p (x )||p (x )||||
|---|---|---|---|---|---|---|---|---|
|||||∗ ′′|3 ∗|2||3|
|∗|′ ∗||∗|||′ ∗||2|
|1|||||1|||1|
|∗ ′′′|∗|′′ ∗|||||||
||3|2||3|||||

> <3 2 3 + + *X₁ − X₁Y₁* + *O*(*|X₁, Y₁|*)*,* 6 2 2 2 (8) > > <u>F (x)h (x)</u> > >*Y* ˙ = *F* (*x*)*h* (*x*)*X₁ − cξϕ*(*w*)*F* (*x*)*Y₁* + *X²* + *h* (*x*)*X₁Y₁ − cξϕ*(*w*)*Y* + > > 2 > > > : <u>F (x)h (x) h (x)</u> *X₁* + *X₁Y₁* + *O*(*|X₁, Y₁|*)*.* 6 2 Using the condition of Hopf bifurcation (7), the system (4) becomes (

|1|2|3 2|
|---|---|---|
|1|2 2|3 2|

*X* ˙ = *a₁₀X₁* + *a₀₁Y₁* + *a₂₀X₁* + *a₁₁X₁Y₁* + *a₃₀X₁* + *a₂₁X₁Y₁* + *O*(*|X₁, Y₁|* 4 )

(9)
*Y* ˙ = *b₁₀X₁ − a₁₀Y₁* + *b₂₀X₁* + *b₀₂Y₁* + *b₁₁X₁Y₁* + *b₃₀X₁* + *b₂₁X₁Y₁* + *O*(*|X₁, Y₁|*)*,*

where the coefficients are given by *∗ ′ ∗ ∗ ′ ∗ ′ ∗* <u>p(x</u> *∗* <u>)F</u> *′′* <u>(x</u> *∗* <u>)</u> *′ ∗* *a₁₀* = *p*(*x*)*F* (*x*), *a₀₁* = *−p*(*x*), *a₂₀* = *p* (*x*)*F* (*x*) +, *a₁₁* = *−p* (*x*),

*F* *′′′* (*x* *∗* )*p*(*x* *∗* ) *F* *′′* (*x* *∗* )*p* *′* (*x* *∗* ) *F* *′* (*x* *∗* )*p* *′′* (*x* *∗* ) *p* *′′* (*x* *∗* ) *∗ ′ ∗* *a₃₀* = + +*, a₂₁* = *−*, *b₁₀* = *F* (*x*)*h* (*x*)*,* 6 2 2 2 *F* (*x* *∗* )*h* *′′* (*x* *∗* ) *′ ∗* *F* (*x* *∗* )*h* *′′′* (*x* *∗* ) *h* *′′* (*x* *∗* ) *b₂₀* =, *b₀₂* = *−cξϕ*(*w*), *b₁₁* = *h* (*x*),*b₃₀* =, *b₂₁* =. 2 6 2 Hence, we can write (9) as follows:

|1|∗ ∗ ∗|2|3|2|4|
|---|---|---|---|---|---|
|1||2 2|3|2|4|

*X* ˙ *X₁ a₂₀X₁* + *a₁₁X₁Y₁* + *a₃₀X₁* + *a₂₁X₁Y₁* + *O*(*|X₁, Y₁|*) *Y* ˙ *Y₁ b₂₀X₁* + *b₀₂Y₁* + *b₁₁X₁Y₁* + *b₃₀X₁* + *b₂₁X₁Y₁* + *O*(*|X₁, Y₁|*) = *J* (*x, y*) +*.*

Now, to reduce system (9) to a more canonical form, we apply the transformation <u>−a₁₀ δ₀</u> *X₁* = *X₂* and *Y₁* = *X₂ − Y₂*, ([17]). *a₀₁ a₀₁* Under this transformation, the above system becomes (

|2|2|3|2|
|---|---|---|---|
|2|2|2|3|

*X* ˙ = *−δ₀Y₂* + *A₂₀X₂* + *A₁₁X₂Y₂* + *A₃₀X₂* + *A₂₁X₂Y₂* + *O*(*|X₂, Y₂|* 4 )*,* 2 4 (10) *Y* ˙ = *δ₀X₂* + *B₂₀X₂* + *B₁₁X₂Y₂* + *B₀₂Y₂* + *B₃₀X₂* + *B₂₁X₂Y₂* + *O*(*|X₂, Y₂|*)*,*

where the coefficients are: *a₁₁a₁₀ a₁₁δ₀ a₂₁a₁₀ a₂₁δ₀* *A₂₀* = *a₂₀ −*, *A₁₁* = *−*, *A₃₀* = *a₃₀ −*, *A₂₁* = *−*, *a₀₁ a₀₁ a₀₁ a₀₁* 1 *b₀₂a²*10*a₁₁a²*10*a₁₀a₁₁ b₀₂a₁₀ b₂₀δ₀* *B₂₀* = *− b₂₀a₀₁ − b₁₁a₁₀*+*a₂₀a₁₀*+ *−*, *B₁₁* = +*b₁₁−* 2, *B₀₂* = *−*, *δ₀ a₀₁ a₀₁ a₀₁ a₀₁ a₀₁* *a₁₀ a₂₀a₁₀ b₃₀a₀₁ a₂₁a₁₀* *B₃₀* = *− a₃₀ −*, *B₂₁* = + *b₂₁.* *δ₀ a₀₁ a₁₀ a₀₁*

According to [22][p-353], for system (10), the Lyapunov number is given by <u>3π</u> *α₁* = 2 3*δ₀A₃₀* + *δ₀B₂₁* + *A₁₁A₂₀ − B₁₁*(*B₂₀* + *B₀₂*) *−* 2*A₂₀B₂₀*. 2*δ₀* The direction of the Hopf bifurcation is determined by the sign of the first Lyapunov coefficient *α₁ <* 0, which yields a supercritical Hopf with stable small-amplitude periodic solutions, while *α₁ >* 0 gives a subcritical Hopf with unstable cycles. Thus, the stability of the bifurcating periodic solution directly depends on *α₁*, with supercritical Hopf yielding stable limit cycles and subcritical Hopf yield- ing unstable ones. Numerically, it is shown that, taking (*b, c, d, r, k, α, β, ξ*) = (0.5,0.1,0.1,0.4985,2.5,0.5,0.285,1.5) and for some *ϕ*(*w*), *α₁ >* 0.

Hence, the system (3) exhibits the Hopf Bifurcation at *E* *∗* (*x* *∗* *, y* *∗* ), which is subcritical as *α₁ >* 0 (fig.-5).

### 4 Global bifurcation: Cusp singularity and Bogdanov-Takens bifurcations

For the system (4) to undergo a Bogdanov-Takens bifurcation at the interior point *E* *∗* = (*x* *∗* *, y* *∗* ), the Jacobian *J* *∗* at (*x* *∗* *, y* *∗* ) must have a double zero eigenvalue in a single Jordan block. This implies that both the determinant and the trace of the Jacobian matrix *J* *∗* vanish simultaneously.

That is, *det*(*J* *∗*

) = 0 and *tr*(*J*
*∗*

) = 0.
Now *−*

||∗|∗ ∗||
|---|---|---|---|
|∗|∗|∗|∗2 2|

<u>rx x (b + 2x)</u> *tr*(*J*) = 0 =*⇒ ϕ*(*w*) = *− cξ* (11) *ky* (1 + *αξ* + *bx* + *x*)

and

*∗* *cξ* (*x* *∗* *− k*)(*b* + 2*x* *∗* ) *β*(*k − x* *∗*

)(1 + *αξ − bξ −* 2*x*
*∗* *ξ − x* *∗*2 ) *det*(*J*) = 0 =*⇒* 1 + *∗ ∗*2 + *∗ ∗ ∗*2 2 = 0*.* (12) *k* (1 + *αξ* + *bx* + *x*) *ky* (1 + *αξ* + *bx* + *x*)

**Theorem 4.1.** *If* (*ξ, ϕ*(*w*)) = (*ξ* *CP* *, ϕ* *CP*

(*w*))*, then the positive equilibrium E*
*∗* *=*(*x* *∗* *, F*(*x* *∗* )) *is a cusp* *of co-dimension-2.*

*Proof.* We begin by shifting coordinates via the affine transformation *X₁* = *x − x* *∗* and *Y₁* = *y − F*(*x* *∗* ), which brings the equilibrium *E* *∗* = (*x* *∗* *, F*(*x* *∗* )). Expanding the system in a Taylor series around *E* *∗*, we obtain the following reduced system: 8 *∗ ′′ ∗* > <*X*˙ = *p*(*x* *∗* )*F* *′* (*x* *∗* )*X − p*(*x* *∗* )*Y* + *p* *′* (*x* *∗* )*F* *′* (*x* *∗* ) + <u>p(x)F (x)</u> *X² − p* *′* (*x* *∗* )*X Y* + *O*(*|X, Y |* 3 )*,* 1 1 1 1 1 1 1 1 2 > : ˙ *∗ ′ ∗ ∗* <u>F (x</u> *∗* <u>)h</u> *′′* <u>(x</u> *∗* <u>)</u> 2 *′ ∗* 2 3 *Y₁* = *F* (*x*)*h* (*x*)*X₁ − cξϕ*(*w*)*F* (*x*)*Y₁* + *X₁* + *h* (*x*)*X₁Y₁ − cξϕ*(*w*)*Y₁* + *O*(*|X₁, Y₁|*)*.* 2 (13) Under the condition of double zero eigenvalues of *J* *∗*, *tr*(*J* *∗*

) = 0 and *det*(*J*
*∗*

) = 0, which implies as follows:
*F* *′* (*x* *∗* )*p*(*x* *∗* ) = *cξϕ*(*w*)*F* (*x* *∗*

)*,* (14)
*h* *′* (*x* *∗* ) = *cξϕ*(*w*)*F* *′* (*x* *∗*

)*.* (15)
Using the condition (14), system (13) becomes (

||1||2||||
|---|---|---|---|---|---|---|
||1||2|2 ∗|′′ ∗|3|
|∗ ′ ∗||∗ ∗ ′′ ∗|∗ ′ ∗|||′ ∗|
|∗ ′ ∗|||||′ ∗||

*X* ˙ = *a₁₀X₁* + *a₀₁Y₁* + *a₂₀X₁* + *a₁₁X₁Y₁* + *O*(*|X₁, Y₁|* 3 )*,* (16) *Y* ˙ = *b₁₀X₁ − a₁₀Y₁* + *b₂₀X₁* + *b₀₂Y₁* + *b₁₁X₁Y₁* + *O*(*|X₁, Y₁|*)*,*

where the coefficients are given by *′* <u>p(x)F (x)</u> *a₁₀* = *p*(*x*)*F* (*x*), *a₀₁* = *−p*(*x*), *a₂₀* = *p* (*x*)*F* (*x*) +, *a₁₁* = *−p* (*x*), 2 <u>F (x)h (x)</u> *b₁₀* = *F* (*x*)*h* (*x*), *b₂₀* =, *b₀₂* = *−cξϕ*(*w*), *b₁₁* = *h* (*x*). 2 From the equation (14) *F* *′* (*x* *∗* )*p*(*x* *∗* ) = *cξϕ*(*w*)*F* (*x* *∗*

) *>* 0, as *F* (*x*
*∗*

) *>* 0. Hence *F*
*′* (*x* *∗* )*p*(*x* *∗* ) *̸*= 0 implies *a₁₀ ̸*= 0. From the equation (15) *h* *′* (*x* *∗* ) = *cξϕ*(*w*)*F* *′* (*x* *∗* ) *̸*= 0.Therefore *b₁₀* = *F* (*x* *∗* )*h* *′* (*x* *∗* ) *̸*= 0. Now to reduce the system (16) to more general canonical form, we apply the transformation <u>Y₂ Y₂</u> *X₁* = *X₂* + and *Y₁* =. *b₁₀ a₁₀* Under this transformation, the system (16) becomes (

|2|2|2|3|
|---|---|---|---|
|2|2|2|3|

*X* ˙ = *d₀₁Y₂* + *d₂₀X₂* + *d₀₂Y₂* + *d₁₁X₂Y₂* + *O*(*|X₂, Y₂|*)*,* (17) *Y* ˙ = *c₁₀X₂* + *c₂₀X₂* + *c₀₂Y₂* + *c₁₁X₂Y₂* + *O*(*|X₂, Y₂|*)*,*

where the coefficients are as follows: *a₁₀b₂₀ b₀₂ b₁₁ a₁₀b₂₀* *c₁₀* = *a₁₀b₁₀*, *c₂₀* = *a₁₀b₂₀*, *c₀₂* = + +, *c₁₁* = + *b₁₁* *b₁₀ a₁₀ b₁₀ b₁₀* *a₁₀ a₀₁ a₁₀b₂₀ a₁₁ a₂₀ a₁₀b₂₀ b₀₂ b₁₁* *d₀₁* = +, *d₂₀* = *a₂₀ −*, *d₀₂* = + *− − −*, 2 3 2 *b₁₀ a₁₀ b₁₀ a₁₀b₁₀ b₁₀ b₁₀ a₁₀b₁₀ b₁₀* *a₁₁* 2*a₂₀* 2*a₁₀b₂₀ b₁₁* *d₁₁* = +

|−|−.||
|---|---|---|
|2|||
|∗|2||

*a₁₀ b₁₀ b₁₀ b₁₀* <u>a₁₀ a₀₁</u> Now, since *det*(*J*) = 0, implies that *a₁₀* + *b₁₀a₀₁* = 0. That is, *d₀₁* = + = 0*.* *b₁₀ a₁₀*

Then system(17) becomes ( ˙3

|2 2|2|
|---|---|
|2|2 2|

*X* = *d₂₀X₂* + *d₀₂Y₂* + *d₁₁X₂Y₂* + *O*(*|X₂, Y₂|*)*,* (18) ˙3 *Y* = *c₁₀X₂* + *c₂₀X₂* + *c₀₂Y₂* + *c₁₁X₂Y₂* + *O*(*|X₂, Y₂|*)*.*

<u>c₁₁ + d₂₀ C₂₀</u> Making a *C∞*-change of variables *X₃* = *c₁₀X₂* +*c₀₂Y₂₂ − d₂₀X₂Y₂*, *Y₃* = *Y₂ − Y₂₂ − X₂Y₂* in 2*c₁₀ C₁₀* a small neighborhood of (0*,*0), system (18) transforms to the Standard normal form ( ˙2 3 *X*3= *D₁Y₃* + *D₂X₃Y₃* + *O*(*|X₃, Y₃|*)*,* (19) ˙3 *Y*3= *X₃* + *O*(*|X₃, Y₃|*)*,*

where *D₁* = *c₁₀d₀₂*, *D₂* = (*d₁₁* + 2*c₀₂*). *CP CP CP CP* Notice that, for the values of *ϕ* (*w*) and *ξ*, *D₁D₂ ̸*= 0, where *ϕ* (*w*) and *ξ* satisfy equations (14) and (15). *∗* Hence the positive equilibrium *E* is a cusp of co-dimension 2.

We now discuss if the system (4) undergoes Bogdanov-Takens bifurcation in a small neighborhood of (*ϕ*(*w*)*, ξ*), choosing *ϕ*(*w*) and *ξ* as bifurcation parameters, we perform a bifurcation analysis of the *∗ ∗ ∗ ∗* system (4) as (*ϕ*(*w*)*, ξ*) varies near (*ϕ* (*w*)*, ξ*), where *ϕ* (*w*) and *ξ* satisfies the equations (11) and (12). We consider the following unfolding system of the system (4) 8 *dx* (*ϕ*(*w*) + *λ₁*)*xy* > *x* > = *rx* 1 *− −* = *p₁*(*x*) *F₁*(*x*) *− y,* >*k* 2 > < *dt* 1 + *αξ* + *bx* + *x* <u>dy βϕ(w)(x + ξ)y</u> (20) 2 > = *− dy − c*(*ξ* + *λ₂*)*ϕ*(*w*)*y* = *y h*(*x*) *− c*(*ξ* + *λ₂*)*ϕ*(*w*)*y,* > 2 > *dt* 1 + *αξ* + *bx* + *x* > : *x*(0) *>* 0*, y*(0) *>* 0*.*

<u>(ϕ(w) + λ₁)x</u> where *λ* = (*λ₁, λ₂*) are small parameters and *p₁*(*x*) =, 2 1 + *αξ* + *bx* + *x* *r x βϕ*(*w*)(*x* + *ξ*) 2 *F₁*(*x*) = 1 *−* (1 + *αξ* + *bx* + *x*), *h*(*x*) = *− d*. 2 (*ϕ*(*w*) + *λ₁*) *k* 1 + *αξ* + *bx* + *x*

##### Now we have the following theorem:

**Theorem 4.2.** *If we vary* (*λ₁, λ₂*) *in a small neighborhood of origin, then the system* (4) *undergoes* *∗* *Bogdanov-Takens bifurcation in a small neighborhood of E.*

*Proof.* When *λ₁* = *λ₂* = 0, the equilibrium *E* *∗* is a cusp of dimension 2. Now we consider Bogdanov- Takens bifurcation of the system (20) in a small neighborhood of *E* *∗* (*x* *∗* *, y* *∗* ). When (*λ₁, λ₂*) vary in a small neighborhood of origin, let *x₁* = *x − x* *∗* and *y₁* = *y − y* *∗* *.* Then the system (20) becomes (

|x˙|= u₁₀x₁ + u₀₁y₁ + u₁₁x₁y₁ + u₂₀x²|||+ O(|x₁, y₁|||),|||
|---|---|---|---|---|---|---|---|---|
|1||||1||3|||
|1|||||2|∗ ′′|3 ∗||
|∗ ′′ ∗|′ ∗ ∗|∗ ∗ ′ ∗||′ ∗ ′ ∗|′ ∗|∗||′ ∗ ∗|

(21) *y*˙ = *v₀₀* + *v₁₀x₁* + *v₀₁y₁* + *v₁₁x₁y₁* + *v₂₀x₁* + *v₀₂y₁₂* + *O*(*|x₁, y₁|*)*,*

<u>p₁(x)F₁ (x)</u> where *u₁₀* = *p₁*(*x*)*F₁*(*x*), *u₀₁* = *−p₁*(*x*), *u₂₀* = *p₁*(*x*)*F₁*(*x*) +, *u₁₁* = *−p₁*(*x*) 2

*v₀₀* = *−cλ₂ϕ*(*w*)*F₁*(*x*), *v₁₀* = *F₁*(*x*)*h* (*x*), *v₀₁* = *−c*(*ξ* + *λ₂*)*ϕ*(*w*)*F₁*(*x*) *− cλ₂ϕ*(*w*)*F₁*(*x*),

<u>F₁(x</u> *∗* <u>)h (x)</u> *v₂₀* =, *v₀₂* = *−c*(*ξ* + *λ₂*)*ϕ*(*w*), *v₁₁* = *h* (*x*). 2 We now apply the transformation *x₂* = *x₁* and *y₂* = *u₁₀x₁* + *u₀₁y₁* as in [12, 15]. The system (21) becomes: 8 > > <u>u₁₁u₁₀</u> 2 <u>u₁₁</u> 3 > > *x*˙2= *y₂* + *u₂₀ − x₂* + *x₂y₂* + *O*(*|x₂, y₂|*)*,* > > *u₀₁ u₀₁* <2 2 <u>u₁₁u₁₀ v₀₂u₁₀</u> 2 *y*˙2= *u₀₁v₀₀* + (*u₀₁v₁₀ − u₁₀v₀₁*)*x₂* + (*u₁₀* + *v₀₁*)*y₂* + *u₁₀u₂₀ −* + *v₂₀u₀₁* + *− v₁₁u₁₀ x₂*+ > > *u₀₁ u₀₁* > > > > <u>u₁₁u₁₀ v₀₂</u> 2 3 : + *v₁₁ −* 2*v₀₂u₁₀ x₂y₂* + *y₂* + *O*(*|x₂, y₂|*)*.* *u₀₁ u₀₁* (22) Now, we using the following *C* *∞* change of co-ordinates in a small neighborhood of (0,0) as

<u>u₁₁ v₀₂</u> 2 *x₃* = *x₂ −* + *x₂,* 2*u₀₁* 2*u₀₁* <u>u₁₁u₁₀</u> 2 <u>v₀₂</u> *y₃* = *y₂* + *u₂₀ − x₂ − x₂y₂.* *u₀₁ u₀₁*

Hence, the system (22) becomes 8 > >*x*˙3= *y₃* + *O*(*|x₃, y₃|* 3 )*,* > < <u>u₁₁u₁₀</u> *y*˙3= *u₀₁v₀₀* + (*u₀₁v₁₀ − u₁₀v₀₁ − v₀₂v₀₀*)*x₃* + (*u₁₀* + *v₀₁*)*y₃* + *v₁₁ −* 2*v₀₂u₁₀* + 2*u₂₀ − x₃y₃* > > *u₀₁* > : 2 3 +*A₁*(*λ*)*x₃* + *O*(*|x₃, y₃|*)*,* (23) *u₁₁u²*10*v₀₂u²*10*v₀₂* where *A₁*(*λ*) = *u₁₀u₂₀ −* + *v₂₀u₀₁* + *− v₁₁u₁₀ −* (*u₀₁v₁₀ − u₁₀v₀₁*) *−* (*u₁₀* + *v₀₁*) *u₂₀ −* *u₀₁ u₀₁ u₀₁* *u₁₁u₁₀ u₁₁ v₀₂* + + *u₀₁v₁₀ − u₁₀v₀₁ − v₀₂v₀₀*. *u₀₁* 2*u₀₁* 2*u₀₁*

Now, we choose another *C* *∞* change of co-ordinates near the origin as *Z₁* = *x₃* and *Z₂* = *y₃* + *O*(*|x₃, y₃|* 3 ) and obtained from system (23) that

> >*Z* ˙ = *Z₂,* > < *Z* ˙ = *u₀₁v₀₀* + (*u₀₁v₁₀ − u₁₀v₀₁ − v₀₂v₀₀*)*Z₁* + (*u₁₀* + *v₀₁*)*Z₂* + *A₁*(*λ*)*Z₁* + *G₁*(*Z₁*) + *Z₂G₂*(*Z₁*)+ > > <u>u₁₁u₁₀</u> > : *v₁₁ −* 2*v₀₂u₁₀* + 2*u₂₀ − Z₁Z₂* + *Z²G₃*(*Z₁, Z₂*)*,* 2 *u₀₁* (24) where *G₁, G₂* are *C* *∞* in *Z₁* and *G₃* is *C* *∞* in (*Z₁, Z₂*) and *G₁*(*Z₁*) = *O*(*|Z₁|* 3 ), *G₂*(*Z₁*) = *O*(*|Z₁|* 2 ), *G₃*(*Z₁, Z₂*) = *O*(*|Z₁, Z₂|*). We rewrite the system (24) as follows: 8 <*Z* ˙ 1= *Z₂,* <u>u₁₁u₁₀</u> : *Z*˙2= *θ*(*Z₁, λ*) + (*u₁₀* + *v₀₁*)*Z₂* + *v₁₁ −* 2*v₀₂u₁₀* + 2*u₂₀ − Z₁Z₂* + *Z₂G₂*(*Z₁*) + *Z₂₂G₃*(*Z₁, Z₂*)*,* *u₀₁* (25) where *θ*(*Z₁, λ*) = *u₀₁v₀₀* + (*u₀₁v₁₀ − u₁₀v₀₁ − v₀₂v₀₀*)*Z₁* + *A₁*(*λ*)*Z₁₂* + *G₁*(*Z₁*). Now, for certain conditions of *ϕ*(*w*) and *ξ*, we have <u>u₁₁u²10v₀₂u²10</u> *A₁*(0) = *u₁₀u₂₀ −* + *v₂₀u₀₁* + *− v₁₁u₁₀ >* 0. *u₀₁ u₀₁* Applying the Malgrange Preparation Theorem [[6, 15]] to *θ*(*Z₁, λ*), we have

*θ*(*Z₁, λ*) = *η₁*(*λ*) + *η₂*(*λ*)*Z₁* + *Z₁₂* Φ(*Z₁, λ*),

<u>u₀₁v₀₀ u₀₁v₁₀ − u₁₀v₀₁ − v₀₂v₀₀</u> where *η₁*(*λ*) =, *η₂*(*λ*) = and Φ(0*, λ*) = *A₁*(*λ*) and Φ(*Z₁, λ*) is a power *A₁*(*λ*) *A₁*(*λ*) series in *Z₁*, whose coefficients depend on the parameters *λ* = (*λ₁, λ₂*). *Z₂* R*t*p Now we consider *Q₁* = *Z₁*, *Q₂* = p and *T* = 0 (Φ(*Z₁*(*s*)*, λ*)) *ds*. Then the system (25) Φ(*Z₁, λ*) becomes ( *Q* ˙ 1= *Q₂,* 2 (26) *Q* ˙ 2= *η₁*(*λ*) + *η₂*(*λ*)*Q₁* + *Q₁* + *η₃*(*λ*)*Q₂* + *η₄*(*λ*)*Q₁Q₂* + *R*(*Q₁, Q₂, λ*)*,*

(*u*<u>10+ v₀₁)</u> *B u₁₁u₁₀ v₀₂*(*u₁₀* + *v₀₁*) where *η₃*(*λ*) = p, *η₄*(*λ*) = p, *B* = *v₁₁* + 2*u₂₀ − −* 2*v₀₂u₁₀ −* (Φ(0*, λ*)) (Φ(0*, λ*)) *u₀₁ u₀₁* *i j* and *R*(*Q₁, Q₂,*0) is a power series of (*Q₁, Q₂*) with the term *Q₁Q₂* such that *i* +*j ≥* 3, *i ≥* 4 and *j ≥* 2. By numerically we have seen that, for some parameter values of *ϕ*(*w*) and *ξ*, *B >* 0. Hence with certain condition *η₄*(*λ*) *>* 0. <u>η₁(λ)</u> Now we make an another affine transformation as *X* = *Q₁* + and *Y* = *Q₂.* Then using 2 Taylor’s series expansion, we have the system (26) as follows: ( *X* ˙ = *Y,* 2 3 (27) *Y* ˙ = *µ₁*(*λ₁, λ₂*) + *µ₂*(*λ₁, λ₂*)*Y* + *X* + *η₄*(*λ*)*XY* + *O*(*|X, Y |*)*,*

<u>η₂</u> 2

<u>(λ) 1</u>
where *µ₁*(*λ₁, λ₂*) = *η₁*(*λ*) *−* and *µ₂*(*λ₁, λ₂*) = *η₃*(*λ*) *− η₂*(*λ*)*η₄*(*λ*). 4 2 Now, with parameter values of *ϕ* *∗*

(*w*) and *ξ*
*∗*, we have <u>∂(η₁, η₂) c²ξϕ(w)pF²h</u> *′* *′ ′ ′ ′′ ′* = *−* 5*/*2 (*h* + *p F* + *pF* + 2*ph*) *̸*= 0*.* *∂*(*λ₁, λ₂*) *λ* =*λ* =0 2*A₁*(0)

Using lemma 8.8 in [16], the system (27) is locally topologically equivalent to the following ( *X* ˙ = *Y,* 2 (28) *Y* ˙ = *µ₁*(*λ₁, λ₂*) + *µ₂*(*λ₁, λ₂*)*Y* + *X* + *η₄*(*λ*)*XY,*

which is strongly topologically equivalent to ( *X* ˙ = *Y,* 2 (29) *Y* ˙ = *µ₁*(*λ₁, λ₂*) + *µ₂*(*λ₁, λ₂*)*Y* + *X* + *XY.*

Choosing *µ₁, µ₂* as bifurcation parameters, the system (28) undergoes a Bogdanov-Takens bifurca- tion in a small neighborhood of *E* *∗*, when (*λ₁, λ₂*) vary in a small neighborhood of origin. Now we observe that, if *µ₁ >* 0, the system (28) has no critical value. If *µ₁* = 0 and *µ₂ ̸*= 0, then the system (28) has only one critical value (0*,*0), which is non hyperbolic. In this case system (28) has saddle-node at origin.

*√ √* If *µ₁ <* 0, then the system (28) has two equilibrium points ( *−µ₁,*0) and (*− −µ₁,*0). Now Jaco- bian matrix for any equilibrium of the system (28) is given by

*′*0 1 *J* =*.* 2*X* + *η₄*(*λ*)*Y µ₂* + *η₄*(*λ*)*X*

*√* As the eigenvalues for the <u>equilibrium point ( −µ₁,0)</u> are s <u>1</u> *√ √* 2 *√* *µ₂* + *η₄*(*λ*) *−µ₁ ±* (*µ₂* + *η₄*(*λ*) *−µ₁*) + 8 *−µ₁*, then it is saddle point. 2 p The eigenvalues of the <u>equilibrium point (− −µ₁,0) are</u> s <u>1</u> *√ √* 2 *√* *µ₂ − η₄*(*λ*) *−µ₁ ±* (*µ₂* + *η₄*(*λ*) *−µ₁*) *−* 8 *−µ₁*. 2 *√* If *µ₂ > η₄*(*λ*) <u>−µ₁</u>, then stable focus. *√* If *µ₂ < η₄*(*λ*) <u>−µ₁</u>, then unstable focus and *√* if *µ₂* = *η₄*(*λ*) *−µ₁* then non-hyperbolic.

We observe that for the system (28), Lyapunov number according to [22] is given by <u>3π</u> *σ* = *√* 3*/*2 *η₄*(*λ*) *>* 0. 2(2 *−µ₁*) *√* Hence the system (28) undergoes a subcritical hopf bifurcation at *µ₂* = *η₄*(*λ*) *−µ₁*.

Hence we obtain the local representations of the bifurcation curves as follows: n

(*i*) Saddle–node bifurcation curve: *SN* = (*λ₁, λ₂*) : *µ₁*(*λ₁, λ₂*) = 0*,*
o *µ₂*(*λ₁, λ₂*) *̸*= 0*.* n (*ii*) Hopf bifurcation curve: *H* = (*λ₁, λ₂*) : *µ₁*(*λ₁, λ₂*) *<* 0*,* p o *µ₂*(*λ₁, λ₂*) = *η₄*(*λ*) *−µ₁*(*λ₁, λ₂*)*.*

##### Now from [22][p-481], we obtain

n (*iii*) Homoclinic bifurcation curve: *HC* = (*λ₁, λ₂*) : *µ₁*(*λ₁, λ₂*) *<* 0*,* p o <u>5</u> *µ₂*(*λ₁, λ₂*) = *η₄*(*λ*) *−µ₁*(*λ₁, λ₂*)*.* 7

### 5 Numerical simulations

We now analyze the numerical simulations for the models (3) and (4). Here we discuss how the wind function performs to find the number of equilibrium points, their stability, and the occurrence of dif- ferent types of bifurcation. In Figs. 1a, 1b and 1c we have performed a time series analysis over a long time period (*t* = 1000) to obtain the values of the stable equilibrium points *E₂*(*k,*0), *E₁*(0*, y₁*) and *E* *∗* (*x* *∗* *, y* *∗* ) from the set of carefully chosen parameters. The set of parameters chosen to obtain a stable equilibrium is r=0.5, k = 4, *α* = 0*.*4*, ξ* = 0*.*6*, b* = 0*.*1*, β* = 0*.*6*, d* = 0*.*1*, c* = 0*.*2. When *ϕ*(*w*)=1.5 prey-free equilibrium point *E₁* is stable, when *ϕ*(*w*) = 1 interior equilibrium point *E* *∗* is stable and for *ϕ*(*w*) = 0*.*6 predator-free equilibrium point *E₂* is stable. Therefore, the figures show with decreasing *ϕ*(*w*) the fitness of predator switches to fitness of prey. In Fig. 2, the stability dynamics of the region is stated by different colours. The figure interprets the *∗ ∗* <u>d(1 + αξ + bk + k²)</u> curves *−tr*(*J*) = 0, *det*(*J*) = 0, *− ϕ*(*w*) = 0 and *β*(*k* + *ξ*)

*d* + *rcξ*(1 + *αξ*) (1 + *αξ*) *ϕ*(*w*) *−* = 0, which are the stability conditions of the all equilibriums with *βξ* respect to *ϕ*(*w*). In the region *R₁*(blue), both equilibria *E* *∗* and *E₁* are stable. Hence in this region the system (3) experiences bi-stability between *E* *∗* and *E₁*. In the region *R₂*(green), only the predator-free equilibrium *E₂* is stable. For *R₃*(red), both *E₂* and *E* *∗* are stable, which shows that in this region the system (3) experiences the bi-stability between *E₂* and *E* *∗*. In the region *R₄*(magenta) all the equilibriums are stable, which indicates that the system (3) also has bi-stability between two axial equilibrium *E₁* and *E₂*. For the region *R₅*(yellow), only the interior equilibrium *E* *∗* is stable. In Figs. 3a and 3b, we get the existence of transcritical bifurcation of the system (3). The parameter set chosen to get these two bifurcations is r=0.5, k=2.5, b=0.5, d=0.1, *ξ* = 1*.*5*, β* = 0*.*285*, α* =

0*.*5*, c* = 0*.*1*.* In fig. 3a, the points *E*
*∗* and *E₂* are stable and unstable, respectively, for the condition (*T C*) *∗* *ϕ*(*w*) *> ϕ₂* (*w*) = 0*.*812, marked by black dot(TC) and *E* (which is not feasible here) and *E₂* are (*T C*) unstable and stable, respectively, for the condition *ϕ*(*w*) *< ϕ₂* (*w*)(in theorem 3.1). Hence, we get a transcritical bifurcation between *E₂* and *E* *∗*. In fig. 3b, the points *E* *∗* and *E₁* are stable and unstable (*T C*) *∗* respectively, for the condition *ϕ*(*w*) *< ϕ₁* (*w*)=0*.*95, marked by black dot(TC) and *E* (which is (*T C*) infeasible here) and *E₁* are unstable and stable respectively, for the condition *ϕ*(*w*) *> ϕ₁* (*w*)(in the- orem 3.2). Hence, we get a transcritical bifurcation between *E₁* and *E* *∗*. Hence, we get 2 transcritical bifurcations for the same parameter set with different values of *ϕ*(*w*). In Figs. 4a and 4b, we get the existence of Saddle-Node bifurcation of the system (3). The parameter set chosen to get these two bifurcation is r=0.5, k=2.5, b=0.5, d=0.1, *ξ* = 1*.*5*, β* = 0*.*285*, α* = 0*.*5, c=0.1. In fig. 4a, two interior points (one stable and one unstable) coincide at *ϕ*(*w*) = *ϕ* *SN* *∗*(*w*) =

*.,* (in theorem 3.3) marked by a black dot(SN). When *ϕ*(*w*) *> ϕ* *SN* *∗*(*w*), there is no interior equilib- rium. In fig. 4b, two interior points ( one stable and one unstable) coincide at *ϕ*(*w*) = *ϕ* *SN* *∗*(*w*) = 0*.,* marked by a black dot(SN). When *ϕ*(*w*) *< ϕ* *SN* *∗*(*w*), there is no interior equilibrium. Hence, we get saddle-node bifurcation at *ϕ*(*w*) = 1*.*3985 and *ϕ*(*w*) = 0*.*895. Hence, two saddle-node bifurcations for the same parameter set with different values of *ϕ*(*w*). In fig. 6, the global bifurcation that can be seen in section 4 has been studied numerically. The figure 6a shows the codimension bifurcation dynamics, and it is observed that multiple interior equilibrium points cause the two saddle-node bifurcation and a Hopf bifurcation. It is well-known that a region with Hopf and saddle-node bifurcation causes a Bogdanov-Takens (BT) bifurcation [16, 5]. We study the (*ξ, ϕ*(*w*)) parameter space in fig. 6b and show the existence of BT bifurcation and cusp (CP) of codimension 2. Fig. 6c shows the two-parameter Hopf curve on which the trace of the Jacobian is always zero. As is established in past studies, the neighborhood of the BT bifurcation shows the existence of a homoclinic orbit. In fig. 6d, it can be seen that when two interior equilibrium points are close to each other at the BT-bifurcation neighborhood, a homoclinic orbit is formed. In Fig. 11, we present the plot of *x* versus *f* (*x*) = *x⁵* + *Ax⁴* + *Bx³* + *Cx²* + *Dx* + *E* for four different values of the wind function *ϕ*(*w*). The others parameters are r=0.5, k=2.5, b=0.5, d=0.1, *ξ* = 1*.*5*,* *β* = 0*.*285, *α* = 0*.*5, c=0.1. For *ϕ*(*w*) = 0*.*92, *ϕ*(*w*) = 0*.*892, *ϕ*(*w*) = 0*.*86 and *ϕ*(*w*) = 1*.*5, the expression *f* (*x*) cut the positive part of *f* (*x*) = 0 at three points, two points, one point and nowhere respectively. Hence we get three interior, two interior, unique interior and no interior equilibrium respectively, of the system (3).

### 6 Effects of different wind-predation rate interaction on sys- tem dynamics

In this section, we discussed the effects of the wind on population dynamics. Since wind intensity can vary seasonally or stochastically, its inclusion in ecological models helps explain complex dynam- ics such as instability, coexistence, or sudden regime shifts. Here we choose four different predation functions *ϕ*(*w*) with respect to wind in the system (3) that provides a more realistic framework to understand population dynamics in flowing environments.

#### 6.1 Bounded U-shaped wind effect

To capture the non–monotonic influence of wind speed on predation, the predation rate is modeled *−*6(*w−w*0)2 by a U-shaped bounded function *ϕ*(*w*)=21 *− e*, which attains minimal values near the intermediate wind level *w₀* and increases toward both lower and higher wind extremes. This func- tional choice is intended to represent ecological situations in which predation pressure is intensified under environmental stress at both extremes of wind intensity, while moderate wind conditions reduce effective predator–prey encounters. The bounded nature of the function ensures biological realism by preventing unbounded growth of predation intensity. The bifurcation structures corresponding to this formulation are illustrated in Figures 7a and 7b. It is observed that the stability of boundary equilibria depends strongly on wind speed. In the regions of low and high wind intensity, the prey-free equilibrium is found to be stable, indicating that strong predation pressure at these extremes can drive the prey population to extinction. In contrast, for intermediate wind speeds, the predator-free equilibrium becomes stable, suggesting reduced predation

efficiency and possible predator decline. Figures 7c and 7d illustrate the time evolution of the prey and predator populations, respectively. The corresponding phase portraits for different values of the wind speed parameter *w* are presented in Figure 7e. The diagram 7f further reveal parameter intervals where multiple attractors coexist, and as shown in the corresponding phase portraits, bistability is present, meaning that the long-term outcome depends sensitively on initial population densities. From a biological perspective, these results highlight that wind acts as a nonlinear environmental regulator capable of generating alternative stable states. Both low and high wind conditions may enhance predator success, whereas intermediate wind speeds may provide a refuge-like zone for prey. Consequently, moderate environmental conditions may stabilize coexistence, while extreme conditions promote dominance of one species, emphasizing the ecological significance of incorporating U-shaped environmental responses into predator–prey models.

#### 6.2 Periodic wind effect

To represent recurrent environmental fluctuations in wind intensity, the predation rate is modeled as a periodic function, *ϕ*(*w*) = 1 *− sin*(2*πw*). This formulation is chosen to reflect cyclical variations in wind conditions, such as seasonal or rhythmic atmospheric patterns, which may repeatedly enhance or reduce predator–prey encounter rates. The periodic structure allows the predation pressure to alternate regularly between higher and lower levels as wind speed varies. The corresponding dynamical behavior is depicted in Figures 8a and 8b. It is observed that within each period of the function, the stability of equilibria alternates systematically. Specifically, for wind speeds near the lower and upper phases of each cycle, the prey-free equilibrium is found to be stable, indicating intensified predation pressure. In contrast, in the intermediate phase of each period, the predator-free equilibrium becomes stable, suggesting reduced predator efficiency and possible predator decline. The bifurcation patterns repeat consistently across successive periods, demonstrating that the qualitative dynamics are periodically modulated by wind speed. As wind speed progresses through suc- cessive periods, the system repeatedly shifts between prey-dominated and predator-dominated states, emphasizing the dynamic nature of ecological responses under periodic environmental drivers. Figures 8c and 8d illustrate the time series dynamics of the prey and predator populations, respectively. Fig- ure 8e presents the corresponding phase portraits for different values of the wind speed parameter *w*. These figures collectively demonstrate how variations in wind speed influence the temporal evolution and qualitative behavior of the prey–predator system. Biologically, these results indicate that cyclical wind fluctuations can generate repeated transitions between predator-dominated and prey-dominated states. Hence, wind speed acts as a time-varying environmental driver capable of inducing regular shifts in ecosystem structure, highlighting the im- portance of incorporating periodic environmental forcing in prey–predator models.

#### 6.3 Exponential wind effect

To understand the influence of wind on predator–prey interactions, an increasing exponential predation <u>e</u> *σw* function of the form *ϕ*(*w*) = is considered. This functional choice reflects the assumption that 5 predation intensity accelerates with increasing wind speed, such that small increments in wind at higher levels produce disproportionately large increases in predation pressure. Such a formulation is ecologically justified when wind enhances predator efficiency through mechanisms such as improved scent dispersion or the flushing of prey from refuges. The dynamical consequences of this assumption are illustrated in Figures 9a and 9b. Variations in wind speed are observed to significantly affect the stability properties of the equilibria. For relatively

low wind speeds, the predator-free equilibrium is found to be stable, indicating predator extinction and prey persistence. As the intensity of the wind increases, the system undergoes qualitative changes, and for sufficiently high wind speeds, the equilibrium of prey-free becomes stable, implying prey extinction due to enhanced predation pressure. These transitions suggest that wind modifies dispersal patterns and hunting efficiency in a nontrivial manner, leading to shifts in dominance between species. Further- more, the figure 9f indicate the presence of bistability in certain parameter regimes, where multiple stable states coexist and the long-term outcome depends on initial population densities. Figures 9c and 9d represent the temporal dynamics of the prey and predator populations, respectively, whereas

Figure 9e shows the phase portraits corresponding to various values of the wind speed parameter *w*.

Biologically, it can therefore be concluded that wind speed acts as a crucial external environmental driver capable of restructuring community outcomes. Depending on its magnitude, wind may either suppress predator populations or intensify predation to the extent of prey collapse. Therefore, climatic factors such as wind should be regarded as critical external forces that can reshape predator–prey dynamics, potentially leading to population imbalance or even local prey depletion under sustained high-wind conditions. The presence of bistability suggests ecological sensitivity to initial conditions and environmental fluctuations, highlighting the potential for abrupt regime shifts in wind-influenced ecosystems.

#### 6.4 Bounded concave wind effect

To incorporate a more ecologically realistic wind effect, a concave bounded predation function of the <u>2w</u> form *ϕ*(*w*) = *√* is considered. This functional response is selected to represent a situation 1 + *w⁴* in which predation initially increases with wind speed but gradually saturates, reflecting biological constraints that prevent indefinite growth in hunting efficiency. This formulation captures the idea that while moderate wind may improve encounter rates, excessive wind can limit predator performance due to movement difficulty, sensory interference, or energetic costs. The bifurcation structure with respect to wind speed is depicted in Figures 10a and 10b. From the diagrams, it is observed that for both low and high wind speeds, the predator-free equilibrium is stable, indicating predator extinction under these environmental extremes. In contrast, within inter- mediate ranges of wind intensity, the prey-free equilibrium becomes stable, suggesting that predators successfully dominate when wind conditions are moderately favorable. The transition between these stability regions highlights the presence of wind-driven qualitative changes in the system dynamics. Furthermore, the diagram 10f reveal the presence of bistability within certain wind intervals, where two stable equilibria coexist. In these regions, the long-term outcome depends sensitively on initial population densities. Figures 10c and 10d depict the time series of the prey and predator populations, respectively, while Figure 10e illustrates the corresponding phase portraits for different values of the wind speed *w*. From a biological perspective, these results indicate that wind acts as a regulating environmental factor with a saturating influence on predation. Moderate wind speeds may enhance predator success by disturbing prey movement or reducing escape efficiency, whereas strong wind imposes limitations on both species, preventing unlimited escalation of predation pressure. The emergence of bistability further suggests that ecosystem responses to wind variation can be non-unique and history-dependent, highlighting the complex role of environmental forcing in shaping population persistence and extinction patterns.

### Discussion

In this study, we investigate the dynamical behavior of a prey–predator system incorporating the effect of wind on population interactions. The model exhibits rich dynamical features like stability switching, oscillatory dynamics and global bifurcations. From a biological perspective, this means that population dynamics are not governed solely by intrinsic growth and predation parameters, but also by external abiotic drivers that can regulate or destabilize ecological balance. Unlike classical prey– predator models, where population changes depend solely on biological interactions, the inclusion of wind introduces an external ecological driver that significantly alters system stability and long-term behavior. As a result, wind acts not merely as a perturbation but as a key control parameter governing the qualitative behavior of the system. In natural ecosystems—such as grasslands, coastal regions, agricultural fields, or open marine environments—wind can significantly alter foraging efficiency, prey vulnerability, and habitat accessibility. The system shows the phenomenon of bistability, which can be biologically crucial. Ecologically, this indicates the presence of alternative stable states in the predator–prey system, where long-term population outcomes depend on initial conditions and disturbance magnitude by wind. Such systems exhibit threshold behavior and reduced resilience, implying that environmental forcing, including wind variability, can trigger abrupt regime shifts between coexistence and oscillatory or extinction states. From the bifurcation perspective, parameter variation reveals transitions between distinct dynam- ical regimes. For different wind intensities, the system typically maintains a stable coexistence equi- librium, indicating balanced prey-predator interaction. However, as wind-related parameters vary, the stability of equilibrium points changes qualitatively. The emergence of saddle–node or transcrit- ical bifurcations indicates thresholds at which coexistence states are created or destroyed, reflecting ecological tipping points in which small environmental changes can result in population extinction or persistence. At low wind intensity, the system undergoes a subcritical Hopf bifurcation, producing unstable limit cycles around the coexistence equilibrium. Ecologically, this indicates that predator–prey populations may experience abrupt transitions and reduced resilience under wind disturbances. Wind significantly influences prey-predator interactions by altering encounter and capture effi- ciency under varying environmental conditions. Changes in wind speed can either enhance or reduce interaction strength, reflecting ecological constraints and behavioral responses of both species. Under fluctuating wind conditions, interaction intensity may vary cyclically, leading to recurrent population oscillations rather than stable coexistence. In some situations, small variations in wind can produce rapid changes in interaction strength, making the system highly sensitive to environmental forcing and potentially causing sudden transitions in population dynamics. Furthermore, under appropriate parameter conditions, we see that the system exhibits richer codimension-two dynamics (ex., Bogdanov-Takens Bifurcation). Near this singularity, the system can exhibit multiple dynamical phenomena, including saddle-node bifurcations, Hopf bifurcations, and homoclinic orbits. Also for different type of predation function, we have seen dynamical changes of population. Overall, the biological interpretation emphasizes that wind acts as a regulatory environmental driver that can reshape prey-predator stability, persistence, and resilience. The model highlights the ecological importance of incorporating abiotic factors into population dynamics studies, particularly for predicting ecosystem responses to environmental variability and climate-induced changes. Although the present study provides a comprehensive qualitative analysis of the proposed prey–predator model under the influence of wind-dependent predation, several important directions remain open for future investigation. First, spatial heterogeneity could be included through reaction–diffusion formulations.

Wind often plays a significant role in spatial dispersal of species; therefore, extending the model to a spatial domain may lead to pattern formation, traveling wave solutions, or Turing instability. The higher order rich bifurcations such as like saddle-transcritical bifurcation, generalized Hopf etc. can be studied further. Experimental results to understand the functional response behavior for particular ecosystems are yet to be analyzed where wind speed over time can be of great importance to study an autonomous system and produce time dependent predictions for the species populations.

### Conflict of interest

The authors have no conflict of interest.

|5||Prey||Prey||5||Prey|
|---|---|---|---|---|---|---|---|---|
|4||Predator|3|Predator||4||Predator|
|3|||2|||3|||
|2|||1|||2|||
|population 1|||population 0|||population 1|||
|0|||-1|||0|||
|0 200|400 600|800 1000|0 200 time|600 800|1000|0 200 time|400 600|800 1000|

**400 time**

(a) (b) (c)
Figure 1: Time series diagram for the local stability of *E₂*(*k,*0), *E₁*(0*, y₁*), *E*

*∗* (*x* *∗* *, y* *∗* ) of (3) in figures 1a, 1b and 1c respectively with the initial condition (3*,*0*.*5) and *ϕ*(*w*) = 0*.*61, *ϕ*(*w*) = 1*.*5 and *ϕ*(*w*) = 1, respectively and the others parameters are *r* = 0*.*5*, k* = 4*, α* = 0*.*4*, ξ* = 0*.*6*, b* = 0*.*1*, β* = 0*.*6*, d* =

0*.*1*, c* = 0*.*2*.*
Figure 2: The figure shows the local stability of equilibriums of the model (3) with respect to the
 wind speed function *ϕ*(*w*). The other parameters are *r* = 1*, k* = 5*, α* = 0*.*1*, ξ* = 2*, b* = 0*.*2*, β* =
0*.*7*, d* = 0*.*1*, c* = 0*.*1*.* The region *R₁*(blue) is the region in which both the prey-free equilibrium *E₁* and the interior equilibrium *E*
*∗* are stable. In the region *R₂*(green), only the predator-free equilibrium *E₂* is stable. In the region *R₃*(red), both predator-free equilibrium *E₂* and interior equilibrium *E* *∗* are stable. The region *R₄*(magenta) is the region in which all the equilibriums are stable. In the region *R₅*(yellow), only interior equilibrium *E* *∗* is stable.

Table 1: Existence and stability analysis of equilibria of the system (3)

|S.No.|Equilibrium Points|Feasibility Con- dition||Status of Stability||proof|
|---|---|---|---|---|---|---|
|(i)|E₀ (0, 0)|Always (8.2)||Saddle point d (1 + αξ + bk + k²) stable node if ϕ (w) < in Fig. β (k + ξ) 1a||(8.3)|
|(ii)|E₂ (k, 0)|Always (8.2) βξϕ (w)||d (1 + αξ + bk + k²) Saddle point if ϕ (w) > β (k + ξ) d (1 + αξ + bk + k²) Neutral if ϕ (w) = β (k + ξ) d + rcξ (1 + αξ) (1 + αξ) stable node if ϕ (w) > βξ in Fig. 1b||( 8.4)|
|(iii)|E₁ (0, y₁), y₁ = βξ − cξ (1 + αξ) d cξϕ (w)|d − < 0 1 + αξ (8.2)||d + rcξ (1 + αξ) (1 + αξ) Saddle point if ϕ (w) < βξ d + rcξ (1 + αξ) (1 + αξ) Neutral if ϕ (w) = βξ||( 8.5)|
|(iv)|∗ ∗ ∗ E (x, y)|Any one of A, B, C, D, E is negative (8.2)||∗ ∗ asymptotically stable if tr (J) < 0 and det (J) > 0 in Fig. (1c) ∗ non-hyperbolic if det (J) = 0||( 8.6)|

(a) (b)
Figure 3: *r* = 0*.*5*, k* = 2*.*5*, b* = 0*.*5*, d* = 0*.*1*, ξ* = 1*.*5*, β* = 0*.*285*, α* = 0*.*5*, c* = 0*.*1*.*

Dotted lines indicates unstable and solid lines denote stable equilibriums. Transcritical between axial *E₂* and interior equilibrium at *ϕ*(*w*)=0*.*812 in 3a and transcritical between axial *E₁* and interior equilibrium at *ϕ*(*w*) = 0*.*95 in 3b. TC: Transcritical.

(a) (b)
Figure 4: *r* = 0*.*5*, k* = 2*.*5*, b* = 0*.*5*, d* = 0*.*1*, ξ* = 1*.*5*, β* = 0*.*285*, α* = 0*.*5*, c* = 0*.*1*.*

Solid lines denote stable and dotted lines denotes unstable equilibrium.In figure 4a and 4b, at *ϕ*(*w*) =

1*.*3985 and at *ϕ*(*w*) = 0*.*895 respectively, saddle-node bifurcation occurs. SN: Saddle-node.
Figure 5: The figure shows the bifurcation diagram of *ϕ*(*w*) vs prey population. The grey shaded region
 shows the unstable limit cycle, and the black line signifies the stable equilibrium and this change is due to the Hopf bifurcation. The parameters used are *r* = 0*.*5*, k* = 2*.*5*, b* = 0*.*5*, d* = 0*.*1*, ξ* = 1*.*5*, β* =
0*.*285*, α* = 0*.*5*, c* = 0*.*1*.*

SN

1.5 1
x(t)

0.5 SN 0
TC H

-0.5

0.6 0.7 0.8 0.9 1 1.1 1.2 1.3
(w)
(a) (b)
0.7
0.6 1.4
Predator 0.605 BT 1.2 0.604 Equilibrium Point

0.5
Prey Nullcline

0.603
0.602
1 0.601

0.40.6
0.224 0.226 0.228 0.23 0.232
0.8
0.3
y(t)

0.6
0.20.4 Homoclinic
0.10.2
0 0 0.5 1 1.5 2 2.5 1 1.1 1.2 1.3 1.4 1.5 1.6 1.7 1.8

(w)
x(t)

(c) (d)
Figure 6: The figure shows the existence of Bogdanov-Takens bifurcation and dynamics around the

neighborhood. Figure 6a and 6b show the codimension 1 and 2 bifurcation diagrams, respectively.

Figure 6c shows the Hopf curve with two changing parameters *ξ* and *ϕ*(*w*). Figure 6d shows the

prey nullcline (Blue) and predator nullcline (red), and the boxed region is the equilibrium where a homoclinic orbit exists. The zoomed-in image shows the existence of a homoclinic orbit around the same BT neighborhood. SN: Saddle-node, TC: Transcritical, BT: Bogdanov-Takens, CP: Cusp. The parameters used are *r* = 0*.*5*, k* = 2*.*5*, b* = 0*.*5*, d* = 0*.*1*, β* = 0*.*285*, α* = 0*.*5*, c* = 0*.*1*.*

(a) (b)
**3 2 w=1**

**2.5 w=0.6741.5w=0.2** **2**
**1.5 1 prey** **1 predator**
**0.5**
**0.5w=0.674 w=0.2**
**0** **0 w=1** **0 1000 2000 3000 4000 5000 0 1000 2000 3000 4000 5000 time time**

(c) (d)
**w=0.66**

||1.2||||1|||
|---|---|---|---|---|---|---|---|
||w=0.21|||E10.8|(0.6,0.9)|||
||0.8|||||||
|0.6||w=0.674||0.6|(1,0.5)|||
|predator 0.4|(1,0.5)|||predator 0.4||w=0.66||
|0.2 0|||w=1|0.2|||E*|
||0|2|3|0|0.5|1.5|2 2.5|
|||||prey||||

**1.2**
**1**

**1 1 prey**

(e) (f)
(*−*6(*w−w*0)2)

Figure 7: Here we choose a bounded U-shaped function *ϕ*(*w*) = 2 1 *− e*, where *w₀* is the

optimum wind speed. Figs. 7a and 7b represents the bifurcation figures of wind speed *w* vs prey and predator population, respectively. In Figs. 7a and 7b, dotted red lines represents unstable equilibrium and solid red lines indicates stable equilibrium and solid blue line represents the function *ϕ*(*w*). Figs. 7c and 7d shows the time series for prey and predator population with different *w* and fig. 7e is the phase portrait of the respective population. The others parameters are r=0.5, k=2.5, b=0.5, d=0.1, *ξ* = 1*.*5*, β* = 0*.*285*, α* = 0*.*5 c=0.1, *w₀*=1. SN: Saddle-Node, TC: Transcritical.

(a) (b)

||2|||||3||
|---|---|---|---|---|---|---|---|
|||||||2.5|w=0.3|
|1.5||w=0.6||||2|w=0.487|
|1|||||1.5|||
||||||prey|||
|predator 0.5|||w=0.487||1 0.5|||
|0|||w=0.3||0||w=0.6|
|0|1000 2000|3000|4000|5000|0|1000 2000|4000|
|||||||time||

**3000 5000 time**

(c) (d)
**w=0.6**

**1.2** **1**
**0.8**
**0.6 w=0.487 predator**
**0.4**
**(1,0.5)**

**0.2 w=0.3** **0** **0 1 2 3 prey**
(e)
Figure 8: Here we choose a periodic function *ϕ*(*w*)=1 *− sin*(2*πw*). Figs. 8a and 8b shows the

bifurcation figures of wind speed *w* vs prey and predator population, respectively. In Figs. 8a and 8b, dotted red lines represent unstable equilibrium, and solid red lines indicate stable equilibrium, and the solid blue line represents the function *ϕ*(*w*). Figs. 8c and 8d show the time series for prey and predator population with different *w* and fig. 8e is the phase portrait of the respective population dynamics. The others parameters are r=0.5, k=2.5, b=0.5, d=0.1, *ξ* = 1*.*5*, β* = 0*.*285*, α* = 0*.*5*,* c=0.1. SN: Saddle-Node, TC: Transcritical.

(a) (b)

||3|||2|||
|---|---|---|---|---|---|---|
||2.5 2|w=0.5 w=0.85|1.5|||w=1.2|
|1.5 prey|||1||||
|1|||predator 0.5||||
|0.5|||||w=0.85||
|0||w=1.2|0|||w=0.5|
|0|1000 2000|4000|0|1000 2000|3000|4000|
|||||time|||

**3000 5000 5000 time**

(c) (d)
**E** **1** **w=0.9** **1**

**1.2 w=1.2** **1(0.4,0.9)0.8**
**0.8**
**0.6**
**0.6w=0.85 w=0.9 predator predator(1,0.5)**
**0.4**
**(1,0.5)0.4** **E** *****

**0.2**
**0.2 w=0.5**
**0** **0 1 2 3 0 0.5 1 1.5 2 2.5 prey prey**

(e) (f)
<u>e</u> *σw*

Figure 9: We choose an strictly increasing function *ϕ*(*w*) =. Figs. 9a and 9b shows the bifurcation

5 figures of wind speed *w* vs prey and predator population, respectively. In Figs. 9a and 9b, dotted red lines and solid red lines represents unstable and stable equilibrium, respectively and solid blue line represents the function *ϕ*(*w*). Figs. 9c and 9d shows the time series for prey and predator population with different *w* and fig. 9e is the phase portrait of the respective population dynamics. The others parameters are r=0.5, k=2.5, b=0.5, d=0.1, *ξ* = 1*.*5*, β* = 0*.*285*, α* = 0*.*5*,* c=0.1, *σ* = 2. SN: Saddle- Node, TC: Transcritical.

(a) (b)
**3 2 w=0.3**

**2.5 w=0.47**
**1.5**
**2w=1**

**1.5 1 prey** **1 predator**
**0.5**
**0.5 w=0.47 w=10** **0 w=0.3** **0 1000 2000 3000 4000 5000 0 1000 2000 3000 4000 5000 time time**
(c) (d)
**1.2 w=0.6**
**1 w=1 1** **E** **1** **(0.4,0.9)**

**0.8**
**0.8**

|0.6||w=0.47||0.6||w=0.6||
|---|---|---|---|---|---|---|---|
|predator 0.4|(1,0.5)|||0.4|(1,0.5)|||
|0.2 0|||w=0.3|0.2|||E*|
||0|2|3|0|0.5 1|1.5|2 2.5|
|||||prey||||

**predator**

**1 prey**

(e) (f)
<u>2w</u>

Figure 10: We choose an bounded function *ϕ*(*w*)=*√*. Figs. 10a and 10b shows the bifurcation

1 + *w⁴* figures of wind speed *w* vs prey and predator population, respectively. In Figs. 10a and 10b, dotted red lines and solid red lines represents unstable and stable equilibrium, respectively and solid blue line represents the function *ϕ*(*w*). Figs. 10c and 10d shows the time series for prey and predator population with different *w* and fig. 10e is the phase portrait of the respective population dynamics. The others parameters are r=0.5, k=2.5, b=0.5, d=0.1, *ξ* = 1*.*5*, β* = 0*.*285*, α* = 0*.*5*,* c=0.1. SN: Saddle-Node, TC: Transcritical.

### 8 Appendix

#### 8.1 Positivity and uniform bounded

With regard to the positivity of the system represented by equation (3), the following outcome has been obtained.

||10|5|
|---|---|---|
||5||
|-5|0|0|
|-10-1||-5-0.5|

**f(x) f(x)**

**0 1 2 0 0.5 1 1.5 2 x x**

(a) (b)

||4||||200|
|---|---|---|---|---|---|
|2|||||150|
|0||||100||
|-2||||50||
|-4||||0||
|-6-0.5 0|0.5|1 1.5|2 2.5|-50-1|0|

**f(x) f(x)**

**1 2 3 x x**

(c) (d)
Figure 11: The figure represents the nullcline curve as in equation (37) for different values of *ϕ*(*w*).

For *ϕ*(*w*) = 0*.*92, *ϕ*(*w*) = 0*.*8932, *ϕ*(*w*) = 0*.*86 and *ϕ*(*w*) = 1*.*5, the equation (37) that is *f* (*x*) = 0 has 3 solution, 2 solution, unique solution, no solution respectively on R +. The others parameters are r=0.5, k=2.5, b=0.5, d=0.1, *ξ* = 1*.*5*, β* = 0*.*285*, α* = 0*.*5*, c* = 0*.*1*.*

**Theorem 8.1.** *All solutions x(t) and y(t) that satisfy system* (3) *and initial conditions x*(0) *>* 0*,* *y*(0) *>* 0 *exhibit uniform boundedness.*

*Proof.* Using the first equation of the system (3), it can be inferred that

<u>dx</u> <u>x</u> *≤ rx* 1 *−* *k*

*.* (30)
*dt* The above inequality leads to lim *sup x*(*t*) *≤ k.* (31) *t→∞* Hence, for any positive constant *ϵ >* 0 sufficiently small, there exists a *T₁ >* 0 such that for all *t ≥ T₁*,

*k − ϵ ≤ x*(*t*) *≤ k* + *ϵ.* (32)

For t *≥ T₁*, it follows from the second equation of the system (3) that

<u>dy βϕ(w)(x + ξ)y</u> 2 = 2 *− dy − ϕ*(*w*)*y ,* *dt* 1 + *αξ* + *bx* + *x* <u>βϕ(w)(k + ϵ + ξ)</u> *≤ y* 2 *− d − ϕ*(*w*)*y,* 1 + *αξ* + *b*(*k − ϵ*) + (*k − ϵ*) <u>βϕ(w)(k + ϵ + ξ) ϕ(w)y</u> *≤ y* 2 *− d* 1 *−.* 1 + *αξ* + *b*(*k − ϵ*) + (*k − ϵ*) <u>βϕ(w)(k + ϵ + ξ)</u> *− d* 1 + *αξ* + *b*(*k − ϵ*) + (*k − ϵ*)

The above inequality leads to

<u>βϕ(w)(k + ϵ + ξ)</u> lim *sup y*(*t*) *≤ − d.* (33) *t→∞*1 + *αξ* + *b*(*k − ϵ*) + (*k − ϵ*)2

Since *ϵ* is a small positive constant, setting *ϵ →* 0 in (33) leads to

<u>βϕ(w)(k + ξ)</u> lim *sup y*(*t*) *≤ − d.* (34) *t→∞*1 + *αξ* + *bk* + *k*2

Hence, from equations (34) and (31), x(t) and y(t) of the system (3) with the initial conditions x(0) *>* 0, y(0)*>* 0 are uniformly bounded.

#### 8.2 Existence of the equilibria

With regard to the presence of equilibria in the system (3), the following result has been observed.

1. The vanishing equilibrium point *E₀*(0*,*0) and the predator-free equilibrium point *E₂*(*k,*0) always
exist.

2. There is a prey-free equilibrium point *E₁*(0*, y₁*)
<u>βξ d</u> where *y₁* = *−*, if *cξ*(1 + *αξ*) *cξϕ*(*w*) <u>βξϕ(w)</u> *d − <* 0*.* (35) 1 + *αξ*

3. Other non-negative interior steady states of (3) can be solved from the following equations
<u>x ϕ(w)y</u> *f₁*(*x, y*) = *r* 1 *− −* = 0*,* 2 *k* 1 + *αξ* + *bx* + *x* (36) <u>βϕ(w)(x + ξ)</u> *g₁*(*x, y*) = *− d − cξϕ*(*w*)*y* = 0*.* 2 1 + *αξ* + *bx* + *x*

From the first equation of (36), we have

<u>r x</u> 2 *y* = (1 + *αξ* + *bx* + *x*) 1 *−* =*⇒ y >* 0 *∀* 0 *< x < k.* *ϕ*(*w*) *k*

Solving equation (36), we get a 5-degree equation of *x* as follows:

*x⁵* + *Ax⁴* + *Bx³* + *Cx²* + *Dx* + *E* = 0*,* (37)

where *A* = 2*b − k*, *B* = 2 + *b²* + 2*αξ −* 2*bk*, <u>dk</u> 2 *C* = 2*b* + 2*bαξ − −* 2*k − b k −* 2*αξk*, *rcξ* <u>kβϕ(w) dkb</u> 2 2 *D* = 1 + *α ξ* + 2*αξ* + *− −* 2*kb −* 2*bkαξ*, *rcξ rcξ* <u>kβϕ(w)ξ − dk − dkαξ</u> 2 2 *E* = *−α ξ k − k −* 2*αξk* +. *rcξ* + By numerical methods, we show that equation (37) has at most 3 roots in R. Figure 11.

**Theorem 8.2.** *The system* (3) *has*

- *trivial and predator-free equilibrium points, which always exist,*
<u>βξϕ(w)</u>

- *prey-free equilibrium point if d − <* 0*,*
1 + *αξ*

- *no interior equilibrium point if A, B, C, D, E >* 0*,*
- *unique equilibrium point if*
*1. E <* 0 *and A, B, C, D >* 0*,*
*2. E, D <* 0 *and C, B, A >* 0*,*
*3. E, D, C <* 0 *and A, B >* 0*,*
*4. E, D, C, B <* 0 *and A >* 0*,*
*5. A, B, C, D, E <* 0*,*
*where A, B, C, D and E are the coefficients in* (37)*.*

#### 8.3 Local stability analysis

We introduce the Jacobian Matrix of model (3), which is calculated at any arbitrary equilibrium point as follows:

*fxfy* *J* =*,* *gxgy*

*x rx* *ϕ*(*w*)*y ϕ*(*w*)*xy*(*b* + 2*x*)

|where f = r|− −|+||,|
|---|---|---|---|---|
||k k|2||2 2|
|y|2||||
|x|2|2 2|||
|y|2||||

*x*1 *−k k* 2 2 2 1 + *αξ* + *bx* + *x* (1 + *αξ* + *bx* + *x*) *ϕ*(*w*)*x* *f* = *−*, 1 + *αξ* + *bx* + *x* *βϕ*(*w*)*y* <u>βϕ(w)(x + ξ)y(b + 2x)</u> *g* = *−*, 1 + *αξ* + *bx* + *x* (1 + *αξ* + *bx* + *x*) *ϕ*(*w*)(*x* + *ξ*) *g* = *β − d −* 2*cξϕ*(*w*)*y.* 1 + *αξ* + *bx* + *x*

**Lemma 8.3.** *The trivial Equilibrium Point of the system* (3) *is always a saddle point.*

*Proof.* At equilibrium *E₀*(0*,*0), the Jacobian matrix is

*r* 0 *Jo*= 0 *−d*

with eigenvalues: *λ₁* = *r*, *λ₂* = *−d*. Since*λ₁ >* 0 and *λ₂ <* 0, *E₀*(0*,*0) is a saddle point.

**Lemma 8.4.** *For the predator-free Equilibrium Point E₂*(*k,*0)

- *It is a stable node if*
<u>d(1 + αξ + bk + k²)</u> *ϕ*(*w*) *<,* *β*(*k* + *ξ*)

- *It is a saddle point if*
<u>d(1 + αξ + bk + k²)</u> *ϕ*(*w*) *>,* *β*(*k* + *ξ*)

- *It is non-hyperbolic if*
<u>d(1 + αξ + bk + k²)</u> *ϕ*(*w*) =*.* *β*(*k* + *ξ*)

*Proof.* At equilibrium *E₂*(*k,*0), the Jacobian matrix is

0 1 *ϕ*(*w*)*k* *−r −* 2 B 1 + *αξ* + *bk* + *k* C *J₂* = @ A <u>βϕ(w)(k + ξ)</u> 0 *−d* + 2 1 + *αξ* + *bk* + *k*

<u>βϕ(w)(k + ξ)</u> with eigenvalues : *λ₁* = *−r*, *λ₂* = *−d* + 2. 1 + *αξ* + *bk* + *k* Since *λ₁ <* 0, the stability depends on *λ₂*. <u>d(1 + αξ + bk + k²)</u>

- ** If *ϕ*(*w*) *<*, then *λ₂ <* 0. Hence *E₂*(*k,*0) is a stable node.
*β*(*k* + *ξ*) <u>d(1 + αξ + bk + k²)</u>

- ** If *ϕ*(*w*) *>*, then *λ₂ >* 0. Hence *E₂*(*k,*0) is a saddle point.
*β*(*k* + *ξ*) <u>d(1 + αξ + bk + k²)</u>

- ** If *ϕ*(*w*) =, then *λ₂* = 0. Hence *E₂*(*k,*0) is neutral.
*β*(*k* + *ξ*)

**Lemma 8.5.** *For the prey-free Equilibrium Point E₁*(0*, y₁*)

- *It is a stable node if*
*d* + *rcξ*(1 + *αξ*) (1 + *αξ*) *ϕ*(*w*) *>,* *βξ*

- *It is a saddle point if*
*d* + *rcξ*(1 + *αξ*) (1 + *αξ*) *ϕ*(*w*) *<,* *βξ*

- *It is non-hyperbolic if*
*d* + *rcξ*(1 + *αξ*) (1 + *αξ*) *ϕ*(*w*) =*.* *βξ*

*Proof.* At equilibrium *E₁*(0*, y₁*), the Jacobian matrix is

<u>βϕ(w)ξ</u> B *r − cξ* (1 + *αξ*) 1 + *αξ* *− d* C *J₁* = B @ C A *.* *β βϕ*(*w*)*ξ βξb βϕ*(*w*)*ξ βξϕ*(*w*) *− d −* 2 *− d d −* *cξ*(1 + *αξ*) 1 + *αξ cξ*(1 + *αξ*) 1 + *αξ* 1 + *αξ*

Here we are describing the condition of stability of the prey-free equilibrium point *E₁* of model (3). So the characteristic equation at *E₁*(0*, y₁*) is given below,

*P* (*λ*) = *λ²* + *µ₁λ* + *µ₀* = 0*,* (38)

where coefficients are

***µ₁*** = *−tr*(*J₁*) = *−*(*a₁₁* + *a₂₂*)*,* ***µ₀*** = *det*(*J₁*) = *a₁₁a₂₂ − a₁₂a₂₁,*

*a₁₁ a₁₂* where *J₁* = is the Jacobian matrix of model (3) at *E₁*. The components of the Jacobian *a₂₁ a₂₂* matrix are given below:

1 <u>βϕ(w)ξ</u> *J₁₁* = *r − − d,* *cξ*(1 + *αξ*) 1 + *αξ* *J₁₂* = 0*,* <u>β βϕ(w)ξ βξb βϕ(w)ξ</u> *J₂₁* = *− d −* 2 *− d,* *cξ*(1 + *αξ*) 1 + *αξ cξ*(1 + *αξ*) 1 + *αξ* <u>βξϕ(w)</u> *J₂₂* = *d −.* 1 + *αξ*

Here *µ²*1*−* 4*µ₀* = (*a₁₁ − a₂₂*) 2 *≥* 0. Therefore, all the roots of equation (33) are real. If *tr*(*J₁*) = (*a₁₁* + *a₂₂*) *<* 0 i.e. *µ₁ >* 0 and *det*(*J₁*) = *a₁₁a₂₂ >* 0 then both roots are real negative. Hence *E₁* is a stable node. As *a₂₂ <* 0, *a₁₁a₂₂ >* 0 implies *a₁₁ <* 0, that is,

*d* + *rcξ*(1 + *αξ*) (1 + *αξ*) *ϕ*(*w*) *>.* *βξ*

If *det*(*J₁*) = *a₁₁a₂₂ <* 0 then one positive and one negative real roots. Hence *E₁* is a saddle point.

As *a₂₂ <* 0, *a₁₁a₂₂ <* 0 implies *a₁₁ >* 0, that is,

*d* + *rcξ*(1 + *αξ*) (1 + *αξ*) *ϕ*(*w*) *<.* *βξ*

If

*d* + *rcξ*(1 + *αξ*) (1 + *αξ*) *ϕ*(*w*) =*,* *βξ*

then *E₁* is neutral. *∗ ∗ ∗* **Lemma 8.6.** *For the interior equilibrium point E* (*x, y*)

*∗ ∗*

- *It is asymptotically stable if tr*(*J*) *<* 0 *and det*(*J*) *>* 0*,*
*∗*

- *It is non-hyperbolic if det*(*J*) = 0*.*
*∗ ∗ ∗ ∗J₁₁ J₁₂* *Proof.* At the coexisting equilibrium point *E* (*x, y*), the Jacobian matrix is *J* =, *J₂₁ J₂₂*

|∗|∗ ∗|∗||||
|---|---|---|---|---|---|
|∗ ∗|∗|∗2 2||||
|∗||∗ ∗|∗|||
|∗ ∗2 ∗||∗|∗2 2|||
||∗ ∗ ∗||||∗|

<u>rx ϕ(w)x y (b + 2x)</u> where *J₁₁* = *−* +, *k* (1 + *αξ* + *bx* + *x*) *ϕ*(*w*)*x* *J₁₂* = *−*, *∗*2 1 + *αξ* + *bx* + *x* *βϕ*(*w*)*y* <u>βϕ(w)(x + ξ)y (b + 2x)</u> *J₂₁* = *−*, 1 + *αξ* + *bx* + *x* (1 + *αξ* + *bx* + *x*) *J₂₂* = *−cξϕ*(*w*)*y*. Here, we describe the stability condition of the coexisting equilibrium point *E* of model (3). So, the characteristic equation at *E* (*x, y*) is given below,

*Q*(*λ*) = *λ²* + *η₁λ* + *η₀* = 0*,* (39)

where coefficients are

***η₁*** = *−tr*(*J₁*) = *−*(*J₁₁* + *J₂₂*)*,* ***η₀*** = *det*(*J₁*) = *J₁₁J₂₂ − J₁₂J₂₁.*

Here, *∗ ∗ ∗ ∗* <u>ϕ(w)x y (b + 2x) rx</u> *∗ ∗* *tr*(*J*) = *− − cξϕ*(*w*)*y* and *∗ ∗*2 2 (1 + *αξ* + *bx* + *x*) *k* *∗ ∗ ∗ ∗* 2 *∗ ∗ ∗ ∗* *ϕ*(*w*)*x y* (*b* + 2*x*) *βϕ*(*w*) *x y* (*x* + *ξ*)(*b* + 2*x*) *∗ ∗* *det*(*J*.

|) = cξϕ(w)y|−|||+ rx +||1−||
|---|---|---|---|---|---|---|---|
|∗ ∗||∗|∗ ∗2 2 ∗ ∗||∗ ∗|∗2 2|∗ ∗2|

*∗ ∗*2 2 *∗ ∗*2 2 *∗ ∗*2 (1 + *αξ* + *bx* + *x*) *k* (1 + *αξ* + *bx* + *x*) (1 + *αξ* + *bx* + *x*)

If *trJ <* 0 and *detJ >* 0, then *E* is locally asymptotically stable. If *det*(*J*) = 0, then one of eigenvalue of *J* is zero. Hence, *E* is non-hyperbolic.

Hence from lemma 8*.*3, 8*.*4, 8*.*5 and 8*.*6, a theorem has been formulated as below:

**Theorem 8.7** (Stability of equilibria)**.** *Consider the dynamical system* (3) *with the parameter set* *{b, c, d, r, k, α, β, ξ, ϕ*(*w*)*}. The system has the following equilibria:*

*1. The trivial Equilibrium Point E₀*(0*,*0) *is always a saddle point.*
*2. For the predator-free equilibrium point E₁*(0*, y₁*)*, stability depends on ϕ*(*w*)*.*
8 > > *d* + *rcξ*(1 + *αξ*) (1 + *αξ*) > > > >

|d|βξ + rcξ (1 + αξ) (1 +|αξ)|
|---|---|---|
|d|βξ + rcξ (1 + αξ) (1 +|αξ)|
|8 > >|βξ (k, 0) d (1 + αξ + bk + k²)|, stability depends on ϕ|
|< > > > > <|β (k + ξ) 2 d (1 + αξ + bk + k)|,|
|= > > > > > >|β (k + ξ) 2 d (1 + αξ + bk + k)|,|

>*>, stable,* > > > > > < *ϕ*(*w*) > *non-hyperbolic,* >=*,* > > > > > > > > > > :*<, saddle.*

*3. For the prey-free equilibrium point E₂* (*w*)*.*
*stable,*

*ϕ*(*w*) *non-hyperbolic,*

:*>, saddle.* *β*(*k* + *ξ*)

|∗|∗ ∗||
|---|---|---|
|∗ ∗||∗|
|∗||∗|

*4. For interior equilibrium point E* (*x, y*)*,*
8 > >*tr*(*J*) *<* 0 *and det*(*J*) *>* 0*, stable,* > < *det*(*J*) = 0*, non-hyperbolic,* > > > : *tr*(*J*) *>* 0 *or det*(*J*) *<* 0*, unstable.*

### References

[1] Peter B Banks, Andrew Daly, and Jenna P Bytheway. Predator odours attract other predators, creating an olfactory web of information. *Biology Letters*, 12(5):20151053, 2016.

[2] Dipesh Barman, Jyotirmoy Roy, and Shariful Alam. Impact of wind in the dynamics of prey– predator interactions. *Mathematics and Computers in Simulation*, 191:49–81, 2022.

[3] Dipesh Barman and Ranjit Kumar Upadhyay. Modelling predator–prey interactions: A trade-off between seasonality and wind speed. *Mathematics*, 11(23):4863, 2023.

[4] David A Beauchamp, D Wahl, and Brett M Johnson. Predator–prey interactions. *Analysis and* *interpretation of freshwater fisheries data. American Fisheries Society, Bethesda, Maryland*, pages 765–842, 2007.

[5] W-J Beyn. Numerical analysis of homoclinic orbits emanating from a takens-bogdanov point. *IMA Journal of Numerical Analysis*, 14(3):381–410, 1994.

[6] S-N Chow and Jack K Hale. *Methods of bifurcation theory*, volume 251. Springer Science & Business Media, 2012.

[7] Kim Cuddington and Peter Yodzis. Predator-prey dynamics and movement in fractal environ- ments. *The American Naturalist*, 160(1):119–134, 2002.

[8] Ellen I Damschen, Dirk V Baker, Gil Bohrer, Ran Nathan, John L Orrock, Jay R Turner, Lars A Brudvig, Nick M Haddad, Douglas J Levey, and Joshua J Tewksbury. How fragmentation and corridors affect wind dynamics and seed dispersal in open habitats. *Proceedings of the National* *Academy of Sciences*, 111(9):3484–3489, 2014.

[9] P Domenici, G Claireaux, and DJ McKenzie. Environmental constraints upon locomotion and predator–prey interactions in aquatic organisms: an introduction, 2007.

[10] Verna Louise Engstrom-Heg. Predation, competition and environmental variables: some mathe- matical models. *Journal of Theoretical Biology*, 27(2):175–195, 1970.

[11] H.I. Freedman and G.S.K. Wolkowicz. Predator-prey systems with group defence: The paradox of enrichment revisited. *Bulletin of Mathematical Biology*, 48(5):493–508, 1986.

[12] Yi-jun Gong and Ji-cai Huang. Bogdanov-takens bifurcation in a leslie-gower predator-prey model with prey harvesting. *Acta Mathematicae Applicatae Sinica, English Series*, 30(1):239–244, 2014.

[13] Kiran Kumar Gurubilli, PDN Srinivasu, and Malay Banerjee. Global dynamics of a prey-predator model with allee effect and additional food for the predators. *International Journal of Dynamics* *and Control*, 5(3):903–916, 2017.

[14] Geoff M Hilton, Graeme D Ruxton, and Will Cresswell. Choice of foraging area with respect to predation risk in redshanks: the effects of weather and predator activity. *Oikos*, pages 295–302,

1999.
[15] Jicai Huang, Shigui Ruan, and Jing Song. Bifurcations in a predator–prey system of leslie type with generalized holling type iii functional response. *Journal of Differential Equations*, 257(6):1721–1752, 2014.

[16] Yuri A Kuznetsov. *Elements of applied bifurcation theory*. Springer, 1998.

[17] Lu Li, Xiang-Ping Yan, and Cun-Hua Zhang. Turing, hopf and turing–hopf bifurcations in a modified leslie–gower predator–prey diffusive system with smith prey growth and nonmonotonic functional response. *Chaos, Solitons & Fractals*, 201:117226, 2025.

[18] Steven L Lima. Nonlethal effects in the ecology of predator-prey interactions. *Bioscience*, 48(1):25–34, 1998.

[19] Paul Marrow, Ulf Dieckmann, and Richard Law. Evolutionary dynamics of predator-prey systems: an ecological perspective. *Journal of mathematical biology*, 34(5):556–578, 1996.

[20] Ran Nathan, Gabriel G Katul, Gil Bohrer, Anna Kuparinen, Merel B Soons, Sally E Thompson, Ana Trakhtenbrot, and Henry S Horn. Mechanistic models of seed dispersal by wind. *Theoretical* *Ecology*, 4(2):113–132, 2011.

[21] Rana D Parshad, Sureni Wickramasooriya, Kwadwo Antwi-Fordjour, and Aniket Banerjee. Ad- ditional food causes predators to explode—unless the predators compete. *International Journal* *of Bifurcation and Chaos*, 33(03):2350034, 2023.

[22] Lawrence Perko. *Differential equations and dynamical systems*, volume 7. Springer Science & Business Media, 2013.

[23] BSRV Prasad, Malay Banerjee, and PDN Srinivasu. Dynamics of additional food provided predator–prey system with mutually interfering predators. *Mathematical biosciences*, 246(1):176– 190, 2013.

[24] Sourav Kumar Sasmal and Yasuhiro Takeuchi. Dynamics of a predator-prey system with fear and group defense. *Journal of Mathematical Analysis and Applications*, 481(1):123471, 2020.

[25] Andrew Sih and David E Wooster. Prey behavior, prey dispersal, and predator impacts on stream prey. *Ecology*, 75(5):1199–1207, 1994.

[26] PDN Srinivasu and BSRV Prasad. Time optimal control of an additional food provided predator– prey system with applications to pest management and biological conservation. *Journal of math-* *ematical biology*, 60(4):591–613, 2010.

[27] PDN Srinivasu and BSRV Prasad. Role of quantity of additional food to predators as a control in predator–prey systems with relevance to pest management and biological conservation. *Bulletin* *of mathematical biology*, 73(10):2249–2276, 2011.

[28] PDN Srinivasu, BSRV Prasad, and M Venkatesulu. Biological control through provision of ad- ditional food to predators: a theoretical study. *Theoretical Population Biology*, 72(1):111–120,

2007.
[29] PDN Srinivasu, DKK Vamsi, and I Aditya. Biological conservation of living systems by provid- ing additional food supplements in the presence of inhibitory effect: a theoretical study using predator–prey models. *Differential Equations and Dynamical Systems*, 26(1):213–246, 2018.

[30] Zulima Tablado, Per Fauchald, Geraldine Mabille, Audun Stien, and Torkild Tveraa. Environ- mental variation as a driver of predator-prey interactions. *Ecosphere*, 5(12):1–13, 2014.

[31] Ashraf Adnan Thirthar, Bashar Ahmed Sharba, Salam Jasim Majeed, Prabir Panja, and Thabet Abdeljawad. The dynamics of prey–predator model with global warming on carrying capacity and wind flow on predation. *Nonlinear Engineering*, 15(1):20250182, 2026.

[32] CFG Thomas, P Brain, and PC Jepson. Aerial activity of linyphiid spiders: modelling dispersal distances from meteorology and behaviour. *Journal of Applied Ecology*, pages 912–927, 2003.

[33] Urvashi Verma, Kanishka Goyal, Chanaka Kottegoda, and Rana D. Parshad. An additional food driven biological control patch model, incorporating generalized competition. *Nonlinear Science*, 6:100114, 2026.

[34] Eamonn IF Wooster, Erick J Lundgren, Dale G Nimmo, Mitchell A Cowan, Evan C Fricke, Anke SK Frank, Alexandra JR Carthey, Kathryn L Grabowski, Jennifer R Green, Grant D Linley, et al. Predator-prey temporal niche partitioning under human disturbance: a meta-analysis. *Nature Communications*, 2026.
