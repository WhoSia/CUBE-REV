import fs from "node:fs";
const packet=JSON.parse(fs.readFileSync(process.argv[2],"utf8"));
const events=fs.readFileSync(process.argv[3],"utf8").trim().split(/\r?\n/).filter(Boolean).map(JSON.parse);
const out=process.argv[4];
if(!out) throw new Error("output required");
const forbidden=["name","email","phone","school_id","ip_address"];
const failures=[];
const sessions=new Map();
for(const e of events){
  for(const k of forbidden) if(Object.prototype.hasOwnProperty.call(e,k)) failures.push("FORBIDDEN_FIELD:"+k);
  if(!sessions.has(e.session_id)) sessions.set(e.session_id,[]);
  sessions.get(e.session_id).push(e);
}
for(const [sid,es] of sessions){
  es.sort((a,b)=>a.event_index-b.event_index);
  if(es[0]?.event_type!=="session_start") failures.push("NO_SESSION_START:"+sid);
  const start=es.find(x=>x.event_type==="session_start");
  if(start?.packet_sha256!==packet.packet_sha256) failures.push("PACKET_HASH:"+sid);
  if(es.at(-1)?.event_type!=="session_complete") failures.push("NO_SESSION_COMPLETE:"+sid);
  let active=null;
  for(const e of es){
    if(e.event_type==="trial_presented"){
      if(active!==null) failures.push("NESTED_TRIAL:"+sid);
      active=e.trial_id;
    }else if(e.event_type==="choice_committed"){
      if(active!==e.trial_id) failures.push("CHOICE_WITHOUT_MATCHING_PRESENT:"+sid);
      if(!(Number(e.latency_ms)>=0)) failures.push("LATENCY:"+sid);
    }else if(e.event_type==="trial_complete"){
      if(active!==e.trial_id) failures.push("COMPLETE_WITHOUT_ACTIVE:"+sid);
      active=null;
    }
  }
  if(active!==null) failures.push("OPEN_TRIAL_AT_END:"+sid);
}
const report={schema_version:"g7-p5-event-integrity-1",pass:failures.length===0,failures,sessions:sessions.size,events:events.length};
fs.writeFileSync(out,JSON.stringify(report,null,2)+"\n");
if(failures.length){console.error(failures.join("\n"));process.exit(1);}
console.log("G7_P5_EVENT_INTEGRITY_PASS");
console.log("SESSIONS\t"+sessions.size);
console.log("EVENTS\t"+events.length);
