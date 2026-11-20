import SemanticGraph

namespace CubeRev029.Eighteen

/-- Encode the one slot move described by the original record sort, or
the fixed oriented label described by the original second-color response. -/
def actionAt (p : Position) (q : Address) (reply : Nat) : Except String Action := do
  let seen := p.record[q.1]!
  if seen == blank then
    let pending := p.record.set q.1 reply
    let i := (List.range pending.length).countP (fun k =>
      pending[k]! < reply || (pending[k]! == reply && k < q.1))
    return .first i
  else
    let possibilities := p.labels.flatMap fun id => [2 * id, 2 * id + 1]
    let some fixed := possibilities.find? (fun id => sticker id false == seen && sticker id true == reply)
      | throw "Second read specifies no oriented edge."
    return .second fixed

def Action.lift (action : Action) (q : Address) (w : Word) : Word :=
  match action with
  | .first j => restoreFirst q.1 j q.2 w
  | .second fixed => w.insertIdx q.1 fixed

/-- Build the finite graph from the original certificate, in budget order.
The chosen sample pair is for node nonemptiness. The semantic validator
independently checks the premises for lifting every admissible word. -/
def loadSemantic (source : String) : Except String Graph := do
  let obj ← (← Lean.Json.parse source).getObj?
  let rows ← obj.toList.mapM (fun (key, row) => do
    return (← parsePosition key, ← row.getArr?))
  let mut nodes : Array Node := #[]
  let mut index : Std.HashMap Position Nat := {}
  for budget in List.range 19 do
    for (position, inputs) in rows do
      if position.budget == budget then
        if index.contains position then throw "Repeated canonical node."
        let mut arcs := #[]
        let mut witnesses : Option Pair := none
        if budget == 0 then
          witnesses := some (← wordPair position inputs.toList)
        else
          let addresses := queryAddresses position.record
          unless inputs.size == addresses.length && inputs.size > 0 do throw "Query coverage mismatch."
          for (q, answer) in addresses.zip inputs.toList do
            let some c := readColor (← answer.getStr?) | throw "Invalid color."
            let (child, _) ← invert position q.1 q.2 c
            let some target := index[child]? | throw "Missing earlier child."
            let action ← actionAt position q c
            arcs := arcs.push ⟨q, c, target, action⟩
            if witnesses.isNone then
              let reached := nodes[target]!
              witnesses := some (action.lift q reached.left, action.lift q reached.right)
        let some (left, right) := witnesses | throw "Missing node witnesses."
        index := index.insert position nodes.size
        nodes := nodes.push ⟨position, left, right, arcs⟩
  let some even := index[root 0]? | throw "Missing even root."
  let some odd := index[root 1]? | throw "Missing odd root."
  return ⟨nodes, even, odd⟩

def loadChecked (source : String) : Except String Graph := do
  let graph ← loadSemantic source
  if graph.valid then return graph else throw "Invalid universal transition or witness."

end CubeRev029.Eighteen
