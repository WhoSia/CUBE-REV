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
const full=bfs(names.map((_,i)=>i),4),half=bfs(H,5);
assert.deepEqual(full.layers,[1,18,243,3240,43239]);
assert.deepEqual(half.layers,[1,6,27,120,519,1932]);
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
for(const state of half.visited.keys())assert(orbitPreserved(state),'True halfturn word must respect all three tetrads');
const goodByDepth=Array(5).fill(0),badByDepth=Array(5).fill(0),hitByDepth=Array(5).fill(0);
for(const [state,depth] of full.visited){
  const good=orbitPreserved(state),hit=half.visited.has(state);
  if(good)goodByDepth[depth]++;else badByDepth[depth]++;
  if(hit)hitByDepth[depth]++;
  assert(!hit||good,'Necessary orbit invariant');
  assert.equal(good,hit,'Finite radius4 counterexample to exact orbit gate completeness');
}
assert.deepEqual(goodByDepth,[1,6,27,120,519]);
assert.deepEqual(badByDepth,[0,12,216,3120,42720]);
assert.deepEqual(hitByDepth,goodByDepth);
console.log(JSON.stringify({
 marker:'CUBE_REV_024_P0_R1_REAL_54_STICKER_EDGE_TETRAD_INVARIANT',
 whole18_exact_layers_r4:full.layers,
 six_halfturn_exact_layers_r5:half.layers,
 three_physically_generated_edge_orbits:orbits,
 real_full18_states_r4:full.visited.size,
 orbit_preserved_and_halfturn_reachable_within5:goodByDepth.reduce((a,b)=>a+b,0),
 violated_orbit_and_unbounded_halfturn_impossible:badByDepth.reduce((a,b)=>a+b,0),
 by_depth_orbit_preserved:goodByDepth,
 by_depth_orbit_violated:badByDepth,
 exact_on_this_finite_r4_cohort_only:true,
 edge_orbit_condition_globally_sufficient:false,
 human_behaviour_inferred:false
},null,2));
