/**
 * CUBE-REV 0.21 P2-H: deterministic ecologically grounded candidate pack.
 * No simulated human participants. Every row uses genuine 54-sticker Rubik states
 * and a camera restricted to one REAL face's nine standard colour stickers.
 */
import assert from 'node:assert/strict';
import {solvedStickerCube,applyMoveToken,toCubieState} from '../cube/sticker-cube.mjs';
import {ACTIONS} from '../cuberev-013/cross4-pdb.mjs';

const frames={
 U:{normal:[0,1,0],up:[0,0,-1],right:[1,0,0],hidden:'D'},
 D:{normal:[0,-1,0],up:[0,0,1],right:[1,0,0],hidden:'U'},
 F:{normal:[0,0,1],up:[0,1,0],right:[1,0,0],hidden:'B'},
 B:{normal:[0,0,-1],up:[0,1,0],right:[-1,0,0],hidden:'F'},
 R:{normal:[1,0,0],up:[0,1,0],right:[0,0,-1],hidden:'L'},
 L:{normal:[-1,0,0],up:[0,1,0],right:[0,0,1],hidden:'R'}
};
const dot=(p,q)=>p[0]*q[0]+p[1]*q[1]+p[2]*q[2];
const eq=(p,q)=>p.every((x,i)=>x===q[i]);
function view(cube,face){
 const v=frames[face],out=Array(9).fill(null);
 for(const s of cube)if(eq(s.n,v.normal)){
  const row=1-dot(s.p,v.up),col=1+dot(s.p,v.right);
  assert(Number.isInteger(row)&&row>=0&&row<=2);
  assert(Number.isInteger(col)&&col>=0&&col<=2);
  const ix=row*3+col;assert.equal(out[ix],null);out[ix]=s.c;
 }
 assert(out.every(x=>x&&'URFDLB'.includes(x)));
 return out.join('');
}
function cubeFor(tokens){
 const cube=solvedStickerCube();
 for(const x of tokens)applyMoveToken(cube,x);
 const {ep,eo,cp,co}=toCubieState(cube);
 assert.equal(new Set(ep).size,12);assert.equal(new Set(cp).size,8);
 assert.equal(eo.reduce((x,y)=>x+y,0)%2,0);
 assert.equal(co.reduce((x,y)=>x+y,0)%3,0);
 return cube;
}
const colors= c=>c.map(s=>s.c+':'+s.p.join(',')+':'+s.n.join(',')).join(';');
const copy= c=>c.map(s=>({p:[...s.p],n:[...s.n],c:s.c}));
const seeds=[
 [],['U','R','F2'],['R','U','F','B2'],['L2','D',"R'",'U'],
 ['F',"D'",'R2'],["U'",'F2','L','B'],['D','R2','U',"B'",'F'],
 ["R'",'F','U','D2','L'],['F2','R2','U2','D2','L2'],
 ['D2','U','R','F','L','B'],["R'","U'",'F','R2','D'],
 ['U','F2','R',"D'",'L','U2'],['U','L','F2',"D'",'B2','R'],
 ['D','B',"R'",'F2','L','U2']
];
const trials=[],stats={};let rejected=0;
for(const face of Object.keys(frames)){
 const entries=[];
 for(const seed of seeds){
  const hidden=frames[face].hidden;
  const variants=[[],[hidden],[hidden+"'"],[hidden+'2']];
  const cubes=variants.map(suffix=>cubeFor([...seed,...suffix]));
  assert.equal(new Set(cubes.map(colors)).size,4);
  const first=cubes.map(c=>view(c,face));
  assert.equal(new Set(first).size,1,'all four physically different cubes share the camera view');
  const outcomes=ACTIONS.map(action=>{
   const displayed=cubes.map(c=>{
    const next=copy(c);applyMoveToken(next,action);
    return view(next,face);
   });
   return {action,rank:new Set(displayed).size,possiblePhotos:displayed};
  });
  const most=Math.max(...outcomes.map(o=>o.rank));
  if(most!==4){rejected++;continue;}
  // This is a candidate-identification problem (which of 4 preannounced possibilities?)
  // not Rubik cube-solving, and NOT a claim that all four full cube states are known to laypeople.
  const record={
   trial_id:face+'-'+(entries.length+1),
   camera_face:face,
   blind_opposite_face:hidden,
   shared_base_scramble:seed.join(' '),
   hidden_variant_action:['none',hidden,hidden+"'",hidden+'2'],
   initial_camera_nine_sticker_colours:first[0],
   example_one_turn_perfect_diagnostic_actions:outcomes.filter(o=>o.rank===4).map(o=>o.action),
   one_step_rank_by_all_18_actions:Object.fromEntries(outcomes.map(o=>[o.action,o.rank])),
   // Only include the first six representative actions' hypothetical colours in public seed pack.
   selected_preview_actions:outcomes.filter(o=>o.rank===4).slice(0,2).map(o=>({action:o.action,possiblePhotos:o.possiblePhotos})),
   experimenter_answer_key_index:1
  };
  entries.push(record);
  if(entries.length===4)break;
 }
 if(entries.length!==4)throw new Error('insufficient six-camera fully-discriminable physically legal trials for '+face+'; found '+entries.length);
 stats[face]={selected:entries.length,one_turn_diagnostic_actions:entries.map(x=>x.example_one_turn_perfect_diagnostic_actions.length)};
 trials.push(...entries);
}
assert.equal(trials.length,24);
console.log(JSON.stringify({
 result:'CUBE_REV_021_P2H_24_REAL_STICKER_TRIALS_READY',
 status:'PHYSICAL_TRIAL_GENERATOR_VALIDATED__HUMAN_PILOT_NOT_EXECUTED',
 scope:'24 matched four-hypothesis Rubik 54-sticker camera tasks, six camera faces, with actual original 18 HTM turns',
 trial_count:24,
 all_four_hypotheses_share_nine_colour_view_before_action:true,
 all_trial_legal_full_cube_states_cubie_parities_checked:true,
 all_trials_have_at_least_one_perfect_one_turn_action:true,
 rejected_seed_candidates_without_one_turn_full_identification:rejected,
 per_camera:stats,
 design:{
  observer_objective:'correctly identify which of four known physically legal Rubik cube configurations lies behind a one-face camera',
  memory_intervention:'continuous action list always; randomize historical screenshot strip ON versus OFF',
  planning_intervention:'randomize counterfactual action previews (four hypothesis-conditioned F-face images) ON versus OFF',
  motor_and_time:'record actual next-action decision latency, UI execution time separately; remote control camera hides other faces',
  primary_endpoint:'accurate identification with fewest turns and deliberation time',
  safeguarding:'no human data have been collected; voluntary opt-in, teacher/guardian review for any school participant; do not store faces or identifying information',
  planning_caveat:'preview displays hypothetical all-candidate photographs, NEVER which hidden cube was actually selected; human cannot see hidden back faces.'
 },
 trials
},null,2));
