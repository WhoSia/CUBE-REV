import assert from "node:assert/strict";
import {solvedStickerCube,applyAlgorithm,applyMoveToken,solvedUpToRotation,toCubieState,cubieSolved} from "./sticker-cube.mjs";

let c=solvedStickerCube();
applyAlgorithm(c,"R U2 F' F U2 R'");
assert.equal(solvedUpToRotation(c),true);
assert.equal(cubieSolved(toCubieState(c)),true);

const expectedR={
 cp:[4,1,2,0,7,5,6,3],
 co:[2,0,0,1,1,0,0,2],
 ep:[8,1,2,3,11,5,6,7,4,9,10,0],
 eo:[0,0,0,0,0,0,0,0,0,0,0,0]
};
c=solvedStickerCube();applyMoveToken(c,"R");
assert.deepEqual(toCubieState(c),expectedR);

for(const t of ["x","y","z","M","E","S","r","l","u","d","f","b","Rw","Uw'"]){
  c=solvedStickerCube();
  for(let i=0;i<4;i++) applyMoveToken(c,t);
  assert.equal(cubieSolved(toCubieState(c)),true,t);
}
console.log("G7_P4_STICKER_CUBE_TEST_PASS");
