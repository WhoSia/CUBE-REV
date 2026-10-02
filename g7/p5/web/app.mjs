import {verifyPacketBrowser,trialOrder,orderedActions,BrowserEventLog} from "./browser-core.mjs";
import {renderNet} from "./state-net.mjs";
const $=id=>document.getElementById(id);
let packet,trials,idx=0,log;
$("load").onclick=async()=>{
  const file=$("packetFile").files[0]; if(!file)return;
  packet=JSON.parse(await file.text()); await verifyPacketBrowser(packet);
  const sessionId="VALIDATION-"+crypto.randomUUID();
  trials=await trialOrder(packet,sessionId); log=new BrowserEventLog(sessionId,packet);log.start();
  idx=0;$("status").textContent="Packet verified. Validation session started.";show();
};
async function show(){
  if(idx>=trials.length){log.finish();$("trial").classList.add("hidden");$("export").disabled=false;$("status").textContent="Validation session complete.";return;}
  const t=trials[idx];$("trial").classList.remove("hidden");$("trialId").textContent=t.trial_id;renderNet($("cube"),t.scramble);
  const box=$("moves");box.replaceChildren();log.present(t);
  const actions=await orderedActions(packet.action_space,t.condition.choice_order_seed); actions.forEach(move=>{const b=document.createElement("button");b.textContent=move;b.onclick=()=>{log.choose(t,move,null);log.complete(t);idx++;show();};box.appendChild(b);});
}
$("export").onclick=()=>{
  const blob=new Blob([log.jsonl()],{type:"application/x-ndjson"});
  const a=document.createElement("a");a.href=URL.createObjectURL(blob);a.download="g7-p5-validation-events.jsonl";a.click();URL.revokeObjectURL(a.href);
};

document.addEventListener("visibilitychange",()=>{
  if(log) log.push("visibility_change",{visibility_state:document.visibilityState,trial_id:trials?.[idx]?.trial_id??null});
});
