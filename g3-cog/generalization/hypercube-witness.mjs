import {certifyFamily,certifyReversibility} from './rstp-core-v2.js';

const system={
  id:'HYPERCUBE4-LANDMARK-CONTEXT-v1',
  clone:s=>[...s],serialize:s=>s.join(''),actions:()=>['X0','X1','X2','X3'],inverse:a=>a,
  apply(state,a){const s=[...state],i=Number(a.slice(1));if(!Number.isInteger(i)||i<0||i>=4)throw new Error(`bad action ${a}`);s[i]^=1;return s;},
  contextInit:()=> 'A',
  contextStep:(z,{after})=>z==='I'||after.join('')==='1000'?'I':'A'
};
const states=[];for(let n=0;n<16;n++)states.push([0,1,2,3].map(i=>(n>>i)&1));
const common=['X3','X1'];
const hit=['X0','X0','X1','X2',...common];
const avoid1=['X1','X0','X0','X2',...common];
const avoid2=['X1','X0','X2','X0',...common];
const reversibility=certifyReversibility(system,states,system.actions());
const family=certifyFamily(system,{start:[0,0,0,0],divergent:[hit,avoid1],control:[avoid1,avoid2],commonSuffix:common});
const pass=reversibility.pass===reversibility.total&&family.pass;
const receipt={schema:'CUBE-REV-RSTP-HYPERCUBE-WITNESS-v1',system:system.id,reversibility,common_suffix:common,family,result:pass?'PASS':'FAIL'};
console.log(JSON.stringify(receipt,null,2));if(!pass)process.exit(1);
