import {spawnSync} from "node:child_process";
const input="source_id\tmove_index\trank_before\trank_after\taction_index\tmethod_family\treconstructor\n1\t1\t0\t0\t0\tCFOP\tR\n";
const p=spawnSync("cargo",["run","-q","-p","search-geometry-core","--bin","g7_p4_phase1_batch"],{input,encoding:"utf8"});
if(p.status!==0) throw new Error(p.stderr||p.stdout);
if(!p.stdout.includes("local_regret")) throw new Error("HEADER");
if(!p.stdout.includes("1\t1\t0\t0\t0\tCFOP\tR")) throw new Error("ROW");
console.log("G7_P4_PHASE1_BATCH_TEST_PASS");
