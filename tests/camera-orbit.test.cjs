"use strict";

const assert = require("node:assert/strict");
const orbit = require("../js/camera-orbit.js");

let camera = orbit.resetCamera(1);
camera = orbit.screenRelativeOrbit(camera, 0, Math.PI / 0.008, 0.008);
assert.ok(Math.abs(camera.pitch - Math.PI) < 1e-12);
const before = camera.view_matrix.slice();
const next = orbit.screenRelativeOrbit(camera, 120, 0, 0.008);
const expected = orbit.multiply(orbit.rotationY(0.96), before);
for (let i = 0; i < 9; i++) assert.ok(Math.abs(next.view_matrix[i] - expected[i]) < 1e-12);
const reset = orbit.resetCamera(1.25);
assert.deepEqual(reset.view_matrix, orbit.IDENTITY);
assert.equal(reset.zoom, 1.25);

console.log("CUBE-REV 0.7.12 screen-relative camera orbit tests passed.");
