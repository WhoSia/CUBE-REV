import assert from 'node:assert/strict';
import {cosetObservationWitness,sixCrossTables} from './coset-observation-witness.mjs';
const expected={
 U:'85e932d0e78b3acbe61c89427723b10fcc21d3645edf085a29dca9a7607dccdd',
 D:'916a33eec009cf7c46216616dd73261bb5f420173e0dbd7d2505df47883749b2',
 R:'59efcecb5f8f17815cf63901089d7979d96ddd144d129a1a8426f15e1d17cd8a',
 L:'b0f895f8b74262bdb7048b334da2b604a28a9d5d6b8f345768a26d52356a1dd0',
 F:'ec57326d048460ccbee9f5ccb172ffec228b619919bdbe86c02b8bde585e7890',
 B:'969c099c3610c69a65ccc3d2b655a4846af65f3189026d3aa579f1da8e067486'
};
const tables=sixCrossTables();
for(const f of Object.keys(expected))assert.equal(tables[f].sha256,expected[f],'EXACT_190080_PDB_'+f);
const x=cosetObservationWitness(tables,2);
assert.equal(x.phase1_fiber,'G1');
assert.equal(x.full_channel_equal,false);
assert.deepEqual(x.delta_U_Up,[1,-1]);
function close(a,b){assert.ok(Math.abs(a-b)<1e-9,a+' != '+b);}
close(x.probability_U_Up[0],0.026905466459394328);
close(x.probability_U_Up[1],0.5272970941259929);
close(x.leakage_e.full,0.6748667214094297);
close(x.leakage_U.full,0.24614370232292693);
close(x.leakage_e.face,0.6748667214094297);
close(x.leakage_U.face,0.19054799935373723);
close(x.leakage_e.power,0);
close(x.leakage_U.power,0.03776186368458352);
assert.ok(x.leakage_e.full!==x.leakage_U.full);
console.log('CUBE_REV_014_P5_COSET_NONFACTORIZATION_PASS');
