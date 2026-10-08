import assert from 'node:assert/strict';
import {operatorSignature,operatorIdentity} from './operator-permutation.mjs';
for(const face of ['U','R','F','D','L','B','x','y','z','M','E','S']){
  assert.ok(operatorIdentity([face,face+"'"]));
  assert.ok(operatorIdentity([face+'2',face+'2']));
}
assert.equal(operatorSignature(['U','D']),operatorSignature(['D','U']));
assert.notEqual(operatorSignature(['R','U']),operatorSignature(['U','R']));
assert.equal(operatorSignature(["L'",'U','L','U2','F']),operatorSignature(['F','U2','R','U',"R'"]));
console.log('CUBE_REV_011_OPERATOR_SIGNATURE_PASS');
