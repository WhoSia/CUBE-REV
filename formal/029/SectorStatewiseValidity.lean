import FrozenJsonSectorParser

namespace CubeRev029.Nineteen

/-- A finite-state phrasing of certificate validity. At each read node,
we check the child reached by each currently surviving candidate state.
This eliminates any need to enumerate the infinitely many Nat reply
values: only *feasible* response fibers matter. -/
def StatewiseSectorValid {S Q R : Type} [DecidableEq R]
    (graph : Array (FrozenInstruction Q R Unit))
    (observe : S → Q → R) (sign : S → Bool) :
    (budget : Nat) → (idx : Nat) → (belief : List S) → Prop
  | 0, idx, belief =>
      match graph[idx]? with
      | some (.finish _) => AtMostOnePerSign sign belief
      | _ => False
  | n+1, idx, belief =>
      match graph[idx]? with
      | none => False
      | some (.finish _) => AtMostOnePerSign sign belief
      | some (.choose q child) =>
          ∀ state, state ∈ belief →
            StatewiseSectorValid graph observe sign n
              (child (observe state q))
              (finiteReplyFiber observe belief q (observe state q))
      | some (.padding _ child) =>
          StatewiseSectorValid graph observe sign n child belief

/-- Exact equivalence between quantifying over feasible replies and
quantifying over the finite surviving candidate states. This is the
logical justification for a statewise certificate verifier: it checks
only replies that some actual candidate can produce, without silently
discarding a branch that could occur physically. -/
theorem statewise_sector_valid_iff_semantic {S Q R : Type}
    [DecidableEq R]
    (graph : Array (FrozenInstruction Q R Unit))
    (observe : S → Q → R) (sign : S → Bool) :
    ∀ budget root belief,
      SemanticallyValidSector graph observe sign budget root belief ↔
        StatewiseSectorValid graph observe sign budget root belief := by
  intro budget
  induction budget with
  | zero =>
      intro root belief
      rfl
  | succ n ih =>
      intro root belief
      cases nodeEq : graph[root]? with
      | none =>
          simp [SemanticallyValidSector, StatewiseSectorValid, nodeEq]
      | some instruction =>
          cases instruction with
          | finish output =>
              simp [SemanticallyValidSector, StatewiseSectorValid, nodeEq]
          | padding query child =>
              simpa [SemanticallyValidSector, StatewiseSectorValid, nodeEq]
                using ih child belief
          | choose query child =>
              simp only [SemanticallyValidSector, StatewiseSectorValid, nodeEq]
              constructor
              · intro valid state present
                exact (ih (child (observe state query))
                  (finiteReplyFiber observe belief query
                    (observe state query))).mp
                  (valid (observe state query) ⟨state, present, rfl⟩)
              · intro valid reply feasible
                obtain ⟨state, present, same⟩ := feasible
                have childValid := (ih (child (observe state query))
                  (finiteReplyFiber observe belief query
                    (observe state query))).mpr (valid state present)
                simpa only [same] using childValid

/-- Combined theorem that directly consumes the *finite-candidate*
statewise validity specification and returns the exact tagged
terminal answer. The sign is still an argument to a returned decoder:
the policy never queries an unobserved Bool oracle. -/
theorem statewise_checked_sector_recovers_each_candidate {S Q R : Type}
    [DecidableEq R]
    (graph : Array (FrozenInstruction Q R Unit))
    (observe : S → Q → R) (sign : S → Bool)
    (budget root : Nat) (belief : List S)
    (verified : StatewiseSectorValid graph observe sign
      budget root belief)
    (state : S) (member : state ∈ belief) :
    ((compileSectorDecoder graph observe sign budget root belief).val.run
      observe state) (sign state) = some state := by
  exact valid_sector_compilation_recovers_each_candidate
    graph observe sign budget root belief
    ((statewise_sector_valid_iff_semantic graph observe sign
      budget root belief).mpr verified)
    state member

#print axioms statewise_sector_valid_iff_semantic
#print axioms statewise_checked_sector_recovers_each_candidate

end CubeRev029.Nineteen
