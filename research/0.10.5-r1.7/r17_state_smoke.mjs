import fs from 'node:fs';
import crypto from 'node:crypto';
import { cube3x3x3 } from 'cubing/puzzles';

const inPath=process.env.R17_SMOKE_INPUT || '/tmp/r17smoke/STATE_SMOKE_INPUT.json';
const outPath=process.env.R17_SMOKE_OUTPUT || '/tmp/r17smoke/STATE_ENGINE_SMOKE.json';
const input=JSON.parse(fs.readFileSync(inPath,'utf8'));
const kpuzzle=await cube3x3x3.kpuzzle();

function stable(x){
  if(Array.isArray(x)) return '['+x.map(stable).join(',')+']';
  if(x && typeof x==='object') return '{'+Object.keys(x).sort().map(k=>JSON.stringify(k)+':'+stable(x[k])).join(',')+'}';
  return JSON.stringify(x);
}
function thash(t){return crypto.createHash('sha256').update(stable(t.transformationData)).digest('hex');}

// Enumerate the 24 whole-cube orientations as exact transformations.
const orientationMoves=['x','y','z'];
const orientations=[]; const oq=[kpuzzle.identityTransformation()]; const oseen=new Set();
while(oq.length){
  const t=oq.shift(); const h=thash(t); if(oseen.has(h)) continue;
  oseen.add(h); orientations.push(t);
  for(const m of orientationMoves) oq.push(t.applyMove(m));
  if(orientations.length>30) throw new Error('ORIENTATION_GROUP_OVERFLOW');
}
if(orientations.length!==24) throw new Error(`ORIENTATION_GROUP_SIZE_${orientations.length}`);
const orientationHashes=new Set(orientations.map(thash));
function solvedModuloOrientation(t){return orientationHashes.has(thash(t));}
function orientationCanonicalHash(t){
  let best=null;
  for(const o of orientations){const h=stable(t.applyTransformation(o).transformationData); if(best===null||h<best) best=h;}
  return crypto.createHash('sha256').update(best).digest('hex');
}

const faceMoves=[];
for(const f of ['U','R','F','D','L','B']) for(const s of ['', '2', "'"]) faceMoves.push(f+s);
const faceSet=new Set(faceMoves);
function faceOf(m){return m[0];}
const shortest=new Map();
function addShortest(seq){
  const t=seq.length?kpuzzle.algToTransformation(seq.join(' ')):kpuzzle.identityTransformation();
  const h=thash(t); const prev=shortest.get(h);
  if(!prev || seq.length<prev.length || (seq.length===prev.length && seq.join(' ')<prev.join(' '))) shortest.set(h,[...seq]);
}
addShortest([]);
for(const a of faceMoves) addShortest([a]);
for(const a of faceMoves) for(const b of faceMoves){ if(faceOf(a)===faceOf(b)) continue; addShortest([a,b]); }
for(const a of faceMoves) for(const b of faceMoves) for(const c of faceMoves){
  if(faceOf(a)===faceOf(b)||faceOf(b)===faceOf(c)) continue;
  addShortest([a,b,c]);
}

const results=[];
let parseFail=0, solvedCount=0, exactLoopRecords=0, rewriteRecords=0, orientationOnlyRevisitRecords=0;
for(const rec of input.accepted_records){
  const out={reco_id:rec.reco_id,method:rec.method,speed_bin:rec.speed_bin,attempt_value:rec.attempt_value,
             move_count:rec.moves.length,rotation_tokens:rec.rotation_tokens,slice_tokens:rec.slice_tokens,wide_tokens:rec.wide_tokens};
  try{
    const scrambleT=kpuzzle.algToTransformation(rec.scramble);
    let state=scrambleT;
    const exactHashes=[thash(state)]; const orientHashes=[orientationCanonicalHash(state)]; const states=[state];
    for(const m of rec.moves){state=state.applyMove(m); states.push(state); exactHashes.push(thash(state)); orientHashes.push(orientationCanonicalHash(state));}
    out.final_exact_identity=state.isIdentityTransformation();
    out.final_solved_mod_orientation=solvedModuloOrientation(state);
    if(out.final_solved_mod_orientation) solvedCount++;

    const exactLoops=[]; const byExact=new Map();
    for(let j=0;j<exactHashes.length;j++){
      const h=exactHashes[j]; const arr=byExact.get(h)||[];
      for(const i of arr){
        const span=j-i; if(span<2||span>24) continue;
        const seg=rec.moves.slice(i,j);
        const segT=kpuzzle.algToTransformation(seg.join(' '));
        if(segT.isIdentityTransformation()) exactLoops.push({start:i,end:j,length:span,moves:seg.join(' ')});
      }
      arr.push(j); byExact.set(h,arr.slice(-6));
    }
    exactLoops.sort((a,b)=>a.length-b.length||a.start-b.start);
    out.exact_state_revisit_loops=exactLoops.slice(0,20);
    out.exact_loop_count=exactLoops.length;
    if(exactLoops.length) exactLoopRecords++;

    const orientationOnly=[]; const byOri=new Map();
    for(let j=0;j<orientHashes.length;j++){
      const h=orientHashes[j]; const arr=byOri.get(h)||[];
      for(const i of arr){
        const span=j-i; if(span<2||span>24||exactHashes[i]===exactHashes[j]) continue;
        orientationOnly.push({start:i,end:j,length:span});
      }
      arr.push(j); byOri.set(h,arr.slice(-6));
    }
    out.orientation_only_revisits=orientationOnly.slice(0,20);
    out.orientation_only_revisit_count=orientationOnly.length;
    if(orientationOnly.length) orientationOnlyRevisitRecords++;

    const rewrites=[];
    const moves=rec.moves;
    for(let i=0;i<moves.length;i++){
      for(let len=2;len<=8 && i+len<=moves.length;len++){
        const win=moves.slice(i,i+len); if(!win.every(m=>faceSet.has(m))) continue;
        const t=kpuzzle.algToTransformation(win.join(' ')); const alt=shortest.get(thash(t));
        if(!alt || alt.length>=len) continue;
        // Counterfactual verification against full route endpoint, not just local lookup.
        const cf=[...moves.slice(0,i),...alt,...moves.slice(i+len)];
        const cfFinal=scrambleT.applyAlg(cf.join(' '));
        if(!cfFinal.isIdentical(state)) throw new Error('COUNTERFACTUAL_ENDPOINT_MISMATCH');
        rewrites.push({start:i,end:i+len,actual_length:len,replacement_length:alt.length,saved_moves:len-alt.length,
                       actual:win.join(' '),replacement:alt.join(' ')});
      }
    }
    rewrites.sort((a,b)=>b.saved_moves-a.saved_moves||a.actual_length-b.actual_length||a.start-b.start);
    out.shorter_exact_rewrites=rewrites.slice(0,30);
    out.shorter_exact_rewrite_count=rewrites.length;
    out.max_saved_moves_in_window=rewrites.length?Math.max(...rewrites.map(x=>x.saved_moves)):0;
    if(rewrites.length) rewriteRecords++;
  }catch(e){out.error=String(e?.stack||e).slice(0,1200);parseFail++;}
  results.push(out);
}
const n=results.length; const solved=results.filter(x=>x.final_solved_mod_orientation).length;
const summary={
  schema_version:'CR0105R17-STATE-ENGINE-SMOKE-1',
  status:(n>=36 && solved/n>=0.70)?'PASS':'HOLD',
  cubing_npm_version:'0.63.3',orientation_group_size:orientations.length,
  admitted_records:n,engine_parse_failures:parseFail,solved_mod_orientation:solved,
  solved_mod_orientation_rate:n?solved/n:0,
  records_with_exact_state_revisit_loop:exactLoopRecords,
  records_with_shorter_exact_rewrite:rewriteRecords,
  records_with_orientation_only_revisit:orientationOnlyRevisitRecords,
  counterfactual_rule:'A redundancy candidate is promoted only when cube transformation equality verifies that deletion or a shorter local replacement preserves the full route endpoint.',
  rotation_rule:'Whole-cube rotations are preserved in replay. Solved-state admission is modulo the 24 physical cube orientations; deletion-safe loops require exact fixed-frame state equality, not orientation-normalized equality.',
  results,human_observations:0
};
fs.writeFileSync(outPath,JSON.stringify(summary,null,2)+'\n');
console.log(JSON.stringify({...summary,results:undefined},null,2));
if(summary.status!=='PASS') process.exit(2);
