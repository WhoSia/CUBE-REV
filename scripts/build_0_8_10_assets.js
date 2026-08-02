'use strict';

const fs=require('fs');
const path=require('path');
const crypto=require('crypto');

const VERSION='CUBE-REV 0.8.10';
const BANK_SCHEMA='CR0810-PUBLIC-STIMULUS-BANK-1';
const CONFIG_SCHEMA='CR0810-COGNITIVE-MODE-CONFIG-1';
const MANIFEST_SCHEMA='CR0810-ASSET-MANIFEST-1';

function readJson(file){return JSON.parse(fs.readFileSync(file,'utf8'))}
function writeText(file,text){fs.mkdirSync(path.dirname(file),{recursive:true});fs.writeFileSync(file,text)}
function writeJson(file,value){writeText(file,JSON.stringify(value)+'\n')}
function canonical(value){return JSON.stringify(value)}
function sha256(value){return crypto.createHash('sha256').update(typeof value==='string'?value:canonical(value)).digest('hex')}
function clone(value){return JSON.parse(JSON.stringify(value))}

function assertParent(bank,config,manifest){
  if(bank.version!=='CUBE-REV 0.8.9'||bank.schema_version!=='CR0809-PUBLIC-STIMULUS-BANK-1')throw new Error('PARENT_BANK_IDENTITY');
  if(config.version!=='CUBE-REV 0.8.9'||config.schema_version!=='CR0809-COGNITIVE-MODE-CONFIG-1')throw new Error('PARENT_CONFIG_IDENTITY');
  if(manifest.version!=='CUBE-REV 0.8.9'||manifest.schema_version!=='CR0809-BUILD-MANIFEST-1')throw new Error('PARENT_MANIFEST_IDENTITY');
  if(sha256(bank)!==manifest.public_bank_sha256)throw new Error('PARENT_BANK_HASH_MISMATCH');
  if(sha256(config)!==manifest.public_config_sha256)throw new Error('PARENT_CONFIG_HASH_MISMATCH');
  if(!/^[0-9a-f]{64}$/.test(manifest.private_crosswalk_sha256||''))throw new Error('PARENT_PRIVATE_HASH_INVALID');
  if(!Array.isArray(bank.stimuli)||bank.stimuli.length!==28)throw new Error('PARENT_STIMULUS_COUNT');
  if(!config.schedules||Object.keys(config.schedules).length!==24)throw new Error('PARENT_SEQUENCE_COUNT');
}

function build(parentBank,parentConfig,parentManifest){
  assertParent(parentBank,parentConfig,parentManifest);
  const publicBank=clone(parentBank);
  publicBank.schema_version=BANK_SCHEMA;
  publicBank.version=VERSION;
  publicBank.source_bundle={
    version:'CUBE-REV 0.8.9',
    public_bank_sha256:parentManifest.public_bank_sha256,
    opaque_choice_code_count:parentManifest.choice_code_count
  };

  const publicConfig=clone(parentConfig);
  publicConfig.schema_version=CONFIG_SCHEMA;
  publicConfig.version=VERSION;
  publicConfig.participant_route='participant-cognitive-mode-0.8.10.html';
  publicConfig.resume={
    storage_key:'cube-rev-cognitive-mode-0810-v1',
    quarantine_key:'cube-rev-cognitive-mode-0810-quarantine-v1',
    telemetry_persisted:true,
    immutable_submission_snapshot:true,
    migration_journal_key:'cube-rev-migration-0810-v1',
    legacy_archive_prefix:'cube-rev-migrated-legacy-0810-'
  };
  publicConfig.migration={
    source_versions:['CUBE-REV 0.8.8','CUBE-REV 0.8.9'],
    source_storage_keys:['cube-rev-cognitive-mode-0808-v1','cube-rev-cognitive-mode-0809-v1'],
    assignment_continuity_required:true,
    source_state_preserved:true,
    sealed_legacy_policy:'LEGACY_VERSION_RETRY_ONLY',
    rollback_on_target_validation_failure:true
  };
  publicConfig.assets={
    manifest_path:'research/CUBE_REV_0.8.10_ASSET_MANIFEST.json',
    public_bank_path:'cognitive/PARTICIPANT_STIMULUS_BANK_0.8.10.json',
    public_config_path:'cognitive/COGNITIVE_MODE_CONFIG_0.8.10.json',
    hash_algorithm:'SHA-256',
    canonicalization:'JSON_STRINGIFY_PARSED_OBJECT_V1',
    verification_required_before_state_load:true
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
    parent_manifest_sha256:sha256(parentManifest),
    parent_public_bank_sha256:parentManifest.public_bank_sha256,
    parent_public_config_sha256:parentManifest.public_config_sha256,
    private_crosswalk_sha256:parentManifest.private_crosswalk_sha256,
    response_encoding:'OPAQUE_CHOICE_CODE_V1',
    stimulus_count:publicBank.stimuli.length,
    sequence_count:Object.keys(publicConfig.schedules).length,
    choice_code_count:parentManifest.choice_code_count,
    migration_sources:['CUBE-REV 0.8.8','CUBE-REV 0.8.9']
  };
  const pins={
    schema_version:'CR0810-ASSET-PINS-1',
    version:VERSION,
    manifest_sha256:sha256(manifest),
    public_bank_sha256:manifest.public_bank_sha256,
    public_config_sha256:manifest.public_config_sha256,
    parent_manifest_sha256:manifest.parent_manifest_sha256,
    private_crosswalk_sha256:manifest.private_crosswalk_sha256
  };
  return {publicBank,publicConfig,manifest,pins};
}

function pinModule(pins){
  return `(function(g){'use strict';const p=${JSON.stringify(pins)};if(typeof module!=='undefined'&&module.exports)module.exports=p;g.CUBE_REV_ASSET_PINS_0810=p;})(typeof window!=='undefined'?window:globalThis);\n`;
}

function main(argv=process.argv.slice(2)){
  const root=path.resolve(__dirname,'..');
  const parentBankPath=path.resolve(argv[0]||path.join(root,'cognitive/PARTICIPANT_STIMULUS_BANK_0.8.9.json'));
  const parentConfigPath=path.resolve(argv[1]||path.join(root,'cognitive/COGNITIVE_MODE_CONFIG_0.8.9.json'));
  const parentManifestPath=path.resolve(argv[2]||path.join(root,'research/CUBE_REV_0.8.9_BUILD_MANIFEST.json'));
  const bankPath=path.resolve(argv[3]||path.join(root,'cognitive/PARTICIPANT_STIMULUS_BANK_0.8.10.json'));
  const configPath=path.resolve(argv[4]||path.join(root,'cognitive/COGNITIVE_MODE_CONFIG_0.8.10.json'));
  const manifestPath=path.resolve(argv[5]||path.join(root,'research/CUBE_REV_0.8.10_ASSET_MANIFEST.json'));
  const pinsPath=path.resolve(argv[6]||path.join(root,'js/asset-pins-0.8.10.js'));
  const out=build(readJson(parentBankPath),readJson(parentConfigPath),readJson(parentManifestPath));
  writeJson(bankPath,out.publicBank);
  writeJson(configPath,out.publicConfig);
  writeJson(manifestPath,out.manifest);
  writeText(pinsPath,pinModule(out.pins));
  console.log(`CR0810_ASSET_BUILD_PASS stimuli=${out.manifest.stimulus_count} choices=${out.manifest.choice_code_count}`);
}

if(require.main===module)main();
module.exports={VERSION,BANK_SCHEMA,CONFIG_SCHEMA,MANIFEST_SCHEMA,canonical,sha256,assertParent,build,pinModule};
