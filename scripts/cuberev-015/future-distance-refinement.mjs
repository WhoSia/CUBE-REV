/** 0.15 — Exact full future-distance congruence on 190080 D-cross states.
 * All state and action data are mathematical; no human reconstructions.
 * The k-step observational partition refines by ALL 18 named action successors.
 */
import {solvedStickerCube,applyMoveToken,toCubieState} from '../cube/sticker-cube.mjs';
import {ACTIONS,buildCrossPDB} from '../cuberev-013/cross4-pdb.mjs';

const N=190080,R=11880,A=18;
function rank(p){
 const pool=Array.from({length:12},(_,i)=>i);let v=0;
 for(let k=0;k<4;k++){
  const j=pool.indexOf(p[k]);if(j<0)throw Error('DUPLICATE_EDGE');
  v=v*(12-k)+j;pool.splice(j,1);
 }return v;
}
function unrank(v){
 const ds=[];for(const r of [9,10,11,12]){ds.push(v%r);v=Math.floor(v/r);}
 if(v!==0)throw Error('INVALID_RANK');
 const pool=Array.from({length:12},(_,i)=>i);
 return ds.reverse().map(j=>pool.splice(j,1)[0]);
}
export function exactCrossTransitions(){
 const maps=ACTIONS.map(a=>{
  const cube=solvedStickerCube();applyMoveToken(cube,a);
  const {ep,eo}=toCubieState(cube),inverse=new Array(12);
  ep.forEach((src,dest)=>inverse[src]=dest);
  return {inverse,eo};
 });
 const rankMove=new Uint16Array(R*A),flips=new Uint8Array(R*A);
 for(let r=0;r<R;r++){
  const p=unrank(r);
  if(rank(p)!==r)throw Error('RANK_ROUNDTRIP');
  for(let a=0;a<A;a++){
   const m=maps[a],np=p.map(k=>m.inverse[k]),off=r*A+a;
   rankMove[off]=rank(np);
   flips[off]=np.reduce((sum,d,k)=>sum|(m.eo[d]<<k),0);
  }
 }
 const next=(s,a)=>{const off=(s>>>4)*A+a;return(rankMove[off]<<4)|((s&15)^flips[off]);};
 return {next,rankMove,flips};
}
export function exhaustiveFutureDistanceRefinement(){
 const pdb=buildCrossPDB('D');
 if(pdb.sha256!=='916a33eec009cf7c46216616dd73261bb5f420173e0dbd7d2505df47883749b2')
  throw Error('PDB_IMMUTABILITY_FAILURE');
 const d=pdb.distances,{next}=exactCrossTransitions();
 let inverses=0,triangles=0;
 for(let s=0;s<N;s++)for(let a=0;a<A;a++){
  const t=next(s,a),inv=Math.floor(a/3)*3+([1,0,2][a%3]);
  if(next(t,inv)!==s)throw Error('NONINVERTIBLE_TRANSITION');
  if(Math.abs(d[t]-d[s])>1)throw Error('DISTANCE_NOT_LIPSCHITZ');
  inverses++;triangles++;
 }
 let ids=Uint32Array.from(d);
 const rounds=[];
 for(let k=0;k<=8;k++){
  const counts=new Map();for(const id of ids)counts.set(id,(counts.get(id)||0)+1);
  let largest=0,singles=0;
  for(const n of counts.values()){largest=Math.max(largest,n);if(n===1)singles++;}
  rounds.push({k,classes:counts.size,largest_class:largest,singleton_classes:singles});
  if(counts.size===N)break;
  const table=new Map(),nextIds=new Uint32Array(N);
  for(let s=0;s<N;s++){
   const sig=[ids[s]];for(let a=0;a<A;a++)sig.push(ids[next(s,a)]);
   const key=sig.join(',');
   let j=table.get(key);
   if(j===undefined){j=table.size;table.set(key,j);}
   nextIds[s]=j;
  }
  ids=nextIds;
 }
 if(rounds.at(-1)?.classes!==N)throw Error('CONGRUENCE_NOT_DISCRETE');
 return {state_count:N,action_count:A,pdb_sha256:pdb.sha256,
   transition_inverse_checks:inverses,triangle_checks:triangles,
   minimal_counterfactual_horizon:rounds.at(-1).k,partition_rounds:rounds};
}
