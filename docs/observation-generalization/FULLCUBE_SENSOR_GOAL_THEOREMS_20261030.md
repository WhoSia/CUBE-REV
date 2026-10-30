# CUBE-REV — Exact Full-Cube Sensor Placement & Goal Reachability (2026-10-30)

## Mathematical scope

State space: complete fixed-center physical 54-facelet 3×3 cube. Actions: legal 18 HTM turns, each a bijection. Public initial belief B: an arbitrary finite set of full cube states. Hidden state: one unknown member of B. Readings: noiseless orientation bits of specified ORIGINAL tagged edge cubies after each move. Goal: the entire physical cube solved, not just the sensed edge identified.

For each tagged edge e define pi_e(s) to be its physical position (12 choices) and orientation (2 choices). For E a set of tags, pi_E is the product factor. This is an exact closed transition factor: pi_E(T_a(s))=tau_a(pi_E(s)). Observations are only the orientation bits of pi_E, not the factor positions.

## Lemma — all 24 tagged-edge factor states are observable with at most two actions

Each of the twelve edge choices has 24 physically realized factor states and 276 distinct state pairs. Independent 54-sticker-derived exact action transition enumeration shows 240 pairs can be separated by observing after one legal turn; the remaining 36 by observations after at most two turns. These experiments do not require an initial free reading. Python proof checker: scripts/cuberev-observation/fullcube_sensor_goal_theorem.py.

## Theorem A — exact reachability criterion for full cube goal

For any finite public belief B of whole-cube states, a guaranteed finite contingent policy for fully solving the cube exists **if and only if** pi_E restricted to B is injective.

Necessity: If distinct whole-cube states have identical physical tagged-factor vector, the closed factor and deterministic actions give identical observed histories under every feedback policy. The policy chooses identical actions for both worlds. Bijective moves cannot map two different complete cube states to the identical solved goal.

Sufficiency: Given two distinct candidates in the belief, injectivity ensures they differ in some tagged-edge factor. The separation lemma supplies a one- or two-turn experiment with different binary transcripts for them. After any observation branch, at least one candidate is eliminated. Repeating at most |B|-1 times identifies the actual full cube. A complete 18HTM solver finishes. Using the proved full Rubik's Cube 18HTM diameter 20, the constructive bound is:

V(B) <= 2(|B|-1)+20 turns.

This is a loose existence bound, not a result about efficient humans or globally minimum contingent costs.

Original diameter evidence: Rokicki, Kociemba, Davidson, Dethridge (2013), SIAM J. Discrete Math. 27(2), 1082–1105, DOI 10.1137/120867366. User shelf: https://drive.google.com/file/d/1cPtmb_5Npbnd8bghe4JNh734otHybnOV/view

## Theorem B — exact minimum tagged-edge sensor count for the entire single-turn shell

Let B1 contain the 18 distinct complete physical cubes obtained by turning one face once from solved. For a chosen edge-tag set E, define c(E) as the number of the SIX cube face names incident to at least one selected edge. The three HTM powers of each uncovered face do not move any tagged cubie; these 3(6-c(E)) physically distinct whole-cube states have identical tagged-factor vectors. Every turned state about a covered face has a unique factor vector, also verified across all selected original cubies and all legal powers.

Therefore the exact number of permanently indistinguishable B1 pairs is:

N_bad(E) = binom(3(6-c(E)),2).

This is verified by enumerating every selection of one, two, or three from the twelve physically possible edge tags:
- 1 tag: 12 designs, all with 66 impossible source pairs.
- 2 tags: 30 designs with 15 impossible pairs, 36 with 36 impossible pairs.
- 3 tags: 8 designs with ZERO impossible pairs, 96 with 3, 108 with 15, 8 with 36.

Two tags cover at most four faces, leaving at least two untracked faces and 15 ambiguous pairs, hence two are insufficient. Three tags suffice exactly if their incident faces partition all six face names into three adjacent pairs: a perfect matching of the six-face adjacency graph (octahedral graph), with eight designs. Example: UR, DF and BL. Theorem A then gives a guaranteed full-cube solving policy for all states of B1.

**Exact minimum sensors = 3** in this fixed physical/sensing design problem. This is an internally derived cube-specific theorem, NOT a verified global novelty claim over existing automata or sensor-placement results.

## Goal changes the answer

Two distinct full cubes F(solved) and D(solved) are forever indistinguishable through the original UR tag alone; jointly fully solving them is impossible. But both states already satisfy the relaxed goal 'the original UR edge cubie is in its solved position and orientation', so zero turns achieve that goal. The full-singleton goal criterion above cannot be transferred to arbitrary partial/saturated goals.

## Projected 0.24–0.27-style lower bounds

Physically induced complete projected edge PDBs for UR; UR+DF; and UR+DF+BL contain exactly 24, 528, and 10,560 states, with HTM pattern diameters 3, 5, and 7. An exact pattern-to-goal distance h_E(s) is always admissible for the full cube: h_E(s) <= d_full(s,solved). Stored PDBs were validated via legal successor/predecessor and 1-Lipschitz checks.

Fair same-input AND-OR benchmark: 18 HTM actions, same UR+DF+BL noisy-free readings, same full cube goal and three-turn horizon; only the lower-bound strategy varies. For the hidden full cube pair {U,U'}, the plain AND-OR method evaluated 4896 action choices; using the projected PDB evaluated 69; using radius-four exact whole-cube distance frontier evaluated 42. All proved the identical minimum worst-case cost 3. This is an INTERNAL baseline comparison and not a run of a third-party FOND or POMDP implementation. The large historical 0.27 deep-geodesic backend was NOT executed or imported.

## Literature and originality controls

- Kaelbling, Littman, Cassandra (1998), Planning and Acting in Partially Observable Stochastic Domains: https://drive.google.com/file/d/13lNQIQF4duF31tGa9VGldEMWXxrtz6Sh/view
- Veiga and Renoux (2023), From Reactive to Active Sensing: https://drive.google.com/file/d/1TkVb3xW240KmhjqAKwzvQoQBUNnI_6GP/view
- Gao et al. (2026), CubeBench: Diagnosing Interactive, Long-Horizon Spatial Reasoning under Partial Observations (ICLR 2026): https://drive.google.com/file/d/1f0JglIVVE1Dl3zopdiUEUSA8t6sAy0lj/view

Their work already spans belief-state contingent planning and partial-view cube interaction, so neither "active sensing" nor "using a Rubik's cube" constitutes novel territory. What is established here is a narrowly scoped exact physical theorem with a complete finite census and constructive policy bound. Publication-grade novelty relative to sensor-selection theory and competitive solver speed is still unproved. The known one-erasure L7 dictionary problem k=4 also remains unresolved (3 <= M* <= 5).

Evidence code: scripts/cuberev-observation/fullcube_sensor_goal_theorem.py; fullcube_goal_pattern_databases.py; fullcube_multisensor_goal_cases.py; fullcube_andor_baseline_comparison.py; physical receipts attached to GitHub's read-only workflow.
