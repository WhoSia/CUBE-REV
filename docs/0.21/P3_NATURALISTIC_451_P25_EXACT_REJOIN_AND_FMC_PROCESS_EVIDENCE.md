# CUBE-REV 0.21 — P3: Naturalistic 451-Solve Rejoin, Exact FC3 Behavioral Support and FMC Process-Evidence Court

**Inherited active version:** CUBE-REV 0.21 — Active Reconstruction of the Rubik's Cube: Observation-Driven Action Selection, Belief-State Dynamics, Physical Information Access & the Limits of Adaptive Solving.

**Status (2026-10-10):** **P3 LOCAL VERIFIED / LEGACY P25 EXACT REPLAY PASS / 451-SOURCE DESCRIPTIVE EXTENSION / NEW HUMAN MECHANISM & GENERALISATION HOLD / FMC TEXT EVIDENCE GROUNDED / VIDEO NOT ACQUIRED**. P0–P2 and all previous versions remain intact. This work follows the archive-based rule SECONDARY DATA FIRST; no new human recruitment or 24-task deployment was performed.

## A. Physical and documentary inputs — checked bytes

1. Canonical old secondary-data derivative: [Drive CUBE_REV_0.11_RECOVERED_452_PRIVATE_REPLAY.zip](https://drive.google.com/file/d/1NYY_8J47dnFnevfqc8g_dj5bKkyiOuO8/view), 1,370,797 bytes, verified SHA-256 `fb88827cce327d0021a0741e47dfa09670651083b8baaaa46cccc9051d73568e`. Its three ZIP members `MANIFEST.json`, `exact-trajectories.json` and `prefix-states.jsonl` all pass ZIP corruption check. Its 452 source IDs contain 25,320 recorded actions and 25,772 cubie state snapshots including each initial position. Original source HTML excluded, rights remain private research derivative: **do not republish corpus**.
2. Content duplicate: source IDs `2778` and `2970` give the same complete scramble+raw token/kind sequence+solved record; keep original source identity in custody but designate one representative for **451 distinct complete reconstruction contents**, 25,272 next-action rows and **25,723** state rows including terminal. The **21,118** face-turn records are only a subset; wide turns, slices and cube rotations are other action types.
3. Genuine historical G7-P24 primary [GitHub Actions #37577119533](https://github.com/WhoSia/CUBE-REV/actions/runs/37577119533) artifact [#11462569548](https://github.com/WhoSia/CUBE-REV/actions/runs/37577119533/artifacts/11462569548), ZIP SHA-256 `41d53aaf0f354660882e744dcfb2d215e13a5ee9f8872bdf54db788bc172fad8`. Contains the actual **3,329 original 60-source** `observations.tsv` and exact FC6, FC4, FC3 operator recipe.
4. The original Rust FC observer [`g7_p24_fixed_center_census.rs`](../../crates/cuberev-core/src/bin/g7_p24_fixed_center_census.rs) encodes actual eight corner sticker positions and their orientation in the frozen face order `URFDLB`; FC6 uses six corner-face observations, FC4 `UFRD`, FC3 `UFR`. This is a **fixed-centre, corner-only observation operator**, **not a validated rendering of what a human visually sees** and not the special 0.21 P2 nine-color face camera.

## B. Exact G7-P24 and P25 reconstruction

A fresh independent local Python implementation reconstructed corner sticker facelets from every (cp,co) state, then compared `FC3 / FC4 / FC6` key strings **for all 3,329 historical 60-source P24 rows** via exact `source_id × prefix_index` join. **3,329 / 3,329 identical** (including 60 terminal states) to original immutable `observations.tsv`. Unlike superficially similar theoretical FC3 operators, this matches the actual P24 source implementation byte-for-byte at the observation-key level.

P25 former behavioral contrast at these original collision keys:

| Quantity | Historical original 60-source P25 replay |
| --- | ---: |
| FC3 distinct-corner-state collision keys | 10 |
| All nonterminal next-action rows in those keys | 25 |
| Cross-source SAME_CORNER_STATE pairs | 4; 3 disagree |
| Cross-source DIFFERENT_CORNER_STATE pairs | 17; 14 disagree |
| Key-balanced SAME mean | 0.833333333 |
| Key-balanced DIFFERENT mean | 0.700000000 |
| **Δ = DIFFERENT − SAME** | **−0.133333333** |
| Common-key-only sensitivity (2 common keys) | +0.166666667 |

Thus the old **G7-P25 CLOSED / DESCRIPTIVE PASS / PREDICTIVE HOLD** remains correct; its original negative descriptive evidence was genuinely recovered, **not redefined or overwritten**. Differences in denominator matter: a 10-key mean minus a 2-key mean is not matched-key causal inference.

## C. Expand original exact FC3 operator to 451 reconstructed real solves

Recompute FC3 / FC4 / FC6 on **every one of the 25,723** complete 451-source snapshots with **the same** P24 physical sticker projection; compare observation collisions by **distinct exact corner state**, not merely duplicate rows.

| Observation operator | Unique observed keys | Multi-state collision keys | Rows lying in multi-state keys |
| --- | ---: | ---: | ---: |
| **FC6** | 19,559 | 0 | 0 |
| **FC4** | 19,552 | 7 | 18 |
| **FC3** | 19,259 | **270** | **832** |

Original 60-source P25's ten collision keys still occur; **260** of the 270 collision keys were not occupied as distinct-state collisions in the original P7 set. This is **additional descriptive support from existing historical data**, not a freshly sampled population or a registered confirmation cohort.

For the complete 451 content-unique corpus, *nonterminal* cross-source pairs in FC3 multistate keys and cosmetically normalized next-action tokens (`X2'`→`X2`) yield:

| Comparison (descriptive only) | SAME corner state | DIFFERENT corner state |
| --- | ---: | ---: |
| Cross-source row pairs | 687 | 755 |
| Differing next-action tokens | 570 | 631 |
| Distinct FC3 keys with pair type | 90 | 268 |
| Key-balanced mean disagreement | **0.782711** | **0.803400** |

Hence the descriptive key-balanced difference on the broadened archival cohort is **+0.02068835**, versus **−0.13333333** in original P25. On the **391 non-P7** old source reconstructions alone, `Δ=+0.01160304` (211 multi-state keys; 617 associated rows). Restricting the 451 corpus to immediate next actions classified as FACE_TURN yields `Δ=+0.05415883` (253 keys, 728 rows). Among **90 keys that support both pair types in the 451 corpus**, within-common-key difference is **+0.03988141**. All of these figures are **descriptive changes with large key/source dependence**.

**No causal human-psychological conclusion:** All 451 are previously contacted naturalistic data, with solver/reconstructor dependence and nonrandom selection, not 451 independent people. The stored full cubie positions `(cp,co,ep,eo)` are center-canonical and do **not** retain the complete accumulated notation/viewpoint frame. Apparent action disagreement can arise from method/stage/past history, cube orientations, notation conventions, alternative legal actions, and recording or reconstruction bias. In-sample entropy or action splitting is not held-out prediction.

This P3 does **not** claim G7-P25's alias mechanism becomes true after changing the corpus. Instead, changing from `-0.1333` on ten observed keys to `+0.0207` on 270 keys is a **selection/support fragility diagnostic** that motivates an honest nested/provenance-aware future test.

## D. FMC data custody versus evidence types — checked

**Drive audit:** The present CUBE-REV Drive folder `20_SECONDARY_DATA_FRONTIER` contains WCA export/raw/derived folders and an old 0.11 reconstruction corpus. A Drive search targeting FMC-specific filenames did not locate a curated, independently preserved **FMC search-process log dataset**; absence in filename/folder search is **not** a theorem that no other Drive file contains FMC metadata.

**Grounded external public sources:**
- [WCA FMC World 2026 official results](https://www.worldcubeassociation.org/competitions/FMCWorld2026/results/all): official competition and per-attempt numerical outcomes; does not expose a human solver's chronological internal search.
- [333.fm FMC World 2026 reconstructions](https://333.333.fm/wca/reconstruction/FMCWorld2026): community/player-provided submissions and optional written analyses; provenance and participant status are checked record by record.
- [Written FMC 2026 annotated case: Yining Wang](https://333.fm/wca/reconstruction/FMCWorld2026/2023WANY06): result entries 29,25,32 and public stage annotations including EO, RZP, DR, HTR, finishing stage. A stage-annotated final algorithm **does not establish which unsuccessful options were considered or when**.
- [Written FMC 2026 annotated case: Akash Sreedharan](https://333.333.fm/wca/reconstruction/FMCWorld2026/2019SREE06): 23,22,DNF entries; two completed entries annotate EO, RZP, DR, HTR and finish. Third entry includes a self-report of an error; it is **self-report**, not independently observed search-time behavioral causality.

**Conservative ontology of admissible labels:**
- `WCA_OFFICIAL_OUTCOME`: official attempt/result/DNF and scramble when exact linkage.
- `SUBMITTED_ALGORITHM`: final written 3×3 move sequence if source rights permit derived use.
- `AUTHOR_EXPLICIT_STAGE`: preserved raw EO/RZP/DR/HTR etc. markers, mapping to normalized category only after expert audit.
- `AUTHOR_REPORTED_SEARCH_CLAIM`: human statements as reports, distinct from time-stamped verified behavior.
- `OBSERVED_BRANCH_CHANGE`, `REJECTED_CANDIDATE`, `HESITATION_TIME`, `FUTURE_SEARCH_PREVIEW`: **UNKNOWN** from final solution; no invented values.
- `VIDEO_VISIBLE_ACTION` and `VIDEO_EXPLICIT_UTTERANCE`: only after a verified accessible video is used to support a specific unresolved hypothesis; track continuous time, edits and occluded portions. **No video was fetched or automatically labeled in P3.**

**Different tasks:** FMC is a time-limited written solution-length optimization, whereas speedsolve seeks fast completion and reco.nz mostly contains selected speedsolve trajectories; WCA macro attempt data lacks move-by-move policy histories. Do not equate FMC move-count, `M^*(L)` preset dictionary size and 0.21 adaptive feedback depth.

## E. Transparent artifact/proof grades

**Local independent computation DONE:** original 3,329-row P24 byte-exact-key replication; old P25 `-0.1333333` contrast replication; source-content dedup 452→451; full 25,723-row original FC3/FC4/FC6 extension; explicit pooled and non-P7 subset sensitivity; verified public FMC source/annotation examples. A reproducible six-file local research package includes two standard-library Python programs, the 451 aggregate JSON receipt, small source-observation audit JSON, a README and the original P24 public GitHub proof ZIP. **The private 452-solve research corpus is intentionally excluded** and remains on Drive. Package SHA256 `95b2fb4fe2616b249c5fba806d3ce25fb4ca34443a6815d7682455e8922bef6e`, 86,479 bytes.

**Not executed / do not claim:** external GitHub CI for the new 451-source derived results; source-unique human cognitive mechanism; independent prospective replication; newly downloaded FMC bulk solution corpus; video-based reconstruction of internal search; any human participants. This is a P3 **research-result / descriptor promotion**, not a replacement for former P25 or an automatic claim of FMC behavioral process.

**Next hypothesis, not yet a result:** Which part of FC3 observational aliasing survives controlling for full edge and corner state, observed move sequence and notation frame, matched progress/phase, solver/reconstructor and source selection? Use recorded FMC solutions for explicit written stage evidence and videos only when a measurable unobserved search-stage event has a genuine source and meaningful inferential role.

**Result:** `P24_REFERENCE_KEYS_3329/3329_EXACT__P25_HISTORICAL_DELTA_REPRODUCED__451_TRACE_FC3_EXTENDED__INFERENCE_NOT_IDENTIFIED__FMC_SOURCE_AUDITED__VIDEO_HOLD`.
