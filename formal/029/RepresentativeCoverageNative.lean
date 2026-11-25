import RepresentativeRootInclusion

namespace CubeRev029.Nineteen

/-- The ONLY new `native_decide` of BS-3. Trust boundary: the compiled
evaluation of `coverageCheck` on the same SHA-256-pinned certificate bytes
as `fifty_two_frozen_roots_semantically_accepted`. -/
theorem representative_prefixes_covered_source :
    coverageCheck (include_str "upper-policy-certificate.json") = true := by
  native_decide

#print axioms representative_prefixes_covered_source

end CubeRev029.Nineteen
