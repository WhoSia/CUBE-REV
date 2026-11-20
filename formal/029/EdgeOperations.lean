import PhysicalEdgeWords
import EdgeSorting
import EdgeFlips

namespace CubeRev029.Physical

open Eighteen

def edgeSlot (i : Fin 12) (side : Bool) : Slot :=
  ⟨2*i.val + side.toNat, by have := i.isLt; have := Bool.toNat_le side; omega⟩

@[simp] theorem edgeSlot_cubie (i : Fin 12) (side : Bool) :
    (edgeSlot i side).val / 2 = i.val := by
  change (2*i.val + side.toNat) / 2 = i.val
  have := Bool.toNat_le side
  omega

@[simp] theorem edgeSlot_side (i : Fin 12) (side : Bool) :
    ((edgeSlot i side).val % 2 == 1) = side := by
  cases side <;> simp [edgeSlot] <;> omega

theorem edgeSlot_inside (i : Fin 12) (side : Bool) : (edgeSlot i side).val < 24 := by
  change 2*i.val + side.toNat < 24
  have := i.isLt
  have := Bool.toNat_le side
  omega

def adjSlot (i : Fin 11) (s : Slot) : Slot :=
  if edge : s.val < 24 then
    edgeSlot ⟨adjIndex i.val (s.val / 2), by
      unfold adjIndex
      have := i.isLt
      split <;> (try split) <;> omega⟩ (s.val % 2 == 1)
  else s

def flipSlot (i : Fin 12) (s : Slot) : Slot :=
  if s.val < 24 ∧ s.val / 2 = i.val then edgeSlot i (!(s.val % 2 == 1)) else s

def pairSwapWord (i j : Fin 11) : List Turn := pairSwapTable[11*i.val+j.val]!
def pairFlipWord (i j : Fin 12) : List Turn := pairFlipTable[12*i.val+j.val]!

/-- Every table entry is checked against the geometric face turns on all
48 slots, including all 24 corner stickers. -/
theorem pair_actions_match : pairSwapTable.size = 121 ∧ pairFlipTable.size = 144 ∧
    (∀ (i j : Fin 11) (s : Slot), follow (pairSwapWord i j) s = adjSlot j (adjSlot i s)) ∧
    (∀ (i j : Fin 12) (s : Slot), follow (pairFlipWord i j) s = flipSlot j (flipSlot i s)) := by
  native_decide

def encodeEdges (w : Word) : Coloring := fun s =>
  if s.val < 24 then observeWord w (s.val/2, s.val % 2 == 1) else solved s

theorem encode_on_edge (w : Word) (i : Fin 12) (side : Bool) :
    encodeEdges w (edgeSlot i side) = observeWord w (i.val, side) := by
  simp [encodeEdges, edgeSlot_inside]

theorem encode_adjacent (w : Word) (len : w.length = 12) (i : Fin 11) (s : Slot) :
    encodeEdges (adjacent i.val w) s = encodeEdges w (adjSlot i s) := by
  by_cases inside : s.val < 24
  · rw [encodeEdges, ite_eq_left inside]
    simp only [adjSlot, dite_eq_left inside, encode_on_edge, observeWord,
      get_adjacent w i.val (s.val / 2) (by have := i.isLt; omega)]
  · simp [encodeEdges, adjSlot, inside]

set_option maxRecDepth 10000 in
set_option maxHeartbeats 0 in
theorem encode_identity : encodeEdges ((List.range 12).map (2*·)) = solved := by
  funext s
  exact (show ∀ q : Slot, encodeEdges ((List.range 12).map (2*·)) q = solved q by decide +kernel) s

theorem reachable_adjacent_pair (w : Word) (len : w.length = 12)
    (r : Reachable (encodeEdges w)) (i j : Fin 11) :
    Reachable (encodeEdges (adjacent j.val (adjacent i.val w))) := by
  have result := paint_reachable _ r (pairSwapWord j i)
  have same : encodeEdges (adjacent j.val (adjacent i.val w)) =
      paint (pairSwapWord j i) (encodeEdges w) := by
    funext s
    rw [encode_adjacent _ ((adjacent_length i.val w).trans len),
      encode_adjacent _ len]
    exact congrArg (encodeEdges w) (pair_actions_match.2.2.1 j i s).symm
  rwa [same]

theorem encode_flipAt (w : Word) (len : w.length = 12) (i : Fin 12) (s : Slot) :
    encodeEdges (flipAt i.val w) s = encodeEdges w (flipSlot i s) := by
  by_cases inside : s.val < 24
  · by_cases eq : s.val / 2 = i.val
    · have bound : i.val < w.length := by rw [len]; exact i.isLt
      rw [flipSlot, ite_eq_left ⟨inside, eq⟩, encode_on_edge, encodeEdges, ite_eq_left inside]
      simp [observeWord, get_flipAt, eq, List.getElem?_eq_getElem bound, sticker_reverse]
    · simp [flipSlot, encodeEdges, inside, eq, observeWord, get_flipAt]
  · simp [flipSlot, encodeEdges, inside]

theorem reachable_flip_pair (w : Word) (len : w.length = 12)
    (r : Reachable (encodeEdges w)) (i j : Fin 12) :
    Reachable (encodeEdges (flipAt j.val (flipAt i.val w))) := by
  have same : encodeEdges (flipAt j.val (flipAt i.val w)) =
      paint (pairFlipWord j i) (encodeEdges w) := by
    funext s
    rw [encode_flipAt _ ((flipAt_length i.val w).trans len),
      encode_flipAt _ len]
    exact congrArg (encodeEdges w) (pair_actions_match.2.2.2 j i s).symm
  rw [same]
  exact paint_reachable _ r _

#print axioms pair_actions_match

end CubeRev029.Physical
