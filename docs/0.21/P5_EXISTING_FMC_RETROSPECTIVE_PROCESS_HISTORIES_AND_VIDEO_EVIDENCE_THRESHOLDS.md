# CUBE-REV 0.21 — P5: Retrospective Human FMC Search Histories and the Boundaries of Behavioral Reconstruction

**Continuity:** This is an additive chapter in CUBE-REV 0.21 (*Active Reconstruction of the Rubik's Cube: Observation-Driven Action Selection, Belief-State Dynamics, Physical Information Access & the Limits of Adaptive Solving*). Original 0.11/FACTORY/G7 P24–P27 and 0.18–0.20 physical results are unchanged. **Secondary data first; no new participant recruitment.**

**Evidence verdict:** `EXISTING_PUBLIC_FMC_RETROSPECTIVE_SEARCH_EVENTS_RECOVERED__ORDERED_NARRATIVES_PARTIAL__CANDIDATE_DEFER_NOT_EVALUATED_DISTINGUISHED__TIMESTAMPED_DIRECT_PROCESS_TRACE_NOT_ACQUIRED__VIDEO_FRAME_GROUNDING_HOLD`.

## 1. The research object: actual reported exploration, not an idealized policy

A finalized written FMC algorithm can show the submitted sequence and publicly described stages (EO, RZP, DR, HTR, slice, finish); alone it cannot tell when an alternative was generated, ignored, revisited or rejected. We searched and inspected actual already-existing author reports and historical annotated working files for **reported temporal ordering**. The evidence hierarchy is:

- **Official event/outcome**: WCA competition/result (valid outcome, not planning history).
- **Contemporaneously saved executed command sequence**: a genuine `.vfmc` command history, if independently sourced, could preserve discrete logged decisions, but not unlogged deliberation or wall-clock times.
- **Retrospective author narration / archived working note**: may support stated before/after, candidate counts and self-reported times, with provenance tag `AUTHOR_RETROSPECTIVE_STATEMENT`.
- **Video-visible actions/utterances**: require actually inspected video frames and timecode, with annotation of edits, occlusion and provenance; audio-only text is not video observation.
- **Unobservable mental options or cognitive costs**: `UNKNOWN` unless supported by appropriate independent measurements.

None of the P5 events are certified as direct, continuous, timestamped real-time behavior. No study should convert a writer's submission timestamp into an attempted-action timestamp or a self-reported candidate count into objectively checked branches.

## 2. Actually acquired public records (compact annotated seed, not copyrighted full text)

**Six episodes/worked cases by five authors, 29 curated retrospective or archival events** from the following authentic source pages:

1. [Alexander Wheeler, CubingUSA Southeast FMC Championship 2026 Final A1](https://www.api.333.fm/wca/reconstruction/SoutheastFMCChampionship2026/2014WHEE01). Highly informative stepwise retrospective: says >50 EOs were written without evaluating all; explicitly distinguishes first, then and next candidate options; an intermediate candidate was *deferred and never evaluated*, while another led to a 25-turn backup. Reported elapsed milestones: about 30 minutes (search-family switch), about 55 minutes (backup written), about 56 minutes (inverse/NISS revisit), approximately 2.5 minutes remaining (last refinement), and 59:57 (final writing completed). Submitted 20 HTM. **All time anchors are author-reported, not independent video timestamps.**
2. [Ibrahim Quraishi, FMC World 2026 Final A3](https://www.api.333.fm/wca/reconstruction/FMCWorld2026/2018QURA01). Reports many 5-turn EO candidates, an unproductive initial family until approximately 50 minutes, return to EO search, discovery of **two previously overlooked NISS 4-turn EOs**, then exploration of RZP/DR/HTR alternatives and final 21-turn solution. The claim about unproductive search applies to that person's account, not proof that every such route was impossible.
3. [Baiqiang Dong, FMC World 2026 Final A1](https://18.333.fm/wca/reconstruction/FMCWorld2026/2008DONG06). Reports previous 21-turn candidate involving slice insertion, revisit in the last ten minutes, and eventual 19-turn result. Exact timing or branch-by-branch record unavailable.
4. [Baiqiang Dong, FMC World 2026 Final A2](https://18.333.fm/wca/reconstruction/FMCWorld2026/2008DONG06). Reports **42 EOs written**, the selected continuation arising from the **38th EO tried**, and a 19-turn result. **Crucial:** `42 written` does *not* entail `42 evaluated`, nor does `38th tested` reveal the contents/order of all 37 preceding explorations.
5. [Krzysztof Pietrusiak, FMC Warszawa 2026 Final A2](https://www.api.333.fm/wca/reconstruction/FMCWarszawa2026/2019PIET01). Reports an earlier candidate and subsequent NISS reworking leading to final solution. Precise per-step clock chronology unavailable.
6. [Guido Dipietro, archival personal solution *24 with DR and neat stuff*](https://github.com/GuidoDipietro/FMC/blob/master/solutions/24%20with%20DR%20and%20neat%20stuff.txt). Personal historical working note contains a 27-turn draft, an explicit later revision after eliminating a rotation from the expression, a 24-turn rewritten outcome, and **another solver's subsequent 23-turn proposal**, tagged `OTHER_AUTHOR_POSTHOC_NOTE`—**not** treated as an action in the original author's search. Archived personal practice, not automatically an official 2026 competition attempt.

The [full public authored historical FMC repository](https://github.com/GuidoDipietro/FMC) also contains `data/__FMC_all.txt` (GitHub blob SHA `a0593f222e2d7618d71c94bd4b1472d94355b1fb`, 396,258 characters / 14,461 text lines at audited ref) plus numerous annotated solutions. Some records explicitly list first/second insertion candidates and later amendments. **This is a heterogeneous historical solution/work-note archive**, not one homogeneous ordered timestamped session table. Do not infer that every line is a human decision event, or that all notes were written while working.

**Curation source:** [data/cuberev-021/p5_fmc_existing_search_event_seed.json](../../data/cuberev-021/p5_fmc_existing_search_event_seed.json). This stores original Korean analytical paraphrases, exact page URLs, case IDs, reported event types, source kinds and seven **self-reported-only** time anchors. There are **29 event records**, **three explicitly reported revisits**, **three classified alternative-enumeration/comparison/selection event records**, **one never-evaluated candidate** distinguishable from a failed tested candidate, and **one other-author improvement** isolated from the primary author's actions. These numbers describe **the manually selected six rich narratives**, not prevalence among FMC contestants.

## 3. Why this evidence is substantially stronger than final algorithms but does not yet prove cognition

The Wheeler and Quraishi histories demonstrate author-stated **revisit** and **changing the focus of search**. Wheeler especially separates a candidate *not checked* from candidates where attempted extensions produced no satisfactory continuation. A physically impossible move path and an author who abandoned a promising route are different things. In action ontology terms we must distinguish `CANDIDATE_WRITTEN`, `CANDIDATE_TRIED`, `DEFERRED_UNEVALUATED`, `REPORTED_UNPRODUCTIVE_SEARCH`, `REVISIT`, `REWRITE/REPRESENTATION_SWITCH`, `BACKUP`, `FINAL`.

Even when a comment describes an exact order, it is a **retrospective account**, not a continuously logged observed sequence. Missing alternatives remain missing (not zero). An explicit difference between first and later candidate may be meaningful but cannot separate memory-limited search, deliberation-cost minimization, puzzle state opportunity and note-writing selection bias without further independent evidence.

No inference is made that a person saw the earlier `FC3` operator used by G7 P24–P27. Written FMC NISS search differs from speedsolve physical turning and from 0.21's orientation-one-bit sensor. Hypothesis linkage is explicit and modest: **the reported policy state includes candidate sets, revisit information and alternative-selection history which a final cube state alone does not represent**.

## 4. Independent VFMC code audit and honest negative data acquisition

[rodneykinney/VFMC](https://github.com/rodneykinney/VFMC) is an Apache-2.0 open-source virtual FMC practice environment, not a newly recruited population. [Original `src/vfmc/app.py`](https://github.com/rodneykinney/VFMC/blob/main/src/vfmc/app.py) implementation:
- `Commands.execute` appends executable interpreted commands and legal move entries to a command history. 
- `Commands.save_session` writes a VFMC version header and then a newline-separated ordered `command_history` to a `.vfmc` file.
- `Commands.load_session` executes these lines again.
- No independent per-command wall-clock timestamps are serialized in that save routine. GUI edits, thinking silently and operations not reflected in stored commands cannot be reliably recovered.
- Public GitHub targeted search (code search for `.vfmc`, `VFMC version`, etc.) predominantly returned the VFMC application implementation and unrelated uses of FMC; Google Drive filename search in the existing project did not identify a pre-existing real `.vfmc` user trace. **This is a bounded search-negative result**, not a proof that none are public. **Actual external historical `.vfmc` sessions acquired: 0.**

Potential next input is **an existing already-published user's `.vfmc`**, with its own provenance and permission constraints; do NOT generate a synthetic session and call it human data.

## 5. Media and the audio-only issue

Transcript/voice-only processing can support only explicit spoken statements. Visual claims about faces moved, observed cube configurations, candidate papers or hands require independent sampling of actual frames with timestamps and edits. A third-party tool advertising video analysis does not prove that its *currently connected interface* returns frames; if it returns only audio, grade it `AUDIO_UTTERANCE_ONLY`. A VFMC tutorial, post-event explanation or sped-up recreation is **not** continuous real-attempt observation. In this P5 we searched for full ongoing FMC footage but did not positively authenticate a usable uncut participant attempt for these six source cases. **Source-linked footage acquired: 0; frames inspected: 0; video labels assigned: 0.**

Escalate to actual audiovisual event tracing only if three checks pass: source video is a real task attempt and attributable to the corresponding published scramble/session; relevant frames and timecode can be accessed; rights, edits and occlusions are recorded. Otherwise continue with **existing written and command-log evidence**.

## 6. Certified code/receipt without overclaiming

- [P5 historical source-event ledger](../../data/cuberev-021/p5_fmc_existing_search_event_seed.json), all six source URLs preserved; it does not reproduce source long text or full algorithms.
- [P5 deterministic evidence-grade verifier](../../scripts/cuberev-021/verify-p5-fmc-retrospective-process-evidence.py) checks schema, exact case/event counts, author-report timing grades, candidate-count units, chronological monotonicity only of author-reported Wheeler milestones, distinction between written and tried candidates, and removal of another author from original cognition.
- [P5 **external GitHub Actions SUCCESS** run #38044689958](https://github.com/WhoSia/CUBE-REV/actions/runs/38044689958); [machine receipt artifact #11667277023](https://github.com/WhoSia/CUBE-REV/actions/runs/38044689958/artifacts/11667277023), SHA-256 `7d72f5b0c78a76a6d6ae8c5c4881e37182489cc7c02c3f4df1a8a6324c2b0534`.
- **What P5 CI verifies:** internal event ontology, numerical extraction consistency and refusal to claim audiovisual timing. **What P5 CI does not verify:** full content of remote webpages line-for-line, that personal narrative really captures all considered branches, behavioral causal effects, private 451-source corpus, or any new real-person data.
- The pre-existing P7 active-set audit CI failure is legacy allowlist/governance, not evidence against the new P5 event-grade check; do not silently edit unrelated historic state.

## 7. What to attack next with the existing evidence

The scientifically useful next step is not to re-run ideal feedback Bellman simulation and then ask humans to perform it. It is to **represent the reported actual search path as a partial-order action/candidate graph** and test what is identified:
- **Branch availability:** authored candidate written versus actually evaluated; the missingness mechanism is informative.
- **Revisit:** whether a candidate was returned to, and which exact source text supports that ordering.
- **Action selection under constraints:** subjective time allocation and backup management are author reports unless a session clock exists.
- **Future model comparison:** memory/history-aware versus candidate-quality-heuristic versus explicit time-pressure decision policies only if independent sessions with matched task conditions become available.
- **Mathematical return:** formalize the minimum state variables needed to reproduce *observed* search decisions, not hypothetical internal options. Do not prematurely treat self-report DAG as full interactive trace.

**P5 CLOSED as bounded evidence retrieval + transparent ontology sample / HUMAN-PROCESS TIMESTAMP, CAUSAL MODEL, AND VIDEO GROUND TRUTH HOLD.**
