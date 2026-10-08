import assert from 'node:assert/strict';
import {exhaustiveFutureDistanceRefinement} from './future-distance-refinement.mjs';
const got=exhaustiveFutureDistanceRefinement();
assert.equal(got.state_count,190080);
assert.equal(got.transition_inverse_checks,3421440);
assert.equal(got.triangle_checks,3421440);
assert.equal(got.minimal_counterfactual_horizon,3);
assert.deepEqual(got.partition_rounds,[
 {k:0,classes:9,largest_class:97254,singleton_classes:1},
 {k:1,classes:153252,largest_class:30,singleton_classes:129765},
 {k:2,classes:190077,largest_class:2,singleton_classes:190074},
 {k:3,classes:190080,largest_class:1,singleton_classes:190080}
]);
console.log('CUBE_REV_015_EXHAUSTIVE_FUTURE_CONGRUENCE_PASS');
