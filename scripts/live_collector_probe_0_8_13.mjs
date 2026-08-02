import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {createRequire} from 'node:module';

const ROOT=path.resolve(path.dirname(new URL(import.meta.url).pathname),'..');
const require=createRequire(import.meta.url);
require('../js/public-asset-verifier-0.8.13.js');
const M=require('../js/participant-cognitive-mode-0.8.13.js');
const configText=fs.readFileSync(path.join(ROOT,'collector-config.js'),'utf8');
const endpoint=(configText.match(/endpoint:\s*'([^']+)'/)||[])[1];
if(!endpoint)throw new Error('COLLECTOR_ENDPOINT_NOT_FOUND');
const snapshotPath=process.argv[2]||path.join(ROOT,'artifacts/0.8.13/live_synthetic_snapshot.json');
const evidencePath=process.argv[3]||path.join(ROOT,'artifacts/0.8.13/live_collector_evidence.json');
const snapshotText=fs.readFileSync(snapshotPath,'utf8');
const snapshot=JSON.parse(snapshotText);
if(snapshot.version!=='CUBE-REV 0.8.13'||snapshot.schema_version!=='CR0813-COLLECTOR-PAYLOAD-1')throw new Error('SNAPSHOT_IDENTITY');
const snapshotSha256=crypto.createHash('sha256').update(snapshotText).digest('hex');
const collectorEnvelope=M.collectorEnvelopeFromSnapshot(snapshot,{
  generated_at:'2026-08-02T11:00:30.000Z',
  status:'engineering_synthetic_live_cert',
  synthetic_live_cert:true,
  exclude_from_human_cohort:true,
  immutable_snapshot_sha256:snapshotSha256
});
const collectorPayloadText=JSON.stringify(collectorEnvelope);
const collectorPayloadSha256=crypto.createHash('sha256').update(collectorPayloadText).digest('hex');

function fnv1a(s){let h=0x811c9dc5;for(let i=0;i<s.length;i++){h^=s.charCodeAt(i);h=Math.imul(h,0x01000193)}return h>>>0}
function parseJsonp(text,callback){const prefix=`${callback}(`,trim=text.trim();if(!trim.startsWith(prefix)||!trim.endsWith(');'))throw new Error(`JSONP_PARSE:${trim.slice(0,120)}`);return JSON.parse(trim.slice(prefix.length,-2))}
async function jsonp(params,callback){const url=new URL(endpoint);for(const [k,v] of Object.entries({...params,callback,_:Date.now()}))url.searchParams.set(k,String(v));const r=await fetch(url,{redirect:'follow',signal:AbortSignal.timeout(20000)});const text=await r.text();if(!r.ok)throw new Error(`GET_${r.status}:${text.slice(0,200)}`);return parseJsonp(text,callback)}
async function health(){const p=await jsonp({action:'health',collector_id:'CUBE-REV-0712-MAIN',protocol_version:'receipt-v2',version:'0.7.12'},'cr0813Health');if(p.ok!==true||p.collector_id!=='CUBE-REV-0712-MAIN'||p.protocol_version!=='receipt-v2'||p.expected_version!=='0.7.12')throw new Error(`HEALTH_CONTRACT:${JSON.stringify(p)}`);return p}
async function post(nonce){
  if(!/^[0-9a-f]{24}$/.test(nonce))throw new Error(`NONCE_FORMAT:${nonce}`);
  const checksum=fnv1a(collectorPayloadText).toString(16).padStart(8,'0');
  const fields={payload:collectorPayloadText,encoding:'json',study_id:'CUBE-REV-0.7.12',collector_id:'CUBE-REV-0712-MAIN',protocol_version:'receipt-v2',session_id:collectorEnvelope.session_id,version:'0.7.12',checksum_fnv1a32:checksum,original_bytes:Buffer.byteLength(collectorPayloadText),submission_nonce:nonce};
  const r=await fetch(endpoint,{method:'POST',headers:{'content-type':'application/x-www-form-urlencoded;charset=UTF-8'},body:new URLSearchParams(fields),redirect:'follow',signal:AbortSignal.timeout(30000)});const body=await r.text();if(!r.ok)throw new Error(`POST_${r.status}:${body.slice(0,200)}`);return {fields,response_status:r.status,response_url:r.url,response_body_prefix:body.slice(0,120)};
}
async function receipt(nonce,checksum){const deadline=Date.now()+90000;let polls=0;while(Date.now()<deadline){polls++;const p=await jsonp({action:'receipt',submission_nonce:nonce,session_id:collectorEnvelope.session_id,collector_id:'CUBE-REV-0712-MAIN',protocol_version:'receipt-v2',version:'0.7.12'},`cr0813Receipt${polls}`);if(p.status==='pending'){await new Promise(r=>setTimeout(r,1500));continue}if(p.ok===true&&['stored','duplicate'].includes(p.status)&&String(p.checksum_fnv1a32||'').toLowerCase()===checksum)return {...p,polls};throw new Error(`RECEIPT_CONTRACT:${JSON.stringify(p)}`)}throw new Error('RECEIPT_TIMEOUT')}

const startedAt=new Date().toISOString(),h=await health();
const nonceA='0813a0000000000000000001',nonceB='0813b0000000000000000002';
const a=await post(nonceA),ra=await receipt(nonceA,a.fields.checksum_fnv1a32);
const b=await post(nonceB),rb=await receipt(nonceB,b.fields.checksum_fnv1a32);
if(a.fields.checksum_fnv1a32!==b.fields.checksum_fnv1a32)throw new Error('CHECKSUM_DIVERGENCE');
if(rb.status!=='duplicate')throw new Error(`SECOND_DELIVERY_NOT_DUPLICATE:${rb.status}`);
const evidence={schema_version:'CR0813-LIVE-COLLECTOR-EVIDENCE-1',started_at:startedAt,completed_at:new Date().toISOString(),endpoint_origin:new URL(endpoint).origin,endpoint_sha256:crypto.createHash('sha256').update(endpoint).digest('hex'),health:{ok:h.ok,collector_id:h.collector_id,protocol_version:h.protocol_version,expected_version:h.expected_version,deployment_id:h.deployment_id||null,receipt_confirmation_available:h.receipt_confirmation_available===true},collector_envelope:{schema_version:'CR0813-COLLECTOR-COMPATIBILITY-ENVELOPE-1',project:collectorEnvelope.project,version:collectorEnvelope.version,session_id:collectorEnvelope.session_id,original_scientific_session_id:collectorEnvelope.data_submission.original_scientific_session_id,transport_session_policy:collectorEnvelope.data_submission.transport_session_policy,trial_count:collectorEnvelope.trials.length,sha256:collectorPayloadSha256,checksum_fnv1a32:a.fields.checksum_fnv1a32,bytes:Buffer.byteLength(collectorPayloadText)},snapshot:{session_id:snapshot.session_id,schema_version:snapshot.schema_version,version:snapshot.version,response_count:snapshot.responses.length,sha256:snapshotSha256},deliveries:[{nonce:nonceA,status:ra.status,receipt_code:ra.receipt_code||null,file_name:ra.file_name||null,polls:ra.polls},{nonce:nonceB,status:rb.status,receipt_code:rb.receipt_code||null,file_name:rb.file_name||null,polls:rb.polls}],result:'PASS_LIVE_COLLECTOR_TWO_NONCE_DEDUP'};
fs.mkdirSync(path.dirname(evidencePath),{recursive:true});fs.writeFileSync(evidencePath,JSON.stringify(evidence,null,2));
console.log(`CR0813_LIVE_COLLECTOR_PASS first=${ra.status} second=${rb.status} file=${rb.file_name||ra.file_name} envelope=${collectorPayloadSha256} snapshot=${snapshotSha256}`);
