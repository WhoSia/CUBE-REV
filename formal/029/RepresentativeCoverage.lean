import NineteenReadData
import ResidualWord

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

end CubeRev029.Nineteen
