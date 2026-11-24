import ReachableEdgeCoordinates
import CornerPermutationSign

namespace CubeRev029.Physical

open CubeRev029.Eighteen

set_option autoImplicit false

/-!
# All legal turn words: exact reduction to two parity-reindex laws

The finite twelve-turn parity receipt `edge_corner_turn_sign_agree` does not
by itself prove global parity coupling. The remaining mathematical input is
how inversion parity changes when a permutation is reindexed by a *second*
permutation. The two explicitly scoped hypotheses below apply only to
permutations of the complete edge/corner alphabets, not to arbitrary lists
with repeated cubie IDs (for which the naive parity formula is false).

Once the two reindex laws are established in the core Lean environment,
this theorem automatically supplies physical edge/corner parity coupling
for every legal turn history and every Reachable original Coloring.
-/

/-- The actual 12-position physical edge permutation sign. -/
def edgePermutationParity (a : EdgeCoordinates) : Nat :=
  parity (edgePieceList a)

/-- The genuine solved edge and corner permutations are both even. -/
theorem solved_edge_corner_parity_agree :
    edgePermutationParity solvedEdgeCoordinates =
      cornerPermutationParity solvedCornerCoordinates := by
  decide +kernel

/-- The exact two finite-size generic permutation-reindexing lemmas whose
proofs are needed before `edge_corner_turn_sign_agree` can be lifted
from generators to every legal history. Their hypotheses explicitly
exclude degenerate repeated piece IDs. -/
def EdgeParityReindexLaw : Prop :=
  ∀ (t : Turn) (a : EdgeCoordinates),
    (edgePieceList a).Perm (canonicalEdgeSources.map Fin.val) →
    edgePermutationParity (edgeAction t a) =
      (edgePermutationParity a + parity (edgeTurnPieceList t)) % 2

def CornerParityReindexLaw : Prop :=
  ∀ (t : Turn) (a : CornerCoordinates),
    (cornerPieceList a).Perm canonicalCornerSources →
    cornerPermutationParity (cornerAction t a) =
      (cornerPermutationParity a + parity (cornerTurnPieceList t)) % 2

/-- Generator parity agreement plus the two *precisely stated* generic
permutation parity reindex laws imply parity coupling after any number
of actual physical face turns. The induction order exactly matches
`paint` and `edgeCoordinatesAlong` / `coordinatesAlong`. -/
theorem edge_corner_parity_coupling_all_turn_words
    (edgeReindex : EdgeParityReindexLaw)
    (cornerReindex : CornerParityReindexLaw)
    (turns : List Turn) :
    edgePermutationParity (edgeCoordinatesAlong turns) =
      cornerPermutationParity (coordinatesAlong turns) := by
  induction turns with
  | nil =>
      exact solved_edge_corner_parity_agree
  | cons t tail ih =>
      have hEdge := edgeReindex t (edgeCoordinatesAlong tail)
        (edge_coordinates_along_piece_perm tail)
      have hCorner := cornerReindex t (coordinatesAlong tail)
        (coordinatesAlong_piece_perm tail)
      calc
        edgePermutationParity (edgeCoordinatesAlong (t :: tail)) =
            (edgePermutationParity (edgeCoordinatesAlong tail) +
              parity (edgeTurnPieceList t)) % 2 := hEdge
        _ = (cornerPermutationParity (coordinatesAlong tail) +
              parity (cornerTurnPieceList t)) % 2 := by
              rw [ih, edge_corner_turn_sign_agree t]
        _ = cornerPermutationParity (coordinatesAlong (t :: tail)) :=
              hCorner.symm

/-- All Reachable physical cube colorings admit both exact edge and
corner coordinate descriptions with the physical permutation signs
coupled. This is conditional ONLY on the two generic parity-reindex
lemmas, never on a parity oracle or an arbitrary signed state tag. -/
theorem reachable_has_parity_coupled_coordinates
    (edgeReindex : EdgeParityReindexLaw)
    (cornerReindex : CornerParityReindexLaw)
    (s : Coloring) (reachable : Reachable s) :
    ∃ (edges : EdgeCoordinates) (corners : CornerCoordinates),
      EdgesAgree edges s ∧
      CornersAgree corners s ∧
      (edgePieceList edges).Perm (canonicalEdgeSources.map Fin.val) ∧
      (cornerPieceList corners).Perm canonicalCornerSources ∧
      edgePermutationParity edges = cornerPermutationParity corners := by
  obtain ⟨turns, rfl⟩ := reachable
  exact ⟨edgeCoordinatesAlong turns, coordinatesAlong turns,
    edge_coordinates_along_agree turns,
    coordinatesAlong_agree turns,
    edge_coordinates_along_piece_perm turns,
    coordinatesAlong_piece_perm turns,
    edge_corner_parity_coupling_all_turn_words
      edgeReindex cornerReindex turns⟩

#print axioms solved_edge_corner_parity_agree
#print axioms edge_corner_parity_coupling_all_turn_words
#print axioms reachable_has_parity_coupled_coordinates

end CubeRev029.Physical
