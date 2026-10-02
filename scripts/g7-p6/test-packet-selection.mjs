import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import {spawnSync} from "node:child_process";
const d=fs.mkdtempSync(path.join(os.tmpdir(),"g7-p6-select-"));
let p=spawnSync("cargo",["run","-q","-p","search-geometry-core","--bin","g7_p6_packet_bank"],{encoding:"utf8"});
if(p.status!==0) throw new Error(p.stderr||p.stdout);
fs.writeFileSync(path.join(d,"b.tsv"),p.stdout);
p=spawnSync(process.execPath,["scripts/g7-p6/compile-packet-bank.mjs",path.join(d,"b.tsv"),path.join(d,"b.json")],{encoding:"utf8"});
if(p.status!==0) throw new Error(p.stderr||p.stdout);
p=spawnSync(process.execPath,["scripts/g7-p6/select-prospective-packets.mjs",path.join(d,"b.json"),path.join(d,"out")],{encoding:"utf8"});
if(p.status!==0) throw new Error(p.stderr||p.stdout);
const a=JSON.parse(fs.readFileSync(path.join(d,"out","selection-receipt.json"),"utf8"));
if(a.development_states!==32||a.confirmation_states!==32||a.reserve_states!==192) throw new Error("SIZE");
if(a.exact_state_overlap_dev_confirm!==0||a.state_id_overlap_dev_confirm!==0) throw new Error("OVERLAP");
for(const role of ["development","confirmation"]){
 const x=JSON.parse(fs.readFileSync(path.join(d,"out",role+"-packet.json"),"utf8"));
 const seeds=new Set(x.records.map(r=>r.seed_id)), motifs=new Set(x.records.map(r=>r.motif));
 if(seeds.size!==8||motifs.size!==4) throw new Error("BALANCE:"+role);
 const cells=new Set(x.records.map(r=>r.seed_id+"|"+r.motif));
 if(cells.size!==32) throw new Error("CELL:"+role);
}
console.log("G7_P6_PACKET_SELECTION_TEST_PASS");
