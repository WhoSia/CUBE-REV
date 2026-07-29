(function (root, factory) {
  const value = factory();
  if (typeof module === "object" && module.exports) module.exports = value;
  root.CUBE_REV_CALIBRATION_CONFIG = value;
})(typeof globalThis !== "undefined" ? globalThis : this, function () {
  "use strict";

  return Object.freeze({
    protocol_version: "0.7.11",
    host_baseline_version: "0.6.11",
    build_id: "0.7.11-source-bound-calibration-1",
    mode: "run_in_only",
    source_bound: Object.freeze({
      repository: "WhoSia/CUBE-REV",
      baseline_commit: "58619a909a9343ff0f50e945ee2d2cf443c585d7",
      baseline_sha256: "ced1836b372e407b328d0863b0bc968cd7d89359d5edfa91da9313989444bb31",
      generated_from: "index.html"
    }),
    governance: Object.freeze({
      approved: false,
      approval_id: null,
      approved_at: null
    }),
    collection: Object.freeze({
      enabled: false,
      prospective_human_data_allowed: false,
      collector_contract: "receipt-v2",
      production_receipt_required: true
    }),
    eligibility_clock: Object.freeze({
      activation_enabled: false,
      authorization_id: null,
      activated_at: null
    }),
    probe_policy: Object.freeze({
      policy_id: "fixed-balanced-hash-v1",
      adaptive: false,
      arms: Object.freeze(["no_probe", "sham_probe", "diagnostic_probe"]),
      assignment_probabilities: Object.freeze({
        no_probe: 1 / 3,
        sham_probe: 1 / 3,
        diagnostic_probe: 1 / 3
      })
    }),
    memory_factorial: Object.freeze({
      design: "2x2x2",
      factors: Object.freeze({
        history_visibility: Object.freeze(["hidden", "shown"]),
        history_type: Object.freeze(["geodesic", "redundant_equivalent"]),
        view_context: Object.freeze(["stable", "reoriented"])
      })
    })
  });
});
