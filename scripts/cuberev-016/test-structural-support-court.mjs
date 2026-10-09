import assert from 'node:assert/strict';
import {urMoveAutomaton} from '../cuberev-015/ur-fiber-tomography.mjs';
import {exactH4SupportStructure,FOUR_TURN_36_WORDS,fourTurnRankFormula} from './structural-support-court.mjs';
const r=exactH4SupportStructure(urMoveAutomaton());
assert.equal(r.totalSupports,4095);
assert.equal(r.sourcePartitionTypes,1913);
assert.equal(r.countVectorClasses,124);
assert.equal(r.categoryValueContradictions,0);
assert.equal(r.closedFormContradictions,0);
assert.equal(r.strictFeedbackSupports,1331);
assert.equal(r.minimalAntichainCount,216);
assert.equal(r.allMinimalSetsHaveSize6,true);
assert.equal(r.upwardClosureCount,1331);
assert.equal(r.upwardClosureMismatches,0);
assert.equal(r.combinatorialCount,1331);
assert.deepEqual(r.winnersBySize,
 {'6':216,'7':432,'8':396,'9':208,'10':66,'11':12,'12':1});
assert.deepEqual(r.faceClasses,{F:[1,5,8,9],B:[3,7,10,11],other:[0,2,4,6]});
assert.equal(r.minimalMasks[0],175);
console.log('CUBE_REV_016_INTERNAL_P4_EXACT_216_ANTICHAIN_124_CLASS_IFF_PASS');

// Independent P5 SMALL BASIS court: replay only 36 literal words, no full 18^4 search.
const actions=[...'URFDLB'].flatMap(f=>[f,f+"'",f+'2']);
const moveMaps=urMoveAutomaton();
assert.equal(FOUR_TURN_36_WORDS.length,36);
const partitions=FOUR_TURN_36_WORDS.map(w=>{
 const a=w.split(' ').map(t=>actions.indexOf(t));
 assert.equal(a.length,4);assert.ok(a.every(j=>j>=0));
 const groups=new Uint16Array(16);
 for(let p=0;p<12;p++){
  let x=2*p,v=0;
  for(let t=0;t<4;t++){x=moveMaps[a[t]][x];v|=(x&1)<<t;}
  groups[v]|=1<<p;
 }
 return groups;
});
const F=new Set([1,5,8,9]),B=new Set([3,7,10,11]);
const fiveBases=[[0,2,3],[2,0,3],[1,2,2],[2,1,2],[2,2,1]];
const expected={3:220,4:492,5:480},covered={3:0,4:0,5:0};
function choose(k,lo,mask){
 if(!k){
  let counts=[0,0,0];for(let p=0;p<12;p++)if(mask&(1<<p))counts[F.has(p)?0:B.has(p)?1:2]++;
  const n=counts.reduce((a,b)=>a+b,0);
  const admitted=n===3||(n===4&&counts.filter(Boolean).length>=2)||
   (n===5&&fiveBases.some(b=>b.every((v,i)=>counts[i]>=v)));
  if(!admitted)return;
  assert.ok(partitions.some(part=>part.reduce((acc,g)=>acc+Number(Boolean(mask&g)),0)===n),
   '36-word basis certificate missing '+mask);
  covered[n]++;return;
 }
 for(let p=lo;p<=12-k;p++)choose(k-1,p+1,mask|(1<<p));
}
for(const k of [3,4,5])choose(k,0,0);
assert.deepEqual(covered,expected);
assert.deepEqual(fourTurnRankFormula([2,2,2]),{fixed:5,adaptive:6});
assert.deepEqual(fourTurnRankFormula([1,1,3]),{fixed:4,adaptive:4});
assert.deepEqual(fourTurnRankFormula([2,1,3]),{fixed:5,adaptive:5});
assert.deepEqual(fourTurnRankFormula([4,4,0]),{fixed:4,adaptive:4});
assert.throws(()=>fourTurnRankFormula([0,0,0]));
// Concrete non-submodular marginal: Q={0,2,3,4}, add F slots1 and5.
const fixedRanks=[fourTurnRankFormula([0,1,3]).fixed,
 fourTurnRankFormula([1,1,3]).fixed,fourTurnRankFormula([2,1,3]).fixed];
assert.deepEqual(fixedRanks,[4,4,5]);
console.log('CUBE_REV_016_P5_COMPACT_36_WORD_1192_BASIS_PASS');
