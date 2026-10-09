import assert from 'node:assert/strict';
import {ACTIONS} from '../cuberev-013/cross4-pdb.mjs';
import {urMoveAutomaton} from '../cuberev-015/ur-fiber-tomography.mjs';
import {ROBUST_UR_WORD,urOrientationCodewords} from '../cuberev-015/robust-ur-probes.mjs';
import {exactThreeReadCensus} from './three-read-feedback-census.mjs';
const m=urMoveAutomaton();
assert.equal(ACTIONS.length,18);
assert.deepEqual(urOrientationCodewords(m,ROBUST_UR_WORD),[
 98803,32268,131071,0,65743,65328,127231,3840,511,130560,32259,98812,
 69631,61440,61455,69616,61635,69436,32707,98364,130575,496,32575,98496]);
const result=exactThreeReadCensus(m);
assert.equal(result.initialSupportCount,4095);
assert.equal(result.allFixedActionTriples,5832);
assert.equal(result.uniqueFixedHistoryPartitions,254);
assert.deepEqual(result.leafCountHistogram,{
 '1,1':12,'2,2':76,'3,3':509,'4,3':2,'4,4':3496
});
assert.deepEqual(result.strictAdaptiveWitnesses,[
 {subset:170,adaptive:4,fixed:3},
 {subset:3840,adaptive:4,fixed:3}
]);
assert.equal(result.maxAdaptiveLeafAdvantage,1);
assert.equal(result.summaryClasses,43);
assert.equal(result.summaryAdaptiveDisagreementClasses,9);
assert.equal(result.summaryFixedDisagreementClasses,9);
assert.equal(result.summaryValueDisagreementSupports,970);
const a=Object.fromEntries(ACTIONS.map((x,i)=>[x,i]));
const read=x=>Number((x&1)===0);
function witnessRead(initialSlot){
 let state=m[a.F][2*initialSlot],y1=read(state);
 state=m[y1===0?a.R:a.U][state];
 let y2=read(state);
 const finalAct=y1===0&&y2===0?a.F:y1===1&&y2===1?a.B:a.U;
 state=m[finalAct][state];
 return `${y1}${y2}${read(state)}`;
}
for(const support of [[1,3,5,7],[8,9,10,11]])
 assert.equal(new Set(support.map(witnessRead)).size,4);
console.log('CUBE_REV_016_P2_EXACT_4095_AND_TWO_ADAPTIVE_WITNESSES_PASS');
console.log(JSON.stringify(result));
