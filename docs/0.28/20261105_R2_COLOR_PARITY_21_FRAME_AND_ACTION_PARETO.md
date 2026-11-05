# CUBE-REV 0.28 — 2026-11-05 R2: From an ideal cubie oracle to legal six-color facelet reconstruction

**Current bounded theorem:** With one fixed edge-facelet probe and one fixed corner-facelet probe, each reporting exactly ONE categorical face color (one of six) after known controllable legal 18-HTM turns, the full fixed-centre legal 3x3 Rubik group can be recovered using **21 predetermined observation frames**. An information-theoretic lower bound is **13** frames even with adaptive observations. Thus `13 <= h_color(full G) <= 21`. Neither the 21-frame optimum nor minimal HTM route cost has been proved.

## Falsifiable channel contract

- Physical cube state is the original-to-spatial-slot 48-moving-sticker permutation in the independent 3D P48 engine.
- Each observation returns **only a face color at two specific stationary spatial sticker slots**, one edge and one corner (6×6 categorical outcomes), **not** complete incoming original cubie identity, full orientation, multiple simultaneous colors, or a scanned photograph.
- All turns and the sequence of queried initial spatial facelet slots are known. Sensor output has no noise, misclassification, unknown color mapping or occlusion. "Realistic" here means **weaker and color-categorical**, not experimentally calibrated hardware.
- The 24 edge-facelet and 24 corner-facelet spatial slots have all `24×24=576` jointly reachable pairs under real legal face turns. Any selected pair may be sent to the two fixed probes by a known relative turn word, without resetting the physical cube.

## Stepwise physically constructed upper bounds and explicit use of legal invariants

**24 frames:** Read every one of 24 edge stickers and 24 corner stickers. The unordered original edge two-color pairs and original corner three-color triples uniquely identify piece labels, with orientation from sticker-color placement. [Physical scanner](../../scripts/cuberev-observation/construct_color_p48_24_frame_scanner.py).

**22 frames:** Read all facelets of eleven edge spatial positions (22 facelets), all facelets of seven corner positions (21 facelets), and one facelet of the last corner (one). The only unobserved original edge label and destination are determined by bijection; its flip is forced by the **even global edge-flip sum**. The last corner label is the remaining label, and its one observed face color chooses exactly one of its three cyclic orientations. [22-frame code](../../scripts/cuberev-observation/construct_color_p48_22_frame_parity_scan.py).

**21 frames:** Read 10 full spatial edges (20 colors) and one facelet of the eleventh edge (one); read all three facelets of seven corners (21 colors). The remaining corner label is known and its cyclic orientation is forced by the **corner-twist sum = 0 modulo 3**. Two original edge labels remain for the two partially/unobserved edge positions. Exactly one assignment matches the already inferred **corner permutation parity**, since legal edge and corner permutation signs agree. The one measured facelet on the partially read edge selects its unique orientation, and the last unread edge's flip is forced by **edge-flip sum = 0 modulo 2**. Every inference is made only from observed categorical colors, the known action frames and the universal legality constraints; the actual input state is used solely to simulate observations and independently assert correctness in tests. [21-frame physical source](../../scripts/cuberev-observation/construct_color_p48_21_frame_legality_scan.py).

These are proofs over **all legal states** by the reachability and cube-legality argument, not an infeasible enumeration of all 43 quintillion group elements. Full physical P48 B2 (262 states), legal face turns, nontrivial 12–13-turn words and mutation/assertion controls were used as executable regressions. On the published 21-frame source, no direct full-ID-orientation sensor, discarded orientation bit or access to a hidden perfect state oracle is part of the reconstruction algorithm.

## Lower bound and nonidentity with prior ideal channel

The group cardinality is `8! * 3^7 * 12! * 2^10 = 43,252,003,274,489,856,000`. Any adaptive protocol with only two categorical one-facelet readings per frame has at most `36^n` observable histories, and `36^12 < |G| <= 36^13`. Therefore **13 frames are necessary** without further state-dependent channels. The earlier **11-frame** full-group ideal probe theorem uses *full cubie identity+orientation* and does not transfer to the color-only channel. The 13 lower bound is not shown tight; the present 21 upper is not shown minimal. A one-erasure bound of 14 or one adversarially corrupted joint frame bound of 15 is presently proved by coding arguments **only for fixed nonadaptive measurement schedules**, not arbitrary adaptive feedback.

## Observation/action tradeoff: same physical channel and same exact replay criterion

A deterministic nearest-neighbor plus two-opt tour reorders the specific certified readout frames, using exact P48 replay of every no-reset relative legal turn sequence and exact same-face 18-HTM cancellations. On the same three constructive frame families:

| Fixed frame family | Readout frames | Baseline route with same-face reductions | Improved executable route |
|---|---:|---:|---:|
| All 48 facelet colors | 24 | 164 HTM | **136 HTM** |
| Legal edge flip inferred | 22 | 150 HTM | **123 HTM** |
| Edge flip + corner twist + matched permutation parity | 21 | 142 HTM | **119 HTM** |

[Executable joint Pareto audit](../../scripts/cuberev-observation/audit_color_p48_frame_action_pareto.py) checks all 262 physical B2 states for each reordered schedule; the constructive full-group correctness follows from the mathematical bijective observations, not the finite test count. [Read-only remote CI 41938711695](https://github.com/WhoSia/CUBE-REV/actions/runs/41938711695) SUCCESS and actual job logs carry `COLOR_P48_PARETO_24_FRAMES_EXACT_PHYSICAL_REPLAY_PASS ... 136`, `COLOR_P48_PARETO_22_FRAMES_EXACT_PHYSICAL_REPLAY_PASS ... 123`, and `COLOR_P48_PARETO_21_FRAMES_EXACT_PHYSICAL_REPLAY_PASS ... 119`.

**Do not use the table as a proof of a monotonic general law.** These three schedules are carefully chosen upper-bound examples. The 2-opt order search does NOT optimize over all allowed readout frame realizations, alternative color observation sites, all policies or error conditions.

## Relationship to the older B6 exchange structure and actual research question

The [2026-11-05 B6 exchange court](20261105_B6_EXCHANGE_LINE_GRAPH_AND_COLOR_FACELET_OBSERVABILITY.md) structurally resolves the 156-base single-sensor exchange graph into a 96-vertex component fibered over the cube line graph, twelve C4 cycles and twelve isolated vertices. This is an **exact local geometric explanation**, not an arbitrary-group theorem. The 21-frame color scan provides the complementary *observation-channel* direction: algebraic legality reduces the number of necessary readouts when local color fidelity is weakened. Both are driven by legal physical state restrictions, but **no unified theorem equating exchange connectivity and color measurement redundancy has yet been proved**.

Hard open problems remain deliberately large: prove or refute the global minimal color observation horizon between 13 and 21; formulate an exact adaptive policy with bounded HTM action cost rather than a fixed query schedule; study a nonideal color-confusion channel and its robust cost; explain B4/B6 support geometry across radius and action grammar with falsifiable counterexamples; and only then test prospective human reconstruction mechanisms with actual independent participant measurements.

**Prior art / publication boundary:** Cube-scanning RGB hardware and adaptive distinguishing-sequence information-cost optimization predate this work. The contribution claimed here is the source-audited particular Rubik P48 mathematical and algorithmic construction. This is NOT a validated optical sensor, cognitive mechanism, journal priority verdict, or submission-ready paper.

**Doctrine:** Notion carries concise semantic verdict; GitHub stores exact small programs/receipts with WhoSia author+committer; Drive receives irreplaceable raw bytes when necessary; CI remains read-only and has no bot commit path.
