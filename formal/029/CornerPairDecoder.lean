import PhysicalPolicyCompilerFast

namespace CubeRev029.Physical

open Eighteen

/-- An oriented corner cubie is its piece index (0..7) and a cyclic
orientation (0..2), packed into a Fin 24. -/
def cornerPiece (x : Fin 24) : Nat := x.val / 3
def cornerTwist (x : Fin 24) : Nat := x.val % 3

def cornerCyclicPair (x : Fin 24) : Nat × Nat :=
  let name := cornerNames[x.val / 3]!.toList
  (colorCode name[x.val % 3]!, colorCode name[(x.val % 3 + 1) % 3]!)

set_option maxRecDepth 10000
set_option maxHeartbeats 0

/-- In the oriented 3x3x3-corner alphabet, the first two cyclically
ordered colors uniquely determine the cubie identity and twist. -/
theorem cornerCyclicPair_injective :
    ∀ x y : Fin 24, cornerCyclicPair x = cornerCyclicPair y → x = y := by
  decide +kernel

abbrev CornerCoordinates := Fin 8 → Fin 24

/-- A legal cube has each corner piece exactly once, hence this total is
0+1+...+7 = 28; the three-way twist sum is a multiple of 3. These are the
two conservation laws used to infer the final unobserved corner. -/
def cornerPieceTotal (a : CornerCoordinates) : Nat :=
  cornerPiece (a 0) + cornerPiece (a 1) + cornerPiece (a 2) + cornerPiece (a 3) + cornerPiece (a 4) + cornerPiece (a 5) + cornerPiece (a 6) + cornerPiece (a 7)

def cornerTwistTotal (a : CornerCoordinates) : Nat :=
  cornerTwist (a 0) + cornerTwist (a 1) + cornerTwist (a 2) + cornerTwist (a 3) + cornerTwist (a 4) + cornerTwist (a 5) + cornerTwist (a 6) + cornerTwist (a 7)

structure LegalCornerCoordinates (a : CornerCoordinates) : Prop where
  piece_total : cornerPieceTotal a = 28
  twist_total : cornerTwistTotal a % 3 = 0

/-- Fourteen ordered colors (two at each of seven positions) determine the
entire legally constrained eight-corner state. The proof of last-corner
uniqueness uses only the conservation laws, not enumeration of 8! * 3^7
states. The separate physical-generator proof must establish those laws
for Reachable colorings. -/
theorem corner_fourteen_unique (a b : CornerCoordinates)
    (ha : LegalCornerCoordinates a) (hb : LegalCornerCoordinates b)
    (same : ∀ i : Fin 8, i.val < 7 →
      cornerCyclicPair (a i) = cornerCyclicPair (b i)) : a = b := by
  have e0 : a 0 = b 0 := cornerCyclicPair_injective _ _ (same 0 (by decide))
  have e1 : a 1 = b 1 := cornerCyclicPair_injective _ _ (same 1 (by decide))
  have e2 : a 2 = b 2 := cornerCyclicPair_injective _ _ (same 2 (by decide))
  have e3 : a 3 = b 3 := cornerCyclicPair_injective _ _ (same 3 (by decide))
  have e4 : a 4 = b 4 := cornerCyclicPair_injective _ _ (same 4 (by decide))
  have e5 : a 5 = b 5 := cornerCyclicPair_injective _ _ (same 5 (by decide))
  have e6 : a 6 = b 6 := cornerCyclicPair_injective _ _ (same 6 (by decide))
  have lastPiece : cornerPiece (a 7) = cornerPiece (b 7) := by
    have x := ha.piece_total
    have y := hb.piece_total
    simp only [cornerPieceTotal, e0, e1, e2, e3, e4, e5, e6] at x
    simp only [cornerPieceTotal] at y
    omega
  have lastTwist : cornerTwist (a 7) = cornerTwist (b 7) := by
    have x := ha.twist_total
    have y := hb.twist_total
    simp only [cornerTwistTotal, e0, e1, e2, e3, e4, e5, e6] at x
    simp only [cornerTwistTotal] at y
    have hA : cornerTwist (a 7) < 3 := Nat.mod_lt _ (by decide)
    have hB : cornerTwist (b 7) < 3 := Nat.mod_lt _ (by decide)
    omega
  have last : a 7 = b 7 := by
    apply Fin.ext
    have x := Nat.mod_add_div (a 7).val 3
    have y := Nat.mod_add_div (b 7).val 3
    dsimp [cornerPiece, cornerTwist] at lastPiece lastTwist
    omega
  funext i
  by_cases h : i.val < 7
  · exact cornerCyclicPair_injective _ _ (same i h)
  · have endIndex : i = (7 : Fin 8) := Fin.ext (by omega)
    simpa [endIndex] using last


/-- The published nineteen-frame controller does not use the first two colors
of corner position 5. Its actual seven observed positions are
0, 2, 3, 6, 7, 4, 1 (in that chronological order). This version of the
uniqueness theorem matches *that specific physical schedule*, rather than
the convenient but different schedule omitting position 7 above. -/
theorem corner_fourteen_unique_missing_five (a b : CornerCoordinates)
    (ha : LegalCornerCoordinates a) (hb : LegalCornerCoordinates b)
    (same : ∀ i : Fin 8, i ≠ 5 →
      cornerCyclicPair (a i) = cornerCyclicPair (b i)) : a = b := by
  have e0 : a 0 = b 0 := cornerCyclicPair_injective _ _ (same 0 (by decide))
  have e1 : a 1 = b 1 := cornerCyclicPair_injective _ _ (same 1 (by decide))
  have e2 : a 2 = b 2 := cornerCyclicPair_injective _ _ (same 2 (by decide))
  have e3 : a 3 = b 3 := cornerCyclicPair_injective _ _ (same 3 (by decide))
  have e4 : a 4 = b 4 := cornerCyclicPair_injective _ _ (same 4 (by decide))
  have e6 : a 6 = b 6 := cornerCyclicPair_injective _ _ (same 6 (by decide))
  have e7 : a 7 = b 7 := cornerCyclicPair_injective _ _ (same 7 (by decide))
  have missingPiece : cornerPiece (a 5) = cornerPiece (b 5) := by
    have x := ha.piece_total
    have y := hb.piece_total
    simp only [cornerPieceTotal, e0, e1, e2, e3, e4, e6, e7] at x
    simp only [cornerPieceTotal] at y
    omega
  have missingTwist : cornerTwist (a 5) = cornerTwist (b 5) := by
    have x := ha.twist_total
    have y := hb.twist_total
    simp only [cornerTwistTotal, e0, e1, e2, e3, e4, e6, e7] at x
    simp only [cornerTwistTotal] at y
    have hA : cornerTwist (a 5) < 3 := Nat.mod_lt _ (by decide)
    have hB : cornerTwist (b 5) < 3 := Nat.mod_lt _ (by decide)
    omega
  have missing : a 5 = b 5 := by
    apply Fin.ext
    have x := Nat.mod_add_div (a 5).val 3
    have y := Nat.mod_add_div (b 5).val 3
    dsimp [cornerPiece, cornerTwist] at missingPiece missingTwist
    omega
  funext i
  by_cases hi : i = (5 : Fin 8)
  · simpa [hi] using missing
  · exact cornerCyclicPair_injective _ _ (same i hi)

/-- Exactly the fourteen distinct sticker addresses used by the X controller.
The final element is observed on frame 19. The order matters for causal
availability but not for the uniqueness theorem. -/
def scheduledCorners : List (Fin 8) := [0, 0, 2, 2, 3, 3, 6, 6, 7, 7, 4, 4, 1, 1]

theorem scheduledCorners_excludes_five : (5 : Fin 8) ∉ scheduledCorners := by decide

theorem scheduledCorners_coverage :
    ∀ i : Fin 8, i ≠ 5 → scheduledCorners.count i = 2 := by decide

#print axioms corner_fourteen_unique_missing_five
#print axioms scheduledCorners_coverage

#print axioms cornerCyclicPair_injective
#print axioms corner_fourteen_unique

end CubeRev029.Physical
