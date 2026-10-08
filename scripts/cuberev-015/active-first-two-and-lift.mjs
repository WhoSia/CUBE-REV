/** CUBE-REV 0.15 P3A: exact first-two-step active distance observation.
 * Pure finite cube mathematics. No human solve records or hidden-world claims.
 * One-step/minimax-two-step COUNTS only; not an optimal full decision tree.
 */
import {exactCrossTransitions} from './future-distance-refinement.mjs';
import {buildCrossPDB,indexOfFourEdges,FACE_EDGE_IDS,ACTIONS} from '../cuberev-013/cross4-pdb.mjs';
import {solvedStickerCube,applyMoveToken,toCubieState} from '../cube/sticker-cube.mjs';
const N=190080,A=18;
export function radiusSixActiveMinimax(){
 const pdb=buildCrossPDB('D');
 if(pdb.sha256!=='916a33eec009cf7c46216616dd73261bb5f420173e0dbd7d2505df47883749b2')throw Error('PDB_HASH');
 const d=pdb.distances,{next}=exactCrossTransitions();
 const shell=[];for(let s=0;s<N;s++)if(d[s]===6)shell.push(s);
 if(shell.length!==97254)throw Error('SHELL_SIZE');
 const rows=[];
 for(let a=0;a<A;a++){
  const groups=Array.from({length:9},()=>[]);
  for(const s of shell){const t=next(s,a);groups[d[t]].push(t);}
  const firstMax=groups.reduce((v,g)=>Math.max(v,g.length),0);
  const responses=[];
  for(let y=0;y<9;y++)if(groups[y].length){
   let secondMin=N;const best=[];
   for(let b=0;b<A;b++){
    const count=new Uint32Array(9);
    for(const state of groups[y])count[d[next(state,b)]]++;
    const maximum=count.reduce((v,n)=>Math.max(v,n),0);
    if(maximum<secondMin){secondMin=maximum;best.length=0;best.push(ACTIONS[b]);}
    else if(maximum===secondMin)best.push(ACTIONS[b]);
   }
   responses.push({observed_distance:y,candidates:groups[y].length,best_second_worst:secondMin,best_second_moves:best});
  }
  rows.push({first_move:ACTIONS[a],first_counts:groups.map(g=>g.length),first_worst:firstMax,
    adaptive_two_worst:responses.reduce((v,r)=>Math.max(v,r.best_second_worst),0),responses});
 }
 const one=Math.min(...rows.map(r=>r.first_worst));
 const two=Math.min(...rows.map(r=>r.adaptive_two_worst));
 return {states:N,shell6:shell.length,first_minimax_worst:one,
  best_first_moves:rows.filter(r=>r.first_worst===one).map(r=>r.first_move),
  best_two_step_minimax_worst:two,
  best_two_first_moves:rows.filter(r=>r.adaptive_two_worst===two).map(r=>r.first_move),
  sharpened_minimum:one>3**10?12:11,previous_constructive_upper:42,rows};
}
export function dCrossPhysicalLiftObstruction(){
 const e=solvedStickerCube(),u=solvedStickerCube();applyMoveToken(u,'U');
 const a=toCubieState(e),b=toCubieState(u);
 const get=(c,f)=>indexOfFourEdges(c.ep,c.eo,FACE_EDGE_IDS[f]);
 const indexD=[get(a,'D'),get(b,'D')],indexU=[get(a,'U'),get(b,'U')];
 const pd=buildCrossPDB('D').distances,pu=buildCrossPDB('U').distances;
 const result={d_index:indexD,u_index:indexU,
   d_distances:indexD.map(i=>pd[i]),u_distances:indexU.map(i=>pu[i])};
 if(indexD[0]!==indexD[1]||result.u_distances[0]!==0||result.u_distances[1]!==1)
   throw Error('LIFT_OBSTRUCTION_NOT_VERIFIED');
 for(const turn of ACTIONS){
  const x=solvedStickerCube(),y=solvedStickerCube();
  applyMoveToken(y,'U');applyMoveToken(x,turn);applyMoveToken(y,turn);
  const p=toCubieState(x),q=toCubieState(y);
  if(get(p,'D')!==get(q,'D'))throw Error('D_PROJECTION_NOT_EQUIVARIANT');
 }
 return result;
}
