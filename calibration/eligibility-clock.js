(function (root, factory) {
  const api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  root.CubeRevEligibilityClock = api;
})(typeof globalThis !== "undefined" ? globalThis : this, function () {
  "use strict";

  function evaluate(context) {
    const checks = {
      governance_approved: context?.governance?.approved === true,
      clock_activation_enabled: context?.eligibility_clock?.activation_enabled === true,
      prospective_human_data_allowed: context?.collection?.prospective_human_data_allowed === true,
      collection_enabled: context?.collection?.enabled === true,
      server_participant_token: context?.linkage?.server_issued === true,
      source_bound_verified: context?.source_bound_verified === true,
      build_frozen: context?.build_frozen === true,
      protocol_frozen: context?.protocol_frozen === true,
      collector_receipt_verified: context?.collector_receipt_verified === true,
      two_pass_annotation_ready: context?.two_pass_annotation_ready === true,
      authorization_present: !!context?.eligibility_clock?.authorization_id
    };
    const reasons = Object.entries(checks).filter(([, ok]) => !ok).map(([name]) => name);
    return Object.freeze({
      state: reasons.length ? "NOT_STARTED" : "ELIGIBLE_TO_ACTIVATE",
      eligible: reasons.length === 0,
      activated: false,
      checked_at: new Date().toISOString(),
      checks: Object.freeze(checks),
      blocking_reasons: Object.freeze(reasons)
    });
  }
  function activate() {
    throw new Error("Prospective clock activation is governance-controlled and unavailable in this build.");
  }
  return { evaluate, activate };
});
