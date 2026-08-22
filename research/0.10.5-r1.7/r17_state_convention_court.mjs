import fs from 'node:fs';
import crypto from 'node:crypto';
import { cube3x3x3 } from 'cubing/puzzles';
const input=JSON.parse(fs.readFileSync('research/0.10.5-r1.7/evidence-state-smoke2/STATE_SMOKE_INPUT.json','utf8'));
const kp=await cube3x3x3.kpuzzle();
function stable(x){if(Array.isArray(x))return '['+x.map(stable).join(',')+']';if(x&&typeof x==='object')return '{'+Object.keys(x).sort().map(k=>JSON.stringify(k)+':'+stable(x[k])).join(',')+'}';return JSON.stringify(x)}
function h(t){return crypto.createHash('sha256').update(stable(t.transformationData)).digest('hex')}
const orientations=[];const q=[kp.identityTransformation()];const seen=new Set();
while(q.length){const t=q.shift(),z=h(t);if(seen.has(z))continue;seen.add(z);orientations.push(t);for(const m of ['x','y','z'])q.push(t.applyMove(m));}
const oh=new Set(orientations.map(h));
const isSolved=t=>oh.has(h(t));
const counts={};const examples={};
function hit(name,t,id){counts[name]=(counts[name]||0)+(isSolved(t)?1:0);if(isSolved(t)&&(examples[name]||[]).length<8)(examples[name]??=[]).push(id);}
for(const r of input.accepted_records){
 const S=kp.algToTransformation(r.scramble);
 const all=r.moves.join(' ');
 const noInspection=r.lines.filter(x=>String(x.comment).toLowerCase()!=='inspection').flatMap(x=>x.moves).join(' ');
 const noRot=r.moves.filter(m=>!['x','y','z'].includes(m[0].toLowerCase())).join(' ');
 const noInsNoRot=r.lines.filter(x=>String(x.comment).toLowerCase()!=='inspection').flatMap(x=>x.moves).filter(m=>!['x','y','z'].includes(m[0].toLowerCase())).join(' ');
 for(const [sn,T] of [['all',kp.algToTransformation(all)],['noInspection',kp.algToTransformation(noInspection)],['noRot',kp.algToTransformation(noRot)],['noInsNoRot',kp.algToTransformation(noInsNoRot)]]){
   const Si=S.invert(), Ti=T.invert();
   const variants={
    [`S_then_${sn}`]:S.applyTransformation(T),
    [`${sn}_then_S`]:T.applyTransformation(S),
    [`Sinv_then_${sn}`]:Si.applyTransformation(T),
    [`${sn}_then_Sinv`]:T.applyTransformation(Si),
    [`S_then_${sn}Inv`]:S.applyTransformation(Ti),
    [`${sn}Inv_then_S`]:Ti.applyTransformation(S),
    [`Sinv_then_${sn}Inv`]:Si.applyTransformation(Ti),
    [`${sn}Inv_then_Sinv`]:Ti.applyTransformation(Si),
   };
   for(const [name,v] of Object.entries(variants)) hit(name,v,r.reco_id);
 }
}
const ranking=Object.entries(counts).sort((a,b)=>b[1]-a[1]||a[0].localeCompare(b[0])).map(([name,solved])=>({name,solved,rate:solved/input.accepted_records.length,examples:examples[name]||[]}));
const out={schema_version:'CR0105R17-STATE-CONVENTION-COURT-1',status:'PASS_DIAGNOSTIC',n:input.accepted_records.length,orientation_group_size:orientations.length,ranking,
 interpretation:'This court diagnoses group-composition and inclusion conventions only. It does not license redundancy phenotypes. A convention must independently explain essentially all exact WCA-scramble-linked reconstructions or the parser/frame model remains on HOLD.',human_observations:0};
fs.mkdirSync('research/0.10.5-r1.7/evidence-state-convention',{recursive:true});
fs.writeFileSync('research/0.10.5-r1.7/evidence-state-convention/STATE_CONVENTION_COURT.json',JSON.stringify(out,null,2)+'\n');
console.log(JSON.stringify(out,null,2));
