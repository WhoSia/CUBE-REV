"use strict";

const assert = require("node:assert/strict");
const config = require("../calibration/calibration-config.js");
const linkage = require("../calibration/linkage.js");
const clock = require("../calibration/eligibility-clock.js");
const exportDecoration = require("../calibration/export-decoration.js");
const randomization = require("../calibration/randomization.js");
const history = require("../calibration/history-presentation.js");
const neutral = require("../calibration/neutral-probe.js");

global.CUBE_REV_CALIBRATION_CONFIG = config;
global.CubeRevCalibrationLinkage = linkage;
global.CubeRevEligibilityClock = clock;
global.CubeRevExportDecoration = exportDecoration;
global.CubeRevDecisionRandomization = randomization;
global.CubeRevHistoryPresentation = history;
global.CubeRevNeutralProbe = neutral;
const { CubeRevCalibrationRuntime } = require("../calibration/runtime.js");

assert.equal(config.protocol_version, "0.7.12");
assert.equal(config.host_baseline_version, "0.7.12");
assert.equal(config.preserved_baseline_version, "0.6.11");
assert.equal(config.collection.enabled, true);
assert.deepEqual(config.history_presentation.modalities, ["TERMINAL_ONLY"]);
assert.equal(config.history_presentation.generation_motion_visible, false);
assert.equal(config.memory_factorial.design, "1x2x1");
assert.equal(config.eligibility_clock.activation_enabled, false);
assert.equal(clock.evaluate(config).state, "NOT_STARTED");
assert.throws(() => clock.activate(), /governance-controlled/);

const storage = {
  value: null,
  getItem() { return this.value; },
  setItem(_, value) { this.value = value; }
};
const runtime = new CubeRevCalibrationRuntime({ storage });
const modalities = new Set(Array.from({length:512},(_,i)=>runtime.factorialCell(`cell-${i}`).history_modality));
assert.deepEqual(modalities, new Set(history.MODALITIES));
assert.equal(runtime.collectionAllowed(), true);
assert.equal(runtime.eligibility.state, "NOT_STARTED");

const trial = runtime.resolveTrial({
  trial_id: "H-RB-005",
  scramble: "R2 U' F'",
  scramble_tokens: ["R2","U'","F'"],
  hidden_generation_candidates: [
    { label:"geodesic", scramble:"R2 U' F'", length:3, redundancy:0 },
    { label:"uniform_reduced_bridge", scramble:"F2 R2 U F2 R2 F", length:6, redundancy:3 }
  ]
}, "participant-a");
const record = { ordinal: 1 };
runtime.decorateTrial(record, trial);
assert.equal(trial.presentation_mode, "TERMINAL_ONLY");
assert.equal(trial.show_scramble_text, false);
assert.equal(record.generating_path_hidden, true);
assert.equal(record.scramble_text_shown, false);
assert.equal(record.scramble_animation_shown, false);
assert.equal(record.replay_inference_allowed, false);
const assignment = runtime.decideProbe(record, 1, { getRandomValues(buffer) { buffer[0] = 6; } });
assert.equal(assignment.arm, "TIME_MATCHED_NEUTRAL");
assert.equal(record.probe_after, true);

const session = { project:"CUBE-REV", version:"0.7.12", trials:[record] };
runtime.decorateSession(session);
const exported = runtime.decorateExport(session);
assert.equal(exported.calibration_0712.protocol_version, "0.7.12");
assert.equal(exported.calibration_0712.eligibility_clock.state, "NOT_STARTED");
assert.equal(exported.calibration_0712.history_visibility_status, "TERMINAL_STATE_ONLY");
assert.equal(exported.calibration_0712.browser_timing_status, "NOT_APPLICABLE_NO_GENERATION_MOTION");
assert.equal(exported.calibration_0712.data_classification, "RUN_IN_INELIGIBLE_UNTIL_GATES_PASS");

console.log("CUBE-REV 0.7.12 calibration runtime tests passed.");
