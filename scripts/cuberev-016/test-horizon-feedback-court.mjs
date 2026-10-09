import assert from 'node:assert/strict';
import {urMoveAutomaton} from '../cuberev-015/ur-fiber-tomography.mjs';
import {ROBUST_UR_WORD,urOrientationCodewords} from '../cuberev-015/robust-ur-probes.mjs';
import {exactH4AllBeliefs,exactH5SelectedBeliefs} from './horizon-feedback-court.mjs';
const moves=urMoveAutomaton();
const frozen=[98803,32268,131071,0,65743,65328,127231,3840,511,130560,32259,98812,
 69631,61440,61455,69616,61635,69436,32707,98364,130575,496,32575,98496];
assert.deepEqual(urOrientationCodewords(moves,ROBUST_UR_WORD),frozen,
 'CUBE-REV 0.15 sticker-derived physical-action contract drift');
const h4=exactH4AllBeliefs(moves);
assert.equal(h4.supports,4095);
assert.equal(h4.allFixedWords,104976);
assert.equal(h4.distinctFixedPartitions,1913);
assert.equal(h4.strictCount,1331);
assert.deepEqual(h4.histogram,{'1,1':12,'2,2':66,'3,3':223,
 '4,4':901,'5,5':1562,'6,5':1331});
assert.equal(h4.firstStrict[0].mask,175);
const h5=exactH5SelectedBeliefs(moves);
assert.equal(h5.allFixedWords,1889568);
assert.deepEqual([h5.full12.adaptive,h5.full12.fixed],[8,7]);
assert.deepEqual([h5.full24.adaptive,h5.full24.fixed],[12,10]);
assert.deepEqual([h5.known170.adaptive,h5.known170.fixed],[4,4]);
assert.deepEqual([h5.unknown170.adaptive,h5.unknown170.fixed],[8,8]);
assert.deepEqual([h5.unknown3840.adaptive,h5.unknown3840.fixed],[8,8]);
assert.deepEqual(h5.full12.histogram,
 {'1':537824,'2':882752,'3':222464,'4':196032,'5':42816,'6':7040,'7':640});
assert.deepEqual(h5.full24.histogram,
 {'2':691488,'4':895104,'6':176256,'8':112896,'10':13824});
console.log('CUBE_REV_016_INTERNAL_P3_H4_4095_AND_H5_1889568_PASS');
console.log(JSON.stringify({h4:{strict:h4.strictCount,distinct:h4.distinctFixedPartitions},
 h5:{full12:[h5.full12.adaptive,h5.full12.fixed],
 full24:[h5.full24.adaptive,h5.full24.fixed]}}));
