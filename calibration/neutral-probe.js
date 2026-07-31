(function (root, factory) {
  const api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  root.CubeRevNeutralProbe = api;
})(typeof globalThis !== "undefined" ? globalThis : this, function () {
  "use strict";

  const MINIMUM_EXPOSURE_MS = 700;
  const FORBIDDEN_CONTENT = Object.freeze([
    "strategy",
    "comfort",
    "discomfort",
    "success",
    "failure",
    "difficulty",
    "confidence"
  ]);

  function configureDom(document, options = {}) {
    const now = options.now || (() => performance.now());
    const title = document.querySelector("#probeScreen h2");
    const description = document.querySelector("#probeScreen p");
    const labels = Array.from(document.querySelectorAll("#probeChoices label"));
    const confidence = document.getElementById("probeConfidence")?.closest(".field");
    const submit = document.getElementById("probeSubmit");
    const startedAt = now();
    if (title) title.textContent = "●";
    if (description) description.textContent = "표시를 확인한 뒤 계속하세요.";
    labels.forEach((label, index) => {
      label.classList.toggle("hidden", index !== 0);
      const input = label.querySelector("input");
      const text = label.querySelector("span");
      if (index === 0) {
        if (input) input.value = "neutral_acknowledged";
        if (text) text.textContent = "확인";
      }
    });
    confidence?.classList.add("hidden");
    if (submit) {
      submit.disabled = true;
      const remaining = Math.max(0, MINIMUM_EXPOSURE_MS - (now() - startedAt));
      setTimeout(() => { submit.disabled = false; }, remaining);
    }
    return {
      probe_type: "lower_content_interruption_control",
      minimum_exposure_ms: MINIMUM_EXPOSURE_MS,
      started_at_perf_ms: startedAt,
      forbidden_content: FORBIDDEN_CONTENT
    };
  }

  function restoreDom(document) {
    document.getElementById("probeConfidence")?.closest(".field")?.classList.remove("hidden");
    const submit = document.getElementById("probeSubmit");
    if (submit) submit.disabled = false;
  }

  return {
    MINIMUM_EXPOSURE_MS,
    FORBIDDEN_CONTENT,
    configureDom,
    restoreDom
  };
});
