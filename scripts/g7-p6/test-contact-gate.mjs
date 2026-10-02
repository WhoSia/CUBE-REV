import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import {spawnSync} from "node:child_process";
const d=fs.mkdtempSync(path.join(os.tmpdir(),"g7-p6-contact-"));
const src={records:Array.from({length:32},(_,i)=>({
 state_id:"S"+i,seed_id:"Q"+(i%8),motif:["A","B","C","D"][i%4],phase1_lb:7,
 cube:{cp:[0,1,2,3,4,5,6,7],co:[0,0,0,0,0,0,0,0],ep:[0,1,2,3,4,5,6,7,8,9,10,11],eo:Array(12).fill(0)},
 rivals:{H1_MAX_PDB_GREEDY:[0],H2_MAX_PDB_LOOKAHEAD:[1],H3_MAX_PDB_LOOKAHEAD:[2],H1_TWIST_SLICE_COMPONENT:[3],H1_FLIP_SLICE_COMPONENT:[4]}
}))};
fs.writeFileSync(path.join(d,"src.json"),JSON.stringify(src));
let p=spawnSync(process.execPath,["scripts/g7-p6/compile-instrument-packet.mjs",path.join(d,"src.json"),"DEVELOPMENT",path.join(d,"p.json")],{encoding:"utf8"});
if(p.status!==0) throw new Error(p.stderr||p.stdout);
const packet=JSON.parse(fs.readFileSync(path.join(d,"p.json"),"utf8"));
const closed={consent_metadata_present:false,supervision_or_research_authorization_present:false,device_timing_resolution_ms:1,visibility_api_supported:true,packet_sha256:packet.sha256,participant_set_role:"DEVELOPMENT"};
fs.writeFileSync(path.join(d,"c.json"),JSON.stringify(closed));
p=spawnSync(process.execPath,["scripts/g7-p6/evaluate-contact-gate.mjs",path.join(d,"p.json"),path.join(d,"c.json"),path.join(d,"g.json")],{encoding:"utf8"});
if(p.status!==0) throw new Error(p.stderr||p.stdout);
let g=JSON.parse(fs.readFileSync(path.join(d,"g.json"),"utf8"));
if(g.open) throw new Error("SHOULD_BE_CLOSED");
const open={...closed,consent_metadata_present:true,supervision_or_research_authorization_present:true};
fs.writeFileSync(path.join(d,"o.json"),JSON.stringify(open));
p=spawnSync(process.execPath,["scripts/g7-p6/evaluate-contact-gate.mjs",path.join(d,"p.json"),path.join(d,"o.json"),path.join(d,"g2.json")],{encoding:"utf8"});
if(p.status!==0) throw new Error(p.stderr||p.stdout);
g=JSON.parse(fs.readFileSync(path.join(d,"g2.json"),"utf8"));
if(!g.open) throw new Error("SHOULD_OPEN");
console.log("G7_P6_CONTACT_GATE_TEST_PASS");
