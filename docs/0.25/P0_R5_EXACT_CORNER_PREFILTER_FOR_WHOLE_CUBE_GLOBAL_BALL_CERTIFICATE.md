# CUBE-REV 0.25 P0-R5 — Sound Physical-Corner Prefilter for Complete-Cubie Bidirectional Certification

**Status: executable native C++17 algorithm and GitHub Actions committed; real completed-run outcome and exact measured performance PENDING.** Official original WCA Seoul Summer 2026 Final A1, all legal physical 18 HTM, 54 original facelets, all 8 CP/CO and 12 EP/EO. No original human trajectories included.

## Exact theorem (one-sided proof-preserving membership filter)

Let \(G\) be the true fixed-center whole Rubik group. Let \(\pi_C:G\to Q_C\) be the *entire eight-corner permutation and orientation projection*. Let \(T=B_6(e)\) be the exact FULL-cubie goal ball containing 8,240,087 physically distinct complete cube states. Form its projected set \(C=\pi_C(T)\) and store it by **exact reversible corner key equality**, not probabilistic fingerprints. For every genuine source-side full-cube state \(x\),

\[
x\in T\implies \pi_C(x)\in C.
\]

Thus if its complete exact corner projection is absent from \(C\), a costly exact whole-state membership query against \(T\) can be skipped **without a false negative**. If its corner projection is present, the algorithm MUST still check the complete CP, CO, EP, EO state; matching corners does not imply solved edges or whole-cube set membership.

**Critical limitation:** A nonmember at source-prefix depth \(k\) may have successors whose corner projection IS in \(C\). Therefore this optimization **must never discard descendant branches**. It is a membership prefilter, not a globally admissible subtree cutoff. The C++ visit function does EXACTLY that: it visits every source-prefix normal-form successor regardless of whether a parent fails the projected membership check.

Every source-side normal-form word through depth7 is still generated under the inherited completeness-safe adjacent-same-face reduction and commuting-opposite-face canonical rule. Goal full ball B6 is built by inherited externally verified P1-R6 code. Neither group element nor original source word is synthetic.

The code declares each source DFS call in one of two mutually exclusive audited cases: **projection reject** or **exact full-cubie query**, and requires
\[
N_{\rm source}=N_{\rm corner\ rejected}+N_{\rm exact\ full\ queries}.
\]
A true full match requires the original two-word complete-cubie key equality. If any resource cutoff occurs, the executable emits a typed HOLD and nonzero exit; it cannot claim nonintersection on partial work.

## Actual executable source and matched baseline

[Whole-cube C++17 source-complete physical prefilter](../../scripts/cuberev-025/p0_r5_corner_projected_global_membership_cpp/main.cpp) reuses the existing independently physically tested [P1-R6 unrestricted full-cube C++ proof](../../scripts/cuberev-024/p1_r6_global_full18_bidir_cpp/main.cpp) and its true original 54-sticker turn tables.

[Read-only P0-R5 regression and proof experiment](../../.github/workflows/cuberev-025-P0-R5-corner-prefilter-global-wholecube.yml) compiles the actual full cube code and checks goal B6 versus source B7. It must independently reproduce exactly 8,240,087 full goal states, 120,213,368 cumulative source DFS entries, zero actual whole-cube intersections, and global interval **14≤d18(s)≤18**. It additionally reports the **number of projected corner states**, **corner-filtered membership negatives**, **complete-cubie full queries**, and the fraction of full-state queries avoided versus the no-filter P1-R6 baseline.

**Report the actual measured counts only from completed logs. Do NOT invent a 90% or 98% query reduction:** projected source distribution may be highly nonuniform, and an additional corner lookup may or may not improve elapsed runtime or memory. A count of full hash probes is not equivalent to wall-clock speed improvement; the projected set takes additional real RAM.

## Cross-check and next theorem

The already reproduced [P0-R2 full 88,179,840-corner PDB](P0_R2_FULL_CORNER_88M_AND_CERTIFIED_OPERATOR_COST_DUALITY.md) provides a stronger exact *distance* classifier but costs substantial additional storage. This P0-R5 program uses only the corner projections of the **existing exact whole-cubie goal radius6** and is hence much more economical to construct and inherits the source's actual true-cube original physics.

P0-R3/R4 established that five independently priced four-cubie projections have an exact continuous face-price optimization ceiling7 for this source, even while true full-cube distance≥14. That negative theorem motivates **synchronizing physical combined cubies rather than tinkering with these five independent scalar prices**.

After source-verified P0-R5, the next hard challenge is safe **actual descendant pruning**: prove a genuine admissible full-corner/edge joint remaining-distance bound exceeding the remaining radius, or produce a complete source-prefix cover of legal full words for a true new lower15. A saved exact lookup alone is a solver engineering improvement, NOT a new global geodesic bound.

**Source-grade finality:** at document creation, external P0-R5 CI and query counts are not yet confirmed; P0-R2 Lean was externally kernel-built (later full CI pass #38354902944). All GitHub authors and committers WhoSia only; bot contributions forbidden, GitHub Actions has only contents:read and no code writes.
