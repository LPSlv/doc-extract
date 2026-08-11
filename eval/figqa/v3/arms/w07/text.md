# QASP: Query-Adaptive Robust Vector Search Policy

*∗* *∗* Hakan Ferhatosmanoglu Kushal Kumar Tal Wagner Andy Warfield *Amazon Amazon* *Amazon and Tel-Aviv University Amazon* London, UK New York, USA Tel Aviv, Israel Vancouver, Canada hakanf@amazon.com kushlku@amazon.com talw@amazon.com warfield@amazon.com

***Abstract*—A fundamental challenge of vector search is achiev- ing consistently high recall while minimizing computational**

**costs. Fixed search parameters cause significant performance variance across queries, and conventional evaluation on average**

**recall masks these per-query disparities. We introduce QASP** **(Query-Adaptive robust vector Search Policy), which predicts the complete recall progression curve per query via a single upfront**

**supervised regression, from which a search policy is derived for any recall target; this avoids iterative model invocations**

**during search or separate predictors per target. By predicting normalized recall values with scale-invariant features and pre-**

**search inference, QASP generalizes across recall targets, index configurations, and datasets. Its fine-grained progress predictions**

**further enable a lightweight reactive complement that adjusts search depth based on predicted-versus-observed deviations with-**

**out additional inference. We prove that QASP requires a finite training sample independent of dataset size and dimensionality,**

**that its loss exceeds the irreducible lower bound of any fixed** **policy by a vanishing margin, and that its data access savings over fixed probing grow exponentially in intrinsic dimensionality.**

**Experimentally, QASP achieves significantly lower recall variance and deviation from target, higher query satisfaction rate, and**

**scales to large data and hierarchical indices without retraining, achieving 99% recall with 80% less data access.**

***Index Terms*—Vector Search Policy, Approximate Nearest** **Neighbor Search, Proactive Policy Learning**

I. INTRODUCTION
Given a query vector*q∈*R *d* and a dataset*X⊂*R *d*, vector (similarity) search aims to find the*k*vectors*{x* *q*

||,...,x|}⊂|
|---|---|---|
|q ·|1|k|

1 *q* *k* *X*that minimize dist(*q,x* *q* ), where dist(*·,·*)is a notion of distance. The fraction of*k*closest vectors found is the*recall* for that query. A vector search policy determines the search parameters to achieve high recall with low cost. Practitioners typically rely on heuristic guidelines to identify search parameters based on average performance, generating rules such as accessing *√* a fixed proportion*α∈*[0*.*05*,*0*.*1] of the dataset or*⌊ L⌋*out of*L*partitions [1]–[3]. Query- agnostic settings fail to capture heterogeneous query difficulty and the resulting variation in computational needs [4]–[7]. This causes over-reading for easy queries and under-reading for difficult ones. Conventional evaluation methods compound this problem by focusing on average recall, which masks per-query disparities. Figure1illustrates how query-agnostic

*∗* Equal contribution.

policies access significantly more data than the query-adaptive approach. Our goal is to design a proactive search policy that consis- tently achieves high recall with minimal performance variance across queries regardless of difficulty. We present QASP, **Q**uery-**A**daptive robust vector**S**earch**P**olicy, which addresses this through supervised regression that predicts the complete recall progression curve, from which a policy is derived for any recall target. A single upfront inference produces the fine-grained predictions, departing from recent approaches that invoke models iteratively during search or design sepa- rate predictors per recall target. QASP’s formulation predicts normalized recall values, and combined with scale-invariant features and pre-search inference, admits richer architectures and target-agnostic deployment. QASP’s fine-grained progress predictions also enable a lightweight reactive complement that treats each progress estimate as a testable hypothesis and ad- justs search depth based on deviations between predicted and observed discovery rates, without additional model inference. QASP is designed for partitioning-based indices, e.g., In- verted File (IVF), clustering, quantization, multi-dimensional trees, due to their discrete, independent units that enable highly efficient upfront recall estimation with minimal training data, and enable proactive parameter selection and resource allocation. Partitioning-based methods are widely preferred in production systems due to their memory efficiency, paral- lelization across computational and storage units, compatibility with distributed architectures, and ability to achieve sublinear scaling [8]. We establish theoretical guarantees for QASP. We prove that a finite sample of queries suffices for training, independent of dataset size and dimensionality. We show a fundamental lower bound on the population loss of any fixed probe policy, determined by the variance in query difficulty, and show that QASP’s loss exceeds that of the optimal fixed policy by only a negligible margin that vanishes with increased data, establishing both generalization and competitive performance guarantees. Beyond loss, we show that QASP achieves strictly lower expected data access than fixed probing, with the savings growing exponentially in the data’s intrinsic dimensionality as query difficulty heterogeneity increases. To our knowledge, this is also the first work to explore transfer learning and domain adaptation in vector search,

## arXiv:2607.29606v1 [cs.IR] 31 Jul 2026

Fig. 1: Comparing fixed and adaptive policies: Query sat-

isfaction rate (% of queries achieving 90% recall) versus data accessed (Deep1B 10M dataset). For fixed nprobe, we gradually increase probes and plot query satisfaction and data accessed. QASP adaptively sets parameters for the same query satisfaction. Fixed policy consistently over-reads, with the gap widening as more queries reach recall target.

where prior solutions are predominantly coupled to specific index configurations and recall targets. We design normalized scale-invariant features that integrate query difficulty signals with index characteristics, and express both features and predictions as normalized ratios, enabling the learned function to better generalize across index configurations, recall targets, and datasets. Through ablation studies and feature importance analysis, we identify the most influential features for recall prediction. Experimental evaluation confirms that QASP consistently outperforms baselines and achieves around57*.*7%lower recall variance,33*.*6%lower deviation from recall target, and7*.*3% higher query satisfaction rate with similar or lower data access. QASP transfers effectively across datasets and index config- urations with zero-shot or minimal fine-tuning, and scales to larger data and to hierarchical indices achieving 99% recall with 80% less data access. To summarize, this paper makes following contributions: *•*We introduce QASP, a learning-based query-adaptive search that predicts fine-grained recall progress, from which search policies are derived for any recall target. QASP enables search optimization beyond early termination, cross- domain transfer, and a lightweight reactive complement that can monitor predictions during search. *•*We establish theoretical bounds on sample size to train QASP to near optimality. We show that fixed policies leave an inherent sub-optimality gap, and prove that QASP is guaranteed to perform within this gap up to a negligible margin. We further prove that QASP achieves strictly lower

|||∗|∗|∗ ∗|
|---|---|---|---|---|
|∗ ∗|||||
|||d|||

expected data access, with savings growing exponentially in intrinsic dimensionality. *•*We conduct experiments using both standard and query variability-aware evaluation metrics. QASP achieves signifi-

cant performance improvements over baselines, with further gains on large datasets, at high recall targets, and for hard queries, where traditional approaches struggle with both consistency and cost.

### II. QUERY-ADAPTIVEROBUSTVECTORSEARCHPOLICY

We formalize a learning framework to design a robust search policy based on predicting fine-grained recall contributions of each index partition to optimize per-query performance. Ideal ML-enhanced search should support low inference overhead. Partitioning-based data organization offers a well-suited set- ting that makes this feasible by decomposing search into units whose recall contributions can be predicted separately and up- front. We present our framework concretely for clustering/IVF (Inverted File) indices [9]–[13], though the approach extends to any partitioning-based organization, including hierarchical clustering as we study in SectionII-D3. Partitioning-based indices are the core component of large-scale vector databases [12]–[16]. An IVF-type index*I*(*D*)built over a dataset*D⊂*R *d* is meant to improve the computational cost of fully exhaustive search. To this end, it partitions*D*into*L*non-overlapping partitions (clusters)*C₁,...,CL*with corresponding centroids *µ,...,µ*. Given a query*q∈*R, *d* exhaustive search is 1 *L* performed only on the*l*top-ranked clusters, where*l≪L*, and the clusters are ranked by their centroid distance from the query. This raises the question of how to set*l*, which is called the number of*probes*. Commonly,*l*is set to a fixed value for all queries (see SectionV), which we refer to as*fixed probe* *policy*. Our goal is to leverage supervised learning in order to predict the optimal*l*per query. To start, we formally define query-dependent probe policies.

*d* **Definition 1.***A*probe policy*is a mapg*:R *×*[0*,*1]*→*N*,* *d* *which maps a queryq∈*R *and a recall targetr∈*[0*,*1] *to a numberl*=*g*(*q,r*)*of top-ranked clusters to probe for*

*q. The policy is*valid*for an indexI*(*D*)*withLclusters if*
*d* 1*≤g*(*q,r*)*≤Lfor allq∈*R *andr >*0*(thus, the policy* *instructs us to probe at least one cluster and no more than all* *clusters per query).*

Given a query set*Q⊂*R *d* and recall target*r* *∗* *∈*[0*,*1], we say that a policy*g*is*optimal*for*Q*and*r* *∗* if it probes exactly the minimal number of clusters necessary to achieve recall*r* *∗*

on each query*q∈Q*. Formally, let*RI*(*D*)(*q,l*)denote the recall attained for a query*q*when probing its*l*top-ranked clusters in*I*(*D*). Then, the optimal number of probes*ℓ* *∗* can be defined as follows:

*ℓ* *∗* (*q,r*) := min*{l*: *RI*(*D*)(*q,l*)*≥r}.*(1)

An optimal policy*g* for*Q*and*r* satisfies*g* (*q,r*) = *ℓ* (*q,r*)for all*q∈Q*. This does not specify the behavior of*g*on queries*q∈*R *\Q*, i.e., it does not specify how to generalize beyond*Q*.

*A. Ordinal Regression* Our goal is thus to find a policy which is optimal (or close to it) on*Q*, while also generalizing to unseen queries*q∈*R
*d* *\Q* and to recall values beyond*r* *∗*. This can be naturally cast as a supervised learning problem, where we train a machine learning model to predict the behavior of the index*I*(*D*)on the workload*Q*, using its observed performance on*Q*as well as the ground-truth nearest neighbors of*Q*in*D*as labels to train on. Supervised learning is useful here for two key properties: on the one hand, ML models can be efficiently trained to find high-quality solutions in the large function spaces, like that of probe policies; on the other hand, if trained with suitable features, ML models are known to generalize well to unseen inputs. We now formalize an appropriate supervised learning prob- lem. LetΘbe the parameter space for a parameterized class *G*=*{gθ*: *θ∈*Θ*}*of probe policies. To find an optimal probe policy in*G*for queries*Q*and recall target*r* *∗*, consider the optimization problem:

||1|X||||
|---|---|---|---|---|---|
|∗|θ∈Θ 2|∗|∗ θ|∗ 2||
|||q∈Q||||

*θ* = arg min (*ℓ* (*q,r*)*−g* (*q,r*))*.*(2) *L |Q|*

This is an ordinal regression problem, since its goal is to learn a function*gθ∗* whose output is an ordinal value*l∈{*1*,...,L}*. The normalization by*L²|Q|*ensures that the minimized loss is in[0*,*1]for convenience and does not alter the minimization problem.

*B. Recall-based Regression* Since ordinal regression is notoriously difficult to optimize [17], we develop an alternative recall-based approach for learning the probe-policy. To this end, we learn a*recall* *predictor*as an intermediate step. It maps a query*q*and number of probes*l*to the recall it expects to achieve for that query by probing the index its*l*top-ranked clusters. A recall predictor gives rise to a probe policy by using the minimal number probes predicted to attain the recall target. **Definition 2.***Given an indexI*(*D*)*withLclusters, a*recall predictor*is a functionf*:R
*d* *×*N*→*[0*,*1]*that maps a query* *and probe count to a predicted recall value.*

**Definition 3.***A recall predictorfinduces a probe policyg* [*f*]

*defined as*

[*f*] *g* (*q,r*) := min*{l*: *f*(*q,l*)*≥r}.*(3)

Let Θeparameterize a class of recall predictors,*F*=*{fθ*: *θ∈* Θe*}*. The induced class of parameterized probe policies is*G*=*{gθ*=*g* [*fθ*] : *θ∈* Θe*}*. We learn a recall predictor by optimizing an L2 loss:

X X*L* *∗*<u>1</u> 2 *θ* = arg min*θ I*(*D*)(*q,l*)

|||f (q,l)−R|.(4)|
|---|---|---|---|
|θ∈Θ|q∈Q l=1|θ||

*θ∈*Θ *L|Q|*

Learning a recall predictor as a surrogate for learning a probe policy is justified by the following consistency property.

**Proposition 4.***Supposeθ* *∗* *∈* Θe*is such thatfθ∗ attains zero* *loss in eq. (4). Theng ∗* =*g* [*fθ∗*] *attains zero loss in eq. (2).* *θ*

*Proof.*Zero loss in eq. (4) implies that*fθ∗* (*q,l*) =*RI*(*D*)(*q,l*) for all*q,l*. Plugging this in eqs. (1) and (3) yields*ℓ* *∗* (*q,r*) = *g* [*fθ∗*] (*q,r*)for all*q,r*. This yields zero loss in eq. (2).

Recall-based regression (eq. (4)) offers numerous advan- tages over direct ordinal regression for the probe policy (eq. (2)). First, it is more tractable to optimize [17]. Second, since its target predictions are values in a fixed range[0*,*1], independent of the number of clusters*L*, the same induced policy is transferrable across indices with different numbers of clusters. Third, the learning problem in eq. (4), unlike that in eq. (2), is independent of a recall target*r* *∗*, and thus generalizes better across different recall values. Fourth, the loss function in eq. (4) directly involves*L*numerical values obtained from the index*I*(*D*)per query (the values *{RI*(*D*)(*q,l*) : *l*= 1*,...,L* *∗* *}*), *∗* compared to just one such value in eq. (2) (the value*ℓ* (*q,r*)). This allows the learning model to use more supervised labels per query from the index, increasing ground-truth utilization and learning effectiveness. Directly predicting nprobe couples the model to a specific recall target and index size, and provides*L×*fewer supervision signals per query. We confirm empirically (in SectionVI-D) that single-nprobe prediction results in significantly higher variance and more data access than QASP (TableII). Fifth, recall-based regression inherently produces a recall prediction per cluster, and these values can be leveraged at search time for further optimizations without model inference, such as reactive early/late termination if rate of newly discovered neighbors per probe subceeds/exceeds (respectively) the initial recall predictions (see SectionII-E).

*C. Model Training* QASP employs supervised learning to model the relation- ship between query characteristics and retrieval performance. We share details on different parts of the training pipeline.
*1) Training Data Generation:* We obtain training signals by
performing nearest neighbor search under configurations that approximate exhaustive retrieval for queries sampled from the dataset (or query workload if available). Recall measurements are obtained for every searched partition and serve as pre- diction targets. Query features are obtained as a by-product of this one time search with no additional overhead (see SectionIII). The resulting dataset is split into validation and testing. Training data generation involves the same operations as any search parameter optimization; ground-truth neighbors and recall at varying probe depths are needed even to select a fixed nprobe. QASP fits a lightweight model on the collected data.

*2) Model Selection:* We build three variants of pre-trained
QASP models. First,*QASP-DL*is a lightweight deep learning architecture for tabular learning [18] with batch normalization and dropout. Second,*QASP-GBDT*is a gradient boosted decision tree model which is a de-facto architecture for tabular learning tasks due to their ability to handle decision manifolds

effectively [19]. Third,*QASP-LITE*is a polynomial regression model. All variants are trained to optimize mean squared error loss and differ in expressive power, inference latency, ease of integration and adaptability to unseen domains.

*D. Model Invocation* Training QASP models on the recall regression task serves as a surrogate for the search policy during model invocation SectionII-B. Beyond the naive application of QASP to the same data distribution as it is trained on, QASP can be effectively employed at search-time.
*1) Model Inference:* QASP model inference is performed
proactively on the query workload prior to vector search execu- tion. This design allows rich architecture such as deep learning unlike prior work [20] due to workload-level optimizations. Batching for large-scale inference allows easy parallelism and GPU acceleration can yield significant scaling benefits. By processing queries in batches, the approach amortizes computational overhead and sustains high throughput, even as the index partitioning scales to orders of magnitude beyond the size observed during training.

*2) Domain Adaptation:* Recall prediction serves as a foun-
dational training objective for vector search, generalizing effectively across datasets, query distributions, and index configurations. We design features that are normalized and scale-invariant (see SectionIII), which capture fundamental search difficulty signals that transfer across heterogeneous scales and indexing schemes. This enables QASP to adapt to new domains via both zero-shot transfer, where the pre-trained model generalizes to unseen datasets and index configurations without adjustment, and few-shot transfer, with limited train- ing on batch normalization [21] and final projection layers

||||,µ )/d(q,µ|), where||
|---|---|---|---|---|---|
||||l l|π (1)||
|l l|l|π (1)||l|l|

using very few queries from the target domain.

*3) Scaling to Hierarchical Indices:* At invocation time,
QASP can be scaled to large indices without additional training by extending the same feature transformations on hierarchical partitioning. QASP models can effectively be trained once on a smaller flat index and applied across all hierarchy levels. At inference, model features at each level are computed using coresets, with second-level centroids already available from index construction providing a lightweight approximation. This combination enables fast, scalable model invocation across large indices.

*E. Lightweight Reactive Complement* QASP’s fine-grained recall predictions*R₁,...,R*

||enable|||))/d(q,µ|), where|
|---|---|---|---|---|---|
||L|π (1)|π (·)||π (1)|
|i i|i−1|||||
|i||π (L)|π (i) π (L)|L i=1|π (i)|
 real-time validation as search progresses: Each prediction*Ri* represents cumulative recall after searching*i*partitions, mak- ing the incremental contribution *DR* g =*R −R* a testable hypothesis about partition*i*’s value. For example, when QASP predicts that partition*i*will increase recall from 0.89 to 0.94, it asserts that this partition contains approximately0*.*05*k*true nearest neighbors, which can be immediately verified during search. The actual discovery rate*DR* is observed as partition *i*’s contribution to the running result set.
The goal is to detect whether predicted rates *DR* g*i*under- predict or over-predict observed rates*DRi*as search pro- gresses. We adapt a lightweight statistical process control solution using EWMA smoothing: *SDRi*=*α·DRi*+ (1*−α*)*·SDRi−*1to prioritize recent discovery rates. A Shewhart-type run rule detects consistent deviations∆*i*= (*SDRi− DR* g*i*)*/DR* g*i*over consecutive steps. Consistently negative values indicate early termination opportunities, while consistently positive values suggest extending search beyond initial predictions. See SectionVI-Gfor pseudocode.

III. MODELFEATURES Model features are data signals that are informative for recall prediction task and accessible at inference with no additional computation. We define a set of features, with scale- invariant transformations, designed to capture diverse query and index characteristics.

*A. Feature Types*
*√* *Dataset Features. Data Size*:1*/* *d* *n*, where*n*=*|D|*, is the dataset size and*d*is the vector dimensionality. This quantity captures the expected separation (min distance) between*n* points packed in a unit sphere. *Index Features. Rank*:1*−*exp(*−l/L*), where*l*is centroid rank and*L*is total number of centroids. Normalization by*L* ensures rank*∈*(0*,*1*−*1*/e*]for all indices. Exponential decay captures diminishing returns of accessing further clusters. P*l* *Cumulative Cluster Size*:*i*=1*|Cπq* (*i*)*|/|D|*. This represents fraction of vectors read up to a given centroid rank*l*. This feature is especially useful for imbalanced indices. *Cluster Coefficient of Variance*: *σ*(*d*(*vl,µl*))*/µ*(*vl,µl*), where *σ*(*d*(*vl,µl*))is the standard deviation and*µ*(*d*(*vl,µl*))is the mean distance between data vectors*vl∈Cl*and centroid*µl*. *Maximum Cluster Distance*:max(*vl l πq*(1) max(*v ,µ*)is the max distance between data vectors*v ∈C* and centroid*µ* and*d*(*q,µq*)is the distance between query and the centroid of nearest cluster. We also consider other statistical summaries (like*min,p*25*,p*75) over the distance distribution. Normalization with(*q,µπq*(1))is performed at search time. *Query Features. Relative Distance*:tanh(*δ*(*q,l*)*−*1), where *δ*(*q,l*) =*d*(*q,µl*)*/d*(*q,µπq*(1))and*d*(*q,µπq*(1))is the distance from query*q*to its nearest centroid. Query-to-centroid dis- tances are normalized relative to the nearest centroid distance. Hyperbolic tangent compresses distances into bounded ranges and aims to capture diminishing returns of accessing distant clusters. *Local Relative Contrast*: *µ*(*d*(*q,µq q* *d*(*q,µq*)is the distance from query*q*to its nearest centroid and the numerator represents the average distance to all other centroids. This feature is an adaptation of the local relative contrast defined by [22] using centroid vectors. P *Local Intrinsic Dimensionality*:*−k/* [ln*d*(*q,µq*)*−* ln*d*(*q,µq*)], where*d*(*q,µq*)is the distance from query *q*to the*i*th centroid and*d*(*q,µq*)is the distance between *q*and the farthest centroid. It quantifies the difficulty of the query [22] and we adapt it using centroid vectors.

*B. Feature Transformation* The foregoing feature design incorporates various trans- formation (e.g., normalization with respect to*L*or*|D|*, using exponential decay and hyperbolic tangent) to bound feature ranges within fixed intervals, thereby providing a scale- invariant feature representation across varying search config- urations. By expressing features as normalized ratios, they remain meaningful across different vector space distributions, dataset scales or index configurations. Another transformation we consider is*relative difference*or “relative jumps” for any feature, call it*φ*(*q,l*), varying with*l*:
<u>φ(q,l)−φ(q,l−1)</u> ∆(*φ*;*q,l*) =*.* max₁*<j<l*(*φ*(*q,j*)*−φ*(*q,j−*1)

This allows QASP to rely not only on the raw feature value but also on how much the feature value changes as more clusters are probed in order to detect diminishing returns. We pad the output of this transformation with0wherever undefined. We conduct feature analysis and ablations to find the feature set (see SectionVII-C).

### IV. THEORETICALGUARANTEES FORQASP

In this section we analyze QASP’s optimization and connect the structure of the vector index to the provable advantage of QASP. We first show that every fixed policy suffers irreducible loss determined by the variance of query difficulty, and that QASP can be trained nearly optimally with a finite number of samples independent of dataset size and never outperformed by any fixed policy except by a vanishing margin. We then derive a dominance condition proving that QASP’s data access savings grow exponentially in intrinsic dimensionality. Let*Q*be a query distribution overR *d*. Suppose that the given query set*Q*is a sample from*Q*. Let*r* *∗* *∈*[0*,*1]be the recall target. We define the population loss of a probe policy *∗* *g*on*Q*and*r* as

<u>1</u>*∗ ∗ ∗* 2 *L*(*g*) :=E*q∼Q* 2 (*ℓ* (*q,r*)*−g*(*q,r*))*,*(5) *L*

where*ℓ* *∗* (*q,r* *∗* )is the minimum number of clusters in*I*(*D*) that need to be probed to attain recall*r* *∗* for*q*, as per eq. (1). For a finite sample*Q*from*Q*, we define the corresponding ˆ( empirical loss *L g*)as follows. Observe that the probe policy learning problem in eq. (2) minimizes this empirical loss on

*Q*.
<u>1</u> X

|ˆ( L g) :=||(ℓ (q,r )−g(q,r )).||h 1|i|Var(Λ)||
|---|---|---|---|---|---|---|---|
||2||||2|||
||q∈Q|||||||

2 *∗ ∗ ∗* 2 *L |Q|*

*A. Sub-Optimality of Fixed Probe Policies* We first provide a suboptimality bound for the population loss of fixed policies. A fixed policy*g*maps all queries to a fixed number of probes. We denote by*g*
(*l*) the fixed*l*-probe
policy, defined as

*∀q∈*R *d* *, g*

(*l*) (*q,r* *∗* ) =*l.*(6)
We define a distribution over*{,...,L}*from*Q*. LetΛbe a random variable in*{,...,L}*drawn by sampling*q∼Q* and setting *∗ ∗* Λ =*ℓ* (*q,r*)*.*(7)

Thus,Λis the optimal number of clusters that needs to be scanned for a query drawn at random from*Q*, under the recall target*r* *∗*. We can relate the sub-optimality of fixed probe policies to the distribution ofΛas follows.

**Theorem 5.***For everyl∈{*1*,...,L}, the population loss of* *the fixed-probe policyg*

(*l*) *satisfiesL*(*g*
(*l*) )*≥*Var(Λ)*/L .*
2

Thus, the single quantity <u>Var(Λ)</u> is a uniform lower bound *L*2 on the population losses of every fixed probe policy simultane- ously. We can evaluate this quantity — either empirically from the given query workload, or analytically under a distributional query model — to quantify the sub-optimality enforced by restricting the search procedure to fixed-probe policies. *Example—Zipfian probes:* The*ρ*-Zipfian law,Pr[*ℓ*]*∝* 1*/ℓ* *ρ*, is commonly used to model access frequency patterns [23]. For simplicity, we focus on the most standard case *ρ*= 1. Thus, for a partition-based vector index with*L*clusters and a query drawn at random from*Q*, the probability that its optimal number of probes is*ℓ*is proportional to1*/ℓ*. Hence,Λis distributed asPr[Λ = P *ℓ*]=1*/*(*ℓ·HL*), where *L* <u>1</u> *th* *HL*=*i*=1 *i* = Θ(ln*L*)is the*L* harmonic number. A direct calculation yields that

*L*(*L*+ 1) *L² L² L²* Var(Λ) = *−* 2 = Θ = Θ*.* 2*HLHLHL*ln*L*

Hence, by Theorem5, the population loss (5) of every fixed- probe policy is at leastΩ(1*/*ln*L*)*>*0.

*Proof of Theorem5..*We recall the following basic fact:

**Lemma 6.***For every real-valued random variableXwith* E[*X*]*<∞, it holds that*arg min E (*µ−X*) 2 =E[*X*]*.* *µ∈*R

Using this, every fixed probe policy*g*

(*l*) satisfies,
(*l*)<u>1</u>(*l*) *∗ ∗ ∗* 2
*L*(*g*) =E*q∼Q* 2 (*g* (*q,r*)*−ℓ* (*q,r*)) eq. (5) *L*

= 1 E *q∼Q*(*l−ℓ* *∗* (*q,r* *∗* )) 2 eq. (6) *L²* 1*∗ ∗* 2 *≥* min E*q∼Q*(*µ−ℓ* (*q,r*)) *L² µ∈*R h i = 1 E *q∼Q*(E*q∼Q*[*ℓ* *∗* (*q,r* *∗* )]*−ℓ* *∗* (*q,r* *∗* )) 2 *L²* 2 = E (E[Λ]*−*Λ) =*.*eq. ( 7) *L² L²*

*B. QASP versus Fixed Probe Policies* We show that a finite sample of queries*Q*from*Q*suffices to train QASP to better loss than any fixed probe policy with high probability, up to a small gap that vanishes as the sample size grows. Importantly, the requisite sample size is independent of the dataset size*|D|*, and depends only on the number of clusters*L*and on the structure of the QASP model.

We start with some learning-theoretic definitions. The pseudo- dimension characterizes the number of samples required to certify generalization [24]–[28]. We define pseudo-dimension for probe policies as follows:

**Definition 7**(pseudo-dimension of probe policy class)**.***LetG* *be a class of probe policies. LetQ*=*{q₁,...,q}⊂*R*. We*

|||M d|QASP|
|---|---|---|---|
|M ∗|||(l)|
|i d|i|||

*say thatQis*pseudo-shattered*byGif there exist thresholds* *τ₁,...,τ ∈*R*such that for everyI⊂*[*M*]*, there isg∈G* *such thatg*(*q,r*)*> τ ⇔i∈I. The*pseudo-dimension*of* *Gis denoted*pdim(*G*)*and defined as the largest size of a set* *Q⊂*R *pseudo-shattered byG.*

Function classes with finite pseudo-dimension are called *learnable*because their population loss can be approximately optimized from a finite sample. Specifically, the pseudo- dimension governs the sample size required to guarantee that the empirical loss approximates the population loss for every probe policy in the class, a property known as*uniform* *convergence*[29].

**Theorem 8**( [30], Theorem 19.2)**.***Letε,η∈*(0*,*1)*. LetQbe* *a sample fromQof sizeO*((pdim(*G*) + log(1*/η*))*/ε²*)*. Then,* h i Pr *∀g∈G*:*|L*(*g*)*− L*ˆ(*g*)*|< ε ≥*1*−η.*

The pseudo-dimension can be bounded using the dimension of the parameter space and the complexity of the learned model, as per the following theorem, which is a specialization of Theorem 8 from [31] (based on [32], [33]) to probe policies.

**Theorem 9.***LetG*=*{gθ*: *θ∈*Θ*}be a class of probe policies* *parameterized by anm-dimensional parameter space*Θ*. Let* *F*(*q*)*be any set of numerical features representing a queryq∈* R *d* *. Suppose that for everyθ∈*Θ*andq∈*R *d* *, it is possible to* *∗* *computegθ*(*q,r*)*fromθandF*(*q*)*with an algorithm that can* *perform arithmetic operations{*+*,−,×,÷}and numerical* *comparisons{*=*,̸*=*,>,≥,<,≤}. Suppose the algorithm has* *running timet. Then,*pdim(*G*) =*O*(*mt*)*. Furthermore, if the* *algorithm is also allowed to perform exponentiation (x7→e* *x* *),* 2 *then*pdim(*G*) =*O*((*mt*))*.*

We show that our implicit ML-based search policy, where probe decisions are induced through recall predictions can be analyzed through bounded pseudo-dimension theory. We prove that QASP’s compositionally-defined policy class has finite pseudo-dimension despite complex interactions between neural network recall predictors, query features, and the min- imization operation that determines optimal probe counts.

**Lemma 10.***The pseudo-dimension*pdim(*G*QASP)*of all three* *QASP variants is finite. Furthermore, it depends only onL,* *and is independent of the dataset sizenand the dimensionality*

*d.* *Proof.*Invoke Theorem9. By SectionIII, the number of features*|F*(*q*)*|*per query*q*is*O*(*L*), hence so is the number of trainable parameters (i.e., the dimension of the param- eter space) per QASP model. By SectionII-C2, all three QASP architectures can be computed from*F*(*q*)using only
arithmetic operations and numerical comparisons, and (in the case of QASP-DL) exponentiations (in order to compute sigmoid activations). Therefore, the proposition follows from Theorem9.

**Theorem 11.***Letε,η∈*(0*,*1)*. Suppose the sampleQhas size* *O*(pdim(*G*QASP)*/ε²*+log(1*/η*))*. Letg be the policy that* *minimizes eq. (2). Then, with probability*1*−η, it holds that*

*∀l∈*[*L*]*,L*(*g*)*≤L*(*g*) + 2*ε.*(8) QASP

*Note that both the failure probabilityηand the performance* *gap*2*εvanish as we increase the sample size|Q|.*

*Proof.*With Lemma10, we can proof Theorem11. Since ˆ *g* QASPminimizes the empirical loss *L*, we have,

*∀l∈*[*L*]*, L*ˆ(*g*QASP)*≤ L*ˆ(*g*

(*l*)
)*.*(9)
By definition, the learned policy*g*QASPis realizable in the QASP model, meaning*g*QASP*∈ G*QASP. Furthermore, all fixed-probe policies*g*

(*l*) are realizable in the QASP model.
Therefore, by Lemma10and Theorem8, we have with probability1*−η*,

*|L*(*g*QASP)*− L*ˆ(*g*QASP)*|< ε*and*∀l,|L*(*g*

(*l*) )*− L*ˆ(*g*
(*l*) )*|< ε.*
Together with eq. (9), with probability1*−η*, eq. (8) follows.

*Remark.*The same conclusion as Theorem11holds if we define the empirical loss with eq. (4) instead of eq. (2) and the appropriate analogous population loss (replacingΣ*q∈Q* withE in eq. (4)). The formal proof goes by augment- *q∼Q* ing the feature set*F*(*q*)with the additional query features *{R* (*q,l*)*}* *L*, which enables computing the contribution *I*(*D*) *l*=1 of*q*to the loss from*F*(*q*)while maintaining the size bound *|F*(*q*)*|*=*O*(*L*). We omit further details. In SectionIV-Awe establish that fixed policies inherently leave room for loss improvement. Proposition10allows us to complement this result and prove that even in the worst case, with high probability, QASP’s loss is never*worse*than any fixed policy, except by a negligible margin that tends to zero as the sample size grows.

*C. Cost Dominance of Adaptive Probing* SectionIV-Aand SectionIV-Bestablish that QASP gener- alizes from finite samples and that fixed policies are inherently sub-optimal in loss. We now ask a complementary question: *how much data access does QASP save*, and under what conditions does it dominate fixed probing despite predictor imperfection? Fixed policies must provision for the tail of the query difficulty distribution, forcing every query, including easy ones, to pay the cost of the hardest queries. QASP instead pays what each query individually requires. We formalize this intuition and derive the precise conditions under which QASP dominates, connecting the geometry of the vector index to the quality of the learned predictor, with the gap growing exponentially in the intrinsic dimensionality of the data.

We introduce three quantities characterizing the index. Let *DI*= max*j*max*x∈Cj∥x−µj∥*be the maximum cluster radius,*σI*= min*j̸*=*j′ ∥µj−µj′ ∥*the minimum inter-centroid separation, and∆the doubling dimension 1 of the dataset union centroids. Write*r*(*q*) =*∥q−x* *∗*

(*q*)*∥*for the nearest-
neighbor distance of query*q*,*Fr*for its CDF over*Q*, and *r* *δ*=*Fr−* 1 (1*−δ*)for the(1*−δ*)-quantile.

**Lemma 12**(Cell Intersection Bound)**.***ℓ* *∗* (*q,*1)*≤* ∆ 4(*r*(*q*) +*DI*)*/σI.*

*Proof.*Let*j* *∗* be the cluster containing*x* *∗*

(*q*). By the triangle
inequality,*∥q−µj∗ ∥≤r*(*q*) +*DI*, so*µj∗ ∈B*(*q,r*(*q*) +*DI*). Every centroid ranked before*µj∗* also lies in this ball, so *ℓ* *∗* (*q,*1)is at most the number of centroids in*B*(*q,r*(*q*)+*DI*). Since centroids are pairwise separated by*≥σI*, the balls *{B*(*µj,σI/*2)*}*are disjoint and contained in*B*(*q,r*(*q*) +*DI*+ *σI/*2). By the doubling-dimension packing property [34], a ball of radius*R*contains at most(2*R/ρ*) ∆ points with pairwise distance*≥ρ*. Setting*R*=*r*(*q*) +*DI*+*σI/*2 and*ρ*=*σI*gives*ℓ* *∗* (*q,*1)*≤*(2(*r*(*q*) +*DI*)*/σI*+ 1) ∆ *≤* (4(*r*(*q*) +*DI*)*/σI*) ∆ when*r*(*q*) +*DI≥σI/*2.

The ratio(*r*(*q*) +*DI*)*/σI*captures geometric query diffi- culty: queries far from their nearest neighbor or in poorly sep- arated partitions require more probes. This bound is tight up to constants: by definition of doubling dimension, there exist point configurations whereΘ((*R/ρ*) ∆ )points with pairwise separation*≥ρ*fit in a ball of radius*R*[34], so the upper bound is achievable. Note that*ℓ* *∗* (*q,*1)bounds the probes needed to retrieve the single nearest neighbor; for*k*-NN recall at target *r* *∗*, the bound is conservative since achieving partial recall is strictly easier.

**Proposition 13**(Fixed Probe Requirement)**.***A fixed-ℓpolicy* *achieves recall≥*1*−δwhen* ∆ <u>4(rδ+DI)</u> *ℓ≥ℓ*fix(*δ*) :=*.*(10) *σI* <u>σ</u> <u>I</u> 1*/*∆ *∗* *Proof.*By Lemma12,*r*(*q*)*≤* 4 *ℓ −DI*implies*ℓ* (*q,*1)*≤* *ℓ*. Setting this threshold*≥rδ*gives (10).

This is the cost every query pays under fixed probing — including easy queries with*r*(*q*)*≪rδ*that would succeed with far fewer probes. We now bound what QASP pays instead. Let *ℓ* ˆ(*q*) =*g* QASP(*q,r* *∗* )be QASP’s predicted probe count. Define the*failure rateε*= Pr[*ℓ*ˆ(*q*)*< ℓ* *∗* (*q,r* *∗* )]and the*overshoot* ¯= *η* E[*ℓ*ˆ(*q*)*−ℓ* *∗* (*q,r* *∗* )*| ℓ*ˆ(*q*)*≥ℓ* *∗* (*q,r* *∗* )]. The failure rate*ε*is the probability QASP under-probes (missing the recall target); the overshoot¯is the average wasted probes when it succeeds. *η*

**Proposition 14**(QASP Expected Probes)**.**E[*ℓ*ˆ(*q*)]*≤*E[Λ] + ¯+*η ε·L.*

*Proof.*Condition on success (*ℓ*ˆ*≥ℓ* *∗* ) and failure (*ℓ < ℓ* ˆ *∗* ): E[*ℓ*ˆ] = (1*−ε*)(E[*ℓ* *∗* *|*success] + ¯) + *η ε*E[*ℓ*ˆ*|*failure]. Since

The smallest integer such that every ball of radius*r*is covered by2∆ balls of radius*r/*2.

Fig. 2: Expected probes vs. recall target for fixed probing

(black) and QASP (gray) under three NN distance distributions (∆ = 5,*L*= 1000,¯= *η* 2,*ε*=*δ*). The vertical gap between matched curves is the data access savings from adaptive probing. QASP benefits most when*Fr*has a heavy tail (exponential, uniform) and at high recall targets, where fixed probing must provision for the worst-case quantile*rδ*.

(1*−ε*)E[*ℓ* *∗* *|*success]*≤*E[Λ],(1*−ε*)¯*≤ η* ¯,*η* andE[*ℓ*ˆ*|* failure]*≤L*(a worst-case bound; in practice failure queries cost far less than*L*probes), the bound follows.

**Corollary 15**(Dominance Condition)**.***At matched recall (ε*= *δ), QASP has strictly lower expected data access than fixed* *probing whenever*

<u>4(r +D)</u> ∆ <u>δ I</u> ¯<u>+η</u> *ε*<u>·</u>*L < −*E[Λ]*.*(11) | {z} <u>σI</u> *predictor overhead*| {z} *tail waste of fixed probing*

Combining Propositions13and14yields the main result. The left side is the total cost of predictor imperfection: wasted probes from over-prediction (¯) plus the penalty from under-*η* prediction failures (*εL*). The right side is the*tail waste*: the gap between the fixed probe count (driven by the hardest queries via*rδ*) and the average difficultyE[Λ]. This gap grows as the ∆-th power of the ratio between worst-case and average query difficulty. QASP dominates whenever the predictor is “good enough” relative to this heterogeneity; conversely, when*Fr*is concentrated, all queries are equally hard and adaptive probing offers no advantage. Figure2illustrates the dominance con- dition under three NN distance distributions: the gap between fixed and QASP curves at any recall target represents data access savings, largest for heavy-tailed distributions at high recall and vanishing for concentrated distributions. Note that we do not model*εL*and¯as functions of the recall target, *η* which in practice influences predictor performance.

V. RELATEDWORK
QASP targets partitioning-based indexing, the most com- prehensive class of vector search methods, which partition the space for pruning and scale to distributed architectures.

These include clustering and IVF (Inverted File Index) [5], [9]–[12], multi-dimensional space trees [34]–[37], and vector quantization [10], [11], [38] which uses clustering at its core. Partitioning-based indices achieve sublinear scaling [8], mak- ing them the preferred choice for large vector databases due to their parallelizability and resource efficiency. Partitioning also underpins distributed search architectures to distribute vectors across storage units or processors [13]–[16]. Vector search libraries predominantly relied on static em- pirical parameter settings and target average recall without adapting to query difficulty. These include defaulting to nprobe = 8 (number of clusters to search), recommending proportional scaling with nlist (total number of clusters) and experimental tuning [39]; setting nprobe to cover 5–10% of the dataset [ *√ √* 1]; setting nlist based on dataset size (4*· N*to16*· N*) with limited nprobe guidance [2] and testing multiple values (1, 4, 16, 64, 256) [40]. SPANN [12] and SQUASH [16] use thresholds to decide which clusters to search. Popular graph-based methods [41] constrain the candidate list size at query time, traditionally fixed for all queries. Recent methods [4], [20], [42] set this parameter per query through either statistical scoring or reactive early termination. Statistical scoring offers lightweight runtime adaptation but requires distributional assumptions that may not hold across diverse workloads. Reactive early termination provides flex- ible stopping criteria but periodically invokes models during traversal, introducing per-step inference overhead that limits model capacity. These methods target graph indices. For IVF indices, PCE-Net [43] predicts a single nprobe per query, coupling the prediction to a specific recall target and resulting in higher variance and data access (SectionVI-D). QASP instead learns fine-grained recall contributions over partitions proactively through a single upfront inference. This enables richer architectures and generalization across recall targets, with significant improvements also demonstrated experimen- tally.

VI. PERFORMANCEEVALUATION

*A. Experimental Setup* All experiments are performed on*Intel(R) Xeon(R) Plat-* *inum 8175M CPU @ 2.50GHz & 96 CPU cores*. We use Python 3.10 with Pytorch 1.13 for deep-learning and scikit- learn 1.2.2 for gradient boosting, regression and kmeans++.
*1) Vector Datasets:* We build QASP on seven datasets from
a range of vector spaces, distance measures and application domains. SIFT1M [44], 1 million 128-dimensional SIFT im- age descriptors; MNIST [45], 60k 784-dimensional vectors trained on handwritten digits; GIST1M [46], 1 million 960- dimensional global color GIST descriptors. DEEP1B 10M, 10 million subset of Deep1B [47] with 96-dimensional deep learning embeddings; GLOVE-200 [48], 1.2 million 200- dimensional word embeddings trained on Wikipedia; COCO- I2I [49], 113k 512-dimensional vectors for image-to-image retrieval; COCO-T2I [49], 113k 512-dimension vectors for text-to-image retrieval. Each dataset has a*QuerySet*with 100true neighbors from exact search.

*2) Training, Validation and Test Sets:* We use a random
sample ofmin(1000*,⌊|QuerySet|/ ⌋*)queries for gener- ating offline training and validation sets. Model features, as discussed in sectionIII, are obtained per query and centroid rank by searching up tomin(300*,⌊*0*.*3*L⌋*)probes. Ground truth is used to obtain recall target labels. The offline dataset is split 80:20 for training and validation. For testing,1000queries are sampled from the remaining query set and features are obtained on-the-fly during search. See SectionVIIfor model performance and fit analysis.

*3) Model Details:* Deep Learning (DL) neural architecture
of QASP, called QASP-DL, contains 3 hidden layers with hidden dimension of 18 with ReLU activation [50]. Each input feature is projected on a 4-dim learnable embeddings space following tabular learning using DL [18]. We use batch normalization on input embeddings and dropout with rate 0.1 for regularization. Each DL model is trained for 100 epochs with a constant learning rate of 5e-3 and batch size of 512, though convergence is observed much earlier. The best model is selected using held-out validation set performance. Gradient boosting decision tree (GBDT) model variant of QASP, called QASP-GBDT, is trained using 100 trees with a maximum depth of 3 and a learning rate of 0.1. Polynomial variant of QASP, called QASP-LITE, is a lightweight and easy to adopt alternative in production environment, is fitted using Lasso regression with*α*=1e-5 on sklearnPolynomialFeatures processing with degree 3. *Latency and Throughput*- The DL model has a modest parameter count of1513trainable parameters and a total memory footprint of just 6-7 KB, making it practical for deployment even in memory-constrained environments. For DL model, mean latency on CPU with batch size 32 is 0.26 ms/batch, throughput 124K queries/sec and P99 latency 0.33 ms using 4 threads. For GBDT, mean latency on CPU with batch size 32 is 0.199 ms/batch, throughput 161K queries/sec and P99 latency 0.55 ms. For QASP-LITE, mean latency on CPU with batch size 32 is 0.06 ms/batch, throughput 524K queries/sec and P99 latency 0.09 ms. All measurement is over 100 runs with 10 warm-up iterations.

*4) Index Details:* We first build flat IVF indices with
*√* nlist as*scalar× n*where*n*is the base size and use three*scalar*values[0*.*5*,*1*,*4]to span across different index configurations per dataset. Distance metrics is either Squared Euclidean or Cosine Distance depending on the dataset and the clustering algorithm used is k-means++ [51]. We also build a hierarchical index using two-level kmeans clustering for scaling experiments to larger datasets of size (*>*10*MM*). *√* 3 Each level of the index is clustered using fixed nlist as *n*that gives equal sized partitions ideal for disk-based experiments.

*B. Query Variability-Aware Evaluation* The traditional method for evaluating vector similarity search results is to measure the deviation of observed aver- age recallPfrom recall target. Given observed average recall, ¯= *r* *|Q| q∈Q*
*r*(*q*), where*r*(*q*)is the observed recall for query*q*and recall target*r* *∗*, traditional evaluation concerns

TABLE I: Comparison of QASP-DL and Oracle Nprobe policy across three recall targets. Oracle Nprobe achieves recall target by over-reading in the 50% Easy split and under-reading in the 50% Hard split, while QASP optimizes search on both splits. *∗* We highlight¯with large deviation from *r r* in red otherwise in teal, while best average QVE metrics are emboldened when *∗* ¯*≈r r*. These results empirically validate Corollary15where*A*%improvements are better at higher recall targets. *∗* *∗ ∗*

|Dataset|Search Policy||r =90%r||||=95%r||||=99%||
|---|---|---|---|---|---|---|---|---|---|---|---|---|
|||¯r|↓δ↓S%↑A%↓|||¯r|σ ↓δ↓S%↑A%↓|||¯r|σ ↓δ↓S%↑A%↓||
|AVERAGE|Oracle Nprobe|89.87142.71|9.39|72.613.92||94.9353.12|5.32|80.89|7.08|98.934.491.21||95.8518.64|
||QASP-DL|90.9760.37|6.23|79.953.98||95.1225.62|3.80|85.17|6.02|98.604.191.26||95.0712.23|
|50% EASY|Oracle Nprobe|96.5725.79|7.89|94.51|4.11|98.636.35|4.23|97.37|7.35|99.660.50|0.85|99.71 19.06|
||QASP-DL|91.6163.97|6.68|81.06|1.83|95.4129.15|4.07|85.66|2.71|98.744.23|1.19|95.54 6.56|
|50% HARD|Oracle Nprobe|83.26167.28|10.82|51.77|3.75|91.3171.26|6.38|64.83|6.82|98.276.73|1.53|92.29 18.24|
||QASP-DL|90.4952.06|5.71|79.37|6.03|94.8420.25|3.50|84.83|9.17|98.463.49|1.27|94.74 17.82|

2 2 2 *σ*

only with*|*¯*−r r* *∗* *|*. While useful as a summary statistic, it masks performance variations across queries and fails to capture user experience consistency. To address this shortcoming, we propose a comprehensive Query Variability-aware Evaluation (QVE) framework with the following metrics to compare query variability even when¯*≈r r* *∗* between search policies. 2 <u>1</u> P 2 *•***Recall Variance**: *σ* = *|Q| q∈Q* (*r*(*q*)*−*¯)*r*- Measures variance of the observed recall across test queries. <u>1</u> P *∗* *•***Absolute Query Deviation**: *δ*= *|Q| q∈Q* *|r*(*q*)*−r |*- Measures mean of absolute deviation from recall target. <u>|{q∈Q: r(q)≥r</u> *∗* <u>}|</u> *•***Query Satisfaction Rate**: *S*% = 100*×* *|Q|* - % of queries satisfied by the search policy, i.e. achieve at least recall*r* *∗*. Since exact*r* *∗* per query is rarely useful, we subtract a small margin (5%) from*r* *∗* to relax the criteria. <u>100</u> P *•***% Data Accessed**: *A*% = *|Q×D| q∈Q* *|{v∈D*: *d*(*v,q*)is calculated*}|*, % of data accessed.

*C. QASP versus Oracle Fixed Policy* We first compare QASP to policies that search a fixed number of probes, which are industry standard where sev- eral open source libraries like Faiss [2], Milvus [39], and OpenSearch [3] recommend tuningnprobeparameter for IVF for a given dataset and query workload. To simplify comparison, we obtain the best fixed policy, called Oracle Nprobe, which is the smallestnprobethat results in¯*≈r r*
*∗*. The Oracle Nprobe policy represents a theoretical upper bound of what fixed policies can achieve and thus is a strong baseline to QASP. We obtain Oracle Nprobe from the same training dataset used for training QASP models. See TableIcontains comparison results averaged across the seven datasets. Both Oracle Nprobe and QASP achieve similar¯’s*r* close to the target. However, QASP consistently outperforms Oracle Nprobe on QVE metrics achieving57*.*7%lower*σ²* and33*.*7% lower*δ*, while satisfying7*.*3%more queries and accessing just0*.*06%more data for*r* *∗* = 90%. As*r* *∗* increases, QASP accesses much fewer data than Oracle Nprobe to achieve the same recall without lowering satisfaction rate. To further understand this behavior, we split the test dataset into two halves -*50% EASY*and*50% HARD*, using Local Relative Contrast feature. We observe that Oracle Nprobe consistently over-reads in the*50% EASY*set and under-reads in the*50%* *HARD*set. QASP, being query adaptive, does the opposite by

reading less in the*50% EASY*set and more in the*50% HARD* set as intended.

*D. Baselines* We extend our comparison to proactive baselines from popular vector search libraries and prior work. Several libraries recommend tuningnprobeparameter for IVF [2], [3], [39] for which we use Oracle Nprobe. LanceDB [1] suggests searching for a fixed % of vectors for which we obtain Oracle Access % from training dataset. SPANN [12] is a popular clustering index with query-aware pruning that searches until cluster rank*j*such that*Dist*(*q,cj*)*≤*(1 +*ϵ*)*×Dist*(*q,c₁*). SQUASH [16] also involves a scalar multiple on distance to create a search mask. We obtain Oracle Distance Multiplier to represent these methods. Vexless [14] uses a threshold on absolute distance, for which we derive Oracle Distance. PCE- Net [43] is a learned baseline that predicts a single nprobe per query using neural encoders over the query vector and centroid distance distribution; we evaluate them on the same IVF index for a fair comparison of the probing approaches. TableIIcontains comparative results across the seven datasets. First, we observe that all the oracle baselines can be tuned to achieve¯*≈r r*
*∗* except Oracle Distance [14]. PCE- Net achieves high recall but at a steep cost: it reads 14.8% of data—more than twice QASP-DL’s 6.0%—as its asymmetric loss incentivizes over-probing. Its variance (*σ²* = 69*.*8) and deviation (*δ*= 5*.*6) also exceed all QASP variants. QASP consistently outperforms all baselines on QVE metrics while achieving recall target, satisfying more queries and accessing fewer vectors. We split test queries into easy and hard. We observe that fixed policies like Oracle Nprobe and Oracle Access% over-read by 4.3% for easy queries and under- read by 2.3% for hard queries. Oracle Distance Multiplier is more adaptive; reading less in easy queries and more in hard queries. However, when compared to QASP models this policy had 176% higher variance. PCE-Net [43], which predicts per query nprobe, exhibits an inverted pattern: it over-reads on hard queries (¯= *r* 97*.*7) and under-reads on easy queries (¯= 93 *r.*5). PCE-Net achieves recall target at higher variance and deviation compared to fixed policies like Oracle Nprobe and Oracle Access%. Moreover, while it achieves a higher*S*% than QASP, it achieves so by accessing*≈. ×*more than QASP-DL with*A*% = 14*.*78, highest among all methods.

TABLE II: Comparison of QASP to proactive baselines at recall target 95%. QASP outperforms Oracle policies averaged over seven datasets. QASP-DL outperforms other variants. <u>r</u> *∗* <u>=95%</u> Dataset Search Policy ¯*r σ*2*↓δ↓S*%*↑A*%*↓* AVERAGE Oracle Nprobe [2], [3], [39] 94.9053.57 5.34 80.72 7.08 Oracle Access % [1] 94.8453.16 5.30 80.14 6.90 Oracle Distance Multiplier [12], [16] 94.6070.72 5.32 82.83 9.21 Oracle Distance [14] 92.40302.94 9.07 82.13 14.69 PCE-Net [43] 95.6369.76 5.55**87.09**14.78 50% EASY Oracle Nprobe [2], [3], [39] 98.636.35 4.23 97.37 7.35 Oracle Access % [1] 98.338.67 4.21 96.14 6.89 Oracle Distance Multiplier [12], [16] 92.50104.25 6.52 74.66 2.56 Oracle Distance [14] 98.7028.50 4.96 97.11 17.27 PCE-Net [43] 93.4988.92 5.99 79.69 15.22 50% HARD Oracle Nprobe [2], [3], [39] 91.3171.26 6.38 64.83 6.82 Oracle Access % [1] 91.3673.15 6.42 64.26 6.90 Oracle Distance Multiplier [12], [16] 96.7027.53 4.20 91.46 15.53 Oracle Distance [14] 86.29482.88 12.99 67.34 12.09 PCE-Net [43] 97.6950.60 5.11 94.49 14.33 AVERAGE QASP-DL 95.12**25.62 3.80**85.17**6.02** QASP-GBDT 95.0927.51 3.89 84.95 6.31 QASP-LITE 95.4334.95 4.16 86.58 7.33 50% EASY QASP-DL 95.4129.15 4.07 85.66 2.71 QASP-GBDT 95.5128.92 4.08 86.49 2.68 QASP-LITE 95.0044.46 4.68 83.54 3.17 50% HARD QASP-DL 94.8420.25 3.50 84.83 9.17 QASP-GBDT 94.6725.13 3.71 83.23 9.90 QASP-LITE 95.8920.97 3.57 89.49 11.46

*E. Deployment Efficiency* Figure3evaluates QASP’s deployment efficiency in both in-memory and disk-based scenarios. We also include Oracle Nprobe which yields the most competitive latency and recall variance among all baselines (though still much higher than

|Source|Target|Zero-Shot||Few-Shot||Fully Trained||
|---|---|---|---|---|---|---|---|
|||¯r|δ↓|¯r|δ↓|¯r|δ↓|
|GIST1M|SIFT1M|98.60|4.01|93.70|4.23|95.47|3.44|
|MNIST|GIST1M|95.50|3.97|92.00|5.09|92.30|4.56|
|SIFT1M|GIST1M|26.80|68.22|92.90|4.36|92.30|4.56|
|SIFT1M + MNIST|GIST1M|93.70|4.57|94.60|3.87|92.30|4.56|
|COCOI2I|GLOVE200|93.10|5.52|94.90|3.84|95.23|3.46|
|GLOVE200|COCOI2I|91.80|6.30|96.80|3.63|95.83|3.98|
|AVERAGE-||83.25|15.76|94.15|4.17|93.91|4.09|
 QASP, cf. TableI). For in-memory deployment, we measure total runtime (milliseconds) required to satisfy95%of queries. QASP involves a single inference plus search time, while Oracle Nprobe only incurs search time. QASP-DL’s marginal inference overhead (*∼*1.5 ms/query) becomes proportionally smaller at higher recall targets and with larger datasets, as search time increases while inference time remains constant. We observe diminishing recall returns at higher recalls with Oracle Nprobe compared to QASP models, eventually offset- ting inference cost. QASP-DL achieves significant gains for larger datasets (*>*10M) where the fixed inference cost is offset by more efficient search, as also shown in SectionVI-H. For disk-based settings, QASP’s benefits are even more pronounced as I/O costs dominate search time. The single inference becomes negligible compared to I/O costs, and
QASP directly reduces disk operations. QASP variants con- sistently read 20-40% less data than Oracle Nprobe across all recall levels, with this efficiency gap widening as recall targets increase (Figure3). This behavior is supported by the theoretical dominance condition illustrated in Figure2.

*F. Domain Adaptation*
*1) Cross-Dataset Generalization:* We evaluate QASP’s
generalization to unseen datasets using two QVE metrics (¯*r* and*δ*) under two transfer settings: zero-shot (direct applica- tion) and few-shot (fine-tuning with1%of target data; see Sec- tionII-D2). As shown in TableIII, QASP-DL often generalizes well zero-shot—e.g., GIST1M*→*SIFT1M achieves¯= 98 *r.*60 without tuning. Where gaps exist (e.g., SIFT1M*→*GIST1M), few-shot fine-tuning with minimal data closes them effectively. Training on diverse sources further helps: a model trained on SIFT1M+MNIST combined outperforms individual models on GIST1M in the zero-shot setting.

TABLE III: Cross-dataset generalization of QASP for recall target 95%. QASP-DL models generalize well under zero- shot and achieve recall close to target, while few-shot training bridges the gap on average with fully trained. QASP models can be fine-tuned with just 1% queries from target domain.

|Dataset|Source Config|Target Config|Zero-Shot|Fully Trained||
|---|---|---|---|---|---|
||||¯r δ↓|¯r|δ↓|
|SIFT1M|IVF(L=1000)|IVF(L=4000)|85.00 10.83|93.50|4.08|
|SIFT1M|IVF(L=4000)|IVF(L=1000)|96.30 3.30|95.47|3.44|
|GIST1M|IVF(L=1000)|IVF(L=4000)|91.50 5.17|91.40|5.17|
|GIST1M|IVF(L=4000)|IVF(L=1000)|92.30 4.56|92.30|4.56|
|COCOI2I|IVF(L=336)|IVF(L=1346)|87.80 9.28|95.10|4.08|
|COCOI2I|IVF(L=1346)|IVF(L=336)|97.20 3.74|95.83|3.98|
|GLOVE200|IVF(L=1087)|IVF(L=4531)|94.70 3.79|94.70|3.79|
|GLOVE200|IVF(L=4531)|IVF(L=1087)|95.10 3.59|95.23|3.46|
|AVERAGE-||-|93.84 4.78|94.29|4.07|

(a) In-Memory (b) Disk-Based
Fig. 3: Search time (ms) vs. recall (in-memory) and data

accessed vs. recall (disk-based). QASP achieves recall target with less search cost than Oracle Nprobe and PCE-Net, with gains further widening at higher recall targets. Legend:QASP- DL,QASP-GBDT,QASP-LITE,Oracle Nprobe,PCE-Net

*2) Cross-Index Configuration Generalization:* We investi-
gate the robustness of QASP models to varying index con- figurations by testing how well they perform on the same dataset but with a different number of clusters*L*. As observed in TableIV, QASP-DL models generalize well on unseen index configurations without fine-tuning. Domain adaptation methods remain applicable where few-shot learning can bridge the gap. However, zero-shot application of QASP models to unseen indices produces competitive performance on average.

TABLE IV: Cross-index generalization of QASP on QVE metrics for recall target = 95%. QASP models trained on one index configuration (source) generalize well zero-shot to unseen configurations (target) reducing the need of fine-tuning.

*G. Reactive Complement* We evaluate the performance of QASP’s reactive comple- ment described in SectionII-E, which guides policy behavior at search. See Algorithm1for the psuedocode of the reactive complement policy based on observed discovery rates. The im- plementation parameters include a smoothing factor*α*= 0*.*3, *Lδ*= 3and a threshold of 0.25 on*δi*to capture positive and negative rates. For baselines, we use LAET [4] which pauses search at a fixed nprobe and predicts when to stop and DARTH [20] which predicts recall at regular intervals to terminate the search early. We tune LAET’s*multiplier* parameter to attain recall target of 95%. For DARTH, we set*mpi*and*ipi*parameters using recommended defaults from training statistics. For a fair comparison, we train DARTH models for*k*= 100and test on unseen queries and search parameters. TableVshows results when all mechanisms are applied on the same IVF index. Both QASP and QASP + Reactive consistently outperform LAET and DARTH on all three datasets with QASP + Reactive further boosting QASP performance. TABLE V: Comparison of QASP to reactive baselines at recall target 95%. QASP outperforms both baselines and reactive complement improves QVE metrics at higher average recall.
<u>r</u> *∗*<u>=95%</u> Dataset Search Policy

|||||||c|←c|+ 1,c|←0▷Negative discovery||
|---|---|---|---|---|---|---|---|---|---|---|
|||¯r|σ ↓δ↓S%↑A%↓|||18:|p||||
|SIFT1M|LAET [4]|95.44|78.74 5.59|86.2|4.14||+ +|−|||
||DARTH [20]|94.20|29.45 4.13|79.5|3.19|19:|||||
||QASP-DL|95.47|19.64 3.44|87.77|2.76|20:|||||
||QASP + Reactive|95.78|17.23 3.36|89.97|2.83||− +||||
|GIST1M|LAET [4]|94.91|117.41 5.54|86.5|10.42|21:|||||
||DARTH [20]|91.94|47.14 5.51|65.7|9.39|22:|||||
||QASP-DL QASP + Reactive|92.30 94.61|34.57 4.56 24.85 3.85|68.50 80.6|6.12 7.64|23:|− δ|p|||
|DEEP1B 10M|LAET [4]|94.83|42.98 4.86|80.53|0.87|24:|||||
||DARTH [20]|95.81|27.15 4.23|85.8|1.35||||||
||QASP-DL QASP + Reactive|95.20 95.83|27.20 3.84 20.91 3.64|85.47 87.97|0.91 0.94|25: 26:||−|+||
|AVERAGE|LAET [4]|95.0679.71|5.33|84.41|5.23|27:|||||
||DARTH [20]|93.9834.58|4.62|77.00|4.64||||||
||QASP-DL QASP + Reactive|94.3227.14 95.4121.00|3.95 3.62|80.583.26 86.183.80||28: 29:|prev p||||
|||||||30: 31:|p||||

¯*r σ*2*↓δ↓S*%*↑A*%*↓*

**Algorithm 1**Reactive Adaptive Search for a Single Query **Require:** Query*q*, nearest cluster ordering *∗* *Cq*, planned probes *P*, recall target*r* *|Cq |* **Require:** Recall estimates*{*ˆ*ir}i*=1from QASP model **Require:** Constants: *ϵ*(margin of error),*δ*(deviation thresh- old),*α*(smoothing factor),*Lδ*(consecutive deviation limit) **Ensure:** Top-*k*results and actual probes used 1: *P*min*←*max(1*,⌊P*(1*−ϵ*)*⌋−Lδ*) 2: *P*max*←*min(*|Cq|,⌈P*(1 +*ϵ*)*⌉−Lδ*) 3: Initialize smoothed discovery rate *−* + *SDR←*0 4: Initialize counters*c ←*0,*c ←*0 5: Initialize previous neighbors set*R*prev*←∅* 6: **for***p*=*P*min**to***P*max**do** *p* 7: *Rp←*SEARCHONECLUSTER(*q,Cq,R*prev) 8: **if***p*=*P*min**then***▷*Skip comparison for first probe 9: *R*prev*←Rp* 10: **continue** 11: **end if** 12: DR*p←|Rp\R*prev*|/k ▷*True discovery rate 13: DR f*p←*max(1*e* *−*3 *,*ˆ*pr −*ˆ*pr−*1)*▷*Estimated discovery rate 14: *SDR←α·*DR*p*+ (1*−α*)*·SDR* 15:∆*p←*(*SDR−* DR f*p*)*/*DR f*p* 16: **if**∆*p* *−* *<−δ* *−* **then** + 17: 18: **else if**∆*p> δ***then** *c ←c* + 1,*c ←*0*▷*Positive discovery **else** *c,c ←*0 **end if** **if***c ≥L* **and**ˆ*r ≥r∗*(1*−ϵ*)**then** **break***▷*Over-search detected **end if** **if***p*=*P***and***c* = 0**and***c* = 0**then** **break***▷*Consistent with estimation **end if** *R ←R* **end for** **return***R*

*H. Scaling to Hierarchical Index* We evaluate hierarchical scaling (SectionII-D3) by applying a QASP-DL model trained on Deep1B-10M to larger subsets of both SIFT1B and Deep1B (10M–100M). For each subset, we *√* construct a two-level index withnlist1=nlist2 = 3 *n*, yielding balanced partitions suitable for disk-based search. We compare against*Oracle Nprobe*, which optimizes nprobe1via binary search withnprobe2=nlist2. QASP operates level-wise, predicting adaptivenprobe1from first- level features and selectively probing second-level partitions based on predicted recall contribution. As shown in Figure4, this reduces data access by*≥*80% at 99% recall consistently across both datasets (SIFT1B: 82–87%, Deep1B: 80–84%), demonstrating that QASP’s efficiency gains generalize across data distributions and scale without retraining.
### VII. REGRESSIONFITANALYSIS

*A. Training Error Analysis* Figure5presents training error curves for three diverse datasets. All models converge rapidly, with most error re- duction occurring within the first 20–30 epochs. Training and validation curves follow similar trajectories with minimal gaps, indicating good generalization without overfitting. Dataset- specific differences in convergence speed and final error levels reflect the varying complexity of the recall prediction task. Overall, QASP trains efficiently across diverse datasets, en- abling rapid adaptation to new index configurations and query distributions in practice.

TABLE VI: Comparison of model fit across all feature abla- tions for Euclidean and Angular datasets on validation set.

|Feature Set|Euclidean Dataset||Angular Dataset||
|---|---|---|---|---|
||MSE↓R|↑|MSE↓R|↑|
|ALL|0.00186|0.87123|0.00409|0.82741|
|ALL\Cumulative Cluster Size|0.00193|0.86634|0.00417|0.82387|
|ALL\Relative Distance|0.00246|0.82950|0.00454|0.80837|
|ALL\Local Relative Contrast|0.00188|0.86954|0.00432|0.81743|
|ALL\Cluster Coeff. of Variance|0.00192|0.86678|0.00413|0.82565|
|ALL\∆(Relative Distance)|0.00191|0.86783|0.00419|0.82296|
|ALL\Data Size|0.00188|0.86990|0.00415|0.82464|
|ALL\∆(Cumulative Cluster Size)|0.00186|0.87096|0.00410|0.82686|
|ALL\Rank|0.00186|0.87094|0.00416|0.82444|
|ALL\Maximum Cluster Distance|0.00187|0.87078|0.00416|0.82407|

**2 2**

Fig. 4: *A*%for SIFT1B and Deep1B subsets (10M–100M)

on a two-level hierarchical index at 99% recall target. QASP model. Cumulative cluster size and relative distance contribute is trained on a 10M subset and applied at inference without most to positive recall predictions for both Euclidean and retraining. QASP consistently yields*≥*80% reduction in*A*%. Angular datasets, though with high variance—expected since large cluster sizes and relative distances do not guarantee high recall for extremely hard queries. Feature ablation results (Ta- bleVI) confirm that cumulative cluster size, relative distance, and local relative contrast are important across both dataset categories, while features such as jump in relative distance

(d) GLOVE-
are more influential for angular datasets.

(a) MNIST (b) GIST (c) SIFT1M 200
(e) DEEP1B 10M (f) COCOI2I (g) COCOT2I
Fig. 5: Training loss (MSE) over epochs

*B. Prediction Error Analysis* Figure6shows actual versus predicted recall for DL and GBDT models (we omit Lite for brevity). Both models achieve MSE of 0.002 and similar R² with DL slightly better. Errors are balanced around the diagonal with a slight bias toward over-prediction—preferable for meeting recall targets. Predic- tion accuracy remains high across the entire recall range.
Fig. 7: Feature importance analysis. Left: Euclidean datasets.

Right: Angular datasets.

VIII. CONCLUSION We introduced QASP to optimize vector search by predict- ing the complete recall progression curve per query via a single proactive inference, from which a search policy is derived for any recall target. QASP decouples the policy from specific targets or index configurations and enables domain adaptation with zero-shot or minimal fine-tuning. We provide theoretical guarantees, including that a finite sample suffices for conver- gence independent of dataset size and dimensionality, and a dominance condition where QASP’s data access savings over fixed policies grow exponentially in intrinsic dimensionality. Our query variability-aware evaluation demonstrates the im- portance of minimizing recall variance across queries. QASP achieves significantly lower variance, lower deviation from target, and higher satisfaction rate while accessing similar or less data, with improvements most pronounced for hard queries and high recall regimes. QASP extends to hierarchical partitioning using inference-time scaling alone, achieving 99% recall with 80% less data access. QASP’s progressive recall predictions further enable a lightweight reactive complement without additional inference.

REFERENCES [1]LanceDB, “IVF-PQ index,” LanceDB Documentation,[https://lancedb](https://lancedb). github.io/lancedb/concepts/index ivfpq/#query-the-index.

(a) SIFT1M(G) (b) SIFT1M(D) (c) MNIST(G) (d) MNIST(D)
(g) (h)
(e) GIST(G) (f) GIST(D) DEEP10M(G) DEEP10M(D)
Fig. 6: Prediction error analysis showing actual vs. predicted

recall between GBDT (G) and DL (D) recall predictor models.

*C. Feature Studies* We fix a set of nine features (Fig.7) and analyze their contributions using SHAP values [52] from the QASP-GBDT

[2]Facebook AI Research, “Guidelines to choose an index,” FAISS Wiki,[https://github.com/facebookresearch/faiss/wiki/](https://github.com/facebookresearch/faiss/wiki/) Guidelines-to-choose-an-index. [3]OpenSearch, “Choose the k-NN algorithm for your billion- scale use case with OpenSearch,” Amazon OpenSearch Service Blog, 2022,[https://aws.amazon.com/blogs/big-data/](https://aws.amazon.com/blogs/big-data/) choose-the-k-nn-algorithm-for-your-billion-scale-use-case-with-opensearch/. [4]C. Li, M. Zhang, D. G. Andersen, and Y. He, “Improving approximate nearest neighbor search through learned adaptive early termination,” in *Proceedings of the 2020 ACM SIGMOD International Conference on* *Management of Data*, 2020, pp. 2539–2554. [5]J. Mohoney, D. Sarda, M. Tang, S. R. Chowdhury, A. Pacaci, I. F. Ilyas, T. Rekatsinas, and S. Venkataraman, “Quake: Adaptive indexing for vector search,” 2025. [6]Y. Fu, C. Chen, Y. Chen, W.-F. Wong, and B. He, “Vista: Vector indexing and search for large-scale imbalanced datasets,” in*2025 IEEE 41st* *International Conference on Data Engineering (ICDE)*, 2025, pp. 543–

556.
[7]H. Wang, W. Wu, C. Luo, A. Bian, C. Meng, Y. Wu, and J. Sun, “Boosting accuracy and efficiency for vector retrieval with local scaling graph,” in*2025 IEEE 41st International Conference on Data Engineer-* *ing (ICDE)*, 2025, pp. 336–348. [8]P. Sun, F. Chern, Y. Akhremtsev, R. Guo, D. Simcha, and S. Kumar, “Scaling laws for nearest neighbor search,” in*The 1st Workshop on* *Vector Databases*, 2025. [9]H. Ferhatosmanoglu, E. Tuncel, D. Agrawal, and A. El Abbadi, “Ap- proximate nearest neighbor searching in multimedia databases,” in*Pro-* *ceedings 17th International Conference on Data Engineering (ICDE)*. IEEE, 2001, pp. 503–511. [10]E. Tuncel, H. Ferhatosmanoglu, and K. Rose, “Vq-index: An index struc- ture for similarity searching in multimedia databases,” in*Proceedings* *of the 10th ACM International Conference on Multimedia*, 2002, pp. 543–552. [11]H. Jegou, M. Douze, and C. Schmid, “Product quantization for nearest neighbor search,”*IEEE Transactions on Pattern Analysis and Machine* *Intelligence*, vol. 33, no. 1, pp. 117–128, 2010. [12]Q. Chen, B. Wang, Y. Guo, Y. Zheng, Y. Li, X. Chang, E. Y. Sun,

J. Zhang, X. Li, and X. Zhang, “Spann: Highly-efficient billion-scale approximate nearest neighbor search,” in*Advances in Neural Informa-* *tion Processing Systems*, vol. 34, 2021, pp. 10 337–10 349.
[13]M. D. Manohar, Z. Shen, G. Blelloch, L. Dhulipala, Y. Gu, H. V. Simhadri, and Y. Sun, “Parlayann: Scalable and deterministic parallel graph-based approximate nearest neighbor search algorithms,” in*Pro-* *ceedings of the 29th ACM SIGPLAN Annual Symposium on Principles* *and Practice of Parallel Programming*, 2024, pp. 270–285. [14]Y. Su, Y. Sun, M. Zhang, and J. Wang, “Vexless: A serverless vector data management system using cloud functions,”*Proceedings of the ACM on* *Management of Data*, vol. 2, no. 3, pp. 1–26, 2024. [15]S. Jayaram Subramanya, F. Devvrit, H. V. Simhadri, R. Krishnawamy, and R. Kadekodi, “Diskann: Fast accurate billion-point nearest neighbor search on a single node,”*Advances in Neural Information Processing* *Systems*, vol. 32, 2019. [16]J. Oakley and H. Ferhatosmanoglu, “SQUASH: Serverless and dis- tributed quantization-based attributed vector similarity search,”*arXiv* *preprint arXiv:2502.01528*, 2025. [17]F. Pedregosa, F. Bach, and A. Gramfort, “On the consistency of ordinal regression methods,”*Journal of Machine Learning Research*, vol. 18, no. 55, pp. 1–35, 2017. [18]Y. Gorishniy, I. Rubachev, and A. Babenko, “On embeddings for numer- ical features in tabular deep learning,”*Advances in Neural Information* *Processing Systems*, vol. 35, pp. 24 991–25 004, 2022. [19]R. Shwartz-Ziv and A. Armon, “Tabular data: Deep learning is not all you need,”*Information Fusion*, vol. 81, pp. 84–90, 2022. [20]M. Chatzakis, Y. Papakonstantinou, and T. Palpanas, “Darth: Declara- tive recall through early termination for approximate nearest neighbor search,”*Proc. ACM Manag. Data*, vol. 3, no. 4, Sep. 2025. [21]Y. Li, N. Wang, J. Shi, J. Liu, and X. Hou, “Revisiting batch normal- ization for practical domain adaptation,” 2016. [22]M. Aumuller and M. Ceccarello, “The role of local dimensionality mea-¨ sures in benchmarking nearest neighbor search,”*Information Systems*, vol. 101, p. 101807, 2021. [23]R. Rivest, “On self-organizing sequential search heuristics,”*Communi-* *cations of the ACM*, vol. 19, no. 2, pp. 63–67, 1976.

[24]D. Pollard, “Convergence of stochastic processes,”*Springer Series in* *Statistics*, 1984. [25]——,*Empirical Processes: Theory and Applications*. Institute of Mathematical Statistics, 1990. [26]A. Blumer, A. Ehrenfeucht, D. Haussler, and M. K. Warmuth, “Learn- ability and the vapnik-chervonenkis dimension,”*Journal of the ACM* *(JACM)*, vol. 36, no. 4, pp. 929–965, 1989. [27]R. Gupta and T. Roughgarden, “A pac approach to application-specific algorithm selection,”*SIAM Journal on Computing*, vol. 46, no. 3, pp. 992–1017, 2017. [28]M.-F. Balcan, “Data-driven algorithm design,”*Beyond Worst Case* *Analysis of Algorithms (Tim Roughgarden, ed.)*, 2020. [29]V. N. Vapnik and A. Y. Chervonenkis, “On the uniform convergence of relative frequencies of events to their probabilities,” in*Measures of* *complexity: festschrift for alexey chervonenkis*. Springer, 2015, pp. 11–30. [30]M. Anthony and P. L. Bartlett,*Neural network learning: Theoretical* *foundations*. Cambridge University Press, 2009. [31]P. L. Bartlett and W. Maass, “Vapnik-chervonenkis dimension of neural nets,”*The handbook of brain theory and neural networks*, pp. 1188– 1192, 2003. [32]P. W. Goldberg and M. R. Jerrum, “Bounding the vapnik-chervonenkis dimension of concept classes parameterized by real numbers,”*Machine* *Learning*, vol. 18, no. 2-3, pp. 131–148, 1995. [33]M. Karpinski and A. Macintyre, “Polynomial bounds for vc dimension of sigmoidal and general pfaffian neural networks,”*Journal of Computer* *and System Sciences*, vol. 54, no. 1, pp. 169–176, 1997. [34]A. Beygelzimer, S. M. Kakade, and J. Langford, “Cover trees for nearest neighbor,” in*Proceedings of the 23rd International Conference* *on Machine Learning (ICML)*. ACM, 2006, pp. 97–104. [35]J. L. Bentley, “Multidimensional binary search trees used for associative searching,”*Communications of the ACM*, vol. 18, no. 9, pp. 509–517,

1975.
[36]S. M. Omohundro, “Five balltree construction algorithms,”*International* *Computer Science Institute Berkeley*, 1989. [37]P. Zezula, P. Savino, G. Amato, and F. Rabitti, “Approximate similarity retrieval with m-trees,”

1998.
*The VLDB Journal*, vol. 7, no. 4, pp. 275–293,

[38]H. Ferhatosmanoglu, E. Tuncel, D. Agrawal, and A. El Abbadi, “Vector- approximation based indexing for non-uniform high dimensional data sets,”*Proceedings of the 9th International Conference on Information* *and Knowledge Management (CIKM)*, pp. 202–209, 2000. [39]Milvus, “Configure index parameters,” Milvus Documentation v2.3.0, 2023,[https://milvus.io/docs/v2.3.0/index.md](https://milvus.io/docs/v2.3.0/index.md). [40]Facebook AI Research, “Autotune example,” FAISS Source Code,https: //github.com/facebookresearch/faiss/blob/main/tutorial/cpp/4-GPU.cpp. [41]Y. A. Malkov and D. A. Yashunin, “Efficient and robust approxi- mate nearest neighbor search using hierarchical navigable small world graphs,”*IEEE Transactions on Pattern Analysis and Machine Intelli-* *gence*, vol. 42, no. 4, pp. 824–836, 2018. [42]C. Zhang and R. J. Miller, “Distribution-aware exploration for adaptive HNSW search,”*Proceedings of the ACM on Management of Data*, vol. 4, no. 1, 2026. [43]B. Zheng, Z. Yue, Q. Hu, X. Yi, X. Luan, C. Xie, X. Zhou, and C. S. Jensen, “Learned probing cardinality estimation for high-dimensional approximate NN search,” in*2023 IEEE 39th International Conference* *on Data Engineering (ICDE)*, 2023, pp. 3209–3221. [44]D. G. Lowe, “Distinctive image features from scale-invariant keypoints,” *Int. J. Comput. Vision*, vol. 60, no. 2, p. 91–110, Nov. 2004. [45]Y. LeCun, L. Bottou, Y. Bengio, and P. Haffner, “Gradient-based learning applied to document recognition,”*Proceedings of the IEEE*, vol. 86, no. 11, pp. 2278–2324, 2002. [46]A. Oliva and A. Torralba, “Modeling the shape of the scene: A holistic representation of the spatial envelope,”*International journal of computer* *vision*, vol. 42, pp. 145–175, 2001. [47]A. Babenko and V. Lempitsky, “Efficient indexing of billion-scale datasets of deep descriptors,” in*Proceedings of the IEEE Conference* *on Computer Vision and Pattern Recognition*, 2016, pp. 2055–2063. [48]J. Pennington, R. Socher, and C. D. Manning, “Glove: Global vectors for word representation,” in*Empirical Methods in Natural Language* *Processing (EMNLP)*, 2014, pp. 1532–1543. [49]T.-Y. Lin, M. Maire, S. Belongie, L. Bourdev, R. Girshick, J. Hays,

P. Perona, D. Ramanan, C. L. Zitnick, and P. Dollar, “Microsoft coco: ´ Common objects in context,” 2015.

[50]A. F. Agarap, “Deep learning using rectified linear units (relu),” 2019. [51]D. Arthur and S. Vassilvitskii, “k-means++: the advantages of careful seeding,” in*Proceedings of the Eighteenth Annual ACM-SIAM Sym-* *posium on Discrete Algorithms*, ser. SODA ’07. USA: Society for Industrial and Applied Mathematics, 2007, p. 1027–1035. [52]S. Lundberg and S.-I. Lee, “A unified approach to interpreting model predictions,” 2017.

IX. AI ASSISTANCESTATEMENT We used Claude (Anthropic, Opus 4.6) to assist with imple- mentation of the PCE-Net baseline directly from the original paper descriptions as the original implementation was not available. Claude was also used for refining figure aesthetics and layout. All experimental design, theoretical analysis, and scientific content are solely the authors’ work.
