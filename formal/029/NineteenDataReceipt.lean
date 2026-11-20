import NineteenReadData

open CubeRev029.Nineteen

private def pinned : String := include_str "upper-policy-certificate.json"

private def hasExpectedReceipt : Bool :=
  match check pinned with
  | .ok receipt => receipt == ⟨52, 1362, 144736, 141097, 3188, 70774⟩
  | .error _ => false

/-- Receipt for the S policy in representative coordinates. -/
theorem cuberev_nineteen_data_receipt : hasExpectedReceipt = true := by
  native_decide

#print axioms cuberev_nineteen_data_receipt
