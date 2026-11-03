#!/usr/bin/env node
/**
 * Independent JavaScript check of the full 156-layout one-sensor exchange
 * graph. Rebuilds oriented cube geometry from face-normal vectors, instead of
 * importing the Python geometric-rule or pair graph implementation.
 *
 * It uses the same previously certified B6 four-case incidence RULE as
 * scientific input. No new facelet-physics or HTM word-distance certificate
 * is claimed.
 */
"use strict";

const FACES = {
  U: [0, 1, 0], D: [0, -1, 0], R: [1, 0, 0],
  L: [-1, 0, 0], F: [0, 0, 1], B: [0, 0, -1],
};
const EDGE_NAMES = ["UR","UF","UL","UB","DR","DF","DL","DB","FR","FL","BL","BR"];
const equal = (a,b) => a.join(",") === b.join(",");
const cornerId = x => x.join(",");
function endpoints(edge) {
  const a=FACES[edge[0]], b=FACES[edge[1]];
  if (!a || !b) throw new Error("Bad edge");
  const m=a.map((v,i)=>v+b[i]);
  const k=m.indexOf(0);
  if (k < 0) throw new Error("Adjacent faces required");
  return [-1,1].map(sign=>m.map((v,i)=>i===k?sign:v));
}
const END = Object.fromEntries(EDGE_NAMES.map(e=>[e,endpoints(e).map(cornerId)]));
const MID = Object.fromEntries(EDGE_NAMES.map(e=>[
  e,FACES[e[0]].map((v,i)=>v+FACES[e[1]][i])
]));
const share = (p,q) => p.some(x=>q.includes(x));
const reverseCorner = id => id.split(",").map(v=>-Number(v)).join(",");
function valid(core,ea,eb) {
  if (ea===eb) return false;
  const ends=END[core];
  const opposite=ends.map(reverseCorner);
  const star=EDGE_NAMES.find(e=>equal([...END[e]].sort(),[...opposite].sort()));
  if (!star) throw new Error("Missing antipodal edge");
  const near=EDGE_NAMES.filter(e=>e!==core && share(END[e],ends));
  const far=EDGE_NAMES.filter(e=>e!==star && share(END[e],opposite));
  const axis=MID[core].indexOf(0);
  const parallel=EDGE_NAMES.filter(e=>e!==core && e!==star && MID[e].indexOf(0)===axis);
  if (near.length!==4 || far.length!==4 || parallel.length!==2) throw new Error("Wrong neighborhood");
  const nearer = near.includes(ea) && near.includes(eb)
    && (END[ea].includes(ends[0]) !== END[eb].includes(ends[0]));
  const farther = far.includes(ea) && far.includes(eb)
    && [...ea].some(f=>eb.includes(f));
  const antipodal = (ea===star && far.includes(eb)) || (eb===star && far.includes(ea));
  const parallelPair = parallel.includes(ea) && parallel.includes(eb);
  return nearer || farther || antipodal || parallelPair;
}
const layouts = [];
for (const h of EDGE_NAMES) {
  const coreCount=layouts.length;
  for(let i=0;i<EDGE_NAMES.length;i++)
    for(let j=i+1;j<EDGE_NAMES.length;j++) {
      const [ea,eb]=[EDGE_NAMES[i],EDGE_NAMES[j]];
      if(valid(h,ea,eb)) layouts.push({h,c:new Set(END[h]),e:new Set([ea,eb])});
    }
  if (layouts.length-coreCount!==13) throw new Error("Not 13 per core "+h);
}
if(layouts.length!==156) throw new Error("Wrong 156 count");
function diffCount(a,b) {
  let d=0;
  for(const x of a) if(!b.has(x))d++;
  for(const x of b) if(!a.has(x))d++;
  return d;
}
const graph = Array.from({length:layouts.length},()=>new Set());
let within=0,cross=0;
for(let i=0;i<layouts.length;i++) for(let j=i+1;j<layouts.length;j++){
  const a=layouts[i],b=layouts[j];
  if (diffCount(a.c,b.c)+diffCount(a.e,b.e)!==2) continue;
  graph[i].add(j);graph[j].add(i);
  if (a.h===b.h) within++; else cross++;
}
const todo=new Set(graph.map((_,i)=>i));
const components=[];
while(todo.size) {
  const seed=todo.values().next().value;
  const queue=[seed], group=new Set([seed]);todo.delete(seed);
  for(let k=0;k<queue.length;k++)
    for(const v of graph[queue[k]])
      if(!group.has(v)){group.add(v);todo.delete(v);queue.push(v)}
  components.push(group);
}
components.sort((a,b)=>b.size-a.size);
const sizes=components.map(c=>c.size);
const degrees={};
for(const neigh of graph) degrees[neigh.size]=(degrees[neigh.size]||0)+1;
const requireEqual=(actual,expected,name)=>{
  if(JSON.stringify(actual)!==JSON.stringify(expected))throw new Error(name+":"+JSON.stringify(actual));
};
requireEqual([within,cross],[264,72],"edge count");
requireEqual(sizes,[96,...Array(12).fill(4),...Array(12).fill(1)],"components");
requireEqual(degrees,{"0":12,"2":48,"4":24,"6":24,"7":48},"degrees");
for(const h of EDGE_NAMES){
  const c=components.map(comp=>Array.from(comp).filter(i=>layouts[i].h===h).length).filter(Boolean).sort((a,b)=>a-b);
  requireEqual(c,[1,4,8],"per core components");
}
let crossInLargest=0;
for(const i of components[0])for(const j of graph[i])if(layouts[i].h!==layouts[j].h)crossInLargest++;
if(crossInLargest/2!==72)throw new Error("Cross links not wholly in giant component");
console.log("PASS independent JS cube-face geometry: 156 layouts / 336 swaps");
console.log("PASS 264 fixed-corner + 72 changing-corner swaps");
console.log("PASS 25 components: 96 + 12*4 + 12*1; per-core 8+4+1");
console.log("PASS degree profile",JSON.stringify(degrees));
console.log("LIMIT: four-case B6 geometry inherited; not independent HTM certificate");
