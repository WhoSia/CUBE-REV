import SemanticInput

open CubeRev029.Eighteen

/-- Change a stored operation while preserving the witnesses, address,
reply and requested budget. Only its universal transition is invalid. -/
def badArc (graph : Graph) (first : Bool) : Except String Graph := do
  for i in List.range graph.nodes.size do
    let node := graph.nodes[i]!
    for j in List.range node.arcs.size do
      let arc := node.arcs[j]!
      let corrupted := match arc.action, first with
        | .first slot, true => some {arc with action := .first (slot + node.position.record.length)}
        | .second w, false => some {arc with action := .second (reverseWord w)}
        | _, _ => none
      if let some other := corrupted then
        return {graph with nodes := graph.nodes.set! i {node with arcs := node.arcs.set! j other}}
  throw "Missing target transition."

def main (args : List String) : IO Unit := do
  let [file] := args | throw (IO.userError "Pass the original uncompressed certificate.")
  let .ok graph := loadChecked (← IO.FS.readFile file)
    | throw (IO.userError "The original graph failed validation.")
  for (first, label) in [(true, "first-read position"), (false, "second-read orientation")] do
    let .ok changed := badArc graph first | throw (IO.userError ("No target for " ++ label))
    if changed.valid then throw (IO.userError ("Accepted corrupt " ++ label))
    IO.println ("REJECTED corrupt universal " ++ label)
