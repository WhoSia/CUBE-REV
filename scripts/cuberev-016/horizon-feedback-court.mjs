/** CUBE-REV 0.16 internal P3: exhaustive fixed-vs-adaptive horizon courts.
 * Input: trusted 0.15 24-coordinate edge permutations; all 18 HTM turns.
 * This computes ideal mathematical read histories, NOT human sensor behavior.
 */
const FULL24=0xffffff,EVEN24=0x555555;
function check(moves){
 if(!Array.isArray(moves)||moves.length!==18||
    moves.some(m=>m.length!==24||new Set(m).size!==24))throw Error('FROZEN_HTM_24_CONTRACT');
}
function countBits(x){let n=0;while(x){x&=x-1;n++;}return n;}
function applyMask(mask,map){
 let z=0;
 while(mask){let bit=31-Math.clz32(mask&-mask);mask&=mask-1;z|=(1<<map[bit]);}
 return z;
}
/** Bellman-maximize the number of nonempty noiseless transcripts. */
export function makeFeedbackDP(moves){
 check(moves);const cache=new Map();
 function value(mask,h){
  if(!mask)return 0;
  if(h===0||!(mask&(mask-1)))return 1;
  const key=mask+':'+h,old=cache.get(key);if(old!==undefined)return old;
  let best=1;const cap=Math.min(countBits(mask),1<<h);
  for(const map of moves){
   const z=applyMask(mask,map);
   const score=value(z&EVEN24,h-1)+value(z&(FULL24^EVEN24),h-1);
   if(score>best)best=score;if(best===cap)break;
  }
  cache.set(key,best);return best;
 }
 return {value,cache};
}
function maskOfSlots(slots,both){
 let mask=0;for(const p of slots){mask|=1<<(2*p);if(both)mask|=1<<(2*p+1);}return mask;
}
function srcIndices(mask){
 const out=[];for(let i=0;i<24;i++)if(mask&(1<<i))out.push(i);return out;
}
/** Full 18^4 fixed-word census; equivalent unlabeled source partitions deduped. */
export function exactH4FixedPartitions(moves){
 check(moves);const unique=new Map();const h=4;
 for(let w=0;w<18**h;w++){
  let q=w;const acts=[];
  for(let i=0;i<h;i++){acts.push(q%18);q=Math.floor(q/18);}
  const groups=new Uint16Array(16);
  for(let p=0;p<12;p++){
   let x=2*p,code=0;
   for(let i=0;i<h;i++){x=moves[acts[i]][x];code|=(x&1)<<i;}
   groups[code]|=1<<p;
  }
  const sorted=Array.from(groups).sort((a,b)=>a-b);
  const key=sorted.join(',');
  if(!unique.has(key))unique.set(key,sorted.filter(Boolean));
 }
 return [...unique.values()];
}
export function exactH4AllBeliefs(moves){
 const groups=exactH4FixedPartitions(moves),dp=makeFeedbackDP(moves);
 const hist={},strict=[],values=[],all=(1<<12)-1;
 for(let s=1;s<=all;s++){
  let fixed=1;const ceiling=Math.min(16,countBits(s));
  for(const part of groups){
   let n=0;for(const m of part)if(m&s)n++;
   if(n>fixed)fixed=n;if(fixed===ceiling)break;
  }
  let stateMask=0;for(let p=0;p<12;p++)if(s&(1<<p))stateMask|=1<<(2*p);
  const adaptive=dp.value(stateMask,4);
  if(adaptive<fixed)throw Error('FIXED_POLICY_EXCEEDS_FEEDBACK');
  const key=adaptive+','+fixed;hist[key]=(hist[key]||0)+1;
  values.push({mask:s,adaptive,fixed});
  if(adaptive>fixed)strict.push({mask:s,adaptive,fixed});
 }
 return {supports:4095,allFixedWords:18**4,distinctFixedPartitions:groups.length,
  histogram:hist,strictCount:strict.length,firstStrict:strict.slice(0,10),
  allPolicyValues:values,
  memoStates:dp.cache.size};
}
/** Full 18^5 exhaustive fixed enumeration, no heuristic stop or approximation. */
export function exactH5SelectedBeliefs(moves){
 check(moves);const dp=makeFeedbackDP(moves),bases={
  full12:{initial:maskOfSlots(Array.from({length:12},(_,i)=>i),false)},
  full24:{initial:FULL24},
  known170:{initial:maskOfSlots([1,3,5,7],false)},
  unknown170:{initial:maskOfSlots([1,3,5,7],true)},
  unknown3840:{initial:maskOfSlots([8,9,10,11],true)}
 };
 for(const spec of Object.values(bases)){
  spec.indices=srcIndices(spec.initial);spec.fixed=0;spec.hist={};
 }
 const total=18**5;
 for(let w=0;w<total;w++){
  let x=w;const acts=new Int8Array(5);
  for(let t=0;t<5;t++){acts[t]=x%18;x=Math.floor(x/18);}
  const states=new Uint8Array(24),codes=new Uint8Array(24);
  for(let i=0;i<24;i++)states[i]=i;
  for(let t=0;t<5;t++){
   const map=moves[acts[t]];
   for(let i=0;i<24;i++){
    const z=map[states[i]];states[i]=z;codes[i]|=(z&1)<<t;
   }
  }
  for(const spec of Object.values(bases)){
   let seen=0;for(const i of spec.indices)seen|=1<<codes[i];
   const n=countBits(seen);if(n>spec.fixed)spec.fixed=n;
   spec.hist[n]=(spec.hist[n]||0)+1;
  }
 }
 const result={allFixedWords:total};
 for(const [key,spec] of Object.entries(bases)){
  const adaptive=dp.value(spec.initial,5);
  if(spec.fixed>adaptive)throw Error('FIXED_EXCEEDS_FEEDBACK');
  result[key]={priorStates:spec.indices.length,adaptive,fixed:spec.fixed,histogram:spec.hist};
 }
 return result;
}