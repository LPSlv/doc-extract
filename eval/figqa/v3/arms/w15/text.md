## LEMUR: Learning to Align with Multi-Objective Reinforcement Learning from Preference Feedback

1,4∗ 1,4

###, Samuele Vinanzi³

### Manith Adikari

###, Bei Peng²

###, Angelo Cangelosi

1 Department of Computer Science, University of Manchester 2 School of Computer Science, University of Sheffield 3 School of Computing & Digital Technologies, Sheffield Hallam University 4 Centre for Robotics & AI, University of Manchester

#### Abstract

Reinforcement Learning (RL) systems are typically trained using a single, well-specified scalar reward function. How- ever, real-world decision-making tasks often involve multiple, competing objectives, such as performance versus efficiency, where ground-truth reward functions are difficult to specify orinaccessible.WhileMulti-ObjectiveRL(MORL)addresses such trade-offs by modeling rewards as vectors, existing ap- proaches typically assume access to a well-specified reward function for each objective, inheriting the same challenges faced by single-objective RL. Meanwhile, Preference-based RL (PbRL) has shown great potential in solving complex tasks without access to a pre-defined reward function through reward learning from human feedback, yet has largely been studiedinsingle-objectivesettings.Inthiswork,webridgethis gap with LEMUR: Learning to Align with Multi-Objective Reinforcement Learning with Preference feedback, a novel framework where an agent interactively learns from the pref- erences of multiple humans to learn optimal multi-objective policies. Our approach jointly learns policies and multiple objective-specific reward models from human feedback, en- abling agents to effectively balance competing objectives dur- ing learning. We evaluate LEMUR on a variety of benchmark multi-objective tasks, and empirical results demonstrate its superior performance over baseline methods. Our method presents a promising direction for solving multi-objective decision-making tasks without pre-defined reward functions.

### 1 Introduction

Reinforcement Learning (RL) has achieved remarkable suc- cess in training autonomous agents, from game-playing (Mnih et al. 2013) to robotics (Tan et al. 2018). By formal- izing learning as the maximization of cumulative rewards through trial and error learning (Sutton and Barto 1998), RL provides a natural framework for training autonomous ‘goal- seeking’ agents (McCarthy 1997). However, standard RL relies on two critical assumptions: that the goal can be repre- sentedbyasingle*scalarreward*,andthatthisrewardfunction is*well-specified*. In practice, these assumptions rarely hold in complex, real-world domains. Real-world tasks often involve*multiple, competing*ob- jectives (Dulac-Arnold, Mankowitz, and Hester 2019), such as balancing speed versus safety in autonomous driving

∗ Corresponding Author: manith.adikari@manchester.ac.uk

(Wang et al. 2026), or throughput versus energy efficiency in robotics (Huang et al. 2022; Kouritem et al. 2022). The field of Multi-Objective Reinforcement Learning (MORL) addresses this by modeling*rewards as vectors*to find a set of Pareto-optimal policies (Roijers et al. 2013): policies where no objective’s expected returns can be in- creased without decreasing the returns of other objectives. However, existing MORL approaches typically assume that the ground-truth reward function for each objective is ac- cessible and manually specified (Hayes et al. 2022b). Thus, they inheritthe same challengesof reward specificationfrom the single-objective RL domain, now across multiple objec- tives. Manually designing a reward function that can achieve an adequate balance between competing objectives is chal- lenging and can lead to oversimplification, which results in suboptimal policies (Knox et al. 2012) and possible reward exploitation (Amodei et al. 2016). To avoid complicated re- ward engineering, Preference-based RL (PbRL) learns re- ward models directly from human feedback (Christiano et al.

2017), which leads to better alignment between the system’s behavior and human preferences. Despite progress in re- ward learning for single-objective RL, this problem remains largely unexplored in the MORL setting. While some works consider reward learning in MORL, they are typically lim- ited to Large Language Model (LLM) post-training settings or narrow natural language-based tasks (Bakker et al. 2022; Rame et al. 2023; Yang et al. 2024), and do not study the joint learning of policies and rewards in environments with multiple, competing objectives. Reward specification is already a major bottleneck in scal- ingsingle-objectiveRLsettings,andbecomesevenmorecrit- icalinMORL.Twokeychallengesarise.First,theagentmust optimize multiple objectives whose underlying reward func- tions are complex, implicit, or inaccessible. Second, even when human feedback is available, collapsing multi-criteria reward signals into a single scalar obscures the very trade- off structure that MORL is designed to optimize (Vamplew et al. 2011; Roijers et al. 2013; Sorensen et al. 2024). Con- sider training a robotic system: *non-expert*operators can re- liably judge task-level success, such as whether objects were grasped or placed correctly, while expert operators are re- quired to assess fine-grained criteria such as grasp stability, long-term wear, or safety-related objectives. Collapsing such *heterogeneous*feedback into a single reward risks conflating
# arXiv:2607.29559v1 [cs.AI] 31 Jul 2026

*distinct*objectivesanddilutingexpertsignals,motivatingthe need for*separate*, objective-specific reward models learned from the appropriate source of feedback. This creates a crucial gap: *How can agents learn optimal* *trade-offs between conflicting objectives when the reward* *functions are unknown and must be inferred from feedback?* To address this gap, we introduce**LEMUR**: **Le**arning to Align with**Mu**lti-Objective**R**einforcement Learning from Preference Feedback, a framework for learning to balance multiple objectives without pre-defined reward functions. Our approach jointly learns policies and multiple objective- specific reward models from preference feedback, enabling agents to effectively balance competing objectives during learning. By removing the assumption of known reward functions and explicitly modeling multiple objectives, our method tackles a key challenge to scaling MORL in real- world, human-aligned domains. To summarize, our main contributions are: •We propose a novel framework, LEMUR, which learns *multiple*objective-specific reward models from pref- erence feedback and then optimizes policies against these reward models using multi-objective reinforcement learning. This enables agents to effectively solve multi- objective decision-making tasks without access to pre- defined reward functions, while naturally accommodat- ing heterogeneous sources of feedback, where different annotators may hold expertise over different objectives. •OurextensiveexperimentsdemonstratethatLEMURout- performs baselines across a range of benchmark multi- objective environments, namely high-dimensional con- tinuous control tasks, and further show LEMUR’s ro- bustness to label noise, constrained feedback budgets, and scaling to more objectives.

### 2 Preliminaries

**Multi-Objective Reinforcement Learning.**We formu- late the problem as a Multi-Objective Markov Decision Process (MOMDP) (White 1982), defined by the tuple *⟨S,A,T,γ,*r*⟩*.Here,*S*and*A*denotestateandactionspaces respectively,*T*the transition dynamics, and*γ∈*[0*,*1)the discount factor. Unlike standard RL, the reward is a vector r(*s,a*)*∈*R *m* comprising*m*distinct objectives. The agent’s goal is to maximize the expected discounted vector returns P

|∞|t||||
|---|---|---|---|---|
|π t=0|t t||||
||′|∞ π t t=0|T ψ|t t|
||′||||

*J*(*π*) =E [ *γ* r(s*,*a)]. A policy*π*maps states to action distributions. Since no single policy typically max- imizes all objectives in MORL, the agent learns a set of policiesΠrepresenting optimal trade-offs, defined by Pareto dominance (Hayes et al. 2022a). A policy*π*dominates*π* *′* (denoted*J*(*π*)*≻J*(*π*)) if it is superior in at least one ob- jective and no worse in others. The solution set is the Pareto Frontier*F*=*{π∈*Π*|*∄*π ∈*Π : *J*(*π* *′* )*≻J*(*π*)*}*. **SoftActor-Critic(SAC).**SAC(Haarnojaetal.2018)isan off-policy actor-critic algorithm grounded in the maximum entropy framework. It augments standard single-objective RLwithanentropytermtoencourageexploration.Theagent P aims to maximize*J*(*π*) =E*π*[*tγ* *t* (*rt*+*αH*(*π*(*·|*s*t*)))]. **Reward Learning from Preference Feedback.**We fol- low the standard Preference-based RL (PbRL) framework,

which uses ‘latent rewards’ as a proxy for values (Christiano et al. 2017). Each human’s reward function is learned inde- pendently using their respective preference feedback. Simi- lar to prior work, we use preferences over pairs of trajectory segments,(*σ⁰,σ¹*). An expert teacher (e.g., human) pro- vides a label*y∈ {*0*,*1*,*0*.*5*}*to indicate their preference. To learn a reward functionˆparameterized by *r ψ*, we em- ploy the Bradley-Terry model (Bradley and Terry 1952), modeling the preference probability as P *P*[*σ¹ ≻σ⁰*;*ψ*] = <u>P exp</u> <u>ˆ(r σ</u> 1 <u>P</u> <u>)</u>. Given a dataset*D*, the reward func- exp ˆ(*r σ¹*)+exp ˆ(*r σ⁰*) tion is trained by minimizing the cross-entropy loss: h i *L* *CE*

(*ψ*) =*−*E*D*(1*−y*) log*P*[*σ⁰ ≻σ¹*]+*y*log*P*[*σ¹ ≻σ⁰*]*.*
(1)
The learned reward function can then be used to update the policy with any RL algorithm to maximize expected returns.

### 3 Problem Setup

Inthissection,wepresentourformulationofMulti-Objective Reinforcement Learning (MORL)*without pre-defined*re- ward functions for*multiple, conflicting*objectives.

**Latent Reward Vector.**In standard MORL, the reward function is a known vectorr(*s,a*)*∈*R *m*. However, in our work, the agent*does not*have access to the ground-truth reward function. Instead, we assume the existence of*m*dis- tinct multiple, conflicting human users (objectives), where each dimension*ri*corresponds to the latent reward function of the*i*-th specific user. Since these rewards are inaccessible, we must approximate them. We define a parameterized re- ward vectorˆr (*s,a*) = [ˆ*r* (*s,a*)*,...,*ˆ*r* (*s,a*)] *T*, where *ψ ψ*1 *ψm* eachcomponentisarewardmodellearnedfromhumanpref- erence feedback (Christiano et al. 2017).

**Multi-Objective RL Optimization.**The agent’s goal is to maximize the expected discounted vector returns. We adopt the most prevalent MORL formalism called the utility-based approach (Roijers et al. 2013), where we define a scalariza- *⊤ m* tion function*f*w(r) =w r, wherew P *∈*R is a preference weight vector on the simplex (i.e., *wi*= 1). Thus, we define an optimal MORL agent to be the policies belonging to the Convex Coverage Set (CCS), the subset of*F*optimal for linearly scalarized preferences (Roijers et al. 2013). To summarize, the MORL agent learns these policies by maximizingtheexpectedreturnsofthe*learned*latentreward vector linearly scalarized by the weight*w*, which determines the trade-offs between objectives: " # X *J*(*π*) =E *γ* w ˆr (*s,a*)*.*(2)

### 4 LEMUR

**LEMUR**(**Le**arning to Align with**Mu**lti-Objective **R**einforcement Learning from Preference Feedback), illus- trated in Figure 1 proceeds in three stages: (1) unsupervised pre-training,wheretheagentexploresviaintrinsicrewardsto collect diverse experiences (Section 4.1); (2) reward learn- ing, where multiple human teachers are queried for pref- erence feedback to train objective-specific reward models

Figure 1: Illustration of our framework LEMUR: (1) Unsupervised Pre-training for the MORL agent to explore and collect

diverseexperiencesviamaximizingstateentropyH(s).(2)RewardlearningfromPreferencefeedback,whereeachrewardmodel is learned separately from the preferences queried from each teacher. The reward models are used to dynamically relabel the state-action pairs as a reward vector for each objective (i.e., each teacher’s preferences). (3) Multi-Objective RL agent denoted by*πϕ*uses each of the trained reward models to do multi-objective policy optimization to maximize the expected vector rewards.

(Section 4.2); and (3) multi-objective RL training against the learned reward models (Section 4.3). Stages 2 and 3 repeat, continually improving both the reward models and the multi-objective policies. Full pseudocode is provided in Appendix B.

#### 4.1 Unsupervised Pre-training

Standard PbRL suffers from uninformative queries caused by the limited coverage of random initialization. To generate informative queries, LEMUR employs an unsupervised pre- training phase driven by intrinsic motivation (Lee, Smith, and Abbeel 2021). We encourage exploration by maximiz- ingstateentropy,approximatedviaaparticle-based*k*-nearest neighbors (*k*-NN) estimator (Liu and Abbeel 2021). The in-

|int t|t|k t|
|---|---|---|
|π|T t=0 t int|t|

trinsic reward*r* (*s*) = log(*∥s −s ∥*)is the normalized distancetothe*k*-thnearestneighborin*B*,andtheagentmax- P imizes*Jint*(*ϕ*) =E*ϕ*[ *γ* **r** (*s*)]. This populates the buffer with diverse behaviors, accelerating the subsequent multi-objective reward learning.

#### 4.2 Reward learning of Multiple Objectives from Preferences

A core challenge in our setup is that the agent does not have access to the ground-truth rewards, and the*m*conflicting objectives are characterized instead by the conflicting pref- erences of*m*humans. Following the PbRL formulation in Section 2, LEMUR learns a separate reward model ˆr*ψj*(*s,a*) per teacher, trained by minimizing the cross-entropy loss between the model’s predictions and that teacher’s labels (Equation 1). **Weight-ConditionedRewardModels.**Ratherthanlearn- ing each teacher’s reward in isolation, we condition every objective-specific model on the shared objective space. Each teacher*j*is assigned a reward model ˆr*ψj*(*s,a*), a lightweight

MLP predicting the full objective vector, whose scalar util- ity is obtained by projecting onto that teacher’s preference anchor,ˆ*jr* (*s,a*) =a *⊤* *j*ˆr*ψj*(*s,a*). This couples the*m*learned modelstoacommonvector-rewardstructure,sothatapolicy conditioned onwreads a consistent per-teacher utility at in- ference, and the reward models remain directly comparable as the number of conflicting teachers grows. We deliber- ately adopt this simple architecture, as in prior approaches (Mu, Luan, and Jia 2025); we find it sufficient to recover strong compromise policies while keeping reward learning fast enough to remain in the loop with online policy opti- mization. **Query Sampling Strategy.**We sample trajectory pairs 0 1 (*σ ,σ*)uniformly at random from the buffer*B*, so that queries span the diverse state-action distributions explored by all policies. While more sophisticated disagreement- based strategies exist, uniform sampling offers simplicity and avoids bias toward particular regions of the objective space during early training.

#### 4.3 Multi-Objective RL Training

Given the parameterized reward vectorˆr*ψ*(*s,a*), LEMUR trains the MORL agent to maximize expected latent*vec-* *tor*rewards (Equation 2). For policy optimization we lever- age MORL/D, a state-of-the-art Multi-Objective Soft Actor- Critic (MO-SAC) algorithm (Felten, Talbi, and Danoy 2024) which learns a set of independent SAC policies and applies an evolutionary strategy for policy search. This off-policy choice is deliberate: reusing past experience from the re- play buffer is essential for sample efficiency under a limited human feedback budget. **Weight Vector Initialization and Adaptation.**The scalarization weight vectors*{*w*}*determine the trade-offs betweenobjectives.Givenw*∈*R *m* ,weoptimizeforpolicies using SAC (Haarnoja et al. 2018) on the scalarized reward of

Equation 2. We employ a Pareto Simulated Annealing (PSA) approach similar to (Felten, Talbi, and Danoy 2024), adapt- ing the weight vector in response to the current policies and theirdistancetonon-dominatedsolutions,allowingtheagent to focus training on feasible regions of the objective space while maintaining policy diversity. **Cooperation via Shared Buffer.**To facilitate informa- tion exchange across policies learning different trade-offs, all policies store and sample from a common replay buffer

*B*. This enables policies to learn from diverse experiences collected under different preference weightings, improving sample efficiency, a critical consideration given the limited human feedback budget. **RelabelingofVectorRewards**.Combiningoff-policyRL with a reward function learned from preferences introduces non-stationarity: as the reward model is updated with new feedback, rewards associated with past transitions in the buffer become stale, destabilizing learning. To address this, LEMURemploysavectorrewardrelabelingstrategyinspired by prior work (Lee, Smith, and Abbeel 2021). Rather than storing rewards, we store only the transitions, and compute vector rewards on the fly when a batch is sampled, using the most up-to-date reward models. This ensures the agent always trains on updated rewards, synchronizing policy and reward learning while preserving the sample efficiency of our off-policy approach.
### 5 Experiments

Our experiments address three questions: (1) Can LEMUR learn multi-objective policies that balance multiple*learned* reward models from*multiple*teachers? (2) How does LEMUR compare to existing baselines on multi-objective benchmarks? (3) Does explicitly learning multiple reward models for conflicting feedback outperform aggregating feedback into a single reward model? For all experiments, we report the mean across five random seeds with standard error. Additional implementation details are reported in Ap- pendices D & E. **Benchmark Environments & Setup.**We evaluate LEMUR on high-dimensional environments from the *MORL-Generalization*benchmark (Teoh, Varakantham, and Vamplew 2025). Following standard practice in PbRL (Lee et al. 2021; Christiano et al. 2017), we use scripted teach- ers that generate feedback according to the components of the ground-truth vector reward, enabling quantitative eval- uation; the ground-truth rewards remain inaccessible to the agent, which must jointly learn the conflicting preferences and optimize to find a balance. Our main experiments use twoconflictingteachers,thefundamentalversionoftheprob- lem; Section 5.1 demonstrates scaling to more objectives. We evaluate on:MO-Lunarlander, where Teacher A re- wards precise, stable landings and Teacher B prioritizes fuel conservation;MO-HopperandMO-Cheetah, continuous control locomotion tasks where Teacher A prefers fast loco- motionandTeacherBprefersslow,energy-efficientgaits;and MO-MetaWorld(Drawer-Close), a robotic-manipulation task from the Meta-World suite (Yu et al. 2020). Meta-World tasks are natively single-objective; we convert Drawer-Close into a two-objective task by pairing the native task-progress

reward(TeacherA)withacontrol-effortpenalty(TeacherB), mirroring the reward decomposition standard in the MORL benchmark suite (Teoh, Varakantham, and Vamplew 2025). Full environment details are given in Appendix G. **Baselines.**We compare against five baselines spanning distinct strategies for preference aggregation and learning from multiple objectives: (1) a**Utilitarian**agent, a sin- gle SAC agent optimizing the arithmetic mean of the in- dependently learned rewards; (2)**Naive**data pooling, which trains one monolithic reward model on all conflicting feed- back, akin to standard Reinforcement Learning from Human Feedback (RLHF); (3)**MORAL**(Peschl et al. 2022), which recovers per-teacher rewards via Adversarial Inverse Rein- forcement Learning (AIRL) and learns a scalarization over them; (4)**PbMORL**(Mu, Luan, and Jia 2025), a recent preference-based multi-objective method learning a weight- conditioned vector reward from pairwise feedback; and (5) **FPbRL**(Siddique, Sinha, and Cao 2023), which aggregates learnedper-teacherrewardsthroughaGeneralizedGiniWel- fare scalarization to optimize for fairness. We additionally report an (6)**Oracle**trained on ground-truth rewards as an upper bound. Unless otherwise noted, every baseline shares LEMUR’s interactive learning loop, reward-model architec- ture,pre-trainingstage,teacherweightvectors,querybudget, and environment-step budget; the primary distinction lies in *howconflictingrewardsignalsareaggregatedandoptimized*. Whereabaseline’soriginalpolicyoptimizerwoulddisadvan- tageitinourenvironments,weadaptinthebaseline’sfavour; all deviations are disclosed in Appendix E.

#### 5.1 Results & Analysis

Figure 2 presents the learning curves for all methods across

the benchmark environments. Across every environment, LEMUR is the method that most closely tracks the Ora- cle on both objectives simultaneously, effectively recovering policies that balance multiple, conflicting objectives. The Utilitarian and Naive agents remain flat with suboptimal re- turnsthroughout,supportingourhypothesisthataggregating conflicting reward signals into a single scalar degrades per- formance in such multi-objective settings. While MORAL improves early in LunarLander and Hop- per, it fails to sustain this progress: in MO-Hopper its re- turns peak mid-training and then steadily declines. This is consistent with the known failure of out-of-distribution op- timization due to static reward models; MORAL infers its per-teacher rewards offline from expert demonstrations via AIRL and holds them fixed. LEMUR instead does online policy optimization and addresses non-stationarity through *vector reward relabeling*. PbMORL and FPbRL, which both learn vector rewards from preference feedback, perform better than the aggrega- tionbaselines,yetstillfallshortofLEMUR.Weattributethis to the assumptions both methods inherit. PbMORL trains a single weight-conditioned reward model over pooled feed- back, implicitly assuming all preferences originate from one single teacher; under conflicting teachers the pooled model must average over conflicting labels, degrading the reward signal, most visibly in MO-Hopper and MO-Cheetah where it consistently trails LEMUR on both objectives. FPbRL

LunarLander Hopper 1400 70 1200 1000 80 800 90 600 Episode Returns(Objective One)400 100 200 110 0 20 40 60 80 0 0 2 4 6 1400 60 1200 1000 800 70 600 Episode Returns(Objective Two) 400 80 200

0 20 40 60 80 0 0 2 4 6 Training Steps (×10³) Training Steps (×10

Ground Truth (Oracle) FPbRL

Cheetah MetaWorld

2500 5000 2000 4000 1500 3000 2000 1000 1000 500 0 0 2 4 0 0 1 2 3 4 5 4500 4000 1400 3500 1200 3000 1000 2500 800 2000 600 1500 1000 400 500 200 0 0 2 4 0 0 1 2 3 4 5 ) Training Steps (×10) Training Steps (×10)

**LEMUR** MORAL PbMORL Utilitarian Naive

#### PbMORL,FPbRL) learn but consistently trail LEMUR.

100 **LEMUR**

|Environment|Hypervolume (↑)||Sparsity (↓)|
|---|---|---|---|
||LEMUR|PbMORL|LEMUR|
|MO-LunarLander1.10×10||1.09×10|134.57.8|
|MO-Hopper3.67×10||2.24×10|294.71731.7|
|MO-HalfCheetah4.86×10||4.78×10|294.72191.0|
|MO-MetaWorld2.15×10||1.43×10|436.35564.7|

Ground Truth (Oracle) 80 PbMORL FPbRL Naive Utilitarian 60MORAL

40 Success Rate (%) 20

0 0 1 2 3 4 5 Training Steps (×10)

Figure 3: Task Success Rate (%) learning curves on Meta-

World (Drawer Close Task).

preserves the vector structure but employs a fixed Gener- alized Gini welfare scalarization a priori, converging to a single welfare-optimal policy rather than a set of trade-offs: it achieves reasonable returns on MetaWorld, but fails to achieve task success (shown in Figure 3) nor make progress on the other environments. LEMUR avoids both failure modes by maintaining objective-specific reward models and adapting the trade-off online. On MO-MetaWorld, Figure 3 reports the task success rate: LEMUR reaches closest to the Oracle, while PbMORL plateaus.

**Multi-Objective Metrics.**We evaluate LEMUR using standard multi-objective metrics (Hayes et al. 2022a).*Hy-* *pervolume*(HV) measures the volume of objective space, re- warding policies that are both high-performing and broadly spread (Teoh, Varakantham, and Vamplew 2025);*Sparsity*

**PbMORL** 4 4 6 6 7 7 6 6

Table 1: Hypervolume and Sparsity for LEMUR and Pb-

MORL. Full results are in Appendix F.1.

(SPS) measures the average distance between policies along the front, with lower values indicating more uniform cov- erage (Teoh, Varakantham, and Vamplew 2025). As sum- marised in Table 1, LEMUR attains the highest or compara- ble Hypervolume across all four environments while achiev- ing markedly lower sparsity than PbMORL, indicating that it learns policies that is both higher-performing and more uniformly distributed over the trade-off space. MORAL is excludedfromtheseset-basedmetrics,asitssingle-objective policyoptimizationagainstascalarizedrewardrecoversonly one solution rather than a front. Full results are reported in Appendix F.1.

**Reward Model Alignment.**We additionally evaluate the learned reward models directly against the ground-truth teacherrewards,followingestablishedPbRLevaluationprac- tice (Lee et al. 2021). We report*Spearman*rank correlation, which measures how accurately the learned reward models rankindividualstatescomparedtotheteachers’ground-truth

Figure 2: Learning curves on all benchmark environments:MO-LunarLander,MO-Hopper,MO-Cheetah, and

MO-MetaWorld. Curves depict the true objective returns (inaccessible to the agent), averaged across five seeds, with shaded regions representing standard error.**LEMUR**(blue) most closely tracks the**Oracle**(red) on both objectives simultaneously. Baselines that aggregate conflicting feedback (**Naive**,**Utilitarian**) fail to make progress, while the external baselines (**MORAL**,

reward; the*Trajectory Alignment Coefficient*(TAC) (Mus- limani et al. 2025), which compares rankings over whole trajectories rather than individual transitions. Table 2 shows that LEMUR’s reward models recover their teachers’ pref- erence orderings with consistently strong correlation, and outperform both PbMORL and FPbRL (Appendix F.2).

|Environment|Spearman (|ρ↑|)|TAC (|↑ )|
|---|---|---|---|---|---|
|MO-Hopper0|. 945|± 0. 002|0|. 856 ±|0. 014|
|MO-HalfCheetah0|. 710|± 0. 005|0|. 898 ±|0. 041|
|MO-MetaWorld0|. 520|± 0. 007|0|. 347 ±|0. 026|

Table 2: LEMUR reward model alignment, reporting Spear-

man rank correlation and Trajectory Alignment Coefficient (TAC). Per-metric comparisons against PbMORL and FP- bRL are in Appendix F.2.

7000 7000 6000 6000 5000 5000 4000 4000 Episode Returns(Objective One) 2000 3000 Episode Returns(Objective One) 2000 3000 1000 1000 0 0 5000 6000 4000 5000 4000 3000 3000 Episode Returns (Objective Two) 2000 Episode Returns(Objective Two) 2000 1000 1000 0 0

2000 3000 2000 Episode Returns (Objective Three) 1000 Episode Returns(Objective Three) 1000 0 0 1 2 3 4 5 0 Training Steps (×10)

**LEMUR** 2000 Ground-Truth Reward (Oracle) Episode Returns(Objective Four) 1000 0 0 1 2 3 4 Training Steps (×10)

Figure 4: LEMUR scalability to higher-dimensional objec-

tive spaces. Episode returns for**(a)**3-objective and**(b)**4- objective tasks, comparing policies trained with LEMUR (blue) versus ground-truth oracle rewards (orange).

**Scaling to More Objectives.**We next vary the teacher configuration onMO-Cheetah. Figure 4 extends LEMUR to three and four conflicting teachers: the learned-reward policies closely track the ground-truth oracle across all ob- jectives, demonstrating the per-teacher decomposition scales without modification, each additional objective adding one reward model.

#### 5.2 Ablation Studies

To validate the components of LEMUR, we conduct ablation studiesonthehigh-dimensionalMO-Cheetahdomain;Fig- ure 5 visualizes the learning curves. **ImpactofSharedBuffer,Relabeling,andPre-training.**

Figure 5(a) isolates the contributions of the shared re-

play buffer, vector reward relabeling, and unsupervised pre-

training. Disabling the shared buffer causes the most severe degradation. With the shared buffer intact, removing rela- beling alone produces a modest but consistent drop relative to full LEMUR, confirming that recomputing rewards under the current models stabilizes learning against reward non- stationarity. Removing pre-training accelerates the earliest phase of training, but converges to lower final returns, indi- cating that the diverse initial buffer ultimately yields better reward models and policies. **Robustness to Label Noise.**Figure 5(b) corrupts a frac- tion of teacher labels (flipping preferences with probability up to 15%), following PbRL benchmarking protocol (Lee et al. 2021). LEMUR degrades gracefully: performance is essentially unaffected up to 10% noise, and at 15% the agent still learns effective compromise policies on both objectives, albeit with slower convergence and higher variance, indicat- ing tolerance to levels of annotator error. **Impact of Feedback Budget.**Figure 5(c) varies the total query budget from 260 to 5,200 per teacher. Performance improves with budget, and larger budgets learn faster; no- tably, even 260 total learns adequate policies on both objec- tives. This feedback efficiency is particularly important in preference-based RL, where human queries are limited. **Reward Model Ablation.**To verify that LEMUR’s gains stem from its weight-conditioned reward model rather than the surrounding pipeline, we re-run LEMUR replacing this component with an ensemble of three unconditioned MLPs (Christiano et al. 2017; Lee, Smith, and Abbeel 2021), hold- ing all else fixed. The weight-conditioned variant converges to6*,*812*±*39and4*,*404*±*22on the two objectives, against 4*,*556*±*369and2*,*902*±*245for the ensemble. (For full results, refer to Appendix C.7). **Additional Experiments.**In Appendices C.1-C.7, we demonstrate that LEMUR accommodates changing teacher- s/objectives mid-training, varying levels of conflict between teachers, and also non-stationary preferences without reini- tialization. Query ablations reveal that segment length is im- portant to performance, and we verify that LEMUR main- tains performance even when teachers are in agreement with overlapping preferences.

### 6 Related Work

**RewardLearningfromPreferenceFeedback.**Designing reward functions is a primary bottleneck in scaling RL, as manual crafting is impractical and can induce unsafe behav- ior (Amodei et al. 2016); prior work instead learns rewards from demonstrations (Ng and Russell 2000; Abbeel and Ng

2004), language (Lin et al. 2022), or human feedback (Chris- tiano et al. 2017). Preference-based RL (PbRL) learns re- wards from pairwise comparisons (Christiano et al. 2017; Lee, Smith, and Abbeel 2021); popularized as RLHF (Stien- nonetal.2020;Ouyangetal.2022),ittypicallytrainsasingle reward model, aggregating diverse feedback into one scalar (Ouyangetal.2022)andfailingtocapturethemulti-objective nature of human values (Sorensen et al. 2024). Offline vari- ants train rewards on fixed datasets before policy optimiza- tion(Shin,Dragan,andBrown2023),butstaticmodelssuffer distributionshiftasthepolicydivergesfromtheofflinecover- age,causingrewardexploitation(Gao,Schulman,andHilton

0% Noise 260 Total Queries No Relabel 1,300 Total Queries No Shared Buffer 5% Noise 10% Noise 3,900 Total Queries 6000 5000LEMUR No Shared Buffer, No Relabel 500015% Noise 5,200 Total Queries 5000 4000No Pretrain 4000 4000 3000 3000 3000 Episode Returns(Objective One) 2000 2000 2000 1000 1000 1000 0 0 0 4000 4000 4000 3000 3000 3000 2000 2000 2000 (Objective Two) Episode Returns 1000 1000 1000 0 0 1 2 3 4 5 0 0 0 0 3 4 5 6 1 2 3 4 5 6 7 8 Training Steps (×10) 1 2 Training Steps (×10 ) Training Steps (×10 )

(a) Buffer Relabeling
(b) Noisy Labels (c) Query Budget
Figure 5: Ablation studies onMO-Cheetahevaluating the impact of (a) the shared buffer, vector reward relabeling, and

unsupervised pre-training, (b) noisy teacher labels, and (c) varying the total query budget per teacher on agent returns for both objectives; by default LEMUR uses 3900 queries (green). The results are averaged over multiple runs across five seeds.

2023; Ye et al. 2024). Online, iterative RLHF mitigates this by collecting feedback alongside policy optimization (Dong etal.2024;Gao,Schulman,andHilton2023;Yeetal.2024), which is more critical still in MORL, where the agent must span a space of diverse policies (Hayes et al. 2022a); offline MORL instead presupposes specified rewards or adequate dataset coverage (Yuan et al. 2024; Zhu, Dang, and Grover

2023). LEMUR circumvents this by jointly and interactively optimizing both the reward models and the multi-objective policy online.
#### Multi-Objective Reinforcement Learning (MORL).

MORLlearnsasetofpoliciesapproximatingtheParetofron- tier(Roijersetal.2013;Hayesetal.2022b),viasingle-policy scalarization, weight-conditioned, or multi-policy methods; multi-taskandMeta-RLarecloselyrelated(Chenetal.2019; Abdolmaleki et al. 2020; Sener and Koltun 2018). Most of this literature assumes a vector of ground-truth reward func- tions (Hayes et al. 2022b), which is impractical in complex, real-world tasks. Reward-free MORL (Chen et al. 2026) re- laxes this only partially, using reward-free exploration as an auxiliary objective while still assuming an extrinsically specified ground-truth reward. LEMUR extends the MORL paradigm to the setting where the objectives are never ob- served and must be inferred directly from preferences.

**Learning & Alignment with Diverse Objectives.**Stan- dard RLHF fails to capture the*pluralistic*nature of hu- man values (Sorensen et al. 2024), and existing remedies rely on manual aggregation functions (Rodriguez-Soto et al.

2023), expensive consensus datasets (Tessler et al. 2024), static offline learning (Bakker et al. 2022), or model het- erogeneous feedback as hidden context without optimizing the trade-off between preferences (Siththaranjan, Laidlaw, and Hadfield-Menell 2024). Our closest baselines learn re- wards for multiple objectives but inherit strong coherence assumptions: MORAL (Peschl et al. 2022) requires expert demonstrations and freezes AIRL-learned rewards (Fu, Luo, and Levine 2018), PbMORL (Mu, Luan, and Jia 2025) as- sumes a single teacher, and FPbRL (Siddique, Sinha, and
Cao 2023) fixes a welfare scalarization a priori. LEMUR instead learns objective-specific reward models from sepa- rate feedback streams and jointly optimizes amulti-objective policy online via*vector reward relabeling*, without offline pre-training or expert demonstrations.

### 7 Conclusion & Limitations

We propose LEMUR, a framework for Multi-Objective RL indomainswhererewardfunctionsareunknownandmustbe inferred from the conflicting preferences of multiple teach- ers.LEMURjointlylearnstheobjectivesandthepoliciesthat balancethem,withoutexpertdemonstrations,pre-definedre- wards, or a priori aggregation rules that existing methods require. Across multi-objective RL control and robotic ma- nipulation benchmark environments, LEMUR outperforms aggregation baselines and recent preference-based multi- objectivemethods,andremainsrobusttolabelnoise,reduced feedback budgets, and scaling to additional objectives. Sev- eral directions for future work are as follows. Our evaluation uses scripted teachers, standard practice in PbRL for con- trolled and reproducible comparison (Lee et al. 2021); our noise ablations suggest the framework tolerates the label er- ror real annotators exhibit, and a human study is the natural next validation. We adopt linear scalarization, and extend- ing to non-linear scalarization would allow the framework to learn policies in non-convex regions of the front (Roi- jers et al. 2013; Hayes et al. 2022b). Finally, active querying (Akrour, Schoenauer, and Sebag 2012) offers a route to fur- ther reducing the number of queries, which is a promising path for deploying preference-based MORL in real-time.

### References

Abbeel, P.; and Ng, A. Y. 2004. Apprenticeship learning via inverse reinforcement learning. In*Proceedings of the* *twenty-first international conference on Machine learning*,

1. Abdolmaleki, A.; Huang, S.; Hasenclever, L.; Neunert, M.; Song, F.; Zambelli, M.; Martins, M.; Heess, N.; Hadsell, R.;

and Riedmiller, M. 2020. A distributional view on multi- objective policy optimization. In*International conference* *on machine learning*, 11–22. PMLR. Akrour, R.; Schoenauer, M.; and Sebag, M. 2012. April: Active preference learning-based reinforcement learning. In *Joint European conference on machine learning and knowl-* *edge discovery in databases*, 116–131. Springer. Amodei, D.; Olah, C.; Steinhardt, J.; Christiano, P.; Schul- man, J.; and Mané, D. 2016. Concrete problems in AI safety. *arXiv preprint arXiv:1606.06565*. Bahlous-Boldi,R.;Puri,I.;Shenfeld,I.;Kumar,A.;Damani,

M.;Risi,S.;Khattab,O.;Hong,Z.-W.;andAgrawal,P.2026. Vector Policy Optimization: Training for Diversity Improves Test-Time Search.*arXiv preprint arXiv:2605.22817*. Bai, Y.; Jones, A.; Ndousse, K.; Askell, A.; Chen, A.; Das- Sarma, N.; Drain, D.; Fort, S.; Ganguli, D.; Henighan, T.; et al. 2022. Training a helpful and harmless assistant with reinforcementlearningfromhumanfeedback.*arXivpreprint* *arXiv:2204.05862*. Bakker, M.; Chadwick, M.; Sheahan, H.; Tessler, M.; Campbell-Gillingham, L.; Balaguer, J.; McAleese, N.; Glaese, A.; Aslanides, J.; Botvinick, M.; et al. 2022. Fine- tuning language models to find agreement among humans with diverse preferences.*Advances in neural information* *processing systems*, 35: 38176–38189. Bowling, M.; Martin, J. D.; Abel, D.; and Dabney, W. 2023. Settling the reward hypothesis. In*International Conference* *on Machine Learning*, 3003–3020. PMLR. Bradley, R. A.; and Terry, M. E. 1952. Rank analysis of in- completeblockdesigns:I.themethodofpairedcomparisons. *Biometrika*, 39(3/4): 324–345. Chen, X.; Ghadirzadeh, A.; Björkman, M.; and Jensfelt, P.
2019. Meta-learningformulti-objectivereinforcementlearn- ing. In*2019 IEEE/RSJ International Conference on Intelli-* *gent Robots and Systems (IROS)*, 977–983. IEEE. Chen, Y.-T.; Hung, W.; Wu, B.-S.; Hong, Z.-W.; and Hsieh,
P.-C. 2026. A Reward-Free Viewpoint on Multi-Objective Reinforcement Learning. In*The Fourteenth International* *Conference on Learning Representations*. Christiano, P. F.; Leike, J.; Brown, T.; Martic, M.; Legg, S.; and Amodei, D. 2017. Deep Reinforcement Learning from HumanPreferences. InGuyon,I.;Luxburg,U.V.;Bengio,S.; Wallach, H.; Fergus, R.; Vishwanathan, S.; and Garnett, R., eds.,*Advances in Neural Information Processing Systems*, volume 30. Curran Associates, Inc. Ding, L.; Zhang, J.; Clune, J.; Spector, L.; and Lehman, J.
2024. Quality Diversity through Human Feedback: Towards Open-Ended Diversity-Driven Optimization. In*Forty-first* *International Conference on Machine Learning*. Dong, H.; Xiong, W.; Pang, B.; Wang, H.; Zhao, H.; Zhou,
Y.; Jiang, N.; Sahoo, D.; Xiong, C.; and Zhang, T. 2024. RLHF Workflow: From Reward Modeling to Online RLHF. *Transactions on Machine Learning Research*. Dulac-Arnold,G.;Mankowitz,D.;andHester,T.2019. Chal- lenges of Real-World Reinforcement Learning.
Felten,F.;Talbi,E.-G.;andDanoy,G.2024. Multi-Objective Reinforcement Learning Based on Decomposition: A Tax- onomy and Framework.*Journal of Artificial Intelligence* *Research*, 79: 679–723. Fickinger, A.; Zhuang, S.; Hadfield-Menell, D.; and Russell,

S. 2020. Multi-principal assistance games.*arXiv preprint* *arXiv:2007.09540*. Fu, J.; Luo, K.; and Levine, S. 2018. Learning Robust Re- wards with Adverserial Inverse Reinforcement Learning. In *International Conference on Learning Representations*. Gao, L.; Schulman, J.; and Hilton, J. 2023. Scaling laws for rewardmodeloveroptimization. In*InternationalConference* *on Machine Learning*, 10835–10866. PMLR. Gunjal, A.; Wang, A.; Lau, E.; Nath, V.; He, Y.; Liu, B.; and Hendryx, S. M. 2025. Rubrics as Rewards: Reinforce- mentLearningBeyondVerifiableDomains. In*NeurIPS2025* *Workshop on Efficient Reasoning*. Haarnoja, T.; Zhou, A.; Abbeel, P.; and Levine, S. 2018. Soft actor-critic: Off-policy maximum entropy deep rein- forcement learning with a stochastic actor. In*International* *conference on machine learning*, 1861–1870. Pmlr. Hayes, C. F.; Rădulescu, R.; Bargiacchi, E.; Källström, J.; Macfarlane, M.; Reymond, M.; Verstraeten, T.; Zintgraf,
L.M.;Dazeley,R.;Heintz,F.;Howley,E.;Irissappane,A.A.; Mannion, P.; Nowé, A.; Ramos, G.; Restelli, M.; Vamplew,
P.; and Roijers, D. M. 2022a. A practical guide to multi- objectivereinforcementlearningandplanning.*Auton.Agent.* *Multi. Agent. Syst.*, 36(1). Hayes, C. F.; Rădulescu, R.; Bargiacchi, E.; Källström, J.; Macfarlane, M.; Reymond, M.; Verstraeten, T.; Zintgraf,
L. M.; Dazeley, R.; Heintz, F.; Howley, E.; Irissappane,
A. A.; Mannion, P.; Nowé, A.; Ramos, G.; Restelli, M.; Vamplew, P.; and Roijers, D. M. 2022b. A Practical Guide to Multi-Objective Reinforcement Learning and Planning. *Autonomous Agents and Multi-Agent Systems*, 36(1): 26. ArXiv:2103.09568 [cs]. Huang, S.; Abdolmaleki, A.; Vezzani, G.; Brakel, P.; Mankowitz, D. J.; Neunert, M.; Bohez, S.; Tassa, Y.; Heess,
N.;Riedmiller,M.;etal.2022. Aconstrainedmulti-objective reinforcement learning framework. In*Conference on Robot* *Learning*, 883–893. PMLR. Ibarz, B.; Leike, J.; Pohlen, T.; Irving, G.; Legg, S.; and Amodei, D. 2018. Reward learning from human preferences and demonstrations in atari.*Advances in neural information* *processing systems*, 31. Kirk,R.;Mediratta,I.;Nalmpantis,C.;Luketina,J.;Hambro,
E.; Grefenstette, E.; and Raileanu, R. 2024. Understanding the Effects of RLHF on LLM Generalisation and Diversity. In*The Twelfth International Conference on Learning Repre-* *sentations*. Knox, W. B.; Glass, B. D.; Love, B. C.; Maddox, W. T.; and Stone, P. 2012. How humans teach agents: A new experi- mentalperspective.*InternationalJournalofSocialRobotics*, 4(4): 409–421. Kouritem, S. A.; Abouheaf, M. I.; Nahas, N.; and Hassan,
M. 2022. A multi-objective optimization design of indus-

trial robot arms.*Alexandria Engineering Journal*, 61(12): 12847–12867. Lee, K.; Smith, L.; Dragan, A.; and Abbeel, P. 2021. B-Pref: Benchmarking Preference-Based Reinforcement Learning. In*Thirty-fifth Conference on Neural Information Processing* *Systems Datasets and Benchmarks Track (Round 1)*. Lee, K.; Smith, L. M.; and Abbeel, P. 2021. PEBBLE: Feedback-Efficient Interactive Reinforcement Learning via Relabeling Experience and Unsupervised Pre-training. In Meila, M.; and Zhang, T., eds.,*Proceedings of the 38th In-* *ternational Conference on Machine Learning*, volume 139 of*Proceedings of Machine Learning Research*, 6152–6163. PMLR. Lin, J.; Fried, D.; Klein, D.; and Dragan, A. 2022. Inferring Rewards from Language in Context. In*Proceedings of the* *60th Annual Meeting of the Association for Computational* *Linguistics (Volume 1: Long Papers)*, 8546–8560. Liu, H.; and Abbeel, P. 2021. Behavior from the void: Unsu- pervisedactivepre-training.*AdvancesinNeuralInformation* *Processing Systems*, 34: 18459–18473. Ma, Y. J.; Hejna, J.; Fu, C.; Shah, D.; Liang, J.; Xu, Z.; Kirmani, S.; Xu, P.; Driess, D.; Xiao, T.; Bastani, O.; Jayara- man, D.; Yu, W.; Zhang, T.; Sadigh, D.; and Xia, F. 2025. Vision Language Models are In-Context Value Learners. In Yue, Y.; Garg, A.; Peng, N.; Sha, F.; and Yu, R., eds.,*Inter-* *national Conference on Learning Representations*, volume 2025, 33984–34009. McCarthy, J. 1997. What is Artificial Intelligence? Stanford University. Also available in a 2007 version at http://www- formal.stanford.edu/jmc/whatisai.pdf. Mnih, V.; Kavukcuoglu, K.; Silver, D.; Graves, A.; Antonoglou, I.; Wierstra, D.; and Riedmiller, M. A. 2013. Playing Atari with Deep Reinforcement Learning.*CoRR*, abs/1312.5602. Mu, N.; Luan, Y.; and Jia, Q.-S. 2025. Preference-based multi-objective reinforcement learning.*IEEE Transactions* *on Automation Science and Engineering*. Munos, R.; Valko, M.; Calandriello, D.; Gheshlaghi Azar,

M.; Rowland, M.; Guo, Z. D.; Tang, Y.; Geist, M.; Mesnard,
T.; Fiegel, C.; Michi, A.; Selvi, M.; Girgin, S.; Momchev,
N.; Bachem, O.; Mankowitz, D. J.; Precup, D.; and Piot, B.
2024. Nash Learning from Human Feedback. In Salakhutdi- nov,R.;Kolter,Z.;Heller,K.;Weller,A.;Oliver,N.;Scarlett,
J.; and Berkenkamp, F., eds.,*Proceedings of the 41st Inter-* *national Conference on Machine Learning*, volume 235 of *Proceedings of Machine Learning Research*, 36743–36768. PMLR. Muslimani,C.;Johnstonbaugh,K.;Chandramouli,S.;Booth,
S.; Knox, W. B.; and Taylor, M. E. 2025. Towards Improving Reward Design in RL: A Reward Alignment Metric for RL Practitioners. In*Reinforcement Learning Conference*. Ng, A. Y.; and Russell, S. J. 2000. Algorithms for Inverse Reinforcement Learning. In*Proceedings of the Seventeenth* *International Conference on Machine Learning*, 663–670. Ouyang, L.; Wu, J.; Jiang, X.; Almeida, D.; Wainwright, C.; Mishkin,P.;Zhang,C.;Agarwal,S.;Slama,K.;Ray,A.;etal.
2022. Training language models to follow instructions with humanfeedback.*Advancesinneuralinformationprocessing* *systems*, 35: 27730–27744. Pásztor,B.;Buening,T.K.;andKrause,A.2025. Stackelberg Learning from Human Feedback: Preference Optimization as a Sequential Game. In*NeurIPS 2025 Workshop: Second* *Workshop on Aligning Reinforcement Learning Experimen-* *talists and Theorists*. Peschl,M.;Zgonnikov,A.;Oliehoek,F.A.;andSiebert,L.C.
2022. MORAL: Aligning AI with Human Norms through Multi-ObjectiveReinforcedActiveLearning. In*Proceedings* *of the 21st International Conference on Autonomous Agents* *and Multiagent Systems*, 1038–1046. Pierrot, T.; Richard, G.; Beguir, K.; and Cully, A. 2022. Multi-objective quality diversity optimization. In*Proceed-* *ingsofthegeneticandevolutionarycomputationconference*, 139–147. Rafailov, R.; Sharma, A.; Mitchell, E.; Manning, C. D.; Er- mon, S.; and Finn, C. 2023. Direct preference optimization: Your language model is secretly a reward model.*Advances* *in neural information processing systems*, 36: 53728–53741. Rame, A.; Couairon, G.; Dancette, C.; Gaya, J.-B.; Shukor,
M.;Soulier,L.;andCord,M.2023. Rewardedsoups:towards pareto-optimalalignmentbyinterpolatingweightsfine-tuned ondiverserewards.*AdvancesinNeuralInformationProcess-* *ing Systems*, 36: 71095–71134. Rodriguez-Soto, M.; Rodriguez-Aguilar, J. A.; Lopez- Sanchez, M.; and Nowé, A. 2023. Multi-objective rein- forcement learning for guaranteeing alignment with multiple values.*In 2023 Adaptive and Learning Agents Workshop at* *AAMAS.* Roijers, D. M.; Vamplew, P.; Whiteson, S.; and Dazeley,
R. 2013. A survey of multi-objective sequential decision- making.*Journal of Artificial Intelligence Research*, 48(1): 67–113. Ross, S.; Gordon, G.; and Bagnell, D. 2011. A reduction of imitation learning and structured prediction to no-regret on- line learning. In*Proceedings of the fourteenth international* *conference on artificial intelligence and statistics*, 627–635. JMLR Workshop and Conference Proceedings. Sener, O.; and Koltun, V. 2018. Multi-task learning as multi- objective optimization.*Advances in neural information pro-* *cessing systems*, 31. Shen, W. F.; Qiu, X.; Whitehouse, C.; Alazraki, L.; Goel, S.; Barbieri, F.; Willi, T.; Mathur, A.; and Leontiadis, I. 2026. Rethinking Rubric Generation for Improving LLM Judge and Reward Modeling for Open-ended Tasks.*arXiv preprint* *arXiv:2602.05125*. Shin, D.; Dragan, A. D.; and Brown, D. S. 2023. Bench- marks and Algorithms for Offline Preference-Based Reward Learning. ArXiv:2301.01392 [cs]. Siddique, U.; Sinha, A.; and Cao, Y. 2023. Fairness in Preference-based Reinforcement Learning. In*ICML 2023* *Workshop The Many Facets of Preference-Based Learning*. Silver, D.; Singh, S.; Precup, D.; and Sutton, R. S. 2021. Reward is enough.*Artificial intelligence*, 299: 103535.

Siththaranjan, A.; Laidlaw, C.; and Hadfield-Menell, D.

2024. Distributional Preference Learning: Understanding andAccountingforHiddenContextinRLHF. In*TheTwelfth* *International Conference on Learning Representations*. Skalse,J.M.V.;andAbate,A.2023. TheRewardHypothesis is False. Sorensen, T.; Moore, J.; Fisher, J.; Gordon, M. L.; Mireshghallah, N.; Rytting, C. M.; Ye, A.; Jiang, L.; Lu,
X.; Dziri, N.; Althoff, T.; and Choi, Y. 2024. Position: A Roadmap to Pluralistic Alignment. In Salakhutdinov, R.; Kolter, Z.; Heller, K.; Weller, A.; Oliver, N.; Scarlett, J.; and Berkenkamp, F., eds.,*Proceedings of the 41st International* *Conference on Machine Learning*, volume 235 of*Proceed-* *ings of Machine Learning Research*, 46280–46302. PMLR. Stiennon,N.;Ouyang,L.;Wu,J.;Ziegler,D.;Lowe,R.;Voss,
C.; Radford, A.; Amodei, D.; and Christiano, P. F. 2020. Learning to summarize with human feedback.*Advances in* *neural information processing systems*, 33: 3008–3021. Sutton, R. S.; and Barto, A. G. 1998.*Reinforcement learn-* *ing: an introduction*. Adaptive computation and machine learning. Cambridge, Mass: MIT Press. ISBN 978-0-262- 19398-6. Tan, J.; Zhang, T.; Coumans, E.; Iscen, A.; Bai, Y.; Hafner,
D.; Bohez, S.; and Vanhoucke, V. 2018. Sim-to-Real: Learn- ing Agile Locomotion For Quadruped Robots.*Preprint*. Teoh, J.; Varakantham, P.; and Vamplew, P. 2025. On Gen- eralization Across Environments In Multi-Objective Rein- forcement Learning. In*The Thirteenth International Con-* *ference on Learning Representations*. Tessler,M.H.;Bakker,M.A.;Jarrett,D.;Sheahan,H.;Chad- wick,M.J.;Koster,R.;Evans,G.;Campbell-Gillingham,L.; Collins, T.; Parkes, D. C.; Botvinick, M.; and Summerfield,
C. 2024. AI can help humans find common ground in demo- cratic deliberation.*Science*, 386(6719): eadq2852. Umer, M.; Mohsin, M. A.; Bilal, A.; Chaudhry, A.; Haupt,
A.; Koyejo, S.; Fox, E.; and Cioffi, J. M. 2026. Gen- eral Preference Reinforcement Learning.*arXiv preprint* *arXiv:2605.18721*. Vamplew, P.; Dazeley, R.; Berry, A.; Issabekov, R.; and Dekker, E. 2011. Empirical evaluation methods for multiob- jective reinforcement learning algorithms.*Machine learn-* *ing*, 84(1): 51–80. Vamplew, P.; Smith, B. J.; Källström, J.; Ramos, G.; Răd- ulescu, R.; Roijers, D. M.; Hayes, C. F.; Heintz, F.; Mannion,
P.; Libin, P. J.; et al. 2022. Scalar reward is not enough: A response to silver, singh, precup and sutton (2021).*Au-* *tonomous Agents and Multi-Agent Systems*, 36(2): 41. Van Seijen, H.; Fatemi, M.; Romoff, J.; Laroche, R.; Barnes,
T.; and Tsang, J. 2017. Hybrid reward architecture for re- inforcement learning.*Advances in neural information pro-* *cessing systems*, 30. Wang, Z.; Rahmani, S.; Cornelisse, D.; Sarkar, B.; Goldie,
A. D.; Foerster, J. N.; and Whiteson, S. 2026. Learning to Drive in New Cities Without Human Demonstrations. In *Workshop on Simulation for Autonomous Driving*.
White, D. 1982. Multi-objective infinite-horizon discounted Markov decision processes.*Journal of mathematical analy-* *sis and applications*, 89(2): 639–647. Wu,Z.;Hu,Y.;Shi,W.;Dziri,N.;Suhr,A.;Ammanabrolu,P.; Smith, N. A.; Ostendorf, M.; and Hajishirzi, H. 2023. Fine- grained human feedback gives better rewards for language model training.*Advances in Neural Information Processing* *Systems*, 36: 59008–59033. Xu, J.; Tian, Y.; Ma, P.; Rus, D.; Sueda, S.; and Matusik,

W. 2020. Prediction-guided multi-objective reinforcement learning for continuous robot control. In*International con-* *ference on machine learning*, 10607–10616. PMLR. Yang, R.; Pan, X.; Luo, F.; Qiu, S.; Zhong, H.; Yu, D.; and Chen, J. 2024. Rewards-in-Context: Multi-objective Align- ment of Foundation Models with Dynamic Preference Ad- justment. In*Forty-firstInternationalConferenceonMachine* *Learning*. Yang, R.; Sun, X.; and Narasimhan, K. 2019. A generalized algorithmformulti-objectivereinforcementlearningandpol- icy adaptation.*Advances in neural information processing* *systems*, 32. Ye, C.; Xiong, W.; Zhang, Y.; Dong, H.; Jiang, N.; and Zhang, T. 2024. Online Iterative Reinforcement Learning from Human Feedback with General Preference Model. In *The Thirty-eighth Annual Conference on Neural Information* *Processing Systems*. Yu, T.; Quillen, D.; He, Z.; Julian, R.; Hausman, K.; Finn,
C.; and Levine, S. 2020. Meta-world: A benchmark and evaluation for multi-task and meta reinforcement learning. In*Conference on robot learning*, 1094–1100. PMLR. Yuan, Y.; Zheng, Z.; Dong, Z.; and Hao, J. 2024. MOD- ULI: Unlocking Preference Generalization via Diffusion Models for Offline Multi-Objective Reinforcement Learn- ing. ArXiv:2408.15501 [cs]. Zhi-Xuan,T.;Carroll,M.;Franklin,M.;andAshton,H.2025. Beyond Preferences in AI Alignment: T. Zhi-Xuan et al. *Philosophical Studies*, 182(7): 1813–1863. Zhou, Z.; Liu, J.; Shao, J.; Yue, X.; Yang, C.; Ouyang, W.; andQiao,Y.2024. Beyondone-preference-fits-allalignment: Multi-objective direct preference optimization. In*Findings* *oftheAssociationforComputationalLinguistics:ACL2024*, 10586–10613. Zhu, B.; Dang, M.; and Grover, A. 2023. Scaling Pareto- Efficient Decision Making via Offline Multi-Objective RL. In*The Eleventh International Conference on Learning Rep-* *resentations*.

### Appendix A Extended Related Works

**VectorRewardsandtheLimitsofScalarReward.**Akey premise in modern RL is the*reward hypothesis*: that goals can be adequately captured by maximizing a single*scalar* reward (Silver et al. 2021). A growing body of work contests the sufficiency of this framing, arguing that many objectives ofinterestcannotalwaysbeexpressedbyscalarreward(Vam- plewetal.2022;SkalseandAbate2023;Bowlingetal.2023; Van Seijen et al. 2017) and are more naturally represented as *vectors*(Vamplew et al. 2022; Skalse and Abate 2023). Vec- tor rewards and Pareto-optimal policy sets are common in multi-objective decision-making (Roijers et al. 2013; Hayes et al. 2022b), where general policy optimization recovers the Pareto front by conditioning a single policy-network on a sampled weight vector. This literature, however, largely assumes the ground-truth vector reward function is given. The reward-free viewpoint of (Chen et al. 2026) relaxes part of this assumption by using preference-guided exploration as an auxiliary task, yet still requires the ground-truth multi- objectiverewardduringtraining.Incontrast,LEMURavoids these assumptions. Instead, it posits that true objectives are never directly observed and must be learned, in this case from preference feedback. Thus, the agent jointly learns re- wardmodelsandanoptimizedpolicythatbalancesitsvarious components.

#### Multi-Dimensional and Fine-Grained Preference Learn-

**ing.**StandardRLHFdistillshumancomparisonsintoasin- glescalarreward(Christianoetal.2017;Ouyangetal.2022), which can conflate distinct criteria and collapse the multi- objective structure of human values (Sorensen et al. 2024). A line of work therefore decomposes feedback into finer- grained components: Fine-Grained RLHF (Wu et al. 2023) attaches rewards to localized segments and categories, while Rewarded Soups (Rame et al. 2023) and MODPO (Zhou etal.2024)obtainaseparatesignalperobjectiveandexposea Paretofamilythroughweightinterpolationorscalarizedpref- erence optimization. These methods combine per-objective signals*post hoc*rather than jointly learning the rewards and a trade-off policy, and are developed almost exclusively for LLM post-training. A related direction forgoes the reward model entirely, optimizing the policy directly from prefer- ence data (e.g., DPO (Rafailov et al. 2023)); such methods are effective but train on static or periodically refreshed pref- erences, forgoing the online, interactive feedback and policy optimization, ideal for reliable reward learning under policy improvement(Christianoetal.2017;Lee,Smith,andAbbeel 2021;Gao,Schulman,andHilton2023;Baietal.2022;Ross, Gordon, and Bagnell 2011; Ibarz et al. 2018; Stiennon et al.

2020). A further perspective treats heterogeneous feedback as hidden context, learning a distribution over reward func- tions (Siththaranjan, Laidlaw, and Hadfield-Menell 2024); this captures*which*preferences are present but does not, on its own, optimize an explicit compromise between them. LEMURdiffersfromallthree:itlearnsanexplicit,objective- specificrewardmodelperfeedbackstream*online*,andjointly optimizes a set of policies over the resulting vector reward
in continuous control. A complementary line moves beyond the Bradley-Terry preference model assumption itself. Gen- eral preference models represent preferences with a richer (e.g., skew-symmetric,*k*-dimensional) structure that admits *intransitive*cycles, optimizing policies directly against this structure rather than a scalar reward (Umer et al. 2026). Re- lated game-theoretic formulations cast alignment as a Nash or Stackelberg equilibrium over preferences (Munos et al. 2024; Pásztor, Buening, and Krause 2025). Intransitivity is a different failure mode of scalar rewards from the one we study; it concerns the*shape*of preferences rather than the presence of multiple objectives, and we regard bridging it with multi-objective preference optimization as promising future work. In the LLM setting, rubric-based rewards have similarly been used to supply multi-dimensional supervision for reinforcement fine-tuning, though their reliability is sen- sitive to rubric coverage and correlated criteria (Gunjal et al. 2025; Shen et al. 2026). These directions are largely orthog- onaltoLEMUR,whichtargetsonlinevector-rewardlearning and trade-off policy optimization.

#### Connections to Diversity and Foundation-Model Post-

**Training.**Acontemporarylineofworkobservesthatscalar RL post-training induces*entropy collapse*, eroding the solu- tion diversity required by inference-time search (Kirk et al.

2024). Most directly, Vector Policy Optimization (Bahlous- Boldi et al. 2026) samples scalarizations over the reward simplex and trains a policy to output a set of solutions spanning the Pareto front, improving downstream best-of-*N* search. Such methods share LEMUR’s premise that collaps- ing a vector reward into a scalar discards useful structure. They differ from our setting in three respects: (i) they tar- get LLM*test-time search*, seeking a diverse candidate pool for a downstream selector, whereas LEMUR seeks a pol- icythat*compromises*betweenobjectives*duringdeployment*; (ii) they assume the reward components are*known and ob-* *servable*(e.g., per-test-case correctness), whereas LEMUR must*learn*them from feedback; and (iii) they operate on natural language generation rather than continuous control. We therefore treat this literature as motivating context rather than comparable works, and leave the study of train-time multi-objective learning from feedback to improve test-time diversity(Dingetal.2024;Pierrotetal.2022)asfuturework.
#### Pluralistic Alignment and Multiple Principals.

LEMUR’s multi-teacher formulation connects to*plu-* *ralistic alignment*, which holds that a single reward model cannot represent the plurality of human values (Sorensen et al. 2024) and that an agent should instead balance multiple objectives to reach a compromise across them. A closely related framing casts this as serving*multiple principals*: a single agent acting on behalf of several stakeholders must respect the preferences of each, turning alignment into the problemofrepresentingandtradingoffcompetingprincipals rather than satisfying one (Fickinger et al. 2020). How to reconcile these principals is itself contested. Naively aggre- gating preferences via RLHF has been shown to behave as a Borda count over latent objectives, with limited normative justification (Siththaranjan, Laidlaw, and Hadfield-Menell

2024), and others question whether aggregation is the right

LEMUR (2 3 Teachers) Teacher C Added 5000 4000 3000 Episode Returns(Objective One) 2000 1000 0

2000 (Objective Two) 1000 Episode Returns

2000 Episode Returns (Objective Three) 1000

0 0 1 2 3 4 5 6 7 8 Training Steps (×10)

Figure 6: **Adding a third teacher mid-training**

5 **(MO-Cheetah).**A third teacher is introduced at4*×*10 steps (dotted line) into an already-training two-teacher run. The new objective (bottom) is learned from scratch while the two existing objectives (top, middle) are preserved, so no retraining from scratch is required. Mean*±*std over five seeds.

frame at all, proposing non-aggregative alternatives for reconciling plural values (Zhi-Xuan et al. 2025). Practical efforts that do aggregate rely on curated consensus datasets or hand-specified aggregation functions (Bakker et al. 2022; Rodriguez-Soto et al. 2023; Tessler et al. 2024), both costly to obtain a priori and brittle when preferences shift during deployment. Rather than collapsing principals to a consensus in advance or assuming their reward functions are known, LEMUR preserves each principal’s objective as a separate learned reward model and recovers an explicit compromise through multi-objective optimization.

### B LEMUR Pseudocode

#### Algorithm 1: LEMUR

**Require:** Feedback frequency*K*, queries per session*M*, number of objectives*m* 1:Initialize policy*ϕ*and reward models*{ψj}* *m* *j*=1 2:Initialize shared buffer*B ←∅*and preference datasets *Dj←∅*

*int* 3: *B←*Explore(*πϕ,r*)*▷*Pre-training

4: **for**each iteration**do** 5: **if**iterationmod*K*== 0**then***▷*Reward learning 6: **for**each teacher*j∈{*1*,...,m}***do** 7:Sample queries(*σ⁰,σ¹*)*∼B* 8: *Dj←Dj∪{*(*σ⁰,σ¹,yj*)*}* *M* *n*=1 9:Updateˆ*ψrj*on*Dj*via cross-entropy loss 10: **end for** 11: **end if**

12:Collect transitions(*st,at,st*+1)with*πϕ*and store in *B* 13: **for**each gradient step**do***▷*Multi-objective policy optimization 14:Sample batch(*s,a,s* *′* )*∼B* 15:Relabel vector rewards: *rw*=w *⊤* ˆr*ψ*(*s,a*) 16:Update actor and critic using MO-SAC 17: **end for** 18: **end for**

5 at4*×*10 environment steps, with training continuing un- interrupted from the existing population. Figure 6 shows the outcome. The newly added Objective Three is optimized from a cold start and rises steeply once its teacher joins, while Objectives One and Two, already near convergence at the changepoint, are retained rather than degraded, settling into a marginally adjusted equilibrium that accommodates the new objective. Crucially, the framework absorbs the new preference source*online*, without reinitialising either the re- ward models or the policy population, demonstrating that the cost of adding a teacher is incremental rather than a full retraining cycle.

#### C.2 Non-Stationary Preferences

Human preferences are not static, and a teacher may revise its trade-off during the course of training. Since LEMUR re-queries every teacher and relabels the shared replay buffer at each feedback interval, a revised preference propagates into the learned reward and hence into the policy objective without any special-case handling. To test this, Teacher A’s weight vector is altered at2*×*10 5 steps mid-training. Figure7showsthatallthreeobjectivescontinuetoimprove monotonically across the changepoint: the policy adapts to the revised utility rather than collapsing or plateauing, and the widening variance band immediately after the change reflects the transient period during which the reward models are being re-fit to the new preference before the population re-converges.

### C Additional Experiments

#### C.1 Adding a Teacher Mid-Training

A practical deployment of preference-based MORL is un- likely to have a fixed, known set of stakeholders at the outset: new preference sources appear over time. A framework that requires retraining from scratch whenever a teacher joins is therefore of limited practical use. Because LEMUR main- tains one weight-conditioned reward model per teacher and couples them only through the shared MORL/D population, adding a teacher requires instantiating a single new reward model and extending the vector reward, leaving the existing reward models and the trained policy population intact. We test this directly: a run begins with the standard two- teacherMO-Cheetahsetupandathirdteacherisintroduced

LEMUR (Non-Stationary Preferences) Preference Change 4000 3000 Episode Returns(Objective One) 2000 1000 0

2000 Episode Returns (Objective Two) 1000

0 7000 6000 5000 4000 Episode Returns 3000 (Objective Three) 2000 1000 0 0 1 Training Steps (×10 2 3 4 ) 5

Figure 7: **Non-stationary preferences (MO-Cheetah).**

TeacherA’spreferencevectorischangedat2*×*10 5 steps(dot- tedline).Returnscontinuetoimproveacrossthechangepoint, indicating that the online re-query and buffer-relabeling loop tracks the revised utility. Mean*±*std over five seeds.

6000 Query Length 50 Query Length 35 5000Query Length 1 4000 3000 Episode Returns(Objective One) 2000 1000 0

2000 Episode Returns (Objective Two) 1000

00.0 0.5 1.0 1.5
Training Steps (×10

2.0 2.5 3.0 3.5
) 4.0
4.5
Figure 8: **Effect of query segment length (MO-Cheetah).**

Ground-truth return per objective for preference queries of length50(default),35and1transition, at a fixed budget of 300queries per teacher. Shading is*±*1std; the length-35and length-1arms are single seeds and carry a nominal band. Shorter segments learn faster early but plateau by*∼*2*×* 10 5 steps, while length50overtakes them and continues improving.

#### C.3 Ablation: Query Length

LEMUR elicits preferences over*trajectory segments*, deter- mining the behavioral context teachers see per comparison. At a fixed budget of 300 queries per teacher, we tested seg- ment lengths of 50, 35, and 1 transition (Figure 8). LEMUR maintains performance even with shorter segments of feed- back. The improvement in performance due to longer seg- ments is potentially due to more context for reward learning (Lee et al. 2021; Lee, Smith, and Abbeel 2021).

#### C.4 Ablation: Query Sampling Strategy

Wealsotestedif*which*segmentsarequeriedmattersatafixed budget and length. We compared LEMUR’s default uniform sampler against an entropy-based sampler that selects the most uncertain segment pairs from a 10*×*candidate pool (Figure 9). Entropy-based selection yields a modest gain in perfor- mance. Uniform sampling recovers most of the achievable return without requiring uncertainty estimates, candidate pools, or extra forward passes. Combined with our query- length findings, this shows that under a fixed budget,*how* *much behavior each query covers*matters significantly more than*which*specific segments are chosen.

#### C.5 Overlapping Preferences

Our main results consider teachers whose anchors are gen- uinely conflicting. A natural question is whether the ma- chinery required to resolve conflict imposes a cost when the teachers largely*agree*. We therefore repeat the experiment withoverlapping(near-aligned)teacherweightvectors,com- paring LEMUR against the ground-truth oracle upper bound

6000 Standard Uniform Sampling Entropy-Based Sampling 5000 4000 3000 Episode Returns(Objective One) 2000 1000 0 4000 3000

Episode Returns (Objective Two) 2000 1000

00.0 0.5 1.0 1.5 2.0 2.5 3.0 3.5 4.0 4.5
Training Steps (×10)

Figure 9: **Uniform vs. entropy-based query sampling**

**(MO-Cheetah).**Ground-truth return per objective for the default uniform sampler and an entropy-based sampler that scores a10*×*candidate pool by reward-model uncertainty. Shading is*±*1std; the entropy arm is a single seed and car- ries a nominal band. Entropy-based selection is consistently ahead, but by a small margin relative to the effect of query length (Figure 8).

LEMUR (Overlapping) Ground Truth Oracle (Overlapping) 6000 5000 4000 3000 Episode Returns(Objective One) 2000 1000 0 6000 5000 4000 3000 (Objective Two) 2000 Episode Returns 1000 0 0 1 2 3 4 5 6 7 Training Steps (×10)

Figure10: **Overlappingpreferences(MO-Cheetah).**With near-aligned teacher anchors, LEMUR converges close to the ground-truth oracle on both objectives, showing that the method degrades gracefully when teachers largely agree. Mean*±*std over five seeds.

under the same overlap condition.

Figure 10 shows that LEMUR tracks the oracle closely

on both objectives, converging to a comparable final return with only a modest lag in sample efficiency. This indicates that the weight-conditioned formulation degrades gracefully towardthesingle-preferencecase,whenthereislittleconflict to resolve.

#### C.6 Ablation: Varying Levels of Teacher Conflict

This ablation isolates the*degree*of teacher disagreement. HoldingMO-Cheetah, the MORL/D backbone, explorer, and query budget fixed, we sweep the anchors from mildly to severely opposed and train LEMUR alongside an Oracle given the same anchors at each level. Comparing against a per-levelOracleseparatesdegradationcausedbythetrade-off becomingharderfromdegradationcausedbyrewardlearning failing under disagreement. LEMUR remains competitive across the sweep (Figure 11).

#### C.7 Ablation: Weight-Conditioned Reward Model vs. Reward Ensemble

LEMUR’s central architectural choice is to condition each teacher’s reward model on a preference weight vector, rather than learning an ensemble of unconditioned reward models as in the earlier formulation. To isolate the contribution of this choice wehold everything else fixed, the sameMORL/D backbone, explorer, teacher anchors, and query budget, and vary only the reward model.

Figure 12 shows a substantial and consistent gap on

both objectives: the weight-conditioned model converges to6*,*812*±*39and4*,*404*±*22, against4*,*556*±*369and 2*,*902*±*245for the ensemble. The ensemble also exhibits an order-of-magnitude larger standard error, indicating greater seed-to-seed instability.

### D LEMUR Implementation Details

**TrainingDetails.**WeutilizetheMORL/Dalgorithm(Felten, Talbi, and Danoy 2024), a Multi-Objective Soft Actor-Critic (MO-SAC) implementation from the*MORL-Generalization* benchmark (Teoh, Varakantham, and Vamplew 2025). A summary of the hyperparameters is provided in Tables 3 and 4. In the initial*Exploration*phase (Stage 0), an intrinsic- motivationexplorerbootstrapsareplaybufferofenvironment transitions,runfor50,000timestepsonLunarLander,80,000 on Hopper, and 100,000 on Cheetah and MetaWorld. This bufferissharedidenticallywitheverybaseline,sonomethod receives more exploration data than another. In the*Reward Learning*phase (Stage 1), each of the*m* teachers trains its own*weight-conditioned*reward model: a 2-layer MLP with 256 hidden units that takes the state- action pair*concatenated with a preference weight vector* w, trained by Bradley–Terry cross-entropy over pairwise trajectory-segment comparisons of length*H*= 50. Rather than querying each teacher only at its own fixed anchorw*j*, weights are sampled from a Dirichlet distribution centred on that anchor with concentration*κ*= 30, so a single model generalises across a neighbourhood of the anchor instead of memorising one point on the simplex. At each iteration of reward-learning and policy-optimization, the per-teacher query budgets are*M*= 200(LunarLander),500(Hopper), and300(Cheetah, MetaWorld), each trained for 100 epochs with Adam optimizer. For*Multi-Objective Policy Optimization*(Stages 2-3), a population of 6 MO-SAC policies is trained on the*m*- dimensional learned vector reward, coupled by a shared re- play buffer, weighted-sum scalarization, PSA weight adap- tation, and weight transfer between neighbouring policies (neighbourhood size 2). Learning rates and exchange fre- quencies are adapted per environment (Table 4) while the population size is held constant at 6 across all environments. Crucially, reward learning does not terminate after Stage 1: everyfeedback_intervalsteps the pipeline re-queries all teachers, performs 30 online reward-update epochs, and *relabels the shared replay buffer*with the updated reward models,sothepolicyandtherewardmodelco-adaptthrough- out training.

### E Baselines Implementation Details

To ensure a fair comparison, all baselines share LEMUR’s Stage-0 explorer, scripted teacher weight vectors, query bud- get*M*,querylength,interactionfrequency*K*,reward-model capacity, and total environment-step budget, and are evalu- ated and logged under identical protocols (Tables 3 and 4). The primary distinction between methods therefore lies in *howconflictingrewardsignalsareaggregatedandoptimized*, not in the data or compute they receive. Each baseline retains its own defining reward-learning mechanism: MORAL’s adversarial AIRL rewards, Pb- MORL’s weight-conditioned Bradley–Terry model, and FP- bRL’sGGFwelfaremodel.Whereamethod’soriginalpolicy optimizer would place it at an unfair disadvantage in our en- vironments, we adapt*in the baseline’s favour*, upgrading

Medium Conflict Level (w=0.6/0.4) Hard Conflict Level (w=0.75/0.25) Harder Conflict Level (w=0.9/0.1) 6000 Medium Conflict Level (w=0.6/0.4) Medium Conflict Level Oracle 6000 Hard Conflict Level (w=0.75/0.25) Hard Conflict Level Oracle 6000 Harder Conflict Level (w=0.9/0.1) Harder Conflict Level Oracle 5000 5000 5000 4000 4000 4000 3000 3000 3000 Episode Returns(Objective One) 2000 2000 2000 1000 1000 1000 0 0 0 4000 4000 4000 3000 3000 3000 2000 2000 2000 Episode Returns (Objective Two) 1000 1000 1000

00.0
0.5 1.0 1.5 2.0 2.5 3.0 3.5 4.0 4.5
00.0
0.5 1.0 1.5 2.0 2.5 3.0 3.5 4.0 4.5
00.0
0.5 1.0 1.5 2.0 2.5 3.0 3.5 4.0 4.5
Training Steps (×10) Training Steps (×10) Training Steps (×10)

Figure 11: **Varying levels of teacher conflict (MO-Cheetah).**Each column is one conflict level, set by the teacher preference

anchors: medium (*w*= [0*.*6*,*0*.*4]*/*[0*.*4*,*0*.*6]), hard ([0*.*75*,*0*.*25]*/*[0*.*25*,*0*.*75]) and harder ([0*.*9*,*0*.*1]*/*[0*.*1*,*0*.*9]). Rows give each objective’sground-truthreturn.SolidlinesareLEMUR,dashedtheground-truth-rewardOracleundertheidenticalconfiguration; shading is*±*1std across seeds, with a common*y*-scale per row.

**Hyperparameter Value Hyperparameter Value**

*Exploration (Stage 0)* Explorer Timesteps 50,000 (LunarLander), 80,000 (Hopper), 100,000 (Cheetah, MetaWorld) Explorer Batch Size 128

|Explorer Timesteps|50,000 (LunarLander), 80,000 (Hopper), 100,000 (Cheetah, MetaWorld)||Explorer Batch Size|128|
|---|---|---|---|---|
|Explorer Policy / Q LR3×10||Reward Learning (Stage 1)|Optimizer|Adam|
|Reward Model|Weight-conditioned MLP (2-layer)||Hidden Dim|256|
|Reward Learning Rate5e-4(LL),3e-4(Hopper),2.5e-4(Cheetah),1.5e-4(MetaWorld)|||Reward Batch Size|64|
|Queries per Teacher (M)|200 (LL), 500 (Hopper), 300 (Cheetah, MetaWorld)||Query Length (H)|50|
|Reward Epochs|100 (All Environments)||Loss|Bradley–Terry CE|
|Dirichlet Concentrationκ30.0 (All Environments)||Online Reward Updates (Stages 2–3)|Optimizer|Adam|
|Online Update Epochs|30||Buffer Relabeling|True|

*−*4

Table 3: Hyperparameters for Exploration (Stage 0) and Reward Learning (Stage 1).

**Hyperparameter Value Hyperparameter Value** Algorithm MORL/D (MO-SAC) Batch Size 512 (LL, MetaWorld), 1024 (Hopper, Cheetah)

|Algorithm|MORL/D (MO-SAC)|Batch Size|512 (LL, MetaWorld), 1024 (Hopper, Cheetah)|
|---|---|---|---|
|MORL Timesteps|100,000 (LL), 750,000 (Hopper, Cheetah), 500,000 (MetaWorld)|Target Entropy Scale|0.3|
|Policy LR5e-5(LL),3e-4(Hopper, Cheetah),1e-4(MetaWorld)||Optimizer|Adam|
|Q LR5e-5(LL),1e-4(Hopper, MetaWorld),3e-4(Cheetah)||Discount Factorγ0.99||
|Population Size|6 (All Environments)|Shared Buffer|True|
|Exchange Frequency|5,000 (LL), 10,000 (Hopper, Cheetah, MetaWorld)|Weight Transfer|True|
|Weight Adaptation|PSA|Neighborhood Size|2|
|Scalarization|Weighted Sum (ws)|||

Table 4: Hyperparameters for Multi-Objective Policy Optimization (Stages 2–3).

**Hyperparameter Value Hyperparameter Value**

*PbMORL (Mu, Luan, and Jia 2025)* Reward Model Weight-conditioned MLP Hidden Dim 256

|Reward Model|Weight-conditioned MLP||Hidden Dim|256|
|---|---|---|---|---|
|Query Budget (M)|300 (total, split across teachers)||Query Length (H)|50|
|Reward LR / Epochs2.5e-4/ 100|||Reward Batch Size|64|
|Optimizer (policy)|Envelope (LunarLander), MORL/D (Others)|FPbRL (Siddique, Sinha, and Cao 2023)|Population Size|6|
|Reward Model|GGF welfare MLP (K-dim)||Hidden Dim|256|
|Query Budget (M) / Length|300 / 50||Reward LR / Epochs2.5e-4/ 100||
|Policy Algorithm|PPO (continuous), SAC-discrete (LunarLander)||Policy LR3e-4||
|PPO Steps / Iter|2,048||PPO Minibatches|32|
|PPO Update Epochs|10||PPO Clip Coef|0.2|
|GAEλ0.95|||GGF Weights|Decreasing on sorted utilities|

Table 5: Hyperparameters for the PbMORL and FPbRL baselines.

#### Hyperparameter Value Hyperparameter Value

*Stage 0 & 1: Expert Collection & AIRL Reward Inference* 6 Expert Timesteps1*×*10 Demo Episodes 50

|Expert Timesteps1×10||Demo Episodes|50|
|---|---|---|---|
|Expert Net Arch.|256, 256|Expert Batch Size|256|
|Expert Policy / Q LR3×10||Expert Buffer Size1×10||
|Expertα/τ0.2 / 0.005||Expert Learning Starts|10,000|
|AIRL Hidden Dim|32|AIRL Generator Timesteps|200,000|
|AIRL Disc. Update Interval|1,024|AIRL Gen. Net Arch.|256, 256|
|AIRL Gen. Buffer / Batch|300,000 / 256|Optimizer|Adam|

*−*4 6

Table 6: MORAL (Peschl et al. 2022): hyperparameters for expert demonstration collection and adversarial AIRL reward

training.

|Hyperparameter|Value|Hyperparameter|Value|
|---|---|---|---|
||Stage 2: Online Policy Optimization with Active Learning|||
|Policy Algorithm|SAC (all environments; see App. E)|Active Query Budget|5,000|
||− 4|||
|Policy / Q LR3|× 10|Query Interval|200|
|Batch Size|256|Scalarization Posterior|Bradley-Terry|
|Discount Factor|γ 0.99|Query Strategy|Volume removal|

Table 7: MORAL (Peschl et al. 2022): hyperparameters for online policy optimization (Stage 2). Note we optimize with SAC

rather than the original work’s PPO; see Appendix E.

Weight-Conditioned (LEMUR) Reward Ensemble 5000 4000 3000 Episode Returns(Objective One) 2000 1000 0

2000 (Objective Two) Episode Returns 1000

0 0 1 2 3 4 5 6 7 Training Steps (×10)

Figure 12: **Reward-model ablation (MO-Cheetah).**The

weight-conditioned reward model substantially outperforms the reward-ensemble variant on both objectives under an identical optimizer, explorer, and query budget. Mean*±*std over five seeds.

the optimizer rather than reproducing the paper verbatim, so that reported gaps reflect differences in reward learning and preference aggregation, the object of study, rather than differences in policy optimization. Most notably, MORAL is optimized with SAC rather than the PPO used in the original work, substantially improving its sample efficiency on our continuous-control tasks. All such deviations are disclosed below.

**Utilitarian Agent.**This baseline imposes an*a priori* scalarization on the objectives. Like LEMUR, it learns*m* distinct reward models*{*ˆ*ψrj}* *m* *j*=1, one per teacher, but rather than learning a set of trade-off policies it trains a*single*SAC agent to optimize their arithmetic mean:

X *m* <u>1</u> *r* util(*s,a*) = ˆ*ψrj*(*s,a*)*.*(3) *m* *j*=1

Learning rates, batch sizes, and buffer sizes are identical to LEMUR, with the population size set to1(standard single- objective SAC).

**Naive Data Pooling.**This baseline aggregates conflicting preferences at the*data*level, mimicking standard RLHF ap- plied to heterogeneous feedback. Rather than maintaining separate datasets*Dj*per objective, all feedback tuples are S*m* stored in a single monolithic dataset*D*pool=*j*=1*Dj*, over which one reward modelˆpool*r* is trained to minimize the cross-entropy loss. The policy is then trained with standard SAC to maximize

*r* naive(*s,a*) = ˆpool*r* (*s,a*)*.*(4)

As with the Utilitarian baseline, we use the environment- specific hyperparameters in Table 4 with the population size fixed to1.

**PbMORL (Mu, Luan, and Jia 2025).**The original Pb- MORLassumesasingle,internally-consistentteacherwhose preferencesarevalidunderanysampledscalarizationweight, andthereforehasnomechanismformultiple,independently- opinionated teachers. We retain its weight-conditioned*m*- dimensional reward model, trained with the Bradley–Terry cross-entropy objective over pairwise trajectory compar- isons, and extend it to our setting in the two most nat- ural ways: *PbMORL-naive*pools all teachers’ preferences into one shared weight-conditioned model, while*PbMORL-* *utilitarian*trains a separate model per teacher and combines them at inference by a fixed uniform average. Each teacher answers every query under its own fixed weight vector, ex- actly as in LEMUR. The original paper pairs its reward model with Envelope Q-learning (Yang, Sun, and Narasimhan 2019), a discrete, value-based method. We retain this paper-faithful pairing on LunarLander, but Envelope’s Q-network requires an argmax over actions and is structurally inapplicable to continuous control; on Hopper, HalfCheetah, and MetaWorld we there- fore substitute MORL/D (Felten, Talbi, and Danoy 2024), the same population-based optimizer LEMUR uses. This is theonlystructuralsubstitution,anditequalizestheoptimizer between PbMORL and LEMUR on those environments, iso- lating the reward-learning strategy as the sole difference.

**FPbRL (Siddique, Sinha, and Cao 2023).**We implement FPbRL’s*K*-dimensional welfare reward model, trained from Generalized Gini Welfare (GGF)-based preferences over the same*K*= 2scripted teachers across which LEMUR and the other baselines compromise. At each policy-update iter- ation, the learned*K*-dimensional reward is scalarized by the GGF weight assignment, which places the largest weight on the currently worst-off objective, refreshed from a running per-objective return estimate, the standard practical form of Siddique et al.’s fair policy gradient. Unlike MORAL, we retain PPO for continuous-action en- vironments, matching the original paper: FPbRL’s fair pol- icy gradient is formulated for an on-policy optimizer, and substituting an off-policy method would alter the method’s semantics rather than simply strengthen it. On LunarLander we use SAC-discrete, as no discrete PPO implementation is used elsewhere in our pipeline. In addition to the per-teacher returns reported for all methods, we log FPbRL’s own fair- ness metrics (welfare, coefficient of variation, and minimum objective), so that it is also evaluated on the criterion it is explicitly designed to optimize.

**MORAL(Peschletal.2022).**WereimplementMORAL’s pipeline in three stages: (i) two expert policies are trained on the ground-truth per-teacher scalarized reward and used to collect demonstrations; (ii) for each teacher, an AIRL (Fu, Luo, and Levine 2018) discriminator is trained*adversar-* *ially*against a live generator, rather than against a fixed pool of shuffled expert transitions, which would render train- ing non-adversarial, yielding a per-teacher learned reward *g*(*s*); and (iii) an active-learning wrapper scalarizes the two frozen AIRL rewards with a Bradley-Terry weight poste- rior, updated online via volume-removal preference queries, which a single-objective policy optimizes. Since the original

MORAL was evaluated only on grid-world tasks, we adopt the AIRL hyperparameters and network architectures of Fu et al. (Fu, Luo, and Levine 2018) for our high-dimensional MuJoCo experiments; these are detailed in Tables 6 and 7. WedeliberatelypreserveMORAL’sdefiningcontribution, adversarial IRL reward learning combined with an actively-

0.600
queried scalarization posterior, and do not replace it withObjective One Weight

0.575Objective Two Weight
our own preference-based reward model, as doing so would0.550 no longer constitute a MORAL baseline. We do, however, 0.525 strengthen its policy optimization: the original work uses0.500

0.475
PPO, whereas we optimize with SAC (SAC-continuous, or

0.450
SAC-discreteonLunarLander)acrossallenvironments.This0.425 Learned preference weight 0.400 off-policy upgrade materially improves MORAL’s sample efficiency under an identical environment-step budget and0 1 2 3 4 5 6 7 Training Steps (×10) matches the backbone family used by LEMUR, ensuring MORAL is not penalized for an on-policy optimizer choice Figure 13: **MORAL’s learned scalarisation weights in** unrelated to its reward-learning contribution. **(MO-Cheetah).**The two components of MORAL’s active- query scalarisation posterior over training.

**E.1 MORAL Baseline: Learned Weights and Optimiser Choice** **Learnedscalarisationweights.**MORALmaintainsapos- terior over a scalarisation weight vector, refined through ac- tive queries, and it is this posterior, rather than a per-teacher rewarddecomposition,thatcarriesitsnotionofwhoseprefer- encesthepolicyisserving.Figure13tracksbothcomponents over training. **SAC vs. PPO.**As described in Appendix E, we optimize the MORAL baseline with SAC rather than the PPO used in theoriginalwork,onthegroundsthatanon-policyoptimizer would disadvantage the baseline for reasons unrelated to its
MORAL (SAC) reward-learning contribution. This ablation verifies that theMORAL (PPO) 100 substitutionisgenuinelyfavourabletoMORALandtherefore that our reported comparison is conservative. 200

Figure 14 confirms this: holding MORAL’s adversarial

Episode Returns(Objective One) AIRL reward learning and active-query scalarisation poste-300 rior fixed and varying only the policy optimizer, the SAC variant dominates PPO on both objectives throughout train-400 ing,andthegapwidensastrainingproceeds.ThePPOvariant 100 additionallydisplaysapronouncedsawtoothcharacteristicof on-policy updates (shown here under heavy smoothing). Re-200 portingMORALwithSACthereforestrengthensthebaseline 300 relative to a faithful reproduction of the original paper, and Episode Returns(Objective Two) the weight collapse in Figure 13 is a property of MORAL’s400 scalarization posterior rather than a symptom of the opti-500 0 1 2 3 4 5 6 7 mizer. Training Steps (×10)

Figure 14: **MORAL optimizer ablation (MO-Cheetah).**

### F Additional Results

WithMORAL’srewardlearningheldfixed,SACoutperforms

**F.1 Multi-Objective RL Metrics** the original work’s PPO on both objectives, confirming that
our SAC upgrade strengthens the baseline. Curves are heav- Evaluating a multi-objective agent requires assessing the ily smoothed to expose the trend beneath PPO’s on-policy *set*of policies it recovers rather than any single return, oscillation. Mean*±*std over five seeds. so we adopt two metrics standard in the MORL litera- ture (Hayes et al. 2022a; Roijers et al. 2013). Let*P*= *{J*(*π₁*)*,...,J*(*πP*)*}*denote the set of objective-value vec- tors attained by the learned policy population.

**Hypervolume (HV).**Given a reference pointzdominated by all solutions, Hypervolume is the volume of the region

dominated by*P*and bounded byz,   [ HV(*P,*z) = Λ [z*,*p]*,*(5) p*∈P*

whereΛis the Lebesgue measure. It simultaneously rewards solutions that are high-performing (pushing the front out- ward) and diverse (covering more of the objective space), and is the most widely adopted MORL quality indicator be- cause it is the only common metric strictly monotonic with Pareto dominance: any set that dominates another is guaran- teed a higher score (Roijers et al. 2013). We use the refer- encepointsuppliedbythe*MORL-Generalization*benchmark (Teoh, Varakantham, and Vamplew 2025) so that values are comparable across methods within an environment; absolute magnitudes are not comparable*across*environments, since theydependonboththereferencepointandtherewardscale.

**Sparsity (SPS).**Sparsity measures how evenly solutions are distributed along the recovered front. Sorting the*|P|* ˜ solutions by each objective*i*and writing *Pi*(*k*)for the*k*-th value,

X *m |P|−*X¹ 2 <u>1</u> ˜ ˜ SPS(*P*) = *Pi*(*k*)*− Pi*(*k*+ 1)*,*(6) *|P|−*1 *i*=1 *k*=1 withlowervaluesindicatingmoreuniformcoverage(Xuetal.

2020). Sparsity must be read alongside Hypervolume rather than independently: a degenerate front that collapses to a single solution reports a low, apparently favourable value despite failing to cover the objective space, which is why we report both. This is the case for FPbRL, whose fixed welfare scalarization converges to a single policy, so no front is recovered and sparsity is undefined (*−*) on three of four environments. **Environment LEMUR PbMORL FPbRL**
**Hypervolume (***↑***)** LunarLander1*.*10*×*104 6 *±*2*.*46*×*102 5

1*.*09*×*104*±* 6
2*.*87*×*1025*.*05*×*103
4 *±*5*.*75*×*102 4 Hopper3*.*67*×*10 7 *±*2*.*01*×*10 5

2*.*24*×*10 7 *±*0*.*000 7*.*19*×*10
5 *±*2*.*04*×*10 5 HalfCheetah4*.*86*×*10 6 *±*9*.*45*×*10 5

4*.*78*×*10 6 *±*0*.*000 5
7*.*73*×*10 6 *±*2*.*91*×*10
5 MetaWorld-DrawerClose2*.*15*×*10 *±*6*.*49*×*10 1*.*43*×*10 *±*4*.*43*×*10 2*.*79*×*10 *±*3*.*39*×*10 **Sparsity (***↓***)** LunarLander134*.*57*.*8*−* Hopper294*.*71731*.*7*−* HalfCheetah294*.*72191*.*0*−* MetaWorld-DrawerClose436*.*3 5564*.*70*.*000

Table 8: Hypervolume and Sparsity across benchmark envi-

ronments.FPbRL’sfixedwelfarescalarizationfailstorecover asetoftrade-offpolicies,converginginsteadtoasinglesolu-

|Metric|LEMUR|PbMORL|FPbRL|
|---|---|---|---|
|Spearman ( ρ↑ )0|. 710 ± 0. 0050|. 705 ± 0. 000|0. 512 ± 0. 089|
|Pearson ( r↑ )0|. 863 ± 0. 0030|. 853 ± 0. 000|0. 493 ± 0. 065|
|VOC ( ↑ )0|.. 863 ± 0 .. 003|.. 853 ± 0 .. 000|00 .. 493 ± 0 .. 065|
|VOC (traj) ( ↑ )0|858 ± 0 0030|0 851 ± 0 000|494 ± 0 066|
|Kendall τ (policy) (|↑ )0. 939 ± 0. 0300|. 933 ± 0. 000|0. 567 ± 0. 233|
|Traj-Alignment Coeff (|↑ )0. 898 ± 0. 0410|. 858 ± 0. 000|0. 633 ± 0. 233|

tion:sparsityisthereforeundefined(*−*)wherenofrontexists, and its near-zero value on MetaWorld-DrawerClose reflects this collapse rather than uniform coverage. PbMORL is de- terministic under our protocol on Hopper and HalfCheetah, hence zero variance.

ground-truthteacherutilities,followingPbRLbenchmarking practice (Lee et al. 2021). Letˆ*ψrj*denote teacher*j*’s learned rewardmodeland*r* (*s,a*) =w *⊤* r(*s,a*)itsground-truthutil- *j j* ity,whereristheenvironment’snativevectorrewardandw*j* teacher*j*’s scripted weight vector. All metrics lie in[*−*1*,*1], higher is better, and are averaged across the*m*teachers.

**Per-state correlation.**Over states sampled from evalua- tionrollouts,*Spearman*rankcorrelationmeasureshowfaith- fullythelearnedrewardordersindividualtransitions.Itisour primary metric because preference-based rewards are iden- tifiable only up to a positive monotone transform, making an order-preserving measure the appropriate notion of cor- rectness. We also report*Pearson*correlation on raw values, which is stricter in penalising any nonlinear distortion; fol- lowing prior reward-evaluation work we refer to this as the *Value-Order Correlation*(VOC) (Ma et al. 2025).

**Trajectory and policy ranking.**Per-state correlation can be high even when a reward model induces the wrong or- dering over whole*behaviours*, which is what the policy ultimately optimizes. We therefore roll out each policy in the MORL/D population and compare the induced rankings using Kendall’s*τ*-b over trajectory returns, and the*Trajec-* *toryAlignmentCoefficient*(TAC)of(Muslimanietal.2025), computed identically but on*discounted*returns so that align- mentis weightedby thesame temporaldiscounting theagent optimizes.*Trajectory VOC*additionally averages the within- trajectory correlation between learned and ground-truth per- step reward sequences, capturing whether the model tracks the shape of the signal within an episode rather than only across episodes.

**Results.**Tables9-11reportallmetrics.LEMURattainsthe strongest per-state correlations on every environment, with the largest margins on Hopper and MetaWorld-DrawerClose where the teachers’ anchors are most opposed, consistent with per-teacher decomposition mattering most under gen- uine conflict. Trajectory-level metrics are more mixed: FP- bRL attains a higher Kendall*τ*and TAC on Hopper despite substantially weaker per-state correlation, reflecting that its welfare scalarization orders whole behaviours consistently even where the underlying reward is poorly calibrated. Re- porting both families is what makes this distinction visible, and we recommend the same practice for future work in this setting.

#### F.2 Reward Model Evaluation Metrics

Policy return alone cannot distinguish a reward model that has genuinely recovered a teacher’s utility from one merely correlated with it on the visited state distribution. We there- fore evaluate the learned reward models directly against the

Table 9: Reward-Model Evaluation Metrics : HalfCheetah.

### G Benchmark Environment Details

Table 12 summarises the native multi-objective struc-

ture of each benchmark environment and the scripted

|Metric|LEMUR|PbMORL|FPbRL|
|---|---|---|---|
|Spearman ( ρ↑ )0|. 520 ± 0. 0070|. 231 ± 0. 000|0. 085 ± 0. 074|
|Pearson ( r↑ )0|. 589 ± 0. 0200|. 335 ± 0. 000|0. 345 ± 0. 005|
|VOC ( ↑ )0|. 589 ± 0. 0200|. 335 ± 0. 000|0. 345 ± 0. 005|
|VOC (traj) ( ↑ )0|. 340 ± 0. 035|0. 339 ± 0. 0000|. 358 ± 0. 010|
|Kendall τ (policy) (|↑ )0. 359 ± 0. 0020|. 291 ± 0. 000|− 0. 167 ± 0. 100|
|Traj-Alignment Coeff (|↑ )0. 347 ± 0. 0260|. 300 ± 0. 000|0. 167 ± 0. 167|

steps. This mirrors the forward-reward/control-cost decom- position standard to the MuJoCo suite, but applied to a more complex robot-manipulation domain. Teacher A is rewarded by task completion, Teacher B by smooth, energy-efficient actuation.

**Environment Actions***m***Native Objectives Teacher Weights**(w*A*;w*B*)

Table 10: Reward-Model Evaluation Metrics: MetaWorld-MO-LunarLander

MO-HopperContinuous Discrete 34 shaping, main-engine cost, side-engine cost, landing forward velocity, jump height, energy cost[0 [0*..*6 8 *,,*0 0

*..*3 1 *,,*0 0
*..*05 1]; *,* [0
0*..*05] 3*,*0 ;[0
*.*5*,.*0 6
*.,*2]
0*.*05*,*0*.*3*,*0*.*05]
DrawerClose.MO-Cheetah MO-MetaWorld Continuous (Drawer-Close)Continuous 22 forward velocity, control cost task progress, control effort[0 [0*..*66*,,*00*..*4]4];;[0 [0*..*44*,,*00*..*6]6]

Table12:Benchmarkenvironments:nativeobjectivedecom-

|Metric|LEMUR|PbMORL|FPbRL|
|---|---|---|---|
|Spearman ( ρ↑ )0|. 945 ± 0. 0020|. 527 ± 0. 000|0. 648 ± 0. 094|
|Pearson ( r↑ )0|. 951 ± 0. 0020|. 532 ± 0. 000|0. 716 ± 0. 073|
|VOC ( ↑ )0|. 951 ± 0. 0020|. 532 ± 0. 000|0. 716 ± 0. 073|
|VOC (traj) ( ↑ )0|. 947 ± 0. 0040|. 606 ± 0. 000|0. 714 ± 0. 073|
|Kendall τ (policy) (|↑ )0. 914 ± 0. 002|0. 291 ± 0. 0000|. 933 ± 0. 000|
|Traj-Alignment Coeff (|↑ )0. 856 ± 0. 014|0. 370 ± 0. 0000|. 933 ± 0. 000|

position and scripted teacher weight vectors.*m*denotes the dimensionality of the native vector reward.

### H Compute Resources

Table 11: Reward-Model Evaluation Metrics: Hopper. Inallexperiments,weuse12CPUsandasingleGPU,oftype

either NVIDIA A100 or L40. Training in all environments takes approximately three to five hours on average. teacher weight vectors used throughout our experiments. In every case, teacher*j*’s ground-truth utility is the linear scalarisation*rj*(*s,a*) =w*j⊤*r(*s,a*)of the envi- ronment’s native vector rewardr, and it is this quan- tity thatvalidation/gt_teacher_{a,b}_return tracks during training. The weight vectors are chosen to be genuinely conflicting: each teacher places its largest weight on a different objective, so no single policy can simultane- ously maximise both utilities.

**MO-LunarLander.**A four-objective variant of the classic LunarLanderdomainwithadiscreteactionspace,takenfrom the MORL-Generalization benchmark (Teoh, Varakantham, and Vamplew 2025). The native reward vector comprises the shaping term (progress toward the landing pad), the main- engine fuel cost, the side-engine fuel cost, and the terminal landing/crash outcome. Teacher A weights the two engine- cost terms asymmetrically against Teacher B, producing a fuel-allocation conflict on top of a shared landing objective.

**MO-Hopper.**A three-objective continuous-control lo- comotion task in which the native reward vector is [*vx, h,−c∥a∥* 2]: forward velocity, hop height, and a negated energy/control cost. Teacher A ([0*.*8*,*0*.*1*,*0*.*1]) strongly prefers fast locomotion, while Teacher B ([0*.*3*,*0*.*5*,*0*.*2]) prefers a higher, more energy-efficient and stable gait.

**MO-Cheetah.**A two-objective continuous- control task whose native reward vector is [reward_forward*,*reward_ctrl], i.e. forward velocity against control cost. The teacher anchors[0*.*6*,*0*.*4] and[0*.*4*,*0*.*6]place opposing emphasis on velocity versus energy efficiency.

**MO-MetaWorld**(Drawer-Close). Meta-World tasks are natively*single*-objective, providing only a dense task- progress reward. We convertDrawer-Closeinto a two- objective task by pairing this native reward with a control- effort penalty, yielding the vector reward[*r*task*,−λ∥a∥* 2] with control-cost weight*λ*= 0*.*1and a fixed horizon of 500
