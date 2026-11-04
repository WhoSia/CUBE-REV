# CUBE-REV — Physical Rubik's Cube: Reconstruction, Observation & Certified Search

**Active scientific stage:** 0.28 — *Radius-Restricted Cubie Bases, Short-Support Geometry & Robust Active Observation*  
**State reviewed:** 2026-11-04 · **Source of scientific meaning:** [Notion 0.28](https://app.notion.com/p/409ef561cf928193b3d1dc1165ad92ea)  
**Single active research branch carrying 0.28:** `research/current` · **Long-term branch policy:** [REPOSITORY_POLICY.md](REPOSITORY_POLICY.md)

> **Evidence warning:** A finite program's successful return, an independently checked certificate, a mathematical proof and a new general theorem are four different claims. Keep them separate. Do not infer human cognition from exact cube combinatorics, nor infer an HTM shortest path from a stabilizer's abstract group order.

## Scientific question and physical model

In the **fixed-center legal 3×3 Rubik's cube group**, what can a constrained observer recover about a cube state from the positions **and orientations** of a selected set of its **20 original tagged cubies**, given a maximum of `r` outer-face **half-turn metric (HTM)** moves from solved? How do the spatial geometry, failure of permanently selected sensors, available actions, finite memory and observation costs alter identifiability?

Let `G` be the legal cube group with its 18 face-turn HTM generators, `B_r` the solved word ball, `S` a set of original tagged cubie factors, and `H_S` their full-position-and-orientation pointwise stabilizer. Define `b_r` as the fewest tags needed to distinguish every state in `B_r`.

**Elementary group-action equivalence, for consistent original-tag conventions:**

```text
projection(B_r, S) injective  <=>  H_S ∩ B_(2r) = {identity}
```

This is **not** the global classical group-base problem, and **not** an orientation-only sticker experiment, an adaptive finite-state-machine test or the old 0.18 experiment-dictionary `M*` problem.

## Reproduced / inherited finite results and status

| Radius | Reported `b_r` for full original-cubie tags | Evidence boundary |
|:--:|:--:|---|
| 1 | 2 | historical 0.28 physical finite census |
| 2 | 4 | historical 0.28 physical finite census |
| 3 | 8 | historical 0.28 physical finite census |
| 4 | 14 | historical 0.28 physical finite census / 2,856 optimal layouts |
| 5 | 16 | archive-based negative and positive finite certificates |
| **6** | **16** | **Fully independent P48 physical 15-sensor lower bound plus exact 4,845-design classification: 4,689 physical negatives, 156 positive via 41/41 radius-six MITM (2026-11-04)** |
| 7 | 18 | historical 0.28 positive/negative archive; scope and independent replay remain separate |

For `r=6`: the physical six-ball has **8,240,087 distinct full states**; **156** geometrically identified 16-tag positive layouts fall into **8 proper 24-rotation orbits** (6 full 48-spatial-symmetry orbits). With 2 missing corner tags and 2 missing edge tags, the full legal stabilizer has 12 states. The historical physical goal generator produces **88** nonidentity target entries across eight orbit representatives, **74** distinct states, and **41** word-distance classes after 48 spatial symmetries and inversion. A separate exact two-sided radius-six algorithm reports **41/41 zero intersections**, each proving 18-HTM distance **≥13** for its canonical target relative to the original 54-facelet move semantics. This 2026-11-03 algorithm independently checked the positive B6 classification **relative to its inherited 54-facelet model**. On 2026-11-04, a second model built from 48 labelled moving stickers generated independent goal states and action tables; its own 41/41 exact MITM also PASSED [hosted GitHub Actions 41763106125](https://github.com/WhoSia/CUBE-REV/actions/runs/41763106125). **Current upgrade:** an independent P48 physical short-support certificate now covers all 4,689 B6-negative size-16 designs. Its 872 supports are 220 B5 three-edge triples, 16 B6 nonadjacent two-corner pairs, 216 freshly P48-MITM-discovered B5 adjacent four-tag witnesses and 420 P48-physically-replayed B6 adjacent four-tag supports. The 41 positive classes were rerun alongside the full 4,845-layout test in [Actions 41767450421](https://github.com/WhoSia/CUBE-REV/actions/runs/41767450421). The B6 >=16 lower bound is now independently implied by just the first 236 supports; a further [Actions 41767769694](https://github.com/WhoSia/CUBE-REV/actions/runs/41767769694) verified all 15,504 size-15 exclusions and the 872-member certificate's inclusion-wise irredundancy.

- [Exact `b_6=16` and proof dependency ledger](docs/0.28/B6_EXACT_16_TWO_CERTIFICATE_CLOSURE.md)
- [All 41 MITM distance-certificate receipts](docs/0.28/evidence/B6_MITM_41_20261103.md)
- [Radius doubling, original-tag composition order and 12-element stabilizer](docs/0.28/B6_RADIUS_DOUBLING_STABILIZER.md)
- [Geometry: 66 omitted-edge pairs, 18 B5 failures + 35 new B6 failures + 13 successes](docs/0.28/B6_66_PARTITION_EVIDENCE_AUDIT.md)
- [Full research-value and novelty audit](docs/0.28/B6_20261103_RESEARCH_VALUE_AUDIT.md)

**Further historical 0.28 evidence:** for two permanent original-cubie-tag erasures, the first 2-support collision occurs at radius 6; for one permanent erasure, all 20 tags are required from radius 7 onward, subject to the explicitly recorded physical witness and model assumptions in [the support phase diagram](docs/observation-generalization/CUBEREV028_SHORT_SUPPORT_PHASE_DIAGRAM_20261031.md). This concerns permanently erased *tag factors*, **not** temporally missing orientation bits or stochastic noise.

## Recent mathematics — what is proved and what remains inherited

The new 2026-11-03 algebraic work is **a consequence of standard cube legality, not new abstract group theory**:

- **Exact legal-stabilizer and support spectrum:** for `c` omitted corners and `e` omitted edges, `|H(c,e)| = ((c!e! + δ(c)δ(e))/2) · 3^max(c−1,0) · 2^max(e−1,0)`, with `δ(n)=1` for `n≤1` and `0` otherwise. Two-dimensional binomial inversion gives the number of states with *exactly* the specified support. [Proof](docs/0.28/CUBIE_STABILIZER_SUPPORT_SPECTRUM_THEOREM.md).
- **Structure and overlap:** a 2-corner/2-edge stabilizer is `S3 × C2`. Stabilizers with the same missing corner pair and different missing edge pairs intersect in a common pure-corner `C3`. Their union count `3+9m` proves **88 nonidentity entries → 74 distinct targets** for `m=8`, without trusting identical 54-facelet hashes. The **74→41** quotient still depends on separate signed-spatial-symmetry and inversion checks. [Proof](docs/0.28/B6_STABILIZER_GROUP_AND_74_GOAL_OVERLAP.md).
- **Nonmatroidal minimum-sensor family:** the previously certified physical B6-positive 16-tag layouts fail the matroid basis-exchange axiom. A concrete missing-edge counterexample uses `{FR,UR}`, `{DR,UL}` with the same missing adjacent corners at `DL`; exchanging the observed `DR` produces only two B6-negative configurations. **2,112** ordered exchange failures follow from the 12-core geometric classification. The underlying 156-design classification is now independently P48 physically certified; the exchange counterexample is a case-specific deduction, not an abstractly new matroid theorem. [Counterexample, exact assumptions](docs/0.28/B6_MINIMUM_SENSOR_EXCHANGE_COUNTEREXAMPLE.md).
- **Complete optimal-design exchange graph (post-README update):** allowing one original-cubie tag to be replaced, **including corner tags**, gives a graph on all 156 historically B6-positive size-16 sensor sets with **336 edges and 25 connected components**: one component of size **96**, twelve of size **4**, and twelve isolated designs. The 336 links comprise 264 within-fixed-corner links and 72 cross-corner links; a **24 adjacent-core-pair × 3 shared omission-pairs** argument proves why the 12 local eight-design wheel components form the 96-component (see [structural theorem](docs/0.28/B6_FULL_SWAP_GRAPH_24_BY_3_THEOREM.md)). Read the [global exchange-graph auditor](scripts/cuberev-observation/audit_b6_full_sensor_swap_graph.py) and [structural note](docs/0.28/B6_OPTIMAL_SENSOR_EXCHANGE_GRAPH_COMPONENTS.md). The graph is exactly checked against the B6 geometric classification, now independently P48 physically certified across all 4,845 size-16 designs.


**Exact one-original-cubie-erasure robustness at B6 (2026-11-04):** under the archived B5 all-220 pure-three-edge supports, independently replayed B6 12-HTM pure-two-corner midpoint supports, and previously certified B6 156 positive size-16 layouts, the minimum one-erasure-robust sensor count is **b6^(1)=19**, with **exactly twelve minimum layouts**: all eight original corners and any eleven edges. The lower bound comes directly from B5/B6 physical collision supports; the positive 19-tag upper bound has a ten-orbit geometric witness certificate. This restores an older physical fact overlooked by an interim 18–19 bound; it does NOT use the false assumption that every valid larger set contains a valid 16-tag sublayout. [Proof, source genealogy and retraction](docs/0.28/B6_SINGLE_ERASURE_ROBUSTNESS_19_TAG_THEOREM.md) · [Physical midpoint and combinatorial verifier](scripts/cuberev-observation/verify_b6_one_erasure_exact19.py).

The new P48 implementation **does** independently establish the 41 positive HTM geodesic **lower bounds ≥13** by finite exhaustive computation, but does not prove each exact distance equals 13. The new physical P48 proof also certifies all 4,689 B6-negative size-16 layouts and the no-15 lower bound, but it does not establish a new general hardness result, a generic matroid theorem, a human planning mechanism or the exact value of each >=13 goal distance.


**2026-11-04 independent P48 B6 and structural redundancy update.** The 41 positive B6 HTM classes have now passed a completely separate geometry-generated 48-moving-sticker physical transition model and exact radius-six MITM, both locally and in [read-only Actions run 41763106125](https://github.com/WhoSia/CUBE-REV/actions/runs/41763106125). See the [source-independent physical certificate and 26-backup-core structural theorem](docs/0.28/P48_B6_41_INDEPENDENT_CLOSURE_AND_BACKUP_CORE_SPECTRUM_20261104.md), [physical generator](scripts/cuberev-observation/b6_independent_48sticker_goals.py), [MITM](scripts/cuberev-observation/verify_b6_41_mitm_p48.cpp) and [CI definition](.github/workflows/cuberev-028-independent-p48-mitm.yml). Each optimal 19-tag robust layout contains exactly **26** positive sixteen-tag backups; after deleting a selected edge the backup count is **1/2/3/4** (multiplicities **4/1/4/2**), versus **4/6/10** after deleting a selected corner (multiplicities **2/4/2**), conditional on the 156-layout positive classification. Every one of the twelve robust 19-tag layouts has 78 backup-core/failure incidences. This is a concrete finite-case geometry refinement, not a general new fault-tolerance result.

**2026-11-04 new full physical B6 certification.** [All 4,845 B6 sixteen-sensor placements](scripts/cuberev-observation/verify_b6_complete_4845_p48.py) are classified with 872 physical supports; 4,689 have concrete indistinguishable radius-six endpoint witnesses and the remaining 156 are injective by the independent P48 41-class distance search. The 872-member support family is inclusion-wise irredundant (not globally cardinality-minimal among all possible support systems). A new [B5 radius-five P48 MITM](scripts/cuberev-observation/discover_b5_adjacent_p48_mitm.cpp) independently found nine actual five-turn/five-turn pairs accounting for the B5-adjacent 216-support piece; [full hosted CI](https://github.com/WhoSia/CUBE-REV/actions/runs/41767769694) verifies the complete chain including 15,504 size-fifteen obstructions and all 41 positive classes. The preserved historical 54-facelet scripts and receipts remain audit evidence, not hidden dependencies of the new P48 proof. **The Grand Doctrine remains broader than the paper:** representation-dependent observation, action costs, bounded memory, adaptive control and the onset geometry of short supports remain ambitious open research axes.

## Reproduction and source integrity

The 0.28 small algebraic/sensor regressions are ordinary Python `unittest` tests. The *historical* 54-facelet 41-target MITM requires the separately sealed original archive and C++17. The newly source-independent **P48 41-target MITM needs only the committed Python 48-sticker generator and C++17**; it generates its own 20-factor table, 41 full-state goals and run outputs without the archive.

```bash
# Small, locally runnable algebra / sensor checks (may require existing project dependencies)
python -m unittest discover -s scripts/cuberev-observation -p 'test_*.py' -v

# Standalone new algebra / geometry without the historical physical archive
python scripts/cuberev-observation/verify_stabilizer_support_spectrum.py
python scripts/cuberev-observation/verify_b6_stabilizer_group_structure.py
python scripts/cuberev-observation/verify_b6_goal_union_count.py
python scripts/cuberev-observation/verify_b6_basis_exchange_failure.py

# Physical exhaustive proof requires separately obtained archive:
bash scripts/cuberev-observation/run_b6_41_mitm.sh \
  /absolute/path/CUBE_REV_20261030_EXACT_B1_B5_SENSOR_CERTIFICATES.zip \
  /tmp/cuberev41
```

Required archival source ZIP SHA-256: `002887a198bac812ad360ba536309f2522899d5c28d12fb73bb92062ae889c94`. Canonical 41-goal 54-facelet set SHA-256: `c3dbf41177e16d8d0cb0cd76b433304e14f9cdac4a14f205d6231dc9dd8abc1e`. These are **custody/identity checks**, not shortcuts to a semantic reachability proof.

[Observation code guide](scripts/cuberev-observation/README.md) · [Existing read-only CI workflow](.github/workflows/cuberev-observation-generalization.yml) · [0.28 theorem and evidence files](docs/0.28)

**Confirmed new independent hosted CI:** [P48 41/41 exact B6 MITM run 41763106125](https://github.com/WhoSia/CUBE-REV/actions/runs/41763106125), all five batches SUCCESS and evidence artifact [13290449539](https://github.com/WhoSia/CUBE-REV/actions/runs/41763106125/artifacts/13290449539). The prior 63-test [observation run 41604820224](https://github.com/WhoSia/CUBE-REV/actions/runs/41604820224) is a separate historical smoke run, not the independent MITM court.

## Active research questions

1. **Physical source independence — complete finite B6 size-16 classification PASS:** independent 48-sticker P48 goals and actions, 41 B12 positive exclusions, fresh B5 nine-pair witness discovery, B6 negative 420 and 220+16 short supports, exact 4,845-layout partition and no-15 bound have remote read-only CI success. Remaining: external third-party proof checker, independent semantic fuzzing, durable raw-byte custody and broader radius/observation/action-cost theorems.
2. **Explanation rather than recensus:** derive shorter word-metric lower bounds for the four positive cube-incidence types (N–N, F–F, F–h*, P–P), with fail-closed proof obligations on every excluded canonical turn-word branch.
3. **Combinatorial structure:** determine the precise failure of the matroid exchange property, and whether any weaker independently established independence system supports exact algorithms.
4. **Active/reversible observation:** separate static original-tag identifying sets, preset distinguishing words, adaptive distinguishing trees, homing sequences, unknown-machine conformance, temporary erasure and human observational behavior. [Existing boundary note](docs/0.28/REVERSIBLE_OBSERVATION_THEORY_GATE.md).
5. **Research novelty/paper gate:** distinguish prior group bases, graph fixing sets, resolving sets, finite automata theory and test-collection hardness from the *physical-HTM restricted-radius* result. A paper requires independently replayable physical semantics and careful bibliography, not only a list of exact counts.

## Historical work, archives and governance

- **0.27 separate search program:** proof-carrying original 18-HTM optimal-solution lower-bound work lives in [docs/0.27](docs/0.27). Its P20 source-prefix coverage is **not** a complete independently certified global no-17 theorem. An external solver-backed 18-move result must never be promoted to an independently verified global certificate.
- **0.28 manuscript stage:** [Working Draft D0.5 (not submission-ready)](papers/0.28/RADIUS_RESTRICTED_CUBIE_OBSERVATION_DRAFT_01.md) and [literature/novelty gate](docs/0.28/LITERATURE_AND_NOVELTY_GATE_20261103.md). Prior exchange-property work includes Boutin (Graphs and Combinatorics 25, 2009, DOI 10.1007/s00373-010-0880-6); the B6 sensor exchange obstruction must **not** be presented as a new general exchange theorem.
- **0.26/0.25 and earlier:** version-specific [docs](docs) and Git commit SHAs preserve the historical program. Old 0.18 `30≤M*≤34` and 0.19 dictionary optima are **different mathematical models** from `b_r`; numerical cross-comparison without a model bridge is invalid.
- **Full pre-rewrite README snapshot:** [2026-11-03 Google Drive CUBE-REV/README archive](https://docs.google.com/document/d/1wNsqPo3Iit14kDNkugY_84VmEtDMTSUnhLxzw_yNiJY/edit), corresponding to Git blob `bd643ceeef2f928efd89a0e54070aab424e8d88d`. The Google Doc reproduces every source character, with only Google's extra final document newline. The earlier 2026-10-12 raw Markdown archive remains [here](https://drive.google.com/file/d/1QQ18TJ2Ary6xl4tD1iRX3ErdVx5HDHwi/view).
- **Research OS:** [0.28 canonical Notion](https://app.notion.com/p/409ef561cf928193b3d1dc1165ad92ea) stores scientific verdicts; Drive stores immutable source snapshots and literature; GitHub stores compact executable sources and receipts. Do not publish private human records or infer observed human behavior from solver output.

**Contributors and branch hygiene.** Every Git commit must have authenticated human **author AND committer**; `github-actions[bot]` and `github-action[bot]` are prohibited. Actions have `contents:read` and must not write commits. Repository policy names `research/current` as the **single active research branch**, and 0.28 has already been integrated into it by non-forced fast-forward. The former `research/observation-generalization` branch is only an ancestor ref with **zero unique commits**; it is eligible for separate ref deletion after normal operator review. **Do not create a new research stage branch** or move/deploy `main` automatically. The stable `main` publication/deployment branch must not be silently overwritten.
