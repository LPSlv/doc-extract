# Multi-User MIMO Enhancement using Metasurface Wavefront Bending (MWB)

´

***Abstract*—This paper introduces metasurface wavefront bend- ing (MWB) to enhance spatial multiplexing in radiative near-**

**field multi-user multiple-input multiple-output (MU-MIMO) sys- tems. By increasing spherical-wave curvature, MWB strengthens**

**range-dependent phase variations across the receiver array, reduces inter-user channel correlation and improves user separa-**

**bility. The paper develops a curvature-dependent channel anal- ysis, a generalized-sheet-transition-condition (GSTC) synthesis**

**procedure for MWB and a complete metasurface-assisted MU-** **MIMO channel model. Both a practical common-profile scheme and an ideal user-specific benchmark are evaluated. The results**

**demonstrate that MWB provides substantial improvements in spectral efficiency and effective channel rank. Finally, a three-**

**layer transmissive Huygens metasurface architecture is proposed for physical implementation.**

***Index Terms*—MU MIMO, radiative near field, wavefront bending, plane waves and spherical waves, metasurface, spatial**

**multiplexing.**

I.INTRODUCTION
Future wireless communication systems are expected to operate at increasingly high carrier frequencies and to employ extremely large antenna apertures [1]–[5]. Since the far-field 2 limit distance scales as*d*F*≈*2*D /λ*[6], where*D*denotes the largest antenna array dimension and*λ*the wavelength, 1 the combined increase in aperture size (*D*) and decrease in wavelength (*λ*) will expand the radiative near-field zone. Regions that were in the far field in earlier systems may fall within the near field in future deployments. Within these regions, the impinging electromagnetic fields are no longer plane waves over the entire receiver aperture. Instead, they exhibit spherical wavefronts, whose spatial phase variation across the receiver apertures depends not only on the angle of arrival but also on the transmitter range [7], [8]. This range- dependent spatial structure provides an additional degree of freedom for distinguishing users located in similar angular directions but at different distances, thereby creating an oppor- tunity for enhancing spatial multiplexing in near-field multi- user multiple-input multiple-output (MU-MIMO) systems. Most near-field MIMO studies to date have focused on characterizing, estimating or processing channels naturally determined by the propagation geometry of the system. Rep- resentative research directions include extremely large array channel modeling [7], near-field beam focusing [9], near-field multiple access [10], channel estimation [11], and near-field

1 The physical size of a simple antenna (e.g., dipole antenna) scales down

|with frequency|(e.g.,ℓ=λ/2|=c/(2f)).|However,|modern|wireless|
|---|---|---|---|---|---|
|communication radiative elements (typically patches) decreases with frequency, whereas the overall array size (D) may remain identical for larger directive gain—from|systems|use antennaarrays,|where|only the size|of the|
|larger electrical directive gain.|size—or|even increase|in absolute|terms, for|super-high|

with frequency (e.g.,*ℓ*=*λ/* =*c/*(2*f*)). However, modern wireless

### Fellow, IEEE

RIS beamforming [12]–[15]. These studies have established that curved, typically spherical, phase fronts can enhance channel capacity. However, they generally treat the curved electromagnetic wavefronts incident on the receiver array as a consequence of the underlying propagation conditions. They neither elucidate the fundamental physics underlying this effect nor explore the corresponding opportunities for electromagnetic engineering. In this work, we fill up this gap, by providing the electro- magnetic explanation of the capacity enhancement in terms of physical reduced channel correlation, and using properly engi- neered metasurfaces [16]–[20] to reshape the wireless environ- ment for higher multiplexing gain. In the latter, source-shifting transmissive metasurfaces increases the effective curvature of an incident spherical wavefront, which we shall refer to as *metasurface wavefront bending (MWB)*, so as to enhance near- field MU-MIMO multiplexing. The corresponding transforma- tion is used as a design prescription and the metasurfaces are synthesized using the generalized sheet transition conditions (GSTCs) [21], which relate the desired field discontinuities to the required electric and magnetic surface susceptibilities. The resulting transmitted wavefronts exhibit increased effective curvature on the receiver side, thereby strengthening the range- dependent spatial phase variation across the base-station array, reducing inter-user channel correlation, and enhancing spatial multiplexing capability. The paper further develops a complete metasurface-assisted electromagnetic channel model, evaluates both a practical common-profile curvature-bending scheme and an ideal user-specific benchmark, and proposes a three- layer transmissive Huygens (electric and magnetic) metasur- face architecture for physical implementation [19], [22], [23]. The remainder of the paper is organized as follows. Sec- tion II explains the fundamental principle of MWB through an intuitive phase-difference and phasor-addition interpreta- tion. Section III formulates the free-space near-field uplink MU-MIMO model and shows how spherical-wave curvature affects normalized channel correlation. Section IV presents the GSTC-based metasurface synthesis used to realize the curvature-bending transformation. Section V integrates the synthesized transformation into a complete user–metasurface–

profile MWB and the user-specific benchmark. Section VII presents a physical implementation based on a three-layer transmissive Huygens metasurface. Finally, Sec. VIII con- cludes the paper.

II.PRINCIPLE

Figure 1 highlights a fundamental difference between planar

and spherical wavefronts in terms of channel correlation. Con-

Xiaolu Yang, Oscar Cespedes Vicente, and Christophe Caloz, KU Leuven, Department of Electrical Engineering, Kasteelpark Arenberg 10, 3001, Leuven, Belgium

base-station channel model. Section VI evaluates common-

## arXiv:2607.29542v1 [eess.SP] 31 Jul 2026

sider two transmitters,*T₁* and*T₂*, located at different ranges from a receiver array, with axial distances*d₁* and*d₂*, respec- tively, and range separation∆*d*=*d₂ −d₁*. The receiver array
consists of*N*elements, denoted by*R₁,...,Rn,...,RN*.
The corresponding channel vectors are written ash₁ = [*h₁₁,...,h₁N*] T andh₂ = [*h₂₁,...,h₂N*] T, with elements *jϕ*1*n jϕ*2*n* *h₁n*=*a₁ne* and*h₂n*=*a₂ne*, where*ϕ₁n*and*ϕ₂n* denote the phases produced by*T₁* and*T₂*, respectively, at the*n*th element of the receiver, leading to the relative phase difference∆*ϕn*=*ϕ₂n−ϕ₁n*. The correlation between the two channel vectors is then given by [24]

||X||X|||
|---|---|---|---|---|---|
|H|∗|||j∆ϕ||
|1|1n n=1|n|n n=1|n||

*N N* *ρ₁₂* =*|*h H 1h₂*|*= *h* *∗* 1*nh₂n*= *a₁na₂ne* *j*∆*ϕn* *,*(1)

which may be interpreted as a vector sum of phasors, where the*n*-th phasor has the magnitude*a₁na₂n*and angle∆*ϕn*.

denoting the transverse coordinate of the*n*th receiver element as*xn*, the propagation distances can be approximated as q2 2 2 <u>xn</u> *r₁n*= *d₁* +*xn≈d₁* +*,*(2a) q 2*d₂₁*

*r₂n*= *d²* +*x² ≈d₂* + <u>xn</u>

*.*(2b)
2 *n* 2*d*2

### The resulting phase difference is then

∆*ϕn*=*k₀* (*r₂n−r₁n*)*≈k₀* ∆*d*+ <u>1</u> *−* <u>1</u> *x²,* 2*d* 2*d* *n* 2 1

(3)
which is a function of*n*, causing the phasors in Eq. (1) to point in different directions and partially cancel. This partial cancellation reduces the magnitude of their resultant and, hence, the channel correlation. The preceding discussion demonstrates that spherical-wave curvature can reduce channel correlation by producing an inter-user phase difference that varies across the receiver aperture. This observation motivates the deliberate engineering of wavefront curvature illustrated in Fig. 2. A transmissive metasurface may be designed to impose a curvature-bending transformation on the incident spherical wavefronts, thereby increasing the effective curvature of the received fields. The resulting enhancement in spatial phase variation across the receiver array is expected to improve the distinguishability of the user channels, which will be demonstrated later. Figure 3 shows, for later use, a perspective view of Fig. 2 with wavefront bending (WFB) for a single user on.

Fig. 1: Channel correlation reduction from planar to spherical

wavefronts.

In the case*planar*wavefronts, represented in the left of

Fig. 1, the path-length difference between the waves radiated

by the two users is∆*d*at all the receiver elements, i.e., ∆*ϕn*=*k₀*∆*d*is constant. Therefore, all phasors in Eq. (1) point in the same direction and add coherently, yielding a max- imum resultant magnitude for the given phasor amplitudes. By contrast, for*spherical*wavefronts, shown in the right panel of

Fig. 1, the relative phase difference depends on the receiver-

element position. Denoting the propagation distances from*T₁* and*T₂* to the*n*th receiver element as*r₁n*and*r₂n*, respectively, the relative phase difference is∆*ϕn*=*k₀* (*r₂n−r₁n*), and

Fig. 2: Illustration of wavefront bending (WFB) by a properly

designed metasurface placed between the transmitters and the receiver array to reduce correlation between transmitters as shown in Fig. 1.

III.CURVATURE-DEPENDENTMU-MIMO

*A.Channel Model* We consider an uplink communication system comprising *K*single-antenna user equipments (UEs) and a base-station (BS) receiver array with*N*antenna elements, as illustrated in
Fig. 4. The BS array is positioned in the*x*–*y*plane, with
 its center selected as the origin of a Cartesian coordinate system. The position of the*n*th BS element is denoted by r *n*= (*xn,yn,*0), with*n*= 1*,...,N*. To isolate the effect of

|K|||
|---|---|---|
|n|kn k|n|
|k=1|||

Fig. 3: Perspective representation of the WFB metasurface in

Fig. 2 for a single transmitter on.

wavefront curvature, we consider the most-challenging config- uration, that shown in the figure, where the UEs are aligned in a row perpendicular to the BS and differ only in range. UE*k*is located ats*k*= (0*,*0*,−dk*), with*dk*=*d₁* + (*k−*1)∆*d*, where *dk*denotes the axial distance from UE*k*to the center of the BS array and∆*d*denotes the range spacing between adjacent UEs.

|||k|N||
|---|---|---|---|---|
|H|H|H|H||
|k k|k k k|k i̸=k interference|i i k noise||

This configuration provides no angular separability, so user discrimination relies solely on the spherical-wave curvature observed across the aperture, as illustrated in Fig. 1.

||K||−1|
|---|---|---|---|
|MMSE||H||
|k|i|i i|N k|
||i=1|||

Fig. 4: Uplink MU-MIMO system without metasurface.

The symbol transmitted by UE*k*is modeled as*sk∼* *CN*(0*,pk*), where*CN*denotes the circularly symmetric com- plex Gaussian distribution² [25], with0being the mean of and*pk*the variance, which corresponds to the transmit power

A circularly symmetric complex Gaussian random variable has a prob- ability distribution that remains unchanged under any rotation in the com- plex plane. Specifically, if*sk∼ CN*(0*,pk*), then*ejθsk*=*sk*for any *θ∈*[0*, π*). Equivalently, writing*sk*=*sk,*R+*jsk,*I, its real and imaginary parts are independent and satisfy*sk,*R*,sk,*I*∼ N*(0*,pk/*2). Consequently, E*{|sk|}*=*pk*.

of UE*k*. The received signal vector at the BS may then be written as X *K* y= h*ksk*+n*,*(4) *k*=1 whereh*k*= [*hk*1*,hk*2*,...,hkN*] T *∈*C *N*, with the superscript *T*denoting the transpose operation, represents the channel vec- tor from UE*k*to the BS array. The vectorn*∼CN*(0*,σ²*I*N*) represents circularly symmetric complex Gaussian noise³. The received signal at the*n*th BS element is therefore

X *y* = *h s* +*n.*(5)

For line-of-sight free-space propagation, the channel coeffi- cient between UE*k*and BS element*n*corresponds to the scalar spherical Green’s function [6]

*e* *−jk*0 *Rkn* *hkn*=*C₀,*(6) *Rkn* where*C₀* =*jk₀* 2 */*(4*πωϵ₀*)for a dipole source and q q *Rkn*=*∥*r*n−*s*k∥*= *x²* +*y²* +*d²* = *r²* +*d²,*(7) *n n k n k*

is the propagation distance from UE*k*to BS element*n*. To detect UE*k*, the BS multiplies the received signal vector y[Eq. (4)] by a combining vectorv *∈*C *N*, which yields X ˆ*s* =v y=v h *s* + v h *s* +v n}*,*(8) |{z | {z}

with the superscript H denoting the the Hermitian conjugate operation and where the successive terms correspond to the desired signal, residual multi-user interference and receiver noise, respectively. In this operation, the BS uses the minimum mean-square-error (MMSE) combining vector

X !

v = *p* h h +*σ²*I h*,*(9)

that maximizes the desired-signal against interference and noise [26]. For a general*K*-user system, one may quantify the inter- ference of UE*k*from the other*K−*1users as noise and define the corresponding signal-to-interference-plus-noise ratio (SINR) as [24] H 2 SINR*k*= P <u>pk|vkhk|</u> *,*(10) *pi|*v H h*i|*2+*σ ∥*2v*k∥*2 *i̸*=*k k* which corresponds to the spectral efficiency

*η* *k*= log₂(1 + SINR*k*)*.*(11)

We may also define the normalized channel correlation be- tween pair of UEs*i*and*k*among the*K*users as P*N* H *h* *∗* *h* <u>|hihk| n=1</u> *in kn* ¯ *ik* *ρ* = *∥*h*i∥∥*h*k∥* = q P*N* qP *N* *,*(12) *|hin| |hkn|* *n*=1 *n*=1

The distributionn*∼ CN* (0*,σ* I*N*)indicates thatE*{*n*}*=0and E*{*nnH*}*=*σ* I*N*. Therefore, each noise component satisfies*nn ∼* *CN*(0*,σ*)and has average powerE*{|nn|}*=*σ*.

which measures the spatial separability between these UEs independently of their path loss, with value close to one indicating very poor separability and value close to zero indicating nearly orthogonal channels. To characterize the joint spatial separability of all the*K* users, we consider the channel matrixH=*{*h₁*,*h₂*,...,*h*K}*. Let*{σi}* *r* *i*=1, where*r*is the rank ofH, denote the list of nonzero singular values of the normalized channel matrix He = H*/||*H*||*and define the corresponding normalized weights as P *q*

|=σ /|σ. We can then define the effective rank [27]|||||||
|---|---|---|---|---|---|---|---|
|i r j=1|j eff|r i i=1|i|ik|N −jk n=1 N n=1 2 in|(R −R) in kn N n=1 2 kn||

*i* the channel matrix as ! X *r* = exp *− q* ln*q,*(13)

which approaches one when the*K*channels are nearly parallel and approaches*K*when they are nearly orthogonal. For the particular case*K*= 2, the SINR of UE*k*in Eq. (10) can be expressed more intuitively in terms of its interference- free SNR, <u>pk</u> *γk*≜ 2

*.*(14)
*σ* The corresponding SINR formula is obtained by substituting Eq. (9) into Eq. (10), replacing the channel vectors with their normalized counterparts, he*k*≜h*k/∥*h*k∥*, and identifying the quantities defined in Eqs. (12) and (14) in the resulting expression, which yields

<u>γk</u> 2 SINR*k*=*γk*1*−* ¯*ikρ,*(15) 1 +*γk*

whose complete derivation is provided in Appendix A.

*B.Curvature-Dependent Performance for Two-User MIMO* We shall consider here the simplest case,*K*= 2, as in
Fig. 1, to show how spherical-wave curvature affects channel
 multiplexing performance. This case suffices to reveal the relationship between wavefront curvature and spatial separabil- ity in a direct and intuitive manner. The subsequent analysis of the metasurface-assisted system extends the performance evaluation to general*K*-user scenarios. For the spherical wavefront generated by UE*k*, the propa- gation distance*Rkn*determines the local curvature [28] at the *n*th BS element as
<u>1 1</u>

||κ =|= p||,(16)|Eq. (15)|gives SINR|= 10 (1−10/11)|=|
|---|---|---|---|---|---|---|---|---|
||kn|kn|2 k|2 n|||k||
|2|2||||||||
|n n|n n|||||ik|||
||||k||||||
|||k|||||||

*kn* 2 *R d* +*r*2

where*r* =*x²* +*y* (Fig. 4). At the center of the BS array, where*r* = 0, this curvature reduces to <u>1</u> ≜*κ.*(17) *d* Substituting Eq. (17) into Eq. (16) gives

|κ|∂κ||1||
|---|---|---|---|---|
|k||kn|||
|2 k n 2||k|2 k n 2 3/2||
||k|k|k|kn kn|

*κkn*= p*,* = *>*0*.*(18) 1 +*κ r ∂κ* (1 +*κ r*)

where the first equation relates the local curvature*κ* to the central curvature*κ*, while the second shows that*κ* increases monotonically with*κ*, so that*κ* may be used as a unique parameter to quantify the overall curvature.

Considering two UEs at distances*dk*and*di*from the receiver array and with separation∆*d*=*di−dk*. The curvature of UE*i*is related to that of UE*k*from Eq. (17), as

1 1 *κk* *κi*= = =*.*(19) *didk*+ ∆*d* 1 +*κk*∆*d* We can then evaluate the channel correlation between the two users in term of curvature. For this purpose, we first explicit Eq. (12) with Eq. (6), which yields

P <u>e</u>0 *kn in* <u>R R</u> ¯*ρ* = r r P <u>1</u> P <u>1</u> *,*(20)

*R R*

where we approximate the phase terms as q <u>r²</u> *k₀Rkn*=*k₀ d²* +*r² ≈k₀ dk*+ 2 <u>n</u> *,*(21) *k n* *dk*

the amplitude terms as1*/Rkn≈*1*/dk*, and substitute Eq. (19) in the resulting expression, which leads to the normalized channel correlation

X *N* 2 ¯ *ik* *ρ ≈* <u>1</u> exp *−j* <u>k₀</u> *κk*∆*d* *r* *n* 2 *,*(22) *N* *n*=1 2 1 +*κk*∆*d*

as a function of the central curvature*κk*. Assuming∆*d >*0, 2 the factor*κk*∆*d/*(1+*κk*∆*d*)increases monotonically with*κk*. Therefore, a larger curvature produces greater phase variation 2 across the BS elements through the factor*rn*, resulting in stronger phasor cancellation and, in general, lower channel correlation, as illustrated in Fig. 1 in the extreme comparison between planar wavefronts (*κk*= 0) and spherical wavefronts (*κk>*0).

Figure 5 presents the curvature-dependent performance for

the two-user uplink MU-MIMO system. Figure 5(a) plots, using Eq. (20),¯*ikρ* as a function of*κk*for several values of∆*d*. As*κk*approaches zero, the correlation approaches unity because the wavefronts are locally planar over the BS aperture. As*κk*increases, the greater phase variation across the aperture reduces the correlation. In addition, for a fixed *κk*, a larger range separation∆*d*leads to a lower correlation.

Figure 5(b) shows the corresponding SINR of UE*k*, evaluated

using Eq. (15) with an interference-free reference SNR of *γk*= 10 dB. In the plane-wave limit,*κk→*0and¯*ikρ →*1, *k*10*/*11, which corresponds to*−*0*.*41 dB. As the curvature increases, the reduction in¯*ρ* enables more effective suppression of co- user interference, and the SINR gradually approaches the interference-free reference value of10 dB.

### IV.METASURFACE WAVEFRONTBENDING

The benefits of increased wavefront curvature demonstrated in Sec. III-B motivate the use of a WFB metasurface, concep- tually illustrated with the receiver array in Figs. 2 and 3 and repeated with technical details in Fig. 6. A dipolar physical source generates an incident spherical wavefront, which the WFB metasurface transforms into a transmitted wavefront with greater curvature, as conceptually

(a) (b)
Fig. 5: Curvature-dependent performance for two-user MIMO

with different user spacings. (a) Normalized channel correla- tion¯*ikρ* [Eq. (20)] versus central curvature*λκk*. (b) SINR of UE*k*[Eq. (15)] versus*λκk*, evaluated using an interference- free reference SNR of*γk*= 10 dB. The system configuration corresponds to Fig. 4, with a10*×*10BS array and element spacing of*λ/*2, corresponding to aperture dimensions of *w*BS=*ℓ*BS= 4*.*5*λ*. The operating frequency is*f*= 10 GHz.

(a) (b)
Fig. 6: Metasurface wavefront bending (WFB) transformation

for a single user. (a) Perspective illustration of the transfor- mation. The metasurface is represented schematically because its deeply subwavelength unit-cell details are not visible at this scale. (b) Corresponding longitudinal-sectional view (*x*- *z*plane), with physical source at distance*d*psfrom the metasurface and virtual source for the transmitted field located at the shorter distance*d*vs.

illustrated in Fig. 6(a). As shown in Fig. 6(b), this transfor- mation is achieved by converting the incident field produced by the physical source in the plane of the metasurface, at the distance*d*ps, *−* dip Etan(*x,y*) =Etan(*x,y*;*d*ps)*,*(23a)

H *−* tan(*x,y*) =H dip tan(*x,y*;*d*ps)*,*(23b)

into a new field associated with a nearby virtual source, placed at the shorter distance*d*vs. Exact expressions of the dipole fields in Eqs. (23) are available in textbooks [6]. Prescribing the desired transmitted field to exhibit the wavefront associated with the virtual source and the same magnitude as the incident field, we have h i E + tan(*x,y*) = E *−* tan(*x,y*) exp *j*∠E dip tan(*x,y*;*d*vs)*,*(24a) h i H + tan(*x,y*) = H *−* tan(*x,y*) exp *j*∠H dip tan(*x,y*;*d*vs)*,*(24b)

where the superscripts*−*and+denote the fields immedi- ately before and after the metasurface, i.e., at*z*= 0 *−* and *z*= 0 +, respectively. According to Eq. (17), the distances *d*psand*d*vsproduce the wavefront curvatures of1*/d*psand 1*/d*vs, respectively, at the metasurface center. The condition *d*vs*< d*pstherefore produces curvature amplification, which we quantify through the bending ratio

<u>dps</u> *β*= *>*1*.*(25) *d*vs

To determine the metasurface required to realize the trans- formation prescribed in Eq. (24), we relate the electromagnetic fields immediately before and after the metasurface through GSTCs [21]. Assuming a tangential monoanisotropic meta- surface, the GSTCs read

zˆ*×*∆H=*jωϵ₀χ*eeEav*,*(26a) ∆E*×* zˆ=*jωµ₀χ* Hav*,*(26b) mm

where *χ*eeand *χ*mmdenote the electric and magnetic surface susceptibility tensors, respectively, and where we define the field jumps and averages as

∆E=E + *−*E *−* *,*∆H=H + *−*H *−* *,*(27a) <u>E</u> + <u>+E</u> *−* <u>H</u> + <u>+H</u> *−* Eav=*,*Hav=*.*(27b) 2 2 Inserting Eqs. (27) into Eqs. (26) yields the scalar equations

*xx xy* *−*∆*Hy*=*jωϵ₀* (*χ*ee*Ex,*av+*χ*ee*Ey,*av)*,*(28a) ∆*H* =*jωϵ* (*χ* *yx* *E* +*χ* *yy*

*E*)*,*(28b)
*x* 0 ee *x,*av ee *y,*av ∆*Ey*=*jωµ₀* (*χ* *xx* mm*Hx,*av+*χ* *xy* mm*Hy,*av)*,*(28c) *yx yy* *−*∆*Ex*=*jωµ₀* (*χ*mm*Hx,*av+*χ*mm*Hy,*av)*.*(28d)

Further assuming nongyrotropy, i.e.,*χ* *xy* =*χ* *yx* =*χ* *xy* = ee ee mm *χ* *yx* = 0, and considering an*x*-directed incident electric field mm reduce Eqs. (28) to

*−*∆*Hy*=*jωϵ₀χ* *xx* ee*Ex,*av*,*(29a) *−*∆*Ex*=*jωµ₀χ* *yy* *Hy,*av*,*(29b) mm

with the dipolar fields in Eq. (23) being approximated in the *radiative near-field zone*by their far-field expressions⁴

2 *Ex*(*x,y*;*d*) =*Ex*(*R*) =*jIℓk₀* exp (*−jk₀R*)*/*(4*πωϵ₀R*)*,* (30a) *Hy*(*x,y*;*d*) =*Hy*(*R*) =*jIℓk₀d*exp (*−jk₀R*)*/*(4*πR²*)*,* (30b) p where*R*= *x²* +*y²* +*d²*. Using the physical-source distance*d*psand the virtual-source distance*d*vs, we explicitly write the incident tangential fields at the metasurface as

*E* *−* (*x,y*) =*E* (*x,y*;*d*)*,*(31a) *x x* ps *Hy−*(*x,y*) =*Hy*(*x,y*;*d*ps)*,*(31b)

One may naturally use the complete exact dipole fields [6] in the synthesis of our susceptibilities, but only the dominant far-field terms—with their *radiative near-field*curvature—play a significant role in this operation of WFB because the relevant distances are much larger than the reactive near field (*R < λ/*2, [29]), which involves the remaining terms.

and the prescribed transmitted fields as

|+|−|||
|---|---|---|---|
|x|x|x|vs|
|y+|y−|y|vs|

*E* (*x,y*) =*|E* (*x,y*)*|*exp [*j*∠*E* (*x,y*;*d*)]*,*(32a) *H* (*x,y*) =*|H* (*x,y*)*|*exp [*j*∠*H* (*x,y*;*d*)]*.*(32b)

### Equations (29) provide the susceptibilities

*xx*<u>∆Hy(x,y)</u> *χ*ee(*x,y*) =*−,*(33a) *jωϵ₀Ex,*av(*x,y*)

*yy*<u>∆Ex(x,y)</u> *χ*mm(*x,y*) =*−,*(33b) *jωµ₀Hy,*av(*x,y*)

where the difference and average fields are obtained by substituting Eqs. (31) and (32) into Eqs. (27). The prescribed MWB transformation is thus synthesized through the electric susceptibility*χ* *xx* eeand the magnetic susceptibility*χ* *yy* mmof the metasurface.

Figure 7 shows the susceptibility distributions obtained from

Eq. (33). Figures 7(a) and 7(b) present the real parts of*χ* *xx* eeand *χ* *yy* mm, respectively. The radial symmetry of the susceptibilities results from the coaxial configuration of the physical and virtual sources. The pronounced annular variations occur near locations where the incident and prescribed transmitted fields approach an antiphase condition. At these locations, the aver- age tangential fields in the denominators of Eq. (33) is small while the corresponding field jumps remain finite, resulting in large local susceptibility values. The imaginary parts shown in Figs. 7(c) and 7(d) remain close to zero over most of the aperture, indicating that the synthesized transformation is predominantly reactive and involves negligible loss.

(a) (b)
Fig. 8: Local transmission coefficient [Eq. (34)] corresponding

to the susceptibilities in Fig.7. (a) Magnitude,*|T|*. (b) Phase, ∠*T*.

and (32) into Eqs. (27), and then substituting the resulting field averages and field jumps into Eqs. (29), which yields

<u>4 +k₀</u> 2 <u>χ</u> *xx* <u>eeχ</u> *yy* <u>mm</u> *T*(*x,y*) = (2 + *jk₀χxx* ee) (2 +*jk₀χ* *yy* mm)

*.*(34)
That is a*local* + transmission coefficient—a function of*x*and *y*at*z*= 0, which is plotted in Fig. 8 for the susceptibilities in Fig.7

V.MODELINGCOMPLETESYSTEM
*A.System Configuration*
Figure 9 shows the complete metasurface-assisted uplink
 MU-MIMO system, in which the*K*UEs transmit toward the BS through a transmissive metasurface positioned between them. The metasurface lies in the*x*–*y*plane, with its center selected as the origin of a Cartesian coordinate system. The metasurface comprises*M*subwavelength unit cells, where unit cell*m*is located atr

||= (x|,y ,0), withm= 1,...,M.||
|---|---|---|---|
||MS m|m m||
|BS n|n n MR||MR|
||||TM k|
||TM k|TM 1|TM k|
 The BS comprises*N*antenna elements, where element*n*is lo- cated atr = (*x,y,d*), with*n*= 1*,...,N*. Here,*d* denotes the axial distance between the metasurface and BS planes. UE*k*lies on the broadside axis ats*k*= (0*,*0*,−d*), with*k*= 1*,...,K*and*d* =*d* + (*k−*1)∆*d*, where*d* denotes the axial distance between UE*k*and the metasurface plane, and∆*d*denotes the range spacing between adjacent UEs. The corresponding axial distance between UE*k*and the BS plane therefore follows as*d*
TR *k*=*d* TM *k*+*d* MR.

*B.Channel Model for Common-Profile Curvature Bending* Following the synthesis procedure in Sec. IV, we select UE*i* as the reference UE and design the metasurface to increase the curvature of its incident wavefront by a prescribed bending ratio*β*. The reference UE*i*generates the incident field
<u>e</u> *−jk*0 *Rim* TM *−*

|||||E (x ,y|) =E x|,y ;d||,(35)|
|---|---|---|---|---|---|---|---|---|
||ps yy|xx|xx ee|i m|m x|m m i|TM im||
|yy mm|mm|ee|||||0 TM|0|
||||||||im||
|+||||TM im|TM 2 i|2 2 m m|TM 2 i|2 m|

*m m x m m* TM *≈C₀* *i i* *R* TM *im*

at metasurface element*m*, where*C* =*jk²/*(4*πωϵ*)under the unit-current-moment (*Iℓ*= 1) and*R* denotes the distance between UE*i*and metasurface element*m*, q q *R* = *d* +*x* +*y* = *d* +*r.*(36)

Fig. 7: GSTC-synthesized WFB metasurface susceptibilities

*xx* [Eqs. (33)] for*d*ps= 10*λ*and*β*= 8. (a) Real part of*χ*.

(b) Real part of*χ*. (c) Imaginary part of*χ*. (d) Imaginary part of*χ*. The transmission coefficient just after the metasurface, at *z*=, may be obtained by first substituting Eqs. (31)

|+||−|||
|---|---|---|---|---|
|k m −|m|k m|m (MS i,β)|m m|
|k m|m|(MS i,β)|m m||
|||+ k m|m||

Fig. 9: Metasurface assisted MU-MIMO system configuration.
 According to the transformation prescribed in Eq. (24), the amplitude of the incident field is preserved while the phase is associated with a virtual source at the axial distance*d*
TM *i/β*. The target transmitted field of UE*i*is therefore

+<u>d</u> TM <u>i</u> *Ei*(*xm,ym*) = *Ei−*(*xm,ym*) exp *j*∠*Exxm,ym*;*.* *β* (37) Taking the ratio of Eqs. (35) and (37) yields the metasurface local transmission coefficients

<u>Ei</u> + <u>(xm,ym)</u> *T*(MS *i,β*)(*xm,ym*) = *−* *Ei*(*xm,ym*) <u>d</u> TM <u>i</u> = exp *j* ∠*Exxm,ym*; *β* TM *−*∠*Exxm,ym*;*di,*(38)

where s  TM TM 2 <u>di</u>  <u>di</u> 2  ∠*Exxm,ym*; =*−k₀* +*rm,*(39a) *β β* q TM TM 2 2 ∠*Exxm,ym*;*di*=*−k₀ di*+*rm,*(39b)

2 p with*rm*= *x²m*+*ym*2. Substituting Eq. (39) into Eq. (38) gives  s  <u>d</u> TM 2 *T*(MS *i,β*)(*xm,ym*) = exp *−jk₀*  <u>i</u> +*rm*2  *β* q TM 2 2 *− di*+*rm.*(40)

We will use Eq. (40) as a common transmission profile and apply it to the incident fields of all UEs. We now consider an arbitrary UE*k*and derive its channel to the BS array through the metasurface. UE*k*generates the incident field *−jk Rkm* TM *−* TM<u>e</u>

|(x E|,y ) =E|x ,y|;d ≈C₀||||(49)|
|---|---|---|---|---|---|---|---|
|k m|m|x m m|k|TM||||
|||||km||||

*k m m x m m k* TM *,*(41) *R* *km*

at metasurface element*m*, where*Rkm* TM denotes the distance between UE*k*and metasurface element*m*, q q TM TM 2 2 2 TM 2 2 *Rkm*= *d* *k* +*xm*+*ym*= *d* *k* +*rm.*(42)

The common metasurface profile transforms the incident field of UE*k*into the transmitted field,

### E (x,y) =E (x,y)T (x,y),(43)

where*E* (*x,y*)and*T* (*x,y*)are given by Eqs. (41) and (40), respectively. The transmitted field*E* (*x,y*)subsequently propagates from the metasurface to the BS array. We model this stage using a Rayleigh–Sommerfeld-like scalar diffraction formula- tion [30], which gives the channel coefficient between UE*k* and BS element*n*as ZZ *−jk*0 *R* MR MR <u>1</u>+<u>e</u>*mn*<u>d</u> *hkn*= *E* (*xm,ym*) d*xm*d*ym,* *jλA* MS *k* *Rmn* MR*Rmn* MR (44) where the factor*d* MR */R*is the Rayleigh–Sommerfeld obliq- uity factor, which weights the contribution of each aperture point according to its direction with respect to BS element

*n*. We assume that each metasurface unit cell has area∆*S* and discretize Eq. (44) over the*M*elements. Substituting this discretization,*dxmdym*= ∆*S*and Eq. (43) into Eq. (44) gives
*M* MR <u>∆S</u> X*−* MS*e* *−jk*0 *Rmn* <u>d</u> MR *hkn≈* *jλ* *E* *k* (*xm,ym*)*T*(*i,β*)(*xm,ym*) *Rmn* MR*Rmn* MR *.* *m*=1 (45) Substituting then Eq. (41) and Eq. (40) into Eq. (45) yields the explicit expression of the channel as

<u>∆S</u> X *M* <u>C₀ d</u> MR *hkn*(*β*)*≈* *jλ R* TM (*R*MR) 2 *m*=1 *km mn* TM MR exp *−jk₀ Rkm*+*Rmn* s  TM 2 q   <u>di</u> 2 TM 2 2  + +*rm− di*+*rm,* *β* 

(46)

where*Rmn* MR is the distance between metasurface element*m* and BS element*n*, q *R* MR = (*d*MR) 2 + (*x −x*)2+ (*y −y*)2 *mn n m n m* q = (*d*MR) 2 +*r².*(47) *mn*

For compactness, we shall later collect the amplitude factor in the expression (46) as

<u>∆SC d</u> MR <u>0</u> *Akmn*= 2

*.*(48)
*jλR* *km* TM (*Rmn* MR)

Particularly, the channel coefficient of the reference UE (*k*=*i*) takes the simpler form    s TM MR <u>di</u>  *hin*(*β*) =*Aimn*exp *−jk₀ Rmn*+ +*rm,*  *β* 

presents the spectral efficiency sum using Eq. (11), with the channel coefficients given by Eqs. (46) and (49). Figure 10(a) shows that, without the metasurface, the normalized channel correlation remains high. This occurs because in the consid- ered configuration, the reference UE*i*lies at an axial distance

|||||2d|ofd = 60λfrom the BS, which yields only weak spherical-|
|---|---|---|---|---|---|
|||||k|TR i|
|MR|MR 2|2|MR|mn 2||
|mn||mn||MR||
|TM|2|TM|2|||
|i|2 m|i|m TM|||
||||i|||
|TM|2 2|TM|m 2|||
|i|m|i|TM|||
||||i|||

TR *i* wave curvature across the BS aperture and therefore provides insufficient spatial variation for distinguishing channel vectors. After applying the common-profile WFB metasurface,¯*ikρ* initially decreases as*β*increases, reaches a minimum at an intermediate bending ratio, and then increases at larger values of*β*. The dependence on the range separation∆*d*also remains nonmonotonic over the considered bending-ratio range. The strongest decorrelation occurs for∆*d*= 2*λ*, for which the channel correlation decreases to approximately0*.*1at*β*= 8. The spectral efficiency sum in Fig. 10(b) exhibits the inverse trend. It increases as the channel correlation decreases, reaches its maximum close to the correlation minimum, and then decreases when the correlation rises again.

To separate the phase contributions of the different prop- agation stages and identify their dependence on the bending ratio, we approximate the phase terms in Eq. (46) as q2 TM TM 2 2 TM<u>rm</u> *k₀Rkm*=*k₀ d* *k* +*rm≈k₀ dk*+ TM *,* *k* (50a) q <u>r</u> *k₀R* =*k₀* (*d*) +*r ≈k₀ d* +*,* 2*d* (50b) s 

 *d*  *d r* *k₀* +*r ≈k₀* +*,*(50c) *β β* 2*d /β* q <u>r</u> *k₀ d* +*r ≈k₀ d* +*.*(50d) 2*d*

Substituting Eqs. (50) and (48) into Eq. (46) gives then phase- approximated channel of UE*k*as

X *M* <u>r²</u> *hkn*(*β*)*≈ Akmn*exp *−jk₀ d* TM *k*+TM <u>m</u>

*m*=1 2*d* *k* *d* TM *iβrm* 2 TM*rm* 2 + + TM *− di*+ TM *β* 2*d* *i*2*di* MR<u>rmn</u> 2 + *d* + MR

*.*(51)
2*d*

The first term inside the square brackets represents the prop- agation phase from UE*k*to metasurface element*m*. The difference between the second and third terms represents the common curvature-bending phase imposed by the reference UE*i*. The final term represents the propagation phase from metasurface element*m*to BS element*n*. Particularly, the channel coefficient of the reference UE (*k*=*i*) takes the simpler form

|M|TM||i k|||||
|---|---|---|---|---|---|---|---|
|imn|i|TM m|i k|||||
|m=1|MR|i mn 2 MR||||MS BS BS|MS|
|||||||TM||
||||MR|TR i|TM i|i||

X *M* <u>d βr²</u> *hin*(*β*)*≈ A* exp *−jk₀* + *β* 2*d*

<u>r</u> + *d* +*.*(52) 2*d*

VI.DEMONSTRATION

This section uses the complete channel model in Sec. V to quantify the multiplexing gains achieved with MWB. The evaluation first considers a practical common-profile scheme, where a MWB profile is designed for one reference UE and then applied to all UEs. We then compare this practical scheme with a user-specific MWB benchmark, where each UE is assigned an ideal curvature-bending profile. The benchmark clarifies the spatial multiplexing gain attainable when distinct curvature signatures can be assigned to different users.

*A.Performance under Common-Profile Curvature Bending* Consider the reference UE*i*and an arbitrary UE*k*.
Figure 10 plots the corresponding two-user performance as
 a function of the bending ratio. Figure 10(a) presents the normalized channel correlation in Eq. (12) and Fig. 10(b)
(a) (b)
Fig. 10: Two-user MIMO performance for common-profile

MWB as a function of the bending ratio*β*, obtained for the system configuration shown in Fig. 9. (a) Normalized channel correlation,¯*ikρ* [Eq. (12)]. (b) Spectral efficiency sum, *i k* *η* +*η* [Eq. (11)], with the interference-free reference SNR of *γ* =*γ* = 10 dB. The metasurface profile is designed for the reference UE*i*and applied to both UEs as a common profile. The simulation parameters are*f₀* = 5 GHz,*ℓ* =*w* = 10*λ*, with a unit-cell spacing of*λ/*5,*ℓ* =*w* = 10*λ*, with an antenna-element spacing of*λ/*2,*d* = 10*λ*, and *d* = 50*λ*,*d* =*d* +*d* MR = 60*λ*.

To explain the nonmonotonic dependence on*β*observed in

Fig. 10, we explicitly derive the elementwise cross-channel

product*h* *∗* *inhkn*using Eq. (52) and Eq. (51). This product takes the form

TM TMX *M*X*M* *h* *∗* *inhkn≈e* *−jk*0 (*dk−di*) *A* *∗* *iqnAkmn* *m*=1 *q*=1 <u>1 1</u>2 exp *−jk₀* 2*d* TM *−* 2*d* TM *i* *r* *m* *k* <u>β</u>2 2 + TM *r* *m−rq* *di*

+ *rmn−rqn.*(53) *d*MR The exponent in Eq. (53) contains three aperture-dependent phase contributions. The first contribution results from the

range mismatch between the reference and non-reference UEs. The second contribution is directly controlled by the bending ratio*β*. The third contribution arises from propagation between the metasurface and the BS array. The numerator of the normalized correlation in Eq. (12) is obtained by summing Eq. (53) over the BS-element index*n*. It is therefore a finite, geometry-dependent phasor sum over the metasurface indices *m*and*q*and the BS index*n*. Its value depends jointly on*β*, MR ∆*d*,*d*, and the metasurface and BS aperture dimensions.

|T|(x ,y ) = exp|∠E x|,y; d||
|---|---|---|---|---|
|(US k,β)|m m|x m|m||
||||k||
|||x m m|TM k US k|k|

Consequently, neither the bending ratio nor the range separa- tion alone determines the resulting correlation. As*β*increases from unity, the second phase term in Eq. (53) produces a larger phase dispersion. The corresponding phasors then add less coherently in Eq. (12), causing the channel correlation to decrease. When*β*becomes very large, however, the bending- related phase factor wraps rapidly across the finite metasurface aperture and interacts with the fixed range-mismatch and MS–

||US|H US|
|---|---|---|
||i i|k k|
|ik i k|US i i|US k k|

BS propagation factors. The phasor sum can then become par- tially coherent again, producing the increase in¯*ikρ* observed at large*β*in Fig. 10(a). The same expression also explains the nonmonotonic dependence on∆*d*: increasing∆*d*enlarges the first phase term in Eq. (53) and strengthens decorrelation over a useful range, but excessive mismatch can again produce phase wrapping rather than monotonic improvement. The common-profile MWB scheme is next evaluated for arbitrary*K*(*K≥*2). The closest UE is selected as the reference UE, and the same metasurface from Eq. (40) is applied to all users. For each UE, the channel vector is assembled from Eq. (46). Figure 11 reports the resulting MU- MIMO performance, where the spectral efficiency sum follows Eq. (11) and the effective channel rank follows Eq. (13). The first row in the figure involves*K*UEs located along the same broadside direction, with an adjacent range spacing ∆*d*= 2*λ*. Without the metasurface, the spectral efficiency sum and effective rank remain low because the UE channels are nearly parallel. The common-profile MWB scheme provides a clear improvement over the no-MS case. Increasing the bending ratio further enhances both metrics, indicating that the curvature-bending metasurfaces creates additional spatial diversity even when the users are angularly aligned. The sec- ond row pertains to UEs that are randomly distributed within a range-angle sector. Unlike the same-direction arrangement, these UEs possess natural diversity in both range and angle, so the no-MS baseline already benefits from angular sepa- ration. The common-profile MWB scheme further enhances the multiplexing by introducing curvature-induced diversity in addition to the existing angular diversity. In both rows, the incremental benefit of MWB tends to saturate as the number of users*K*increases because a single common metasurface cannot generate a new independent spatial mode for every additional UE. Nevertheless, for any fixed*K*, the bending- induced phase diversity reduces the overall channel similarity and enhances the multiplexing capability relative to the no-MS case.

*B.Performance under User-Specific Curvature Bending* The common-profile MWB scheme uses the same metasur- faces for all UEs. This is the simplest practical configuration,
but it limits in the maximum achievable multiplexing gain. To quantify the additional gain available from independent wavefront-curvature control, we here introduce an ideal user- specific MWB benchmark. For UE*k*, the transformation profile is obtained by replacing the reference distance in Eq. (40) with*d* TM *k*and by assigning a user-specific bending ratio*βk*, which yields TM <u>k</u> (US *k,βk*) *m mjx m m* *βk* *−*∠*E x,y*;*d.*(54)

The corresponding channel vector, denoted byh (*β*), is evaluated using the complete UE–metasurface–BS channel model in Eq. (45), with the bending profile designed specif- ically for UE*k*. For UEs*i*and*k*, the normalized channel correlation is

h (*β*) h (*β*) ¯*ρ* (*β,β*) =*.*(55) h (*β*) h (*β*)

The bending-ratio assignment proceeds sequentially. The first UE is assigned a specific bending ratio,*β₁*. When UE *k*(*k≥*2)is added, the previously assigned bending ratios *β₁,...,βk−*1remain fixed. Eq. (45) generates the channel of UE*k*from each available candidate*β∈ B*, and Eq. (55) evaluates its correlations with all previously assigned*k−*1 UE channels. The selected bending ratio for UE*k*minimizes the largest pairwise correlation:

*βk*= arg min 1 max *<i<k* ¯ *ik* *ρ* (*βi,β*)*.*(56) *β∈B\{β₁,...,βk−*1*}*

Thus, each newly introduced UE is assigned the bending ratio that minimizes its largest pairwise channel correlation with the preceding*k−*1UEs. The resulting bending-ratio sets for*K*= 2*,...,*10are listed in Appendix B. Because the benchmark assigns a different phase profile to each UE, it represents an ideal upper-bound reference.

Figure 12 compares the no-MS case, the common-profile

MWB scheme with*β*= 8, and the user-specific MWB bench- mark. The no-MS and common-profile channels are generated using the physical channel models developed in Secs. III and V, respectively, whereas the user-specific benchmark is constructed from the ideal curvature channels defined above. The first and second rows of Fig. 12 correspond, respectively, to the same-direction UE arrangement in Fig. 11(a) and the random-sector arrangement in Fig. 11(d). In both configura- tions, the common-profile MWB scheme improves the multi- plexing capability relative to the no-MS case, although the gain remains limited by the use of a single shared MWB profile. For the user-specific benchmark, the effective rank is equal to *K*, while the spectral efficiency sum increases approximately linearly with*K*in both rows. These observations confirm that the benchmark provides mutually orthogonal channel vectors for all K users, regardless of the UE distribution. Realizing the user-specific benchmark would require differ- ent curvature transformations to be applied simultaneously to the incident fields of different UEs. Such functionality cannot be achieved by a unique metasurface placed between the users

(a)
(b) (c)
(d)
(e) (f)
Fig. 11: Multi-user performance for the common-profile MWB scheme for different bending ratios*β*. First row: *K*same-

direction UEs with adjacent range spacing∆*d*= 2*λ*: (a) system configuration, (b) spectral efficiency sum, and (c) effective channel rank. Second row: UEs randomly distributed in the specified range-angle sector: (d) system configuration, (e) spectral efficiency sum, and (f) effective channel rank. The UE-to-MS-center distance is independently and uniformly distributed over TM *◦* *◦* *d* *∈*[5*λ,*12*λ*], while the angular position is independently and uniformly distributed over*θ ∈*[*−*15 *,*15], corresponding *k* *◦* to a sector centered around the broadside direction with a total angular span of30. The remaining system parameters are the *i*

### same as those in Fig. 10.

and the BS. It would therefore require additional user-selective degrees of freedom, potentially enabled by a sophisticated con- stellation of active, nonlinear or spatiotemporally modulated metasurfaces. Accordingly, the user-specific result here is in- terpreted as an idealized, upper-bound benchmark, illustrating the potential of future metasurface architectures with user- selective wavefront control. The following implementation dis- cussion instead focuses on the common-profile MWB scheme, which is compatible with a passive transmission profile.

VII.METASURFACEIMPLEMENTATION In the preceding sections, we have assumed a metasurface with a continuously varying local transmission phase associ- ated with continuous mathematical susceptibility functions. In practice, however, a metasurface consists of finite-sized unit cells and can provide only a discrete set of transmission states. We therefore quantize here the continuous phase∠*T*(*x,y*) into eight uniformly spaced states over the full2*π*range, corresponding to a phase resolution of∆*ϕ*=*π/*4. The quantized transmission phase assigned to the unit cell at (*xm,ym*)is therefore <u>∠T(x,y)</u>

|||m m|
|---|---|---|
|quan|m m||

∠*T* (*x,y*) = ∆*ϕ×*round*,*(57) ∆*ϕ* with the resulting phase wrapped into the interval(*−π,π*]. The corresponding local transmission coefficient is

*T*quan(*xm,ym*) = exp [*j*∠*T*quan(*xm,ym*)]. Figure 13 shows the realization of the MWB transformation under3-bit phase quantization. Figure 13(a) shows the eight-state phase map obtained from the continuous GSTC-designed transmission phase in Fig. 8(b), using Eq. (57). Figure 13(b) verifies the resulting transmitted field. The output wavefront remains more strongly curved than the incident field, indicating that the essential MWB operation survives finite phase quantization.

To evaluate the system-level impact of phase quantization, we replace the ideal common-profile transmission coefficient *T* MS (*x,y*)in Eq. (45) with the coefficient*T* (*x,y*) (*i,β*) *m m* quan *m m* constructed from Eq. (57). We then assemble the channel vector of each UE using Eq. (45), and evaluate the spectral efficiency sum and effective channel rank using Eqs. (11) and (13), respectively. Figure 14 compares the no-MS ref- erence and the common-profile MWB scheme with*β*= 8 using the ideal continuous phase profile in Fig. 8(b) and the eight-state quantized profile in Fig. 13(a). For both the same- direction UE configuration in Fig. 11(a) and the random-sector configuration in Fig. 11(d), phase quantization introduces only minor performance deviations while preserving most of the MWB gain relative to the no-MS case. These results demonstrate that3-bit phase control preserves the principal MU-MIMO multiplexing enhancement achieved by the ideal continuous-phase MWB system.

(a) (b)
(a) (b)
Fig. 14: Effect of phase quantization on the common-profile

MWB performance for*β*= 8, with ideal-bending curves obtained for the continuous transmission phase in Fig. 8(b) and actual-bending curves obtained after applying the discrete phase profile in Fig. 13(a). The left and right vertical axes report the spectral efficiency sum computed from Eq. (11) and the effective channel rank computed from Eq. (13), respectively. (a) Same-direction UE configuration in Fig. 11(a).

(b) Random-sector UE configuration in Fig. 11(d).
(c) (d)
Fig. 12: Comparison of the multi-user performance achieved

by the user-specific MWB benchmark and the common-profile *ϵ* *r*= 3, loss tangenttan*δ*= 0*.*001, and spacer thickness MWB scheme with*β*= 8. First row: same-direction UE

1*.*52 mm, resulting in a total dielectric thickness of3*.*04 mm.
configuration (in Fig. 11(a)): (a) spectral efficiency sum and

Figure 15 shows the adopted unit-cell topology. The metallic

(b) effective channel rank. Second row: randomly distributed
dogbone is oriented to accommodate the*x*-polarized incident UE configuration (Fig. 11(d)): (c) spectral efficiency sum and field assumed in the channel model.

(d) effective channel rank.
**H** **E**

(a) (b)
Fig. 13: Eight-state quantized realization of the WFB meta-

surface. (a) Transmission phase distribution obtained from discretizing the continuous profile in Fig. 8(b) according to Eq. (57). (b) Resulting wavefront curvature bending transfor- mation.

To realize a physical metasurface, we map the quantized phase states in Fig. 13(a) onto subwavelength scattering par- ticles and adopt three-layer dogbone Huygens metasurface architecture. The symmetric three-layer configuration provides the minimum degrees of freedom required to independently control the effective electric and magnetic surface responses. When these responses are properly balanced, the backward- scattered fields cancel, ideally yielding zero reflection and full transmission while providing complete2*π*transmission-phase coverage [19], [22]. The metallic layers are separated by two Rogers RO3003 dielectric spacers with relative permittivity

(a) (b)
Fig. 15: Metasurface scattering particle with generic variable

dimensions. (a) Unit cell perspective view with dielectric substrates made transparent for visualization. (b) Unit cell front view with dogbone-shaped metallic particle.

Based on the three-layer dog-bone architecture shown in

Fig. 15, eight unit cells are designed to realize the quantized

transmission-phase states required by the MWB profile. Table I lists the optimized design parameters and the corresponding target transmission phase assigned to each unit cell. We simulated the eight unit cells in CST Microwave Stu- dio using the topology shown in Fig. 15, the geometrical dimensions listed in Table I and periodic boundary conditions.

Figure 16 presents the corresponding full-wave transmission

responses under normal incidence, with*θi*= 0 *◦*. Figure 16(a) shows that the eight unit cells collectively cover the full *◦* transmission-phase range around the operating frequency of10 GHz, with an approximately45 *◦* phase interval be- tween adjacent states. Figure 16(b) shows that most unit cells maintain high transmission magnitudes (*|T|>.*9) near the

TABLE I: Design parameters and target transmission phases for the eight unit cells. OL denotes the identical outer layers (top and bottom), and ML denotes the middle layer.

*Common design parameters*

|f|(GHz)|||10|||
|---|---|---|---|---|---|---|
|L =L|(mm)|||5.50|||
|W =W||(mm)||0.50|||
|A =A|(mm)|||0.50|||
|t =t|(mm)|||1.52|||
|p =p|(mm)λ||Cell 1|/5 = 6.00 Cell 2|Cell 3|Cell 4|
|Target phase−135||||−90|−45|0|
|B|(mm)||1.77|1.26|0.70|5.80|
|B|(mm)||4.50 Cell 5|5.80 Cell 6|4.50 Cell 7|1.24 Cell 8|
|Target phase45||||90|135|180|
|B|(mm)||2.45|2.20|2.00|1.80|
|B|(mm)||1.95|1.92|1.85|1.28|

0 OL ML *x* *x* OL ML *y* *y* OL ML *x* *x* 1 2 *x y* 0

(a)
- *◦ ◦ ◦*
OL *y* ML *y*

- *◦ ◦ ◦*
OL *y* ML *y*

operating frequency. These results confirm that the eight-state quantized phase profile in Fig. 13(a) can be implemented using the proposed three-layer unit-cell library, thereby linking the GSTC-derived MWB phase profile to a realizable passive metasurface. Appendix C further reports the transmission responses of the eight unit cells under oblique incidence.

VIII.CONCLUSION

This paper introduced metasurface wavefront bending (MWB) to enhance radiative near-field MU-MIMO multi- plexing by increasing spherical-wave curvature and reducing inter-user channel correlation. The proposed MWB design and system-level evaluations demonstrated substantial improve- ments in spectral efficiency sum and effective channel rank. Future work will further optimize the metasurface unit-cell design to improve its robustness under oblique incidence and will focus on the fabrication and experimental validation of the proposed metasurface-assisted MU-MIMO system.

|MMSE|H −1||
|---|---|---|
|k|k k|k|

APPENDIXA DERIVATION OF THECORRELATION-DEPENDENTSINR

We consider two UEs, indexed by*i*and*k*, with equal transmit powers*pi*=*pk*=*p*. To isolate spatial separability from channel path loss, we normalize the channel vectors as

h e *i*=*,* h e *k*=*,*(58) <u>hihk</u> *∥*h*i∥ ∥*h*k∥*

such that*∥*he*i∥*=*∥*he*k∥*= 1. For the detection of UE*k*, we replace the channel vectors in Eq. (10) with the normalized ones in Eq. (58). The resulting normalized-channel SINR becomes *p* v*k* H h e *k* SINR*k*=*.*(59) *p* v *k* H h e *i*+*σ²∥*v*k∥*

(b)
Fig. 16: Simulated transmission responses of the eight three-

*◦* layer dogbone unit cells under normal incidence,*θi*= 0. The unit-cell architecture is shown in Fig. 15, and the corresponding geometrical parameters are listed in Table I.

(a) Transmission phase and (b) transmission amplitude versus frequency. For this two-user system, the MMSE combining vector in Eq. (9) becomes MMSE H H 2
*−*1 v = *p*he e*i*h +*p*he*k*he +*σ* I*N*he*k.*(60) *k i k*

We define the interference-plus-noise terms in Eq. (60) as

R*i*≜*p*he*i*he H *i*+*σ²*I*N.*(61)

Substitution of Eq. (61) into Eq. (60) gives

v = R +*p*he he he*.*(62) *i*

Applying the matrix inversion lemma to Eq. (62) yields

<u>R</u> *−*1 <u>h</u> <u>e</u> MMSE <u>i k</u> v*k*= H *−*1

*.*(63)
1 +*p*he *k* R*i*he*k*

The denominator in Eq. (63) is a nonzero scalar. Moreover, any nonzero scaling of the combining vector leaves the output SINR unchanged [25]:

SINR (*kc*v ) = SINR (v )*k k k, c̸*= 0*.*(64)

Indeed, replacingv*k*with*c*v*k*in Eq. (59) multiplies the desired-signal, interference, and noise powers by the same factor*|c|*, which cancels between the numerator and denom- inator. Equation (64) therefore allows us to omit the scalar

denominator in Eq. (63) and use the equivalent combining vector as v*k*=R *−* *i* 1 h e *k*

*.*(65)
We first substitute Eq. (65) into the numerator of Eq. (59) and obtain

||H 2|H −1|2||
|---|---|---|---|---|
||k k|k i|k||
||i||||
|H 2|2 H|H|2|H|
|k i|k k|i i|N k|k i k|

*p* v he =*p* he R he*.*(66)

Using the definition ofR in Eq. (61), we rewrite the denom- inator of Eq. (59) as

2 *p* v he +*σ ∥*v *∥* =v *p*he he +*σ* I v =v R v*.* (67) Substitution of Eq. (65) into Eq. (67) then gives

v*k* H R*i*v*k*= he H *k*R *−* *i* 1 R*i*R *−* *i* 1 h e *k*= h eH *k*R *−* *i* 1 h e *k*

*.*(68)
BecauseR*i*is Hermitian positive definite, the quadratic form h eH *k*R *−* *i* 1 h e *k*is real and strictly positive. We therefore substitute Eqs. (66) and (68) into Eq. (59) and cancel the common quadratic factor. This substitution yields

H *−*1 SINR*k*=*p*he*k*R*i*he*k.*(69)

*−*1 We next evaluateR*i*. Applying the Sherman–Morrison iden- tity [25] to Eq. (61) gives " # *−*1 2 H *−*1<u>1 p</u> H R*i*= *σ* I*N*+*p*he*i*he*i*= 2 I *N−* h e *i* h e *i* *σ σ²* +*p∥*he *i* *∥* 2 (70) e 2 Using*∥*h*i∥* = 1, we simplify Eq. (70) to

*−*1<u>1</u> *p* e eH R*i*= 2 I *N−*2h*i*h*i.*(71) *σ σ* +*p*

Substituting Eq. (71) into Eq. (69) yields

<u>p</u> eH *p* e eHe SINR*k*= 2 h*k*I*N−* 2 h*i*h*i*h*k* *σ σ* +*p* <u>p</u> eHe *p* eHe eHe = 2 h*k*h*k−* 2 h*k*h*i*h*i*h*k,*(72) *σ σ* +*p*

where the first term satisfies he H *k*h e *k*= 1, and the term can 2 be written as he H *k*h e *i* h eH *i*h e *k*= h eH *i*h e *k*= ¯*ikρ²*. Consequently, Eq. (72) becomes

<u>p p</u>2 SINR*k*= 2 1*−* 2 ¯ *ik* *ρ.*(73) *σ σ* +*p*

Finally, defining the interference-free reference SNR as <u>p</u> *γ*≜ 2 *,*(74) *σ* and substituting Eq.(74) into Eq.(73) gives the desired correlation-dependent SINR expression

*γ* SINR*k*=*γ −* ¯*ikρ,*(75) 1 +*γ*

which explicitly separates the effect of the interference-free reference SNR from that of the normalized channel correlation between the two users.

APPENDIXB SELECTEDBENDINGRATIOS FOR THEUSER-SPECIFIC MWB BENCHMARK This appendix reports the user-specific bending-ratio sets obtained from the sequential minimax-correlation selection in Eq. (56). The selected bending ratios are nonuniformly distributed over the available range. This behavior results from the nonlinear dependence of the channel correlation on the bending ratio and from the combined effects of the UE geometry, finite metasurface and BS apertures, and UE– metasurface–BS propagation. As*K*increases, the previously selected values are retained and one additional bending ratio is introduced, yielding the nested solution sets listed in Table II.

TABLE II: Selected bending ratios for the user-specific MWB benchmark in the random-sector UE configuration. *K* *k k*=1 *K*Selected bending ratios*{β}* 2*{*1*.*00*,*3*.*00*}* 3*{*1*.*00*,*3*.*00*,*8*.*00*}* 4*{*1*.*00*,*3*.*00*,*4*.*27*,*8*.*00*}* 5*{*1*.*00*,*3*.*00*,*4*.*27*,*8*.*00*,*9*.*36*}* 6*{*1*.*00*,*1*.*73*,*3*.*00*,*4*.*27*,*8*.*00*,*9*.*36*}* 7*{*1*.*00*,*1*.*73*,*3*.*00*,*4*.*27*,*6*.*09*,*8*.*00*,*9*.*36*}* 8*{*1*.*00*,*1*.*73*,*3*.*00*,*4*.*27*,*6*.*09*,*6*.*82*,*8*.*00*,*9*.*36*}* 9*{*1*.*00*,*1*.*73*,*3*.*00*,*4*.*27*,*6*.*09*,*6*.*82*,*7*.*27*,*8*.*00*,*9*.*36*}* 10*{*1*.*00*,*1*.*73*,*3*.*00*,*4*.*27*,*4*.*64*,*6*.*09*,*6*.*82*,*7*.*27*,*8*.*00*,*9*.*36*}*

*.* APPENDIXC TRANSMISSIONCOEFFCIENTS VERSUSINCIDENTANGLE

Figure 17 presents the simulated transmission responses

under oblique incidence. At*θi*= 15 *◦* and30, most unit cells *◦*

retain phase responses close to their target states and maintain high transmission amplitudes. At*θ* = 45, larger phase devia- *◦* *◦* *i* *◦* tions appear for Cell 4 (0 ) and Cell 8 (180 ), while Cell 4 also exhibits a noticeable amplitude reduction. Nevertheless, most states remain relatively robust over the considered angular range. Since spherical-wave illumination produces spatially varying local incidence angles across the metasurface aperture, the angular stability of the unit-cell transmission responses is essential for preserving the prescribed phase profile. In the proposed design,*p*=*λ/*5, and hence the unit-cell far- 2 field distance is*d*FF*,*uc= 2*p /λ*= 0*.*08*λ*, which is much smaller than the considered UE–MS distances. Each unit cell therefore experiences an approximately locally planar wave with a position-dependent incidence angle. For a broadside source at a distance*d* TM, the maximum local incidence angle occurs <u>at an aperture corner</u> and is given by*θ* = p i*,*max tan *−*1 (*ℓ /*2)2+ (*w /*2)2*/d* TM. For*ℓ* =*w* = MS MS MS MS 10*λ*and*d* TM = 5*λ*used in this paper, this gives*θ ≈* i*,*max 54 *◦*. The local incidence angles therefore span approximately *θ* *i∈*[0 *◦* *,*54 *◦*]. Most unit cells experience moderate incidence angles, while the largest angles are confined to regions near the aperture edges and corners. Consequently, the proposed unit- cell library provides sufficiently robust transmission responses over most of the metasurface aperture, although the edge and corner cells may exhibit larger phase and amplitude deviations.

Fig. 17: Simulated transmission responses of the eight dog-bone unit cells under oblique incidence. The unit-cell architecture

is shown in Fig. 15, and the corresponding geometrical parameters are listed in Table I. The columns correspond to incidence *◦* *◦* *◦* angles of*θ* = 15 ,30, and45, respectively. The top and bottom rows show the transmission phase∠*T*and transmission *i* amplitude*|T|*, respectively.

REFERENCES

[1]T. L. Marzetta, “Noncooperative cellular wireless with unlimited num- bers of base station antennas,”*IEEE Trans. Wirel. Commun.*, vol. 9, no. 11, pp. 3590–3600, 2010. [2]E. Bjornson, C.-B. Chae, R. W. Heath Jr, T. L. Marzetta, A. Mezghani, ¨

L. Sanguinetti, F. Rusek, M. R. Castellanos, D. Jun, and O. T. Demir, ¨ “Towards 6G MIMO: Massive spatial multiplexing, dense arrays, and interplay between electromagnetics and processing,”*arXiv preprint* *arXiv:2401.02844*, 2024.
[3]H. Lu, Y. Zeng, C. You, Y. Han, J. Zhang, Z. Wang, Z. Dong,

S. Jin, C.-X. Wang, T. Jiang*et al.*, “A tutorial on near-field XL-MIMO communications toward 6G,”*IEEE Commun. Surv. Tutor.*, vol. 26, no. 4, pp. 2213–2257, 2024.
[4]M. Cui, Z. Wu, Y. Lu, X. Wei, and L. Dai, “Near-field MIMO communications for 6G: Fundamentals, challenges, potentials, and future directions,”*IEEE Commun. Mag.*, vol. 61, no. 1, pp. 40–46, 2022. [5]O. Koutsos, F. Manzillo, A. Clemente, and R. Sauleau, “Analysis, rigor- ous design and characterization of a three-layer anisotropic transmitarray at 300 GHz,”*IEEE Trans. Antennas Propag.*, vol. 70, no. 7, pp. 5437– 5446, 2022. [6]C. A. Balanis,*Antenna Theory: Analysis and Design*. John wiley & sons, 2016. [7]H. Lu and Y. Zeng, “Communicating with extremely large-scale ar- ray/surface: Unified modeling and performance analysis,”*IEEE Trans.* *Wirel. Commun.*, vol. 21, no. 6, pp. 4039–4053, 2022. [8]P. Ramezani, A. Kosasih, A. Irshad, and E. Bjornson, ¨ “Exploiting the depth and angular domains for massive near-field spatial multiplexing,” *IEEE BITS Inf. Theory Mag.*, vol. 3, no. 1, pp. 14–26, 2023. [9]H. Zhang, N. Shlezinger, F. Guidi, D. Dardari, M. F. Imani, and Y. C. Eldar, “Beam focusing for near-field multiuser MIMO communications,” *IEEE Trans. Wirel. Commun.*, vol. 21, no. 9, pp. 7476–7490, 2022. [10]Z. Wu and L. Dai, “Multiple access for near-field communications: SDMA or LDMA?”*IEEE J. Sel. Areas Commun.*, vol. 41, no. 6, pp. 1918–1935, 2023. [11]M. Cui and L. Dai, “Channel estimation for extremely large-scale MIMO: Far-field or near-field?”*IEEE Trans. Commun.*, vol. 70, no. 4, pp. 2663–2677, 2022. [12]E. Bjornson, ¨ O. T. Demir, and L. Sanguinetti, “A primer on near-field ¨ beamforming for arrays and reconfigurable intelligent surfaces,” in

*55th Asilomar Conference on Signals, Systems, and Computers*. IEEE, 2021, pp. 105–112. [13]P. Mei, Y. Cai, K. Zhao, Z. Ying, G. F. Pedersen, X. Q. Lin, and

S. Zhang, “On the study of reconfigurable intelligent surfaces in the near-field region,”*IEEE Trans. Antennas Propag.*, vol. 70, no. 10, pp. 8718–8728, 2022.
[14]A. Papazafeiropoulos, P. Kourtessis, S. Chatzinotas, D. I. Kaklamani, and I. S. Venieris, “Near-field beamforming for stacked intelligent metasurfaces-assisted MIMO networks,”*IEEE Wirel. Commun. Lett.*, vol. 13, no. 11, pp. 3035–3039, 2024. [15]V. G. Ataloglou and G. V. Eleftheriades, “A reconfigurable intelligent surface with surface-wave assisted beamforming capabilities,”*IEEE* *Trans. Antennas Propag.*, 2025. [16]C. L. Holloway, E. F. Kuester, J. A. Gordon, J. O’Hara, J. Booth, and D. R. Smith, “An overview of the theory and applications of metasurfaces: The two-dimensional equivalents of metamaterials,”*IEEE* *Antennas Propag. Mag.*, vol. 54, no. 2, pp. 10–35, 2012. [17]G. Minatti, F. Caminita, E. Martini, M. Sabbadini, and S. Maci, “Synthesis of modulated-metasurface antennas with amplitude, phase, and polarization control,”*IEEE Trans. Antennas Propag.*, vol. 64, no. 9, pp. 3907–3919, 2016. [18]M. Di Renzo, A. Zappone, M. Debbah, M.-S. Alouini, C. Yuen,

J. De Rosny, and S. Tretyakov, “Smart radio environments empowered by reconfigurable intelligent surfaces: How it works, state of research, and the road ahead,”*IEEE J. Sel. Areas Commun.*, vol. 38, no. 11, pp. 2450–2525, 2020.
[19]K. Achouri and C. Caloz,*Electromagnetic Metasurfaces: Theory and* *Applications*. John Wiley & Sons, 2021. [20]Z. Wani, M. P. Abegaonkar, and S. K. Koul, “Thin planar metasurface lens for millimeter-wave MIMO applications,”*IEEE Trans. Antennas* *Propag.*, vol. 70, no. 1, pp. 692–696, 2021. [21]K. Achouri, M. A. Salem, and C. Caloz, “General metasurface synthesis based on susceptibility tensors,”*IEEE Trans. Antennas Propag.*, vol. 63, no. 7, pp. 2977–2991, 2015. [22]C. Pfeiffer and A. Grbic, “Metamaterial Huygens’ surfaces: tailoring wave fronts with reflectionless sheets,”*Phys. Rev. Lett*, vol. 110, no. 19,

p. 197401, 2013.
[23]A. Epstein and G. V. Eleftheriades, “Huygens’ metasurfaces via the equivalence principle: design and applications,”*J. Opt. Soc. Am. B*, vol. 33, no. 2, pp. A31–A50, 2016.

[24]E. Bjornson, J. Hoydis, and L. Sanguinetti, “Massive MIMO networks: ¨ Spectral, energy, and hardware efficiency,”*Foundations and TrendsW in ˆ* *Signal Processing*, vol. 11, no. 3-4, pp. 154–655, 2017. [25]D. Tse and P. Viswanath,*Fundamentals of Wireless Communication*. Cambridge university press, 2005. [26]U. Madhow and M. L. Honig, “MMSE interference suppression for direct-sequence spread-spectrum CDMA,”*IEEE Trans. Commun.*, vol. 42, no. 12, pp. 3178–3188, 1994. [27]O. Roy and M. Vetterli, “The effective rank: A measure of effective dimensionality,” in*Proc. 15th Eur. Signal Process. Conf. (EUSIPCO),*

*2007*. IEEE, 2007, pp. 606–610.
[28]M. P. Do Carmo,*Differential Geometry of Curves and Surfaces*. Courier Dover Publications, 2016. [29]M. Monemi, S. Bahrami, M. Rasti, and M. Latva-aho, “A study on characterization of near-field sub-regions for phased-array antennas,” *IEEE Trans. Commun.*, vol. 73, no. 5, pp. 2964–2979, 2024. [30]M. Born and E. Wolf,*Principles of Optics: Electromagnetic Theory of* *Propagation, Interference and Diffraction of Light*. Elsevier, 2013.
