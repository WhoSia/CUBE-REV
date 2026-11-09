# CUBE-REV 0.28 / R14-P6.2 — Full Finite-Game Covariant Belief Quotient and Inverse-Policy Court

**Audit date:** 2026-11-09. **Status:** LOCAL PASS for the explicitly defined 648-state 3-edge/3-corner coupled-parity miniature. **Not** a 20-frame solution for the physical full 12-edge/8-corner cube. The existing full-cube `18 <= h_adaptive <= 21` bound is unchanged. No novelty/priority claim is made for generic group-equivariant minimax.

## 1. What is being proved

Let `X` be all 648 parity-matched, zero-orientation-sum states of the independent 3-edge/3-corner categorical-color model, and let `Q` contain its 6×9=54 paired-facelet spatial queries. Let `G` be its entire 648-element *legal spatial-position permutation group*. For a state `x` represented as its edge/corner facelet-color words, the spatial left action `g·x` is the word with color `c_(g·x)(g·i)=c_x(i)` separately on edge and corner slots. `g·x` is a legal complete state because `g` belongs to `G`.

For **every** belief `B ⊆ X`, query `q`, and literal ordered color outcome `y`,

    g(B_{q,y}) = (gB)_{gq,y}.                          (1)

This is verified by the explicit state index permutation and by all 54 literal query masks. Because singleton detection and the set of available queries are preserved, exact Bellman minimax `Win(B,k)` is invariant under `g` for every budget `k`.

A **sound canonical belief** is therefore the minimum numeric 648-bit mask among the *exactly* 648 transformed beliefs `gB`; the implementation also returns a group element `w` certifying `wB=canonical(B)`. A winning canonical query `q*` is transported back to the original coordinates by `w^{-1}q*`; the 6-color response symbols are unchanged under this **spatial left action**. This is more restrictive than a hypothetical general color-relabeling double action; source-color automorphisms need separate validation in the full P48 model.

## 2. Reproducible finite checks

The executable script is **standalone**: it does not import the P6.1 script, any Rubik physical geometry, or third-party libraries. It independently reconstructs all 648 states, 648 legal spatial group elements, and all 54 query-output masks. It builds its own exact 648-state AND–OR Bellman solver and full depth-four policy, replaying its 648 decoder leaves. If the earlier P6.1 complete certificate JSON happens to be next to it, the entire policy is compared exactly, but this is optional: the new script works in a clean GitHub checkout with no stored P6.1 certificate.

The first execution passed:

| Court | Actual result | Strict meaning |
|---|---:|---|
| Miniature states and legal spatial transformations | 648 each | Explicit legal state closure and bijectivity |
| All spatial paired query choices | 54 | No heuristic query filtering |
| Complete reference adaptive policy | 963 nodes / 648 reconstructed leaves | Full decoder, maximum depth 4 |
| Exact color-branch covariance | **153,090** paired (belief, spatial transform, query) checks | Every realized next color branch agrees under transformation |
| Distinct belief sets inspected | **2,007** | Policy nodes plus all first-layer query outcomes |
| Group orbits actually enumerated | **49** | Exact transformed belief masks and witness elements |
| Bellman-value comparison | **315** policy nonterminal beliefs | Win(B,k)=Win(gB,k), including one smaller feasible budget |
| Winning policy transport back | **315** inversions | Every returned original-space query has the same outcome branches and remains winning |

This is a complete *finite test of correctness and transport* for the sampled 315 policy-node beliefs; it does **not** assert that all `2^648` abstract belief subsets have been enumerated. Statement (1), however, holds for every subset mathematically by the query covariance identity.

## 3. Critical P6 negative-control correction and a genuine replacement

The P6 equal-108-candidate pair `A={(edge slot 0)=U,(corner slot 0)=U}` and `B={(edge slot 0)=U,(corner slot 4)=U}` have different next-response-size partitions **for the same fixed query** `(0,0)`:

- `A`: `[108]` (the query is redundant);
- `B`: `[12,12,24,24,36]`.

The older narrow conclusion—that *candidate count alone* does not determine a **fixed spatial query's response partition**—is correct. But P6.2's exact complete group enumeration shows `A` and `B` **are spatially group-equivalent**. They MUST NOT be presented as a counterexample to global query-permutation-aware Bellman equivalence. The earlier source and README already cautioned against that extrapolation; this new court resolves it exactly.

**Genuine non-isomorphism test:** P6.2 finds two actual reachable beliefs `A'`, `B'`, each with **36 legal candidates**, whose 54-query action profiles are different even after discarding query index and individual color-response names. Define

    P(B) = multiset_{q ∈ Q} (sorted nonzero child cardinalities for B under q).

If two beliefs are related by *any* observation-game isomorphism that bijectively permutes the query set and response labels (including the legitimate group action), their `P(B)` must agree. Here `P(A')≠P(B')` with an explicit machine-readable difference in frequency of a partition tuple (e.g. `[1,1,1,1,1,1,2,2,2,2,2,2,3,3,6,6]` occurs 24 times in one and zero times in the other). Consequently this pair is **not** observation-isomorphic under query permutations and response relabeling. Exact 648-bit belief masks and the differing frequencies are preserved in the JSON receipt. This is a stronger, properly scoped negative control.

Do not infer unequal optimal worst-case depths from this non-isomorphism: non-isomorphic beliefs can share the same depth.

## 4. Why this is a necessary but insufficient full-P48 step

The full physical Rubik group cannot be enumerated as 648 states or 648 spatial transformations. For full P48, the exact parity-factored matching constraints from P6 supply a symbolic belief interface. The next engineering gate is to implement a **proof-carrying canonical constraint signature** using legal cubie permutations and local orientations *plus* any color-symbol relabels justified by a legal original-source action, retaining both the forward and inverse query-and-outcome maps. A sound quotient must preserve the **entire posterior set**, not just candidate counts or one-step child-size multisets. It must handle repeated reads, contradictory transcripts, both permutation parity classes, orientation sums, physical corner chirality, and P5.4's two-unvisited-cubies parity boundary.

Only after these checks may a branch-and-bound/AND–OR search for `h_adaptive<=20` use the quotient. Neither a failed finite search nor a large partial certificate is an impossibility proof. Full adaptive optimum remains unknown.

## 5. Source and custody

- `scripts/cuberev-observation/audit_r14_p62_exact_belief_covariance.py`
- Raw standalone Python / raw JSON receipt to be preserved in Drive with readback SHA-256.
- The complete P6.1 reference remains independently replayable, but does not need to be downloaded into clean CI.
- No newly claimed theorem is a general replacement for classical group action or for the Fundamental Theorem of Cubology.
