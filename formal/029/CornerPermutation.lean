import ReachableCornerIdentification

namespace CubeRev029.Physical

set_option maxRecDepth 16000
set_option maxHeartbeats 0

/-- The identity index of a corner is always in `Fin 8`. -/
def cornerPieceFin (x : Fin 24) : Fin 8 :=
  ⟨cornerPiece x, by
    have h := x.isLt
    dsimp [cornerPiece]
    omega⟩

/-- The complete list of oriented corner identities, forgetting twist. -/
def cornerPieceList (a : CornerCoordinates) : List (Fin 8) :=
  canonicalCornerSources.map (fun i => cornerPieceFin (a i))

/-- Physical twisting cannot change the identity of any one cubie. -/
theorem cornerPieceFin_shifted (x : Fin 24) (shift : Fin 3) :
    cornerPieceFin (shiftedCorner x shift) = cornerPieceFin x := by
  apply Fin.ext
  exact cornerPiece_shifted x shift

/-- Every basic face turn merely permutes the eight source cubie identities.
This holds for arbitrary corner arrangements, not just reachable ones. -/
theorem corner_pieceList_action_perm (t : Turn) (a : CornerCoordinates) :
    (cornerPieceList (cornerAction t a)).Perm (cornerPieceList a) := by
  have hp := (corner_sources_perm t).map (fun i => cornerPieceFin (a i))
  simpa [cornerPieceList, cornerSources, canonicalCornerSources,
    cornerAction, cornerPieceFin_shifted] using hp

/-- The solved cube has all eight cubies, exactly once. -/
theorem solved_corner_pieceList :
    cornerPieceList solvedCornerCoordinates = canonicalCornerSources := by
  decide +kernel

/-- Any finite sequence of legal turns preserves the eight-cubie multiset. -/
theorem coordinatesAlong_piece_perm (turns : List Turn) :
    (cornerPieceList (coordinatesAlong turns)).Perm canonicalCornerSources := by
  induction turns with
  | nil =>
      change (cornerPieceList solvedCornerCoordinates).Perm canonicalCornerSources
      rw [solved_corner_pieceList]
  | cons t tail ih =>
      change (cornerPieceList (cornerAction t (coordinatesAlong tail))).Perm
        canonicalCornerSources
      exact (corner_pieceList_action_perm t (coordinatesAlong tail)).trans ih

/-- Each genuinely reachable cube has eight *distinct* corner cubies as well
as the conservation laws and exact correspondence with its sticker colors. -/
theorem reachable_has_permutation_corners (s : Coloring) (h : Reachable s) :
    ∃ a : CornerCoordinates,
      LegalCornerCoordinates a ∧ CornersAgree a s ∧
      (cornerPieceList a).Perm canonicalCornerSources := by
  obtain ⟨turns, rfl⟩ := h
  exact ⟨coordinatesAlong turns, coordinatesAlong_legal turns,
    coordinatesAlong_agree turns, coordinatesAlong_piece_perm turns⟩

#print axioms corner_pieceList_action_perm
#print axioms coordinatesAlong_piece_perm
#print axioms reachable_has_permutation_corners

end CubeRev029.Physical
