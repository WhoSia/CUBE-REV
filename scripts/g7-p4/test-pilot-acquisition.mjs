import {spawnSync} from "node:child_process";
const p=spawnSync(process.execPath,["scripts/g7-p4/acquire-pilot.mjs"],{encoding:"utf8"});
if(p.status!==0) throw new Error(p.stderr||p.stdout);
if(!p.stdout.includes("G7_P4_PILOT_DRY_RUN")) throw new Error("DRY_RUN");
if(!p.stdout.includes("12137,2104,11859,1019,6403,5070,12096,12832,2092,3449")) throw new Error("IDS");
if(!p.stdout.includes("MAX_SOLVES\t10")) throw new Error("COUNT");
console.log("G7_P4_PILOT_ACQUISITION_TEST_PASS");
