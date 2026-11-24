import NineteenReadData
import ResidualWord
import PrefixColorGauge

namespace CubeRev029.Nineteen

open Eighteen

set_option autoImplicit false

/-- BS-1: the first sticker of an oriented edge value is the omitted-edge
enumeration's sticker for its label, with the orientation bit as the side. -/
theorem sticker_split (e : Nat) :
    sticker e false = sticker (2 * (e / 2)) (decide (e % 2 = 1)) := by
  unfold sticker
  have h1 : (2 * (e / 2)) / 2 = e / 2 := by omega
  have h2 : (2 * (e / 2)) % 2 = 0 := by omega
  rw [h1, h2]
  rcases Nat.mod_two_eq_zero_or_one e with h | h <;> simp [h]

theorem mem_rawWords_cons {id : Nat} {ids : List Nat} {r : List Nat} :
    r ∈ rawWords (id :: ids) ↔
      ∃ b t, t ∈ rawWords ids ∧ r = sticker (2 * id) b :: t := by
  simp only [rawWords, List.mem_append, List.mem_map]
  constructor
  · rintro (⟨t, ht, rfl⟩ | ⟨t, ht, rfl⟩)
    · exact ⟨false, t, ht, rfl⟩
    · exact ⟨true, t, ht, rfl⟩
  · rintro ⟨b, t, ht, rfl⟩
    cases b
    · exact Or.inl ⟨t, ht, rfl⟩
    · exact Or.inr ⟨t, ht, rfl⟩

/-- Reordering the omitted-edge label list only permutes the enumerated rows. -/
theorem rawWords_perm {l1 l2 : List Nat} (h : l1.Perm l2) :
    ∀ r ∈ rawWords l1, ∃ r' ∈ rawWords l2, r.Perm r' := by
  induction h with
  | nil => intro r hr; exact ⟨r, hr, List.Perm.refl _⟩
  | cons x _ ih =>
      intro r hr
      rw [mem_rawWords_cons] at hr
      obtain ⟨b, t, ht, rfl⟩ := hr
      obtain ⟨t', ht', hp⟩ := ih t ht
      exact ⟨_, mem_rawWords_cons.2 ⟨b, t', ht', rfl⟩, hp.cons _⟩
  | swap x y l =>
      intro r hr
      rw [mem_rawWords_cons] at hr
      obtain ⟨b, t, ht, rfl⟩ := hr
      rw [mem_rawWords_cons] at ht
      obtain ⟨c, u, hu, rfl⟩ := ht
      exact ⟨_, mem_rawWords_cons.2
        ⟨c, _, mem_rawWords_cons.2 ⟨b, u, hu, rfl⟩, rfl⟩,
        List.Perm.swap _ _ _⟩
  | trans _ _ ih1 ih2 =>
      intro r hr
      obtain ⟨r1, h1, p1⟩ := ih1 r hr
      obtain ⟨r2, h2, p2⟩ := ih2 r1 h1
      exact ⟨r2, h2, p1.trans p2⟩

/-- Every word's first-sticker row is enumerated for its own label list. -/
theorem first_sticker_row_enumerated (ws : List Nat) :
    ws.map (fun e => sticker e false) ∈ rawWords (ws.map (· / 2)) := by
  induction ws with
  | nil => simp [rawWords]
  | cons e ws ih =>
      rw [List.map_cons, List.map_cons, mem_rawWords_cons]
      exact ⟨decide (e % 2 = 1), _, ih, by rw [sticker_split e]⟩

theorem counts_perm {xs ys : List Nat} (h : xs.Perm ys) : counts xs = counts ys := by
  unfold counts
  apply List.map_congr_left
  intro c _
  exact (h.filter _).length_eq

/-- BS obligation 1. For EVERY complete legal edge word `ws ++ [x]`, the
histogram of the first eleven first-stickers equals the histogram of a row
of `rawWords` over the twelve labels with the last label omitted. This is
exactly the family inserted into `representativeVectors`. -/
theorem first_eleven_histogram_represented (ws : List Nat) (x : Nat)
    (complete : (wordLabels (ws ++ [x])).Perm (List.range 12)) :
    ∃ omitted ∈ List.range 12,
      ∃ row ∈ rawWords ((List.range 12).erase omitted),
        counts (ws.map (fun e => sticker e false)) = counts row := by
  have hp : (wordLabels ws ++ [x / 2]).Perm (List.range 12) := by
    simpa [wordLabels] using complete
  have h1 : (x / 2 :: wordLabels ws).Perm (List.range 12) :=
    (List.perm_append_comm (l₁ := [x / 2]) (l₂ := wordLabels ws)).trans hp
  have hmem : x / 2 ∈ List.range 12 :=
    hp.subset (List.mem_append_right _ (List.mem_singleton_self _))
  have h2 : (wordLabels ws).Perm ((List.range 12).erase (x / 2)) :=
    List.Perm.cons_inv (h1.trans (List.perm_cons_erase hmem))
  have enum : ws.map (fun e => sticker e false) ∈ rawWords (wordLabels ws) :=
    first_sticker_row_enumerated ws
  obtain ⟨r', hr', hperm⟩ := rawWords_perm h2 _ enum
  exact ⟨x / 2, hmem, r', hr', counts_perm hperm⟩

#print axioms first_eleven_histogram_represented

/-! ### BS-2: `lexLess` is a strict total order on equal-length histograms -/

theorem lexLess_irrefl : ∀ a : List Nat, ¬ lexLess a a = true := by
  intro a
  induction a with
  | nil => simp [lexLess]
  | cons x xs ih =>
      intro h
      simp [lexLess] at h
      exact ih h

theorem lexLess_trans : ∀ (a b c : List Nat),
    lexLess a b = true → lexLess b c = true → lexLess a c = true
  | [], [], _, h1, _ => by simp [lexLess] at h1
  | [], _ :: _, [], _, h2 => by simp [lexLess] at h2
  | [], _ :: _, _ :: _, _, _ => by simp [lexLess]
  | _ :: _, [], _, h1, _ => by simp [lexLess] at h1
  | _ :: _, _ :: _, [], _, h2 => by simp [lexLess] at h2
  | x :: xs, y :: ys, z :: zs, h1, h2 => by
      simp only [lexLess, Bool.or_eq_true, Bool.and_eq_true,
        decide_eq_true_eq, beq_iff_eq] at h1 h2 ⊢
      have ih := lexLess_trans xs ys zs
      rcases h1 with h1 | ⟨h1, h1'⟩ <;> rcases h2 with h2 | ⟨h2, h2'⟩
      · exact Or.inl (by omega)
      · exact Or.inl (by omega)
      · exact Or.inl (by omega)
      · exact Or.inr ⟨by omega, ih h1' h2'⟩

theorem lexLess_trichotomy : ∀ a b : List Nat, a.length = b.length →
    a = b ∨ lexLess a b = true ∨ lexLess b a = true := by
  intro a
  induction a with
  | nil =>
      intro b hlen
      cases b with
      | nil => exact Or.inl rfl
      | cons y ys => simp at hlen
  | cons x xs ih =>
      intro b hlen
      cases b with
      | nil => simp at hlen
      | cons y ys =>
          have hl : xs.length = ys.length := by simpa using hlen
          rcases Nat.lt_trichotomy x y with h | h | h
          · exact Or.inr (Or.inl (by simp [lexLess, h]))
          · subst h
            rcases ih ys hl with h' | h' | h'
            · subst h'; exact Or.inl rfl
            · exact Or.inr (Or.inl (by simp [lexLess, h']))
            · exact Or.inr (Or.inr (by simp [lexLess, h']))
          · exact Or.inr (Or.inr (by simp [lexLess, h]))

/-- The strict-improvement fold used by BOTH `representativeVectors` and
`choosePrefixGauge` returns an element no member (initial value included)
strictly beats. Only the strict order laws above are used; ties are not
resolved here. -/
theorem foldl_lex_min {α : Type} (f : α → List Nat)
    (hlen : ∀ x y, (f x).length = (f y).length) :
    ∀ (L : List α) (b : α),
      (L.foldl (fun best c => if lexLess (f c) (f best) = true then c else best) b = b ∨
        L.foldl (fun best c => if lexLess (f c) (f best) = true then c else best) b ∈ L) ∧
      ∀ d ∈ b :: L, ¬ lexLess (f d)
        (f (L.foldl (fun best c => if lexLess (f c) (f best) = true then c else best) b)) = true := by
  intro L
  induction L with
  | nil =>
      intro b
      refine ⟨Or.inl rfl, ?_⟩
      intro d hd
      have hdb : d = b := by simpa using hd
      subst hdb
      exact lexLess_irrefl _
  | cons c L ih =>
      intro b
      simp only [List.foldl_cons]
      by_cases hc : lexLess (f c) (f b) = true
      · rw [if_pos hc]
        obtain ⟨h1, h2⟩ := ih c
        refine ⟨?_, ?_⟩
        · rcases h1 with h1 | h1
          · exact Or.inr (List.mem_cons.2 (Or.inl h1))
          · exact Or.inr (List.mem_cons_of_mem _ h1)
        · intro d hd
          rcases List.mem_cons.1 hd with rfl | hd'
          · intro hlt
            exact h2 c (List.mem_cons_self ..) (lexLess_trans _ _ _ hc hlt)
          · rcases List.mem_cons.1 hd' with rfl | hd''
            · exact h2 d (List.mem_cons_self ..)
            · exact h2 d (List.mem_cons_of_mem _ hd'')
      · rw [if_neg hc]
        obtain ⟨h1, h2⟩ := ih b
        refine ⟨h1.imp id (List.mem_cons_of_mem _), ?_⟩
        intro d hd
        rcases List.mem_cons.1 hd with rfl | hd'
        · exact h2 d (List.mem_cons_self ..)
        · rcases List.mem_cons.1 hd' with rfl | hd''
          · intro hlt
            rcases lexLess_trichotomy (f b) (f d) (hlen _ _) with h | h | h
            · rw [h] at h2
              exact h2 b (List.mem_cons_self ..) hlt
            · exact h2 b (List.mem_cons_self ..) (lexLess_trans _ _ _ h hlt)
            · exact hc h
          · exact h2 d (List.mem_cons_of_mem _ hd'')

#print axioms foldl_lex_min

end CubeRev029.Nineteen

namespace CubeRev029.Physical

open Eighteen

set_option autoImplicit false

theorem symmetries_in_frozen_route :
    ∀ sigma ∈ Nineteen.symmetries, sigma ∈ frozenRouteOrderedColorMaps := by
  decide +kernel

/-- BS obligation 2 (minimality half). The EXECUTABLE gauge choice attains
the least histogram over all 48 symmetries: no symmetry's prefix histogram
is lexicographically below the chosen one. -/
theorem chosen_gauge_histogram_minimal (replies : List FrameColor) :
    ∀ sigma ∈ Nineteen.symmetries,
      ¬ Nineteen.lexLess
          (prefixGaugeHistogram (replies.map Prod.fst) sigma)
          (prefixGaugeHistogram (replies.map Prod.fst)
            (chosenPrefixColorMap replies)) = true := by
  intro sigma hsigma
  have inRoute := symmetries_in_frozen_route sigma hsigma
  unfold chosenPrefixColorMap choosePrefixGauge
  exact (Nineteen.foldl_lex_min
    (fun s : {t : List Nat // t ∈ Nineteen.symmetries} =>
      prefixGaugeHistogram (replies.map Prod.fst) s.val)
    (fun _ _ => by simp [prefixGaugeHistogram, Nineteen.counts]) _ _).2
    ⟨sigma, hsigma⟩
    (List.mem_cons_of_mem _
      (List.mem_map.2 ⟨⟨sigma, inRoute⟩, List.mem_attach _ _, rfl⟩))

/-- BS obligation 2 (uniqueness half). ANY symmetry attaining the minimum
yields the same histogram as the executable choice, so the selected maps
may differ (tie cases) without changing the representative histogram. -/
theorem minimal_gauge_histogram_unique (replies : List FrameColor)
    (sigma : List Nat) (hsigma : sigma ∈ Nineteen.symmetries)
    (hmin : ∀ tau ∈ Nineteen.symmetries,
      ¬ Nineteen.lexLess
          (prefixGaugeHistogram (replies.map Prod.fst) tau)
          (prefixGaugeHistogram (replies.map Prod.fst) sigma) = true) :
    prefixGaugeHistogram (replies.map Prod.fst) sigma =
      prefixGaugeHistogram (replies.map Prod.fst)
        (chosenPrefixColorMap replies) := by
  rcases Nineteen.lexLess_trichotomy
      (prefixGaugeHistogram (replies.map Prod.fst) sigma)
      (prefixGaugeHistogram (replies.map Prod.fst)
        (chosenPrefixColorMap replies))
      (by simp [prefixGaugeHistogram, Nineteen.counts]) with h | h | h
  · exact h
  · exact absurd h (chosen_gauge_histogram_minimal replies sigma hsigma)
  · exact absurd h (hmin _ (chosen_prefix_color_map_legal replies))

#print axioms chosen_gauge_histogram_minimal
#print axioms minimal_gauge_histogram_unique

end CubeRev029.Physical
