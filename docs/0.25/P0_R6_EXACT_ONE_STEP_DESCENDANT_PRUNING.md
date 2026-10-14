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
