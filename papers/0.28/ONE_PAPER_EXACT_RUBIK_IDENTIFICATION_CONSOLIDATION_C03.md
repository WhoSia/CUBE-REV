# WORKING UNIFIED PAPER — When Does Exact Observability Saturate? Two Observation Regimes on the Rubik Group

**Consolidated draft C0.3 (2026-11-13), with the R14-P8.40–P8.41 adaptive threshold update. NOT SUBMISSION-READY.**

**Editorial lineage:** C0.3 succeeds [single-paper C0.2](ONE_PAPER_EXACT_RUBIK_IDENTIFICATION_CONSOLIDATION_C02.md) and [C0.1](ONE_PAPER_EXACT_RUBIK_IDENTIFICATION_CONSOLIDATION_C01.md). [Paper A D0.5](RADIUS_RESTRICTED_CUBIE_OBSERVATION_DRAFT_01.md) and [Paper B D0.8](DUAL_COLOR_PROBE_ADAPTIVE_IDENTIFICATION_DRAFT_01.md) remain unchanged as full technical source documents. This is an *A-led, B-supported comparative case-study candidate*, not a proof that sensor counts in A and frame counts in B are commensurable, or a universal group-observability theorem. Mathematical proofs, executable certificates, exact remote CI outcomes and external novelty must be evaluated separately.

## Provisional title

**When Does Exact Observability Saturate? Radius-Restricted Tagged-Cubie Bases and Adaptive Color Probing in the Rubik Group**

## Abstract

We examine zero-error state identification in the legal fixed-center Rubik group under two physically distinct deterministic sensing protocols. In the first, a sensor reveals the complete location and orientation of a persistently identified original corner or edge cubie, and the unknown state lies in a word-metric ball \(B_r\). Existing independently implemented radius-six certificates give an optimum of sixteen permanent tags, attained by precisely 156 of the \(\binom{20}{16}=4845\) possible designs. We revalidate a sharp transition at the next radius: \(b_7=18\), with 96 optimal eighteen-tag designs, and prove the stronger **complete identifying-family saturation** \(\mathcal I(B_7)=\mathcal I(G)\), not merely equality of minima. The full family contracts from 1,023 identifying designs on \(B_6\) to exactly 117 on \(B_7\), losing 906 designs. Eight explicit physical words of length at most fourteen, split into two legal radius-seven states and conjugated under proper cube rotations, furnish collision witnesses for all 28 corner pairs and 66 edge pairs. An independently written 48-moving-sticker verifier checks 720 rotated state-pair instances; the implication from such pair collisions to a necessary sensor hitting condition is separately kernel-checked in Lean 4.34.1. Consequently the full-group tagged-sensor threshold is attained on the much smaller \(B_7\), well before the full group is reached in word-metric radius. In the second, each observation frame returns one six-category color on a spatial edge facelet and one on a spatial corner facelet, with known legal inter-frame turns allowed at zero *frame* cost. Existing separate physical certificates establish an exact nonadaptive minimum of 21 frames, and the adaptive minimum is exactly 19 frames. A constructive policy attains 19, and an exact minimax computation excludes 18 even with full corner information supplied at the outset. These results illustrate two non-equivalent mechanisms of exact identification—finite-radius collision saturation under rich permanent labels and feedback advantage under weak categorical observations—within one precisely defined puzzle group. The static pair-cover and adaptive belief-recursion formulations are standard mathematics; originality is claimed, provisionally, only for the particular finite cube-case classifications and complete policies after model-equivalent prior-art screening.

**Keywords:** Rubik group, exact identification, radius-restricted stabilizers, permanent cubie tags, collision support, adaptive distinguishing sequences, group-equivariant sensing, executable certificates.

## 1. Introduction: a single scientific question, two legitimate answers

What aspects of a legal puzzle's state become recoverable from a limited measurement channel, and when does either a larger reachable-state domain or access to feedback force greater observational resources?

Both experiments concern exactly the same physical state space \(G\), its legal group constraints and deterministic observation functions. They differ in three scientifically meaningful parameters: the hidden domain (\(B_r\) versus all of \(G\)), the sensor channel (full original-cubie identity/location/orientation versus a spatial sticker's categorical color), and the allowed decision rule (one static set versus an adaptive sequence of paired queries). They therefore do **not** share a single numerical optimization target.

We deliberately begin with the sharply classified full-tag radius threshold; a second theorem compares preset and adaptive schedules only **within** the low-information color channel. We do not infer human cognitive mechanisms, camera noise performance or turn-time optimality from either exact mathematical result.

**Contributions and evidence levels.**

1. A newly re-executed radius-six physical benchmark, \(b_6=16\) with 156 optimum layouts and 432 inclusion-wise minimal layouts across sizes 16 and 17; 41 independent C++ 12-HTM negative-distance searches now have fresh execution receipts. This result and its full 41-target shortest-distance proof are inherited from the preceding independent P48 audit, not re-executed in the C0.2 editorial cycle.
2. A newly **revalidated, not newly discovered** sharp radius-six-to-seven jump \(b_6=16\to b_7=18\) for persistent original-cubie tags. The full 28+66 two-tag collision support family is witnessed by eight physical word seeds, 24 spatial rotations and explicit two-B7-state splits. The associated \(b_r=18\) stabilization for all \(r\ge7\) is an elementary consequence of the global eighteen-tag upper bound.
3. Exact whole-group thresholds of 21 fixed and 19 adaptive paired frames. The lower bound uses a full corner oracle and exhaustive residual edge matching.
4. Reproducibility boundaries: standalone physical 48-facelet checks, historical permutation transport, and a genuinely completed Lean kernel proof of the conditional pair-hitting implication; no assertion that the entire physical word dataset has been imported into Lean.

## 2. State space, sensor semantics and common combinatorics

Let \(T\) contain the 18 symmetric face moves in the half-turn metric (HTM) of the fixed-center \(3\times3\times3\) Rubik group \(G\), and let \(\ell_T(g)\) be minimal word length. Define \(B_r=\{g\in G:\ell_T(g)\le r\}\). Classical legality constraints are even edge flips, zero total corner twist modulo 3 and matching parity of edge and corner permutations.

For a finite hidden-state set \(X\), deterministic queries \(q\in Q\), and outcomes \(O_q(x)\), the difference support of two distinct states is
\[
D_{x,y}=\{q\in Q:O_q(x)\neq O_q(y)\}.
\]
A static family \(S\subseteq Q\) identifies \(X\) if and only if \(S\cap D_{x,y}\neq\varnothing\) for all \(x\neq y\). This is the standard test-cover/hitting-set equivalence, **not** a new result.

For an adaptive channel on a current belief set \(C\subseteq X\), let
\[
C_{q,a}=\{x\in C:O_q(x)=a\}.
\]
The usual finite minimax recursion chooses a query minimizing the largest feasible successor's remaining depth. A sound compression of \(C\) must preserve full future query/outcome partitions; candidate-set size or coarse parity counts are not generally lossless. The two sensing regimes instantiate this language with different query families and costs.

### 2.1 Regime A: persistent tagged original cubies

Let \(\Omega=C\sqcup E\), \(|C|=8\), \(|E|=12\). A selected tag \(u\) reports the complete original cubie's current spatial position and orientation. The set of tags \(S\subseteq\Omega\) is selected once and read jointly. Define
\[
b_r=\min\{|S|:\pi_S|_{B_r}\text{ is injective}\}.
\]
Here a known intervening cube turn changes the reported coordinates deterministically and cannot create new information about an already completely observed original tagged cubie.

For \(H_S\), the legal whole-group pointwise stabilizer of the fully observed tags, standard word-metric ball factorization gives
\[
\pi_S|_{B_r}\text{ injective }\iff H_S\cap B_{2r}=\{e\}.
\]
Indeed, \(B_r^{-1}B_r=B_{2r}\) for a symmetric word metric, and equality of two full-tag signatures holds exactly when their relative group element belongs to \(H_S\). This is an elementary lemma under the specified action and comparison conventions.

### 2.2 Regime B: paired spatial six-color facelet probes

One frame reports the ordered color pair at one **spatial edge sticker** and one **spatial corner sticker**. There are 24 moving edge and 24 moving corner facelet slots, hence 576 possible paired spatial queries. Known physical face turns may be performed and undone at zero *observation-frame* charge. No query returns the original cubie's identity directly. The hidden state ranges over all \(G\), whose order is
\[
|G|=\frac{12!\,2^{11}\,8!\,3^7}{2}
=43{,}252{,}003{,}274{,}489{,}856{,}000.
\]
Let \(h_{\rm fixed}\) and \(h_{\rm adaptive}\) minimize worst-case paired observation frames for a fixed and a color-feedback query schedule, respectively. These are *not* directly comparable to \(b_r\).

## 3. First main result: the exact static observation phase transition

### Theorem A — radius-six optimum (inherited P48 physical certificate)

For Regime A, \(b_6=16\), with exactly 156 identifying subsets of size sixteen among 4845 size-sixteen candidates. The 156 optima form eight orbits under the proper cube rotation group of order 24.

The complete physical proof package classifies all size-sixteen choices by 872 irredundant short-support obstructions, a 41-class exact stabilizer-distance positive certificate for the survivors, and a separate no-fifteen lower bound. The prior [independent P48 MITM CI run 41774686324](https://github.com/WhoSia/CUBE-REV/actions/runs/41774686324), checkout `1b69b54`, was revisited and its five batches of 41 target successes were verified from logs. The historical CI ZIP was actually downloaded, its SHA-256 matched the original upload log, all 12 embedded manifest checksums were checked, 41/41 target PASS and 4,845 layout receipts were inspected, and the full ZIP was [preserved to Drive and independently byte-read back](https://drive.google.com/file/d/1FHQVSfwMsEartPjPqdYlIb09vDjUA0Ge/view). See the [machine-readable custody record](../../data/0.28/R14_P832_20261111_RESTORED_B6_41_TARGET_CI_ZIP_SHA256_CUSTODY.json). This is a new verification of a **historical execution receipt**, not a fresh 41-target numerical rerun or recovery of the separate October 30 original archive. The full [Paper A D0.5](RADIUS_RESTRICTED_CUBIE_OBSERVATION_DRAFT_01.md) and its independent P48 scripts remain the scientific source. This theorem is conditional on successful preservation/reproduction of that finite prior certificate for a future external release.

**P8.33 fully new 41-target distance computation and raw custody (2026-11-13).** The historic 2026-11-04 artifact is now supplemented by a *fresh* successful read-only [GitHub Actions run 43349579675](https://github.com/WhoSia/CUBE-REV/actions/runs/43349579675): `b6_independent_48sticker_goals.py --emit` regenerated the 48-sticker-derived factor table and 41 canonical goals, their **three SHA-256 hashes all matched** the byte-sealed historical result, and a newly authored C++ MITM implementation (not an import of the prior C++ verifier) enumerated 8,240,087 radius-six states from 8,331,112 normalized paths. All 41 targets were probed through 8,331,112 normalized right-side paths each, **341,575,592 total probes**, with no radius-twelve intersection, proving lower HTM distance ≥13 for those target actions. The new complete [ZIP computational receipt](https://drive.google.com/file/d/1wBw8zCFs4pBXzRMx2ONOCWCZDLZKZSec/view) was SHA-checked after GitHub download and Drive *re-download* byte comparison, and its [machine-readable custody manifest](../../data/0.28/R14_P833_20261113_FRESH_B6_41_TARGET_FULL_REPLAY_AND_DRIVE_SEAL.json) and [methodological note](../../docs/0.28/20261113_R14_P833_FRESH_B6_FULL_41_MITM_AND_DRIVE_CUSTODY.md) preserve the distinction between re-executed computation and the generator's mathematical 156-layout to 41-distance-class quotient. The missing 2026-10-30 B5 historical ZIP remains a separate research-provenance item; it is **not an input** to this newly executed P48 physical proof path.

**Corollary (inherited B6 minimality spectrum).** There are 156 inclusion-wise minimal identifying sets of cardinality 16 and 276 of cardinality 17, and none of larger cardinality, so there are 432 inclusion-wise minimal sets. Minimality-by-inclusion is not the same as minimum cardinality. This finite closure system is not matroidal, as its minimal generators have different sizes. The 156 size-sixteen layouts have an exchange graph with 336 edges and 25 connected components in the previously certified model.

### Theorem B — full pair collision support already within the radius-seven ball (revalidated)

For **each** unordered pair of distinct original corners \(\{c,c'\}\), there exist distinct legal states \(x,y\in B_7\) that agree on the complete position-and-orientation readings of all original cubies except possibly those two corners, and differ on exactly those two. The analogous assertion holds for every pair of original edges.

There are precisely \(\binom82=28\) possible corner pairs and \(\binom{12}2=66\) edge pairs.

**Constructive proof spine.** Eight explicit HTM words, each of length 12, 13 or 14, produce physical permutations with changes confined to precisely two original cubie tags. For each seed word \(w=ps\), each cut for which \(\ell(p),\ell(s)\le7\) yields two legal states \(s^{-1},p\in B_7\). The inverse-prefix/suffix construction \(p^{-1},s\in B_7\) must also be included: its *original-label* support need not coincide with that of the first construction, even when the endpoint permutation has the same abstract cycle type. Conjugation by each of the 24 proper spatial cube rotations preserves legal HTM radius and transports the original-cubie support. An independent, no-import 48-moving-sticker coordinate engine verifies **720** rotated two-state physical collision checks and exhaustive support coverage 28/28 and 66/66. This avoids a full B7 breadth-first enumeration and requires no assumption that the eight seed words are geodesics.

The same original group representation was independently compared with Zassenhaus (1982)'s 48-sticker generators through 288 explicit equivariant source-to-coordinate maps in R14-P8.29. That verification is a representation transport test, not an independent B7 shortest-distance proof.

**Corollary B1 — exact tagged-sensor saturation radius.**
\[
\boxed{b_7=18,\qquad b_r=18\ \text{for every } r\ge7.}
\]
**Proof.** If a selected sensor family omits at least two corners, Theorem B supplies a pair of distinct B7 states with identical readings on every selected original tag; the same applies when at least two edges are omitted. Hence any identifying tag set must contain at least seven corners and eleven edges, so its cardinality is at least eighteen. Conversely, observing all but at most one corner and one edge fixes the unobserved position/permutation uniquely and the unobserved orientations by the mod-3 corner twist and mod-2 edge flip constraints. Such a set identifies every legal cube state, hence also B7; eighteen tags suffice. This upper bound and monotonicity in r imply saturation for all r≥7. QED.

**Corollary B2 — all optimal saturated layouts.** At radius seven and globally, the 96 optimal 18-tag families are exactly those omitting **one** of eight corners and **one** of twelve edges, \(8\cdot12=96\). There are four proper-rotation orbits of 24 layouts each (as checked by the earlier exact orbit code). In conjunction with the inherited radius-six theorem, the first radius attaining the full-group minimum sensor count is exactly seven. Every one of the 156 inherited B6-optimal sixteen-tag layouts first fails at B7, conditional on the B6 positivity proof.

**Why the transition matters.** The physical cube group has not been exhausted at radius seven. Yet the family of pair ambiguities *needed to force the global minimum observation budget* is already complete by that radius. This is a finite-case example of early **observation-cost saturation**, not a claim of early state-space saturation and not a new abstract group theorem.

**Corollary B3 — saturation of the entire identifying-set family (stronger than minimum-cost saturation).** Let
\[
\mathcal I(X)=\{S\subseteq\Omega:\pi_S\text{ is injective on }X\}.
\]
Then
\[
\boxed{\mathcal I(B_7)=\mathcal I(G)
=\{S\subseteq\Omega:|S\cap C|\ge7,\ |S\cap E|\ge11\}.}
\]
**Proof.** If a selected family omits two corners or two edges, the complete physical pair-collision certificate from Theorem B supplies a distinct pair in \(B_7\) that the sensors cannot distinguish. Therefore every member of \(\mathcal I(B_7)\) observes at least seven corners and eleven edges. Conversely, such observations uniquely determine every legal cube state by the one-missing-piece permutation and orientation-sum constraints, so these families already belong to \(\mathcal I(G)\). The converse inclusion \(\mathcal I(G)\subseteq\mathcal I(B_7)\) is automatic. QED.

There are precisely \(\binom87\binom{12}{11}=96\) identifying designs of size 18, twenty of size 19 and one of size 20: **117 total**. The separately established full radius-six family comprises 156 sixteen-tag, 672 seventeen-tag, 174 eighteen-tag, 20 nineteen-tag and one twenty-tag design: **1,023 total**. Consequently the transition \(B_6\to B_7\) destroys **906** previously sufficient designs: 156 of size 16, 672 of size 17 and 78 of size 18. No 19- or 20-tag design is lost.

The independent [P8.34 exhaustive 1,048,576-subset audit](https://github.com/WhoSia/CUBE-REV/actions/runs/43350675032) reconstructs all 872 physically grounded B6 obstruction supports and all 94 P8.30 physically verified B7 two-tag supports, applies a complete upward support-closure census and checks the exact \(1{,}023\to117\) family collapse. It is a **derived classification**: the positive side for B6 uses the separately successful P8.33 41-target MITM proof. The new [P8.34 complete receipt ZIP](https://drive.google.com/file/d/1LzA07XNgexLT7nYJmCowjd3hB5-2Ei1Y/view) has been downloaded, hashed, stored in Drive and read back byte-for-byte.

This strengthens the descriptive conclusion: **the entire zero-error permanent-sensor identifying family, not only its minimum cardinality, becomes identical to the whole-group family at radius seven**. It does not claim the state set itself reaches the full group by radius seven.

### 3.3 Verification scope of Theorem B

The prior B7 collision-completion scripts already made the exhaustive pair-support claim; this draft expressly credits that earlier internal lineage. The new P8.30 verifier independently rederived the physical check in a second standalone geometry engine. Its [remote GitHub Actions run](https://github.com/WhoSia/CUBE-REV/actions/runs/42973939189) finished SUCCESS, including 720 checks and a read-only repository gate. The P8.31 Lean 4.34.1 kernel [build](https://github.com/WhoSia/CUBE-REV/actions/runs/42974864873) proves an abstract, conditional statement: a selected identifying set must hit each witnessed two-tag collision support. **Lean has not yet recomputed the physical eight turn words, rotations or all 94 supports internally.** This distinction is part of the proof release contract.

## 4. Second main result: adaptive advantage under categorical observations

### Theorem C — fixed versus adaptive frame complexity

For Regime B,
\[
\boxed{h_{\rm fixed}=21,\qquad h_{\rm adaptive}=19.}
\]
The fixed lower certificate excludes all twenty-frame preset schedules. The 21-frame fixed construction is realizable under tracked legal turns. The worst-case feedback advantage within this channel is two frames.

**Constructive upper bound.** [P8.40](../../docs/0.28/20261113_R14_P840_CONSTRUCTIVE_19_FRAME_UPPER.md) starts with one facelet on each of eleven edges. The policy adapts over the remaining locations and uses the shared permutation sign after the fourteenth response. Symmetry transport and exhaustive checks on 52 representative games establish coverage. Physical addressability is checked on all 576 joint locations.

**Unrestricted lower bound.** [P8.41](../../docs/0.28/20261113_R14_P841_EXACT_ADAPTIVE_19_FRAME_THEOREM.md) gives the observer the complete corner state and arbitrary access to original edge coordinates. An exact matching recurrence tracks the remaining labels, single-read colors, and both residual parity constraints. Both initial sign sectors lose at depth 18. A separate explicit-coordinate implementation verifies both roots and checks its recursion against literal decision trees on smaller beliefs.

## 5. Comparative synthesis: common formal questions, non-equivalent resource laws

The two regimes give two concrete answers to a shared *methodological* question—when does exact reconstruction become identifiable? Regime A enlarges the unknown-state domain while fixing a rich, permanent sensor set; its budget saturates at radius seven because complete two-original-tag collision supports are present. Regime B fixes the entire legal state domain and a sparse spatial color channel; its feedback access improves the worst-case frame budget relative to preset queries. These are neither two measurements of the same \(h\) nor a direct reduction from Theorem B to Theorem C.

The common mathematical operations are (a) pairwise difference supports, (b) zero-error distinguishing signatures, (c) group-equivariant transportation of physical certificates and (d) belief-state refinements. An identifying *static* set must hit all pairwise difference supports, while an *adaptive* strategy needs a rooted decision tree whose every feasible leaf is a singleton. These established general principles are useful for comparing proof structures; they do not imply that 16 permanent sensors “equal” 19 low-information observation frames.

The current kernel-checked generic Lean lemmas establish conditional hitting and abstract observation correspondence only. They do not yield a new numerical optimality theorem across the two regimes, and the manuscript is defensible as one article **only if** the case study's scientific question and proof protocol are considered sufficiently coherent by external reviewers.

## 6. Relation to prior work, model risks and falsification

**R14-P8.36 primary-source close reading and verified custody (13 November 2026).** We obtained and directly read all three previously metadata-only cube-related original PDFs, verified the bibliographic identities with conference/publisher records, computed SHA-256 for the exact stored bytes, and moved all three original files metadata-only from Research OS `00_INTAKE` to `10_PAPERS`, preserving file IDs and bytes. Full [source-by-source critical audit](../../docs/0.28/20261113_R14_P836_THREE_PRIMARY_PAPERS_CLOSE_READ_GHOST_AUDIT_AND_CUSTODY.md) and [physical custody register](../../data/0.28/R14_P836_20261113_THREE_SCHOLARLY_PDF_CANONICAL_INTAKE_SHA256.json). The three originals have **no longer** an outstanding missing-PDF status.

- **Image-rich camera regime is not our exact low-bandwidth categorical site-probe regime.** [Wang, Wang, Shi and Li (2022)](https://doi.org/10.1109/ICSPS58776.2022.00141), *Research on State Recognition of Rubik's Cube Based on Monocular Vision*, IEEE ICSPS 2022, 777–780 (IEEE indexed in 2023), combines HSV/KNN pixel classification, cube contours and geometric keyframe detection with AR/Kociemba operation guidance. Its Section IV reports 20 repeated guided restoration demonstrations; its approximately 20 **solving turns** (Section III.C) must **never** be confused with our 20 paired categorical **observation frames**, and its one physical camera captures far more information per exposure than two facelet-color outcomes. In particular the printed introduction's rounded legal Rubik state count is unreliable; use the independently verified legal group cardinality 43,252,003,274,489,856,000 instead. [Verified original IEEE PDF in 10_PAPERS](https://drive.google.com/file/d/1ny5tJVihORd9BxDwrYsBymKLYDmMBhXN/view) (4 pages, restricted publisher-access markings, do not redistribute source bytes).
- **Near-admissible learned search heuristics do not certify exact word-metric exclusions.** [Futuhi and Sturtevant (2026)](https://mlanthology.org/iclr/2026/futuhi2026iclr-learning/), *Learning Admissible Heuristics for A*: Theory and Practice*, ICLR 2026, introduce a Cross-Entropy Admissibility loss and sample-complexity/generalization analysis for neural approximations to Rubik PDB heuristics. Their Table 2 has small **nonzero** overestimation rates, e.g. 2×10⁻⁵ (7 edges) and 3×10⁻⁷ (8 corners); therefore this heuristic's reported empirical accuracy is not an exact lower-distance proof for **every** target. Our P8.33 positive B6 sensor certificate uses genuinely exhaustive 41-target exact HTM midpoint enumeration. The [stored arXiv:2509.22626v2 PDF](https://drive.google.com/file/d/15GM1mtoAicpgEwgafy7QQt3VxVvEaDF3/view) carries ICLR 2026 conference front matter; source-version identity is recorded without falsely asserting bytes identical to the publisher's final copy.
- **The per-original-cubie 24-pose encoding is pre-existing, not an original result.** [Harker, Vogel and Gedeon (2007)](https://doi.org/10.1007/s10851-007-0024-7), *Analysis of Constrained Optimization Variants of the Map-Seeking Circuit Algorithm*, *J. Math. Imaging Vis.* 29, 49–62, explicitly represent each original corner or edge cubie as a 24-valued one-hot pose variable (8×3 and 12×2) in Section 2.2. They study multilinear correspondence maximization and compare MSC, PG and SQP solvers on **100 random cube states at each scramble length 2–12** (Section 5.2); these are neither full exact B6/B7 identifying-set classifications nor a zero-error color-feedback decision-tree result. Their conclusions do not prove generic global convergence of MSC. [Verified publisher-layout 14-page journal PDF](https://drive.google.com/file/d/1P4XAjtmSI3O6FazqQhQKPUclqQ48P-S9/view).

**Novelty limits.** Identifying sets, abstract hitting-set conditions, 24-valued cubie factors, classical permutation-group base methods, color cameras and generic sequential-machine distinguishing experiments predate this work. Candidate new mathematical statements are the **specified finite exact** static restriction/saturation results and **specified finite exact** categorical-probe feedback bounds only, pending a full model-equivalent literature search and independent expert review. Do not extrapolate a public-paper claim from this three-source bibliography screen.

Classical permutation-group base/stabilizer methods (Sims, Blaha, Jerrum; Bailey and Cameron) explain much of the group-action vocabulary. Metric dimension and graph resolving-set work use distance responses and cannot be directly substituted for tagged-cubie pose measurements. Matroidal exchange questions about irredundant permutation bases require distinct premises, as illustrated by Cameron–Fon-Der-Flaass, Boutin and Dalla Volta–Mastrogiacomo–Spiga. Moore-machine identifying experiments and adaptive distinguishing sequences predate the present project; Lee–Yannakakis, Hierons and related splitting-tree literature must inform novelty analysis.

The observation budgets here assume exact six-way categorical readings, uncharged known legal cube turns in Regime B, zero observation noise, full original-cubie pose readout in Regime A and an unrestricted exact decoder. Any change in these assumptions defines another optimization problem. Human memory, causal reconstruction behavior, robotic camera precision and motor movement cost require separate empirical or engineering studies.

During R14-P8.36 the three paper PDFs above were actually acquired, read and transferred into the canonical Research OS `10_PAPERS` folder, with per-file SHA-256 in the linked custody register. The seven separate historical missing core originals remain to acquire; authorship, exact editions, citation text and research priority still require external bibliographic review. No publication novelty or submission readiness is inferred.

### 6.1 Classical experiments and failure robustness: newly read primary corpus

Source-bound P8.37 original reads now make the experiment terminology historically precise. **Sokolovskii (1971)**, [*Diagnostic Experiments with Automata*](https://doi.org/10.1007/BF01068822), distinguishes *unconditional* from *conditional* diagnostic experiments, and the **initial-state** diagnostic task from *final-state homing*. Conditional experiment inputs are chosen in response to observed outputs. Its branching/splitting-word construction is a genuine mathematical predecessor of our feedback-policy ideas; nevertheless, unrestricted Mealy-machine transition coalescence is not equivalent to the bijective Rubik action, and no classic general bound automatically solves our precise 19-frame categorical game. **Vasilevskii (1973)**, [*Failure Diagnosis of Automata*](https://doi.org/10.1007/BF01068590), considers conformance/failure of an unknown machine against a known target, often with multiple reset experiments, so its failure-diagnosis length is also not our initial-cube-state frame budget. **Hopcroft (1971), Stanford STAN-CS-71-190** shows efficient exact automaton partition refinement, an algorithmic data structure precedent but **not** a minimum observation-depth theorem. **Furst, Hopcroft & Luks (1980), Cornell TR 80-442** supply permutation-group membership/subgroup computation precedent; the physically distinct FOCS proceedings version remains separate.

The 1976 **Harary–Melter** *Ars Combinatoria* paper remains a *primary original-PDF gap*, but its graph-distance sensor ideas can be checked via [Khuller, Raghavachari & Rosenfeld (1996), *Landmarks in Graphs*](https://doi.org/10.1016/0166-218X(95)00106-2), and [Bailey & Cameron (2011), *Base Size, Metric Dimension and Other Invariants of Groups and Graphs*](https://doi.org/10.1112/blms/bdq096), both physically held and read. **The 1996 paper explicitly states the 1976 tree proof has an error in Lemma 1**, and supplies a different proof; the 1976 result must not be copied uncritically. Metric dimension uses **graph shortest-path-distance responses**, not our persistent original cubie full-pose responses. [Source-critical reconstruction ledger](../../docs/0.28/20261113_R14_P837E_HARARY_MELTER_REPLACEMENT_TEXTS_AND_BABAI_PRIMARY_FIX.md). Hennie (1964) remains a real conference article (SWCT 1964 pp.95–110); its [NASA NTRS record 19650037493](https://ntrs.nasa.gov/citations/19650037493) explicitly offers **no downloadable file**; no fabricated original-PDF custody or full-text claim. [Access and scope ledger](../../docs/0.28/20261113_R14_P837F_HENNIE_1964_NASA_NO_DOWNLOAD_AND_ACCESS_LADDER.md).

**Adversarial one-sensor erasure corollary (P8.38; supplemental, not a third main-paper objective):** Define \(\mathcal I_f(X)=\{S:\forall F\subseteq S,|F|\le f,\ S\setminus F\in\mathcal I(X)\}\). With 20 distinct available original-piece full-pose sensors and no duplicates, the exact complete [P8.38 all-subset CI census](https://github.com/WhoSia/CUBE-REV/actions/runs/43361772300) yields on B6 **12 identifying 19-tag layouts resilient to one missing sensor, plus the full 20-tag layout**, and on B7 **only the full 20-tag layout**. No 2-sensor arbitrary deletion-tolerant design exists even for B6. This is not fault-tolerant *graph metric dimension* as defined by [Krishnan & Rajan (2016)](https://doi.org/10.4236/am.2016.77055), whose observation map is vertex distance, not pose. The B6-positive classification inherits the independently passed P8.33 MITM premise, and exact lost design count is **12** in the one-fault class. [Full mathematical definition and proof limitations](../../docs/0.28/20261113_R14_P838_FAULT_TOLERANT_PERSISTENT_TAG_EXACT_CENSUS.md); [archived Drive CI proof bytes](https://drive.google.com/file/d/1o2Gr7efoBuZYLTXqQ2zj1gNIYyzC2oNO/view). No effect on the still-OPEN unrestricted 19-frame color-feedback minimax result.

## 7. Reproducibility and release obligations

| Result | Source of evidence | Status | Unclosed obligation |
| --- | --- | --- | --- |
| \(b_6=16\), 156 optima and 4,689 excluded | Fresh P8.33 physically regenerated P48 data, 41 newly executed C++ HTM exclusions + earlier 872 obstruction suite | [Fresh CI PASS](https://github.com/WhoSia/CUBE-REV/actions/runs/43349579675), [Drive-byte-sealed receipt](https://drive.google.com/file/d/1wBw8zCFs4pBXzRMx2ONOCWCZDLZKZSec/view) | Independent referee review of the 156-layout-to-41-class quotient and full journal-ready source package; old 2026-10-30 ZIP archival custody remains separate |
| B6 432 inclusion-wise minimal layouts | Independent finite geometry and prior B6 classification | Conditional on inherited B6 physical verdict | Referee check of all minimality witnesses |
| All 28+66 B7 pair supports | Standalone P8.30 48-sticker engine; 720 physical pairs | [GitHub CI PASS](https://github.com/WhoSia/CUBE-REV/actions/runs/42973939189) | Peer-review independently supplied short-word witness dataset |
| \(b_7=b_G=18\), 96 designs | P8.30 physical pairs + exact legality upper bound | Mathematically derived finite theorem | Formal physical word generation in Lean, external novelty comparison |
| Entire identifying-family saturation \(\mathcal I(B_7)=\mathcal I(G)\) | Complete 1,048,576-subset P8.34 census over 872 B6 and 94 B7 physical supports | [New CI PASS](https://github.com/WhoSia/CUBE-REV/actions/runs/43350675032); 1,023 → 117 layouts, 906 lost | Depends on separately verified P8.33 B6 positives; no claim of a new universal theorem |
| Pair-support hitting implication | `formal/028/B7PairSupport.lean` | [Lean kernel PASS](https://github.com/WhoSia/CUBE-REV/actions/runs/42974864873) | Import physical enumeration as checked Lean inputs, without unproved assumptions |
| \(h_{\rm fixed}=21\) | Prior physical preset collision certificate | Inherited | Independent full raw receipt replay and model-equivalent literature comparison |
| Adaptive upper bound 19 | P8.40 complete feedback policy | Exhaustive representative games and physical routing | Preserve the transport proof and executable policy |
| Exact adaptive minimum 19 | P8.40 upper bound and P8.41 full corner oracle lower bound | Exact finite minimax and independent checker | Preserve both root replays |

**Final reviewer gate.** This revised C0.3 article has a defensible *single case-study question* but **not** a single universal theorem connecting the two objective functions. Do not force publication as one piece if a mathematical referee sees merely juxtaposed results. The fallback is a focused Paper A with Theorem B's sharp B6-to-B7 transition as the central climax and Theorem C preserved as a separate, already developed Paper B.

## 8. Selected scholarly background (working citation list, no new custody claims)

- Bailey and Cameron (2011), *Base size, metric dimension and other invariants of groups and graphs*.
- Cameron and Fon-Der-Flaass (1995), *Bases for Permutation Groups and Matroids*.
- Boutin (2009/2010 journal), *Determining Sets, Resolving Sets, and the Exchange Property*.
- Dalla Volta, Mastrogiacomo and Spiga (2024), *On the Cardinality of Irredundant and Minimal Bases of Finite Permutation Groups*.
- Blaha (1989 PhD dissertation; 1992 journal), permutation-group base algorithms, distinct editions.
- Moore (1956), *Gedanken-Experiments on Sequential Machines*.
- Lee and Yannakakis (1994), *Testing Finite-State Machines: State Identification and Verification*.
- Hierons et al. (2008), *Using Adaptive Distinguishing Sequences in Checking Sequence Constructions*.
- Türker, Ünlüyurt and Yenigün (2016), adaptive distinguishing-sequence minimum-cost algorithms.
- Soucha and Bogdanov (2020), *State Identification Sequences from the Splitting Tree*.
- Zassenhaus (1982), *Rubik's Cube: A Toy, a Galois Tool, Group Theory for Everybody*.
- Rokicki et al. (2013/2014 versions), cube HTM diameter twenty (not needed for the sharper B7 saturation proof).

No acceptance, originality priority, universal new automata theorem, or human cognitive implication is asserted.
