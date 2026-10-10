/**
 * CUBE-REV 0.23 P0: source-grade, actual full-sticker physical reconstruction and strict human-trace limits.
 * This is exact finite physical search, not a reconstruction of human thought.
 * Assumption: fixed physical DR axis, DR-preserving 10-face-turn alphabet,
 * then exact HTR Cayley BFS. Query only 4 non-HTR quarter turns in last layer.
 */
import assert from 'node:assert/strict';
import fs from 'node:fs';
import crypto from 'node:crypto';
import {solvedStickerCube, applyMoveToken, toCubieState, solvedUpToRotation} from '../cube/sticker-cube.mjs';
import {ACTIONS} from '../cuberev-013/cross4-pdb.mjs';

const ledger=JSON.parse(fs.readFileSync('data/cuberev-022/p7_fmc_source_anchored_candidate_ledger.json','utf8'));
assert.equal(ledger.schema,'cuberev-022-p7-fmc-authored-physical-candidate-ledger-v1');
const tokenize=s=>{const a=s.trim().split(/\s+/).filter(Boolean);assert(a.every(t=>ACTIONS.includes(t)));return a;};
const stickerAfter=word=>{const x=solvedStickerCube();for(const t of word)applyMoveToken(x,t);return x;};
const cubieAfter=w=>toCubieState(stickerAfter(w));
const key=s=>s.cp.join(',')+'/'+s.co.join(',')+'/'+s.ep.join(',')+'/'+s.eo.join(',');
const enc=s=>String.fromCharCode(...s.cp.map(x=>65+x),...s.ep.map(x=>65+x));
const solved=cubieAfter([]);
const FACE=Object.fromEntries(ACTIONS.map(t=>[t,cubieAfter([t])]));
const compose=(s,m)=>({
 cp:m.cp.map(i=>s.cp[i]),
 co:m.co.map((x,i)=>(s.co[m.cp[i]]+x)%3),
 ep:m.ep.map(i=>s.ep[i]),
 eo:m.eo.map((x,i)=>s.eo[m.ep[i]]^x)
});
const normal={'0,1,0':'U','1,0,0':'R','0,0,1':'F','0,-1,0':'D','-1,0,0':'L','0,0,-1':'B'};
const ROT={UD:null,FB:'x',LR:'z'};
function frameMap(rot) {
 if(!rot)return {original_to_frame:Object.fromEntries('URFDLB'.split('').map(x=>[x,x])),frame_to_original:Object.fromEntries('URFDLB'.split('').map(x=>[x,x]))};
 const c=stickerAfter([rot]), oldToFrame={};
 for(const s of c)if(s.p.every((v,i)=>v===s.n[i])) oldToFrame[s.c]=normal[s.n.join(',')];
 assert.equal(Object.keys(oldToFrame).length,6);
 return {original_to_frame:oldToFrame,frame_to_original:Object.fromEntries(Object.entries(oldToFrame).map(([k,v])=>[v,k]))};
}
const MAP=Object.fromEntries(Object.keys(ROT).map(a=>[a,frameMap(ROT[a])]));
function phaseState(originalStickers,axis) {
 const rot=ROT[axis];assert(Object.hasOwn(ROT,axis));
 if(!rot)return toCubieState(originalStickers);
 const x=originalStickers.map(s=>({p:[...s.p],n:[...s.n],c:s.c}));
 applyMoveToken(x,rot);for(const s of x)s.c=MAP[axis].original_to_frame[s.c];
 return toCubieState(x);
}
const eo=s=>s.eo.every(v=>v===0);
const dr=s=>eo(s)&&s.co.every(v=>v===0)&&s.ep.slice(8).every(v=>v>=8);
const HALF='U2 R2 F2 D2 L2 B2'.split(' ');
const DR='U U2 U\u0027 D D2 D\u0027 R2 L2 F2 B2'.split(' ');
assert.equal(DR.length,10);
for(const t of DR)assert(dr(compose(solved,FACE[t])));
for(const a of Object.keys(ROT))assert.equal(key(phaseState(stickerAfter([]),a)),key(solved));
for(const a of Object.keys(ROT))for(const t of ACTIONS){
 const f=MAP[a].original_to_frame[t[0]]+t.slice(1);
 assert.equal(key(phaseState(stickerAfter([t]),a)),key(FACE[f]),'axis conjugacy check '+a+'/'+t);
}


const C=JSON.parse(fs.readFileSync('data/cuberev-023/p0_source_evidence_contract.json','utf8'));
const F=JSON.parse(fs.readFileSync('data/cuberev-022/p8_r3_source_anchored_phase2_exact_witness_fixtures.json','utf8'));
assert.equal(C.schema,'cuberev-023-p0-source-evidence-contract-v1');
assert.equal(C.original_scramble,ledger.normal_scramble);
assert.deepEqual(C.candidate_words.map(x=>x.id),ledger.eo_dr_pairs.map(x=>x.id));
assert.equal(C.sources.length,2);
for(const x of C.sources){
 assert(x.wca_id&&x.url.endsWith('/'+x.wca_id));
 assert(x.line_span&&x.author);
}
const scramble=tokenize(C.original_scramble),witnesses=[],physicalMap=new Map(),drMap=new Map();
for(let i=0;i<C.candidate_words.length;i++){
 const l=ledger.eo_dr_pairs[i],record=C.candidate_words[i];
 assert.equal(record.id,l.id);assert.equal(record.author,l.author);
 assert.equal(record.eo_prefix,l.eo_prefix);assert.equal(record.dr_extension,l.dr_extension);
 const authored=[...tokenize(record.eo_prefix),...tokenize(record.dr_extension)];
 assert.equal(authored.length,record.literal_total_HTM);
 const originalSticker=stickerAfter([...scramble,...authored]);
 const originalCubie=toCubieState(originalSticker),fullKey=key(originalCubie);
 const axes=Object.keys(ROT).filter(a=>dr(phaseState(originalSticker,a)));
 assert.equal(axes.length,record.fixed_axis_that_physically_replays_as_DR===null?0:1);
 if(axes.length)assert.deepEqual(axes,[record.fixed_axis_that_physically_replays_as_DR]);
 if(!physicalMap.has(fullKey))physicalMap.set(fullKey,[]);
 physicalMap.get(fullKey).push(record.id);
 let stageGroupHash=null;
 if(axes.length){
  const phys=phaseState(originalSticker,axes[0]);
  const pr=F.rows.find(x=>x.id===record.id);
  assert(pr&&pr.axis===axes[0]);
  assert.equal(pr.exact_minimum_DR_to_solved,record.post_prefix_exact_all18_HTM);
  assert.equal(record.raw_source_stage_plus_optimal_all18_HTM,authored.length+pr.exact_minimum_DR_to_solved);
  const solution=tokenize(pr.actual_phase2_word);
  assert.equal(solution.length,record.post_prefix_exact_all18_HTM);
  assert(solvedUpToRotation(stickerAfter([...scramble,...authored,...solution])),'Physical source-prefix-specific complete solve differs');
  stageGroupHash=crypto.createHash('sha256').update(key(phys)).digest('hex');
  if(!drMap.has(stageGroupHash))drMap.set(stageGroupHash,[]);
  drMap.get(stageGroupHash).push(record.id);
 }else{
  assert.equal(record.id,'riabov_other_2');
  assert.equal(record.warning,'HOLD_SOURCE_SIDE_OR_CONCATENATION_CONTEXT_NOT_AUTHOR_ERROR');
  assert.equal(record.post_prefix_exact_all18_HTM,null);
 }
 witnesses.push({
  id:record.id,source_grade:C.source_grades.authored,
  authored_word:authored.join(' '),
  declared_grammar:record.grammar_authority,
  human_source_line_span:record.source_lines,
  observed_original_full_cube_SHA256:crypto.createHash('sha256').update(fullKey).digest('hex'),
  DR_verified_axis:axes[0]||null,
  phase_full_cubie_SHA256:stageGroupHash,
  source_specific_complete_solution_replayed:axes.length>0,
  historical_human_choice_evaluation_NOT_OBSERVED:true
 });
}
assert.equal(witnesses.length,6);
assert.equal(physicalMap.size,5);
assert.equal(drMap.size,4);
assert.equal(witnesses.filter(x=>x.DR_verified_axis!==null).length,5);
const alias=[...drMap.values()].find(x=>x.length===2);
assert.deepEqual(alias,['miao_main','riabov_main']);
const pairOriginal=C.candidate_words.filter(x=>['miao_main','miao_alternative_from_same_eo'].includes(x.id));
assert.equal(pairOriginal.length,2);
assert.equal(pairOriginal[0].eo_prefix,pairOriginal[1].eo_prefix);
assert.equal(pairOriginal[0].author,pairOriginal[1].author);
assert.equal(pairOriginal[0].raw_source_stage_plus_optimal_all18_HTM,19);
assert.equal(pairOriginal[1].raw_source_stage_plus_optimal_all18_HTM,23);
assert.notEqual(witnesses.find(x=>x.id===pairOriginal[0].id).observed_original_full_cube_SHA256,witnesses.find(x=>x.id===pairOriginal[1].id).observed_original_full_cube_SHA256);
// Independent physical commute negative control and explicitly non-identical words.
const f2b=key(toCubieState(stickerAfter(['F2','B']))),bf2=key(toCubieState(stickerAfter(['B','F2'])));
assert.equal(f2b,bf2);
const humanFinal=tokenize(ledger.submitted_final_19);
assert.equal(humanFinal.length,19);
assert(solvedUpToRotation(stickerAfter([...scramble,...humanFinal])));
const report={
 marker:'CUBE_REV_023_P0_ACTIVATED_SOURCE_EVIDENCE_ORIGINAL_FULL_CUBE',
 activation:'USER_AUTHORIZED_2026_10_11',
 version:'0.23',
 physical_input_authentic_3x3_54_stickers:true,
 independent_source_author_pages:C.sources.map(x=>({author:x.author,wca_id:x.wca_id,url:x.url,attempt:x.attempt,verified_line_span:x.line_span})),
 exact_human_written_word_count:witnesses.length,
 original_full_cubie_distinct_endpoint_count:physicalMap.size,
 DR_valid_source_word_count:witnesses.filter(x=>x.DR_verified_axis).length,
 DR_valid_distinct_phase_endpoints:drMap.size,
 independent_author_alias_record_pair:alias,
 human_submitted_19_move_original_scramble_solved:true,
 physical_F2_B_commutes_negative_control:true,
 source_ambiguous_riabov_other2_status:'PARSE_HOLD_NOT_AUTHOR_ERROR',
 relative_main_vs_alt_same_human_written_eo:true,
 relative_main_vs_alt_physically_different_DR:true,
 relative_main_vs_alt_raw_source_prefix_all18_costs:[19,23],
 P8_R6_synthetic_neighborhood_has_no_human_observation:true,
 human_process_causal_identification:'NOT_IDENTIFIED',
 counters:witnesses,
 all_readonly_CI_original_source_and_physical_negative_controls_PASS:true
};
console.log(JSON.stringify(report,null,2));
