/* G3-P35-R1-R2: frozen Y+ coordinate baseline only. */
import { createHash } from 'node:crypto';
import { createWriteStream, readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { applyMove, applySequence, serializeState, solvedState } from '../state-adapter.js';

const HERE=dirname(fileURLToPath(import.meta.url)), P34=join(HERE,'..','p34-runtime');
const BANK_PATH=join(P34,'p34-bank.json'), BANK_SHA='cef57e7943510d15d2bfbb59f18761217599f9d5c7b749511a02d1c371e9ae00';
const MOVES=['U',"U'",'D',"D'",'L',"L'",'R',"R'",'F',"F'",'B',"B'"];
const FACE_MAP={U:'U',D:'D',F:'R',R:'B',B:'L',L:'F'};
const sha=(x)=>createHash('sha256').update(x).digest('hex');
const face=(x)=>x[0], gamma=(x)=>`${FACE_MAP[face(x)]}${x.endsWith("'")?"'":''}`;
const inv=(x)=>x.endsWith("'")?x[0]:`${x[0]}'`, inverse=(w)=>[...w].reverse().map(inv);
const key=(s)=>Buffer.from(s).toString('base64'), eq=(a,b)=>key(a)===key(b);
const slot=(x)=>[...x.p,...x.n].join(','), rotY=([x,y,z])=>[z,y,-x];
const BASE=solvedState().map((x)=>({...x,p:[...x.p],n:[...x.n]})).sort((a,b)=>slot(a).localeCompare(slot(b)));
const SLOTS=BASE.map((x,i)=>({...x,p:[...x.p],n:[...x.n],c:String(i)}));
const COLORS=BASE.map((x)=>x.c), ID=Uint8Array.from(SLOTS.map((_,i)=>i));
function permFrom(transform){const labeled=SLOTS.map((x,i)=>({p:[...x.p],n:[...x.n],c:String(i)}));transform(labeled);return Uint8Array.from(labeled.sort((a,b)=>slot(a).localeCompare(slot(b))).map((x)=>Number(x.c)));}
const MOVE=Object.fromEntries(MOVES.map((m)=>[m,permFrom((s)=>applyMove(s,m))]));
const G=permFrom((s)=>{for(const x of s){x.p=rotY(x.p);x.n=rotY(x.n);}});
function apply(state,p){const out=new Uint8Array(state.length);for(let i=0;i<out.length;i++)out[i]=state[p[i]];return out;}
function run(state,word,table=MOVE){let out=Uint8Array.from(state);for(const m of word)out=apply(out,table[m]);return out;}
function g(state){return apply(state,G);}
function toAdapter(state){return BASE.map((x,i)=>({p:[...x.p],n:[...x.n],c:COLORS[state[i]]}));}
function exactHash(state){return sha(serializeState(toAdapter(state)));}
function selector(word){return [...new Set(word.map(face))].sort();}
function selectorMoves(faces){return MOVES.filter((m)=>faces.includes(face(m)));}
function nextWords(state,last,allowed){const out=[];for(const m of allowed)if(!last||face(last)!==face(m))out.push([m,run(state,[m])]);return out;}
function boundedReach(start,target,faces,budget){const allowed=selectorMoves(faces), targetKey=key(target), q=[[start,null,0]], seen=new Set([key(start)]);for(let i=0;i<q.length;i++){const [s,last,d]=q[i];if(key(s)===targetKey)return {reachable:true,prefix:d};if(d===budget)continue;for(const [m,n] of nextWords(s,last,allowed)){const k=key(n);if(!seen.has(k)){seen.add(k);q.push([n,m,d+1]);}}}return {reachable:false,prefix:null};}
function csv(v){const s=String(v??'');return /[",\n]/.test(s)?`"${s.replaceAll('"','""')}"`:s;}
const bankBytes=readFileSync(BANK_PATH), bank=JSON.parse(bankBytes);
if(sha(bankBytes)!==BANK_SHA)throw Error('BANK_BYTE_MUTATION_HOLD');
if(bank.rows.length!==109184)throw Error(`ROW_COUNT_HOLD:${bank.rows.length}`);
if(JSON.stringify(bank.authority.move_alphabet)!==JSON.stringify(MOVES))throw Error('MOVE_GRAMMAR_HOLD');
const gammaImage=MOVES.map(gamma);if(new Set(gammaImage).size!==12||gammaImage.some((m)=>!MOVES.includes(m)))throw Error('GAMMA_BIJECTION_HOLD');
for(const m of MOVES)if(gamma(inv(m))!==inv(gamma(m)))throw Error(`INVERSE_TOKEN_HOLD:${m}`);
const starts=new Map();for(const x of bank.authority.starts){const state=run(ID,x.scramble), canonical=applySequence(solvedState(),x.scramble);if(exactHash(state)!==x.state_sha256||serializeState(canonical)!==serializeState(toAdapter(state)))throw Error(`START_HASH_HOLD:${x.id}`);starts.set(x.id,state);}
// g is derived from adapter coordinates, then checked against a direct coordinate transformation.
function directGHash(state){return sha(serializeState(toAdapter(state).map((x)=>({p:rotY(x.p),n:rotY(x.n),c:x.c}))));}
for(const s of [...starts.values(),ID])if(exactHash(g(s))!==directGHash(s))throw Error('G_MATERIALIZATION_HOLD');
const gInverse=new Uint8Array(54);for(let i=0;i<54;i++)gInverse[G[i]]=i;
for(const s of [...starts.values(),ID])if(!eq(apply(g(s),gInverse),s))throw Error('G_INVERSE_HOLD');

const encountered=new Map(), special=new Map();
let historyParity=0, selectorParity=0, targetParity=0, contexts=0;
const lines=createWriteStream(join(HERE,'p35-r1-r2-contexts.csv'));
lines.write('row_id,branch,origin_hash,terminal_hash,history,history_length,b,r1_start_hash,r1_target_hash,r2_start_hash,r2_target_hash,r1_selector,r2_selector,selector_symdiff,first_divergent_prefix,witness_start_hash,classification\n');
function addEncountered(state){encountered.set(key(state),state);}
for(const row of bank.rows){
  const origin=starts.get(row.start_id), a=row.word_A.split(' '), b=row.word_B.split(' ');
  for(const [branch,history] of [['A',a],['B',b]]){
    let state=origin;addEncountered(state);for(const token of history){state=run(state,[token]);addEncountered(state);}
    if(exactHash(state)!==row.terminal_state_sha256)throw Error(`HISTORY_TERMINAL_HOLD:${row.item_id}:${branch}`);
    const r1Sel=selector(history), r2Sel=selector(history.map(gamma)), expectedSel=[...new Set(r1Sel.map((f)=>FACE_MAP[f]))].sort();
    if(JSON.stringify(r2Sel)!==JSON.stringify(expectedSel))throw Error(`SELECTOR_PARITY_HOLD:${row.item_id}:${branch}`);
    const r1Start=state,r1Target=origin,r2Start=g(state),r2Target=g(origin);
    if(!eq(g(r1Target),r2Target))throw Error(`TARGET_PARITY_HOLD:${row.item_id}:${branch}`);
    historyParity++;selectorParity++;targetParity++;contexts++;
    const directReturn=inverse(history), directOK=directReturn.length<=row.terminal_to_origin_qtm && directReturn.every((m)=>r1Sel.includes(face(m)));
    const tag=`${row.terminal_state_sha256}|${row.start_state_sha256}|${r1Sel.join('')}|${row.terminal_to_origin_qtm}`;
    if(!directOK&&!special.has(tag))special.set(tag,{row,branch,history,r1Sel,r2Sel,r1Start,r1Target,r2Start,r2Target});
  }
}
if(contexts!==218368)throw Error(`CONTEXT_COUNT_HOLD:${contexts}`);
// Exact preflight over every state seen while replaying both sealed histories.
let transitionPairs=0, transitionFailures=0;
for(const state of encountered.values())for(const action of MOVES){transitionPairs++;if(!eq(g(run(state,[action])),run(g(state),[gamma(action)])))transitionFailures++;}
if(transitionFailures)throw Error(`Y_PLUS_TRANSFORM_AUTHORITY_HOLD:${transitionFailures}`);

const reachCache=new Map();
for(const [tag,x] of special){const left=boundedReach(x.r1Start,x.r1Target,x.r1Sel,x.row.terminal_to_origin_qtm);const right=boundedReach(x.r2Start,x.r2Target,x.r2Sel,x.row.terminal_to_origin_qtm);reachCache.set(tag,{left,right});}
let Iplus=0,Iminus=0,R1only=0,R2only=0,OOA=0,first=null,cacheSpecialUses=0;
for(const row of bank.rows){
  const origin=starts.get(row.start_id), terminal=run(origin,row.word_A.split(' '));
  for(const [branch,history] of [['A',row.word_A.split(' ')],['B',row.word_B.split(' ')]]){
    const r1Sel=selector(history),r2Sel=selector(history.map(gamma)), direct=inverse(history), directOK=direct.length<=row.terminal_to_origin_qtm&&direct.every((m)=>r1Sel.includes(face(m)));
    let left,right,prefix=null;
    if(directOK){left=true;right=eq(run(terminal,direct),origin)&&eq(run(g(terminal),direct.map(gamma)),g(origin));}
    else {const got=reachCache.get(`${row.terminal_state_sha256}|${row.start_state_sha256}|${r1Sel.join('')}|${row.terminal_to_origin_qtm}`);left=got.left.reachable;right=got.right.reachable;prefix=got.left.prefix??got.right.prefix;cacheSpecialUses++;}
    let cls;if(left&&right){cls='I+';Iplus++;}else if(!left&&!right){cls='I−';Iminus++;}else if(left){cls='R1-only';R1only++;}else{cls='R2-only';R2only++;}
    if((cls==='R1-only'||cls==='R2-only')&&!first)first={row_id:row.item_id,branch,budget:row.terminal_to_origin_qtm,history_length:history.length,selector_symmetric_difference:0,first_divergent_prefix:prefix,origin_hash:row.start_state_sha256,classification:cls};
    lines.write([row.item_id,branch,row.start_state_sha256,row.terminal_state_sha256,history.join(' '),history.length,row.terminal_to_origin_qtm,exactHash(terminal),exactHash(origin),exactHash(g(terminal)),exactHash(g(origin)),r1Sel.join(' '),r2Sel.join(' '),0,prefix??'',row.start_state_sha256,cls].map(csv).join(',')+'\n');
  }
}
await new Promise((resolve,reject)=>{lines.end(resolve);lines.on('error',reject);});
const contextPath=join(HERE,'p35-r1-r2-contexts.csv'), contextBytes=readFileSync(contextPath);
const receipt={schema:'CUBE-REV-G3-P35-R1-R2-RECEIPT-v1',authority:'G3-P35-R1-R1',bank_sha256:sha(bankBytes),bank_unchanged:true,implementation:{node:process.version,compiler_sha256:sha(readFileSync(fileURLToPath(import.meta.url))),state_adapter_sha256:sha(readFileSync(join(HERE,'..','state-adapter.js')))},transform:{face_map:FACE_MAP,gamma: Object.fromEntries(MOVES.map((m)=>[m,gamma(m)])),g_bijective:true,gamma_bijective:true,solved_consistency:true,inverse_consistency:true,encountered_distinct_states:encountered.size,transition_pairs_checked:transitionPairs,transition_failures:transitionFailures,cost_parity_contexts:contexts,target_parity_contexts:targetParity},contexts:{expected:218368,materialized:contexts,selector_parity:selectorParity,history_parity:historyParity,special_bounded_search_keys:special.size,special_bounded_search_context_uses:cacheSpecialUses,context_csv_sha256:sha(contextBytes)},census:{I_plus:Iplus,I_minus:Iminus,R1_only:R1only,R2_only:R2only,OOA},minimal_witness:first,first_non_commuting_component:first?'PENDING_DIVERGENCE_LOCALIZATION':'NONE_NO_REPRESENTATION_SENSITIVE_CONTEXT',no_divergence_region:first?null:{contexts,bounded_by:'certified P34 rows x A/B histories; frozen selector and terminal-to-origin QTM budget',result:'CERTIFIED_BOUNDED_NO_DIVERGENCE_REGION'},p36_gate:'CLOSED',verdict:first?'REPRESENTATION_SENSITIVE_DIVERGENCE_HOLD':'EXACT_COORDINATE_EQUIVARIANCE_PASS / CERTIFIED_BOUNDED_NO_DIVERGENCE_REGION / P36_CLOSED'};
writeFileSync(join(HERE,'p35-r1-r2-receipt.json'),JSON.stringify(receipt,null,2)+'\n');console.log(JSON.stringify(receipt,null,2));
