/** Internal CUBE-REV 0.16 mathematical court. Supplied edge maps are the
 * frozen sticker-derived 0.15 24-state bijective 18-HTM action permutations.
 * Tracks ONE physical edge; no full-cube solve or human cognition asserted.
 */
const ALL=0xffffff,EVEN=0x555555;
const bits=x=>{let n=0;for(;x;x&=x-1)n++;return n;};
function check(m){if(!Array.isArray(m)||m.length!==18||m.some(r=>r.length!==24||new Set(r).size!==24||r.some(v=>!Number.isInteger(v)||v<0||v>=24)))throw Error('NEED_18_BIJECTIVE_24STATE_MOVES');}
function move(mask,row){let out=0;while(mask){const bit=mask&-mask;mask-=bit;const x=31-Math.clz32(bit);out|=1<<row[x];}return out;}
export function exactUnknownEdgeDiagnosis(m,maxH=8){
 check(m);const memo=new Map();
 function V(s,h){
  if(!s)return 0;if(!h||!(s&(s-1)))return 1;
  const key=s*32+h;if(memo.has(key))return memo.get(key);
  let best=1,cap=Math.min(bits(s),2**h);
  for(const row of m){const z=move(s,row),q=V(z&EVEN,h-1)+V(z&(ALL^EVEN),h-1);if(q>best)best=q;if(best===cap)break;}
  memo.set(key,best);return best;
 }
 return {maxLeaves:Array.from({length:maxH+1},(_,h)=>V(ALL,h)),memoStates:memo.size};
}
export function exactUnknownEdgeReset(m,maxH=10,target=0){
 check(m);if(target<0||target>=24)throw Error('BAD_TARGET');const goal=1<<target,memo=new Map();
 function P(s,h){
  if(s===0||s===goal)return true;
  if(!h||bits(s)>2**h)return false;
  const key=s*32+h;if(memo.has(key))return memo.get(key);
  for(const row of m){const z=move(s,row);if(P(z&EVEN,h-1)&&P(z&(ALL^EVEN),h-1)){memo.set(key,true);return true;}}
  memo.set(key,false);return false;
 }
 return {feasible:Array.from({length:maxH+1},(_,h)=>P(ALL,h)),memoStates:memo.size};
}
export function exactForgottenWordPreimages(m,len=4,origin=0){
 check(m);if(!Number.isInteger(len)||len<0||len>12||origin<0||origin>=24)throw Error('BAD_HISTORY');
 let counts=Array.from({length:24},(_,x)=>x===origin?1n:0n);
 for(let t=0;t<len;t++){const next=Array(24).fill(0n);
  for(const row of m)for(let x=0;x<24;x++)next[row[x]]+=counts[x];
  counts=next;
 }
 const max=counts.reduce((a,b)=>a>b?a:b),total=counts.reduce((a,b)=>a+b);
 return {totalWords:String(total),sameEndpointCount:String(counts[origin]),
  largestEndpointFiber:String(max),worstCaseAdditionalBits:max<=1n?0:(max-1n).toString(2).length,
  endpointCounts:counts.map(String)};
}
