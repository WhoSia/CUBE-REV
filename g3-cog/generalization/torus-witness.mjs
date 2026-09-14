import {certifyReversibility,certifyTransposition} from './rstp-core.js';

const N=5,mod=x=>(x%N+N)%N;
const system={
  id:'TORUS5-LANDMARK-CONTEXT-v1',
  clone:s=>[...s],
  serialize:s=>`${s[0]},${s[1]}`,
  actions:()=>['E','W','N','S'],
  inverse:a=>({E:'W',W:'E',N:'S',S:'N'})[a],
  apply:([x,y],a){if(a==='E')x++;else if(a==='W')x--;else if(a==='N')y++;else if(a==='S')y--;else throw new Error(`bad action ${a}`);return[mod(x),mod(y)];},
  contextInit:()=> 'A',
  contextStep:(z,{after})=>z==='I'||(after[0]===1&&after[1]===0)?'I':'A'
};

const states=[];for(let x=0;x<N;x++)for(let y=0;y<N;y++)states.push([x,y]);
const reversibility=certifyReversibility(system,states,system.actions());
const historyA=['E','N','W','S','N','E'];
const historyB=['W','N','E','S','N','E'];
const transposition=certifyTransposition(system,{start:[0,0],historyA,historyB,commonSuffix:['N','E']});

const pass=reversibility.pass===reversibility.total&&transposition.same_terminal&&transposition.same_pre_suffix&&transposition.common_suffix&&transposition.different_context&&transposition.equal_action_histogram&&transposition.action_surface.length===4;
const receipt={schema:'CUBE-REV-RSTP-NONCUBE-WITNESS-v1',system:system.id,reversibility,historyA,historyB,common_suffix:['N','E'],transposition,result:pass?'PASS':'FAIL'};
console.log(JSON.stringify(receipt,null,2));
if(!pass)process.exit(1);
