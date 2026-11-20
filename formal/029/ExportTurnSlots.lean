import FaceTurns

open CubeRev029.Physical

def main : IO Unit := do
  let maps := (List.finRange 12).map fun t => (List.finRange 48).map fun s => (turnSlot t s).val
  IO.println (Lean.toJson maps).compress
