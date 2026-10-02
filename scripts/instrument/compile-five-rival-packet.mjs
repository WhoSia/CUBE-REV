import fs from "node:fs";
import crypto from "node:crypto";
const src=JSON.parse(fs.readFileSync(process.argv[2],"utf8"));
const role=process.argv[3]||"DEVELOPMENT";
const out=process.argv[4];
if(!out) throw new Error("OUTPUT_REQUIRED");
if(!["DEVELOPMENT","CONFIRMATION"].includes(role)) throw new Error("ROLE");
const actions=["U","U2","U'","R","R2","R'","F","F2","F'","D","D2","D'","L","L2","L'","B","B2","B'"];
const records=src.records;
if(!Array.isArray(records)||records.length!==32) throw new Error("EXPECTED_32_STATES");
if(new Set(records.map(x=>x.state_id)).size!==32) throw new Error("STATE_DUPLICATE");
const rivalFamilies=[
 "H1_MAX_PDB_GREEDY","H2_MAX_PDB_LOOKAHEAD","H3_MAX_PDB_LOOKAHEAD",
 "H1_TWIST_SLICE_COMPONENT","H1_FLIP_SLICE_COMPONENT"
];
for(const r of records) for(const f of rivalFamilies) if(!Array.isArray(r.rivals?.[f])||!r.rivals[f].length) throw new Error("RIVAL:"+r.state_id+":"+f);
const trials=records.map((r,i)=>({
 trial_id:(role==="DEVELOPMENT"?"D":"C")+String(i+1).padStart(2,"0"),
 state_id:r.state_id,seed_id:r.seed_id,motif:r.motif,phase1_lb:r.phase1_lb,cube:r.cube,rivals:r.rivals,
 display:{
   prompt_condition:(i%2===0?"NEUTRAL":"DELIBERATE"),
   action_order_seed:"CUBE-REV-"+role+"-"+r.state_id,
   confidence_prompt:(i%4===0)
 }
}));
const core={schema_version:"core-five-rival-instrument-packet-1",role,human_contact_authority:"CLOSED_PENDING_CONTACT_GATE",action_space:actions,rival_families:rivalFamilies,trials};
const sha256=crypto.createHash("sha256").update(JSON.stringify(core)).digest("hex");
fs.writeFileSync(out,JSON.stringify({...core,sha256},null,2)+"\n");
console.log("CORE_INSTRUMENT_PACKET_COMPILE_PASS");
console.log("ROLE\t"+role);
console.log("TRIALS\t"+trials.length);
console.log("SHA256\t"+sha256);
