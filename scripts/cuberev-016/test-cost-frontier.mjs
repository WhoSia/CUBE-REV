import assert from 'node:assert/strict';
import {urMoveAutomaton} from '../cuberev-015/ur-fiber-tomography.mjs';
import {exactCostFrontiers,valueFromLines} from './cost-frontier.mjs';
const moves=urMoveAutomaton();
for(const slots of [[1,3,5,7],[8,9,10,11]]){
 const r=exactCostFrontiers(moves,slots);
 assert.equal(r.allFixedWords,5832);
 assert.deepEqual(r.adaptive,[[1,0],[2,4],[3,8],[4,12]]);
 assert.deepEqual(r.fixed,[[1,0],[2,4],[3,8]]);
 for(const k of [0,.02,.05,.1,.125,.15,.2,.24,.25,.3,.4,1]){
  const av=valueFromLines(r.adaptive,k),fx=valueFromLines(r.fixed,k);
  const expected=Math.max(0,.25-k);
  assert.ok(Math.abs((av-fx)-expected)<1e-12,
    JSON.stringify({slots,k,av,fx,expected}));
 }
 assert.equal(valueFromLines(r.adaptive,0),1);
 assert.equal(valueFromLines(r.fixed,0),.75);
 assert.equal(valueFromLines(r.adaptive,.25),.25);
 assert.equal(valueFromLines(r.fixed,.25),.25);
}
console.log('CUBE_REV_016_INTERNAL_P3_COMPLETE_RATIONAL_COST_FRONTIER_PASS');
