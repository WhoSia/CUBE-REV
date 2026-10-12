// CUBE-REV 0.24 P1-R2 — source/ecology holdout for a real-cube IDA engine.
// Real public WCA 3x3 scrambles are outcome-stage inputs, NOT move-by-move
// reconstructions of human thought. Public authored FMC prefixes are text,
// and are only physically tested under their declared source parse contract.
// No original private 451-solve rows, no re-identification, no video claims.
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {createHash} from 'node:crypto';
import {cubeFromWords,solveOptimal} from './p1_r2_full18_pdb_ida_engine.mjs';
import {toCubieState,cubieSolved} from '../cube/sticker-cube.mjs';
const ledger=JSON.parse(fs.readFileSync('data/cuberev-022/p7_fmc_source_anchored_candidate_ledger.json','utf8'));
assert.equal(ledger.schema,'cuberev-022-p7-fmc-authored-physical-candidate-ledger-v1');
const wca=[
 {id:'SeoulSummer2026_Final_A_1',event:'333',stage:'WCA_OFFICIAL_SCRAMBLE_ONLY',
  origin:'https://www.worldcubeassociation.org/competitions/SeoulSummer2026/scrambles',
  tokens:"R' B' F2 D2 F2 L2 R2 U' F2 L2 D2 B2 D F L' R2 B U2 F2 R2".split(' ')},
 {id:'SeoulSummer2026_First_A_1',event:'333',stage:'WCA_OFFICIAL_SCRAMBLE_ONLY',
  origin:'https://www.worldcubeassociation.org/competitions/SeoulSummer2026/scrambles',
  tokens:"L2 F2 U F2 R2 U B2 R2 D U F L U F' R2 B R' D B'".split(' ')}
];
const publicFmc=ledger.eo_dr_pairs.filter(x=>['miao_main','riabov_main'].includes(x.id)).map(row=>({
 id:row.id,event:'333fm',stage:'AUTHORED_DOCUMENTED_EO_PLUS_DR_PREFIX',
 origin:'data/cuberev-022/p7_fmc_source_anchored_candidate_ledger.json',
 parse:row.declared_mode,
 tokens:[...ledger.normal_scramble.split(/\s+/),...row.eo_prefix.split(/\s+/),...row.dr_extension.split(/\s+/)]
}));
assert.equal(publicFmc.length,2);
const results=[];
for(const item of [...wca,...publicFmc]){
 const physical=cubeFromWords(item.tokens),state=toCubieState(physical);
 const id=createHash('sha256').update(JSON.stringify({cp:state.cp,co:state.co,ep:state.ep,eo:state.eo})).digest('hex');
 const out=solveOptimal(item.tokens,{useHIncumbent:true,hIncumbentMode:'cheap_H5',
   nodeCap:30000,timeCapMs:500,maxDepth:11});
 if(out.word){
  const after=cubeFromWords([...item.tokens,...out.word]);
  assert(cubieSolved(toCubieState(after)),'entire original 54-sticker cube replay');
 }
 if(out.result==='OPTIMAL')assert(out.bounded_optimum_certificate,
   'never report globally optimal physical solve without completed certificate');
 assert(['OPTIMAL','HOLD','INCUMBENT_UNCERTIFIED'].includes(out.result));
 results.push({id:item.id,event:item.event,source_grade:item.stage,declared_source_parse:item.parse||null,
  origin:item.origin,original_complete_cubie_sha256:id,
  legal_source_action_tokens:item.tokens.length,
  admissible_IDA_lower_bound:out.lower_bound,
  result:out.result,reason:out.reason,complete_optimality_certificate:out.bounded_optimum_certificate,
  verified_fully_solving_18HTM_word:out.word?.join(' ')||null,
  actual_54_facelet_replay:!!out.word,
  expanded_IDA_calls:out.idaNodes,
  no_human_process_measured:true});
}
console.log(JSON.stringify({
 marker:'CUBE_REV_024_P1_R2_PUBLIC_WCA_AND_AUTHORED_FMC_SOURCE_BOUNDARY',
 cohorts:results,
 rights:'only existing public source-authored competition/FMC source; no private 451 archive',
 interpretation:'HOLD is a resource failure, not unsolvability, not observed human slow cognition',
 publication_grade:'EXPLORATORY_SOURCE_BOUNDARY_NOT_INDEPENDENT_HUMAN_REPLICATION'
},null,2));
