import EdgeCornerParityInduction
import EdgeSorting

namespace CubeRev029.Physical

open CubeRev029.Eighteen

set_option autoImplicit false
set_option maxRecDepth 16000
set_option maxHeartbeats 0

/-!
# Universal edge/corner sign coupling from the existing adjacent-swap proof

The previous CUBE-REV EdgeSorting formalization already proves three very
useful generic statements:

* permutation_has_adjTrace: every finite permutation has a bounded adjacent
  swap realization;
* adjTrace_parity: each such swap toggles inversion parity on distinct Nat
  labels;
* adjTrace_map: the same swap trace commutes with arbitrary relabeling.

Applying those results both to the distinct original piece IDs and to the
canonical slot indices proves the permutation-composition parity law, with
NO enumeration of 12! legal edge permutations or 8! corner permutations.

This candidate file has not been Lean-compiled in the current sandbox.
The finite source-geometry side has been independently tested in
scripts/check_turn_parity.py. Do not promote to a verified theorem before
pinned Lean CI and axiom inspection.
-/

/-- Generic parity under an arbitrary finite permutation of the *positions*.
The source labels and reference labels are both collision-free, and the
reference starts with even inversion parity. -/
theorem parity_reindex_of_even_reference
    {α : Type} {xs ys : List α} (permutation : xs.Perm ys)
    (f g : α → Nat)
    (distinctF : (xs.map f).Nodup)
    (distinctG : (xs.map g).Nodup)
    (evenG : parity (xs.map g) = 0) :
    parity (ys.map f) =
      (parity (xs.map f) + parity (ys.map g)) % 2 := by
  obtain ⟨path, routed, bounds⟩ := permutation_has_adjTrace permutation
  have boundsF : ∀ i ∈ path, i + 1 < (xs.map f).length := by
    simpa using bounds
  have boundsG : ∀ i ∈ path, i + 1 < (xs.map g).length := by
    simpa using bounds
  have pf := adjTrace_parity path (xs.map f) distinctF boundsF
  have pg := adjTrace_parity path (xs.map g) distinctG boundsG
  rw [← adjTrace_map f path xs, routed] at pf
  rw [← adjTrace_map g path xs, routed, evenG] at pg
  omega

/-- The twelve edge positions are exactly their own canonical source
indices; the generator's ordered source indices are the already checked
edgeTurnPieceList, without a second separately specified turn table. -/
theorem edge_source_indices_are_generator_labels (t : Turn) :
    (edgeSourceIndices t).map Fin.val = edgeTurnPieceList t := by
  rfl

/-- Generator action on the edge *piece* list is exactly a positional
reindex of the input piece identities; flips do not change piece labels. -/
theorem edge_action_piece_labels (t : Turn) (a : EdgeCoordinates) :
    edgePieceList (edgeAction t a) =
      (edgeSourceIndices t).map (fun i => a i / 2) := by
  simp [edgePieceList, edgeSourceIndices, edgeAction,
    List.map_map, orient_label]

/-- Full edge parity reindex theorem, restricted to physically possible
nonrepeated twelve-piece permutations. -/
theorem edge_parity_reindex_proved : EdgeParityReindexLaw := by
  intro t a legal
  have hdistinct :
      (canonicalEdgeSources.map (fun i => a i / 2)).Nodup := by
    exact legal.symm.nodup (by decide +kernel)
  have hcanonical : (canonicalEdgeSources.map Fin.val).Nodup := by
    decide +kernel
  have hzero : parity (canonicalEdgeSources.map Fin.val) = 0 := by
    decide +kernel
  have h := parity_reindex_of_even_reference
    (edge_source_indices_perm t).symm
    (fun i => a i / 2) Fin.val hdistinct hcanonical hzero
  rw [← edge_action_piece_labels t a,
    edge_source_indices_are_generator_labels] at h
  exact h

/-- The canonical corner source list is the existing physical turn-slot
ordering; no relabeling of corner positions is silently introduced. -/
theorem corner_sources_are_index_map (t : Turn) :
    cornerSources t = canonicalCornerSources.map (cornerSourceIndex t) := by
  rfl

/-- The actual corner generator labels use exactly the same source indices
as cornerAction, in the same initial-pose destination order. -/
theorem corner_source_indices_are_generator_labels (t : Turn) :
    (cornerSources t).map Fin.val = cornerTurnPieceList t := by
  rfl

/-- Orientation twists preserve the physical corner piece identity, so
cornerAction on a piece list is simply source-index reordering. -/
theorem corner_action_piece_labels (t : Turn) (a : CornerCoordinates) :
    (cornerPieceList (cornerAction t a)).map Fin.val =
      (cornerSources t).map (fun i => (cornerPieceFin (a i)).val) := by
  simp [cornerPieceList, cornerSources, canonicalCornerSources,
    cornerAction, cornerPieceFin_shifted, List.map_map]

/-- Full corner parity reindex theorem for genuine permutations of the
eight physical corner pieces. -/
theorem corner_parity_reindex_proved : CornerParityReindexLaw := by
  intro t a legal
  have hdistinct :
      (canonicalCornerSources.map
        (fun i => (cornerPieceFin (a i)).val)).Nodup := by
    have p := (legal.map Fin.val).symm.nodup (by decide +kernel)
    simpa [cornerPieceList, List.map_map, Function.comp_def] using p
  have hcanonical : (canonicalCornerSources.map Fin.val).Nodup := by
    decide +kernel
  have hzero : parity (canonicalCornerSources.map Fin.val) = 0 := by
    decide +kernel
  have h := parity_reindex_of_even_reference
    (corner_sources_perm t).symm
    (fun i => (cornerPieceFin (a i)).val) Fin.val
    hdistinct hcanonical hzero
  rw [← corner_action_piece_labels t a,
    corner_source_indices_are_generator_labels] at h
  exact h

/-- All legal lookup-order face-turn histories conserve equality of
physical twelve-edge and eight-corner permutation signs. -/
theorem physical_edge_corner_parity_agree_all_turn_words (turns : List Turn) :
    edgePermutationParity (edgeCoordinatesAlong turns) =
      cornerPermutationParity (coordinatesAlong turns) :=
  edge_corner_parity_coupling_all_turn_words
    edge_parity_reindex_proved corner_parity_reindex_proved turns

/-- Every reachable physical coloring has coherent edge/corner coordinate
witnesses with the SAME permutation sign. This is the physical parity
coupling needed by FrozenTerminalSignBridge, not a hidden parity sensor. -/
theorem reachable_has_parity_coupled_coordinates_unconditional
    (s : Coloring) (reachable : Reachable s) :
    ∃ (edges : EdgeCoordinates) (corners : CornerCoordinates),
      EdgesAgree edges s ∧
      CornersAgree corners s ∧
      (edgePieceList edges).Perm (canonicalEdgeSources.map Fin.val) ∧
      (cornerPieceList corners).Perm canonicalCornerSources ∧
      edgePermutationParity edges = cornerPermutationParity corners :=
  reachable_has_parity_coupled_coordinates
    edge_parity_reindex_proved corner_parity_reindex_proved s reachable

/-- Extract the original twelve oriented edge words in the same physical
position order as the frozen certificate's Word representation. -/
def originalPhysicalEdgeWord (turns : List Turn) : Word :=
  canonicalEdgeSources.map (edgeCoordinatesAlong turns)

/-- This is the *actual original* edge-word/physical-corner sign identity,
with no `legalCoupling` hypothesis. It follows from the proved all-turn
coupling and the exact id / 2 edge-word labeling convention.
The later normalization parity transport remains a separate obligation. -/
theorem original_physical_edge_word_sign_agrees_corner
    (turns : List Turn) :
    parity ((originalPhysicalEdgeWord turns).map (· / 2)) =
      cornerPermutationParity (coordinatesAlong turns) := by
  exact physical_edge_corner_parity_agree_all_turn_words turns

#print axioms original_physical_edge_word_sign_agrees_corner

#print axioms parity_reindex_of_even_reference
#print axioms edge_parity_reindex_proved
#print axioms corner_parity_reindex_proved
#print axioms physical_edge_corner_parity_agree_all_turn_words
#print axioms reachable_has_parity_coupled_coordinates_unconditional

#print axioms edge_source_indices_are_generator_labels
#print axioms edge_action_piece_labels
#print axioms corner_sources_are_index_map
#print axioms corner_source_indices_are_generator_labels
#print axioms corner_action_piece_labels

end CubeRev029.Physical
