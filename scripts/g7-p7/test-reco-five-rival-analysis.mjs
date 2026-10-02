import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import {spawnSync} from "node:child_process";
const d=fs.mkdtempSync(path.join(os.tmpdir(),"g7-p7-analysis-"));
const ctx=[
 {source_id:1,prefix_index:0,boundary_after:false,annotation_after:null,next_action_index:0,method_family:"CFOP",cohort:"X",reconstructor:"R"},
 {source_id:1,prefix_index:1,boundary_after:true,annotation_after:"cross",next_action_index:3,method_family:"CFOP",cohort:"X",reconstructor:"R"},
 {source_id:1,prefix_index:2,boundary_after:false,annotation_after:null,next_action_index:null,method_family:"CFOP",cohort:"X",reconstructor:"R"}
];
fs.writeFileSync(path.join(d,"c.jsonl"),ctx.map(JSON.stringify).join("\n")+"\n");
fs.writeFileSync(path.join(d,"f.tsv"),[
"source_id\tprefix_index\tphase1_lb\tts_lb\tfs_lb\tis_g1\tboundary_after\tnext_action\th1_best\th2_best\th3_best\tts_best\tfs_best\trival_unique_sets\tmean_pairwise_jaccard_distance\tobserved_match_h1\tobserved_match_h2\tobserved_match_h3\tobserved_match_ts\tobserved_match_fs",
"1\t0\t5\t5\t4\t0\t0\t0\t0\t0,1\t1\t0\t2\t4\t0.7\t1\t1\t0\t1\t0",
"1\t1\t4\t4\t3\t0\t1\t3\t3\t3\t4\t3,4\t5\t4\t0.8\t1\t1\t0\t1\t0",
"1\t2\t0\t0\t0\t1\t0\t-1\t0,1,2\t0,1,2\t0,1,2\t0,1,2\t0,1,2\t1\t0\t-1\t-1\t-1\t-1\t-1"
].join("\n")+"\n");
const p=spawnSync(process.execPath,["scripts/g7-p7/analyze-reco-five-rival.mjs","--context",path.join(d,"c.jsonl"),"--features",path.join(d,"f.tsv"),"--out",path.join(d,"o")],{encoding:"utf8"});
if(p.status!==0) throw new Error(p.stderr||p.stdout);
const r=JSON.parse(fs.readFileSync(path.join(d,"o","five-rival-analysis.json"),"utf8"));
if(r.corpus.solves!==1||r.boundary_states.states!==1) throw new Error("SIZE");
if(r.raw_annotation_summary_min_n2.cross) throw new Error("MIN_N");
if(r.by_stage_family.CROSS_OR_XCROSS.states!==1) throw new Error("STAGE");
console.log("G7_P7_RECO_FIVE_RIVAL_ANALYSIS_TEST_PASS");
