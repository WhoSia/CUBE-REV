/** CUBE-REV 0.21 P7 mathematical/TCS: EXACT minimal observations at optimal HTM depth.
 * Legal sticker-derived 18 Rubik moves, 12 initially zero-flip UR source slots.
 * Query = read intrinsic edge orientation bit AFTER a legal face turn; a turn may
 * be silent (no query), but still physically transports all hidden candidate states.
 * This is an idealized sensor oracle, NEVER a claim of human vision or FMC action traces.
 */
import assert from 'node:assert/strict';
import {urMoveAutomaton,UR_ORIENT_ZERO_MASK} from '../cuberev-015/ur-fiber-tomography.mjs';
import {ACTIONS} from '../cuberev-013/cross4-pdb.mjs';

const moves=urMoveAutomaton();
assert.equal(moves.length,18);
assert.equal(UR_ORIENT_ZERO_MASK,0x555555);
const all24=(1<<24)-1;
for(const p of moves) assert.deepEqual([...p].sort((a,b)=>a-b),Array.from({length:24},(_,i)=>i));
const EVEN=UR_ORIENT_ZERO_MASK,ODD=all24^EVEN;
const key=(m,h,k)=>m+','+h+','+k;
const M=new Map(),NEXT=new Map();
const bitcount=(x)=>{let n=0;while(x){n++;x&=x-1;}return n;};
let recursionVisits=0;
function moveBelief(mask,a){
 const cacheKey=mask+','+a;
 if(NEXT.has(cacheKey))return NEXT.get(cacheKey);
 let m=0;
 while(mask){
  const b=mask&-mask;const i=31-Math.clz32(b);
  m|=(1<<moves[a][i]);mask^=b;
 }
 NEXT.set(cacheKey,m);
 return m;
}
function can(mask,h,k){
 recursionVisits++;
 if(bitcount(mask)<=1)return true;
 if(h===0||k===0||(1<<Math.min(h,k))<bitcount(mask))return false;
 const keyString=key(mask,h,k);
 if(M.has(keyString))return M.get(keyString);
 for(let a=0;a<18;a++){
  const moved=moveBelief(mask,a);
  const e=moved&EVEN,o=moved&ODD;
  if(e!==0 && o!==0 && can(e,h-1,k-1) && can(o,h-1,k-1)){
   M.set(keyString,{action:a,observe:true}); return M.get(keyString);
  }
  if(h>k && can(moved,h-1,k)){
   M.set(keyString,{action:a,observe:false});return M.get(keyString);
  }
 }
 M.set(keyString,false);
 return false;
}
function witnessFor(startState){
 let mask=EVEN,state=startState,remainingH=7,remainingK=4;
 const turns=[],readBits=[];
 while(bitcount(mask)>1){
  assert(remainingH>0);
  const node=can(mask,remainingH,remainingK);
  assert(node&&typeof node==="object");
  const action=ACTIONS[node.action];
  state=moves[node.action][state];
  const next=moveBelief(mask,node.action);
  turns.push({action,observe:node.observe});
  if(node.observe){
   const bit=state&1;
   mask=next&(bit?ODD:EVEN);
   readBits.push(bit);
   remainingK--;
  } else mask=next;
  remainingH--;
  assert(mask&(1<<state),'actual piece must remain in belief');
 }
 assert.equal(bitcount(mask),1,'exact source identified');
 assert.equal(mask,1<<state,'identified final state agrees with true physical transport');
 return {initial_slot:startState/2,moves:turns.map(x=>x.action),observed_after_turns:turns.flatMap((x,i)=>x.observe?[i+1]:[]),
  queried_bits:readBits.join(''),turns:turns.length,queries:readBits.length,final_edge_state:state};
}
const initialSources=Array.from({length:12},(_,i)=>2*i);
assert.equal(bitcount(EVEN),12);
assert.equal(can(EVEN,6,6),false,'no 6 turn ideal all-query adaptive policy');
assert.equal(can(EVEN,7,3),false,'binary decision tree 3 bits < 12 sources');
assert(can(EVEN,7,4),'real seven-turn four-query law must have exact constructive witness');
const paths=initialSources.map(witnessFor);
assert.equal(new Set(paths.map(x=>x.queried_bits)).size,12);
assert(paths.every(x=>x.turns<=7&&x.queries<=4));
const timeDist=Object.fromEntries([1,2,3,4,5,6,7].map(t=>[t,paths.filter(x=>x.turns===t).length]));
const queryDist=Object.fromEntries([1,2,3,4].map(t=>[t,paths.filter(x=>x.queries===t).length]));
assert.deepEqual(queryDist,{'1':0,'2':0,'3':4,'4':8});
assert.deepEqual(timeDist,{'1':0,'2':0,'3':0,'4':0,'5':0,'6':4,'7':8});
assert.equal(paths.reduce((sum,x)=>sum+2**(-x.queries),0),1,'query code saturates Kraft equality');
const pairPrefixFree=(a,b)=>!a.startsWith(b)&&!b.startsWith(a);
for(let i=0;i<12;i++)for(let j=i+1;j<12;j++)assert(pairPrefixFree(paths[i].queried_bits,paths[j].queried_bits));
const firstMoves=new Set(paths.map(p=>p.moves[0]));
assert.deepEqual([...firstMoves],['F']);

console.log(JSON.stringify({
 marker:'CUBE_REV_021_P7_REAL_RUBIK_JOINT_TURN_QUERY_MINIMUM_PASS',
 result:'PHYSICAL_LEGAL_STICKER_REPLAY_EXACT_BRANCH_AND_INFORMATION_BOUND',
 original_geometry:'genuine Rubik sticker-derived 18 actions, UR edge unknown among 12 original zero-flip positions, intrinsic bit oracle only',
 query_protocol:'on each face turn choose to inspect the intrinsic orientation bit or omit it; action choices may depend only on prior inspected bits, known action history and turn/inspection budgets',
 optimal_worst_turn_count:7,
 optimal_worst_orientation_queries:4,
 joint_optimum_turns_queries:[7,4],
 evidence_lower_bound_turns:'EXHAUSTIVE_BELIEF_DP_6_TURNS_ALL_6_QUERIES_IMPOSSIBLE',
 evidence_lower_bound_queries:'INFORMATION_THEORETIC_AT_MOST_2^3_LEAVES_LESS_THAN_12_INITIAL_SOURCES',
 physical_sticker_automaton_bijection_validation:true,
 achieved_query_lengths:queryDist,
 achieved_move_lengths:timeDist,
 observed_code_kraft_sum:1,
 distinct_prefix_free_query_codes:true,
 all_12_initial_states_replayed:true,
 root_first_action:'F',
 cache_states:M.size,
 transition_cache_states:NEXT.size,
 recursion_visits:recursionVisits,
 witnesses:paths,
 not_claimed:'NOT physical camera human observation, NOT arbitrary full-cube FMC policy, NOT an observed cost estimate'
},null,2));
