import ResidualDecidable

namespace CubeRev029.Eighteen

inductive Action where
  | first (destination : Nat)
  | second (word : Nat)
  deriving Inhabited

structure Arc where
  address : Address
  color : Nat
  destination : Nat
  action : Action
  deriving Inhabited

instance : Inhabited Position := ⟨root 0⟩

structure Node where
  position : Position
  left : Word
  right : Word
  arcs : Array Arc
  deriving Inhabited

structure Graph where
  nodes : Array Node
  even : Nat
  odd : Nat
  deriving Inhabited

def Graph.pos (g : Graph) (i : Nat) : Position := g.nodes[i]!.position

def Action.valid (action : Action) (p child : Position) (q : Address) (color : Nat) : Prop :=
  match action with
  | .first j => FirstStep p child q.1 j q.2 color
  | .second fixed => q.2 = true ∧ color = sticker fixed true ∧ SecondStep p child q.1 fixed

instance decideAction (action : Action) (p child : Position) (q : Address) (color : Nat) :
    Decidable (action.valid p child q color) := by
  cases action <;> unfold Action.valid <;> infer_instance

theorem Action.edgeLift {action : Action} {p child : Position} {q : Address} {color : Nat}
    (valid : action.valid p child q color) :
    Nonempty (EdgeLift observeWord (Completes p) (Completes child) q color) := by
  cases action with
  | first j => exact ⟨FirstStep.asEdgeLift valid⟩
  | second w =>
      obtain ⟨hs, eq, transition⟩ := valid
      rcases q with ⟨i, side⟩
      change side = true at hs
      subst side color
      exact ⟨transition.asEdgeLift⟩

def addressAt (k : Nat) : Address := (k / 2, k % 2 == 1)

def known (p : Position) (q : Address) : Prop :=
  q.2 = false ∧ p.record[q.1]! ≠ blank

instance decideKnown (p : Position) (q : Address) : Decidable (known p q) := by
  unfold known
  infer_instance

def validateReply (g : Graph) (n : Node) (q : Address) : Prop :=
  if n.position.budget = 0 ∨ known n.position q then True
  else match n.arcs.find? (fun a => a.address == q) with
    | none => False
    | some a => a.destination < g.nodes.size ∧ (g.pos a.destination).budget + 1 = n.position.budget ∧
                 a.action.valid n.position (g.pos a.destination) q a.color

instance decideReply (g : Graph) (n : Node) (q : Address) : Decidable (validateReply g n q) := by
  unfold validateReply
  split
  · exact isTrue trivial
  · split <;> infer_instance

def validNode (g : Graph) (n : Node) : Prop :=
  Completes n.position n.left ∧ Completes n.position n.right ∧ n.left ≠ n.right ∧
    ∀ i : Fin (2 * n.position.record.length), validateReply g n (addressAt i)

instance decideNode (g : Graph) (n : Node) : Decidable (validNode g n) := by
  unfold validNode
  infer_instance

def Graph.valid (g : Graph) : Prop :=
  g.even < g.nodes.size ∧ g.odd < g.nodes.size ∧ g.pos g.even = root 0 ∧ g.pos g.odd = root 1 ∧
    ∀ n : Fin g.nodes.size, validNode g g.nodes[n.val]!

instance decideGraph (g : Graph) : Decidable g.valid := by
  unfold Graph.valid
  infer_instance

theorem address_roundtrip (q : Address) :
    addressAt (2 * q.1 + q.2.toNat) = q := by
  rcases q with ⟨i, side⟩
  cases side <;> simp [addressAt] <;> omega

theorem known_response (h : known p q) (hw : Completes p w) (inside : q.1 < p.record.length) :
    observeWord w q = p.record[q.1]! := by
  rcases q with ⟨i, side⟩
  obtain ⟨hs, hc⟩ := h
  change side = false at hs
  subst side
  apply agrees_lookup hw.record
  · rw [List.getElem!_eq_getElem?_getD, List.getElem?_eq_getElem inside]
    rfl
  · exact hc

/-- A checked finite graph is a semantic adversarial certificate over all
words, using the universal lift theorem at every fresh query. -/
def Graph.certificate (g : Graph) (valid : g.valid) :
    ResidualCertificate observeWord (Fin g.nodes.size) where
  remaining node := (g.pos node.val).budget
  belief node := Completes (g.pos node.val)
  witnesses node := by
    obtain ⟨ha, hb, distinct, _⟩ := valid.2.2.2.2 node
    exact ⟨g.nodes[node.val]!.left, g.nodes[node.val]!.right, ha, hb, distinct⟩
  respond node q positive := by
    let n := g.nodes[node.val]!
    change 0 < n.position.budget at positive
    change (∃ r, ∀ w, Completes n.position w → observeWord w q = r) ∨ _
    by_cases inside : q.1 < n.position.record.length
    · by_cases h : known n.position q
      · exact .inl ⟨n.position.record[q.1]!, fun _ hw => known_response h hw inside⟩
      · let k : Fin (2 * n.position.record.length) :=
          ⟨2*q.1 + q.2.toNat, by have := Bool.toNat_le q.2; omega⟩
        have reply := (valid.2.2.2.2 node).2.2.2 k
        change validateReply g n (addressAt k.val) at reply
        have eq : addressAt k.val = q := address_roundtrip q
        have active : ¬ (n.position.budget = 0 ∨ known n.position q) := by
          intro off
          exact off.elim (by omega) h
        rw [eq, validateReply, ite_eq_right active] at reply
        cases found : n.arcs.find? (fun a => a.address == q) with
        | none => simp [found] at reply
        | some a =>
            rw [found] at reply
            obtain ⟨fits, less, action⟩ := reply
            exact .inr ⟨⟨a.destination, fits⟩, a.color, less, Action.edgeLift (action := a.action) action⟩
    · exact .inl ⟨sticker 0 q.2, fun w hw =>
        observe_invalid w q (by have := agrees_length hw.record; omega)⟩

end CubeRev029.Eighteen
