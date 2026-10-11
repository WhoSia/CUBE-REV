/** CUBE-REV 0.23 P3-R2A — actual public 2x2 source frame SEMANTIC FALSIFICATION.
 * Frozen author's printed strings preserved; only source-unprovided orientation
 * inserted as explicit conditional interpretation. Not evidence of human choice.
 */
import assert from 'node:assert/strict';
import fs from 'node:fs';
import crypto from 'node:crypto';
import {solvedStickerCube,applyMoveToken} from '../cube/sticker-cube.mjs';

const P=JSON.parse(fs.readFileSync('data/cuberev-023/p3_r2a_2x2_24_orientation_frame_audit_prereg.json','utf8'));
const frozen=JSON.parse(fs.readFileSync('data/cuberev-023/p3_r1c_real_public_2x2_solve_reconstruction_prereg.json','utf8'));
assert.equal(P.schema,'cuberev-023-p3-r2a-2x2-rotational-source-grammar-audit-prereg-v1');
assert.equal(P.frozen,frozen.published_scramble);
assert.equal(P.frozen_solution,frozen.published_solution_with_orientation);
const source=P.frozen.split(/\s+/),post=P.frozen_solution.split(/\s+/);
const letters='URFDLB',normal={'0,1,0':'U','1,0,0':'R','0,0,1':'F','0,-1,0':'D','-1,0,0':'L','0,0,-1':'B'};
function replay(tokens){
 const st=solvedStickerCube();
 for(const word of tokens)applyMoveToken(st,word);
 return st;
}
function cornerFaces(stickers){
 const faces=Object.fromEntries([...letters].map(x=>[x,[]]));
 for(const st of stickers){
  if(!st.p.every(v=>Math.abs(v)===1))continue;
  const face=normal[st.n.join(',')];assert(face);
  faces[face].push(st.c);
 }
 const result={};
 for(const f of letters){
  assert.equal(faces[f].length,4);
  result[f]=faces[f].slice().sort().join('');
 }
 return result;
}
function solved2x2(stickers){
 const faces=cornerFaces(stickers);
 return Object.values(faces).every(s=>s===s[0].repeat(4))&&new Set(Object.values(faces).map(x=>x[0])).size===6;
}
function orientationKey(cube){
 const byFace={};
 for(const st of cube){
  if(!st.p.every(v=>v===0||Math.abs(v)===1))throw Error("bad sticker position");
  if(st.p.filter(x=>Math.abs(x)===1).length!==1)continue;
  const f=normal[st.n.join(',')];assert(f);
  byFace[f]=st.c;
 }
 assert.equal(Object.keys(byFace).length,6);
 return [...letters].map(f=>byFace[f]).join('');
}
const rotations=[{word:[],key:orientationKey(replay([]))}];
const seen=new Set(rotations.map(x=>x.key));
for(let i=0;i<rotations.length;i++){
 for(const t of ['x','y','z']){
  const word=[...rotations[i].word,t];
  const key=orientationKey(replay(word));
  if(seen.has(key))continue;
  seen.add(key);rotations.push({word,key});
 }
}
assert.equal(rotations.length,24);
assert.equal(seen.size,24);
const initial=cornerFaces(replay(source));
const baseline=cornerFaces(replay([...source,...post]));
assert.deepEqual(baseline,{U:'DDFU',R:'BDLR',F:'BDLR',D:'BBFU',L:'FLLU',B:'FRRU'},'Never silently change previous P3-R1C source-fail fixture');
assert(!solved2x2(replay([...source,...post])));
const tests=[];
for(const rot of rotations){
 const st=replay([...source,...rot.word,...post]);
 const finished=solved2x2(st);
 tests.push({orientation_center_color_signature:rot.key,extra_frame_after_scramble:rot.word.join(' '),extra_face_reorientation_actions:rot.word.length,physically_corner_solved:finished,after_six_actual_2x2_corner_faces:cornerFaces(st)});
}
assert.equal(tests.length,24);
const eligible=tests.filter(x=>x.physically_corner_solved);
assert(!tests[0].physically_corner_solved);
for(const x of eligible)assert(x.extra_frame_after_scramble!==''&&x.extra_face_reorientation_actions>0);
const grade=eligible.length>0?'CONDITIONAL_EXTRA_FRAME_COMPATIBLE_NOT_SOURCE_VALIDATED':'SOURCE_GRAMMAR_HOLD_EVEN_24_FRAMES';
console.log(JSON.stringify({
 marker:'CUBE_REV_023_P3_R2A_24_REAL_CUBE_2X2_ROTATION_FRAME_AUDIT',
 published_source:P.reported_reconstruction,
 original_public_competition:P.official_wca,
 source_literal_scramble_untouched:P.frozen,
 source_literal_solution_untouched:P.frozen_solution,
 true_physical_distinct_cube_frame_count:rotations.length,
 exact_literal_result_reproduced_as_SOURCE_CONVENTION_HOLD:true,
 original_literal_corner_facelets_after:baseline,
 genuinely_physical_original_color_corner_facelets_before:initial,
 count_of_conditional_hidden_frame_matches:eligible.length,
 all_conditional_hidden_frame_matches:eligible,
 scientific_authority_grade:grade,
 existing_human_0_47_official_result_unchanged:true,
 source_explicitly_records_hidden_extra_frame:false,
 conditional_frame_not_claimed_competitor_actual:true,
 no_human_heuristic_or_neural_inference:true,
 all_24_original_physical_sticker_results:tests,
 source_literal_SHA256:crypto.createHash('sha256').update(P.frozen+'\n'+P.frozen_solution).digest('hex')
},null,2));
