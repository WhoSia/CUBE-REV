import SemanticInput

open CubeRev029.Eighteen

def main (args : List String) : IO UInt32 := do
  let [file] := args | throw (IO.userError "Pass the original uncompressed certificate.")
  match loadChecked (← IO.FS.readFile file) with
  | .error msg => IO.eprintln msg; return 1
  | .ok graph =>
      let arcs := graph.nodes.foldl (fun n node => n + node.arcs.size) 0
      IO.println s!"semantic graph: {graph.nodes.size} nodes, {arcs} universal arcs, both roots"
      return 0
