import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import {spawnSync} from "node:child_process";
const d=fs.mkdtempSync(path.join(os.tmpdir(),"g7-p4-exact-"));
const rows=[
 {source_id:1,stratum:{method_family:"CFOP"},parsed:{solver:"A",reconstructor:"R",scramble_raw:"R U2 F'",reconstruction_raw:"F U2 R' // done"}},
 {source_id:2,stratum:{method_family:"ROUX"},parsed:{solver:"B",reconstructor:"Q",scramble_raw:"R",reconstruction_raw:"R' x // rotated solved"}}
];
const input=path.join(d,"s.jsonl");fs.writeFileSync(input,rows.map(JSON.stringify).join("\n")+"\n");
const p=spawnSync(process.execPath,["scripts/g7-p4/materialize-exact-trajectories.mjs","--input",input,"--out",path.join(d,"o")],{encoding:"utf8"});
if(p.status!==0) throw new Error(p.stderr||p.stdout);
const r=JSON.parse(fs.readFileSync(path.join(d,"o","exact-trajectories.json"),"utf8"));
if(r.replay_status_counts.SUPPORTED!==2) throw new Error("SUPPORTED");
if(!r.records.every(x=>x.end_solved_up_to_rotation)) throw new Error("END_SOLVED");
if(r.records[0].prefixes.at(-1).event_kind!=="ANNOTATION") throw new Error("ANNOTATION_BOUNDARY");
console.log("G7_P4_EXACT_TRAJECTORY_TEST_PASS");
