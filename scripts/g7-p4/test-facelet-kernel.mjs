import assert from "node:assert/strict";
import {solvedStickers,applyAlg,stateSignature,isSolvedUpToRotation,validateStickerState} from "./facelet-kernel.mjs";
const s=solvedStickers(), sig=stateSignature(s);
assert.equal(validateStickerState(s),true);
for(const m of ["U","R","F","D","L","B","M","E","S","x","y","z","r","u","f","Rw","Uw","Fw"]){
  assert.equal(stateSignature(applyAlg(s,`${m} ${m} ${m} ${m}`)),sig,m+" order4");
}
assert.equal(stateSignature(applyAlg(s,"r")),stateSignature(applyAlg(s,"R M'")),"r = R M'");
assert.equal(stateSignature(applyAlg(s,"u")),stateSignature(applyAlg(s,"U E'")),"u = U E'");
assert.equal(stateSignature(applyAlg(s,"f")),stateSignature(applyAlg(s,"F S")),"f = F S");
assert.equal(stateSignature(applyAlg(s,"(r2' y)")),stateSignature(applyAlg(s,"r2' y")),"group punctuation");
assert.equal(stateSignature(applyAlg(s,"R U R' U' R U R' U' R U R' U' R U R' U' R U R' U' R U R' U'")),sig,"sexy x6");
assert.equal(isSolvedUpToRotation(applyAlg(s,"x y z")),true);
assert.equal(isSolvedUpToRotation(applyAlg(s,"R")),false);
console.log("G7_P4_FACELET_KERNEL_TEST_PASS");
