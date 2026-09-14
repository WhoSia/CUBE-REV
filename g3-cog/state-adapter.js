export const FACES=['U','R','F','D','L','B'];
const FACE_DEF={
 U:{n:[0,1,0],axis:'y',layer:1,sign:-1,color:'U'},
 D:{n:[0,-1,0],axis:'y',layer:-1,sign:1,color:'D'},
 R:{n:[1,0,0],axis:'x',layer:1,sign:-1,color:'R'},
 L:{n:[-1,0,0],axis:'x',layer:-1,sign:1,color:'L'},
 F:{n:[0,0,1],axis:'z',layer:1,sign:-1,color:'F'},
 B:{n:[0,0,-1],axis:'z',layer:-1,sign:1,color:'B'}
};

function rotPos(v,axis,q){
  const [x,y,z]=v;
  if(axis==='x') return q===1?[x,-z,y]:[x,z,-y];
  if(axis==='y') return q===1?[z,y,-x]:[-z,y,x];
  return q===1?[-y,x,z]:[y,-x,z];
}

function faceStickerPositions(face){
  const out=[];
  for(let a=-1;a<=1;a++) for(let b=-1;b<=1;b++){
    if(face==='U'||face==='D') out.push([a,FACE_DEF[face].layer,b]);
    else if(face==='R'||face==='L') out.push([FACE_DEF[face].layer,a,b]);
    else out.push([a,b,FACE_DEF[face].layer]);
  }
  return out;
}

export function solvedState(){
  const stickers=[];
  for(const face of FACES){
    const def=FACE_DEF[face];
    for(const p of faceStickerPositions(face)) stickers.push({p:[...p],n:[...def.n],c:def.color});
  }
  return stickers;
}

export function cloneState(state){return state.map(s=>({p:[...s.p],n:[...s.n],c:s.c}));}

export function parseToken(token){
  const face=token[0];
  if(!FACE_DEF[face]) throw new Error(`unsupported token ${token}`);
  const suffix=token.slice(1);
  if(suffix==='' ) return {face,quarter:1};
  if(suffix==="'") return {face,quarter:-1};
  if(suffix==='2') return {face,quarter:2};
  throw new Error(`unsupported token ${token}`);
}

export function applyMove(state,token){
  const {face,quarter}=parseToken(token),def=FACE_DEF[face];
  let steps=quarter===2?2:1;
  const q=quarter===-1?-def.sign:def.sign;
  while(steps--){
    for(const s of state){
      const coord=def.axis==='x'?s.p[0]:def.axis==='y'?s.p[1]:s.p[2];
      if(coord===def.layer){s.p=rotPos(s.p,def.axis,q);s.n=rotPos(s.n,def.axis,q);}
    }
  }
  return state;
}

export function applySequence(start,tokens){
  const s=cloneState(start);
  for(const t of tokens) applyMove(s,t);
  return s;
}

export function serializeState(state){
  return state.map(s=>({p:s.p,n:s.n,c:s.c}))
    .sort((a,b)=>{
      const ak=[...a.p,...a.n,a.c].join(','),bk=[...b.p,...b.n,b.c].join(',');
      return ak.localeCompare(bk);
    })
    .map(s=>`${s.p.join('')}:${s.n.join('')}:${s.c}`).join('|');
}

export function equalState(a,b){return serializeState(a)===serializeState(b);}

export async function sha256Text(text){
  const bytes=new TextEncoder().encode(text);
  const dig=await crypto.subtle.digest('SHA-256',bytes);
  return [...new Uint8Array(dig)].map(x=>x.toString(16).padStart(2,'0')).join('');
}

export async function stateDigest(state){return sha256Text(serializeState(state));}

export function checkpointStates(start,tokens){
  const s=cloneState(start),out=[cloneState(s)];
  for(const t of tokens){applyMove(s,t);out.push(cloneState(s));}
  return out;
}
