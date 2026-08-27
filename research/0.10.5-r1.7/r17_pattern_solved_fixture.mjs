import fs from 'node:fs';
import crypto from 'node:crypto';
import { cube3x3x3 } from 'cubing/puzzles';
const kp=await cube3x3x3.kpuzzle();
function stable(x){if(Array.isArray(x))return '['+x.map(stable).join(',')+']';if(x&&typeof x==='object')return '{'+Object.keys(x).sort().map(k=>JSON.stringify(k)+':'+stable(x[k])).join(',')+'}';return JSON.stringify(x)}
function h(t){return crypto.createHash('sha256').update(stable(t.transformationData)).digest('hex')}
const q=[kp.identityTransformation()],seen=new Set(),ori=[];while(q.length){const t=q.shift(),z=h(t);if(seen.has(z))continue;seen.add(z);ori.push(t);for(const m of ['x','y','z'])q.push(t.applyMove(m));}
const oh=new Set(ori.map(h));
const fixtures=[
 {name:'reco_12564_teodor',source:'reco.nz 12564 alg.cubing reconstruction',setup:"L B R2 B' R2 U2 F D R2 U R2 F2 D2 R U B L2",alg:`x' // inspection
r' U F U' r U' r' U2 r' U r // xxxcross
R U2' R2' U' R U R U2' R' // 4th pair
U' F' r U R' U' r' F R // ZBLL`},
 {name:'reco_11919_ryan',source:'reco.nz 11919 no-rotation reconstruction',setup:"D2 F2 R F2 L F2 R' B2 L2 U' L2 R2 B2 D L R B' R2 B2",alg:`B' U L2' // cross
R' U' R // 1st pair
D L' U' L D' // 2nd pair
U' L' U L // 3rd pair
U R U' R' // 4th pair
U2' r U R' U R U2' r2' F' r U' r' F2 r // 1LLL`},
 {name:'cubing_docs_setup_example',source:'js.cubing.net cubing/twisty setup-alg documentation example',setup:"F U2 L2 B2 F' U L2 U R2 D2 L' B L2 B' R2 U2",alg:`y x' // inspection
U R2 U' F' L F' U' L' // XX-Cross + EO
U' R U R' // 3rd slot
R' U R U2' R' U R // 4th slot
U R' U' R U' R' U2 R // OLL / ZBLL
U // AUF`}
];
const results=[];
for(const f of fixtures){
 let rec={name:f.name,source:f.source};
 try{
   const S=kp.algToTransformation(f.setup),T=kp.algToTransformation(f.alg),endT=S.applyTransformation(T);
   const endP=kp.defaultPattern().applyAlg(f.setup).applyAlg(f.alg);
   rec={...rec,parse:true,transformation_exact_identity:endT.isIdentityTransformation(),orientation_hash_solved:oh.has(h(endT)),
        kpattern_solved_ignore_orientation_and_center:endP.experimentalIsSolved({ignorePuzzleOrientation:true,ignoreCenterOrientation:true}),
        kpattern_solved_ignore_orientation_only:endP.experimentalIsSolved({ignorePuzzleOrientation:true,ignoreCenterOrientation:false}),residual_hash:h(endT)};
 }catch(e){rec={...rec,parse:false,error:String(e?.stack||e)}}
 results.push(rec);
}
const discrepancy=results.filter(r=>r.kpattern_solved_ignore_orientation_and_center!==r.orientation_hash_solved).length;
const out={schema_version:'CR0105R17-KPATTERN-SOLVED-FIXTURE-1',status:'PASS_DIAGNOSTIC',cubing_version:'0.63.3',orientation_hash_group_size:ori.length,results,predicate_discrepancy_count:discrepancy,
 decision:discrepancy?'REPLACE_HANDROLLED_ORIENTATION_HASH_WITH_KPATTERN_SOLVED':'HANDROLLED_PREDICATE_NOT_EXONERATED',human_observations:0};
fs.mkdirSync('research/0.10.5-r1.7/evidence-pattern-solved',{recursive:true});fs.writeFileSync('research/0.10.5-r1.7/evidence-pattern-solved/KPATTERN_SOLVED_FIXTURE.json',JSON.stringify(out,null,2)+'\n');console.log(JSON.stringify(out,null,2));
