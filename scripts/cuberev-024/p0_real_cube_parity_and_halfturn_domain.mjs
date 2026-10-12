// CUBE-REV 0.24 P0 — complete original-facelet physical control cohort.
// Legal outer 18 HTM, 54 ordered sticker coordinates and normal vectors;
// six H-only half turns and exact corner cubie parity (no human data).
import assert from 'node:assert/strict';
const F='URFDLB';
const N={U:[0,1,0],R:[1,0,0],F:[0,0,1],D:[0,-1,0],L:[-1,0,0],B:[0,0,-1]};
const G={U:[1,1,-1],R:[0,1,-1],F:[2,1,-1],D:[1,-1,1],L:[0,-1,1],B:[2,-1,1]};
const slots=[];
for(const f of F){
  const n=N[f],a=[];
  for(let x=-1;x<=1;x++)for(let y=-1;y<=1;y++)
    a.push({p:n[0]?[n[0],x,y]:n[1]?[x,n[1],y]:[x,y,n[2]],n});
  a.sort((a,b)=>a.p.join(',').localeCompare(b.p.join(','),'en'));
  slots.push(...a);
}
const k=s=>s.p.join(',')+'|'+s.n.join(','), loc=new Map(slots.map((s,i)=>[k(s),i]));
assert.equal(loc.size,54);
function rot(v,ax,n){
  let [x,y,z]=v;
  for(let i=0;i<(n+4)%4;i++){
    if(ax===0)[x,y,z]=[x,-z,y];
    if(ax===1)[x,y,z]=[z,y,-x];
    if(ax===2)[x,y,z]=[-y,x,z];
  }
  return [x,y,z];
}
const actions=[...F].flatMap(f=>[f,f+"'",f+'2']);
const perm=actions.map(m=>{
  const [ax,layer,q]=G[m[0]],power=m.endsWith("'")?3:m.endsWith('2')?2:1;
  const p=slots.map(s=>{
    const t=s.p[ax]===layer?{p:rot(s.p,ax,q*power),n:rot(s.n,ax,q*power)}:s;
    return loc.get(k(t));
  });
  assert.equal(new Set(p).size,54);
  return p;
});
const solved=[...F].map(f=>f.repeat(9)).join('');
function turn(s,idx){
  const arr=Array(54),p=perm[idx];
  for(let j=0;j<54;j++)arr[p[j]]=s[j];
  return arr.join('');
}
for(let i=0;i<18;i++){
  const t=actions[i],back=t.endsWith('2')?t:t.endsWith("'")?t[0]:t+"'";
  assert.equal(turn(turn(solved,i),actions.indexOf(back)),solved);
}
const half=actions.map((t,i)=>t.endsWith('2')?i:-1).filter(i=>i>=0);
function bfs(alphabet,radius){
  const seen=new Map([[solved,{d:0,shortest:1}]]);
  let frontier=[solved],layers=[1];
  for(let d=1;d<=radius;d++){
    const next=[];
    for(const s of frontier)for(const m of alphabet){
      const t=turn(s,m),previous=seen.get(t),ways=seen.get(s).shortest;
      if(previous){if(previous.d===d)previous.shortest+=ways;continue;}
      seen.set(t,{d,shortest:ways});next.push(t);
    }
    frontier=next;layers.push(next.length);
  }
  return {seen,layers};
}
const full=bfs(actions.map((_,i)=>i),3);
const h5=bfs(half,5);
assert.deepEqual(full.layers,[1,18,243,3240]);
assert.deepEqual(h5.layers,[1,6,27,120,519,1932]);
const positions=[...new Set(slots.filter(s=>s.p.every(x=>Math.abs(x)===1))
  .map(s=>s.p.join(',')))].sort();
assert.equal(positions.length,8);
const colorSlots=positions.map(p=>slots.map((s,i)=>s.p.join(',')===p?i:-1).filter(i=>i>=0));
assert(colorSlots.every(a=>a.length===3));
const names=colorSlots.map(indices=>indices.map(i=>solved[i]).sort().join(''));
assert.equal(new Set(names).size,8);
function cornerParity(state){
  const permutation=colorSlots.map(index=>names.indexOf(index.map(i=>state[i]).sort().join('')));
  assert(permutation.every(i=>i>=0));
  let inversions=0;
  for(let i=0;i<8;i++)for(let j=i+1;j<8;j++)if(permutation[i]>permutation[j])inversions++;
  return inversions%2;
}
const census=Array.from({length:4},()=>({half5:0,even_outside_half5:0,odd_proven_outside_half_group:0}));
const examples=[];
for(const [state,v] of full.seen){
  const parity=cornerParity(state),bounded=h5.seen.has(state);
  if(bounded)assert.equal(parity,0,'Halfturn subgroup must preserve corner sign');
  const field=bounded?'half5':parity?'odd_proven_outside_half_group':'even_outside_half5';
  census[v.d][field]++;
  if(parity===0&&!bounded&&examples.length<3)
    examples.push({depth:v.d,physical_state_SHA_unpublished:true,bounded_h5:false});
  if(v.d>0){
    let parents=0,words=0;
    for(let j=0;j<18;j++){
      const prior=full.seen.get(turn(state,j));
      if(prior?.d===v.d-1){parents++;words+=prior.shortest;}
    }
    assert(parents>0&&words===v.shortest);
  }
}
assert.deepEqual(census,[
  {half5:1,even_outside_half5:0,odd_proven_outside_half_group:0},
  {half5:6,even_outside_half5:0,odd_proven_outside_half_group:12},
  {half5:27,even_outside_half5:108,odd_proven_outside_half_group:108},
  {half5:120,even_outside_half5:1440,odd_proven_outside_half_group:1680},
]);
assert.equal(census.flatMap(x=>Object.values(x)).reduce((x,y)=>x+y,0),3502);
assert.equal(census.reduce((n,x)=>n+x.half5,0),154);
console.log(JSON.stringify({
  marker:'CUBE_REV_024_P0_ORIGINAL_54_STICKER_EXACT_DOMAIN_BASELINE',
  full18_exact_layers_r3:full.layers,
  half6_exact_layers_r5:h5.layers,
  total_full18_r3_states:full.seen.size,
  half6_reachable_within_r5:154,
  even_parity_but_not_within_half6_r5:1548,
  odd_corner_parity_proven_excluded_from_all_halfturn_words:1800,
  per_depth_census:census,
  proof_scope:'Finite radius3 full-18HTM cohort; corner-sign algebra excludes odd states for UNBOUNDED halfturn language. Even outside H5 is ONLY bounded negative evidence.',
  participant_actions_measured:false,
  special_same_corner_62_cohort_generalized:false
},null,2));
