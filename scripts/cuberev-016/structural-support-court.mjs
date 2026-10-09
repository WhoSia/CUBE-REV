/** CUBE-REV 0.16 internal P4: exact support-incidence law at horizon four.
 * The triple of occupancy COUNTS, not merely occupied-category flags, preserves
 * the optimum VALUE of both feedback and predetermined-action controllers.
 * All 4095 source-subset policy values come from the exact h4 finite court.
 * This is not a recursively sufficient belief state or human cognitive model.
 */
import {exactH4AllBeliefs} from './horizon-feedback-court.mjs';
const F=new Set([1,5,8,9]),B=new Set([3,7,10,11]),OTHER=new Set([0,2,4,6]);
function popcnt(x){let n=0;while(x){x&=x-1;n++;}return n;}
export function exactH4SupportStructure(moves){
 const census=exactH4AllBeliefs(moves);
 if(census.allPolicyValues.length!==4095)throw Error('INCOMPLETE_H4_COURT');
 const valueClasses=new Map(),winMasks=new Set();
 let categoryValueContradictions=0,closedFormContradictions=0;
 const winnersBySize={};
 for(const row of census.allPolicyValues){
  const counts=[0,0,0];
  for(let p=0;p<12;p++)if(row.mask&(1<<p))
   counts[F.has(p)?0:B.has(p)?1:2]++;
  const type=counts.join(',');
  const earlier=valueClasses.get(type);
  if(earlier&&(earlier[0]!==row.adaptive||earlier[1]!==row.fixed))
   categoryValueContradictions++;
  if(!earlier)valueClasses.set(type,[row.adaptive,row.fixed]);
  const expected=counts.every(v=>v>=2),observed=row.adaptive>row.fixed;
  if(expected!==observed)closedFormContradictions++;
  if(observed){
   winMasks.add(row.mask);
   const size=popcnt(row.mask);
   winnersBySize[size]=(winnersBySize[size]||0)+1;
  }
 }
 const minimal=[];
 for(const mask of winMasks){
  let ok=true;
  for(let p=0;p<12;p++)if(mask&(1<<p)){
   if(winMasks.has(mask^(1<<p))){ok=false;break;}
  }
  if(ok)minimal.push(mask);
 }
 minimal.sort((a,b)=>a-b);
 if(minimal.some(x=>popcnt(x)!==6))throw Error('MINIMAL_SET_SHAPE_FAIL');
 let closureCount=0,closureMismatches=0;
 for(let s=1;s<4096;s++){
  const generated=minimal.some(m=>(s&m)===m);
  const direct=winMasks.has(s);
  if(generated!==direct)closureMismatches++;
  if(generated)closureCount++;
 }
 return {
  totalSupports:4095,sourcePartitionTypes:census.distinctFixedPartitions,
  countVectorClasses:valueClasses.size,categoryValueContradictions,
  closedFormContradictions,strictFeedbackSupports:winMasks.size,
  minimalAntichainCount:minimal.length,minimalMasks:minimal,
  allMinimalSetsHaveSize6:minimal.every(x=>popcnt(x)===6),
  upwardClosureCount:closureCount,upwardClosureMismatches:closureMismatches,
  combinatorialCount:(6+4+1)**3,winnersBySize,
  faceClasses:{F:[...F].sort((a,b)=>a-b),B:[...B].sort((a,b)=>a-b),
   other:[...OTHER].sort((a,b)=>a-b)}
 };
}
/** 0.16 internal P5: the shorter proof's STATIC construction certificate.
 * The upper bounds are proved from physical face-incidence geometry.
 * These 36 exact action words prove the lower bounds by covering ONLY
 * 220 triples, 492 admissible quadruples and 480 admissible quintuples;
 * unlike the predecessor P4 court, no 104976-word search is required.
 */
export const FOUR_TURN_36_WORDS=Object.freeze([
 "B F U F",
 "B F U2 F",
 "B F U B",
 "F' U' B F",
 "B' U' B F",
 "B F' R2 F",
 "B F R F",
 "B' R' B F",
 "B' F L B",
 "B F L' F",
 "B' F' U2 F",
 "B' F R B",
 "B' F R2 F",
 "F L B F",
 "B D' B F",
 "F D' B F",
 "B F' U F",
 "B' L' B F",
 "B F D B",
 "B F' D' F",
 "B U' B F",
 "F' R' B F",
 "F' D B F",
 "F U B F",
 "B' D B F",
 "B F R2 F",
 "B L B F",
 "B F R B",
 "U' F U F",
 "R' F' R F",
 "U' B U B",
 "D' B D B",
 "U2 F U F",
 "D F' U F",
 "D2 B U2 F",
 "L2 B' R2 F"
]);
export const FOUR_TURN_FIVE_BASES=Object.freeze([[0,2,3],[2,0,3],[1,2,2],[2,1,2],[2,2,1]]);
export function fourTurnRankFormula(counts){
 if(!Array.isArray(counts)||counts.length!==3||counts.some(v=>!Number.isInteger(v)||v<0||v>4)||counts.every(v=>v===0))throw Error('BAD_NONEMPTY_INCIDENCE_TRIPLE');
 const n=counts.reduce((x,y)=>x+y,0);
 let fixed=Math.min(n,3);
 if(n>=4&&counts.filter(v=>v>0).length>=2)fixed=4;
 if(FOUR_TURN_FIVE_BASES.some(t=>t.every((v,i)=>counts[i]>=v)))fixed=5;
 return {fixed,adaptive:fixed+Number(counts.every(v=>v>=2))};
}
