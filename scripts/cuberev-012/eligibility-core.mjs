/** CUBE-REV 0.12: Past-only stage and independent-donor admissibility. */
export function stagesBefore(prefixes){
  let prior=null;
  return prefixes.map(p=>{
    const stage=prior;
    const after=(p.annotation_after||'').trim().toLowerCase().replace(/\s+/g,' ');
    if(after)prior=after;
    return stage;
  });
}
export function stageClean(prefixes,start,length){
  return length>0&&start>=0&&start+length<=prefixes.length&&
    !prefixes.slice(start,start+length-1).some(p=>p.annotation_after||p.boundary_after);
}
export function independentDonor(a,b){
  return a.source_id!==b.source_id && Boolean(a.solver&&b.solver) &&
    a.solver!==b.solver && a.cohort!==b.cohort && a.stage!==null &&
    a.stage===b.stage && a.length===b.length && a.operator===b.operator &&
    a.elementary_form!==b.elementary_form && a.first_operator!==b.first_operator;
}
