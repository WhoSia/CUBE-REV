import assert from 'node:assert/strict';
import {buildCrossPDB,FACE_EDGE_IDS,indexOfFourEdges,STATE_COUNT} from './cross4-pdb.mjs';
const ep=Array.from({length:12},(_,i)=>i),eo=new Array(12).fill(0);
for(const [face,sha] of Object.entries({
 D:'916a33eec009cf7c46216616dd73261bb5f420173e0dbd7d2505df47883749b2',
 U:'85e932d0e78b3acbe61c89427723b10fcc21d3645edf085a29dca9a7607dccdd'
})){
 const r=buildCrossPDB(face);
 assert.equal(r.reachable,STATE_COUNT);
 assert.equal(r.diameter,8);
 assert.equal(r.distances[indexOfFourEdges(ep,eo,FACE_EDGE_IDS[face])],0);
 assert.equal(r.sha256,sha,'cross PDB engine parity: '+face);
}
console.log('CUBE_REV_013_EXACT_CROSS_PDB_PASS');
