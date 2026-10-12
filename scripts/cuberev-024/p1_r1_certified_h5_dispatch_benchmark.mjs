// CUBE-REV 0.24 P1-R1: physically exact restricted-word incumbent and
// complete 18HTM radius-5 solver, with honest same-engine same-goal-table baseline.
// Real 54-sticker outer-face permutations derived from 3D physical coordinates.
// The 62 same-corner cohort and all private human solve files are NOT inputs.
// Benchmarks are transparent retrospective pilot, not preregistered speed claims.
import assert from 'node:assert/strict';
import {performance} from 'node:perf_hooks';
const F='URFDLB';
const normal={U:[0,1,0],R:[1,0,0],F:[0,0,1],D:[0,-1,0],L:[-1,0,0],B:[0,0,-1]};
const geometry={U:[1,1,-1],R:[0,1,-1],F:[2,1,-1],D:[1,-1,1],L:[0,-1,1],B:[2,-1,1]};
const positions=[];
for(const face of F){
  const n=normal[face],a=[];
  for(let x=-1;x<=1;x++)for(let y=-1;y<=1;y++)
    a.push({p:n[0]?[n[0],x,y]:n[1]?[x,n[1],y]:[x,y,n[2]],n});
  a.sort((u,v)=>u.p.join(',').localeCompare(v.p.join(','),'en'));
  positions.push(...a);
}
const k=s=>s.p.join(',')+'|'+s.n.join(',');
const location=new Map(positions.map((s,i)=>[k(s),i]));
assert.equal(location.size,54);
function rotation(v,a,p){
  let [x,y,z]=v;
  for(let i=0;i<((p%4)+4)%4;i++){
    if(a===0)[x,y,z]=[x,-z,y];
    else if(a===1)[x,y,z]=[z,y,-x];
    else [x,y,z]=[-y,x,z];
  }
  return [x,y,z];
}
const actions=[...F].flatMap(f=>[f,f+"'",f+'2']);
const permutations=actions.map(t=>{
  const [a,layer,q]=geometry[t[0]],power=t.endsWith("'")?3:t.endsWith('2')?2:1;
  const p=positions.map(s=>location.get(k(s.p[a]===layer
    ?{p:rotation(s.p,a,q*power),n:rotation(s.n,a,q*power)}:s)));
  assert.equal(new Set(p).size,54);
  return p;
});
const goal=[...F].map(f=>f.repeat(9)).join('');
function apply(s,m){const out=Array(54),p=permutations[m];for(let i=0;i<54;i++)out[p[i]]=s[i];return out.join('')}
const all=actions.map((_,i)=>i);
const half=actions.map((t,i)=>t.endsWith('2')?i:-1).filter(i=>i>=0);
function inverse(i){const t=actions[i];return actions.indexOf(t.endsWith('2')?t:t.endsWith("'")?t[0]:t+"'")}
function invertWord(word){return word.toReversed().map(inverse)}
function replay(s,word){for(const m of word)s=apply(s,m);return s}
for(const i of all)assert.equal(replay(goal,[i,inverse(i)]),goal);
function breadthFirst(alphabet,max){
  const start=performance.now(),seen=new Map([[goal,{d:0,word:[]}]]);
  let front=[goal],layers=[1];
  for(let d=1;d<=max;d++){
    const next=[];
    for(const s of front)for(const m of alphabet){
      const state=apply(s,m);
      if(seen.has(state))continue;
      seen.set(state,{d,word:[...seen.get(s).word,m]});
      next.push(state);
    }
    front=next;layers.push(next.length);
  }
  return {seen,layers,ms:performance.now()-start};
}
// Baseline and dispatch are BOTH complete shortest solvers only for d_18<=5.
function full18Radius5(s,goal4){
  let probes=1,rotations=0;
  const ready=goal4.get(s);
  if(ready)return {word:invertWord(ready.word),probes,rotations,method:'goal4'};
  for(const i of all){
    const child=apply(s,i);rotations++;
    const known=goal4.get(child);probes++;
    if(known)return {word:[i,...invertWord(known.word)],probes,rotations,method:'full18'};
  }
  return {word:null,probes,rotations,method:'HOLD_OUTSIDE_RADIUS5'};
}
// Proof gate: s not in the exact full18 ball d<=4, and an H5
// physical word of length exactly 5 exists => 5<=d18(s)<=5.
function certifiedDual(s,goal4,h5){
  let probes=1,rotations=0;
  const known=goal4.get(s);
  if(known)return {word:invertWord(known.word),probes,rotations,method:'goal4'};
  const h=h5.get(s);probes++;
  if(h?.d===5)return {word:invertWord(h.word),probes,rotations,method:'certified_H5'};
  for(const i of all){
    const child=apply(s,i);rotations++;
    const q=goal4.get(child);probes++;
    if(q)return {word:[i,...invertWord(q.word)],probes,rotations,method:'full18'};
  }
  return {word:null,probes,rotations,method:'HOLD_OUTSIDE_RADIUS5'};
}
const R4=breadthFirst(all,4);
if(global.gc)global.gc();
const baselineMemory={heap:process.memoryUsage().heapUsed,rss:process.memoryUsage().rss};
const H5=breadthFirst(half,5);
if(global.gc)global.gc();
const hybridMemory={heap:process.memoryUsage().heapUsed,rss:process.memoryUsage().rss};
assert.deepEqual(R4.layers,[1,18,243,3240,43239]);
assert.deepEqual(H5.layers,[1,6,27,120,519,1932]);
assert.equal(R4.seen.size,46741);
assert.equal(H5.seen.size,2605);
const full5=breadthFirst(all,5);
const HGroup=breadthFirst(half,16); // Evaluation oracle ONLY, NOT solver resource.
assert.deepEqual(full5.layers,[1,18,243,3240,43239,574908]);
assert.equal(HGroup.seen.size,663552);
assert.equal(HGroup.layers.at(-1),0);
const positive=[],distorted=[],negative=[];
let allNegative=0,seed=0xC0BE2026;
function random(){seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return seed>>>0}
for(const [s,v] of full5.seen){
  if(v.d!==5)continue;
  const h=HGroup.seen.get(s);
  if(h){
    if(h.d===5)positive.push(s);
    else if(h.d===8||h.d===9)distorted.push(s);
    else throw Error('UNEXPECTED_PHYSICAL_H_DISTANCE:'+h.d);
  }else{
    allNegative++;
    if(negative.length<4096)negative.push(s);
    else{const i=random()%allNegative;if(i<4096)negative[i]=s}
  }
}
assert.equal(positive.length,1932);
assert.equal(distorted.length,192);
assert.equal(allNegative,572784);
assert.equal(negative.length,4096);
const summary=[];
const median=a=>a.toSorted((u,v)=>u-v)[Math.floor(a.length/2)];
for(const [category,cohort] of [
  ['halfturn_five_is_full18_geodesic',positive],
  ['halfturn_distance_8_or_9_but_full18_five',distorted],
  ['outside_full_halfturn_subgroup_seeded_reservoir',negative]
]){
  const baseline={probes:0,rotations:0},dual={probes:0,rotations:0,certified:0};
  for(const s of cohort){
    const a=full18Radius5(s,R4.seen),b=certifiedDual(s,R4.seen,H5.seen);
    assert.equal(a.word?.length,5);
    assert.equal(b.word?.length,5);
    assert.equal(replay(s,a.word),goal);
    assert.equal(replay(s,b.word),goal);
    baseline.probes+=a.probes;dual.probes+=b.probes;
    baseline.rotations+=a.rotations;dual.rotations+=b.rotations;
    if(b.method==='certified_H5')dual.certified++;
  }
  const trials={baseline:[],dual:[]};
  for(let round=0;round<5;round++){
    for(const algorithm of (round%2?['dual','baseline']:['baseline','dual'])){
      const start=performance.now();let checksum=0;
      for(const s of cohort){
        const result=algorithm==='baseline'?full18Radius5(s,R4.seen):certifiedDual(s,R4.seen,H5.seen);
        checksum+=result.word.length;
      }
      assert.equal(checksum,cohort.length*5);
      trials[algorithm].push(performance.now()-start);
    }
  }
  summary.push({
    cohort:category,physical_sources:cohort.length,
    source_selection:category.startsWith('outside')?'predeclared xorshift32 0xC0BE2026, single reservoir draw from all full18 d5 states outside full H group':'entire source class from full18 radius5 evaluator',
    baseline,dual,baseline_median_ms:median(trials.baseline),dual_median_ms:median(trials.dual),
    probe_change_percent:100*(dual.probes/baseline.probes-1),
    rotation_change_percent:100*(dual.rotations/baseline.rotations-1),
    all_original_facelets_replayed_and_solved:true
  });
}
// Actual 3x3 edge-position signature filter. Allowed pairs are derived
// ONLY from genuine physical H5 states, never from the evaluator's H group.
// Rejecting a pair cannot reject any H5 optimality certificate. False
// positives merely lead to harmless full18 fallback.
const edgePositions=[...new Set(positions.filter(p=>p.p.filter(c=>Math.abs(c)===1).length===2)
  .map(p=>p.p.join(',')))].sort();
const edgePairs=edgePositions.map(p=>positions.map((a,i)=>a.p.join(',')===p?i:-1).filter(i=>i>=0));
assert.equal(edgePairs.length,12);assert(edgePairs.every(p=>p.length===2));
const faceCode=new Uint8Array(128);
for(let i=0;i<6;i++)faceCode[F.charCodeAt(i)]=i;
const allowedEdgePair=edgePairs.map(pair=>{
  const allowed=new Uint8Array(36);
  for(const s of H5.seen.keys())
    allowed[6*faceCode[s.charCodeAt(pair[0])]+faceCode[s.charCodeAt(pair[1])]]=1;
  assert.equal(allowed.reduce((x,y)=>x+y,0),4);
  return allowed;
});
function edgeGate(s){
  for(let j=0;j<12;j++){
    const pair=edgePairs[j],v=6*faceCode[s.charCodeAt(pair[0])]+faceCode[s.charCodeAt(pair[1])];
    if(!allowedEdgePair[j][v])return {pass:false,checks:j+1};
  }
  return {pass:true,checks:12};
}
for(const s of HGroup.seen.keys())assert(edgeGate(s).pass,
  'All genuine H states preserve actual four-edge orbit signatures');
function orbitCertified(s,goal4,h5){
  let probes=1,rotations=0;
  const ready=goal4.get(s);
  if(ready)return {word:invertWord(ready.word),probes,rotations,edgeChecks:0,method:'goal4'};
  const g=edgeGate(s);
  if(g.pass){
    const h=h5.get(s);probes++;
    if(h?.d===5)return {word:invertWord(h.word),probes,rotations,edgeChecks:g.checks,method:'certified_H5'};
  }
  for(const m of all){
    const child=apply(s,m);rotations++;probes++;
    const next=goal4.get(child);
    if(next)return {word:[m,...invertWord(next.word)],probes,rotations,edgeChecks:g.checks,method:'full18'};
  }
  return {word:null,probes,rotations,edgeChecks:g.checks,method:'HOLD_OUTSIDE_RADIUS5'};
}
let gateSourceCount=0,h5GateCount=0;
for(const [s,v] of full5.seen){
  if(v.d!==5)continue;
  const g=edgeGate(s).pass;
  if(g)gateSourceCount++;
  if(H5.seen.get(s)?.d===5){h5GateCount++;assert(g);}
}
assert.equal(gateSourceCount,2124);
assert.equal(h5GateCount,1932);
const easyLookupSavings=summary[0].baseline.probes-summary[0].dual.probes;
assert.equal(easyLookupSavings,16143);
const fullShellExactLookupDelta=gateSourceCount-h5GateCount-easyLookupSavings;
assert.equal(fullShellExactLookupDelta,-15951);
const orbitCohorts=[];
for(const [label,cohort] of [
  ['halfturn_five_is_full18_geodesic',positive],
  ['halfturn_distance_8_or_9_but_full18_five',distorted],
  ['outside_full_halfturn_subgroup_seeded_reservoir',negative]
]){
  const data={probes:0,rotations:0,edgeChecks:0,certified:0,gatePassed:0};
  for(const s of cohort){
    const x=orbitCertified(s,R4.seen,H5.seen);
    assert.equal(x.word?.length,5);assert.equal(replay(s,x.word),goal);
    data.probes+=x.probes;data.rotations+=x.rotations;data.edgeChecks+=x.edgeChecks;
    if(x.method==='certified_H5')data.certified++;
    if(x.edgeChecks===12)data.gatePassed++;
  }
  const t=[];
  for(let round=0;round<5;round++){
    const start=performance.now();let n=0;
    for(const s of cohort)n+=orbitCertified(s,R4.seen,H5.seen).word.length;
    assert.equal(n,cohort.length*5);
    t.push(performance.now()-start);
  }
  orbitCohorts.push({cohort:label,physical_sources:cohort.length,...data,median_ms:median(t),trials_ms:t});
}

// Complete-domain contract: an actual out-of-radius-five state MUST produce
// a HOLD from both bounded solvers; neither may mistake H membership for an
// unrestricted optimality witness.
const beyond=(()=>{for(const [s,v] of full5.seen){
 if(v.d!==5)continue;
 for(const i of all){const t=apply(s,i);if(!full5.seen.has(t))return t;}
}throw Error('NO_R6_CONTROL')})();
assert.equal(full18Radius5(beyond,R4.seen).method,'HOLD_OUTSIDE_RADIUS5');
assert.equal(certifiedDual(beyond,R4.seen,H5.seen).method,'HOLD_OUTSIDE_RADIUS5');
assert.equal(orbitCertified(beyond,R4.seen,H5.seen).method,'HOLD_OUTSIDE_RADIUS5');
const realCounterexamples=[
 ["D U R2 D U",9],["D U R2 D' U",8]
];
for(const [scramble,dH] of realCounterexamples){
  const s=replay(goal,scramble.split(/\s+/).map(t=>actions.indexOf(t)));
  assert.equal(full5.seen.get(s)?.d,5);
  assert.equal(HGroup.seen.get(s)?.d,dH);
  const solved=certifiedDual(s,R4.seen,H5.seen);
  const screened=orbitCertified(s,R4.seen,H5.seen);
  assert.equal(screened.method,'full18');
  assert.equal(screened.word.length,5);
  assert.equal(replay(s,screened.word),goal);
  assert.equal(solved.method,'full18');
  assert.equal(solved.word.length,5);
  assert.equal(replay(s,solved.word),goal);
}
console.log(JSON.stringify({
  marker:'CUBE_REV_024_P1_R1_CERTIFIED_FULL18_VS_HALF_TURN_POLICY_PILOT',
  status:'LOCAL_NODE_EXACT_REPLAY_PASS; GITHUB_ACTIONS_RUN_NOT_VERIFIED',
  objective:'whole-cube HTM-optimal solving WITHIN full18 radius five only',
  source_geometry:'complete real 54 ordered facelets',
  full18_goal_radius4_layers:R4.layers,
  H5_goal_layers:H5.layers,
  baseline_goal_entries:46741,
  dual_additional_H5_entries:2605,
  offline_evaluator_only_full18_radius5_states:full5.seen.size,
  offline_evaluator_only_complete_H_order:HGroup.seen.size,
  baseline_goal_precompute_ms:R4.ms,
  additional_H5_precompute_ms:H5.ms,
  extra_H5_heap_mib:(hybridMemory.heap-baselineMemory.heap)/1048576,
  extra_H5_rss_mib:(hybridMemory.rss-baselineMemory.rss)/1048576,
  test_cohorts:summary,
  screened_orbit_policy_cohorts:orbitCohorts,
  complete_d5_edge_signature_gate_positive:gateSourceCount,
  complete_d5_H5_certificates:h5GateCount,
  exact_all_574908_d5_lookup_change_screened_minus_baseline:fullShellExactLookupDelta,
  complete_d5_wallclock_NOT_MEASURED:true,
  complete_full18_shell_d5_size:574908,
  certified_H5_in_full18_shell_d5:1932,
  certified_H5_prevalence_percent:1932/574908*100,
  original_full18_radius6_control_result:'HOLD_BY_BOTH',
  explicit_distortion_counterexamples_pass:2,
  cpu_and_memory_measured_in_node_process_only:true,
  independent_go_external_CI_pending:true,
  no_unrestricted_cube_solver_claim:true,
  benchmark_is_retrospective_pilot_not_preregistered:true
},null,2));
