import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import {spawnSync} from "node:child_process";
const d=fs.mkdtempSync(path.join(os.tmpdir(),"g7-p5-final-"));
const inst={verdict:"PASS_INSTRUMENT_VALIDATED_HUMAN_CONTACT_NOT_YET_OPEN",human_contact_open:false};
const fresh={conclusion:"PASS_TWO_SEED_PACKET_CONSTITUTION_REPLICATION"};
fs.writeFileSync(path.join(d,"i.json"),JSON.stringify(inst));
fs.writeFileSync(path.join(d,"f.json"),JSON.stringify(fresh));
fs.writeFileSync(path.join(d,"e.tsv"),[
 "G7_P5_RIVAL_ECOLOGY_PASS",
 "STATES\t6000",
 "H1_H3_DISAGREE_RATE\t0.2",
 "H1_H2_DISAGREE_RATE\t0.15",
 "H2_H3_DISAGREE_RATE\t0.1",
 "H2_UNIQUE_RATE\t0.02",
 "TS_FS_DISAGREE_RATE\t0.4",
 "COMPONENT_UNIQUE_RATE\t0.03",
 "JACCARD_H1_H3\t0.7"
].join("\n")+"\n");
const p=spawnSync(process.execPath,["scripts/g7-p5/evaluate-final-precontact.mjs","--instrument",path.join(d,"i.json"),"--fresh",path.join(d,"f.json"),"--ecology",path.join(d,"e.tsv"),"--out",path.join(d,"o")],{encoding:"utf8"});
if(p.status!==0) throw new Error(p.stderr||p.stdout);
const r=JSON.parse(fs.readFileSync(path.join(d,"o","G7-P5-FINAL-PRECONTACT.json"),"utf8"));
if(!r.p5_close_recommended||!r.expanded_rival_ecology_required_next_phase||!r.promoted_rivals.H2_PDB_LOOKAHEAD) throw new Error("BOUNDARY");
console.log("G7_P5_FINAL_PRECONTACT_TEST_PASS");
