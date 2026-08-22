import fs from 'node:fs';
import crypto from 'node:crypto';
import { cube3x3x3 } from 'cubing/puzzles';

const input=JSON.parse(fs.readFileSync('research/0.10.5-r1.7/evidence-state-smoke2/STATE_SMOKE_INPUT.json','utf8'));
const kp=await cube3x3x3.kpuzzle();
function stable(x){if(Array.isArray(x))return '['+x.map(stable).join(',')+']';if(x&&typeof x==='object')return '{'+Object.keys(x).sort().map(k=>JSON.stringify(k)+':'+stable(x[k])).join(',')+'}';return JSON.stringify(x)}
function thash(t){return crypto.createHash('sha256').update(stable(t.transformationData)).digest('hex')}
function physicalSolved(t){return kp.defaultPattern().applyTransformation(t).experimentalIsSolved({ignorePuzzleOrientation:true,ignoreCenterOrientation:true});}

const faceMoves=[];for(const f of ['U','R','F','D','L','B'])for(const s of ['', '2', "'"])faceMoves.push(f+s);
const faceSet=new Set(faceMoves);const shortest=new Map();
function faceOf(m){return m[0]}
function addShortest(seq){const t=seq.length?kp.algToTransformation(seq.join(' ')):kp.identityTransformation();const h=thash(t),prev=shortest.get(h);if(!prev||seq.length<prev.length||(seq.length===prev.length&&seq.join(' ')<prev.join(' ')))shortest.set(h,[...seq]);}
addShortest([]);for(const a of faceMoves)addShortest([a]);for(const a of faceMoves)for(const b of faceMoves){if(faceOf(a)!==faceOf(b))addShortest([a,b]);}for(const a of faceMoves)for(const b of faceMoves)for(const c of faceMoves){if(faceOf(a)!==faceOf(b)&&faceOf(b)!==faceOf(c))addShortest([a,b,c]);}

const results=[];let parseFail=0,solved=0,loopRecords=0,rewriteRecords=0;
for(const rec of input.accepted_records){
 const out={reco_id:rec.reco_id,method:rec.method,speed_bin:rec.speed_bin,attempt_value:rec.attempt_value,move_count:rec.moves.length};
 try{
  const S=kp.algToTransformation(rec.scramble);let state=S;const hashes=[thash(state)];
  for(const m of rec.moves){state=state.applyMove(m);hashes.push(thash(state));}
  out.final_kpattern_solved=physicalSolved(state);if(out.final_kpattern_solved)solved++;
  const loops=[],by=new Map();
  for(let j=0;j<hashes.length;j++){const h=hashes[j],arr=by.get(h)||[];for(const i of arr){const len=j-i;if(len<2||len>24)continue;const seg=rec.moves.slice(i,j),T=kp.algToTransformation(seg.join(' '));if(T.isIdentityTransformation())loops.push({start:i,end:j,length:len,moves:seg.join(' ')});}arr.push(j);by.set(h,arr.slice(-6));}
  loops.sort((a,b)=>a.length-b.length||a.start-b.start);out.exact_state_revisit_loops=loops.slice(0,30);out.exact_loop_count=loops.length;if(loops.length)loopRecords++;
  const rew=[];
  for(let i=0;i<rec.moves.length;i++)for(let len=2;len<=8&&i+len<=rec.moves.length;len++){
   const win=rec.moves.slice(i,i+len);if(!win.every(m=>faceSet.has(m)))continue;const T=kp.algToTransformation(win.join(' ')),alt=shortest.get(thash(T));if(!alt||alt.length>=len)continue;
   const cf=[...rec.moves.slice(0,i),...alt,...rec.moves.slice(i+len)];const cfEnd=S.applyAlg(cf.join(' '));if(!cfEnd.isIdentical(state))throw new Error('COUNTERFACTUAL_ENDPOINT_MISMATCH');
   rew.push({start:i,end:i+len,actual_length:len,replacement_length:alt.length,saved_moves:len-alt.length,actual:win.join(' '),replacement:alt.join(' ')});
  }
  rew.sort((a,b)=>b.saved_moves-a.saved_moves||a.start-b.start);out.shorter_exact_rewrites=rew.slice(0,40);out.shorter_exact_rewrite_count=rew.length;out.max_saved_moves_in_window=rew.length?Math.max(...rew.map(x=>x.saved_moves)):0;if(rew.length)rewriteRecords++;
 }catch(e){out.error=String(e?.stack||e).slice(0,1200);parseFail++;}
 results.push(out);
}
const n=results.length,rate=n?solved/n:0;
const out={schema_version:'CR0105R17-STATE-ENGINE-SMOKE-KPATTERN-1',status:(n>=36&&rate>=0.95&&parseFail===0)?'PASS':'HOLD',cubing_version:'0.63.3',
 solved_predicate:'KPattern.experimentalIsSolved(ignorePuzzleOrientation=true, ignoreCenterOrientation=true)',admitted_records:n,engine_parse_failures:parseFail,kpattern_solved:solved,kpattern_solved_rate:rate,
 records_with_exact_state_revisit_loop:loopRecords,records_with_shorter_exact_rewrite:rewriteRecords,
 conservative_counterfactual_rule:'Candidate deletion/rewrite still requires exact KTransformation equality and full-route endpoint equality. KPattern is used only for physical solved-state admission, correcting the overly strict hand-rolled transformation-hash predicate.',
 prior_validator_failure:'The previous hand-rolled 24-orientation transformation hash rejected known solved fixtures; see KPattern solved fixture court.',results,human_observations:0};
fs.mkdirSync('research/0.10.5-r1.7/evidence-state-smoke-kpattern',{recursive:true});fs.writeFileSync('research/0.10.5-r1.7/evidence-state-smoke-kpattern/STATE_ENGINE_SMOKE_KPATTERN.json',JSON.stringify(out,null,2)+'\n');console.log(JSON.stringify({...out,results:undefined},null,2));if(out.status!=='PASS')process.exit(2);
