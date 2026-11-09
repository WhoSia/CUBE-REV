# CUBE-REV 0.28 — R14-P7.1: Exact Two-Step Lookahead on All 495 Four-Edge Residual Label Sets

**Date:** 2026-11-09. **Computational status:** complete finite census, source-independent second full-state verification, **47,520/47,520** greedy-policy starting states decoded. **Not** a proof that two-step lookahead is optimal for every residual size or for full P48. Entire adaptive cube horizon remains **18 <= h_adaptive <= 21**.

## Mathematical experiment

Take any four types from the twelve physical Rubik edge types `{UR,UF,UL,UB,DR,DF,DL,DB,FR,FL,BL,BR}`. Condition on a known even residual permutation parity and even residual edge-flip parity. The possible states consist of `4!/2 * 2^3 = 96` distinct oriented edge matchings. Each query reads the six-color value of one of eight spatial edge stickers. There are `C(12,4)=495` distinct type sets. The model is an **edge-only lower-bound/residual game with a parity oracle**, not the full paired-color two-sector model.

Let `B` be a nonempty residual state belief and `B_{q,c}` its nonempty outcome child after reading sticker position q and observing color c. Define

    M(B,q) = max_c |B_{q,c}|,
    V(B)   = min_{q yielding >1 children} M(B,q),   V({single state})=1,
    W_2(B,q) = max_c V(B_{q,c}).

Our **one-step** policy takes q minimizing the tuple `(M(B,q), sum_c |B_{q,c}|^2, q)`. Our **two-step** policy instead minimizes `(W_2(B,q), M(B,q), sum_c |B_{q,c}|^2, q)`. Both policies are defined by their **current belief only**, never by knowing the true hidden state. The two-step rule is an exact worst-leaf-*cardinality* lookahead of length two, not a two-level Bellman minimax solution for the eventual remaining **number of observations**.

For each type set, independently compute the exact zero-error minimum adaptive depth by a complete AND–OR search

    Win(B,k) := (|B|==1) or
       exists q: for all nonempty outcomes c, Win(B_{q,c},k-1).

Do not evaluate a claimed optimum from the two-step strategy itself; calculate the exact optimum in the same 96-state game and verify it by a second implementation.

## Exhaustive 495-set result

| Zero-error worst-case observations | Exact optimal AND–OR sets | One-step policy sets | Two-step policy sets |
|---|---:|---:|---:|
| 3 | 72 | 72 | **72** |
| 4 | 369 | 249 | **369** |
| 5 | 54 | 174 | **54** |
| Total | 495 | 495 | 495 |

**120 of the 495** edge-label sets induce a **one-observation regret** under the immediate max-cell greedy policy. Every one of those **120** failures is repaired by the **two-step max-cell lookahead**, with **zero** cases made worse. A concrete counterexample to one-step optimality is `{UR,UF,UL,DR}`: exact depth **4**, one-step greedy depth **5**, two-step lookahead depth **4**.

**Independent replay:** a standalone verification script does not import the producer. It reconstructs all 96 states per label set and uses frozenset-based direct *per-state* color partitioning rather than the producer's bitmask algebra. It recomputes **all three** depths (one-step, two-step, exact AND–OR), verifies every of the **495** tuples, and executes the two-step policy on all **495 × 96 = 47,520** distinct starting state/set cases, checking exact final singleton identity and horizon bound. Output: `R14_P7_INDEPENDENT_ALL_495_TWO_STEP_EXACT_MINIMAX_PASS`.

For a fixed known residual parity/flip bit, odd parity or odd flip cases are spatially query-isomorphic to the even-even reference: swap two observed spatial cubie positions to change permutation parity and reverse the two facelet slots at one spatial cubie to change total flip parity. These transformations biject all states and queries and do not alter color outputs after the corresponding coordinate relabeling. The explicitly executed 495 court is **even-even**; the argument extends the *conditional residual problem* to the other three parity-bit combinations, not the entire 12-edge/8-corner optimal policy.

## Relationship to the R14-P7 certificate gap

All 648 microgame initial states have an individualized length-2 separating certificate despite exact adaptive depth 4. For the selected hard residual sets, the individualized certificate lengths are 3, 4, 6, whereas previously established adaptive minimax depths are 5, 7, 9. The two-step observation rule achieves depths 5, 7, 9 on those three hard residual exemplars when the one-step greedy policy does too; **this isolated fact alone does not prove general two-step optimality for residual sizes five or six**.

The all-495 outcome demonstrates a structural failure of immediate population minimization and a surprising finite success of two-step population lookahead. This is an **exhaustive algorithmic observation**, possibly a theorem once specified as an exact finite verified classification. It does **not** establish a simple closed-form, a noncomputational explanation, a general greedy-approximation bound, a global adaptive 20-frame strategy, or published priority. The next theoretical question is whether the 2-step lookahead property follows from a cube edge-color graph (K_{2,2,2}) invariant and remains true for other type-set sizes. Search for a **counterexample** before generalizing.

## Next falsification gates

1. Independently replay 5- and 6-edge mixed residual games with the 2-step rule; search for first failure relative to exact previously established depths. A five/six-edge failure is scientifically valuable as a counterexample to an overbroad conjecture.
2. Test all four residual parity/flip cases by explicit isomorphism witnesses, rather than a loose appeal to parity.
3. Investigate why the 120 bad one-step cases are corrected: compare optimal first query, maximum size after 1 and 2 reads, and shortest remaining certificates on the children.
4. Extend online sensing to the full two-probe coupled-parity P48 physical model. Keeping the edge-only oracle separate from corners is obligatory; the equal-time simultaneous corner probe is not automatically innocuous when deriving a global policy.

## Evidence and custody

- Producer: `scripts/cuberev-observation/audit_r14_p7_lookahead.py`.
- Independent direct-frozenset checker: `scripts/cuberev-observation/verify_r14_p7_lookahead.py`.
- The machine-readable 495-row receipt: `R14_P7_ALL_495_LOOKAHEAD_RESULTS.json` (Drive immutable raw bytes).
- Same-turn raw execution result: all 495 compared, 47,520 state replays, zero mismatch.
- Related separate P7 full 940-collision ledger and greedily distilled 7/12/41 obstruction cores in Drive, with independent check.
- Previous R8/R9 adaptive depths 72,369,54 are reproduced **fresh** by the producer and verifier; this does not replace review of original physical edge-color labeling and orientation/chirality conventions before manuscript publication.
- Prior theory: Buhrman and de Wolf (2002), *Complexity Measures and Decision Tree Complexity: A Survey*, DOI 10.1016/S0304-3975(01)00144-X; the generic certificate/decision gap is preexisting work.
