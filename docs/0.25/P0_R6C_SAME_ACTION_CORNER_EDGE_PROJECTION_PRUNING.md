# CUBE-REV 0.25 P0-R6C — Same-Generator Synchronization of Exact Corner and Edge Goal Projections

**Stage: SOURCE IMPLEMENTED, EXTERNAL ACTIONS AND COST RESULTS UNVERIFIED.** Parent stage P0-R6A uses only the exact one-step corner envelope; P0-R6B tries full source B8 against target B6 for a potential actual lower15. P0-R6C is a third **independent physical search-design hypothesis** evaluated on the identical WCA Seoul Summer 2026 Final A1 complete 3×3 cube, all 18 outer-face HTM legal moves, exact 54-sticker sourced transitions and full CP/CO/EP/EO equality.

## Theorem: an identical generator must satisfy both projections

Let G be the original full physical fixed-center cube state graph, T=B6(e) the EXACT full cubie solved-side ball, and π_C, π_E be exact reversible corner and edge projections. Define C=π_C(T) and E=π_E(T). For source-side state x and actual legal generator a∈A, a necessary condition for x a∈T is simultaneously

    π_C(x a) ∈ C   and   π_E(x a) ∈ E.

Crucially, **the same actual generator a** must satisfy both predicates. Thus for the set of canonical last moves A_last(x), if no a∈A_last(x) satisfies both then no allowed immediate child can meet the goal ball. Every rejected a has a full-cubie state provably outside T; a candidate passing both tests still requires exact full CP/CO/EP/EO equality, since the two independently projected ball images can contain incompatible corners/edges.

This test is sound without assigning fractional operator costs. It is structurally stronger or equal in rejected last-layer children to the P0-R6A C7-envelope screen because any candidate with π_C(x a)∈C automatically implies π_C(x)∈the exact one-step backward envelope. Conversely C7 membership by itself does not require one common action meeting the edge projection. Improvement for THIS source is empirical, not stipulated.

**Not claimed:** a full joint corner-edge exact shortest-distance PDB, an additive PDB theorem, a source-general hardware speedup, human speedcuber behavior, or global lower15 without fully completed source B8 + target B6 disjointness.

## Executable proof obligations and hierarchy

1. [C++17 exact same-generator solver](../../scripts/cuberev-025/p0_r6_joint_next_action_cpp/main.cpp) imports the existing physical P0-R6A kernel under a main-as-library guard; the original P0-R6A standalone executable is unchanged in behavior. The solver builds exact goal corner C and exact goal edge E from all complete-cubie keys in the same actual B6(e), and retains P0-R6A C7 for cheap early negative checks.
2. At penultimate-depth nodes, if the exact one-step C7 envelope rejects the current parent, count ALL omitted canonical children. Otherwise simulate each genuine legal original-cube move, inspect the successor full key's corner part, and then (only after corner membership passes) its exact edge part. Reject individual children when either necessary projection predicate fails; visit surviving children and test complete-cubie goal membership as usual. At earlier depths do NOT drop a parent based on this one-step predicate.
3. C++ source completeness checks **N_R = actual visited recursive calls + skipped immediate canonical children**, where the independently counted old unpruned iterative DFS baseline is N7=120,213,368 for the historical original physical source B7, or N8=1,604,664,504 for future source B8.
4. An independent [Go audit executable](../../scripts/cuberev-025/p0_r6_receipt_go/main.go), invoked as \`--joint P0-R6A.log P0-R6C.log\`, checks exact baseline, preserved original full B6, zero full-cubie intersections, and that R6C omitted **no fewer** children than R6A before comparing wall seconds and maximum RSS.
5. [Read-only two-job CI](../../.github/workflows/cuberev-025-P0-R6C-joint-same-generator.yml) separates a **fast small-radius C++17 compile + Go compile + original physical 54-sticker smoke test** from a subsequent **full B6/B7 matched runner comparison**. If the quick job fails, no expensive full run starts. Both jobs reject GitHub bot contributors, checkout without persistent credentials, permissions \`contents:read\`, and refuse repository writeback.

## Scientific interpretation

Let N_A and N_C be old corner-only and new joint-next-action source recursive visits. On an uninterrupted common B6/B7 test with no whole-cube intersections, both are accounted against the **same** normal-form N_base=120,213,368. Thus the **additional actual last-layer eliminated visit count** is N_A − N_C, which should be nonnegative. This is not the fraction of runtime saved. New E projection materialization and 18 generator tests can increase wall time and resident memory even when N_C<N_A. Failure to achieve wall/RSS benefits is a valid negative solver-engineering result and must be retained.

Test the full source B7 before expanding R6C to B8. The existing B8 P0-R6B remains an independent complete-cube lower15 attempt and should not be misreported as already verified. On any resource timeout, uncaught exception, missing log, or found original full-cubie intersection the relevant original lower bound is **not** certified by that run. Prior lower14 from older independently completed P1-R6 and P0-R5 remains established.

## Parallel research programme

- **Track A — CI/benchmark:** P0-R6A old-v-new exact last-layer pruning; both time and peak RSS on a common runner.
- **Track B — full mathematical distance:** P0-R6B B8(source)/B6(goal) exact no-intersection attempt for the *open* lower15.
- **Track C — noncommutative information:** this P0-R6C same-action corner+edge constraint, tested on the SAME original source, not a new synthetic substitute.
- **Track D — independent proof audit:** Go recurrence of complete canonical frontier, separate original 54-sticker replays and longer-term Lean proof of abstract one-step/pair-filter soundness. Do not claim a Lean kernel proof before an actual successful external build.

**Evidence state at document creation:** C++/Go programs and GitHub read-only workflow committed; matched original B7 full run, exact corner/edge projection cardinalities, additional skipped children, real wall seconds, real peak RSS, full source B8, and lower15 are all **UNVERIFIED**. No numerical results were fabricated to fill pending CI slots.

## Repro commands

    g++ -std=c++17 -O3 -Wno-return-type scripts/cuberev-025/p0_r6_joint_next_action_cpp/main.cpp -o /tmp/p0r6c
    /tmp/p0r6c 3 3 90
    /usr/bin/time -v /tmp/p0r6c 6 7 1000
    go run scripts/cuberev-025/p0_r6_receipt_go/main.go --joint /tmp/r6a.log /tmp/r6c.log

Use full measurements only from completed logs with exact commit/toolchain/runner identity. The tiny synthetic finite group sanity check is merely a mathematical counterexample/implementation aid, never a stand-in for a real cube certificate.


## Quantifier-order counterexample and limitation of the noncommutative label

The important advance is synchronizing **one identical action**, not yet a theorem about noncommuting word order. In particular, an abstract, completely commuting test system already separates the two logical forms

    (exists a: cornerPass(a)) and (exists b: edgePass(b))

from

    (exists a: cornerPass(a) and edgePass(a)).

For an explicit finite counterexample, take states (c,e) in Z/3Z × Z/3Z, legal moves +(1,1) and −(1,1), and full target T={(0,0)}. From x=(1,2), the + move reaches (2,0) and meets the *edge* projection of T only, while the − move reaches (0,1) and meets the *corner* projection only. So both separately existential one-step tests pass, but there is NO single legal generator jointly passing both. This demonstration was also checked in a standalone locally executed Go exhaustive finite-state toy search. **It is a counterexample to a logic mistake, NOT a real-cube benchmark or performance result.**

True Rubik's-cube noncommutative **word-order** synchronization needs to couple two or more legally ordered generators and retain enough information to distinguish \`ab\` from \`ba\` when those moves do not commute. P0-R6C does not yet do that; treat it as the first joint-generator predicate before the stronger multi-action programme. The physical original-cube C++17 experiment remains essential.
