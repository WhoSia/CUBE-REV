"use strict";

const assert = require("node:assert/strict");
const neutral = require("../calibration/neutral-probe.js");

const classList = () => {
  const values = new Set();
  return {
    add: value => values.add(value),
    remove: value => values.delete(value),
    toggle: (value, force) => force ? values.add(value) : values.delete(value),
    contains: value => values.has(value)
  };
};
const labels = Array.from({length:5}, () => ({
  classList: classList(),
  input: { value: "" },
  text: { textContent: "" },
  querySelector(selector) { return selector === "input" ? this.input : this.text; }
}));
const title = { textContent: "" }, description = { textContent: "" };
const confidenceField = { classList: classList() };
const confidence = { closest: () => confidenceField };
const choices = { classList: classList(), setAttribute() {}, removeAttribute() {} };
const submit = { disabled: false };
const document = {
  querySelector(selector) {
    if (selector === "#probeScreen h2") return title;
    if (selector === "#probeScreen p") return description;
    return null;
  },
  querySelectorAll: () => labels,
  getElementById(id) {
    if (id === "probeChoices") return choices;
    if (id === "probeConfidence") return confidence;
    if (id === "probeSubmit") return submit;
    return null;
  }
};
const originalSetTimeout = global.setTimeout;
let scheduledDelay = null;
global.setTimeout = (callback, delay) => { scheduledDelay = delay; return 1; };
try {
  const record = neutral.configureDom(document, { now: () => 100 });
  assert.equal(record.minimum_exposure_ms, 700);
  assert.equal(title.textContent, "●");
  assert.equal(choices.classList.contains("hidden"), true);
  assert.equal(labels.every(label => label.classList.contains("hidden")), true);
  assert.equal(confidenceField.classList.contains("hidden"), true);
  assert.equal(submit.disabled, true);
  assert.equal(scheduledDelay, 700);
  const visibleText = `${title.textContent} ${description.textContent} ${labels[0].text.textContent}`.toLowerCase();
  for (const forbidden of neutral.FORBIDDEN_CONTENT) assert.equal(visibleText.includes(forbidden), false);
  neutral.restoreDom(document);
  assert.equal(choices.classList.contains("hidden"), false);
  assert.equal(labels.every(label => !label.classList.contains("hidden")), true);
  assert.equal(confidenceField.classList.contains("hidden"), false);
  assert.equal(submit.disabled, false);
} finally {
  global.setTimeout = originalSetTimeout;
}

console.log("CUBE-REV 0.7.12 neutral probe tests passed.");
