(function (root, factory) {
  const api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  root.CubeRevCalibrationLinkage = api;
})(typeof globalThis !== "undefined" ? globalThis : this, function () {
  "use strict";

  const KEY = "CUBE_REV_INSTALLATION_ID_V1";
  const LEGACY_KEYS = Object.freeze(["CUBE_REV_0711_INSTALLATION_ID"]);
  const hex = (bytes) => Array.from(bytes, (x) => x.toString(16).padStart(2, "0")).join("");
  function randomId() {
    const bytes = new Uint8Array(16);
    if (globalThis.crypto?.getRandomValues) globalThis.crypto.getRandomValues(bytes);
    else for (let i = 0; i < bytes.length; i++) bytes[i] = Math.floor(Math.random() * 256);
    return `CRI-${hex(bytes)}`;
  }
  function getInstallationId(storage) {
    let id = null;
    try {
      id = storage?.getItem(KEY) || null;
      if (!id) {
        for (const legacyKey of LEGACY_KEYS) {
          id = storage?.getItem(legacyKey) || null;
          if (id) break;
        }
      }
    } catch (_) {}
    if (!/^CRI-[0-9a-f]{32}$/.test(String(id || ""))) {
      id = randomId();
      try { storage?.setItem(KEY, id); } catch (_) {}
    } else {
      try { storage?.setItem(KEY, id); } catch (_) {}
    }
    return id;
  }
  function createRunInToken(installationId) {
    const suffix = String(installationId).replace(/^CRI-/, "").slice(0, 12);
    return Object.freeze({
      participant_token: `RUNIN-${suffix}`,
      token_source: "local_run_in",
      server_issued: false,
      eligible_for_prospective_clock: false
    });
  }
  function validateServerToken(value) {
    return !!value &&
      value.server_issued === true &&
      /^CRP-[A-Z0-9_-]{12,80}$/.test(String(value.participant_token || "")) &&
      typeof value.issued_at === "string";
  }
  return { getInstallationId, createRunInToken, validateServerToken };
});
