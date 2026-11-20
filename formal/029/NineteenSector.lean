import NineteenReadData
import ResidualWord

namespace CubeRev029.Nineteen

open Eighteen

private theorem first_colors_differ (id : Fin 12) :
    sticker (2 * id.val) false ≠ sticker (2 * id.val) true := by
  revert id
  decide +kernel

private theorem flipBit_cons (id : Nat) (w : Word) :
    flipBit (id :: w) = (id % 2 + flipBit w) % 2 := by
  simp [flipBit, Nat.add_mod]

/-- Every oriented assignment with the requested first colors and flip bit is
listed by the enumeration used at the root of an upper-bound policy. -/
theorem sector_complete (firstColors : List Nat) (unread : List Nat) (flip : Nat) (w : Word)
    (labels : (wordLabels w).Perm unread)
    (range : ∀ id ∈ unread, id < 12)
    (len : w.length = firstColors.length + 1)
    (orientation : flipBit w = flip)
    (colors : (w.take firstColors.length).map (fun id => sticker id false) = firstColors) :
    w ∈ sector unread flip firstColors := by
  induction firstColors generalizing unread flip w with
  | nil =>
      cases w with
      | nil => simp at len
      | cons head tail =>
          cases tail with
          | nil =>
              have single : unread = [head / 2] := by
                simpa [wordLabels] using labels.symm
              have headBit : head % 2 = flip := by
                simpa [flipBit] using orientation
              rw [single, ← headBit]
              have decomp : 2 * (head / 2) + head % 2 = head := by omega
              simp [sector, decomp]
          | cons second tail => simp at len
  | cons c cs ih =>
      cases w with
      | nil => simp at len
      | cons head tail =>
          let id := head / 2
          have labelsCons : (id :: wordLabels tail).Perm unread := labels
          have mem : id ∈ unread := labelsCons.mem_iff.mp (by simp)
          have tailLabels : (wordLabels tail).Perm (unread.erase id) := by
            simpa using labelsCons.erase id
          have tailRange (j : Nat) (member : j ∈ unread.erase id) : j < 12 :=
            range j (List.mem_of_mem_erase member)
          have tailLen : tail.length = cs.length + 1 := by simpa using len
          have hc : sticker head false = c := by simpa using congrArg List.head? colors
          have hcs : (tail.take cs.length).map (fun n => sticker n false) = cs := by
            simpa using congrArg List.tail colors
          have tailBit : flipBit tail < 2 := Nat.mod_lt _ (by decide)
          rw [flipBit_cons] at orientation
          change head :: tail ∈ (unread.flatMap _)
          apply List.mem_flatMap.mpr
          refine ⟨id, mem, ?_⟩
          by_cases even : head % 2 = 0
          · have heq : head = 2 * id := by dsimp [id]; omega
            have color : sticker (2*id) false = c := heq ▸ hc
            have flipEq : flipBit tail = flip := by omega
            rw [heq]
            simp only [color, beq_self_eq_true, ite_true, List.mem_map]
            exact ⟨tail, ih _ _ _ tailLabels tailRange tailLen flipEq hcs, rfl⟩
          · have odd : head % 2 = 1 := by omega
            have heq : head = 2 * id + 1 := by dsimp [id]; omega
            have color : sticker (2*id) true = c := by
              rw [← hc, heq]
              unfold sticker
              rw [show (2*id+1) / 2 = (2*id) / 2 by omega,
                show (2*id+1) % 2 = 1 by omega, show (2*id) % 2 = 0 by omega]
              rfl
            have off : sticker (2*id) false ≠ c := by
              rw [← color]
              exact first_colors_differ ⟨id, range id mem⟩
            have flipEq : flipBit tail = 1-flip := by omega
            rw [heq]
            simp only [off, beq_iff_eq, ite_false, color, ite_true, List.mem_map]
            exact ⟨tail, ih _ _ _ tailLabels tailRange tailLen flipEq hcs, rfl⟩

#print axioms sector_complete

end CubeRev029.Nineteen
