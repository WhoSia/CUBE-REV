import FrozenRootReflection

namespace CubeRev029.Nineteen

/-- This is the same immutable JSON file used by NineteenDataReceipt,
and restored only after the raw SHA-256 check in the read-only workflow.
There is NO copied or hand-built approximation of its 52 decision trees. -/
private def immutableUpperSource : String :=
  include_str "upper-policy-certificate.json"

/-- Concrete verification of ALL fifty-two frozen representative roots
under the newly proved exact finite-candidate semantic checker.

Unlike a count-only audit, the evaluated Boolean examines the actual
posterior and the actual response-labeled branches at every reachable
tree node, with exactly the frozen address and color coding. The
original 52-root receipt is also rechecked on the identical JSON bytes.

Trust boundary: native_decide on an immutable, SHA-256-checked data
artifact. The universal implication check=true -> sector soundness was
proved separately in the kernel without native_decide. -/
theorem fifty_two_frozen_roots_semantically_accepted :
    certifiedFrozenRoots immutableUpperSource = true := by
  native_decide

/-- For every entry of the genuine, immutable source file, acceptance
of the single frozen receipt now supplies an exact typed graph and
correct, actual eight-read sign-deferred continuation. No extra
enumeration of policies or assumptions about the finite leaves are
introduced in this theorem. -/
theorem every_actual_frozen_root_recovers
    (roots : Array Lean.Json)
    (parsed : parsedRepresentativeArray immutableUpperSource = .ok roots)
    (entry : Lean.Json) (member : entry ∈ roots.toList) :
    ∃ (graph : Array (FrozenInstruction Nat Nat Unit))
      (belief : List Eighteen.Word),
      parseRepresentativeRoot entry = .ok (graph, belief) ∧
      (∀ word, word ∈ belief →
        ((exactEightSectorPolicy 0 graph observation edgeWordSign
          0 belief).run observation word) (edgeWordSign word) =
          some word) := by
  exact certified_source_each_root_recovers
    immutableUpperSource roots parsed
    fifty_two_frozen_roots_semantically_accepted entry member

#print axioms fifty_two_frozen_roots_semantically_accepted
#print axioms every_actual_frozen_root_recovers

end CubeRev029.Nineteen
