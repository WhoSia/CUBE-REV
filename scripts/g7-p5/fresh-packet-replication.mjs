import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import {spawnSync} from "node:child_process";

const d=fs.mkdtempSync(path.join(os.tmpdir(),"g7-p5-fresh-"));
function make(seed,label){
  const env={...process.env,G7_P5_PACKET_SEED_HEX:seed};
  let p=spawnSync("cargo",["run","-q","-p","search-geometry-core","--bin","g7_p5_packet_generator"],{encoding:"utf8",env});
  if(p.status!==0) throw new Error(p.stderr||p.stdout);
  const tsv=path.join(d,label+".tsv"), json=path.join(d,label+".json"), audit=path.join(d,label+"-audit.json");
  fs.writeFileSync(tsv,p.stdout);
  p=spawnSync(process.execPath,["scripts/g7-p5/compile-packet.mjs",tsv,json],{encoding:"utf8"});
  if(p.status!==0) throw new Error(p.stderr||p.stdout);
  p=spawnSync(process.execPath,["scripts/g7-p5/audit-packet.mjs",json,audit],{encoding:"utf8"});
  if(p.status!==0) throw new Error(p.stderr||p.stdout);
  return {packet:JSON.parse(fs.readFileSync(json,"utf8")),audit:JSON.parse(fs.readFileSync(audit,"utf8"))};
}
const canonical=make("C0BE5A1720261002","canonical");
const fresh=make("A17E2026BADC0FFE","fresh");
if(canonical.packet.packet_sha256===fresh.packet.packet_sha256) throw new Error("FRESH_PACKET_COLLISION");
for(const x of [canonical,fresh]){
  if(!x.audit.pass||x.audit.trials!==24||x.audit.pairs!==12) throw new Error("AUDIT");
  if(x.audit.rival_disagreement_trials!==24) throw new Error("RIVAL_SUPPORT");
  if(x.audit.distinct_phase1_lb<2) throw new Error("LB_SUPPORT");
}
const out={
  schema_version:"g7-p5-fresh-packet-replication-1",
  canonical_sha256:canonical.packet.packet_sha256,
  fresh_sha256:fresh.packet.packet_sha256,
  canonical_audit:canonical.audit,
  fresh_audit:fresh.audit,
  conclusion:"PASS_TWO_SEED_PACKET_CONSTITUTION_REPLICATION"
};
fs.writeFileSync(process.argv[2],JSON.stringify(out,null,2)+"\n");
console.log("G7_P5_FRESH_PACKET_REPLICATION_PASS");
console.log("CANONICAL_SHA\t"+out.canonical_sha256);
console.log("FRESH_SHA\t"+out.fresh_sha256);
