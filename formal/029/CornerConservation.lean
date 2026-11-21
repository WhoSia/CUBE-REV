import ReachableCornerCoordinates

namespace CubeRev029.Physical

set_option maxRecDepth 16000
set_option maxHeartbeats 0

/-- The eight source corner positions of a quarter turn are a permutation of
all eight positions. These indices come from the geometric `turnSlot`. -/
def cornerSources (t : Turn) : List (Fin 8) :=
  [cornerSourceIndex t 0, cornerSourceIndex t 1,
   cornerSourceIndex t 2, cornerSourceIndex t 3,
   cornerSourceIndex t 4, cornerSourceIndex t 5,
   cornerSourceIndex t 6, cornerSourceIndex t 7]

def canonicalCornerSources : List (Fin 8) :=
  [0, 1, 2, 3, 4, 5, 6, 7]

/-- A finite proof about twelve geometric generators, not an assumed table. -/
theorem corner_sources_perm :
    ∀ t : Turn, (cornerSources t).Perm canonicalCornerSources := by
  decide +kernel

/-- An explicitly expanded eight-term sum avoids any external dependencies. -/
def cornerSum8 (f : Fin 8 → Nat) : Nat :=
  (List.map f canonicalCornerSources).sum

/-- Summation is invariant under every quarter-turn's corner source map. -/
theorem cornerSum8_reindex (t : Turn) (f : Fin 8 → Nat) :
    cornerSum8 (fun i => f (cornerSourceIndex t i)) = cornerSum8 f := by
  have hp := (corner_sources_perm t).map f
  have hsum := hp.sum_nat
  simpa [cornerSum8, cornerSources, canonicalCornerSources] using hsum

/-- Cyclically rotating a corner does not change its piece identity. -/
theorem cornerPiece_shifted (x : Fin 24) (shift : Fin 3) :
    cornerPiece (shiftedCorner x shift) = cornerPiece x := by
  change (3 * (x.val / 3) + (x.val % 3 + shift.val) % 3) / 3 = x.val / 3
  have hr : (x.val % 3 + shift.val) % 3 < 3 := Nat.mod_lt _ (by decide)
  omega

/-- The orientation changes exactly by the cyclic offset modulo three. -/
theorem cornerTwist_shifted (x : Fin 24) (shift : Fin 3) :
    cornerTwist (shiftedCorner x shift) =
      (cornerTwist x + shift.val) % 3 := by
  change (3 * (x.val / 3) + (x.val % 3 + shift.val) % 3) % 3 =
    (x.val % 3 + shift.val) % 3
  omega

/-- The geometric source permutation conserves the total of piece labels,
regardless of whether the input array is reachable. -/
theorem corner_piece_total_action (t : Turn) (a : CornerCoordinates) :
    cornerPieceTotal (cornerAction t a) = cornerPieceTotal a := by
  have hp := cornerSum8_reindex t (fun i => cornerPiece (a i))
  simp [cornerSum8, cornerSources, canonicalCornerSources, cornerPieceTotal,
    cornerAction, cornerPiece_shifted] at hp ⊢
  omega

/-- Modulo three, the reindexed input twists and the generator's offsets
conserve the total corner twist for every input array. -/
theorem corner_twist_total_action (t : Turn) (a : CornerCoordinates) :
    cornerTwistTotal (cornerAction t a) % 3 = cornerTwistTotal a % 3 := by
  have hp := cornerSum8_reindex t (fun i => cornerTwist (a i))
  have hd := corner_turn_zero_twist_offset t
  simp [cornerSum8, cornerSources, canonicalCornerSources, cornerTwistTotal,
    cornerAction, cornerTwist_shifted, cornerTurnOffset, cornerTurnOffsetTotal]
    at hp hd ⊢
  omega

/-- The two conservation laws are stable under all twelve legal generators. -/
theorem legal_corner_action (t : Turn) (a : CornerCoordinates)
    (ha : LegalCornerCoordinates a) :
    LegalCornerCoordinates (cornerAction t a) := by
  constructor
  · rw [corner_piece_total_action]
    exact ha.piece_total
  · rw [corner_twist_total_action]
    exact ha.twist_total

/-- The solved cube starts in the correctly constrained coordinate sector. -/
theorem solved_corner_legal : LegalCornerCoordinates solvedCornerCoordinates := by
  constructor <;> decide +kernel

/-- Conservation for turn words of arbitrary length, by structural induction. -/
theorem coordinatesAlong_legal (turns : List Turn) :
    LegalCornerCoordinates (coordinatesAlong turns) := by
  induction turns with
  | nil => exact solved_corner_legal
  | cons t tail ih => exact legal_corner_action t _ ih

/-- Every reachable physical cube has legal oriented corner coordinates
whose colors exactly reproduce its real twenty-four corner stickers. -/
theorem reachable_has_legal_corners (s : Coloring) (h : Reachable s) :
    ∃ a : CornerCoordinates, LegalCornerCoordinates a ∧ CornersAgree a s := by
  obtain ⟨turns, rfl⟩ := h
  exact ⟨coordinatesAlong turns, coordinatesAlong_legal turns,
    coordinatesAlong_agree turns⟩

#print axioms corner_sources_perm
#print axioms corner_piece_total_action
#print axioms corner_twist_total_action
#print axioms coordinatesAlong_legal
#print axioms reachable_has_legal_corners

end CubeRev029.Physical
