(function(global){
'use strict';
const VERSION='CUBE-REV 0.8.5', SCHEMA='CR0805-RESUME-STATE-1';
const STORAGE_KEY='cube-rev-cognitive-mode-0805-v1';
const QUARANTINE_KEY='cube-rev-cognitive-mode-0805-quarantine-v1';
function fnv1a(s){let h=0x811c9dc5;for(let i=0;i<s.length;i++){h^=s.charCodeAt(i);h=Math.imul(h,0x01000193)}return h>>>0}
function stableToken(storage,cryptoObj){let t=storage.getItem('cube-rev-anonymous-participant-v1');if(t)return t;const a=new Uint32Array(4);cryptoObj.getRandomValues(a);t='CRP-'+Array.from(a,x=>x.toString(16).padStart(8,'0')).join('');storage.setItem('cube-rev-anonymous-participant-v1',t);return t}
function sequenceId(token){return String((fnv1a(token)%24)+1)}
function checksum(x){return fnv1a(JSON.stringify(x)).toString(16).padStart(8,'0')}
function validateState(x,config){if(!x||x.schema_version!==SCHEMA||x.version!==VERSION||x.mode_id!=='COG-MODE-001')return false;if(!Array.isArray(x.schedule)||x.schedule.length!==28)return false;if(x.sequence_id!==sequenceId(x.participant_token))return false;if(x.cursor<0||x.cursor>x.schedule.length||x.responses.length!==x.cursor)return false;if(x.schedule.join('|')!==(config.schedules[x.sequence_id]||[]).join('|'))return false;return x.integrity===checksum({...x,integrity:undefined})}
function seal(x){const y={...x};delete y.integrity;return {...y,integrity:checksum({...y,integrity:undefined})}}
function create(config,storage,cryptoObj,now){const token=stableToken(storage,cryptoObj),sid=sequenceId(token);return seal({schema_version:SCHEMA,version:VERSION,mode_id:'COG-MODE-001',participant_token:token,session_id:'CR085-'+now().replace(/\D/g,'').slice(0,14)+'-'+fnv1a(token+now()).toString(16).padStart(8,'0'),sequence_id:sid,schedule:[...config.schedules[sid]],cursor:0,responses:[],status:'IN_PROGRESS',created_at:now(),updated_at:now(),submitted_at:null,submission_receipt:null,revision:0})}
function loadOrCreate(config,deps){const {storage,cryptoObj,now}=deps;const raw=storage.getItem(STORAGE_KEY);if(raw){try{const x=JSON.parse(raw);if(validateState(x,config))return {state:x,resumed:true}}catch(e){}storage.setItem(QUARANTINE_KEY,raw);storage.removeItem(STORAGE_KEY)}const x=create(config,storage,cryptoObj,now);storage.setItem(STORAGE_KEY,JSON.stringify(x));return {state:x,resumed:false}}
function persist(storage,state,now){const x=seal({...state,revision:state.revision+1,updated_at:now()});storage.setItem(STORAGE_KEY,JSON.stringify(x));return x}
function record(storage,state,response,now){if(state.status!=='IN_PROGRESS')throw new Error('SESSION_NOT_ACTIVE');if(response.trial_id!==state.schedule[state.cursor])throw new Error('TRIAL_ORDER_MISMATCH');const r={...response,position:state.cursor+1,recorded_at:now()};return persist(storage,{...state,responses:[...state.responses,r],cursor:state.cursor+1,status:state.cursor+1===state.schedule.length?'READY_TO_SUBMIT':'IN_PROGRESS'},now)}
function envelope(state){return {schema_version:'CR0805-COLLECTOR-PAYLOAD-1',version:VERSION,mode_id:state.mode_id,session_id:state.session_id,participant_token:state.participant_token,sequence_id:state.sequence_id,trial_count:state.schedule.length,responses:state.responses,started_at:state.created_at,completed_at:state.updated_at,resume_revision:state.revision,participant_ui:{legacy_fixed_set_selector:false,diagnostic_labels_exposed:false}}}
function saveExternalMutation(storage,state,now){return persist(storage,state,now)}
function markSubmitted(storage,state,receipt,now){if(state.status==='SUBMITTED')return state;if(state.status!=='READY_TO_SUBMIT')throw new Error('SESSION_NOT_COMPLETE');return persist(storage,{...state,status:'SUBMITTED',submitted_at:now(),submission_receipt:receipt||null},now)}
function resetForTest(storage){storage.removeItem(STORAGE_KEY);storage.removeItem(QUARANTINE_KEY)}
const api={VERSION,SCHEMA,STORAGE_KEY,QUARANTINE_KEY,fnv1a,sequenceId,validateState,loadOrCreate,record,envelope,saveExternalMutation,markSubmitted,resetForTest};
if(typeof module!=='undefined'&&module.exports)module.exports=api;global.CUBE_REV_COGNITIVE_MODE_0805=api;
})(typeof window!=='undefined'?window:globalThis);
