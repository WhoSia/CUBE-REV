# CUBE-REV 0.22 — P0: Task-Relative Physical Belief Sufficiency, Action-Labelled Decision Congruence & Prior-Sensitive Policy Separation

**User-confirmed active version title (2026-10-10):** CUBE-REV 0.22 — Cost-Sensitive Physical Identification & Finite-State Decision Semantics: Exact Turn–Observation Pareto Geometry, Task-Relative History Sufficiency, Observation-Automaton Structure & Evidence-Constrained Human Search.

**Canonical Notion:** https://app.notion.com/p/3f5ef561cf9281d8b77ede12f15718d3 (new child of unchanged 0.21 historical version).

**P0 result:** REAL_RUBIK_PHYSICAL_66_PAIR_ACTION_PROFILE_PASS / SAME_SCALAR_VALUE_NOT_ACTION_CONGRUENCE / PRIOR-SENSITIVE_OPTIMAL_ACTION_COUNTEREXAMPLE_PASS / BELIEF_SUFFICIENCY_INHERITED / MINIMAL_BELIEF_CONTROLLER_HOLD.

## 1. Inherited authority: no fabricated novelty reset

Previous CUBE-REV Generation III research established important GENERAL theories: [G3-P23 claim-preserving quotient](https://app.notion.com/p/3ddef561cf92819983c7fc9b6066ac82), [G3-P26 intervention-stable congruence](https://app.notion.com/p/3ddef561cf9281209cb3d5140c368fa5), [G3-P27 dynamic quotient and separating tests](https://app.notion.com/p/3deef561cf928163b86ed1882b9a606e), and [G3-P29 persistent-state belief times accumulated-path sufficiency](https://app.notion.com/p/3deef561cf928164ba09e6f1bfaf022f). Classical POMDP posterior sufficiency, Moore minimization, Myhill–Nerode-style congruence and finite partition refinement are NOT original to P0.

The existing physical instance is from [0.15 sticker-derived UR edge](../../scripts/cuberev-015/ur-fiber-tomography.mjs), [0.21 P7 joint (7,4) worst-case optimum](../0.21/P7_JOINT_TURN_QUERY_OPTIMALITY_REAL_RUBIK_AND_EXACT_FMC_EVENT_POSET_COMPLETIONS.md), and [0.21 P8 exact cost-Pareto (71,45),(74,44) and 24-state Moore minimality](../0.21/P8_EXACT_TURN_QUERY_MEAN_COST_PARETO_MOORE_MINIMALITY_AND_BELIEF_SUFFICIENCY.md).

New original finite-instance result: the following exact source-specific physical counterexamples to invalid *control-memory* compressions, NOT new general universal theory.

## 2. Exact physical/decision model

The 18 legal 3×3 HTM face moves are regenerated from the original full-sticker transform. One tracked UR physical edge has 24 position/orientation states. The original initial edge orientation is zero and initial location is one of 12 slots. Only the tracked edge's intrinsic flip bit is observable after an optionally inspected physical turn. This is not normal human cube vision, real FMC search, or a photographic camera. Source probabilities below are mathematical assumptions, not human measurements.

For known reversible transitions T_a, observation O, fixed prior and a fixed source-identification objective, the current weighted posterior distribution b over transported physical states and remaining turn/read budgets (h,q) is sufficient for optimal future control by Bayesian induction. With the original uniform initial prior and deterministic permutations, posterior mass stays uniform on the surviving candidates, and a support bitmask suffices for future *control*. For arbitrary priors, masses matter. Naming the actual **initial slot** at termination may additionally require the accumulated known action permutation or an explicit origin-label map, as distinguished already in G3-P29; reaching singleton current support does not itself encode an initial-slot name.

## 3. Physical theorem P0-A: four exact one-turn action-labelled decision profiles

For each unordered pair of initial zero-flip edge slots, define the set D(i,j) of legal actions a such that the post-turn intrinsic orientation bits of the two physically transported candidate cubies differ. There are exactly C(12,2)=66 source pairs.

| One-turn orientation-splitting legal actions | Number of pairs |
| --- | ---: |
| F and F-prime only | 16 |
| B and B-prime only | 16 |
| Both front and back quarter-turn families | 16 |
| No one-turn action splits the two source candidates | 18 |

These four classes are exhaustive. 48 original pair beliefs can be identified with one legal move plus one orientation read. For each of the remaining 18, legal two-move transport followed by a read can separate the pair, verified directly using original sticker-derived permutations. The 4+4+4 front/back/equatorial physical support decomposition also gives a hand combinatorial proof: three off-diagonal cross-category 4×4 pair families, and 3×C(4,2) same-category pairs.

**Value equality is not reusable control congruence.** The pair belief over starting slots {0,1} has one-turn splitting actions {F,F-prime}. The pair {0,3} instead has {B,B-prime}. Both have scalar optimal unit-turn cost 1 under a one-turn one-read identification task, but choosing F from their merged scalar-value state fails for {0,3}. A generally reusable quotient for labelled actions must preserve the action/output/successor transition structure, not just a single optimal value.

This is task-relative: a quotient for a different restricted permitted-action set can be different. Nor does this finite result prove a globally minimum belief-controller state count.

## 4. Physical theorem P0-B: the same geometric support can require disjoint optimal first actions under different priors

Fix one legal initial support S={0,1,3}, slot order shown. Compare **two different hypothetical priors**, not two alleged posterior distributions from a single frozen initial experiment:

- Prior A (0.05,0.90,0.05): after F and one orientation read, slot 1 is isolated with probability 0.90. On the two-source remaining branch {0,3}, B and an orientation read uniquely separate the pair. Expected number of face turns = 0.90×1+0.10×2 = **1.10**. The complete set of optimal first turns is {F,F-prime}.
- Prior B (0.05,0.05,0.90): after B and one orientation read, slot 3 is isolated with probability 0.90. On the remaining {0,1} branch, F and a read separate the pair. Expected face turns again **1.10**. The complete set of optimal first turns is {B,B-prime}.

Any one-turn binary query can immediately identify at most one of the three possible initial slots. Therefore universal information bound E[T]≥1+(1−max_i p_i)=1.10. Both policies attain it. A first-turn read which does not isolate the 90%-mass source leaves that source in a nonsingleton branch and incurs expected cost at least 1.90; a silent first move cannot end before two moves. Hence the two optimal initial-action sets are genuinely disjoint. The same unweighted support does not suffice for Bayesian optimal decisions across differing priors.

The 0.9 parameter is chosen only to yield an explicit counterexample; do not interpret it as human cognitive frequency or measured cost.

## 5. Distinct objects; do not conflate minimum state claims

1. Physical 24-state Moore machine: under *all legal continuation words*, distinct individual hidden states have distinct future output profiles (0.21 P8). This is an ontology-level state minimality.
2. Posterior over 24 states plus budgets: a provably sufficient *controller state* under fixed dynamics/goal/prior. No new claim its entire reachable belief-state automaton is minimal.
3. Uniform-prior support bitmask: sufficient specifically when posterior weights are uniform; arbitrary priors defeat this compression.
4. Candidate count and one scalar residual cost: insufficient for action-labelled control, as physical P0 witnesses show.
5. Retrospective 8 FMC case graphs: legitimate small-N evidence of stated human search choices, not proof of imagined hidden cognition nor source of physical bit-oracle parameters. No new participants, video, or VFMC-session engineering.

The next task-relative belief congruence must explicitly freeze an admissible action/observation alphabet and termination-cost interface and check that all matched states have response-consistent successors *under each labelled action*, not merely equal Bellman numbers. G3-P26 dynamic refinement is a direct formal antecedent. Controller quotient minimality, horizon dependence, and nonuniform-prior transport await separate finite proofs.

## 6. Exact independently executed certificate

[P0 real-sticker physical verifier](../../scripts/cuberev-022/verify-p0-physical-task-history-counterexamples.mjs) enumerates all 66 2-source masks, verifies 16/16/16/18 full action signature partition, checks two-move separability of 18 one-step-inseparable pairs, identifies cost-equal/action-incompatible pair states, scans physically achievable two-step 3-source plans, and verifies disjoint optimal first-turn sets across two priors. All physical action maps are imported from the original 0.15 sticker-derived 18-move oracle.

[GitHub Actions #38051049160 — SUCCESS](https://github.com/WhoSia/CUBE-REV/actions/runs/38051049160) at commit caabe9a0566c048951ebc25a6ad61ea753b3db0b. [Proof/witness artifact #11668824627](https://github.com/WhoSia/CUBE-REV/actions/runs/38051049160/artifacts/11668824627), SHA-256 dadac939febe8d0d46ce42836a0d349a13e7e7e82dcaa459e7f50ffd73461d6f. Existing unrelated legacy P7 repository active-set governance audit failures are not disguised as P0 experiment failures or silently edited.

**Boundary:** P0 is CLOSED as a precise real-physical counterexample-and-sufficiency court. FULL reachable optimal belief-controller minimization, effects of arbitrary priors/observation errors, and actual human search-mechanism claims remain OPEN/HOLD.

## 7. P1 candidate

**CUBE-REV 0.22 P1 — Task-Conditioned Belief Congruence & Minimal Costed Controller Quotients: Horizon-Relative Residual Experiments, Action-Labelled Refinement, Prior-Transport Obstructions & Physical Separation Certificates.**

This is a proposed stage heading, not a concluded theorem. Start with physical reachable beliefs and labelled continuation signatures, specify terminal outputs and costs, and prove an actual quotient-minimality certificate. Avoid using the 24-state Moore-machine minimality as an illicit substitute for belief-controller memory minimality.
