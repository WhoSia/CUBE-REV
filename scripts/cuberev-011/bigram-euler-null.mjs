/** CUBE-REV 0.11-J — deterministic Euler surrogate of one move-token sequence.
 * Preserves each directed adjacent-token count, token count, first/last token,
 * token multiset, and length. DOES NOT preserve Rubik solving trajectories.
 */
export function directedBigramCounts(tokens){
 const counts=new Map();
 for(let i=0;i+1<tokens.length;i++){
  const k=JSON.stringify([tokens[i],tokens[i+1]]);
  counts.set(k,(counts.get(k)||0)+1);
 }
 return [...counts].sort((a,b)=>a[0].localeCompare(b[0]));
}
export function seedRng(seed){
 let s=seed>>>0;
 return ()=>{s^=s<<13;s^=s>>>17;s^=s<<5;return (s>>>0)/4294967296;};
}
export function eulerBigramSurrogate(tokens,rng){
 if(!Array.isArray(tokens)||!tokens.every(x=>typeof x==='string'))throw Error('BAD_TOKENS');
 if(tokens.length<2)return [...tokens];
 const edges=new Map();
 for(let i=0;i<tokens.length-1;i++){
  const from=tokens[i];
  if(!edges.has(from))edges.set(from,[]);
  edges.get(from).push(tokens[i+1]);
 }
 for(const a of edges.values()){
  for(let i=a.length-1;i>0;i--){
   const j=Math.floor(rng()*(i+1));
   [a[i],a[j]]=[a[j],a[i]];
  }
 }
 const stack=[tokens[0]],path=[];
 while(stack.length){
  const v=stack[stack.length-1],out=edges.get(v);
  if(out?.length)stack.push(out.pop());else path.push(stack.pop());
 }
 path.reverse();
 if(path.length!==tokens.length||path[0]!==tokens[0]||path.at(-1)!==tokens.at(-1))
  throw Error('EULER_PATH_GATE');
 if(JSON.stringify(directedBigramCounts(path))!==JSON.stringify(directedBigramCounts(tokens)))
  throw Error('BIGRAM_PRESERVATION_GATE');
 return path;
}
