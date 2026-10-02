import {spawnSync} from "node:child_process";
const p=spawnSync("cargo",["run","-q","-p","search-geometry-core","--bin","g7_p5_packet_generator"],{encoding:"utf8"});
if(p.status!==0) throw new Error(p.stderr||p.stdout);
const lines=p.stdout.trim().split(/\r?\n/);
if(lines.length!==25) throw new Error("EXPECTED_24_TRIALS");
const h=lines[0].split("\t");
const rows=lines.slice(1).map(x=>Object.fromEntries(x.split("\t").map((v,i)=>[h[i],v])));
for(let i=0;i<rows.length;i+=2){
  if(rows[i].pair_id!==rows[i+1].pair_id) throw new Error("PAIR");
  if(rows[i].phase1_lb!==rows[i+1].phase1_lb) throw new Error("LB_MATCH");
  if(rows[i].h1_best===rows[i].h3_best||rows[i+1].h1_best===rows[i+1].h3_best) throw new Error("RIVAL_DISAGREEMENT");
}
console.log("G7_P5_PACKET_GENERATOR_TEST_PASS");
