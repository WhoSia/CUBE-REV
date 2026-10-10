# CUBE-REV 0.22 P1 — Task-Conditioned Belief Congruence & Minimal Costed Controller Quotients: Horizon-Relative Residual Experiments, Action-Labelled Refinement, Prior-Transport Obstructions & Physical Separation Certificates

**Status:** P1 CLOSED FOR FROZEN TWO-SOURCE PHYSICAL SUBSYSTEM / FULL TWELVE-SOURCE MINIMAL CONTROLLER HOLD. Active formal version 0.22 as confirmed by the user. [Notion version home](https://app.notion.com/p/3f5ef561cf9281d8b77ede12f15718d3). No changes to prior 0.21 evidence.

## 1. Authority and mathematical contract

This is a finite *physical instance* result, not a new universal theorem in automata theory. The project previously established G3-P23 (coarsest claim quotient), G3-P26 (dynamic intervention congruence closure), G3-P27 (separating-word test bases), G3-P29 (persistent-state belief and accumulated-path sufficiency), and 0.21 P7/P8 exact physical active sensing. Relevant earlier Notion receipts:
- [G3-P26](https://app.notion.com/p/3ddef561cf9281209cb3d5140c368fa5)
- [G3-P27](https://app.notion.com/p/3deef561cf928163b86ed1882b9a606e)
- [G3-P29](https://app.notion.com/p/3deef561cf928164ba09e6f1bfaf022f)

Original [0.15 sticker-derived physical moves](../../scripts/cuberev-015/ur-fiber-tomography.mjs) generate **18 genuine legal 3x3 HTM face-turn maps** on the **24 orientation/slot states of one tagged edge**. Initial orientation is zero and initial slot is one of 12. P1 deliberately restricts the identification task to *two unknown initial source slots* (any of 66 distinct-slot pairs, with equal weights if probabilities are needed). This does not establish minimum memory for the original whole 12-source adaptive controller.

Each legal physical turn a can be accompanied by SILENT (one turn, zero sensor reads) or READ (one turn, one intrinsic-orientation-bit read). A READ splitting the physical two-source belief into distinct bits creates two anonymous singleton success terminals. A READ producing the same bit leaves a transported two-source belief. SILENT always transports both alternatives without an output. Naming a historical original source may additionally require the known accumulated permutation, as G3-P29 already noted. This is not visual human cube inspection.

## 2. Exact reachable pair-state census

There are C(24,2)=276 unordered pairs of distinct 24-coordinate physical edge states. The 66 original zero-flip two-source pairs generate, under all common legal physical move words, **264 reachable physical pair states**. Precisely 12 other unordered pairs contain opposite-flip alternatives at the **same physical edge slot** and cannot be reached from initial different physical slots by bijective physical moves. The reachable set is closed under all 18 action maps.

## 3. Theorem A: coarsest action/output/cost-labelled congruence

Define equivalence at horizon h by identity of every permitted length-at-most-h labelled continuation experiment: the same named physical turn, same chosen READ or SILENT option, the same emitted bit and termination flags, and equivalent successor pair beliefs. Preserve action costs: 1 HTM turn per move, plus 1 sensor-read cost only when READ is chosen. The coarsest stable equivalence can be computed by monotone partition refinement of the 264 reachable nonterminal pair beliefs.

Exact original-move result:

| Maximum continuation depth | All 264 reachable pair beliefs: number of classes | Original 66 zero-flip roots: number of distinct classes |
| --- | ---: | ---: |
| 0 | 1 | 1 |
| 1 | **19** | **6** |
| 2 | **264** | **66** |
| 3 (fixed-point confirmation) | **264** | **66** |

Therefore no two distinct reachable pair beliefs can be merged by a controller representation **required to preserve every named legal action, READ/SILENT choice, observation bit, terminal predicate, and future transition**. The P0 census of four one-step *success-only* split-action profiles is not the same as the six one-step classes among original roots: raw observation-bit values add distinctions.

This is a universal interface congruence, not the coarsest representation preserving merely *one optimal policy*. Standard finite bisimulation/Mealy refinement logic is classical, and was also established abstractly in previous G3 work. The novelty claim here is the exact Rubik physical instance and its certified finite counts.

## 4. Theorem B: direct physical two-turn word certificate, separate from refinement

Independently of the partition-refinement code, the P1 verifier enumerates actual physical read transcripts for:
- 18 one-turn READ protocols;
- 324 two-turn READ then READ protocols (stop upon singleton identification);
- 324 two-turn SILENT then READ protocols.

It computes the full set of possible labelled transcripts (including singleton termination) for each of the **264** reachable two-candidate physical edge beliefs. Under only the first two categories, their response signatures yield exactly **139 distinct types**. Once SILENT then READ is added, the signatures yield **264 distinct types**.

It then checks every C(264,2)=**34,716** pair of distinct pair-belief tasks and finds an actual physically legal short separating protocol:
- **32,556** comparisons distinguishable by a one-turn READ;
- **2,160** additional comparisons require a suitable length-two protocol.

**Concrete witness of the necessity of optional omission in the declared experiment language:** current physical edge-state pair beliefs {0,3} and {0,11} are indistinguishable across all one- or two-turn protocols that always read whenever they turn and terminate immediately when identified. But SILENT(U), READ(F) gives the first pair only bit 1 (remaining nonterminal), while the second gives both possible bits 0/1 (terminal identification). The actual move names U,F are legal physical 3×3 turns.

This demonstrates strict separation of **universal choice-of-measurement interfaces**, not that hiding freely available information improves the unique best-time identification policy. If query cost is zero and only an optimal identifying policy matters, reading earlier then ignoring the extra bit may be sufficient, and a coarser policy-specific quotient may exist.

## 5. Fixed-width storage meaning and non-identification boundaries

The coarsest labelled reachable two-source interface monitor contains **264 different nonterminal pair states** and one generic terminal goal. A fixed-width state ID requires at least ceil(log2(265))=**9 bits**; 9 bits also suffice simply to assign a different ID to each of those 265 logical states. This is a narrow *logical monitor state-label bound* and is NOT a theorem about:
- the minimal controller state count for the original **12-source** P7/P8 identification task;
- minimum memory under a fixed optimal policy rather than arbitrary labelled actions;
- posterior belief values for nonuniform source priors (P0 demonstrated real-cube support-only failure);
- human cognition, actual human perception, FMC search-time cost or visual/video analysis;
- implementation memory for a controller plus its transition lookup, origin decoder or runtime clock.

## 6. Independent proof run, including retained failed stronger claim

[Executable 18-move sticker-derived Rubik P1 verifier](../../scripts/cuberev-022/verify-p1-physical-pair-belief-costed-congruence.mjs) audits the 264 reachable states, the horizon partition 1/19/264, the 139-vs-264 interface gap, every one of 34,716 direct physical separating cases, and the explicit U-silent/F-read counterexample.

[Authoritative new P1 GitHub Actions SUCCESS #38051893411](https://github.com/WhoSia/CUBE-REV/actions/runs/38051893411), [full numerical receipt artifact #11669860845](https://github.com/WhoSia/CUBE-REV/actions/runs/38051893411/artifacts/11669860845), artifact SHA-256 **b222a4e8d986a9cabebcafdf698491ecb64249030e905ee585cacacd0c465cbc**.

[Earlier P1 partition audit SUCCESS #38051682825](https://github.com/WhoSia/CUBE-REV/actions/runs/38051682825) did not yet include the independent short-protocol test. [A stronger forced-read-only certification FAILED #38051788272](https://github.com/WhoSia/CUBE-REV/actions/runs/38051788272), correctly showing only 139 distinguishable types under that restricted interface. The failed proof attempt is retained as a **falsification and repair audit**; silent-read choices were explicitly incorporated before final success. Unrelated legacy P7 repository active-set audit failures were not silently rewritten.

## 7. Literature placement and next P2 question

State identification and adaptive distinguishing experiments are classical (e.g. [Lee & Yannakakis, 1994](https://doi.org/10.1109/12.272431) and [minimum-cost adaptive distinguishing sequences research](https://doi.org/10.1016/j.infsof.2016.02.001)). Hence this result is an original **physically grounded exact instance** within existing theory, not a brand-new theory of all finite-state controllers.

**Next proposed P2:** *Optimal-Policy Quotient Geometry & Cost-Dependent Belief Compression: Horizon–Price Phase Transitions, Universal-Versus-Selective Congruence Gaps, Nonuniform-Prior Transport & Physical Minimality Witnesses.*

It must explicitly address a smaller controller that only has to preserve a chosen optimal policy under specified cost, horizon and prior. Begin with the original twelve-source physical reachable belief graph, not the entire 264-state pair family, and distinguish value equivalence from policy congruence. The user requested video/VFMC engineering and fresh human experiment recruitment to remain on HOLD.

**P1 closure:** COMPLETE AS TWO-SOURCE PHYSICAL UNIVERSAL ACTION-LABELLED EXPERIMENT QUOTIENT; 12-SOURCE OPTIMAL-CONTROLLER MEMORY STILL UNPROVEN.
