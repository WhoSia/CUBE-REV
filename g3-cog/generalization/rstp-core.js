export function canonical(value){return JSON.stringify(value);}

export function runHistory(system,start,history){
  let state=system.clone(start),context=system.contextInit?.()??null;
  const trace=[{state:system.clone(state),context}];
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
  const out={};for(const a of history)out[a]=(out[a]||0)+1;return out;
}

export function certifyTransposition(system,{start,historyA,historyB,commonSuffix=[]}){
  const A=runHistory(system,start,historyA),B=runHistory(system,start,historyB);
  const suffixN=commonSuffix.length;
  const preA=suffixN?A.trace[A.trace.length-1-suffixN].state:A.trace[A.trace.length-1].state;
  const preB=suffixN?B.trace[B.trace.length-1-suffixN].state:B.trace[B.trace.length-1].state;
  const suffixMatches=suffixN===0||canonical(historyA.slice(-suffixN))===canonical(commonSuffix)&&canonical(historyB.slice(-suffixN))===canonical(commonSuffix);
  return {
    same_terminal:sameState(system,A.state,B.state),
    same_pre_suffix:sameState(system,preA,preB),
    common_suffix:suffixMatches,
    different_context:A.context!==B.context,
    equal_action_histogram:canonical(actionHistogram(historyA))===canonical(actionHistogram(historyB)),
    terminal_serialization:system.serialize(A.state),
    context_A:A.context,
    context_B:B.context,
    action_surface:[...(system.actions?.(A.state)??[])],
    trace_A:A.trace.map(x=>({state:system.serialize(x.state),context:x.context,action:x.action??null})),
    trace_B:B.trace.map(x=>({state:system.serialize(x.state),context:x.context,action:x.action??null}))
  };
}

export function certifyReversibility(system,states,actions){
  let pass=0,total=0;
  for(const s of states)for(const a of actions){
    total++;
    const next=system.apply(system.clone(s),a);
    const back=system.apply(system.clone(next),system.inverse(a));
    if(sameState(system,s,back))pass++;
  }
  return {pass,total};
}
