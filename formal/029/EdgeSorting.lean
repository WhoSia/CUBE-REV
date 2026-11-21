import ResidualWord
import Init.Data.List.Sort.Lemmas

namespace CubeRev029.Eighteen

def adjacent : Nat → List α → List α
  | 0, a::b::tail => b::a::tail
  | i+1, a::tail => a :: adjacent i tail
  | _, xs => xs

def adjTrace : List Nat → List α → List α
  | [], xs => xs
  | a::path, xs => adjTrace path (adjacent a xs)

theorem adjacent_perm (i : Nat) (xs : List α) : (adjacent i xs).Perm xs := by
  induction i generalizing xs with
  | zero =>
      cases xs with
      | nil => rfl
      | cons a tail => cases tail with
        | nil => rfl
        | cons b tail => exact .swap a b tail
  | succ i ih =>
      cases xs with
      | nil => rfl
      | cons a tail => exact (ih tail).cons a

theorem adjacent_length (i : Nat) (xs : List α) :
    (adjacent i xs).length = xs.length := (adjacent_perm i xs).length_eq

theorem adjTrace_append (a b : List Nat) (xs : List α) :
    adjTrace (a ++ b) xs = adjTrace b (adjTrace a xs) := by
  induction a generalizing xs with
  | nil => rfl
  | cons _ _ ih => exact ih _

theorem adjTrace_lift (a : α) (path : List Nat) (xs : List α) :
    adjTrace (path.map Nat.succ) (a :: xs) = a :: adjTrace path xs := by
  induction path generalizing xs with
  | nil => rfl
  | cons _ _ ih => exact ih _

/-- The standard permutation derivation supplies a word of adjacent swaps,
with every swap inside the original list. -/
theorem permutation_has_adjTrace (h : xs.Perm ys) :
    ∃ path, adjTrace path xs = ys ∧ ∀ i ∈ path, i+1 < xs.length := by
  induction h with
  | nil => exact ⟨[], rfl, by simp⟩
  | cons x _ ih =>
      obtain ⟨path, target, bounds⟩ := ih
      refine ⟨path.map Nat.succ, by rw [adjTrace_lift, target], ?_⟩
      intro i mem
      obtain ⟨j, hj, rfl⟩ := List.mem_map.mp mem
      have := bounds j hj
      simp only [List.length_cons]
      omega
  | swap a b rest =>
      refine ⟨[0], rfl, ?_⟩
      simp
  | trans first _ ih₁ ih₂ =>
      obtain ⟨a, ra, ba⟩ := ih₁
      obtain ⟨b, rb, bb⟩ := ih₂
      refine ⟨a ++ b, by rw [adjTrace_append, ra, rb], ?_⟩
      intro i mem
      rcases List.mem_append.mp mem with left | right
      · exact ba i left
      · simpa only [first.length_eq] using bb i right

theorem adjacent_parity (i : Nat) (xs : List Nat) (distinct : xs.Nodup)
    (bound : i+1 < xs.length) :
    parity (adjacent i xs) = (parity xs + 1) % 2 := by
  induction i generalizing xs with
  | zero =>
      cases xs with
      | nil => simp at bound
      | cons a tail =>
          cases tail with
          | nil => simp at bound
          | cons b tail =>
              have separate : a ≠ b := fun eq => (List.nodup_cons.mp distinct).1 (by simp [eq])
              simp only [adjacent, parity, inversions, List.countP_cons]
              by_cases less : a < b
              · have other : ¬ b < a := by omega
                simp [less, other]
                omega
              · have other : b < a := by omega
                simp [less, other]
                omega
  | succ i ih =>
      cases xs with
      | nil => simp at bound
      | cons a tail =>
          have inner : i + 1 < tail.length := by simp only [List.length_cons] at bound; omega
          have previous := ih tail (List.nodup_cons.mp distinct).2 inner
          have same := (adjacent_perm i tail).countP_eq (· < a)
          simp only [adjacent, parity, inversions, same] at previous ⊢
          omega

theorem adjTrace_parity (path : List Nat) (xs : List Nat) (distinct : xs.Nodup)
    (bounds : ∀ i ∈ path, i+1 < xs.length) :
    parity (adjTrace path xs) = (parity xs + path.length) % 2 := by
  induction path generalizing xs with
  | nil => simp [adjTrace, parity]
  | cons i tail ih =>
      have ix := bounds i (by simp)
      have inner := ih (adjacent i xs) ((adjacent_perm i xs).symm.nodup distinct)
        (by intro j mem; rw [adjacent_length]; exact bounds j (by simp [mem]))
      simp only [adjTrace, List.length_cons]
      rw [inner, adjacent_parity i xs distinct ix]
      omega

theorem root_even_swap_path {w : Word} (h : Completes (root 0) w) :
    ∃ path, adjTrace path (List.range 12) = wordLabels w ∧
      (∀ i ∈ path, i < 11) ∧ path.length % 2 = 0 := by
  have source : (List.range 12).Perm (wordLabels w) := h.labels.symm
  obtain ⟨path, output, bounds⟩ := permutation_has_adjTrace source
  refine ⟨path, output, ?_, ?_⟩
  · intro i mem
    have := bounds i mem
    simp only [List.length_range] at this
    omega
  · have sign := adjTrace_parity path (List.range 12) List.nodup_range bounds
    rw [output, h.sign] at sign
    have zero : parity (List.range 12) = 0 := by decide +kernel
    simpa [root, zero] using sign.symm

def adjIndex (i j : Nat) : Nat :=
  if j = i then i+1 else if j = i+1 then i else j

theorem get_adjacent (xs : List α) (i j : Nat) (bound : i+1 < xs.length) :
    (adjacent i xs)[j]? = xs[adjIndex i j]? := by
  induction i generalizing xs j with
  | zero =>
      cases xs with
      | nil => simp at bound
      | cons a tail =>
          cases tail with
          | nil => simp at bound
          | cons b tail =>
              cases j with
              | zero => rfl
              | succ j =>
                  cases j with
                  | zero => rfl
                  | succ j => simp [adjacent, adjIndex]
  | succ i ih =>
      cases xs with
      | nil => simp at bound
      | cons a tail =>
          cases j with
          | zero => rfl
          | succ j =>
              have step : i+1 < tail.length := by simp only [List.length_cons] at bound; omega
              have eq : adjIndex (i+1) (j+1) = adjIndex i j + 1 := by
                by_cases a : j = i <;> by_cases b : j = i+1 <;> simp [adjIndex, a, b]
              simp only [adjacent, List.getElem?_cons_succ, eq, ih tail j step]

theorem adjacent_map (f : α → β) (i : Nat) (xs : List α) :
    (adjacent i xs).map f = adjacent i (xs.map f) := by
  induction i generalizing xs with
  | zero =>
      cases xs with
      | nil => rfl
      | cons _ tail => cases tail <;> rfl
  | succ i ih => cases xs <;> simp [adjacent, ih]

theorem adjTrace_map (f : α → β) (path : List Nat) (xs : List α) :
    (adjTrace path xs).map f = adjTrace path (xs.map f) := by
  induction path generalizing xs with
  | nil => rfl
  | cons hd tl ih => simp [adjTrace, ih, adjacent_map]


/-- Applying the SAME legal adjacent-swap trace to any two distinct-label
lists preserves their relative inversion parity, irrespective of the list
length or the concrete labels. This is a generic transport lemma rather than
a certificate for the cube-specific stable-sort normalization. -/
theorem adjTrace_relative_parity_invariant
    (path : List Nat) (xs ys : List Nat)
    (hx : xs.Nodup) (hy : ys.Nodup)
    (sameLength : xs.length = ys.length)
    (bounds : ∀ i ∈ path, i + 1 < xs.length) :
    (parity (adjTrace path xs) + parity (adjTrace path ys)) % 2 =
      (parity xs + parity ys) % 2 := by
  have boundsY : ∀ i ∈ path, i + 1 < ys.length := by
    intro i hi
    rw [← sameLength]
    exact bounds i hi
  have px := adjTrace_parity path xs hx bounds
  have py := adjTrace_parity path ys hy boundsY
  omega

#print axioms adjTrace_relative_parity_invariant

/-- Relabeling and a shared position-swap trace commute. Consequently,
the parity *difference* introduced by a collision-free relabeling is
unchanged by any valid adjacent position-swap trace. Unlike finite
48-symmetry enumeration, this lemma quantifies over arbitrary relabeling
functions and arbitrary distinct input lists. It is conditional on the
relabeling staying injective over this particular list. -/
theorem adjTrace_relabel_parity_shift_invariant
    (path : List Nat) (f : Nat → Nat) (xs : List Nat)
    (originalDistinct : xs.Nodup)
    (relabeledDistinct : (xs.map f).Nodup)
    (bounds : ∀ i ∈ path, i + 1 < xs.length) :
    (parity ((adjTrace path xs).map f) +
       parity (adjTrace path xs)) % 2 =
      (parity (xs.map f) + parity xs) % 2 := by
  rw [adjTrace_map]
  exact adjTrace_relative_parity_invariant path (xs.map f) xs
    relabeledDistinct originalDistinct (by simp)
    (by simpa using bounds)

#print axioms adjTrace_relabel_parity_shift_invariant

/-- Every valid adjacent-transposition representation of the same
reordering has the same parity of swap count. This rules out a spurious
dependence on which adjacent-swap decomposition a stable-sort witness uses. -/
theorem adjTrace_equal_outputs_force_same_swap_parity
    (first second : List Nat) (xs : List Nat)
    (distinct : xs.Nodup)
    (firstBound : ∀ i ∈ first, i + 1 < xs.length)
    (secondBound : ∀ i ∈ second, i + 1 < xs.length)
    (sameOutput : adjTrace first xs = adjTrace second xs) :
    first.length % 2 = second.length % 2 := by
  have firstParity := adjTrace_parity first xs distinct firstBound
  have secondParity := adjTrace_parity second xs distinct secondBound
  rw [sameOutput] at firstParity
  omega

#print axioms adjTrace_equal_outputs_force_same_swap_parity

/-- An arbitrary reordering of the ELEVEN distinct observation-slot IDs
is witnessed by a bounded adjacent-swap trace, and its trace parity agrees
with the inversion parity of the final slot order. This theorem deliberately
uses unique position IDs, not the first colors (which may repeat). -/
theorem eleven_slot_reordering_has_parity_witness
    (order : List Nat) (valid : (List.range 11).Perm order) :
    ∃ path : List Nat,
      adjTrace path (List.range 11) = order ∧
      (∀ i ∈ path, i < 10) ∧
      path.length % 2 = parity order := by
  obtain ⟨path, output, bounds⟩ :=
    permutation_has_adjTrace valid
  refine ⟨path, output, ?_, ?_⟩
  · intro i hi
    have bound := bounds i hi
    simp only [List.length_range] at bound
    omega
  · have h := adjTrace_parity path (List.range 11)
      List.nodup_range bounds
    rw [output] at h
    have zero : parity (List.range 11) = 0 := by decide +kernel
    rw [zero] at h
    omega

#print axioms eleven_slot_reordering_has_parity_witness

/-- Every eleven-slot position reordering can be performed on its
actual repeated-color observations by the same adjacent swaps. Since the
position IDs remain unique, the resulting parity is unambiguous even if
the eleven observation colors contain repetitions. -/
theorem eleven_slot_colors_follow_position_witness
    (order : List Nat) (valid : (List.range 11).Perm order)
    (colorAt : Nat → Nat) :
    ∃ path : List Nat,
      adjTrace path (List.range 11) = order ∧
      adjTrace path ((List.range 11).map colorAt) =
        order.map colorAt ∧
      (∀ i ∈ path, i < 10) ∧
      path.length % 2 = parity order := by
  obtain ⟨path, output, bounds, parityWitness⟩ :=
    eleven_slot_reordering_has_parity_witness order valid
  refine ⟨path, output, ?_, bounds, parityWitness⟩
  rw [← adjTrace_map]
  rw [output]

#print axioms eleven_slot_colors_follow_position_witness

/-- Total, deterministic stable order of the eleven *unique position IDs*.
The comparison is lexicographic by observed color and then original position.
Using positions as tie-breakers avoids treating repeated colors as distinct. -/
def elevenStableSlotOrder (colorAt : Nat → Nat) : List Nat :=
  (List.range 11).mergeSort (fun i j =>
    if colorAt i == colorAt j then decide (i ≤ j)
    else decide (colorAt i ≤ colorAt j))

/-- This executable normalizer is genuinely a permutation of all eleven
distinct slots for every possible observation function, including repeated
color replies. No feasibility or posterior hypothesis is needed. -/
theorem eleven_stable_slot_order_perm (colorAt : Nat → Nat) :
    (List.range 11).Perm (elevenStableSlotOrder colorAt) := by
  exact (List.mergeSort_perm (List.range 11) _).symm

/-- Deterministic stable sorting has a real adjacent-swap witness; its
parity is exactly the inversion parity of the chosen position order, and
the *actual possibly repeated color vector* is transported by that same
witness. This proves the slot-order part only, not the full cube gauge
cocycle or the physical 19-frame policy. -/
theorem eleven_stable_slot_order_certified (colorAt : Nat → Nat) :
    ∃ path : List Nat,
      adjTrace path (List.range 11) = elevenStableSlotOrder colorAt ∧
      adjTrace path ((List.range 11).map colorAt) =
        (elevenStableSlotOrder colorAt).map colorAt ∧
      (∀ i ∈ path, i < 10) ∧
      path.length % 2 = parity (elevenStableSlotOrder colorAt) := by
  exact eleven_slot_colors_follow_position_witness
    (elevenStableSlotOrder colorAt)
    (eleven_stable_slot_order_perm colorAt) colorAt

#print axioms eleven_stable_slot_order_perm
#print axioms eleven_stable_slot_order_certified






#print axioms root_even_swap_path

end CubeRev029.Eighteen
