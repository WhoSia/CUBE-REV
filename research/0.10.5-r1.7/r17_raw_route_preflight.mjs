import fs from 'node:fs';
import { cube3x3x3 } from 'cubing/puzzles';
const x=JSON.parse(fs.readFileSync('research/0.10.5-r1.7/evidence-raw-route-preflight/RAW_ROUTE_EXTRACT.json','utf8'));
const kp=await cube3x3x3.kpuzzle();
const results=[];
for(const r of x.records){
 const c=r.chosen;const out={url:r.url,type:c?.type||null};
 try{
  const end=kp.defaultPattern().applyAlg(c.setup).applyAlg(c.alg);
  out.parse=true;out.kpattern_solved=end.experimentalIsSolved({ignorePuzzleOrientation:true,ignoreCenterOrientation:true});out.setup=c.setup;out.alg=c.alg;
 }catch(e){out.parse=false;out.error=String(e?.stack||e).slice(0,900)}
 results.push(out);
}
const out={schema_version:'CR0105R17-RAW-ROUTE-PREFLIGHT-KPATTERN-1',status:results.every(r=>r.parse&&r.kpattern_solved)?'PASS':'HOLD',results,human_observations:0};
fs.writeFileSync('research/0.10.5-r1.7/evidence-raw-route-preflight/RAW_ROUTE_KPATTERN.json',JSON.stringify(out,null,2)+'\n');console.log(JSON.stringify(out,null,2));if(out.status!=='PASS')process.exit(2);
