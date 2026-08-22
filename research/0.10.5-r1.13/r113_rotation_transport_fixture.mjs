import fs from 'node:fs';
import { buildR19Core, sha } from '../0.10.5-r1.9/r19_quotient_core.mjs';

const ROOT=process.env.R113_ROOT||'/tmp/r113'; fs.mkdirSync(ROOT,{recursive:true});
const core=await buildR19Core();
const {defaultPattern,ORIENT}=core;
const ROT=['x',"x'",'x2','y',"y'",'y2','z',"z'",'z2'];
const PROBE_ALGS=[
  "R U F2 L D B' R2 U' F L2 D'",
  "F R2 U B' L2 D R' U2 F' D2",
  "L U2 B R' D F2 U' L2 B' R"
];
const probes=PROBE_ALGS.map(a=>defaultPattern.applyAlg(a));
const sig=p=>sha(p.patternData);

function targetSignatures(g){return probes.map(p=>sig(p.applyTransformation(ORIENT[g])));}
const target=ORIENT.map((_,g)=>targetSignatures(g));
const table={}; const rows=[];
for(let g=0;g<ORIENT.length;g++){
  table[g]={};
  for(const rot of ROT){
    const matches=[];
    for(let h=0;h<ORIENT.length;h++){
      let ok=true;
      for(let pi=0;pi<probes.length;pi++){
        const a=sig(probes[pi].applyMove(rot).applyTransformation(ORIENT[h]));
        if(a!==target[g][pi]){ok=false;break;}
      }
      if(ok)matches.push(h);
    }
    table[g][rot]=matches.length===1?matches[0]:null;
    rows.push({old_gauge:g,rotation:rot,new_gauge:table[g][rot],candidate_count:matches.length,candidates:matches});
  }
}
function step(g,rot){return table[g]?.[rot];}
const identityChecks=[];
for(let g=0;g<24;g++){
  const pairs=[["x","x'"],["x'","x"],["y","y'"],["y'","y"],["z","z'"],["z'","z"]];
  for(const [a,b] of pairs){const x=step(step(g,a),b);identityChecks.push({g,a,b,result:x,ok:x===g});}
  for(const a of ['x','y','z']){let x=g;for(let i=0;i<4;i++)x=step(x,a);identityChecks.push({g,a4:a,result:x,ok:x===g});}
  for(const [a,a2] of [['x','x2'],['y','y2'],['z','z2']]){const x=step(step(g,a),a);identityChecks.push({g,double:a,a2,result:x,expected:step(g,a2),ok:x===step(g,a2)});}
}
const pureRotationPathTests=[];
const paths=[['x','y',"z'",'x2'],['z','z','y2',"x'"],["y'",'x','z2','y']];
for(let g0=0;g0<24;g0++)for(const path of paths){
  for(let pi=0;pi<probes.length;pi++){
    let p=probes[pi],g=g0;const baseline=sig(p.applyTransformation(ORIENT[g0]));
    let ok=true;
    for(const rot of path){p=p.applyMove(rot);g=step(g,rot);if(g===null||sig(p.applyTransformation(ORIENT[g]))!==baseline){ok=false;break;}}
    pureRotationPathTests.push({initial_gauge:g0,probe:pi,path,final_gauge:g,ok});
  }
}
const checks={
  orientation_group_24:ORIENT.length===24,
  mapping_rows_216:rows.length===24*9,
  every_mapping_unique:rows.every(r=>r.candidate_count===1&&Number.isInteger(r.new_gauge)),
  inverse_and_order_checks:identityChecks.every(r=>r.ok),
  pure_rotation_path_invariance:pureRotationPathTests.every(r=>r.ok),
  table_rows_are_permutations:ROT.every(rot=>new Set(rows.filter(r=>r.rotation===rot).map(r=>r.new_gauge)).size===24)
};
const pass=Object.values(checks).every(Boolean);
const out={
  schema_version:'CR0105R113-ROTATION-COVARIANT-GAUGE-FIXTURE-1',
  generation:'ROUX-MEASUREMENT-G3',
  status:pass?'PASS_ROTATION_GAUGE_ALGEBRA':'HOLD_ROTATION_GAUGE_ALGEBRA',
  cubing_version:'0.63.3',
  transport_semantics:'For pure whole-cube rotation r, G_next is the unique orientation representative such that (X apply r) apply G_next == X apply G_old on all asymmetric probes.',
  rotation_tokens:ROT,
  probe_algs:PROBE_ALGS,
  checks,
  mapping_rows:rows,
  identity_checks:identityChecks,
  pure_rotation_path_tests:pureRotationPathTests,
  transport_table:table,
  post_result_table_change:false,
  human_observations:0
};
out.semantic_sha256=sha(out);
fs.writeFileSync(`${ROOT}/ROTATION_GAUGE_TRANSPORT_FIXTURE.json`,JSON.stringify(out,null,2)+'\n');
console.log(JSON.stringify({status:out.status,checks,semantic_sha256:out.semantic_sha256},null,2));
