/** CUBE-REV 0.14 — Synthetic finite goal/action observation channel.
 * Pure math: NOT cryptographic security, human neural measurements, or source records.
 * Fixed full 18-move grammar and six center-color cross goals.
 */
import {ACTIONS} from '../cuberev-013/cross4-pdb.mjs';
export const GOALS=['U','D','R','L','F','B'];
function logSumExp(v){
 const m=Math.max(...v);return m+Math.log(v.reduce((s,x)=>s+Math.exp(x-m),0));
}
export function actionChannel(deltaByGoal,beta){
 if(!Number.isFinite(beta)||beta<0)throw Error('BAD_BETA');
 return GOALS.map(f=>{
  const d=deltaByGoal[f];
  if(!Array.isArray(d)||d.length!==18||!d.every(x=>Number.isFinite(x)&&Math.abs(x)<=1))
   throw Error('BAD_EXACT_DELTA');
  const v=d.map(x=>-beta*x),z=logSumExp(v);
  const p=v.map(x=>Math.exp(x-z));
  if(Math.abs(p.reduce((a,b)=>a+b,0)-1)>1e-12)throw Error('CHANNEL_NORM');
  return p;
 });
}
export const OBSERVATIONS={
 full:token=>token,face:token=>token[0],power:token=>token.slice(1)
};
export function informationBits(channel,observable=OBSERVATIONS.full){
 if(!Array.isArray(channel)||channel.length!==6||channel.some(q=>q.length!==18))
  throw Error('SIX_BY_EIGHTEEN_REQUIRED');
 const classes=[...new Set(ACTIONS.map(observable))],groups=classes.map(t=>ACTIONS.map((a,i)=>observable(a)===t?i:-1).filter(i=>i>=0));
 const mass=channel.map(q=>groups.map(ids=>ids.reduce((s,i)=>s+q[i],0)));
 for(const q of mass)if(q.some(v=>!Number.isFinite(v)||v<0)||Math.abs(q.reduce((a,b)=>a+b,0)-1)>1e-10)throw Error('CHANNEL_NORM');
 const marginal=groups.map((_,j)=>mass.reduce((s,q)=>s+q[j]/6,0));
 let information=0;
 for(const q of mass)for(let k=0;k<q.length;k++)if(q[k]>0)information+=q[k]/6*Math.log2(q[k]/marginal[k]);
 if(information<-1e-11||information>Math.log2(6)+1e-11)throw Error('INFORMATION_BOUNDS');
 return Math.max(0,information);
}
export function observationLeakage(deltaByGoal,beta){
 const q=actionChannel(deltaByGoal,beta);
 const full=informationBits(q,OBSERVATIONS.full),face=informationBits(q,OBSERVATIONS.face),
       power=informationBits(q,OBSERVATIONS.power);
 if(face>full+1e-10||power>full+1e-10)throw Error('DATA_PROCESSING_VIOLATION');
 return {full,face,power,faceLoss:full-face,powerLoss:full-power};
}
