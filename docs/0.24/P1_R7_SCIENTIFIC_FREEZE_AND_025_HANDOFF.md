# CUBE-REV 0.24 P1-R7 — Scientific Freeze of Physical Solver Architecture & Audited Handoff to Generation 0.25

**Decision (2026-10-12): 0.24 SCIENTIFICALLY CLOSED / SOURCE-FROZEN; 0.25 user-authorized to activate.** Freeze means a stable, falsifiable research baseline with explicit unresolved claims, NOT proof that every 0.24 research question or every whole-cube optimum is finished. Preserve original P0–P1-R6 source and historical errors; amendments remain possible only as explicitly versioned errata, not stealth retroactive correction.

## 1. Actual Rubik's Cube, not an arbitrary graph proxy

The immutable public test state is the original fixed-center legal full 3×3 cube after WCA Seoul Summer 2026, 3×3 Final A Scramble 1:

    R' B' F2 D2 F2 L2 R2 U' F2 L2 D2 B2 D F L' R2 B U2 F2 R2

An actually legal original 54-sticker complete solution of exactly **18 HTM** has been independently reproduced:

    F U F D' R' F' L' F' D' L B L2 F2 U2 L2 U F' R2

[Physical source-original NISS dual-side 18-word generator / independent original 54-sticker replay](P1_R5_R1_WCA_REAL_18HTM_NISS_CONWAY_GROUP_CERTIFICATE.md). The machine-discovered word came from real q=F R2 two-premoves, physical DR entry after 11 moves, a 6-move exact DR-subgrammar suffix, and the true cube group interface F2*F = F' shrinking a raw 19-turn program to 18. It is not an observed player solve.

What 0.24 learned mechanically: phase1 DR shortest arrival alone is not a good predictor of whole-solution length; the selected FULL cubie phase-interface state and genuine legal group-word normalization determine subsequent cost. Changing original physical DR axis affects restricted subgroup programs even though it cannot change the unrestricted true full18HTM distance. Ordinary two-phase, IDA*, PDBs, NISS, commuting disjoint faces and basic group identities are inherited prior art, not newly invented algorithms.

## 2. Audited proof-grade frontier at the moment of closure

[Original unrestricted full18HTM entire-cube P1-R6 proof report](P1_R6_SOURCE_COMPLETE_FULL18_GLOBAL_BIDIRECTIONAL_CERTIFICATE_AND_025_GATE.md) supplies the currently proven bound:

    14 <= d18(s) <= 18

- UPPER BOUND 18: actual source + legal full-cube 18-turn word returns all original 8 CP/CO and 12 EP/EO cubies and all 54 facelets to the fixed solved frame. Original physical C++ and separately programmed Node source replay PASS.
- UNRESTRICTED LOWER BOUND 14: enumerate exact WHOLE-cubie 18HTM goal radius6 ball, **8,240,087 distinct full states**, and all normal-form source words of length<=7, **120,213,368 iterative-deepening recursive entries** (NOT distinct source states). Intersections: **0**, all bounds completed, no resource cutoff. Thus NO unrestricted full-cube solution of length<=13. Original-state comparison uses a reversible full CP/CO/EP/EO two-word key, not hash-only equality, and only admissible same-face and opposite-face word normalization. This does not require visiting DR or any chosen phase.
- INDEPENDENT WEAKER REPLICATION: separate Go construction of original physical 54 facelets independently evaluates entire physical source radius5 and goal radius5, no intersection => unrestricted lower11. The Go result is not falsely promoted into independent lower14.
- ACTUAL EXTERNAL CI SUCCESS: [P1-R6 Actions complete run 38210864083](https://github.com/WhoSia/CUBE-REV/actions/runs/38210864083), source head 2aaf34e3e56df29244beebc6f423fe651a3bf934: full C++ global radius6+7, Go original facelets 5+5, Node real 18-word source replay, bot-author gate and read-only checkout all PASS.
- REPAIRED HISTORICAL CI: P1-R3 YAML had been syntactically damaged; the broken zero-job Actions were historical workflow defects, not failed cube proof. [Corrected P1-R3 whole-cube original-source 21/19/9/9 regression](https://github.com/WhoSia/CUBE-REV/actions/runs/38211534949) PASS. Prior failed run records remain visible.
- LOCAL HARDWARE-GRADED RECEIPT for P1-R6: final original C++17 full radius6+7 run 81.59 s wall time, 653,964 KiB resident peak (~639 MiB); not a benchmark of all machines.

**OPEN AT FREEZE:** actual unrestricted existence or absence of valid 14–17-move solutions; specifically whether the verified 18-word is globally shortest. A true d18>=18 certificate would have to eliminate all real <=17 words; subgroup-only enumerations (even billions of recursive calls) cannot discharge that obligation. No optimality status fabricated.

## 3. Original-source human FMC and speedcubing science

0.22–0.24 inherited the actual documented human-written FMC Miao/Riabov source programs and true original cubie endpoints. Differently spelled authorized words may reach the SAME physical state, and NISS/source parse uncertainty must remain source-specific. The public authentic FMC main DR endpoint exact nine-HTM suffix was already proved in 0.22 and reproduced in 0.24, not double-counted as novelty or as a competitor's submitted full solution. Source-literal uncertainty on Riabov Other #2, prior conditional 2×2 rotation-y2 issue, and protected private 451 human-authored reconstruction trajectories retain original scope/holds. Previously maximum-conditioned human observational key support fell to zero; that is no evidence for causal effects or particular mental processes.

Speedcubing 0.24 independently calculated original WCA Cross distances, but an exact four-edge Cross alone is NOT a performance or human-cognition result. Actual original physical Cross-preserving Cross→first F2L continuation and recorded time-stamped legal move events are testable 0.25 mechanisms. Video AI is optional measurement technology, not a substitute for actual move telemetry or for a model of internal strategy. Confirm license, rights, participation/source provenance and sampling before reading/publishing any human traces.

## 4. Scientific errors and negative experiments retained, not erased

- The original P1-R3-R1 declaration that every phase1 depth through13 had been scanned was incorrect. With source admissible h=7 and executable min(13,h+4), the true prior horizon ended at11. Corrected scientific documents maintain the original counts as depth<=11 evidence. The original 12+8 raw20-to-19 actual cube witness exposes the error.
- The source inverse20 was always an exact upper bound for a 20-turn original WCA scramble. A generated 21-turn solution was a legal whole cube solver but a WORSE incumbent. P1-R4 improved to real19; P1-R5-R1 improved to real18. Do not advertise 21 or 19 as present optimal or best source solution.
- DR-bounded unsuccessful raw, trace-closure and one-/two-premoves NISS experiments have explicitly specified source transformations, first-entry depth, output grammar, completion and caps. NONE prove nonexistence of shorter unrestricted full18HTM cube solutions.
- The attempted harder phase1 LR depth14 encountered a two-billion recursive-call resource cap and is explicit PARTIAL RESOURCE HOLD, never a negative proof. Global B6+B7 proves only <=13 exclusion.
- Zero independent human support at high matching and source-incomplete source frames remain carried-forward epistemic boundaries; they do not change actual mathematical cube distances.

## 5. Handoff rules to formally active 0.25

0.25 is **not** the claim that 0.24 solved global geodesic optimality. The user explicitly approved the new full formal name and asked for its opening after this P1-R7 close. At 0.25 opening establish exactly three physical-science priority lines:

1. **Global geodesic proof frontier on the same original whole cube:** prove or falsify d18>=18; source-complete coset/PDB/bidirectional frontiers with independent checker and resource-scaled certificates, plus any strictly shorter original full 54-facelet 17-word witness.
2. **Executable physical solver program synthesis:** actually implement and benchmark whole-cubie move grammars, full-state quotient soundness, exact stage interface cost, PDB admissibility, memory/time on source-independent real original states and WCA/FMC held-out targets. Prove branch elimination does not remove the actual shortest legal word.
3. **Physically grounded speedcubing / human FMC falsification:** exact Cross→F2L actual cube continuation, authored FMC program predictions and, when source rights permit, direct time-stamped smart-cube move logs. No fabricated human behavior from algorithmic words.

Each hypothesis must specify legal generator set and HTM/cost contract, original full cubie source state, proof grade, independent verifier, hardware/time/memory caps and a named adversarial falsification case. Do not use research governance, pure graph relabeling, or administrative monitoring as a substitute for actual Rubik cube innovation.

**Handoff outcome:** 0.24 remains immutable scientific predecessor, 0.25 starts with the EXACT inherited interval **14<=d18(s)<=18** and its certified source code. Author/committer ONLY human WhoSia; github-actions[bot] and github-action[bot] are prohibited contributors; GitHub Actions contents:read and no workflow writeback. P7 active-set manifest records new approved file paths with exact Git blob SHAs. The release of 0.25 requires no source deletion and does not erase 0.24 failure reports.
