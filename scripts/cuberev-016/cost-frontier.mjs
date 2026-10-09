/** CUBE-REV 0.16 internal P3: exact cost frontiers (max horizon=3).
 * Every action is followed by one perfect orientation read. The stage charge
 * k = movement cost + sensor cost is inseparable under this contract.
 * Both feedback and fixed-word policies may stop on any observed branch.
 * Lines (L,T) mean 0/1 Bayes reward (L - k*T)/|S| under uniform priors:
 * L = number of terminal transcripts, T = sum path lengths over hypotheses.
 */
const EVEN=0x555555,FULL=0xffffff;
function popcnt(x){let n=0;while(x){x&=x-1;n++;}return n;}
function forward(mask,action,moves){
 let next=0;
 while(mask){const i=31-Math.clz32(mask&-mask);mask&=mask-1;next|=1<<moves[action][i];}
 return [next&EVEN,next&(FULL^EVEN)];
}
function pareto(lines){
 const by=new Map();
 for(const [leaves,totalSteps] of lines){
  if(!by.has(leaves)||by.get(leaves)>totalSteps)by.set(leaves,totalSteps);
 }
 return [...by].sort((a,b)=>a[0]-b[0]);
}
function appendBranches(out,lo,hi,price){
 for(const [l,c] of lo)for(const [r,d] of hi)out.push([l+r,c+d+price]);
}
export function exactCostFrontiers(moves,slots){
 if(moves.length!==18||slots.length!==4||new Set(slots).size!==4)throw Error('P3_COST_CONTRACT');
 let initial=0;for(const p of slots)initial|=1<<(2*p);
 const memo=new Map();
 function adapt(mask,h){
  if(!mask)return [[0,0]];
  const key=mask+':'+h;
  if(memo.has(key))return memo.get(key);
  let options=[[1,0]];
  if(h){
   for(let a=0;a<18;a++){
    const [lo,hi]=forward(mask,a,moves);
    appendBranches(options,adapt(lo,h-1),adapt(hi,h-1),popcnt(mask));
   }
  }
  const result=pareto(options);memo.set(key,result);return result;
 }
 function precommitted(mask,word,t){
  if(!mask)return [[0,0]];
  if(t===word.length)return [[1,0]];
  let opts=[[1,0]];
  const [lo,hi]=forward(mask,word[t],moves);
  appendBranches(opts,precommitted(lo,word,t+1),
    precommitted(hi,word,t+1),popcnt(mask));
  return pareto(opts);
 }
 const allFixed=[];
 for(let w=0;w<18**3;w++){
  let q=w;const word=[];
  for(let t=0;t<3;t++){word.push(q%18);q=Math.floor(q/18);}
  allFixed.push(...precommitted(initial,word,0));
 }
 return {support:slots,adaptive:adapt(initial,3),
  fixed:pareto(allFixed),allFixedWords:18**3};
}
export function valueFromLines(lines,k,size=4){
 if(!Number.isFinite(k)||k<0)throw Error('NONNEGATIVE_COST');
 return Math.max(...lines.map(([L,T])=>(L-k*T)/size));
}
