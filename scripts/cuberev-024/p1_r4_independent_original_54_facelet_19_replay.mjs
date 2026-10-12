// Independent pre-existing Node original 54-sticker cube mechanics verify the
// new C++ source-anchored 19-HTM solution of Seoul Summer 2026 Final 333 A1.
// Does NOT assert God's-optimal full-18HTM distance 19. Proven upper bound only.
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {solvedStickerCube,applyMoveToken,toCubieState,cubieSolved} from '../cube/sticker-cube.mjs';
import {ACTIONS} from '../cuberev-013/cross4-pdb.mjs';
const officialSource="R' B' F2 D2 F2 L2 R2 U' F2 L2 D2 B2 D F L' R2 B U2 F2 R2";
const originalFull20BoundaryWord="F2 R B U2 B' L F' U2 F U' L2 B B2 R' D2 L R' U2 L2 U2";
const newSolution19="F2 R B U2 B' L F' U2 F U' L2 B' R' D2 L R' U2 L2 U2";
const toks=s=>s.trim().split(/\s+/);
function apply(original,word){
 const s=solvedStickerCube();
 for(const token of [...toks(original),...toks(word)]){
  assert(ACTIONS.includes(token),'must be an original legal HTM move: '+token);
  applyMoveToken(s,token);
 }
 return s;
}
const initial=solvedStickerCube();
for(const token of toks(officialSource))applyMoveToken(initial,token);
const raw=apply(officialSource,originalFull20BoundaryWord);
const normalized=apply(officialSource,newSolution19);
const answer=toCubieState(normalized),rawAnswer=toCubieState(raw);
assert.equal(toks(officialSource).length,20);
assert.equal(toks(originalFull20BoundaryWord).length,20);
assert.equal(toks(newSolution19).length,19);
assert.deepEqual(answer,rawAnswer,'B B2 and B prime must be exactly the same real physical group action');
assert(cubieSolved(answer));
assert(cubieSolved(rawAnswer));
const compare=a=>a.map(x=>[x.p,x.n,x.c].join('|')).sort();
assert.deepEqual(compare(normalized),compare(solvedStickerCube()),
 'strict 54 original sticker locations/orientations, not a 2x2/cross/phase surrogate');
for(let i=1,seq=toks(newSolution19);i<seq.length;i++)
 assert.notEqual(seq[i-1][0],seq[i][0],'global HTM result has no mergeable adjacent face turns');
const inv=toks(officialSource).reverse().map(x=>x.endsWith('2')?x:x.endsWith("'")?x[0]:x+"'");
assert.equal(inv.length,20);
assert(cubieSolved(toCubieState(apply(officialSource,inv.join(' ')))));
console.log(JSON.stringify({
 marker:'CUBE_REV_024_P1_R4_OFFICIAL_WCA_FINAL_SOURCE_GLOBAL_18HTM_UPPER_BOUND_19',
 original_public_source:'https://www.worldcubeassociation.org/competitions/SeoulSummer2026/scrambles',
 published_competition:'Seoul Summer 2026',
 round:'3x3 Final Group A Scramble 1',
 full_source_scramble:officialSource,
 original_inverse_upper_bound:20,
 new_constructive_valid_upper_bound:19,
 raw_two_phase_program_length:20,
 exact_subgroup_boundary_group_product:'B B2 = B\\u0027',
 independently_original_54_facelet_replayed_and_solved:true,
 newly_proved_statement:'d18(source) <= 19',
 NOT_PROVED:'d18(source) = 19 or no 18-move solution exists',
 source_sha256:createHash('sha256').update(officialSource).digest('hex'),
 verified_word_sha256:createHash('sha256').update(newSolution19).digest('hex'),
 verified_solution_word:newSolution19
},null,2));
