/**
 * CUBE-REV 0.22 P8: real authored DR -> HTR -> half-turn-complete bounded geometry.
 * This is exact finite physical search, not a reconstruction of human thought.
 * Assumption: fixed physical DR axis, DR-preserving 10-face-turn alphabet,
 * then exactly six physical half-turn moves. Bound D=7 applies to DR stage only.
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
const start=enc(solved);
const groupDist=new Map([[start,0]]), groupParents=new Map(), queue=[start], hist=[1];
let head=0;
while(head<queue.length) {
 const current=queue[head++],d=groupDist.get(current);
 for(const t of HALF){
  const m=FACE[t];let next='';
  for(let i=0;i<8;i++)next+=current[m.cp[i]];
  for(let i=0;i<12;i++)next+=current[8+m.ep[i]];
  if(groupDist.has(next))continue;
  groupDist.set(next,d+1);groupParents.set(next,[current,t]);queue.push(next);
  hist[d+1]=(hist[d+1]??0)+1;
  if(queue.length>663552)throw Error('HTR_SUBGROUP_OVERSHOT');
 }
}
assert.equal(groupDist.size,663552);
assert.equal(hist.length-1,15); // BFS levels are contiguous; no spread over 663552 values
assert.equal(hist.reduce((a,b)=>a+b,0),663552);
function checksum(s){return crypto.createHash('sha256').update(key(s)).digest('hex');}
function htrDistance(s){return dr(s)?groupDist.get(enc(s)):undefined;}
function exactReturnFromHTR(s){
 const path=[];let state=enc(s);
 assert(groupDist.has(state),'HTR state not in exact subgroup');
 while(state!==start){
  const parent=groupParents.get(state);
  assert(parent,'Subgroup BFS parent missing');
  path.push(parent[1]);state=parent[0];
 }
 assert.equal(path.length,groupDist.get(enc(s)),'Shortest HTR suffix does not match BFS certificate');
 let c=s;for(const t of path)c=compose(c,FACE[t]);
 assert.equal(key(c),key(solved),'Actual half-turns must solve canonical cube');
 return path;
}
const scramble=tokenize(ledger.normal_scramble), submitted=tokenize(ledger.submitted_final_19);
assert.equal(submitted.length,19);
assert(solvedUpToRotation(stickerAfter([...scramble,...submitted])));
const submittedIsLiteralPrefix=[];
const VALID_IDS=new Set(['miao_main','riabov_main','miao_alternative_from_same_eo','riabov_other_1','riabov_other_3']);
const results=[];
const DMAX=7;
for(const candidate of ledger.eo_dr_pairs){
 const prefix=[...tokenize(candidate.eo_prefix),...tokenize(candidate.dr_extension)];
 const baseStickers=stickerAfter([...scramble,...prefix]);
 const stageAxes=Object.keys(ROT).filter(a=>dr(phaseState(baseStickers,a)));
 const admitted=VALID_IDS.has(candidate.id);
 assert.equal(stageAxes.length>0,admitted);
 if(!admitted){
  results.push({id:candidate.id,source_mode:candidate.declared_mode,source_status:'NO_DR_UNDER_PROVISIONAL_PARSE',stage_axes:stageAxes,continuation:null});
  continue;
 }
 assert.equal(stageAxes.length,1,'P8 fixed stage-axis analysis needs unique verified axis');
 const axis=stageAxes[0],initial=phaseState(baseStickers,axis);
 assert(dr(initial));
 assert.equal(htrDistance(initial)!==undefined,groupDist.has(enc(initial)));
 const actualFromCanonical=t=>MAP[axis].frame_to_original[t[0]]+t.slice(1);
 let frontier=new Map([[key(initial),{s:initial,w:[]}]]);
 let firstHit=null,best=null;const layers=[];
 for(let depth=0;depth<=DMAX;depth++){
  let htrMembers=0,layerBest=null;
  for(const p of frontier.values()){
   const tail=htrDistance(p.s);
   if(tail===undefined)continue;
   htrMembers++;
   const actualSuffix=p.w.map(actualFromCanonical);
   // Verify both the phase-2 prefix and entire reconstructed solution by full stickers.
   const full=phaseState(stickerAfter([...scramble,...prefix,...actualSuffix]),axis);
   assert.equal(key(full),key(p.s),'Original physical sticker cross-check');
   const halfCanonical=exactReturnFromHTR(p.s);
   const halfActual=halfCanonical.map(actualFromCanonical);
   const fullPhysicalSolution=[...prefix,...actualSuffix,...halfActual];
   const actualSolved=stickerAfter([...scramble,...fullPhysicalSolution]);
   assert(solvedUpToRotation(actualSolved),'P8 complete witness fails real physical cube');
   assert.equal(key(phaseState(actualSolved,axis)),key(solved),'HTR return must produce exact canonical solved');
   const cost=depth+tail;
   if(!layerBest||cost<layerBest.phase2_total_moves)layerBest={
    depth_from_DR:depth,HTR_to_solved_half_turns:tail,phase2_total_moves:cost,
    canonical_DR_preserving_turns:p.w.join(' '),
    actual_face_turns:actualSuffix.join(' '),
    HTR_to_solved_actual_half_turns:halfActual.join(' '),
    complete_legal_original_face_turn_solution:fullPhysicalSolution.join(' '),
    physically_solves_original_scramble_with_original_54_sticker_oracle:true,
    HTR_endpoint_sha256:checksum(p.s)
   };
   if(firstHit===null)firstHit=depth;
   if(!best||cost<best.phase2_total_moves)best=layerBest;
  }
  layers.push({added_turns:depth,unique_full_cubie_states:frontier.size,unique_HTR_states:htrMembers,
    best_two_phase_moves_at_this_exact_depth:layerBest?.phase2_total_moves??null});
  if(depth===DMAX)break;
  const next=new Map();
  for(const p of frontier.values())for(const t of DR) {
   const s=compose(p.s,FACE[t]);
   assert(dr(s),'DR-preserving alphabet closure');
   const k=key(s);
   if(!next.has(k))next.set(k,{s,w:[...p.w,t]});
  }
  frontier=next;
 }
 const authoredIsPrefix=prefix.every((t,i)=>submitted[i]===t);
 submittedIsLiteralPrefix.push({id:candidate.id,author_prefix_length:prefix.length,
  is_literal_prefix_of_submitted_solution:authoredIsPrefix,
  first_mismatch_1based:authoredIsPrefix?null:prefix.findIndex((t,i)=>submitted[i]!==t)+1});
 const output={
  id:candidate.id,source_mode:candidate.declared_mode,axis,authored_stage_turns:prefix.length,
  DR_endpoint_sha256:checksum(initial),
  source_status:candidate.declared_mode==='CONTIGUOUS_NORMAL_SIDE_PREFIX'?'SOURCED_LINEAR_PREFIX':'CONDITIONAL_ON_CONTIGUOUS_NORMAL_SIDE',
  first_exact_DR_to_HTR_minimum_within_bound:firstHit,
  exact_minimum_DR_to_HTR_proved:firstHit!==null,
  layers,best_two_phase_continuation_with_DR_depth_at_most_7:best,
  candidate_total_prefix_plus_bounded_two_phase_best:best?prefix.length+best.phase2_total_moves:null,
  no_claim_of_unrestricted_solution_optimality:true
 };
 results.push(output);
}
const valid=results.filter(x=>x.axis);
assert.equal(valid.length,5);
const aliases=new Map();for(const x of valid){
 if(!aliases.has(x.DR_endpoint_sha256))aliases.set(x.DR_endpoint_sha256,[]);
 aliases.get(x.DR_endpoint_sha256).push(x.id);
}
assert.equal(aliases.size,4);
const a=results.find(x=>x.id==='miao_main'),b=results.find(x=>x.id==='riabov_main');
assert.deepEqual(a.layers,b.layers);
assert.equal(a.DR_endpoint_sha256,b.DR_endpoint_sha256);
assert.equal(a.best_two_phase_continuation_with_DR_depth_at_most_7?.phase2_total_moves,
  b.best_two_phase_continuation_with_DR_depth_at_most_7?.phase2_total_moves);
assert.equal(submittedIsLiteralPrefix.find(x=>x.id==='miao_main').first_mismatch_1based,10);
assert.equal(submittedIsLiteralPrefix.find(x=>x.id==='miao_main').is_literal_prefix_of_submitted_solution,false);
const result={
 marker:'CUBE_REV_022_P8_BOUNDED_SOURCE_RELATIVE_DR_HTR_CONTINUATION_PHYSICAL_CENSUS',
 physical_model:'Original 3x3 full 54-sticker cubie transformations and real 18 legal HTM outer turns',
 provenance:'Human-authored retrospectively published FMC World 2026 attempt1 candidate ledger; Riabov Other parse hypotheses explicitly conditional',
 study_assumption:'Keep the verified DR axis fixed; only 10 genuine DR-preserving HTM turns until first HTR; thereafter six half-turn generators to solved',
 DR_preserving_canonical_actions:DR,
 phase2_pre_HTR_budget_HTM:DMAX,
 HTR_subgroup_exact_order:groupDist.size,
 HTR_square_generator_Cayley_diameter:15,
 HTR_depth_histogram:hist,
 candidates:results,
 physically_distinct_DR_endpoints:[...aliases].map(([hash,members])=>({DR_endpoint_sha256:hash,members})),
 authored_stage_words_are_NOT_a_literal_prefix_of_final_solution:submittedIsLiteralPrefix,
 provided_final_19_solved:true,
 counting_rule:'Candidate strings, unique physical states, phase group membership and human reported candidate operations are noninterchangeable',
 human_process_not_observed:true,
 exact_minimum_is_ONLY_FOR_FIXED_AXIS_DR_PRESERVING_GRAMMAR:true,
 above_budget_continuations_UNEXPLORED:true,
 psychological_mechanism_NOT_IDENTIFIED:true,
 video_VFMC_new_recruitment_HOLD:true,
 stage_version:'CUBE-REV 0.22 P8, without promoting 0.23 or altering prior proofs'
};
console.log(JSON.stringify(result,null,2));
