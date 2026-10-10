# CUBE-REV 0.21 — P8: Exact Physical Turn–Query Cost Frontiers, Finite-Observation Moore Minimality & Belief-State Sufficiency

**Version:** The project remains *CUBE-REV 0.21 — Active Reconstruction of the Rubik's Cube: Observation-Driven Action Selection, Belief-State Dynamics, Physical Information Access & the Limits of Adaptive Solving*. This is an additive P8. Original 0.11 FACTORY/G7, 0.18–0.20 and P0–P7 are immutable historical findings; no new human participant recruitment, no FMC video analysis, no .vfmc-session fabrication. **P8 closes one pure mathematics/TCS research stage before a proposed but not-yet-adopted 0.22.**

**Exact evidence-grade headline:** `EXACT_STICKER_DERIVED_7_HTM_TURN_COST_PARETO_TWO_VERTICES(71,45)/(74,44)__STRICT_(7,4)_EXACT_OPT(74,44)__24_STATE_MOORE_MINIMAL_BY_DEPTH_TWO__HUMAN_COST_AND_CONTROLLER_MINIMIZATION_NOT_INFERRED__EXTERNAL_CI_SUCCESS`.

## 1. The empirical-versus-physical/ideal observational contract

Use the **actual 18 HTM physical turn permutations** regenerated from [0.15 original 54-sticker oracle](../../scripts/cuberev-015/ur-fiber-tomography.mjs) and genuine move generator, tracking the designated UR edge. Initial unknown source is uniform over **12** legal original flip-zero edge slots. At each legal turn the controller may pay for an **intrinsic cubie-orientation one-bit sensor reading** or skip the reading. The physical cube still turns when the sensor is skipped; skipped readings do not reveal a bit. Source priors are uniform only for **this mathematical instance**, not asserted about human FMC or speed-solving. All 12 sources must be identified exactly in **at most seven physical face turns**; numerical mean costs are sums of leaf depths divided by 12.

Define integer totals `T = Σ_{12 starts} actual HTM turns` and `Q = Σ_{12 starts} actual orientation-bit readings`; thus `E[T]=T/12` and `E[Q]=Q/12`. To avoid mixing objectives distinguish:
- **Problem U (uncapped queries):** worst-case physical turns `≤7`; each turn may yield at most one optional query but maximum number of queries is **not separately capped at four**. Minimize `J_lambda=(T+lambda Q)/12` for a prescribed nonnegative real read-price `lambda`.
- **Problem C (hard cap):** worst-case `turns≤7` AND worst-case actual bit readings `≤4`. Minimize expectation of turns, queries or a nonnegative scalarization under both hard constraints. A policy with five readings on some path **is invalid for Problem C**, even if its mean reads are close to four.

Do not confuse this with older unrestricted dictionary size `M*(L)`, the 2026 P2 full nine-sticker photograph experiment, the 132/528 two-target edge presence experiment, or human naturalistic FMC search.

## 2. Exact finite theorem P8-A: only two nondominated mean-cost vertices under ≤7 physical turns

**Theorem:** The entire Pareto frontier of feasible **aggregate integer sums** `(T,Q)` for Problem U consists of **exactly**
`(71,45)` and `(74,44)`.
Consequently for *every* `lambda≥0` the exact optimal scalar cost is
`V(lambda)= (min{71+45 lambda, 74+44 lambda})/12`.
The optimum is the first policy for `0≤lambda<3`, either for `lambda=3`, and the second for `lambda>3`. `lambda=3` is a mathematical *relative sensor-price break*, not an estimate of actual human read-versus-turn effort.

**Proof:**
1. Rooted finite-horizon exact Bellman recursion over all physically legal 18 transitions yields `T≥71` for every perfectly identifying ≤7-turn policy (the `lambda=0` optimum).
2. For any perfectly identifying deterministic binary read-history tree on 12 equiprobable distinguishable sources, prefix-freeness and Kraft/Shannon yield `Q≥ceil(12 log₂12)=44`; 44 actually attained.
3. Independently run the **same exact all-18-action Bellman DP** with integer read price `lambda=3`. It proves a **dual supporting inequality** `T+3Q≥206` for *every feasible policy*.
4. Exact complete physical branch reconstruction/replay on **all 12 true initial states** provides `(71,45)` and `(74,44)` legal policies satisfying equality as needed: `71+3·45=206=74+3·44`.
5. Since `Q\in\mathbb Z` and `Q≥44`, `Q=44 ⇒ T≥74` by dual inequality; for `Q≥45`, `T≥71` by original Bellman bound. Hence every other feasible integer pair is weakly dominated by one of the two witnesses. The two witnesses trade three actual total turns against one total query across the 12-source prior. **No convex interpolation, sampling or heuristic failure is used to exclude other Pareto vertices.**

The underlying Bellman recurrence at belief `B` of size `m` and remaining turns `h`, with optional query remaining budget `k`, is written on **unnormalized integer sums across all current equiprobable sources**:
`F(B,h,k)=min_{a∈A} { [m+F(T_a B,h−1,k)] , [m(1+lambda)+ F(B^a_0,h−1,k−1)+F(B^a_1,h−1,k−1)] }`,
where queried terms require **both** branches nonempty; silent terms require feasible future complete identification, terminal `F({s},h,k)=0`; infeasible states are `∞`. The action value at each state is minimized exactly (not approx) for nonnegative integer `lambda=0,3,4,100`, and `h≤7`. `B^a_b=T_aB∩O^{-1}(b)`. For Problem U use `k=h` initially; Problem C set `k=4`. Querying a state that cannot split candidates is never necessary under nonnegative read costs.

**Uniform-prior witness distributions (verified, original real cube):**
- `(71,45)`: turn depths 4×1, 5×3, 6×4, 7×4 (sum 71); query code lengths 3×5,4×5,5×2 (sum 45). Worst queries **5**, thus **not admissible in strict P7 (7,4) hard cap**.
- `(74,44)`: turn depths 5×2,6×6,7×4 (sum 74); query code lengths 3×4,4×8 (sum 44), worst queries 4.
Both sets of bit codes are prefix-free and saturate Kraft `Σ2^{-queries}=1`. All moves exactly match the physical sticker oracle, and all 12 posterior identifications were replayed against transported true physical states. The first policies can save **three aggregate turns** at a cost of one additional query across the 12 uniformly weighted possibilities. No one claims the same branch means are empirical human response times.

## 3. Exact finite theorem P8-B: simultaneous mean optimum subject to original hard (7,4) cap

P7 proved the physical **worst-case** pair `(7 turns,4 queries)` can be achieved; the prior illustrative P7 policy had **aggregate** `T=80,Q=44`. This policy was optimal only **in the worst-case coordinatewise sense**, not in expected turns.

A separate exact Bellman DP imposing `h≤7,k≤4` now finds a physical witness with **`T=74,Q=44`**, and independently optimizes at `lambda=0` and `lambda=100`; both return `(74,44)`. The uncapped dual `T+3Q≥206`, finite certified DP for capped `T_{min}=74`, and `Q≥44` prove simultaneous expected turn and expected query optimality in the strict original `(7,4)` feasible class. This strictly improves the previous valid illustrative P7 policy in expected turns **80→74** without increasing total/maximum queries, without changing the already established worst-case `(7,4)` result.

**CORRECTION to potential ambiguous comparisons:** Previous P7/P1 comparison against a policy that **reads after every turn**, with `T=71,Q=71`, created an illustrative `lambda>1/3` crossing with `(80,44)`. Such a comparison was never a global cost frontier. The now-exact optimum **with optional reads** is instead `(71,45)` vs `(74,44)` with genuine frontier break at **`lambda=3`**, in Problem U only. The P1 best-turn value `71/12` is preserved; the additional P8 finding is that read optimization permits the same `71` turn total with `45` rather than `71` reads.

## 4. Exact physical observational automaton minimization, Moore-style

Independently of the belief-policy optimization, consider the full **24-state** single-edge deterministic transition automaton with legal actions `A=18 real face turns` and Moore output `O(s)=orientation bit`. Moore distinguishability equivalence is: `s≈t` iff **for every legal finite action word w**, the output after `w` agrees. This is a right congruence because `O(T_a s)\) is part of the response semantics. Partition refinement yields exactly:
- **Depth zero (current bit): 2** observational equivalence classes.
- **Depth one (all 18 legal one-step response functions): 6** classes.
- **Depth two (all 18² possible two-step response functions): 24 singleton classes**.

Equivalently, among all `C(24,2)=276` unordered state pairs, shortest separating-word depth is **0:144 pairs, 1:96 pairs, 2:36 pairs**. Therefore the full 24-state physical Moore machine is **state-minimal** under its action/output semantics; all 24 individual physical states are future-distinguishable. This **does not mean** one common two-turn preset word identifies all 24 states, or that a real human can inspect the intrinsic edge orientation bit unaided. It is a machine minimization theorem for the original exact physical ontology, not a global automata minimization result.

**Immediate physical counterexample to lossy memory compression by candidate cardinality alone:** Consider initial-zero edge-state beliefs of size two. Sources in original slots **0 and 1** can be distinguished by a single `F` turn followed by reading the orientation bit. Sources in slots **0 and 2** **cannot** be separated by any of the 18 legal one-turn orientation-bit read experiments. Thus `|B|=2` by itself is **not sufficient** to predict one-step residual solvability; the geometry of the surviving states matters. This counterexample is recomputed from original 18 sticker-derived maps.

**Belief-Markov sufficiency theorem (standard, instance-grounded):** With deterministic known transitions, a fixed prior (uniform in this experiment) updated by noiseless observations, a fixed terminal identification objective, and nonnegative turn/read costs, the **posterior weighted belief** plus remaining resource budgets is a sufficient statistic of the full action/observation history for every admissible future control experiment. Since our actions are permutation-valued and the initial prior is uniform, all elements of the posterior support remain equiprobable; a simple **24-bit belief mask + remaining turn budget (and query budget for hard caps)** is sufficient. This is a *valid finite control-state representation*, **not** a proof that all these beliefs are pairwise minimal. In particular the 24 singleton automaton result and the belief-controller minimal-state result are different questions.

## 5. Novelty and literature calibration

Adaptive distinguishing sequences and minimization of their costs are longstanding subjects in formal methods and testing. For example [Effective algorithms for constructing minimum cost adaptive distinguishing sequences, Information and Software Technology 74 (2016)](https://doi.org/10.1016/j.infsof.2016.02.001) covers ADS cost minimization in FSMs, and [State Identification and Verification with Satisfaction (2022)](https://research.ou.nl/en/publications/state-identification-and-verification-with-satisfaction/) covers SAT-based construction. Myhill–Nerode/Moore right-distinguishability and Bayesian belief sufficiency are classical tools. CUBE-REV's novel verified **physical instance** content is the **exact two-point joint cost frontier, supporting dual `T+3Q≥206`, physical strictly capped optimum and the precise 24-state orientation-response refinement** for the original realistic 18-move physical Rubik edge. General NP-hardness/completeness and arbitrary FSM results are **not claimed to be newly proven here**.

Eight real FMC retrospective event graphs and 288000 admissible reported-node order completions (P6/P7) remain valuable source-limited naturalistic observations, but their psychological relevance is a separate question from this idealized tagged-edge oracle. Small-N human studies can be scientifically valuable for mechanistic existence and carefully designed repeated measures; these eight intentionally selected writeups do **not** license statistical generalization to all FMC practitioners or identify human turn/query costs.

## 6. Certified external court

**Code:** [P8 original 18-action physical Bellman, 12-source witness replay and independent Moore refinement](../../scripts/cuberev-021/verify-p8-physical-cost-frontier-and-minimal-moore.mjs) (sends all precise numerical vertices and witness paths to an inspectable JSON receipt).

**GitHub Actions:** [P8 run #38047782290 SUCCESS](https://github.com/WhoSia/CUBE-REV/actions/runs/38047782290); [actual full 12-source physical Pareto and automaton certificate artifact #11668466858](https://github.com/WhoSia/CUBE-REV/actions/runs/38047782290/artifacts/11668466858) SHA256 `8dc75fbba0ef5cd1de8593f3b9d40f3526c7f39fa661650771ca65592ec15dcd`. The Actions job replays deterministic DP, full physical histories, prefix-free code tests, hard cap guard, 24-state future-equivalence profile refinement and a second receipt-shape check. Local independent Python Bellman implementation using frozen exact original move maps also reproduced `(71,45)`, `(74,44)` and cap `(74,44)`. This external CI does **not** test FMC humans or an unknown camera viewer.

**Evidence grade:** `P8 EXACT PHYSICAL FINITE-PROOF REPLAY SUCCESS; HISTORICAL HUMAN-COGNITIVE COST INFERENCE HOLD; VIDEO/VFMC ENGINEERING HELD AS REQUESTED`.

## 7. Proposed next major version — 0.22 (name only; user confirmation pending)

**Formal proposed title:**
**CUBE-REV 0.22 — Cost-Sensitive Physical Identification & Finite-State Decision Semantics: Exact Turn–Observation Pareto Geometry, Task-Relative History Sufficiency, Observation-Automaton Structure & Evidence-Constrained Human Search**

Why the title is warranted: The exact P8 cost Pareto theorem supplies the verified economic tradeoff at the physical sensor level; the full 24-state Moore minimization and belief-sufficiency/candidate-cardinality counterexample supply the formal-systems substrate; P5–P7 retrospectively documented FMC search events supply an evidence-graded—but not falsely causal—human behavior axis. **What remains prospective in 0.22:** minimal quotients of full *policy* belief-state controllers rather than underlying 24-state Moore machine, nonuniform priors and varying horizons/cost regimes, full edge/corner or real sticker visual sensors, and empirical search-policy contrasts with genuinely timestamped naturalistic source data. Keep 0.22 unactivated until its name is accepted; no renaming of active Notion 0.21 page or 0.21 repository files.

**Next step, if the user continues:** Start 0.22 P0 with the finite controlled-observation right-congruence definition and a **counterexample-first** minimization court; do not pretend 24 Moore-minimal source states prove no belief-state quotient. Independently test nonuniform priors and 8/9-turn versions before calling the entire cost geometry a universal law.
