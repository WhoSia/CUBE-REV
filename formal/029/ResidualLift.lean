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

/-- Recover the slot that acquired its first color. The other slots keep
their relative order. `side` specifies whether the color was read on the
reversed side in the parent. -/
structure FirstStep (parent child : Position) (i j : Nat) (side : Bool) (reply : Nat) : Prop where
  childSlot : j < child.record.length
  parentSlot : i ≤ (child.record.eraseIdx j).length
  color : child.record[j]? = some reply
  nonblank : reply ≠ blank
  record : (child.record.eraseIdx j).insertIdx i blank = parent.record
  labels : child.labels = parent.labels
  distinctLabels : child.labels.Nodup
  sign : (child.sign + i + j) % 2 = parent.sign
  flip : (child.flip + side.toNat) % 2 = parent.flip

def restoreFirst (i j : Nat) (side : Bool) (w : Word) : Word :=
  (w.eraseIdx j).insertIdx i (orient side (w[j]?.getD 0))

def firstRoute (i j : Nat) (side : Bool) (q : Address) : Sum Nat Address :=
  if q.1 = i then .inr (j, q.2 != side)
  else .inr (eraseRoute j (if q.1 < i then q else (q.1 - 1, q.2)))

theorem FirstStep.child_bound {p child : Position} {i j side reply}
    (step : FirstStep p child i j side reply) (h : Completes child w) : j < w.length := by
  rw [← agrees_length h.record]
  exact step.childSlot

theorem FirstStep.parent_bound {p child : Position} {i j side reply}
    (step : FirstStep p child i j side reply) (h : Completes child w) :
    i ≤ (w.eraseIdx j).length := by
  have eq := agrees_length (agrees_eraseIdx h.record j)
  rw [← eq]
  exact step.parentSlot

theorem FirstStep.lifts_legal {p child : Position} {i j side reply}
    (transition : FirstStep p child i j side reply) {w : Word} (h : Completes child w) :
    Completes p (restoreFirst i j side w) := by
  let t := w.eraseIdx j
  let id := w[j]?.getD 0
  let label := id / 2
  have readBound := transition.child_bound h
  have oldBound : j ≤ t.length := by simp [t, List.length_eraseIdx_of_lt readBound]; omega
  have newBound : i ≤ t.length := transition.parent_bound h
  have restore : t.insertIdx j id = w := by
    dsimp [t, id]
    rw [List.getElem?_eq_getElem readBound]
    exact restore_erased w j readBound
  have oldLabels : (wordLabels t).insertIdx j label = wordLabels w := by
    change (t.map (· / 2)).insertIdx j (id / 2) = w.map (· / 2)
    rw [← map_insertIdx, restore]
  have newLabels :
      wordLabels (restoreFirst i j side w) = (wordLabels t).insertIdx i label := by
    simp only [restoreFirst, wordLabels, map_insertIdx, orient_label, id, t, label]
  have oldLen : j ≤ (wordLabels t).length := by simpa [wordLabels] using oldBound
  have newLen : i ≤ (wordLabels t).length := by simpa [wordLabels] using newBound
  have oldPerm : (label :: wordLabels t).Perm (wordLabels w) := by
    rw [← oldLabels]
    exact (List.perm_insertIdx _ _ oldLen).symm
  have noLabel : label ∉ wordLabels t := by
    have nd := oldPerm.symm.nodup (h.labels.symm.nodup transition.distinctLabels)
    exact (List.nodup_cons.mp nd).1
  refine ⟨?_, ?_, ?_, ?_⟩
  · rw [newLabels, ← transition.labels]
    exact (List.perm_insertIdx _ _ newLen).trans (oldPerm.trans h.labels)
  · rw [newLabels, parity_insertIdx _ _ _ newLen noLabel, ← transition.sign, ← h.sign,
      ← oldLabels, parity_insertIdx _ _ _ oldLen noLabel]
    omega
  · change flipBit (t.insertIdx i (orient side id)) = p.flip
    rw [apply_flip_insertIdx _ _ _ newBound, orient_flip, ← transition.flip, ← h.flip,
      ← restore, apply_flip_insertIdx _ _ _ oldBound]
    omega
  · rw [← transition.record]
    exact agrees_insertIdx (agrees_eraseIdx h.record j) i blank (orient side id) (.inl rfl)

theorem observe_restoreFirst (w : Word) (i j : Nat) (side : Bool)
    (bound : i ≤ (w.eraseIdx j).length) (q : Address) :
    observeWord (restoreFirst i j side w) q = mappedColor observeWord w (firstRoute i j side q) := by
  rw [restoreFirst, observe_insertIdx _ _ _ bound]
  rcases q with ⟨k, b⟩
  by_cases e : k = i
  · subst k
    simp [insertRoute, firstRoute, mappedColor, sticker_orient, observeWord]
  · by_cases l : k < i
    · simp [insertRoute, firstRoute, mappedColor, e, l, observe_eraseIdx]
    · simp [insertRoute, firstRoute, mappedColor, e, l, observe_eraseIdx]

def FirstStep.asEdgeLift {parent child : Position} {i j : Nat} {side : Bool} {reply : Nat}
    (transition : FirstStep parent child i j side reply) :
    EdgeLift observeWord (Completes parent) (Completes child) (i, side) reply where
  embed := restoreFirst i j side
  query := firstRoute i j side
  memory w h := by
    refine ⟨transition.lifts_legal h, ?_⟩
    rw [observe_restoreFirst _ _ _ _ (transition.parent_bound h)]
    simpa [firstRoute, mappedColor] using
      agrees_lookup h.record j reply transition.color transition.nonblank
  injective s t hs ht same := by
    have eqErase := congrArg (fun w : Word => w.eraseIdx i) same
    simp only [restoreFirst, List.eraseIdx_insertIdx_self] at eqErase
    have eqAt := congrArg (fun w : Word => w[i]?) same
    simp [restoreFirst, List.getElem?_insertIdx_self,
      transition.parent_bound hs, transition.parent_bound ht] at eqAt
    have eqId := congrArg (orient side) eqAt
    simp only [orient_involution] at eqId
    have sb := transition.child_bound hs
    have tb := transition.child_bound ht
    simp only [List.getElem?_eq_getElem sb, List.getElem?_eq_getElem tb, Option.getD_some] at eqId
    rw [← restore_erased s j sb, ← restore_erased t j tb, eqErase, eqId]
  compatible w h q := observe_restoreFirst w i j side (transition.parent_bound h) q

#print axioms SecondStep.asEdgeLift
#print axioms FirstStep.asEdgeLift

end CubeRev029.Eighteen
