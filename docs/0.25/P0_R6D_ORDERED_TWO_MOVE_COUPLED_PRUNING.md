# CUBE-REV 0.25 P0-R6D — Ordered Two-Turn Corner–Edge Synchronization and Source-Complete Subtree Accounting

**CURRENT: original C++17 physical B7+Go paired C/D Actions SUCCESS #38518256469; this early status sentence is preserved as the superseded preflight hypothesis.** Do not call this a new lower bound. Inherited original WCA Seoul Summer 2026 3×3 Final A1 physical 18 HTM source remains **14≤d18(s)≤18**. All 54 original stickers, complete CP/CO/EP/EO and original 18 HTM move maps remain mandatory.

## Original question and genuine mathematical improvement

R6A excludes direct children at the one-move boundary using a goal-side complete-corner envelope. R6C tests one actual generator against **both** exact goal B6 corner and edge projected images. R6D advances one whole **ordered physical generator pair** earlier: for a source prefix x with exactly TWO remaining legal HTM moves in its complete canonical DFS, consider each legal first generator a and all canonical second generators b.

Let T=B6(e) be the exact complete-cubie solved goal ball, C=π_C(T) and E=π_E(T). A first-action subtree rooted at xa can be discarded if BOTH conditions hold:

1. xa fails the jointly necessary condition [π_C(xa)∈C AND π_E(xa)∈E]; AND
2. For EVERY legal canonical second action b, xab fails [π_C(xab)∈C AND π_E(xab)∈E].

All actions are the SAME original physical actions in both cubie projections, and **the order a,b is preserved exactly**. There is no abstract commutative face histogram. The two-turn rejection holds for any subgroup or full-state goal T when both projections are true necessary images, without assuming that their joint membership is sufficient for full-cube membership. Every retained candidate remains subject to full exact complete-cubie equality.

## Proof of safety and complete-cover accounting

If any full-cubie one-action child xa belongs to T, the defining projection implication forces BOTH exact projected membership tests in (1) to hold. Similarly, if some canonical two-action successor xab belongs to T, (2) must fail for that SAME ordered pair. Hence a subtree satisfying both negative conditions contains NO full T intersection at depths one or two. The current prefix x itself is always checked for exact T membership BEFORE attempting any subtree rejection. Earlier source levels beyond two remaining moves are explored normally, and remaining-one levels reuse the older proven-necessary R6C tests. Source-canonical completeness relies on the unchanged full original 18 HTM normal form, inherited from P1-R6.

A skipped first-action subtree consists of the first child (one recursive DFS call) plus EVERY canonical second-action child that could have been visited beneath it. Thus for source bound R, the new C++17 implementation counts

    SKIPPED_CANONICAL_CALLS += 1 + |{b : canonical(a,b)}|

for each whole two-step first-action subtree it eliminates. Reused R6C last-layer checks count individual omitted terminal calls. A separate purely combinatorial recurrence counts all unpruned canonical recursive calls for iteratively repeated source depth limits 0..R. Its exact audit condition is

    BASELINE_CANONICAL_CALLS = ACTUAL_VISITS + SKIPPED_CANONICAL_CALLS.

This is stronger bookkeeping than counting only the number of rejected first actions. Inherited values: R7 baseline=120,213,368 and R8 baseline=1,604,664,504; these are repeated recursive CALLS, not distinct physical cube states. Counting equality plus theorem proof guarantees that **every omitted call is accounted for**, conditional on exact legal move physics and the correct goal projections.

## Actual physical implementation, status and risk

[Original physical C++17 R6D solver](../../scripts/cuberev-025/p0_r6_ordered_two_turn_cpp/main.cpp) reuses [C++17 R6C](../../scripts/cuberev-025/p0_r6_joint_next_action_cpp/main.cpp) under a guarded main-as-library compilation route; it reuses R6A/P1-R6 original fixed-center 54-sticker-derived turns. Physical independence is NOT claimed for these inherited turn tables. The executable directly checks the original WCA source's 54-sticker representation and known 18-move solution, verifies the original physical full-cubie words U F and F U have different endpoints, and builds exact full-cubie goal B6 together with its exact C6/E6 projections.

For each source node with remaining depth=2 it considers canonical a; as a cheaper early negative it first checks whether xa lies outside the exact one-step corner envelope C7, which excludes both direct and a subsequent terminal corner match. Otherwise it checks actual ordered successors xab only until the first possible joint projection match. If no match, skips the full first-action subtree. This may consume MORE CPU than R6C despite visiting fewer states. It also adds counters for first-action branches, exact skipped canonical recursive calls, candidate branches, tested ordered pairs, and projected successes. Any resource expiration returns typed HOLD, and any real complete-cubie intersection suppresses a claimed lower bound.

**Potential algorithmic limitation:** this is bounded ordered two-turn conjunction of separately projected goal sets, NOT a complete-coupled corner/edge exact-distance PDB, NOT source-general runtime dominance, and NOT a lower15 certificate by itself. A full B8/B6 disjointness proof or actual shorter whole-cube witness is still required.

## Independent finite unit test performed locally

To falsify unsafe projection pruning in an independent finite construction, built and executed a standalone C++17 test on S3×S3 permutation-pair states with two genuinely noncommuting legal generators. The full goal was the identity pair. Exhaustively checked 36 possible state pairs × two choices of first move = **72 first-action cases**. The necessary projected two-turn logic rejected **66 cases**; it rejected **zero** cases where the exact full-goal state was reachable in one or two actual ordered moves. All 36 starting states had the two move orders distinct. The test needed a local compile correction for the identifier name (a user-defined rank conflicted with std::rank), and a sharper singleton target to exercise nontrivial rejection. Final command compiled with g++ -std=c++17 -O2 -Wall -Wextra -Werror and passed. These finite-test numbers are NOT physical Rubik cube pruning results.

## Experiment design — remove dependence on slow Actions

[Two-job read-only R6D CI](../../.github/workflows/cuberev-025-P0-R6D-ordered-two-turn.yml) separates a low-cost 3+3 actual original physical smoke test (C++17 R6C and R6D plus Go compiler) from a matched original physical B6/B7 full benchmark. The second job starts only when the first succeeds, uses the SAME runner for comparison of C vs D, records GNU /usr/bin/time wall seconds and maximum RSS (KiB), and saves logs as 30-day diagnostic artifacts even on failure/HOLD. No CI job has Git write permissions or writes a commit.

[Separate Go receipt verifier](../../scripts/cuberev-025/p0_r6_receipt_go/main.go) now supports --ordered R6C.log R6D.log. Requires the actual original C and D complete-cubie B6 target size 8,240,087, corner projection 1,405,068, zero true intersections, exact 120,213,368 total canonical call ledger for both, and D skipping at least as many calls as C. Outputs measured A/B comparison only when both wall/RSS values exist in completed logs. A failed job, resource timeout, uncaptured log, or missing run ID cannot be silently translated to success.

The public GitHub Actions run page could not be fetched through available page access; the current GitHub connector lists only PR-triggered commit runs, not the needed push runs. Thus actual run IDs/job IDs and **actual original full-cube C-vs-D quantitative savings remain OPEN**; no fictional numerical improvements are filled in.

## Reproduction and scientific progression

    g++ -std=c++17 -O3 -Wno-return-type scripts/cuberev-025/p0_r6_ordered_two_turn_cpp/main.cpp -o /tmp/p0r6d
    /tmp/p0r6d 3 3 100
    /usr/bin/time -v /tmp/p0r6d 6 7 1000
    go run scripts/cuberev-025/p0_r6_receipt_go/main.go --ordered /tmp/r6c.log /tmp/r6d.log

Proof scope hierarchy: R6A one-step corner-only → R6C one shared physical action corner+edge → **R6D ordered two-action subtree elimination** → OPEN: stronger joint projection, reusable two-turn backward tables and source-general deep prefix coverage. In all phases preserve human-author/committer WhoSia, no github-actions[bot] or github-action[bot] contributors, read-only CI, and private 451 human original recordings out of public research code.


## Completed original physical external run and measured negative cost result (2026-10-14)

**The opening-era UNVERIFIED note above is now superseded for B7 by actual completed [GitHub Actions #38518256469](https://github.com/WhoSia/CUBE-REV/actions/runs/38518256469).** Both quick original 54-sticker B3+B3 C++17/Go compile/smoke and the full original physical B6(goal)/B7(source) same-runner C-vs-D job were independently observed as completed SUCCESS. The compiled code is real physical C++17, the measured comparison is a single GitHub runner experiment and the result is checked by the independent Go receipt auditor.

- Baseline exhaustive *unpruned* iterative 0..7 canonical calls: **120,213,368**. Full true solved-side B6 states: **8,240,087**; projected corner6 **1,405,068**, expanded corner7 **6,807,696**, projected edge6 **7,672,278**.
- P0-R6C common single-action: **9,005,784 actual recursive calls**, **111,207,584 omitted**, wall **20.01 s**, peak RSS **1,340,256 KiB**.
- P0-R6D **ordered two-action**: **674,679 actual recursive calls**, **119,538,689 omitted**, wall **20.00 s**, peak RSS **1,341,068 KiB**.
- R6D extra omitted relative to C: **8,331,105 recursive calls**, or **92.508381% fewer actual recursive visits** than R6C (but essentially **0.05% less wall time**, within the noise of one comparison). D ran **7,462,988 actual ordered pair candidate checks**, with 8,331,105 first-action subtree rejections and exactly 5 projected pair passes.
- Both full-cubie intersections **0**. Go audit prints **P0R6D_GO_AUDIT_PASS**, checks independent exact source partition against baseline 120,213,368, and reports signed time/RSS changes. Source-only B7 regression therefore reproduces **global lower14**, already surpassed by independently certified R6B B8 **global lower15**.

**Falsifiable interpretation:** R6D materially reduces DFS visits but yields *no useful wall-time improvement* against C under this particular runner and source because physical ordered-pair checks and materializing both exact projections consume overhead. Peak RSS remains approximately unchanged relative to C. The next optimization target is reusable ordered-pair support masks, cache keys, precomputation/cost accounting, or a stronger full cube potential that reduces the number of expensive pair expansions. Never call a 92.5% search-visit reduction a 92.5% wall-time speedup, and never advertise new lower16 without a completed original B9/B6 source-complete certificate.

**General Lean4 soundness lemma now ACTUALLY KERNEL BUILT:** [P0-R6C Lean Actions SUCCESS #38517271238](https://github.com/WhoSia/CUBE-REV/actions/runs/38517271238), with five-job Lake build completed. This establishes an abstract common-action necessary condition, not the full empirical C/D or whole-cube B8 proof.
