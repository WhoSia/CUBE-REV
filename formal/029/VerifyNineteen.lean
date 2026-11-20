import NineteenReadData

open CubeRev029.Nineteen

def main (args : List String) : IO UInt32 := do
  let [path] := args | throw (IO.userError "Usage: lean --run VerifyNineteen.lean upper-policy-certificate.json")
  match check (← IO.FS.readFile path) with
  | .error err =>
    IO.eprintln err
    return 1
  | .ok receipt =>
    IO.println (reprStr receipt)
    return 0
