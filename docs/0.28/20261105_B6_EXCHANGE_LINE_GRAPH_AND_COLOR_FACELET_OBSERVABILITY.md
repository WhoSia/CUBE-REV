# CUBE-REV 0.28 — 2026-11-05 Structural mechanism and observation-channel realism court

**Research status:** mathematical/computational progress on two distinct questions, NOT an external novelty verdict or evidence of real-human cube cognition. Preserve both: (1) a precise finite explanation of the B6 optimal-layout exchange-graph decomposition; (2) an actual constructive full-group recovery procedure with a weaker six-color measurement channel. No retreat from hard generalization, and no inference about optical noise without measurements.

## A. Why 156 optimum B6 layouts split into 25 exchange components

The complete P48 B6 physical certification (41 positive MITM distance classes plus complete negative layout census) already showed 156 size-16 sensor sets. Their complements are 4 original cubie positions: two adjacent corners (the endpoints of a cube edge h), plus two omitted edge cubies chosen from a 13-pair family P(h). Work with these complements; exchanging one sensor amounts to changing **exactly one of the four omitted cubie positions**.

The new [independent combinatorial exchange auditor](../../scripts/cuberev-observation/audit_b6_exchange_line_graph.py) constructs the 156 accepted four-tag complements from the physical 3D cube geometry and directly computes the graph whose two vertices differ by one tag. Its exact source-level statements are:

1. Each of the **12** possible core cube edges h has a local fiber of **13** certified layouts, partitioning across **global** connected components as **8 + 4 + 1**.
2. The four-element family is an induced simple cycle **C4**, with no exchange edges leaving that core. The one remaining exceptional layout is an isolated **K1**, with no exchange edges.
3. Each eight-vertex fiber belongs to a common connected **96-vertex** component. Its within-core induced subgraph contains **18** exchange edges. Across any pair of different core edges there are exactly **three** exchange edges if and only if the core edges share a **cube corner**; otherwise zero.
4. The quotient over the twelve core edges is exactly the **line graph L(Q3)** of the cube graph Q3: twelve vertices and twenty-four degree-four adjacency edges, with three exchange edges between fibers for each quotient adjacency.
5. Therefore the large component contains 12*18 = **216** within-core edges and 24*3 = **72** cross-core edges, while twelve disjoint C4 components contribute **48** edges. Total:
   
   `|V| = 96 + 12*4 + 12 = 156,`
   
   `|E| = 216 + 72 + 48 = 336,`
   
   `components = 1 + 12 + 12 = 25.`
   
   Degree counts inside the large component are 24 vertices of degree 4, 24 of degree 6 and 48 of degree 7.

This is a **geometric/local-to-global explanation** of the measured count rather than merely quoting components 96,4,1. It depends on the exact certified 13-pair local B6 criterion; the small script does NOT redo full 41-distance MITM. Its finite case classifications and line-graph quotient are verified by code. No claim that generic group-action base exchange decomposes universally into L(Q3) fibers, or that line graphs and exchange decompositions themselves are new concepts.

## B. Sensor fidelity separates ideal piece recognition from actual one-facelet color readings

The earlier *ideal* stationary edge-site/corner-site probes report the **complete original identity and orientation** of the incoming cubie. Under that channel the full unrestricted fixed-centre legal Rubik group can be reconstructed in exactly 11 observation frames.

A weaker channel has one stationary **edge facelet** and one stationary **corner facelet** color probe. Every frame returns only one of six *categorical* colors at each probe. It does not directly report which physical cubie is in either slot. There are at most `6 * 6 = 36` possible joint frame symbols.

For a deterministic adaptive policy whose chosen legal move word depends only on preceding observed categorical colors and known actions (no additional state-dependent channels), at most `36^n` observation histories are possible in n frames. The full group cardinality is `|G| = 8! * 3^7 * 12! * 2^10 = 43,252,003,274,489,856,000`. Since `36^12 < |G| <= 36^13`, the clean full-group information bound is **n >= 13**, even for adaptive feedback.

For a **fixed nonadaptive** schedule only, standard q-ary coding bounds strengthen it to at least **14** frames if one known-position joint-frame reading is erased and at least **15** frames if one arbitrary joint-frame symbol is replaced by another adversarially. The latter follows `|G| * (1 + 35n) <= 36^n`. This codeword argument is **not** automatically valid for arbitrary adaptive policies, where corrupted readings change future actions.

The smaller B4 physical ball has `|B4| = 46,741`, just **85 greater** than `36^3=46,656`; hence its clean color-only information lower bound is **4 frames**. This is a lower bound only; no B4 color-optimal policy has been certified.

## C. New constructive full-group two-color-probe upper bound: 24 frames

The [P48 two-color physical reconstruction implementation](../../scripts/cuberev-observation/construct_color_p48_24_frame_scanner.py) builds a joint BFS on two actual spatial *sticker slots*: 24 possible edge sticker positions x 24 possible corner sticker positions. Every one of the **576 pairs** is reachable by legal 18-HTM face turns from the reference pair. Therefore select 24 known frame words that each bring one distinct initial edge facelet and one distinct initial corner facelet to the two stationary color readout sites.

After each known rotation, use its inverse position action to associate the two observed colors with the corresponding initial spatial sticker slots. In 24 frames every one of the **48** moving spatial sticker slots has been read. Each original edge cubie has a unique unordered pair of original face colors, each original corner cubie a unique unordered triple, and individual oriented original sticker indices follow from the observed assignment of colors to physical slots. This determines the **complete original-to-slot 48-sticker permutation for EVERY legal group state**, not merely the B2 regression inputs.

The executable confirms the precise 48-sticker frame map, 576 joint orbit, 24 complete observations, a **maximum five HTM turns** in an absolute reference-frame word, and a concrete no-reset relative-turn program of **169 HTM** for this first nonoptimized scan order. Exhaustive B2 262-state regression and independent sample controls passed. These finite regressions supplement, but do not replace, the general constructive argument from the 576-pair joint orbit and uniqueness of colored cubies.

Combining the information lower and the algorithmic upper:

```
13 <= h_color(G, two stationary single-facelet 6-color probes) <= 24.
```

This upper is not optimal, and **169 HTM** is a feasible move count, NOT a minimum. Neither figure assumes live RGB calibration, color classification error or occlusion. One color *per probe per frame* is a sharply different model from complete cubie-identity/orientation observation, where the earlier exact horizon is 11.

## D. Hostile novelty and future gates

- The line graph L(Q3) and the elementary branching/coding lower bounds are classical mathematics. The contribution is a specific verified cube-relative geometric mechanism and a physically constructive weaker-channel bridge, **not** new generic information theory.
- Two physical RGB sensors and cube rotations already appeared in the MIT 6.111 2017 robot. Do not misrepresent two-color sensing as a new device.
- **Immediate hard gates:** optimize the 24-frame color interrogation program's *actual HTM movement cost* with no reset; prove or disprove a sub-24-frame full-color reconstruction policy using inference between color readings rather than reading all 48 facelets; determine B4/B6 color-only radii and adaptive distinctions; then model measurable confusion/lighting errors and produce independent prospective observations.
- **Structural gate:** express B4's 84 three-edge + 12 four-edge obstruction geometry and B6's 8+4+1 fiber geometry in one falsifiable support-hypergraph criterion, and identify the smallest altered action grammar/radius where that criterion predicts a wrong answer.

## Verification/custody

- [Read-only GitHub Actions 41936996176](https://github.com/WhoSia/CUBE-REV/actions/runs/41936996176) — finite B6 geometric exchange and six-color information bounds PASS.
- [Read-only GitHub Actions 41937372938](https://github.com/WhoSia/CUBE-REV/actions/runs/41937372938) — both above plus full 24-frame P48 constructive color recovery and tests PASS. Actual job log includes `B6_EXCHANGE_CUBE_LINE_GRAPH_QUOTIENT_PASS`, `COLOR_P48_24_FRAME_FULL_STICKER_SCANNER_PASS`, `COLOR_P48_B2_ALL_262_STATES_REPLAY_PASS`, `COLOR_P48_NO_RESET_ACTION_UPPER_HTM 169`.
- Proof scope: 0.28 remains **NOT SUBMISSION-READY**, and this is neither human cognition evidence nor optical experiment data. Raw CI artifacts must be preserved to Drive if required for durable byte custody; no claim of Drive migration is made here.
- GitHub branch `research/current`; WhoSia author/committer only; GitHub Actions contents:read; Notion is the semantic decision record and GitHub is the source/replay record.
