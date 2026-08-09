(function(global){
'use strict';

const VERSION='CUBE-REV 0.8.13';
const HEX64=/^[0-9a-f]{64}$/;
const TRANSPORT_SESSION_RE=/^CR-[0-9]{14}-[0-9a-f]{12}$/;
const FORBIDDEN=new Set(['state_id','rotation_id','face_map','choice_canonical','canonical_move','pair_id','member_id','probe_name','diagnostic_class','branch_count','branch_level','decision_class','distance']);
function canonicalText(text){return JSON.stringify(JSON.parse(text))}
function hex(bytes){return Array.from(new Uint8Array(bytes),x=>x.toString(16).padStart(2,'0')).join('')}
async function sha256Text(text,cryptoObj){
  const c=cryptoObj||global.crypto;
  if(c&&c.subtle&&typeof TextEncoder!=='undefined')return hex(await c.subtle.digest('SHA-256',new TextEncoder().encode(text)));
  if(typeof require!=='undefined')return require('crypto').createHash('sha256').update(text).digest('hex');
  throw new Error('SHA256_UNAVAILABLE');
}
function assertNoForbidden(value,trail='$'){
  if(Array.isArray(value)){value.forEach((v,i)=>assertNoForbidden(v,`${trail}[${i}]`));return}
  if(!value||typeof value!=='object')return;
  for(const [key,v] of Object.entries(value)){if(FORBIDDEN.has(key))throw new Error(`FORBIDDEN_PUBLIC_FIELD:${trail}.${key}`);assertNoForbidden(v,`${trail}.${key}`)}
}
function countCodes(bank){
  const codes=new Set();
  for(const stimulus of bank.stimuli||[]){
    const entries=Object.entries(stimulus.choice_codes||{});if(entries.length!==18)throw new Error(`CHOICE_COUNT:${stimulus.stimulus_id}`);
    for(const [,code] of entries){if(!/^CR9C-[0-9a-f]{16}$/.test(code))throw new Error(`CHOICE_CODE_INVALID:${code}`);if(codes.has(code))throw new Error(`CHOICE_CODE_DUPLICATE:${code}`);codes.add(code)}
  }
  return codes.size;
}
function assertSchedules(bank,config){
  const ids=new Set((bank.stimuli||[]).map(x=>x.stimulus_id));if(ids.size!==28)throw new Error('STIMULUS_CARDINALITY');
  const schedules=config.schedules||{};if(Object.keys(schedules).length!==24)throw new Error('SEQUENCE_CARDINALITY');
  for(const [sid,schedule] of Object.entries(schedules)){if(!Array.isArray(schedule)||schedule.length!==28)throw new Error(`SCHEDULE_LENGTH:${sid}`);if(new Set(schedule).size!==28||schedule.some(x=>!ids.has(x)))throw new Error(`SCHEDULE_MEMBERSHIP:${sid}`)}
}
function assertActiveConfig(config){
  const r=config.resume||{},a=config.active_session||{};
  if(r.active_write_lock_required!==true||r.active_write_lock_name!=='cube-rev-session-write-0813-exclusive-v1')throw new Error('ACTIVE_LOCK_POLICY_INVALID');
  for(const key of ['active_write_journal_key','active_write_conflict_key','storage_key','quarantine_key','native_browser_evidence_key'])if(typeof r[key]!=='string'||!r[key])throw new Error(`ACTIVE_KEY_MISSING:${key}`);
  if(a.operation_dispatcher!=='REVISION_CAS_OPERATION_DISPATCHER_V2_NATIVE_BROWSER')throw new Error('DISPATCHER_POLICY_INVALID');
  if(a.revision_policy!=='STRICT_MONOTONIC_INCREMENT_BY_ONE_V1')throw new Error('REVISION_POLICY_INVALID');
  if(a.scientific_write_policy!=='EXPECTED_REVISION_REQUIRED_V1')throw new Error('SCIENTIFIC_WRITE_POLICY_INVALID');
  if(a.telemetry_policy!=='LOCKED_APPEND_MERGE_ON_LATEST_REVISION_V1')throw new Error('TELEMETRY_POLICY_INVALID');
  if(a.submission_policy!=='LEASE_TOKEN_SINGLE_NETWORK_OWNER_V1')throw new Error('SUBMISSION_POLICY_INVALID');
  if(a.native_browser_contract!=='TWO_PAGE_SAME_ORIGIN_WEB_LOCKS_STORAGE_EVENT_V1')throw new Error('NATIVE_BROWSER_POLICY_INVALID');
  if(a.delayed_network_contract!=='TWO_NONCE_SAME_SNAPSHOT_RECEIPT_DEDUP_V1')throw new Error('DELAYED_NETWORK_POLICY_INVALID');
  if(a.factory_adapter_contract!=='CR0813_COGNITIVE_SNAPSHOT_FACTORY_ADAPTER_V1')throw new Error('FACTORY_POLICY_INVALID');
  if(!Number.isInteger(a.lease_timeout_ms)||a.lease_timeout_ms<30000)throw new Error('LEASE_TIMEOUT_INVALID');
  const p=a.parent_asset_binding||{};for(const key of ['manifest_sha256','public_bank_sha256','public_config_sha256','private_crosswalk_sha256'])if(!HEX64.test(p[key]||''))throw new Error(`PARENT_BINDING_INVALID:${key}`);
}
async function verifyBundle(o){
  if(!o||!o.pins)throw new Error('ASSET_PINS_REQUIRED');const pins=o.pins;
  for(const key of ['manifest_sha256','public_bank_sha256','public_config_sha256','parent_manifest_sha256','private_crosswalk_sha256'])if(!HEX64.test(pins[key]||''))throw new Error(`PIN_INVALID:${key}`);
  const manifestText=canonicalText(o.manifestText),bankText=canonicalText(o.bankText),configText=canonicalText(o.configText);
  const [manifestHash,bankHash,configHash]=await Promise.all([sha256Text(manifestText,o.cryptoObj),sha256Text(bankText,o.cryptoObj),sha256Text(configText,o.cryptoObj)]);
  if(manifestHash!==pins.manifest_sha256)throw new Error('MANIFEST_PIN_MISMATCH');
  if(bankHash!==pins.public_bank_sha256)throw new Error('PUBLIC_BANK_PIN_MISMATCH');
  if(configHash!==pins.public_config_sha256)throw new Error('PUBLIC_CONFIG_PIN_MISMATCH');
  const manifest=JSON.parse(manifestText),bank=JSON.parse(bankText),config=JSON.parse(configText);
  if(manifest.version!==VERSION||manifest.schema_version!=='CR0813-ASSET-MANIFEST-1')throw new Error('MANIFEST_IDENTITY');
  if(bank.version!==VERSION||bank.schema_version!=='CR0813-PUBLIC-STIMULUS-BANK-1')throw new Error('BANK_IDENTITY');
  if(config.version!==VERSION||config.schema_version!=='CR0813-COGNITIVE-MODE-CONFIG-1')throw new Error('CONFIG_IDENTITY');
  if(manifest.public_bank_sha256!==bankHash||manifest.public_config_sha256!==configHash)throw new Error('MANIFEST_ASSET_DISAGREEMENT');
  if(manifest.parent_manifest_sha256!==pins.parent_manifest_sha256)throw new Error('PARENT_MANIFEST_PIN_MISMATCH');
  if(manifest.private_crosswalk_sha256!==pins.private_crosswalk_sha256)throw new Error('PRIVATE_CROSSWALK_PIN_MISMATCH');
  if(manifest.response_encoding!=='OPAQUE_CHOICE_CODE_V1'||bank.response_encoding!=='OPAQUE_CHOICE_CODE_V1')throw new Error('RESPONSE_ENCODING_MISMATCH');
  if(manifest.active_session_serialization!=='NATIVE_WEB_LOCKS_EXCLUSIVE_REVISION_CAS_V2')throw new Error('ACTIVE_SERIALIZATION_IDENTITY');
  assertNoForbidden(bank);assertSchedules(bank,config);assertActiveConfig(config);
  const codeCount=countCodes(bank);if(codeCount!==504||manifest.choice_code_count!==504)throw new Error('CHOICE_CODE_CARDINALITY');
  return {manifest,bank,config,binding:{manifest_sha256:manifestHash,public_bank_sha256:bankHash,public_config_sha256:configHash,private_crosswalk_sha256:pins.private_crosswalk_sha256},parent0812Binding:{...config.active_session.parent_asset_binding}};
}

function assertTransportEnvelope(envelope,snapshot,m){
  if(!envelope||typeof envelope!=='object')throw new Error('COLLECTOR_ENVELOPE_REQUIRED');
  if(!snapshot||typeof snapshot!=='object')throw new Error('SCIENTIFIC_SNAPSHOT_REQUIRED');
  if(typeof m.transportSessionIdentity!=='function')throw new Error('TRANSPORT_IDENTITY_API_MISSING');
  const expected=m.transportSessionIdentity(snapshot),data=envelope.data_submission||{};
  if(!TRANSPORT_SESSION_RE.test(String(envelope.session_id||'')))throw new Error('COLLECTOR_TRANSPORT_SESSION_INVALID');
  if(envelope.session_id!==expected.session_id)throw new Error('COLLECTOR_TRANSPORT_SESSION_MISMATCH');
  if(envelope.original_scientific_session_id!==snapshot.session_id||data.original_scientific_session_id!==snapshot.session_id)throw new Error('COLLECTOR_SCIENTIFIC_SESSION_MISMATCH');
  if(envelope.transport_session_policy!==expected.transport_session_policy||data.transport_session_policy!==expected.transport_session_policy)throw new Error('COLLECTOR_TRANSPORT_POLICY_MISMATCH');
  if(data.transport_session_id!==expected.session_id)throw new Error('COLLECTOR_DATA_TRANSPORT_SESSION_MISMATCH');
  if(envelope.cognitive_snapshot!==snapshot&&JSON.stringify(envelope.cognitive_snapshot)!==JSON.stringify(snapshot))throw new Error('COLLECTOR_SNAPSHOT_IDENTITY_MISMATCH');
  return envelope;
}
function augmentCognitiveApi(m){
  if(!m||m.__collector_transport_bridge_0813===true)return m;
  const baseEnvelope=m.collectorEnvelopeFromSnapshot;
  if(typeof baseEnvelope!=='function'||typeof m.scientificSnapshot!=='function'||typeof m.transportSessionIdentity!=='function')return m;
  m.assertTransportEnvelope=(envelope,snapshot)=>assertTransportEnvelope(envelope,snapshot,m);
  m.collectorEnvelopeFromSnapshot=function(snapshot,options={}){
    return assertTransportEnvelope(baseEnvelope(snapshot,options),snapshot,m);
  };
  m.exportSnapshot=function(state){
    const snapshot=m.scientificSnapshot(state);
    return m.collectorEnvelopeFromSnapshot(snapshot,{immutable_snapshot_integrity_fnv1a32:state.submission_snapshot_hash});
  };
  m.__collector_transport_bridge_0813=true;

  const Base=global.CubeRevCollectorClient;
  if(typeof Base==='function'&&Base.__cr0813_transport_bridge!==true){
    class CubeRevCollectorClient0813 extends Base{
      constructor(options){
        const originalGetSession=options.getSession;
        const originalExportSession=options.exportSession;
        super({...options,
          getSession:()=>{
            const session=originalGetSession();
            if(session&&!TRANSPORT_SESSION_RE.test(String(session.session_id||'')))throw new Error('COLLECTOR_SESSION_VIEW_INVALID');
            return session;
          },
          exportSession:()=>{
            const exported=originalExportSession();
            if(!exported||!TRANSPORT_SESSION_RE.test(String(exported.session_id||'')))throw new Error('COLLECTOR_TRANSPORT_SESSION_INVALID');
            const snapshot=exported.cognitive_snapshot;
            return assertTransportEnvelope(exported,snapshot,m);
          }
        });
      }
    }
    CubeRevCollectorClient0813.__cr0813_transport_bridge=true;
    global.CubeRevCollectorClient=CubeRevCollectorClient0813;
  }
  return m;
}
function installCognitiveBridge(){
  const key='CUBE_REV_COGNITIVE_MODE_0813';
  if(global[key]){augmentCognitiveApi(global[key]);return}
  let value;
  Object.defineProperty(global,key,{configurable:true,enumerable:true,get(){return value},set(v){value=augmentCognitiveApi(v)}});
}
installCognitiveBridge();

const api={VERSION,FORBIDDEN,TRANSPORT_SESSION_RE,canonicalText,sha256Text,assertNoForbidden,countCodes,assertSchedules,assertActiveConfig,verifyBundle,assertTransportEnvelope,augmentCognitiveApi};
if(typeof module!=='undefined'&&module.exports)module.exports=api;
global.CUBE_REV_PUBLIC_ASSET_VERIFIER_0813=api;
})(typeof window!=='undefined'?window:globalThis);
