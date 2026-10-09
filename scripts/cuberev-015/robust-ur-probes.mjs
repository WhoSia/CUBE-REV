/** CUBE-REV 0.15 P3D-E — deterministic, single-error-correcting UR observation word.
 * Mathematical 24-coordinate edge automaton; no human source data.
 * Certificates are for a tracked UR intrinsic-orientation bit after each move.
 */
import {ACTIONS} from '../cuberev-013/cross4-pdb.mjs';
export const ROBUST_UR_WORD=Object.freeze(
 ['U','F','R2','B','L2','F','R','F','B','R','L','F','U','L','B','F']);
export const ORIGINAL_P3C_UNIVERSAL_WORD=Object.freeze(
 ['F','B','D','F','R2',"B'",'F','R',"F'",'B']);
export function urOrientationCodewords(moves,word=ROBUST_UR_WORD){
 if(!Array.isArray(moves)||moves.length!==18||word.length>21)throw Error('MOVE_CONTRACT');
 const result=Array.from({length:24},(_,initial)=>{
  let x=initial,code=Number(x%2===0);
  for(let t=0;t<word.length;t++){
   const a=ACTIONS.indexOf(word[t]);if(a<0)throw Error('ILLEGAL_MOVE');
   x=moves[a][x];code|=Number(x%2===0)<<(t+1);
  }
  return code;
 });
 return result;
}
export function minimumCodeDistance(codewords){
 let min=Infinity,pairs=0;
 for(let i=0;i<codewords.length;i++)for(let j=i+1;j<codewords.length;j++){
  let v=codewords[i]^codewords[j],d=0;
  while(v){v&=v-1;d++;}
  if(d<min){min=d;pairs=1;}else if(d===min)pairs++;
 }
 return {minimum:min,pairsAtMinimum:pairs};
}
export function verifySingleBitCorrection(codewords,bitCount){
 if(bitCount>22)throw Error('CODE_LENGTH');
 const seen=new Set();
 for(const w of codewords){
  for(const candidate of [w,...Array.from({length:bitCount},(_,i)=>w^(1<<i))]){
   if(seen.has(candidate))return false;
   seen.add(candidate);
  }
 }
 return seen.size===codewords.length*(bitCount+1);
}
