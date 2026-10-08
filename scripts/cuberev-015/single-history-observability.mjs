/** 0.15 — One fixed observed history is not the all-actions response oracle.
 * Exact partition refinement for ONE frozen nonadaptive 18-move word.
 */
import {exactCrossTransitions} from './future-distance-refinement.mjs';
import {buildCrossPDB} from '../cuberev-013/cross4-pdb.mjs';
const N=190080,A=18;
export function fixedWordObservation(seed=2026100901,maxSteps=100){
 const {next}=exactCrossTransitions(),d=buildCrossPDB('D').distances;
 const state=Uint32Array.from({length:N},(_,i)=>i),ids=Uint32Array.from(d);
 let rng=seed>>>0;
 const draw=()=>{rng^=rng<<13;rng^=rng>>>17;rng^=rng<<5;return rng>>>0;};
 const word=[],rounds=[{k:0,classes:9,largest_class:97254}],moves=[...'URFDLB'].flatMap(f=>[f,f+"'",f+'2']);
 let first=null;
 for(let k=1;k<=maxSteps;k++){
  const a=draw()%A;word.push(moves[a]);
  const table=new Map(),counts=[],updated=new Uint32Array(N);
  for(let i=0;i<N;i++){
   state[i]=next(state[i],a);
   const key=ids[i]*9+d[state[i]];
   let c=table.get(key);
   if(c===undefined){c=table.size;table.set(key,c);counts.push(0);}
   updated[i]=c;counts[c]++;
  }
  ids.set(updated);
  let max=0;for(const n of counts)max=Math.max(max,n);
  rounds.push({k,classes:table.size,largest_class:max});
  if(table.size===N){first=k;break;}
 }
 return {seed,word,first_injective:first,rounds};
}
export function elementaryObservationLowerBound(){
 const layerCount=[1,15,158,1394,9809,46381,97254,34966,102];
 const hardest=Math.max(...layerCount);
 let k=0,capacity=1;
 while(capacity<hardest){capacity*=3;k++;}
 return {max_initial_distance_fiber:hardest,min_observed_turns:k};
}
