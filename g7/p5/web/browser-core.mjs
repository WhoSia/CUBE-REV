export async function sha256Hex(text){
  const buf=await crypto.subtle.digest("SHA-256",new TextEncoder().encode(text));
  return [...new Uint8Array(buf)].map(x=>x.toString(16).padStart(2,"0")).join("");
}
export async function verifyPacketBrowser(packet){
  const {packet_sha256,...core}=packet;
  const actual=await sha256Hex(JSON.stringify(core));
  if(actual!==packet_sha256) throw new Error("PACKET_HASH_MISMATCH");
  if(packet.human_contact_authority!=="HOLD_UNTIL_INSTRUMENT_VALIDATED") throw new Error("CONTACT_AUTHORITY");
  return true;
}
export async function trialOrder(packet,sessionId){
  const hex=await sha256Hex(packet.packet_sha256+"|"+sessionId);
  let s=parseInt(hex.slice(0,8),16)>>>0;
  const rand=()=>{s=(Math.imul(s,1664525)+1013904223)>>>0;return s/2**32;};
  const a=[...packet.trials];
  for(let i=a.length-1;i>0;i--){const j=Math.floor(rand()*(i+1));[a[i],a[j]]=[a[j],a[i]];}
  return a;
}
export class BrowserEventLog{
  constructor(sessionId,packet){this.sessionId=sessionId;this.packet=packet;this.events=[];this.t0=null;}
  push(type,data={}){const e={event_index:this.events.length,event_type:type,session_id:this.sessionId,monotonic_ms:performance.now(),...data};this.events.push(e);return e;}
  start(){return this.push("session_start",{packet_sha256:this.packet.packet_sha256,instrument_version:this.packet.instrument_version,consent_status:"SYNTHETIC_OR_VALIDATION_ONLY"});}
  present(t){this.t0=performance.now();return this.push("trial_presented",{trial_id:t.trial_id,pair_id:t.pair_id,state_id:t.state_id,condition_id:t.condition.display_horizon_condition,representation_family:"BLINDED",display_horizon_condition:t.condition.display_horizon_condition,slack_band:`LB${t.phase1_lb}`,choice_order_seed:t.condition.choice_order_seed});}
  choose(t,choice,confidence=null){if(this.t0===null)throw new Error("NOT_PRESENTED");const latency=performance.now()-this.t0;return this.push("choice_committed",{trial_id:t.trial_id,pair_id:t.pair_id,state_id:t.state_id,choice_token:choice,latency_ms:latency,confidence_ordinal:confidence});}
  complete(t){this.t0=null;return this.push("trial_complete",{trial_id:t.trial_id});}
  finish(){return this.push("session_complete",{trial_count:this.packet.trials.length});}
  jsonl(){return this.events.map(JSON.stringify).join("\n")+"\n";}
}
