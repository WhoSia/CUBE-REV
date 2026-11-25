import NineteenCornerTranscript
import ObservedTerminalParity

namespace CubeRev029.Physical

/-- Decode only from the charged record, never from a state witness. -/
def decodeScheduledCorners (replies : List Nat) : Option CornerCoordinates := do
  if replies.length != 19 then none else
    let slots : List (Nat × Nat) := [(0,1),(12,18),(2,3),(4,5),(10,11),(6,7),(8,9)]
    if !(replies.all (· < 6)) then none else
      if !(((replies.drop 13).take 5).all (· == replies[8]!)) then none else
        let observed ← slots.mapM fun (i,j) =>
          (List.finRange 24).find? fun x =>
            cornerCyclicPair x == (replies[i]!, replies[j]!)
        let pieces := observed.map cornerPiece
        if pieces.eraseDups.length != 7 then none else
          let total := pieces.sum
          if total > 28 then none else
            let p := 28 - total
            let t := (3 - (observed.map cornerTwist).sum % 3) % 3
            if h : 3*p+t < 24 then
              let missing : Fin 24 := ⟨3*p+t, h⟩
              let full := observed.take 5 ++ [missing] ++ observed.drop 5
              some (fun i => full[i.val]!)
            else none

def decodeScheduledTerminalParity (pre : List FrameColor)
    (replies : List Nat) : Option Nat :=
  (decodeScheduledCorners replies).map (observedTerminalCorrectedParity pre)

/-- Finite left inverse of the existing oriented-corner alphabet. -/
theorem scheduled_corner_pair_search_correct :
    ∀ x : Fin 24,
      (List.finRange 24).find? (fun y =>
        cornerCyclicPair y == cornerCyclicPair x) = some x := by
  decide +kernel

#print axioms scheduled_corner_pair_search_correct

/-- The arithmetic completion of the missing corner uses only conservation.
No search over full cube states is required. -/
theorem scheduled_corner_missing_arithmetic
    (p t sp st : Nat) (hp : p + sp = 28)
    (ht : (t + st) % 3 = 0) (bound : t < 3) :
    28 - sp = p ∧ (3 - st % 3) % 3 = t := by
  omega

#print axioms scheduled_corner_missing_arithmetic

/-- The charged transcript in coordinate form, in the exact frozen order. -/
theorem scheduled_corner_colors_of_agreement
    (a : CornerCoordinates) (s : Coloring) (h : CornersAgree a s) :
    scheduledCornerColors s =
      [orientedCornerColor (a 0) 0, orientedCornerColor (a 0) 1,
       orientedCornerColor (a 2) 0, orientedCornerColor (a 2) 1,
       orientedCornerColor (a 3) 0, orientedCornerColor (a 3) 1,
       orientedCornerColor (a 6) 0, orientedCornerColor (a 6) 1,
       orientedCornerColor (a 7) 0, orientedCornerColor (a 7) 1,
       orientedCornerColor (a 4) 0, orientedCornerColor (a 4) 1,
       orientedCornerColor (a 1) 0,
       orientedCornerColor (a 7) 0, orientedCornerColor (a 7) 0,
       orientedCornerColor (a 7) 0, orientedCornerColor (a 7) 0,
       orientedCornerColor (a 7) 0, orientedCornerColor (a 1) 1] := by
  have e0 := h 0 0
  have e1 := h 0 1
  have e2 := h 2 0
  have e3 := h 2 1
  have e4 := h 3 0
  have e5 := h 3 1
  have e6 := h 6 0
  have e7 := h 6 1
  have e8 := h 7 0
  have e9 := h 7 1
  have e10 := h 4 0
  have e11 := h 4 1
  have e12 := h 1 0
  have e18 := h 1 1
  change [s (cornerRawSlot 0 0), s (cornerRawSlot 0 1),
    s (cornerRawSlot 2 0), s (cornerRawSlot 2 1),
    s (cornerRawSlot 3 0), s (cornerRawSlot 3 1),
    s (cornerRawSlot 6 0), s (cornerRawSlot 6 1),
    s (cornerRawSlot 7 0), s (cornerRawSlot 7 1),
    s (cornerRawSlot 4 0), s (cornerRawSlot 4 1),
    s (cornerRawSlot 1 0), s (cornerRawSlot 7 0),
    s (cornerRawSlot 7 0), s (cornerRawSlot 7 0),
    s (cornerRawSlot 7 0), s (cornerRawSlot 7 0),
    s (cornerRawSlot 1 1)] = _
  rw [e0,e1,e2,e3,e4,e5,e6,e7,e8,e9,e10,e11,e12,e18]

theorem scheduled_corner_pair_matches_oriented :
    ∀ x : Fin 24,
      cornerCyclicPair x = (orientedCornerColor x 0, orientedCornerColor x 1) := by
  decide +kernel

theorem scheduled_corner_color_range :
    ∀ x : Fin 24, ∀ j : Fin 3, orientedCornerColor x j < 6 := by
  decide +kernel

#print axioms scheduled_corner_colors_of_agreement
#print axioms scheduled_corner_pair_matches_oriented
#print axioms scheduled_corner_color_range

-- Full transcript correctness and pinned Lean compilation are pending.
end CubeRev029.Physical
