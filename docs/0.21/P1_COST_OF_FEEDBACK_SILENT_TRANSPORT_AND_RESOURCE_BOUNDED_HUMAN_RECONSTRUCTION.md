# CUBE-REV 0.21 — P1: The Price of Physical Feedback, Silent Preparation, and Human-Bounded Reconstruction

**Version continuity:** This is an additive P1 chapter within the formal 0.21 title *Active Reconstruction of the Rubik's Cube: Observation-Driven Action Selection, Belief-State Dynamics, Physical Information Access & the Limits of Adaptive Solving*. It preserves all 0.15, 0.18, 0.19, 0.20 results, source receipts, historical failures and open verification obligations.

**Research lenses:** real 3×3 Rubik edge mechanics; exact physical decision-tree computation; human active information seeking; behavioral economics of deliberation, attention, memory and cognitive effort. The scientific object stays the same physical cube rather than a replacement generic finite automaton.

## I. Frozen real-cube ontology and unconfounded comparison

- Physical process: original 18 face moves in HTM, real 3×3 sticker-derived 24-state *tracked UR edge* position/orientation maps, intrinsic orientation after every selected turn.
- Same initial state set for both controllers: twelve possible edge positions, each with initial intrinsic orientation 0, bitmask `0x555555`.
- A single *preset word* fixes the entire future move sequence before seeing observations. An *adaptive policy* can choose the next physically legal turn based on the exact observed sequence and updated state-support set. Both get the same one-bit sensor each turn and know their own executed moves.
- Exact worst-case unit is **number of HTM face turns to distinguish the original initial slot among 12**. It is NOT 0.18/0.19's independent-reset experiment dictionary cardinality `M*(L)`, NOT solved-full-cube distance, human reaction time, or FMC.

**Matched physical optimum:**
`D_fixed_single_word(0x555555)=9`, inherited from the exact L8 physical exclusion and L9 positive witness in the historical [0.19 P5](../0.19/P5_EXACT_OBSERVABILITY_HORIZONS_COLLISION_PAIRS_AND_ADAPTIVITY.md).
`D_feedback_minimax(0x555555)=7`, originally from the unmodified 0.15 `adaptiveOrientationDepth`, independently rechecked by 0.21 P0 and again in P1.
The exact **worst-case physical feedback saving** is `9-7=2 HTM moves` (`2/9=22.22%` relative to worst-case single preset word). Do not claim this as a new result independent of the inherited 0.19/0.15 source proofs.

A particular 9-HTM fixed witness is `F B U R2 F B' U F B`, with twelve-start successive rank sequence `[2,3,3,3,6,9,9,11,12]`. Direct replay verifies all twelve final nine-bit histories are distinct. The new P1 CI replays the witness, **not the entire 0.19 exhaustive length-8 lower bound**, whose historical finite receipts retain their own grades.

## II. Explicit initial-prior expectation and an adaptive policy trace

For the *specified* prior uniform over the twelve possible initial slots and **stopping as soon as the current original slot is identifiable**, allow a prescribed adaptive controller with a max-depth seven constraint. Define `S(B,h)` as the minimum sum of remaining face-turn counts over all physically possible states in B, where `S=0` for singletons, and
`S(B,h)=|B|+min_{a∈18 HTM} Σ_{z: B[a,z]≠∅}S(B[a,z],h-1)`
with invalid horizon branches assigned infinity.

Exact result on the unchanged oracle:
- All **twelve** original source states have distinct, machine-replayed observation-contingent action traces terminating by seven turns.
- Minimum total turns under max-depth seven: `S(0x555555,7)=71`. Thus the uniform-prior mean is **71/12 = 5.91666… turns**, with worst-case seven. For the explicitly tested larger horizons eight, nine and ten, the same minimum sum was returned; do not extrapolate to an unbounded-horizon optimum without a separate stopping theorem.
- Trace depth distribution among the twelve equally likely sources: **one 4-turn, three 5-turn, four 6-turn, four 7-turn**.
- For *this one fixed nine-turn witness*, stopping at the earliest identifying prefix produces depth distribution **two 5-turn, four 6-turn, four 8-turn, two 9-turn** and uniform-prior mean `84/12=7`. Consequently the comparison of these two explicit executable protocols is a difference of `84/12-71/12=13/12≈1.08333` expected moves. This does NOT prove that seven is the globally minimal early-stopping expectation over *all* preset words with arbitrary lengths.
- The only actions attaining the worst-case optimal seven at the first step of the original twelve-source belief are `F,F',B,B'` (all other actions have depth eight under a forced first move). This is a physical orientation-access fact, not a behavioral data fit.

## III. Physical 'silent transport' obstruction — a prospective cognitive challenge

After taking `F` and seeing orientation bit 0, followed by `B` and seeing orientation bit 0, the posterior *current-coordinate* belief is exactly four positions `B=0x1111`. This branch occurs within the physically derived original oracle, not a noncube countermodel.

**Exact finite physical finding:** For **each of the 18 legal HTM turns** `a`, `B[a,0]` or `B[a,1]` is empty, i.e. the immediate orientation observation provides **no separation among the four candidate states**. Nonetheless the exact remaining minimax identification depth is `D(B)=5`. One physical legal `U` turn is uninformative (the belief stays cardinality four) but repositions the candidates so that a following `F` divides the beliefs **3+1**. Thus a preparatory physical manipulation can have zero immediate Shannon information and positive future diagnostic value.

This is a **fixed-ontology exact 18-action finite statement**, not a universal law about all hidden-state systems or a human response. Even in this physical court, 'immediate information gain = 0' does NOT imply 'no useful action'. The mechanism is transported edge positions under legal cube moves, inherited from the 0.20 transported-cut theory. The P1 executable script also records a deterministic one-step-worst-cardinality greedy policy (tie-break in original 18-move registry order) that fails to identify some initial slots within a 20-turn probe. This is a counterexample only to **that explicit heuristic**, not to every policy described informally as greedy.

## IV. Cognitive-science literature and precisely delimited bridge hypotheses

Primary articles checked by current external bibliographic search:
1. Najemnik & Geisler (2005), *Optimal eye movement strategies in visual search*, Nature, doi: [10.1038/nature03390](https://doi.org/10.1038/nature03390). Ideal observer and observed human eye-movement comparison in visual target search, **not** Rubik's orientation sensing.
2. Gottlieb, Oudeyer, Lopes & Baranes (2013), *Information-seeking, curiosity, and attention: computational and neural mechanisms*, Trends in Cognitive Sciences, doi: [10.1016/j.tics.2013.09.001](https://doi.org/10.1016/j.tics.2013.09.001). Review of curiosity, novelty, intrinsic information sampling, attention; does **not** supply a 7/9 physical Rubik estimate.
3. Petitet et al. (2021), *The computational cost of active information sampling before decision-making under uncertainty*, Nature Human Behaviour, doi: [10.1038/s41562-021-01116-6](https://doi.org/10.1038/s41562-021-01116-6). Empirical active sampling incorporates measurable cognitive-effort costs.
4. Lieder & Griffiths (2019/2020), *Resource-rational analysis: Understanding human cognition as the optimal use of limited computational resources*, Behavioral and Brain Sciences. [Publisher](https://www.cambridge.org/core/journals/behavioral-and-brain-sciences/article/abs/resourcerational-analysis-understanding-human-cognition-as-the-optimal-use-of-limited-computational-resources/586866D9AD1D1EA7A1EECE217D392F4A). Computational-resource-limited normative lens; NOT a claim all humans are ideal.
5. Meinz et al. (2023), *Ability and Nonability Predictors of Real-World Skill Acquisition: The Case of Rubik's Cube Solving*, Journal of Intelligence 11(1):18, doi: [10.3390/jintelligence11010018](https://doi.org/10.3390/jintelligence11010018). Actual N=79 novice instruction, skill acquisition study, **not** evidence for this specialized hidden UR-edge orientation task.

**Pre-registered contrast worth testing:** A human participant may prefer immediately informative turns over the 'silent' setup, or choose a silent setup successfully given a preview of its two-step orientation consequence. Control for manual familiarity, turn-instruction understanding, history visibility, prior Rubik expertise, and choice time. Memory bottlenecks and incorrect posterior updates can be experimentally dissociated with external scratchpad / perfect orientation-history display.

## V. Behavioral economics: costed information acquisition, not automatic human ideality

6. Gabaix, Laibson, Moloche & Weinberg (2006), *Costly Information Acquisition: Experimental Analysis of a Boundedly Rational Model*, American Economic Review 96:1043–1068, doi: [10.1257/aer.96.4.1043](https://doi.org/10.1257/aer.96.4.1043). Experimental directed cognition and information-acquisition cost, not cube turns.
7. Sims (2003), *Implications of rational inattention*, Journal of Monetary Economics 50:665–690, doi: [10.1016/S0304-3932(03)00029-1](https://doi.org/10.1016/S0304-3932(03)00029-1). An information-capacity model of economic control, not a directly fitted Rubik cognitive mechanism.

Candidate falsifiable economic controller:
`J(π)=c_T E_π[N_turn]+c_Q E_π[N_active_choice]+c_M E_π[memory_operations]+c_E Pr_π(error)`.
The terms are operational measurement targets, **NOT fitted human parameters**. Deliberation/time/effort costs can outweigh saved rotations. For an explicit illustrative model in which adapting incurs extra overhead `κ` per executed turn but a preselected word does not, the **worst-case** costs `7(1+κ)` and `9` cross at `κ=2/7`. Using the early-stopping fixed witness and uniform-prior adaptive policy instead, `(71/12)(1+κ)` and `7` cross at `κ=13/71`. These thresholds derive entirely from **declared hypothetical costs**, not observed psychology, and are not universal economics theorems.

## VI. Human experiment with valid physical-cube semantics

The laboratory information interface must preserve the source oracle: 18 real HTM face actions, post-turn readout of the **identity-tracked UR edge intrinsic flip** (a specialized binary sensor, not ordinary unrestricted naked-eye cube vision). A digital replay simulator based on physical stickers suffices for a pilot; a physical instrumented cube or independently validated sensing rig would be a second-stage ecological test.

Suggested randomly assigned trial conditions:
- **Fixed/preset:** choose a whole action sequence before receiving readings; allow transcript-based early stopping if explicitly part of the comparison.
- **Feedback/active:** next turn can depend on revealed orientation bit.
- Within participant or randomized counterbalanced **history-visible vs history-hidden** and **low vs high choice-time/action costs** conditions, recording comprehension and familiarity; avoid mixing these costs into the initial 7/9 HTM theorem.

Pre-specified outcome measures: correct hidden start-slot identification, conditional sequence of legal turns, worst-case/mean turn count, elapsed deliberation time, posterior calibration, fraction of silent information-preparation actions chosen, and behavior after `B=0x1111`. Compare ideal minimax policy, immediately-greedy physical baseline, and costed resource-rational controller by out-of-sample predictive likelihood or preregistered model comparison. The user has provided **no human response data**: this is an experimental protocol, not a result.

**Falsifiers:** If participants routinely execute useful silent physical preparations even without consequence previews, simple instantaneous-entropy greedy models are falsified; if predicted cognitive overhead fails to explain when feedback is abandoned, the proposed cost model needs replacement; if apparent physical observability requires showing unavailable hidden state, reject that interface's ecological claim.

## VII. Next mathematical return (keep on roadmap, do not prematurely switch away)

Future automata/TCS research should address what part of a complete 24-state belief is truly necessary as **finite controller memory** to implement a cost-sensitive policy, and distinguish observational continuation equivalence from source-state equality. This may eventually demand a Myhill–Nerode-like minimal observation-history controller theorem, but there is NO new automata minimization theorem in P1. First measure human selection and information-cost effects under the real physical transition protocol.

## Verification grade and custody

- [External P1 GitHub Actions run — SUCCESS](https://github.com/WhoSia/CUBE-REV/actions/runs/38040188831) source commit `9d2997e7b59c9f964e25791d56f00bede3b9824e`.
- [P1 proof receipt: exact 12-start source trajectories, path length distributions, original nine-turn positive witness, 18-action silent state](https://github.com/WhoSia/CUBE-REV/actions/runs/38040188831/artifacts/11665274078), emitted artifact ZIP SHA256 `8ba6c53bdb730944fec808a0bd6af92c53dbd4c0cc2bfd76b5eb6b351175c621`.
- [Source checker](../../scripts/cuberev-021/verify-p1-feedback-silent-action.mjs) calls [unmodified physical sticker-derived oracle](../../scripts/cuberev-015/ur-fiber-tomography.mjs), uses independent 7-depth feasibility and exact 12-source policy replay.
- **External P1 CI is not a rerun of the 0.19 complete L8 negative certificate.** Nor is it full-cube solving, a human study, or a general automata theorem.
- Notion [0.21 continuity home](https://app.notion.com/p/3f5ef561cf92815e86efc7d923b6ffa8), older 0.20 and prior remain preserved. P7 legacy active-set failure remains separately tracked.

**P1 state:** mathematical physical feedback comparison REPLAY/PASS; literature bridge sourced; behavioral hypothesis/protocol OPEN; no behavioral effects or samples observed yet.
