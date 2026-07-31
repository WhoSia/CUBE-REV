(function (root, factory) {
  const api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  root.CubeRevHistoryPresentation = api;
})(typeof globalThis !== "undefined" ? globalThis : this, function () {
  "use strict";

  const MODALITIES = Object.freeze([
    "TERMINAL_ONLY",
    "TEXT_HISTORY",
    "ANIMATED_HISTORY"
  ]);
  const EXPOSURE_MS = 2400;
  const MIN_ANIMATED_MOVE_MS = 55;

  function plan(modality, tokens, options = {}) {
    if (!MODALITIES.includes(modality)) {
      throw new Error(`Unknown history modality: ${modality}`);
    }
    const sequence = Array.from(tokens || []);
    const exposureMs = Number(options.exposure_ms) || EXPOSURE_MS;
    const minimumMoveMs = Number(options.minimum_move_ms) || MIN_ANIMATED_MOVE_MS;
    const moveDurationMs = modality === "ANIMATED_HISTORY"
      ? exposureMs / Math.max(1, sequence.length)
      : null;
    if (modality === "ANIMATED_HISTORY" && sequence.length &&
        moveDurationMs < minimumMoveMs) {
      const error = new Error("ANIMATION_BUDGET_INFEASIBLE");
      error.code = "ANIMATION_BUDGET_INFEASIBLE";
      error.move_count = sequence.length;
      error.move_duration_ms = moveDurationMs;
      throw error;
    }
    return Object.freeze({
      modality,
      tokens: Object.freeze(sequence),
      exposure_ms: exposureMs,
      move_duration_ms: moveDurationMs,
      minimum_move_ms: minimumMoveMs,
      replay_inference_allowed: modality !== "TERMINAL_ONLY"
    });
  }

  async function present(presentation, helpers) {
    const started = helpers.now?.() ?? 0;
    helpers.setCubeVisible?.(presentation.modality === "ANIMATED_HISTORY");
    if (presentation.modality === "TERMINAL_ONLY") {
      helpers.setText?.("●");
      await helpers.sleep(presentation.exposure_ms);
    } else if (presentation.modality === "TEXT_HISTORY") {
      helpers.setText?.(presentation.tokens.join(" "));
      await helpers.sleep(presentation.exposure_ms);
    } else {
      helpers.setText?.(helpers.privateLabel?.() || "");
      for (let index = 0; index < presentation.tokens.length; index++) {
        const token = presentation.tokens[index];
        helpers.log?.("history_animation_move_started", {
          display_index: index + 1,
          move: token,
          nominal_duration_ms: presentation.move_duration_ms
        });
        helpers.animateMove(token, presentation.move_duration_ms);
        await helpers.waitVisualIdle();
        helpers.log?.("history_animation_move_settled", {
          display_index: index + 1,
          move: token
        });
      }
      const spent = (helpers.now?.() ?? started) - started;
      if (spent < presentation.exposure_ms) {
        await helpers.sleep(presentation.exposure_ms - spent);
      }
    }
    helpers.setText?.(helpers.privateLabel?.() || "");
    helpers.setCubeVisible?.(true);
    return {
      modality: presentation.modality,
      nominal_exposure_ms: presentation.exposure_ms,
      nominal_move_duration_ms: presentation.move_duration_ms,
      move_count: presentation.tokens.length,
      replay_inference_allowed: presentation.replay_inference_allowed
    };
  }

  return {
    MODALITIES,
    EXPOSURE_MS,
    MIN_ANIMATED_MOVE_MS,
    plan,
    present
  };
});
