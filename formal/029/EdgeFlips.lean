import ResidualWord

namespace CubeRev029.Eighteen

def flipAt : Nat → Word → Word
  | 0, a::tail => reverseWord a :: tail
  | i+1, a::tail => a :: flipAt i tail
  | _, [] => []

def flipTrace : List Nat → Word → Word
  | [], w => w
  | i::path, w => flipTrace path (flipAt i w)

theorem flipAt_length (i : Nat) (w : Word) : (flipAt i w).length = w.length := by
  induction i generalizing w with
  | zero => cases w <;> rfl
  | succ i ih => cases w <;> simp [flipAt, ih]

theorem get_flipAt (w : Word) (i j : Nat) :
    (flipAt i w)[j]? = if j = i then w[j]?.map reverseWord else w[j]? := by
  induction i generalizing w j with
  | zero =>
      cases w with
      | nil => simp [flipAt]
      | cons a tail => cases j <;> simp [flipAt]
  | succ i ih =>
      cases w with
      | nil => simp [flipAt]
      | cons a tail =>
          cases j with
          | zero => rfl
          | succ j => simpa [flipAt] using ih tail j

theorem flipTrace_lift (a : Nat) (path : List Nat) (w : Word) :
    flipTrace (path.map Nat.succ) (a::w) = a :: flipTrace path w := by
  induction path generalizing w with
  | nil => rfl
  | cons _ _ ih => exact ih _

def unflipped (w : Word) : Word := w.map (fun a => 2 * (a/2))

theorem orientation_trace (w : Word) :
    ∃ path, flipTrace path (unflipped w) = w ∧ (∀ i ∈ path, i < w.length) ∧
      path.length = (w.map (· % 2)).sum := by
  induction w with
  | nil => exact ⟨[], rfl, by simp, rfl⟩
  | cons a tail ih =>
      obtain ⟨path, after, bounds, size⟩ := ih
      by_cases turned : a % 2 = 1
      · refine ⟨0 :: path.map Nat.succ, ?_, ?_, ?_⟩
        · have restored : reverseWord (2 * (a/2)) = a := by unfold reverseWord; omega
          change flipTrace (path.map Nat.succ)
            (reverseWord (2 * (a/2)) :: unflipped tail) = a :: tail
          rw [flipTrace_lift, restored, after]
        · intro i mem
          rcases List.mem_cons.mp mem with p | p
          · simp [p]
          · obtain ⟨j, hj, rfl⟩ := List.mem_map.mp p
            simpa using bounds j hj
        · simp [size, turned, Nat.add_comm]
      · refine ⟨path.map Nat.succ, ?_, ?_, ?_⟩
        · have unchanged : 2 * (a/2) = a := by omega
          change flipTrace (path.map Nat.succ) (2 * (a/2) :: unflipped tail) = a :: tail
          rw [flipTrace_lift, unchanged, after]
        · intro i mem
          obtain ⟨j, hj, rfl⟩ := List.mem_map.mp mem
          simpa using bounds j hj
        · have zero : a % 2 = 0 := by omega
          simp [size, zero]

theorem root_even_flip_path {w : Word} (h : Completes (root 0) w) :
    ∃ path, flipTrace path (unflipped w) = w ∧
      (∀ i ∈ path, i < w.length) ∧ path.length % 2 = 0 := by
  obtain ⟨path, after, bounds, len⟩ := orientation_trace w
  refine ⟨path, after, bounds, ?_⟩
  rw [len]
  exact h.flip

theorem unflipped_is_label_embedding (w : Word) :
    unflipped w = (wordLabels w).map (2*·) := by
  simp [unflipped, wordLabels, List.map_map, Function.comp_def]

#print axioms root_even_flip_path

end CubeRev029.Eighteen
