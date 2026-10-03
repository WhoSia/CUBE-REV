import {spawnSync} from "node:child_process";
const manifest=process.argv[2];
if(!manifest) throw new Error("MANIFEST_ARG");
const p=spawnSync(process.execPath,["scripts/g7-p13/acquire-fresh80-reco-batch.mjs","--manifest",manifest,"--batch","1","--out","/tmp/unused"],{encoding:"utf8"});
if(p.status!==0) throw new Error(p.stderr||p.stdout);
if(!p.stdout.includes("G7_P13_RECO_BATCH_DRY_RUN")||!p.stdout.includes("MAX_SOLVES\t10")) throw new Error("DRY_RUN");
console.log("G7_P13_RECO_BATCH_ACQUIRE_TEST_PASS");