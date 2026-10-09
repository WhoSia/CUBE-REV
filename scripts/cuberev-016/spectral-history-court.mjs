/** CUBE-REV 0.16 INTERNAL P8 — spectral action-history theorem.
 * State x=2p+f is the 0.15 frozen tracked UR edge coordinate.
 * Formula counts literal sequences of 18 HTM tokens, including cancellations,
 * given the INITIAL and FINAL states of ONE edge, not full cube history.
 * Physical move maps must be supplied by the frozen cubie oracle.
 */
const FACE_NAMES='URFDLB';
const SLOTS=Object.freeze([
 ['U','R'],['U','F'],['U','L'],['U','B'],
 ['D','R'],['D','F'],['D','L'],['D','B'],
 ['F','R'],['F','L'],['B','L'],['B','R']
]);
export function orientedFacePair(x){
 if(!Number.isInteger(x)||x<0||x>=24)throw Error('BAD_EDGE_STATE');
 const pair=SLOTS[x>>1];
 return x&1?[pair[1],pair[0]]:pair.slice();
}
export function incidenceMultigraph(){
 const C=Array.from({length:12},()=>new Array(24).fill(0));
 for(let x=0;x<24;x++){
  const [a,b]=orientedFacePair(x);
  C[FACE_NAMES.indexOf(a)][x]=1;
  C[6+FACE_NAMES.indexOf(b)][x]=1;
 }
 return Array.from({length:24},(_,x)=>Array.from({length:24},(_,y)=>{
  let v=x===y?10:0;
  for(let r=0;r<12;r++)v+=C[r][x]*C[r][y];
  return v;
 }));
}
export function observedActionCountMatrix(moves){
 if(!Array.isArray(moves)||moves.length!==18||moves.some(m=>m.length!==24||
   new Set(m).size!==24))throw Error('NOT_18_EDGE_PERMUTATIONS');
 const B=Array.from({length:24},()=>new Array(24).fill(0));
 for(const row of moves)for(let x=0;x<24;x++)B[x][row[x]]++;
 return B;
}
export function verifyFaceArcIdentity(moves){
 const direct=observedActionCountMatrix(moves);
 const derived=incidenceMultigraph();
 let differing=0;
 for(let x=0;x<24;x++)for(let y=0;y<24;y++)
  if(direct[x][y]!==derived[x][y])differing++;
 const rowSums=direct.map(row=>row.reduce((a,b)=>a+b,0));
 return {differing,rows:24,cols:24,legalActions:moves.length,
  symmetric:direct.every((row,x)=>row.every((v,y)=>v===direct[y][x])),
  minimumSelfLoops:Math.min(...direct.map((row,x)=>row[x])),
  maximumSelfLoops:Math.max(...direct.map((row,x)=>row[x])),
  rowSumsEqual18:rowSums.every(v=>v===18)};
}
export function exactReturnCount(t){
 if(!Number.isInteger(t)||t<0)throw Error('NONNEGATIVE_INTEGER_LENGTH');
 const n=BigInt(t);
 const num=18n**n+2n*16n**n+6n*14n**n+2n*12n**n+13n*10n**n;
 if(num%24n!==0n)throw Error('SPECTRAL_INTEGRALITY');
 return num/24n;
}
export function exactWorstCaseLogBits(t){
 const fiber=exactReturnCount(t);
 return fiber<=1n?0:(fiber-1n).toString(2).length;
}
export function independentEndpointCounts(moves,t,x=0){
 if(!Number.isInteger(t)||t<0||!Number.isInteger(x)||x<0||x>=24)
  throw Error('BAD_ENDPOINT_QUERY');
 const B=observedActionCountMatrix(moves);
 let prev=Array.from({length:24},(_,i)=>i===x?1n:0n);
 for(let j=0;j<t;j++){
  const next=Array(24).fill(0n);
  for(let y=0;y<24;y++)if(prev[y]!==0n)
   for(let z=0;z<24;z++)if(B[y][z])next[z]+=prev[y]*BigInt(B[y][z]);
  prev=next;
 }
 return prev;
}
export function spectralChiSquared(t){
 if(!Number.isInteger(t)||t<0)throw Error('BAD_TIME');
 return 2*(8/9)**(2*t)+6*(7/9)**(2*t)
  +2*(2/3)**(2*t)+13*(5/9)**(2*t);
}
export function entropyCorrectionBound(t){
 return Math.log2(1+spectralChiSquared(t));
}
