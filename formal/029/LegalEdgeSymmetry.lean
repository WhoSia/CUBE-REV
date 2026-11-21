import SymmetryWordTransport

namespace CubeRev029.Nineteen

open Eighteen

set_option maxRecDepth 16000
set_option maxHeartbeats 0

/-- Stronger than a cardinality check: all 48 opposite-pair-preserving center
relabelings yield genuine permutations of the twelve original edge types. -/
theorem every_symmetry_is_an_edge_type_permutation :
    ∀ sigma ∈ symmetries,
      ((List.range 12).map (relabeledEdgeType sigma)).Perm (List.range 12) := by
  decide +kernel

/-- An arbitrary legal assignment uses each of the twelve edge cubies exactly
once. Relabeling them by any of the 48 symmetries preserves this precise
multiset condition, and not merely a sum of labels. -/
theorem symmetry_relabels_any_complete_edge_permutation
    (sigma : List Nat) (hsigma : sigma ∈ symmetries)
    (word : Word) (complete : (wordLabels word).Perm (List.range 12)) :
    (wordLabels (relabelEdgeWord sigma word)).Perm (List.range 12) := by
  rw [relabelEdgeWord_labels]
  exact (complete.map (relabeledEdgeType sigma)).trans
    (every_symmetry_is_an_edge_type_permutation sigma hsigma)

/-- Complete legal edge words contain only the twenty-four oriented edge
identities, even if the word is presented in an arbitrary permutation order. -/
theorem complete_word_oriented_addresses_in_range
    (word : Word) (complete : (wordLabels word).Perm (List.range 12)) :
    ∀ id ∈ word, id < 24 := by
  intro id hid
  have hidLabel : id / 2 ∈ wordLabels word := by
    change id / 2 ∈ word.map (fun x => x / 2)
    exact List.mem_map.mpr ⟨id, hid, rfl⟩
  have hidRange : id / 2 ∈ List.range 12 := complete.mem_iff.mp hidLabel
  have hidSmall : id / 2 < 12 := List.mem_range.mp hidRange
  omega

/-- Replacing the labels in an arbitrary legal orientation word commutes
with reading every sticker on a chosen side. This does not require a
pre-selected scramble or an enumerated list of candidate words. -/
theorem symmetry_relabels_word_observation_vector
    (sigma : List Nat) (hsigma : sigma ∈ symmetries) (side : Bool) :
    ∀ word : Word, (∀ id ∈ word, id < 24) →
      (relabelEdgeWord sigma word).map (fun x => sticker x side) =
        (word.map (fun x => sticker x side)).map (fun color => sigma[color]!) := by
  intro word
  induction word with
  | nil =>
      intro _
      rfl
  | cons head tail ih =>
      intro within
      have headWithin : head < 24 := within head (by simp)
      have tailWithin : ∀ id ∈ tail, id < 24 := by
        intro id hid
        exact within id (List.mem_cons_of_mem head hid)
      change sticker (relabelEdgeValue sigma head) side ::
        (relabelEdgeWord sigma tail).map (fun x => sticker x side) =
        sigma[sticker head side]! ::
          (tail.map (fun x => sticker x side)).map (fun c => sigma[c]!)
      rw [symmetry_relabelEdgeValue_responses sigma hsigma head headWithin side,
          ih tailWithin]

/-- A complete edge word that obeys the Rubik-cube flip parity constraint
remains a complete zero-flip-parity word after *any* allowed color relabeling. -/
theorem symmetry_preserves_both_edge_legality_conditions
    (sigma : List Nat) (hsigma : sigma ∈ symmetries)
    (word : Word)
    (complete : (wordLabels word).Perm (List.range 12))
    (evenFlips : flipBit word = 0) :
    (wordLabels (relabelEdgeWord sigma word)).Perm (List.range 12) ∧
      flipBit (relabelEdgeWord sigma word) = 0 := by
  constructor
  · exact symmetry_relabels_any_complete_edge_permutation
      sigma hsigma word complete
  · rw [symmetry_preserves_flipBit_for_all_complete_words
      sigma hsigma word complete, evenFlips]

/-- The two complete sticker color vectors of *every* legal edge word
transform exactly by the selected center-color symmetry. -/
theorem symmetry_relabels_both_edge_sticker_vectors
    (sigma : List Nat) (hsigma : sigma ∈ symmetries)
    (word : Word) (complete : (wordLabels word).Perm (List.range 12)) :
    (∀ side : Bool,
      (relabelEdgeWord sigma word).map (fun x => sticker x side) =
        (word.map (fun x => sticker x side)).map (fun c => sigma[c]!)) := by
  intro side
  exact symmetry_relabels_word_observation_vector sigma hsigma side word
    (complete_word_oriented_addresses_in_range word complete)

#print axioms every_symmetry_is_an_edge_type_permutation
#print axioms symmetry_relabels_any_complete_edge_permutation
#print axioms complete_word_oriented_addresses_in_range
#print axioms symmetry_relabels_word_observation_vector
#print axioms symmetry_preserves_both_edge_legality_conditions
#print axioms symmetry_relabels_both_edge_sticker_vectors

end CubeRev029.Nineteen
