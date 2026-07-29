import assert from "node:assert/strict";
import crypto from "node:crypto";
import { readFile } from "node:fs/promises";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const read = (name) => readFile(resolve(root, name), "utf8");
const hash = (text) => crypto.createHash("sha256").update(text).digest("hex");
const baseline = await read("index.html");
const archive = await read("CUBE-REV_0.6.11_GitHub_Pages_Pilot.html");
const host = await read("calibration/index.html");

assert.equal(baseline, archive, "0.6.11 baseline files changed or diverged");
assert.equal(
  hash(baseline),
  "19b946c1ded8e16eee34187602c921b007040c378c44c71c3f3e959e0d1a1469",
  "0.6.11 baseline is not the verified source"
);
assert.match(host, /CUBE-REV 0\.7\.11 Calibration/);
assert.match(host, /const VERSION = '0\.6\.11'/);
assert.match(host, /const CALIBRATION_PROTOCOL_VERSION = '0\.7\.11'/);
assert.match(host, /const BUILD_ID = '0\.7\.11-source-bound-calibration-1'/);
assert.match(host, /enabled: false/);
assert.match(host, /endpoint: ''/);
assert.match(host, /autoSubmitOnComplete: false/);
assert.doesNotMatch(host, /script\.google\.com/);
assert.doesNotMatch(host, /studyToken/);
assert.match(host, /calibrationRuntime\.decorateExport/);
assert.match(host, /calibrationRuntime\.presentAssignedHistory/);
assert.match(host, /calibrationRuntime\.prepareProbe/);
assert.match(host, /collector governance lock/);
assert.match(host, /eligibility clock not started/);

console.log("CUBE-REV 0.7.11 source-bound host validation passed.");
