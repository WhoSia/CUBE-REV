import PairedPolicyTransport
import SymmetryInverse
import EdgeSorting

namespace CubeRev029.Nineteen

/-- Explicit edge-slot permutation structure, independent of Mathlib Equiv. -/
structure EdgeSlotOrder where
  forward : Fin 12 → Fin 12
  backward : Fin 12 → Fin 12
  left_inv : ∀ i, forward (backward i) = i
  right_inv : ∀ i, backward (forward i) = i


/-- A bounded adjacent swap of Fin 12 indices. On invalid swap
positions this is the identity. The resulting finite-index map is
involutive, so no external equivalence library is needed. -/
def adjacentTwelveIndex (i : Nat) (j : Fin 12) : Fin 12 :=
  if h : i + 1 < 12 then
    if h₁ : j.val = i then
      ⟨i + 1, h⟩
    else if h₂ : j.val = i + 1 then
      ⟨i, by omega⟩
    else j
  else j

theorem adjacent_twelve_index_involutive
    (i : Nat) (j : Fin 12) :
    adjacentTwelveIndex i (adjacentTwelveIndex i j) = j := by
  by_cases h : i + 1 < 12
  · by_cases h₁ : j.val = i
    · apply Fin.ext
      simp [adjacentTwelveIndex, h, h₁]
      omega
    · by_cases h₂ : j.val = i + 1
      · apply Fin.ext
        simp [adjacentTwelveIndex, h, h₁, h₂]
        omega
      · simp [adjacentTwelveIndex, h, h₁, h₂]
  · simp [adjacentTwelveIndex, h]

/-- Both directions are the same adjacent transposition, with
the inverse equations discharged by the involution proof above. -/
def adjacentTwelveSlotOrder (i : Nat) : EdgeSlotOrder where
  forward := adjacentTwelveIndex i
  backward := adjacentTwelveIndex i
  left_inv := adjacent_twelve_index_involutive i
  right_inv := adjacent_twelve_index_involutive i

/-- Composition of two verified twelve-slot coordinate bijections.
The first and second inverse maps are composed in reverse order. -/
def composeEdgeSlotOrders (a b : EdgeSlotOrder) : EdgeSlotOrder where
  forward := fun i => a.forward (b.forward i)
  backward := fun i => b.backward (a.backward i)
  left_inv := by
    intro i
    change a.forward (b.forward (b.backward (a.backward i))) = i
    rw [b.left_inv, a.left_inv]
  right_inv := by
    intro i
    change b.backward (a.backward (a.forward (b.forward i))) = i
    rw [a.right_inv, b.right_inv]

def identityEdgeSlotOrder : EdgeSlotOrder where
  forward := id
  backward := id
  left_inv := by intro i; rfl
  right_inv := by intro i; rfl

/-- A full list of actual adjacent swaps now constructs a legitimate
twelve-slot EdgeSlotOrder and a real inverse, not merely a proof of
existence or a pair of externally supplied functions. -/
def slotOrderFromAdjacentTrace : List Nat → EdgeSlotOrder
  | [] => identityEdgeSlotOrder
  | i :: rest =>
      composeEdgeSlotOrders (adjacentTwelveSlotOrder i)
        (slotOrderFromAdjacentTrace rest)

theorem slot_order_from_adjacent_trace_round_trip
    (path : List Nat) (i : Fin 12) :
    (slotOrderFromAdjacentTrace path).forward
      ((slotOrderFromAdjacentTrace path).backward i) = i := by
  exact (slotOrderFromAdjacentTrace path).left_inv i

#print axioms adjacent_twelve_index_involutive
#print axioms slot_order_from_adjacent_trace_round_trip

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
