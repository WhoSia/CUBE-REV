import NineteenSchedule

namespace CubeRev029.Physical

set_option maxRecDepth 16000
set_option maxHeartbeats 0

open Eighteen

/-!
These are the *finite generator premises* required before one may lift the
fourteen-corner decoder to all `Reachable` colorings.  No conservation theorem
for arbitrary turn words is claimed by this file alone.

`turnSlot` is the lookup-order 48-sticker map defined from quarter-turn
geometry in `FaceTurns.lean`.  Every source index below is derived from that
same map, not from a separately hand-entered cubie-action table.
-/

def cornerRawSlot (i : Fin 8) (j : Fin 3) : Slot :=
  ⟨24 + 3 * i.val + j.val, by
    have hi := i.isLt
    have hj := j.isLt
    omega⟩

/-- The original, zero-based 24-corner-sticker source address that arrives at
corner position `i` and local sticker `j` after a quarter-turn. -/
def cornerTurnSource (t : Turn) (i : Fin 8) (j : Fin 3) : Nat :=
  (turnSlot t (cornerRawSlot i j)).val - 24

def cornerTurnPiece (t : Turn) (i : Fin 8) : Nat :=
  cornerTurnSource t i 0 / 3

def cornerTurnTwist (t : Turn) (i : Fin 8) : Nat :=
  cornerTurnSource t i 0 % 3

/-- Each of the eight destination corners gets one valid source corner. -/
theorem corner_turn_source_bounded :
    ∀ t : Turn, ∀ i : Fin 8, cornerTurnPiece t i < 8 := by
  decide +kernel

/-- No two destination corners can take the same original cubie. -/
theorem corner_turn_source_injective :
    ∀ t : Turn, ∀ i j : Fin 8,
      cornerTurnPiece t i = cornerTurnPiece t j → i = j := by
  decide +kernel

/-- The three local stickers of a cubie stay in cyclic order. This rules out
mirror-oriented triples, which cannot be encoded by an element of `Fin 24`. -/
theorem corner_turn_cyclic :
    ∀ t : Turn, ∀ i : Fin 8, ∀ j : Fin 3,
      cornerTurnSource t i j =
        3 * cornerTurnPiece t i + (cornerTurnTwist t i + j.val) % 3 := by
  decide +kernel

/-- Total corner-twist offset for one quarter-turn (the eight source pieces
are permuted, so the offsets are the only change to the twist sum modulo 3). -/
def cornerTurnOffsetTotal (t : Turn) : Nat :=
    cornerTurnTwist t 0 + cornerTurnTwist t 1 +
    cornerTurnTwist t 2 + cornerTurnTwist t 3 +
    cornerTurnTwist t 4 + cornerTurnTwist t 5 +
    cornerTurnTwist t 6 + cornerTurnTwist t 7

theorem corner_turn_zero_twist_offset :
    ∀ t : Turn, cornerTurnOffsetTotal t % 3 = 0 := by
  decide +kernel

def edgeTurnPiece (t : Turn) (i : Fin 12) : Nat :=
  (turnSlot t ⟨2 * i.val, by
    have h := i.isLt
    omega⟩).val / 2

def cornerTurnPieceList (t : Turn) : List Nat :=
  [cornerTurnPiece t 0, cornerTurnPiece t 1,
   cornerTurnPiece t 2, cornerTurnPiece t 3,
   cornerTurnPiece t 4, cornerTurnPiece t 5,
   cornerTurnPiece t 6, cornerTurnPiece t 7]

def edgeTurnPieceList (t : Turn) : List Nat :=
  [edgeTurnPiece t 0, edgeTurnPiece t 1,
   edgeTurnPiece t 2, edgeTurnPiece t 3,
   edgeTurnPiece t 4, edgeTurnPiece t 5,
   edgeTurnPiece t 6, edgeTurnPiece t 7,
   edgeTurnPiece t 8, edgeTurnPiece t 9,
   edgeTurnPiece t 10, edgeTurnPiece t 11]

/-- Each geometric face turn changes the corner and edge permutation signs
in precisely the same way. -/
theorem edge_corner_turn_sign_agree :
    ∀ t : Turn, parity (cornerTurnPieceList t) =
      parity (edgeTurnPieceList t) := by
  decide +kernel

#print axioms corner_turn_source_bounded
#print axioms corner_turn_source_injective
#print axioms corner_turn_cyclic
#print axioms corner_turn_zero_twist_offset
#print axioms edge_corner_turn_sign_agree

end CubeRev029.Physical
