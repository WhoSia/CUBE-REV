import CornerTurnGenerators

namespace CubeRev029.Physical

open Eighteen

/-!
The bridge from the geometrical `Reachable` predicate to oriented corner
coordinates.  It proves existence and agreement with all 24 physical corner
sticker colors for arbitrary legal turn words.  Conserved piece/twist totals
are a separate, explicitly open proof obligation.
-/

def cornerSourceIndex (t : Turn) (i : Fin 8) : Fin 8 :=
  ⟨cornerTurnPiece t i, corner_turn_source_bounded t i⟩

def cornerTurnOffset (t : Turn) (i : Fin 8) : Fin 3 :=
  ⟨cornerTurnTwist t i, Nat.mod_lt _ (by decide)⟩

def cornerSourceLocalIndex (t : Turn) (i : Fin 8) (j : Fin 3) : Fin 3 :=
  ⟨((cornerTurnOffset t i).val + j.val) % 3, Nat.mod_lt _ (by decide)⟩

/-- A face turn acts on the three stickers of a corner as one cyclic
rotation of the same source cubie. -/
set_option maxRecDepth 16000 in
set_option maxHeartbeats 0 in
theorem corner_turn_slot_factors :
    ∀ t : Turn, ∀ i : Fin 8, ∀ j : Fin 3,
      turnSlot t (cornerRawSlot i j) =
        cornerRawSlot (cornerSourceIndex t i) (cornerSourceLocalIndex t i j) := by
  decide +kernel

/-- The `j`th sticker color of an oriented corner identity in the conventions
of `FaceTurns.lean`, which indexes each corner's three stickers cyclically. -/
def orientedCornerColor (x : Fin 24) (j : Fin 3) : Nat :=
  colorCode ((cornerNames[x.val / 3]!).toList)[(x.val % 3 + j.val) % 3]!

def shiftedCorner (x : Fin 24) (shift : Fin 3) : Fin 24 :=
  ⟨3 * (x.val / 3) + (x.val % 3 + shift.val) % 3, by
    have hx := x.isLt
    omega⟩

/-- Cyclic shifts compose for each of the twenty-four oriented corner
identities, independent of the other seven corners. -/
set_option maxRecDepth 16000 in
set_option maxHeartbeats 0 in
theorem oriented_color_shift :
    ∀ x : Fin 24, ∀ shift j : Fin 3,
      orientedCornerColor (shiftedCorner x shift) j =
        orientedCornerColor x
          ⟨(shift.val + j.val) % 3, Nat.mod_lt _ (by decide)⟩ := by
  decide +kernel

/-- The eight oriented cubies evolve by source permutation and local cyclic
shift.  This action is defined for *every* coordinate array. -/
def cornerAction (t : Turn) (a : CornerCoordinates) : CornerCoordinates :=
  fun i => shiftedCorner (a (cornerSourceIndex t i)) (cornerTurnOffset t i)

/-- A corner-coordinate array correctly labels all of the twenty-four
corner-sticker colors of a physical coloring, not just the fourteen read by
the identification policy. -/
def CornersAgree (a : CornerCoordinates) (s : Coloring) : Prop :=
  ∀ i : Fin 8, ∀ j : Fin 3,
    s (cornerRawSlot i j) = orientedCornerColor (a i) j

/-- Generator-level semantic agreement with the actual 48-sticker motion. -/
theorem corner_agreement_after_turn (a : CornerCoordinates) (s : Coloring)
    (h : CornersAgree a s) (t : Turn) :
    CornersAgree (cornerAction t a) (turnColoring t s) := by
  intro i j
  calc
    turnColoring t s (cornerRawSlot i j) =
        s (turnSlot t (cornerRawSlot i j)) := rfl
    _ = s (cornerRawSlot (cornerSourceIndex t i)
          (cornerSourceLocalIndex t i j)) := by
        rw [corner_turn_slot_factors t i j]
    _ = orientedCornerColor (a (cornerSourceIndex t i))
          (cornerSourceLocalIndex t i j) := h _ _
    _ = orientedCornerColor ((cornerAction t a) i) j := by
        exact (oriented_color_shift (a (cornerSourceIndex t i))
          (cornerTurnOffset t i) j).symm

/-- The solved cube assigns its own identity to each corner, with twist zero. -/
def solvedCornerCoordinates : CornerCoordinates :=
  fun i => ⟨3 * i.val, by have h := i.isLt; omega⟩

set_option maxRecDepth 16000 in
set_option maxHeartbeats 0 in
theorem solved_corner_agreement : CornersAgree solvedCornerCoordinates solved := by
  decide +kernel

/-- Compose the physical corner action along the same lookup-order turn list
as `paint`; there is no unproved reordering of the move sequence. -/
def coordinatesAlong : List Turn → CornerCoordinates
  | [] => solvedCornerCoordinates
  | t :: tail => cornerAction t (coordinatesAlong tail)

/-- Every *actual* face-turn history has oriented corner coordinates whose
colors agree with the twenty-four corner stickers in the resulting state. -/
theorem coordinatesAlong_agree (turns : List Turn) :
    CornersAgree (coordinatesAlong turns) (paint turns solved) := by
  induction turns with
  | nil => simpa [coordinatesAlong, paint] using solved_corner_agreement
  | cons t tail ih =>
      change CornersAgree (cornerAction t (coordinatesAlong tail))
        (turnColoring t (paint tail solved))
      exact corner_agreement_after_turn _ _ ih t

/-- Totality of the physical-to-corner-coordinate decoder on Reachable
colorings.  Next one must prove that the returned coordinates have a legal
piece permutation and twist-sum zero, before using the 14-color uniqueness
lemma as a whole-cube identification result. -/
theorem reachable_has_oriented_corners (s : Coloring) (h : Reachable s) :
    ∃ a : CornerCoordinates, CornersAgree a s := by
  obtain ⟨turns, rfl⟩ := h
  exact ⟨coordinatesAlong turns, coordinatesAlong_agree turns⟩

#print axioms corner_turn_slot_factors
#print axioms corner_agreement_after_turn
#print axioms coordinatesAlong_agree
#print axioms reachable_has_oriented_corners

end CubeRev029.Physical
