/** CUBE-REV 0.16: internal P2 exact three-read active-vs-fixed census.
 * Inputs: frozen 0.15 tracked-UR 24-state action permutations.
 * Known initial flip0, all 4095 nonempty uniform subsets of 12 positions.
 * Internal bit labels use flip f; actual sensor o=1-f. Complementing every
 * read label leaves all history partitions and adaptive Bayes values unchanged.
 * Not a human perception or behavior observation.
 */
import {validateMoves} from './active-belief-geometry.mjs';
const TOTAL=4095, STATES=12, A=18;
const GROUP_F=new Set([1,5,8,9]),GROUP_B=new Set([3,7,10,11]);
export function exactThreeReadCensus(moves){
 validateMoves(moves);
 const r1=new Uint16Array(A),r2=Array.from({length:A},()=>new Uint16Array(A));
 const r3=Array.from({length:A},()=>Array.from({length:A},()=>new Uint16Array(A)));
 const partitions=new Map();
 for(let a=0;a<A;a++)for(let b=0;b<A;b++)for(let c=0;c<A;c++){
  const masks=new Uint16Array(8);
  for(let p=0;p<STATES;p++){
   const x=moves[a][2*p],y=moves[b][x],z=moves[c][y];
   const f1=x&1,f2=y&1,f3=z&1;
   r1[a]|=f1<<p;r2[a][b]|=f2<<p;r3[a][b][c]|=f3<<p;
   masks[f1+(f2<<1)+(f3<<2)]|=1<<p;
  }
  const normalized=[...masks].filter(Boolean).sort((x,y)=>x-y);
  partitions.set(normalized.join(','),normalized);
 }
 const uniquePartitions=[...partitions.values()];
 const memo2=new Uint8Array(A*4096),memo3=new Uint8Array(A*A*4096);
 const optimalThird=(subset,a,b)=>{
  if(!subset)return 0;
  const ix=(a*A+b)*4096+subset;
  if(memo3[ix])return memo3[ix];
  for(let c=0;c<A;c++){
   const m=r3[a][b][c];
   if((subset&m)&&(subset&(TOTAL^m))){memo3[ix]=2;return 2;}
  }
  memo3[ix]=1;return 1;
 };
 const optimalSecond=(subset,a)=>{
  if(!subset)return 0;
  const ix=a*4096+subset;
  if(memo2[ix])return memo2[ix];
  let best=0;
  for(let b=0;b<A;b++){
   const m=r2[a][b];
   const v=optimalThird(subset&(TOTAL^m),a,b)+optimalThird(subset&m,a,b);
   if(v>best)best=v;
   if(best===4)break;
  }
  memo2[ix]=best;return best;
 };
 const histogram=new Map(),summary=new Map(),witnesses=[];
 let summaryValueDisagreementSupports=0,maxAdvantage=0;
 for(let subset=1;subset<=TOTAL;subset++){
  let fixed=0;
  for(const masks of uniquePartitions){
   let leaves=0;for(const m of masks)leaves+=Number(Boolean(subset&m));
   if(leaves>fixed)fixed=leaves;
   if(fixed===4)break;
  }
  let adaptive=0;
  for(let a=0;a<A;a++){
   const m=r1[a];
   const v=optimalSecond(subset&(TOTAL^m),a)+optimalSecond(subset&m,a);
   if(v>adaptive)adaptive=v;
   if(adaptive===4)break;
  }
  const hkey=`${adaptive},${fixed}`;
  histogram.set(hkey,(histogram.get(hkey)||0)+1);
  if(adaptive>fixed)witnesses.push({subset,adaptive,fixed});
  maxAdvantage=Math.max(maxAdvantage,adaptive-fixed);
  let groups=0;
  for(let p=0;p<STATES;p++)if(subset&(1<<p))groups|=GROUP_F.has(p)?1:GROUP_B.has(p)?2:4;
  const classKey=`${subset.toString(2).replaceAll('0','').length}:${groups}`;
  const prev=summary.get(classKey);
  if(!prev)summary.set(classKey,{adaptive:new Set([adaptive]),fixed:new Set([fixed]),representative:[adaptive,fixed]});
  else{
   if(prev.representative[0]!==adaptive||prev.representative[1]!==fixed)summaryValueDisagreementSupports++;
   prev.adaptive.add(adaptive);prev.fixed.add(fixed);
  }
 }
 return {
  initialSupportCount:TOTAL,allFixedActionTriples:A**3,
  uniqueFixedHistoryPartitions:uniquePartitions.length,
  leafCountHistogram:Object.fromEntries([...histogram.entries()].sort()),
  strictAdaptiveWitnesses:witnesses,maxAdaptiveLeafAdvantage:maxAdvantage,
  summaryClasses:summary.size,
  summaryAdaptiveDisagreementClasses:[...summary.values()].filter(x=>x.adaptive.size>1).length,
  summaryFixedDisagreementClasses:[...summary.values()].filter(x=>x.fixed.size>1).length,
  summaryValueDisagreementSupports
 };
}
