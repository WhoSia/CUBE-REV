/** CUBE-REV 0.13: exact four-edge cross HTM pattern database.
 * 12P4*2^4 = 190080 reachable states, fixed 18 outer-face actions.
 * This public module contains no human data or solve records.
 */
import {solvedStickerCube,applyMoveToken,toCubieState} from '../cube/sticker-cube.mjs';
import {createHash} from 'node:crypto';
const FACES='URFDLB';
const SUFFIX=['',"'",'2'];
export const FACE_EDGE_IDS=Object.freeze({
  U:[0,1,2,3],D:[4,5,6,7],R:[0,4,8,11],L:[2,6,9,10],
  F:[1,5,8,9],B:[3,7,10,11]
});
export const ACTIONS=[...FACES].flatMap(f=>SUFFIX.map(s=>f+s));
export const STATE_COUNT=190080;
function rank(p){
 const pool=Array.from({length:12},(_,i)=>i);let out=0;
 for(let i=0;i<4;i++){
  const ix=pool.indexOf(p[i]);if(ix<0)throw Error('DUPLICATE_EDGE_POSITION');
  out=out*(12-i)+ix;pool.splice(ix,1);
 }
 return out;
}
function unrank(k){
 const digits=[];
 for(const radix of [9,10,11,12]){digits.push(k%radix);k=Math.floor(k/radix);}
 if(k)throw Error('INVALID_RANK');
 const pool=Array.from({length:12},(_,i)=>i);
 return digits.reverse().map(i=>pool.splice(i,1)[0]);
}
export function indexOfFourEdges(ep,eo,targetIds=FACE_EDGE_IDS.D){
 const pos=targetIds.map(id=>ep.indexOf(id));
 if(pos.some(p=>p<0))throw Error('MISSING_TARGET_EDGE');
 return 16*rank(pos)+pos.reduce((s,p,i)=>s+(eo[p]<<i),0);
}
function moveMaps(){
 return ACTIONS.map(token=>{
  const cube=solvedStickerCube();applyMoveToken(cube,token);
  const {ep,eo}=toCubieState(cube);
  const inverse=new Array(12);
  ep.forEach((src,dest)=>{inverse[src]=dest;});
  return {inverse,eo};
 });
}
export function buildCrossPDB(face='D'){
 const targets=FACE_EDGE_IDS[face];if(!targets)throw Error('UNKNOWN_CROSS_FACE');
 const maps=moveMaps(),rankMove=new Uint16Array(11880*18),flip=new Uint8Array(11880*18);
 for(let r=0;r<11880;r++){
  const p=unrank(r);
  for(let m=0;m<18;m++){
   const x=maps[m],dest=p.map(i=>x.inverse[i]),off=r*18+m;
   rankMove[off]=rank(dest);
   flip[off]=dest.reduce((b,i,k)=>b+(x.eo[i]<<k),0);
  }
 }
 const out=new Uint8Array(STATE_COUNT);out.fill(255);
 const goal=indexOfFourEdges(Array.from({length:12},(_,i)=>i),new Array(12).fill(0),targets);
 out[goal]=0;
 const queue=new Uint32Array(STATE_COUNT);let head=0,tail=1,diameter=0;
 queue[0]=goal;
 while(head<tail){
  const state=queue[head++],d=out[state],off=(state>>4)*18,bits=state&15;
  for(let m=0;m<18;m++){
   const nxt=(rankMove[off+m]<<4)+(bits^flip[off+m]);
   if(out[nxt]===255){out[nxt]=d+1;queue[tail++]=nxt;if(d+1>diameter)diameter=d+1;}
  }
 }
 if(tail!==STATE_COUNT)throw Error('INCOMPLETE_CROSS_PDB');
 return {face,distances:out,diameter,reachable:tail,
  sha256:createHash('sha256').update(out).digest('hex')};
}
