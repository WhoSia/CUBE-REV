import assert from 'node:assert/strict';
import {urMoveAutomaton} from '../cuberev-015/ur-fiber-tomography.mjs';
import {ROBUST_UR_WORD,urOrientationCodewords} from '../cuberev-015/robust-ur-probes.mjs';
import {exactUnknownEdgeDiagnosis,exactUnknownEdgeReset,exactForgottenWordPreimages} from './reversal-information-court.mjs';
const maps=urMoveAutomaton();
// Predecessor 0.15 action-coordinate parity — anti-accidental grammar drift.
assert.deepEqual(urOrientationCodewords(maps,ROBUST_UR_WORD),
 [98803,32268,131071,0,65743,65328,127231,3840,511,130560,32259,98812,
  69631,61440,61455,69616,61635,69436,32707,98364,130575,496,32575,98496]);
const identification=exactUnknownEdgeDiagnosis(maps,8);
assert.deepEqual(identification.maxLeaves,[1,2,4,6,8,12,16,20,24]);
const reset=exactUnknownEdgeReset(maps,10);
assert.deepEqual(reset.feasible,[false,false,false,false,false,false,false,false,false,false,true]);
const history=exactForgottenWordPreimages(maps,4,0);
assert.equal(history.totalWords,'104976');
assert.equal(history.sameEndpointCount,'26584');
assert.equal(history.largestEndpointFiber,'26584');
assert.equal(history.worstCaseAdditionalBits,15);
assert.equal(history.endpointCounts.length,24);
console.log('CUBE_REV_016_INTERNAL_P7_EXACT_DIAG8_RESET10_PATH15BITS_PASS');
console.log(JSON.stringify({leaves:identification.maxLeaves,reset:reset.feasible,
 counted_four_words:history.totalWords,largest_history_fiber:history.largestEndpointFiber}));
