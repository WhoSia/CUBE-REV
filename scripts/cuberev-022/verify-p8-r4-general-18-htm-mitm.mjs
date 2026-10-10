/**
 * CUBE-REV 0.22 P8-R3: source-anchored full 18 HTM face-turn meet-in-middle exact depth at most ten.
 * This is exact finite physical search, not a reconstruction of human thought.
 * Assumption: fixed physical DR axis, DR-preserving 10-face-turn alphabet,
 * then exact HTR Cayley BFS. Query only 4 non-HTR quarter turns in last layer.
 */
import assert from 'node:assert/strict';
import fs from 'node:fs';
import crypto from 'node:crypto';
import {solvedStickerCube, applyMoveToken, toCubieState, solvedUpToRotation} from '../cube/sticker-cube.mjs';
import {ACTIONS} from '../cuberev-013/cross4-pdb.mjs';

const ledger=JSON.parse(fs.readFileSync('data/cuberev-022/p7_fmc_source_anchored_candidate_ledger.json','utf8'));
assert.equal(ledger.schema,'cuberev-022-p7-fmc-authored-physical-candidate-ledger-v1');
const tokenize=s=>{const a=s.trim().split(/\s+/).filter(Boolean);assert(a.every(t=>ACTIONS.includes(t)));return a;};
const stickerAfter=word=>{const x=solvedStickerCube();for(const t of word)applyMoveToken(x,t);return x;};
const cubieAfter=w=>toCubieState(stickerAfter(w));
const key=s=>s.cp.join(',')+'/'+s.co.join(',')+'/'+s.ep.join(',')+'/'+s.eo.join(',');
const enc=s=>String.fromCharCode(...s.cp.map(x=>65+x),...s.ep.map(x=>65+x));
const solved=cubieAfter([]);
const FACE=Object.fromEntries(ACTIONS.map(t=>[t,cubieAfter([t])]));
const compose=(s,m)=>({
 cp:m.cp.map(i=>s.cp[i]),
 co:m.co.map((x,i)=>(s.co[m.cp[i]]+x)%3),
 ep:m.ep.map(i=>s.ep[i]),
 eo:m.eo.map((x,i)=>s.eo[m.ep[i]]^x)
});
const normal={'0,1,0':'U','1,0,0':'R','0,0,1':'F','0,-1,0':'D','-1,0,0':'L','0,0,-1':'B'};
const ROT={UD:null,FB:'x',LR:'z'};
function frameMap(rot) {
 if(!rot)return {original_to_frame:Object.fromEntries('URFDLB'.split('').map(x=>[x,x])),frame_to_original:Object.fromEntries('URFDLB'.split('').map(x=>[x,x]))};
 const c=stickerAfter([rot]), oldToFrame={};
 for(const s of c)if(s.p.every((v,i)=>v===s.n[i])) oldToFrame[s.c]=normal[s.n.join(',')];
 assert.equal(Object.keys(oldToFrame).length,6);
 return {original_to_frame:oldToFrame,frame_to_original:Object.fromEntries(Object.entries(oldToFrame).map(([k,v])=>[v,k]))};
}
const MAP=Object.fromEntries(Object.keys(ROT).map(a=>[a,frameMap(ROT[a])]));
function phaseState(originalStickers,axis) {
 const rot=ROT[axis];assert(Object.hasOwn(ROT,axis));
 if(!rot)return toCubieState(originalStickers);
 const x=originalStickers.map(s=>({p:[...s.p],n:[...s.n],c:s.c}));
 applyMoveToken(x,rot);for(const s of x)s.c=MAP[axis].original_to_frame[s.c];
 return toCubieState(x);
}
const eo=s=>s.eo.every(v=>v===0);
const dr=s=>eo(s)&&s.co.every(v=>v===0)&&s.ep.slice(8).every(v=>v>=8);
const HALF='U2 R2 F2 D2 L2 B2'.split(' ');
const DR='U U2 U\u0027 D D2 D\u0027 R2 L2 F2 B2'.split(' ');
assert.equal(DR.length,10);
for(const t of DR)assert(dr(compose(solved,FACE[t])));
for(const a of Object.keys(ROT))assert.equal(key(phaseState(stickerAfter([]),a)),key(solved));
for(const a of Object.keys(ROT))for(const t of ACTIONS){
 const f=MAP[a].original_to_frame[t[0]]+t.slice(1);
 assert.equal(key(phaseState(stickerAfter([t]),a)),key(FACE[f]),'axis conjugacy check '+a+'/'+t);
}

assert.equal(ACTIONS.length,18);
const acts=ACTIONS,move=acts.map(x=>FACE[x]),names=acts.map(x=>x[0]),
 opposite={U:'D',D:'U',R:'L',L:'R',F:'B',B:'F'};
const chars=acts.map((_,i)=>String.fromCharCode(65+i)),inverse={};
for(let i=0;i<acts.length;i++){
 const t=acts[i],s=t.endsWith("'")?t[0]:t.endsWith('2')?t:t[0]+"'";
 inverse[chars[i]]=chars[acts.indexOf(s)];
 assert(inverse[chars[i]]);
}
function encode(s){
 return String.fromCharCode(...s.cp.map(x=>65+x),...s.co.map(x=>65+x),
 ...s.ep.map(x=>65+x),...s.eo.map(x=>65+x));
}
function advance(k,m){
 const v=new Array(40);
 for(let i=0;i<8;i++){
  v[i]=k.charCodeAt(m.cp[i]);v[8+i]=65+(k.charCodeAt(8+m.cp[i])-65+m.co[i])%3;
 }
 for(let i=0;i<12;i++){
  v[16+i]=k.charCodeAt(16+m.ep[i]);
  v[28+i]=65+((k.charCodeAt(28+m.ep[i])-65)^m.eo[i]);
 }
 return String.fromCharCode(...v);
}
function decodeWord(s){return Array.from(s,x=>acts[x.charCodeAt(0)-65]);}
function invertWord(s){return Array.from(s).reverse().map(x=>inverse[x]).join('');}
function adjacentNormalized(word){
 const result=[],e=x=>x.endsWith('2')?2:x.endsWith("'")?3:1;
 for(const x of word){
  const p=result.at(-1);
  if(!p||p[0]!==x[0]){result.push(x);continue;}
  const r=(e(p)+e(x))%4;result.pop();
  if(r)result.push(x[0]+(r===1?'':r===2?'2':"'"));
 }
 return result;
}
const OPPOSITE_CANONICAL=true;
function bfs(source,maxDepth,name){
 const visited=new Map([[source,'']]);
 let frontier=[source],hist=[1],transitions=0;
 for(let depth=1;depth<=maxDepth;depth++){
  const next=[];
  for(const key of frontier){
   const w=visited.get(key);
   const last=w.length?names[w.charCodeAt(w.length-1)-65]:null;
   for(let a=0;a<18;a++){
    const face=names[a];
    if(last!==null&&(face===last||(OPPOSITE_CANONICAL&&opposite[last]===face&&face<last)))continue;
    transitions++;
    const n=advance(key,move[a]);
    if(visited.has(n))continue;
    visited.set(n,w+chars[a]);next.push(n);
   }
  }
  hist.push(next.length);frontier=next;
 }
 return {visited,frontier,hist,transitions,name};
}
const root=encode(solved),G=bfs(root,5,'reverse_from_solved_18_face_htm');
assert(G.hist[0]===1);
assert.equal(G.hist.reduce((a,b)=>a+b,0),G.visited.size);
assert(G.hist[1]===18);
function inspect(source,side,label) {
 let best=null,intersectionChecks=0;
 for(const [key,fw] of side.visited){
  const bw=G.visited.get(key);
  intersectionChecks++;
  if(bw===undefined)continue;
  const total=fw.length+bw.length;
  if(!best||total<best.length){
   best={length:total,forward:fw,backward:bw,
    continuationChars:fw+invertWord(bw)};
  }
 }
 return {best,intersectionChecks};
}
const scramble=tokenize(ledger.normal_scramble);
const rows=[],cache=new Map();
for(const item of ledger.eo_dr_pairs.filter(x=>x.id!=='riabov_other_2')){
 const authored=[...tokenize(item.eo_prefix),...tokenize(item.dr_extension)];
 const cube=stickerAfter([...scramble,...authored]);
 const axes=Object.keys(ROT).filter(a=>dr(phaseState(cube,a)));
 assert.equal(axes.length,1);
 const source=encode(toCubieState(cube));
 let res=cache.get(source);
 if(!res){
  let forward=bfs(source,4,item.id+'_radius4'),scan=inspect(source,forward,item.id);
  const examinedLayers=[...forward.hist];
  let streamed11=0,found11=null;
  if(scan.best===null){
   forward=bfs(source,5,item.id+'_radius5');
   scan=inspect(source,forward,item.id);
   examinedLayers.splice(0,examinedLayers.length,...forward.hist);
   if(scan.best===null){
    // Every path length 11 intersects the source radius-5 sphere
    // and the goal radius-5 sphere with one final goal-side edge.
    // We test that edge without allocating the ~7.6M-state radius-six layer.
    search11:for(const [goalState,goalWord] of G.visited){
     if(goalWord.length!==5)continue;
     for(let a=0;a<18;a++){
      const newState=advance(goalState,move[a]);streamed11++;
      const forwardWord=forward.visited.get(newState);
      if(forwardWord===undefined)continue;
      const candidate=forwardWord+inverse[chars[a]]+invertWord(goalWord);
      assert.equal(candidate.length,11);
      found11={length:11,continuationChars:candidate,forward:forwardWord,backward:goalWord};
      break search11;
     }
    }
    if(found11)scan.best=found11;
   }
  }
  const b=scan.best;
  const shortest=b?.length??null;
  if(shortest!==null)assert(shortest<=11);
  // Every legal word length <=9 has a midpoint radius4 from source and radius5 from solved.
  // If no word at <=9, radius5 each covers all length <=10.
  const certificate=shortest===null?'>=12':shortest<=9?'EXACT_LE_9':shortest===10?'EXACT_10':'EXACT_11';
  const turns=b?decodeWord(b.continuationChars):null;
  const path=turns?[...authored,...turns]:null;
  if(path)assert(solvedUpToRotation(stickerAfter([...scramble,...path])));
  res={full_18_HTM_minimum:shortest,full_18_HTM_warrant:certificate,
   lower_bound_HTM:shortest??12,upper_bound_HTM:shortest??null,
   depth11_goal5_to_source5_streamed_tests:streamed11,
   goal_depth_six_layer_NOT_materialized:true,
   source_frontier_depth:examinedLayers.length-1,source_frontier_counts:examinedLayers,
   forward_states:examinedLayers.reduce((a,b)=>a+b,0),intersection_checks:scan.intersectionChecks,
   actual_18_move_continuation:turns?.join(' ')??null};
  cache.set(source,res);
 }
 const suffix=res.actual_18_move_continuation?tokenize(res.actual_18_move_continuation):null;
 const joint=suffix?[...authored,...suffix]:null;
 const normalized=joint?adjacentNormalized(joint):null;
 if(joint)assert(solvedUpToRotation(stickerAfter([...scramble,...joint])));
 if(normalized)assert(solvedUpToRotation(stickerAfter([...scramble,...normalized])));
 rows.push({id:item.id,axis:axes[0],source_parse_grade:item.declared_mode,
  original_literal_source_prefix_HTM:authored.length,
  ...res,
  full_18_HTM_raw_total_when_witness:joint?.length??null,
  full_18_HTM_normalized_witness_length:normalized?.length??null,
  original_source_prefix_retained_in_normalized_word:normalized?authored.every((x,i)=>x===normalized[i]):null,
  all_18_continuations_original_sticker_physically_valid:joint!==null,
  full_18_HTM_complete_normalized_witness:normalized?.join(' ')??null});
}
const main=rows.find(x=>x.id==='miao_main'),alt=rows.find(x=>x.id==='miao_alternative_from_same_eo');
assert(main.full_18_HTM_minimum===rows.find(x=>x.id==='riabov_main').full_18_HTM_minimum);
const comparison={
 main_raw_total_upper_bound:main.full_18_HTM_minimum===null?null:main.original_literal_source_prefix_HTM+main.full_18_HTM_minimum,
 alternative_raw_total_lower_bound:alt.original_literal_source_prefix_HTM+alt.lower_bound_HTM,
 strict_main_better_proved:(main.full_18_HTM_minimum!==null)&&main.original_literal_source_prefix_HTM+main.full_18_HTM_minimum<alt.original_literal_source_prefix_HTM+alt.lower_bound_HTM,
 exact_both_full_18_HTM:(main.full_18_HTM_minimum!==null&&alt.full_18_HTM_minimum!==null)
};
console.log(JSON.stringify({
 marker:'CUBE_REV_022_P8_R4_FULL_18_HTM_MEET_IN_MIDDLE_SOURCE_PREFIX_COMPARISON',
 true_3x3_model:'Full sticker cube original 18 HTM outer turns, not DR-preserving or mandatory HTR',
 backward_solved_radius_HTM:5,
 backward_bfs_counts:G.hist,
 backward_bfs_states:G.visited.size,
 source_bound_method:'For all paths length <=9: source radius4 / goal radius5 intersection. For <=10: source radius5 / goal radius5 intersection. For exact 11: one streamed legal goal-side step from goal depth5 against source depth5, without materializing the goal depth6 layer. Prune adjacent same-face and reversed opposite commuting turns without losing a shortest canonical representative.',
 source_results:rows,
 same_EO_main_vs_alternative:comparison,
 historical_source_words_not_assumed_actual_search_traces:true,
 normalized_word_distinguished_from_literal_source_prefix:true,
 no_unrestricted_global_competition_FMC_claim:true
},null,2));
