import {certifyFamily,certifyReversibility} from './rstp-core-v2.js';

const N=5,mod=x=>(x%N+N)%N;
const system={
  id:'TORUS5-LANDMARK-CONTEXT-v2',
  clone:s=>[...s],serialize:s=>`${s[0]},${s[1]}`,
  actions:()=>['E','W','N','S'],
  inverse:a=>({E:'W',W:'E',N:'S',S:'N'})[a],
  apply([x,y],a){if(a==='E')x++;else if(a==='W')x--;else if(a==='N')y++;else if(a==='S')y--;else throw new Error(`bad action ${a}`);return[mod(x),mod(y)];},
  contextInit:()=> 'A',
  contextStep:(z,{after})=>z==='I'||(after[0]===1&&after[1]===0)?'I':'A'
};
const states=[];for(let x=0;x<N;x++)for(let y=0;y<N;y++)states.push([x,y]);
const common=['N','E'];
const hit=['E','N','W','S',...common];
const avoid1=['W','N','E','S',...common];
const avoid2=['N','W','S','E',...common];
const reversibility=certifyReversibility(system,states,system.actions());
const family=certifyFamily(system,{start:[0,0],divergent:[hit,avoid1],control:[avoid1,avoid2],commonSuffix:common});
const pass=reversibility.pass===reversibility.total&&family.pass;
const receipt={schema:'CUBE-REV-RSTP-TORUS-WITNESS-v2',system:system.id,reversibility,common_suffix:common,family,result:pass?'PASS':'FAIL'};
console.log(JSON.stringify(receipt,null,2));if(!pass)process.exit(1);
