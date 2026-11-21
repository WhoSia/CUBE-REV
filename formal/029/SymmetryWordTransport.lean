import NineteenSymmetry
import ResidualWord

namespace CubeRev029.Nineteen

open Eighteen

/-- Apply one center-color symmetry to the actual oriented label word.
Unlike a finite list of worked examples, this acts on words of *arbitrary*
length, and retains the second-color orientation bit of each original edge. -/
def relabelEdgeValue (sigma : List Nat) (word : Nat) : Nat :=
  2 * relabeledEdgeType sigma (word / 2) +
    (word % 2 + relabeledEdgeSwap sigma (word / 2)) % 2

def relabelEdgeWord (sigma : List Nat) (word : Word) : Word :=
  word.map (relabelEdgeValue sigma)

/-- A color relabeling changes a piece's name as specified by the 48-element
symmetry table and cannot accidentally exchange piece name with its flip. -/
theorem relabelEdgeValue_label (sigma : List Nat) (word : Nat) :
    relabelEdgeValue sigma word / 2 =
      relabeledEdgeType sigma (word / 2) := by
  unfold relabelEdgeValue
  omega

theorem relabelEdgeValue_flip (sigma : List Nat) (word : Nat) :
    relabelEdgeValue sigma word % 2 =
      (word % 2 + relabeledEdgeSwap sigma (word / 2)) % 2 := by
  unfold relabelEdgeValue
  omega

/-- The relabeling of a complete word is pointwise the same as the relabeling
of its twelve unordered edge types, without a hidden reordering. -/
theorem relabelEdgeWord_labels (sigma : List Nat) (word : Word) :
    wordLabels (relabelEdgeWord sigma word) =
      (wordLabels word).map (relabeledEdgeType sigma) := by
  induction word with
  | nil => rfl
  | cons head tail ih =>
      change relabelEdgeValue sigma head / 2 ::
          wordLabels (relabelEdgeWord sigma tail) =
        relabeledEdgeType sigma (head / 2) ::
          (wordLabels tail).map (relabeledEdgeType sigma)
      rw [relabelEdgeValue_label, ih]

private theorem flipBit_cons_local (head : Nat) (tail : Word) :
    flipBit (head :: tail) = (head % 2 + flipBit tail) % 2 := by
  simp [flipBit, Nat.add_mod]

/-- Universal sum-of-flips rule for any oriented edge word, even an incomplete
or invalid one. The only change is the sum of the label-dependent offsets. -/
theorem relabelEdgeWord_flip_formula (sigma : List Nat) (word : Word) :
    flipBit (relabelEdgeWord sigma word) =
      (flipBit word +
        ((wordLabels word).map (relabeledEdgeSwap sigma)).sum) % 2 := by
  induction word with
  | nil => rfl
  | cons head tail ih =>
      change flipBit (relabelEdgeValue sigma head :: relabelEdgeWord sigma tail) =
        (flipBit (head :: tail) +
          (relabeledEdgeSwap sigma (head / 2) ::
            (wordLabels tail).map (relabeledEdgeSwap sigma)).sum) % 2
      rw [flipBit_cons_local, flipBit_cons_local, ih]
      simp only [List.sum_cons]
      rw [relabelEdgeValue_flip]
      omega

/-- If every original edge label occurs exactly once, all 48 allowed center
color relabelings preserve the legal parity of edge orientations. This is a
*universal* statement about every possible cubie permutation and twist vector,
rather than a finite test of a set of particular scrambles. -/
theorem symmetry_preserves_flipBit_for_all_complete_words
    (sigma : List Nat) (hsigma : sigma ∈ symmetries)
    (word : Word) (complete : (wordLabels word).Perm (List.range 12)) :
    flipBit (relabelEdgeWord sigma word) = flipBit word := by
  have permOffsets :
      ((wordLabels word).map (relabeledEdgeSwap sigma)).Perm
        ((List.range 12).map (relabeledEdgeSwap sigma)) :=
    complete.map (relabeledEdgeSwap sigma)
  have sumOffsets := permOffsets.sum_nat
  rw [relabelEdgeWord_flip_formula, sumOffsets]
  have evenOffsets := symmetry_even_flip_offset sigma hsigma
  omega

/-- The original physical sticker's reported color is carried equivariantly
under all 48 symmetries, for every oriented edge identity and both sides. -/
theorem symmetry_relabelEdgeValue_responses
    (sigma : List Nat) (hsigma : sigma ∈ symmetries)
    (word : Nat) (hword : word < 24) (side : Bool) :
    sticker (relabelEdgeValue sigma word) side =
      sigma[sticker word side]! := by
  simpa [relabelEdgeValue, relabeledOrientedEdge] using
    symmetry_preserves_oriented_edge_colors sigma hsigma ⟨word, hword⟩ side

#print axioms relabelEdgeValue_label
#print axioms relabelEdgeValue_flip
#print axioms relabelEdgeWord_labels
#print axioms relabelEdgeWord_flip_formula
#print axioms symmetry_preserves_flipBit_for_all_complete_words
#print axioms symmetry_relabelEdgeValue_responses

end CubeRev029.Nineteen
