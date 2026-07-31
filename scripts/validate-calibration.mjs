import assert from "node:assert/strict";
import crypto from "node:crypto";
import { readFile } from "node:fs/promises";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const read = name => readFile(resolve(root, name), "utf8");
const hash = text => crypto.createHash("sha256").update(text.replace(/\r\n/g, "\n")).digest("hex");
const index = await read("index.html");
const archive = await read("CUBE-REV_0.7.12_GitHub_Pages_Pilot.html");
const baseline = await read("CUBE-REV_0.6.11_GitHub_Pages_Pilot.html");
const host = await read("calibration/index.html");
const expectedHost = index.replace(/\r\n/g, "\n")
  .replaceAll('src="./calibration/', 'src="./')
  .replaceAll('src="./js/', 'src="../js/');

assert.equal(index, archive, "0.7.12 public host and archive diverged");
assert.equal(
  hash(baseline),
  "ced1836b372e407b328d0863b0bc968cd7d89359d5edfa91da9313989444bb31",
  "preserved 0.6.11 baseline changed"
);
assert.equal(host, expectedHost, "source-bound calibration host was not built from index.html");
assert.match(host, /CUBE-REV 0\.7\.12/);
assert.match(host, /const VERSION = '0\.7\.12'/);
assert.match(host, /const BUILD_ID = '0\.7\.12-terminal-state-hotfix-1'/);
assert.match(host, /enabled: false/);
assert.match(host, /endpoint: ''/);
assert.match(host, /autoSubmitOnComplete: false/);
assert.doesNotMatch(host, /script\.google\.com|studyToken/);
assert.match(host, /calibrationRuntime\.decorateExport/);
assert.match(host, /calibrationRuntime\.presentAssignedHistory/);
assert.match(host, /calibrationRuntime\.decideProbe/);
assert.match(host, /screen_relative_matrix_360_orbit_v1/);
assert.match(host, /COLLECTION LOCKED/);
assert.match(host, /NOT_STARTED/);
assert.match(host, /modalities:\['TERMINAL_ONLY'\]/);
assert.doesNotMatch(host, /history_presentation'\)/);

console.log("CUBE-REV 0.7.12 source-bound host validation passed.");
