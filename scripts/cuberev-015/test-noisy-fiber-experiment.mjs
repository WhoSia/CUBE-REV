import assert from 'node:assert/strict';
import {urMoveAutomaton} from './ur-fiber-tomography.mjs';
import {noisyCodewords,exactBscMap,majorityBitError,uniformFiberGuarantee,
 exactAdaptiveBayes,sensorBit} from './noisy-fiber-experiment.mjs';
const moves=urMoveAutomaton();
const fiber=blocked=>Array.from({length:24},(_,i)=>i)
 .filter(i=>!(blocked?[0,5,6,7]:[4,5,6,7]).includes(i>>1));
const word0=['F','R2','B','D',"B'",'F'];
const word1=["F'",'U2',"B'",'D','B','F'];
for(const [f,w] of [[fiber(false),word0],[fiber(true),word1]]){
 const c=noisyCodewords(f,w,moves,'orientation');
 assert.equal(new Set(c.signatures).size,16);
 assert.equal(c.readCount,7);
 for(const [eps,want] of [[0,1],[.05,.842453995703125],[.5,.0625]]){
  const result=exactBscMap(c.signatures,7,eps);
  assert.ok(Math.abs(result.accuracy-want)<1e-11);
 }
 assert.ok(Math.abs(exactAdaptiveBayes(f,moves,'orientation',.05,2)-.32715625)<1e-12);
}
assert.ok(Math.abs(exactAdaptiveBayes(fiber(false),moves,'completion',.05,2)-.225625)<1e-12);
assert.ok(Math.abs(exactAdaptiveBayes(fiber(true),moves,'completion',.05,2)-.1721875)<1e-12);
assert.ok(Math.abs(majorityBitError(.05,5)-.001158125)<1e-12);
const bound=uniformFiberGuarantee(.05,5);
assert.ok(Math.abs(bound.successLower-.990735)<1e-12);
assert.equal(bound.maxPhysicalReads,40);
assert.equal(sensorBit(0,'completion'),1);
assert.equal(sensorBit(2,'completion'),0);
assert.equal(sensorBit(0,'orientation'),sensorBit(2,'orientation'));
assert.equal(sensorBit(2,'completion'),sensorBit(3,'completion'));
assert.notEqual(sensorBit(2,'orientation'),sensorBit(3,'orientation'));
console.log('CUBE_REV_015_P3D_NOISY_CHANNEL_REGRESSIONS_PASS');
