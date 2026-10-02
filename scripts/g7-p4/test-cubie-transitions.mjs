import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import {spawnSync} from "node:child_process";
const d=fs.mkdtempSync(path.join(os.tmpdir(),"g7-p4-cubie-"));
const rows=[
 {source_id:1,stratum:{method_family:"CFOP"},parsed:{solver:"A",reconstructor:"R",scramble_raw:"R U",reconstruction_raw:"U' R' // done"}},
 {source_id:2,stratum:{method_family:"ROUX"},parsed:{solver:"B",reconstructor:"Q",scramble_raw:"R",reconstruction_raw:"R' x M M' // done"}}
];
const pth=path.join(d,"s.jsonl");fs.writeFileSync(pth,rows.map(JSON.stringify).join("\n")+"\n");
const p=spawnSync(process.execPath,["scripts/g7-p4/materialize-cubie-transitions.mjs","--input",pth,"--out",path.join(d,"o")],{encoding:"utf8"});
if(p.status!==0) throw new Error(p.stderr||p.stdout);
const r=JSON.parse(fs.readFileSync(path.join(d,"o","cubie-transitions.json"),"utf8"));
if(r.solve_count!==2) throw new Error("COUNT");
if((r.transition_counts.SINGLE_HTM||0)<2) throw new Error("SINGLE");
if((r.transition_counts.FRAME_ONLY||0)<1) throw new Error("FRAME");
if((r.transition_counts.MULTI_ACTION_EXTENDED||0)<2) throw new Error("MULTI");
console.log("G7_P4_CUBIE_TRANSITION_TEST_PASS");
