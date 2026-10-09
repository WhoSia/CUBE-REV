import assert from 'node:assert/strict';
import {ACTIONS} from '../cuberev-013/cross4-pdb.mjs';
import {urMoveAutomaton,candidateMask,fixedObservationClasses,adaptiveOrientationDepth,
 UR_ORIENT_ZERO_MASK,FULL_MASK,allOccupancyFiberHistogram} from './ur-fiber-tomography.mjs';
const m=urMoveAutomaton();
assert.equal(m.length,18);
for(const q of m)assert.equal(new Set(q).size,24);
const inversePairs=[['U',"U'"],['R',"R'"],['F',"F'"],['D',"D'"],['L',"L'"],['B',"B'"]];
for(const [a,b] of inversePairs){
 const x=m[ACTIONS.indexOf(a)],y=m[ACTIONS.indexOf(b)];
 for(let j=0;j<24;j++)assert.equal(y[x[j]],j);
}
const support=occupied=>Array.from({length:24},(_,i)=>i).filter(i=>!occupied.includes(i>>1));
const s0=support([4,5,6,7]),s1=support([0,5,6,7]);
assert.equal(s0.length,16);assert.equal(s1.length,16);
const orientation0=['F','R2','B','D',"B'",'F'];
const orientation1=["F'",'U2',"B'",'D','B','F'];
assert.equal(fixedObservationClasses(orientation0,s0,m),16);
assert.equal(fixedObservationClasses(orientation1,s1,m),16);
const universal=['F','B','D','F','R2',"B'",'F','R',"F'",'B'];
assert.equal(fixedObservationClasses(universal,Array.from({length:24},(_,i)=>i),m),24);
const completion0=["U'",'U2','R','R2','U',"B'",'U',"R'","F'","U'",'F2',"U'",'R',"F'",'R',"U'","F'","U'","F'",'R'];
const completion1=["R'",'U2',"U'","R'",'U2',"R'","B'","R'",'U','B','U','F','R',"U'",'F2',"U'","B'","R'",'F',"U'",'R'];
assert.equal(fixedObservationClasses(completion0,s0,m,'completion'),16);
assert.equal(fixedObservationClasses(completion1,s1,m,'completion'),16);
for(const occupied of [[4,5,6,7],[0,5,6,7]]){
 const mask=candidateMask(occupied),memo=new Map();
 assert.equal(Math.max(
  adaptiveOrientationDepth(mask&UR_ORIENT_ZERO_MASK,m,memo),
  adaptiveOrientationDepth(mask&(FULL_MASK^UR_ORIENT_ZERO_MASK),m,memo)),6);
}
for(let a=0;a<18;a++)for(let slot=0;slot<12;slot++)
 assert.equal(m[a][2*slot]>>1,m[a][2*slot+1]>>1,'position is flip-invariant');
const histogram=allOccupancyFiberHistogram(m);
assert.deepEqual(histogram.profile,{'5':192,'6':297,'7':6});
assert.equal(histogram.maxDepth,7);assert.equal(histogram.slotFamilies,495);
console.log('CUBE_REV_015_P3C_ONE_BIT_ADAPTIVE_495_FIBER_PASS',JSON.stringify(histogram));
