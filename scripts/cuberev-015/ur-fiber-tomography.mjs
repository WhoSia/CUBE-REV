/** CUBE-REV 0.15 P3C: exact 24-coordinate tracked UR edge sensor.
 * 18 Rubik face HTM actions, no human solve records or external observations.
 * Distinguishes adaptive belief-state minimax from fixed observation words.
 */
import {solvedStickerCube,applyMoveToken,toCubieState} from '../cube/sticker-cube.mjs';
import {ACTIONS} from '../cuberev-013/cross4-pdb.mjs';
export const UR_ORIENT_ZERO_MASK=0x555555, FULL_MASK=(1<<24)-1;
export function urMoveAutomaton(){
 const moves=[];
 for(const action of ACTIONS){
  const cube=solvedStickerCube();applyMoveToken(cube,action);
  const {ep,eo}=toCubieState(cube);
  const q=[];
  for(let slot=0;slot<12;slot++){
   const dest=ep.indexOf(slot);
   if(dest<0)throw Error('EDGE_PERMUTATION');
   for(let bit=0;bit<2;bit++)q[2*slot+bit]=2*dest+(bit^eo[dest]);
  }
  if(new Set(q).size!==24)throw Error('NONBIJECTIVE_EDGE_MOVE');
  moves.push(q);
 }
 return moves;
}
export function candidateMask(occupiedSlots){
 if(occupiedSlots.length!==4||new Set(occupiedSlots).size!==4||
    occupiedSlots.some(p=>!Number.isInteger(p)||p<0||p>11))throw Error('FOUR_SLOTS_REQUIRED');
 let mask=0;
 for(let p=0;p<12;p++)if(!occupiedSlots.includes(p))mask|=3<<(2*p);
 return mask;
}
export function moveBelief(mask,map){
 let next=0;
 while(mask){const bit=31-Math.clz32(mask&-mask);next|=1<<map[bit];mask&=mask-1;}
 return next;
}
function countBits(x){let n=0;while(x){n++;x&=x-1;}return n;}
export function fixedObservationClasses(word,initials,moves,sensor='orientation'){
 const states=[...initials],seen=states.map(x=>String(sensor==='orientation'?1-x%2:Number(x===0)));
 for(const token of word){
  const i=ACTIONS.indexOf(token);if(i<0)throw Error('INVALID_ACTION');
  for(let j=0;j<states.length;j++){
   states[j]=moves[i][states[j]];
   seen[j]+=String(sensor==='orientation'?1-states[j]%2:Number(states[j]===0));
  }
 }
 return new Set(seen).size;
}
export function adaptiveOrientationDepth(subset,moves,memo=new Map()){
 function win(mask,horizon){
  if(countBits(mask)<=1)return true;
  if(!horizon||countBits(mask)>2**horizon)return false;
  const key=mask+':'+horizon;
  if(memo.has(key))return memo.get(key);
  for(let a=0;a<18;a++){
   const next=moveBelief(mask,moves[a]);
   const yes=next&UR_ORIENT_ZERO_MASK,no=next&(FULL_MASK^UR_ORIENT_ZERO_MASK);
   if(Math.max(countBits(yes),countBits(no))>2**(horizon-1))continue;
   if((!yes||win(yes,horizon-1))&&(!no||win(no,horizon-1))){
    memo.set(key,true);return true;
   }
  }
  memo.set(key,false);return false;
 }
 for(let d=0;d<=10;d++)if(win(subset,d))return d;
 throw Error('NO_RECOVERY_WITHIN_TEN_MOVES');
}
export function allOccupancyFiberHistogram(moves){
 const memo=new Map(),hist={};let seen=0,maxDepth=0;
 for(let a=0;a<12;a++)for(let b=a+1;b<12;b++)
 for(let c=b+1;c<12;c++)for(let d=c+1;d<12;d++){
  const mask=candidateMask([a,b,c,d]);
  const depth=Math.max(
   adaptiveOrientationDepth(mask&UR_ORIENT_ZERO_MASK,moves,memo),
   adaptiveOrientationDepth(mask&(FULL_MASK^UR_ORIENT_ZERO_MASK),moves,memo));
  hist[depth]=(hist[depth]||0)+1;maxDepth=Math.max(maxDepth,depth);seen++;
 }
 if(seen!==495)throw Error('FIBER_SHAPE_COUNT');
 return {slotFamilies:seen,profile:hist,maxDepth,memoSize:memo.size};
}
