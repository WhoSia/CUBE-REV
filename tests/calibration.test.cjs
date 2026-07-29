"use strict";

const assert = require("node:assert/strict");
const config = require("../calibration/calibration-config.js");
const linkage = require("../calibration/linkage.js");
const probe = require("../calibration/probe-policy.js");
const clock = require("../calibration/eligibility-clock.js");
const exportDecoration = require("../calibration/export-decoration.js");

global.CUBE_REV_CALIBRATION_CONFIG = config;
global.CubeRevCalibrationLinkage = linkage;
global.CubeRevProbePolicy = probe;
global.CubeRevEligibilityClock = clock;
global.CubeRevExportDecoration = exportDecoration;
const { CubeRevCalibrationRuntime } = require("../calibration/runtime.js");

assert.equal(config.protocol_version, "0.7.11");
assert.equal(config.host_baseline_version, "0.6.11");
assert.equal(config.collection.enabled, false);
assert.equal(config.collection.prospective_human_data_allowed, false);
assert.equal(config.eligibility_clock.activation_enabled, false);
assert.equal(config.governance.approved, false);

const serverToken = {
  participant_token: "CRP-ABCDEF123456",
  server_issued: true,
  issued_at: "2026-07-30T00:00:00.000Z"
};
assert.equal(linkage.validateServerToken(serverToken), true);
assert.equal(linkage.validateServerToken({ ...serverToken, server_issued: false }), false);
assert.deepEqual(probe.assign("same-key"), probe.assign("same-key"));
assert.equal(probe.assign("same-key").decoder_state_used, false);
assert.deepEqual(
  new Set(Array.from({ length: 120 }, (_, i) => probe.assign(`key-${i}`).arm)),
  new Set(probe.ARMS)
);

const blocked = clock.evaluate(config);
assert.equal(blocked.state, "NOT_STARTED");
assert.equal(blocked.eligible, false);
assert.ok(blocked.blocking_reasons.includes("governance_approved"));
assert.throws(() => clock.activate(), /governance-controlled/);

const storage = {
  value: null,
  getItem() { return this.value; },
  setItem(_, value) { this.value = value; }
};
const runtime = new CubeRevCalibrationRuntime({ storage });
const cells = new Set(Array.from({ length: 256 }, (_, i) => runtime.factorialCell(`cell-${i}`).cell_id));
assert.equal(cells.size, 8);
assert.equal(runtime.collectionAllowed(), false);
assert.equal(runtime.eligibility.state, "NOT_STARTED");
assert.equal(runtime.linkage.server_issued, false);

const baseTrial = {
  trial_id: "H-RB-005",
  condition: "state_only_path_ambiguity",
  scramble: "R2 U' F'",
  hidden_generation_candidates: [
    { label: "geodesic", scramble: "R2 U' F'", length: 3, redundancy: 0 },
    { label: "uniform_reduced_bridge", scramble: "F2 R2 U F2 R2 F", length: 6, redundancy: 3 }
  ]
};
const resolved = runtime.resolveTrial(structuredClone(baseTrial), "participant-a");
assert.ok(["geodesic", "uniform_reduced_bridge"].includes(resolved.assigned_history_label));
assert.equal(resolved.calibration_assignment.probe.adaptive, false);
const record = {};
runtime.decorateTrial(record, resolved);
assert.equal(record.replay_inference_allowed, record.scramble_text_shown);

const session = { project: "CUBE-REV", version: "0.6.11", trials: [record] };
runtime.decorateSession(session);
const exported = runtime.decorateExport(session);
assert.equal(exported.calibration_0711.protocol_version, "0.7.11");
assert.equal(exported.calibration_0711.eligibility_clock.state, "NOT_STARTED");
assert.equal(exported.calibration_0711.visibility_gated_history_causality, true);
assert.equal(exported.calibration_0711.data_classification, "RUN_IN_INELIGIBLE_UNTIL_GATES_PASS");

console.log("CUBE-REV 0.7.11 calibration unit tests passed.");
