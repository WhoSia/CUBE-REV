import assert from "node:assert/strict";
import { classifyToken, parseReconstruction } from "./parse-reconstruction.mjs";

assert.equal(classifyToken("R2"), "FACE_TURN");
assert.equal(classifyToken("Rw'"), "WIDE_TURN");
assert.equal(classifyToken("r2"), "WIDE_TURN");
assert.equal(classifyToken("M'"), "SLICE_TURN");
assert.equal(classifyToken("y"), "ROTATION");
assert.equal(classifyToken("???"), "UNKNOWN");

const a = parseReconstruction("R U R' // cross\nU2 F2 // 1st pair");
assert.equal(a.status, "PARSED");
assert.equal(a.geometry_status, "HTM_READY");
assert.deepEqual(a.events.map(x => x.kind), [
  "FACE_TURN","FACE_TURN","FACE_TURN","ANNOTATION",
  "FACE_TURN","FACE_TURN","ANNOTATION"
]);
assert.equal(a.events[3].annotation, "cross");

const b = parseReconstruction("x // inspection\nR U R'\ny U2");
assert.equal(b.status, "PARSED");
assert.equal(b.geometry_status, "FRAME_CANONICALIZATION_REQUIRED");

const c = parseReconstruction("Rw U M' // setup");
assert.equal(c.geometry_status, "EXTENDED_MOVE_KERNEL_REQUIRED");

const d = parseReconstruction("R U [bad]");
assert.equal(d.status, "PARTIAL");
assert.equal(d.geometry_status, "UNRESOLVED");
assert.equal(d.events.at(-1).kind, "UNKNOWN");

console.log("G7_P2_RECONSTRUCTION_PARSER_PASS");

const grouped = parseReconstruction("(r2' y) // grouped notation");
assert.equal(grouped.status, "PARSED");
assert.deepEqual(grouped.events.filter(e=>e.kind!=="ANNOTATION").map(e=>e.raw), ["r2'","y"]);
assert.equal(grouped.geometry_status, "EXTENDED_MOVE_KERNEL_REQUIRED");

const adjacent = parseReconstruction("U' L' U' l'U R' // cross");
assert.equal(adjacent.status, "PARSED");
assert.deepEqual(adjacent.events.filter(e=>e.kind!=="ANNOTATION").map(e=>e.raw), ["U'","L'","U'","l'","U","R'"]);
