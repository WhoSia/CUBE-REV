# CUBE-REV 0.28 — R14-P8.19: Radius-5 to Radius-6 Basis Attrition With an Explicit Physical-Certificate Gate

Date: 2026-11-11. Status: independent geometry-to-historical-witness-ledger cross-check, not a fresh P48 original move-pair search or a new unqualified published theorem. Main goal is to decide what changes at r=6 when b5=b6=16 and distinguish the exact prior results from new arguments.

## 1. Established numeric phase transition

The fixed-center legal 3x3 18-HTM symmetric radius balls B5 and B6 use the SAME twenty persistent original full position-and-orientation tag sensors. Both have minimum identifying sensor count 16. The earlier physically sealed B5 census produced exactly 576 B5-positive sixteen-tag layouts (all 2 adjacent omitted corners plus 2 omitted edges); the independent physical B6 closure leaves 156 positive layouts. The two valid-layout sets are nested by state-domain monotonicity.

| Count at a fixed original adjacent-corner core edge h | B5 | Newly B6-invalid | B6 |
|---|---:|---:|---:|
| 2-edge omission pairs permitted among 66 | 48 | 35 | 13 |
| Number across 12 core edges | 576 | 420 | 156 |

Thus a uniformly drawn B5 optimum survives the larger radius with exact probability 13/48 and fails with probability 35/48. b5=b6=16 does NOT imply that the same sixteen-tag arrangements remain optimal. This is an important concise physical transition example, but **the 576/420/156 and 18/35/13 results already existed in the 2026-11-04 source genealogy**; the P8.19 audit must NOT rebrand them as newly discovered mathematics.

## 2. Source-provenance hierarchy

**Primary archived B5 physical evidence:** CUBE_REV_20261030_EXACT_B1_B5_SENSOR_CERTIFICATES.zip, historical SHA-256 002887a198bac812ad360ba536309f2522899d5c28d12fb73bb92062ae889c94. Earlier scripts read b5_sixteen_layout_census.json from this archive, obtain 27 eligible proper rotation representatives and reconstruct 576 labelled layouts. The archive has not been downloaded or its raw bytes re-hashed in P8.19.

**Primary independent P48 B6 physical evidence:** scripts/cuberev-observation/verify_b6_complete_4845_p48.py (whole 4,845 negative classifier), verify_b6_negative_19_pairs_p48.py (nineteen literal 6+6-HTM word-pair seeds, 420 proper-rotation support masks), b6_independent_48sticker_goals.py, and the 41-target exact MITM scripts. Historical read-only Actions runs are linked in the top README, but actual new runs of the original physical certificates have NOT been observed in P8.19.

**Preexisting category reference:** docs/0.28/B6_66_PARTITION_EVIDENCE_AUDIT.md already shows every omitted-two-edge type per native omitted-corner core. It is the source of the B5-failed/B6-newly-failed/B6-success counts; its old B5 18 negative + B6-new 35 negative + final 13 positive compose all 66.

**New independent test:** scripts/cuberev-observation/audit_r14_p819_b5_b6_transition.py rebuilds every original cube corner/edge from six orthogonal outward face normals, assigns each edge relative to a native core to h/N/P/F/A type, enumerates all 66 unordered edge omissions for each of the 12 cores, independently applies the B6-positive coordinate rule, and verifies agreement with EVERY entry of the inherited 13-category physical count ledger. The local runnable copy was executed and returned PASS. It deliberately does not predict the exact identities of N-P B5 failures.

## 3. The easy-to-miss 4+4 N–P exception

For core h there are four near edges N and two parallel-side edges P, yielding EIGHT N-P pairs. The historical physically supported division is FOUR already invalid at B5 and FOUR newly invalid at B6; **all eight are invalid at B6**. Assigning all eight to prior B5 failures, as a naive type-based rule would do, incorrectly predicts 44 rather than 48 valid B5 pairs per core and 528 rather than 576 B5-positive sixteen-sensor layouts. Our first independent geometry implementation intentionally exposed this undercount instead of accepting it; the final checker explicitly records 4 old + 4 new and leaves individual-B5 N-P classification awaiting original word-pair replay. This is an observed substantive falsification of an overcoarse hypothesis, not an invented new phase result.

Other newly excluded per-core classes include N-F sixteen of thirty-five (the historical K4,4 obstruction), P-F eight, N-P four, P-A two, N-N two, F-F two, and h-A one. Summing across all cores, the near-far family contributes 192 of the 420 newly lost sixteen-sensor designs; the other known classes contribute 228. Nothing remains unclassified at the COARSE TYPE COUNT level, but distinguishing the concrete N-P pair IDs is still a separate physical evidence task.

## 4. Structural research hypothesis and an honest new theorem gate

Define survival of a labelled fixed-size design S by its critical radius rcrit(S)=minimum radius r where S stops identifying B_r, or ∞ if it remains identifying globally. For the physically certified B5-positive 16-tag family, precisely 420 designs have rcrit=6 and 156 have rcrit>=7; their eventual larger-radius failures were not checked here. This is a convenient **reparameterization of the older 576/420/156 census**, not a new unconditional theorem.

A genuinely new higher-value question is whether the first obstruction to a design's survival can be predicted from a human-sized invariant (stabilizer support incidence, original corner/edge geometry, or a finite orbit classification) without solving each B2r shortest word problem. A second test is the change of the minimum versus inclusion-wise minimal spectrum M(B5)->M(B6); do NOT assign B5 432 or a B5 minimal17 count without a separate B5 full-injectivity classifier. The observed fact b5=b6=16 alone gives no information about M(B5).

## 5. Execution status and immediate next experiment

The local test executed `python /mnt/data/cuberev/transition.py` and obtained status R14_P819_B5_B6_CATEGORY_TRANSITION_LEDGER_CONSISTENCY_PASS, 12 cores, exact 18/35/13 grade, 576/420/156 counts, 13/48 survival and correct N-P 4+4 split. The repository version and read-only workflow cross-check the same graph and historical per-category facts and output JSON that explicitly says original P48 word pairs were NOT rerun. GitHub Actions new workflow result remains unobserved.

Next: reconstruct the four B5-invalid N-P edge-pair IDs for one fixed core **from the original B5 physical witness words**, not from a guessed geometric rule; compare after 24 proper rotations to all cores and see whether the identity can be phrased in a concise geometric predicate. Then reproduce at least one newly B6-invalid N-F and one N-P actual pair of <=6 HTM words using the independent P48 checker before attributing a new physical proof to this stage.

Paper gate: integrate the phase transition as a small explicit illustration in a future B5-to-B6 structural theorem only if something more than the old enumerative 576->156 phenomenon is established. Keep the one-paper C0.1 editorial candidate but avoid extra paper sprawl. All source commits require human WhoSia author/committer on research/current; CI cannot write code.
