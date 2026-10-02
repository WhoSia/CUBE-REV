import {spawnSync} from "node:child_process";
const p=spawnSync("cargo",[
  "run","-q","-p","search-geometry-core","--bin","g7_p4_replay","--",
  "--scramble","R U2 F'",
  "--solution","F U2 R'"
],{encoding:"utf8"});
if(p.status!==0) throw new Error(p.stderr||p.stdout);
if(!p.stdout.includes("G7_P4_EXACT_REPLAY_PASS")) throw new Error("PASS_MARKER");
if(!p.stdout.includes("FINAL_SOLVED\t1")) throw new Error("END_STATE");
if(!p.stdout.includes("SOLUTION_MOVES\t3")) throw new Error("MOVE_COUNT");
console.log("G7_P4_EXACT_REPLAY_TEST_PASS");
