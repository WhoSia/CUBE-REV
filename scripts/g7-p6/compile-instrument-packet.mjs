import fs from "node:fs";
import crypto from "node:crypto";

const src=JSON.parse(fs.readFileSync(process.argv[2],"utf8"));
const role=process.argv[3]||"DEVELOPMENT";
const out=process.argv[4];
if(!out) throw new Error("output");
const actions=["U","U2","U'","R","R2","R'","F","F2","F'","D","D2","D'","L","L2","L'","B","B2","B'"];
const records=src.records;
if(records.length!==32) throw new Error("EXPECTED_32_STATES");
const trials=records.map((r,i)=>({
  trial_id:`${role==="DEVELOPMENT"?"D":"C"}${String(i+1).padStart(2,"0")}`,
  state_id:r.state_id,
  seed_id:r.seed_id,
  motif:r.motif,
  phase1_lb:r.phase1_lb,
  cube:r.cube,
  rivals:r.rivals,
  display:{
    prompt_condition:(i%2===0?"NEUTRAL":"DELIBERATE"),
    action_order_seed:`G7-P6-${role}-${r.state_id}`,
    confidence_prompt:(i%4===0)
  }
}));
const core={
 schema_version:"g7-p6-instrument-packet-1",
 role,
 human_contact_authority:"CLOSED_PENDING_P6_CONTACT_GATE",
 action_space:actions,
 rival_families:[
   "H1_MAX_PDB_GREEDY","H2_MAX_PDB_LOOKAHEAD","H3_MAX_PDB_LOOKAHEAD",
   "H1_TWIST_SLICE_COMPONENT","H1_FLIP_SLICE_COMPONENT"
 ],
 trials
};
const sha256=crypto.createHash("sha256").update(JSON.stringify(core)).digest("hex");
fs.writeFileSync(out,JSON.stringify({...core,sha256},null,2)+"\n");
console.log("G7_P6_INSTRUMENT_PACKET_COMPILE_PASS");
console.log("ROLE\t"+role);
console.log("TRIALS\t"+trials.length);
console.log("SHA256\t"+sha256);
