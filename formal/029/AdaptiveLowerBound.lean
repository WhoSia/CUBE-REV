import Std

namespace CubeRev029

universe u v w x

/-- The next address is selected before its answer is known. -/
inductive Policy (Q : Type v) (R : Type w) (O : Type x) where
  | stop : O → Policy Q R O
  | read : Q → (R → Policy Q R O) → Policy Q R O

def Policy.run (observe : S → Q → R) (state : S) : Policy Q R O → O
  | .stop output => output
  | .read query next => run observe state (next (observe state query))

inductive Fits : Nat → Policy Q R O → Prop where
  | stop (n : Nat) (output : O) : Fits n (.stop output)
  | read (n : Nat) (query : Q) (next : R → Policy Q R O) :
      (∀ reply, Fits n (next reply)) → Fits (n + 1) (.read query next)

def posterior (observe : S → Q → R) (belief : S → Prop) (q : Q) (r : R) : S → Prop :=
  fun s => belief s ∧ observe s q = r

def Ambiguous (belief : S → Prop) : Prop :=
  ∃ s t, belief s ∧ belief t ∧ s ≠ t

def Adversary (observe : S → Q → R) : Nat → (S → Prop) → Prop
  | 0, belief => Ambiguous belief
  | n + 1, belief => ∀ q, ∃ r, Adversary observe n (posterior observe belief q r)

/-- The witness pair survives even when the observer stops early. -/
theorem adversary_ambiguous (someQuery : Q) {observe : S → Q → R} {n : Nat}
    {belief : S → Prop} (h : Adversary observe n belief) : Ambiguous belief := by
  induction n generalizing belief with
  | zero =>
      exact h
  | succ n ih =>
      obtain ⟨reply, child⟩ := h someQuery
      obtain ⟨s, t, hs, ht, distinct⟩ := ih child
      exact ⟨s, t, hs.1, ht.1, distinct⟩

/-- A response for every legal query, followed by leaf collisions, defeats
every policy within the given budget, including policies with early stops. -/
theorem adversary_collision (someQuery : Q) {observe : S → Q → R} {n : Nat}
    {belief : S → Prop} (h : Adversary observe n belief) {tree : Policy Q R O}
    (bounded : Fits n tree) :
    ∃ s t, belief s ∧ belief t ∧ s ≠ t ∧ tree.run observe s = tree.run observe t := by
  induction n generalizing belief tree with
  | zero =>
      cases bounded with
      | stop _ output =>
          obtain ⟨s, t, hs, ht, distinct⟩ := adversary_ambiguous someQuery h
          exact ⟨s, t, hs, ht, distinct, rfl⟩
  | succ n ih =>
      cases bounded with
      | stop _ output =>
          obtain ⟨s, t, hs, ht, distinct⟩ := adversary_ambiguous someQuery h
          exact ⟨s, t, hs, ht, distinct, rfl⟩
      | read _ query next branches =>
          obtain ⟨reply, child⟩ := h query
          obtain ⟨s, t, hs, ht, distinct, same⟩ := ih child (branches reply)
          refine ⟨s, t, hs.1, ht.1, distinct, ?_⟩
          simpa only [Policy.run, hs.2, ht.2] using same

/-- A query and reply adapter. The simulated query is determined by the
original address, and uses only the returned color and supplied side data. -/
def Policy.adapt (query : Q₂ → Q₁) (reply : Q₂ → R₁ → R₂) (output : O₂ → O₁) :
    Policy Q₂ R₂ O₂ → Policy Q₁ R₁ O₁
  | .stop result => .stop (output result)
  | .read q k => .read (query q) (fun a => adapt query reply output (k (reply q a)))

theorem Policy.adapt_run (query : Q₂ → Q₁) (reply : Q₂ → R₁ → R₂) (output : O₂ → O₁)
    (observe : S → Q₁ → R₁) (s : S) (tree : Policy Q₂ R₂ O₂) :
    (tree.adapt query reply output).run observe s =
      output (tree.run (fun state q => reply q (observe state (query q))) s) := by
  induction tree with
  | stop result => rfl
  | read q k ih =>
      simpa only [adapt, run] using ih (reply q (observe s (query q)))

theorem Policy.adapt_fits (query : Q₂ → Q₁) (reply : Q₂ → R₁ → R₂) (output : O₂ → O₁)
    {n : Nat} {tree : Policy Q₂ R₂ O₂} (fit : Fits n tree) :
    Fits n (tree.adapt query reply output) := by
  induction fit with
  | stop n result => exact .stop n (output result)
  | read n q k fit ih => exact .read n (query q) _ (fun a => ih (reply q a))

/-- Disclosing the corner configuration specializes any paired policy to
one edge read per frame. Both addresses still precede the response. -/
theorem paired_lower_bound_of_disclosed_corners (someEdge : E) (edgeColor : S → E → A)
    (knownCorner : C → B) (belief : S → Prop) {n : Nat}
    (hard : Adversary edgeColor n belief) {tree : Policy (E × C) (A × B) O}
    (fit : Fits n tree) :
    ∃ s t, belief s ∧ belief t ∧ s ≠ t ∧
      tree.run (fun state (q : E × C) => (edgeColor state q.1, knownCorner q.2)) s =
      tree.run (fun state (q : E × C) => (edgeColor state q.1, knownCorner q.2)) t := by
  let response : (E × C) → A → (A × B) := fun q a => (a, knownCorner q.2)
  have fit' := Policy.adapt_fits Prod.fst response (fun o : O => o) fit
  obtain ⟨s, t, hs, ht, hne, equal⟩ := adversary_collision someEdge hard fit'
  refine ⟨s, t, hs, ht, hne, ?_⟩
  simpa only [Policy.adapt_run, response] using equal

/-- A parent query is either known on the embedded child belief or
can be answered by one query in the child coordinates. -/
def Policy.pullback (query : Q₁ → Sum R Q₂) : Policy Q₁ R O → Policy Q₂ R O
  | .stop output => .stop output
  | .read q k =>
      match query q with
      | .inl r => pullback query (k r)
      | .inr q' => .read q' (fun r => pullback query (k r))

theorem Fits.succ (h : Fits n tree) : Fits (n + 1) tree := by
  induction h with
  | stop n output => exact .stop (n + 1) output
  | read n q k fit ih => exact .read (n + 1) q k ih

theorem Policy.pullback_fits (query : Q₁ → Sum R Q₂) {n : Nat}
    {tree : Policy Q₁ R O} (fit : Fits n tree) : Fits n (tree.pullback query) := by
  induction fit with
  | stop n output => exact .stop n output
  | read n q k fit ih =>
      cases eq : query q with
      | inl r =>
          simpa only [pullback, eq] using (ih r).succ
      | inr q' =>
          simpa only [pullback, eq] using (Fits.read n q' _ ih)

def mappedColor (observe : S → Q → R) (s : S) : Sum R Q → R
  | .inl r => r
  | .inr q => observe s q

theorem Policy.pullback_run (query : Q₁ → Sum R Q₂) (lift : S₂ → S₁)
    (parent : S₁ → Q₁ → R) (child : S₂ → Q₂ → R) (s : S₂)
    (covariant : ∀ q, parent (lift s) q = mappedColor child s (query q))
    (tree : Policy Q₁ R O) :
    (tree.pullback query).run child s = tree.run parent (lift s) := by
  induction tree with
  | stop output => rfl
  | read q k ih =>
      cases eq : query q with
      | inl r =>
          have h : parent (lift s) q = r := by simpa only [eq, mappedColor] using covariant q
          simpa only [pullback, run, eq, h] using ih r
      | inr q' =>
          have h : parent (lift s) q = child s q' := by simpa only [eq, mappedColor] using covariant q
          simpa only [pullback, run, eq, h] using ih (child s q')

structure EdgeLift (observe : S → Q → R) (parent child : S → Prop) (q : Q) (r : R) where
  embed : S → S
  query : Q → Sum R Q
  memory : ∀ s, child s → posterior observe parent q r (embed s)
  injective : ∀ s t, child s → child t → embed s = embed t → s = t
  compatible : ∀ s, child s → ∀ a, observe (embed s) a = mappedColor observe s (query a)

/-- A compact residual graph, with the semantic obligations of each lift
made explicit. Known colors may be returned without descending the graph. -/
structure ResidualCertificate (observe : S → Q → R) (N : Type) where
  remaining : N → Nat
  belief : N → S → Prop
  witnesses : ∀ node, Ambiguous (belief node)
  respond : ∀ node q, 0 < remaining node →
    (∃ r, ∀ s, belief node s → observe s q = r) ∨
    (∃ child r, remaining child + 1 = remaining node ∧
      Nonempty (EdgeLift observe (belief node) (belief child) q r))

theorem ResidualCertificate.collision {observe : S → Q → R} {N : Type}
    (cert : ResidualCertificate observe N) (node : N)
    {budget : Nat} (room : budget ≤ cert.remaining node)
    {tree : Policy Q R O} (fit : Fits budget tree) :
    ∃ s t, cert.belief node s ∧ cert.belief node t ∧ s ≠ t ∧
      tree.run observe s = tree.run observe t := by
  induction budget generalizing node tree with
  | zero =>
      cases fit with
      | stop _ output =>
          obtain ⟨s, t, hs, ht, distinct⟩ := cert.witnesses node
          exact ⟨s, t, hs, ht, distinct, rfl⟩
  | succ k ih =>
      cases fit with
      | stop _ output =>
          obtain ⟨s, t, hs, ht, distinct⟩ := cert.witnesses node
          exact ⟨s, t, hs, ht, distinct, rfl⟩
      | read _ q next branches =>
          rcases cert.respond node q (by omega) with ⟨r, known⟩ | ⟨child, r, size, ⟨lift⟩⟩
          · obtain ⟨s, t, hs, ht, distinct, same⟩ := ih node (by omega) (branches r)
            exact ⟨s, t, hs, ht, distinct, by simpa only [Policy.run, known s hs, known t ht] using same⟩
          · have bounded := Policy.pullback_fits lift.query (branches r)
            obtain ⟨s, t, hs, ht, distinct, same⟩ := ih child (by omega) bounded
            have a := lift.memory s hs
            have b := lift.memory t ht
            refine ⟨lift.embed s, lift.embed t, a.1, b.1,
              fun eq => distinct (lift.injective s t hs ht eq), ?_⟩
            rw [Policy.pullback_run lift.query lift.embed observe observe s (lift.compatible s hs),
                Policy.pullback_run lift.query lift.embed observe observe t (lift.compatible t ht)] at same
            simpa only [Policy.run, a.2, b.2] using same

theorem ResidualCertificate.paired_collision {N : Type} {edge : S → E → A}
    (cert : ResidualCertificate edge N) (node : N) (corner : C → B)
    {budget : Nat} (room : budget ≤ cert.remaining node)
    {tree : Policy (E × C) (A × B) O} (fit : Fits budget tree) :
    ∃ s t, cert.belief node s ∧ cert.belief node t ∧ s ≠ t ∧
      tree.run (fun state (q : E × C) => (edge state q.1, corner q.2)) s =
      tree.run (fun state (q : E × C) => (edge state q.1, corner q.2)) t := by
  let response : (E × C) → A → (A × B) := fun q a => (a, corner q.2)
  obtain ⟨s, t, hs, ht, distinct, same⟩ :=
    cert.collision node room (Policy.adapt_fits Prod.fst response (fun o : O => o) fit)
  exact ⟨s, t, hs, ht, distinct, by simpa only [Policy.adapt_run, response] using same⟩

def Policy.transcript (observe : S → Q → R) (state : S) : Policy Q R O → List (Q × R)
  | .stop _ => []
  | .read q next =>
      let r := observe state q
      (q, r) :: transcript observe state (next r)

/-- Record both the selected addresses and their answers as output. -/
def Policy.logged (revHistory : List (Q × R)) : Policy Q R O → Policy Q R (List (Q × R))
  | .stop _ => .stop revHistory.reverse
  | .read q next => .read q (fun r => logged ((q,r) :: revHistory) (next r))

theorem Policy.logged_run (observe : S → Q → R) (s : S) (tree : Policy Q R O)
    (revHistory : List (Q × R)) :
    (tree.logged revHistory).run observe s = revHistory.reverse ++ tree.transcript observe s := by
  induction tree generalizing revHistory with
  | stop output => simp [logged, run, transcript]
  | read q next ih =>
      simp only [logged, run, transcript]
      rw [ih (observe s q)]
      simp [List.reverse_cons, List.append_assoc]

theorem Policy.logged_fits {Q : Type v} {R : Type w} {O : Type x} {n : Nat} {tree : Policy Q R O}
    (fit : Fits n tree) (revHistory : List (Q × R)) :
    Fits n (tree.logged revHistory) := by
  induction fit generalizing revHistory with
  | stop n output => exact .stop n _
  | read n q next fit ih => exact .read n q _ (fun r => ih r ((q,r) :: revHistory))

theorem ResidualCertificate.paired_transcript_collision {N : Type} {edge : S → E → A}
    (cert : ResidualCertificate edge N) (node : N) (corner : C → B)
    {budget : Nat} (room : budget ≤ cert.remaining node)
    {tree : Policy (E × C) (A × B) O} (fit : Fits budget tree) :
    ∃ s t, cert.belief node s ∧ cert.belief node t ∧ s ≠ t ∧
      tree.transcript (fun state (q : E × C) => (edge state q.1, corner q.2)) s =
      tree.transcript (fun state (q : E × C) => (edge state q.1, corner q.2)) t := by
  obtain ⟨s, t, hs, ht, distinct, equal⟩ := cert.paired_collision node corner room
    (Policy.logged_fits fit [])
  exact ⟨s, t, hs, ht, distinct, by simpa [Policy.logged_run] using equal⟩

#print axioms adversary_collision
#print axioms paired_lower_bound_of_disclosed_corners
#print axioms ResidualCertificate.paired_transcript_collision

end CubeRev029
