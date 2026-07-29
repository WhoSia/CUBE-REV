(function (root, factory) {
  const api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  root.CubeRevProbePolicy = api;
})(typeof globalThis !== "undefined" ? globalThis : this, function () {
  "use strict";

  const ARMS = Object.freeze(["no_probe", "sham_probe", "diagnostic_probe"]);
  function fnv1a32(text) {
    let hash = 0x811c9dc5;
    for (const ch of String(text)) {
      hash ^= ch.charCodeAt(0);
      hash = Math.imul(hash, 0x01000193) >>> 0;
    }
    return hash >>> 0;
  }
  function assign(key) {
    const arm = ARMS[fnv1a32(key) % ARMS.length];
    return Object.freeze({
      policy_id: "fixed-balanced-hash-v1",
      adaptive: false,
      arm,
      assignment_key_hash_fnv1a32: fnv1a32(key).toString(16).padStart(8, "0"),
      assignment_probabilities: Object.freeze({
        no_probe: 1 / 3,
        sham_probe: 1 / 3,
        diagnostic_probe: 1 / 3
      }),
      decoder_state_used: false
    });
  }
  return { ARMS, fnv1a32, assign };
});
