import ObservationCovariance

/-!
CUBE-REV 0.28 R14-P8.10 -- safe two-probe adversary inference.

A *literal* first-response witness for every possible first query, followed
by a collision for every second query, is a sound reason why no two-read
zero-error adaptive policy exists.

This formalizes the QUANTIFIER ORDER in the P8.3 384-prefix / 2,304-pair
finite certificates. It does not establish that those witness files are
complete, legal full-cube states or correct for this model: importing and
validating that original finite certificate is a future obligation.

SOURCE ONLY until an actual Lean kernel build has been inspected.
-/

namespace CubeRev028

universe u v w

/-- A query has no two different indistinguishable states in the belief. -/
def separates {S : Type u} {Q : Type v} {Y : Type w}
    (observe : S → Q → Y) (belief : S → Prop) (q : Q) : Prop :=
  ∀ x x', belief x → belief x' →
    observe x q = observe x' q → x = x'

/-- At most two *adaptive* reads: choose the first query before any output,
then choose the second after each feasible first output. -/
def winTwo {S : Type u} {Q : Type v} {Y : Type w}
    (observe : S → Q → Y) (belief : S → Prop) : Prop :=
  ∃ q1, ∀ y,
    (∃ x, posterior observe belief q1 y x) →
      ∃ q2, separates observe (posterior observe belief q1 y) q2

/-- An actual first-color branch and a second-query collision for EVERY
second action invalidate EVERY two-read online policy. -/
theorem exact_two_step_adversary_obstruction
    {S : Type u} {Q : Type v} {Y : Type w}
    (observe : S → Q → Y) (belief : S → Prop)
    (adversary : ∀ q1, ∃ y,
      (∃ x, posterior observe belief q1 y x) ∧
      (∀ q2, ∃ x x',
        posterior observe belief q1 y x ∧
        posterior observe belief q1 y x' ∧
        observe x q2 = observe x' q2 ∧ x ≠ x')) :
    ¬ winTwo observe belief := by
  intro hWin
  obtain ⟨q1, hFuture⟩ := hWin
  obtain ⟨y, hPossible, hHard⟩ := adversary q1
  obtain ⟨q2, hSeparates⟩ := hFuture y hPossible
  obtain ⟨x, x', hx, hx', hEq, hNe⟩ := hHard q2
  exact hNe (hSeparates x x' hx hx' hEq)

end CubeRev028
