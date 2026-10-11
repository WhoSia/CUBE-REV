// CUBE-REV 0.23 P3-R3B — genuinely physical 54-sticker meet-in-middle
// solver for the frozen 62 full 3x3 source states, using six legal half-turns.
// Independently derives sticker permutations directly from cube face geometry.
// This code does NOT import the earlier 54-sticker/cubie physical engines.
// Only exact integer/state/string equalities; no human cognition model.
import assert from "node:assert/strict";
import fs from "node:fs";
const FIXTURE = "data/cuberev-023/p3_r1b_real_62_physical_face9_cubie_fixture.csv";
const faces = "URFDLB", normals = {
  U:[0,1,0], R:[1,0,0], F:[0,0,1], D:[0,-1,0], L:[-1,0,0], B:[0,0,-1]
};
const geometries = {
  U:["y",1,-1], D:["y",-1,1], R:["x",1,-1],
  L:["x",-1,1], F:["z",1,-1], B:["z",-1,1]
};
const sourceLines = fs.readFileSync(FIXTURE,"utf8").trim().split(/\r?\n/);
assert.equal(sourceLines.shift(),"index,U,R,F,D,L,B,source_HTM,cubie_sha256");
const sources = sourceLines.map((s,i) => {
  const c=s.split(",");
  assert.equal(c.length,9);
  assert.equal(+c[0],i);
  assert.ok(Number.isInteger(+c[7])&&+c[7]>=0&&+c[7]<=5);
  assert.match(c[8],/^[a-f0-9]{64}$/);
  const face=c.slice(1,7);
  assert.ok(face.every(x=>x.length===9&&/^[URFDLB]{9}$/.test(x)));
  let counts=Object.fromEntries([...faces].map(x=>[x,0]));
  for(const x of face.join(""))counts[x]++;
  assert.ok(Object.values(counts).every(n=>n===9));
  return {state:face.join(""),depth:+c[7],digest:c[8]};
});
assert.equal(sources.length,62);
assert.equal(new Set(sources.map(s=>s.state)).size,62);
assert.equal(new Set(sources.map(s=>s.digest)).size,62);
const slots=[];
for(const face of faces){
  const n=normals[face],local=[];
  for(let a=-1;a<=1;a++)for(let b=-1;b<=1;b++){
    const p=n[0]?[n[0],a,b]:n[1]?[a,n[1],b]:[a,b,n[2]];
    local.push({p,n});
  }
  local.sort((a,b)=>a.p.join(",").localeCompare(b.p.join(","),"en"));
  slots.push(...local);
}
const sig=s=>s.p.join(",")+"|"+s.n.join(",");
const slotIndex=new Map(slots.map((s,i)=>[sig(s),i]));
assert.equal(slotIndex.size,54);
function rotate(v,axis,quarter){
  let [x,y,z]=v;
  for(let i=0;i<(quarter%4+4)%4;i++){
    if(axis==="x")[x,y,z]=[x,-z,y];
    else if(axis==="y")[x,y,z]=[z,y,-x];
    else [x,y,z]=[-y,x,z];
  }
  return [x,y,z];
}
const actions=[...faces].flatMap(f=>[f,f+"'",f+"2"]);
const permutations=actions.map(token=>{
  const [axis,layer,q]=geometries[token[0]];
  const power=token.endsWith("'")?3:token.endsWith("2")?2:1;
  const p=slots.map(s=>{
    const moved=s.p["xyz".indexOf(axis)]===layer
      ?{p:rotate(s.p,axis,q*power),n:rotate(s.n,axis,q*power)}
      :s;
    const index=slotIndex.get(sig(moved));
    assert.ok(Number.isInteger(index));
    return index;
  });
  assert.equal(new Set(p).size,54);
  return p;
});
const identity=[...faces].map(x=>x.repeat(9)).join("");
function move(state,actionIndex){
  const out=Array(54),p=permutations[actionIndex];
  for(let j=0;j<54;j++)out[p[j]]=state[j];
  return out.join("");
}
const halfIds=actions.map((a,i)=>a.endsWith("2")?i:-1).filter(i=>i>=0);
assert.deepEqual(halfIds.map(i=>actions[i]),["U2","R2","F2","D2","L2","B2"]);
for(let i=0;i<18;i++){
  const inverseName=actions[i].endsWith("2")?actions[i]:actions[i].endsWith("'")?actions[i][0]:actions[i]+"'";
  const inverse=actions.indexOf(inverseName);
  assert.ok(inverse>=0);
  assert.equal(move(move(identity,i),inverse),identity);
}
function distanceCensus(alphabet,maxDepth){
  const visited=new Map([[identity,{depth:0,paths:1,word:[]}]]);
  let frontier=[identity],hist=[1];
  for(let depth=1;depth<=maxDepth;depth++){
    const next=[];
    for(const s of frontier){
      const current=visited.get(s);
      for(const i of alphabet){
        const t=move(s,i),old=visited.get(t);
        if(old){
          if(old.depth===depth)old.paths+=current.paths;
          continue;
        }
        visited.set(t,{depth,paths:current.paths,word:[...current.word,i]});
        next.push(t);
      }
    }
    frontier=next;hist.push(next.length);
  }
  return {visited,hist};
}
const full=distanceCensus(actions.map((_,i)=>i),4);
const half=distanceCensus(halfIds,5);
const goalRadius2=distanceCensus(halfIds,2);
assert.deepEqual(full.hist,[1,18,243,3240,43239]);
assert.deepEqual(half.hist,[1,6,27,120,519,1932]);
assert.equal(goalRadius2.visited.size,34);
let firstMoveSupport=Object.fromEntries(halfIds.map(i=>[actions[i],0]));
const shortestCountHist={},firstChoiceHist={},examples=[];
const witnessWords=[],solverForwardHistogram={};
let totalLiteralMoves=0,totalShortestWords=0,totalForwardScanned=0,maxForwardScanned=0;
for(let index=0;index<sources.length;index++){
  const s=sources[index];
  const fullShort=full.visited.get(s.state),halfShort=half.visited.get(s.state);
  assert.equal(fullShort?.depth===undefined?s.depth:fullShort.depth,s.depth);
  assert.equal(halfShort?.depth,s.depth,"Half-turn group source state must be exactly as short");
  // Exact first moves and exact all-18 shortest completion word counts,
  // obtained from the complete all-18 goal ball at depth<=4.
  let allShortestWords=0,halfShortestWords=0,opts=[];
  for(let i=0;i<18;i++){
    const neighbor=full.visited.get(move(s.state,i));
    if(neighbor?.depth===s.depth-1){
      opts.push(actions[i]);allShortestWords+=neighbor.paths;
    }
  }
  for(const i of halfIds){
    const neighbor=half.visited.get(move(s.state,i));
    if(neighbor?.depth===s.depth-1)halfShortestWords+=neighbor.paths;
  }
  assert.ok(opts.length>=1);
  assert.ok(opts.every(t=>t.endsWith("2")));
  assert.equal(allShortestWords,halfShortestWords,
    "Every shortest 18-HTM whole-cube word belongs to the half-turn subgrammar");
  shortestCountHist[allShortestWords]=(shortestCountHist[allShortestWords]||0)+1;
  firstChoiceHist[opts.length]=(firstChoiceHist[opts.length]||0)+1;
  for(const t of opts)firstMoveSupport[t]++;
  totalShortestWords+=allShortestWords;
  totalLiteralMoves+=s.depth;
  // Executable 3+2 search. Enumerate source-side radius<=3 in BFS
  // over real half turns; intersect with the 34 real goal-side states.
  // Reverse witnesses use self-inverse half turns only.
  const seen=new Map([[s.state,[]]]);
  let frontier=[s.state],best=null,scanned=0;
  for(let depth=0;depth<=3;depth++){
    const next=[];
    for(const cur of frontier){
      scanned++;
      const rev=goalRadius2.visited.get(cur);
      if(rev){
        const sequence=[...seen.get(cur),...rev.word.toReversed()];
        if(sequence.length<=5 && (!best||sequence.length<best.length))best=sequence;
      }
      if(depth===3)continue;
      for(const i of halfIds){
        const nextState=move(cur,i);
        if(!seen.has(nextState)){seen.set(nextState,[...seen.get(cur),i]);next.push(nextState);}
      }
    }
    frontier=next;
  }
  assert.ok(best);
  assert.equal(best.length,s.depth,"The constructed program attains global all18 HTM shortest length");
  let replay=s.state;
  for(const m of best)replay=move(replay,m);
  assert.equal(replay,identity,"Every one of 62 program outputs solves the ORIGINAL 54 facelets");
  witnessWords.push(best.map(i=>actions[i]).join(" "));
  totalForwardScanned+=scanned;maxForwardScanned=Math.max(maxForwardScanned,scanned);
  solverForwardHistogram[scanned]=(solverForwardHistogram[scanned]||0)+1;
  if(index<4||opts.length===2)examples.push({
    source_index:index,source_depth:s.depth,
    all_shortest_first_moves:opts,
    exact_optimal_word_count:allShortestWords,
    program_output:best.map(i=>actions[i]).join(" ")
  });
}
assert.deepEqual(shortestCountHist,{"1":50,"2":12});
assert.deepEqual(firstChoiceHist,{"1":58,"2":4});
assert.equal(totalLiteralMoves,306);
assert.equal(totalShortestWords,74);
assert.equal(witnessWords.length,62);
console.log(JSON.stringify({
  marker:"CUBE_REV_023_P3_R3B_REAL_54_STICKER_HALF_TURN_MITM_EXACT_SHORTEST_SOURCE_THEOREM",
  fixture:FIXTURE,physical_source_states:62,
  full18_Cayley_depths_to4:full.hist,
  halfturn_Cayley_depths_to5:half.hist,
  actual_halfturn_generators:halfIds.map(i=>actions[i]),
  halfturn_radius2_goal_table_states:goalRadius2.visited.size,
  source_depth_histogram:{"3":2,"5":60},
  source_all_have_same_exact_full18_and_halfturn_distance:true,
  original_physical_sticker_replays_solved:62,
  all_62_shortest_complete_solution_words_are_halfturn_only:true,
  exact_first_move_choice_histogram:firstChoiceHist,
  exact_geodesic_word_count_histogram:shortestCountHist,
  total_exact_shortest_solution_words:totalShortestWords,
  literal_62_word_table_HTM_token_slots:totalLiteralMoves,
  universal_program_runtime_max_goal_table_states:34,
  universal_program_runtime_forward_depth:3,
  universal_program_forward_scanned_max:maxForwardScanned,
  universal_program_forward_scanned_sum:totalForwardScanned,
  universal_program_forward_scanned_hist:solverForwardHistogram,
  optimal_first_move_frequency:firstMoveSupport,
  examples,
  finite_program_is_not_proven_minimum_byte_description_length:true,
  no_unpriced_state_oracle_for_general_3x3:true,
  no_human_candidate_selection_inferred:true
},null,2));
