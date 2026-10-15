import WeightedPrefixCutset

/-!
CUBE-REV 0.25 P0-R6I-P6 — algebra of certifiable Pareto pruning.
Jobs, additive model total cost, and worst isolated job cost are
separate dimensions. This algebra proves that deleting a componentwise
dominated partial schedule cannot improve ANY subsequent COMMON suffix.

Important limits: makespan under P parallel workers, memory contention,
true whole-cubie source run time, and optimal choice of cutsets are not
asserted by this lemma. The Go code separately exhaustively checks all
2^18 decisions under its explicitly discretized cost model.
-/
namespace CubeRev025

structure CutsetScore where
  jobs : Nat
  total : Nat
  peak : Nat

def scoreJoin (x y : CutsetScore) : CutsetScore :=
  ⟨x.jobs + y.jobs, x.total + y.total, max x.peak y.peak⟩

def scoreWeakDominates (x y : CutsetScore) : Prop :=
  x.jobs ≤ y.jobs ∧ x.total ≤ y.total ∧ x.peak ≤ y.peak

theorem score_dominance_refl (x : CutsetScore) :
    scoreWeakDominates x x := by
  exact ⟨le_refl _, le_refl _, le_refl _⟩

theorem score_dominance_trans
    (x y z : CutsetScore)
    (hxy : scoreWeakDominates x y)
    (hyz : scoreWeakDominates y z) :
    scoreWeakDominates x z := by
  exact ⟨le_trans hxy.1 hyz.1,
         le_trans hxy.2.1 hyz.2.1,
         le_trans hxy.2.2 hyz.2.2⟩

/-- THIS is the exact Pareto DP pruning law. The per-branch scores
may have distinct source-grammar states, but any future suffix schedule
that is INDEPENDENT of the pruned choice must be identical on both
sides. We make no unjustified claim about physical state equivalence. -/
theorem score_join_preserves_domination
    (x y future : CutsetScore)
    (h : scoreWeakDominates x y) :
    scoreWeakDominates (scoreJoin x future)
      (scoreJoin y future) := by
  constructor
  · exact Nat.add_le_add_right h.1 future.jobs
  constructor
  · exact Nat.add_le_add_right h.2.1 future.total
  · apply max_le
    · exact le_trans h.2.2 (le_max_left y.peak future.peak)
    · exact le_max_right y.peak future.peak

/-- Non-commutative original physical action order belongs to the proof
tree, NOT to this commutative cost summary; the sound pruning argument
only applies AFTER structural prefix-cutset completeness is certified. -/
theorem peak_bounded_by_sum (x y : CutsetScore) :
    (scoreJoin x y).peak ≤ x.peak + y.peak := by
  unfold scoreJoin
  apply max_le
  · exact Nat.le_add_right _ _
  · exact Nat.le_add_left _ _

end CubeRev025
