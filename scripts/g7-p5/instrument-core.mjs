import crypto from "node:crypto";

export function verifyPacket(packet){
  const {packet_sha256,...core}=packet;
  const actual=crypto.createHash("sha256").update(JSON.stringify(core)).digest("hex");
  if(actual!==packet_sha256) throw new Error("PACKET_HASH_MISMATCH");
  if(packet.human_contact_authority!=="HOLD_UNTIL_INSTRUMENT_VALIDATED") throw new Error("CONTACT_AUTHORITY");
  if(packet.trials.length!==24) throw new Error("TRIAL_COUNT");
  return true;
}
export function shuffledTrials(packet,sessionId){
  const key=crypto.createHash("sha256").update(packet.packet_sha256+"|"+sessionId).digest();
  let s=key.readUInt32LE(0)>>>0;
  const rand=()=>{s=(Math.imul(s,1664525)+1013904223)>>>0;return s/2**32;};
  const a=[...packet.trials];
  for(let i=a.length-1;i>0;i--){const j=Math.floor(rand()*(i+1));[a[i],a[j]]=[a[j],a[i]];}
  return a;
}
export class EventLog{
  constructor({sessionId,packet,clock=()=>performance.now()}){
    verifyPacket(packet);
    this.sessionId=sessionId;this.packet=packet;this.clock=clock;this.events=[];this.t0=null;
  }
  push(type,data={}){
    const t=this.clock();
    const e={event_index:this.events.length,event_type:type,session_id:this.sessionId,monotonic_ms:t,...data};
    this.events.push(e);return e;
  }
  start(consentStatus="SYNTHETIC_ONLY"){
    return this.push("session_start",{packet_sha256:this.packet.packet_sha256,instrument_version:this.packet.instrument_version,consent_status:consentStatus});
  }
  present(trial){
    this.t0=this.clock();
    return this.push("trial_presented",{trial_id:trial.trial_id,pair_id:trial.pair_id,state_id:trial.state_id,
      condition_id:trial.condition.display_horizon_condition,representation_family:"BLINDED",
      display_horizon_condition:trial.condition.display_horizon_condition,slack_band:`LB${trial.phase1_lb}`,
      choice_order_seed:trial.condition.choice_order_seed});
  }
  choose(trial,choiceToken,confidenceOrdinal=null){
    if(this.t0===null) throw new Error("TRIAL_NOT_PRESENTED");
    const latency=this.clock()-this.t0;
    return this.push("choice_committed",{trial_id:trial.trial_id,pair_id:trial.pair_id,state_id:trial.state_id,
      choice_token:choiceToken,latency_ms:latency,confidence_ordinal:confidenceOrdinal});
  }
  complete(trial){this.t0=null;return this.push("trial_complete",{trial_id:trial.trial_id});}
  finish(){return this.push("session_complete",{trial_count:this.packet.trials.length});}
  jsonl(){return this.events.map(JSON.stringify).join("\n")+"\n";}
}
