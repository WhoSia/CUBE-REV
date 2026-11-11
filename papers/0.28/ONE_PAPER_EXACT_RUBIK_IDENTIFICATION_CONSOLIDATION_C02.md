# WORKING UNIFIED PAPER — When Does Exact Observability Saturate? Two Observation Regimes on the Rubik Group

**Consolidated draft C0.2 (2026-11-11), R14-P8.32 editorial revision. NOT SUBMISSION-READY.**

**Editorial lineage:** C0.2 is a new successor to [one-paper C0.1](ONE_PAPER_EXACT_RUBIK_IDENTIFICATION_CONSOLIDATION_C01.md). [Paper A D0.5](RADIUS_RESTRICTED_CUBIE_OBSERVATION_DRAFT_01.md) and [Paper B D0.8](DUAL_COLOR_PROBE_ADAPTIVE_IDENTIFICATION_DRAFT_01.md) remain unchanged as full technical source documents. This is an *A-led, B-supported comparative case-study candidate*, not a proof that sensor counts in A and frame counts in B are commensurable, or a universal group-observability theorem. Mathematical proofs, executable certificates, exact remote CI outcomes and external novelty must be evaluated separately.

## Provisional title

**When Does Exact Observability Saturate? Radius-Restricted Tagged-Cubie Bases and Adaptive Color Probing in the Rubik Group**

## Abstract

We examine zero-error state identification in the legal fixed-center Rubik group under two physically distinct deterministic sensing protocols. In the first, a sensor reveals the complete location and orientation of a persistently identified original corner or edge cubie, and the unknown state lies in a word-metric ball \(B_r\). Existing independently implemented radius-six certificates give an optimum of sixteen permanent tags, attained by precisely 156 of the \(\binom{20}{16}=4845\) possible designs. We revalidate a sharp transition at the next radius: \(b_7=18\), with exactly 96 optimal eighteen-tag designs, and \(b_r=18\) for every \(r\ge7\). Eight explicit physical words of length at most fourteen, split into two legal radius-seven states and conjugated under proper cube rotations, furnish collision witnesses for all 28 corner pairs and 66 edge pairs. An independently written 48-moving-sticker verifier checks 720 rotated state-pair instances; the implication from such pair collisions to a necessary sensor hitting condition is separately kernel-checked in Lean 4.34.1. Consequently the full-group tagged-sensor threshold is attained on the much smaller \(B_7\), well before the full group is reached in word-metric radius. In the second, each observation frame returns one six-category color on a spatial edge facelet and one on a spatial corner facelet, with known legal inter-frame turns allowed at zero *frame* cost. Existing separate physical certificates establish an exact nonadaptive minimum of 21 frames, whereas a fully specified feedback policy identifies every legal state in at most twenty frames. The unrestricted adaptive minimum remains between 18 and 20. These results illustrate two non-equivalent mechanisms of exact identification—finite-radius collision saturation under rich permanent labels and feedback advantage under weak categorical observations—within one precisely defined puzzle group. The static pair-cover and adaptive belief-recursion formulations are standard mathematics; originality is claimed, provisionally, only for the particular finite cube-case classifications and complete policies after model-equivalent prior-art screening.

**Keywords:** Rubik group, exact identification, radius-restricted stabilizers, permanent cubie tags, collision support, adaptive distinguishing sequences, group-equivariant sensing, executable certificates.

## 1. Introduction: a single scientific question, two legitimate answers

What aspects of a legal puzzle's state become recoverable from a limited measurement channel, and when does either a larger reachable-state domain or access to feedback force greater observational resources?

Both experiments concern exactly the same physical state space \(G\), its legal group constraints and deterministic observation functions. They differ in three scientifically meaningful parameters: the hidden domain (\(B_r\) versus all of \(G\)), the sensor channel (full original-cubie identity/location/orientation versus a spatial sticker's categorical color), and the allowed decision rule (one static set versus an adaptive sequence of paired queries). They therefore do **not** share a single numerical optimization target.

We deliberately begin with the sharply classified full-tag radius threshold; a second theorem compares preset and adaptive schedules only **within** the low-information color channel. We do not infer human cognitive mechanisms, camera noise performance or turn-time optimality from either exact mathematical result.

**Contributions and evidence levels.**

1. A physically supported finite-case radius-six benchmark, \(b_6=16\) with 156 optimum layouts and 432 inclusion-wise minimal layouts across sizes 16 and 17. This result and its full 41-target shortest-distance proof are inherited from the preceding independent P48 audit, not re-executed in the C0.2 editorial cycle.
2. A newly **revalidated, not newly discovered** sharp radius-six-to-seven jump \(b_6=16\to b_7=18\) for persistent original-cubie tags. The full 28+66 two-tag collision support family is witnessed by eight physical word seeds, 24 spatial rotations and explicit two-B7-state splits. The associated \(b_r=18\) stabilization for all \(r\ge7\) is an elementary consequence of the global eighteen-tag upper bound.
3. A separately inherited whole-group low-bandwidth result: \(h_{\mathrm{fixed}}=21\), \(18\le h_{\mathrm{adaptive}}\le20\), implying a strict worst-case feedback advantage of at least one frame. We do **not** claim the exact adaptive minimum is twenty.
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

The complete physical proof package classifies all size-sixteen choices by 872 irredundant short-support obstructions, a 41-class exact stabilizer-distance positive certificate for the survivors, and a separate no-fifteen lower bound. The 41 exact shortest-distance representatives and their original raw receipts are not reproduced in this C0.2 drafting cycle; the full [Paper A D0.5](RADIUS_RESTRICTED_CUBIE_OBSERVATION_DRAFT_01.md) and its independent P48 scripts are the scientific source. This theorem is conditional on successful preservation/reproduction of that finite prior certificate for a future external release.

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

### 3.3 Verification scope of Theorem B

The prior B7 collision-completion scripts already made the exhaustive pair-support claim; this draft expressly credits that earlier internal lineage. The new P8.30 verifier independently rederived the physical check in a second standalone geometry engine. Its [remote GitHub Actions run](https://github.com/WhoSia/CUBE-REV/actions/runs/42973939189) finished SUCCESS, including 720 checks and a read-only repository gate. The P8.31 Lean 4.34.1 kernel [build](https://github.com/WhoSia/CUBE-REV/actions/runs/42974864873) proves an abstract, conditional statement: a selected identifying set must hit each witnessed two-tag collision support. **Lean has not yet recomputed the physical eight turn words, rotations or all 94 supports internally.** This distinction is part of the proof release contract.

## 4. Second main result: adaptive advantage under categorical observations

### Theorem C — fixed versus adaptive frame complexity (inherited full-group result)

For Regime B,
\[
\boxed{h_{\rm fixed}=21,\qquad 18\le h_{\rm adaptive}\le20.}
\]
The fixed lower certificate excludes all twenty-frame preset schedules under the physical two-color-probe model. The 21-frame fixed construction is independently realizable under tracked legal turns. A universal color-history-dependent controller uses at most twenty frames. This immediately yields
\[
1\le h_{\rm fixed}-h_{\rm adaptive}\le3.
\]
This is a strictly within-channel separation, not a relation between \(b_6,b_7\) and \(h\).

**Constructive proof spine.** The feedback controller first reads one facelet from each of twelve spatial edge positions while accumulating ordered adjacent colors for corners. By frame fourteen the corner observations determine the full corner assignment and legally relevant permutation parity. The controller conditions later edge mate reads on real previous color outcomes; the parity oracle is never supplied prematurely. The finite proof classifies 867 realizable first-edge-color vectors into 39 color-orbit representatives, verifies transport over 609,376 canonical conditional edge assignments, and handles an exceptional 2592-state residual family while finishing within twenty frames. A second physical 48-sticker source checks corner codewords and addressability of all 576 joint spatial query locations. The previously completed [P8.6/P8.7 remote CI run 42587382868](https://github.com/WhoSia/CUBE-REV/actions/runs/42587382868) was newly inspected during the C0.2 editorial audit and was SUCCESS: it executed all 867 vector roots, 39 canonical games, 2,592 exceptional legal-state checks, 576-pair physical routing, and the **restricted** prefix lower bound. This is a verified execution result, not an independently repeated 609,376-case source-byte audit or a proof of unrestricted 20-frame optimality. Full source and conditional exhaustiveness obligations remain in [Paper B D0.8](DUAL_COLOR_PROBE_ADAPTIVE_IDENTIFICATION_DRAFT_01.md).

**Critical scope:** The known twenty-frame lower bound for strategies that read a predetermined full twelve-edge first-facelet prefix does **not** prove a global 20-frame adaptive optimum. The unrestricted 18-versus-19-versus-20 problem remains open. Likewise, testing a few thousand physical states does not by itself establish universal completeness over \(|G|\); the exhaustive conditional-edge family and legal transport proof are indispensable.

## 5. Comparative synthesis: common formal questions, non-equivalent resource laws

The two regimes give two concrete answers to a shared *methodological* question—when does exact reconstruction become identifiable? Regime A enlarges the unknown-state domain while fixing a rich, permanent sensor set; its budget saturates at radius seven because complete two-original-tag collision supports are present. Regime B fixes the entire legal state domain and a sparse spatial color channel; its feedback access improves the worst-case frame budget relative to preset queries. These are neither two measurements of the same \(h\) nor a direct reduction from Theorem B to Theorem C.

The common mathematical operations are (a) pairwise difference supports, (b) zero-error distinguishing signatures, (c) group-equivariant transportation of physical certificates and (d) belief-state refinements. An identifying *static* set must hit all pairwise difference supports, while an *adaptive* strategy needs a rooted decision tree whose every feasible leaf is a singleton. These established general principles are useful for comparing proof structures; they do not imply that 16 permanent sensors “equal” 20 low-information observation frames.

The current kernel-checked generic Lean lemmas establish conditional hitting and abstract observation correspondence only. They do not yield a new numerical optimality theorem across the two regimes, and the manuscript is defensible as one article **only if** the case study's scientific question and proof protocol are considered sufficiently coherent by external reviewers.

## 6. Relation to prior work, model risks and falsification

Classical permutation-group base/stabilizer methods (Sims, Blaha, Jerrum; Bailey and Cameron) explain much of the group-action vocabulary. Metric dimension and graph resolving-set work use distance responses and cannot be directly substituted for tagged-cubie pose measurements. Matroidal exchange questions about irredundant permutation bases require distinct premises, as illustrated by Cameron–Fon-Der-Flaass, Boutin and Dalla Volta–Mastrogiacomo–Spiga. Moore-machine identifying experiments and adaptive distinguishing sequences predate the present project; Lee–Yannakakis, Hierons and related splitting-tree literature must inform novelty analysis.

The observation budgets here assume exact six-way categorical readings, uncharged known legal cube turns in Regime B, zero observation noise, full original-cubie pose readout in Regime A and an unrestricted exact decoder. Any change in these assumptions defines another optimization problem. Human memory, causal reconstruction behavior, robotic camera precision and motor movement cost require separate empirical or engineering studies.

The C0.2 drafting process did not acquire or re-read new scholarly PDFs. Bibliographic editions and missing-original provenance remain controlled by the Research OS 10_PAPERS/11_SOURCES ledgers; priority and publication suitability are **unverified**.

## 7. Reproducibility and release obligations

| Result | Source of evidence | Status | Unclosed obligation |
| --- | --- | --- | --- |
| \(b_6=16\), 156 optima and 4,689 excluded | Historical independent P48 full radius-six engine / 41 stabilizer targets | Inherited prior physical/CI certificate | Reassemble exact original raw SHA chain, reproduce 41 shortest-distance classes and all 4,845 labels from preserved bytes |
| B6 432 inclusion-wise minimal layouts | Independent finite geometry and prior B6 classification | Conditional on inherited B6 physical verdict | Referee check of all minimality witnesses |
| All 28+66 B7 pair supports | Standalone P8.30 48-sticker engine; 720 physical pairs | [GitHub CI PASS](https://github.com/WhoSia/CUBE-REV/actions/runs/42973939189) | Peer-review independently supplied short-word witness dataset |
| \(b_7=b_G=18\), 96 designs | P8.30 physical pairs + exact legality upper bound | Mathematically derived finite theorem | Formal physical word generation in Lean, external novelty comparison |
| Pair-support hitting implication | `formal/028/B7PairSupport.lean` | [Lean kernel PASS](https://github.com/WhoSia/CUBE-REV/actions/runs/42974864873) | Import physical enumeration as checked Lean inputs, without unproved assumptions |
| \(h_{\rm fixed}=21\) | Prior physical preset collision certificate | Inherited | Independent full raw receipt replay and model-equivalent literature comparison |
| \(h_{\rm adaptive}\le20\) | P8.6 exact policy and conditional finite game | Inherited | Preserve exact 609,376-case transport proof and independent route verifier |
| Exact \(h_{\rm adaptive}\) | Unrestricted online physical game | OPEN, 18–20 | Construct ≤19 policy or prove universal ≥20 lower bound |

**Final reviewer gate.** This article has a defensible *single case-study question* but **not** a single universal theorem connecting the two objective functions. Do not force publication as one piece if a mathematical referee sees merely juxtaposed results. The fallback is a focused Paper A with Theorem B's sharp B6-to-B7 transition as the central climax and Theorem C preserved as a separate, already developed Paper B.

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

No acceptance, originality priority, universal new automata theorem, completed unrestricted 19-frame proof, or human cognitive implication is asserted.
