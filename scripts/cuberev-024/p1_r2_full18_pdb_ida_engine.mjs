// CUBE-REV 0.24 P1-R2 — actual 18 HTM whole-cube PDB-guided IDA*.
// Source-independent physical cubie transitions from original 54 stickers.
// Uses existing exact four-edge Cross PDB for U and D. Restricted H solutions
// are only admissible *upper-bound witnesses*, never pruning lower bounds.
// Complete if supplied enough resources; otherwise returns explicit HOLD.
import assert from 'node:assert/strict';
import {performance} from 'node:perf_hooks';
import {solvedStickerCube,applyMoveToken,toCubieState,cubieSolved} from '../cube/sticker-cube.mjs';
import {ACTIONS,buildCrossPDB,indexOfFourEdges,FACE_EDGE_IDS} from '../cuberev-013/cross4-pdb.mjs';
export const MOVES=ACTIONS;
const faces=MOVES.map(m=>m[0]);
const opp={U:'D',D:'U',R:'L',L:'R',F:'B',B:'F'};
const inverse=token=>token.endsWith('2')?token:token.endsWith("'")?token[0]:token+"'";
const inverted=word=>[...word].reverse().map(inverse);
export function cubeFromWords(words){
  const s=solvedStickerCube();
  for(const t of words) {assert(MOVES.includes(t),'original external 18HTM token required: '+t);applyMoveToken(s,t);}
  return s;
}
const faceMove=Object.fromEntries(MOVES.map(t=>[t,toCubieState(cubeFromWords([t]))]));
const solved=toCubieState(cubeFromWords([]));
function transition(s,m){
  const x=faceMove[m];assert(x,'unknown source move');
  return {
    cp:x.cp.map(i=>s.cp[i]),
    co:x.co.map((v,i)=>(s.co[x.cp[i]]+v)%3),
    ep:x.ep.map(i=>s.ep[i]),
    eo:x.eo.map((v,i)=>s.eo[x.ep[i]]^v)
  };
}
function key(s){return String.fromCharCode(...s.cp,...s.co,...s.ep,...s.eo)}
function fromTokens(tokens){return toCubieState(cubeFromWords(tokens))}
function legalTokens(tokens){assert(tokens.every(t=>MOVES.includes(t)));}
function applyWord(s,word){for(const t of word)s=transition(s,t);return s}
const half=MOVES.filter(t=>t.endsWith('2'));
function bfs(alphabet,maxDepth){
  const seen=new Map([[key(solved),{state:solved,depth:0,path:[]}]]);
  let frontier=[solved],layers=[1];
  for(let d=1;d<=maxDepth;d++){
    const next=[];
    for(const s of frontier){
      const path=seen.get(key(s)).path;
      for(const move of alphabet){
        const child=transition(s,move),k=key(child);
        if(seen.has(k))continue;
        seen.set(k,{state:child,depth:d,path:[...path,move]});
        next.push(child);
      }
    }
    layers.push(next.length);frontier=next;
  }
  return {seen,layers};
}
const R4=bfs(MOVES,4);
const H5=bfs(half,5);
assert.deepEqual(R4.layers,[1,18,243,3240,43239]);
assert.deepEqual(H5.layers,[1,6,27,120,519,1932]);
const pU=buildCrossPDB('U'),pD=buildCrossPDB('D');
assert(pU.reachable===190080&&pD.reachable===190080);
function crossBound(s){
  return Math.max(pU.distances[indexOfFourEdges(s.ep,s.eo,FACE_EDGE_IDS.U)],
                  pD.distances[indexOfFourEdges(s.ep,s.eo,FACE_EDGE_IDS.D)]);
}
// Exact corner orientation PDB: 3^7=2187 and all-edge orientation PDB:2^11=2048.
// Each abstract action is induced by the actual original physical cubie move.
function orientationPDB(kind){
  const corner=kind==='corner',size=corner?2187:2048,n=corner?8:12,base=corner?3:2;
  const digitCount=n-1;
  function decode(index){
    const x=Array(n).fill(0);let sum=0;
    for(let i=digitCount-1;i>=0;i--){x[i]=index%base;index=Math.floor(index/base);sum+=x[i]}
    x[n-1]=(base-sum%base)%base;
    return x;
  }
  function encode(a){
    let index=0;
    for(let i=0;i<digitCount;i++)index=index*base+a[i];
    return index;
  }
  const permProp=corner?'cp':'ep',oriProp=corner?'co':'eo';
  const maps=MOVES.map(m=>({perm:faceMove[m][permProp],ori:faceMove[m][oriProp]}));
  const transitions=new Uint16Array(size*MOVES.length);
  for(let q=0;q<size;q++){
    const old=decode(q);
    for(let j=0;j<MOVES.length;j++){
      const m=maps[j];
      const next=m.perm.map((from,i)=>(old[from]+m.ori[i])%base);
      transitions[q*18+j]=encode(next);
    }
  }
  const dist=new Uint8Array(size);dist.fill(255);
  const queue=new Uint16Array(size);queue[0]=0;dist[0]=0;
  let head=0,tail=1;
  while(head<tail){
    const p=queue[head++],d=dist[p];
    for(let a=0;a<18;a++){
      const nxt=transitions[p*18+a];
      if(dist[nxt]!==255)continue;
      dist[nxt]=d+1;queue[tail++]=nxt;
    }
  }
  assert.equal(tail,size,'actual orientation quotient must be connected');
  return {dist,encode};
}
const coPDB=orientationPDB('corner'),eoPDB=orientationPDB('edge');
let additionalCrossPDBs=null;
function allCrossBound(s){
  additionalCrossPDBs??=Object.fromEntries('RFBL'.split('').map(f=>[f,buildCrossPDB(f)]));
  return Math.max(crossBound(s),...Object.entries(additionalCrossPDBs).map(([f,pdb])=>pdb.distances[indexOfFourEdges(s.ep,s.eo,FACE_EDGE_IDS[f])]));
}
export function lowerBound(s,useAllCrossPDBs=false){
  const b=Math.max(useAllCrossPDBs?allCrossBound(s):crossBound(s),coPDB.dist[coPDB.encode(s.co)],eoPDB.dist[eoPDB.encode(s.eo)]);
  assert(b>=0&&b<255);
  return b;
}
const positions=Array.from({length:12},(_,i)=>i);
// 12 genuine edge identity-position tetrad filter, extracted from allowed H5
// actual states only. Necessity is exact; sufficiency is NOT claimed.
const allowed=positions.map(pos=>new Set([...H5.seen.values()].map(v=>v.state.ep[pos])));
assert(allowed.every(s=>s.size===4),'genuine halfturn edge tetrad');
function passesTetrads(s){return positions.every(i=>allowed[i].has(s.ep[i]))}
export function restrictedIncumbent(s,limit=9){
  if(!passesTetrads(s))return {word:null,expanded:0,reason:'OUTSIDE_H_TETRADS'};
  const direct=H5.seen.get(key(s));
  if(direct)return {word:inverted(direct.path),expanded:0,reason:'EXACT_H5'};
  let best=null,expanded=0;
  const seen=new Map([[key(s),{state:s,path:[]}]]);
  let frontier=[s];
  for(let depth=0;depth<=4;depth++){
    const next=[];
    for(const u of frontier){
      expanded++;
      const path=seen.get(key(u)).path,meet=H5.seen.get(key(u));
      if(meet){
        const candidate=[...path,...inverted(meet.path)];
        if(candidate.length<=limit&&(!best||candidate.length<best.length))best=candidate;
      }
      if(depth===4)continue;
      for(const move of half){
        const child=transition(u,move),k=key(child);
        if(!seen.has(k)){seen.set(k,{state:child,path:[...path,move]});next.push(child)}
      }
    }
    frontier=next;
  }
  if(best) assert(cubieSolved(applyWord(s,best)));
  return {word:best,expanded,reason:best?'ACTUAL_H_4_PLUS_5':'NO_H_WITHIN_9'};
}
// The raw A* / IDA* graph has reversible legal edges. Consistent admissible
// PDB distances are MAXed, never summed. No H-geodesic length is a lower bound.
function canonicalLast(last,move){
  if(!last)return false;
  if(last[0]===move[0])return true;
  return opp[last[0]]===move[0]&&move[0]<last[0]; // commuting opposite face canonicalization
}
export function solveOptimal(tokens,{useHIncumbent=true,hIncumbentMode='cheap_H5',useAllCrossPDBs=false,nodeCap=250000,timeCapMs=2000,maxDepth=13}={}){
  legalTokens(tokens);
  const initial=fromTokens(tokens),start=performance.now();
  const h0=lowerBound(initial,useAllCrossPDBs);
  const result={source_tokens:tokens,lower_bound:h0,method:'IDA_FULL18',
    result:'HOLD',word:null,length:null,idaNodes:0,idaIterations:[],incumbent:null,
    bounded_optimum_certificate:false,reason:null,elapsedMs:null};
  if(cubieSolved(initial)){return {...result,result:'OPTIMAL',length:0,word:[],method:'ALREADY_SOLVED',bounded_optimum_certificate:true,elapsedMs:performance.now()-start}}
  const exact=R4.seen.get(key(initial));
  if(exact){const word=inverted(exact.path);assert(cubieSolved(applyWord(initial,word)));
    return {...result,result:'OPTIMAL',length:word.length,word,method:'EXACT_R4',bounded_optimum_certificate:true,elapsedMs:performance.now()-start};
  }
  // Avoid paying up to 673 halfturn source-side evaluations on sources for
  // which full18 IDA* closes quickly. Default = only a cheap exact H5 lookup.
  // EXPENSIVE 4+5 H<=9 search is explicit and resource-priced; it is never
  // a lower bound and is not automatically run for distorted d18=5/H8,9.
  const hCandidate=useHIncumbent
    ?(hIncumbentMode==='eager_H9'?restrictedIncumbent(initial,Math.max(9,maxDepth)):
      passesTetrads(initial)
        ?(()=>{const d=H5.seen.get(key(initial));return d
          ?{word:inverted(d.path),expanded:0,reason:'EXACT_H5_DIRECT'}
          :{word:null,expanded:0,reason:'H5_NOT_REACHED'}})()
        :{word:null,expanded:0,reason:'OUTSIDE_H_TETRADS'})
    :null;
  const inc=hCandidate?.word??null;
  if(inc){assert(cubieSolved(applyWord(initial,inc)));result.incumbent={length:inc.length,reason:hCandidate.reason,search_nodes:hCandidate.expanded}}
  else if(hCandidate)result.incumbent={length:null,reason:hCandidate.reason,search_nodes:hCandidate.expanded};
  // Source outside the exact full18 radius-four ball has d18>=5. An actual
  // replayed five-move H-word supplies d18<=5. Thus the full global HTM
  // optimum is certified immediately, with no search or resource cap needed.
  if(inc?.length===5){
    assert(cubieSolved(toCubieState(cubeFromWords([...tokens,...inc]))));
    return {...result,result:'OPTIMAL',length:5,word:inc,method:'H5_SANDWICH_GLOBAL_OPTIMAL',
      reason:'EXACT_FULL18_R4_NEGATIVE_AND_REAL_H5_WITNESS',
      bounded_optimum_certificate:true,elapsedMs:performance.now()-start};
  }
  let best=inc,limit=Math.max(5,h0),found=null,resource=false;
  // We need to search only strictly shorter than a valid incumbent; if none
  // exists the incumbent is OPTIMAL even when it came from restricted H moves.
  const dfs=(state,g,bound,last,path)=>{
    if(result.idaNodes++>=nodeCap||performance.now()-start>timeCapMs){resource=true;return}
    const exactSuffix=R4.seen.get(key(state));
    if(exactSuffix){
      if(g+exactSuffix.depth<=bound)found=[...path,...inverted(exactSuffix.path)];
      return;
    }
    const heuristic=Math.max(5,lowerBound(state,useAllCrossPDBs)); // outside R4 implies d18>=5
    if(g+heuristic>bound||g===bound)return;
    for(const move of MOVES){
      if(canonicalLast(last,move))continue;
      const child=transition(state,move);
      path.push(move);
      dfs(child,g+1,bound,move,path);
      path.pop();
      if(found||resource)return;
    }
  };
  for(;limit<=maxDepth&&(best===null||limit<best.length);limit++){
    const before=result.idaNodes;
    dfs(initial,0,limit,null,[]);
    result.idaIterations.push({bound:limit,nodes:result.idaNodes-before,found:!!found,exhausted:!resource&&!found});
    if(found){best=found;break}
    if(resource)break;
  }
  if(!resource&&best&&!found&&limit>=best.length){
    result.reason='CERTIFIED_NO_SHORTER_FULL18_PATH';
  }else if(found){result.reason='IDA_FIRST_SOLVE_AT_INCREASING_EXACT_LOWER_BOUND'}
  else if(resource){result.reason='RESOURCE_CAP_HOLD'}
  else result.reason='MAX_DEPTH_HOLD';
  if(best&&!resource&&(found||limit>=best.length)){
    const after=cubeFromWords([...tokens,...best]);
    assert(cubieSolved(toCubieState(after)),'FULL_ORIGINAL_54_FACELET_SOLUTION_REQUIRED');
    return {...result,result:'OPTIMAL',length:best.length,word:best,
      method:found?'PDB_IDA_FULL18':'PDB_IDA_CERTIFIED_H_INCUMBENT',
      bounded_optimum_certificate:true,elapsedMs:performance.now()-start};
  }
  return {...result,word:best,length:best?.length??null,
    result:best?'INCUMBENT_UNCERTIFIED':'HOLD',elapsedMs:performance.now()-start};
}
// No implicit program run at import: keep CLI simple and deterministic.
if(process.argv[1]?.endsWith('p1_r2_full18_pdb_ida_engine.mjs')){
  const scrambles=[
    ["U","R2","F","D'","L2","B"],
    ["D","U","R2","D","U"],
    ["D","U","R2","D'","U"],
    ["F2","L","U2","R'","D","B2","U"],
    ["R","U","R'","U'","F2","D2","L"],
    ["R2","F","D'","B2","U","L2","R'","F"]
  ];
  const outcomes=[];
  for(const scramble of scrambles){
    const baseline=solveOptimal(scramble,{useHIncumbent:false,nodeCap:180000,timeCapMs:3000,maxDepth:11});
    const engine=solveOptimal(scramble,{useHIncumbent:true,nodeCap:180000,timeCapMs:3000,maxDepth:11});
    if(baseline.result==='OPTIMAL'&&engine.result==='OPTIMAL')assert.equal(baseline.length,engine.length);
    for(const x of [baseline,engine])if(x.word)assert(cubieSolved(toCubieState(cubeFromWords([...scramble,...x.word]))));
    outcomes.push({scramble:scramble.join(' '),baseline:{result:baseline.result,length:baseline.length,nodes:baseline.idaNodes,ms:baseline.elapsedMs},
      engine:{result:engine.result,length:engine.length,nodes:engine.idaNodes,ms:engine.elapsedMs,incumbent:engine.incumbent},evidence_grade:'ACTUAL_ORIGINAL_FACELETS'});
  }
  console.log(JSON.stringify({marker:'CUBE_REV_024_P1_R2_REAL_CUBE_IDA_PDB_PHYSICAL_ENGINE',
    exact_cross_PDB:['U','D'],each_four_edge_states:190080,
    corner_orientation_PDB_states:2187,edge_orientation_PDB_states:2048,
    H5_upper_bound_states:2605,full18_R4_shortcut_states:46741,
    source_cohorts:outcomes,
    methodological_limit:'Bounded runtime CAP gives HOLD; equal-lower-bound full18 searches are exact only if completed; cross heuristics never summed; real published speedcubing solve cognition is not observed.',
    no_data_rights_expansion:true},null,2));
}
