import {readFileSync,writeFileSync,readdirSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {dirname,join} from 'node:path';
import {fileURLToPath} from 'node:url';
import {solvedState,applySequence,serializeState} from '../state-adapter.js';
const here=dirname(fileURLToPath(import.meta.url)),sha=b=>createHash('sha256').update(b).digest('hex'),read=n=>JSON.parse(readFileSync(join(here,n)));
function check(ok,s){if(!ok)throw Error(s);}
for(const r of read('sha256-manifest.json'))check(sha(readFileSync(join(here,r.name)))===r.sha256,'OUTPUT_HASH '+r.name);
for(const r of read('terminal-receipt.json').input_hashes)check(sha(readFileSync(join(here,'..',r.path)))===r.sha256,'INPUT_HASH '+r.path);
const c=read('canonical-observation-counterexample.json'),d=[];
check(sha(serializeState(c.target))===c.target_hash,'COUNTEREXAMPLE_TARGET');
check(sha(serializeState(c.rival))===c.rival_hash,'COUNTEREXAMPLE_RIVAL');
for(let i=0;i<54;i++)if(c.target[i].c!==c.rival[i].c)d.push(i);
check(JSON.stringify(d)===JSON.stringify(c.canonical_delta)&&d.length===6,'COUNTEREXAMPLE_DELTA');
const O=read('observation-necessity.json');check(O.semantic_parity.startsWith('HOLD'),'SEMANTIC_HOLD');
const H=read('hasse-edges.json');check(H.edge_count===180&&!H.table_recovery_failures&&!H.contextwise_monotonicity_failures&&!H.context_gamma_transport_failures,'HASSE');
const geom=read('size10-orbit.json');
const minimal=read('informative-antichain.json');check(minimal.members.length===11,'MINIMAL_ANTICHAIN');
const informative=H.nodes.filter(x=>x.r1only+x.r2only);
const rank=informative.slice().sort((a,b)=>a.faces.length-b.faces.length||((b.r1+b.r2-b.both)-(a.r1+a.r2-a.both))||Math.abs(a.r1-a.r2)-Math.abs(b.r1-b.r2)||a.M-b.M);
// Independent actual-color-state witness test: unpruned 3+3 halves, all
// legal routes of length <=6, exact adapter serialization at every join.
const w=read('witness-mechanism.json');
const bank=JSON.parse(readFileSync(join(here,'../p34-runtime/p34-bank.json')));
const origin=bank.authority.starts.find(x=>x.id===w.row.start_id);
const q=applySequence(solvedState(),origin.scramble),s=applySequence(q,w.row.word_A.split(' '));
const faces=['U','D','L','R','F','B'],moves=faces.flatMap(f=>[f,f+"'"]),inverse=m=>m.endsWith("'")?m[0]:m+"'";
const rotate=s=>s.map(x=>({p:[x.p[2],x.p[1],-x.p[0]],n:[x.n[2],x.n[1],-x.n[0]],c:x.c}));
function halves(s){const queue=[{s,d:0,last:'',mask:0,path:[]}],map=new Map();for(let i=0;i<queue.length;i++){const n=queue[i],k=serializeState(n.s);if(!map.has(k))map.set(k,[]);map.get(k).push(n);if(n.d===3)continue;for(const m of moves){if(m[0]===n.last)continue;queue.push({s:applySequence(n.s,[m]),d:n.d+1,last:m[0],mask:n.mask|(1<<faces.indexOf(m[0])),path:[...n.path,m]});}}return {map,count:queue.length};}
function exactMasks(s,q){const f=halves(s),r=halves(q),masks=new Set();let joins=0;for(const [k,aa] of f.map){for(const a of aa)for(const b of r.map.get(k)||[]){if(a.d+b.d>6||(a.d&&b.d&&a.last===b.last))continue;const route=[...a.path,...b.path.slice().reverse().map(inverse)];check(serializeState(applySequence(s,route))===serializeState(q),'EXACT_JOIN_ROUTE');masks.add(a.mask|b.mask);joins++;}}const all=[...masks];return {forward_entries:f.count,reverse_entries:r.count,legal_joins:joins,masks:all.filter(m=>!all.some(n=>n!==m&&(n&m)===n)).sort((a,b)=>a-b)};}
const actual={r1:exactMasks(s,q),r2:exactMasks(rotate(s),rotate(q))};
check(JSON.stringify(actual.r1.masks)===JSON.stringify(w.antichains.r1.slice().sort((a,b)=>a-b)),'WITNESS_R1_MASKS');
check(JSON.stringify(actual.r2.masks)===JSON.stringify(w.antichains.r2.slice().sort((a,b)=>a-b)),'WITNESS_R2_MASKS');
const result={status:'AUDIT_ARTIFACT_VERIFICATION_PASS_NOT_TRANSPORT_PROMOTION',counterexample_hashes_verified:true,counterexample_delta:d,actual_color_witness_unpruned_MITM:actual,D_orbit:{size:geom.orbit_size,stabilizer:geom.stabilizer,frontier_one_rotation_orbit:geom.geometry.filter(x=>x.on_size10_frontier).every(x=>x.on_D_orbit),ranking_statistics_invariant:new Set(geom.geometry.filter(x=>x.on_D_orbit).map(x=>JSON.stringify(x.inherited))).size===1},A_rank_under_union_then_balance_then_mask:rank[0].M,A_first_context:read('witness-mechanism.json').frozen_witness_first_under_origin_hash_order,scope:'Witness-specific exact target and unpruned controls do not retroactively certify the entire inherited 6724-key search or its normalization. No inherited artifact changed.'};
writeFileSync(join(here,'verification.json'),JSON.stringify(result,null,2)+'\n');
const manifest=readdirSync(here).filter(n=>n!=='custody-sha256.json').sort().map(name=>{const b=readFileSync(join(here,name));return {name,bytes:b.length,sha256:sha(b)};});
writeFileSync(join(here,'custody-sha256.json'),JSON.stringify(manifest,null,2)+'\n');
console.log(JSON.stringify(result,null,2));
