import LegalEdgeSymmetry

namespace CubeRev029.Nineteen

set_option maxRecDepth 16000
set_option maxHeartbeats 0

/-- The actual inverse permutation of the six center-color codes, built
from the original six-element symmetry table rather than a second trusted
hand-entered mapping. -/
def inverseColorTable (sigma : List Nat) : List Nat :=
  (List.range 6).map (fun color => sigma.idxOf color)

/-- The 48 allowed opposite-pair-preserving color transformations form
an inverse-closed family. -/
theorem inverse_color_table_is_symmetry :
    ∀ sigma ∈ symmetries, inverseColorTable sigma ∈ symmetries := by
  decide +kernel

theorem inverse_color_table_restores_center_code :
    ∀ sigma ∈ symmetries, ∀ color : Fin 6,
      (inverseColorTable sigma)[sigma[color.val]!]! = color.val := by
  decide +kernel

/-- Inversion holds on each of the twenty-four oriented edge identities.
The proof checks the *exact* relabelEdgeValue function used to transport
complete legal words, including the orientation convention. -/
theorem inverse_color_table_restores_oriented_edge :
    ∀ sigma ∈ symmetries, ∀ word : Fin 24,
      relabelEdgeValue (inverseColorTable sigma)
        (relabelEdgeValue sigma word.val) = word.val := by
  decide +kernel

theorem oriented_edge_inverse_table_restores_forward :
    ∀ sigma ∈ symmetries, ∀ word : Fin 24,
      relabelEdgeValue sigma
        (relabelEdgeValue (inverseColorTable sigma) word.val) = word.val := by
  decide +kernel

#print axioms inverse_color_table_is_symmetry
#print axioms inverse_color_table_restores_center_code
#print axioms inverse_color_table_restores_oriented_edge
#print axioms oriented_edge_inverse_table_restores_forward

end CubeRev029.Nineteen
