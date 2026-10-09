/** CUBE-REV 0.16 P1 — all 4095 noiseless uniform-subset belief policies.
 * Input = frozen 0.15 24-state tracked-UR cubie transition permutations.
 * Every one of 18 first and 18 second HTM actions considered; after first
 * binary read an adaptive policy may choose different second actions.
 * Returns exact numbers of distinguishable terminal observation histories.
 * No human action/vision/mental representation is measured.
 */
import {validateMoves} from './active-belief-geometry.mjs';
const F=new Set([1,8,5,9]),B=new Set([3,10,7,11]);
const category=Array.from({length:12},(_,p)=>F.has(p)?1:B.has(p)?2:4);
export function twoStepBeliefCensus(moves){
 validateMoves(moves);
 const y1=Array.from({length:18},(_,a)=>
  Array.from({length:12},(_,p)=>moves[a][2*p]&1));
 const y2=Array.from({length:18},(_,a)=>
  Array.from({length:18},(_,b)=>
   Array.from({length:12},(_,p)=>moves[b][moves[a][2*p]]&1)));
 const summary=new Map(),valueHistogram=new Map();
 let formulaFailures=0,adaptivityWins=0,maxLeaves=0,summaryConflict=null;
 for(let support=1;support<4096;support++){
  const positions=[];let cats=0;
  for(let p=0;p<12;p++)if(support&(1<<p)){positions.push(p);cats|=category[p];}
  const size=positions.length;
  const oneBest=Math.max(...Array.from({length:18},(_,a)=>{
   let flags=0;
   for(const p of positions)flags|=1<<y1[a][p];
   return flags===3?2:1;
  }));
  if(oneBest!==(cats===1||cats===2||cats===4?1:2))formulaFailures++;
  let fixed=0,adaptive=0;
  for(let a=0;a<18;a++){
   let best0=0,best1=0;
   for(let b=0;b<18;b++){
    let mask0=0,mask1=0;
    for(const p of positions){
     if(y1[a][p])mask1|=1<<y2[a][b][p];
     else mask0|=1<<y2[a][b][p];
    }
    const leaf0=(mask0&1)+((mask0>>1)&1);
    const leaf1=(mask1&1)+((mask1>>1)&1);
    best0=Math.max(best0,leaf0);best1=Math.max(best1,leaf1);
    fixed=Math.max(fixed,leaf0+leaf1);
   }
   adaptive=Math.max(adaptive,best0+best1);
  }
  if(adaptive>fixed)adaptivityWins++;
  maxLeaves=Math.max(maxLeaves,adaptive,fixed);
  const v=`${adaptive},${fixed}`;
  valueHistogram.set(v,(valueHistogram.get(v)||0)+1);
  const c=`${size}:${cats}`,prior=summary.get(c);
  if(prior&&(prior.adaptive!==adaptive||prior.fixed!==fixed)&&!summaryConflict)
   summaryConflict={first:prior.support,second:support,key:c};
  if(!prior)summary.set(c,{support,adaptive,fixed});
 }
 return {
  totalSubsets:4095,summaryClasses:summary.size,
  supportFormulaMismatches:formulaFailures,
  adaptivityImprovementSubsets:adaptivityWins,
  noGapSubsets:4095-adaptivityWins,horizon2SummaryConflict:summaryConflict,
  maxAdaptiveLeaves:maxLeaves,
  adaptiveFixedLeafHistogram:Object.fromEntries(valueHistogram)
 };
}
