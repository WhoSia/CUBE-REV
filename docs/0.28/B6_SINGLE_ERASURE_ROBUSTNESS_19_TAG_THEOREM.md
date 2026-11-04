# CUBE-REV 0.28 — Exact B6 one-original-cubie erasure threshold: 19

**2026-11-04, prior-chat provenance restoration and logical correction.** This supersedes the earlier same-day temporary 18–19 uncertainty. The earlier speculative method of deducing 18-tag invalidity from *absence of valid 16-tag subsets* was invalid; it is NOT used in this proof. The decisive lower-bound witnesses were already physically certified in the 2026-10-31 research phase but omitted from the previous audit. New proof stitching and direct midpoint replay make the result explicit and auditable.

## Model and result

Fixed-centre legal 3×3 Rubik group, symmetric 18-HTM word ball B6. Each selected sensor reports its particular **original oriented cubie's full position and orientation**, not graph-landmark distance and not an instantaneous orientation bit. One-erasure robust means for every tag t in S the observation on S\\{t} separates every state in B6.

**Conditional exact theorem:** Given the archived B5 complete pure-three-original-edge-support witnesses and B6 positive 16-tag physical certificates, whose source and replay levels are recorded below,

    b6^(1) = 19

and there are **exactly twelve** optimal robust sets: all eight original corners and any eleven of the twelve original edges. This number is for **one lost sensor**, not the ordinary zero-erasure b6=16, and not the r>=7 result b7^(1)=20.

## General support-hypergraph lemma

For two distinct states x,y∈B6, define the original-tag difference support D(x,y) = {t : the FULL oriented factor of t differs between x and y}. An observed tag set S is one-erasure robust if and only if

    |D(x,y) ∩ S| >= 2    for every x != y in B6.

Proof: a one-tag erasure can remove at most one member of the detected support; if at most one was present, erasing it creates indistinguishable physical states. The converse is immediate. This criterion is general combinatorial elementary prior art, NOT a new lemma in graph theory.

## Lower bound: 8 mandatory corner sensors + 11 mandatory edge sensors

**Corner source (physical midpoint replay).** The established 12-HTM pure-two-original-corner words

    U2 R' B D2 B' R U2 R' B D2 B' R
    U' B2 U L' F2 L U' B2 U L' F2 L

are imported from the 2026-10-31 physical-short-support audit, not newly discovered. A separately implemented 48-movable-sticker physical engine `verify_short_support_phase.py` replays these words. Cutting each 12-move sequence into two six-move endpoint paths produces distinct states in B6; a new `verify_b6_one_erasure_exact19.py` additionally replays the actual two endpoints and computes their original-tag difference directly, rather than assuming the solved-endpoint support matches after midpoint transport. The two geometric orbits contain 12 face-diagonal + 4 body-diagonal original corner pairs, with no edge-tag differences. Their union touches **all eight corners**. Every absent corner c lies in a two-support {c,c'}; the other corner c' is at most one observed factor, failing the >=2 criterion even if every other sensor is installed. Therefore every robust S contains **all 8 corners**.

**Edge source (historical sealed B5 physical certificate).** The earlier 0.28 B5 research and re-executed source archive `CUBE_REV_20261030_EXACT_B1_B5_SENSOR_CERTIFICATES.zip`, SHA256 `002887a198bac812ad360ba536309f2522899d5c28d12fb73bb92062ae889c94`, report 84 pure three-edge support masks in B4, plus 136 disjoint new ones in B5, yielding precisely **C(12,3)=220** triple-edge physical difference supports. Nine B5 new physical representatives and their 24 proper rotations were replayed using the old 54-facelet model; see `docs/0.28/B6_EXACT_16_TWO_CERTIFICATE_CLOSURE.md` and the 2026-10-30 history recorded in Drive `33.md`. **The present new verifier does not independently replay the 220 source witnesses**: it treats the complete triple-edge family as a clearly labelled inherited physical premise.

Suppose two edge sensors e,f are uninstalled. Pick any third edge g. A B5⊆B6 pair differs only in e,f,g; after erasing g, no observed factor distinguishes those states. Therefore one-erasure robustness requires at most **one** omitted edge, i.e. at least **11 selected edges**. Together with all eight mandatory corners:

    |S| >= 8 + 11 = 19.

This proof excludes every 18-tag layout **directly by original physical short-support witnesses**, not by the false 16-subset converse. It does not need classification of any 17-tag B6-positive sets.

## Upper bound: 12 actual 19-tag constructions, using 10 symmetry witnesses

Take all 8 original corners and all 12 original edges except any one e. For any additional single lost edge f, the two missing edges {e,f} are included in at least one of the **156 archived physically positive omitted-four-tag** B6 layouts. For any lost corner c, the two missing tags {e,c} likewise extend to one positive omitted-four-tag layout. Thus the remaining 18 installed tags in either case still contain a genuinely B6-valid sixteen-sensor sublayout; its injectivity is inherited by monotonicity.

The full geometric enumeration gives coverage **66/66** unordered original edge pairs and **96/96** corner–edge pairs. The 24 proper spatial cube rotations permit an explicit shorter certificate:

- Fix one absent original edge DL: its rotation stabilizer is order 2, splitting the eleven other edges into six partner orbits `{BL,DF}, {BR,UF}, {DB,FL}, {DR,UL}, {FR,UB}, {UR}`. A positive omitted-corner-core edge h for the respective representatives BL,BR,DB,DR,FR,UR is **UR, DB, UR, UF, DF, UL**, respectively.
- Fix one absent corner at `(-1,-1,-1)`: the order-3 rotation stabilizer has four original-edge orbits `{BL,DB,DL}, {BR,DF,UL}, {DR,FL,UB}, {FR,UF,UR}`. Every representative BL, BR, DR, FR occurs with missing core h=DL and omitted edge pair **{DF,BL}, {UR,BR}, {UL,DR}, {UR,FR}**, respectively.

`audit_b6_one_erasure_robustness.py` verifies the orbit stabilizers, all ten concrete witness memberships and the full coverage. The 156-layout B6-positive labels are **inherited** from previous exact 41-goal full-state HTM MITM certificates, NOT independently established by the orbit code.

Therefore all twelve 19-tag sets missing one edge work, while no 19-tag set missing one corner works because the physical corner-pair obstruction forces all corners.

    b6^(1)=19,   # minimum one-erasure robust layouts = 12.

QED, at the explicitly recorded physical-source evidence grade.

## Stronger completeness and the B6 → B7 robustness phase transition

The preceding necessity (all 8 corners and at least 11 edges) and sufficiency (all twelve 19-tag missing-one-edge layouts) actually characterize the **entire one-erasure-robust family** on the 20 original-tag ground set, not only its minimum:

- At **radius six**, the robust sets are exactly the twelve 19-tag layouts and the complete 20-tag layout, so **13 robust subsets total** across all 2^20 choices.
- At **radius seven and above**, only the complete 20-tag layout is robust, so **1 robust subset total**. A 13-HTM physical word changing only two original edges, split into actual 6- and 7-turn B7 midpoint states, yields a two-edge collision. Its 24 spatial rotations touch all twelve original edge tags; thus one-erasure robustness requires **all twelve edges**. All eight corners were already mandatory at B6, so all twenty tags are necessary, and sufficient because no legal nonidentity difference has support on only one original cubie.

An additional 48-sticker physical midpoint replay in `verify_b6_one_erasure_exact19.py` checks the 13-HTM adjacent-two-edge word and all 24 rotated support pairs, with the **actual midpoint states** rather than simply equating endpoint support to observed tag support by assumption. This B7 phase change is **prior 2026-10-31 original research** reconnected to the independently certified B6 upper family, not a claim of new general fault-tolerance theory.

| Radius | Minimum one-erasure robust count | All robust tag sets | Smallest robust shape |
| --- | ---: | ---: | --- |
| B6 | **19** | **13** | 8 corners + 11 of 12 edges (12 ways) |
| B7 and larger | **20** | **1** | all 8 corners + all 12 edges |

Equivalently the original-tag one-erasure feasibility predicate becomes strictly stronger from B6 to B7, deleting exactly **twelve previously valid** one-erasure layouts. There is no appeal to a hypothetical B8 full-state census: inclusion B7⊆Br and full20 robustness for all legal-cube states finish the argument.

## What is verified / what is inherited / what changed

| Scientific proposition | Evidential source |
| --- | --- |
| Two specific 12-HTM pure-two-corner words; midpoint transport; 16 rotated supports; all corners touched | **Actually replayed** by independent 48-sticker `verify_b6_one_erasure_exact19.py` + original physical `verify_short_support_phase.py`; not a claim of shortest possible words |
| Every one of the C(12,3)=220 edge triples physically occurs as B5 difference support | **Inherited and historically re-executed** old original 54-facelet B5 certificate; new proof code counts the obligated triples but does not replay them |
| Exactly 156 B6-positive 16-tag layouts | **Inherited** from historical witness census, original physical archive and separate 41-distance full-state MITM; not source-independent fresh facelet engine |
| Constructive 19-tag validity | New 10-orbit finite geometric derivation **conditional on** positive family |
| 18-tag nonexistence for one erasure | Direct short-support-hypergraph consequence of corner and edge physical witnesses; **not** 16-subset inference |
| Relation to prior work | Hernando–Mora–Slater–Wood (2008) studies fault-tolerant **graph-distance landmark** metric bases; not this original-cubie output. Boutin (2008) studies exchange properties more generally |

This restores a genuinely stronger argument from previous chat history rather than inventing the 220-triple premise at this turn. Its value is mathematical integration and executable source-linking, **not** independent physical discovery of an earlier short word or a new generic robustness principle.

## Reproducibility

- `python scripts/cuberev-observation/verify_b6_one_erasure_exact19.py`
- `python -m unittest discover -s scripts/cuberev-observation -p 'test_b6_one_erasure_exact19.py' -v`
- `python scripts/cuberev-observation/audit_b6_one_erasure_robustness.py`
- `python scripts/cuberev-observation/verify_short_support_phase.py`

Mandatory canonical branch: **research/current**, by `REPOSITORY_POLICY.md`. CI is **read only**, no bot-authored commits.

## Retraction genealogy

An intermediate 2026-11-04 draft incorrectly claimed exact 19 by a false general converse about containing a positive 16-core, and a subsequent correction withdrew to 18≤b6^(1)≤19. The **final exact proof here is different**: it imports earlier actual B5=220 triple-edge and B6=16 two-corner physical support evidence, *then* separately proves the 19-tag positive upper construction. The logical issue stays documented to prevent regression.
