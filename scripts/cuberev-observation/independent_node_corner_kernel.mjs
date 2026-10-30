// Independent 54-sticker source-faithful Node physical check, not Python port import.
// Original 0.24 physical coordinate model uses face-normal geometry and 18HTM.
const F='URFDLB';
const N={U:[0,1,0],R:[1,0,0],F:[0,0,1],D:[0,-1,0],L:[-1,0,0],B:[0,0,-1]};
const G={U:[1,1,-1],R:[0,1,-1],F:[2,1,-1],D:[1,-1,1],L:[0,-1,1],B:[2,-1,1]};
const slots=[];
for(const f of F){
  const n=N[f], row=[];
  for(let x=-1;x<=1;x++)for(let y=-1;y<=1;y++)
    row.push({p:n[0]?[n[0],x,y]:n[1]?[x,n[1],y]:[x,y,n[2]],n});
  row.sort((a,b)=>a.p.join(',').localeCompare(b.p.join(','),'en'));
  slots.push(...row);
}
const key=s=>s.p.join(',')+'|'+s.n.join(',');
const loc=new Map(slots.map((s,i)=>[key(s),i]));
function rotate(v,ax,n){
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
  return slots.map(s=>{
    const t=s.p[ax]===layer?
      {p:rotate(s.p,ax,q*power),n:rotate(s.n,ax,q*power)}:s;
    return loc.get(key(t));
  });
});
const solved=[...F].map(f=>f.repeat(9)).join('');
function turn(s,a){
  const r=Array(54),p=perm[actions.indexOf(a)];
  for(let j=0;j<54;j++)r[p[j]]=s[j];
  return r.join('');
}
function sequence(w){return w.split(' ').reduce(turn,solved);}
const edges=[['U','R'],['U','F'],['U','L'],['U','B'],
 ['D','R'],['D','F'],['D','L'],['D','B'],
 ['F','R'],['F','L'],['B','L'],['B','R']];
const edgeSlots=edges.map(([a,b])=>{
  const p=N[a].map((v,i)=>v+N[b][i]);
  return [loc.get(p.join(',')+'|'+N[a].join(',')),
          loc.get(p.join(',')+'|'+N[b].join(','))];
});
function edgeFactors(s){
  return edges.map(([a,b])=>{
    for(let j=0;j<12;j++){
      const [i,k]=edgeSlots[j];
      if(s[i]===a&&s[k]===b)return 2*j;
      if(s[i]===b&&s[k]===a)return 2*j+1;
    }
    throw Error('missing tagged original edge');
  });
}
const word="U L U' R U L' U' R'";
const a=sequence("U L U' R"),b=sequence("R U L U'"),g=sequence(word);
if(g===solved||edgeFactors(g).join()!==edgeFactors(solved).join())
  throw Error('corner-only commutator check failed');
if(a===b||edgeFactors(a).join()!==edgeFactors(b).join())
  throw Error('B4 distinct physical states collision check failed');
console.log(JSON.stringify({
 status:'INDEPENDENT_0_24_NODE_FULL54_CORNER_KERNEL_PASS',
 commutator:word,nonidentity:true,all_twelve_edges_fixed:true,
 radius4_words:["U L U' R","R U L U'"],same_all_twelve_edge_factors:true,
 altered_face_stickers:[...g].filter((x,i)=>x!==solved[i]).length
}));
