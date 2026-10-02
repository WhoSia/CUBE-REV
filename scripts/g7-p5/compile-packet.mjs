import fs from "node:fs";
import crypto from "node:crypto";

const input=process.argv[2], output=process.argv[3];
if(!input||!output) throw new Error("usage: compile-packet input.tsv output.json");
const lines=fs.readFileSync(input,"utf8").trim().split(/\r?\n/);
const header=lines.shift().split("\t");
const rows=lines.map(line=>Object.fromEntries(line.split("\t").map((v,i)=>[header[i],v])));
if(rows.length!==24) throw new Error("PACKET_SIZE");

const trials=rows.map((r,i)=>({
  trial_id:`T${String(i+1).padStart(2,"0")}`,
  pair_id:r.pair_id,
  trial_side:r.trial_side,
  state_id:r.state_id,
  phase1_lb:Number(r.phase1_lb),
  predictions:{
    H1_PDB_GREEDY:r.h1_best.split(",").filter(Boolean).map(Number),
    H3_PDB_LOOKAHEAD:r.h3_best.split(",").filter(Boolean).map(Number)
  },
  rival_disagreement:Number(r.disagreement),
  tie_counts:{h1:Number(r.h1_ties),h3:Number(r.h3_ties)},
  scramble:r.scramble,
  cube:{
    cp:r.cp.split(",").map(Number),co:r.co.split(",").map(Number),
    ep:r.ep.split(",").map(Number),eo:r.eo.split(",").map(Number)
  },
  condition:{
    display_horizon_condition:(i%2===0?"NEUTRAL":"DELIBERATE"),
    choice_order_seed:`P5-${r.pair_id}-${r.trial_side}`
  }
}));
for(let i=0;i<trials.length;i+=2){
  if(trials[i].pair_id!==trials[i+1].pair_id) throw new Error("PAIR_ORDER");
  if(trials[i].phase1_lb!==trials[i+1].phase1_lb) throw new Error("PAIR_LB");
}
const core={
  schema_version:"g7-p5-packet-1",
  instrument_version:"g7-p5-instrument-0.1.0",
  human_contact_authority:"HOLD_UNTIL_INSTRUMENT_VALIDATED",
  representation_families:["H1_PDB_GREEDY","H3_PDB_LOOKAHEAD"],
  action_space:["U","U2","U'","R","R2","R'","F","F2","F'","D","D2","D'","L","L2","L'","B","B2","B'"],
  trials
};
const canonical=JSON.stringify(core);
const packet_sha256=crypto.createHash("sha256").update(canonical).digest("hex");
fs.writeFileSync(output,JSON.stringify({...core,packet_sha256},null,2)+"\n");
console.log("G7_P5_PACKET_COMPILE_PASS");
console.log("TRIALS\t"+trials.length);
console.log("PAIRS\t"+new Set(trials.map(x=>x.pair_id)).size);
console.log("PACKET_SHA256\t"+packet_sha256);
