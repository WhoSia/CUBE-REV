# CUBE-REV Generation VI G6-P2 — 18-HTM Schreier Geometry Court

## Authority and prospective questions

This court runs on `research/current`, based on G6-P1 `a2c0f842d6835a1beb03c46354e48a4b54780fbb`. The four hypotheses and distinctions below were fixed in the user's prospective stage request before outcome computation; this file records their executable operationalization and verdicts, not an independently time-stamped pre-registration. H1, phase-1 distance may differ statewise from full-cube HTM distance; H2, equal coarse coordinates may have different first-hit G1 entry surfaces; H3, a static phase-1 coordinate may fail to determine an executable optimal policy; H4, coordinate, heuristic, symmetry, policy, and full-state representations may satisfy different claim contracts. No 2x2 outcome was used as a 3x3 premise.

## Action and state contract

The action alphabet is the 18 standard face turns in HTM: U/R/F/D/L/B, each to powers 1, 2, and 3. States use Kociemba position-array cubie composition. Legality, inverse, half-turn, identity-round-trip, phase-target, and transition tests are executable. `G1=<U,D,R2,L2,F2,B2>` and the phase-1 coordinate is `(corner twist, edge flip, UD-slice subset)` with cardinalities `2187 × 2048 × 495 = 2,217,093,120`; G1 iff all three coordinates are zero.

## Schreier oracle and materialization boundary

The graph is defined on right cosets `G/G1` with the 18 labeled right-action generators. The executable oracle factors the transition into twist, flip, and slice transition tables. It does not construct the full graph. Exact BFS shells through radius 5 from G1 materialize 95,039 coordinate vertices; exact full-cube HTM shells through radius 5 materialize 621,649 states. On the complete full-state ball through radius 3, all 18 oracle edges per state were checked against cubie transitions. This is a bounded consistency check, not full-graph enumeration.

The phase-1 coordinate is Markov/action-congruent for the abstract coset transition contract. It is not sufficient for full-state transitions or full-cube optimal policy: solved-neighbor states U and D share q=G1, but have distinct exact optimal first-action sets `{U'}` and `{D'}`.

## Phase-1 distance, entry surface, and policy

`d1(q)` is exact distance to G1 in the 18-action Schreier graph; values used for comparisons are exact only in the radius-5 BFS shell. Two projected tables `(twist,slice)` and `(flip,slice)` are separately BFS-computed, with 1,082,565 and 1,013,760 entries. Their maximum is an admissible lower bound to G1, not exact full phase-1 distance, full-state distance, or a policy. The projections are coordinate/PDB machinery, not Korf cubie-subset PDBs.

Entry contract: for a full state x with d1(q(x))=1, the entry surface is the set of full cubie states reached by one HTM action whose q is in G1. This is an exact first-hit/minimum-phase-1-depth contract in the local shell, not a Kociemba full-solver phase-1/phase-2 optimality claim. Deterministic witness: R and U,R have the same q `(1494,0,301)` and d1=1, but their respective entry surfaces contain two endpoints each and are unequal in full cubie state. Thus q preserves abstract coset destinations but not the omitted within-coset endpoint identity.

Policy contracts are separated. Under phase-1-only search, q plus its exact abstract transitions determines abstract optimal first actions. Under full-cube HTM-to-solved optimality, q does not determine Pi: U and D are a deterministic collision. This does not assert any human policy relation.

## Transport court results

| Hypothesis / representation law | Result | Scope |
|---|---|---|
| H1 phase distortion | Statewise disagreement between exact full-cube HTM distance from solved and exact distance to G1 is tested in the intersection of radius-5 balls | This compares distinct targets; not a claim about optimal two-phase solution length |
| H2 entry surface | PASS witness: same q and exact d1, unequal full-state endpoint sets | Explicit collision above |
| H3 static vs dynamic | Split verdict: q is sufficient for abstract phase-1 graph policy; insufficient for full-cube optimal policy | Contract-dependent; no universal static/dynamic slogan |
| H4 claim-relative ecology | Supported locally: q passes membership/quotient-transition claims; projected PDB passes lower-bound claim; q/PDB fail to identify full optimal policy/entry endpoint | Not a total order; no full matrix census |
| C4 axial symmetry | U-D-axis quarter-turn generator set preserves G1; projected-bound equality checked on deterministic probe | No globally materialized symmetry quotient; no global entry or policy invariance claim |

The PDB admissibility contract follows because each projection is a move-consistent abstraction and max of admissible lower bounds remains admissible. Summing is not claimed. Exact distances within the small projection graphs do not make their combined bound exact on the full Schreier graph.

## Literature pressure and precontact boundary

Kociemba's technical two-phase description grounds the coordinate and subgroup definitions; Rokicki et al. (2013, peer-reviewed) treat cube diameter via cosets and symmetry, not evidence of this implementation's completeness; Korf (1997, peer-reviewed proceedings) grounds exact pattern-database distances; Korf & Felner (2002, peer-reviewed) motivate cost-partition conditions for additive disjoint PDBs. External implementations are cross-checks, not novelty authorities. CFOP, Kociemba, perceptual chunks, memorized algorithms, lookahead schemas, and exact coordinates remain rival algorithmic grammars. Human world contact is CLOSED; no recruitment, human-data execution, or machine-to-human identity claim.

## Carried constraints and closure ceiling

P4-R4 viewpoint/mixed-radix execution debt remains BLOCKED. G4-R2 provenance remains HOLD. The full 2,217,093,120-vertex Schreier graph, the 4.3e19 cube group, exhaustive full-cube search, Kociemba solver equivalence, human cognition, and global symmetry quotient were not enumerated or established. A bounded informative negative H1 result is not a global theorem. Scientific closure is limited to the tested, executable contracts and their falsifiers.
