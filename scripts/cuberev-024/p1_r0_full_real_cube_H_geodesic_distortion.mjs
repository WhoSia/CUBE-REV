// CUBE-REV 0.24 P0-R1 — independent original 54-sticker edge orbit court.
// Exhaustive 18HTM original physical cube ball <=4, six true halfturn moves <=5.
// H-generator edge-position orbits produce rigorous GLOBAL negative tests.
// The observed equality inside radius4 is finite only, not a universal theorem.
import assert from 'node:assert/strict';
const F='URFDLB',normal={U:[0,1,0],R:[1,0,0],F:[0,0,1],D:[0,-1,0],L:[-1,0,0],B:[0,0,-1]};
const layers={U:[1,1,-1],R:[0,1,-1],F:[2,1,-1],D:[1,-1,1],L:[0,-1,1],B:[2,-1,1]};
const slots=[];
for(const f of F){
  const n=normal[f],side=[];
  for(let a=-1;a<=1;a++)for(let b=-1;b<=1;b++)
    side.push({p:n[0]?[n[0],a,b]:n[1]?[a,n[1],b]:[a,b,n[2]],n});
  side.sort((x,y)=>x.p.join(',').localeCompare(y.p.join(','),'en'));
  slots.push(...side);
}
const id=s=>s.p.join(',')+'|'+s.n.join(','),positions=new Map(slots.map((s,i)=>[id(s),i]));
assert.equal(positions.size,54);
function rotate(v,axis,q){
  let [x,y,z]=v;
  for(let i=0;i<(q+4)%4;i++){
    if(axis===0)[x,y,z]=[x,-z,y];
    else if(axis===1)[x,y,z]=[z,y,-x];
    else [x,y,z]=[-y,x,z];
  }
  return [x,y,z];
}
const names=[...F].flatMap(f=>[f,f+"'",f+'2']);
const moves=names.map(m=>{
  const [axis,layer,q]=layers[m[0]],power=m.endsWith("'")?3:m.endsWith('2')?2:1;
  const dest=slots.map(s=>{
    const at=s.p[axis]===layer?{p:rotate(s.p,axis,q*power),n:rotate(s.n,axis,q*power)}:s;
    const ix=positions.get(id(at));
    assert(Number.isInteger(ix));
    return ix;
  });
  assert.equal(new Set(dest).size,54);
  return dest;
});
const goal=[...F].map(f=>f.repeat(9)).join('');
function act(state,m){const out=Array(54);for(let i=0;i<54;i++)out[moves[m][i]]=state[i];return out.join('')}
const H=names.map((name,i)=>name.endsWith('2')?i:-1).filter(x=>x>=0);
function bfs(moveset,maxDepth){
  const visited=new Map([[goal,0]]);
  let frontier=[goal],layers=[1];
  for(let d=1;d<=maxDepth;d++){
    const next=[];
    for(const state of frontier)for(const m of moveset){
      const t=act(state,m);
      if(visited.has(t))continue;
      visited.set(t,d);next.push(t);
    }
    frontier=next;layers.push(next.length);
  }
  return {visited,layers};
}
const full=bfs(names.map((_,i)=>i),5);
const Hfull=bfs(H,16);
assert.deepEqual(full.layers,[1,18,243,3240,43239,574908]);
assert.deepEqual(Hfull.layers,[1,6,27,120,519,1932,6484,20310,55034,113892,178495,179196,89728,16176,1488,144,0]);
assert.equal(Hfull.visited.size,663552,'Independent actual 54-facelet six-halfturn subgroup order');
const edgePositions=[...new Set(slots.filter(s=>s.p.filter(x=>Math.abs(x)===1).length===2)
  .map(s=>s.p.join(',')))].sort();
assert.equal(edgePositions.length,12);
const locations=edgePositions.map(p=>slots.map((s,i)=>s.p.join(',')===p?i:-1).filter(i=>i>=0));
assert(locations.every(a=>a.length===2));
const edgeIds=locations.map(two=>two.map(i=>goal[i]).sort().join(''));
assert.equal(new Set(edgeIds).size,12);
const parent=Array.from({length:12},(_,i)=>i);
function root(i){while(parent[i]!==i)i=parent[i];return i}
function union(i,j){parent[root(i)]=root(j)}
for(const m of H){
  const state=act(goal,m);
  for(let i=0;i<12;i++){
    const displaced=edgeIds.indexOf(locations[i].map(j=>state[j]).sort().join(''));
    assert(displaced>=0);union(i,displaced);
  }
}
const groups=new Map();
for(let i=0;i<12;i++){let p=root(i);groups.set(p,[...(groups.get(p)||[]),i])}
const orbits=[...groups.values()].map(g=>g.map(i=>edgeIds[i]).sort()).sort((a,b)=>a[0].localeCompare(b[0]));
assert.deepEqual(orbits,[['BL','BR','FL','FR'],['BD','BU','DF','FU'],['DL','DR','LU','RU']].sort((a,b)=>a[0].localeCompare(b[0])));
assert.deepEqual(orbits.map(g=>g.length),[4,4,4]);
const orbitLabel=Array(12);
for(let label=0;label<orbits.length;label++)
  for(const color of orbits[label])orbitLabel[edgeIds.indexOf(color)]=label;
function orbitPreserved(state){
  for(let i=0;i<12;i++){
    const color=locations[i].map(j=>state[j]).sort().join('');
    const piece=edgeIds.indexOf(color);
    assert(piece>=0);
    if(orbitLabel[piece]!==orbitLabel[i])return false;
  }
  return true;
}
for(const state of Hfull.visited.keys())assert(orbitPreserved(state),'The three physical edge tetrads must be subgroup invariants');
const orbitCount=Array(6).fill(0),members=Array(6).fill(0),d5={};
for(const [state,depth] of full.visited){
  const o=orbitPreserved(state),h=Hfull.visited.get(state);
  if(o)orbitCount[depth]++;
  if(h!==undefined){
    assert(o,'H-subgroup element violates a genuine orbit invariant');
    members[depth]++;
    if(depth===5)d5[h]=(d5[h]||0)+1;
  }
  assert.equal(o,h!==undefined,'First P1 finite cohort equality fails');
}
assert.deepEqual(orbitCount,[1,6,27,120,519,2124]);
assert.deepEqual(members,orbitCount);
assert.deepEqual(d5,{'5':1932,'8':96,'9':96});
function actualShortestWord(state,moveSet,distances){
  const sequence=[];
  while(state!==goal){
    const d=distances.get(state);
    assert(Number.isInteger(d)&&d>0);
    const move=moveSet.find(i=>distances.get(act(state,i))===d-1);
    assert(Number.isInteger(move),'No predecessor for a physical shortest word');
    state=act(state,move);
    sequence.push(names[move]);
  }
  return sequence;
}
function wordState(steps){
  let state=goal;
  for(const turn of steps){const m=names.indexOf(turn);assert(m>=0);state=act(state,m)}
  return state;
}
function solveActual(state,word){
  for(const token of word){const m=names.indexOf(token);assert(m>=0);state=act(state,m)}
  return state===goal;
}
const witnessCases=[
  {scramble:'D U R2 D U',d18:5,dH:9},
  {scramble:"D U R2 D' U",d18:5,dH:8}
];
const witnesses=witnessCases.map(w=>{
  const state=wordState(w.scramble.split(' '));
  assert(orbitPreserved(state));
  assert.equal(full.visited.get(state),w.d18);
  assert.equal(Hfull.visited.get(state),w.dH);
  const fullWord=actualShortestWord(state,names.map((_,i)=>i),full.visited);
  const hWord=actualShortestWord(state,H,Hfull.visited);
  assert.equal(fullWord.length,w.d18);
  assert.equal(hWord.length,w.dH);
  assert(solveActual(state,fullWord));
  assert(solveActual(state,hWord));
  return {source_scramble:w.scramble,globally_shortest_HTM_solution:fullWord.join(' '),halfturn_only_exact_shortest_solution:hWord.join(' '),d18:w.d18,dH:w.dH,source_geometry:'original 54 facelets',both_solutions_solve_all_54_stickers:true};
});
console.log(JSON.stringify({
 marker:'CUBE_REV_024_P1_R0_FULL_PHYSICAL_H_GROUP_GEODESIC_DISTORTION',
 full18_depth_layers_0_to5:full.layers,
 full18_ball_distinct_states:full.visited.size,
 H_six_halfturn_complete_Cayley_shells:Hfull.layers,
 exact_entire_H_group_order:Hfull.visited.size,
 three_true_edge_tetrads:orbits,
 orbit_preserving_full18_depths:orbitCount,
 exact_H_members_in_full18_depths:members,
 all18_depth5_orbit_preserving_vs_H_word_cost:d5,
 all18_depth5_strict_H_distance_penalty4_cases:96,
 all18_depth5_strict_H_distance_penalty3_cases:96,
 zero_H_members_missing_from_orbit_preserving_full18_ball_through5:true,
 original_54_facelet_geodesic_replayed_counterexamples:witnesses,
 global_H_membership_equivalence_unproven_outside_tested_ball:true,
 not_human_cognitive_behavior:true
},null,2));
