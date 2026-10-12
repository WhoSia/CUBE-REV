// CUBE-REV 0.24 P1-R2 — seeded heldout genuine 18HTM scramble court.
// Exact same original cube engine, same R4/H5 tables and IDA implementation;
// only admissible four-edge Cross PDB ensemble changes (U,D) vs all 6 faces.
// Run warm-cache and cold-cache timings separately. This is exploratory,
// synthetic scramble generation, not unobserved human cube solving.
import assert from 'node:assert/strict';
import {performance} from 'node:perf_hooks';
import {cubeFromWords,solveOptimal,warmAllCrossPDBs,MOVES} from './p1_r2_full18_pdb_ida_engine.mjs';
import {toCubieState,cubieSolved} from '../cube/sticker-cube.mjs';
const SEED=0xC0BE24A1;
let seed=SEED;
function nextRandom(){seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return seed>>>0}
const cases=[];
for(const depth of [6,7,8,9]){
  for(let rep=0;rep<4;rep++){
    const source=[];
    while(source.length<depth){
      const candidate=MOVES[nextRandom()%MOVES.length];
      if(source.length&&candidate[0]===source.at(-1)[0])continue;
      source.push(candidate);
    }
    cases.push({name:'synthetic_legal_HTM_'+depth+'_'+rep,
      scramble:source,source_generation:'frozen_xorshift32_0xC0BE24A1'});
  }
}
assert.equal(cases.length,16);
const memoryBefore=process.memoryUsage();
const warm=warmAllCrossPDBs();
const memoryAfter=process.memoryUsage();
let casesSolvedBoth=0,strictNodeGains=0,strictNodeLosses=0,bothHold=0;
const outcomes=[];
for(const [i,c] of cases.entries()){
  const opts={useHIncumbent:true,hIncumbentMode:'cheap_H5',
    nodeCap:140000,timeCapMs:1500,maxDepth:11};
  const b=solveOptimal(c.scramble,{...opts,useAllCrossPDBs:false});
  const d=solveOptimal(c.scramble,{...opts,useAllCrossPDBs:true});
  for(const x of [b,d]){
    if(x.word)assert(cubieSolved(toCubieState(cubeFromWords([...c.scramble,...x.word]))),
      'real original 54-sticker returned path must solve entire cube');
    if(x.result==='OPTIMAL')assert(x.bounded_optimum_certificate);
  }
  if(b.result==='OPTIMAL'&&d.result==='OPTIMAL'){
    assert.equal(b.length,d.length,'PDB ensemble changed proven exact whole-cube optimum');
    casesSolvedBoth++;
    if(d.idaNodes<b.idaNodes)strictNodeGains++;
    else if(d.idaNodes>b.idaNodes)strictNodeLosses++;
  }
  if(b.result!=='OPTIMAL'&&d.result!=='OPTIMAL')bothHold++;
  outcomes.push({id:c.name,source_legal_18HTM_word:c.scramble.join(' '),
    baseline_2_cross_pdb:{status:b.result,certified_length:b.result==='OPTIMAL'?b.length:null,
      nodes:b.idaNodes,ms:b.elapsedMs,lower:b.lower_bound},
    six_cross_pdb:{status:d.result,certified_length:d.result==='OPTIMAL'?d.length:null,
      nodes:d.idaNodes,ms:d.elapsedMs,lower:d.lower_bound},
    no_hidden_true_distance_for_uncertified_states:true});
}
console.log(JSON.stringify({
 marker:'CUBE_REV_024_P1_R2_TRUE_CUBE_SEEDED_HELDOUT_18HTM_IDA',
 frozen_source_seed:'0xC0BE24A1',cases:cases.length,
 mandatory_same_original_move_engine:true,method:'source-side deterministic xorshift32 scramble generator not human authored',
 extra_4_cross_PDB_warmup:warm,
 extra_heap_mib:(memoryAfter.heapUsed-memoryBefore.heapUsed)/1048576,
 extra_rss_mib:(memoryAfter.rss-memoryBefore.rss)/1048576,
 cases_solved_both_certified:casesSolvedBoth,
 both_bounded_hold:bothHold,
 wins_by_IDA_nodes_in_both_certified:strictNodeGains,
 losses_by_IDA_nodes_in_both_certified:strictNodeLosses,
 observations:outcomes,
 speed_cubing_human_real_behavior_inferred:false,
 rigorous_all_scramble_distribution_speedup_claim:false
},null,2));
