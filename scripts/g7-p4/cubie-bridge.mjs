import {solvedStickers,applyToken} from "./facelet-kernel.mjs";

const FACE_VEC={U:[0,1,0],R:[1,0,0],F:[0,0,1],D:[0,-1,0],L:[-1,0,0],B:[0,0,-1]};
const key=v=>v.join(",");
const add=(a,b)=>a.map((x,i)=>x+b[i]);
const scale=(a,k)=>a.map(x=>x*k);

function centers(stickers){
  const out=new Map();
  for(const s of stickers){
    if(s.pos.every((v,i)=>v===s.normal[i])) out.set(s.color,[...s.normal]);
  }
  if(out.size!==6) throw new Error("CENTER_MAP");
  return out;
}
export function canonicalizeByCenters(stickers){
  const c=centers(stickers);
  const desired=FACE_VEC;
  const currentToCanonical=new Map();
  for(const [color,n] of c) currentToCanonical.set(key(n),desired[color]);
  const ex=currentToCanonical.get("1,0,0");
  const ey=currentToCanonical.get("0,1,0");
  const ez=currentToCanonical.get("0,0,1");
  if(!ex||!ey||!ez) throw new Error("CENTER_BASIS");
  const tx=v=>add(add(scale(ex,v[0]),scale(ey,v[1])),scale(ez,v[2]));
  return stickers.map(s=>({id:s.id,pos:tx(s.pos),normal:tx(s.normal),color:s.color}));
}

const CORNER_POS=[
  [1,1,1],[-1,1,1],[-1,1,-1],[1,1,-1],
  [1,-1,1],[-1,-1,1],[-1,-1,-1],[1,-1,-1]
];
const CORNER_FACES=[
  ["U","R","F"],["U","F","L"],["U","L","B"],["U","B","R"],
  ["D","F","R"],["D","L","F"],["D","B","L"],["D","R","B"]
];
const CORNER_COLORS=CORNER_FACES;

const EDGE_POS=[
  [1,1,0],[0,1,1],[-1,1,0],[0,1,-1],
  [1,-1,0],[0,-1,1],[-1,-1,0],[0,-1,-1],
  [1,0,1],[-1,0,1],[-1,0,-1],[1,0,-1]
];
const EDGE_FACES=[
  ["U","R"],["U","F"],["U","L"],["U","B"],
  ["D","R"],["D","F"],["D","L"],["D","B"],
  ["F","R"],["F","L"],["B","L"],["B","R"]
];
const EDGE_COLORS=EDGE_FACES;

function stickerColor(stickers,pos,normal){
  const s=stickers.find(x=>key(x.pos)===key(pos)&&key(x.normal)===key(normal));
  if(!s) throw new Error("STICKER_LOOKUP:"+key(pos)+":"+key(normal));
  return s.color;
}
export function toCubie(stickers){
  const s=canonicalizeByCenters(stickers);
  const cp=Array(8),co=Array(8),ep=Array(12),eo=Array(12);
  for(let i=0;i<8;i++){
    const colors=CORNER_FACES[i].map(f=>stickerColor(s,CORNER_POS[i],FACE_VEC[f]));
    let ori=colors.findIndex(c=>c==="U"||c==="D");
    if(ori<0) throw new Error("CORNER_UD_COLOR");
    const c1=colors[(ori+1)%3], c2=colors[(ori+2)%3];
    const j=CORNER_COLORS.findIndex(x=>x[1]===c1&&x[2]===c2);
    if(j<0) throw new Error("CORNER_PIECE:"+colors.join(""));
    cp[i]=j; co[i]=ori%3;
  }
  for(let i=0;i<12;i++){
    const colors=EDGE_FACES[i].map(f=>stickerColor(s,EDGE_POS[i],FACE_VEC[f]));
    let found=-1,ori=0;
    for(let j=0;j<12;j++){
      if(colors[0]===EDGE_COLORS[j][0]&&colors[1]===EDGE_COLORS[j][1]){found=j;ori=0;break;}
      if(colors[0]===EDGE_COLORS[j][1]&&colors[1]===EDGE_COLORS[j][0]){found=j;ori=1;break;}
    }
    if(found<0) throw new Error("EDGE_PIECE:"+colors.join(""));
    ep[i]=found; eo[i]=ori;
  }
  return {cp,co,ep,eo};
}
const BASIC={
  U:{cp:[3,0,1,2,4,5,6,7],co:[0,0,0,0,0,0,0,0],ep:[3,0,1,2,4,5,6,7,8,9,10,11],eo:[0,0,0,0,0,0,0,0,0,0,0,0]},
  R:{cp:[4,1,2,0,7,5,6,3],co:[2,0,0,1,1,0,0,2],ep:[8,1,2,3,11,5,6,7,4,9,10,0],eo:[0,0,0,0,0,0,0,0,0,0,0,0]},
  F:{cp:[1,5,2,3,0,4,6,7],co:[1,2,0,0,2,1,0,0],ep:[0,9,2,3,4,8,6,7,1,5,10,11],eo:[0,1,0,0,0,1,0,0,1,1,0,0]},
  D:{cp:[0,1,2,3,5,6,7,4],co:[0,0,0,0,0,0,0,0],ep:[0,1,2,3,5,6,7,4,8,9,10,11],eo:[0,0,0,0,0,0,0,0,0,0,0,0]},
  L:{cp:[0,2,6,3,4,1,5,7],co:[0,1,2,0,0,2,1,0],ep:[0,1,10,3,4,5,9,7,8,2,6,11],eo:[0,0,0,0,0,0,0,0,0,0,0,0]},
  B:{cp:[0,1,3,7,4,5,2,6],co:[0,0,1,2,0,0,2,1],ep:[0,1,2,11,4,5,6,10,8,9,3,7],eo:[0,0,0,1,0,0,0,1,0,0,1,1]}
};
const FACES=["U","R","F","D","L","B"];
export function applyCubieFace(c,face,power=1){
  let out={cp:[...c.cp],co:[...c.co],ep:[...c.ep],eo:[...c.eo]};
  for(let k=0;k<power;k++){
    const b=BASIC[face],n={cp:Array(8),co:Array(8),ep:Array(12),eo:Array(12)};
    for(let i=0;i<8;i++){n.cp[i]=out.cp[b.cp[i]];n.co[i]=(out.co[b.cp[i]]+b.co[i])%3;}
    for(let i=0;i<12;i++){n.ep[i]=out.ep[b.ep[i]];n.eo[i]=(out.eo[b.ep[i]]+b.eo[i])%2;}
    out=n;
  }
  return out;
}
export function cubieEqual(a,b){
  return ["cp","co","ep","eo"].every(k=>a[k].every((x,i)=>x===b[k][i]));
}
export function findSingleHtmTransition(a,b){
  if(cubieEqual(a,b)) return {kind:"FRAME_ONLY",action_index:null,move:null};
  for(let fi=0;fi<FACES.length;fi++) for(let power=1;power<=3;power++){
    const n=applyCubieFace(a,FACES[fi],power);
    if(cubieEqual(n,b)) return {kind:"SINGLE_HTM",action_index:fi*3+(power-1),move:FACES[fi]+(power===2?"2":power===3?"'":"")};
  }
  return {kind:"MULTI_ACTION_EXTENDED",action_index:null,move:null};
}
function subsetMasks(){
  const a=[];
  for(let m=0;m<(1<<12);m++) if(m.toString(2).split("1").length-1===4) a.push(m);
  a.sort((x,y)=>x-y);
  const solved=0b1111<<8;
  return [solved,...a.filter(x=>x!==solved)];
}
const MASK_RANK=new Map(subsetMasks().map((m,i)=>[m,i]));
export function phase1(c){
  let twist=0;for(const x of c.co.slice(0,7)) twist=twist*3+x;
  let flip=0;for(const x of c.eo.slice(0,11)) flip=(flip<<1)|x;
  let mask=0;for(let pos=0;pos<12;pos++) if(c.ep[pos]>=8) mask|=1<<pos;
  const slice=MASK_RANK.get(mask);if(slice===undefined) throw new Error("SLICE_MASK");
  return {twist,flip,slice,rank:(twist*2048+flip)*495+slice};
}
export function transitionFromStickerMove(stickers,raw){
  const before=toCubie(stickers);
  const afterStickers=applyToken(stickers,raw);
  const after=toCubie(afterStickers);
  return {afterStickers,before,after,transition:findSingleHtmTransition(before,after),phase1_before:phase1(before),phase1_after:phase1(after)};
}
export function solvedCubie(){return toCubie(solvedStickers());}
