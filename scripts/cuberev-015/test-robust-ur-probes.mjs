import assert from 'node:assert/strict';
import {urMoveAutomaton} from './ur-fiber-tomography.mjs';
import {ROBUST_UR_WORD,ORIGINAL_P3C_UNIVERSAL_WORD,urOrientationCodewords,
 minimumCodeDistance,verifySingleBitCorrection} from './robust-ur-probes.mjs';
const m=urMoveAutomaton();
const expected=[98803,32268,131071,0,65743,65328,127231,3840,511,130560,32259,98812,
 69631,61440,61455,69616,61635,69436,32707,98364,130575,496,32575,98496];
const codes=urOrientationCodewords(m);
assert.deepEqual(codes,expected,'independent C++ frozen search replay');
assert.equal(new Set(codes).size,24);
assert.deepEqual(minimumCodeDistance(codes),{minimum:3,pairsAtMinimum:2});
assert.equal(verifySingleBitCorrection(codes,17),true);
const previous=urOrientationCodewords(m,ORIGINAL_P3C_UNIVERSAL_WORD);
assert.equal(minimumCodeDistance(previous).minimum,1);
assert.equal(verifySingleBitCorrection(previous,11),false);
for(let a=0;a<12;a++)for(let b=a+1;b<12;b++)for(let c=b+1;c<12;c++)for(let d=c+1;d<12;d++){
 const original=Array.from({length:24},(_,i)=>i)
  .filter(i=>![a,b,c,d].includes(i>>1));
 assert.equal(original.length,16);
 assert.equal(new Set(original.map(i=>codes[i])).size,16);
}
console.log('CUBE_REV_015_P3D_ECC_ALL_495_FIBERS_PASS');
