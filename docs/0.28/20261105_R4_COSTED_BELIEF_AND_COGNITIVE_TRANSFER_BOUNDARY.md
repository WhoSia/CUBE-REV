# CUBE-REV 0.28 R4 — Action-cost, belief refinement, and the boundary of cognitive claims

**Status 2026-11-05:** Mathematical finite-case research + explicit proposed empirical bridge. Exact full-group adaptive color optimum still 16–21; nonadaptive exactly 21 (R3). **This document is not a human-subjects experiment or a cognitive-science result.**

## Why the previously minimized 119 HTM is not a human cost

119 HTM is the demonstrated length of a particular executable, no-reset 21-frame route over specified 6-color facelet readout positions. It is neither the shortest possible route nor a measured time, eye-movement burden, working-memory demand, motor difficulty, energy consumption, or error probability. Distinguish four outcomes:

1. **Information:** number of facelet observations, exact identification, residual legal belief-set cardinality.
2. **Geometrical/motor proxy:** 18-HTM count and exact P48 motion replay, with costs fixed by declared action alphabet.
3. **Human behavior:** time, errors, pauses, reacquisitions, strategy/learning under participant measurements; **not measured here**.
4. **Human cognitive processes:** memory, visual attention, chunking, planning and orientation updating, inferred only through an independently validated measurement model; **not established here**.

This separation is essential. HTM action count is a reproducible robotics/active-sensing *proxy*, not a cognitive datum. Prior art already combines information-gathering, motion and sensor costs in POMDPs and active sensing; Rubik-cube human EEG/planning has also been studied. Novelty needs a specifically supported Rubik legality/geometry result or a genuinely discriminating human prediction, not the mere addition of weighted cost.

References (external, prior art; need canonical Drive PDF for load-bearing claims):
- Veiga & Renoux, *From Reactive to Active Sensing*, ACM Computing Surveys (2023), DOI 10.1145/3583068.
- Kurniawati, *POMDPs and Robotics*, Annual Review of Control, Robotics, and Autonomous Systems 5 (2022), DOI 10.1146/annurev-control-042920-092451.
- Zarei et al., *The electrocortical activity of elite Rubik's cube athletes while solving the cube*, Experimental Brain Research 243 (2025), DOI 10.1007/s00221-025-07104-w.

## Precise R4 decision model

An unknown legal initial state `g` is fixed; the known physical orientation frame `p` tracks our executed turns. A legal physical action `a` changes `p` to `a p`. Reading one edge-facelet color and one corner-facelet color at the stationary probes returns `y=o(g,ap)`. An exact belief `B` of possible initial states is updated to

```
B_y = {g in B : o(g, a p) = y}
```

For bounded horizon `t`, exact identification with a **worst-case** additive cost may be written, with positive observation price `c_obs` and a grounded physical action cost `c_move(a,p)`:

```
V_0(B,p) = 0 if |B|=1, else +infinity
V_t(B,p) = 0 if |B|=1, else
  min_{a feasible} [ c_move(a,p) + c_obs +
                     max_{y: B_y nonempty} V_{t-1}(B_y,ap) ].
```

If actions are allowed without immediate observation, an enlarged state/action model and explicit time/turn budgets are required. For expected rather than worst-case cost, replace max by a posterior-weighted sum **only after** specifying a prior. Do not equate these objective functions. Preserve Pareto vectors (frames, HTM, error) rather than choosing arbitrary weights as if calibrated.

## Actual small physical pilot: B2, 262 states, two frames, <=1 HTM between frames

For a bounded finite calibration, fix the actual P48 one-edge/one-corner six-color probes from the R2 channel. First frame has no movement. For the second frame choose either identity or one of the eighteen legal HTM moves. Nonadaptive plans choose the same second action for every first observation; adaptive plans choose by the observed first two-color symbol. The candidate hidden states are **exactly the 262 legal B2 states**. These two frames do **not** identify every state; the measured target is residual belief size.

With the explicitly hypothetical **uniform prior on B2** and exact observations, mean residual posterior cardinality is

```
E[|B_after|] = (sum over terminal observations y of |B_y|^2) / 262.
```

The finite P48 court yields:

| Objective | Adaptive second action | Best fixed second action |
|---|---:|---:|
| Mean residual size, uniform B2 prior | 1976/262 = 7.542 | 2242/262 = 8.557 |
| Relative improvement | 11.8644% smaller | reference |
| Worst-case residual size (separately optimized) | 18 | 18 |
| Complete state identification within two frames | **NO** | **NO** |

The same worst-case score demonstrates the crucial difference between average information gain and guaranteed exact identification. The 11.8644% is a mathematical finite-case result, not a human performance improvement. Both fixed and adaptive policies pay no more than one physical HTM before their second sample; their *conditional expected* action usage may differ. The local proof scan checks all physically possible first-color branches and 19 physically valid second-frame actions, not a guessed global planner.

The accompanying repository source `scripts/cuberev-observation/audit_color_p48_r4_b2_costed_beliefs.py` reuses the independent P48 3D physical state generator and original color probe contract. Initial independent execution reproduced 262 states and both posterior-score numerators; full remote read-only CI verification must be checked before marking remote PASS.

## How to approach a real-world / cognitive bridge

A credible downstream experiment would *pre-register* comparative predictions rather than merely collect solving times:
- Between policies matched for observation count but differing in HTM route difficulty, does elapsed action time track HTM or a better measured motion predictor?
- Between policies matched for executable action cost but differing in legal-invariant inference load, does response time or error change? Randomization and training level have to be controlled.
- Among policies that equalize sensor positions/number of queries, does a noise-tolerant plan reduce observed re-observations under controlled facelet misclassification?

Separate **observation noise**, **motor execution**, **decision latency**, and **reconstruction accuracy**. Record participant prior familiarity, training, task order, hardware/camera and illumination; avoid treating a numerical prior on cube states as a human psychological prior. An approved study protocol would be needed before making any empirical participant claim.

## Open mathematical and experimental gates

1. Full-group adaptive color horizon: `16 <= h_adapt <=21`; exact value OPEN.
2. Prove whether adaptive actions can beat 21 for a full-group zero-error protocol; static-mask collisions alone do not prove the opposite.
3. Costed full-group policies: HTM-minimal joint sensing/turn schedule OPEN; 119 HTM is only an achieved upper bound.
4. Novelty: measure contribution beyond already known active-sensing/POMDP and Rubik recognition prior art.
5. Human contact: no actual behavior, EEG, gaze or timing evidence in CUBE-REV R4; claims remain hypothetical.

**Doctrine:** GitHub human author/committer only, no bot writeback; read-only CI, P7 registered active set; Notion is semantic authority, Drive holds T2 original bytes when produced. Not all interesting finite computations deserve publication.
