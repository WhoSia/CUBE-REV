import PairedPolicyTransport
import SymmetryInverse

namespace CubeRev029.Nineteen

/-- Explicit edge-slot permutation structure, independent of Mathlib Equiv. -/
structure EdgeSlotOrder where
  forward : Fin 12 → Fin 12
  backward : Fin 12 → Fin 12
  left_inv : ∀ i, forward (backward i) = i
  right_inv : ∀ i, backward (forward i) = i


/-- A total decoder for representative-coordinate states. The modulo-24
operation only supplies a default for arbitrary *invalid* representative
outputs; the round-trip theorem below proves it does not alter any valid
state obtained from a physical cubie coloring and an allowed symmetry. -/
def decodeRepresentativePairState
    (sigma : List Nat) (order : EdgeSlotOrder)
    (s : RelabeledAndCornerState) : CubieAndCornerState :=
  ((fun i =>
      (⟨(relabelEdgeValue (inverseColorTable sigma)
           (s.1 (order.backward i))) % 24, Nat.mod_lt _ (by decide)⟩ : Fin 24)),
    s.2)

/-- For *all* oriented edge arrays and corner color arrays, an invertible
position permutation and a valid one of the 48 center-color symmetries can
be undone. This is stronger than verifying a set of particular scrambles. -/
theorem representative_pair_state_round_trip
    (sigma : List Nat) (hsigma : sigma ∈ symmetries)
    (order : EdgeSlotOrder) (state : CubieAndCornerState) :
    decodeRepresentativePairState sigma order
      (representativePairState sigma order.forward state) = state := by
  rcases state with ⟨pieces, corners⟩
  apply Prod.ext
  · funext i
    apply Fin.ext
    change
      (relabelEdgeValue (inverseColorTable sigma)
        (relabelEdgeValue sigma (pieces (order.forward (order.backward i))).val)) % 24 =
          (pieces i).val
    rw [order.left_inv i]
    rw [inverse_color_table_restores_oriented_edge sigma hsigma (pieces i)]
    exact Nat.mod_eq_of_lt (pieces i).isLt
  · rfl

/-- Complete soundness of the concrete symmetry/position policy adapter.
For any admissible family of real cubie/corner states, if an abstract
representative policy is certified correct for every normalized member,
its transported policy reconstructs the original state at the same budget.

The remaining substantive obligation is to produce the representative
policy and discharge its correctness premise for *every* legal first-color
history, including the terminal corner-permutation-sign decoder. -/
theorem correct_original_policy_of_certified_representative
    (sigma : List Nat) (hsigma : sigma ∈ symmetries)
    (order : EdgeSlotOrder)
    (admissible : CubieAndCornerState → Prop)
    (tree : Policy PairedAddress12 PairedReply12 RelabeledAndCornerState)
    {budget : Nat}
    (fits : Fits budget tree)
    (certified : ∀ state, admissible state →
      tree.run relabeledPairRead (representativePairState sigma order.forward state) =
        representativePairState sigma order.forward state) :
    ∃ original : Policy PairedAddress12 PairedReply12 CubieAndCornerState,
      Fits budget original ∧
      ∀ state, admissible state → original.run realPairRead state = state := by
  refine ⟨transportPairedPolicy sigma order.forward
      (decodeRepresentativePairState sigma order) tree,
      transportPairedPolicy_fits sigma order.forward
        (decodeRepresentativePairState sigma order) fits, ?_⟩
  intro state hs
  rw [transportPairedPolicy_run sigma hsigma order.forward
    (decodeRepresentativePairState sigma order) tree state]
  rw [certified state hs]
  exact representative_pair_state_round_trip sigma hsigma order state

#print axioms representative_pair_state_round_trip
#print axioms correct_original_policy_of_certified_representative

end CubeRev029.Nineteen
