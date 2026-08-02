(function(global){
'use strict';

const VERSION='CUBE-REV 0.8.11';
const HEX64=/^[0-9a-f]{64}$/;
const FORBIDDEN=new Set([
  'state_id','rotation_id','face_map','choice_canonical','canonical_move',
  'pair_id','member_id','probe_name','diagnostic_class','branch_count',
  'branch_level','decision_class','distance'
]);

function canonicalText(text){return JSON.stringify(JSON.parse(text))}
function hex(bytes){return Array.from(new Uint8Array(bytes),x=>x.toString(16).padStart(2,'0')).join('')}
async function sha256Text(text,cryptoObj){
  const c=cryptoObj||global.crypto;
  if(c&&c.subtle&&typeof TextEncoder!=='undefined'){
    return hex(await c.subtle.digest('SHA-256',new TextEncoder().encode(text)));
  }
  if(typeof require!=='undefined')return require('crypto').createHash('sha256').update(text).digest('hex');
  throw new Error('SHA256_UNAVAILABLE');
}
function assertNoForbidden(value,trail='$'){
  if(Array.isArray(value)){value.forEach((v,i)=>assertNoForbidden(v,`${trail}[${i}]`));return}
  if(!value||typeof value!=='object')return;
  for(const [key,v] of Object.entries(value)){
    if(FORBIDDEN.has(key))throw new Error(`FORBIDDEN_PUBLIC_FIELD:${trail}.${key}`);
    assertNoForbidden(v,`${trail}.${key}`);
  }
}
function countCodes(bank){
  const codes=new Set();
  for(const stimulus of bank.stimuli||[]){
    const entries=Object.entries(stimulus.choice_codes||{});
    if(entries.length!==18)throw new Error(`CHOICE_COUNT:${stimulus.stimulus_id}`);
    for(const [,code] of entries){
      if(!/^CR9C-[0-9a-f]{16}$/.test(code))throw new Error(`CHOICE_CODE_INVALID:${code}`);
      if(codes.has(code))throw new Error(`CHOICE_CODE_DUPLICATE:${code}`);
      codes.add(code);
    }
  }
  return codes.size;
}
function assertSchedules(bank,config){
  const ids=new Set((bank.stimuli||[]).map(x=>x.stimulus_id));
  if(ids.size!==28)throw new Error('STIMULUS_CARDINALITY');
  const schedules=config.schedules||{};
  if(Object.keys(schedules).length!==24)throw new Error('SEQUENCE_CARDINALITY');
  for(const [sid,schedule] of Object.entries(schedules)){
    if(!Array.isArray(schedule)||schedule.length!==28)throw new Error(`SCHEDULE_LENGTH:${sid}`);
    if(new Set(schedule).size!==28||schedule.some(x=>!ids.has(x)))throw new Error(`SCHEDULE_MEMBERSHIP:${sid}`);
  }
}
function assertAtomicConfig(config){
  const r=config.resume||{},m=config.migration||{};
  if(r.web_locks_required!==true||r.migration_lock_name!=='cube-rev-migration-0811-exclusive-v1')throw new Error('LOCK_POLICY_INVALID');
  for(const key of ['migration_journal_key','migration_epoch_key','migration_owner_key','migration_fence_key','migration_quarantine_key']){
    if(typeof r[key]!=='string'||!r[key])throw new Error(`RESUME_KEY_MISSING:${key}`);
  }
  const expected=['PREPARED','TARGET_WRITTEN','ARCHIVE_WRITTEN','FENCE_WRITTEN','COMMITTED','ROLLED_BACK','ROLLED_BACK_TO_LEGACY'];
  if(!Array.isArray(m.journal_phases)||m.journal_phases.join('|')!==expected.join('|'))throw new Error('JOURNAL_PHASES_INVALID');
  if(m.lock_policy!=='WEB_LOCKS_FAIL_CLOSED_V1'||m.fencing_policy!=='MONOTONIC_EPOCH_OWNER_TOKEN_V1')throw new Error('FENCING_POLICY_INVALID');
  const p=m.parent_0810_asset_binding||{};
  for(const key of ['manifest_sha256','public_bank_sha256','public_config_sha256','private_crosswalk_sha256'])if(!HEX64.test(p[key]||''))throw new Error(`PARENT_BINDING_INVALID:${key}`);
}
async function verifyBundle(o){
  if(!o||!o.pins)throw new Error('ASSET_PINS_REQUIRED');
  const pins=o.pins;
  for(const key of ['manifest_sha256','public_bank_sha256','public_config_sha256','parent_manifest_sha256','private_crosswalk_sha256']){
    if(!HEX64.test(pins[key]||''))throw new Error(`PIN_INVALID:${key}`);
  }
  const manifestText=canonicalText(o.manifestText),bankText=canonicalText(o.bankText),configText=canonicalText(o.configText);
  const [manifestHash,bankHash,configHash]=await Promise.all([
    sha256Text(manifestText,o.cryptoObj),sha256Text(bankText,o.cryptoObj),sha256Text(configText,o.cryptoObj)
  ]);
  if(manifestHash!==pins.manifest_sha256)throw new Error('MANIFEST_PIN_MISMATCH');
  if(bankHash!==pins.public_bank_sha256)throw new Error('PUBLIC_BANK_PIN_MISMATCH');
  if(configHash!==pins.public_config_sha256)throw new Error('PUBLIC_CONFIG_PIN_MISMATCH');
  const manifest=JSON.parse(manifestText),bank=JSON.parse(bankText),config=JSON.parse(configText);
  if(manifest.version!==VERSION||manifest.schema_version!=='CR0811-ASSET-MANIFEST-1')throw new Error('MANIFEST_IDENTITY');
  if(bank.version!==VERSION||bank.schema_version!=='CR0811-PUBLIC-STIMULUS-BANK-1')throw new Error('BANK_IDENTITY');
  if(config.version!==VERSION||config.schema_version!=='CR0811-COGNITIVE-MODE-CONFIG-1')throw new Error('CONFIG_IDENTITY');
  if(manifest.public_bank_sha256!==bankHash||manifest.public_config_sha256!==configHash)throw new Error('MANIFEST_ASSET_DISAGREEMENT');
  if(manifest.parent_manifest_sha256!==pins.parent_manifest_sha256)throw new Error('PARENT_MANIFEST_PIN_MISMATCH');
  if(manifest.private_crosswalk_sha256!==pins.private_crosswalk_sha256)throw new Error('PRIVATE_CROSSWALK_PIN_MISMATCH');
  if(manifest.response_encoding!=='OPAQUE_CHOICE_CODE_V1'||bank.response_encoding!=='OPAQUE_CHOICE_CODE_V1')throw new Error('RESPONSE_ENCODING_MISMATCH');
  if(manifest.arbitration!=='WEB_LOCKS_EXCLUSIVE_WITH_MONOTONIC_FENCING_EPOCH_V1')throw new Error('ARBITRATION_IDENTITY');
  assertNoForbidden(bank);assertSchedules(bank,config);assertAtomicConfig(config);
  const codeCount=countCodes(bank);
  if(codeCount!==504||manifest.choice_code_count!==504)throw new Error('CHOICE_CODE_CARDINALITY');
  return {
    manifest,bank,config,
    binding:{manifest_sha256:manifestHash,public_bank_sha256:bankHash,public_config_sha256:configHash,private_crosswalk_sha256:pins.private_crosswalk_sha256},
    parent0810Binding:{...config.migration.parent_0810_asset_binding}
  };
}

const api={VERSION,FORBIDDEN,canonicalText,sha256Text,assertNoForbidden,countCodes,assertSchedules,assertAtomicConfig,verifyBundle};
if(typeof module!=='undefined'&&module.exports)module.exports=api;
global.CUBE_REV_PUBLIC_ASSET_VERIFIER_0811=api;
})(typeof window!=='undefined'?window:globalThis);
