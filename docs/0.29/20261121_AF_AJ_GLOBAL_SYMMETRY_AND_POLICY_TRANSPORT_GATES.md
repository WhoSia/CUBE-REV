# CUBE-REV 0.29 AF–AJ — global edge symmetry, paired-policy transport, and exact inverse gates

**Date:** 2026-11-21. **Branch:** `research/current`. **Scientific priority:** prove the impossibility of any eighteen-frame adaptive paired-color identification policy, even with disclosed corners, then establish a physically routable nineteen-frame attaining policy. Do not interchange the frozen 52-representative upper-policy computation with an unconditional Lean upper-bound theorem.

## 1. What changes mathematically

A representative 19-frame edge policy starts with eleven one-sided edge colors, canonically renames the six colors with one of 48 opposite-preserving permutations `sigma`, and reorders the first eleven edge positions by a permutation `beta`, fixing the twelfth. The continuation runs in representative coordinates, and its final result must be transported back *without changing the number or causal order of observations*.

This is **not** a mere alphabet renaming. The correctness proof must preserve:
- oriented edge identity and both sticker colors;
- exact multiset of all twelve edge piece labels and even total flip parity;
- possible color answers at each adaptive query under the address pullback;
- the odd/even sign correction of the edge piece permutation when positions and labels are reordered;
- complete inverse reconstruction of the initial, not rotated, coloring;
- the exact time at which corner permutation sign becomes available.

Existing `ObservationTransport.lean` (AC) establishes a general budget-preserving policy adapter under response equivariance; `ElevenPrefix.lean` (AD) composes a fixed eleven-read prefix with an eight-read continuation; `NineteenSymmetry.lean` (AE) kernel-checks the finite tables for 48 color symmetries.

### AF — `SymmetryWordTransport.lean`

Defines `relabelEdgeValue sigma w` and `relabelEdgeWord sigma word` on arbitrary oriented edge words. Theorems prove exact label transformation and the universal flip identity

```text
flipBit (relabelEdgeWord sigma word)
  = (flipBit word + (wordLabels word).map (relabeledEdgeSwap sigma) |>.sum) % 2
```

with the precisely stated Lean expression in the source. If the edge labels form a permutation of `List.range 12`, the finite AE offset-sum proof shows that `flipBit` is unchanged for **every** possible word. Both sticker colors are equivariant under the six-color permutation. The initial AF CI failure was arithmetic: `omega` needed explicit `Nat.add_mod` and the bound `flipBit word < 2`; correction [682811a0](https://github.com/WhoSia/CUBE-REV/commit/682811a0a1bf53d856e7cf09ae1a501846debe0d).

### AG — `LegalEdgeSymmetry.lean`

Extends AF from flip parity to exact legal edge-piece labels. A kernel-computed table shows each of the 48 symmetries maps the twelve edge types to a permutation of the twelve types. Universal List.Perm transport then proves: every word whose labels are a permutation of `List.range 12` retains this property after relabeling; if flip parity was zero, it stays zero. The full vectors of first **and** second sticker colors transform pointwise. This proof applies to every edge permutation and orientation vector, not a sample of scrambles.

### AH — `PairedPolicyTransport.lean`

Defines a paired address `(edge position, edge side, corner address)`, and an edge cubie array plus 24 corner colors. `queryToOriginal beta` reindexes the edge slot, leaving the corner address unchanged. `responseToRepresentative sigma` relabels the edge color and preserves the corner color. The theorem `paired_response_equivariant` proves their equality against the concrete `sticker` function **before** each simultaneous response. `transportPairedPolicy_fits` preserves adaptive frame budgets, and `transportPairedPolicy_run` commutes with the full decision tree for arbitrary prior answers.

### AI — `SymmetryInverse.lean`

Defines the inverse color permutation by `(List.range 6).map (sigma.idxOf ·)`. Kernel-computed finite theorems establish that its inverse is in the same 48-element family and that it exactly undoes the forward relabeling for **all 24 oriented edges** in both composition orders. An independent Python reconstruction of the canonical twelve edge labels checked all 48 × 24 = 1,152 symmetry/oriented-edge inputs in both directions with no mismatches. This finite test is corroboration, not a substitute for the Lean proof.

### AJ — `RepresentativeRoundTrip.lean`

Defines a total decoder from the transported edge/corner representation back to the original using the inverse color table and the inverse `Fin 12 ≃ Fin 12` position permutation. The target theorem `representative_pair_state_round_trip` is the actual identity `decode(encode(s)) = s` for **every** original edge/corner array. A second, *conditional* theorem transports a certified representative decision policy to a correct real-coordinate policy at exactly the same budget; its premise still requires the actual representative decision policy and proof that it identifies every admissible normalized state.

## 2. Scientific trust boundaries

- The previously verified physical 18-frame lower bound is unchanged. Its finite data certificates use `native_decide` and display that corresponding dependency in `#print axioms`.
- The existing 52 upper-policy representative certificates and physical scramble replays are **independent computational evidence**, not a full semantic Lean implementation of their policy trees.
- AC–AJ each has a mandatory `lakefile.toml` target, static manifest assertions, and an explicitly read-only GitHub Actions check that compiles the source and prints theorem axioms. Passing a static test is not kernel success.
- As this research ledger was first written, all AF–AI modules had passed a pinned Lean *compilation step* in a workflow attempt, but several workflows were automatically superseded during sequential commits. The latest AJ workflow [#44895259544](https://github.com/WhoSia/CUBE-REV/actions/runs/44895259544) had not yet reported a final outcome. Recheck **that exact run** and correct any Lean error before claiming a completed AJ module.
- GitHub Actions is read-only and cannot create or author source commits; contributor authorship must remain the user's GitHub identity.

## 3. Remaining theorems in priority order

1. **Permutation parity under arbitrary reindexing and relabeling.** A single legal 12-piece array needs a proven sign identity
   `sign(rep) = sign(original) XOR sign(beta) XOR sign(alpha_sigma)`.
   The current complete piece-label and flip laws do **not** imply it automatically.
2. **Every ordered first-eleven-color transcript.** Define the computable representative selector and stable choice of `sigma`, `beta`, and their inverses. Prove that all legal initial words map into precisely one of the 52 certified representative situations and that every possible continuation response corresponds in both directions.
3. **Reify the actual 52 decision trees as one total Lean policy.** For every real reply branch, prove the frozen certificate supplies a branch, correct remaining candidate restriction, and a unique final identity once the terminal corner parity is supplied.
4. **Timing and terminal parity.** Show that the corner schedule releases the relevant final information at the correct frame without allowing a query to depend on its own response; use the separately verified fourteen-corner decoder to disambiguate any opposite-sign edge pair.
5. **Full upper-bound closure.** Assemble a global `Fits 19` theorem and `∀ s, Reachable s → tree.run abstractPairRead s = s`, then invoke the existing physical fixed-probe compiler. Only then may the manuscript state that the entire nineteen-frame *upper* theorem has been proven in Lean.

**Publication stance:** T/U versions lead with the eighteen-frame impossibility; preserve the W corrected physical example and explicitly identify the stale invalid V version as a negative control. Do not claim new discovery of the older fixed 21-frame construction. Numerical certificate receipts, published mathematical statements, and Lean kernel-check results are different evidence categories.
