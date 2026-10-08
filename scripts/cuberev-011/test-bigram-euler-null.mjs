import assert from 'node:assert/strict';
import {eulerBigramSurrogate,seedRng,directedBigramCounts} from './bigram-euler-null.mjs';
const vectors=[
 [],['U'],['U','R'],['U','R','U','F','U','B','U','R'],
 ['U','R','U','F','U','B','U','F','U','R','U'],
 ['R','U','R',"U'",'R','U','R'],
 ['x','M','u','x','E','u','x','M','u','x']
];
let assertions=0;
for(const seq of vectors)for(const seed of [1,17,2026100801]){
 const s=eulerBigramSurrogate(seq,seedRng(seed));
 assert.deepEqual(directedBigramCounts(s),directedBigramCounts(seq));assertions++;
 assert.equal(s.length,seq.length);assertions++;
 assert.equal(s[0],seq[0]);assert.equal(s.at(-1),seq.at(-1));assertions++;
 assert.deepEqual(s,eulerBigramSurrogate(seq,seedRng(seed)));assertions++;
}
assert.throws(()=>eulerBigramSurrogate('UR',seedRng(1)));
console.log('CUBE_REV_011_BIGRAM_EULER_PASS',assertions+1);
