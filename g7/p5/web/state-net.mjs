import {solvedStickerCube,applyAlgorithm} from "../../../scripts/g7-p4/sticker-cube.mjs";

const normals={U:[0,1,0],R:[1,0,0],F:[0,0,1],D:[0,-1,0],L:[-1,0,0],B:[0,0,-1]};
const eq=(a,b)=>a[0]===b[0]&&a[1]===b[1]&&a[2]===b[2];
function rc(face,p){
  const [x,y,z]=p;
  if(face==="U") return [z+1,x+1];
  if(face==="D") return [1-z,x+1];
  if(face==="F") return [1-y,x+1];
  if(face==="B") return [1-y,1-x];
  if(face==="R") return [1-y,1-z];
  return [1-y,z+1];
}
export function faceMatrices(scramble){
  const cube=solvedStickerCube();
  if(String(scramble).trim()) applyAlgorithm(cube,scramble);
  const out={};
  for(const face of Object.keys(normals)){
    const m=Array.from({length:3},()=>Array(3).fill(null));
    for(const s of cube){
      if(!eq(s.n,normals[face])) continue;
      const [r,c]=rc(face,s.p);m[r][c]=s.c;
    }
    if(m.flat().some(x=>x===null)) throw new Error("FACE_RENDER_INCOMPLETE:"+face);
    out[face]=m;
  }
  return out;
}
export function renderNet(container,scramble){
  const faces=faceMatrices(scramble);
  const color={U:"#f5f5f5",R:"#d32f2f",F:"#2e7d32",D:"#fdd835",L:"#ef6c00",B:"#1565c0"};
  container.replaceChildren();
  container.className="cube-net";
  const positions={U:[1,0],L:[0,1],F:[1,1],R:[2,1],B:[3,1],D:[1,2]};
  for(const [face,[gx,gy]] of Object.entries(positions)){
    const f=document.createElement("div");f.className="cube-face";f.style.gridColumn=String(gx+1);f.style.gridRow=String(gy+1);f.dataset.face=face;
    for(const cell of faces[face].flat()){
      const x=document.createElement("span");x.className="sticker";x.style.background=color[cell];x.dataset.color=cell;f.appendChild(x);
    }
    container.appendChild(f);
  }
}
