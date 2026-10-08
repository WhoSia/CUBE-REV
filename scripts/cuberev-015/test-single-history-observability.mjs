import assert from 'node:assert/strict';
import {fixedWordObservation,elementaryObservationLowerBound} from './single-history-observability.mjs';
const lb=elementaryObservationLowerBound();
assert.equal(lb.max_initial_distance_fiber,97254);
assert.equal(lb.min_observed_turns,11);
const x=fixedWordObservation(2026100901,100);
assert.equal(x.first_injective,42);
for(const [k,classes,largest] of [[0,9,97254],[3,116,27717],[10,29105,1400],
 [11,47507,899],[20,180036,49],[40,190079,2],[41,190079,2],[42,190080,1]]){
 assert.equal(x.rounds[k].classes,classes,'horizon '+k);
 assert.equal(x.rounds[k].largest_class,largest,'largest '+k);
}
assert.equal(x.word.length,42);
console.log('CUBE_REV_015_FIXED_HISTORY_AND_LOWER_BOUND_PASS');
