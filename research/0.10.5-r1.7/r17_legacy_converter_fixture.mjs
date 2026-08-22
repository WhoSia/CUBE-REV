import fs from 'node:fs';
import crypto from 'node:crypto';
import { createRequire } from 'node:module';
import * as cubingAlg from 'cubing/alg';
import { cube3x3x3 } from 'cubing/puzzles';

const require=createRequire(import.meta.url);
const legacy=require('/tmp/r17legacy/alg.js');
const kp=await cube3x3x3.kpuzzle();
function stable(x){if(Array.isArray(x))return '['+x.map(stable).join(',')+']';if(x&&typeof x==='object')return '{'+Object.keys(x).sort().map(k=>JSON.stringify(k)+':'+stable(x[k])).join(',')+'}';return JSON.stringify(x)}
function h(t){return crypto.createHash('sha256').update(stable(t.transformationData)).digest('hex')}
const q=[kp.identityTransformation()],seen=new Set(),ori=[];
while(q.length){const t=q.shift(),z=h(t);if(seen.has(z))continue;seen.add(z);ori.push(t);for(const m of ['x','y','z'])q.push(t.applyMove(m));}
const oh=new Set(ori.map(h));const solved=t=>oh.has(h(t));
const setup="L B R2 B' R2 U2 F D R2 U R2 F2 D2 R U B L2";
const raw=`x' // inspection
r' U F U' r U' r' U2 r' U r // xxxcross
R U2' R2' U' R U R U2' R' // 4th pair
U' F' r U R' U' r' F R // ZBLL`;
function convert(s){return legacy.cube.toCubingJSAlg(legacy.cube.fromString(s),{alg:cubingAlg});}
const legacySetup=convert(setup),legacyAlg=convert(raw);
const directSetup=cubingAlg.Alg.fromString(setup),directAlg=cubingAlg.Alg.fromString(raw);
const LS=kp.algToTransformation(legacySetup),LT=kp.algToTransformation(legacyAlg);
const DS=kp.algToTransformation(directSetup),DT=kp.algToTransformation(directAlg);
const out={schema_version:'CR0105R17-LEGACY-CONVERTER-FIXTURE-1',upstream_alg_cubing_commit:'c245b372f9461eda7a780f22c97a950a70b47dc7',cubing_version:'0.63.3',orientation_group_size:ori.length,
 source_fixture:'reco.nz solve 12564 alg.cubing.net reconstruction link',
 converted:{legacy_setup:String(legacySetup),legacy_alg:String(legacyAlg),direct_setup:String(directSetup),direct_alg:String(directAlg)},
 comparison:{setup_transform_equal:LS.isIdentical(DS),alg_transform_equal:LT.isIdentical(DT),legacy_setup_hash:h(LS),direct_setup_hash:h(DS),legacy_alg_hash:h(LT),direct_alg_hash:h(DT)},
 endpoints:{legacy:{solved_mod_orientation:solved(LS.applyTransformation(LT)),residual_hash:h(LS.applyTransformation(LT))},direct:{solved_mod_orientation:solved(DS.applyTransformation(DT)),residual_hash:h(DS.applyTransformation(DT))}},human_observations:0};
out.status=out.endpoints.legacy.solved_mod_orientation?'PASS_LEGACY_STATE_COMPLETE':'HOLD_LEGACY_STATE_INCOMPLETE';
fs.mkdirSync('research/0.10.5-r1.7/evidence-legacy-converter',{recursive:true});fs.writeFileSync('research/0.10.5-r1.7/evidence-legacy-converter/LEGACY_CONVERTER_FIXTURE.json',JSON.stringify(out,null,2)+'\n');console.log(JSON.stringify(out,null,2));
