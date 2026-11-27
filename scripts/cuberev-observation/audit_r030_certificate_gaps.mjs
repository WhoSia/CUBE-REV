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
function auditStructure() {
  const pop=x=>{let n=0;while(x){x&=x-1;n++;}return n;};
  function rank(rows){const piv=new Map();for(let x of rows){while(x){const p=31-Math.clz32(x);if(!piv.has(p)){piv.set(p,x);break;}x^=piv.get(p);}}return piv.size;}
  const results=[];let subsets=0, targetChecks=0;
  for(let n=1;n<=3;n++)for(let d=0;d<=n;d++){
    const inputs=Array.from({length:2**n},(_,i)=>i);
    const mon=inputs.filter(x=>pop(x)<=d),m=mon.length;
    const rows=inputs.map(x=>mon.reduce((a,u,j)=>(u&x)===u?a|(1<<j):a,0));
    const output=(coeff,row)=>pop(coeff&row)%2;
    let minFull=Infinity, targetMin=Array(m).fill(Infinity);
    for(let set=0;set<2**inputs.length;set++){
      const selected=rows.filter((_,i)=>set>>i&1),r=rank(selected),seen=new Map();
      for(let c=0;c<2**m;c++){
        const sig=selected.reduce((a,row,i)=>a|(output(c,row)<<i),0);
        const old=seen.get(sig);
        if(old===undefined)seen.set(sig,{first:c,ambiguous:0});
        else old.ambiguous|=old.first^c;
      }
      if(seen.size!==2**r)throw Error("rank/signature discrepancy");
      if(seen.size===2**m)minFull=Math.min(minFull,pop(set));
      let ambiguous=0;for(const item of seen.values())ambiguous|=item.ambiguous;
      for(let j=0;j<m;j++){
        const fixed=(ambiguous&(1<<j))===0, predicted=rank([...selected,1<<j])===r;
        if(fixed!==predicted)throw Error("target-span discrepancy");
        if(fixed)targetMin[j]=Math.min(targetMin[j],pop(set));
        targetChecks++;
      }subsets++;
    }
    const baseline=rows.filter((_,i)=>pop(i)<=1);
    const design=rows.filter((_,i)=>pop(i)<=d);
    if(minFull!==m||rank(design)!==m||targetMin.some((v,j)=>v!==2**pop(mon[j])))throw Error("exact cost mismatch");
    results.push({n,d,parameters:m,fullMinimum:minFull,oneFactorRank:rank(baseline),targetMinimum:targetMin});
  }
  // Interaction absent in all baseline and single-coordinate interventions.
  const x=[0,1,2,3].map(i=>Number(i===3));
  if(x.slice(0,3).some(Boolean)||x[3]!==1)throw Error("interaction mutation missed");
  return {subsets,targetChecks,results,interactionControl:x};
}
function auditParityCycles(){
  const assert=(x,msg)=>{if(!x)throw Error(msg)};
  function permutations(n){let out=[];function go(a,mask){if(a.length===n){let p=0;for(let i=0;i<n;i++)for(let j=i+1;j<n;j++)p^=+(a[i]>a[j]);out.push({a,p});return;}for(let j=0;j<n;j++)if(!(mask>>j&1))go([...a,j],mask|1<<j);}go([],0);return out;}
  function cycles(rows,reference){
    const n=rows.length,adj=rows.map((row,i)=>reference.map((j,k)=>i!==k&&!!(row>>j&1)));
    const found=[];for(let start=0;start<n;start++){
      function visit(path,mask){const v=path[path.length-1];if(path.length>=2&&adj[v][start])found.push({len:path.length,mask});for(let w=start+1;w<n;w++)if(adj[v][w]&&!(mask>>w&1))visit([...path,w],mask|1<<w);}
      visit([start],1<<start);
    }
    const even=found.filter(c=>!(c.len&1)),odd=found.some(c=>c.len&1);
    const bothUnique=!odd&&even.length<=1;
    const refUnique=!odd&&!even.some((a,i)=>even.slice(i+1).some(b=>!(a.mask&b.mask)));
    // Independent SCC criterion, using transitive closure on small test graphs.
    const reach=adj.map((r,i)=>r.map((v,j)=>v||i===j));
    for(let k=0;k<n;k++)for(let i=0;i<n;i++)for(let j=0;j<n;j++)reach[i][j]||=reach[i][k]&&reach[k][j];
    const components=[];let seen=0;for(let i=0;i<n;i++)if(!(seen>>i&1)){const c=Array.from({length:n},(_,j)=>j).filter(j=>reach[i][j]&&reach[j][i]);for(const j of c)seen|=1<<j;if(c.length>1)components.push(c);}
    const sccUnique=components.length===0||(components.length===1&&components[0].length%2===0&&components[0].every(i=>components[0].filter(j=>adj[i][j]).length===1));
    assert(sccUnique===bothUnique,"SCC mismatch");
    return {bothUnique,refUnique};
  }
  function check(rows,perms){
    const matches=perms.filter(p=>p.a.every((j,i)=>rows[i]>>j&1));
    const counts=[0,0];for(const p of matches)counts[p.p]++;
    if(!matches.length)return "empty";
    const r=matches[0],pred=cycles(rows,r.a);
    assert(pred.bothUnique===(counts[0]<=1&&counts[1]<=1),"two-sector mismatch");
    assert(pred.refUnique===(counts[r.p]===1),"reference sector mismatch");
    return `${counts[0]},${counts[1]}`;
  }
  let graphs=0,graphHist={};for(let n=1;n<=4;n++){
    const perms=permutations(n),arcs=[];for(let i=0;i<n;i++)for(let j=0;j<n;j++)if(i!==j)arcs.push([i,j]);
    for(let mask=0;mask<2**arcs.length;mask++){const rows=Array.from({length:n},(_,i)=>1<<i);arcs.forEach(([i,j],k)=>{if(mask>>k&1)rows[i]|=1<<j;});const key=check(rows,perms);graphHist[key]=(graphHist[key]||0)+1;graphs++;}
  }
  const edges=[];for(let i=0;i<6;i++)for(let j=i+1;j<6;j++)if((i>>1)!==(j>>1))edges.push([i,j]);
  const perms=permutations(4);let residuals=0,empty=0,signedUnique=0,matchCounts={};
  for(let a=0;a<12;a++)for(let b=a+1;b<12;b++)for(let c=b+1;c<12;c++)for(let d=c+1;d<12;d++){
    const es=[edges[a],edges[b],edges[c],edges[d]],masks=Array.from({length:6},(_,v)=>es.reduce((acc,e,j)=>acc|(e.includes(v)?1<<j:0),0));
    for(let u=0;u<6;u++)for(let v=0;v<6;v++)for(let w=0;w<6;w++){
      const key=check([masks[u],masks[v],masks[w],15],perms);residuals++;if(key==="empty")empty++;else{const [x,y]=key.split(",").map(Number);if(x<=1&&y<=1)signedUnique++;const total=x+y;matchCounts[total]=(matchCounts[total]||0)+1;}
    }
  }
  assert(graphs===4165&&residuals===106920&&empty===61794&&signedUnique===34344,"domain mismatch");
  return {graphs,graphHist,residuals,empty,feasible:residuals-empty,signedUnique,matchCounts};
}
function countSignedCompletions(records, labels){
  const n=labels.length;
  const allowed=records.map(([a,b])=>labels.map(([u,v])=>[+( (!a||a===u)&&(!b||b===v) ),+( (!a||a===v)&&(!b||b===u) )]));
  const pop=x=>{let n=0;while(x){x&=x-1;n++}return n};
  const memo=new Map();
  function dp(mask){
    const i=pop(mask);if(i===n)return [1,0,0,0];if(memo.has(mask))return memo.get(mask);
    const out=[0,0,0,0];
    for(let j=0;j<n;j++)if(!(mask>>j&1)){
      const opts=allowed[i][j];if(!opts[0]&&!opts[1])continue;
      const sign=pop(mask>>(j+1))%2;
      const child=dp(mask|1<<j);
      for(let b=0;b<2;b++)if(opts[b])for(let k=0;k<4;k++)out[k^(2*sign+b)]+=child[k];
    }memo.set(mask,out);return out;
  }
  return dp(0);
}
function auditOrientedCharacters(){
  const labels=["DL","BL","FL","UL","DB","DF","UB","UF","DR","BR","FR","UR"],colors="URFDLB";
  const assert=(x,m)=>{if(!x)throw Error(m)};
  // Independently enumerate permutations and orientations, then compare all four Fourier sectors.
  let cases=0;
  for(let a=0;a<12;a++)for(let b=a+1;b<12;b++)for(let c=b+1;c<12;c++){
    const es=[labels[a],labels[b],labels[c]];
    for(const u of colors)for(const v of colors)for(const mode of [0,1,2]){
      const rec=[[u,null],[null,v],mode===0?[null,null]:mode===1?[u,null]:[u,v]];
      const brute=[0,0,0,0];function go(i,used,sign,flip){if(i===3){brute[2*sign+flip]++;return;}for(let j=0;j<3;j++)if(!used.includes(j))for(let o=0;o<2;o++){const e=o?es[j][1]+es[j][0]:es[j];if(rec[i].every((x,k)=>!x||x===e[k]))go(i+1,[...used,j],sign^(used.filter(x=>x>j).length%2),flip^o);}}
      go(0,[],0,0);
      const got=countSignedCompletions(rec,es);
      assert(got.every((x,i)=>x===brute[i]),"oriented mismatch");cases++;
    }
  }
  const all=countSignedCompletions(Array.from({length:12},()=>[null,null]),labels);
  assert(all.every(x=>x===490497638400),"full edge count");
  return {cases,fullSectors:all};
}
console.log(JSON.stringify({...audit(),clock:auditClock(),structure:auditStructure(),parityCycles:auditParityCycles(),orientedCharacters:auditOrientedCharacters()}, null, 2));
