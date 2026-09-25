import {certifyFamily,certifyReversibility} from './rstp-core-v2.js';

const system={
  id:'S4-ADJACENT-TRANSPOSITION-CONTEXT-v1',
  clone:s=>[...s],serialize:s=>s.join(''),actions:()=>['A','B','C'],inverse:a=>a,
  apply(state,a){const s=[...state],i=({A:0,B:1,C:2})[a];if(i===undefined)throw new Error(`bad action ${a}`);[s[i],s[i+1]]=[s[i+1],s[i]];return s;},
  contextInit:()=> 'A',
  contextStep:(z,{after})=>z==='I'||after.join('')==='2103'?'I':'A'
};
function perms(xs){if(xs.length<=1)return[xs];const out=[];for(let i=0;i<xs.length;i++){const x=xs[i],rest=xs.slice(0,i).concat(xs.slice(i+1));for(const p of perms(rest))out.push([x,...p]);}return out;}
const states=perms([0,1,2,3]),common=['A','C'];
const hit=['A','B','A','C','B','C',...common];
const avoid1=['A','B','C','A','B','C',...common];
const avoid2=['C','B','A','C','B','A',...common];
const reversibility=certifyReversibility(system,states,system.actions());
const family=certifyFamily(system,{start:[0,1,2,3],divergent:[hit,avoid1],control:[avoid1,avoid2],commonSuffix:common});
const pass=reversibility.pass===reversibility.total&&family.pass;
const receipt={schema:'CUBE-REV-RSTP-S4-WITNESS-v1',system:system.id,algebra:'non-Abelian adjacent-transposition action',reversibility,common_suffix:common,family,result:pass?'PASS':'FAIL'};
console.log(JSON.stringify(receipt,null,2));if(!pass)process.exit(1);
