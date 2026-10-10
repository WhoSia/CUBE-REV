# CUBE-REV 0.21 — P6: Source-Grounded Search-Graph Reconstruction, Non-Evaluated FMC Alternatives, Retrospective Event Partial Orders & Video Evidence Boundary

**Version continuity:** CUBE-REV 0.21 — *Active Reconstruction of the Rubik's Cube: Observation-Driven Action Selection, Belief-State Dynamics, Physical Information Access & the Limits of Adaptive Solving*. This is an additive P6 research chapter. **Do not reset or overwrite 0.11/FACTORY, G7 P24–P27, 0.18–0.20 or 0.21 P0–P5 results.** Secondary data first, no fresh participant recruitment, no fabricated human action traces.

**Verdict:** `FMC_AUTHOR_REPORTED_EVENT_PARTIAL_ORDERS_RECONSTRUCTED__EXACT_GRAPH_COURT_EXTERNAL_PASS__UNREPORTED_EVENT_ORDER_HELD_UNKNOWN__NON_EVALUATION_NOT_MISCLASSIFIED_AS_FAILURE__ONE_AUTHOR_LINKED_VIDEO_FOUND_NOT_VISUALLY_AUDITED`.

## 1. Exact inputs and audited primary source correction

The original [P5 historical FMC event seed](../../data/cuberev-021/p5_fmc_existing_search_event_seed.json) comprises six public, retrospective or written-work-note cases: 29 authored-report event labels across five authors. No original article transcription, full source solutions, private 452-solve corpus or real video content is copied into the repository.

P6 adds two **already published actual FMC competition solve accounts** from a seventh and sixth distinct authors:

1. **Vincent Hartanto Utomo, FMC World 2026, Final Attempt 3**, **24 HTM** ([source](https://333.fm/wca/reconstruction/FMCWorld2026/2010UTOM01); [official WCA event](https://www.worldcubeassociation.org/competitions/FMCWorld2026)). The original page explicitly places a long narrative of reopening a previously tested DR, inspecting another continuation, **choosing not to try a seemingly obvious HTR extension because it appeared too time-consuming**, and **not writing an additional EO candidate** under **Attempt 3**, not Attempt 2. The authoritative primary-page read at lines 83–120 corrects an initial working-label error before P6 release: **A3 / 24 HTM**, never A2 / 19 HTM. A hypothetical absolute ~35-minute hesitation is only the author's recollection and not entered as a verified time anchor; exact attempt time uncertain.
2. **Wong Chong Wen, Don't DNF December Singapore 2025, Final Attempt 3**, **20 HTM** ([original retrospective annotated solve](https://333.fm/wca/reconstruction/DDDSingapore2025/2014WENW01); [official WCA attempt results](https://www.worldcubeassociation.org/competitions/DDDSingapore2025)). The author describes not checking the 3-move EO family until about 30 minutes, spending time on an 8+1 route, subsequently examining a DR with limited progress, identifying a meaningful widening possibility at about 45 minutes, and never returning to a separate prior 18-to-slice route. Crucially **the author's own solve account contains a direct YouTube video link**: [youtube.com/watch?v=ftj2Mh0dEpw](https://www.youtube.com/watch?v=ftj2Mh0dEpw). This is an **author-linked candidate**, NOT proof the full hour is filmed, uncut, legible or retrievable through the current tools. **Video frames reviewed: 0; visual action labels: 0.**

The new P6 [source-qualified case supplement](../../data/cuberev-021/p6_fmc_partial_order_extension.json) records twelve new event labels, explicit edge warrants, author names and stable source pages. Total **eight historical attempt/worknote cases, seven distinct named authors, 41 reported-event labels**. This rich-case convenience sample does not represent a population of FMC attempts.

## 2. Mathematical/computational object, and what is NOT justified

For each already-published solve report, let `V` be the set of discrete **author-reported** exploration events (candidate written, candidate attempted, attempt avoided, backup stored, option revisited, representation rewritten, submission). Let `E_≺` contain an arrow only when the author report or an obvious documentary dependency specifically supports the before/after relation. **The order in which a website paragraph happens to be written, or our P5 `sequence_index`, does NOT automatically become a chronological edge.**

Candidate references/revisits `E_ref` are another relation; these do not automatically establish event chronology (e.g. returned to an **EO search pool** does not mean the same particular EO sequence was tried again). A later different-author addition `E_doc` is a third type, **not** an action of the original solver.

Formally, `G=(V,E_≺,E_ref,E_doc)`; check `(V,E_≺)` is acyclic and compute its transitive closure `≺⁺`. For two events in a common case, the relative order is *currently known by the author account* if and only if `a ≺⁺ b` or `b ≺⁺ a`. Otherwise mark `UNKNOWN_RELATIVE_ORDER`. These are *partial-order constraints about reports*, **not video-confirmed ground truth of cognition**. No cardinality of the written candidate set (for example >50 or 42 EO entries) is expanded into invented candidate-evaluation events. This P6 **does not** solve cube states for all author-mentioned alternatives, which often lack enough input notation.

### Externally replayed P6 numerical court

| Quantity | Verified result |
| --- | ---: |
| Distinct historical author-reported cases | **8** |
| Named authors represented | **7** |
| Curated reported-event nodes | **41** |
| Independently warranted direct before/after edges | **27** |
| Other-author documentary later-addition relation | **1** |
| Candidate/branch/return cross-references | **11** |
| Within-case unordered event pairs total | **105** |
| Event pairs ordered by supplied temporal edges or their logical closure | **71** |
| **Event pairs with unresolved relative order** | **34** |
| Explicit reported revisit events | **4** |
| Explicitly deferred/unassessed candidate events | **3** |
| Candidate not even written (separate from tested-and-rejected) | **1** |
| Author-reported elapsed-time anchors | **9** |
| Independently authenticated time anchors from sensors/uncut footage | **0** |
| Explicit author-linked candidate videos | **1** |
| Frames actually examined / historically published real .vfmc user sessions acquired | **0 / 0** |

**Interpretation:** (71/105) indicates the *density of recovered relative event ordering among this hand-selected compact seed*, not the proportion of real FMC decisions observed. Missing 34 pairs mean no claim of ordering, even when a chronological sequence would look tidier. Adding a hypothetical relation to make each source a complete timeline would fabricate evidence.

### Case-by-case precedence under evidence limitation

| Case | Reported events | Ordered comparable pairs | Unknown relative-order pairs |
| --- | ---: | ---: | ---: |
| Wheeler 2026 A1 | 10 | 33 | 12 |
| Quraishi 2026 A3 | 6 | 15 | 0 |
| Dong 2026 A1 | 3 | 3 | 0 |
| Dong 2026 A2 | 3 | 3 | 0 |
| Pietrusiak 2026 A2 | 3 | 3 | 0 |
| Guido historical work note | 4 | 3 | 3 |
| Utomo 2026 A3 | 6 | 6 | 9 |
| Wong 2025 A3 | 6 | 5 | 10 |

**Caution:** If an author presents the selected *few* events sequentially, all of those event-pairs may be ordered in the resulting `G`; it does NOT mean their full search had no hidden unreported branches. Computational poset antichain width is **number of events currently incomparable under reported precedence**, not evidence the author considered them simultaneously, and not the finite-state width of a human's memory.

## 3. Actual behavioral-science value — what the new structure supports

Three distinguishable human actions are present in the reported record:
1. `CANDIDATE_WRITTEN`: a candidate exists in the writer's recorded search space.
2. `CANDIDATE_ATTEMPTED` or `AUTHOR_REPORTED_UNPRODUCTIVE_SEARCH`: the candidate or family was actually explored; author's report about success/failure is graded.
3. `DEFERRED_UNEVALUATED` / `CANDIDATE_NOT_WRITTEN`: an alternative was described without an evaluation or without being transcribed; **do not code as attempted failure.**

The third group is especially relevant to resource-rational and behavioral-economic hypotheses: a subject may skip a potentially informative option due to subjective time cost, perceived branch complexity, current backup, or final answer pressure. These reports **provide descriptive occurrences**, not causal evidence that the cited subjective cost generated the choice. Multiple explanations—objective low promise, note-taking bias, retrospective rationalization—remain open.

A revisit is **not** evidence of a memory defect. It can arise from newly acquired conditional information, a fresh representation/NISS reverse direction, changed estimated return on investment or time pressure. Consequently P6 protects future cognitive modeling from a frequent misclassification: `BACKTRACKED` does **not** imply `FORGOT`.

This is the bridge from the original 0.21 physical active-information court to actual actions: formal optimality on a one-edge idealized sensor is one ontology; these authored *candidate-list/search-history* objects are a different observational regime. Do not claim these reported search event graphs prove a 7-vs-9-turn physical feedback advantage in full FMC.

## 4. Video adjudication: first person-linked real-solve candidate, still no visual verification

A genuinely promising **new source lead** is the direct YouTube link in Wong's authentic competition-specific reconstruction. Its source report states that attempt 3 was filmed. The official WCA result (attempt 3 = 20) independently matches the episode identity. However a linked video itself has NOT been examined for actual duration, visible cube/notes, continuity/editing or the relevant 30-minute and 45-minute statements. **Only two claims are warranted:** (a) the author linked this URL as the corresponding filmed solve, and (b) the page and official competition identify the FMC attempt.

**Next minimal video gate** when actual frame access becomes available:
- Independently check URL resolves and title/date/attempt mapping, duration, edits and recording source.
- Sample **the 25–35 minute and 40–50 minute intervals** for visible puzzle/worksheet manipulation *only if they genuinely appear in this uncut recording*. Do not assume original recording clock aligns with the self-reported FMC 60-minute timer.
- Split `VIDEO_VISIBLE_PHYSICAL_ACTION`, `VIDEO_VISIBLE_WRITTEN_CANDIDATE`, `AUDIO_EXPLICIT_SELF_REPORT`, `RETROSPECTIVE_COMMENT`, `AI_VISUAL_INFERENCE_UNVERIFIED` and `OCCLUDED/EDITED_UNKNOWN`.
- Assess image/frame accessibility, platform conditions and source consent before extracting/reusing content. Preserve minimal event paraphrases/locators rather than copyrighted clips or full third-party transcripts.
- **An audio-only integration cannot meet the visual action gate.** Don't call a video-grounded label verified until frames are independently inspected.

No need to repeatedly suggest a newly recruited human experiment. Genuine historical user .vfmc session is still a possible future high-resolution source, not one already acquired.

## 5. Computational reproduction, scope and custody

Sources:
- [P5 baseline real FMC retrospective event seed](../../data/cuberev-021/p5_fmc_existing_search_event_seed.json) — historical 6 episodes / 29 reported events (preserved unchanged).
- [P6 source extension / per-edge evidence reasons / 2 new original records](../../data/cuberev-021/p6_fmc_partial_order_extension.json) — 8 episodes total, does NOT import 452 private solve bytes.
- [P6 **fresh exact Python verifier**](../../scripts/cuberev-021/verify-p6-fmc-source-grounded-partial-order.py) — input SHA256, DAG topological sort and cycle veto, transitive closure, unknown-order pair count, author-reference link types, a small combinatorial Dilworth max-incomparable antichain test, per-episode retained support, case A3-vs-A2 and HTM count regression, author-linked video honesty boundary. No unknown chronological edge created via `sequence_index`.
- [P6 external **GitHub Actions SUCCESS** #38045975478](https://github.com/WhoSia/CUBE-REV/actions/runs/38045975478) and [actual graph + exact computational receipt artifact #11667229396](https://github.com/WhoSia/CUBE-REV/actions/runs/38045975478/artifacts/11667229396) SHA256 `add3f4c24326e152f069ff7669013866b1dcb8dbaf254d793284e63ed51bbe79`.

The earlier CI **#38045902938** was also SUCCESS but used a less clear poset width field name; P6's authoritative run is **#38045975478**, with the field corrected to `max_set_of_currently_incomparable_events` so nobody confuses mathematical antichains with actual simultaneous human thoughts. Original unrelated P7 repository active-set CI failures remain separately tracked and not silently rewritten.

**External CI proves source-encoding/DAG computations against admitted research inputs; it does not automatically refresh or independently fact-check every external author webpage.** Original content was read from linked public pages for the two added narratives, and manually curated P5 remains retrospective. Existing G7-P25 cognitive causal effect and P27 independent method-effect replication remain **HOLD**.

## 6. Natural next research (P7 candidate, not invented success)

Before another abstract controller theorem, look for **one actual existing complete documented FMC attempt** with command history and sufficient chronological information: original posted `.vfmc` user session, period-authentic attempt notebook snapshots, or independent video frames matched to an officially known scramble. Only then can an effective choice set at each decision point be inferred at a stronger grade. If none is acquired, formally identify *what cannot be deduced from a partially ordered self-report DAG*: branch evaluation count, time spent on unvisited possibilities, candidate revisit frequency per person, and any time-cost coefficient.

**P6 state:** `CLOSED / SOURCE-GROUNDED RETROSPECTIVE EVENT DAG & UNCERTAINTY AUDIT PASS / HUMAN COGNITIVE EFFECTS, TIME AND VIDEO FRAMES NOT IDENTIFIED`.
