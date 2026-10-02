import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import {spawnSync} from "node:child_process";
const d=fs.mkdtempSync(path.join(os.tmpdir(),"g7-p4-replay-"));
const rows=[{
 source_id:1,stratum:{method_family:"CFOP"},
 parsed:{solver:"A",reconstructor:"R",scramble_raw:"R U2 F'",reconstruction_raw:"(F U2 R') // inverse"}
},{
 source_id:2,stratum:{method_family:"ROUX"},
 parsed:{solver:"B",reconstructor:"Q",scramble_raw:"R U R'",reconstruction_raw:"R U' R' // alg\nx x' // frame"}
}];
fs.writeFileSync(path.join(d,"s.jsonl"),rows.map(JSON.stringify).join("\n")+"\n");
const p=spawnSync(process.execPath,["scripts/g7-p4/replay-pilot-exact.mjs","--input",path.join(d,"s.jsonl"),"--out",path.join(d,"o")],{encoding:"utf8"});
if(p.status===0) throw new Error("second fixture should fail solved-end validation");
const rows2=[rows[0]];
fs.writeFileSync(path.join(d,"s2.jsonl"),rows2.map(JSON.stringify).join("\n")+"\n");
const q=spawnSync(process.execPath,["scripts/g7-p4/replay-pilot-exact.mjs","--input",path.join(d,"s2.jsonl"),"--out",path.join(d,"o2")],{encoding:"utf8"});
if(q.status!==0) throw new Error(q.stderr||q.stdout);
const r=JSON.parse(fs.readFileSync(path.join(d,"o2","exact-trajectories.json"),"utf8"));
if(r.exact_end_validation_pass!==1||r.total_prefixes!==3) throw new Error("REPLAY");
console.log("G7_P4_EXACT_TRAJECTORY_TEST_PASS");
