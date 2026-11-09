# CUBE-REV 0.28 — R14-P7.5: Exact adaptive minimax for all 924 six-edge residual type sets, via signed color-observation covariance

**Date:** 2026-11-09. **Status:** Complete exact finite classification under **known residual edge permutation parity and edge-flip sum**, with all 30 conditional orbit-representative Bellman lower proofs, constructive upper policies, independently enumerated 924 signed state/query transports, and a complete 10,644,480-state set-bijection verification. **Not a full-cube physical P48 20-frame solution.** The full dual edge/corner problem remains `18 <= h_adaptive <= 21 OPEN`.

## 1. The finite conditional experiment

Let `T = {UR,UF,UL,UB,DR,DF,DL,DB,FR,FL,BL,BR}` be twelve original edge color types, each a two-color edge of the octahedral color graph `K_(2,2,2)` whose nonedges are the opposite pairs UD, RL, FB. Choose `L subset T`, `|L|=6` with a fixed source label order, six distinct spatial slots, and known even residual permutation sign and even total edge flip. States are words of twelve literal facelet colors with

\[
 |X_L| = (6!/2)\,2^{6-1}=11,520,\quad Q_L=\{0,\ldots,11\},\quad |\binom{T}{6}|=924.
\]

Every query returns the color of exactly one spatial edge facelet; at each belief the observer can freely choose the next query. No corner oracle is asserted for the full cube; known parity is part of this separate residual experimental condition.

Define `Win(B,k)` by exact zero-error Bellman recursion with literal nonempty color children. On all 30 color-graph orbit representatives, P7.4 or P7.5 directly built the deterministic one-step policy minimizing `(max child count, number of nonempty output colors, sum squares, local slot index)` and replayed all 11,520 real target states, then computed `Win(X_L,D-1)=False`. This determines the exact representative minimax depth without assuming greediness optimal.

## 2. Correcting abstract edge-color graph symmetry into a legal-state/query isomorphism

Let `c` be any of the `3! 2^3=48` automorphisms of the six-color graph preserving opposite pairs. It maps each old source edge type to one new source edge type, possibly reversing the canonical two-letter order. Let `L' = sort({c(e):e in L})`, with individual edge color pair canonicalized to the corresponding element of `T`.

- `tau` is the **new ordered source-label index** induced by `c`, i.e. `tau(i)` is the index of the mapped old source type `i` within `L'`.
- `epsilon_i in {0,1}` indicates whether applying `c` to source pair `i` reverses its canonical two-letter order.
- Choose a **spatial slot permutation** `sigma` of the six slots with `sgn(sigma)=sgn(tau)` (identity if even, swap slots 0/1 if odd).
- Choose a **spatial facelet flip vector** `delta` with `sum(delta) mod 2 = sum(epsilon) mod 2` (all zero except possibly slot 0).

For a source state with source permutation `p` and per-position flip vector `f`, the target state is defined by

\[
 p'_i = \tau(p_{\sigma(i)}),\qquad
 f'_i = f_{\sigma(i)}\oplus\epsilon_{p_{\sigma(i)}}\oplus\delta_i.
\]

Its legal invariants are preserved:

\[
 \operatorname{par}(p')=\operatorname{par}(\tau)+\operatorname{par}(p)+\operatorname{par}(\sigma)=0\pmod2,
\]

\[
 \sum_i f'_i = \sum_i f_i +\sum_j\epsilon_j+\sum_i\delta_i=0\pmod2.
\]

For spatial facelet query `q'=(i,s)` in the transformed game define the source query `rho^{-1}(q')=(sigma(i),s xor delta_i)`. If `O` is the literal color observation, then **for every legal state and every query**

\[
 O_{q'}(T_c x)=c\bigl(O_{\rho^{-1}(q')}(x)\bigr).
\]

The state map is bijective, because both source and target have 11,520 states and the source state is recovered uniquely from its mapped labels/positions/flips. The coordinate query map is also bijective. Thus **all children and complete adaptive decision trees are transported**, with outcome colors relabeled by `c`; the exact minimax depth is identical on every orbit member. This is a proof about the **conditional edge-color game**, not the physically legal full 48-sticker edge-plus-corner Rubik move group. Importantly, the query-index tie-break is **not** required to be covariant: the winning policy for each member is transported from its representative, rather than incorrectly assuming the locally recomputed greedy always selects the same kind of query.

## 3. Exact six-edge classification

The graph group has 30 six-edge subset orbits. Their sizes are: 14 orbits of size 48, six of size 24, one of size 16, seven of size 12, and two of size four. All **30 representatives** have exact Bellman `D-1` negative proofs, including both nine-read representatives:

| Exact adaptive worst depth `D*(L)` | Graph orbits | Original six-edge type sets |
|---:|---:|---:|
| 7 | 3 | 20 |
| 8 | 25 | 832 |
| 9 | 2 | 72 |
| **Total** | **30** | **924** |

The exact result is therefore

\[
\boxed{D^*(L)\in\{7,8,9\};\quad\#\{D^*=7\}=20,\quad\#\{D^*=8\}=832,\quad\#\{D^*=9\}=72.}
\]

This is not 924 independent Bellman minimax searches; it is **30 exhaustive Bellman searches plus a proved and explicitly verified observation-game isomorphism**. It does **not** prove the fresh `(M,K,S,q)` one-step implementation is optimal on all 924 type sets under literal local index tie breaks. Every one of the 924 type sets **does** inherit a concrete exact policy by inverse query-and-output transport from its representative.

## 4. Reproducibility and independent verification

1. Original 30 representative constructive upper games from P7.4: **345,600/345,600** literal target-to-singleton policy replays. P7.4 exact Bellman lower receipt completed initial 12 representatives.
2. P7.5 resumed cases 13,14,16–20 and cases 21–30 each had the full `Win(X_L,D-1)=False` verification. One nine-read case 15 timed out under an initial 7-second per-case gate and was honestly preserved as unresolved at that intermediate stage; **later it was re-run with a larger gate and completely passed**, with 180,275 memoized Bellman belief-budget nodes. Combining distinct lower records yields **30/30 exact**.
3. `audit_r14_p75_signed_color_transport.py` constructs the parity-and-flip corrections and checks all 48 color transforms against **all 11,520 states** of one full-size 48-member orbit, plus **177,408** deterministic legal state/query covariance samples (924 sets ×48 transforms×4 states).
4. `verify_r14_p75_all_924_exact_and_transport.py` merges every completed lower certificate, checks policy upper depth per representative, independently rebuilds all 924 orbits and produces an explicit signed `tau/sigma/epsilon/delta`, query-coordinate inverse, and color permutation witness for **every one of the 924 original type sets**.
5. Most strongly, `verify_r14_p75_all_924_full_state_bijections.py` regenerates each type set's complete **11,520** distinct parity-even/flip-even legal color words and verifies that the signed transformed full set is **exactly equal** to the representative's independent full set. It does so for **924×11,520 = 10,644,480** actual transformed words, with zero mismatches. This second verifier does not recompute Bellman itself; the Bellman results have their own producer and receipts.

All recorded Bellman statuses must be distinguished from timeouts, which are never failed-policy proofs. A fresh clean-checkout CI must generate the P7.4 30 upper policies and initial 12 lower receipts before resuming all 18 remaining tests; no `GitHub-Actions[bot]` commits are authorized.

## 5. Scholarly claim and failure boundaries

**Exact theorem:** In the idealized known-parity and known-total-flip *six-edge-only* six-color spatial-facelet query model, complete minimax classification of all 924 residual source-label sets is **7:20 / 8:832 / 9:72**. The orbit transport proof explicitly handles ordered labels, permutation parity, total flip, literal observation color and spatial query index. The group-action/Bellman transfer principle itself is prior mathematics; novelty priority remains an independent prior-literature gate.

**Not claimed:** The originally sought dual fixed edge-plus-corner physically turned Rubik sensor problem is solved; the 48 color automorphisms are physical whole-cube symmetries; the one-step greedy policy is independently optimal with its original index tie-break for each member; motor/HTM cost is optimized; or `h_adaptive=20` or `21` for the complete legal cube. The physically routed **mixed partial edge-and-corner observation** problem remains the real unsolved frontier, with `18<=h_adaptive<=21`.
