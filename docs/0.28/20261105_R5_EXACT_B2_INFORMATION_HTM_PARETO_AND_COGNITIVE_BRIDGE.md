# CUBE-REV 0.28 — R5: Exact finite information/action Pareto court and research-program differentiation

**Date 2026-11-05. Status:** Exact integer-DP mathematics and implemented P48 finite-court code; remote CI outcome must be verified for the final R5 code before declaring a new certified numerical frontier. The full Rubik color-channel adaptive identification horizon remains 16–21; the fixed/nonadaptive horizon is exactly 21 (R3). No human behavioral data are claimed.

## 1. Research target and epistemic boundaries

The ambition is to explain *how physical actions, state legality and limited sensory readouts jointly constrain identification*, then derive predictions falsifiable against changes in observation channel, action repertoire, and eventually measured behavior. This is **not** a claim that the standard ideas of belief-state planning, decision trees, cost-sensitive observation or Pareto optimization were invented by CUBE-REV. HTM count is a physical action-count proxy, **not** human cognitive effort.

Exact R5 is deliberately a small proof court: legal P48 B2 = 262 original states; two categorical stationary facelet probes; first simultaneous readout at identity; then either no motion or exactly one legal 18-HTM move; one additional two-color readout. The chosen second action is either fixed before seeing colors or selected adaptively from the first-color result. Every query/turn is actually applied to the original independent P48 physical cubie/sticker model.

## 2. Two distinct minimization criteria

Let initial states be uniformly distributed over B2 of cardinality N=262. After the first colors, branch j contains n_j possible original states. Let n_{j,a,y} denote the cardinality of the second-color subbranch y for physical second-turn action a.

Define the expected second-turn cost in state-mass integer units:

```
A(pi) = sum_j n_j * 1[pi(j) is a legal non-identity HTM turn]
E[additional HTM]= A(pi)/262.
```

Define residual uncertainty as *average posterior belief cardinality*, not Shannon entropy:

```
M(pi)=sum_j sum_y n_{j,pi(j),y}^2
E[|B_final|] = M(pi)/262.
```

The square sum is a collision statistic. Writing p_y for the probability of a complete observation transcript under the uniform prior, one obtains the exact, useful identity:

```
E[|B_final|] = N * sum_y p_y^2 = N * exp(-H_2(Y)),
H_2(Y)=-ln(sum_y p_y^2).
```

Thus minimizing expected residual *cardinality* maximizes Rényi entropy of order 2 of the transcript under the stated uniform prior. This does **not** prove the policy also maximizes Shannon information, minimizes worst-case belief cardinality, or minimizes decision time. It is an algebraic identity, not claimed new theory.

## 3. Exact finite Pareto dynamic program

Within one branch j, all 18 physical nonidentity second-turn choices have the same additional HTM cost n_j. It therefore suffices for the two-objective (A,M) calculation to keep the one-turn action with minimal squared residual

```
m_j = min_{a in 18 HTM} sum_y n_{j,a,y}^2.
```

The no-turn action is a repeat observation, so has cost 0 and squared residual n_j^2. After processing j branches, the exact minimum possible M for each exact integer A follows

```
F_0(0)=0
F_{j+1}(c)=min{
    F_j(c)+n_j^2,
    F_j(c-n_j)+m_j
}
```

(infeasible terms are +infinity). Remove dominated pairs to obtain the complete attainable Pareto frontier **for this declared finite B2/two-readout/one-turn class**. This is an exact, finite multiple-choice knapsack proof, not a heuristic or an arbitrary weighted scalarization.

The executable `scripts/cuberev-observation/audit_color_p48_r5_exact_b2_pareto.py` builds every physical observed branch, records the full integer Pareto frontier, and cross-checks it against independently calculated scalar-penalty minima for many specified penalties. It additionally rechecks the R4 endpoints of M=1976 for unconstrained adaptive action selection and M=2242 for the best precommitted one-move second action, and the exact worst-case residual cardinality 18 for both choices. The numerical frontier should be cited from the actual executed source and remote CI log, not invented here.

**Critical limitation:** This 2D Pareto frontier does not incorporate belief-state-dependent motor execution time, observation error, or a cognitive cost parameter. A richer 3D+ frontier should treat those as measured or explicitly hypothetical quantities, not substitute HTM counts for human effort.

## 4. Scientific value and direct prior work

The mathematical contribution currently grounded is an exact reproducible physical Rubik-cube instance demonstrating how feedback improves a *mean* belief statistic without necessarily improving the *worst-case* statistic. This is an illustrative instance, not yet evidence of new general active-perception theory.

Important direct prior-art candidates:
- Aronsson, Rahbar & Chehreghani, **A Survey on Active Feature Acquisition Strategies**, IJCAI 2026, https://doi.org/10.24963/ijcai.2026/860. Explicit POMDP/cost-acquisition formulations make broad generic novelty claims indefensible.
- Zarei et al., **The electrocortical activity of elite Rubik's cube athletes while solving the cube**, *Experimental Brain Research* (2025), https://doi.org/10.1007/s00221-025-07104-w. This examines human Rubik planning/execution, but does not validate our color-probe model or equate HTM length to cognitive cost.
- A human visual-working-memory / action-plan study (2024), PubMed 39052393, examines action plan certainty and VWM. It is relevant as a possible mechanism **hypothesis**, not proof for cube identification.

Before any paper uses these as load-bearing authorities, verify exact canonical PDFs in Research OS Drive and compare claim-by-claim rather than relying on search snippets.

## 5. Next hard problem: a reusable structure, not bigger arithmetic

Develop exact multi-horizon policy certificates (small radius first) and test whether legality constraints create a *provable separation* between worst-case required observations and minimum expected action cost. A nonadaptive failure on all 20-facelet masks does not settle the full-group adaptive 16–21 horizon. Seek a state-pair adversary or a full-policy upper certificate rather than calling finite R5 Pareto points an answer to the full-group minimum.

For eventual empirical work, prespecify a protocol comparing real participant completion time, manipulation errors, re-observations and perceived/operational difficulty **on matched observation accuracy and actual motion requirements**; do not assign human numerical cost weights before independent measurements.

## 6. Provenance and custody

Executable source: [R5 exact B2 Pareto](https://github.com/WhoSia/CUBE-REV/blob/research/current/scripts/cuberev-observation/audit_color_p48_r5_exact_b2_pareto.py). Read-only CI workflow: `.github/workflows/cuberev-observation-generalization.yml`; it runs the physical audit and checks receipt markers. P7 active manifest is updated separately. GitHub WhoSia author/committer only, bot writeback prohibited. Notion carries semantic claim limitations; Drive is the designated custody surface for irreplaceable raw proof bytes, not for re-created generic smoke logs.

**Current verdict:** R5 finite Pareto method complete in code; numerical results and remote verification must be quoted from actual receipts; a general geometric theorem and a cognitive-science claim remain OPEN.
