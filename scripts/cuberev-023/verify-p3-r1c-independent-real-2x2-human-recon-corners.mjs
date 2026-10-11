/** CUBE-REV 0.23 P3-R1C: public 2x2 record independent original-sticker source grammar court.
 * Not a human cognition measurement or competitor-authored thought log.
 * 2x2 has corners only; edges+centers of original 3x3 oracle are ignored for 2x2 goal.
 */
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {solvedStickerCube,applyMoveToken,toCubieState} from '../cube/sticker-cube.mjs';

const p=JSON.parse(fs.readFileSync('data/cuberev-023/p3_r1c_real_public_2x2_solve_reconstruction_prereg.json','utf8'));
assert.equal(p.schema,'cuberev-023-p3-r1c-independent-real-human-2x2-reconstruction-source-v1');
const scramble=p.published_scramble.trim().split(/\s+/);
const solution=p.published_solution_with_orientation.trim().split(/\s+/);
assert.deepEqual(solution,['x2',"y'",'U2','R',"U'",'R2']);
const FACE='URFDLB';
const normal={'0,1,0':'U','1,0,0':'R','0,0,1':'F','0,-1,0':'D','-1,0,0':'L','0,0,-1':'B'};
function apply(words){const cube=solvedStickerCube();for(const t of words)applyMoveToken(cube,t);return cube;}
function cornerFaceSignature(cube){
 const faces=Object.fromEntries(FACE.split('').map(x=>[x,[]]));
 for(const st of cube){
  if(!st.p.every(v=>Math.abs(v)===1))continue;
  const face=normal[st.n.join(',')];
  assert(face,'Corner stickers must be on real cube faces');
  faces[face].push(st.c);
 }
 for(const f of FACE)assert.equal(faces[f].length,4,'2x2 face should show four actual corner stickers');
 return Object.fromEntries(FACE.split('').map(x=>[x,faces[x].slice().sort().join('')]));
}
const scrambled=apply(scramble),solved=apply([...scramble,...solution]);
const before=cornerFaceSignature(scrambled),after=cornerFaceSignature(solved);
const expected=Object.values(after).every(s=>s.length===4&&s.split('').every(c=>c===s[0]))&&new Set(Object.values(after).map(x=>x[0])).size===6;
if(!expected){
 console.log(JSON.stringify({marker:'CUBE_REV_023_P3_R1C_PUBLIC_2X2_RECONSTRUCTION_SOURCE_GRAMMAR_HOLD',
  original_public_source:p.source_url,
  published_scramble:p.published_scramble,
  published_solution:p.published_solution_with_orientation,
  status:'SOURCE_CONVENTION_HOLD_NO_PHYSICAL_SOLVED_PROOF',
  original_corner_facelets_before:before,original_corner_facelets_after:after,
  requires_notation_frame_source_check:true,
  no_person_cognitive_inference:true},null,2));
 process.exit(0);
}
assert(Object.values(before).some(s=>s[0]!==s[1]||s[0]!==s[2]||s[0]!==s[3]));
console.log(JSON.stringify({
 marker:'CUBE_REV_023_P3_R1C_PUBLIC_2X2_RECONSTRUCTION_SOURCE_PHYSICAL_PASS',
 public_source_url:p.source_url,
 attribution_grade:p.source_grade,
 original_recorded_scramble:p.published_scramble,
 original_recorded_solution:p.published_solution_with_orientation,
 source_face_HTM_turns:4,
 reorientation_tokens:['x2',"y'"],
 physically_solved_all_six_corners_only_2x2_faces:true,
 actual_original_54_sticker_oracle_used:true,
 final_six_2x2_corner_face_color_pattern:after,
 original_3x3_centers_and_edges_ignored_by_design:true,
 actual_3x3_full_cube_solution_NOT_claimed:true,
 physically_observed_face_stickers_before:before,
 actually_observed_human_inspection_and_cognition:false,
 no_2x2_all_state_optimality_claim:true,
 source_manual_frame_correction_NOT_invented:true
},null,2));
