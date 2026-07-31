"use strict";

const assert = require("node:assert/strict");
const randomization = require("../calibration/randomization.js");

const rejectionSource = {
  values: [0xffffffff, 0xfffffffe, 17],
  getRandomValues(buffer) { buffer[0] = this.values.shift(); }
};
const exact = randomization.drawExactBucket(rejectionSource);
assert.deepEqual(exact.rejected_uint32, [0xffffffff, 0xfffffffe]);
assert.equal(exact.accepted_uint32, 17);
assert.equal(exact.bucket, 7);
assert.equal(randomization.armForBucket(0), "NO_PROBE");
assert.equal(randomization.armForBucket(6), "TIME_MATCHED_NEUTRAL");
assert.equal(randomization.armForBucket(9), "STRATEGY_DIAGNOSTIC");

let state = randomization.initialState();
const fixed = value => ({ getRandomValues(buffer) { buffer[0] = value; } });
let result = randomization.decide({ trial_ordinal: 1, completed_trials: 1, state }, fixed(6));
assert.equal(result.assignment.arm, "TIME_MATCHED_NEUTRAL");
state = result.state;
assert.equal(randomization.decide({ trial_ordinal: 2, completed_trials: 2, state }, fixed(8)).assignment.arm, "NOT_AVAILABLE");
assert.equal(randomization.decide({ trial_ordinal: 3, completed_trials: 3, state }, fixed(8)).assignment.arm, "NOT_AVAILABLE");
result = randomization.decide({ trial_ordinal: 4, completed_trials: 4, state }, fixed(8));
assert.equal(result.assignment.arm, "STRATEGY_DIAGNOSTIC");
const failed = randomization.decide({ trial_ordinal: 1, completed_trials: 1, state: randomization.initialState() }, {});
assert.equal(failed.assignment.arm, "RANDOMIZATION_FAILED_CLOSED");
assert.equal(failed.causal_run_in_eligible, false);

let lcgState = 0x07120001;
const syntheticSource = {
  getRandomValues(buffer) {
    lcgState = (Math.imul(lcgState, 1664525) + 1013904223) >>> 0;
    buffer[0] = lcgState;
  }
};
const counts = { NO_PROBE: 0, TIME_MATCHED_NEUTRAL: 0, STRATEGY_DIAGNOSTIC: 0 };
for (let i = 0; i < 100000; i++) {
  const assignment = randomization.decide({
    trial_ordinal: 1,
    completed_trials: 1,
    state: randomization.initialState()
  }, syntheticSource).assignment;
  counts[assignment.arm]++;
}
assert.ok(Math.abs(counts.NO_PROBE / 100000 - 0.6) < 0.006);
assert.ok(Math.abs(counts.TIME_MATCHED_NEUTRAL / 100000 - 0.2) < 0.006);
assert.ok(Math.abs(counts.STRATEGY_DIAGNOSTIC / 100000 - 0.2) < 0.006);

console.log("CUBE-REV 0.7.12 cryptographic randomization tests passed.");
