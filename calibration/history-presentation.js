(function (root, factory) {
  const api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  root.CubeRevHistoryPresentation = api;
})(typeof globalThis !== "undefined" ? globalThis : this, function () {
  "use strict";

  const MODALITIES = Object.freeze(["TERMINAL_ONLY"]);
  const EXPOSURE_MS = 2400;

  function plan(modality, tokens, options = {}) {
    if (!MODALITIES.includes(modality)) {
      throw new Error(`Visible generation history is disabled: ${modality}`);
    }
    return Object.freeze({
      modality: "TERMINAL_ONLY",
      tokens: Object.freeze(Array.from(tokens || [])),
      exposure_ms: Number(options.exposure_ms) || EXPOSURE_MS,
      move_duration_ms: null,
      replay_inference_allowed: false,
      generation_motion_visible: false,
      path_text_visible: false
    });
  }

  async function present(presentation, helpers) {
    helpers.setCubeVisible?.(false);
    helpers.setText?.(helpers.privateLabel?.() || "");
    helpers.log?.("hidden_generation_visibility_enforced", {
      generation_motion_visible: false,
      path_text_visible: false,
      displayed_move_count: 0
    });
    await helpers.sleep(presentation.exposure_ms);
    helpers.setText?.(helpers.privateLabel?.() || "");
    helpers.setCubeVisible?.(true);
    return {
      modality: "TERMINAL_ONLY",
      nominal_exposure_ms: presentation.exposure_ms,
      nominal_move_duration_ms: null,
      hidden_generation_move_count: presentation.tokens.length,
      displayed_move_count: 0,
      generation_motion_visible: false,
      path_text_visible: false,
      replay_inference_allowed: false
    };
  }

  return {
    MODALITIES,
    EXPOSURE_MS,
    plan,
    present
  };
});
