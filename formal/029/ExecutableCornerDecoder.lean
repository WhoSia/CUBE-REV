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

-- Source candidate: correctness and pinned Lean compilation are pending.
end CubeRev029.Physical
