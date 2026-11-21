import SignedSectorLeaf

namespace CubeRev029.Nineteen

/-- An exact posterior update for a finite representative candidate sector.
Unlike histogram keying, this retains full oriented-edge state identity. -/
def finiteReplyFiber {S Q R : Type} [DecidableEq R]
    (observe : S → Q → R) (belief : List S) (q : Q) (r : R) :
    List S :=
  belief.filter (fun s => decide (observe s q = r))

theorem finite_reply_fiber_mem {S Q R : Type} [DecidableEq R]
    (observe : S → Q → R) (belief : List S) (q : Q) (r : R)
    (s : S) :
    s ∈ finiteReplyFiber observe belief q r ↔
      s ∈ belief ∧ observe s q = r := by
  simp [finiteReplyFiber]

/-- Interpret a frozen typed instruction graph as an eight-read continuation
that RETURNS A SIGN-INDEXED DECODER, rather than receiving the corner sign
as a hidden oracle before the last observation. Missing nodes return none
and padding still consumes one full paired frame. -/
def compileSectorDecoder {S Q R : Type} [DecidableEq R]
    (graph : Array (FrozenInstruction Q R Unit))
    (observe : S → Q → R) (sign : S → Bool) :
    (budget : Nat) → (idx : Nat) → (belief : List S) →
      {tree : Policy Q R (Bool → Option S) // Fits budget tree}
  | 0, idx, belief =>
      match graph[idx]? with
      | some (.finish _) =>
          ⟨.stop (fun bit => firstCandidateWithSign sign bit belief),
            Fits.stop 0 _⟩
      | _ =>
          ⟨.stop (fun _ => none), Fits.stop 0 _⟩
  | n+1, idx, belief =>
      match graph[idx]? with
      | none => ⟨.stop (fun _ => none), Fits.stop (n+1) _⟩
      | some (.finish _) =>
          ⟨.stop (fun bit => firstCandidateWithSign sign bit belief),
            Fits.stop (n+1) _⟩
      | some (.choose q child) =>
          let next := fun r =>
            compileSectorDecoder graph observe sign n (child r)
              (finiteReplyFiber observe belief q r)
          ⟨.read q (fun r => (next r).val),
            Fits.read n q _ (fun r => (next r).property)⟩
      | some (.padding q child) =>
          let next := compileSectorDecoder graph observe sign n child belief
          ⟨.read q (fun _ => next.val),
            Fits.read n q _ (fun _ => next.property)⟩

/-- Exactly the semantic premise needed to trust a compiled certificate:
each reached leaf has at most one distinct candidate of each sign,
and every feasible response descends to a certified child sector.
Infeasible replies are allowed to fail closed, but a real state never
takes such a branch. The budget decreases on each read/repeat. -/
def SemanticallyValidSector {S Q R : Type} [DecidableEq R]
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
          ∀ reply, (∃ s, s ∈ belief ∧ observe s q = reply) →
            SemanticallyValidSector graph observe sign n (child reply)
              (finiteReplyFiber observe belief q reply)
      | some (.padding _ child) =>
          SemanticallyValidSector graph observe sign n child belief

theorem compiled_sector_fits_all_replies {S Q R : Type} [DecidableEq R]
    (graph : Array (FrozenInstruction Q R Unit))
    (observe : S → Q → R) (sign : S → Bool)
    (budget root : Nat) (belief : List S) :
    Fits budget (compileSectorDecoder graph observe sign budget root belief).val :=
  (compileSectorDecoder graph observe sign budget root belief).property

/-- The actual sector checker is a *soundness specification* rather than a
count-only receipt: if every reachable typed node satisfies its finite
posterior invariant, the entire adaptive policy returns a sign decoder
that reconstructs every original candidate on its own true sign.

The corner-sign bit is applied only to the RETURNED function at termination.
A later physical proof must derive that bit from the actual nineteen corner
sticker reads; this theorem does not grant a sign oracle. -/
theorem valid_sector_compilation_recovers_each_candidate {S Q R : Type}
    [DecidableEq R]
    (graph : Array (FrozenInstruction Q R Unit))
    (observe : S → Q → R) (sign : S → Bool) :
    ∀ budget root belief,
      SemanticallyValidSector graph observe sign budget root belief →
      ∀ state, state ∈ belief →
        ((compileSectorDecoder graph observe sign budget root belief).val.run
          observe state) (sign state) = some state := by
  intro budget
  induction budget with
  | zero =>
      intro root belief certified state present
      cases eq : graph[root]? with
      | none =>
          simp [SemanticallyValidSector, eq] at certified
      | some instruction =>
          cases instruction with
          | finish output =>
              have leaf : AtMostOnePerSign sign belief := by
                simpa [SemanticallyValidSector, eq] using certified
              have right := first_candidate_is_correct_of_sign_unique
                sign belief leaf state present
              simpa [compileSectorDecoder, eq, Policy.run] using right
          | choose q child =>
              simp [SemanticallyValidSector, eq] at certified
          | padding q child =>
              simp [SemanticallyValidSector, eq] at certified
  | succ n ih =>
      intro root belief certified state present
      cases eq : graph[root]? with
      | none =>
          simp [SemanticallyValidSector, eq] at certified
      | some instruction =>
          cases instruction with
          | finish output =>
              have leaf : AtMostOnePerSign sign belief := by
                simpa [SemanticallyValidSector, eq] using certified
              have right := first_candidate_is_correct_of_sign_unique
                sign belief leaf state present
              simpa [compileSectorDecoder, eq, Policy.run] using right
          | choose q child =>
              have branches : ∀ reply,
                  (∃ x, x ∈ belief ∧ observe x q = reply) →
                  SemanticallyValidSector graph observe sign n (child reply)
                    (finiteReplyFiber observe belief q reply) := by
                simpa [SemanticallyValidSector, eq] using certified
              have possible := branches (observe state q) ⟨state, present, rfl⟩
              have member : state ∈
                  finiteReplyFiber observe belief q (observe state q) := by
                exact (finite_reply_fiber_mem
                  observe belief q (observe state q) state).2
                    ⟨present, rfl⟩
              have solved := ih (child (observe state q))
                (finiteReplyFiber observe belief q (observe state q))
                possible state member
              simpa [compileSectorDecoder, eq, Policy.run] using solved
          | padding q child =>
              have continuing : SemanticallyValidSector graph observe sign
                  n child belief := by
                simpa [SemanticallyValidSector, eq] using certified
              have solved := ih child belief continuing state present
              simpa [compileSectorDecoder, eq, Policy.run] using solved

#print axioms finite_reply_fiber_mem
#print axioms compiled_sector_fits_all_replies
#print axioms valid_sector_compilation_recovers_each_candidate

end CubeRev029.Nineteen
