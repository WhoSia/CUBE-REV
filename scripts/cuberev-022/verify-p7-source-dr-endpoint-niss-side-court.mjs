/** CUBE-REV 0.22 P7, actual published FMC candidate full-cubie replay + NISS law. */
import assert from 'node:assert/strict';
import fs from 'node:fs';
import crypto from 'node:crypto';
import {solvedStickerCube,applyMoveToken,toCubieState,cubieSolved,solvedUpToRotation} from '../cube/sticker-cube.mjs';
import {ACTIONS} from '../cuberev-013/cross4-pdb.mjs';
const ledger=JSON.parse(fs.readFileSync('data/cuberev-022/p7_fmc_source_anchored_candidate_ledger.json','utf8'));
assert.equal(ledger.schema,'cuberev-022-p7-fmc-authored-physical-candidate-ledger-v1');
const tok=s=>{const a=s.trim().split(/\s+/).filter(Boolean);assert(a.every(x=>ACTIONS.includes(x)),'NON_FACE_HTM:'+s);return a;};
const invToken=t=>t.endsWith("'")?t.slice(0,-1):t.endsWith('2')?t:t+"'";
const inv=w=>[...w].reverse().map(invToken);
const sticker=w=>{const x=solvedStickerCube();for(const t of w)applyMoveToken(x,t);return x;};
const cubie=w=>toCubieState(sticker(w));
const key=s=>s.cp.join(',')+'/'+s.co.join(',')+'/'+s.ep.join(',')+'/'+s.eo.join(',');
const hash=s=>crypto.createHash('sha256').update(key(s)).digest('hex');
const NORMAL={'0,1,0':'U','1,0,0':'R','0,0,1':'F','0,-1,0':'D','-1,0,0':'L','0,0,-1':'B'};
const AXES={UD:null,FB:'x',LR:'z'};
function axisCube(c,axis){
 const rot=AXES[axis];if(rot===null)return c;
 const ref=sticker([rot]),map={};
 for(const q of ref)if(q.p.every((x,i)=>x===q.n[i]))map[q.c]=NORMAL[q.n.join(',')];
 assert.equal(Object.keys(map).length,6);
 const x=c.map(q=>({p:[...q.p],n:[...q.n],c:q.c}));
 applyMoveToken(x,rot);x.forEach(q=>q.c=map[q.c]);return x;
}
const stAxis=(c,a)=>toCubieState(axisCube(c,a));
const isEO=s=>s.eo.every(x=>x===0);
const isDR=s=>isEO(s)&&s.co.every(x=>x===0)&&s.ep.slice(8).every(x=>x>=8);
const scramble=tok(ledger.normal_scramble),solution=tok(ledger.submitted_final_19);
assert.equal(solution.length,19);
assert(solvedUpToRotation(sticker([...scramble,...solution])));
const certified=ledger.eo_dr_pairs.map(c=>{
 assert(['CONTIGUOUS_NORMAL_SIDE_PREFIX','ASSUMED_CONTIGUOUS_NORMAL_SIDE_FOR_TEST_ONLY'].includes(c.declared_mode));
 const E=tok(c.eo_prefix),D=tok(c.dr_extension);
 const ec=sticker([...scramble,...E]),dc=sticker([...scramble,...E,...D]);
 return {id:c.id,author:c.author,source_lines:c.source_lines,
  declared_mode:c.declared_mode,reported_stage:c.reported_label,
  EO_length:E.length,DR_extra_length:D.length,
  EO_axes:Object.keys(AXES).filter(a=>isEO(stAxis(ec,a))),
  DR_axes:Object.keys(AXES).filter(a=>isDR(stAxis(dc,a))),
  eo_hash:hash(toCubieState(ec)),dr_hash:hash(toCubieState(dc)),
  reported_process_NOT_live_timestamps:true};
});
assert.equal(certified.length,6);
assert.equal(certified.filter(x=>x.declared_mode==='ASSUMED_CONTIGUOUS_NORMAL_SIDE_FOR_TEST_ONLY').length,3);
const byId=new Map(certified.map(c=>[c.id,c]));
const mainA=byId.get('miao_main'),mainB=byId.get('riabov_main');
assert.deepEqual(mainA.EO_axes,['FB']);assert.deepEqual(mainB.EO_axes,['FB']);
assert.deepEqual(mainA.DR_axes,['FB']);assert.deepEqual(mainB.DR_axes,['FB']);
assert.equal(mainA.eo_hash,mainB.eo_hash);
assert.equal(mainA.dr_hash,mainB.dr_hash);
assert.notEqual(ledger.eo_dr_pairs[0].dr_extension,ledger.eo_dr_pairs[1].dr_extension);
const classes=new Map();
for(const c of certified){if(!classes.has(c.dr_hash))classes.set(c.dr_hash,[]);classes.get(c.dr_hash).push(c.id);}
const endpointClasses=[...classes].map(([sha,ids])=>({full_cube_endpoint_SHA256:sha,members:ids,member_authors:[...new Set(ids.map(id=>byId.get(id).author))]}));
const sourceDRPassing=certified.filter(c=>c.DR_axes.length>0);
const invalidForStage=certified.filter(c=>c.DR_axes.length===0);
assert.equal(sourceDRPassing.length,5);
assert.equal(invalidForStage.length,1);
assert.equal(invalidForStage[0].id,'riabov_other_2');
assert.equal(classes.size,5);
const certifiedDRGroups=new Set(sourceDRPassing.map(x=>x.dr_hash));
assert.equal(certifiedDRGroups.size,4);

function niss(S,A,B){
 // Group law: N(B,A)=B^{-1} S A ; inverse-view N^{-1}=A^{-1} S^{-1} B.
 const n=cubie([...inv(B),...S,...A]);
 const i=cubie([...inv(A),...inv(S),...B]);
 assert.equal(key(i),key(cubie(inv([...inv(B),...S,...A]))));
 return {normal:n,inverse:i};
}
function runNISS(S,operationEvents){
 const A=[],B=[],sample=[];
 for(const e of operationEvents){
  assert(['NORMAL','INVERSE'].includes(e.side)&&ACTIONS.includes(e.move));
  const old=niss(S,A,B);
  if(e.side==='NORMAL')A.push(e.move);else B.push(e.move);
  const now=niss(S,A,B);
  const expected=e.side==='NORMAL'?
     cubie([...inv(B),...S,...A]):
     cubie([...inv(B),...S,...A]);
  assert.equal(key(now.normal),key(expected));
  sample.push({side:e.side,move:e.move,normal_endpoint_sha256:hash(now.normal),
    inverse_endpoint_sha256:hash(now.inverse),
    not_an_observed_human_time:true});
 }
 return {A,B,final:niss(S,A,B),sample};
}
const cut=9;
const ops=[
 ...solution.slice(0,cut).map(move=>({side:'NORMAL',move})),
 ...inv(solution.slice(cut)).map(move=>({side:'INVERSE',move}))
];
const nissExample=runNISS(scramble,ops);
assert(cubieSolved(nissExample.final.normal));
assert(cubieSolved(nissExample.final.inverse));
assert.deepEqual([...nissExample.A,...inv(nissExample.B)],solution);
const typed=ledger.niss_authored_inverse_segment;
const S2=tok(typed.scramble);
const A2=[...tok(typed.normal_EO_prefix),...tok(typed.normal_JZP)];
const B2=tok(typed.inverse_side_alt_DR_after_JZP);
const typedN=niss(S2,A2,B2);
const wrong=cubie([...S2,...A2,...B2]);
assert.notEqual(key(typedN.normal),key(wrong));
assert.equal(ledger.deliberately_unparsed.length,3);
const allEoHashes=new Set(certified.map(x=>x.eo_hash));
const report={
 marker:'CUBE_REV_022_P7_SOURCE_REAL_DR_ENDPOINT_ALIAS_AND_TYPED_NISS_PASS',
 exact_genuine_scramble_plus_19_HTM_solution:true,
 six_source_authored_normal_side_pairs:certified,
 source_typed_DR_membership_PASS:sourceDRPassing.map(x=>x.id),
 source_typed_DR_membership_NOT_CONFIRMED:invalidForStage.map(x=>x.id),
 same_physical_DR_endpoint_classes:endpointClasses,
 distinct_full_cube_DR_endpoints:classes.size,
 distinct_source_backed_DR_certified_endpoints:certifiedDRGroups.size,
 concatenation_assumptions_for_ria_other_candidates_are_explicit:true,
 unmatched_source_case:{
   id:'riabov_other_2',
   physical_EO_axes_under_chosen_concatenation:byId.get('riabov_other_2').EO_axes,
   physical_DR_axes_under_chosen_concatenation:byId.get('riabov_other_2').DR_axes,
   reason:'Source presents alternative as Other; direct consecutive normal-side transcription fails all three axis checks. Could require distinct side/context or different syntax; NO author-error claim.',
   status:'SOURCE_CONTEXT_SEMANTICS_HOLD'
 },
 different_EO_prefix_physical_state_count:allEoHashes.size,
 matched_authored_main_DR_commutation_collision:{
  author1:'Qijun Miao',author2:'Yurii Riabov',
  real_source_miao_DR:ledger.eo_dr_pairs[0].dr_extension,
  real_source_riabov_DR:ledger.eo_dr_pairs[1].dr_extension,
  identity:'F2 and B commute as opposite face turns, both author reconstructions map same EO and same DR physical endpoints',
  same_actual_scramble:true,same_staged_eo:true,same_staged_full_cubie_DR:true,
  different_literal_DR_turn_words:true,
  no_proof_of_two_different_human_internal_candidate_discoveries:true
 },
 NISS:{
  algebra:'N(B,A)=inverse(B) S A; inverse_view=inverse(A) inverse(S) B',
  normal_ops_right_multiply_and_inverse_ops_left_inverse_multiply:true,
  source_complete_19_move_word_retro_refactorization:{
    normal_side_moves_A:nissExample.A.join(' '),
    inverse_side_moves_B:nissExample.B.join(' '),
    chosen_normal_cut:cut,
    source_final_normal_solution_recovered_exactly:true,
    final_cube_physically_solved_from_both_sides:true,
    not_a_claim_the_author_ever_switched_sides_at_this_cut:true
  },
  sourced_Miao_A2_parenthesized_inverse_alternative:{
    source_url:typed.source_url,source_lines:typed.source_lines,
    normal_prefix:typed.normal_EO_prefix+' '+typed.normal_JZP,
    inverse_side_word:typed.inverse_side_alt_DR_after_JZP,
    correct_partial_state_sha256:hash(typedN.normal),
    naively_appended_word_state_sha256:hash(wrong),
    different_physical_states:true,
    precise_which_side_was_actually_checked_not_identified:true
  },
  authored_mixed_insertion_lines_left_UNPARSED:ledger.deliberately_unparsed
 },
 procedural_constraints:{
  same_physical_endpoint_not_equal_literal_word:true,
  same_physical_endpoint_not_equal_source_event:true,
  complete_search_chronology_not_observed:true,
  all_human_considered_choices_not_recovered:true,
  software_computed_candidates_not_labeled_as_human_actions:true,
  no_video_VFMC_or_new_recruitment:true
 }
};
console.log(JSON.stringify(report,null,2));
