# CUBE-REV 0.25 P0-R6I-P12-P1/P2 — Original Exact Duplicate-Fiber Relative Cycle and Twist-Balance Research Log

**Status 2026-10-16: DEVELOPMENT/EXTERNAL CI PENDING.** This is a stepwise research source and a prospective physical reproducibility contract, NOT a claimed new 576-pair fine-cycle census or a Lean kernel PASS. [Notion 0.25 canonical lab record](https://app.notion.com/p/3f7ef561cf9281ae8e94c46e9f916fdc).

## Motivation and certified predecessor
P11 physical external Actions #38836422743 actually rebuilt original WCA 54-facelet goal B6 with 8,240,087 whole CP/CO/EP/EO entries and exact domain-separated SHA256 82fe545bcad3537c989ec22afce9d286926ddce5f4ef9428c0307951ec2d0979. Exactly 1,405,068 corners have nonempty edge support; 1,404,492 distinct literal edge fibers occur; 576 distinct fiber classes are exactly duplicated. Physical four coarse classes (edge-support fiber cardinality / differing CP positions / differing CO positions / pairs): (1/6/2)=96; (1/6/4)=96; (4/4/0)=256; (4/4/4)=128. All 576 pairs have equal CP parity; 0 are related by one or two legal actual 18HTM corner moves. These are P11 results, not new P12 measurements.

## P12 mathematical refinement
For corners x,y, relative CP permutation delta = inverse(CP_x) composed with CP_y. Equal parity of CP implies delta is even. An even permutation of 8 positions moving exactly 4 positions has nontrivial cycle type (2)(2); one moving exactly 6 has (3)(3) or (4)(2). For CO differences Δ_i = CO_y[i]−CO_x[i] mod3, sum Δ_i=0 mod3. Hence exactly 2 differing positions imply (+1,−1); 4 imply (+1,+1,−1,−1). These necessary laws do NOT determine the empirical numbers 576,96,128,256 or prove a cube group orbit explanation. No source-fixed cube symmetry or canonical-DFA proof transport is asserted.

## Reproduction contract, trust boundary and negative controls
- The new Go source streams the 131,841,392-byte original B6 file, validates strict (corner,edge) sorting and exact content SHA, then groups complete sorted edge-support binary lists by LOSSLESS equality (not digest-only). It asserts the established 1,405,068/1,404,492/576 coarse totals and counts all true cycle types and signed CO differences. It must never print invented fine-cycle counts when the original goal file is absent or corrupt.
- The new read-only Actions workflow reconstructs B6 via inherited original 54-sticker/P9 native physical C++17 and separately runs Go classification; tampered goal bytes must be rejected.
- Lean RelativeCornerCycleConstraints.lean uses the kernel-side omega arithmetic to state four CONDITIONAL numerical necessity lemmas. Fin 8 / Equiv.Perm cycle-construction bridge, actual CP/CO physics interpretation and Lean end-to-end C++ correctness remain OPEN; Lean build until independently seen is PENDING.
- Physical compiler/goal SHA failure, Go mismatch, incomplete 576 pair ledger, Lean compile failure, or missing provenance all result HOLD/FAIL and never upgraded scientific claim.

## Governance and history
Active branch research/current only; GitHub commits must be authored+committed by WhoSia; no Actions bot authors, commits, pushes or source writeback. Jobs use contents:read and persist-credentials:false. Existing P10 exact-fiber gate was +6.8407% SLOWER in the measured source10 benchmark: no speedup inference from this classification. Original 18HTM distance still 16≤d18(s)≤18, first-action B10 cylinders completed {0,3,9,12}; 14 remain OPEN and global lower17 UNPROVED. All pending and failed results are preserved in Notion as they happen, not concealed until PASS.
