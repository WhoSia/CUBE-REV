import Lean
import WeightedPrefixCutset
import ParallelWorkerLoads

/-!
CUBE-REV P0-R6I-P8. A goal fingerprint is an auditable, reproducible
SHA-256 CONTENT COMMITMENT to an actual sorted physical goal image.
SHA256 equality alone is NOT a theorem of extensional set equality:
neither cryptographic collision resistance nor goal-ball BFS completeness
is postulated as a Lean axiom. The soundness bridge below requires
actual pointwise equality of goal membership predicates.
-/
namespace CubeRev025

universe u v w

/-- A proved bounded physical no-reachability certificate may be
reused against an immutable target with the SAME membership predicate.
The source physical action transition and canonical word grammar are
unchanged. SHA-256 equality by itself does not discharge 'goalAgreement'.
-/
theorem immutable_goal_refutation_transfer
    {S : Type u} {Q : Type v} {A : Type w}
    (move : S → A → S)
    (advance : Q → A → Q)
    (allowed : Q → A → Prop)
    (targetBefore targetAfter : S → Prop)
    (k : Nat) (s : S) (q : Q)
    (goalAgreement : ∀ x, targetBefore x ↔ targetAfter x)
    (certificate :
      PrefixRefutation move advance allowed targetBefore k s q) :
    PrefixRefutation move advance allowed targetAfter k s q := by
  apply prefix_refutation_complete move advance allowed targetAfter
  intro word hLength hLegal hPostMeet
  have beforeImpossible :=
    prefix_refutation_sound move advance allowed targetBefore
      k s q certificate word hLength hLegal
  exact beforeImpossible
    ((goalAgreement (runWord move s word)).mpr hPostMeet)

/-- The actual worker-batch refutation requires a completed source root
test AND a checked negative proof at each allowed next action, with
the exact same immutable target membership predicate at every leaf.
This formally composes worker-local leaves into global source coverage
only if ALL children are provided; a partial list cannot invoke it.
-/
theorem compose_complete_worker_batch
    {S : Type u} {Q : Type v} {A : Type w}
    (move : S → A → S)
    (advance : Q → A → Q)
    (allowed : Q → A → Prop)
    (target : S → Prop)
    (k : Nat) (s : S) (q : Q)
    (rootMissing : ¬ target s)
    (allCanonicalChildren : ∀ a, allowed q a →
      WeightedCutRefutation move advance allowed target k
        (move s a) (advance q a)) :
    PrefixRefutation move advance allowed target (k+1) s q := by
  exact weighted_cutset_compose move advance allowed target
    (k+1) s q
    (WeightedCutRefutation.split k s q rootMissing allCanonicalChildren)

end CubeRev025
