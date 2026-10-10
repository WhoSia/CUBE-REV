# CUBE-REV 0.22 P2 — Optimal-Policy Quotient Geometry & Cost-Dependent Belief Compression: Horizon–Price Phase Transitions, Universal-Versus-Selective Congruence Gaps, Nonuniform-Prior Transport & Physical Minimality Witnesses

**Research status:** P2 exact physically legal chosen-policy reconstructions PASS / adversarial belief-model insufficiency PASS / globally minimum full 12-source FSC and empirical human-belief inference HOLD.

**Canonical version:** [CUBE-REV 0.22 Notion](https://app.notion.com/p/3f5ef561cf9281d8b77ede12f15718d3). Frozen 0.21 P8 physical Pareto theorem, 0.22 P0 nonuniform-prior counterexample, 0.22 P1 264-state two-source universal congruence and G3-P23/P26/P27/P29 dynamic-quotient work remain authoritative.

## 1. The M-star(L) objection: do not hide essential dimensions behind one symbol

The original [0.19 exact M-star(5)=8 source](../0.19/P13_FINAL_EXACT_PHYSICAL_MSTAR5_EIGHT.md) **already assumed** the specific 1,192-source family, actual 18 HTM moves, five observation bits, perfect reset, nonadaptive fixed-word experiments, and unit dictionary-word cost. Changing the source family changes the optimum, as [0.20 documents](../0.20/P0_P2_TRANSPORTED_CUTS_AND_NONNESTED_DICTIONARY_EXTENSION.md): five-element sources alone need 7 fixed five-move tests versus 8 for the full originally admitted family. Thus the one-variable notation is a *conditional slice* of a richer design problem, not a universal physical law indexed only by L.

**Direct analogue:** The current 24-bit edge support mask describes a **normative analyst belief under a frozen physical oracle**, not a universal sufficient representation for every task or a measured psychological state. Define a task descriptor theta = (hidden states, legal actions, physical transitions, observation law, prior/model uncertainty, terminal decoding goal, loss/risk criterion, move/read costs, horizon, query budget, available information). The correct question is which task-relative compression Xi_theta(history) preserves the controlled future experiment predictions and the particular required outputs/costs. We should not inflate the state with irrelevant variables, but must test each omitted variable with explicit counterexamples. Different notions of minimal controller state must not be conflated.

## 2. P2-A: full 12-source Rubik optimal policies and their residual decision states

The P2 executable verifier imports genuine [original sticker-derived 18 legal Rubik HTM action maps](../../scripts/cuberev-015/ur-fiber-tomography.mjs). A single tagged edge begins uniformly distributed among 12 originally flip-zero source slots, the ideal sensor reports one intrinsic flip bit, and any real face turn can be followed by an optional sensor read. The exact root identification task has **maximum seven physical turns**, with optional hard cap of four observations. The cost is mean actual turns plus lambda times mean actual observations.

**Full 12-source chosen-policy audit (integer sums over 12 sources):**

| Task | T | Q | Distinct chosen (physical belief, budget) nonterminal states | Anonymously terminating future policy subtrees incl. terminal | Original-source-naming future policy subtrees incl. terminals |
| --- | ---: | ---: | ---: | ---: | ---: |
| Max seven turns, lambda=0, reads uncapped | 71 | 45 | 19 | 17 | 31 |
| Max seven turns, lambda=1, reads uncapped | 71 | 45 | 19 | 17 | 31 |
| Max seven turns, lambda=3, reads uncapped, low-read tie-break | 74 | 44 | 20 | 17 | 32 |
| Max seven turns, lambda=4, reads uncapped | 74 | 44 | 20 | 17 | 32 |
| Max seven turns AND max four reads, lambda=0 | 74 | 44 | 20 | 17 | 32 |
| Max seven turns AND max four reads, lambda=4 | 74 | 44 | 20 | 17 | 32 |

Every selected policy is a **fully replayed physical lawful strategy** on all twelve true starting slots, with legal named moves, chosen read/silent modes and a prefix-free read-bit response tree. The scalar lambda=3 phase transition and exact two Pareto vertices are independently reproduced, but were first established by the prior 0.21 P8 theorem. The T=71 policy uses five reads in some worlds, thus does NOT meet the max-four-read constraint.

**What P2 adds:** Chosen deterministic tie-broken optimal policy action/observation subtrees are hashed under two output contracts. If termination means only “identified,” each chosen policy's future-behavior tree has 17 distinct structural nodes, including the terminal. If termination must name the original starting source, the same concrete policy trees have 31 or 32 structurally distinct nodes. There are 19/20 belief-and-budget states along the respective chosen policies. **These are exact for the selected policies; NOT a global minimization over every equally optimal policy.** The distinction between the physically minimal all-action two-source monitor (264 states in P1) and the 17-node chosen full-root policy is NOT a like-for-like 264-to-17 compression claim because the tasks, reachable sets and output contracts differ. Accumulated path/source identity was already relevant in G3-P29.

## 3. P2-B: do not confuse policy state with the all-action possibility space

A separate direct source-level exploration enumerates **all 18 legal physical actions and both optional read/no-read choices** (deduplicating current physical hypothesis masks) for a fixed first-three-turn prefix only:

| Exact depth | Distinct reachable physical support masks |
| --- | ---: |
| 0 | 1 |
| 1 | 7 |
| 2 | 86 |
| 3 | **946** |

At depth three these 946 include different possible candidate counts, including 20 singleton masks. They are **alternative possible histories across many hypothetical controllers**, not 946 memories used by one controller or one human. The seven-turn all-action state arena was NOT exhaustively built and may not be presented as having only 946 states. Likewise, the 17 anonymous-policy-subtree count is not a general statement about how many beliefs can exist in the environment.

## 4. Exact attack C1 — the same belief support is not sufficient without the remaining resource

The physically legal original zero-flip slot pair 0 and 2 (edge coordinates 0 and 4) **cannot** be distinguished by any single legal face turn followed by the intrinsic flip-bit read; legal two-turn read experiments can distinguish them. The verifier exhaustively checks all 18 one-turn choices and all 18x18 two-turn choices. The same current belief is infeasible with one turn remaining but feasible with two turns remaining. Therefore a memory state claiming task-independent optimal control must include or otherwise know the remaining horizon/time/resource budget, unless those are recoverable from globally fixed context.

This does not refute the standard POMDP sufficient-state theorem with the task horizon included in the decision state; it refutes using the bare physical candidate support as a universally complete decision state.

## 5. Exact attack C2 — even a FULL posterior on physical state is not sufficient for an uncertain observation law

This is a **deliberately hypothetical augmented sensor model**, not an assertion about actual FMC cameras or human eyes. Use two real physical edge states s=0 and s=2, equal prior weights. The genuine F face turn splits their ideal intrinsic edge flip outputs. Now define a fixed unobserved sensor-polarity variable C and the instrument response Y = intrinsic_bit(after F) XOR C.

Two augmented task priors have **the same marginal physical posterior** P(s=0)=P(s=2)=1/2:
- In A, C is definitely zero; F+read produces distinct bits with probability 1/2 each and identifies s.
- In B, C is correlated with the physical source and equals the underlying F-output bit; F+read always returns 0 and **does not identify** s.

Thus the same complete P(s) predicts different next-observation distributions and identification power depending on the **joint latent law P(s,C)**. If observation/transition/calibration parameters are unknown, it is illegitimate to use only a marginal physical-state posterior and pretend the model is fixed. If a known generative law includes these parameters, a posterior on the **augmented** state can again be sufficient under the stated conditions. The mathematical refutation does not imply correlated calibration is present in existing human solve records.

## 6. Attack C3 — no automatic identification of human mental beliefs

Three objects must remain separate:
- **Analyst/normative posterior** calculated from a specified transition model, prior, legal actions, exact sensor and history, as in the verified exact Rubik Bellman program.
- **Naturalistic inferential account** from 451 unique historical cube solve reconstructions, G7 P24–P27, and eight real FMC retrospective author reports. Their actions and stated candidate revisits are partially attested; subjective posterior vectors, discarded invisible options and true mental effort are **not measured** by these records.
- **Psychological cognitive state** as a proposed latent construct. It may be heuristic, learned, context sensitive and costly to update. It is a hypothesis, not a 24-bit mask that humans are known to internally store.

Literature: [Kara and Yuksel, JMLR 2022](https://www.jmlr.org/beta/papers/v23/20-1152.html) analyze belief-MDP finite-memory limitations. [Bayes-Adaptive Interactive POMDPs](https://ojs.aaai.org/index.php/AAAI/article/view/8264) augment latent states with uncertain model parameters. [Littman, Sutton and Singh, Predictive Representations of State, NeurIPS 2001](https://proceedings.neurips.cc/paper/2001/file/1e4d36177d71bbb3558e43af9577d70e-Paper.pdf) provide an action-conditional future-observation prediction representation not requiring identification with an explicit physical posterior. [Finite-State Controllers, ICAPS 2009](https://ojs.aaai.org/index.php/ICAPS/article/view/13379) stress that finite control-memory can be compact and task-dependent.

## 7. Replacement research contract: parameterized information-state sufficiency

Use Xi_theta(history) and an explicit task/model theta. A candidate compressed information state should pass an experiment-relative falsification gate: for every admissible future action-and-observation protocol, histories assigned the same state must agree on the conditional law of relevant observable transcripts, plus goal/termination/cost outputs. If the application demands only one optimal policy, a **different, weaker task-relative quotient** may be valid; a single scalar optimal value still does not prove that its action outputs are compatible (P0 counterexample).

Potential inputs to Xi_theta: joint belief on physical state and uncertain observation/transition parameters; coordinate reference frame when sensor/legality depends on it; source-origin mapping when original label is required; remaining time, moves, reads and task-stage restrictions; prior/risk/cost structure. These are *possible necessary parameters, not a command to put them all in every controller*. For each proposed omission, exhibit two admissible histories with identical projected state but a different future controlled-observation law or required optimal choice. The minimality of a universal augmented Xi has NOT been proven.

## 8. Reproducibility and result boundary

**Source:** [P2 exact 12-source physical Bellman policy, optional read/silent witness and uncertain sensor-model counterexample](../../scripts/cuberev-022/verify-p2-costed-policy-belief-model-audit.mjs).

**External independent execution:** [GitHub Actions #38060261496 — SUCCESS](https://github.com/WhoSia/CUBE-REV/actions/runs/38060261496), [full 12-world-policy and model-counterexample JSON artifact #11672578343](https://github.com/WhoSia/CUBE-REV/actions/runs/38060261496/artifacts/11672578343), ZIP SHA-256 **6bbb51ed6290878d4a2d92e49075c0dc4fdbd2100bdbe52353063714cbd0209f**.

The success proves finite arithmetic assertions under the admitted physical/extended mathematical models and all 12 source replay; it is **not** a validation of human subjective belief, unknown calibration in real footage, a globally minimum full twelve-source FSC, or a complete seven-turn all-action belief-state enumeration.

**P2 scientific status:** costed chosen-policy exact replay PASS / anonymous-vs-source-labelled 17/31-32 difference PASS / all-action depth-3 mask count 946 PASS / physical budget counterexample PASS / augmented-observation law counterexample PASS / universal belief-state or psychological-minimality claim REJECTED or HOLD according to exact scope.

**P3 proposed paragraph name:** Model-Robust Predictive Sufficiency & Resource-Relative Controller Memory: Joint-State Versus Predictive-State Quotients, Nonstationary Cost Policies, Original-Source Decoding & Finite Physical Counterexamples. Video tools, VFMC sessions and new human participant recruitment remain on HOLD.
