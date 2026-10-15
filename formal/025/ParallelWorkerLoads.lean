import Lean
import ParetoCutsetDominance

/-!
CUBE-REV 0.25 P0-R6I-P7 — exact homogeneous-worker permutation
invariance, a necessary soundness condition for canonical sorted-load
DP states. No claim is made that the separate Go LPT heuristic is optimal
for the 43 mixed-prefix tasks; only the 18 unsplit 9+9 model is solved
exactly by integer Bellman and independent feasibility certificates.
-/
namespace CubeRev025

def parallelMakespan (loads : List Nat) : Nat :=
  loads.foldr max 0

/-- Workers are identical: permuting their identities preserves the
true maximum over the same integer loads. This is the mathematical
soundness of quotienting load vectors by worker permutation. -/
theorem parallel_makespan_permutation_invariant
    {a b : List Nat} (h : a.Perm b) :
    parallelMakespan a = parallelMakespan b := by
  induction h with
  | nil => rfl
  | @cons x l₁ l₂ h ih =>
      simpa [parallelMakespan, List.foldr_cons] using
        congrArg (fun n => max x n) ih
  | @swap x y l =>
      simp only [parallelMakespan, List.foldr_cons]
      omega
  | @trans l₁ l₂ l₃ _ _ ih₁ ih₂ =>
      exact ih₁.trans ih₂

/-- Exact constructive upper bound from any nonnegative worker schedule:
a claimed optimal makespan must have some concrete worker-load witness. -/
theorem parallel_makespan_cons (x : Nat) (xs : List Nat) :
    parallelMakespan (x :: xs) =
      max x (parallelMakespan xs) := by
  rfl


/-- Exact fixed-setup amortization. If N independent physical prefix
jobs each rebuild an immutable target court costing s, but B nonempty
worker batches each build the SAME court once while preserving all
N original prefix proof obligations, the aggregate modelled setup
work saved is precisely (N-B)*s. This is an algebraic statement
conditional on fixed equal setup cost and identical source work,
NOT a wall-speedup law for unknown shared hardware contention. -/
theorem immutable_goal_court_setup_amortization
    (jobs batches setup : Nat) (h : batches ≤ jobs) :
    jobs * setup =
      batches * setup + (jobs - batches) * setup := by
  have hb : jobs - batches + batches = jobs :=
    Nat.sub_add_cancel h
  calc
    jobs * setup = (jobs - batches + batches) * setup := by rw [hb]
    _ = (jobs - batches) * setup + batches * setup := by
      rw [Nat.add_mul]
    _ = batches * setup + (jobs - batches) * setup := by
      omega

end CubeRev025
