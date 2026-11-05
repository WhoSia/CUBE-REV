# CUBE-REV 0.28 — R10: Legal No-Reset P48 Lifting of Adaptive Facelet Policies

**Date:** 2026-11-05. **Evidence:** exact 3D-derived P48 physical geometry, actual legally generated edge states, adaptive decision-tree replay, read-only GitHub Actions execution. **CI verified:** [run 41994714970](https://github.com/WhoSia/CUBE-REV/actions/runs/41994714970). These are limited, controlled physical-computation results and NOT full-group identifying policies or human cognitive evidence.

## Research aim

R9 found an exact zero-error worst-case color-feedback gain in a residual edge problem: 216 of 495 remaining four-type sets need one fewer observation with feedback than with any predetermined slots, independently over four parity classes. However R9 gave the observer any desired initial spatial facelet for free and the entire initial corner state for free. R10 asks whether *routing the fixed physical two-facelet probes to adaptively selected slots* breaks the construction.

Do not evade the global cube problem: real full-cube adaptive identification remains 18–21 frames, exact fixed 21. This gate addresses physical action feasibility, not the true complete-corner-oracle problem.

## Lemma: joint probe addressability and no-free-reset transfer

Let e be any one of the 24 original spatial **edge** facelet slots and c any one of the 24 original spatial **corner** facelet slots. Under the original legal 18-HTM group, the joint P48 geometry orbit of the two stationary sensing slots is all 24 × 24 = **576** pairs. Thus an explicitly found legal turn word w(e,c) maps the chosen initial (e,c) pair into the stationary sensor facelets.

For a sequence of chosen target frames p_t, which can itself depend on prior readout colors, the legal relative action is a_t = p_t ◦ p_(t-1)^(-1). The 18-HTM action set is closed under inverse and composition, so this is executable without resetting the physical cube. The color readout after applying a_t equals the color of the selected original spatial facelets; this is verified with actual P48 output rather than inferred from a symbolic frame label.

This fact gives a **conditional action-lifting lemma**: any finite adaptive choice of such *initial spatial slots* can be physically routed with no additional *observation frames*, although it may require arbitrarily many HTM moves depending on the implemented routes. It does NOT provide the true initial corner configuration or a feasible zero-error complete-cube decision tree at the same horizon.

The mathematical group-action observation is an application of the existing R2 576-pair reachability result, not a new foundational group theorem.

## Complete physical experiment

Use the 96 parity-even arrangements of each of three representative unknown-four-edge classes, with all corners at their original solved positions and orientations. Their residual classes have exact adaptive/fixed minimax depths:

| Feedback additional depth | Fixed additional depth | Physical test cube states |
| ---: | ---: | ---: |
| 3 | 4 | 96 |
| 4 | 5 | 96 |
| 5 | 5 | 96 |
| **Total** | | **288** |

Each test begins with a fresh physical cube in a legal P48 state. It reads **sixteen individual edge facelets at eight complete spatial edge positions**, each paired with a known corner spatial facelet. It then executes the exact R9 color-conditioned decision tree, dynamically selecting the next initial edge slot and a corner companion target. For each frame, it constructs the **relative** legal turn sequence from the prior actual frame, composes and checks full 48-sticker permutations, reads both actual six-color probes, and checks the edge symbol against the independent parity-constrained 96-state enumerator. Every resulting posterior is a singleton matching the true test state.

The exact CI log records:

- physical cubie states replayed = **288**;
- individual joint six-color observation frames executed = **5,648**;
- physically executed HTM turn word lengths summed over all independent test trials = **38,732**;
- longest HTM turn word sequence for a single test trial = **149**;
- spatial edge/corner observation pairs available = **576**.

These HTM counts measure only this explicit, nonoptimized routing method. They do not establish a globally shortest motor schedule, any upper bound on a *20-frame complete cube policy*, or real human manipulation time.

**Executed source:** [R10 legal no-reset policy lift](../../scripts/cuberev-observation/audit_r10_physical_feedback_lift.py), read-only [CI step](https://github.com/WhoSia/CUBE-REV/actions/runs/41994714970). The active P7 allowlist includes source and workflow and is separately checked.

## Where the abstract oracle still differs from reality

The three physical test classes have corners intentionally set to solved in the hidden true physical state; the policy is ALSO granted the true complete corner configuration for choosing the residual parity subproblem. Therefore the sample proves that **legal physical turn routing** does not invalidate the R9 residual feedback trees. It does NOT show that the actual fixed corner sensor identifies all corners during the same 19–21 observation frames; the 16+ adaptive prefix currently makes no such guarantee.

Further, repeated individual tests start from separate prepared cubes; the 'no reset' guarantee is **within each test trajectory** only. Trials are not concatenated into a single trajectory or counted as one observation budget. The 38,732 count is a sum over separate trials and should never be used as an individual's task cost or compared to the R2 119-HTM full-cube predetermined route as if it were one route.

## Next hard R10/R11 gate: remove the oracle or prove a new obstruction

The original full-cube channel supplies one edge and one corner six-color read per frame. R2's pair addressability shows that every individual requested edge slot can be accompanied by some freely chosen corner slot; but a valid full-cube policy must jointly identify both edge and corner permutations/orientations and must infer the edge permutation parity from the actual observed corner data.

A legitimate new upper theorem would construct a full legal action-and-observation decision tree of depth 20 or less that perfectly identifies EVERY legal cube, with no preassigned true corner state, no free reset and an independently checked inverse decoder. A legitimate new lower theorem would show any depth-18/19/20 policy has an indistinguishable legal-state pair despite every possible action and past outcome, not merely failure of a fixed 16+4 family.

An immediate falsifiable attempt is to fix a candidate *joint corner-slot observation schedule* paired with the R9 edge branches, enumerate whether the resulting corner symbol histories determine the complete corner state in all branches, and test the residual edge parity inference. A counterexample must preserve actual 48-sticker legality. Do not call an uncalibrated motor-cost proxy cognitive effort.

## Position in the origin-directed programme

CUBE-REV ultimately studies how physical state, action history, observation and representation interact in human reconstruction. Mathematical action-lifting and exact feedback separation are **a precise benchmark and potential experimental intervention design**, but proof of a human history or perceptual mechanism still requires independent behavioral comparison with controlled task/goal and appropriate ethical procedures. The earlier 0.21 strict matched-state/previous-action comparison has zero naturalistic overlap; this restriction is not repaired by the R10 program.

**Custody:** GitHub human WhoSia commits; read-only CI; Notion semantic findings; Drive irreplaceable source data. The program is deterministic and reproducible, but independent mathematical audit of general claims remains open.
