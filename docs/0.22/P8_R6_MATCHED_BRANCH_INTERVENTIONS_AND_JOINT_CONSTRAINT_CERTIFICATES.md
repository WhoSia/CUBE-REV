# CUBE-REV 0.22 P8-R6 — Matched Physical-Branch Interventions & Joint-Constraint Attribution

**Formal P8-R6 stage:** Matched Physical-Branch Interventions & Joint-Constraint Attribution: Source-Faithful DR Neighborhoods, Exact Geodesic-Cost Decomposition, PDB Rank-Reversal Falsification & Human-Trace Identification Limits.

**Status (2026-10-11 KST):** Independent physical 10-generator exact-neighborhood IDA+PDB CI **PASS**, independent full 29,400 HTR left-coset sensitivity CI **PASS**. Does **not** promote 0.23; see separately staged 0.23 proposal.

## 1. Actual sourced states and intervention registration

Author Qijun Miao publicly documented two DR alternatives from the same four-turn EO `L2 F' L D` in FMC World 2026 Attempt1 (source [2014MIAO02](https://333.fm/wca/reconstruction/FMCWorld2026/2014MIAO02), P7 frozen ledger). The written words are the same through their first **six** legal turns; they first diverge at turn **7**, main `B`, other `L'`. Both literal authored stages are genuine **FB DR** physical states after the original source scramble, but they differ in corners and edges; the main stage length is **10**, alternative stage length **11**.

Prior independently verified source states and shortest post-prefix full-cubie distances:

| Sourced endpoint | Authored stage | Exact 10-DR-generator d to solved | Exact all-18-HTM d to solved | Fixed original raw total |
| --- | ---: | ---: | ---: | ---: |
| Miao main | 10 | 9 | 9 | 19 |
| Miao alternative from same EO | 11 | 12 | 12 | 23 |

We next apply each of the **ten** genuine FB-axis DR-preserving turns as the *same canonical intervention* on the respective actual endpoint. For each move a in `U U2 U' D D2 D' R2 L2 F2 B2`, form a matched physical pair `(s_main a, s_alt a)`. These are **20 computer-generated counterfactual states**, not 20 new human-authored candidates or independent random samples. Each is derived from the authentic original scramble, actual authored literal prefix and axis-correct actual face turn using the original 54-sticker oracle. The source stage is held fixed; the extra move is a new synthetic operation.

For each child state record independent reverse 967,680-state corner×E-slice and UD-edge×E-slice projected lower bounds, max admissible lower bound, actual physical cubie digest, exact or certified bounded DR solution length, and provenance grade. Re-run exact DR-preserving IDA (canonical 10 generators) only where the two exact geodesic/metric bounds cannot already settle the distance. Every shortest continuation that needs an explicit constructed witness is replayed against the original 54-sticker scramble. Any conclusion based on triangle inequality is labeled a mathematically exact metric proof, not a newly observed search path.

## 2. Exact matched DR-geodesic results

All **20/20** physical interventions have exact shortest DR-preserving solved distances, **20 distinct original full-cubie SHA-256 state digests**, **20 physically replayed optimal-suffix witnesses**, **688,811 total bounded IDA node visits** across the twenty children, and **zero** resource holds were encountered (each search used an explicit 6-million-visit upper limit, not exhausted). The resulting exact shortest physical continuation costs, including the actual source-prefix lengths and added intervention, are:

| Common synthetic DR turn (axis frame) | Main child's exact continuation | Alternative child's exact continuation | Extra raw completed actions (alternative – main) |
| --- | ---: | ---: | ---: |
| U | 10 | 12 | **3** |
| U2 | 10 | 12 | **3** |
| U' | 10 | 13 | **4** |
| D | 10 | 11 | **2** |
| D2 | 10 | 12 | **3** |
| D' | 10 | 11 | **2** |
| R2 | 8 | 12 | **5** |
| L2 | 10 | 11 | **2** |
| F2 | 10 | 12 | **3** |
| B2 | 10 | 13 | **4** |

**Correct summation:** add to each child continuation the real person's original literal 10- or 11-action prefix **plus the one synthetic move**. Thus the raw total gap is `(11+1+d_alt)−(10+1+d_main)=1+d_alt−d_main`. In all ten full exact matched pairs the alternative costs **2–5 extra raw actions**. These are synthetic endpoint-conditioned staged costs; adjacent same-face move cancellations can change an irreducibly normalized whole-word length and break literal segmentation. Do not represent this intervention census as historical human consideration.

## 3. Stricter all-18-HTM theorem without brute-force 20 all-18 minima

Let `d_18` be actual all-18-face-HTM shortest distance from a physical cube to solved. For **any** legal single face turn a, the Cayley graph's 1-Lipschitz property gives:

`|d_18(s a,e)−d_18(s,e)|≤1`.

Since the sourced Miao main/alternative endpoints have **exact unrestricted-after-prefix** solved distances 9 and 12 (R4/R5), the 10 matched legal DR-preserving child pairs satisfy respectively `d_18(main·a,e)∈[8,10]` and `d_18(alt·a,e)∈[11,13]`. The literal original stage + one synthetic intervention adds 11 main and 12 alternative raw actions, hence for **all ten** moves:

`2 ≤ [12+d_18(alt·a,e)]−[11+d_18(main·a,e)] ≤ 6`.

The **positive advantage survives every listed matched one-step move even if ANY of the 18 real physical face turns are subsequently allowed**, with **no claim to have calculated each child's exact d_18**. This theorem is conditional on retaining the original source prefix and the intervened staged decomposition, not a global solution length after normalizing away the branch boundary.

R6 therefore has two different scientific claims: exact 2–5 action contrast in the ten-generator DR grammar (20 exact search outcomes), and rigorous but non-exact 2–6 lower/upper contrast in the broader 18-move continuation grammar (metric inequality). Do not conflate their epistemic grades.

### Matched radius-r all-18 geodesic robustness threshold (deduced, not enumerated)

The same physical one-step metric fact generalizes to a **matched length-r legal face-turn word w**, applied to BOTH genuine source DR endpoints (the word may leave DR if the study permits general all-18 continuations). Because any legal path of r HTM moves changes solved distance by at most r, the actual base d18 values 9/12 imply

`d18(main·w,e)∈[max(0,9−r),9+r]`; `d18(alt·w,e)∈[max(0,12−r),12+r]`.

When **the same r additional raw actions** are appended to the preserved literal authored prefixes (10 main, 11 alternate), their total raw action cost gap `Δ_r=(11+r+d18(alt·w,e))−(10+r+d18(main·w,e))` satisfies for r≤9

`4−2r ≤ Δ_r ≤ 4+2r`.

This is a certified **interval for every** matched feasible length-r intervention, not a claim that either endpoint's actual geodesic takes an interval endpoint, nor a statistical confidence interval. At r=1 the proven strict gap is [2,6] and the R6 ten real DR-generator comparisons sharpen the DR-grammar gap to exact 2–5. At **r=2 the all-18 metric guarantee first permits equality** (lower bound 0); at r≥3 it no longer rules out a complete ranking reversal. **Whether an actual legally feasible matched radius-two or radius-three branch meets these bounds is OPEN.** The logical boundary gives 0.23's first sharp negative-control/falsification target and avoids expanding neighborhoods without a clearly discriminating hypothesis. A normalized final word can cancel turns at authored/synthetic boundaries, and then this raw source-prefix cost comparison is not directly an irreducible FMC length theorem.

## 4. Independent projected-PDB falsification and independently measured HTR contact

Across **all ten** matched pairs, the exact backward-projection PDB `h=max(h_corner+E,h_UDedge+E)` assigns a **smaller admissible lower bound to the alternative**, even though full physical DR solution cost is **larger** in all ten matched pairs. Thus the R5 rank reversal is robust across this entire predeclared finite one-step intervention alphabet; it is not just a single source state artifact. But these ten interventions are connected moves on only two sourced states, not independent stochastic samples. Do not attach a sampling p-value or describe them as a broadly representative population.

Separately, repeat the genuine **29,400-vertex, 294,000-edge** complete source-verified Schreier HTR coset graph from P8-R4, physical right-action and representative-conjugacy oracle, to measure exact HTR contact costs for all 20 source-derived states. Original HTR costs main 5 / alternative 7. After matched moves:

| DR turn | Main HTR shortest | Alternative HTR shortest |
| --- | ---: | ---: |
| U | 6 | 6 |
| U2 | 6 | 7 |
| U' | 6 | 6 |
| D | 6 | 6 |
| D2 | 6 | 7 |
| D' | 6 | 6 |
| R2 | 4 | 7 |
| L2 | 6 | 7 |
| F2 | 6 | 7 |
| B2 | 5 | 7 |

Despite all 10 exact solved-state DR cost comparisons favoring main, **four matched pairs have exactly equal HTR contact distance** (U, U', D, D'); in six the alternative is further from HTR. Hence HTR distance by itself does not order the final whole-state geodesic cost. Example U: both HTR d=6, but actual DR completion d is **10 vs 12**. This is a direct physical falsification of scalar HTR-contact sufficiency for this task; HTR quotient remains valid for contact, not complete solved cost.

### Independent proof receipts

- [Matched ten-DR exact geodesics CI PASS #38082163320](https://github.com/WhoSia/CUBE-REV/actions/runs/38082163320) / [entire 20-state source-graded physical receipt #11680976082](https://github.com/WhoSia/CUBE-REV/actions/runs/38082163320/artifacts/11680976082), ZIP SHA-256 `b9560e881885cec98e1cd2b71075530f316e158b9b03f010c47efe41ba30e07a`.
- [Matched full-Schreier exact HTR sensitivity CI PASS #38082213361](https://github.com/WhoSia/CUBE-REV/actions/runs/38082213361) / [complete 20-state physical subgroup receipt #11681370457](https://github.com/WhoSia/CUBE-REV/actions/runs/38082213361/artifacts/11681370457), ZIP SHA-256 `6c7d085640d16ca0a118612ebacfee82c1930ac40e5c7577e04e8821bf55697f`.
- Reproducible code: `scripts/cuberev-022/verify-p8-r6-matched-DR-neighborhood-geodesics.mjs`, `scripts/cuberev-022/verify-p8-r6-matched-DR-HTR-Schreier-contacts.mjs`; two read-only GitHub Actions workflow files, `contents: read`.

## 5. Attribution limits and what would make the structural question discriminating

**Falsified:** Choosing the apparently easiest independent backward-PDB projection necessarily chooses the cheapest whole-cube continuation for these source-derived states. Also falsified: shortest HTR-contact distance alone determines the relative whole-cube completion cost for these states.

**Supported:** The identical one-step intervention applies a genuine physical group operation to the two distinct authentic-source DR endpoints; differences in the entire cube's coupled corner/edge permutation constraints persist through all ten matched comparisons. Exact distance residuals `d−h` remain model-dependent abstraction loss; a decomposition is not a unique mediator.

**NOT IDENTIFIED:** Isolated causal contribution of corner-orbit occupancy, UD-edge permutation or an individual structural coordinate. The interventions change multiple coupled variables at once, and parity constraints preclude arbitrary corner-only edits. No single cubie observable has yet been manipulated independently under a valid legal transformation. A broader controlled finite experiment with *feasible physical matching*, not impossible permutation splicing, is required.

**Human evidence:** The actual Miao source has documented two authored alternative EO→DR paths but does not publish an exhaustive timestamped candidate-search record or an explicit computed minimum-cost comparison. Twenty synthetic perturbations are **not** human candidate traces or participant actions. Neither this P8-R6 computational contrast nor its PDB residual identifies causal human choice, mental attention, deliberate exploration, or actual counterfactual execution. Other participant sources remain graded and conditional exactly as in P7. Do not create new recruitment or video collection under this stage.

## 6. P8 closure and 0.23 transition prerequisites

P8-R6 finishes the requested **radius-one matched real-cube intervention census** with two independent passing computational ecologies (exact geodesic/PDB and independent HTR Schreier). P8 and 0.22 are **not automatically version-promoted**: the P7 source grammar and full-cube physical validity, exact full-18 distance proofs for the genuine five parsed source DR candidates, and all mathematical limits must be preserved.

A proposed 0.23 charter lives separately under `docs/0.23/00_PROPOSED_TRANSITION_FROM_022_P8_R6.md` and is explicitly **NOT ACTIVE**. Its first tests should decide whether projection-rank reversal can be erased or preserved under **source-independent physically feasible control matches**, expand beyond one source family with rights-audited examples, and clarify what actual retrospective author comments can support without inventing human timelines.

**Governance:** Only authenticated `WhoSia` human author/committer on actual `research/current`; Actions read-only, no bot authored or committed changes. Do not silently modify archived R3/R4/R5 claims, old failing P7 active-set audit, or historical bot-deployment main-branch provenance. Research documentation is linked from README and canonical Notion after CI proof readback.
