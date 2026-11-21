import ReachableCornerIdentification

namespace CubeRev029.Physical

set_option maxRecDepth 16000
set_option maxHeartbeats 0

/-- The actual nineteen corner observations, including repeated padding
readings, in the initial cube's sticker-address coordinates. This is not
a free corner oracle: the address at each frame must still be routed by the
paired physical controller. -/
def scheduledCornerColors (s : Coloring) : List Nat :=
  cornerFrameAddresses.map (fun addr => s (cornerSlot addr))

/-- Equality of two list-valued observation records implies equality of each
observed entry, including entries which occur more than once. -/
private theorem mapped_corner_colors_agree (s₁ s₂ : Coloring) :
    ∀ xs : List (Fin 24),
      xs.map (fun addr => s₁ (cornerSlot addr)) =
        xs.map (fun addr => s₂ (cornerSlot addr)) →
      ∀ addr ∈ xs, s₁ (cornerSlot addr) = s₂ (cornerSlot addr) := by
  intro xs
  induction xs with
  | nil =>
      intro _ addr hx
      simp at hx
  | cons a tail ih =>
      intro h addr hx
      have parts :
          s₁ (cornerSlot a) = s₂ (cornerSlot a) ∧
          tail.map (fun x => s₁ (cornerSlot x)) =
            tail.map (fun x => s₂ (cornerSlot x)) := by
        simpa only [List.map_cons, List.cons.injEq] using h
      rcases List.mem_cons.mp hx with haddr | htail
      · subst addr
        exact parts.1
      · exact ih parts.2 addr htail

/-- The real nineteen-frame schedule contains both cyclic sticker addresses
for every observed corner. Position five is the sole unobserved position. -/
theorem nineteen_schedule_contains_required_corner_pairs :
    ∀ i : Fin 8, i ≠ 5 →
      (⟨3 * i.val, by have hi := i.isLt; omega⟩ : Fin 24) ∈ cornerFrameAddresses ∧
      (⟨3 * i.val + 1, by have hi := i.isLt; omega⟩ : Fin 24) ∈
        cornerFrameAddresses := by
  decide +kernel

/-- An identical nineteen-element scheduled corner transcript entails exactly
the fourteen-color agreement used by the reachable-cube decoder. -/
theorem same_scheduled_colors_implies_fourteen
    (s₁ s₂ : Coloring)
    (h : scheduledCornerColors s₁ = scheduledCornerColors s₂) :
    FourteenCornerColorsEqual s₁ s₂ := by
  intro i hi
  have members := nineteen_schedule_contains_required_corner_pairs i hi
  have observed := mapped_corner_colors_agree s₁ s₂ cornerFrameAddresses h
  constructor
  · have eq := observed
        (⟨3 * i.val, by have hi' := i.isLt; omega⟩ : Fin 24) members.1
    simpa [cornerSlot, cornerRawSlot] using eq
  · have eq := observed
        (⟨3 * i.val + 1, by have hi' := i.isLt; omega⟩ : Fin 24) members.2
    simpa [cornerSlot, cornerRawSlot] using eq

/-- For any two physically reachable cubes, equality of the actual nineteen
corner replies alone already forces equality of *all* twenty-four corner
stickers. The edge decision policy and its parity transport remain separate
unproved composition obligations. -/
theorem same_nineteen_corner_answers_force_all_corner_colors
    (s₁ s₂ : Coloring) (h₁ : Reachable s₁) (h₂ : Reachable s₂)
    (same : scheduledCornerColors s₁ = scheduledCornerColors s₂) :
    ∀ i : Fin 8, ∀ j : Fin 3,
      s₁ (cornerRawSlot i j) = s₂ (cornerRawSlot i j) := by
  exact reachable_corner_fourteen_complete s₁ s₂ h₁ h₂
    (same_scheduled_colors_implies_fourteen s₁ s₂ same)

#print axioms nineteen_schedule_contains_required_corner_pairs
#print axioms same_scheduled_colors_implies_fourteen
#print axioms same_nineteen_corner_answers_force_all_corner_colors

end CubeRev029.Physical
