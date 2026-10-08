import assert from 'node:assert/strict';
import {normalizeCubeWord as nf,classifyCubeWordPair as cl} from './full-notation-normal-form.mjs';
import {solvedStickerCube,applyAlgorithm} from './sticker-cube.mjs';
const defs=[['r',['x','L']],['l',["x'",'R']],['u',['y','D']],['M',["x'","L'",'R']],['E',["y'","D'","U"]],['S',["F'","B",'z']],['Rw',['r']],['x',['R',"M'","L'"]]];
for(const [a,b] of defs){const x=nf([a]),y=nf(b);assert.equal(x.frame,y.frame);assert.equal(x.elementary_form,y.elementary_form);}
const a=["U'","l'","U","l2","U'","l2","U'","l2","U","l'"];
const b=['U',"r'",'U','r2',"U'",'r2',"U'",'r2','U',"r'",'U','U'];
assert.equal(cl(a,b),'ADDITIONAL_CUBE_RELATION_REQUIRED');
assert.equal(cl(['U','U'],['U2']),'ELEMENTARY_REWRITE_EQUIVALENT');
const frames=new Map([['URFDLB',[]]]),queue=[[]];
for(let i=0;i<queue.length;i++)for(const rot of ['x','y','z']){const word=[...queue[i],rot],frame=nf(word).frame;if(!frames.has(frame)){frames.set(frame,word);queue.push(word);}}
assert.equal(frames.size,24);
let seed=177,parity=0;const tokens=['U','R','L','F','D','B','x','y','z','r','l','u','d','f','b','M','E','S','U2',"R'",'r2',"y'","S'","Rw'"];
const check=seq=>{const x=nf(seq);const expected=solvedStickerCube(),actual=solvedStickerCube();applyAlgorithm(expected,seq.join(' '));applyAlgorithm(actual,[...x.body,...frames.get(x.frame)].join(' '));assert.deepEqual(actual,expected);parity++;};
for(const t of tokens)check([t]);
for(let t=0;t<250;t++){const seq=[],n=1+t%14;for(let k=0;k<n;k++){seed=(Math.imul(seed,1664525)+1013904223)>>>0;seq.push(tokens[seed%tokens.length]);}check(seq);}
const c1=solvedStickerCube(),c2=solvedStickerCube();applyAlgorithm(c1,a.join(' '));applyAlgorithm(c2,b.join(' '));assert.deepEqual(c1,c2);
assert.notEqual(nf(a).elementary_form,nf(b).elementary_form);
console.log('CUBE_REV_011_FULL_NOTATION_PASS 11_ALGEBRA 274_ENGINE_CHECKS 24_ORIENTATIONS');
