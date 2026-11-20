import ResidualWord

namespace CubeRev029.Eighteen

/-- The known colors are returned directly. Every other second-read
transition deletes the now identified edge and translates both parities. -/
structure SecondStep (parent child : Position) (i fixed : Nat) : Prop where
  bound : i ≤ child.record.length
  labelPresent : fixed / 2 ∈ parent.labels
  distinctLabels : parent.labels.Nodup
  labels : child.labels = parent.labels.erase (fixed / 2)
  record : child.record.insertIdx i (sticker fixed false) = parent.record
  sign : (child.sign + i + child.labels.countP (· < fixed / 2)) % 2 = parent.sign
  flip : (child.flip + fixed % 2) % 2 = parent.flip

theorem SecondStep.lifts_legal {parent child : Position} {i fixed : Nat}
    (transition : SecondStep parent child i fixed) {w : Word} (h : Completes child w) :
    Completes parent (w.insertIdx i fixed) := by
  have inside : i ≤ w.length := Nat.le_trans transition.bound (Nat.le_of_eq (agrees_length h.record))
  have onLabels : i ≤ (wordLabels w).length := by simpa [wordLabels] using inside
  have remaining : (wordLabels w).Perm (parent.labels.erase (fixed / 2)) :=
    h.labels.trans (List.Perm.of_eq transition.labels)
  have noFixed : fixed / 2 ∉ wordLabels w := fun found =>
    transition.distinctLabels.not_mem_erase (remaining.mem_iff.mp found)
  have labelsRestored :
      wordLabels (w.insertIdx i fixed) = (wordLabels w).insertIdx i (fixed / 2) := by
    unfold wordLabels
    exact map_insertIdx w i fixed (· / 2)
  refine ⟨?_, ?_, ?_, ?_⟩
  · rw [labelsRestored]
    exact (List.perm_insertIdx _ _ onLabels).trans
      ((remaining.cons _).trans (List.perm_cons_erase transition.labelPresent).symm)
  · rw [labelsRestored, parity_insertIdx _ _ _ onLabels noFixed, h.sign,
      h.labels.countP_eq (· < fixed / 2)]
    exact transition.sign
  · rw [apply_flip_insertIdx w i fixed inside, h.flip, transition.flip]
  · rw [← transition.record]
    exact agrees_insertIdx h.record i (sticker fixed false) fixed (.inr rfl)

/-- A true second read has a universal semantic lift. Its output agreement,
membership and injectivity hold for arbitrary admissible residual words. -/
def SecondStep.asEdgeLift {parent child : Position} {i fixed : Nat}
    (transition : SecondStep parent child i fixed) :
    EdgeLift observeWord (Completes parent) (Completes child) (i, true) (sticker fixed true) where
  embed w := w.insertIdx i fixed
  query := insertRoute i fixed
  memory w h := by
    refine ⟨transition.lifts_legal h, ?_⟩
    rw [observe_insertIdx _ _ _ (Nat.le_trans transition.bound (Nat.le_of_eq (agrees_length h.record)))]
    simp [insertRoute, mappedColor]
  injective _ _ _ _ same := by
    have erasing := congrArg (fun w : Word => w.eraseIdx i) same
    simpa only [List.eraseIdx_insertIdx_self] using erasing
  compatible w h q :=
    observe_insertIdx w i fixed (Nat.le_trans transition.bound (Nat.le_of_eq (agrees_length h.record))) q

#print axioms SecondStep.asEdgeLift

end CubeRev029.Eighteen
