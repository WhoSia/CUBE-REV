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

-- Full transcript correctness and pinned Lean compilation are pending.
end CubeRev029.Physical
