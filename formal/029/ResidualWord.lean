import EighteenReadData
import AdaptiveLowerBound

namespace CubeRev029.Eighteen

/-- Numeric label IDs are the ranks in the root order. Erasing labels
changes their consecutive ranks, but preserves this order. -/
def wordLabels (w : Word) : List Nat := w.map (· / 2)

inductive Agrees : List Nat → Word → Prop where
  | nil : Agrees [] []
  | cons {c id cs w} : (c = blank ∨ sticker id false = c) →
      Agrees cs w → Agrees (c :: cs) (id :: w)

structure Completes (p : Position) (w : Word) : Prop where
  labels : (wordLabels w).Perm p.labels
  sign : parity (wordLabels w) = p.sign
  flip : flipBit w = p.flip
  record : Agrees p.record w

abbrev Address := Nat × Bool

def observeWord (w : Word) (q : Address) : Nat :=
  sticker (w[q.1]?.getD 0) q.2

theorem agrees_length (h : Agrees cs w) : cs.length = w.length := by
  induction h with
  | nil => rfl
  | cons _ _ ih => simp [ih]

theorem agrees_lookup (h : Agrees cs w) (i c : Nat) (atColor : cs[i]? = some c)
    (read : c ≠ blank) : observeWord w (i, false) = c := by
  induction h generalizing i with
  | nil => simp at atColor
  | cons matchHead _ ih =>
      cases i with
      | zero =>
          simp at atColor
          subst c
          exact matchHead.resolve_left read
      | succ i => exact ih i atColor

theorem agrees_eraseIdx (h : Agrees cs w) (i : Nat) :
    Agrees (cs.eraseIdx i) (w.eraseIdx i) := by
  induction h generalizing i with
  | nil => exact .nil
  | cons h₁ h₂ ih =>
      cases i with
      | zero => exact h₂
      | succ i => exact .cons h₁ (ih i)

theorem agrees_insertIdx (h : Agrees cs w) (i c id : Nat)
    (matchHead : c = blank ∨ sticker id false = c) :
    Agrees (cs.insertIdx i c) (w.insertIdx i id) := by
  induction h generalizing i with
  | nil =>
      cases i with
      | zero => exact .cons matchHead .nil
      | succ i => exact .nil
  | cons h₁ h₂ ih =>
      cases i with
      | zero => exact .cons matchHead (.cons h₁ h₂)
      | succ i => exact .cons h₁ (ih i)

theorem agrees_update (h : Agrees cs w) (i c id : Nat)
    (matchHead : c = blank ∨ sticker id false = c) :
    Agrees (cs.set i c) (w.set i id) := by
  induction h generalizing i with
  | nil => exact .nil
  | cons h₁ h₂ ih =>
      cases i with
      | zero => exact .cons matchHead h₂
      | succ i => exact .cons h₁ (ih i)

theorem insertIdx_as_split (xs : List α) (i : Nat) (x : α) (bound : i ≤ xs.length) :
    xs.insertIdx i x = xs.take i ++ [x] ++ xs.drop i := by
  induction xs generalizing i with
  | nil =>
      have hi : i = 0 := by simpa using bound
      subst i
      rfl
  | cons a tail ih =>
      cases i with
      | zero => rfl
      | succ i =>
          simp only [List.insertIdx_succ_cons, List.take_succ_cons, List.drop_succ_cons,
            List.cons_append]
          rw [ih i (by simpa using bound)]

theorem map_insertIdx (xs : List α) (i : Nat) (x : α) (f : α → β) :
    (xs.insertIdx i x).map f = (xs.map f).insertIdx i (f x) := by
  induction xs generalizing i with
  | nil => cases i <;> rfl
  | cons a tail ih => cases i <;> simp [ih]

theorem map_eraseIdx (xs : List α) (i : Nat) (f : α → β) :
    (xs.eraseIdx i).map f = (xs.map f).eraseIdx i := by
  induction xs generalizing i with
  | nil => rfl
  | cons a tail ih => cases i <;> simp [ih]

theorem apply_flip_insertIdx (w : Word) (i id : Nat) (bound : i ≤ w.length) :
    flipBit (w.insertIdx i id) = (flipBit w + id % 2) % 2 := by
  rw [insertIdx_as_split w i id bound, flipBit_reinsert, List.take_append_drop]

theorem parity_insertIdx (xs : List Nat) (i rank : Nat) (bound : i ≤ xs.length)
    (missing : rank ∉ xs) :
    parity (xs.insertIdx i rank) =
      (parity xs + i + xs.countP (· < rank)) % 2 := by
  rw [insertIdx_as_split xs i rank bound]
  have split := List.take_append_drop i xs
  have absent : rank ∉ xs.take i := by
    intro present
    exact missing (List.mem_of_mem_take present)
  have sum := count_below_above (xs.take i) rank absent
  have smaller : xs.countP (· < rank) =
      (xs.take i).countP (· < rank) + (xs.drop i).countP (· < rank) := by
    conv => lhs; rw [← split, List.countP_append]
  have len : (xs.take i).length = i := by simp [List.length_take, Nat.min_eq_left bound]
  unfold parity
  rw [inversions_insert, split, smaller]
  rw [len] at sum
  omega

/-- Restores a deleted absolute slot. Reading the restored slot has a
constant outcome; all other queries pull back to a residual slot. -/
def insertRoute (i id : Nat) (q : Address) : Sum Nat Address :=
  if q.1 < i then .inr q
  else if q.1 = i then .inl (sticker id q.2)
  else .inr (q.1 - 1, q.2)

theorem observe_insertIdx (w : Word) (i id : Nat) (bound : i ≤ w.length) (q : Address) :
    observeWord (w.insertIdx i id) q = mappedColor observeWord w (insertRoute i id q) := by
  rcases q with ⟨j, side⟩
  simp only [observeWord, insertRoute, List.getElem?_insertIdx]
  split
  · rfl
  · split
    · rename_i eq
      subst j
      simp [mappedColor, bound]
    · rfl

theorem observe_invalid (w : Word) (q : Address) (outside : w.length ≤ q.1) :
    observeWord w q = sticker 0 q.2 := by
  simp [observeWord, List.getElem?_eq_none outside]

end CubeRev029.Eighteen
