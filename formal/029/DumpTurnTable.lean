import FaceTurns

open CubeRev029.Physical

/-- One line per quarter turn: the image of slots 0..47 under `turnSlot`. -/
def turnRow (t : Nat) : String :=
  if ht : t < 12 then
    String.intercalate " " ((List.range 48).map fun s =>
      if hs : s < 48 then toString (turnSlot ⟨t, ht⟩ ⟨s, hs⟩).val else "")
  else ""

def main : IO Unit :=
  (List.range 12).forM fun t => IO.println (turnRow t)
