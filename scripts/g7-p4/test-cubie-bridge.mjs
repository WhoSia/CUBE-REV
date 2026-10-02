import assert from "node:assert/strict";
import {solvedStickers,applyAlg} from "./facelet-kernel.mjs";
import {toCubie,solvedCubie,applyCubieFace,cubieEqual,phase1,findSingleHtmTransition} from "./cubie-bridge.mjs";

const s=solvedStickers();
const solved=solvedCubie();
assert.deepEqual(solved,{cp:[0,1,2,3,4,5,6,7],co:[0,0,0,0,0,0,0,0],ep:[0,1,2,3,4,5,6,7,8,9,10,11],eo:[0,0,0,0,0,0,0,0,0,0,0,0]});
for(const face of ["U","R","F","D","L","B"]){
  const a=toCubie(applyAlg(s,face));
  const b=applyCubieFace(solved,face,1);
  assert.ok(cubieEqual(a,b),face+" cubie bridge");
}
assert.ok(cubieEqual(toCubie(applyAlg(s,"x y z")),solved),"whole-cube rotations canonicalize");
assert.equal(phase1(solved).rank,0);
const wide=toCubie(applyAlg(s,"r"));
const tr=findSingleHtmTransition(solved,wide);
assert.equal(tr.kind,"SINGLE_HTM");
const slice=toCubie(applyAlg(s,"M"));
assert.equal(findSingleHtmTransition(solved,slice).kind,"MULTI_ACTION_EXTENDED");
console.log("G7_P4_CUBIE_BRIDGE_TEST_PASS");
