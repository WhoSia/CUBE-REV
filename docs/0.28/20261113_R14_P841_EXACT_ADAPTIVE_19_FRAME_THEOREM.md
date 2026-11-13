# R14-P8.41 — Exact adaptive identification in 19 frames

On the fixed-center legal 3×3 cube, the optimal worst-case adaptive budget is **19** paired color frames. The fixed budget is **21**. P8.40 constructs a 19-frame policy. P8.41 excludes every 18-frame policy, including policies that read both sides of an edge early.

## Lower-bound reduction

Fix a complete legal corner configuration and reveal it before the first frame. Its permutation sign fixes the edge permutation sign. Every edge assignment with this sign and even total flip has a legal completion with these corners. Since turns are known, corner responses are deterministic given the oracle and previous queries. Each legal turn transports the edge probe back to a single original edge sticker. Giving the observer arbitrary access to those 24 original sticker coordinates is a relaxation. A repeated sticker reading can be skipped, since it has a predetermined answer and the observer can track the policy's public turns. It suffices to show that the resulting edge decision game cannot be solved in at most 18 informative readings, even with the sign known at frame zero.

## Exact game on a compressed history

An edge position is complete, single-read, or untouched. Remove complete positions and their known unique labels from the matching problem. Order the remaining labels by their original rank. For a single-read position, put its observed side in local slot zero. Each slot exchange toggles the required residual orientation bit. Order the remaining positions by the observed color, putting untouched positions at the end. Any reordering of positions toggles the required residual permutation sign by its inversion parity. The resulting key contains the remaining label subset, the six single-read color multiplicities, and the two required residual parity bits. It describes the actual feasible set: match the remaining labels bijectively to the positions, choose orientations that agree with the single reads, and impose both residual parity constraints. The label subset and number of single reads also determine the elapsed informative readings.

There are two ways to refine the matching problem.

- **Read an untouched position.** Side one toggles the residual orientation bit when made local side zero. A returned color inserts the new single-read position after all single reads of that color. With zero-based untouched index (u), this move crosses (u) untouched positions and all single-read positions whose color sorts strictly later. Their total modulo two is the required sign update. The other untouched positions keep their relative order. Every untouched query is represented by its index parity and side.
- **Finish a single-read position.** Its first color and the response identify a unique ordered edge label, hence its orientation. If its position index is (i) and the removed label rank is (j), the permutation sign changes by ((i+j)mod2). This follows by moving both matched entries to the front before deleting them. The orientation bit changes by the removed orientation. For any color with multiple single reads, its contiguous block of indices is covered by trying one index of each available parity.

These transformations transport both feasible completions and their future sticker-query partitions. The solver counts completions up to two to distinguish empty, singleton, and ambiguous beliefs. For an ambiguous belief at positive budget it tries each query and accepts only if every feasible response can be solved in one fewer read. Empty beliefs can be accepted vacuously. At zero budget an ambiguous belief loses. These cases exhaust all informative query types. The C++ search returns false at the 18-read root for each of the two initial permutation signs with flip sum zero.

## Independent verification and scope

The Python verifier uses explicit ordered strings for positions and labels. It tries every remaining query coordinate, with no index-parity pruning, and computes each sign change by explicit reordering or matched deletion. It also compares its minimax result with literal permutation/orientation enumeration and set partitioning for 648 combinations of four-edge residual histories, parity requirements, and budgets. Both full roots lose. The reference outputs include cache/visit counts as reproduction diagnostics. The theorem rests on the soundness of the residual-state transport and the exhaustive Boolean recurrence, plus the constructive P8.40 upper bound. Physical turn count, noisy sensing, and the permanent-tag model have separate objectives.

## Reproduce

From the repository root, compile `scripts/cuberev-observation/audit_r14_p841_corner_oracle_minimax.cpp` using `g++ -std=c++20 -O3` and run the resulting executable. Then run `python3 scripts/cuberev-observation/verify_r14_p841_explicit_minimax.py`. Compare the concatenated outputs to `data/0.28/R14_P841_CORNER_ORACLE_MINIMAX_RECEIPT.txt`. The read-only workflow performs these checks and replays the P8.40 upper bound.
