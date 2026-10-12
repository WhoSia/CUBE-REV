// Independent source-sticker certification for a real WCA Final A1 full 18HTM
// machine-discovered legal word. Distinct actual Node cubie/facelet engine from
// the C++17 source-side Conway NISS two-premove search.
// Certifies only d18(source)<=18; NO claim d18(source)=18.
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {solvedStickerCube,applyMoveToken,toCubieState,cubieSolved} from '../cube/sticker-cube.mjs';
import {ACTIONS} from '../cuberev-013/cross4-pdb.mjs';

const official="R' B' F2 D2 F2 L2 R2 U' F2 L2 D2 B2 D F L' R2 B U2 F2 R2";
const premove="F R2";
const phase1="F U F D' R' F' L' F' D' L B";
const phase2="L2 F2 U2 L2 U F2";
const raw19=phase1+" "+phase2+" "+premove;
const normalized18="F U F D' R' F' L' F' D' L B L2 F2 U2 L2 U F' R2";
const t=x=>x.trim().split(/\s+/);
const physical=word=>{
 const c=solvedStickerCube();
 for(const m of t(word)){
  assert(ACTIONS.includes(m),"original legal whole 3x3 18HTM action: "+m);
  applyMoveToken(c,m);
 }
 return c;
};
const positions=c=>c.map(s=>JSON.stringify({p:s.p,n:s.n,c:s.c})).sort();
const goal=solvedStickerCube();
assert.equal(t(official).length,20);
assert.equal(t(phase1).length,11);
assert.equal(t(phase2).length,6);
assert.equal(t(premove).length,2);
assert.equal(t(raw19).length,19);
assert.equal(t(normalized18).length,18);
// Dual-side identity: q*s*x=e is equivalent to s*x*q=e in the ACTUAL
// original physical move group, not a loose inverse-side text convention.
const inverseSide=physical(premove+" "+official+" "+phase1+" "+phase2);
const originalRaw=physical(official+" "+raw19);
const originalReduced=physical(official+" "+normalized18);
const goalCubies=toCubieState(goal);
for(const [name,state] of [
 ["dual_side_q_s_x",inverseSide],["original_source_raw19",originalRaw],
 ["original_source_normalized18",originalReduced]]){
 assert(cubieSolved(toCubieState(state)),name+" must solve ALL 8 corners and 12 edges");
 assert.deepEqual(toCubieState(state),goalCubies,name+" must exactly match source fixed reference");
 assert.deepEqual(positions(state),positions(goal),name+" must restore all original 54 physical stickers");
}
assert.deepEqual(toCubieState(originalRaw),toCubieState(originalReduced));
const x=t(raw19),boundary=t(phase1+" "+phase2);
assert.equal(x[boundary.length-1],"F2");
assert.equal(x[boundary.length],"F");
assert.equal(x[boundary.length+1],"R2");
assert.deepEqual(t(normalized18),[...boundary.slice(0,-1),"F'","R2"],
 "genuine F2*F = F-prime subgroup vs NISS suffix group-product discount");
console.log(JSON.stringify({
 marker:"CUBE_REV_024_P1_R5_OFFICIAL_REAL_3x3_18HTM_COMPLETE_ORIGINAL_FACELETS_PASS",
 source:"https://www.worldcubeassociation.org/competitions/SeoulSummer2026/scrambles",
 event:"3x3 Final Group A scramble 1",
 source_legal_18HTM_actions:20,
 original_previous_full_cube_witness_bound:19,
 new_real_fully_solving_source_upper_bound:18,
 actual_NISS_premove_word:premove,
 actual_DR_first_stage_actions:11,
 actual_DR_10_move_grammar_second_stage_actions:6,
 raw_source_side_word_actions:19,
 group_boundary:"F2 F = F'",
 legal_original_solution:normalized18,
 original_whole_54_facelets_strict_replay:true,
 inverse_side_group_identity_original_stickers:true,
 full_global_18HTM_minimum_NOT_PROVED:true,
 source_literal_sha256:createHash('sha256').update(official).digest('hex'),
 complete_18_word_sha256:createHash('sha256').update(normalized18).digest('hex')
},null,2));
