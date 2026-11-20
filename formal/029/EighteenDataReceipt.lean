import EighteenReadData

open CubeRev029.Eighteen

private def pinned : String := include_str "EIGHTEEN_QUERY_DAG.json"

private def hasExpectedReceipt : Bool :=
  match check pinned with
  | .ok receipt => receipt == ⟨6274, 43870, 1418, 87740⟩
  | .error _ => false

/-- Receipt for the exact data bytes embedded at build time. This theorem
does not assert the semantic EdgeLift conditions for arbitrary completions. -/
theorem cuberev_eighteen_data_receipt : hasExpectedReceipt = true := by
  native_decide

#print axioms cuberev_eighteen_data_receipt
