#!/usr/bin/env python3
from pathlib import Path
import json
src=Path('research/0.10.5-r1.9/r19_future_scale_compatibility.mjs').read_text()
old="comparisons.push({key:key(a),method:a.method,crossfit_stat:a.attempt_statistic,loo_full_scale_stat:a.loo_attempt_statistic,abs_diff:Math.abs(a.attempt_statistic-a.loo_attempt_statistic),familywise_p:p,level:ref.level,n:ref.n});"
new="comparisons.push({key:key(a),method:a.method,fold:a.fold,feature_count_bin:a.feature_count_bin,loo_feature_count_bin:a.loo_feature_count_bin,crossfit_stat:a.attempt_statistic,loo_full_scale_stat:a.loo_attempt_statistic,abs_diff:Math.abs(a.attempt_statistic-a.loo_attempt_statistic),familywise_p:p,level:ref.level,n:ref.n});"
if src.count(old)!=1: raise RuntimeError('R19_SCALE_DIAG_COMPARISON_ANCHOR')
src=src.replace(old,new)
old2="score_transport:{pearson_crossfit_vs_loo:corr,abs_difference:{p50:upperQuantile(diffs,.5),p90:upperQuantile(diffs,.9),p99:upperQuantile(diffs,.99),max:Math.max(...diffs)}},checks,"
new2="score_transport:{pearson_crossfit_vs_loo:corr,abs_difference:{p50:upperQuantile(diffs,.5),p90:upperQuantile(diffs,.9),p99:upperQuantile(diffs,.99),max:Math.max(...diffs)},by_method:Object.fromEntries([...new Set(comparisons.map(x=>x.method))].sort().map(m=>{const z=comparisons.filter(x=>x.method===m),d=z.map(x=>x.abs_diff);return [m,{n:z.length,correlation:(()=>{const xx=z.map(x=>x.crossfit_stat),yy=z.map(x=>x.loo_full_scale_stat),ax=mean(xx),ay=mean(yy);let n=0,dx=0,dy=0;for(let i=0;i<xx.length;i++){n+=(xx[i]-ax)*(yy[i]-ay);dx+=(xx[i]-ax)**2;dy+=(yy[i]-ay)**2;}return dx&&dy?n/Math.sqrt(dx*dy):null;})(),abs_diff_p50:upperQuantile(d,.5),abs_diff_p90:upperQuantile(d,.9),abs_diff_p99:upperQuantile(d,.99),max:Math.max(...d)}]})),by_feature_count_bin:Object.fromEntries([...new Set(comparisons.map(x=>x.feature_count_bin))].sort().map(b=>{const z=comparisons.filter(x=>x.feature_count_bin===b),d=z.map(x=>x.abs_diff);return [b,{n:z.length,abs_diff_p50:upperQuantile(d,.5),abs_diff_p90:upperQuantile(d,.9),abs_diff_p99:upperQuantile(d,.99),max:Math.max(...d)}]})),top_abs_differences:[...comparisons].sort((a,b)=>b.abs_diff-a.abs_diff).slice(0,100)},checks,"
if src.count(old2)!=1: raise RuntimeError('R19_SCALE_DIAG_OUTPUT_ANCHOR')
src=src.replace(old2,new2)
src=src.replace("schema_version:'CR0105R19-FUTURE-SCORE-SCALE-COMPATIBILITY-1'","schema_version:'CR0105R19-FUTURE-SCORE-SCALE-FAILURE-DIAGNOSTIC-1'")
src=src.replace("status,role:'POST-SEAL ZERO-FRESH ENGINEERING AUDIT; DOES NOT CHANGE THE FROZEN METRIC OR NULL'","status:'POSTHOC_DIAGNOSTIC',role:'POSTHOC_DIAGNOSTIC_AFTER_SCALE_GATE_FAILURE; DOES NOT CHANGE THE FROZEN METRIC, NULL, OR FAILED GATE'")
src=src.replace("`${OUT}/FUTURE_SCORE_SCALE_COMPATIBILITY.json`","`${OUT}/FUTURE_SCORE_SCALE_FAILURE_DIAGNOSTIC.json`")
src=src.replace("if(status!=='PASS_FUTURE_SCALE_COMPATIBILITY')process.exit(20);","process.exit(0);")
Path('r19_scale_failure_diagnostic_runtime.mjs').write_text(src)
rec={'schema_version':'CR0105R19-SCALE-FAILURE-DIAGNOSTIC-PATCH-1','status':'POSTHOC_DIAGNOSTIC_PATCH','original_failed_gate':'crossfit_loo_stat_correlation_ge_0_95','gate_changed':False,'metric_changed':False,'null_changed':False,'fresh_current_rows':0,'human_observations':0}
Path('/tmp/r19scalediag').mkdir(parents=True,exist_ok=True);Path('/tmp/r19scalediag/DIAGNOSTIC_PATCH.json').write_text(json.dumps(rec,indent=2)+'\n')
print(json.dumps(rec,indent=2))
