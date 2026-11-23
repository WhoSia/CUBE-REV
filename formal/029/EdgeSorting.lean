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

/-- Lexicographic color then original-position comparison.
Equal observed colors remain separate because the eleven slot IDs are unique. -/
def elevenSlotLexLE (colorAt : Nat → Nat) (i j : Nat) : Bool :=
  decide (colorAt i < colorAt j ∨
    (colorAt i = colorAt j ∧ i ≤ j))

theorem eleven_slot_lex_trans (colorAt : Nat → Nat) (i j k : Nat)
    (hij : elevenSlotLexLE colorAt i j = true)
    (hjk : elevenSlotLexLE colorAt j k = true) :
    elevenSlotLexLE colorAt i k = true := by
  simp only [elevenSlotLexLE, decide_eq_true_eq] at hij hjk ⊢
  omega

theorem eleven_slot_lex_total (colorAt : Nat → Nat) (i j : Nat) :
    (elevenSlotLexLE colorAt i j ||
      elevenSlotLexLE colorAt j i) = true := by
  simp only [Bool.or_eq_true, elevenSlotLexLE, decide_eq_true_eq]
  omega

/-- This propositionally equivalent comparator makes the ordering law
explicit: equal color replies retain increasing original slot indices. -/
theorem eleven_slot_lex_matches_prior_comparator
    (colorAt : Nat → Nat) (i j : Nat) :
    elevenSlotLexLE colorAt i j =
      (if colorAt i == colorAt j then decide (i ≤ j)
       else decide (colorAt i ≤ colorAt j)) := by
  by_cases h : colorAt i = colorAt j
  · simp [elevenSlotLexLE, h]
  · have heq : (colorAt i < colorAt j) ↔
        (colorAt i ≤ colorAt j) := by omega
    simp [elevenSlotLexLE, h, heq]

def elevenStableSlotOrder (colorAt : Nat → Nat) : List Nat :=
  (List.range 11).mergeSort (elevenSlotLexLE colorAt)

/-- For *every* initial eleven-color transcript, not merely realizable
histograms, the chosen order is pairwise lexicographically sorted. This
completes the ordering-law premise of the deterministic prefix normalizer.
The global color-gauge selector and signed sector transport remain open. -/
theorem eleven_stable_slot_order_sorted (colorAt : Nat → Nat) :
    List.Pairwise
      (fun i j => elevenSlotLexLE colorAt i j = true)
      (elevenStableSlotOrder colorAt) := by
  simpa only [elevenStableSlotOrder] using
    (List.pairwise_mergeSort
      (eleven_slot_lex_trans colorAt)
      (eleven_slot_lex_total colorAt) (List.range 11))

#print axioms eleven_slot_lex_matches_prior_comparator
#print axioms eleven_stable_slot_order_sorted

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

/-- An in-range adjacent swap of the first eleven positions never
touches the extra unread twelfth edge position. This is a structural
list identity, independent of how the observed colors are encoded. -/
theorem adjacent_append_unread
    (i : Nat) (xs : List α) (unread : α)
    (bound : i + 1 < xs.length) :
    adjacent i (xs ++ [unread]) = adjacent i xs ++ [unread] := by
  induction i generalizing xs with
  | zero =>
      cases xs with
      | nil => simp at bound
      | cons a tail =>
          cases tail with
          | nil => simp at bound
          | cons b rest => rfl
  | succ i ih =>
      cases xs with
      | nil => simp at bound
      | cons a tail =>
          have inner : i + 1 < tail.length := by
            simp only [List.length_cons] at bound
            omega
          change a :: adjacent i (tail ++ [unread]) =
            a :: (adjacent i tail ++ [unread])
          exact congrArg (List.cons a) (ih tail inner)

/-- An entire bounded eleven-slot swap trace has the same property.
This is the required *list-level* extension to the previously unobserved
twelfth position, prior to constructing a twelve-slot inverse Equiv. -/
theorem adjTrace_append_unread
    (path : List Nat) (xs : List α) (unread : α)
    (bounds : ∀ i ∈ path, i + 1 < xs.length) :
    adjTrace path (xs ++ [unread]) = adjTrace path xs ++ [unread] := by
  induction path generalizing xs with
  | nil => rfl
  | cons i tail ih =>
      have bi : i + 1 < xs.length := bounds i (by simp)
      have bt : ∀ j ∈ tail, j + 1 < (adjacent i xs).length := by
        intro j hj
        rw [adjacent_length]
        exact bounds j (by simp [hj])
      simp only [adjTrace]
      rw [adjacent_append_unread i xs unread bi]
      exact ih (adjacent i xs) bt

/-- The certified stable prefix ordering extends to all twelve distinct
slot IDs with the unobserved last slot *fixed*, not swapped into the
eleven measured positions. The parity contribution is precisely the
eleven-slot sorting parity already certified in the original trace. -/
theorem eleven_slot_trace_fixes_unread_twelfth
    (colorAt : Nat → Nat) :
    ∃ path : List Nat,
      adjTrace path ((List.range 11) ++ [11]) =
        elevenStableSlotOrder colorAt ++ [11] ∧
      (∀ i ∈ path, i < 10) ∧
      path.length % 2 = parity (elevenStableSlotOrder colorAt) := by
  obtain ⟨path, ordered, _, bounds, parityWitness⟩ :=
    eleven_stable_slot_order_certified colorAt
  refine ⟨path, ?_, bounds, parityWitness⟩
  have bound : ∀ i ∈ path, i + 1 < (List.range 11).length := by
    intro i hi
    have h := bounds i hi
    simp only [List.length_range]
    omega
  rw [adjTrace_append_unread path (List.range 11) 11 bound]
  rw [ordered]

#print axioms adjacent_append_unread
#print axioms adjTrace_append_unread
#print axioms eleven_slot_trace_fixes_unread_twelfth


/-- The actual swap trace for a deterministic eleven-slot normalization
is also a valid swap trace on all twelve edge positions, whose last position
is fixed. Its inversion parity is the genuine FULL TWELVE-slot parity.
This closes the potential discrepancy between 11-list parity bookkeeping
and the 12-cubie sign convention of the frozen route_info algorithm. -/
theorem eleven_slot_trace_full_twelve_parity (colorAt : Nat → Nat) :
    ∃ path : List Nat,
      adjTrace path (List.range 12) =
        elevenStableSlotOrder colorAt ++ [11] ∧
      (∀ i ∈ path, i < 10) ∧
      parity (elevenStableSlotOrder colorAt ++ [11]) =
        parity (elevenStableSlotOrder colorAt) ∧
      path.length % 2 =
        parity (elevenStableSlotOrder colorAt ++ [11]) := by
  obtain ⟨path, routed, inRange, traceParity⟩ :=
    eleven_slot_trace_fixes_unread_twelfth colorAt
  have twelveRange : (List.range 11) ++ [11] = List.range 12 := by
    decide +kernel
  have fullRoute : adjTrace path (List.range 12) =
      elevenStableSlotOrder colorAt ++ [11] := by
    rw [← twelveRange]
    exact routed
  have bounds12 : ∀ i ∈ path, i + 1 < (List.range 12).length := by
    intro i hi
    have h := inRange i hi
    simp only [List.length_range]
    omega
  have parityEq := adjTrace_parity path (List.range 12)
    List.nodup_range bounds12
  rw [fullRoute] at parityEq
  have zero : parity (List.range 12) = 0 := by decide +kernel
  rw [zero] at parityEq
  refine ⟨path, fullRoute, inRange, ?_, ?_⟩ <;> omega

#print axioms eleven_slot_trace_full_twelve_parity


/-- An executable eleven-pass adjacent compare/swap schedule. Every index
is constructed as a Fin 10, so it cannot address the unread twelfth
edge, irrespective of the observed colors or earlier swaps. -/
def elevenBubbleSchedule : List (Fin 10) :=
  (List.range 11).flatMap (fun _ =>
    (List.range 10).map (fun i =>
      (⟨i % 10, Nat.mod_lt i (by decide)⟩ : Fin 10)))

/-- The executable comparison budget is exactly eleven complete sweeps
of ten observed-slot boundaries. This is a statement about scheduled
comparisons, not the number of swaps actually emitted. -/
theorem eleven_bubble_schedule_length :
    elevenBubbleSchedule.length = 110 := by
  decide +kernel

/-- Every boundary in the first eleven-slot prefix occurs eleven times
in the fixed schedule. No comparison addresses the twelfth unread edge.
The proof computes only the closed finite schedule, never a color input. -/
theorem eleven_bubble_schedule_boundary_multiplicity :
    ∀ i : Fin 10,
      (elevenBubbleSchedule.filter (fun j => j == i)).length = 11 := by
  decide +kernel

#print axioms eleven_bubble_schedule_length
#print axioms eleven_bubble_schedule_boundary_multiplicity

/-- Build an executable *candidate* trace from the eleven observed colors.
The current ordering is recomputed from its actual preceding swaps, so
each comparison is adaptive to the current position permutation. This
algorithm has not yet been proved equivalent to mergeSort's stable order. -/
def bubbleCandidateTrace11 (colorAt : Nat → Nat) : List (Fin 10) :=
  elevenBubbleSchedule.foldl
    (fun path i =>
      let current := adjTrace (path.map Fin.val) (List.range 11)
      if elevenSlotLexLE colorAt current[i.val + 1]! current[i.val]! then
        path ++ [i]
      else path)
    ([] : List (Fin 10))

def bubbleCandidatePath11 (colorAt : Nat → Nat) : List Nat :=
  (bubbleCandidateTrace11 colorAt).map Fin.val

/-- A single comparison of the *actual current order*; unlike the path
recorder this function applies the optional swap immediately. -/
def bubbleOrderStep (colorAt : Nat → Nat) (xs : List Nat)
    (i : Fin 10) : List Nat :=
  if elevenSlotLexLE colorAt xs[i.val + 1]! xs[i.val]! then
    adjacent i.val xs
  else xs

/-- The exact path-recording transition used by the executable candidate,
factored out to expose its list-level semantics. -/
def bubblePathStep (colorAt : Nat → Nat)
    (path : List (Fin 10)) (i : Fin 10) : List (Fin 10) :=
  let current := adjTrace (path.map Fin.val) (List.range 11)
  if elevenSlotLexLE colorAt current[i.val + 1]! current[i.val]! then
    path ++ [i]
  else path

/-- One recorded comparison has *exactly* the same replay semantics as
one immediate compare/exchange operation on the current eleven-slot list.
This does not assume the sequence eventually sorts. -/
theorem bubble_path_step_replay (colorAt : Nat → Nat)
    (path : List (Fin 10)) (i : Fin 10) :
    adjTrace ((bubblePathStep colorAt path i).map Fin.val)
      (List.range 11) =
    bubbleOrderStep colorAt
      (adjTrace (path.map Fin.val) (List.range 11)) i := by
  unfold bubblePathStep bubbleOrderStep
  split_ifs with h
  · simp only [List.map_append, List.map_cons, List.map_nil,
      adjTrace_append, adjTrace]
  · rfl

/-- Replay of *every prefix* of the original trace is equivalent to
folding the immediate compare/exchange operation in the same order.
The invariant quantifies over arbitrary schedules and preceding paths. -/
theorem bubble_fold_replay (colorAt : Nat → Nat) :
    ∀ (schedule : List (Fin 10)) (path : List (Fin 10)),
      adjTrace ((schedule.foldl (bubblePathStep colorAt) path).map Fin.val)
        (List.range 11) =
      schedule.foldl (bubbleOrderStep colorAt)
        (adjTrace (path.map Fin.val) (List.range 11)) := by
  intro schedule
  induction schedule with
  | nil =>
      intro path
      rfl
  | cons i rest ih =>
      intro path
      simp only [List.foldl_cons]
      rw [ih (bubblePathStep colorAt path i)]
      rw [bubble_path_step_replay]

#print axioms bubble_path_step_replay
#print axioms bubble_fold_replay

/-- The factored path step is definitionally the original recorder.
This equality guards against accidentally proving a theorem about a
different comparison routine than the production candidate. -/
theorem bubble_candidate_trace_is_fold (colorAt : Nat → Nat) :
    bubbleCandidateTrace11 colorAt =
      elevenBubbleSchedule.foldl (bubblePathStep colorAt) [] := by
  rfl

/-- The actual eleven-pass candidate's emitted path replays to the
result of an ordinary in-place comparison sweep. This is the intended
bridge from executable history to a loop-invariant sorting proof. -/
theorem bubble_candidate_replay_eq_direct_fold (colorAt : Nat → Nat) :
    adjTrace (bubbleCandidatePath11 colorAt) (List.range 11) =
      elevenBubbleSchedule.foldl (bubbleOrderStep colorAt) (List.range 11) := by
  rw [bubbleCandidatePath11, bubble_candidate_trace_is_fold]
  simpa only [List.map_nil, adjTrace] using
    bubble_fold_replay colorAt elevenBubbleSchedule []

/-- Each direct comparison preserves the multiset of original slot IDs. -/
theorem bubble_order_step_perm (colorAt : Nat → Nat)
    (xs : List Nat) (i : Fin 10) :
    (bubbleOrderStep colorAt xs i).Perm xs := by
  unfold bubbleOrderStep
  split_ifs
  · exact adjacent_perm i.val xs
  · exact List.Perm.refl xs

/-- Each direct comparison also preserves the number of slot IDs. -/
theorem bubble_order_step_length (colorAt : Nat → Nat)
    (xs : List Nat) (i : Fin 10) :
    (bubbleOrderStep colorAt xs i).length = xs.length := by
  exact (bubble_order_step_perm colorAt xs i).length_eq

#print axioms bubble_candidate_trace_is_fold
#print axioms bubble_candidate_replay_eq_direct_fold
#print axioms bubble_order_step_perm
#print axioms bubble_order_step_length

/-- A direct fold preserves the complete multiset for *any* finite
comparison schedule, including malformed or prematurely stopped
schedules. The eventual sortedness theorem is a separate obligation. -/
theorem bubble_direct_fold_perm (colorAt : Nat → Nat) :
    ∀ (schedule : List (Fin 10)) (xs : List Nat),
      (schedule.foldl (bubbleOrderStep colorAt) xs).Perm xs := by
  intro schedule
  induction schedule with
  | nil =>
      intro xs
      exact List.Perm.refl xs
  | cons i rest ih =>
      intro xs
      simp only [List.foldl_cons]
      exact (ih (bubbleOrderStep colorAt xs i)).trans
        (bubble_order_step_perm colorAt xs i)

/-- The direct version of the complete candidate conserves exactly
eleven original positions, independently of its eventual sortedness. -/
theorem bubble_candidate_direct_fold_perm (colorAt : Nat → Nat) :
    (elevenBubbleSchedule.foldl (bubbleOrderStep colorAt)
      (List.range 11)).Perm (List.range 11) := by
  exact bubble_direct_fold_perm colorAt elevenBubbleSchedule (List.range 11)

#print axioms bubble_direct_fold_perm
#print axioms bubble_candidate_direct_fold_perm

/-- Unlike a raw list of arbitrary Nat positions, the executable trace
has a proof that *every generated swap* stays in the first ten adjacent
boundaries. This is a type-theoretic guarantee, not a finite test. -/
theorem bubble_candidate_path_bounded (colorAt : Nat → Nat) :
    ∀ i ∈ bubbleCandidatePath11 colorAt, i < 10 := by
  intro i hi
  obtain ⟨j, _, rfl⟩ := List.mem_map.mp hi
  exact j.isLt

/-- Regardless of the still-open stable-sort equality, replaying this
concrete bounded path cannot move the unobserved twelfth list element. -/
theorem bubble_candidate_path_preserves_unread
    (colorAt : Nat → Nat) (unread : Nat) :
    adjTrace (bubbleCandidatePath11 colorAt)
      ((List.range 11) ++ [unread]) =
    adjTrace (bubbleCandidatePath11 colorAt)
      (List.range 11) ++ [unread] := by
  apply adjTrace_append_unread
  intro i hi
  have h := bubble_candidate_path_bounded colorAt i hi
  simp only [List.length_range]
  omega

#print axioms bubble_candidate_path_bounded
#print axioms bubble_candidate_path_preserves_unread


/-- Any sequence of adjacent swaps preserves the exact multiset of list
elements. This lemma requires no assumption about its comparator. -/
theorem adjTrace_perm (path : List Nat) (xs : List α) :
    (adjTrace path xs).Perm xs := by
  induction path generalizing xs with
  | nil => exact List.Perm.refl _
  | cons i rest ih =>
      exact (ih (adjacent i xs)).trans (adjacent_perm i xs)

/-- The comparison on DISTINCT slot indices is antisymmetric even when
the two observed sticker colors are identical. -/
theorem eleven_slot_lex_antisymm (colorAt : Nat → Nat) (i j : Nat)
    (hij : elevenSlotLexLE colorAt i j = true)
    (hji : elevenSlotLexLE colorAt j i = true) : i = j := by
  simp only [elevenSlotLexLE, decide_eq_true_eq] at hij hji
  omega

/-- For distinct original slot IDs, a reversed comparison that requests
a swap is a strict inversion: the forward comparison is false. This is
what makes identical observed colors safe, since the tie-breaker is the
original slot ID rather than the observed color alone. -/
theorem eleven_slot_lex_reverse_is_strict (colorAt : Nat → Nat)
    (i j : Nat) (distinct : i ≠ j)
    (reverse : elevenSlotLexLE colorAt j i = true) :
    elevenSlotLexLE colorAt i j = false := by
  cases forward : elevenSlotLexLE colorAt i j with
  | false => rfl
  | true =>
      exact (distinct
        (eleven_slot_lex_antisymm colorAt i j forward reverse)).elim

#print axioms eleven_slot_lex_reverse_is_strict

/-- The executable bubble trace always preserves all eleven original
slot IDs. This is independent of its as-yet-unproved final sortedness. -/
theorem bubble_candidate_order_perm (colorAt : Nat → Nat) :
    (adjTrace (bubbleCandidatePath11 colorAt) (List.range 11)).Perm
      (List.range 11) := by
  exact adjTrace_perm _ _

/-- The slot comparator is reflexive, including when a color occurs more
than once in the observed edge transcript. -/
theorem eleven_slot_lex_refl (colorAt : Nat → Nat) (i : Nat) :
    elevenSlotLexLE colorAt i i = true := by
  simp [elevenSlotLexLE]

/-- Local kernel proof of uniqueness of sorted permutations, avoiding
unavailable external sorted-permutation lemma names. A sorted list with
the same multiset is the same list under the antisymmetric slot order. -/
theorem eleven_sorted_permutations_unique (colorAt : Nat → Nat) :
    ∀ (xs ys : List Nat),
      xs.Perm ys →
      List.Pairwise (fun i j => elevenSlotLexLE colorAt i j = true) xs →
      List.Pairwise (fun i j => elevenSlotLexLE colorAt i j = true) ys →
      xs = ys := by
  intro xs
  induction xs with
  | nil =>
      intro ys hp _ _
      cases ys with
      | nil => rfl
      | cons b bs =>
          have lengthEq := hp.length_eq
          simp at lengthEq
  | cons a as ih =>
      intro ys hp hx hy
      cases ys with
      | nil =>
          have lengthEq := hp.length_eq
          simp at lengthEq
      | cons b bs =>
          cases hx with
          | cons hax hxTail =>
              cases hy with
              | cons hby hyTail =>
                  have hA : a ∈ b :: bs := hp.mem_iff.mp (by simp)
                  have hB : b ∈ a :: as := hp.mem_iff.mpr (by simp)
                  have leAB : elevenSlotLexLE colorAt a b = true := by
                    rcases List.mem_cons.mp hB with eq | mem
                    · subst b
                      exact eleven_slot_lex_refl colorAt a
                    · exact hax b mem
                  have leBA : elevenSlotLexLE colorAt b a = true := by
                    rcases List.mem_cons.mp hA with eq | mem
                    · subst a
                      exact eleven_slot_lex_refl colorAt b
                    · exact hby a mem
                  have same := eleven_slot_lex_antisymm colorAt a b leAB leBA
                  subst b
                  have tailPerm : as.Perm bs := List.Perm.cons_inv hp
                  have tailEq : as = bs := ih bs tailPerm hxTail hyTail
                  simp [tailEq]

/-- A precise verification gate for the executable algorithm: its
pairwise sortedness alone implies equality with the frozen canonical
mergeSort result, since full permutation preservation and antisymmetric
uniqueness have already been established independently. -/
theorem bubble_candidate_eq_stable_of_pairwise
    (colorAt : Nat → Nat)
    (sorted : List.Pairwise
      (fun i j => elevenSlotLexLE colorAt i j = true)
      (adjTrace (bubbleCandidatePath11 colorAt) (List.range 11))) :
    adjTrace (bubbleCandidatePath11 colorAt) (List.range 11) =
      elevenStableSlotOrder colorAt := by
  exact eleven_sorted_permutations_unique colorAt _ _
    ((bubble_candidate_order_perm colorAt).trans
      (eleven_stable_slot_order_perm colorAt))
    sorted
    (eleven_stable_slot_order_sorted colorAt)

#print axioms adjTrace_perm
#print axioms eleven_slot_lex_antisymm
#print axioms bubble_candidate_order_perm
#print axioms bubble_candidate_eq_stable_of_pairwise


/-! ### BG: universal correctness of the eleven-pass compare/exchange schedule

The proof below is generic in an abstract comparator `le` satisfying
`BubbleOrder`, and is then instantiated at `elevenSlotLexLE colorAt` for an
ARBITRARY `colorAt : Nat → Nat` (repeated colors included, because the
comparator breaks ties by original slot index). No finite enumeration of
`colorAt` is used. -/

/-- Index-based compare/exchange with an arbitrary comparator; for
`le := elevenSlotLexLE colorAt` this is `bubbleOrderStep` (see
`bubble_order_step_eq_step_n`). -/
def bubbleStepN (le : Nat → Nat → Bool) (xs : List Nat) (i : Nat) :
    List Nat :=
  if le xs[i + 1]! xs[i]! then adjacent i xs else xs

theorem bubble_order_step_eq_step_n (colorAt : Nat → Nat) (xs : List Nat)
    (i : Fin 10) :
    bubbleOrderStep colorAt xs i =
      bubbleStepN (elevenSlotLexLE colorAt) xs i.val := rfl

/-- One structural bubble pass: the running candidate `x` is carried to the
right; at each boundary the smaller element stays behind. -/
def bubbleCarry (le : Nat → Nat → Bool) (x : Nat) : List Nat → List Nat
  | [] => [x]
  | b :: t =>
      if le b x then b :: bubbleCarry le x t
      else x :: bubbleCarry le b t

def bubblePass (le : Nat → Nat → Bool) : List Nat → List Nat
  | [] => []
  | x :: t => bubbleCarry le x t

/-- `BubbleOrder le` collects exactly the comparator laws used below. -/
structure BubbleOrder (le : Nat → Nat → Bool) : Prop where
  refl : ∀ a, le a a = true
  trans : ∀ a b c, le a b = true → le b c = true → le a c = true
  total : ∀ a b, (le a b || le b a) = true
  antisymm : ∀ a b, le a b = true → le b a = true → a = b

/-- Apply a pass function `k` times (first application innermost). -/
def bubbleIter (f : List Nat → List Nat) : Nat → List Nat → List Nat
  | 0, xs => xs
  | k + 1, xs => bubbleIter f k (f xs)

theorem bubble_iter_succ_last (f : List Nat → List Nat) :
    ∀ (k : Nat) (xs : List Nat),
      bubbleIter f (k + 1) xs = f (bubbleIter f k xs) := by
  intro k
  induction k with
  | zero => intro xs; rfl
  | succ k ih =>
      intro xs
      exact ih (f xs)

theorem bubble_step_n_succ (le : Nat → Nat → Bool) (h : Nat)
    (ys : List Nat) (i : Nat) :
    bubbleStepN le (h :: ys) (i + 1) = h :: bubbleStepN le ys i := by
  have e1 : (h :: ys)[i + 1 + 1]! = ys[i + 1]! := by first | rfl | simp
  have e2 : (h :: ys)[i + 1]! = ys[i]! := by first | rfl | simp
  unfold bubbleStepN
  rw [e1, e2]
  by_cases hc : le ys[i + 1]! ys[i]! = true
  · rw [if_pos hc, if_pos hc] <;> first | rfl | simp [adjacent]
  · rw [if_neg hc, if_neg hc] <;> first | rfl | simp

theorem bubble_foldl_succ (le : Nat → Nat → Bool) (h : Nat) :
    ∀ (l : List Nat) (ys : List Nat),
      (l.map Nat.succ).foldl (bubbleStepN le) (h :: ys) =
        h :: l.foldl (bubbleStepN le) ys := by
  intro l
  induction l with
  | nil => intro ys; rfl
  | cons i rest ih =>
      intro ys
      have e : bubbleStepN le (h :: ys) (Nat.succ i) =
          h :: bubbleStepN le ys i := bubble_step_n_succ le h ys i
      simp only [List.map_cons, List.foldl_cons]
      rw [e]
      exact ih _

/-- The index sweep over `0, …, n-1` of a list of length `n+1` is exactly the
structural carry pass. This is the loop-to-recursion bridge. -/
theorem bubble_range_fold_eq_carry (le : Nat → Nat → Bool) :
    ∀ (n : Nat) (x : Nat) (t : List Nat), t.length = n →
      (List.range n).foldl (bubbleStepN le) (x :: t) = bubbleCarry le x t := by
  intro n
  induction n with
  | zero =>
      intro x t ht
      cases t with
      | nil => rfl
      | cons _ _ => simp at ht
  | succ n ih =>
      intro x t ht
      cases t with
      | nil => simp at ht
      | cons b t' =>
          have ht' : t'.length = n := by simpa using ht
          have e1 : (x :: b :: t')[0 + 1]! = b := by first | rfl | simp
          have e2 : (x :: b :: t')[0]! = x := by first | rfl | simp
          rw [List.range_succ_eq_map, List.foldl_cons]
          cases hb : le b x with
          | true =>
              have step : bubbleStepN le (x :: b :: t') 0 = b :: x :: t' := by
                unfold bubbleStepN
                rw [e1, e2, hb] <;> first | rfl | simp [adjacent]
              rw [step, bubble_foldl_succ, ih x t' ht']
              simp [bubbleCarry, hb]
          | false =>
              have step : bubbleStepN le (x :: b :: t') 0 = x :: b :: t' := by
                unfold bubbleStepN
                rw [e1, e2, hb] <;> first | rfl | simp
              rw [step, bubble_foldl_succ, ih b t' ht']
              simp [bubbleCarry, hb]

/-- One carry pass places a maximum last, and is a permutation. -/
theorem bubble_carry_max {le : Nat → Nat → Bool} (ho : BubbleOrder le) :
    ∀ (t : List Nat) (x : Nat),
      ∃ (ys : List Nat) (m : Nat),
        bubbleCarry le x t = ys ++ [m] ∧
        (ys ++ [m]).Perm (x :: t) ∧
        ∀ y ∈ ys, le y m = true := by
  intro t
  induction t with
  | nil =>
      intro x
      exact ⟨[], x, rfl, List.Perm.refl _, by simp⟩
  | cons b t ih =>
      intro x
      have dom_of : ∀ (ys : List Nat) (m : Nat) (l : List Nat),
          (ys ++ [m]).Perm l → (∀ y ∈ ys, le y m = true) →
          ∀ z ∈ l, le z m = true := by
        intro ys m l hp hd z hz
        have hz' := hp.mem_iff.mpr hz
        rcases List.mem_append.mp hz' with h | h
        · exact hd z h
        · have hzm : z = m := by simpa using h
          rw [hzm]
          exact ho.refl m
      cases hb : le b x with
      | true =>
          obtain ⟨ys, m, heq, hp, hd⟩ := ih x
          refine ⟨b :: ys, m, ?_, ?_, ?_⟩
          · simp [bubbleCarry, hb, heq]
          · exact (hp.cons b).trans (List.Perm.swap x b t)
          · intro y hy
            rcases List.mem_cons.mp hy with h | hy'
            · rw [h]
              exact ho.trans b x m hb (dom_of ys m _ hp hd x (by simp))
            · exact hd y hy'
      | false =>
          obtain ⟨ys, m, heq, hp, hd⟩ := ih b
          refine ⟨x :: ys, m, ?_, ?_, ?_⟩
          · simp [bubbleCarry, hb, heq]
          · exact hp.cons x
          · intro y hy
            rcases List.mem_cons.mp hy with h | hy'
            · rw [h]
              have hxb : le x b = true := by
                have ht := ho.total b x
                rw [hb] at ht
                simpa using ht
              exact ho.trans x b m hxb (dom_of ys m _ hp hd b (by simp))
            · exact hd y hy'

/-- A pairwise-sorted list is a fixed point of a pass. -/
theorem bubble_carry_of_pairwise {le : Nat → Nat → Bool}
    (ho : BubbleOrder le) :
    ∀ (t : List Nat) (x : Nat),
      List.Pairwise (fun a b => le a b = true) (x :: t) →
      bubbleCarry le x t = x :: t := by
  intro t
  induction t with
  | nil => intro x _; rfl
  | cons b t ih =>
      intro x hs
      rw [List.pairwise_cons] at hs
      obtain ⟨hx, hrest⟩ := hs
      have hxb : le x b = true := hx b (by simp)
      have hxt : List.Pairwise (fun a b => le a b = true) (x :: t) := by
        rw [List.pairwise_cons]
        exact ⟨fun a ha => hx a (List.mem_cons_of_mem _ ha),
          (List.pairwise_cons.mp hrest).2⟩
      cases hb : le b x with
      | true =>
          have e : x = b := ho.antisymm x b hxb hb
          have hih := ih x hxt
          subst e
          simp [bubbleCarry, hb, hih]
      | false =>
          simp [bubbleCarry, hb, ih b hrest]

/-- A pass leaves a sorted, dominating suffix untouched. -/
theorem bubble_carry_append_suffix {le : Nat → Nat → Bool}
    (ho : BubbleOrder le) (s : List Nat)
    (hs : List.Pairwise (fun a b => le a b = true) s) :
    ∀ (t : List Nat) (x : Nat),
      (∀ y ∈ x :: t, ∀ z ∈ s, le y z = true) →
      bubbleCarry le x (t ++ s) = bubbleCarry le x t ++ s := by
  intro t
  induction t with
  | nil =>
      intro x hd
      have hxs : List.Pairwise (fun a b => le a b = true) (x :: s) := by
        rw [List.pairwise_cons]
        exact ⟨fun z hz => hd x (by simp) z hz, hs⟩
      have hfix := bubble_carry_of_pairwise ho s x hxs
      simpa [bubbleCarry] using hfix
  | cons b t ih =>
      intro x hd
      have hd1 : ∀ y ∈ x :: t, ∀ z ∈ s, le y z = true := by
        intro y hy z hz
        apply hd y _ z hz
        simp only [List.mem_cons] at hy ⊢
        tauto
      have hd2 : ∀ y ∈ b :: t, ∀ z ∈ s, le y z = true := by
        intro y hy z hz
        apply hd y _ z hz
        simp only [List.mem_cons] at hy ⊢
        tauto
      cases hb : le b x with
      | true =>
          have hih := ih x hd1
          simp [bubbleCarry, hb, hih]
      | false =>
          have hih := ih b hd2
          simp [bubbleCarry, hb, hih]

theorem bubble_pass_perm {le : Nat → Nat → Bool} (ho : BubbleOrder le)
    (xs : List Nat) : (bubblePass le xs).Perm xs := by
  cases xs with
  | nil => exact List.Perm.refl _
  | cons x t =>
      obtain ⟨ys, m, heq, hp, _⟩ := bubble_carry_max ho t x
      show (bubbleCarry le x t).Perm (x :: t)
      rw [heq]
      exact hp

theorem bubble_pass_of_pairwise {le : Nat → Nat → Bool}
    (ho : BubbleOrder le) (xs : List Nat)
    (h : List.Pairwise (fun a b => le a b = true) xs) :
    bubblePass le xs = xs := by
  cases xs with
  | nil => rfl
  | cons x t => exact bubble_carry_of_pairwise ho t x h

/-- Sorted-suffix invariant: after `k` passes the last elements form a sorted
block dominating everything before them, and the unsorted prefix has
shrunk by at least `k`. -/
theorem bubble_iter_invariant {le : Nat → Nat → Bool}
    (ho : BubbleOrder le) (xs : List Nat) :
    ∀ k, ∃ pre suf : List Nat,
      bubbleIter (bubblePass le) k xs = pre ++ suf ∧
      List.Pairwise (fun a b => le a b = true) suf ∧
      (∀ p ∈ pre, ∀ s ∈ suf, le p s = true) ∧
      pre.length ≤ xs.length - k := by
  intro k
  induction k with
  | zero =>
      exact ⟨xs, [], by simp [bubbleIter], List.Pairwise.nil, by simp,
        by simp⟩
  | succ k ih =>
      obtain ⟨pre, suf, heq, hs, hd, hl⟩ := ih
      rw [bubble_iter_succ_last, heq]
      cases pre with
      | nil =>
          refine ⟨[], suf, ?_, hs, by simp, by simp⟩
          rw [List.nil_append]
          exact bubble_pass_of_pairwise ho suf hs
      | cons x t =>
          have hG := bubble_carry_append_suffix ho suf hs t x hd
          obtain ⟨ys, m, hm, hp, hdom⟩ := bubble_carry_max ho t x
          have hmem : ∀ z, z ∈ ys ++ [m] ↔ z ∈ x :: t :=
            fun z => hp.mem_iff
          have h1 : ys.length + 1 = t.length + 1 := by
            simpa using hp.length_eq
          have h2 : t.length + 1 ≤ xs.length - k := by simpa using hl
          refine ⟨ys, m :: suf, ?_, ?_, ?_, ?_⟩
          · show bubbleCarry le x (t ++ suf) = ys ++ m :: suf
            rw [hG, hm]
            simp
          · rw [List.pairwise_cons]
            refine ⟨fun s hs' => ?_, hs⟩
            exact hd m ((hmem m).mp (by simp)) s hs'
          · intro p hp' s hs'
            rcases List.mem_cons.mp hs' with h | h
            · rw [h]
              exact hdom p hp'
            · exact hd p ((hmem p).mp (by simp [hp'])) s h
          · omega

/-- After `xs.length` passes the whole list is sorted. -/
theorem bubble_iter_sorted {le : Nat → Nat → Bool} (ho : BubbleOrder le)
    (xs : List Nat) :
    List.Pairwise (fun a b => le a b = true)
      (bubbleIter (bubblePass le) xs.length xs) := by
  obtain ⟨pre, suf, heq, hs, _, hl⟩ := bubble_iter_invariant ho xs xs.length
  have hpre : pre = [] := by
    cases pre with
    | nil => rfl
    | cons a b => simp at hl
  rw [heq, hpre, List.nil_append]
  exact hs

theorem elevenSlotLexLE_order (colorAt : Nat → Nat) :
    BubbleOrder (elevenSlotLexLE colorAt) where
  refl := eleven_slot_lex_refl colorAt
  trans := fun a b c => eleven_slot_lex_trans colorAt a b c
  total := eleven_slot_lex_total colorAt
  antisymm := fun a b => eleven_slot_lex_antisymm colorAt a b

/-- One complete sweep of the executable schedule (same term as the body of
`elevenBubbleSchedule`). -/
def elevenBubblePass : List (Fin 10) :=
  (List.range 10).map (fun i =>
    (⟨i % 10, Nat.mod_lt i (by decide)⟩ : Fin 10))

theorem eleven_bubble_schedule_eq_passes :
    elevenBubbleSchedule =
      (List.range 11).flatMap (fun _ => elevenBubblePass) := rfl

theorem eleven_bubble_pass_vals :
    elevenBubblePass.map Fin.val = List.range 10 := by
  decide +kernel

theorem bubble_foldl_fin (colorAt : Nat → Nat) :
    ∀ (l : List (Fin 10)) (xs : List Nat),
      l.foldl (bubbleOrderStep colorAt) xs =
        (l.map Fin.val).foldl (bubbleStepN (elevenSlotLexLE colorAt)) xs := by
  intro l
  induction l with
  | nil => intro xs; rfl
  | cons i rest ih =>
      intro xs
      simp only [List.foldl_cons, List.map_cons]
      exact ih _

theorem bubble_foldl_flatMap_const {β : Type}
    (g : List Nat → β → List Nat) (P : List β) :
    ∀ (l : List Nat) (a : List Nat),
      (l.flatMap (fun _ => P)).foldl g a =
        bubbleIter (fun a => P.foldl g a) l.length a := by
  intro l
  induction l with
  | nil => intro a; rfl
  | cons x rest ih =>
      intro a
      rw [List.flatMap_cons, List.foldl_append, ih] <;> rfl

theorem bubble_pass_eq_fold (c : Nat → Nat → Bool) (xs : List Nat)
    (h : xs.length = 11) :
    (List.range 10).foldl (bubbleStepN c) xs = bubblePass c xs := by
  cases xs with
  | nil => simp at h
  | cons x t =>
      have ht : t.length = 10 := by simpa using h
      exact bubble_range_fold_eq_carry c 10 x t ht

theorem bubble_iter_congr (f g : List Nat → List Nat)
    (hfg : ∀ xs : List Nat, xs.length = 11 → f xs = g xs)
    (hg : ∀ xs : List Nat, xs.length = 11 → (g xs).length = 11) :
    ∀ (k : Nat) (xs : List Nat), xs.length = 11 →
      bubbleIter f k xs = bubbleIter g k xs := by
  intro k
  induction k with
  | zero => intro xs _; rfl
  | succ k ih =>
      intro xs hx
      show bubbleIter f k (f xs) = bubbleIter g k (g xs)
      rw [hfg xs hx]
      exact ih (g xs) (hg xs hx)

/-- The *direct* eleven-pass compare/exchange fold sorts the eleven slots,
for every `colorAt`. -/
theorem bubble_candidate_direct_fold_sorted (colorAt : Nat → Nat) :
    List.Pairwise (fun i j => elevenSlotLexLE colorAt i j = true)
      (elevenBubbleSchedule.foldl (bubbleOrderStep colorAt)
        (List.range 11)) := by
  have ho := elevenSlotLexLE_order colorAt
  have hlen : (List.range 11).length = 11 := by simp
  have hpass : ∀ xs : List Nat, xs.length = 11 →
      elevenBubblePass.foldl (bubbleOrderStep colorAt) xs =
        bubblePass (elevenSlotLexLE colorAt) xs := by
    intro xs hx
    rw [bubble_foldl_fin, eleven_bubble_pass_vals]
    exact bubble_pass_eq_fold _ xs hx
  have hcongr := bubble_iter_congr
    (fun a => elevenBubblePass.foldl (bubbleOrderStep colorAt) a)
    (bubblePass (elevenSlotLexLE colorAt)) hpass
    (fun xs hx => (bubble_pass_perm ho xs).length_eq.trans hx)
    11 (List.range 11) hlen
  rw [eleven_bubble_schedule_eq_passes, bubble_foldl_flatMap_const,
    List.length_range, hcongr]
  have key := bubble_iter_sorted ho (List.range 11)
  rw [List.length_range] at key
  exact key

#print axioms bubble_carry_max
#print axioms bubble_carry_of_pairwise
#print axioms bubble_carry_append_suffix
#print axioms bubble_iter_invariant
#print axioms bubble_iter_sorted
#print axioms bubble_range_fold_eq_carry
#print axioms bubble_candidate_direct_fold_sorted

/-- Executable fail-closed postcondition check: run the bounded candidate
trace, then decide whether its actual output is pairwise lexicographically
sorted by the same comparison used by the frozen mergeSort normalizer.
A false value does NOT authorize use of that candidate trace. -/
def bubbleCandidateSorted (colorAt : Nat → Nat) : Bool :=
  decide (List.Pairwise
    (fun i j => elevenSlotLexLE colorAt i j = true)
    (adjTrace (bubbleCandidatePath11 colorAt) (List.range 11)))

theorem bubble_candidate_sorted_of_check (colorAt : Nat → Nat)
    (h : bubbleCandidateSorted colorAt = true) :
    List.Pairwise
      (fun i j => elevenSlotLexLE colorAt i j = true)
      (adjTrace (bubbleCandidatePath11 colorAt) (List.range 11)) := by
  simpa [bubbleCandidateSorted] using h

/-- The exact sorting trace is returned only if its runtime postcondition
was checked. Unlike the existential witness, this is executable data. -/
def verifiedBubbleTrace? (colorAt : Nat → Nat) : Option (List Nat) :=
  if bubbleCandidateSorted colorAt then
    some (bubbleCandidatePath11 colorAt)
  else none

/-- No unchecked trace can escape the executable verifier. Every
successfully returned path is a bounded original-coordinate trace which
replays to the exact canonical stable order. This does NOT assert that
verification always succeeds on all input transcripts. -/
theorem verified_bubble_trace_sound
    (colorAt : Nat → Nat) (path : List Nat)
    (h : verifiedBubbleTrace? colorAt = some path) :
    adjTrace path (List.range 11) = elevenStableSlotOrder colorAt ∧
    (∀ i ∈ path, i < 10) := by
  cases hv : bubbleCandidateSorted colorAt with
  | false =>
      simp [verifiedBubbleTrace?, hv] at h
  | true =>
      simp [verifiedBubbleTrace?, hv] at h
      subst path
      exact ⟨bubble_candidate_eq_stable_of_pairwise colorAt
        (bubble_candidate_sorted_of_check colorAt hv),
        bubble_candidate_path_bounded colorAt⟩

#print axioms bubble_candidate_sorted_of_check
#print axioms verified_bubble_trace_sound

/-- UNIVERSAL TOTALITY (BG): for every `colorAt : Nat → Nat`, including
repeated colors, the executable eleven-pass candidate passes its own
acceptance check. -/
theorem bubble_candidate_sorted_total (colorAt : Nat → Nat) :
    bubbleCandidateSorted colorAt = true := by
  have hsorted : List.Pairwise
      (fun i j => elevenSlotLexLE colorAt i j = true)
      (adjTrace (bubbleCandidatePath11 colorAt) (List.range 11)) := by
    rw [bubble_candidate_replay_eq_direct_fold]
    exact bubble_candidate_direct_fold_sorted colorAt
  unfold bubbleCandidateSorted
  exact decide_eq_true hsorted

/-- The fail-closed interface never returns `none`. -/
theorem verified_bubble_trace_total (colorAt : Nat → Nat) :
    verifiedBubbleTrace? colorAt = some (bubbleCandidatePath11 colorAt) := by
  unfold verifiedBubbleTrace?
  rw [if_pos (bubble_candidate_sorted_total colorAt)]

/-- Unconditional normalization refinement: the executable bubble trace is a
bounded path replaying to the frozen canonical stable order. -/
theorem bubble_candidate_normalizes (colorAt : Nat → Nat) :
    adjTrace (bubbleCandidatePath11 colorAt) (List.range 11) =
        elevenStableSlotOrder colorAt ∧
      (∀ i ∈ bubbleCandidatePath11 colorAt, i < 10) :=
  verified_bubble_trace_sound colorAt _ (verified_bubble_trace_total colorAt)

#print axioms bubble_candidate_sorted_total
#print axioms verified_bubble_trace_total
#print axioms bubble_candidate_normalizes











#print axioms root_even_swap_path

end CubeRev029.Eighteen
