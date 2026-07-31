(function (root, factory) {
  const api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  root.CubeRevDecisionRandomization = api;
})(typeof globalThis !== "undefined" ? globalThis : this, function () {
  "use strict";

  const POLICY_ID = "crypto_exact_bucket_60_20_20_decision_point_v1";
  const UINT32_RANGE = 0x100000000;
  const BUCKET_COUNT = 10;
  const ACCEPT_LIMIT = UINT32_RANGE - (UINT32_RANGE % BUCKET_COUNT);
  const PROBABILITY_VECTOR = Object.freeze({
    NO_PROBE: 0.60,
    TIME_MATCHED_NEUTRAL: 0.20,
    STRATEGY_DIAGNOSTIC: 0.20
  });

  function initialState() {
    return { burden_count: 0, last_probe_trial: null };
  }

  function availability(context = {}) {
    const trialOrdinal = Number(context.trial_ordinal);
    const completedTrials = Number(context.completed_trials);
    const state = context.state || initialState();
    if (!Number.isInteger(trialOrdinal) || trialOrdinal < 1) {
      return { available: false, reason: "invalid_trial_ordinal" };
    }
    if (!Number.isInteger(completedTrials) || completedTrials < 1) {
      return { available: false, reason: "minimum_completed_trials" };
    }
    if ((Number(state.burden_count) || 0) >= 3) {
      return { available: false, reason: "burden_cap_reached" };
    }
    if (Number.isInteger(state.last_probe_trial) &&
        trialOrdinal - state.last_probe_trial <= 2) {
      return { available: false, reason: "cooldown_two_trials" };
    }
    return { available: true, reason: "eligible_decision_point" };
  }

  function cryptoSource(source) {
    const candidate = source || globalThis.crypto;
    return candidate && typeof candidate.getRandomValues === "function"
      ? candidate
      : null;
  }

  function drawExactBucket(source) {
    const crypto = cryptoSource(source);
    if (!crypto) {
      const error = new Error("Web Crypto getRandomValues is required.");
      error.code = "CRYPTO_UNAVAILABLE";
      throw error;
    }
    const rejected = [];
    const buffer = new Uint32Array(1);
    for (;;) {
      crypto.getRandomValues(buffer);
      const value = Number(buffer[0]);
      if (value < ACCEPT_LIMIT) {
        return {
          accepted_uint32: value,
          rejected_uint32: rejected,
          rejection_count: rejected.length,
          bucket: value % BUCKET_COUNT
        };
      }
      rejected.push(value);
    }
  }

  function armForBucket(bucket) {
    if (bucket <= 5) return "NO_PROBE";
    if (bucket <= 7) return "TIME_MATCHED_NEUTRAL";
    return "STRATEGY_DIAGNOSTIC";
  }

  function decide(context = {}, source) {
    const state = {
      burden_count: Number(context.state?.burden_count) || 0,
      last_probe_trial: Number.isInteger(context.state?.last_probe_trial)
        ? context.state.last_probe_trial
        : null
    };
    const gate = availability({ ...context, state });
    const base = {
      policy_id: POLICY_ID,
      trial_ordinal: context.trial_ordinal,
      decision_point_available: gate.available,
      availability_reason: gate.reason,
      probability_vector: PROBABILITY_VECTOR,
      burden_count_before: state.burden_count,
      last_probe_trial: state.last_probe_trial
    };
    if (!gate.available) {
      return {
        assignment: {
          ...base,
          arm: "NOT_AVAILABLE",
          assignment_probability: null,
          accepted_uint32: null,
          rejected_uint32: [],
          bucket: null,
          rejection_count: 0
        },
        state
      };
    }
    let draw;
    try {
      draw = drawExactBucket(source);
    } catch (error) {
      return {
        assignment: {
          ...base,
          arm: "RANDOMIZATION_FAILED_CLOSED",
          assignment_probability: null,
          accepted_uint32: null,
          rejected_uint32: [],
          bucket: null,
          rejection_count: 0,
          failure_code: error.code || "CRYPTO_FAILURE"
        },
        state,
        causal_run_in_eligible: false
      };
    }
    const arm = armForBucket(draw.bucket);
    const probed = arm !== "NO_PROBE";
    return {
      assignment: {
        ...base,
        arm,
        assignment_probability: PROBABILITY_VECTOR[arm],
        ...draw
      },
      state: {
        burden_count: state.burden_count + (probed ? 1 : 0),
        last_probe_trial: probed ? context.trial_ordinal : state.last_probe_trial
      },
      causal_run_in_eligible: true
    };
  }

  return {
    POLICY_ID,
    PROBABILITY_VECTOR,
    ACCEPT_LIMIT,
    initialState,
    availability,
    drawExactBucket,
    armForBucket,
    decide
  };
});
