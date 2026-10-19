# CUBE-REV 0.27 — P7: Exact Goal-Side Parent BFS and 17HTM Witness Extraction

**Result classification: real standalone physical test PASS; real source-depth11 integration COMPILES; no actual WCA 17-move solution found.**

## Demonstrated physical case
Recomputed the original whole-cubie solved B6, 8,240,087 states, BFS depth histogram [1,18,243,3240,43239,574908,7618438], and retained every reached full state with parent index and generating move. Select the actual previously independently 54-sticker-verified WCA 18HTM solution and take its first 12 moves. Look up the whole physical resulting cube state in the solved B6. Walking the goal-ball parent chain reconstructs a valid 6HTM solved tail **7 1 13 0 8 4**. Concatenate and independently replay all 18 moves on the original scrambled full 54 sites: solved exactly. All executed to completion in new C++17 executable `p7_goal_suffix_extractor.cpp`, log `P7_EXECUTION.log`.

## Real source-depth11 engine integration
Changed the authentic physical C++ P6 depth11 DFS to hold a `Packed -> index` goal map and a complete parent-pointers table. An exact B6 encounter at depth11 now reconstructs a suffix of length <=6, concatenates actual source DFS path to form a candidate of length <=17, verifies each full 54-facelet sticker position, and only then emits `P7_VERIFIED_FULL_54_SITE_17HTM_WITNESS`. Fail-closed throw on invalid words. The integrated `p7_depth11_witness_ready.cpp` was compiled with `g++ -std=c++17 -O3 -fopenmp`; it was NOT run through any full actual root sector, and there is no new original 17HTM witness. Previously P6 root14/second1 depth11 timeout remains INCOMPLETE.

## Reproducible local P7 package
`/mnt/data/cuberev027_p7/P7_EXTRACTOR_AND_DEPTH11_WITNESS_READY.zip`, SHA256 **0341e8a5a7038e7717c40eb61f6e1c2d9e8e977c9bb8d609752034e34e0624c6**. Includes original P11 physical header, standalone complete B6 parent court, actual execution stdout, integrated P7 depth11 solver, source patch script, detailed report and per-file SHA manifest. This is current-session T0 only, not Drive T2. The source-depth11 search remains algorithmically and computationally open and is not claimed to be completed.

## Next obligatory tests
1. Controlled injected known depth11 physical meet test from a different known-length<=17 scramble, NOT the original WCA target, to exercise exactly 11+6 extraction with a genuine solved suffix.
2. Checkpointed prefix-partitioning and per-job fail-closed counts/prune accounting for source-depth11 full 17-exclusion (resource feasibility).
3. Globally different constructive 17HTM DR/NISS search families, not more local neighborhood edits.
4. Once true original source 17HTM meet, independent 54-site replay + canonical exact outcome before claiming d=17.

CUBE-REV 0.27 conditional external lower bound 17 and actual 18 upper bound retained; exact distance **still undecided between 17 and18**.