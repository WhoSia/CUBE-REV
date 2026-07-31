import assert from "node:assert/strict";
import crypto from "node:crypto";
import { readFile, access } from "node:fs/promises";
import { resolve } from "node:path";
import vm from "node:vm";

const root = resolve(import.meta.dirname, "..");
const release = Object.freeze({
  version: "0.7.12",
  buildId: "0.7.12-terminal-state-hotfix-1",
  cacheKey: "0712-terminal-state-hotfix-1",
  archiveHtml: "CUBE-REV_0.7.12_GitHub_Pages_Pilot.html",
  preservedBaselineHtml: "CUBE-REV_0.6.11_GitHub_Pages_Pilot.html",
  preservedBaselineSha256: "ced1836b372e407b328d0863b0bc968cd7d89359d5edfa91da9313989444bb31"
});
const read = path => readFile(resolve(root, path), "utf8");
const hash = text => crypto.createHash("sha256").update(text.replace(/\r\n/g, "\n")).digest("hex");

const index = await read("index.html");
const archive = await read(release.archiveHtml);
const baseline = await read(release.preservedBaselineHtml);
const config = await read("collector-config.js");
const dragController = await read("js/cube-drag-controller.js");
const cameraOrbit = await read("js/camera-orbit.js");
const historyPresentation = await read("calibration/history-presentation.js");
const calibrationConfig = await read("calibration/calibration-config.js");
const readme = await read("README.md");
const scripts = [
  "js/i18n-controller.js",
  "js/collector-client.js",
  "js/camera-orbit.js",
  "js/cube-drag-controller.js",
  "js/camera-zoom-controller.js",
  "js/responsive-layout-controller.js"
];

assert.equal(index, archive, "index.html and the versioned 0.7.12 HTML must be byte-identical");
assert.equal(hash(baseline), release.preservedBaselineSha256, "preserved 0.6.11 baseline changed");
assert.match(index, /const VERSION = '0\.7\.12'/);
assert.match(index, /const BUILD_ID = '0\.7\.12-terminal-state-hotfix-1'/);
assert.match(index, /"version":"0\.7\.12"/);
assert.doesNotMatch(index, /0\.6\.11/);
assert.match(index, /studyId: 'CUBE-REV-0\.7\.12'/);
assert.match(config, /enabled: true/);
assert.match(config, /studyId: 'CUBE-REV-0\.7\.12'/);
assert.match(config, /collectorId: 'CUBE-REV-0712-MAIN'/);
assert.match(config, /protocolVersion: 'receipt-v2'/);
assert.match(config, /script\.google\.com\/macros\/s\/[A-Za-z0-9_-]+\/exec/);
assert.doesNotMatch(config, /studyToken/);
assert.ok(readme.includes(`Current public version: ${release.version}`));
assert.ok(readme.includes(`현재 공개 버전: ${release.version}`));
assert.ok(!dragController.includes("pitchLimit"), "camera pitch must remain unrestricted");

const context = {
  console,
  performance: { now: () => 0 },
  module: undefined
};
context.window = context;
vm.runInNewContext(cameraOrbit, context);
vm.runInNewContext(dragController, context);
let cameraProbe = context.CubeRevCameraOrbit.resetCamera(1);
const controller = new context.CubeDragController({
  element: {
    dataset: {},
    style: {},
    getBoundingClientRect: () => ({ left: 0, top: 0 })
  },
  pickSticker: () => null,
  resolveStickerDrag: () => null,
  canTurnFace: () => false,
  applyFaceMove: () => false,
  getCamera: () => ({ ...cameraProbe }),
  setCamera: next => { cameraProbe = { ...cameraProbe, ...next }; },
  setPreview: () => {},
  clearPreview: () => {},
  logEvent: () => {}
});
controller.active = {
  id: 1,
  mode: "camera",
  start: { x: 0, y: 0 },
  last: { x: 0, y: 0 },
  previous: { x: 0, y: 0 },
  cameraStart: { ...cameraProbe },
  pointerType: "mouse",
  pathLength: 0,
  sampleCount: 1,
  maxDistance: 0
};
controller.onPointerMove({
  pointerId: 1,
  clientX: 0,
  clientY: 500,
  preventDefault: () => {}
});
assert.ok(cameraProbe.pitch > Math.PI, "a vertical drag must pass 180 degrees");
assert.equal(cameraProbe.orbit_model, "screen_relative_matrix_v1");
assert.equal(cameraProbe.view_matrix.length, 9);
const afterUpsideHorizontal = context.CubeRevCameraOrbit.screenRelativeOrbit(cameraProbe, 100, 0, 0.008);
const expectedScreenAxis = context.CubeRevCameraOrbit.multiply(
  context.CubeRevCameraOrbit.rotationY(0.8),
  cameraProbe.view_matrix
);
for (let i = 0; i < 9; i++) {
  assert.ok(Math.abs(afterUpsideHorizontal.view_matrix[i] - expectedScreenAxis[i]) < 1e-12);
}

for (const path of scripts) {
  await access(resolve(root, path));
  assert.ok(index.includes(`./${path}?v=${release.cacheKey}`), `${path} must use the shared cache key`);
  new Function(await read(path));
}
for (const path of [
  "calibration/randomization.js",
  "calibration/history-presentation.js",
  "calibration/neutral-probe.js",
  "calibration/runtime.js"
]) {
  await access(resolve(root, path));
  new Function(await read(path));
}

assert.match(index, /camera_orbit_policy:'screen_relative_matrix_360_orbit_v1'/);
assert.match(index, /KeyT:'x'.*KeyB:"x'"/s);
assert.match(index, /Semicolon:'y'.*KeyQ:"z'"/s);
assert.match(index, /id="cameraResetButton"/);
assert.match(index, /COLLECTION LOCKED/);
assert.match(index, /presentation_policy:\{modalities:\['TERMINAL_ONLY'\]/);
assert.doesNotMatch(index, /animateMove:\(token,duration\)=>enqueueAnimation\(token,duration,'history_presentation'\)/);
assert.doesNotMatch(historyPresentation, /animateMove|TEXT_HISTORY|ANIMATED_HISTORY/);
assert.match(calibrationConfig, /modalities: Object\.freeze\(\["TERMINAL_ONLY"\]\)/);
assert.match(calibrationConfig, /design: "1x2x2"/);
assert.doesNotMatch(calibrationConfig, /history_visibility: Object\.freeze\(\["hidden", "shown"\]\)/);

console.log(`CUBE-REV ${release.version} static validation passed.`);
