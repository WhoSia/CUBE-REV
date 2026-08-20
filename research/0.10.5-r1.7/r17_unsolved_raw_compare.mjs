import fs from 'node:fs';
import crypto from 'node:crypto';
import { cube3x3x3 } from 'cubing/puzzles';
const src=JSON.parse(fs.readFileSync('research/0.10.5-r1.7/evidence-unsolved-audit/UNSOLVED_ALG_LINK_EXTRACT.json','utf8'));
const kp=await cube3x3x3.kpuzzle();
function stable(x){if(Array.isArray(x))return '['+x.map(stable).join(',')+']';if(x&&typeof x==='object')return '{'+Object.keys(x).sort().map(k=>JSON.stringify(k)+':'+stable(x[k])).join(',')+'}';return JSON.stringify(x)}
function h(t){return crypto.createHash('sha256').update(stable(t.transformationData)).digest('hex')}
function solved(t){return kp.defaultPattern().applyTransformation(t).experimentalIsSolved({ignorePuzzleOrientation:true,ignoreCenterOrientation:true});}
const results=[];
for(const r of src.records){
  const link=r.alg_links?.[0]; const out={reco_id:r.reco_id,method:r.method,attempt_value:r.attempt_value,alg_link_count:r.alg_links?.length||0};
  try{
    if(!link)throw new Error('ALG_LINK_MISSING');
    const rawS=kp.algToTransformation(link.setup), pageS=kp.algToTransformation(r.page_scramble);
    const rawT=kp.algToTransformation(link.alg), parsedT=kp.algToTransformation(r.parsed_moves.join(' '));
    const rawEnd=rawS.applyTransformation(rawT), parsedEnd=pageS.applyTransformation(parsedT);
    out.link_type=link.type||'(default)';out.raw_setup=link.setup;out.raw_alg=link.alg;
    out.setup_transform_equal=rawS.isIdentical(pageS);
    out.alg_transform_equal=rawT.isIdentical(parsedT);
    out.raw_kpattern_solved=solved(rawEnd);out.parsed_kpattern_solved=solved(parsedEnd);
    out.raw_alg_hash=h(rawT);out.parsed_alg_hash=h(parsedT);out.raw_residual_hash=h(rawEnd);out.parsed_residual_hash=h(parsedEnd);
    out.raw_string_length=link.alg.length;out.parsed_move_count=r.parsed_moves.length;
  }catch(e){out.error=String(e?.stack||e).slice(0,1000)}
  results.push(out);
}
const summary={
 schema_version:'CR0105R17-UNSOLVED-RAW-COMPARE-1',status:'PASS_DIAGNOSTIC',n:results.length,
 raw_solved:results.filter(r=>r.raw_kpattern_solved).length,
 parsed_solved:results.filter(r=>r.parsed_kpattern_solved).length,
 setup_transform_equal:results.filter(r=>r.setup_transform_equal).length,
 alg_transform_equal:results.filter(r=>r.alg_transform_equal).length,
 raw_solved_parsed_unsolved:results.filter(r=>r.raw_kpattern_solved&&!r.parsed_kpattern_solved).map(r=>r.reco_id),
 raw_unsolved:results.filter(r=>r.raw_kpattern_solved===false).map(r=>r.reco_id),
 parser_loss_confirmed:results.some(r=>r.raw_kpattern_solved&&!r.parsed_kpattern_solved),results,human_observations:0
};
fs.writeFileSync('research/0.10.5-r1.7/evidence-unsolved-audit/UNSOLVED_RAW_COMPARE.json',JSON.stringify(summary,null,2)+'\n');console.log(JSON.stringify({...summary,results:undefined},null,2));
