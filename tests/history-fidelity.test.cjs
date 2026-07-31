"use strict";

const assert = require("node:assert/strict");
const history = require("../calibration/history-presentation.js");

const faces = ["U", "R", "F", "D", "L", "B"];
const tokens = faces.flatMap(face => [face, `${face}'`, `${face}2`]);
const corpus = tokens.map(token => [token]);
corpus.push(
  ["R", "R", "R", "R"],
  ["U", "R", "F", "D", "L", "B"],
  ["F", "F'", "U2", "U2"],
  ["R2", "U", "R2", "U'", "R2"],
  Array.from({ length: 24 }, (_, i) => tokens[i % tokens.length])
);

let seed = 0x0712f1de;
for (let trace = 0; trace < 10000; trace++) {
  seed = (Math.imul(seed, 1664525) + 1013904223) >>> 0;
  const length = 1 + (seed % 24);
  const row = [];
  let previousFace = "";
  for (let i = 0; i < length; i++) {
    seed = (Math.imul(seed, 1664525) + 1013904223) >>> 0;
    let token = tokens[seed % tokens.length];
    if (token[0] === previousFace) token = tokens[(seed + 3) % tokens.length];
    row.push(token);
    previousFace = token[0];
  }
  corpus.push(row);
}

assert.equal(corpus.length, 10023);
assert.deepEqual(history.MODALITIES, ["TERMINAL_ONLY"]);
for (const trace of corpus) {
  const presentation = history.plan("TERMINAL_ONLY", trace);
  assert.equal(presentation.modality, "TERMINAL_ONLY");
  assert.equal(presentation.move_duration_ms, null);
  assert.equal(presentation.generation_motion_visible, false);
  assert.equal(presentation.path_text_visible, false);
  assert.equal(presentation.replay_inference_allowed, false);
}
assert.throws(() => history.plan("TEXT_HISTORY", ["R"]), /disabled/);
assert.throws(() => history.plan("ANIMATED_HISTORY", ["R"]), /disabled/);

(async () => {
  const visible = [];
  const text = [];
  const events = [];
  let animationCalls = 0;
  const result = await history.present(
    history.plan("TERMINAL_ONLY", ["R", "U", "F"]),
    {
      setCubeVisible: value => visible.push(value),
      setText: value => text.push(value),
      privateLabel: () => "Hidden",
      log: (type, payload) => events.push({ type, payload }),
      sleep: async milliseconds => assert.equal(milliseconds, 2400),
      animateMove: () => { animationCalls++; }
    }
  );
  assert.deepEqual(visible, [false, true]);
  assert.deepEqual(text, ["Hidden", "Hidden"]);
  assert.equal(animationCalls, 0);
  assert.equal(result.displayed_move_count, 0);
  assert.equal(result.hidden_generation_move_count, 3);
  assert.equal(result.generation_motion_visible, false);
  assert.equal(events[0].type, "hidden_generation_visibility_enforced");
  console.log("CUBE-REV 0.7.12 hidden-history visibility passed: 10023 / 10023 traces.");
})().catch(error => {
  console.error(error);
  process.exitCode = 1;
});
