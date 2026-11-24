import EdgeOperations
import CornerPermutation

namespace CubeRev029.Physical

open CubeRev029.Eighteen

set_option autoImplicit false
set_option maxRecDepth 16000
set_option maxHeartbeats 0

/-!
# A physical twelve-edge coordinate action, derived from the actual sticker geometry

This is the edge analogue of ReachableCornerCoordinates.lean.  The first
sticker of a destination edge determines the source edge piece and whether
its two local stickers were exchanged; the second sticker factorization is
certified against all twelve actual quarter-turns and all twelve positions.

No parity coupling theorem is assumed here.  The purpose of this file is
to supply a physical edge-coordinate witness on every Reachable coloring.
-/

/-- The actual source edge identity for a quarter-turn, extracted from the
existing 48-sticker geometry rather than a duplicated hand-entered table. -/
def edgeSourceIndex (t : Turn) (i : Fin 12) : Fin 12 :=
  ⟨edgeTurnPiece t i, by
    have bounded : ∀ t : Turn, ∀ i : Fin 12,
        edgeTurnPiece t i < 12 := by decide +kernel
    exact bounded t i⟩

/-- Whether a physical quarter-turn reverses the two ordered stickers
of the edge source feeding position i. -/
def edgeSourceFlip (t : Turn) (i : Fin 12) : Bool :=
  (turnSlot t (edgeSlot i false)).val % 2 == 1

/-- The actual turn maps the destination sticker to this source-side bit. -/
def edgeSourceSide (t : Turn) (i : Fin 12) (side : Bool) : Bool :=
  side != edgeSourceFlip t i

/-- All 288 generator/position/side cases are checked directly against
the same turnSlot function used in physical routing. -/
theorem edge_turn_slot_factors :
    ∀ t : Turn, ∀ i : Fin 12, ∀ side : Bool,
      turnSlot t (edgeSlot i side) =
        edgeSlot (edgeSourceIndex t i) (edgeSourceSide t i side) := by
  decide +kernel

/-- An oriented edge coordinate stores the original encoded sticker pair
as a Nat (0..23 on Reachable states).  No extra orientation information
is supplied from outside the physical coloring. -/
abbrev EdgeCoordinates := Fin 12 → Nat

/-- Lookup-order quarter-turn action on oriented edge IDs.  The original
orientation word is changed only when its source sticker pair is reversed. -/
def edgeAction (t : Turn) (a : EdgeCoordinates) : EdgeCoordinates :=
  fun i => orient (edgeSourceFlip t i) (a (edgeSourceIndex t i))

/-- Exact colors of both stickers of each edge in the original pose. -/
def EdgesAgree (a : EdgeCoordinates) (s : Coloring) : Prop :=
  ∀ i : Fin 12, ∀ side : Bool,
    s (edgeSlot i side) = sticker (a i) side

/-- This is an equality of all actual edge-sticker colors, not merely
an equality of piece-label sets. -/
theorem edge_agreement_after_turn
    (a : EdgeCoordinates) (s : Coloring)
    (h : EdgesAgree a s) (t : Turn) :
    EdgesAgree (edgeAction t a) (turnColoring t s) := by
  intro i side
  calc
    turnColoring t s (edgeSlot i side) =
        s (turnSlot t (edgeSlot i side)) := rfl
    _ = s (edgeSlot (edgeSourceIndex t i)
          (edgeSourceSide t i side)) := by
          rw [edge_turn_slot_factors t i side]
    _ = sticker (a (edgeSourceIndex t i))
          (edgeSourceSide t i side) := h _ _
    _ = sticker ((edgeAction t a) i) side := by
          exact (sticker_orient (edgeSourceFlip t i)
            side (a (edgeSourceIndex t i))).symm

/-- Solved-position edge identity i has oriented encoded word 2*i. -/
def solvedEdgeCoordinates : EdgeCoordinates := fun i => 2 * i.val

theorem solved_edge_agreement : EdgesAgree solvedEdgeCoordinates solved := by
  unfold EdgesAgree
  decide +kernel

/-- The recursion order is exactly the lookup-order turn list used by
paint and by the existing corner coordinates. -/
def edgeCoordinatesAlong : List Turn → EdgeCoordinates
  | [] => solvedEdgeCoordinates
  | t :: tail => edgeAction t (edgeCoordinatesAlong tail)

theorem edge_coordinates_along_agree (turns : List Turn) :
    EdgesAgree (edgeCoordinatesAlong turns) (paint turns solved) := by
  induction turns with
  | nil =>
      change EdgesAgree solvedEdgeCoordinates solved
      exact solved_edge_agreement
  | cons t tail ih =>
      change EdgesAgree (edgeAction t (edgeCoordinatesAlong tail))
        (turnColoring t (paint tail solved))
      exact edge_agreement_after_turn _ _ ih t

/-- Every physically Reachable coloring has an edge-coordinate witness
whose 24 edge stickers agree with all original observed edge colors. -/
theorem reachable_has_oriented_edges (s : Coloring) (h : Reachable s) :
    ∃ a : EdgeCoordinates, EdgesAgree a s := by
  obtain ⟨turns, rfl⟩ := h
  exact ⟨edgeCoordinatesAlong turns, edge_coordinates_along_agree turns⟩

/-- Canonical order of physical edge destination positions. -/
def canonicalEdgeSources : List (Fin 12) :=
  [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

def edgeSourceIndices (t : Turn) : List (Fin 12) :=
  canonicalEdgeSources.map (edgeSourceIndex t)

/-- Every physical quarter-turn maps the twelve destination edges to
all twelve source pieces exactly once. -/
theorem edge_source_indices_perm :
    ∀ t : Turn, (edgeSourceIndices t).Perm canonicalEdgeSources := by
  decide +kernel

/-- Ordered original edge identities (not an unordered multiset).
The formula agrees with the word parity convention, id / 2. -/
def edgePieceList (a : EdgeCoordinates) : List Nat :=
  canonicalEdgeSources.map (fun i => a i / 2)

/-- The generator action permutes the source piece multiset even for
arbitrary arrays.  On legal arrays this is an honest permutation. -/
theorem edge_piece_list_action_perm (t : Turn) (a : EdgeCoordinates) :
    (edgePieceList (edgeAction t a)).Perm (edgePieceList a) := by
  have hp := (edge_source_indices_perm t).map (fun i => a i / 2)
  simpa [edgePieceList, edgeSourceIndices, List.map_map,
    edgeAction, orient_label, Function.comp_def] using hp

/-- The solved cube contains precisely pieces 0 through 11. -/
theorem solved_edge_piece_list :
    edgePieceList solvedEdgeCoordinates =
      canonicalEdgeSources.map Fin.val := by
  decide +kernel

/-- Reachability preserves the twelve-piece multiset; this statement
is weaker than, and must not be mistaken for, parity coupling. -/
theorem edge_coordinates_along_piece_perm (turns : List Turn) :
    (edgePieceList (edgeCoordinatesAlong turns)).Perm
      (canonicalEdgeSources.map Fin.val) := by
  induction turns with
  | nil =>
      change (edgePieceList solvedEdgeCoordinates).Perm
        (canonicalEdgeSources.map Fin.val)
      rw [solved_edge_piece_list]
  | cons t tail ih =>
      change (edgePieceList (edgeAction t
        (edgeCoordinatesAlong tail))).Perm
          (canonicalEdgeSources.map Fin.val)
      exact (edge_piece_list_action_perm t
        (edgeCoordinatesAlong tail)).trans ih

/-- Both the exact original edge labeling and its 12-piece permutation
are realized by the SAME physical turn word. -/
theorem reachable_has_permutation_edges (s : Coloring) (h : Reachable s) :
    ∃ a : EdgeCoordinates,
      EdgesAgree a s ∧
      (edgePieceList a).Perm (canonicalEdgeSources.map Fin.val) := by
  obtain ⟨turns, rfl⟩ := h
  exact ⟨edgeCoordinatesAlong turns,
    edge_coordinates_along_agree turns,
    edge_coordinates_along_piece_perm turns⟩

#print axioms edge_turn_slot_factors
#print axioms edge_agreement_after_turn
#print axioms edge_coordinates_along_agree
#print axioms reachable_has_oriented_edges
#print axioms edge_source_indices_perm
#print axioms edge_piece_list_action_perm
#print axioms edge_coordinates_along_piece_perm
#print axioms reachable_has_permutation_edges

#print axioms solved_edge_agreement
#print axioms solved_edge_piece_list

end CubeRev029.Physical
