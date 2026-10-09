import assert from 'node:assert/strict';
import {urMoveAutomaton} from '../cuberev-015/ur-fiber-tomography.mjs';
import {ROBUST_UR_WORD,urOrientationCodewords} from '../cuberev-015/robust-ur-probes.mjs';
import {orientedFacePair,verifyFaceArcIdentity,independentEndpointCounts,
 exactReturnCount,exactWorstCaseLogBits,spectralChiSquared,entropyCorrectionBound} from './spectral-history-court.mjs';
const moves=urMoveAutomaton();
assert.deepEqual(urOrientationCodewords(moves,ROBUST_UR_WORD),
 [98803,32268,131071,0,65743,65328,127231,3840,511,130560,32259,98812,
  69631,61440,61455,69616,61635,69436,32707,98364,130575,496,32575,98496]);
assert.deepEqual(orientedFacePair(0),['U','R']);
assert.deepEqual(orientedFacePair(1),['R','U']);
assert.deepEqual(orientedFacePair(16),['F','R']);
const graph=verifyFaceArcIdentity(moves);
assert.deepEqual(graph,{differing:0,rows:24,cols:24,legalActions:18,symmetric:true,
 minimumSelfLoops:12,maximumSelfLoops:12,rowSumsEqual18:true});
const times=[0,1,2,3,4,5,8,12];
const returns=['1','12','150','1956','26584','375472','1276024704','87115708749824'];
const bits=[0,4,8,11,15,19,31,47];
for(let k=0;k<times.length;k++){
 assert.equal(String(exactReturnCount(times[k])),returns[k]);
 assert.equal(exactWorstCaseLogBits(times[k]),bits[k]);
}
for(let t=0;t<=12;t++){
 const q=exactReturnCount(t),expected=18n**BigInt(t);
 for(let x=0;x<24;x++){
  const counts=independentEndpointCounts(moves,t,x);
  assert.equal(counts.reduce((a,b)=>a+b,0n),expected);
  assert.equal(counts[x],q);
  assert.ok(counts.every(y=>y<=q));
 }
 // Exact endpoint entropy versus the theoretical 2-Renyi mixing correction.
 const counts=independentEndpointCounts(moves,t,0);
 const dist=counts.map(c=>Number(c)/Number(expected));
 const H=-dist.filter(p=>p>0).reduce((z,p)=>z+p*Math.log2(p),0);
 const delta=Math.log2(24)-H;
 assert.ok(delta>=-1e-12);
 assert.ok(delta<=entropyCorrectionBound(t)+1e-12);
 const chisq=24*dist.reduce((z,p)=>z+(p-1/24)**2,0);
 assert.ok(Math.abs(chisq-spectralChiSquared(t))<1e-10);
}
assert.throws(()=>exactReturnCount(-1));
console.log('CUBE_REV_016_P8_EXACT_24X18_LINE_GRAPH_13_HORIZONS_SPECTRUM_PASS');
console.log(JSON.stringify({counts:times.map((t,i)=>({t,returnFibers:returns[i],sideBits:bits[i]})),
 dualGraph:graph,nontrivialSpectralRadius:'8/9'}));
