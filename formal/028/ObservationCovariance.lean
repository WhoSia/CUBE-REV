import Lean

/-!
CUBE-REV 0.28 R14-P8.9 -- generic exact color-posterior transport.

This is a small, pure theorem about a *genuine bijection* on hidden states,
a corresponding query permutation and exact observation covariance.

It does NOT prove that a proposed permutation is physical in the
48-moving-facelet Rubik group; that all 576 paired queries are routable;
that a concrete 648-state/full-P48 canonicalization uses the correct maps;
nor that any 19-frame policy exists or fails.

No cardinality-only or parity-vector-only quotient is assumed.
Lean source is NOT a kernel PASS until a separate runner passes.
-/

namespace CubeRev028

universe u v w

/-- The legal states consistent with one exact observation. -/
def posterior {S : Type u} {Q : Type v} {Y : Type w}
    (observe : S → Q → Y) (belief : S → Prop) (q : Q) (y : Y) :
    S → Prop :=
  fun x => belief x ∧ observe x q = y

/-- Every original state x transports its posterior membership to
the corresponding transformed state. Both parts of the observation
must be included in the output type Y. -/
theorem posterior_transport_at_image
    {S : Type u} {Q : Type v} {Y : Type w}
    (observe : S → Q → Y)
    (mapS unmapS : S → S) (mapQ : Q → Q)
    (leftInverse : ∀ x, unmapS (mapS x) = x)
    (covariant : ∀ x q, observe (mapS x) (mapQ q) = observe x q)
    (belief : S → Prop) (q : Q) (y : Y) (x : S) :
    posterior observe (fun z => belief (unmapS z)) (mapQ q) y (mapS x) ↔
      posterior observe belief q y x := by
  change (belief (unmapS (mapS x)) ∧
    observe (mapS x) (mapQ q) = y) ↔
      (belief x ∧ observe x q = y)
  rw [leftInverse x, covariant x q]

/-- The inverse map must also be valid: this checks the entire posterior
relation, not just an inclusion of sample states. -/
theorem posterior_transport_at_arbitrary
    {S : Type u} {Q : Type v} {Y : Type w}
    (observe : S → Q → Y)
    (mapS unmapS : S → S) (mapQ : Q → Q)
    (rightInverse : ∀ z, mapS (unmapS z) = z)
    (covariant : ∀ x q, observe (mapS x) (mapQ q) = observe x q)
    (belief : S → Prop) (q : Q) (y : Y) (z : S) :
    posterior observe (fun t => belief (unmapS t)) (mapQ q) y z ↔
      posterior observe belief q y (unmapS z) := by
  change (belief (unmapS z) ∧ observe z (mapQ q) = y) ↔
    (belief (unmapS z) ∧ observe (unmapS z) q = y)
  have hc := covariant (unmapS z) q
  rw [rightInverse z] at hc
  rw [hc]

/-- Exact feasible color outcomes are preserved in BOTH directions.
This is a safe prerequisite for AND-OR recursion and query-orbit
pruning. It does not itself prove an optimal Bellman depth. -/
theorem possible_response_transport
    {S : Type u} {Q : Type v} {Y : Type w}
    (observe : S → Q → Y)
    (mapS unmapS : S → S) (mapQ : Q → Q)
    (leftInverse : ∀ x, unmapS (mapS x) = x)
    (rightInverse : ∀ z, mapS (unmapS z) = z)
    (covariant : ∀ x q, observe (mapS x) (mapQ q) = observe x q)
    (belief : S → Prop) (q : Q) (y : Y) :
    (∃ z, posterior observe (fun t => belief (unmapS t)) (mapQ q) y z) ↔
      (∃ x, posterior observe belief q y x) := by
  constructor
  · rintro ⟨z, hz⟩
    exact ⟨unmapS z,
      (posterior_transport_at_arbitrary observe mapS unmapS mapQ
        rightInverse covariant belief q y z).mp hz⟩
  · rintro ⟨x, hx⟩
    exact ⟨mapS x,
      (posterior_transport_at_image observe mapS unmapS mapQ
        leftInverse covariant belief q y x).mpr hx⟩

/-- Arithmetic consequence only. 21, 18 and 20 are inherited
separate Rubik certificates, NOT established by this Lean file. -/
theorem strict_adaptive_gap_from_certified_bounds
    (hFixed hAdaptive : Nat)
    (hFixedExact : hFixed = 21)
    (hAdaptiveLower : 18 ≤ hAdaptive)
    (hAdaptiveUpper : hAdaptive ≤ 20) :
    1 ≤ hFixed - hAdaptive ∧ hFixed - hAdaptive ≤ 3 := by
  omega

end CubeRev028
