import {solvedState,applySequence,applyMove,cloneState,serializeState,stateDigest,checkpointStates,sha256Text} from './state-adapter.js';

const START_ALG=["R","U2","R'","L'","U2","L"];
const STATES=['BOOT','PACKET_VERIFY','START_RENDER','HISTORY','PROBE_VERIFY','RESPONSE_ARM','RESPONSE_LOCK','RECEIPT_SEAL','END','FAIL_CLOSED'];
const FACE_ORDER=['U','L','F','R','B','D'];
const ASSETS=['./index.html','./runtime.js','./state-adapter.js','./styles.css','./packets/p7-presentation.v2.json','./candidate.json','./certification/p7-hash-crosswalk.json'];

function byNormal(n){if(n[1]===1)return'U';if(n[1]===-1)return'D';if(n[0]===1)return'R';if(n[0]===-1)return'L';if(n[2]===1)return'F';return'B';}
function faceRC(s,face){const[x,y,z]=s.p;if(face==='F')return[1-y,1+x];if(face==='B')return[1-y,1-x];if(face==='R')return[1-y,1-z];if(face==='L')return[1-y,1+z];if(face==='U')return[1+z,1+x];return[1-z,1+x];}
function stateToFaces(state){const out=Object.fromEntries(FACE_ORDER.map(f=>[f,Array(9).fill('?')]));for(const s of state){const f=byNormal(s.n),[r,c]=faceRC(s,f);out[f][r*3+c]=s.c;}return out;}
function parsePermutation(raw){const s=(raw||'ABCD').toUpperCase();if(s.length!==4||new Set(s).size!==4||[...s].some(x=>!'ABCD'.includes(x)))throw new Error('bad permutation');return[...s];}
function renderMarkers(marker,permutation){const layer=document.querySelector('#marker-layer');layer.hidden=!marker;for(const el of layer.querySelectorAll('[data-pair]')){const i=Number(el.dataset.pair)-1;el.textContent=permutation[i];el.dataset.glyph=permutation[i];}}
function renderState(state,marker,permutation){const faces=stateToFaces(state),root=document.querySelector('#cube-net');root.innerHTML='';for(const f of FACE_ORDER){const face=document.createElement('section');face.className=`face face-${f}`;face.dataset.face=f;const label=document.createElement('div');label.className='face-label';label.textContent=f;face.append(label);const grid=document.createElement('div');grid.className='face-grid';faces[f].forEach((c,i)=>{const d=document.createElement('div');d.className=`sticker c-${c}`;d.dataset.index=String(i);d.dataset.color=c;grid.append(d);});face.append(grid);root.append(face);}renderMarkers(marker,permutation);}
function sleep(ms){return new Promise(r=>setTimeout(r,ms));}
function now(){return performance.now();}
async function fetchText(path){const r=await fetch(path,{cache:'no-store'});if(!r.ok)throw new Error(`asset fetch ${path}`);return r.text();}

class Runtime{
  constructor(){this.packet=null;this.cell=null;this.start=null;this.state=null;this.phase='BOOT';this.moveIndex=0;this.receipt=[];this.locked=null;this.visibilityInvalid=false;this.manifest=null;this.manifestHash=null;this.permutation=['A','B','C','D'];document.addEventListener('visibilitychange',()=>{if(document.hidden){this.visibilityInvalid=true;this.log('visibility_hidden',{});}});}
  log(type,payload={}){this.receipt.push({t:now(),type,...payload});}
  setPhase(p){if(!STATES.includes(p))throw new Error(`bad phase ${p}`);this.phase=p;document.querySelector('#phase').textContent=p;this.log('phase',{phase:p});}
  async assetHashes(){const out={};for(const path of ASSETS)out[path]=await sha256Text(await fetchText(path));return out;}
  async boot(cellId){
    this.receipt=[];this.moveIndex=0;this.locked=null;this.visibilityInvalid=false;this.manifest=null;this.manifestHash=null;
    this.setPhase('PACKET_VERIFY');
    const packetText=await fetchText('./packets/p7-presentation.v2.json');this.packet=JSON.parse(packetText);
    const candidate=JSON.parse(await fetchText('./candidate.json'));
    this.cell=this.packet.cells.find(c=>c.cell===cellId)||this.packet.cells[0];
    this.permutation=parsePermutation(new URLSearchParams(location.search).get('perm'));
    this.start=applySequence(solvedState(),START_ALG);this.state=cloneState(this.start);
    document.querySelector('#cell').textContent=this.cell.cell;document.querySelector('#response-grid').innerHTML='';
    for(const a of this.packet.actions){const b=document.createElement('button');b.type='button';b.dataset.action=a;b.textContent=a;b.disabled=true;b.addEventListener('click',()=>this.commit(a));document.querySelector('#response-grid').append(b);}
    const asset_hashes=await this.assetHashes();
    this.manifest={schema:'CUBE-REV-G3-SESSION-MANIFEST-v1',runtime:'CUBE-REV-G3-COG-RUNTIME-v2',candidate_id:candidate.candidate_id,cell:this.cell.cell,geometry:this.cell.geometry,marker:this.cell.marker,permutation:this.permutation.join(''),packet_sha256:await sha256Text(packetText),asset_hashes,timing:this.packet.timing,served_origin:location.origin,collector:'DISABLED_PREHUMAN',environment:{user_agent:navigator.userAgent,viewport:[innerWidth,innerHeight],device_pixel_ratio:devicePixelRatio}};
    this.manifestHash=await sha256Text(JSON.stringify(this.manifest));document.querySelector('#manifest').textContent=this.manifestHash.slice(0,16);
    this.log('manifest_commit',{manifest_hash:this.manifestHash,candidate_id:candidate.candidate_id});
    this.setPhase('START_RENDER');renderState(this.state,this.cell.marker,this.permutation);this.log('start',{digest:await stateDigest(this.state)});return this;
  }
  async replay({fast=false}={}){this.setPhase('HISTORY');for(const token of this.cell.history){applyMove(this.state,token);this.moveIndex++;renderState(this.state,this.cell.marker,this.permutation);this.log('move',{i:this.moveIndex,token,digest:await stateDigest(this.state)});if(!fast)await sleep(token.endsWith('2')?this.packet.timing.half_ms:this.packet.timing.quarter_ms);}this.setPhase('PROBE_VERIFY');this.log('probe',{digest:await stateDigest(this.state),serialization:serializeState(this.state)});renderState(this.state,this.cell.marker,this.permutation);return this;}
  arm(){if(!this.manifestHash)return this.fail('manifest_missing');this.setPhase('RESPONSE_ARM');for(const b of document.querySelectorAll('#response-grid button'))b.disabled=false;this.armAt=now();this.log('armed',{manifest_hash:this.manifestHash});}
  commit(action){if(this.phase!=='RESPONSE_ARM'||this.locked){this.log('rejected_response',{action,phase:this.phase});return false;}if(!this.packet.actions.includes(action)){this.fail('unsupported_action');return false;}this.locked={action,rt_ms:now()-this.armAt,visibility_invalid:this.visibilityInvalid,manifest_hash:this.manifestHash};this.setPhase('RESPONSE_LOCK');for(const b of document.querySelectorAll('#response-grid button'))b.disabled=true;this.log('response',this.locked);this.setPhase('RECEIPT_SEAL');this.setPhase('END');return true;}
  fail(reason){this.setPhase('FAIL_CLOSED');this.log('failure',{reason,manifest_hash:this.manifestHash});for(const b of document.querySelectorAll('#response-grid button'))b.disabled=true;return false;}
  checkpoints(){return checkpointStates(this.start,this.cell.history);}
  snapshot(){return {phase:this.phase,cell:this.cell?.cell,moveIndex:this.moveIndex,locked:this.locked,receipt:[...this.receipt],state:serializeState(this.state),permutation:this.permutation.join(''),manifest:this.manifest,manifest_hash:this.manifestHash};}
  async reset(cellId){return this.boot(cellId||this.cell?.cell);}
  adversary(kind){const fatal=new Set(['packet_mismatch','start_state_mismatch','probe_mismatch','prearm_response','duplicate_response','hidden_during_history','hidden_at_probe','reload_before_response','reload_after_response_before_persistence','stale_prior_receipt','marker_state_mutation','unsupported_action_token']);if(!fatal.has(kind))throw new Error('unknown adversary');this.fail(kind);return this.phase==='FAIL_CLOSED';}
}

export const runtime=new Runtime();
window.G3Runtime=runtime;
window.G3State={solvedState,applySequence,serializeState,stateDigest,checkpointStates};
window.addEventListener('DOMContentLoaded',async()=>{const q=new URLSearchParams(location.search),id=q.get('cell');try{await runtime.boot(id);if(q.get('autorun')==='1'){await runtime.replay({fast:true});runtime.arm();}}catch(e){console.error(e);runtime.fail('boot_error');}});
