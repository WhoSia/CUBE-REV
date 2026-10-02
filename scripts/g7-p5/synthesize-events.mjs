import fs from "node:fs";
import {EventLog,verifyPacket,shuffledTrials} from "./instrument-core.mjs";
const packet=JSON.parse(fs.readFileSync(process.argv[2],"utf8")); verifyPacket(packet);
const out=process.argv[3]; if(!out) throw new Error("output");
let now=0; const clock=()=>now;
const logs=[];
for(let s=0;s<8;s++){
  const sid=`SYN${String(s+1).padStart(2,"0")}`;
  const log=new EventLog({sessionId:sid,packet,clock});
  log.start("SYNTHETIC_ONLY");
  for(const tr of shuffledTrials(packet,sid)){
    now+=25;log.present(tr);
    const pred=(s<6?tr.predictions.H3_PDB_LOOKAHEAD:tr.predictions.H1_PDB_GREEDY);
    const choice=pred[(s+tr.trial_id.charCodeAt(2))%pred.length];
    now+=420+((s*37+Number(tr.trial_id.slice(1))*53)%600);
    log.choose(tr,packet.action_space[choice],3+(s%2));
    now+=10;log.complete(tr);
  }
  log.finish();logs.push(log.jsonl().trim());
}
fs.writeFileSync(out,logs.join("\n")+"\n");
console.log("G7_P5_SYNTHETIC_SESSIONS_PASS");
console.log("SESSIONS\t8");
