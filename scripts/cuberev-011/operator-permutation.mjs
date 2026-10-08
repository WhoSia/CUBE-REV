// CUBE-REV 0.11: Exact 54-sticker operator signature, preserving rotations.
import {solvedStickerCube,applyMoveToken} from '../cube/sticker-cube.mjs';
const ref=solvedStickerCube();
const key=x=>x.p.join(',')+'|'+x.n.join(',');
const toIndex=new Map(ref.map((x,i)=>[key(x),i]));
const identity=Uint8Array.from({length:54},(_,i)=>i);
const memo=new Map();
function single(token){
  if(memo.has(token))return memo.get(token);
  const cube=solvedStickerCube().map((x,id)=>({...x,p:[...x.p],n:[...x.n],id}));
  applyMoveToken(cube,token);
  const permutation=new Uint8Array(54);
  for(const sticker of cube){
    const dest=toIndex.get(key(sticker));
    if(dest===undefined)throw Error('STICKER_POSITION_MISMATCH');
    permutation[sticker.id]=dest;
  }
  memo.set(token,permutation);
  return permutation;
}
export function operatorPermutation(tokens){
  let p=identity;
  for(const token of tokens){
    const q=single(token.replace(/2'$/,'2'));
    p=Uint8Array.from(p,i=>q[i]);
  }
  return p;
}
export function operatorSignature(tokens){
  return Buffer.from(operatorPermutation(tokens)).toString('base64');
}
export function operatorIdentity(tokens){
  return operatorPermutation(tokens).every((p,i)=>p===i);
}
