export function stable(value){
  if(Array.isArray(value))return `[${value.map(stable).join(',')}]`;
  if(value&&typeof value==='object')return `{${Object.keys(value).sort().map(k=>`${JSON.stringify(k)}:${stable(value[k])}`).join(',')}}`;
  return JSON.stringify(value);
}

export function runHistory(system,start,history){
  let state=system.clone(start),context=system.contextInit?.()??null;
  const trace=[{state:system.clone(state),context,action:null}];
  for(const action of history){
    const before=system.clone(state);
    state=system.apply(system.clone(state),action);
    context=system.contextStep?.(context,{before,action,after:system.clone(state)})??context;
    trace.push({state:system.clone(state),context,action});
  }
  return {state,context,trace};
}

export function sameState(system,a,b){return system.serialize(a)===system.serialize(b);}

export function actionHistogram(history){
  const m=new Map();for(const a of history)m.set(a,(m.get(a)||0)+1);
  return Object.fromEntries([...m.entries()].sort(([a],[b])=>String(a).localeCompare(String(b))));
}

export function certifyTransposition(system,{start,historyA,historyB,commonSuffix=[]}){
  const A=runHistory(system,start,historyA),B=runHistory(system,start,historyB),n=commonSuffix.length;
  const preA=n?A.trace[A.trace.length-1-n].state:A.state;
  const preB=n?B.trace[B.trace.length-1-n].state:B.state;
  const suffixMatches=n===0||(stable(historyA.slice(-n))===stable(commonSuffix)&&stable(historyB.slice(-n))===stable(commonSuffix));
  const hA=actionHistogram(historyA),hB=actionHistogram(historyB);
  return {
    same_terminal:sameState(system,A.state,B.state),
    same_pre_suffix:sameState(system,preA,preB),
    common_suffix:suffixMatches,
    context_equal:A.context===B.context,
    different_context:A.context!==B.context,
    equal_action_histogram:stable(hA)===stable(hB),
    histogram_A:hA,histogram_B:hB,
    terminal_serialization:system.serialize(A.state),
    context_A:A.context,context_B:B.context,
    action_surface:[...(system.actions?.(A.state)??[])],
    trace_A:A.trace.map(x=>({state:system.serialize(x.state),context:x.context,action:x.action})),
    trace_B:B.trace.map(x=>({state:system.serialize(x.state),context:x.context,action:x.action}))
  };
}

export function certifyFamily(system,{start,divergent,control,commonSuffix=[]}){
  const D=certifyTransposition(system,{start,historyA:divergent[0],historyB:divergent[1],commonSuffix});
  const C=certifyTransposition(system,{start,historyA:control[0],historyB:control[1],commonSuffix});
  const pass=[D.same_terminal,D.same_pre_suffix,D.common_suffix,D.different_context,D.equal_action_histogram,C.same_terminal,C.same_pre_suffix,C.common_suffix,C.context_equal,C.equal_action_histogram,D.action_surface.length>=2,C.action_surface.length>=2].every(Boolean);
  return {pass,divergent:D,control:C};
}

export function certifyReversibility(system,states,actions){
  let pass=0,total=0;
  for(const s of states)for(const a of actions){
    total++;
    const next=system.apply(system.clone(s),a),back=system.apply(system.clone(next),system.inverse(a));
    if(sameState(system,s,back))pass++;
  }
  return {pass,total};
}
