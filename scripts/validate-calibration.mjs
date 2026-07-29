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
  hash(baseline.replace(/\r\n/g, "\n")),
  "ced1836b372e407b328d0863b0bc968cd7d89359d5edfa91da9313989444bb31",
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
