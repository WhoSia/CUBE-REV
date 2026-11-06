# CUBE-REV Paper A â Referee-Grade Proof and Novelty Gate

**2026-11-06 Â· independent editorial scientific audit Â· not a declaration of submission readiness.** Canonical current manuscript: `papers/0.28/RADIUS_RESTRICTED_CUBIE_OBSERVATION_DRAFT_01.md`, current D0.5. This document is a referee-facing risk audit and a bounded D0.6 manuscript revision specification.

## The claim the paper must actually establish

For the legal, fixed-centre 3x3 cube and the symmetric eighteen HTM generators, B_r consists of states at word distance <=r from the solved state. A **tagged cubie sensor** observes the full *original persistent identity, current location and orientation* of a selected original edge or corner. Define b_r as the smallest number of such sensors whose observation map is injective when restricted to B_r.

The central case-specific theorem is **b_6=16, with exactly 156 optimal 16-tag sensor sets among C(20,16)=4,845**. The competing requirements are (i) a lower certificate excluding every 15-sensor design and (ii) positive geodesic certification for every one of the 156 surviving 16-sensor designs. Present them separately. The elementary reduction pi_S injective on B_r iff H_S intersect B_2r={identity} is a standard group-action / word-length fact and is *not* independent novelty.

### Proof object table (referee audit)

| Claim | Dependence | Evidence and remaining audit |
|---|---|---|
| No fifteen sensors suffice | Actual <=5 + <=5 two-sided P48 collisions cover each 3-edge support, and <=6+<=6 pure nonadjacent-corner supports; 15,504 five-omission patterns | Fresh B5 physical 621,649-state BFS and 13 source edge-triple orbit representatives reproduce 220/220 original triple supports; independent P48 corner witness replay; require frozen 15-sensor receipt linked to a precise commit |
| Exactly 4,689 out of 4,845 16-tag layouts fail | 220 triple-edge, 16 nonadjacent-corner, 216 B5 adjacent 4-tag, 420 B6 adjacent 4-tag physical supports | 872 distinct irredundant supports; prove class order and disjoint counts 2,255+1,798+216+420=4,689; attach machine-parseable all-layout witnesses |
| All 156 survivors are positive | 12 adjacent missing corner pairs x 13 allowed edge pairs each, eight layout orbits, 41 independently generated stabilizer target classes | Each nonidentity stabilizer representative must have HTM distance >12. Fresh P48-derived exact six-ball MITM verifies 41/41; attach seeds, bounds, source and remote execution receipt, separate proof of why 41 classes suffice |
| Single-cubie erasure minimum =19 | Pure two-corner and all three-edge support witnesses; positive extension coverage | Check every mandatory corner/edge argument under one-erasure definition, do not use false 16-positive-core converse for 17/18 sensors. Exactly twelve size-19 robust layouts, all eight corners +11 edges |
| Exchange graph disconnected | 156-positive family geometric predicate + symmetric one-tag exchange | 156 vertices, 336 edges, 25 components (one 96, twelve 4-cycles, twelve isolates); clear counterexample to matroid basis exchange but note this failure is generic prior art |

The complete B6 classification is the paper's shortest central theorem; one-erasure and exchange geometry are structural corollaries, not replacements for its independent physical proof.

## Critical mathematical editing decisions

1. Avoid saying a 48-sticker move-permutation geometry alone proves that a stabilizer element has length >=13. That needs the separate exact distance search. For a positive 16-tag set S, the proof is: explicitly enumerate all nonidentity elements of its stabilizer, reduce them to the audited 41 distance classes, and show each is absent from B12 by **complete**, symmetrically generated six-ball MITM.
2. When stating the 872 supports are irredundant, specify **relative to the selected certificate family** and demonstrate private rejected four-tag layouts. Do not claim no smaller alternative proof family exists.
3. Write the exchange graph as *a property of the precisely defined optimal 16-tag set family*, not a new generic theorem that basis exchange can fail. Boutin already demonstrated exchange-property failure in other graph families.
4. The erasure threshold 19 must rely on actual physical pair-collision witnesses, not the false inference that every large valid set contains a valid minimum-size core. The manuscript already documents and retracts the latter; retain the correction visibly.
5. Distinguish original tagged full cubie sensors from spatial one-facelet six-color sensors (Paper B), and never use the latter's 18â21 adaptive horizon to motivate or prove the former's sixteen-tag minimum.
6. For every computable number, specify whether it comes from a complete mathematical census, a unique physical witness replay, a finite probabilistic simulation, or historical data. The manuscript must not treat these as equivalent proof levels.

## Prior-work correction and risk

Boutin, D. L. *Determining Sets, Resolving Sets, and the Exchange Property*. *Graphs and Combinatorics* 25 (2009), 789â806. Published online 10 February 2010, DOI 10.1007/s00373-010-0880-6. The 2008 arXiv version is at https://arxiv.org/abs/0808.1427 . The author's repository full-text manuscript is available at https://people.hamilton.edu/documents/ExchangeProperty.pdf . The current Paper A reference erroneously says âFull text still awaiting inventory,â while a full-text Drive record was already found in the wider project. **Correct that inaccurate custody sentence; do not assume arXiv/manuscript equals the published journal final text line-for-line.**

Bailey and Cameron (2011) already surveyed base size, metric dimension and related invariants; Dalla Volta et al. (2024) studied minimum base sizes; recent fault-tolerance metric-dimension works predate our fault-tolerance terminology. We do not assert a comprehensive negative prior-art search. A targeted exact-model search for `tagged original cubie partial radius ball`, `Rubik base B6`, and `finite Cayley ball identifiability` found no verified exact identical result at this stage, **not** proof that none exists. A paper-level novelty verdict remains pending.

## New model-robustness demands before submission

- Fix the exact 18 HTM move generators and what constitutes a sensor output: persistent original edge/corner identity, position, and orientation.
- Show an alternate output/metric would change the theorem's meaning rather than imply the same sixteen-tag value.
- Provide enough certificate data to verify the 4,845 classification without trusting cached labels. Positive and negative certificates should be independently executable and SHA-sealed on Drive, with GitHub commit refs and remote CI run IDs.
- Explain the distance-search completeness in simple graph-algorithm terms (B6 root search + goal intersection) and include complexity/memory measured on actual executed runs, not fictional benchmarks.
- The paper's main theorem/abstract should stay concise: state b6=16 and 156 layouts, then two structural corollaries (erasure 19 and disconnected swap graph). Detailed intermediate 41/74/88 class genealogies belong in supplementary computational evidence.

## Deliverable gates

- **A0 (source):** all five numerical claims in the table link to a live/replayable source, immutable checksum and independent verification status.
- **A1 (proof):** the minimum-threshold proof has one closed graph of dependencies; every branch covers all cases without circular reference to archived 54-sticker data.
- **A2 (writing):** abstract, theorem statements, proof outline and figures read as one mathematical paper; no repeated historical diary-style paragraphs in the main text.
- **A3 (novelty):** formal prior-art comparison explicitly distinguishes cubie bases, graph determining sets, and sensor resolution. No novelty priority claimed until exact overlap ruled out.
- **A4 (release):** independent collaborator/referee could reproduce numerical outputs and verify every claimed SHA and CI reference using the fixed package.

**Decision:** Paper A is closest to publishable structure but not submission-ready. Revision should focus on proof compactness and independent provenance, not yet another finite sensor-count table. Work on exact adaptive 20-frame Paper B must proceed in parallel.
