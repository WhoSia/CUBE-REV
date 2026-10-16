import Lean
import ExactConditionalFiberLabels

/-!
CUBE-REV 0.25 P0-R6I-P11
Symmetry transport of exact corner-conditioned edge fibers.

The action here is an *automorphism of the goal relation*, such as
an appropriately verified solved-state-fixing cube automorphism.
It is NOT assumed that translating B6 by a face turn preserves B6.
A joint automorphism sends the fiber at corner c to the image of that
fiber under its edge action. Two corners in an automorphism orbit
can share LITERALLY identical edge keys only if the action
stabilizes that edge-support set. This is a necessary statement, not
an unsupported claim that the 576 observed duplicate pairs are
caused by a particular symmetry.
-/
namespace CubeRev025

universe u v w

/-- Right cancellation of a reversible edge permutation plus genuine
joint target preservation forces exact covariance of conditional
corner-edge fibers. -/
theorem exact_fiber_transport_under_joint_automorphism
    {H : Type u} {C : Type v} {E : Type w}
    (actCorner : H → C → C)
    (actEdge : H → E → E)
    (inverse : H → H) (goal : C → E → Prop)
    (edgeRightInverse :
      ∀ h e, actEdge h (actEdge (inverse h) e) = e)
    (goalCovariant :
      ∀ h c e, goal (actCorner h c) (actEdge h e) ↔ goal c e)
    (h : H) (c : C) (e : E) :
    goal (actCorner h c) e ↔
      goal c (actEdge (inverse h) e) := by
  have hTransport :=
    goalCovariant h c (actEdge (inverse h) e)
  rw [edgeRightInverse h e] at hTransport
  exact hTransport

/-- If two corners related by a genuine joint automorphism share
IDENTICAL literal edge fibers, the fiber at the original corner
must be invariant under the inverse edge action. -/
theorem identical_automorphic_corner_fibers_require_edge_stabilizer
    {H : Type u} {C : Type v} {E : Type w}
    (actCorner : H → C → C)
    (actEdge : H → E → E)
    (inverse : H → H) (goal : C → E → Prop)
    (edgeRightInverse :
      ∀ h e, actEdge h (actEdge (inverse h) e) = e)
    (goalCovariant :
      ∀ h c e, goal (actCorner h c) (actEdge h e) ↔ goal c e)
    (h : H) (c : C)
    (sameLiteralFiber :
      ∀ e, goal (actCorner h c) e ↔ goal c e)
    (e : E) :
    goal c e ↔ goal c (actEdge (inverse h) e) := by
  exact (sameLiteralFiber e).symm.trans
    (exact_fiber_transport_under_joint_automorphism
       actCorner actEdge inverse goal edgeRightInverse
       goalCovariant h c e)

/-- A witness that the edge action changes the support set precludes
identical literal corner fibers along this joint automorphism. -/
theorem moving_edge_support_excludes_identical_corner_fibers
    {H : Type u} {C : Type v} {E : Type w}
    (actCorner : H → C → C)
    (actEdge : H → E → E)
    (inverse : H → H) (goal : C → E → Prop)
    (edgeRightInverse :
      ∀ h e, actEdge h (actEdge (inverse h) e) = e)
    (goalCovariant :
      ∀ h c e, goal (actCorner h c) (actEdge h e) ↔ goal c e)
    (h : H) (c : C) (e : E)
    (supportWitness :
      goal c e ≠ goal c (actEdge (inverse h) e)) :
    ¬ (∀ x, goal (actCorner h c) x ↔ goal c x) := by
  intro sameLiteralFiber
  have hStabilizer :=
    identical_automorphic_corner_fibers_require_edge_stabilizer
      actCorner actEdge inverse goal edgeRightInverse goalCovariant
      h c sameLiteralFiber e
  exact supportWitness (propext hStabilizer)

end CubeRev025
