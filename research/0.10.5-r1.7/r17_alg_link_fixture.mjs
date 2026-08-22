import fs from 'node:fs';
import crypto from 'node:crypto';
import { cube3x3x3 } from 'cubing/puzzles';
const kp=await cube3x3x3.kpuzzle();
function stable(x){if(Array.isArray(x))return '['+x.map(stable).join(',')+']';if(x&&typeof x==='object')return '{'+Object.keys(x).sort().map(k=>JSON.stringify(k)+':'+stable(x[k])).join(',')+'}';return JSON.stringify(x)}
function h(t){return crypto.createHash('sha256').update(stable(t.transformationData)).digest('hex')}
const q=[kp.identityTransformation()],seen=new Set(),ori=[];
while(q.length){const t=q.shift(),z=h(t);if(seen.has(z))continue;seen.add(z);ori.push(t);for(const m of ['x','y','z'])q.push(t.applyMove(m));}
const oh=new Set(ori.map(h)); const solved=t=>oh.has(h(t));
const setup="L B R2 B' R2 U2 F D R2 U R2 F2 D2 R U B L2";
const raw=`x' // inspection
r' U F U' r U' r' U2 r' U r // xxxcross
R U2' R2' U' R U R U2' R' // 4th pair
U' F' r U R' U' r' F R // ZBLL`;
const normalized=raw.replaceAll("U2'","U2").replaceAll("R2'","R2").replace(/(^|\s)r'/g,"$1Rw'").replace(/(^|\s)r(?=\s|$)/g,"$1Rw");
const S=kp.algToTransformation(setup);
const out={schema_version:'CR0105R17-ALG-LINK-FIXTURE-1',fixture:{source:'reco.nz solve 12564 public alg.cubing.net link',setup,raw_alg:raw},orientation_group_size:ori.length,tests:{}};
for(const [name,alg] of [['raw',raw],['normalized',normalized]]){
  try{const T=kp.algToTransformation(alg);const end=S.applyTransformation(T);out.tests[name]={parse:true,solved_mod_orientation:solved(end),exact_identity:end.isIdentityTransformation(),residual_hash:h(end)};}
  catch(e){out.tests[name]={parse:false,error:String(e)}}
}
out.status=out.tests.raw?.solved_mod_orientation?'PASS_RAW_ALG_LINK':'HOLD_RAW_ALG_LINK';out.human_observations=0;
fs.mkdirSync('research/0.10.5-r1.7/evidence-alg-link-fixture',{recursive:true});
fs.writeFileSync('research/0.10.5-r1.7/evidence-alg-link-fixture/ALG_LINK_FIXTURE_COURT.json',JSON.stringify(out,null,2)+'\n');
console.log(JSON.stringify(out,null,2));
if(out.status!=='PASS_RAW_ALG_LINK')process.exit(2);
