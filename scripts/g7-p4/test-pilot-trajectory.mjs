import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import {spawnSync} from "node:child_process";
const d=fs.mkdtempSync(path.join(os.tmpdir(),"g7-p4-traj-"));
const input=path.join(d,"s.jsonl");
const rows=[
 {source_id:1,stratum:{method_family:"CFOP"},parsed:{solver:"A",reconstructor:"R",puzzle:"3x3",result_text:"5.00",solve_date:"2025-01-01",reconstruction_raw:"R U R' // pair\nF2 U2 // finish"}},
 {source_id:2,stratum:{method_family:"ROUX"},parsed:{solver:"B",reconstructor:"Q",puzzle:"3x3",result_text:"6.00",solve_date:"2024-01-01",reconstruction_raw:"x r U M' // block"}}
];
fs.writeFileSync(input,rows.map(JSON.stringify).join("\n")+"\n");
const p=spawnSync(process.execPath,["scripts/g7-p4/analyze-pilot-trajectory.mjs","--input",input,"--out",path.join(d,"o")],{encoding:"utf8"});
if(p.status!==0) throw new Error(p.stderr||p.stdout);
const r=JSON.parse(fs.readFileSync(path.join(d,"o","pilot-trajectory.json"),"utf8"));
if(r.solve_count!==2) throw new Error("COUNT");
if(r.geometry_status_counts.HTM_READY!==1) throw new Error("HTM");
if(r.geometry_status_counts.EXTENDED_MOVE_KERNEL_REQUIRED!==1) throw new Error("EXTENDED");
if(r.total_annotations!==3) throw new Error("ANNOT");
console.log("G7_P4_PILOT_TRAJECTORY_TEST_PASS");
