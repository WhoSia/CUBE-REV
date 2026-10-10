# CUBE-REV 0.21 — P7: Jointly Optimal Turn–Observation Complexity on a Real Rubik Edge and Exact Narrative-Poset Completion Counting

**Continuity:** Retain formal CUBE-REV 0.21 version title, G7 P24–P27, 0.18 `M*(4)=34`, 0.19 full `M*(5)=8` proof and fixed 9/adaptive 7 **single-edge trajectory** distinction, 0.20 transported cuts and restricted rank-7 math, and 0.21 P0–P6 as previously certified. This is an additive new pure math/TCS P7, **no new human subjects, video acquisition, tool-integration build or VFMC user-session fabrication**.

**Overall status:** `P7 TWO NEW EXACT FINITE INSTANCE THEOREMS EXTERNAL GITHUB ACTIONS PASS / RETROSPECTIVE SOURCE-GRADE LIMITS PRESERVED / HUMAN MEMORY OR CAUSAL EFFECT CLAIMS HOLD`.

## Theorem A — Real Rubik 3×3 UR edge, optimal turn–query pair (7,4)

### 1. Problem definition and model separation

Original real 3×3 Rubik's cube 18 legally reversible HTM outer face turns `ACTIONS`; they are generated *afresh* from the immutable `solvedStickerCube/applyMoveToken/toCubieState` source using original [0.15 `urMoveAutomaton`](../../scripts/cuberev-015/ur-fiber-tomography.mjs), not an invented abstract state machine.

Track a designated physical UR cubie with possible starting locations 12 distinct edge slots and original intrinsic edge flip 0. Thus initial unknown set `B_0={0,2,...,22}` in the original 24 finite edge state coordinates, bitmask `0x555555`. Every legal move `a` transports state by one of the 18 bijections `T_a:S→S`; sensor `O(s)=s mod 2` is its **intrinsic orientation bit**, not what an unaided human visually sees or the P2 nine-real-sticker camera sees.

**New query choice:** After each physical move, the controller either (i) deliberately queries the 1-bit sensor, paying one observation, then can branch on its value, or (ii) deliberately **does not query** the sensor, allowing the move to transport the physical hidden state without a new branch. Actions can depend on prior observed bits and the known action/query history. A candidate is identified when the current belief has exactly one possible state (equivalently one original source because legal physical actions are bijections). A legal controller must work for all 12 initial sources. Let `T_max` count worst-case HTM turns and `Q_max` worst-case actual sensor readings. This is **not** the old `M*(L)` universal dictionary-cardinality objective, and is not a direct measurement of human cognitive memory.

### 2. Exact theorem and proof

> **Theorem P7-A (simultaneous coordinatewise optimality):** In the original sticker-derived physical UR edge system, the Pareto south-west corner for worst-case (face turns, one-bit sensor observations) is **`(T_max, Q_max)=(7,4)`**. A single valid adaptive policy meets both lower bounds simultaneously and identifies each of the 12 physical original source slots.

**Sensor lower bound:** Any deterministic binary adaptive decision process querying at most `q` bits has at most `2^q` distinguishable complete observation transcripts (prefix-free leaves). Since 12 original slots must yield 12 distinct terminal transcripts, `q≥ceil(log2 12)=4`. Legal moves without reading cannot create a new information branch, although they can improve later queries.

**Physical turn lower bound:** Exhaustive Bellman belief recursion on all 18 genuine sticker-derived permutations proves `W(B_0,6,6)=FALSE`, even with a bit read permitted after **every** of six turns; allowing at most six turns with skipped queries is no stronger. Hence `T_max≥7`. This reproduces and separately corroborates the 0.15/0.21 P0 minimax-7 result, not a new discovery of the turn bound.

**Constructive exact upper bound:** A fully replayed adaptive policy with at most seven turns and at most four queries is emitted by [P7 physical source](../../scripts/cuberev-021/verify-p7-physical-seven-turn-four-query-optimum.mjs), directly importing the original sticker oracle, and verified on all original 12 starting sources. Each legal face turn is real; the policy has silent *unqueried* turns that physically transport the 12 hypotheses. The paths' query-bit strings are all distinct and prefix-free. Four sources require exactly three queries and six turns, and eight require exactly four queries and seven turns. The policy's concrete leaf code lengths saturate Kraft:
`4·2^(-3) + 8·2^(-4) = 1`.
This yields the simultaneous `(7,4)` optimum. There is no claim this particular witness has best expected move/query cost under arbitrary priors.

**Bellman certificate and dominated no-read transition:** Write `T_a B={T_a s:s∈B}`, `B^a_b=T_a B ∩ O^{-1}(b)`. Recursion `W(B,h,q)` is TRUE at singleton, FALSE if `h=0`, `q=0`, or `|B|>2^min(h,q)`. Otherwise there is an action `a` admitting either a silent branch `W(T_aB,h-1,q)` or a queried move such that each **nonempty** observation branch `W(B^a_b,h-1,q-1)` is true. If `h≤q`, skipping a query is dominated by taking it and ignoring the result, hence the physical implementation searches silent actions only when `h>q`. This completeness-preserving optimization, bijective 24-state move proof, and full 12 trace replays are independently re-executed.

### 3. Full finite witness details

The external artifact lists all 12 original slot witnesses and observation indices. Initial move in the certificate is `F`; examples, with `?` for actual read and `~` for no read:
- Source 0: `F? B? U~ R~ F? R~ F?`, queried bits `0011`, 7 turns/4 reads.
- Source 1: `F? U~ R~ F? U~ F?`, queried bits `110`, 6 turns/3 reads.
- Source 2: `F? B? U~ R~ F? U2~ F?`, queried bits `0001`, 7 turns/4 reads.
- Source 9: `F? U~ R~ F? U~ F?`, queried bits `111`, 6 turns/3 reads.

The 12 queried strings form a **complete prefix-free code**. Uniform source prior gives **this particular policy** mean `80/12=20/3≈6.6667` turns and `44/12=11/3≈3.6667` queries. This is not minimum mean total turn cost: P1 computed a different policy with uniform-prior optimum **`71/12≈5.9167` turns** at seven-turn deadline when reading the bit after every turn. For a *hypothetical illustrative* per-query overhead `κ` and turn cost 1, P7 witness cost `(80+44κ)/12` vs that P1 witness cost `(71+71κ)/12`; P7 is cheaper than **that specific comparator** when `κ>1/3`. Neither coefficient nor real human feedback effort was measured; the threshold is not a globally optimized economic policy frontier.

### 4. What is and is not novel

General binary information lower bounds and adaptive distinguishing sequences are classical TCS; see the prior art on minimum-cost adaptive distinguishing sequences [Information and Software Technology 74 (2016), DOI 10.1016/j.infsof.2016.02.001](https://doi.org/10.1016/j.infsof.2016.02.001). The **new verified instance-specific CUBE-REV result** is physical Rubik legality + original edge oracle + *simultaneous attainability of the exact seven-move physical minimax lower bound and four-bit Shannon lower bound*, complete on 12 real source hypotheses. It is not a new lower bound for arbitrary FSMs or a general theorem about all 3×3 cubies or FMC.

## Theorem B — Exact completion ambiguity of the eight authentic FMC reported search posets

### 5. Formal scope

P5/P6 yielded **eight** already-existing retrospective FMC attempt/working-note cases, **41** explicitly curated author-reported event labels and **27** separately warranted within-case chronological edges `E_prec`. Candidate referential links `E_ref`, other-author editorial addition `E_doc` and narrative token sequence indices **are not** automatically chronological edges. These come from written retrospective reports, not contemporaneous hidden thought recordings.

For episode poset `P=(V,≺)`, define a *linear extension* as a total order on the **reported events in V only** respecting all warranted `E_prec`; this does not impute missing actual steps. Let `L(P)` be the exact count.

**Recurrence:** For a prefix order ideal `S⊆V`, let `f(S)` count ways to complete; `f(V)=1` and
`f(S)=Σ_{x in minimal(P\S)} f(S∪{x})`.
Use exact integer DP on bitmasks (`O(n·2^n)` for n≤10 events per case), independently of Rubik ideal sensor automaton.

### 6. Exact certified counts

| Historical narrative | Event nodes | Linear extensions |
| --- | ---: | ---: |
| Wheeler 2026 A1 | 10 | **40** |
| Quraishi 2026 A3 | 6 | **1** |
| Dong 2026 A1 | 3 | **1** |
| Dong 2026 A2 | 3 | **1** |
| Pietrusiak 2026 A2 | 3 | **1** |
| Guido archived note | 4 | **4** |
| Utomo 2026 A3 | 6 | **30** |
| Wong 2025 A3 | 6 | **60** |

As a Cartesian product of within-case compatible orders, **exactly `40×1×1×1×1×4×30×60=288000`** global **tuples of within-case completions** are consistent with the curated source event DAG. This product is NOT asserting authors are independent samples or imposing a global chronological order *between* cases.

For the **105** within-case unordered pairs of distinct recorded event nodes, **71** are comparable in the transitive closure of warranted before/after edges; **34 are incomparable**. For every one of the 34 incomparable pairs `x,y`, exact DP on the augmented order `x≺y` finds at least one linear extension, and exact DP on `y≺x` also finds at least one. **Both completions exist for every pair**, thereby proving that their relative chronological order is *not identifiable from this particular recorded source DAG*. Note that 34 incomparable pairs **cannot be flipped independently**: `2^34` is not the completion count. The correct count is 288000.

`log2(288000)=18.135709...` bits measures **how many binary index bits would be needed to specify one compatible tuple of fully ordered *reported* events** under an efficient representation. It is not memory used by any solver, entropy of human cognitive process, or an empirical probability assignment. A uniform prior on linear extensions would be a chosen combinatorial measure, not a distribution provided by these retrospective sources.

**General elementary lemma (not claimed novel):** If two elements are incomparable in a finite poset, at least one linear extension places `x` before `y` and another places `y` before `x`; adding either directed edge individually cannot create a cycle because no reverse path exists. P7 computes explicit finite counts verifying this for all 34 historical ambiguous pairs. General exact linear extension counting is #P-complete; established by Brightwell–Winkler 1991, [DOI 10.1145/103418.103441](https://doi.org/10.1145/103418.103441) and [Order 8, 225–242](https://doi.org/10.1007/BF00383444). The CUBE-REV eight small posets admit exact bitmask DP.

### 7. What can be learned from 8 cases without inventing a larger sample

Eight deliberately selected rich narratives are absolutely enough to establish **existence** of specifically reported behaviors such as written-but-untried candidate, report of revisiting a previously considered option, or time-cost-based deferral. They are not evidence for population prevalence or causal effect size. The strong mathematical claim is narrower: **the chosen evidence representation demonstrably fails to pin down all recorded events' chronological order**, and the residual mathematical uncertainty has exact count 288000. The value does not depend on having large-N survey respondents; rather it depends on **auditable evidence grades**.

This conclusion helps identify which future evidence would be *decision-relevant*, but **no video engineering or new human recruitment is initiated by P7**.

## Reproducible external court and boundaries

**Theorem A:** [Original 18-sticker-derived move DP + 12 literal source traces](../../scripts/cuberev-021/verify-p7-physical-seven-turn-four-query-optimum.mjs); [GitHub Actions #38047052035 SUCCESS](https://github.com/WhoSia/CUBE-REV/actions/runs/38047052035), [complete witness receipt artifact #11667776646](https://github.com/WhoSia/CUBE-REV/actions/runs/38047052035/artifacts/11667776646), artifact zip SHA256 `92e3e9213764226ec91252f878ad4de19929cd15216e91104e4da23fc192e71e`.

**Theorem B:** [Source-grounded P6 event builder](../../scripts/cuberev-021/verify-p6-fmc-source-grounded-partial-order.py), [new exact P7 poset extension counter + 34 bilateral-witness proofs](../../scripts/cuberev-021/verify-p7-fmc-poset-linear-extensions.py); [GitHub Actions #38047106098 SUCCESS](https://github.com/WhoSia/CUBE-REV/actions/runs/38047106098), [source DAG/receipt artifact #11668216002](https://github.com/WhoSia/CUBE-REV/actions/runs/38047106098/artifacts/11668216002), artifact zip SHA256 `fb2972fca7fcf01ced1503e6811409c52c83496b31fc722db7c4fa3181ba2ce1`.

**DO NOT MIX:** P7-A physical **edge source hypotheses** are twelve actually legal states under the **intrinsic one-bit sensor**. P7-B historical FMC **reported event DAGs** are source-limited partial descriptions of actual people's after-the-fact narratives, not facelet-observation automata. There is no assertion that 288000 chronologies are equally likely human decisions, or that four orientation-bit queries model actual FMC mental inspections. Any generalization to full cube multi-cubie mixed cameras needs its own exact legality audit.

**New next theorem candidates (not achieved here):** (i) minimize expected `turn cost + λ query cost` over physical real 18-action policies with recorded source priors, giving a bona fide Pareto frontier rather than a comparison of two witnesses; (ii) measurement-dependent Myhill–Nerode right congruence for partial-observation belief/action histories, with task-specific equivalence and finite-state implementation; (iii) bounded-error active identification allowing one faulty sensor bit and legal-cube redundancy. Each requires independent proof, not a rhetorical extrapolation.

**P7 state:** `PURE_MATH_TCS_TWO_ORIGINAL_INSTANCE_RESULTS_EXTERNAL_PASS / REAL_PHYSICAL_SENSOR_OBSERVATION(7,4) / RETROSPECTIVE_FMC_POSET_COMPLETIONS(288000) / HUMAN_COGNITION_ESTIMATION_HOLD`.
