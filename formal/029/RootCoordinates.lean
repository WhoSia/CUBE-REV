import ResidualWord

namespace CubeRev029.Eighteen

theorem root_length {sign : Nat} {w : Word} (h : Completes (root sign) w) :
    w.length = 12 := by
  have counts := h.labels.length_eq
  simpa [wordLabels, root, labelNames] using counts

theorem root_id_in_range {sign : Nat} {w : Word} (h : Completes (root sign) w)
    {id : Nat} (occurs : id ∈ w) : id < 24 := by
  have rank : id / 2 ∈ (root sign).labels :=
    h.labels.mem_iff.mp (List.mem_map.mpr ⟨id, occurs, rfl⟩)
  have below : id / 2 < 12 := by simpa [root, labelNames] using rank
  omega

set_option maxRecDepth 10000 in
set_option maxHeartbeats 0 in
theorem oriented_edge_color_pair_injective :
    ∀ x y : Fin 24, (sticker x.val false, sticker x.val true) =
      (sticker y.val false, sticker y.val true) → x = y := by decide +kernel

def faceletColor (w : Word) (q : Fin 12 × Bool) : Nat :=
  observeWord w (q.1.val, q.2)

/-- At a root, distinct legal edge words really describe different
24-facelet assignments, rather than redundant encodings. -/
theorem root_facelets_separate {sign : Nat} {s t : Word}
    (hs : Completes (root sign) s) (ht : Completes (root sign) t)
    (same : ∀ q, faceletColor s q = faceletColor t q) : s = t := by
  apply List.ext_getElem?
  intro i
  have ls := root_length hs
  have lt := root_length ht
  by_cases hi : i < 12
  · have is : i < s.length := by omega
    have it : i < t.length := by omega
    rw [List.getElem?_eq_getElem is, List.getElem?_eq_getElem it]
    apply congrArg some
    let sx : Fin 24 := ⟨s[i], root_id_in_range hs (List.getElem_mem is)⟩
    let tx : Fin 24 := ⟨t[i], root_id_in_range ht (List.getElem_mem it)⟩
    have e₁ := same (⟨i, hi⟩, false)
    have e₂ := same (⟨i, hi⟩, true)
    simp only [faceletColor, observeWord, List.getElem?_eq_getElem is,
      List.getElem?_eq_getElem it, Option.getD_some] at e₁ e₂
    exact congrArg Fin.val (oriented_edge_color_pair_injective sx tx (Prod.ext e₁ e₂))
  · rw [List.getElem?_eq_none (by omega : s.length ≤ i),
        List.getElem?_eq_none (by omega : t.length ≤ i)]

#print axioms root_facelets_separate

end CubeRev029.Eighteen
