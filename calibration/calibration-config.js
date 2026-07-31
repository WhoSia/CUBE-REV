(function (root, factory) {
  const value = factory();
  if (typeof module === "object" && module.exports) module.exports = value;
  root.CUBE_REV_CALIBRATION_CONFIG = value;
})(typeof globalThis !== "undefined" ? globalThis : this, function () {
  "use strict";

  return Object.freeze({
    protocol_version: "0.7.12",
    host_baseline_version: "0.7.12",
    preserved_baseline_version: "0.6.11",
    build_id: "0.7.12-camera-neutral-bypass-hotfix-1",
    mode: "run_in_only",
    source_bound: Object.freeze({
      repository: "WhoSia/CUBE-REV",
      baseline_commit: "f0779a583c2a9919d0171b0ca819718c0e3b6ac5",
      preserved_0611_sha256: "ced1836b372e407b328d0863b0bc968cd7d89359d5edfa91da9313989444bb31",
      generated_from: "index.html"
    }),
    governance: Object.freeze({
      approved: true,
      approval_id: "user-authorized-collector-unlock-2026-07-31",
      approved_at: "2026-07-31T00:00:00+09:00"
    }),
    collection: Object.freeze({
      enabled: true,
      prospective_human_data_allowed: true,
      collector_contract: "receipt-v2",
      production_receipt_required: true
    }),
    eligibility_clock: Object.freeze({
      activation_enabled: false,
      authorization_id: null,
      activated_at: null
    }),
    probe_policy: Object.freeze({
      policy_id: "crypto_exact_bucket_60_20_20_decision_point_v1",
      adaptive: false,
      minimum_completed_trials: 1,
      cooldown_trials: 2,
      burden_cap: 3,
      arms: Object.freeze(["NO_PROBE", "TIME_MATCHED_NEUTRAL", "STRATEGY_DIAGNOSTIC"]),
      assignment_probabilities: Object.freeze({
        NO_PROBE: 0.60,
        TIME_MATCHED_NEUTRAL: 0.20,
        STRATEGY_DIAGNOSTIC: 0.20
      })
    }),
    history_presentation: Object.freeze({
      modalities: Object.freeze(["TERMINAL_ONLY"]),
      nominal_exposure_ms: 2400,
      generation_motion_visible: false,
      path_text_visible: false,
      browser_wall_clock_certified: false
    }),
    neutral_probe: Object.freeze({
      minimum_exposure_ms: 700,
      classification: "nonvisual_timing_control",
      presentation_visibility: "hidden",
      user_interaction_required: false,
      human_reactivity_estimated: false
    }),
    memory_factorial: Object.freeze({
      design: "1x2x1",
      factors: Object.freeze({
        history_visibility: Object.freeze(["hidden"]),
        history_type: Object.freeze(["geodesic", "redundant_equivalent"]),
        view_context: Object.freeze(["stable"])
      })
    })
  });
});
