const FACE_NORMALS={
  U:[0,1,0],R:[1,0,0],F:[0,0,1],D:[0,-1,0],L:[-1,0,0],B:[0,0,-1]
};
const FACE_COLORS={U:"U",R:"R",F:"F",D:"D",L:"L",B:"B"};

const DIRS=[[1,0,0],[-1,0,0],[0,1,0],[0,-1,0],[0,0,1],[0,0,-1]];
const eq=(a,b)=>a[0]===b[0]&&a[1]===b[1]&&a[2]===b[2];
const dot=(a,b)=>a[0]*b[0]+a[1]*b[1]+a[2]*b[2];
const cross=(a,b)=>[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]];
const add=(a,b)=>[a[0]+b[0],a[1]+b[1],a[2]+b[2]];

export function solvedStickerCube(){
  const out=[];
  for(const face of Object.keys(FACE_NORMALS)){
    const n=FACE_NORMALS[face], c=FACE_COLORS[face];
    for(const a of [-1,0,1]) for(const b of [-1,0,1]){
      let p;
      if(n[0]) p=[n[0],a,b];
      else if(n[1]) p=[a,n[1],b];
      else p=[a,b,n[2]];
      out.push({p,n:[...n],c});
    }
  }
  return out;
}
function rotVec(v,axis,q){
  let [x,y,z]=v;
  q=((q%4)+4)%4;
  for(let i=0;i<q;i++){
    if(axis==="x") [x,y,z]=[x,-z,y];
    else if(axis==="y") [x,y,z]=[z,y,-x];
    else [x,y,z]=[-y,x,z];
  }
  return [x,y,z];
}
function primitive(cube,base,power){
  if("URFDLB".includes(base)){
    const m={
      U:["y",1,-1],D:["y",-1,1],R:["x",1,-1],
      L:["x",-1,1],F:["z",1,-1],B:["z",-1,1]
    }[base];
    const [axis,layer,q]=m;
    for(let k=0;k<power;k++) for(const s of cube){
      const idx=axis==="x"?0:axis==="y"?1:2;
      if(s.p[idx]===layer){s.p=rotVec(s.p,axis,q);s.n=rotVec(s.n,axis,q);}
    }
    return;
  }
  if("xyz".includes(base)){
    const [axis,q]={x:["x",-1],y:["y",-1],z:["z",-1]}[base];
    for(let k=0;k<power;k++) for(const s of cube){
      s.p=rotVec(s.p,axis,q);s.n=rotVec(s.n,axis,q);
    }
    return;
  }
  throw new Error("PRIMITIVE:"+base);
}
export function parseMoveToken(raw){
  const token=String(raw).replace(/[’′]/g,"'").trim();
  const m=token.match(/^([URFDLB]w|[urfdlb]|[MESxyz]|[URFDLB])(2'?|'?)$/);
  if(!m) throw new Error("UNSUPPORTED_TOKEN:"+token);
  const [,base,suffix]=m;
  const power=suffix.startsWith("2")?2:(suffix==="'"?3:1);
  return {base,power,raw:token};
}
export function applyMoveToken(cube,raw){
  const {base,power}=parseMoveToken(raw);
  if("URFDLBxyz".includes(base)){primitive(cube,base,power);return cube;}
  const key=base.endsWith("w")?base[0].toLowerCase():base;
  const seq={
    r:["x","L"], l:["x'","R"], u:["y","D"], d:["y'","U"], f:["z","B"], b:["z'","F"],
    M:["x'","L'","R"], E:["y'","D'","U"], S:["F'","B","z"]
  }[key];
  if(!seq) throw new Error("EXTENDED_TOKEN:"+raw);
  for(let k=0;k<power;k++) for(const t of seq) applyMoveToken(cube,t);
  return cube;
}
export function applyAlgorithm(cube,text){
  for(const t of String(text).trim().split(/\s+/).filter(Boolean)) applyMoveToken(cube,t);
  return cube;
}
export function solvedUpToRotation(cube){
  const groups=new Map();
  for(const s of cube){
    const k=s.n.join(",");
    if(!groups.has(k)) groups.set(k,[]);
    groups.get(k).push(s.c);
  }
  return groups.size===6&&[...groups.values()].every(x=>x.length===9&&new Set(x).size===1);
}
function orientationMatrices(){
  const out=[];
  for(const ex of DIRS) for(const ey of DIRS){
    if(dot(ex,ey)!==0) continue;
    const ez=cross(ex,ey);
    if(!DIRS.some(d=>eq(d,ez))) continue;
    out.push([ex,ey,ez]);
  }
  return out;
}
const ORIENTATIONS=orientationMatrices();
function matApply(M,v){
  return [0,1,2].map(i=>v[0]*M[0][i]+v[1]*M[1][i]+v[2]*M[2][i]);
}
export function canonicalizeCenters(cube){
  const centers={};
  for(const s of cube) if(eq(s.p,s.n)) centers[s.c]=s.n;
  const M=ORIENTATIONS.find(T=>eq(matApply(T,centers.U),FACE_NORMALS.U)&&eq(matApply(T,centers.F),FACE_NORMALS.F));
  if(!M) throw new Error("CENTER_FRAME_NOT_ORIENTABLE");
  return cube.map(s=>({p:matApply(M,s.p),n:matApply(M,s.n),c:s.c}));
}
const CORNER_NORMALS=[
  [[0,1,0],[1,0,0],[0,0,1]], [[0,1,0],[0,0,1],[-1,0,0]],
  [[0,1,0],[-1,0,0],[0,0,-1]], [[0,1,0],[0,0,-1],[1,0,0]],
  [[0,-1,0],[0,0,1],[1,0,0]], [[0,-1,0],[-1,0,0],[0,0,1]],
  [[0,-1,0],[0,0,-1],[-1,0,0]], [[0,-1,0],[1,0,0],[0,0,-1]]
];
const CORNER_COLORS=[
  ["U","R","F"],["U","F","L"],["U","L","B"],["U","B","R"],
  ["D","F","R"],["D","L","F"],["D","B","L"],["D","R","B"]
];
const EDGE_NORMALS=[
  [[0,1,0],[1,0,0]],[[0,1,0],[0,0,1]],[[0,1,0],[-1,0,0]],[[0,1,0],[0,0,-1]],
  [[0,-1,0],[1,0,0]],[[0,-1,0],[0,0,1]],[[0,-1,0],[-1,0,0]],[[0,-1,0],[0,0,-1]],
  [[0,0,1],[1,0,0]],[[0,0,1],[-1,0,0]],[[0,0,-1],[-1,0,0]],[[0,0,-1],[1,0,0]]
];
const EDGE_COLORS=[
  ["U","R"],["U","F"],["U","L"],["U","B"],["D","R"],["D","F"],["D","L"],["D","B"],
  ["F","R"],["F","L"],["B","L"],["B","R"]
];
const posOf=normals=>normals.reduce((a,b)=>add(a,b),[0,0,0]);
const key=(p,n)=>p.join(",")+"|"+n.join(",");
export function toCubieState(cube){
  const c=canonicalizeCenters(cube);
  const mp=new Map(c.map(s=>[key(s.p,s.n),s.c]));
  const cp=[],co=[],ep=[],eo=[];
  for(const normals of CORNER_NORMALS){
    const pos=posOf(normals);
    const colors=normals.map(n=>mp.get(key(pos,n)));
    const ori=colors.findIndex(x=>x==="U"||x==="D");
    if(ori<0) throw new Error("CORNER_ORIENTATION");
    const c1=colors[(ori+1)%3], c2=colors[(ori+2)%3];
    const cubie=CORNER_COLORS.findIndex(x=>x[1]===c1&&x[2]===c2);
    if(cubie<0) throw new Error("CORNER_ID");
    cp.push(cubie);co.push(ori%3);
  }
  for(const normals of EDGE_NORMALS){
    const pos=posOf(normals);
    const colors=normals.map(n=>mp.get(key(pos,n)));
    let found=-1,flip=0;
    for(let j=0;j<EDGE_COLORS.length;j++){
      const x=EDGE_COLORS[j];
      if(colors[0]===x[0]&&colors[1]===x[1]){found=j;flip=0;break;}
      if(colors[0]===x[1]&&colors[1]===x[0]){found=j;flip=1;break;}
    }
    if(found<0) throw new Error("EDGE_ID");
    ep.push(found);eo.push(flip);
  }
  return {cp,co,ep,eo};
}
export function cubieSolved(s){
  return s.cp.every((x,i)=>x===i)&&s.co.every(x=>x===0)&&s.ep.every((x,i)=>x===i)&&s.eo.every(x=>x===0);
}
export function faceActionIndex(raw){
  const {base,power}=parseMoveToken(raw);
  if(!"URFDLB".includes(base)) return null;
  const face="URFDLB".indexOf(base);
  return face*3+(power-1);
}
