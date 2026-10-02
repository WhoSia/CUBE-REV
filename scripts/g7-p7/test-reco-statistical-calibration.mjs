import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import {spawnSync} from "node:child_process";
const d=fs.mkdtempSync(path.join(os.tmpdir(),"g7-p7-cal-"));
const ctx=[];
const feat=[
"source_id\tprefix_index\tphase1_lb\tts_lb\tfs_lb\tis_g1\tboundary_after\tnext_action\th1_best\th2_best\th3_best\tts_best\tfs_best\trival_unique_sets\tmean_pairwise_jaccard_distance\tobserved_match_h1\tobserved_match_h2\tobserved_match_h3\tobserved_match_ts\tobserved_match_fs"
];
for(let s=1;s<=12;s++){
  ctx.push({source_id:s,prefix_index:0,boundary_after:false,method_family:"CFOP",reconstructor:"R",cohort:(s<=6?"P4_PILOT":"P7_BATCH1")});
  ctx.push({source_id:s,prefix_index:1,boundary_after:true,method_family:"CFOP",reconstructor:"R",cohort:"X"});
  feat.push([s,0,5,5,4,0,0,0,"0","0,1","0,1,2","0","1",4,0.6,1,1,1,1,0].join("\t"));
  feat.push([s,1,5,5,4,0,1,0,"0","0,1","0,1,2","0","1",4,0.5,1,1,1,1,0].join("\t"));
}
fs.writeFileSync(path.join(d,"c.jsonl"),ctx.map(JSON.stringify).join("\n")+"\n");
fs.writeFileSync(path.join(d,"f.tsv"),feat.join("\n")+"\n");
const p=spawnSync("python3",["scripts/g7-p7/calibrate-reco-statistics.py","--context",path.join(d,"c.jsonl"),"--features",path.join(d,"f.tsv"),"--out",path.join(d,"o"),"--permutations","1000"],{encoding:"utf8"});
if(p.status!==0) throw new Error(p.stderr||p.stdout);
const r=JSON.parse(fs.readFileSync(path.join(d,"o","statistical-calibration.json"),"utf8"));
if(r.solves!==12||r.progress_matched_boundary_calibration.eligible_solves!==12) throw new Error("SIZE");
if(!r.robustness_stress?.choice_by_campaign_epoch?.P4_PREDECESSOR||!r.robustness_stress?.choice_by_campaign_epoch?.P7_FRESH_CAMPAIGN) throw new Error("EPOCH");
if(Object.keys(r.robustness_stress.leave_one_cohort_out).length!==2) throw new Error("LOO_COHORT");
if(!(r.choice_calibration.H1.solve_mean_excess>r.choice_calibration.H3.solve_mean_excess)) throw new Error("COVERAGE_ADJUSTMENT");
if(!(r.progress_matched_boundary_calibration.mean_matched_delta<0)) throw new Error("BOUNDARY");
console.log("G7_P7_RECO_STATISTICAL_CALIBRATION_TEST_PASS");
