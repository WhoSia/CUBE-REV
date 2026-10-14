# CUBE-REV 0.25 P0-R6 — Exact One-Step Projected Descendant Pruning for a Whole-Cubie Global Certificate

**State: implementation committed for external verification; CI PASS and measured savings NOT YET CLAIMED.** This is a deliberately narrow first research attack under the broader P0-R6 corner–edge joint-admissibility programme. Real WCA Seoul Summer 2026 3×3 Final A1, original fixed-center 54 stickers, legal 18 HTM, full CP/CO/EP/EO collision-free equality. Original established global bound remains **14 <= d18(s) <= 18**.

## New finite theorem
Let T=B6(e) be the **full-cubie** exact solved-side ball. Set C6=pi_C(T), and define E7=C6 union {pi_C(g a): g is a full representative of any corner projection in C6, a is one of the 18 physically legal HTM turns}. The definition is representative independent: the Rubik's legal corner turn depends only on corner configuration, not edge configuration. Equivalently E7 is the exact one-step reverse-reachable corner enlargement of pi_C(T), including zero moves. Because every 18HTM inverse is in the same legal alphabet, forward and reverse one-step neighborhood coincide.

For any original full cubie state x, if pi_C(x) is NOT in E7 then **neither x nor any of its one-move children can be in T**. The proof is by contradiction: if x a belongs to T, then x=(x a)a^{-1}, so pi_C(x) belongs to the one-step envelope E7. If x belongs to T then pi_C(x) belongs to C6 subset E7.

Thus, at source DFS nodes with exactly ONE move remaining before the previously source-complete B7 boundary, omit all legal canonical children when pi_C(x) not in E7. Continue to check genuine full CP/CO/EP/EO equality on any non-rejected state. The optimization never removes a completion shorter than or equal to the prior source radius 7. This is an **actual descendant subtree prune**, unlike P0-R5's full-key lookup elision. It is not automatically a wall-clock speedup: constructing E7 consumes CPU and RAM, and source prefix reductions only concern the last layer.

## Implementation and reproducibility contract
- C++17 physical checker: `scripts/cuberev-025/p0_r6_one_step_descendant_cpp/main.cpp` includes the unchanged historical P1-R6 physical engine under the existing library guard.
- E7 is built from all exact B6 full-state keys using one **lossless actual-cubie representative per distinct corner projection**. Move permutations come from the inherited real original 54-sticker-derived physical turn tables. All membership uses exact 64-bit packed corner equality; an unordered-set hash collision cannot create a false negative because equality remains exact.
- Read-only GitHub Actions workflow compiles the C++17 engine and runs both the full-source B6/B7 experiment and small-radius regression. A timed-out or partially completed run exits typed HOLD, not PASS.
- Report raw goal and expanded corner cardinalities, cumulative source visits, descendant cutoff nodes, skipped canonical children, true whole-cubie queries, hits, wall clock and peak resident memory, then compare the same source/radii against P0-R5. Counts MUST come from completed CI logs, not estimates.
- One-sided invariant: no full equality match omitted; canonical successor counting applies the **original identical** normal-form rule. If the original completed full-cubie B6 goal cardinality or projected B6 corner cardinality differs from P0-R5, the executable fails.

## Limitations and future hard attacks
This theorem only uses **a one-step corner extension**, not yet a joint corner–edge PDB. For source radii <=7 and goal radius6, it can exclude the last layer of canonical children of eligible penultimate-depth nodes; it does NOT by itself prove d18>=15 or rule out 14–17 solutions. A more powerful true h_CE would require a sound shared-word corner–edge synchronization, additive operator-cost proof, or a combined projection/certificate. Do not add independent overlapping corner/edge heuristic distances. The immediate evaluation is experimental: subtree count and relative hardware cost might improve or regress.

### Governance
Commit author+committer WhoSia only; github-actions[bot]/github-action[bot] forbidden. CI contents:read, checkout persist-credentials:false, zero Git writeback. Preserve 0.24/P0-R1..R5 negative proof boundaries and protected private 451 human records. No Python-first implementation.


## 2026-10-14 P0-R6A follow-up — independent canonical-word accounting and paired cost experiment

**Implementation complete; GitHub Actions completion and numerical performance not yet independently observed.** This changes the quality of the pending experiment, not its externally attested result.

The original source DFS checks ALL canonical legal prefixes at each iterative depth limit. Let c_d count legal canonical exact-length d action words, with c_0=1. The independent recurrence tracks the final generator and applies precisely the original source \`canonical(last,next)\` adjacency rule (no consecutive identical faces, reorder commuting opposite faces into the chosen canonical direction). Thus the unpruned total recursive call count for bounds 0..R is

\[
N_R=\sum_{d=0}^{R}(R-d+1)c_d.
\]

A small independent C++17 combinatorial program, compiled and executed locally in the audit environment, returned N6=9,005,776, N7=120,213,368, N8=1,604,664,504. The N7 count agrees EXACTLY with the previous GitHub Actions P0-R5 physical source-visit receipt. These counts are **normal-form DFS recursive calls including repeated iterative-depth visits**, NOT distinct physical cube states.

Because this P0-R6 initial theorem prunes only a node's immediate canonical children when exactly one move remains, each pruned child corresponds to exactly one missing baseline recursive visit. The C++ executable now checks the exact equation

\[
\text{VISITED}+\text{SKIPPED\_CHILDREN}=N_R.
\]

It throws and cannot certify a lower bound if equality fails. This equality checks whole-prefix accounting; the separate actual corner-envelope theorem proves that each skipped child could not meet B6(e). Neither condition alone is sufficient as an external physical proof.

The [paired read-only P0-R6A Actions workflow](../../.github/workflows/cuberev-025-P0-R6-descendant-pruning.yml) now compiles both historical P0-R5 and new P0-R6, runs source B7 versus actual complete-cubie target B6 on the **same GitHub runner**, logs true GNU time wall seconds and maximum resident memory (KiB) for each, and invokes the independently authored [Go receipt auditor](../../scripts/cuberev-025/p0_r6_receipt_go/main.go). The Go checker refuses to report verified savings if either historical physical no-intersection result, baseline visit count, exact source partition, or measured costs are missing. It reports signed changes in wall time and RSS rather than assuming descendant elimination yields a speedup. Running two alternatives in fixed order on one runner controls hardware class but does not eliminate order, contention or cache effects; source-general performance claims require more benchmarks and repetitions.

## P0-R6B — direct full-physical exclusion test for 14 moves or fewer

**Mathematical target (NOT YET AN OBSERVED RESULT):**
\[
B_8(s)\cap B_6(e)=\varnothing\quad\Longrightarrow\quad d_{18}(s,e)\ge15.
\]
Conversely any intersection supplies a whole-cubie state on an actual source word of length at most 8 and a goal word of length at most 6; it refutes the attempted lower15. The earlier B7(s) versus B6(e) excludes only lengths <=13 and therefore proves lower14, **not** the nonexistence of 14-move solutions.

The physical C++17 R6 search now accepts source radius 8 with the original 54-sticker physical check, full exact CP/CO/EP/EO equality, and identical canonical normal-form coverage. The same one-step envelope is applied to each penultimate-depth prefix; this does NOT presume complete corner-edge coupled admissibility. The expected unpruned iterative source count is exactly **1,604,664,504**. Any source resource limit, timeout, unexpectedly changed goal cardinality, broken equality, or discovered source–goal intersection exits without the lower15 certificate. Only after a complete collision-free original physical zero-intersection run can the executable emit \`P0R6_GLOBAL_LOWER 15 UPPER 18 ... ALL_14_OR_LESS_EXCLUDED 1\`.

The dedicated [read-only P0-R6B Actions experimental court](../../.github/workflows/cuberev-025-P0-R6B-global-lower15-source8.yml) has a bounded wall/resource budget and logs measured wall time and RSS. A separate Go-mode verifier independently computes N8 and requires a completed zero-intersection whole-cube receipt before recognizing a claimed lower15. The new court is an **ATTEMPT to solve the open 14-move exclusion problem**, and a HOLD caused by insufficient compute remains a HOLD. No verified P0-R6B run ID or result has been obtained at this writing.

**Claim status:** P0-R6A finite theorem and code committed, native full-scale PASS pending. P0-R6B exact 14-or-less exclusion programme committed, global lower15 pending. External GitHub Actions run listing for push-triggered executions was not available through the current connector query, which only exposes PR-associated commit runs; an empty return is not evidence of failure or success. Preserve earlier certified **14<=d18(s)<=18** until completed run logs and independent evidence are read.
