*Astronomy & Astrophysics*manuscript no. main©ESO 2026 <u>August 3, 2026</u>

## Fishing for Jellyfish Galaxies: Exploring ram-pressure stripping with crowd science

*,*2 *,*4,*★*

C. Bellhouse¹
###, Y. L. Jaffé³

, J. P. Crossett³, S. L. McGee⁵, Ignacio Quiroz³, C. Dulcien³, R. Smith³, B. M. 6 *,*8 Poggianti¹, B. Vulcani¹, V. Sampaio³, A. Werle¹, N. Tomicić ˆ, A. Müller⁷, N. Akerman¹, A. Ignesti¹, and A. *,*10 Khoram⁹

1 INAF- Osservatorio astronomico di Padova, Vicolo Osservatorio 5, I-35122 Padova, Italy 2 School of Physics and Astronomy, University of Nottingham, University Park, Nottingham NG7 2RD, UK 3 Departamento de Física, Universidad Técnica Federico Santa María, Avenida España 1680, Valparaíso, Chile 4 Millennium Nucleus for Galaxies (MINGAL) 5 School of Physics and Astronomy, University of Birmingham, Birmingham B15 2TT, UK 6 Department of Physics, Faculty of Science, University of Zagreb, Bijenička Cesta 32, 10000 Zagreb, Croatia 7 Ruhr University Bochum, Faculty of Physics and Astronomy, Astronomical Institute (AIRUB), Universitätsstraße 150, 44801 Bochum, Germany 8 Dipartimento di Fisica e Astronomia ‘Galileo Galilei’, Università di Padova, vicolo dell’Osservatorio 3, IT-35122 Padova, Italy 9 Dipartimento di Fisica e Astronomia, Universit‘a di Bologna, Via Gobetti 93/2, I-40129, Bologna, Italy 10 INAF, Astrophysics and Space Science Observatory Bologna, Via P. Gobetti 93/3, I-40129 Bologna, Italy

Received September 30, 20XX

**ABSTRACT**

*Aims.*We present the first results of*Fishing for Jellyfish Galaxies*, a pilot citizen-science project using Zooniverse to identify galaxies undergoing ram-pressure stripping (RPS). *Methods.*Volunteers visually inspected colour images of late-type galaxies from the Dark Energy Camera Legacy Survey. The sample consistedof49,703galaxiesselectedwithin4×*𝑅₅₀₀* ofclustersandgroups,restrictedtothosebrighterthan19thmagnitudeinthe*g*and *r*bands, and with a minimum half-light radius of 2 arc seconds, to aid classification. We detail our data processing, including debiasing classifications and optimising vote-fraction thresholds to maximise completeness and purity, calibrated against a ground-truth set of pre-labelled galaxies. *Results.*Our final catalogue contains 6739 jellyfish candidates (6621 new), 5430 merger candidates, and 29,729 undisturbed galaxies, with 3910 jellyfish exhibiting prominent tail-like morphologies. We find that the fraction of RPS candidates rises from∼10% in galaxy groups to∼20–30% in massive clusters, confirming the findings of previous studies carried out on smaller samples. For the subset of our RPS candidate sample with spectroscopic data, we measure a median cluster-centric velocity53%higher than the general cluster population, consistent with galaxies in early stages of accretion into the cluster. They are also typically late-type blue galaxies with elevated star-formation rates, in agreement with expectations. These results demonstrate that citizen scientists can reliably identify galaxies that undergo environmental processes. We provide the initial release of 37,599 visually classified galaxies as a resource for future studies of galaxy transformation in clusters.

**Key words.**Galaxies: clusters: intracluster medium – Galaxies: evolution – Galaxies: interactions

### 1. Introduction

Dense environments, such as those found in groups and clus- ters, can promote gravitational and hydrodynamical encounters whichdrasticallyalterthemorphologyandgascontentofagalaxy (Boselli & Gavazzi 2006). Since gas fuels star formation, under- standing these processes and their influence on the population of a cluster is critical to the study of galaxy evolution. The mechanisms which transform galaxies in clusters can be divided into two primary categories: gravitational effects, re- sulting from tidal encounters between galaxies (Spitzer & Baade 1951; Toomre 1977; Tinsley & Larson 1979; Merritt 1983; Mihos et al. 1993; Springel 2000) or their interactions with the cluster potential (Byrd & Valtonen 1990; Valluri 1993), and hy- drodynamical processes, resulting from the interaction between galaxies and the intracluster medium (ICM).

*★* Corresponding author: yara.jaffe@usm.cl

One of the most efficient mechanisms of gas removal is the process of ram-pressure stripping (RPS; Gunn & Gott 1972). When a galaxy infalls into a cluster with sufficient velocity, the cluster ICM imparts a drag force that acts upon the interstellar medium within the galaxy. The resulting interaction can effec- tively remove the gas component from the galaxy, forming a trail ofmaterialbehindit,withoutdirectlydisruptingtheexistingstel- lar component, which is too dense to be affected. The observable effects of RPS include leading-edge compression (Vollmer et al.

2001), the presence of a tail or trailing material, the conden- sation of star-forming clumps in the tail (Kenney et al. 2004; Fossati et al. 2016; Giunchi et al. 2023a,b, 2025) accompanied by a temporary boost in star-formation (Poggianti et al. 2016; Vulcani et al.2018,2020a,2023;Tomičić et al.2018),eventually leading to quenching if the gas is completely removed. In such cases, galaxies typically transition into early-type morphologies (Sampaio et al. 2022, 2024). In addition, several cases of galax-
Article number, page 1

# arXiv:2607.28739v1 [astro-ph.GA] 30 Jul 2026

*A&A proofs:*

iesbeing‘unwound’byRPShavebeenobserved(Bellhouse et al. 2021; Vulcani et al. 2022; Matijević et al. 2026). The most extreme cases of RPS result in so-called ‘jelly- fish’ galaxies, with characteristic tails of stripped material. Such galaxies are valuable laboratories for testing the processes that enhance and quench star formation in galaxies (Poggianti et al. 2019; Vulcani et al. 2022) and, in rare cases, may trigger ac- tive galactic nucleus (AGN) formation (Poggianti et al. 2017a; Peluso et al.2022).Untanglingthecomplexrelationshipbetween hydrodynamical influences, morphology, and environment re- quires a large sample of galaxies. This is especially important when measuring the effects of environment in subsamples of galaxies with specific properties, which may constitute only a small fraction of the full sample. Statistical studies of RPS across cluster properties such as halo mass and dynamical state have highlighted the need for larger, homogeneous samples of stripped galaxies. Ram-pressure stripping has been shown to be enhanced by cluster merg- ers and shocks in simulations (Roediger et al. 2014) and indi- vidual clusters (Stroe et al. 2015, 2020; Bellhouse et al. 2022). Lourenço et al.(2023)extendedthisanalysisacrossalargersam- ple of clusters, finding an increase in instances of RPS with in- creased cluster disturbance; however, they emphasise that larger homogeneoussamplesofRPSgalaxiesarenecessarytoprovidea statistically significant result. Similarly, Salinas et al. (2024) car- ried out statistical studies of the tail directions in RPS galaxies and highlighted the importance of increased sample sizes, with a particular emphasis on homogeneous samples of spectroscopi- cally confirmed cluster members. A major challenge in the study of RPS galaxies is iden- tification. Past samples of RPS galaxies have been iden- tified in various ways, from visual inspection of imag- ing data in optical (Poggianti et al. 2016; McPartland et al. 2016; Roberts & Parker 2020; Vulcani et al. 2022; Kolcu et al.

2022) and UV (George et al. 2024) wavelengths, H*𝛼*imaging (Yagi et al.2010),HIandradiocontinuumsurveys(Roberts et al. 2022; Ignesti et al. 2023), or X-ray data (Sun et al. 2006). A discussion of the different selection criteria and their inher- ent drawbacks and advantages can be found in Poggianti et al. (2025). The disturbance signatures are generally morphological andwidelyvariedintheirnature,makingautomatedclassification a challenge, especially given the relatively small current sample. One practical solution to this lies in citizen science projects. The success of Galaxy Zoo (Lintott et al. 2008; Walmsley et al. 2022;Bamford et al.2009;Willett et al.2013)anditsZooniverse toolkit has given rise to dedicated citizen science projects. One such example is Zinger et al. (2024), which showed images of simulated galaxies from IllustrisTNG (Vogelsberger et al. 2014; Genel et al. 2014; Sijacki et al. 2015) to thousands of volun- teers, whowere askedto classifywhether theirvisual appearance was consistent with galaxies experiencing RPS. Until now, such an analysis has not been carried out on observational data. By combining the responses of several volunteers for each galaxy, we can separate different galaxy types based on vote fractions. Crossett et al. (2025) showed that even when the volunteers are not specifically looking for signs of RPS, their combined re- sponses on questions about ‘oddities’ can be used to identify the presence of RPS signatures in images of galaxies. Building on the success of these volunteer-powered projects and with the goal of producing a large, homogeneous sample of visually classified stripping candidates (SCs) for future statisti- cal studies of RPS, we designed and executed a dedicated citi- zen science project based on the Zooniverse platform. In Sect.2 we detail the process of selecting target clusters across a range Article number, page 2
manuscript no. main

of masses and the selection of satellite galaxies therein, outlin- ing the morphology, brightness, and angular size constraints on the subject galaxies. Section3 describes the classification pro- cess, including details of the Zooniverse workflow, definitions of the vote fractions, as well as the debiasing and combination of classifications to produce the final sample selection criteria. Section4.1 describes the catalogue, detailing the included pa- rameters and showing examples of jellyfish candidate galaxies found by the identification process. To test the viability of the visually classified sample of galaxies as genuine candidates for stripping as well as investigating trends in the incidence of RPS across cluster mass, we carried out an initial analysis of the re- sults, described in Sect.4. We investigate the abundance of RPS candidates as a function of environment and compare the mor- phologies and colours of the different samples and the star for- mationrates(SFRs)ofasubsetofthesamplecross-matchedwith SDSS.Finally,inSect.5,wesummarisetheresultsanddrawcon- clusions. Throughout this paper we assume a standard Lambda cold dark matter (ΛCDM) flat cosmology withΩm=0*.*3and *𝐻₀* =70 km s −1 Mpc −1.

### 2. The sample

*2.1. Catalogues and images* We used images from the Dark Energy Camera Legacy Survey (DECaLS: Dey et al. 2019), the same survey data utilised by the Galaxy Zoo: DESI/DECaLS project (Walmsley et al. 2022). The DECaLS survey uses the Dark Energy camera (DECam: Flaugher et al. 2015) on the 4m Blanco telescope at the Cerro TololoInter-AmericanObservatory.DECamhasa0.32deg² field of view (FoV) with a plate scale of 0.262 arc seconds per pixel. The median point spread function has a full width at half maxi- mum of 1."29, 1."18, and 1."11 in the g, r, and z bands, respec- tively. The images have greater depth and higher resolution than the Sloan Digital Sky Survey (SDSS, York et al. 2000) data used in the original iteration of Galaxy Zoo (Lintott et al. 2008), making them more suitable for identifying low-surface-brightness fea- tures in distant galaxies, as we aim to do with this project. For an initial release of 36 clusters for classification by the public, we utilised data from DECaLS DR9. We later added 43 clusters and additional coverage for three of the original clusters once DECaLS DR10 was available. We selected target galaxies from the DECaLS Tractor catalogue, using the Astro Data Lab ADQL query interface to impose initial selection criteria based on the Tractor morphologies, as described in Sect.2.3.
*2.2. Target clusters* We selected 79 clusters across a redshift range of0*.*0031*< 𝑧 <*
0*.*0562, and X-ray mass range13*.*3*<*log₁₀(*𝑀₂₀₀*/*𝑀*⊙)*<*15*.*2. to probe galaxy morphologies in a range of environments. The clustersweredrawnfromtheX-rayselectedcataloguesofMCXC (Piffaretti et al. 2011) and CODEX (Finoguenov et al. 2020). We specifically included several clusters which overlap with the X-ray selected WINGS (Fasano et al. 2006) and OmegaW- INGS (Gullieuszik et al. 2015) catalogues, since these surveys were inspected previously by Poggianti et al. (2016) to construct the GASP sample (Poggianti et al. 2017b, 2025). The GASP sample includes a MUSE large programme of confirmed ram- pressure stripped galaxies, with rich IFU data confirming the presence of offset ionised gas. These clusters therefore provide an additional labelled dataset for validation and, in particular, an

C. Bellhouse et al.: Fishing for Jellyfish Galaxies: Exploring ram-pressure stripping with crowd science
Table 1: Host clusters included in the DECaLS data release 9 Table 2: Host clusters included in the DECaLS data release 10

sample. sample.

<u>Cluster RedshiftLog₁₀(M₂₀₀)NgalaxiesCluster RedshiftLog₁₀(M₂₀₀)Ngalaxies</u> Abell 2052 0.035 14.72 Abell 3562 0.049 14.71

|Abell 2052|0.035|14.72|743|Abell 3562|0.049|14.71|460|
|---|---|---|---|---|---|---|---|
|Abell 957*|0.044|14.36|226|Abell S727|0.050|14.46|108|
|Abell 3301*|0.054|14.40|177|Abell 3581|0.023|14.37|616|
|RXJ0058.9+2657|0.045|14.23|141|Abell S753|0.013|13.89|682|
|Abell 3667*|0.056|15.01|458|Abell 160|0.044|14.18|229|
|Abell 2877*|0.024|14.16|637|Abell 1644*|0.047|14.80|403|
|Abell 3341*|0.038|14.34|270|Abell 780*|0.054|15.19|243|
|RXJ1740.5+3539|0.043|14.27|202|CAN 40|0.035|14.09|223|
|ZwCl8338|0.050|14.42|162|Abell 3380|0.055|14.34|110|
|Abell 2151a|0.037|14.41|404|Abell 194*|0.018|13.86|528|
|Abell 2147|0.035|14.73|896|Abell 2589|0.042|14.55|334|
|MKW 8|0.026|14.22|576|Abell 2806|0.028|13.91|275|
|Abell 2572a|0.042|14.53|282|Abell 2572a0.042||14.53|16|
|Abell 576|0.038|14.56|549|Abell 1736|0.046|14.69|496|
|Abell 2199|0.030|14.84|1106|Abell 978|0.054|14.43|162|
|Abell 76|0.040|14.43|248|Abell 3736|0.049|13.65|162|
|Abell S560*|0.037|13.98|108|Abell 3570|0.038|14.24|214|
|Abell 496*|0.033|14.82|436|Abell 2665|0.056|14.56|171|
|Abell 2634*|0.031|14.37|708|Abell 1142|0.035|14.11|236|
|Abell 85*|0.056|15.20|418|Abell 2657|0.040|14.58|313|
|Abell 2063|0.035|14.63|576|HCG 62|0.015|13.92|739|
|CGCG170-018|0.050|14.59|83|Abell 6710.050||14.36|11|
|MKW4|0.020|14.20|728|Abell S721|0.050|14.48|194|
|Abell S463|0.040|14.37|252|Abell S617|0.034|14.04|219|
|Abell 3391|0.051||265|NGC1550|0.013|14.21|521|
|NGC1407|0.006|13.34|1204|Abell S547|0.051|14.26|98|
|Abell 548W*|0.042|14.07|234|AM 0711|0.032|13.96|98|
|Pegasus II|0.042|14.38|270|Abell 3565*|0.012|14.33|733|
|Abell 3376*|0.047|14.58|230|Abell 536|0.040|14.96|132|
|Abell S861|0.051|14.47|370|Abell 3571*|0.039|15.00|570|
|Abell 671|0.050|14.36|186|Abell 147*|0.044|14.12|154|
|UGC 04991|0.032||139|NGC1650|0.036|14.22|281|
|Abell S41|0.049|14.46|218|Abell 3990|0.029|14.93|139|
|Abell 548E*|0.042|14.56|326|Abell S141|0.019|13.83|223|
|NGC 4636|0.003|13.76|4833|Abell 3574E*|0.016|14.50|642|
|Abell 1367|0.021|14.53|1633|Abell S851|0.010|13.91|624|
|||||Abell 3526|0.011|14.51|1566|
|Notes.Clusters marked with an asterisk are also in the CHANCES cat-||||Abell 4038|0.030|14.61|512|
|alogue, which will provide additional spectroscopic coverage for future analysis.TheN|columndescribesthenumberofgalaxiesincluded|||IC 1365|0.049|13.90|178|
|in the subject catalogue, selected from the4×R₅₀₀ region surrounding||||Abell 119*|0.044|14.71|376|
|the cluster.||||IC4992|0.019|13.95|333|
|||||Abell S805|0.015|13.87|569|
|||||Abell S410.049||14.46|17|
|||||Abell 2593|0.043|14.44|315|
|overlap with the GASP sample of ram-pressure stripped galaxies||||Hydra (A1060)*|0.013|14.40|1786|
|confirmed with integral-field spectroscopy. Additionally, we selected several clusters that overlap with CHANCES (the Chilean Cluster Galaxy Evolution Survey; Sifón et al. 2025), which will provide additional spectroscopic||||NGC1713 Notes.Clusters marked in bold indicate additional coverage added to clusters already included in the DR9 release. The columns and asterisks are as described in the Table1 caption.|0.015|13.69|294|

galaxies

coverage from the 4MOST Spectroscopic Survey Facility on the VISTA observatory. Our full sample is representative of clusters across the halo *2.3. Sample selection* mass range but undersamples lower redshift clusters (z≤0*.*025, A crucial factor for citizen science projects is user retention, i.e. seeFig. A.1).Weusedthefullsampleforthesubsequentanalysis howmuchtimeagivenuseriswillingtocontributetocompleting but show in Sect.4 that using a representative subsample has no classifications. A sense of meaningful contribution to scientific effect on our conclusions. research has been shown to be the primary motivating factor for The final sample of DECaLS DR9 and DR10 clusters are userstogivemoreoftheirtimeandcompletemoreclassifications shown in Tables1 and 2 respectively. Clusters overlapping with (Raddick et al. 2013). When selecting galaxies for the project, the CHANCES sample are marked with asterisks. we therefore aimed to maximise the number of potential RPS

Article number, page 3

Fig. 1: Examples of the icons used to denote various morpholog-

ical features of the galaxies and provide a visual reference for the workflow options.*Top row*: Disturbed, not merging.*Middle row*: Undisturbed.*Bottom row*: Disturbed, merging.

candidates in the sample to ensure that a sufficient number of ‘interesting’ candidates would appear during the classification process, thereby maintaining a user’s interest. We selected galaxies within a projected distance of4×*𝑅₅₀₀* (corresponding to2*.*87×*𝑅₂₀₀* on average) of their host cluster X-ray centres, since the majority of RPS interactions are ex- pected to occur at low cluster-centric radii (Jaffé et al. 2018). The choice of*𝑅₅₀₀* in the definition was motivated by the MCXC catalogue which defined only the*𝑅₅₀₀* radius of the clusters. At a later date, after the initial sample was live on the Zooni- verse project, additional cluster parameters were made available from the CODEX catalogue (Finoguenov et al. 2020) including the*𝑅₂₀₀* radius. We therefore maintained the*𝑅₅₀₀* constraint for consistency in the catalogue selection but used*𝑅₂₀₀* when defin- ing cluster membership in the subsamples. Of the full sample of 42684 objects, 9236(∼20%)have spectroscopic information, and we define a subsample of 2618 spectroscopically confirmed clustermembersusingthespectroscopicsample,selectinggalax- ies with*𝑅 <*2×*𝑅₂₀₀* and|Δ*𝑉*LOS|*<*4*𝜎*. We constrained the sample to galaxies which were classified by the DECaLS source extraction as‘EXP’(exponential disk),‘REX’(round exponen- tial disk), and‘SER’(modelled by a Sérsic profile). For galaxies classifiedas‘SER’,wefurtherconstrainedthesampletoaSérsic index of*𝑛 <*2*.*5(including galaxies up to a Sérsic index of 5 in a small number of cluster samples, for future comparison). Ram- pressure interactions have occasionally been reported in early- type galaxies (Sheen et al. 2017); however, the most common and most striking examples of ram-pressure disrupted galaxies are generally gas-rich, late-type galaxies (Poggianti et al. 2016), making them a prime target for maximising the expected fraction of RPS galaxies in the sample. WecleanedthesamplebyimposingconstraintsusingtheDE- CaLS tractor catalogue bit-mask flags to remove sources which contain pixels flagged as saturated, hot pixels, bad columns or contaminated by cosmic rays. With the goal of cleaning the sam- ple of galaxies that are too small or faint to reliably classify, we imposed a magnitude limit of 19 in the*r*and*g*bands and a minimum half-light radius of 2 arc seconds. We downloaded red-green-blue (RGB) colour cutouts of the selected galaxies from the legacy survey image data using the default outputs, which show the low-surface brightness features of the jellyfish galaxies well. For each galaxy, we auto-scaled the cutoutsusingthehalf-lightradiustoensurethateachgalaxyfilled the majority of the image. In addition, we downloaded a cutout witha2*.*5×widerFoVtoshowmoreofthegalaxy’ssurroundings to better show extended tails and reveal any neighbouring or interacting companions that aren’t visible in the narrow FoV cutout.

galaxy, and minimal time is spent classifying galaxies we are not specifically searching for. The workflow was designed to be as simple and descriptive as possible, so that users with little knowledge of the underly- ing science and little experience viewing images of disturbed galaxies would be able to classify galaxies based solely with ref- erence to their appearance. To that end, visual icons describing different morphologies were included for most of the answers, showing different examples of features for users to classify based on physical features and comparisons. Several examples of the icons used are shown in Fig. 1, with the full set of icons shown in the workflow diagram (see Fig C.1) in the appendix. The initial steps of the workflow were thus chosen to classify galaxies as either disturbed or undisturbed, and as merging or not merging,with‘undisturbed’referringtogalaxieswithnosignsof morphological disturbance, regardless of origin. Classifications of ‘undisturbed’ or ‘merging’ both end the workflow. If a galaxy was flagged as disturbed, but not merging, the classification pro- cesscontinued,focusingonthemorphologyofthegalaxyandthe nature of the disturbance. The subsequent step in the workflow assessed the visibility of the spiral arms and, if present, whether they exhibit unwinding properties. In the subsequent step, we flagged the presence of a tail or extraplanar material. If a galaxy was classified with a tail, the final step in the workflow involved describing the tail’s origin as either from the centre, elsewhere in the galaxy, or from the whole disk. The user was then prompted to draw the path of the tail using a line drawing annotation tool.

*3.2. Beta testing-A2626* To validate and test the effectiveness of the classification process as well as verify the usability and clarity of the workflow for non-experts, we prepared a beta test, using a sample of galaxies using the same selection parameters as the main sample for the region within4×R₅₀₀ of A2626. We also prepared tutorials and a field guide with information about galaxy clusters, the process of RPS, and merging interactions to give the volunteers context surrounding the galaxies and classification system. For the beta test, we trialled different retirement limits (i.e. the number of
### 3. Classification process

*3.1. Workflow* The workflow of tasks, which are comprised of questions about physical characteristics of the subject, is shown in Fig C.1 of the appendix. The workflow was designed with the goal of getting as much information about the visual characteristics relevant to strippingwhilstfilteringoutmergersandundisturbedgalaxies,in asfewstepsaspossible.Themotivationforkeepingtheworkflow asshortaspossibleistoensurethatavolunteerisabletocomplete as many classifications as possible within a given time frame. Moreover, mergers and undisturbed galaxies should be identified as soon as possible so that the classifier can move onto the next Article number, page 4

C. Bellhouse et al.: Fishing for Jellyfish Galaxies: Exploring ram-pressure stripping with crowd science
*.*

*.*

*.*

0*.*4
Number of users 10 1

0*.*2
100

0*.*0
0 5000 10000 15000 20000 Number of classifications by user

Fig. 2: Green-shaded histogram showing the distribution of users

according to the total number of classifications contributed. The black line indicates, for each bin, the cumulative total of classifi- cations contributed by users in each bin.

classifications a subject must receive before it is no longer shown to classifiers) of 5, 10, and 20. A higher retirement limit provides more reliable classifications and dilutes the impact of erroneous classifications, whilst a lower limit allows a larger overall sample to be classified. Duringthebetatestingphase,wefamiliarised400non-expert volunteers classifying a sample of 290 galaxies with the Zooni-

|1|||
|---|---|---|
|00. 0|0. 4|0. 6|
||F||

verse platform. In total, we received 5829 classifications. To pro- cess the beta test results, we defined the sample using simplified classificationcriteria,assigningeachobjectthelabelthatreceived more than 50% of the votes. Inparticular,wedefined‘disturbed’,‘undisturbed’,and‘prob- lem’ galaxies (representing cases hard to classify). The ‘dis- turbed’ category was further subdivided into ‘merger’ and ‘tail’ galaxies, with the vote fractions defined as

“Disturbed” -*𝐹*dist*.*=Vdist*.*/ (Vdist*.*+Vundist*.*), “Merger” -*𝐹*merg*.*=Vmerg*.*/Vdist*.*, “Tail” -*𝐹*tail=Vtail/Vdist*.*, “Undisturbed” -*𝐹*undist*.*=Vundist*.*/ (Vdist*.*+Vundist*.*), “Problem” -*𝐹*prob*.* prob*.* total

|=V|/V|,|||||
|---|---|---|---|---|---|---|
|prob.|prob.|total||Normalised Density|||
|||||1|||
|||||0|||
|||||0. 0|0. 4|0. 6|
||||||F||

whereVxis the number of votes for a given feature x, and Vtotalis the total number of classifications a galaxy has received. These definitions were used for the vote fractions given in the catalogue and described in the subsequent sections. Based on these criteria, we defined 230 undisturbed objects, 49 disturbed and not merging, seven disturbed and merging, and four galaxies flagged as a ‘problem’. Based on visual inspection of the classified objects by ex- perts, we determined that the public reliably identified disturbed morphologies but struggled to differentiate between merging and non-merging cases of disturbance, i.e. between gravitational and hydrodynamical (RPS) interactions, which are in fact hard to separate in many cases based on broadband imaging alone. To mitigate this difficulty, we updated the tutorial and field guide to include a wide variety of merging and stripped galaxies as a reference for the classifiers to compare. Tocompareretirementlimits,wecalculatedtheclassification of each subject after the first five votes, the first ten votes and the full set of 20 votes. We found that the majority of classifications did not change between each limit, with 10% of classifications differing between five and 20 votes, and 4% of classifications differing between ten and 20 votes. We therefore selected ten classificationsasanoptimalretirementlimitforthemainproject.

*.* All Zoo Known JF

*.* Known JF (High JClass)

1*.*5
(cumulative)

1*.*0 Normalised Density
0*.*5
0*.*
00*.*0 0*.*2 0*.*4 0*.*6 0*.*8 1*.*0
Fdist*.*

2 Normalised Density 1

0*.*2 0*.*8 1*.*0
tail

2 Normalised Density

0*.*2 0*.*8 1*.*0
merg*.*

Fig. 3: Histograms of the debiased vote fractions of galaxies

matched with known ram-pressure stripped galaxies drawn from theliterature.Thegrey-shadedhistogramshowsthefullzoosam- ple.TheblacklineshowsallmatchestoknownRPSgalaxies(ex- cluding those without optical tails) from the literature compiled in Crossett et al. (2025). The dashed grey line shows the matches to the subset of known RPS galaxies classified asJClass≥3, i.e. those with moderate to strong optical signs of stripping.

Assuming a fixed number of total classifications, this would dou- ble the sample of retired galaxies compared to 20 classifications, at a loss of only 4% in accuracy.

*3.3. Results and vote fractions* Approximately 18 months after launching the project on the Zooniverse platform, sufficient classifications were received to
Article number, page 5

Fraction of classifications

retire the full sample. In total, 5286 users (or unique user ses- sions for logged-out users) classified 49703 unique objects, with an average of 97.8 classifications per user. In total, 517,152 clas- sifications were contributed, giving an average of 10.4 classifi- cations per unique object. Figure B.1 shows the distribution of classifications per image, while Fig.2 shows the number of clas- sifications completed by users as a red histogram. We found that 2197 users, approximately half of the total, classified under ten galaxies. On the other hand 667 users classified more than 100 galaxies. In the same figure, the black stepped histogram shows the total votes contributed by these users, revealing that whilst most users contributed fewer than 100 classifications, the small number of experienced users collectively contributed a signifi- cant fraction of the total. For the purpose of classification, we combined the votes for each subject, as explained in Sect. 3.2, by defining vote fractions for each question in the workflow. We examined galaxies in Abell 1644 to reevaluate the ‘prob- lem’ fraction,*𝐹*prob*.*, defined as the proportion of citizens who considered the statement, ’The galaxy is not clear or too small / there is a problem with the image’, true. Whilst we removed any sources flagged by the DECaLS bit masks, a small percentage of images still contained bright stars, missing bands, or other is- sues that could potentially hinder classification. The inclusion of the ‘problem’ classification allowed volunteers to flag galaxies, which suffered sufficiently poor image quality to preclude classi- fication. Notably, however, we find no clear correlation between *𝐹*prob*.*and image quality. Contrary to expectations, a high*𝐹*prob*.* doesnotnecessarilyindicateanunclassifiablegalaxy.Infact,low *𝐹*prob*.*often correspond to poor image quality, while high*𝐹*prob*.* may appear in galaxies that are clearly classifiable. This sug- gests that citizens use the ‘problem’ label when uncertain about distinguishing between disturbed and undisturbed morphologies, rather than based solely on image quality. We speculate that the wording of the question in the workflow could have played a role in the misuse of the ‘problem’ option, even though there were clear examples in the field guide. Since the sample was cleaned for images with saturation, cosmic rays, and bad pixels, galax- ies – which are genuinely unclassifiable due to issues with the images – are therefore rare. In the rest of the analysis, we used a relaxed threshold, only flagging a galaxy as a ‘problem’ only when*>*80%of users flag it as such.

*3.4. Classification criteria* As a ground-truth for calibrating the selection of RPS candi- dates, a group of experts (co-authors of this paper) classified all 403galaxiesintheAbell1644clustersampleasmergers,jellyfish galaxies,andundisturbedgalaxies.Wescoredtheperformanceof the public classifications against the expert classifications using purity (P) and completeness (C). Purity is defined as the fraction of citizen-selected candidates that agree with the expert sam- ple (Eq. 1), and completeness is the fraction of expert-selected candidates recovered by the citizen sample (Eq. 2): ◦ <u>𝑁</u> <u>JF matched</u> P= ◦
*,*(1) *𝑁* JF citizens

◦ <u>𝑁</u> <u>JF matched</u> C= ◦ *,*(2) *𝑁* JF experts

where*𝑁* JF citizens ◦ ,*𝑁* JF experts ◦, and*𝑁* JF matched ◦ are the number of galaxies classified as jellyfish by the citizen science tester, expert

Article number, page 6

classifiers, and both groups. A completeness of 100% means all expert-selected candidates are included, while 100% purity indicates all non-candidates are excluded. Wethenexploredawiderangeofthresholdsonthedisturbed, non-merger,andtailvotefractionsusingaMonteCarloapproach. The optimal criteria for defining RPS galaxy candidates are

### 𝐹dist.≥0.39 & 𝐹merg.≤0.23∥𝐹tail≥0.37,(3)

which yield a calibrated selection with purity*𝑃*=0*.*63and completeness*𝐶*=0*.*57. We defined galaxies meeting these cri- teriaasSCs.Thefullperformancelandscapeinthe3Dparameter space is shown in Fig., D.1 of the appendix. Whilst the purity level of*𝑃*=0*.*63indicates that this sample is subject to con- tamination, we tested a stricter threshold of*𝐹*dist*.*>0.5 and find no significant deviation from the results presented in the follow- ing section. Applying these thresholds to the Abell 1644 sample, we selected galaxies with morphologies consistent with jelly- fish features, confirming that the chosen criteria provide a robust compromise between minimising contamination and recovering a large sample of ram-pressure stripped systems. We defined undisturbed galaxies as those with*𝐹*dist*.*< 0.1, referred hereafter as the reference sample (RS). We also included a sample of merging galaxies, defined as

### 𝐹dist.≥0.39 &𝐹merg.≥0.23(4)

to which we refer hereafter as merging candidates (MCs). Fi- nally,withinthedefinitionofjellyfishcandidates,wealsodefined a subsample exhibiting tail features as

### 𝐹dist.≥0.39 &𝐹merg.≤0.23 &𝐹tail≥0.37.(5)

For the rest of the paper, we refer to these galaxies as SCs with tails (SC+T) and use this sample to illustrate the trends in stronger cases of stripping. This overlaps with the SC label but excludes cases of jellyfish-like disturbance where a significant tail is not present.

Figure 6 shows the thresholds for each classification criterion

overlaid on the the corresponding distributions of vote fractions for the disturbed, merging, and tail labels across the sample.

*3.5. Combining and debiasing responses* An important step in producing a robust classification system is debiasing user votes. Debiasing the classifications homogenises the results across the pool of volunteers by prioritising patterns of votes consistent with the majority and minimises contamina- tion by spurious voting patterns, well-intentioned or otherwise. Therearemultipletechniquesfordebiasinguserscores,suchasa weighting system that downweights the votes of users who clas- sified*< 𝑁*objects (i.e. less experienced users) or systems based on each user’s concordance, i.e. the likelihood of a given user to agree with the majority. Their voting behaviour was compared blindly, i.e. without comparing individual user votes to labelled data or known RPS galaxies. We tested a combination of these systems to determine the optimal method for cleaning the vote distributions and minimis- ing the impact of spurious or random votes. First, to ‘score’ the classifications as predictors of the majority consensus, we used the fraction of user classifications in which the parameter matched the final classification. This was done separately for the

C. Bellhouse et al.: Fishing for Jellyfish Galaxies: Exploring ram-pressure stripping with crowd science
Fig. 4: Selected examples of galaxies classified as SC based on the criteria described in the text. Top: Galaxies classified as having

no tail-like feature. Bottom: Galaxies flagged as SC+T.

1*.*0
3

0*.*8 10
0*.*6
102

(unweighted)

*.*0*.*4
N dist F 101

0*.*2
0*.*0 100 12 13 14 15 16 17 18 19
*g* [mag]

Fig. 5: Distribution of*𝐹*dist*.*vs g-band magnitude, for the full

sample.Thepinklineshowsthemean*𝐹*dist*.*,binnedbymagnitude, whilst the shaded region indicates the standard deviation of*𝐹*dist*.* within each bin. The grey-shaded hexagon shows the number of galaxies binned by magnitude and*𝐹*dist*.*. A slight trend is visible with a smaller disturbed fraction at fainter magnitudes; however, the trend is within the overall scatter of the distribution of classifications in each magnitude bin.

following classifications: disturbed versus undisturbed, tail ver- sus no tail, merging versus non-merging, and ‘problem’ cases. Scores were allocated only when the final classification received more than two-thirds of the vote fraction (or 80% for ‘problem’ classifications), to avoid downweighting users in cases where the finalclassificationwasambiguous.Weexploredthisconcordance metricagainstthenumberofclassificationsauserhadcompleted, noting a minimum of ten classifications as the point at which a user typically had sufficient experience classifying galaxies and became a good predictor of the final outcome in at least 70% of classifications. In addition to a minimum threshold on the number of clas- sifications, we investigated the concordance metric itself as a

criterion for weighting user’s votes. We trialled downweighting users with a high fraction of ‘disagreements’, i.e. those who voted against other classifiers in more thanNthreshclassifications. Nthreshis a tuneable parameter describing the maximum fraction of disagreements a user can have before being downweighted. This method of debiasing should, in principle, reduce the effect ofspuriousclassifiers,suchasuserswhomisinterpretneighbour- galaxiesing galaxies as stripped material. In previous galaxy zoo studies (e.g. Walmsley et al. 2022) debiasing was carried out using a brightness-limited sample, since faint objects are challenging to classify and debiasing them is unreliable. We investigated possible trends in the classifica- tions:Vdist*.*/ (Vdist*.*+Vundist*.*) against the g-band magnitude for the galaxies within our sample. When users struggled to identify disturbance in fainter galaxies, we expected a decreasing trend with magnitude. The results are shown in Fig.5. The figure indi- cates a slight trend, as expected, but this trend is well within the classification scatter in each magnitude bin. Since our sample is limited to a g-band magnitude of 19, it is unlikely that the objects are faint enough to cause issues with classifications; therefore, we did not apply an additional magnitude cut for the debiasing process. To test the effectiveness of the two debiasing methods, we compared the debiased and non-debiased user classifications on the pre-classified sample of Abell 1644 to measure the effect of debiasing on the completeness and purity of the user classified sample.

Wefindthatdebiasingthevotesbydownweightinguserswho classifiedfewerthantenobjectsby50%increasedboththepurity and completeness by 0.03 in cases where the vote thresholds were not optimised, i.e. the purity and completeness were lower; however, when the vote thresholds were tuned to maximise the completeness and purity, the difference is negligible.

On the other hand, debiasing the votes by downweighting users with a higher disagreement fraction yields slightly lower purity and completeness. The observed reduction in purity and completeness likely result from the difficulty associated with identifyingram-pressurestrippedgalaxies.Usersmoreproficient atidentifyingtrueram-pressure-strippedgalaxies(particularlyin less obvious cases of RPS) are within the minority of the user-

Article number, page 7

Disturbed (N=49703)

Merger (N=12964)

Tail (N=1335)

0*.*0 0*.*2 0*.*4 0*.*6 0*.*8 1*.*0
Weighted vote fraction

Fig. 6: Weighted vote fractions for ‘disturbed’, ‘merging’, and

‘tail’ labels, as defined in Sect.3.5. The vertical dashed lines indicate our chosen criteria used to select galaxies within a spe- cific sample. Middle: Galaxies defined as disturbed. Bottom: Significantly disturbed galaxies with*𝐹*dist*.*> 0.8. The disturbed vote fraction shows a slight bimodality, which suggests that the classification step successfully distinguishes distinct populations within the sample. The merger vote fraction shows a peak at the lower end, suggesting a clear population of disturbed – but not merging – galaxies. Another smaller peak is present at the upper end, suggesting that the volunteers are in unilateral agreement in the clearest cases of merging.

base and are therefore more likely to be downweighted according to their disagreement fraction. Based on these findings, we opted to use debiasing only to downweight users who had carried out fewer than ten classifica- tions,ratherthanbasingitonthedisagreementfraction.Although the gain from debiasing is negligible with the tuned vote thresh- olds,thedebiasedscoresmaybemoreusefulingeneralisedcases, where different criteria may be applied to produce purer or more complete samples, as required. We combined the debiased results using the same fractions defined in Sect.3.3, using the weighted rather than unweighted votes.

*3.6. Comparison with jellyfish galaxies from the literature* To assess the effectiveness of the classifiers in recognising gen- uine cases of RPS, we spatially cross-matched the sample, based on optical position, with examples of ram-pressure stripped galaxies in the literature, i.e. those classified by experts in previous studies compiled from the catalogue in Crossett et al. (2025). The images used in the literature classifications originate from different instruments, and the visibility of individual strip- ping signatures may vary; nevertheless, the general correlations againsttheliteratureclassificationsisanindicatoroftheeffective- ness of the classification process. Figure 3 shows histograms of Article number, page 8
the debiased vote fractions of the ‘disturbed’, ‘tail’, and ‘merger’ labels for the full sample of known RPS galaxies from the liter- ature (excluding those exhibiting only radio or X-Ray tails) and known RPS galaxies categorised by Crossett et al. (2025) with aJClass≥3(i.e. with moderate to strong visual signs of strip- ping (Poggianti et al. 2016)). The top panel shows a substantial difference in the distribution of the vote fraction between the full sample and the high-JClass matches, with the median*𝐹*dist*.*ap- proximately1.5timeshigherfortheknownjellyfishgalaxiesthan forthefullsample.Thisclearlyindicatesthattheusersareableto distinguish cases of disturbance due to RPS. Moreover the high- JClass matches are skewed towards even higher vote fractions for disturbance, which confirms that the vote fraction correlates with the level of visual disturbance. The middle panel shows that the jellyfish galaxies from the literature receive higher vote fractions for tail-like features, with high-JClass jellyfish galaxies skewed towards higher vote fractions. However, the difference is less pronounced than in the case of ‘disturbance’ votes. The non-negligible population of literature jellyfish candidates with *𝐹𝑡 𝑎𝑖𝑙*∼0likely corresponds to galaxies with tails visible in deeper data, which are not as visible in the Legacy Survey im- ages. The lower panel of Fig. 3 shows that, whilst the literature jellyfish galaxies are more frequently misidentified as merging galaxies than the full zoo sample, the overall vote fractions for merging are generally low. This suggests that users are not con- fusing RPS cases with merging cases. This is consistent with expert classifications. Poggianti et al. (2025) show that contam- ination by merging galaxies is very low (∼10%) in the visually identified sample of RPS candidates identified by Poggianti et al. (2016) in clusters, whilst Vulcani et al. (2021) show that con- tamination by non-RPS mechanisms increases to (∼70%) in the field. Collectively, these plots reveal that true jellyfish galax- ies confirmed in the literature receive more votes for disturbed morphologies, indicating that the public are successfully able to distinguish genuine visual signs of stripping.

### 4. Results

In Sect. 4.1 we present the catalogue of RPS candidates gener- ated by this project. In the sections that follow, we discuss using this catalogue to test the effectiveness of the public classification method in selecting galaxies undergoing physical interactions. We examine the expected properties of the SC, SC+T, and MC samples, including their locations within clusters, morphologies, colours, and SFRs. The classifiers were provided no information on the physical parameters. Correlations with phase-space posi- tion and star-formation rate, which are stronger in the classified SC and SC+T samples than in the undisturbed sample, can there- fore be interpreted as confirmation that the visually classified samples experience hydrodynamical interactions. To incorporate stellarmassesandstar-formationratesintoouranalysis,wecross- matched our classified galaxies with SDSS using a 3-arc-second threshold,retrievingderivedpropertiesfor9816matchedsources from the MPA-JHU emission-line analysis of SDSS DR7.

*4.1. Catalogue of ram-pressure stripped candidates* Based on the criteria derived in Sect.3.4, we obtained a cata- logue of 6739 SC galaxies, of which 3910 exhibit tail features (SC+T), 5430 MC galaxies, and 29729 RS galaxies. Figure 4 shows examples of SC and SC+T galaxies. The initial catalogue of classified objects released along with thispaperconsistsof37,599objectsfromtheclusterssample.An extract from the catalogue is shown in Table E.1 of the appendix.

C. Bellhouse et al.: Fishing for Jellyfish Galaxies: Exploring ram-pressure stripping with crowd science
SC

|20|SC||||
|---|---|---|---|---|
||SC+T||||
|15 10 SC Fraction (%) 5|MC||||
|0 1013||1014 cluster mass|1015|14 ⊙|

Fig. 7: Fraction of galaxies classified as SC (orange), MC (blue),

and SC+T (pink) by the volunteers, shown as a function of host cluster or group mass. The error bars indicate the standard error withineachmassbin.Thehistogramshowsthenumberofclusters across the halo mass range of the sample.

14*.*8
30 14*.*6 ) *c*

14*.*4200
20

14*.*2
SC Fraction (%) 10

14*.*0
13*.*8
0

MKW4MKW 8A0957A0671A2151aA1367 A2063A2052A2147A2199 NGC 4636 CGCG170-018

Fig.8:Fractionofjellyfishcandidatesoverallstar-forminggalax- ies in clusters with spectroscopy and SDSS overlap, showing only spectroscopically confirmed members and galaxies with *𝑀*∗*>*10

9*.*7 M⊙. The error bars show the1*𝜎*binomial errors
following a normal approximation.

shown that these optically selected samples, while incomplete, are pure (at an*>*80% level for galaxies in clusters Poggianti et al.

2025). Therefore, quantifying the fraction of optically selected RPS candidates in clusters sets a robust lower limit on the influ- ence of RPS.
Figure 7 shows the fraction of jellyfish candidates, mergers,
 and jellyfish candidates with tails as a function of cluster halo massforspectroscopicallyconfirmedmembers.Thefractionsare defined as the number of galaxies in each sample divided by the total number of classified subjects within the cluster; therefore, both the numerator and denominator are both subject to the same selection criteria defined in Sect.2.3. The top panel shows a histogram of the cluster halo masses across the sample. The plot shows that both the SC and SC+T samples exhibit an increasing fraction with cluster halo mass, whereas the merging galaxies exhibit a flatter, fluctuating trend with host cluster mass. Figure7 showsthat thefractionofgalaxiesclassified asSC is generallyindependentofhalomassforclustersbelow3×10 M. Above this value, the SC fraction increases sharply. With more higher-velocityinfallersandadenserICM,itisnaturallyexpected that more massive clusters host environments more conducive to RPS. A similar trend with halo mass is observed in Roberts et al. (2021a,b). The sample of MC galaxies fluctuates in their observed frac- tion as a function of environment, exhibiting the same over- all shape as the SC sample with a less significant increase at higher halo masses. Due to dynamical friction, a lower merger rate in clusters is expected compared to groups, owing to the high velocity dispersion observed in the former. Yet, galaxies in clusters can still face high-speed encounters, known as harass-
Log(M ment (Moore et al. 1996) that may also affect their morphology. Since our classification images do not reveal the end state of the galaxies’interactions,merginggalaxiesandthoseundergoingha- rassment are challenging to visually distinguish, and it is likely that a combination of these two processes drives the observed fluctuation in fraction across cluster mass.

Figure 8 shows the fraction of SC galaxies in a sample of

clusters with both spectroscopic data and SDSS overlap, with clusters ordered by halo mass. Stripping candidate fractions were calculated relative to star-forming galaxies, and a stellar mass limit of*𝑀*∗*>*10

9*.*7 M⊙(derived from the SDSS MPA-
JHU catalogue), was imposed, following the methodology of (Roberts et al. 2021a), to ensure stellar mass completeness. The error bars show the1*𝜎*binomial errors on the fraction calcu- lated following the normal approximation described in Cameron (2011). The plot shows a trend similar to that in Fig.7, with clusters below∼10

14*.*3 M⊙exhibiting low fractions. Above this
threshold, the plot reveals that the SC fraction is largely inde- pendent of environment, with a maximum of around30%of star-forming galaxies exhibiting visual signs of RPS in A2151a and A2052. A2052 exhibits an excess in the fraction of RPS can- didates compared to clusters of similar mass. This is likely due to sloshing processes resulting from the cluster’s highly disturbed nature (Blanton et al. 2011), which can boost stripping events (Roediger et al. 2014; Stroe et al. 2015, 2020; Bellhouse et al.

2022). With the exception of A2052, clusters in the middle of the mass range exhibit higher jellyfish fractions than those at the upper end of the range. As discussed in Sect.2, our sample of clusters is represen- tative across the halo mass range at the 5% significance level (p-value 0.20); however, the full sample undersamples clusters at low redshifts (z≤0.025). If we restrict our clusters to redshifts above this limit, the resulting sample is representative across
Article number, page 9

The catalogue contains the right ascension and declination of each galaxy derived from the DECaLS tractor catalogue, along withthetotalnumberofclassifications,weightedandunweighted votefractionsforeachfeature,andweightedandunweightedvote counts for each feature. The weighted votes and fractions were derived from the debiasing process outlined in Sect.3.5. The fractions are defined in Sect.3.3. The additional group sample andShapleysuperclustersamplewillbereleasedalongsideforth- coming papers in this series.

*4.2. The abundance of RPS candidates across environments* One of the key open questions that studies such as this one hope to answer is how important RPS is for galaxy transformations in clusters (Sampaio et al. 2022, 2024). This is a challenging question to answer due to observational limitations, and optical studies such as ours only observe strong cases of stripping where star formation occurs in the stripped debris. However, it has been

*.* SC *.* MC

RS *.* SC

1*.*0
3 SC+T [mag]

0*.*8 *r*
*|/σ* 2 LOS *g−*

0*.*6
∆V *|*

0*.*4
1

0*.*2

|0 0. 0|1. 0|1. 5|2. 0|0. 0 − 16|− 18|− 20|− 22|− 24|
|---|---|---|---|---|---|---|---|---|
||r/R|||||M [mag]|||

0*.*5
200 *r*

Fig. 9: Projected phase-space diagram for galaxies spectroscop-

Fig. 10: Colour-magnitude diagram of the full RS, SC, and MC

ically confirmed as cluster members, separated into RS (grey samples, showing the full spectroscopic samples, i.e. not limited dots), SC (orange stars), and SC+T (red stars). Middle panel: to galaxies with cluster membership. The undisturbed sample is Escape velocity (grey line) of an NFW profile with a concentra- shown as a greyscale density map, whilst the jellyfish and merger tion parameter,*𝑐*=6. Top and right panels: Radial and velocity samplesareshownasindividualpoints.Thehistogramshowsthe distributions, respectively. In the histograms, we also show the distribution of g-r colours for the three samples. median value for each subgroup.

both halo mass and redshift at the 5% significance level, and the observed trends with halo mass remain unchanged.

*4.3. Location within the clusters* To explore whether the publicly classified SC and SC+T galax- ies exhibit any trends or tendencies with location in their host clusters, we measured the phase-space locations of the subset of galaxies with spectroscopic redshifts, restricting the samples to show only galaxies within2×R₂₀₀ of their host cluster cen- tres with|Δ*𝑉*LOS|/*𝜎*cluster*<*4. Figure9 shows the phase-space plot, along with histograms of the cluster-centric radius and ve- locity, for the RS, SC, and SC+T samples. The histograms are normalised to show the density of each sample, to facilitate com- parison. The individual galaxies are shown in the phase-space plot as grey, orange, and blue points for the undisturbed, jellyfish candidate, and merger samples, respectively. The curves show theescapevelocitycalculatedforanNavarro-Frenk-White(NFW Navarro et al. 1996) profile of a cluster with a concentration pa- rameter of*𝑐*=6. The dashed line indicates the completeness limit, constrained by the4×R₅₀₀ criterion used to select the initial catalogue. The mean limiting radius is2*.*87×R₂₀₀ across the full sample of clusters; however, for the most centrally con- centrated cluster, the cutoff value of4×R₅₀₀ limits the selection to∼2×R₂₀₀. The velocity histogram shows that the distributions of the SC and SC+T samples shift slightly towards higher absolute line-of- sight (LOS) velocities compared to the undisturbed sample by ∼20%. Kolmogorov–Smirnov (K-S) tests of the distributions of the velocities of each sample reveal that they are distinct from the distributionofundisturbedgalaxiesatthe5%level,withp-values of 0.0032 (SC) and 0.0007 (SC+T). Interestingly, the SC galaxies are found at larger cluster- centric radii than undisturbed galaxies, but only by≲10% on average. A K-S test shows that the distributions of cluster-centric radii of both the SC sample and the SC+T sample are distinct Article number, page 10
0*.*8 RS
SC

0*.*7
MC

0*.*6
0*.*5
0*.*4
0*.*3 Normalised Density
0*.*2
0*.*1
0*.*0 0
*.*0 0*.*5 1*.*0 1*.*5 2*.*0 2*.*5
Sersic index

Fig. 11: Histogram of Sérsic index for the RS, MC, and SC

samples,showingallgalaxiesclassifiedas‘SER’intheDECaLS tractor catalogue, including objects without spectroscopy.

from the RS galaxies at the 5% level, with p-values of 0.007 and

0.021 respectively. Since ram-pressure strength scales with galaxy velocity and environmental density, jellyfish galaxies are typically found at higher LOS velocities in phase space and at lower cluster-centric radii (Jaffé et al. 2015; Rhee et al. 2017; Jaffé et al. 2018). This is also an indication that they are on first infall at preferentially radial orbits (Salinas et al. 2024; Biviano et al. 2024). Our sam- ple shows that the selected SC galaxies, and to a lesser extent the MC galaxies, are kinematically distinct from the RS galaxies, as expected for recent infallers.
*4.4. Galaxy colours and morphologies* We also compared the colours and morphologies of the classi- fied samples. Whilst the magnitude limits of the sample selection

C. Bellhouse et al.: Fishing for Jellyfish Galaxies: Exploring ram-pressure stripping with crowd science
a grey hexbin plot, with the individual galaxies in the SC, SC+T, andMCsamplescolouredinorange,pink,andblue,respectively. The solid lines and shaded regions show the linear fits and68% confidence intervals of each sample. The figure shows that all samples exhibit elevated SFR in comparison to the undisturbed RS galaxies, with the difference being more pronounced at lower stellar masses. Ram-pressure stripping is expected to produce an elevated SFR, including in visually identified samples (Poggianti et al. 2016; Vulcani et al. 2020b; Roberts & Parker 2020; Vulcani et al. 2022). Our results confirm that the optically selected SC galaxies selected by the publicexhibitatentativeexcessinSFRand,therefore,areconsis- tent with results for galaxies undergoing environmentally driven disruption as found in the literature.

implicitly impose a colour cut, the selection criteria did not ex- plicitly limit the sample to blue galaxies. Instead, the sample is constrained by the morphology criteria described in Sect.2.3.

Figure 10 shows the colour-magnitude diagram for the spec-

troscopic sample, not limited by cluster membership, with the histogram of colours shown in the panel to the right of the figure. The grey hexbin plot shows the RS galaxies, which show signif- icantly redder g-r colours compared to both of the SC and MS samples. The MC sample, shown by the blue points, are biased towards the blue cloud but are present in both regions. The SC galaxies, shown as orange points, clearly favour the blue cloud. This is evidence that the publicly identified SCs tend to have young stellar populations, in comparison with the overall sam- ple. The histogram shows that both the SC and MC samples are significantly bluer than the RS galaxies. Moreover, K-S tests re- veal that both populations are distinct from the RS galaxies with p-values consistent with zero in both cases. This is consistent with the findings of Vulcani et al. (2022) who compared the B-V colours of both SCs with a reference sample of cluster galaxies. In terms of morphologies, both the MC and SC samples have late-typemorphologies,andthesubsamplesofgalaxiesclassified as‘SER’in the DECaLS tractor catalogue exhibit slightly lower Sérsic indices on average compared to the RS galaxies, as shown in Fig. 11. Whilst the average Sérsic indices are consistent across the samples, K-S tests show that the distributions of the Sérsic indexinboththeSCandMCsamplesdifferfromtheRSgalaxies, with p-values consistent with zero. Both the SC and MC samples exhibitslightbiasestowardslowerSérsicindices,whichisconsis- tent with Vulcani et al. (2022) who found that visually identified SCs generally exhibit late-type morphologies compared with the reference sample. Nevertheless, our morphology constraints in the initial sample selection yield a lesser distinction between the populations, as our sample was pre-selected to include late type morphologies.

*4.5. Star formation rate* ToinvestigatewhethertheSC,SC+T,andMCsamplesexhibiten- hanced SFR in comparison to other blue galaxies, we performed a more detailed analysis of the SFR across the samples using the SDSScross-matchedsubsets.Jellyfishgalaxiesaretypicallychar- acterised as star-forming or composite systems (Poggianti et al. 2017a; Roberts et al. 2021a). The MPA-JHU catalogue assigns abptclassparameter, which distinguishes the dominant ioni- sation sources according to the Baldwin, Phillips, and Terlevich diagram (BPT; Baldwin et al. 1981). This parameter classifies each source as one of six categories: (i) star-forming, (ii) low- SN star-forming, (iii) composite, (iv) Seyfert, (v) LINER, and (vi) unclassified. To mitigate contamination from galaxies with only weak nebular emission, we required anH*𝛼*equivalent width *𝐸𝑊*(*𝐻𝛼*)*>*3Å,consistentwiththeWHANdiagnosticthreshold used to distinguish genuine LINERs from ‘retired’ galaxies pow- ered by old stellar populations (Cid Fernandes et al. 2010). This ensures that systems dominated by faint emission from evolved starsareexcludedfromouranalysis.Anestimateoftheuncertain- ties in the emission lines can be seen in Table 2 of Sampaio et al. (2023). We selected only objects identified as star-forming in the BPT diagram, for which SFRs were computed directly from the H*𝛼*emission-line flux.
Figure 12 shows the SFR versus stellar mass relation for
 the SC, SC+T, and MC samples. In this figure, the full sample of classified,cross-matchedgalaxiesisshownwithnoconstraintson cluster membership. The figure shows the undisturbed sample as
### 5. Conclusions

We presented the first results of*Fishing for Jellyfish Galaxies*, theinauguralcitizen-scienceprojectaimedatidentifyinggalaxies undergoing RPS in optical data. Using imaging from the Dark Energy Camera Legacy Survey and a tailored workflow on the Zooniverseplatform,morethan4400volunteersclassifiednearly 50,000 galaxies across 82 clusters. By calibrating vote-fraction thresholds against expert classi- fications in one cluster (Abell 1644), we defined robust selection criteriawithacompletenessof0.57andPurityof0.63thatyielda catalogue of 6739 jellyfish candidates (SC), 5430 mergers (MC), and 29729 undisturbed galaxies (RS). A subset of 3910 can- didates exhibit clear tail-like features (SC+T), confirming their morphological similarity to previously identified jellyfish sys- tems. An initial analysis shows that SC galaxies preferentially oc- cupylargercluster-centricradiiandhigherline-of-sightvelocities than undisturbed galaxies, consistent with conditions where RPS is most effective. They also display enhanced SFRs, as reported by previous studies, providing independent and more statistically robust evidence that the selected galaxies experience hydrody- namical interactions. An analysis of the spectroscopically con- firmed SC galaxies and their host clusters confirms a trend with environment,withmoremassiveclustershostingalargerfraction of SC and SC+T galaxies, as well as an increased fraction of MC galaxies. These results demonstrate that citizen scientists can reliably identifygalaxiesaffectedbyenvironmentalprocesses,evenwhen the signatures are subtle. The resulting catalogue of∼49,703 visually classified galaxies represents the largest homogeneous sample of its kind to date and provides a valuable resource for future studies of galaxy transformation in clusters. Looking ahead, this catalogue will serve as a training set to fine-tune automated methods for detecting RPS candidates in large surveys (Jaffé et al., in prep.), and to guide the design of future citizen-science projects aimed at identifying galaxies un- dergoing a variety of environmental processes (e.g. ’Looking for strangegalaxies’ 1 ).Itwillalsoenablestatisticalstudiesofthede- tailed properties of RPS candidates in clusters, an investigation of the ‘unwinding’ galaxy population. In a forthcoming publi- cation, we will further present the extension of the ‘Fishing for Jellyfish’ project that uses deeper optical data from HSC and a more-detailedflowchartforclassifications(Quirozetal.inprep.).

[https://www.zooniverse.org/projects/vitorms/](https://www.zooniverse.org/projects/vitorms/) looking-for-strange-galaxies

Article number, page 11

|1 SC|1 SC+T|1 MC|
|---|---|---|
|)|||
|yr 0|0|0|

*−*

*−* 1 *−* 1 *−* 1 log(SFR/M

*−* 2 *−* 2 *−* 2

|1 8|9|10|11 1 8|9|10|11 1 8|9|10|11|
|---|---|---|---|---|---|---|---|---|---|
|0|||0|||0||||
|∆ SFMS (dex) − 81|9 log(M|10 /M|11 − 81 )|9 log(M|10 /M|11 − 81 )|9 log(M|10 /M|11 )|

*∗* *∗ ∗*

Fig. 12: SFR mass relation for galaxies in the SC, SC+T, and MC samples, using the full classified sample of galaxies cross-matched

with SDSS. The coloured points show individual galaxies in the sample, whilst the grey hex-plot shows the density of the RS galaxies. The coloured lines and shaded regions indicate a linear fit and 1*𝜎*confidence interval respectively.

### Data availability

The catalogue of classified galaxies produced by this project is only available in electronic form at the CDS via anonymous ftp to cdsarc.u-strasbg.fr (130.79.128.5) or via [http://cdsweb.u-](http://cdsweb.u-) strasbg.fr/cgi-bin/qcat?J/A+A/.

*Acknowledgements.*This publication uses data generated via the Zooniverse.org platform,developmentofwhichisfundedbygeneroussupport,includingaGlobal Impact Award from Google, and by a grant from the Alfred P. Sloan Founda- tion. We gratefully acknowledge the thousands of volunteers who participated in the Fishing for Jellyfish Galaxies Zooniverse project. Their classifications made this work possible. We thank the Zooniverse community for their enthusiasm, careful visual inspections, and valuable discussions on the Talk forums. This project has received funding from the European Research Council (ERC) under the European Union’s Horizon 2020 research and innovation programme (grant agreement No. 833824). YLJ acknowledges support from the Agencia Nacional deInvestigaciónyDesarrollo(ANID)throughBasalprojectFB210003,FONDE- CYT Regular projects 1241426 and 123044, and Millennium Science Initiative Program NCN2024_112.

### References

Baldwin, J. A., Phillips, M. M., & Terlevich, R. 1981, PASP, 93, 5 Bamford, S. P., Nichol, R. C., Baldry, I. K., et al. 2009, MNRAS, 393, 1324 Bellhouse, C., McGee, S. L., Smith, R., et al. 2021, MNRAS, 500, 1285 Bellhouse, C., Poggianti, B., Moretti, A., et al. 2022, ApJ, 937, 18 Biviano, A., Poggianti, B. M., Jaffé, Y., et al. 2024, ApJ, 965, 117 Blanton, E. L., Randall, S. W., Clarke, T. E., et al. 2011, ApJ, 737, 99 Boselli, A. & Gavazzi, G. 2006, PASP, 118, 517 Byrd, G. & Valtonen, M. 1990, ApJ, 350, 89 Cameron, E. 2011, PASA, 28, 128 Cid Fernandes, R., Stasińska, G., Schlickmann, M. S., et al. 2010, MNRAS, 403, 1036 Crossett, J. P., Jaffé, Y. L., McGee, S. L., et al. 2025, A&A, 694, A204 Dey, A., Schlegel, D. J., Lang, D., et al. 2019, AJ, 157, 168 Fasano, G., Marmo, C., Varela, J., et al. 2006, A&A, 445, 805 Finoguenov, A., Rykoff, E., Clerc, N., et al. 2020, A&A, 638, A114 Flaugher, B., Diehl, H. T., Honscheid, K., et al. 2015, AJ, 150, 150 Fossati, M., Fumagalli, M., Boselli, A., et al. 2016, MNRAS, 455, 2028 Genel, S., Vogelsberger, M., Springel, V., et al. 2014, MNRAS, 445, 175 George, K., Poggianti, B. M., Omizzolo, A., et al. 2024, A&A, 690, A337 Giunchi, E., Gullieuszik, M., Poggianti, B. M., et al. 2023a, ApJ, 949, 72 Giunchi, E., Poggianti, B. M., Gullieuszik, M., et al. 2023b, ApJ, 958, 73 Giunchi, E., Scarlata, C., Werle, A., et al. 2025, A&A, 696, A228 Gullieuszik, M., Poggianti, B., Fasano, G., et al. 2015, A&A, 581, A41 Gunn, J. E. & Gott, III, J. R. 1972, ApJ, 176, 1

Article number, page 12

Ignesti, A., Vulcani, B., Botteon, A., et al. 2023, A&A, 675, A118 Jaffé, Y. L., Poggianti, B. M., Moretti, A., et al. 2018, MNRAS, 476, 4753 Jaffé, Y. L., Smith, R., Candlish, G. N., et al. 2015, MNRAS, 448, 1715 Kenney, J. D. P., van Gorkom, J. H., & Vollmer, B. 2004, AJ, 127, 3361 Kolcu, T., Crossett, J. P., Bellhouse, C., & McGee, S. 2022, MNRAS, 515, 5877 Lintott, C. J., Schawinski, K., Slosar, A., et al. 2008, MNRAS, 389, 1179 Lourenço, A. C. C., Jaffé, Y. L., Vulcani, B., et al. 2023, MNRAS, 526, 4831 Matijević, L., Tomičić, N., Marasco, A., et al. 2026, A&A, 707, A40 McPartland, C., Ebeling, H., Roediger, E., & Blumenthal, K. 2016, MNRAS, 455, 2994 Merritt, D. 1983, ApJ, 264, 24 Mihos, J. C., Bothun, G. D., & Richstone, D. O. 1993, ApJ, 418, 82 Moore, B., Katz, N., Lake, G., Dressler, A., & Oemler, A. 1996, Nature, 379, 613 Navarro, J. F., Frenk, C. S., & White, S. D. M. 1996, ApJ, 462, 563 Peluso, G., Vulcani, B., Poggianti, B. M., et al. 2022, ApJ, 927, 130 Piffaretti, R., Arnaud, M., Pratt, G. W., Pointecouteau, E., & Melin, J. B. 2011, A&A, 534, A109 Poggianti, B. M., Fasano, G., Omizzolo, A., et al. 2016, AJ, 151, 78 Poggianti, B. M., Ignesti, A., Gitti, M., et al. 2019, ApJ, 887, 155 Poggianti, B. M., Jaffé, Y. L., Moretti, A., et al. 2017a, Nature, 548, 304 Poggianti, B. M., Moretti, A., Gullieuszik, M., et al. 2017b, ApJ, 844, 48 Poggianti, B. M., Vulcani, B., Tomicic, N., et al. 2025, A&A, 699, A357 Raddick,M.J.,Bracey,G.,Gay,P.L.,etal.2013,arXive-prints,arXiv:1303.6886 Rhee, J., Smith, R., Choi, H., et al. 2017, ApJ, 843, 128 Roberts, I. D. & Parker, L. C. 2020, MNRAS, 495, 554 Roberts, I. D., van Weeren, R. J., McGee, S. L., et al. 2021a, A&A, 650, A111 Roberts, I. D., van Weeren, R. J., McGee, S. L., et al. 2021b, A&A, 652, A153 Roberts, I. D., van Weeren, R. J., Timmerman, R., et al. 2022, A&A, 658, A44 Roediger,E.,Brüggen,M.,Owers,M.S.,Ebeling,H.,&Sun,M.2014,MNRAS, 443, L114 Salinas, V., Jaffé, Y. L., Smith, R., et al. 2024, MNRAS, 533, 341 Sampaio, V. M., Aragón-Salamanca, A., Merrifield, M. R., et al. 2023, MNRAS, 524, 5327 Sampaio,V.M.,deCarvalho,R.R.,Aragón-Salamanca,A.,etal.2024,MNRAS, 532, 982 Sampaio,V.M.,deCarvalho,R.R.,Ferreras,I.,Aragón-Salamanca,A.,&Parker,

L. C. 2022, MNRAS, 509, 567
Sheen, Y.-K., Smith, R., Jaffé, Y., et al. 2017, ApJ, 840, L7 Sifón, C., Finoguenov, A., Haines, C. P., et al. 2025, A&A, 697, A92 Sijacki, D., Vogelsberger, M., Genel, S., et al. 2015, MNRAS, 452, 575 Spitzer, Jr., L. & Baade, W. 1951, ApJ, 113, 413 Springel, V. 2000, MNRAS, 312, 859 Stroe, A., Hussaini, M., Husemann, B., Sobral, D., & Tremblay, G. 2020, ApJ, 905, L22 Stroe, A., Oosterloo, T., Röttgering, H. J. A., et al. 2015, MNRAS, 452, 2731 Sun, M., Jones, C., Forman, W., et al. 2006, ApJ, 637, L81 Tinsley, B. M. & Larson, R. B. 1979, MNRAS, 186, 503 Tomičić, N., Hughes, A., Kreckel, K., et al. 2018, ApJ, 869, L38 Toomre, A. 1977, in Evolution of Galaxies and Stellar Populations, ed. B. M. Tinsley & R. B. G. Larson, D. Campbell (Yale University Observatory), 401

C. Bellhouse et al.: Fishing for Jellyfish Galaxies: Exploring ram-pressure stripping with crowd science
Valluri, M. 1993, ApJ, 408, 57 Vogelsberger, M., Genel, S., Springel, V., et al. 2014, MNRAS, 444, 1518 Vollmer, B., Cayatte, V., Balkowski, C., & Duschl, W. J. 2001, ApJ, 561, 708 Vulcani, B., Fritz, J., Poggianti, B. M., et al. 2020a, ApJ, 892, 146 Vulcani, B., Poggianti, B. M., Gullieuszik, M., et al. 2018, ApJ, 866, L25 Vulcani, B., Poggianti, B. M., Moretti, A., et al. 2021, ApJ, 914, 27 Vulcani, B., Poggianti, B. M., Smith, R., et al. 2022, ApJ, 927, 91 Vulcani, B., Poggianti, B. M., Tonnesen, S., et al. 2020b, ApJ, 899, 98 Vulcani, B., Treu, T., Calabrò, A., et al. 2023, ApJ, 948, L15 Walmsley, M., Lintott, C., Géron, T., et al. 2022, MNRAS, 509, 3966 Willett, K. W., Lintott, C. J., Bamford, S. P., et al. 2013, MNRAS, 435, 2835 Yagi, M., Yoshida, M., Komiyama, Y., et al. 2010, AJ, 140, 1814 York, D. G., Adelman, J., Anderson, Jr., J. E., et al. 2000, AJ, 120, 1579 Zinger, E., Joshi, G. D., Pillepich, A., Rohr, E., & Nelson, D. 2024, MNRAS, 527, 8257

Article number, page 13

*A&A proofs:* manuscript no. main

### Appendix A: Redshift of the cluster sample

Figure A.1 shows the distribution of redshifts of the clusters con- sidered in our sample, which is representative of clusters across the halo mass range considered, with a slight undersampling at very low redshifts (*𝑧 <.*025).

500 Number of galaxies 250

0*.*00 0*.*05 0*.*10 0*.*15 0*.*20 0*.*25 0*.*30 0*.*35
z

Fig. A.1: Redshift distribution of the clusters listed in Tables 1

and 2

### Appendix B: Number of classifications per galaxy

Figure B.1 shows the distribution of classifications per galaxy, showing the minimum number of classifications is 10, the maxi- mum is above 70, and that the sample is not dominated by poorly sampled galaxies.10

Number of galaxies 101

100 10 20 30 40 50 60 70 classifications

Fig. B.1: Distribution of classifications per galaxy, showing that

the sample is not dominated by poorly sampled galaxies.

Article number, page 14

C. Bellhouse et al.: Fishing for Jellyfish Galaxies: Exploring ram-pressure stripping with crowd science
### Appendix C: Classification workflow steps

### Does the galaxy appear warped, disturbed or asymmetric?

**Bad image** **Yes No**

**Does the galaxy appear to be merging or interacting with another galaxy?**

**Not Merging Merging**

**Does the galaxy have clear spiral arms?**

**No Yes**

### Do the spiral arms appear to be extending, or unwinding?

**Yes No**

**Does the Galaxy have a distinct tail or removed material?**

**Yes No**

**Is the tail clear enough that you can draw a line indicating its direction?**

**Yes No**

**Does the tail extend from the centre of the galaxy, or elsewhere on the disk?**

**Centre Elsewhere The Whole Disk**

**Draw the direction of the tail**

**End Classification**

Fig. C.1: Workflow used in the classification process. The workflow is designed to minimise the time spent classifying objects, such

as undisturbed galaxies or mergers, which are not of interest, whilst simultaneously maximising the information gained from objects of interest, such as those with signs of stripped tails.

Article number, page 15

|||A&A proofs:|||
|---|---|---|---|---|
||1.0 1.0||1.0|1.0|
||0.8 0.8 0.6 a 0.6||0.8 a 0.6|0.8 0.6|
|||||0.5|
||0.4 0.4||0.4||
||0.2 0.2||0.2||
||0.0 0.0 0.0 0.2 0.4 0.6 0.8 1.0 0.0 F d i s t u r b e d|0.2 0.4 0.6 0.8 F d i s t u r b e d|0.0 0.0|0.0 0.4 0.6 0.8 1.0 F n o n m e r g e r|
||1.0 1.0||1.0|1.0|
||0.8 0.8||0.8||
||0.6 a 0.6||a 0.6|0.7 0.6|
|||||0.5|
||0.4 0.4||0.4|0.4|
||0.2 0.2||0.2||
||0.0 0.0 0.0 0.2 0.4 0.6 0.8 1.0 0.0 F d i s t u r b e d 𝐹 disturbed, 𝐹 non_merger, and 𝐹 tail|0.2 0.4 0.6 0.8 F d i s t u r b e d. 39, 0. 77, 0.|0.0 0.0|0.0 0.4 0.6 0.8 1.0 F n o n m e r g e r 𝑥 = Δ 𝑦 = Δ 𝑧 =0. 05. Within each|

### Appendix D: Classification criteria optimisation

r e g er il il nm t t o n*F F* Purity *F*

(weighted by voxel counts)

1.0 0.2
r e g er il il nm t t o n*F F* *F* Completeness

(weighted by voxel counts)

1.0 0.2
Fig.D.1:Distributionofpurity(top)andcompleteness(bottom)fordifferentcombinationsofthekeyvotefractionsusedforselecting RPS candidates:(). The plots are voxelised with uniform cellsΔ voxel we compute the mean of the metric, and each 2D pixel displays in colour the count-weighted mean across the hidden axis. The dashed lines mark the adopted thresholds in our criteria(0 37)(see Sect. 3.4), and the star marks their intersection.

### Appendix E: Catalogue description

Table E.1 shows a brief example of the catalogue of classified objects associated with this paper. The selection criteria to produce the samples of SC, SC+T, and MC galaxies in this study are described in Sect.3.4; however, for most purposes we recommend recalculating appropriate criteria depending on the level of purity required.

Article number, page 16

Table E.1: Example lines from the catalogue showing a selection of classified galaxies from two separate regions.

RA Dec Nclass*.𝐹*dist*.𝐹*dist*.𝐹*merg*.𝐹*merg*.𝐹*tail*𝐹*tail*𝐹*prob*.𝐹*prob*.*Vdist*.*Vdist*.*Vmerg*.*Vmerg*.*VtailVtailVprob*.*Vprob*.* *weighted weighted weighted weighted weighted weighted*weighted *weighted*

|90.449−|59.375|10|0.13|0.13|0.00|0.00|1.00|1.00|0.20|0.20|1.0|1|0.0|0|1.0|1|2.0|2|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|89.296−|59.207|10|0.10|0.10|0.00|0.00|1.00|1.00|0.00|0.00|1.0|1|0.0|0|1.0|1|0.0|0|
|89.393−|59.245|10|0.00|0.00|0.00|0.00|0.00|0.00|0.30|0.30|0.0|0|0.0|0|0.0|0|3.0|3|
|89.622−|59.315|10|0.10|0.10|0.00|0.00|1.00|1.00|0.00|0.00|1.0|1|0.0|0|1.0|1|0.0|0|
|89.623−|59.125|10|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.0|0|0.0|0|0.0|0|0.0|0|
|89.686−|59.221|10|0.17|0.20|0.00|0.00|0.00|0.00|0.00|0.00|1.5|2|0.0|0|0.0|0|0.0|0|
|89.742−|59.191|10|0.43|0.43|0.67|0.67|0.00|0.00|0.30|0.30|3.0|3|2.0|2|0.0|0|3.0|3|
|89.878−|59.305|10|0.25|0.25|0.00|0.00|0.50|0.50|0.20|0.20|2.0|2|0.0|0|1.0|1|2.0|2|
|89.928−|59.198|10|0.38|0.38|0.33|0.33|0.33|0.33|0.20|0.20|3.0|3|1.0|1|1.0|1|2.0|2|
|90.084−|59.366|10|0.00|0.00|0.00|0.00|0.00|0.00|0.20|0.20|0.0|0|0.0|0|0.0|0|2.0|2|
|90.145−|59.235|10|0.33|0.33|0.33|0.33|0.67|0.67|0.10|0.10|3.0|3|1.0|1|2.0|2|1.0|1|
|90.152−|59.256|10|0.43|0.43|0.67|0.67|0.33|0.33|0.30|0.30|3.0|3|2.0|2|1.0|1|3.0|3|
|90.162−|59.148|10|0.30|0.30|0.00|0.00|0.67|0.67|0.00|0.00|3.0|3|0.0|0|2.0|2|0.0|0|
|90.322−|59.237|10|0.30|0.30|0.33|0.33|0.67|0.67|0.00|0.00|3.0|3|1.0|1|2.0|2|0.0|0|
|90.340−|59.317|10|0.11|0.11|0.00|0.00|0.00|0.00|0.10|0.10|1.0|1|0.0|0|0.0|0|1.0|1|
|90.556−|59.358|10|0.50|0.50|0.00|0.00|0.80|0.80|0.00|0.00|5.0|5|0.0|0|4.0|4|0.0|0|
|90.627−|59.159|10|0.00|0.00|0.00|0.00|0.00|0.00|0.26|0.30|0.0|0|0.0|0|0.0|0|2.5|3|
|90.984−|59.149|10|0.38|0.38|0.33|0.33|0.67|0.67|0.20|0.20|3.0|3|1.0|1|2.0|2|2.0|2|
|91.147−|59.187|10|0.79|0.80|0.00|0.00|0.53|0.50|0.00|0.00|7.5|8|0.0|0|4.0|4|0.0|0|
|91.197−|59.196|10|0.70|0.70|0.00|0.00|1.00|1.00|0.00|0.00|7.0|7|0.0|0|7.0|7|0.0|0|
|89.420−|58.982|11|0.27|0.27|0.00|0.00|0.33|0.33|0.00|0.00|3.0|3|0.0|0|1.0|1|0.0|0|
|89.491−|58.980|10|0.56|0.56|0.00|0.00|0.40|0.40|0.10|0.10|5.0|5|0.0|0|2.0|2|1.0|1|
|89.503−|59.050|10|0.20|0.20|0.50|0.50|0.00|0.00|0.00|0.00|2.0|2|1.0|1|0.0|0|0.0|0|
|89.576−|59.032|10|0.00|0.00|0.00|0.00|0.00|0.00|0.30|0.30|0.0|0|0.0|0|0.0|0|3.0|3|
|89.781−|59.062|10|0.14|0.14|0.00|0.00|0.00|0.00|0.30|0.30|1.0|1|0.0|0|0.0|0|3.0|3|
|89.875−|59.022|10|0.10|0.10|0.00|0.00|1.00|1.00|0.00|0.00|1.0|1|0.0|0|1.0|1|0.0|0|
|89.955−|58.935|10|0.25|0.25|0.50|0.50|0.50|0.50|0.20|0.20|2.0|2|1.0|1|1.0|1|2.0|2|
|90.608−|59.105|10|0.50|0.50|0.00|0.00|0.50|0.50|0.20|0.20|4.0|4|0.0|0|2.0|2|2.0|2|
|90.734−|59.040|10|0.67|0.67|0.33|0.33|0.67|0.67|0.10|0.10|6.0|6|2.0|2|4.0|4|1.0|1|
|353.818|26.317|10|0.33|0.33|0.50|0.50|0.50|0.50|0.37|0.40|2.0|2|1.0|1|1.0|1|3.5|4|
|353.825|26.296|10|0.38|0.38|0.00|0.00|0.67|0.67|0.16|0.20|3.0|3|0.0|0|2.0|2|1.5|2|
|353.846|26.147|10|0.40|0.40|0.50|0.50|0.00|0.00|0.50|0.50|2.0|2|1.0|1|0.0|0|5.0|5|
|353.851|26.182|10|0.12|0.11|0.00|0.00|1.00|1.00|0.11|0.10|1.0|1|0.0|0|1.0|1|1.0|1|
|353.874|26.184|10|0.38|0.38|0.00|0.00|1.00|1.00|0.20|0.20|3.0|3|0.0|0|3.0|3|2.0|2|
|353.884|26.315|10|0.22|0.22|0.00|0.00|1.00|1.00|0.10|0.10|2.0|2|0.0|0|2.0|2|1.0|1|
|353.897|26.201|10|0.12|0.11|1.00|1.00|0.00|0.00|0.11|0.10|1.0|1|1.0|1|0.0|0|1.0|1|
|353.910|26.367|10|0.14|0.14|0.00|0.00|1.00|1.00|0.30|0.30|1.0|1|0.0|0|1.0|1|3.0|3|
|354.017|26.367|10|0.00|0.00|0.00|0.00|0.00|0.00|0.60|0.60|0.0|0|0.0|0|0.0|0|6.0|6|
|354.055|26.362|10|0.88|0.88|0.14|0.14|0.29|0.29|0.20|0.20|7.0|7|1.0|1|2.0|2|2.0|2|
|354.078|26.180|10|0.14|0.14|0.00|0.00|0.00|0.00|0.30|0.30|1.0|1|0.0|0|0.0|0|3.0|3|
|354.100|26.370|10|0.30|0.30|0.00|0.00|0.33|0.33|0.00|0.00|3.0|3|0.0|0|1.0|1|0.0|0|
|···|···|···|···|···|···|···|···|···|···|···|···|···|···|···|···|···|···|···|
|Notes.N Columns marked as|is the total number of classifications, which is always greater than 10. The fractions, for example weightedshow the counts after debiasing, as described in Sect.3.5.|||||||||𝐹|, are defined in Sect.3.3. The vote columns show the total numberfor each feature.||||||||

C. Bellhouse et al.: Fishing for Jellyfish Galaxies: Exploring ram-pressure stripping with crowd science
Article number, page 17

class dist*.*
