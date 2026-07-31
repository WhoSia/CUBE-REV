(function (root, factory) {
  const api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  root.CubeRevExportDecoration = api;
})(typeof globalThis !== "undefined" ? globalThis : this, function () {
  "use strict";

  function decorate(session, state) {
    const out = structuredClone(session);
    out.calibration_0712 = {
      protocol_version: state.config.protocol_version,
      calibration_build_id: state.config.build_id,
      host_baseline_version: state.config.host_baseline_version,
      source_bound: state.config.source_bound,
      linkage: state.linkage,
      cohort: "clock_eligible_run_in_candidate",
      data_classification: "RUN_IN_INELIGIBLE_UNTIL_GATES_PASS",
      probe_policy: state.config.probe_policy,
      probe_randomization_state: structuredClone(state.probeState),
      history_presentation: state.config.history_presentation,
      neutral_probe: state.config.neutral_probe,
      memory_factorial: state.config.memory_factorial,
      governance_snapshot: state.config.governance,
      collection_snapshot: state.config.collection,
      eligibility_clock: state.eligibility,
      visibility_gated_history_causality: true,
      engineering_fidelity_status: "ENGINEERING_FIDELITY_CERTIFIED",
      browser_timing_status: "BROWSER_TIMING_PENDING",
      live_receipt_status: "NOT_DONE",
      human_causal_claim: "NO_HUMAN_CAUSAL_CLAIM",
      annotation_protocol: "two_pass_blinded_then_context_v1",
      decorated_at: new Date().toISOString()
    };
    return out;
  }
  return { decorate };
});
