import {spawnSync} from "node:child_process";
const p=spawnSync(process.execPath,["scripts/g7-p4/acquire-confirmatory.mjs"],{encoding:"utf8"});
if(p.status!==0) throw new Error(p.stderr||p.stdout);
if(!p.stdout.includes("G7_P4_CONFIRMATORY_DRY_RUN")) throw new Error("DRY_RUN");
if(!p.stdout.includes("3594,8402,3722,1976,785,9332,11750,1164,9693,7905")) throw new Error("IDS");
if(!p.stdout.includes("MAX_SOLVES\t10")) throw new Error("COUNT");
console.log("G7_P4_CONFIRMATORY_ACQUISITION_TEST_PASS");
