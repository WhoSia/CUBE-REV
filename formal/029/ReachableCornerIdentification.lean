import CornerConservation

namespace CubeRev029.Physical

/-- The fourteen observed corner colors: two cyclic sticker addresses at each
corner position except position five. This is exactly the coordinate support
of the published nineteen-frame corner schedule. -/
def FourteenCornerColorsEqual (s₁ s₂ : Coloring) : Prop :=
  ∀ i : Fin 8, i ≠ 5 →
    s₁ (cornerRawSlot i 0) = s₂ (cornerRawSlot i 0) ∧
    s₁ (cornerRawSlot i 1) = s₂ (cornerRawSlot i 1)

/-- The algebraic pair decoder and the two real cyclic sticker reads share
the same ordered color convention, including corner orientation. -/
theorem cornerCyclicPair_colors (x : Fin 24) :
    cornerCyclicPair x =
      (orientedCornerColor x 0, orientedCornerColor x 1) := by
  simp [cornerCyclicPair, orientedCornerColor]

/-- Fourteen corner observations determine every physical corner sticker for
any two reachable physical cubes. The conservation premises are discharged by
`reachable_has_legal_corners`, not assumed in this theorem. -/
theorem reachable_corner_fourteen_complete
    (s₁ s₂ : Coloring) (h₁ : Reachable s₁) (h₂ : Reachable s₂)
    (same : FourteenCornerColorsEqual s₁ s₂) :
    ∀ i : Fin 8, ∀ j : Fin 3,
      s₁ (cornerRawSlot i j) = s₂ (cornerRawSlot i j) := by
  obtain ⟨a, ha, haAgree⟩ := reachable_has_legal_corners s₁ h₁
  obtain ⟨b, hb, hbAgree⟩ := reachable_has_legal_corners s₂ h₂
  have pairs : ∀ i : Fin 8, i ≠ 5 →
      cornerCyclicPair (a i) = cornerCyclicPair (b i) := by
    intro i hi
    have obs := same i hi
    rw [cornerCyclicPair_colors, cornerCyclicPair_colors]
    apply Prod.ext
    · exact (haAgree i 0).symm.trans (obs.1.trans (hbAgree i 0))
    · exact (haAgree i 1).symm.trans (obs.2.trans (hbAgree i 1))
  have coords : a = b := corner_fourteen_unique_missing_five a b ha hb pairs
  intro i j
  calc
    s₁ (cornerRawSlot i j) = orientedCornerColor (a i) j := haAgree i j
    _ = orientedCornerColor (b i) j := by rw [coords]
    _ = s₂ (cornerRawSlot i j) := (hbAgree i j).symm

#print axioms cornerCyclicPair_colors
#print axioms reachable_corner_fourteen_complete

end CubeRev029.Physical
