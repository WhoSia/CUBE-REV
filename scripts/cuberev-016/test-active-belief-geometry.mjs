import assert from 'node:assert/strict';
import {ACTIONS} from '../cuberev-013/cross4-pdb.mjs';
import {urMoveAutomaton} from '../cuberev-015/ur-fiber-tomography.mjs';
import {ROBUST_UR_WORD,urOrientationCodewords} from '../cuberev-015/robust-ur-probes.mjs';
import {ACTIONS_016,validateMoves,exactP0Court,oneReadBayesValue,
  bayesUpdate,oneBitExperiment,nongarblingWitness} from './active-belief-geometry.mjs';
const moves=urMoveAutomaton();
assert.deepEqual(ACTIONS_016,ACTIONS,'0.15 fixed HTM grammar parity');
assert.equal(validateMoves(moves),true);
assert.deepEqual(urOrientationCodewords(moves,ROBUST_UR_WORD),[
 98803,32268,131071,0,65743,65328,127231,3840,511,130560,32259,98812,
 69631,61440,61455,69616,61635,69436,32707,98364,130575,496,32575,98496]);
const court=exactP0Court(moves);
assert.deepEqual(court.partitionHorizonCounts,[2,6,24,24]);
assert.equal(court.terminalClasses,24);
assert.deepEqual(court.pairOutcomes,{distinguishable:48,indistinguishable:18});
assert.equal(court.valueBad,0.5);
assert.equal(court.valueGood,1);
assert.equal(court.sameEntropyBits,1);
assert.deepEqual(court.blackwellFnotFromB,{p:0,q:1});
assert.deepEqual(court.blackwellBnotFromF,{p:0,q:3});
assert.equal(court.uConstantOnKnownFlip0,true);
assert.equal(court.uniformPriorOneReadNoNoise.F,1/6);
assert.equal(court.uniformPriorOneReadNoNoise.U,1/12);
const bad=Array.from({length:24},(_,x)=>x===0||x===4?0.5:0);
const good=Array.from({length:24},(_,x)=>x===2||x===6?0.5:0);
for(let a=0;a<18;a++)assert.equal(oneReadBayesValue(bad,moves,a,0.05),0.5);
assert.equal(oneReadBayesValue(good,moves,ACTIONS.indexOf('F'),0.05),0.95);
for(const eps of [0,0.05,0.25,0.5]){
 const prior=Array.from({length:24},(_,x)=>x===0?0.7:x===1?0.3:0);
 const results=[0,1].map(y=>bayesUpdate(prior,moves[ACTIONS.indexOf('U')],y,eps));
 assert.ok(Math.abs(results.reduce((s,v)=>s+v.likelihood,0)-1)<1e-12);
 for(const {posterior} of results)if(posterior)assert.ok(
  Math.abs(posterior.reduce((a,b)=>a+b,0)-1)<1e-12);
}
for(const eps of [0,0.05,0.2]){
 const F=oneBitExperiment(moves,ACTIONS.indexOf('F'),eps);
 const B=oneBitExperiment(moves,ACTIONS.indexOf('B'),eps);
 assert.ok(nongarblingWitness(F,B));
 assert.ok(nongarblingWitness(B,F));
}
console.log('CUBE_REV_016_P0_FROZEN_015_CUBIE_SOURCE_PASS');
console.log(JSON.stringify(court));
