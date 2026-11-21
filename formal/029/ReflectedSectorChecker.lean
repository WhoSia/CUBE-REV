import ExactEightSector

namespace CubeRev029.Nineteen

/-- A transparent finite Boolean universal quantifier, used instead of
classical infinitary decision procedures. The only states inspected by
this checker are the actual, surviving elements of the finite belief. -/
def allFinite {S : Type} (test : S → Bool) : List S → Bool
  | [] => true
  | x :: xs => test x && allFinite test xs

theorem allFinite_true_implies_every_member {S : Type}
    (test : S → Bool) :
    ∀ xs : List S, allFinite test xs = true →
      ∀ x, x ∈ xs → test x = true := by
  intro xs
  induction xs with
  | nil =>
      intro valid x member
      cases member
  | cons head tail ih =>
      intro valid x member
      have both : test head = true ∧ allFinite test tail = true := by
        simpa [allFinite, Bool.and_eq_true] using valid
      rcases List.mem_cons.mp member with same | inTail
      · subst x
        exact both.1
      · exact ih both.2 x inTail

/-- One may decode by sign at a leaf precisely when no two distinct
surviving candidates have the same permutation sign. This finite
executable check makes BOTH identity and sign comparisons explicit. -/
def checkSignUnique {S : Type} [DecidableEq S]
    (sign : S → Bool) (belief : List S) : Bool :=
  allFinite (fun a =>
    allFinite (fun b => decide (sign a ≠ sign b ∨ a = b)) belief) belief

theorem checkSignUnique_sound {S : Type} [DecidableEq S]
    (sign : S → Bool) (belief : List S)
    (accepted : checkSignUnique sign belief = true) :
    AtMostOnePerSign sign belief := by
  intro a ha b hb same
  have outer := allFinite_true_implies_every_member
    (fun a => allFinite (fun b =>
      decide (sign a ≠ sign b ∨ a = b)) belief)
    belief accepted a ha
  have pair := allFinite_true_implies_every_member
    (fun b => decide (sign a ≠ sign b ∨ a = b))
    belief outer b hb
  by_contra different
  have notDiffSign : ¬sign a ≠ sign b := fun unequal => unequal same
  simp [notDiffSign, different] at pair

/-- A total, terminating, executable finite proof checker. It recurses
on the actual remaining-read budget, not on arbitrary JSON graph
indices, so cycles in an untrusted graph cannot cause nontermination.
A read checks one branch per surviving state (duplicates harmless), a
repeat consumes one real read, and a leaf checks exact per-sign
uniqueness. No node can pass after a malformed budget exhaustion. -/
def checkFiniteSector {S Q R : Type}
    [DecidableEq S] [DecidableEq R]
    (graph : Array (FrozenInstruction Q R Unit))
    (observe : S → Q → R) (sign : S → Bool) :
    (budget : Nat) → (root : Nat) → (belief : List S) → Bool
  | 0, idx, belief =>
      match graph[idx]? with
      | some (.finish _) => checkSignUnique sign belief
      | _ => false
  | n+1, idx, belief =>
      match graph[idx]? with
      | none => false
      | some (.finish _) => checkSignUnique sign belief
      | some (.choose q child) =>
          allFinite (fun state =>
            checkFiniteSector graph observe sign n (child (observe state q))
              (finiteReplyFiber observe belief q (observe state q))) belief
      | some (.padding _ child) =>
          checkFiniteSector graph observe sign n child belief

/-- Soundness is for EVERY typed graph and finite candidate list, not
an assumption about one particular frozen certificate. The Boolean
checker cannot accept a feasible response branch that breaks exact
posterior semantics. All graph arrays, including cyclic or corrupt
ones, remain well-founded because the budget strictly decreases. -/
theorem checkFiniteSector_sound {S Q R : Type}
    [DecidableEq S] [DecidableEq R]
    (graph : Array (FrozenInstruction Q R Unit))
    (observe : S → Q → R) (sign : S → Bool) :
    ∀ budget root belief,
      checkFiniteSector graph observe sign budget root belief = true →
      StatewiseSectorValid graph observe sign budget root belief := by
  intro budget
  induction budget with
  | zero =>
      intro root belief accepted
      cases found : graph[root]? with
      | none =>
          simp [checkFiniteSector, found] at accepted
      | some instruction =>
          cases instruction with
          | finish value =>
              change AtMostOnePerSign sign belief
              apply checkSignUnique_sound
              simpa [checkFiniteSector, found] using accepted
          | choose q child =>
              simp [checkFiniteSector, found] at accepted
          | padding q child =>
              simp [checkFiniteSector, found] at accepted
  | succ n ih =>
      intro root belief accepted
      cases found : graph[root]? with
      | none =>
          simp [checkFiniteSector, found] at accepted
      | some instruction =>
          cases instruction with
          | finish value =>
              change AtMostOnePerSign sign belief
              apply checkSignUnique_sound
              simpa [checkFiniteSector, found] using accepted
          | padding q child =>
              have nextValid : checkFiniteSector graph observe sign
                  n child belief = true := by
                simpa [checkFiniteSector, found] using accepted
              simpa [StatewiseSectorValid, found] using
                ih child belief nextValid
          | choose q child =>
              have validReplies : ∀ state, state ∈ belief →
                  StatewiseSectorValid graph observe sign n
                    (child (observe state q))
                    (finiteReplyFiber observe belief q
                      (observe state q)) := by
                intro state present
                have allChecked :
                      allFinite (fun s =>
                      checkFiniteSector graph observe sign n
                        (child (observe s q))
                        (finiteReplyFiber observe belief q (observe s q)))
                      belief = true := by
                  simpa [checkFiniteSector, found] using accepted
                have thisChecked :=
                  allFinite_true_implies_every_member
                    (fun s =>
                      checkFiniteSector graph observe sign n
                        (child (observe s q))
                        (finiteReplyFiber observe belief q (observe s q)))
                    belief allChecked state present
                exact ih (child (observe state q))
                  (finiteReplyFiber observe belief q (observe state q))
                  thisChecked
              simpa only [StatewiseSectorValid, found] using validReplies

/-- The first executable, proof-reflected integration with the exact
eight-read sign-deferred policy. A TRUE finite Boolean result is a
trusted premise for correct recovery, without assuming correctness of
the external JSON or using a corner-parity oracle during query choice. -/
theorem checked_eight_sector_recovers
    {S Q R : Type} [DecidableEq S] [DecidableEq R]
    (fallback : Q)
    (graph : Array (FrozenInstruction Q R Unit))
    (observe : S → Q → R) (sign : S → Bool)
    (root : Nat) (belief : List S)
    (accepted : checkFiniteSector graph observe sign 8 root belief = true)
    (state : S) (member : state ∈ belief) :
    ((exactEightSectorPolicy fallback graph observe sign root belief).run
        observe state) (sign state) = some state := by
  exact exact_eight_sector_recovers_given_terminal_sign
    fallback graph observe sign root belief
    (checkFiniteSector_sound graph observe sign 8 root belief accepted)
    state member

/-- Negative-control / positive-control sector:
two distinct candidates with opposite sign may be a valid zero-read leaf,
but same-sign ambiguity can never pass. -/
private def testLeafGraph : Array (FrozenInstruction Nat Nat Unit) :=
  #[.finish ()]

private def testSign (n : Nat) : Bool := n % 2 == 1

theorem opposite_sign_leaf_accepted :
    checkFiniteSector testLeafGraph (fun s (_ : Nat) => s)
      testSign 0 0 [0,1] = true := by
  decide +kernel

theorem same_sign_leaf_rejected :
    checkFiniteSector testLeafGraph (fun s (_ : Nat) => s)
      testSign 0 0 [0,2] = false := by
  decide +kernel

#print axioms allFinite_true_implies_every_member
#print axioms checkSignUnique_sound
#print axioms checkFiniteSector_sound
#print axioms checked_eight_sector_recovers
#print axioms opposite_sign_leaf_accepted
#print axioms same_sign_leaf_rejected

end CubeRev029.Nineteen
