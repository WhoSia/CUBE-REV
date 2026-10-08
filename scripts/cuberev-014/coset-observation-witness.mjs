/** CUBE-REV 0.14 P5: coset-fiber counterexample, public cube mathematics only.
 * Kociemba G1 includes U; both e and U are in the same Phase-1 identity fiber.
 * This does NOT claim human cognitive or cryptographic security results.
 */
import {solvedStickerCube,applyMoveToken,toCubieState} from '../cube/sticker-cube.mjs';
import {ACTIONS,FACE_EDGE_IDS,indexOfFourEdges,buildCrossPDB} from '../cuberev-013/cross4-pdb.mjs';
import {GOALS,actionChannel,observationLeakage} from './finite-observation-channel.mjs';
export function sixCrossTables(){
 return Object.fromEntries(GOALS.map(f=>[f,buildCrossPDB(f)]));
}
export function exactGoalActionDelta(cube,tables){
 const state=toCubieState(cube),delta={};
 for(const f of GOALS){
  const idx=x=>indexOfFourEdges(x.ep,x.eo,FACE_EDGE_IDS[f]);
  const d=tables[f].distances;
  const base=d[idx(state)];
  delta[f]=ACTIONS.map(a=>{
   const child=cube.map(s=>({p:[...s.p],n:[...s.n],c:s.c}));
   applyMoveToken(child,a);
   const v=d[idx(toCubieState(child))]-base;
   if(!Number.isInteger(v)||Math.abs(v)>1)throw Error('PDB_ACTION_DELTA_INVARIANT');
   return v;
  });
 }
 return delta;
}
export function cosetObservationWitness(tables,beta=2){
 const e=solvedStickerCube(),u=solvedStickerCube();applyMoveToken(u,'U');
 const c0=toCubieState(e),c1=toCubieState(u);
 for(const c of [c0,c1]){
  if(c.co.some(x=>x!==0)||c.eo.some(x=>x!==0)||
     new Set(c.ep.slice(8,12)).size!==4||
     !c.ep.slice(8,12).every(x=>[8,9,10,11].includes(x)))
    throw Error('KOCIEMBA_G1_MEMBERSHIP');
 }
 const d0=exactGoalActionDelta(e,tables),d1=exactGoalActionDelta(u,tables);
 const q0=actionChannel(d0,beta),q1=actionChannel(d1,beta);
 const i=GOALS.indexOf('U'),j=ACTIONS.indexOf("U'");
 return {
  phase1_fiber:'G1',state_0:'e',state_1:'U',
  delta_U_Up:[d0.U[j],d1.U[j]],
  probability_U_Up:[q0[i][j],q1[i][j]],
  full_channel_equal:q0.every((row,k)=>row.every((x,j)=>Math.abs(x-q1[k][j])<=1e-12)),
  leakage_e:observationLeakage(d0,beta),
  leakage_U:observationLeakage(d1,beta),
  exact_pdb_sha:Object.fromEntries(GOALS.map(f=>[f,tables[f].sha256]))
 };
}
