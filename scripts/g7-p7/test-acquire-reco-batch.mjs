import {spawnSync} from "node:child_process";
const p=spawnSync(process.execPath,["scripts/g7-p7/acquire-reco-batch.mjs","--batch","1","--out","/tmp/unused"],{encoding:"utf8"});
if(p.status!==0) throw new Error(p.stderr||p.stdout);
if(!p.stdout.includes("G7_P7_RECO_BATCH_DRY_RUN")||!p.stdout.includes("MAX_SOLVES\t10")) throw new Error("DRY_RUN");
console.log("G7_P7_RECO_BATCH_ACQUIRE_TEST_PASS");