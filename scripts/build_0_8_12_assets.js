'use strict';

const fs=require('fs');
const path=require('path');
const crypto=require('crypto');

const VERSION='CUBE-REV 0.8.12';
const BANK_SCHEMA='CR0812-PUBLIC-STIMULUS-BANK-1';
const CONFIG_SCHEMA='CR0812-COGNITIVE-MODE-CONFIG-1';
const MANIFEST_SCHEMA='CR0812-ASSET-MANIFEST-1';

function readJson(file){return JSON.parse(fs.readFileSync(file,'utf8'))}
function writeText(file,text){fs.mkdirSync(path.dirname(file),{recursive:true});fs.writeFileSync(file,text)}
function writeJson(file,value){writeText(file,JSON.stringify(value)+'\n')}
function canonical(value){return JSON.stringify(value)}
function sha256(value){return crypto.createHash('sha256').update(typeof value==='string'?value:canonical(value)).digest('hex')}
function clone(value){return JSON.parse(JSON.stringify(value))}

function assertParent(bank,config,manifest){
  if(bank.version!=='CUBE-REV 0.8.11'||bank.schema_version!=='CR0811-PUBLIC-STIMULUS-BANK-1')throw new Error('PARENT_BANK_IDENTITY');
  if(config.version!=='CUBE-REV 0.8.11'||config.schema_version!=='CR0811-COGNITIVE-MODE-CONFIG-1')throw new Error('PARENT_CONFIG_IDENTITY');
  if(manifest.version!=='CUBE-REV 0.8.11'||manifest.schema_version!=='CR0811-ASSET-MANIFEST-1')throw new Error('PARENT_MANIFEST_IDENTITY');
  if(sha256(bank)!==manifest.public_bank_sha256)throw new Error('PARENT_BANK_HASH_MISMATCH');
  if(sha256(config)!==manifest.public_config_sha256)throw new Error('PARENT_CONFIG_HASH_MISMATCH');
  if(!/^[0-9a-f]{64}$/.test(manifest.private_crosswalk_sha256||''))throw new Error('PARENT_PRIVATE_HASH_INVALID');
  if(!Array.isArray(bank.stimuli)||bank.stimuli.length!==28)throw new Error('PARENT_STIMULUS_COUNT');
  if(!config.schedules||Object.keys(config.schedules).length!==24)throw new Error('PARENT_SEQUENCE_COUNT');
}

function build(parentBank,parentConfig,parentManifest){
  assertParent(parentBank,parentConfig,parentManifest);
  const parentBinding={
    manifest_sha256:sha256(parentManifest),
    public_bank_sha256:parentManifest.public_bank_sha256,
    public_config_sha256:parentManifest.public_config_sha256,
    private_crosswalk_sha256:parentManifest.private_crosswalk_sha256
  };

  const publicBank=clone(parentBank);
  publicBank.schema_version=BANK_SCHEMA;
  publicBank.version=VERSION;
  publicBank.source_bundle={
    version:'CUBE-REV 0.8.11',
    manifest_sha256:parentBinding.manifest_sha256,
    public_bank_sha256:parentBinding.public_bank_sha256,
    opaque_choice_code_count:parentManifest.choice_code_count
  };

  const publicConfig=clone(parentConfig);
  publicConfig.schema_version=CONFIG_SCHEMA;
  publicConfig.version=VERSION;
  publicConfig.participant_route='participant-cognitive-mode-0.8.12.html';
  publicConfig.resume={
    ...publicConfig.resume,
    storage_key:'cube-rev-cognitive-mode-0812-v1',
    quarantine_key:'cube-rev-cognitive-mode-0812-quarantine-v1',
    active_write_lock_name:'cube-rev-session-write-0812-exclusive-v1',
    active_write_journal_key:'cube-rev-session-write-0812-journal-v1',
    active_write_conflict_key:'cube-rev-session-write-0812-conflicts-v1',
    active_write_lock_required:true
  };
  publicConfig.active_session={
    parent_version:'CUBE-REV 0.8.11',
    parent_storage_key:'cube-rev-cognitive-mode-0811-v1',
    parent_asset_binding:parentBinding,
    operation_dispatcher:'REVISION_CAS_OPERATION_DISPATCHER_V1',
    revision_policy:'STRICT_MONOTONIC_INCREMENT_BY_ONE_V1',
    scientific_write_policy:'EXPECTED_REVISION_REQUIRED_V1',
    stale_write_policy:'REJECT_WITHOUT_STATE_MUTATION_V1',
    response_conflict_policy:'ONE_WINNER_QUARANTINE_LOSER_EVIDENCE_V1',
    telemetry_policy:'LOCKED_APPEND_MERGE_ON_LATEST_REVISION_V1',
    snapshot_policy:'IMMUTABLE_SCIENTIFIC_ENVELOPE_RETRY_STABLE_V2',
    submission_policy:'LEASE_TOKEN_SINGLE_NETWORK_OWNER_V1',
    collector_metadata_policy:'LEASE_AUTHORIZED_AUXILIARY_MERGE_V1',
    lease_timeout_ms:120000,
    mutation_history_limit:256,
    conflict_history_limit:64,
    source_state_preserved:true,
    sealed_parent_policy:'PARENT_VERSION_RETRY_ONLY'
  };
  publicConfig.assets={
    manifest_path:'research/CUBE_REV_0.8.12_ASSET_MANIFEST.json',
    public_bank_path:'cognitive/PARTICIPANT_STIMULUS_BANK_0.8.12.json',
    public_config_path:'cognitive/COGNITIVE_MODE_CONFIG_0.8.12.json',
    hash_algorithm:'SHA-256',
    canonicalization:'JSON_STRINGIFY_PARSED_OBJECT_V1',
    verification_required_before_state_lock:true
  };
  publicConfig.collector={...publicConfig.collector,files_modified:false,collector_contract_version:'0.7.12',app_payload_version:VERSION};

  const manifest={
    schema_version:MANIFEST_SCHEMA,
    version:VERSION,
    canonicalization:'JSON_STRINGIFY_PARSED_OBJECT_V1',
    hash_algorithm:'SHA-256',
    public_bank_path:publicConfig.assets.public_bank_path,
    public_config_path:publicConfig.assets.public_config_path,
    public_bank_sha256:sha256(publicBank),
    public_config_sha256:sha256(publicConfig),
    parent_manifest_sha256:parentBinding.manifest_sha256,
    parent_public_bank_sha256:parentBinding.public_bank_sha256,
    parent_public_config_sha256:parentBinding.public_config_sha256,
    private_crosswalk_sha256:parentBinding.private_crosswalk_sha256,
    response_encoding:'OPAQUE_CHOICE_CODE_V1',
    stimulus_count:publicBank.stimuli.length,
    sequence_count:Object.keys(publicConfig.schedules).length,
    choice_code_count:parentManifest.choice_code_count,
    active_session_serialization:'WEB_LOCKS_EXCLUSIVE_REVISION_CAS_V1',
    response_conflict_control:'ONE_WINNER_STALE_WRITE_REJECT_V1',
    submission_serialization:'LEASE_TOKEN_SINGLE_NETWORK_OWNER_V1'
  };
  const pins={
    schema_version:'CR0812-ASSET-PINS-1',
    version:VERSION,
    manifest_sha256:sha256(manifest),
    public_bank_sha256:manifest.public_bank_sha256,
    public_config_sha256:manifest.public_config_sha256,
    parent_manifest_sha256:manifest.parent_manifest_sha256,
    private_crosswalk_sha256:manifest.private_crosswalk_sha256
  };
  return {publicBank,publicConfig,manifest,pins,parentBinding};
}

function pinModule(pins){
  return `(function(g){'use strict';const p=${JSON.stringify(pins)};if(typeof module!=='undefined'&&module.exports)module.exports=p;g.CUBE_REV_ASSET_PINS_0812=p;})(typeof window!=='undefined'?window:globalThis);\n`;
}

function main(argv=process.argv.slice(2)){
  const root=path.resolve(__dirname,'..');
  const parentBankPath=path.resolve(argv[0]||path.join(root,'cognitive/PARTICIPANT_STIMULUS_BANK_0.8.11.json'));
  const parentConfigPath=path.resolve(argv[1]||path.join(root,'cognitive/COGNITIVE_MODE_CONFIG_0.8.11.json'));
  const parentManifestPath=path.resolve(argv[2]||path.join(root,'research/CUBE_REV_0.8.11_ASSET_MANIFEST.json'));
  const bankPath=path.resolve(argv[3]||path.join(root,'cognitive/PARTICIPANT_STIMULUS_BANK_0.8.12.json'));
  const configPath=path.resolve(argv[4]||path.join(root,'cognitive/COGNITIVE_MODE_CONFIG_0.8.12.json'));
  const manifestPath=path.resolve(argv[5]||path.join(root,'research/CUBE_REV_0.8.12_ASSET_MANIFEST.json'));
  const pinsPath=path.resolve(argv[6]||path.join(root,'js/asset-pins-0.8.12.js'));
  const out=build(readJson(parentBankPath),readJson(parentConfigPath),readJson(parentManifestPath));
  writeJson(bankPath,out.publicBank);
  writeJson(configPath,out.publicConfig);
  writeJson(manifestPath,out.manifest);
  writeText(pinsPath,pinModule(out.pins));
  console.log(`CR0812_ASSET_BUILD_PASS stimuli=${out.manifest.stimulus_count} choices=${out.manifest.choice_code_count}`);
}

if(require.main===module)main();
module.exports={VERSION,BANK_SCHEMA,CONFIG_SCHEMA,MANIFEST_SCHEMA,canonical,sha256,assertParent,build,pinModule};
