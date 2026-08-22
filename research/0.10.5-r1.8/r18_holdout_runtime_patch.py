#!/usr/bin/env python3
from pathlib import Path
import json
src=Path('research/0.10.5-r1.8/r18_holdout_score.mjs').read_text(encoding='utf-8')
old="const lineRate=segments.length?segments.filter(x=>x.algorithm_excess).length/segments.length:null,lineBoot=[];if(certified.length){for(let b=0;b<1200;b++){let pos=0,n=0;for(let i=0;i<certified.length;i++){const r=certified[Math.floor(rng()*certified.length)],ss=segments.filter(z=>z.result_id===r.result_id&&z.attempt_number===r.attempt_number);pos+=ss.filter(z=>z.algorithm_excess).length;n+=ss.length}if(n)lineBoot.push(pos/n)}}"
new="const lineRate=segments.length?segments.filter(x=>x.algorithm_excess).length/segments.length:null,lineBoot=[];const lineByAttempt=new Map();for(const z of segments){const k=`${z.result_id}:${z.attempt_number}`,v=lineByAttempt.get(k)||{n:0,pos:0};v.n++;if(z.algorithm_excess)v.pos++;lineByAttempt.set(k,v)}if(certified.length){for(let b=0;b<1200;b++){let pos=0,n=0;for(let i=0;i<certified.length;i++){const r=certified[Math.floor(rng()*certified.length)],v=lineByAttempt.get(`${r.result_id}:${r.attempt_number}`)||{n:0,pos:0};pos+=v.pos;n+=v.n}if(n)lineBoot.push(pos/n)}}"
if src.count(old)!=1: raise RuntimeError(f'R18_HOLDOUT_BOOTSTRAP_PATCH_ANCHOR_{src.count(old)}')
src=src.replace(old,new)
out=Path('r18_holdout_score_runtime.mjs');out.write_text(src,encoding='utf-8')
rec={'schema_version':'CR0105R18-HOLDOUT-RUNTIME-PATCH-1','status':'PASS_COMPUTATIONAL_EQUIVALENCE_PATCH','change':'Pre-index phase-line positive/eligible counts by official attempt before cluster bootstrap; estimand, PRNG, bootstrap resampling unit, replicate count, and scoring thresholds unchanged.','scientific_definition_changed':False,'holdout_route_outcomes_read_by_patch':False,'human_observations':0}
Path('/tmp/r18holdout').mkdir(parents=True,exist_ok=True);Path('/tmp/r18holdout/HOLDOUT_RUNTIME_PATCH.json').write_text(json.dumps(rec,indent=2)+'\n');print(json.dumps(rec,indent=2))
