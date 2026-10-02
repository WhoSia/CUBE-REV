import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import {spawnSync} from "node:child_process";
const d=fs.mkdtempSync(path.join(os.tmpdir(),"g7-p4-geom-"));
const exact={solve_count:1,exact_end_validation_pass:1,total_prefixes:2,authority:"EXACT_EXTENDED_REPLAY_PASS",records:[{
 source_id:1,reconstructor:"R",method_family:"CFOP",
 prefixes:[
  {kind:"FACE_TURN",boundary_after:true,annotation_after:"cross"},
  {kind:"ROTATION",boundary_after:false,annotation_after:null}
 ]
}]};
fs.writeFileSync(path.join(d,"e.json"),JSON.stringify(exact));
fs.writeFileSync(path.join(d,"f.tsv"),[
 "source_id\tprefix_index\tq_rank\tlb\tts_lb\tfs_lb\tis_g1\tboundary_after\tobs_next_action\th1_regret\th2_regret\th3_regret\thorizon_optimal_count\th1_opt_count\th2_opt_count\th3_opt_count",
 "1\t0\t1\t3\t3\t2\t0\t0\t0\t0\t0\t1\t2\t1\t2\t3",
 "1\t1\t2\t2\t2\t1\t0\t1\t-1\t-1\t-1\t-1\t0\t2\t3\t4",
 "1\t2\t0\t0\t0\t0\t1\t0\t-1\t-1\t-1\t-1\t0\t10\t10\t10"
].join("\n")+"\n");
const p=spawnSync(process.execPath,["scripts/g7-p4/analyze-rival-geometry.mjs","--exact",path.join(d,"e.json"),"--features",path.join(d,"f.tsv"),"--out",path.join(d,"o")],{encoding:"utf8"});
if(p.status!==0) throw new Error(p.stderr||p.stdout);
const r=JSON.parse(fs.readFileSync(path.join(d,"o","policy-geometry.json"),"utf8"));
if(r.observational_geometry.source_annotation_boundaries!==1) throw new Error("BOUNDARY");
if(r.search_representation_geometry.observed_face_next_states!==1) throw new Error("OBS");
if(r.measurement_boundary.pooled_mechanism_claim!=="NOT_AUTHORIZED") throw new Error("AUTH");
console.log("G7_P4_POLICY_GEOMETRY_TEST_PASS");
