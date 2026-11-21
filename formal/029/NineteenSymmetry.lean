import NineteenReadData

namespace CubeRev029.Nineteen

open Eighteen

set_option maxRecDepth 16000
set_option maxHeartbeats 0

/-- Relabel the unordered colors of one original edge type under a six-center
color symmetry. A reversed ordering still denotes the same physical piece.
The finite symmetry lemmas below guarantee that the fallback never contributes
for any genuine member of the forty-eight-element symmetry family. -/
def relabeledEdgeType (sigma : List Nat) (id : Nat) : Nat :=
  let a := sigma[sticker (2 * id) false]!
  let b := sigma[sticker (2 * id) true]!
  ((List.range 12).find? fun j =>
    (sticker (2 * j) false == a && sticker (2 * j) true == b) ||
    (sticker (2 * j) false == b && sticker (2 * j) true == a)).getD 0

/-- Whether the center-color relabeling reverses the chosen canonical first
sticker of the relabeled edge type. -/
def relabeledEdgeSwap (sigma : List Nat) (id : Nat) : Nat :=
  if sticker (2 * relabeledEdgeType sigma id) false ==
    sigma[sticker (2 * id) false]! then 0 else 1

/-- The relabelled oriented edge word: id and flip bit are both transformed. -/
def relabeledOrientedEdge (sigma : List Nat) (w : Fin 24) : Nat :=
  2 * relabeledEdgeType sigma (w.val / 2) +
    (w.val % 2 + relabeledEdgeSwap sigma (w.val / 2)) % 2

/-- Every symmetry in the actual policy's 48-element family permutes
the twelve edge types without duplicates or out-of-range fallbacks. -/
theorem symmetry_preserves_edge_type_bijection :
    ∀ sigma ∈ symmetries,
      ((List.range 12).map (relabeledEdgeType sigma)).eraseDups.length = 12 ∧
      ((List.range 12).map (relabeledEdgeType sigma)).all (· < 12) = true := by
  decide +kernel

/-- The total orientation offset over all twelve edge labels is even.
For a legal edge permutation each edge label occurs once, so the flip-parity
constraint is unchanged by any valid color symmetry. -/
theorem symmetry_even_flip_offset :
    ∀ sigma ∈ symmetries,
      (((List.range 12).map (relabeledEdgeSwap sigma)).sum % 2) = 0 := by
  decide +kernel

/-- Response equivariance at each of the twenty-four oriented edge facelets:
relabeling a piece then reading one of its two sticker sides agrees with
reading first and relabeling the color. Both sides are checked. -/
theorem symmetry_preserves_oriented_edge_colors :
    ∀ sigma ∈ symmetries, ∀ w : Fin 24, ∀ side : Bool,
      sticker (relabeledOrientedEdge sigma w) side =
        sigma[sticker w.val side]! := by
  decide +kernel

#print axioms symmetry_preserves_edge_type_bijection
#print axioms symmetry_even_flip_offset
#print axioms symmetry_preserves_oriented_edge_colors

end CubeRev029.Nineteen
