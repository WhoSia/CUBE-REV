import {spawnSync} from "node:child_process";
const p=spawnSync("cargo",["run","-q","-p","search-geometry-core","--bin","g7_p6_packet_bank"],{encoding:"utf8"});
if(p.status!==0) throw new Error(p.stderr||p.stdout);
const lines=p.stdout.trim().split(/\r?\n/); const h=lines.shift().split("\t");
const rows=lines.map(x=>Object.fromEntries(x.split("\t").map((v,i)=>[h[i],v])));
if(rows.length!==256) throw new Error("COUNT:"+rows.length);
if(new Set(rows.map(x=>x.state_id)).size!==256) throw new Error("STATE_IDS");
for(const m of ["H2_UNIQUE","ALL_HORIZON_DISAGREE","COMPONENT_UNIQUE","COMPONENT_VS_MAX_CONFLICT"]){
  if(rows.filter(x=>x.motif===m).length!==64) throw new Error("MOTIF:"+m);
}
for(let s=1;s<=8;s++) if(rows.filter(x=>x.seed_id===`S${String(s).padStart(2,"0")}`).length!==32) throw new Error("SEED:"+s);
console.log("G7_P6_PACKET_BANK_TEST_PASS");
