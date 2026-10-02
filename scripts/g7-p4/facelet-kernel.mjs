const AXES = {x:0,y:1,z:2};
const FACE_COLOR = {
  "0,1,0":"U","1,0,0":"R","0,0,1":"F",
  "0,-1,0":"D","-1,0,0":"L","0,0,-1":"B"
};

function key(v){return v.join(",");}
function rot90(v,axis,sign){
  const [x,y,z]=v;
  if(axis==="x") return sign===1 ? [x,-z,y] : [x,z,-y];
  if(axis==="y") return sign===1 ? [z,y,-x] : [-z,y,x];
  if(axis==="z") return sign===1 ? [-y,x,z] : [y,-x,z];
  throw new Error("AXIS");
}
function powQuarter(v,axis,q){
  let out=v;
  const n=((q%4)+4)%4;
  for(let i=0;i<n;i++) out=rot90(out,axis,1);
  return out;
}
function surfaceToken(raw){
  return String(raw).replace(/[’′]/g,"'").trim().replace(/^[()]+|[()]+$/g,"");
}
function tokenBase(raw){
  const t=surfaceToken(raw);
  const m=t.match(/^([URFDLBMESxyz]|[URFDLB]w|[urfdlb])(2'?|'|)?$/);
  if(!m) throw new Error("UNSUPPORTED_TOKEN:"+t);
  let base=m[1], suffix=m[2]||"";
  if(/^[urfdlb]$/.test(base)) base=base.toUpperCase()+"w";
  const power=suffix.startsWith("2")?2:suffix==="'"?3:1;
  return {base,power,raw:t};
}
export function expandToken(raw){
  const t=surfaceToken(raw);
  try{return [tokenBase(t)];}catch{}
  const memo=new Map();
  function rec(i){
    if(i===t.length) return [[]];
    if(memo.has(i)) return memo.get(i);
    const out=[];
    for(let j=i+1;j<=t.length;j++){
      const part=t.slice(i,j);
      let base;
      try{base=tokenBase(part);}catch{continue;}
      for(const tail of rec(j)){
        out.push([base,...tail]);
        if(out.length>1) break;
      }
      if(out.length>1) break;
    }
    memo.set(i,out);
    return out;
  }
  const xs=rec(0);
  if(xs.length!==1 || xs[0].length<2) throw new Error(xs.length>1?"AMBIGUOUS_TOKEN:"+t:"UNSUPPORTED_TOKEN:"+t);
  return xs[0];
}
const BASE = {
  U:{axis:"y",selector:p=>p[1]===1,q:-1},
  D:{axis:"y",selector:p=>p[1]===-1,q:1},
  R:{axis:"x",selector:p=>p[0]===1,q:-1},
  L:{axis:"x",selector:p=>p[0]===-1,q:1},
  F:{axis:"z",selector:p=>p[2]===1,q:-1},
  B:{axis:"z",selector:p=>p[2]===-1,q:1},
  M:{axis:"x",selector:p=>p[0]===0,q:1},
  E:{axis:"y",selector:p=>p[1]===0,q:1},
  S:{axis:"z",selector:p=>p[2]===0,q:-1},
  Uw:{axis:"y",selector:p=>p[1]>=0,q:-1},
  Dw:{axis:"y",selector:p=>p[1]<=0,q:1},
  Rw:{axis:"x",selector:p=>p[0]>=0,q:-1},
  Lw:{axis:"x",selector:p=>p[0]<=0,q:1},
  Fw:{axis:"z",selector:p=>p[2]>=0,q:-1},
  Bw:{axis:"z",selector:p=>p[2]<=0,q:1},
  x:{axis:"x",selector:()=>true,q:-1},
  y:{axis:"y",selector:()=>true,q:-1},
  z:{axis:"z",selector:()=>true,q:-1},
};

export function solvedStickers(){
  const out=[];
  let id=0;
  for(const [normalKey,color] of Object.entries(FACE_COLOR)){
    const normal=normalKey.split(",").map(Number);
    const axis=normal.findIndex(x=>x!==0);
    for(const a of [-1,0,1]) for(const b of [-1,0,1]){
      const pos=[0,0,0];
      pos[axis]=normal[axis];
      const rest=[0,1,2].filter(i=>i!==axis);
      pos[rest[0]]=a; pos[rest[1]]=b;
      out.push({id:id++,pos,normal:[...normal],color});
    }
  }
  return out;
}
export function applyToken(stickers,raw){
  let out=stickers;
  for(const {base,power} of expandToken(raw)){
    const spec=BASE[base];
    if(!spec) throw new Error("UNSUPPORTED_BASE:"+base);
    const q=spec.q*power;
    out=out.map(s=>{
      if(!spec.selector(s.pos)) return {id:s.id,pos:[...s.pos],normal:[...s.normal],color:s.color};
      return {id:s.id,pos:powQuarter(s.pos,spec.axis,q),normal:powQuarter(s.normal,spec.axis,q),color:s.color};
    });
  }
  return out;
}
export function applyAlg(stickers,text){
  let out=stickers;
  const tokens=String(text).trim().split(/\s+/).filter(Boolean);
  for(const t of tokens) out=applyToken(out,t);
  return out;
}
export function stateSignature(stickers){
  return stickers.slice().sort((a,b)=>a.id-b.id).map(s=>s.id+":"+key(s.pos)+":"+key(s.normal)+":"+s.color).join("|");
}
export function isSolvedUpToRotation(stickers){
  const groups=new Map();
  for(const s of stickers){
    const k=key(s.normal);
    if(!groups.has(k)) groups.set(k,new Set());
    groups.get(k).add(s.color);
  }
  if(groups.size!==6) return false;
  const colors=[];
  for(const set of groups.values()){
    if(set.size!==1) return false;
    colors.push([...set][0]);
  }
  return new Set(colors).size===6;
}
export function validateStickerState(stickers){
  if(stickers.length!==54) return false;
  const ids=stickers.map(s=>s.id).sort((a,b)=>a-b);
  if(ids.some((x,i)=>x!==i)) return false;
  for(const s of stickers){
    if(!FACE_COLOR[key(s.normal)]) return false;
    const boundary=s.pos.filter(v=>Math.abs(v)===1).length;
    if(boundary<1) return false;
    if(s.normal.reduce((a,x)=>a+Math.abs(x),0)!==1) return false;
    if(s.pos.some(v=>![-1,0,1].includes(v))) return false;
  }
  return true;
}
export function normalizeToken(raw){return expandToken(raw);}
