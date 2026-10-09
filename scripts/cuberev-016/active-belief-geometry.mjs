/** CUBE-REV 0.16-P0: exact ideal-UR orientation channel / active belief geometry.
 * Pure finite mathematics. Supply the sticker-derived 24-state automaton from
 * 0.15 urMoveAutomaton(); human perception and real sensor rates are NOT tested.
 */
export const ACTIONS_016=Object.freeze([..."URFDLB"].flatMap(f=>[f,f+"'",f+"2"]));
export const bit=x=>Number((x&1)===0);
export function validateMoves(moves){
 if(!Array.isArray(moves)||moves.length!==18)throw Error('EIGHTEEN_MOVES_REQUIRED');
 for(const m of moves){
  if(!Array.isArray(m)||m.length!==24||new Set(m).size!==24||
     m.some(x=>!Number.isInteger(x)||x<0||x>=24))throw Error('NONBIJECTIVE_MAP');
 }
 for(let i=0;i<6;i++){
  const m=moves[3*i],inv=moves[3*i+1],half=moves[3*i+2];
  for(let x=0;x<24;x++){
   if(inv[m[x]]!==x||m[inv[x]]!==x||half[half[x]]!==x||m[m[x]]!==half[x])throw Error('GROUP_ACTION_INVERSE');
  }
 }
 return true;
}
function classify(keys){
 const ids=new Map(),out=[];
 for(const key of keys){if(!ids.has(key))ids.set(key,ids.size);out.push(ids.get(key));}
 return out;
}
/** Equivalent if every counterfactual action/read response of horizon k agrees.
 * Does NOT assert a single realized length-k trajectory identifies the state.
 */
export function futureObservationRefinement(moves){
 validateMoves(moves);
 let current=classify(Array.from({length:24},(_,x)=>String(bit(x))));
 const levels=[{horizon:0,classes:new Set(current).size,blocks:current.slice()}];
 for(let k=1;k<=24;k++){
  const next=classify(Array.from({length:24},(_,x)=>
   `${bit(x)}|${moves.map(m=>current[m[x]]).join(',')}`));
  const size=new Set(next).size;
  levels.push({horizon:k,classes:size,blocks:next.slice()});
  const stable=Array.from({length:24},(_,x)=>x).every(x=>
   Array.from({length:24},(_,y)=>y).every(y=>
    (current[x]===current[y])===(next[x]===next[y])));
  if(stable)return {levels,stableAt:k,terminalBlocks:next};
  current=next;
 }
 throw Error('PARTITION_NONTERMINATING');
}
export function pairBeliefCourt(moves,epsilon=0){
 validateMoves(moves);
 if(epsilon<0||epsilon>=0.5)throw Error('EPS_RANGE');
 const hist={distinguishable:0,indistinguishable:0},pairs=[];
 for(let p=0;p<12;p++)for(let q=p+1;q<12;q++){
  const choices=[];
  for(let a=0;a<18;a++)if(bit(moves[a][2*p])!==bit(moves[a][2*q]))choices.push(ACTIONS_016[a]);
  const separate=choices.length>0;
  hist[separate?'distinguishable':'indistinguishable']++;
  pairs.push({p,q,choices,oneReadValue:separate?1-epsilon:0.5});
 }
 if(pairs.length!==66)throw Error('PAIR_COUNT');
 return {hist,pairs};
}
export function oneReadBayesValue(prior,moves,a,epsilon=0){
 validateMoves(moves);
 if(prior.length!==24||prior.some(w=>w<0||!Number.isFinite(w))||
    Math.abs(prior.reduce((x,y)=>x+y,0)-1)>1e-12||epsilon<0||epsilon>0.5)
  throw Error('BAD_PRIOR_NOISE');
 return [0,1].reduce((sum,y)=>sum+Math.max(...prior.map((w,x)=>
  w*(bit(moves[a][x])===y?1-epsilon:epsilon))),0);
}
/** Posterior at the post-action position. No state mutation when impossible. */
export function bayesUpdate(prior,move,y,epsilon){
 if(prior.length!==24||move.length!==24||![0,1].includes(y)||epsilon<0||epsilon>0.5)throw Error('UPDATE_CONTRACT');
 const post=new Array(24).fill(0);let likelihood=0;
 for(let x=0;x<24;x++){
  const z=move[x],v=prior[x]*(bit(z)===y?1-epsilon:epsilon);
  post[z]+=v;likelihood+=v;
 }
 if(likelihood===0)return {likelihood,posterior:null};
 return {likelihood,posterior:post.map(w=>w/likelihood)};
}
export function oneBitExperiment(moves,action,epsilon=0){
 validateMoves(moves);
 if(epsilon<0||epsilon>=0.5)throw Error('EPS_RANGE');
 return Array.from({length:12},(_,p)=>{
  const z=bit(moves[action][2*p]);
  return z===0?[1-epsilon,epsilon]:[epsilon,1-epsilon];
 });
}
/** Equality under channel A cannot be split by a state-independent garbling. */
export function nongarblingWitness(from,to){
 for(let p=0;p<12;p++)for(let q=p+1;q<12;q++){
  if(from[p].every((v,j)=>v===from[q][j])&&
     to[p].some((v,j)=>v!==to[q][j]))return {p,q};
 }
 return null;
}
export function exactP0Court(moves){
 const ref=futureObservationRefinement(moves),pairs=pairBeliefCourt(moves);
 const F=oneBitExperiment(moves,ACTIONS_016.indexOf('F'));
 const B=oneBitExperiment(moves,ACTIONS_016.indexOf('B'));
 const U=oneBitExperiment(moves,ACTIONS_016.indexOf('U'));
 const prior=Array.from({length:24},(_,x)=>x%2===0?1/12:0);
 return {
  name:'CUBE_REV_016_P0',numStates:24,numActions:18,
  partitionHorizonCounts:ref.levels.map(x=>x.classes),
  stableAt:ref.stableAt,terminalClasses:new Set(ref.terminalBlocks).size,
  pairCount:66,pairOutcomes:pairs.hist,
  equalEntropyPairBad:[0,2],equalEntropyPairGood:[1,3],
  sameEntropyBits:1,priorMode:0.5,
  valueBad:pairs.pairs.find(x=>x.p===0&&x.q===2).oneReadValue,
  valueGood:pairs.pairs.find(x=>x.p===1&&x.q===3).oneReadValue,
  blackwellFnotFromB:nongarblingWitness(B,F),
  blackwellBnotFromF:nongarblingWitness(F,B),
  uConstantOnKnownFlip0:U.every(row=>row.join()===U[0].join()),
  uniformPriorOneReadNoNoise:{
   F:oneReadBayesValue(prior,moves,ACTIONS_016.indexOf('F')),
   U:oneReadBayesValue(prior,moves,ACTIONS_016.indexOf('U'))
  }
 };
}
