# CUBE-REV R14-P8.17 — Unified Manuscript Referee Gate

Date: 2026-11-10. Scientific-editorial audit, not publication acceptance or novelty certification.

## What exists now

One C0.1 single-paper working manuscript is saved at papers/0.28/ONE_PAPER_EXACT_RUBIK_IDENTIFICATION_CONSOLIDATION_C01.md. The A D0.5 and B D0.8 source papers are preserved without modification/deletion. Main A theorem: exact radius-six tagged-cubie 16-sensor minimum and 156 positive layouts; corollary 432 minimal layouts, orbit and selection results, all conditional on inherited P48 physical certificates. Main B theorem: full-group two-categorical-facelet preset minimum 21 and adaptive whole-cube upper 20, unrestricted lower 18; h_adaptive exact value open. The A and B state sets, observation outputs and cost units differ, so NO claim of a numerical comparison or shared optimality theorem.

## Gate for one-paper editorial coherence

1. Keep a single intellectual question: exact original-state identification under two precisely defined legal Rubik observation regimes. Generic pair-cover and Bellman equations are established theory, not novel claims.
2. Do not claim tagged cubie 16 sensors versus two six-color facelet 20 frames are commensurate or that B follows from A. Avoid human cognition and RGB robot performance inference.
3. Every claimed figure must be explicitly scoped and tied to actual code, physical cube verifier, exact historical distance/route data and independent reproduction. One hundred examples do not prove a whole-cube theorem.
4. The 16/156 physical radius-six result is the strongest current publication-ready direction, subject to source custody and external priority checks. The 21-vs-20 strict adaptive gap is a second independent theorem but a venue reviewer may find it intellectually separate.
5. If external referees see no meaningful single contribution spanning two channels, prefer a condensed A-centric single submission with B held as an independently maintained research result, rather than an arbitrary 2-paper split or a forced merge.
6. Preserve all original separate proofs in git and raw bytes in Drive until C0.1 has a grounded acceptance review; editorial merge is not epistemic erasure.

## New exact six-state bridge, independently executable

New script scripts/cuberev-observation/audit_r14_p817_common_observation_bridge.py defines states A0,A1,A2,B0,B1,B2 and three ternary queries. q0 distinguishes A versus B; q1 distinguishes A0..2 and is constant on B; q2 distinguishes B0..2 and is constant on A. All 15 pair-separation supports are nonempty. Complete static set-cover enumeration proves minimum 3 preset queries, whereas Bellman AND-OR minimax and an explicit conditional decoder prove 2 adaptive queries. A separate local Python implementation confirmed 3 and 2. This is a generic illustrative example, NOT a Rubik theorem.

New formal/028/StaticObservationSupport.lean states the exact standard equivalence between injectivity of all selected observations and hitting every pair's difference support. It is a third target in formal/028/lakefile.toml; the read-only GitHub Actions gate now also tests the six-state example. No installed local Lean compiler or observed remote kernel SUCCESS: keep SOURCE_PENDING_KERNEL, do not claim that syntax alone is a certified proof.

## Verified relevant prior work

Moore (1956) experiments, Lee & Yannakakis (1994) identification, Türker–Ünlüyurt–Yenigün (2016) minimum-cost ADS doi:10.1016/j.infsof.2016.02.001; Soucha–Bogdanov (2020) splitting tree doi:10.1016/j.infsof.2020.106297; Hierons–Türker (2016) noncommunicating distributed ports doi:10.1093/comjnl/bxw004; group bases Bailey–Cameron (2011), Cameron–Fon-Der-Flaass (1995), Dalla Volta et al. (2024). These are owned or verified primary references. Search-negative for an identical cube theorem is not proof of novelty.

## Next scientific priorities rather than extra literature bureaucracy

1. Replay physical 41-class B12 positive target proofs and 872 support masks with original P48 bytes/SHAs and an independent source path. Record exact successes and blockers.
2. Rerun entire canonical 609,376 conditional edge family of Paper B and physical route checker including exceptional parity timing, not just example random states.
3. Obtain actual Lean kernel verdict; instantiate legal finite cube geometry and 66-pair certificate index, avoiding unproved physical numerical assumptions.
4. External referee evaluation for C0.1 unity: if two theorem proofs are only juxtaposed and no common scientific inference is made, one concise A-focused paper is the stronger choice.

Decision: use C0.1 as one-paper candidate, keep A and B intact as source history, and focus substantive next effort on physical reproduction and exact formal proof bridges.
