// Independent original 54-sticker replay of C++17 P1-R3 physical full-cube
// witnesses; no C++ cubie/PDB routines are imported here. Existing mature
// project cubie core supplies a distinct implementation of legal face turns.
import assert from 'node:assert/strict';
import {solvedStickerCube,applyMoveToken,toCubieState,cubieSolved} from '../cube/sticker-cube.mjs';
import {ACTIONS} from '../cuberev-013/cross4-pdb.mjs';
const fmcScramble="R' U' F L2 D' L2 U' R U F' D R L' F U2 D2 F L2 F' R2 F2 D R' U' F";
const records=[
  {id:'WCA_SeoulSummer2026_333_Final_A1',reference:'https://www.worldcubeassociation.org/competitions/SeoulSummer2026/scrambles',
   input:"R' B' F2 D2 F2 L2 R2 U' F2 L2 D2 B2 D F L' R2 B U2 F2 R2",
   cpp_solution:"R L B' R2 U L F2 R D B L2 F2 U B2 U B2 U' L2 F2 D2 F2",
   axis:'UD',stage1:10,stage2:11,actual_inverse_baseline:20},
  {id:'WCA_SeoulSummer2026_333_First_A1',reference:'https://www.worldcubeassociation.org/competitions/SeoulSummer2026/scrambles',
   input:"L2 F2 U F2 R2 U B2 R2 D U F L U F' R2 B R' D B'",
   cpp_solution:"B D' R B' R2 F U' L' F' U' D' R2 B2 U' R2 F2 U' F2 L2",
   axis:'UD',stage1:9,stage2:10,actual_inverse_baseline:19}
];
const miao=fmcScramble+" L2 F' L D L2 F2 B L B2 L";
const riabov=fmcScramble+" L2 F' L D L2 B F2 L B2 L";
for(const [id,input] of [['FMC_Miao_main_authored_EO_DR',miao],['FMC_Riabov_main_authored_EO_DR',riabov]])
 records.push({id,reference:'data/cuberev-022/p7_fmc_source_anchored_candidate_ledger.json',
 input,cpp_solution:"R2 B' R2 U2 B U2 L2 F B",
 axis:'FB',stage1:0,stage2:9,actual_inverse_baseline:35});
const parts=t=>t.trim().split(/\s+/);
function after(word){let x=solvedStickerCube();for(const token of parts(word)){
  assert(ACTIONS.includes(token),'legal exact original 18 HTM token: '+token);
  applyMoveToken(x,token);
}return x;}
const solved=toCubieState(solvedStickerCube());
const goal=JSON.stringify(solved),answers=[];
for(const row of records){
 const start=after(row.input),state=toCubieState(start);
 const afterCandidate=after(row.input+' '+row.cpp_solution),result=toCubieState(afterCandidate);
 assert(cubieSolved(result),'independent original full-cubie solver replay');
 assert.equal(JSON.stringify(result),goal,'strict exact orientation-fixed 3x3 solved');
 assert.equal(parts(row.cpp_solution).length,row.stage1+row.stage2);
 assert(parts(row.input).length>=row.actual_inverse_baseline);
 answers.push({id:row.id,axis:row.axis,phase1:row.stage1,phase2:row.stage2,
   proof_type:'REAL_54_FACELET_LEGAL_COMPLETE_SOLUTION_ONLY',
   source_actions:parts(row.input).length,legal_solution_actions:parts(row.cpp_solution).length,
   inverse_scramble_ceiling:row.actual_inverse_baseline,
   strictly_better_than_inverse:parts(row.cpp_solution).length<row.actual_inverse_baseline,
   physically_solves_all_cubies:true,source_grade:'WCA_SCRAMBLE_OR_PUBLIC_WRITTEN_FMC_STAGE'});
}
assert.deepEqual(toCubieState(after(miao)),toCubieState(after(riabov)),
  'two different authored stage word spellings, one true physical state');
assert.equal(answers.filter(x=>x.strictly_better_than_inverse).length,2);
assert.equal(answers.filter(x=>!x.strictly_better_than_inverse).length,2);
console.log(JSON.stringify({marker:'CUBE_REV_024_P1_R3_INDEPENDENT_CUBIE_AND_ORIGINAL_FACELET_REPLAY_PASS',
 true_physical_source_endpoints:3,written_source_rows:4,
 stage2_is_exact_for_its_reached_DR_state_not_full18_global:true,
 novel_optimality_claim:false,rows:answers},null,2));
