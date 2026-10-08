/** CUBE-REV 0.14: Six-face Cross-goal posterior from TWO observed face turns.
 * The caller supplies exact PDB distance changes for all 18 legal alternatives.
 * No annotations, future turns, source IDs or private records enter this module.
 */
import {ACTIONS} from '../cuberev-013/cross4-pdb.mjs';
export const GOALS=Object.freeze(['U','D','R','L','F','B']);
const logSumExp=x=>{const m=Math.max(...x);return m+Math.log(x.reduce((s,v)=>s+Math.exp(v-m),0));};
export function goalPosterior(turns,beta,prior=Object.fromEntries(GOALS.map(f=>[f,1/6]))){
 if(!Array.isArray(turns)||turns.length!==2)throw Error('TWO_TURNS_REQUIRED');
 if(!Number.isFinite(beta)||beta<0)throw Error('INVALID_BETA');
 let total=0;for(const f of GOALS){
  if(!Number.isFinite(prior[f])||prior[f]<=0)throw Error('POSITIVE_PRIOR_REQUIRED');
  total+=prior[f];
 }
 if(Math.abs(total-1)>1e-9)throw Error('PRIOR_NOT_NORMALIZED');
 const ll=GOALS.map(f=>{
  let score=Math.log(prior[f]);
  for(const turn of turns){
   if(!ACTIONS.includes(turn.observed)||!turn.deltas||!Array.isArray(turn.deltas[f])||turn.deltas[f].length!==18)
    throw Error('INCOMPLETE_ACTION_OPPORTUNITIES');
   if(!turn.deltas[f].every(x=>Number.isFinite(x)&&Number.isInteger(x)&&x>=-1&&x<=1))
    throw Error('INVALID_DISTANCE_DELTA');
   const z=turn.deltas[f].map(x=>-beta*x);
   score+=z[ACTIONS.indexOf(turn.observed)]-logSumExp(z);
  }
  return score;
 });
 const normalizer=logSumExp(ll);
 return Object.fromEntries(GOALS.map((f,i)=>[f,Math.exp(ll[i]-normalizer)]));
}
export function properGoalScores(prob,truth){
 if(!GOALS.includes(truth))throw Error('UNKNOWN_LABEL');
 if(!GOALS.every(f=>Number.isFinite(prob[f])&&prob[f]>0))throw Error('INVALID_PROB');
 if(Math.abs(GOALS.reduce((s,f)=>s+prob[f],0)-1)>1e-8)throw Error('PROB_NOT_NORMALIZED');
 return {logLoss:-Math.log(prob[truth]),brier:GOALS.reduce((s,f)=>s+(prob[f]-(f===truth?1:0))**2,0)};
}
