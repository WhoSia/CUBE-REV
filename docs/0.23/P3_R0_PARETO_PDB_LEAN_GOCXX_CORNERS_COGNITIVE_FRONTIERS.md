# CUBE-REV 0.23 P3-R0 — Representation-Relative Difficulty and Cognitive Opportunity

**Formal stage name:** CUBE-REV 0.23 P3-R0 — Representation-Relative Difficulty and Cognitive Opportunity: Pareto-Inverted Physical PDB Bounds, Lean-Certified Order Obstructions, 2×2/3×3 Observation Fibers, Multivariate M* Resource Lattices & Source-Graded Human Skill Ecologies.

**Date / active research:** 2026-10-11. All finished results below are **physically grounded / formal proof / independent compiler PASS** where specified. The cognitive models are **hypotheses**, not measurements of human working memory or neurological activity. CUBE-REV 0.23 remains active; source-authored Miao and Dong records from P2-R2 are preserved without retelling synthetic paths as people's choices.

## 1. Why this multi-axis extension matters

The origin is physical Rubik states and feasible action, not proof engineering for its own sake. CUBE-REV 0.19 established **M*(5)=8 only for a frozen 1,192-obligation resettable fixed-observation physical model**, not human short-term memory capacity. 0.20–0.21 studied physically implemented action transports, sticker observations and observational/behavioral sufficiency limits. 0.22 developed genuine FMC source-anchored two-stage DR/HTR physical planning and PDB heuristic certificates. 0.23 P0–P2-R2 established real authored source words, actual cubie endpoints, exact shortest continuations and source-boundary opportunity signatures in **two different authored FMC competition ecologies**.

Reviewed full current Notion 0.23 and Research OS CURRENT runtime/method shelf; older Drive chat archives [24.md](https://drive.google.com/file/d/1LEwsLIaHsXfpd1_T88HVO7fq29O5eqCH/view) / [25.md](https://drive.google.com/file/d/1h_CkPn2o5Z6GAWFBdS_9jwiIkqN2e0bk/view) and prior 0.21 real-naturalistic human solve evidence as historical genealogy. Do not privilege old chat prose over actual original experiment receipts.

## 2. Exact physical Pareto rank reversal of TWO simultaneous DR pattern databases — Go + C++

Reopened independently passing [0.22 P8-R6 original 54-sticker physical court](../0.22/P8_R6_MATCHED_BRANCH_INTERVENTIONS_AND_JOINT_CONSTRAINT_CERTIFICATES.md), its [CI #38082163320](https://github.com/WhoSia/CUBE-REV/actions/runs/38082163320) receipt, and extracted a strictly integer-checked [10-intervention actual-cubie CSV](../../data/cuberev-023/p3_r0_source_matched_R6_real_PDB_10_action_census.csv). In each row apply exactly the SAME one of ten legal FB DR generator moves to Miao's two real author-written same-EO DR source states. All twenty synthetic child cubies were independently verified in R6 as actual full Rubik states, with **exact ten-DR-action distances**. This is not a 10-person cohort or 20 mentally considered human candidates.

The corner+E-slice exact projected lower bound and UD-edge+E-slice exact projected lower bound are both **weakly LOWER for the alternate** than for the main source child (in fact both **strictly lower in all ten**), while the **actual exact shortest ten-DR-turn completion is strictly LONGER for the alternate in all ten**. Therefore **Pareto reversal = 10/10**, even before taking the maximum of the two admissible PDB bounds, not merely a scalar-max anomaly.

For the original `U` matched move, actual main/alternate corner lower bounds are 6/5, UD-edge 9/7, joint max 9/7, but true full-cubie DR completion is 10/12. No coordinatewise monotone predictor of only these two PDB projected distances can be exact on both endpoints. A third new feature could fix individual rankings; this is NOT an impossibility theorem for all heuristic models.

| Metric across ten actual source-paired DR interventions | Main sum | Alternate sum |
| --- | ---: | ---: |
| Exact 10-DR-generator solved distance | **98** | **119** |
| Joint admissible PDB maximum | **82** | **65** |

Source-conditional raw staged completion gap remains **2–5 turns favoring main for all ten**, and the prior *all-18-HTM child costs* remain **uncalculated**, bounded by 1-Lipschitz rather than invented exact values. At source states themselves, exact full-18 solved distances are 9 main vs 12 alternate.

**Two independently implemented languages:** [Go standard-library checker](../../scripts/cuberev-023/rank_reversal_go/main.go) and [C++17 checker](../../scripts/cuberev-023/rank_reversal_cpp/main.cpp) parse the source-grounded comma-separated physical PDB ledger independently. Both verify exactly 10 legal move IDs, integers, both admissible component bounds, strictly inverted observed actual cost, stage cost gaps, and produce **byte-identical** result receipts. [Independent two-language CI PASS #38133579548](https://github.com/WhoSia/CUBE-REV/actions/runs/38133579548), [Go/C++ archive artifact #11699499546](https://github.com/WhoSia/CUBE-REV/actions/runs/38133579548/artifacts/11699499546) SHA256 `c347525bd17d0e7cb49d31f8fb93afd540329b6d554b23735161316c348ed2f0`. No bot code commits; Actions read-only. The original incorrect preliminary CSV field binding was identified and corrected **before** CI scientific acceptance; prior failed runs retained.

## 3. Lean 4 formal order impossibility and monotone M* resource relaxation

Independent Lean 4 file [`formal/cuberev023/PDBRankReversal.lean`](../../formal/cuberev023/PDBRankReversal.lean) and isolated pinned toolchain [`lean-toolchain`](../../formal/cuberev023/lean-toolchain), with zero external Lean dependencies, compile under Lean 4 v4.24.0 with no `sorry`/admit.

**(A) Pareto rank inversion formal theorem.** If two states have projected coordinates `cAlt≤cMain` and `eAlt≤eMain` but actual solved costs `dMain<dAlt`, then no coordinatewise nondecreasing `f(c,e)` agrees exactly with BOTH physical costs. This is a mathematical theorem about finite order, not a physically realized cube theorem in isolation. Actual original Miao `U` physical row **instantiates** it (6/5 corner, 9/7 edge, 10/12 real).

**(B) Multivariate M* feasible-set order.** Define `AttainedMinimum P n := P n ∧ ∀ k<n, ¬P k`. If resource regime `expand` admits every old feasible certificate and both minima are attained, then `min(expand)≤min(restrict)`. Also Lean proves restricting required observations and expanding the admissible action witness pool preserves feasibility under explicitly given embeddings. The result establishes formal monotonicity ONLY when the change truly **increases the feasible witness set under the SAME target requirements and scoring**. Increasing observations can carry costs and change the objective; those are NOT automatically monotone.

[Lean CI PASS in independent final #38133579548](https://github.com/WhoSia/CUBE-REV/actions/runs/38133579548), [formal proof log artifact #11699808837](https://github.com/WhoSia/CUBE-REV/actions/runs/38133579548/artifacts/11699808837), SHA256 `b96dd1a62a747b46c92cc99e3f990bfdd17c15ca36d76f65094af2cc351d55b8`. An initial Lean CI failed only due missing isolated Lake manifest, and a later draft relied on a non-core proof tactic; fixed both and re-ran to **success**. All failures remain in Actions history.

## 4. Physical 2×2 corner projection versus whole 3×3 in the SAME original legal face-turn universe

New [full 3×3 to corners-only quotient enumerator](../../scripts/cuberev-023/verify-p3-r0-corner-2x2-quotient-vs-full-3x3.mjs) uses the exact original full 54-sticker-derived cubie action and all 18 outer-face HTM turns. Enumerate the **entire fixed-frame true 3×3 full-cubie Cayley radius≤5** (distance layers **1,18,243,3240,43239,574908**, total **621,649 distinct true full states**) and then ignore ONLY the edges, retaining the eight actual corners' permutation **and orientation**. This is a **2×2-corner-like physical projection**, not the 2×2 competition's whole-rotation-equivalence quotient, nor an entire 2×2 God's-number computation.

Results independently physically certified:
- **236,552** distinct observed corner-only keys among the actual **621,649** full 3×3 states.
- **385,097** additional full states share a corner-only key with some earlier real whole-cube state.
- **152,263** corner observation keys each hide at least two distinct real full 3×3 edge states.
- Largest corner-only observation fiber contains **62** physically different whole-cube states, all in the fixed full 3×3 radius≤5 experiment. Any hypothetical deterministic independent binary questions that must uniquely resolve that whole fiber require **at least `ceil(log2(62))=6` binary outcomes** in the worst case, under the fixed same true state-set assumptions. This is an information-counting lower bound, **not** six human working-memory chunks nor six visual glances.
- Explicit real face-turn witness: **`U2 R2 U2` and `R2 U2 R2`** produce identical corner permutation+orientation but **different edge permutation and/or orientation**. The original 54-sticker reconstructions were replayed in both cases.

[Read-only physical 2×2-corner/3×3-full proof CI SUCCESS #38133695418](https://github.com/WhoSia/CUBE-REV/actions/runs/38133695418), [full cubie/alias-fiber certificate #11699339996](https://github.com/WhoSia/CUBE-REV/actions/runs/38133695418/artifacts/11699339996), SHA256 `9decdb2dba6f9e03bfcc0d8b553eebee4cee528f89d9a12beb5e9bed4c34f0f4`. An earlier attempt ran out of JS call-stack space from a 236k-argument maximum; replaced by a streaming exact maximum before obtaining valid physical CI.

**Consequence:** Task-dependent observation sufficiency is geometrically real. An ideal corner-only observation may be complete for the modeled corner goal and structurally insufficient for the full edge+corner 3×3 goal. Different goal constraints alter the required *observation and action opportunities*, even if a human's underlying neurocognitive ability were unchanged. This provides a new physical dimension for a multivariate M* construction.

## 5. Multivariate M* as a research program, not an ungrounded psychology score

Proposed formal object, still an open model not a newly measured human quantity:

```
M*(R; A, O, L, Π, B, C)
= minimum dictionary / policy resource needed to meet the exact physical requirement family R
  using physically legal action grammar A, accessible observation operators O,
  observation/action horizon L, admissible policy/algorithm class Π,
  budget/resource constraints B and explicitly defined cost functional C.
```

Keep **R (target)** fixed before applying monotonicity. If `A/O/Π/B` changes but the actual feasible witness set is not nested, even the sign of `ΔM*` may not be determined. The older CUBE-REV exact **M*(5)=8** is a specific *constant* slice of this more general mathematical object and remains unchanged.

**Competing models to falsify:** (i) physical observability, (ii) finite dictionary of learned chunked algorithms, (iii) recognition/inspection opportunity, (iv) speed/ergonomic execution, (v) source-annotated conditional planning, (vi) real human working-memory/cognitive-flexibility measures. These are different variables, potentially interacting. WCA solve seconds alone cannot identify which is responsible.

## 6. Genuine existing human data, psychometrics, and rights boundary

### Already-held secondary human action corpus — 3×3, not newly fabricated

The [historical 0.21 P3 naturalistic human reconstruction audit](../0.21/P3_NATURALISTIC_451_P25_EXACT_REJOIN_AND_FMC_PROCESS_EVIDENCE.md) documented **452 archived solve IDs but only 451 unique full reconstruction contents**, around **25,272** nonterminal next-action rows and **25,723** state snapshots including terminals. These actual reconstruction actions include slices, wide turns and cube rotations as well as simple faces; don't misparse as all-18 HTM. Source custody resides in an **existing PRIVATE Google Drive archived derivative**, which must NOT be mirrored to a public GitHub repository. Original G7-P24 FC3/FC4/FC6 60-source rejoin exact; 451-source descriptive contrast `ΔD≈+0.0207` is NOT prospective held-out human mechanism confirmation. The follow-on [0.21 P4 stage/frame confounding study](../0.21/P4_NATURALISTIC_BEHAVIORAL_STATE_SUFFICIENCY_SOURCE_CONFOUNDS_AND_FMC_SEARCH_TRACE_TRIAGE.md) loses matched source-stage support: cross-source collision pairs **1442→151→62→10→1** with tighter frame/stage/history restrictions; no clean causal test after stage matching. **This evidence is meaningful precisely because the human behavior problem is hard; no new participants necessary.**

### WCA official 2×2 / 3×3 public result source — suitable outcomes, NOT unobserved cognition

[Official WCA results export](https://www.worldcubeassociation.org/export/results), currently V2.0.2 with 2026-10-10 metadata, contains event types, results, attempt-level result values, official scramble metadata and persons/competition IDs. Valid for publicly attributable *outcome* distribution analyses after actual export download and license/attribution checks; 2×2 and 3×3 event results cannot by themselves show exact visual attention, learned algorithms, per-move timing, inspection contents or mental decision speed. The published [2026-04-01 WCA regulations](https://www.worldcubeassociation.org/regulations/) state inspection is allotted strictly less than 15 s; this is a rule governing an opportunity budget, NOT a per-athlete observed inspection duration. This stage verified official public schema and current release but **did not fetch/extract the 363 MB entire WCA TSV to produce novel participant statistics**. No 2×2 per-move human traces acquired yet; label `2x2_BEHAVIORAL_TRACE_HOLD`.

### Actual primary psychology full text already in canonical Drive

Read actual stored original [Meinz et al. (2023), “Ability and Nonability Predictors of Real-World Skill Acquisition: The Case of Rubik’s Cube Solving”](https://drive.google.com/file/d/1evZEtiF9f1oyg9kjMctEKVZ3VFmec6mA/view) (Journal of Intelligence 11:18; DOI 10.3390/jintelligence11010018), N=79 trained novice learners under a seven-step procedure. **Their** observed Gf score predicted solve performance/efficiency; WMC and investigated nonability factors did not add equivalent predictive value in their reported analysis. The study is on **novice teaching**, not expert Roux/CFOP/Ortega multi-algorithm search, does not prove a brain subsystem mechanism, and does not permit individual psychological inference from WCA times. They assessed skill acquisition within that experiment, not an individual speedcuber's mental deliberation.

Additional prospect for broad historical learning: [Krakauer, Kardeş, Grochow (2025), “Universality in Collective Intelligence on the Rubik's Cube,” arXiv 2511.18609](https://arxiv.org/abs/2511.18609). **Drive 미확보(색인 검색 기준); 직접 PDF 미확인.** Abstract-level context only, not a read-and-validated original; do not cite as definitive neuroscientific evidence. Source and derived participant rights need audit before any person-level joins or broad redistributions.

## 7. Next falsifiable experiment, no invented recruitment

**P3-R1 — Resource-Indexed Observation–Algorithm Frontier & Heuristic Recognition Transfer:** choose fixed original physical cube tasks and a precommitted observation/action/recognition budget grid; compute a Pareto surface of physical coverage and deterministic move cost for (a) 2×2 corner goal vs (b) 3×3 corner+edge goal. Preserve the old 0.19 resettable dictionary slice as baseline, add a syntactically fixed bounded algorithm grammar representing *hypothetical learned snippets* without asserting what any participant knows. Use Go/C++ for exact independent finite enumeration, Lean to prove nesting/order lemmas, Rust/JS real sticker oracle for geometry. If time is measured, keep turn execution, observation and pause/inspection data separately. Reuse private 451 reconstruction corpus only inside approved private environment with author-split held-out grouping and strict phase/frame controls; human heuristics are an empirical **test**, not output of group theory.

**P3-R2 — source-authored human candidate choice and PDB rank reversal transfer:** find new independently human-recorded alternate paths across actual 3×3 FMC or 2×2/3×3 speed solve; freeze their source and side grammar before rendering counterfactuals; test whether candidate selection follows lower projected h, exact shortest distance, sticker-recognition opportunities or conventional algorithm tokens. Only with genuinely observed event order/time may distinguish heuristic/recognition vs deliberation. Avoid categorical “System 1 vs System 2” neural mapping from moves alone.

## 8. README retirement and governance

The prior full **0.21 historical empirical/active-era README section (6,746 characters)** was copied to a real **text/markdown file in Google Drive**, [CUBE_REV_021_README_HISTORICAL_RETIRED_20261011.md](https://drive.google.com/file/d/1GoOQpUTROhKxIIYFGRQhN0fH-tc6-vsx/view), and its archived section independently fetched from Drive **exactly matched** the previous active README substring. Only then was that obsolete README prose removed and replaced by a short link. All `docs/0.21` source reports, proof code, CI receipts, old Notion and commits are preserved: no destructive rewrite, and no old scientific findings swept aside. Archive contents have repository-root-relative internal Markdown links; open them from GitHub if navigating. Drive 80_ARCHIVE folder accessed via the connected Library upload workflow with full readback.

Read-only GitHub Actions; no new bot-authored commit. The P7 exact-path allowlist must be expanded ONLY by reviewed explicit new source paths and Git blob SHA, not blanket folder exceptions. Existing separate historical non-default-main bot deployment provenance is not secretly repaired. A clean active-set path audit checks tracked files against approved paths; it is not a grant of scientific accuracy to every old research result.
