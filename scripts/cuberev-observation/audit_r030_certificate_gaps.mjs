// Deterministic finite-model audit; no dependencies. Run with node.
function audit() {
  const eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
  const require=(ok,msg)=>{if(!ok)throw Error(msg)};
  function costs(rows,labels) {
    const n=rows.length,m=rows[0].length,full=(1n<<BigInt(n))-1n;
    const bit=i=>1n<<BigInt(i);
    const masks=Array.from({length:m},(_,q)=>rows.reduce((a,row,s)=>row[q]?a|bit(s):a,0n));
    const pairs=[];for(let s=0;s<n;s++)for(let t=s+1;t<n;t++)if(labels[s]===labels[t]){
      let diff=0n;for(let q=0;q<m;q++)if(rows[s][q]!==rows[t][q])diff|=bit(q);
      pairs.push({s,t,diff,states:bit(s)|bit(t)});
    }
    const memo=new Map();
    function dp(b){if(!pairs.some(p=>(b&p.states)===p.states))return 0;if(memo.has(b))return memo.get(b);let v=Infinity;
      for(const mask of masks){const a=b&mask,c=b^a;if(a&&c)v=Math.min(v,1+Math.max(dp(a),dp(c)));}
      memo.set(b,v);return v;
    }
    function cover(ps) {
      if(ps.some(p=>p.diff===0n))return Infinity;
      const distinct=[...new Set(ps.map(p=>p.diff))];
      const cache=new Map();
      function visit(rem){if(!rem.length)return 0;const key=rem.join(",");if(cache.has(key))return cache.get(key);
        let v=Infinity,choose=rem[0];for(let q=0;q<m;q++)if(choose&bit(q))v=Math.min(v,1+visit(rem.filter(mask=>!(mask&bit(q)))));cache.set(key,v);return v;}
      return visit(distinct);
    }
    const local=Math.max(...rows.map((_,s)=>cover(pairs.filter(p=>p.s===s||p.t===s))));
    const early=Math.max(...[...new Set(labels)].map(k=>dp(labels.reduce((a,l,s)=>l===k?a|bit(s):a,0n))));
    const delayed=dp(full), fixed=cover(pairs);
    require(local<=early&&early<=delayed&&delayed<=fixed,"bound failure");
    return [local,early,delayed,fixed].map(x=>Number.isFinite(x)?x:"inf");
  }
  const hist={};for(let a=0;a<256;a++)for(let l=0;l<16;l++){
    const rows=Array.from({length:4},(_,s)=>[a>>(2*s)&1,a>>(2*s+1)&1]);
    const labels=Array.from({length:4},(_,s)=>l>>s&1);const key=costs(rows,labels).join(",");hist[key]=(hist[key]||0)+1;
  }
  require(hist["inf,inf,inf,inf"]===2416&&hist["1,1,1,1"]===672&&hist["1,1,2,2"]===192,"census mismatch");
  const indexing=[];for(let k=1;k<=4;k++)for(let d=1;d<=3;d++){
    const rows=[],labels=[];for(let i=0;i<k;i++)for(let b=0;b<2**d;b++){
      rows.push(Array.from({length:k*d},(_,q)=>Math.floor(q/d)===i?(b>>(q%d))&1:0));labels.push(i);
    }const got=costs(rows,labels);require(eq(got,[d,d,k*d,k*d]),"indexing mismatch");indexing.push({k,d,costs:got});
  }
  const onehot=[];for(let n=2;n<=12;n++){
    const rows=Array.from({length:n},(_,s)=>Array.from({length:n},(_,q)=>+(q===s)));const got=costs(rows,Array(n).fill(0));require(eq(got,[1,n-1,n-1,n-1]),"onehot mismatch");onehot.push({n,costs:got});
  }
  const routing=[];for(let d=1;d<=4;d++){
    const n=2**d,rows=Array.from({length:n},(_,s)=>Array.from({length:n-1},(_,q)=>{
      let node=q+1,lo=0,hi=n;const path=node.toString(2).slice(1);for(const b of path){const mid=(lo+hi)/2;if(b==="0")hi=mid;else lo=mid;}return +(s>=(lo+hi)/2&&s<hi);
    }));const got=costs(rows,Array(n).fill(0));require(got[1]===d&&got[2]===d&&got[3]===n-1,"routing mismatch");routing.push({d,costs:got});
  }
  return {order:["local","early","delayed","fixed"],hist,indexing,onehot,routing};
}
function auditClock() {
  const results=[];
  for(let k=1;k<=4;k++)for(let d=1;d<=3;d++){
    const n=k*2**d,m=k*d,bit=i=>1n<<BigInt(i),full=bit(n)-1n;
    const label=s=>Math.floor(s/2**d);
    const masks=Array.from({length:m},(_,q)=>{let b=0n;for(let s=0;s<n;s++)if(label(s)===Math.floor(q/d)&&((s%(2**d))>>(q%d)&1))b|=bit(s);return b;});
    const fibers=Array.from({length:k},(_,i)=>{let b=0n;for(let s=0;s<n;s++)if(label(s)===i)b|=bit(s);return b;});
    const post=new Map(),pre=new Map();
    function known(b){if(!b||!(b&(b-1n)))return 0;if(post.has(b))return post.get(b);let v=Infinity;for(const mask of masks){const a=b&mask,c=b^a;if(a&&c)v=Math.min(v,1+Math.max(known(a),known(c)));}post.set(b,v);return v;}
    function hidden(b,t){if(!b)return 0;if(t===0)return Math.max(...fibers.map(f=>known(b&f)));const key=b+":"+t;if(pre.has(key))return pre.get(key);let v=Infinity;
      for(const mask of masks){const a=b&mask,c=b^a;v=Math.min(v,1+Math.max(hidden(a,t-1),hidden(c,t-1)));}pre.set(key,v);return v;
    }
    for(let t=0;t<=m+1;t++){const got=hidden(full,t),expect=t+Math.max(0,d-Math.floor(t/k));if(got!==expect)throw Error(JSON.stringify({k,d,t,got,expect}));results.push({k,d,t,depth:got});}
  }
  // With a constant label, two primary bits need 2 frames alone; one
  // additional state-dependent auxiliary bit can identify all four in 1.
  const states=[0,1,2,3];
  const primaryDistinct=Math.max(...[0,1].map(q=>new Set(states.map(s=>s>>q&1)).size));
  const jointDistinct=new Set(states.map(s=>`${s&1},${s>>1&1}`)).size;
  if(primaryDistinct!==2||jointDistinct!==4)throw Error("auxiliary leakage control failed");
  return {checked:results.length,results,auxiliaryLeakage:{earlyPrimary:2,paired:1,constantLabel:true}};
}
console.log(JSON.stringify({...audit(),clock:auditClock()}, null, 2));
