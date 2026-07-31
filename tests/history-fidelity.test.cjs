"use strict";

const assert = require("node:assert/strict");
const history = require("../calibration/history-presentation.js");

const BASE_MOVES = {
  U:{cp:[3,0,1,2,4,5,6,7],co:[0,0,0,0,0,0,0,0]},
  R:{cp:[4,1,2,0,7,5,6,3],co:[2,0,0,1,1,0,0,2]},
  F:{cp:[1,5,2,3,0,4,6,7],co:[1,2,0,0,2,1,0,0]},
  D:{cp:[0,1,2,3,5,6,7,4],co:[0,0,0,0,0,0,0,0]},
  L:{cp:[0,2,6,3,4,1,5,7],co:[0,1,2,0,0,2,1,0]},
  B:{cp:[0,1,3,7,4,5,2,6],co:[0,0,1,2,0,0,2,1]}
};
const solved = () => ({ cp:[0,1,2,3,4,5,6,7], co:[0,0,0,0,0,0,0,0] });
function quarter(state, face) {
  const move = BASE_MOVES[face], out = solved();
  for (let i = 0; i < 8; i++) {
    out.cp[i] = state.cp[move.cp[i]];
    out.co[i] = (state.co[move.cp[i]] + move.co[i]) % 3;
  }
  return out;
}
function apply(state, token) {
  const face = token[0], exp = token.endsWith("2") ? 2 : token.endsWith("'") ? 3 : 1;
  let out = state;
  for (let i = 0; i < exp; i++) out = quarter(out, face);
  return out;
}
const applyAlg = (state, tokens) => tokens.reduce(apply, state);

const faces = ["U","R","F","D","L","B"];
const tokens = faces.flatMap(face => [face, `${face}'`, `${face}2`]);
const corpus = tokens.map(token => [token]);
corpus.push(
  ["R","R","R","R"],
  ["U","R","F","D","L","B"],
  ["F","F'","U2","U2"],
  ["R2","U","R2","U'","R2"],
  Array.from({length:24},(_,i)=>tokens[i%tokens.length])
);
let seed = 0x0712f1de;
for (let trace = 0; trace < 10000; trace++) {
  seed = (Math.imul(seed, 1664525) + 1013904223) >>> 0;
  const length = 1 + (seed % 24), row = [];
  let previousFace = "";
  for (let i = 0; i < length; i++) {
    seed = (Math.imul(seed, 1664525) + 1013904223) >>> 0;
    let token = tokens[seed % tokens.length];
    if (token[0] === previousFace) token = tokens[(seed + 3) % tokens.length];
    row.push(token); previousFace = token[0];
  }
  corpus.push(row);
}
assert.equal(corpus.length, 10023);
for (const trace of corpus) {
  const batch = applyAlg(solved(), trace);
  let animated = solved();
  const presentation = history.plan("ANIMATED_HISTORY", trace);
  for (const token of presentation.tokens) animated = apply(animated, token);
  assert.deepEqual(animated, batch);
  assert.equal(presentation.move_duration_ms * trace.length, 2400);
}
assert.equal(history.plan("TERMINAL_ONLY", ["R"]).replay_inference_allowed, false);
assert.equal(history.plan("TEXT_HISTORY", ["R"]).replay_inference_allowed, true);
assert.throws(
  () => history.plan("ANIMATED_HISTORY", Array.from({length:44},()=> "R")),
  error => error.code === "ANIMATION_BUDGET_INFEASIBLE"
);

console.log("CUBE-REV 0.7.12 history fidelity passed: 10023 / 10023 traces.");
