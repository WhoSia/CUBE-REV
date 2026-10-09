# Reversible Experiments and Forgotten Action Histories in a Rubik Edge Automaton

**Working manuscript — DRAFT 0.1, 2026-10-09. Not submitted; novelty review and proof-authority gates OPEN.**
Research owner: CUBE-REV 0.16 — *Active Information Geometry, Belief-State Control & the Limits of Reversible Inference*. The separately opened [0.17 program](../0.17/PROGRAM_CHARTER.md) concerns generalizations and does not supersede this finite mathematical paper.

## Abstract

A reversible physical action need not make its unrecorded history identifiable under restricted observation. We examine a finite reversible automaton arising from the position and orientation of one tracked edge of a Rubik's Cube, acted on by all eighteen half-turn-metric face tokens. By identifying its twenty-four states with ordered adjacent face pairs, we represent its action-count multigraph as an incidence Gram matrix over a bipartite double cover of the octahedral face graph. The spectrum is `{18¹,16²,14⁶,12²,10¹³}`, yielding a closed form for the maximal number of length-`t` literal action words with the same observed single-edge endpoint. For an ideal one-bit orientation observation after each action, exact finite-policy certificates give worst-case adaptive initial-state diagnosis and single-edge target reset lengths of eight and ten turns, respectively. A separate four-turn experiment family exhibits a closed-form face-incidence rank classification and finite, proof-carrying bounds on the size of a universal separating-word catalogue. The claims concern one tracked edge and an artificial mathematical observation function—not human perception, human memory, or solution of the full 3×3 cube. Model-specific novelty versus prior automata, algebraic graph and coding literature remains under audit.

**Keywords:** permutation automata; adaptive distinguishing sequences; finite group action; Rubik's Cube; line graph; spectral graph theory; experiment design; proof certificates.

## 1. Introduction and precise distinction

Given a complete executed word `w=a₁...a_t`, applying the reverse inverse word `w⁻¹` always returns the **entire physical configuration** to its origin. This group-theoretic triviality says nothing about identifying `w` from a restricted terminal readout. Three tasks must be distinguished: identifying an unknown initial edge coordinate; feedback-steering that edge to a fixed target coordinate; and reconstructing the unknown literal action history from endpoint evidence. The third is a many-to-one **observation projection** even though individual physical moves are permutations.

Prior work on preset/adaptive distinguishing and homing of finite/reversible automata, controlled sensing, and classical graph spectral methods must be credited. The present novelty candidate is a **specific Rubik-edge action graph isomorphism and exact all-length multiplicity**, plus certified controlled finite optima—not the generic concept of adaptive information gain or invertibility.

## 2. Exact physical-state and observation model

Let `X` be the 24 possible `(edge slot, intrinsic flip)` coordinates of a single tracked UR edge: 12 available edge slots, 2 physical orientations. Let `A` be the 18 literal HTM face tokens `U,U',U2,R,R',R2,F,F',F2,D,D',D2,L,L',L2,B,B',B2`; inverse/canceling words are **counted as different literal histories** where appropriate. Each action induces a permutation `T_a:X→X` consistent with the physically-derived 0.15 edge geometry.

The ideal observation `o(x)` is a single intrinsic flip bit (equivalently its complement as documented in the canonical code), read after each selected move. Action choices may be conditioned on earlier observations, but the initial state has **no gratis time-zero read**. In the diagnosis and reset tasks, the initial state ranges across all 24 coordinates. In the four-turn source-position rank result, prior initial orientation is instead known as flip-zero and the original slot is drawn uniformly from a nonempty subset of the twelve initial positions. These are DIFFERENT experiments and must never be conflated.

## 3. Algebraic all-length history multiplicity

**Theorem 1 (physical action graph and spectrum).** There exists an explicit source-state bijection from `X` to the 24 directed edge-adjacency arcs of the six-face octahedral adjacency graph. For an appropriate unsigned incidence matrix `C` of a bipartite double cover, the action-count matrix `B` over all literal tokens satisfies

```text
B = 10 I_24 + Cᵀ C
spec(B) = {18¹, 16², 14⁶, 12², 10¹³}.
```

The physical coordinate-to-face-arc correspondence is verified for every one of the 24×18 action incidences by independently reconstructed implementations. A human-readable algebraic graph and incidence proof is in [P8 mathematical theorem](P8_SPECTRAL_HISTORY_THEOREM.md).

**Theorem 2 (maximal literal path fiber, all t).** For any fixed initial coordinate `x`, the largest number of words of length `t≥0` ending in any one `y∈X` equals the return count

```text
M_t = (18^t + 2·16^t + 6·14^t + 2·12^t + 13·10^t)/24.
```

Proof idea: `B` is real symmetric positive semidefinite and vertex-transitive; Cauchy–Schwarz on `B^t` (for t>0) bounds off-diagonal entries by the common diagonal return count, while trace/eigenvalues give that diagonal exactly. This is a statement about the endpoint coordinate of **one edge**, NOT the entire cube endpoint.

**Corollary (worst-case fixed side log).** If original and terminal single-edge coordinates and `t` are given but the exact literal history is forgotten, a fixed auxiliary log always sufficient to disambiguate historical words requires at least `ceil(log₂ M_t)` bits and can achieve that length by indexing within the terminal fiber. At `t=4`, the largest fiber has 26,584 words and 15 bits are needed. Under uniform i.i.d. literal tokens, `H(W_t|Y_t)=t log₂18−H(Y_t)`; the graph spectrum supplies explicit convergence of `Y_t` to uniform 24-state endpoint distribution.

**Boundary:** This side-log lower bound CHANGES if the complete physical cube endpoint, retained executed actions, additional observation history, or a restricted action grammar is supplied. It is not a human working-memory capacity measurement.

## 4. Adaptive diagnosis, reset and four-turn decision ranks

**Theorem 3 (exact finite machine-assisted optimum).** Under the ideal per-turn intrinsic bit observation and full24 initial uncertainty, the optimal number of distinct terminal diagnosis histories at horizons 0...8 is

```text
1,2,4,6,8,12,16,20,24.
```

Hence exact worst-case adaptive initial-edge identification needs eight actions, with a full finite Bellman lower certificate and an explicit 24-source decision tree. A feedback controller physically steering the edge to one designated target coordinate is impossible in ≤9 actions and possible in ten, again from complete exact finite recursion and direct independent physical policy replay. This is a **one-edge reset**, NOT solved 3×3 cube. The non-Bellman handwritten group-invariant lower bounds are not yet known; the finite certificates are not Lean-kernel verified.

**Theorem 4 (four-action support rank).** Partition original edge positions into `F={1,5,8,9}`, `B={3,7,10,11}`, and `N={0,2,4,6}`. For nonempty known-flip-zero uniform original-slot support `S`, define counts `(f,b,n)`. The exact optimal fixed-word terminal-history count is a piecewise function `R(f,b,n)` given by five minimal rank-five threshold vectors `(0,2,3),(2,0,3),(1,2,2),(2,1,2),(2,2,1)`; otherwise rank four under at least four sources spanning multiple categories; otherwise `min(|S|,3)`. Optimal adaptive rank is `R+1` iff `f,b,n≥2`, else `R`. The lower-bound constructions rely on a verified 36-word finite covering certificate; the upper geometric arguments are handwritten. Exactly 216 inclusion-minimal strict-feedback supports, and 1,331 strict-feedback supports in total, occur over the 4,095 nonempty source-slot beliefs.

## 5. Experiment dictionary covering problem and finite obstruction

Let `M*` be the minimum number of **fixed four-turn HTM words** forming a menu that collectively distinguishes all 1,192 rank-minimal source-position basis sets. Current mathematically certified bounds are

```text
25 ≤ M* ≤ 34.
```

The upper bound is a physically replayed explicit 34-word menu. The lower derives from a 60-positive-basis rational dual and exclusion of any 24-word cover. An exact reduction under the **hypothetical 24-word** mass slack restricts the needed masks to 80 near-tight candidates in a 28-target component, with 20 heavier and eight lighter target conditions.

**Proposition (24-target critical finite obstruction).** All twenty heavy targets together with four particular light targets form an **inclusion-minimal** 24-target set not coverable by five near-tight candidate words. A complete independent enumeration of `C(80,5)=24,040,016` combinations shows exactly 3,008 cover the heavy twenty, yielding seventeen possible eight-light coverage profiles. Ten six-light profiles define a ten-edge missing-pair graph with a four-edge perfect matching; a particular four-vertex cover blocks all these profiles, while none of the seven four-light profiles covers the chosen four targets. This is a concise **graph-theoretic argument conditional on the exact finite 17-profile completeness lemma**. It is NOT a fully non-enumerative proof.

**Key logical boundary:** The near-tight 80-candidate restriction follows from a hypothetical **24-word** cover (dual-weight slack4). It does **not** apply to **25-word** candidate covers (slack24). In particular, failure to find a 25-word solution inside the reduced candidates is NOT a proof `M*≥26`. A particular 25-word positive-dual-only construction fails 75 of the full1,192 basis requirements; that failure cannot exclude other 25-word global menus.

Detailed proof authority [P12 certificate](P12_MINIMAL_GRAPH_OBSTRUCTION.md).

## 6. Proof authority, falsifiers, scope and publication status

| Claim | Human analytical proof | Reproducible independent exact court | Lean kernel | Unresolved |
|---|---|---|---|---|
| All-length path multiplicity formula | Incidence/spectral graph derivation | 24×18 physical grammar, t≤12 exact integer checks | Not yet | Novelty audit |
| Diagnosis 8 and reset 10 | Generic reversible/injective bounds only | Exhaustive finite Bellman and 24-source witnesses | Not yet | Non-Bellman lower proof |
| Four-action rank and feedback iff | Geometric upper + finite construction | All source supports and compact witness menu | Not yet | Remove finite lower catalogue |
| Dictionary lower25 / upper34 | Weighted slack and covering arguments | Exact rational dual, 34-word replay, finite core UNSAT | Not yet | Exact M* |
| P12 24-target critical core | Vertex cover/matching conditional proof | 24M combination histogram, 24 one-deletion witnesses | Source only, not compiled | Nonenumerative profile classification |

**Lean policy:** A Lean source that has not actually compiled is `SOURCE_WRITTEN`, never `KERNEL_PASS`. Even an abstract table proof does not close the physical action-grammar semantic bridge.

**Publication judgment:** This is predominantly *theoretical computer science / finite automata and algebraic combinatorics*, with possible discrete applied math venues. Current intrinsic flip sensor observations are artificial and there is NO human experiment: this is not yet an empirical cognitive-science article. Originality relative to reversible/preset/adaptive automata, Rubik graph models and spectral history enumerations requires direct originals/literature review before submission.

**Preliminary originality comparison, NOT complete primary-text review:** [Yao & Lee (2024), *Solving a Rubik's Cube Using Its Local Graph Structure*](https://arxiv.org/abs/2408.07945) is already present as an original PDF in the user's canonical Drive corpus. Its verified public abstract concerns graph-convolution-derived heuristics for A* solving the **whole cube**, rather than this paper's spectral multiplicities of literal 18-action words on a **single tracked edge**. This distinction is preliminary: the underlying original PDF has not yet been section-by-section audited for overlapping background lemmas. [Radionova & Okhotin (2026), *Decision Problems for Reversible and Permutation Automata*](https://doi.org/10.1016/j.ic.2026.105488) studies complexity classes of classical reversible/permutation automata decision problems, not evidence of novelty for our model. [Rivest & Schapire (1993), *Inference of Finite Automata Using Homing Sequences*](https://doi.org/10.1006/inco.1993.1021) is held as a canonical Drive original and is a necessary homing/diagnosis predecessor. These comparisons from abstracts establish *topic separation*, NOT first-discovery priority.

**References to verify from actual held originals before submission:** the above Drive PDFs; controlled sensing Nitinawarat, Atia & Veeravalli (2013); adaptive distinguishing/homing reversible finite-state machine literature; classical spectral graph/line-graph and association scheme theory. Final novel-claim authority stays HOLD until primary source text and methods/limitations are read.

**Next manuscript tasks:** produce clean human-readable theorem/proof appendices, independent reruns with full action coordinate tables as stable mathematical definitions, actual Lean kernel receipts, targeted novelty audit, and decide whether P12 covering should be a full companion paper rather than distract from the stronger spectral result.

**Draft status:** `NOT_SUBMITTED / INTERNAL_PREPRINT_DRAFT / 0.16_OPEN / 0.17_OPEN_SEPARATE_GENERAL_QUESTION`.
