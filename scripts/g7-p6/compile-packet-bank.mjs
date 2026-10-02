import fs from "node:fs";
import crypto from "node:crypto";
const input=process.argv[2], output=process.argv[3];
if(!input||!output) throw new Error("usage");
const lines=fs.readFileSync(input,"utf8").trim().split(/\r?\n/);
const h=lines.shift().split("\t");
const rows=lines.map(line=>Object.fromEntries(line.split("\t").map((v,i)=>[h[i],v])));
const parseSet=s=>s?s.split(",").map(Number):[];
const parseArr=s=>s.split(",").map(Number);
const records=rows.map(r=>({
  seed_id:r.seed_id,motif:r.motif,state_id:r.state_id,phase1_lb:Number(r.phase1_lb),
  rivals:{
    H1_MAX_PDB_GREEDY:parseSet(r.h1_best),
    H2_MAX_PDB_LOOKAHEAD:parseSet(r.h2_best),
    H3_MAX_PDB_LOOKAHEAD:parseSet(r.h3_best),
    H1_TWIST_SLICE_COMPONENT:parseSet(r.ts_best),
    H1_FLIP_SLICE_COMPONENT:parseSet(r.fs_best)
  },
  cube:{cp:parseArr(r.cp),co:parseArr(r.co),ep:parseArr(r.ep),eo:parseArr(r.eo)}
}));
const core={schema_version:"g7-p6-packet-bank-1",human_contact_authority:"CLOSED",records};
const sha256=crypto.createHash("sha256").update(JSON.stringify(core)).digest("hex");
fs.writeFileSync(output,JSON.stringify({...core,sha256},null,2)+"\n");
console.log("G7_P6_PACKET_BANK_COMPILE_PASS");
console.log("STATES\t"+records.length);
console.log("SHA256\t"+sha256);
