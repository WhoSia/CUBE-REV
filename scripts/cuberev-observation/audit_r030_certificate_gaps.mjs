import { readFileSync } from 'node:fs';
import { gunzipSync } from 'node:zlib';
import { createHash } from 'node:crypto';
function loadPinnedCertificate(){
  const packed=Buffer.from(readFileSync(new URL('../../formal/029/certificate_blobs/upper-policy-certificate.json.gz.b64',import.meta.url),'utf8').trim(),'base64');
  const plain=gunzipSync(packed),sha=b=>createHash('sha256').update(b).digest('hex');
  if(sha(packed)!=='d9dd5f9c283b9d79a86bcf00cefc51e013bc8d20a1c8c34077316a1c81e3f1d3'||sha(plain)!=='80f334520d288b09d0ad2398b596e8910515d312b342cf07ceeb5e4107922227')throw Error('pinned certificate hash mismatch');
  return JSON.parse(plain.toString('utf8'));
}
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
function auditFrozenLeaves(cert){
  const labels=["DL","BL","FL","UL","DB","DF","UB","UF","DR","BR","FR","UR"];
  const must=(x,msg)=>{if(!x)throw Error(msg)};
  let nodes=0,leaves=0,assignments=0,orientationEssential=0,signEssential=0,rawMatchingAmbiguity=0;
  const hist={},byBlank={};
  must(cert.representatives.length===52,"root count");
  for(const e of cert.representatives){
    const record=[...e.prefix].map(c=>[c,null]);record.push([null,null]);
    const seen=new Set();let rootMass=0;
    function visit(i,depth){
      must(Number.isInteger(i)&&i>=0&&i<e.nodes.length&&!seen.has(i)&&depth<=8,"tree");seen.add(i);nodes++;
      const node=e.nodes[i];
      if(node[0]==="leaf"){
        leaves++;
        const [ee,eo,oe,oo]=countSignedCompletions(record,labels);
        const actual=ee+oe;must(actual>=1&&ee<=1&&oe<=1,"terminal parity");
        const blank=record.filter(([a,b])=>!a&&!b).length;
        const key=`${blank},${ee},${eo},${oe},${oo}`;
        hist[key]=(hist[key]||0)+1;
        const lastReads=record[11].filter(Boolean).length;
        byBlank[lastReads]=(byBlank[lastReads]||0)+1;
        if(actual===2)signEssential++;
        if(blank===0&&(ee+eo>1||oe+oo>1)){orientationEssential++;rawMatchingAmbiguity++;}
        rootMass+=actual;assignments+=actual;return;
      }
      must(depth<8,"budget");
      if(node[0]==="repeat"){visit(node[1],depth+1);return}
      must(node[0]==="read"&&Number.isInteger(node[1])&&node[1]>=0&&node[1]<13,"read");
      const q=node[1],r=q<11?q:11,col=q===11?0:1,old=record[r][col];
      for(const [c,j] of Object.entries(node[2])){must(!old||old===c,"conflicting repeat");record[r][col]=c;visit(j,depth+1);}
      record[r][col]=old;
    }
    const expected=countSignedCompletions(record,labels);visit(0,0);
    must(seen.size===e.nodes.length&&rootMass===expected[0]+expected[2],"root mass");
  }
  must(nodes===141097&&leaves===73962&&assignments===144736,"pinned totals");
  return {nodes,leaves,assignments,signEssential,orientationEssential,rawMatchingAmbiguity,byLastEdgeReads:byBlank,sectorHistogram:hist};
}
function auditPrefixPolymatroid(){
  const edges=[];for(let i=0;i<6;i++)for(let j=i+1;j<6;j++)if((i>>1)!==(j>>1))edges.push([i,j]);
  const pow=Array.from({length:6},(_,i)=>5**i),vec=x=>pow.map(p=>Math.floor(x/p)%5);
  let s=new Set([0]);
  for(const [u,v] of edges){const next=new Set(s);for(const x of s){next.add(x+pow[u]);next.add(x+pow[v]);}s=next;}
  const rank=Array.from({length:64},(_,mask)=>edges.filter(([u,v])=>((mask>>u)|(mask>>v))&1).length);
  let checks=0;for(let a=0;a<64;a++)for(let b=0;b<64;b++){if(rank[a]+rank[b]<rank[a|b]+rank[a&b])throw Error("submodular");checks++;}
  let h=Array(13).fill(0),dp=Array(13).fill(0);
  for(let x=0;x<5**6;x++){let v=vec(x),k=v.reduce((a,b)=>a+b,0);const ok=Array.from({length:64},(_,m)=>v.reduce((t,a,i)=>t+(m>>i&1?a:0),0)).every((a,m)=>a<=rank[m]);if(ok!==s.has(x))throw Error("Hall support mismatch");if(ok)h[k]++;if(s.has(x))dp[k]++;}
  let forest=Array(6).fill(0);for(let mask=0;mask<1<<12;mask++){let p=Array.from({length:6},(_,i)=>i),root=i=>p[i]===i?i:root(p[i]),k=0,valid=true;for(let j=0;j<12;j++)if(mask>>j&1){const [u,v]=edges[j],a=root(u),b=root(v);if(a===b){valid=false;break}p[a]=b;k++;}if(valid)forest[k]++;}
  if(forest.reduce((a,b)=>a+b,0)!==h[12]||h[11]!==1362)throw Error("forest count");
  return {submodularChecks:checks,latticeCandidates:5**6,allPrefixSupport:h,forestCoefficients:forest,total:s.size};
}
function auditParityPolytope(){
 const labels=["DL","BL","FL","UL","DB","DF","UB","UF","DR","BR","FR","UR"],colors="URFDLB",p=Array.from({length:6},(_,i)=>5**i),vec=x=>p.map(q=>Math.floor(x/q)%5),encode=a=>a.reduce((s,x,i)=>s+x*p[i],0);
 const fibers=new Map(), orientations=[];
 for(let m=0;m<4096;m++){let x=0,b=0;let adj=Array.from({length:6},()=>[]);for(let i=0;i<12;i++){const f=m>>i&1,u=colors.indexOf(labels[i][f]),v=colors.indexOf(labels[i][1-f]);x+=p[u];b^=f;adj[v].push(u)}let c=fibers.get(x)||[0,0];c[b]++;fibers.set(x,c);orientations.push({x,b,adj});}
 function oddCycle(adj){for(let i=0;i<6;i++){function walk(v,seen,n){for(const w of adj[v]){if(w===i&&n>=3&&n%2===1)return true;if(!(seen>>w&1)&&walk(w,seen|1<<w,n+1))return true}return false}if(walk(i,1<<i,1))return true}return false}
 let h={evenOnly:0,oddOnly:0,both:0},oddCycleCount=0;for(const [x,c] of fibers){h[c[0]&&c[1]?"both":c[0]?"evenOnly":"oddOnly"]++}
 for(const {x,adj} of orientations){const odd=oddCycle(adj);if(odd)oddCycleCount++;if(odd!==fibers.get(x).every(Boolean))throw Error("odd cycle criterion")}
 function exchange(set){const rows=[...set].map(x=>[x,vec(x)]);let failures=0,witness=null,checks=0;for(const [x,a] of rows)for(const [y,b] of rows)for(let i=0;i<6;i++)if(a[i]>b[i]){checks++;let options=[];for(let j=0;j<6;j++)if(a[j]<b[j])options.push({j,x:vec(x-p[i]+p[j]),y:vec(y+p[i]-p[j]),inX:set.has(x-p[i]+p[j]),inY:set.has(y+p[i]-p[j])});if(!options.some(o=>o.inX)){failures++;if(!witness)witness={x:a,y:b,i,options};}}return {checks,failures,witness}}
 const even=new Set([...fibers].filter(([x,c])=>c[0]).map(([x])=>x)),odd=new Set([...fibers].filter(([x,c])=>c[1]).map(([x])=>x));
 const result={h,oddCycleCount,even:exchange(even),odd:exchange(odd),unrestricted:exchange(new Set(fibers.keys()))};
 for(const t of [result.even,result.odd]){const w=t.witness;w.counts={x:fibers.get(encode(w.x)),y:fibers.get(encode(w.y)),alternatives:w.options.map(o=>fibers.get(encode(o.x))||[0,0])}}
 if(h.evenOnly!==222||h.oddOnly!==216||h.both!==645||result.unrestricted.failures!==0||!result.even.failures||!result.odd.failures)throw Error("parity/exchange regression");
 return result
}
function auditParityHoles(){
 const labels=["DL","BL","FL","UL","DB","DF","UB","UF","DR","BR","FR","UR"],colors="URFDLB",p=Array.from({length:6},(_,i)=>5**i),vec=x=>p.map(q=>Math.floor(x/q)%5),enc=a=>a.reduce((s,x,i)=>s+x*p[i],0),fibers=new Map();
 for(let m=0;m<4096;m++){let x=0,b=0;for(let i=0;i<12;i++){let f=m>>i&1;x+=p[colors.indexOf(labels[i][f])];b^=f}let h=fibers.get(x)||[0,0];h[b]++;fibers.set(x,h)}
 const results=[];
 for(let b=0;b<2;b++){
   const keys=[...fibers].filter(([x,c])=>c[b]).map(([x])=>x),set=new Set(keys),rows=keys.map(x=>[x,vec(x)]),holes=new Set();let witness=null;
   for(let i=0;i<rows.length;i++)for(let j=i+1;j<rows.length;j++){const [x,a]=rows[i],[y,z]=rows[j];if(!a.every((v,k)=>(v+z[k])%2===0))continue;const m=(x+y)/2;if(!set.has(m)){if(!fibers.has(m))throw Error("unrestricted convex hole");holes.add(m);if(!witness)witness={a,c:z,midpoint:vec(m),counts:[fibers.get(x),fibers.get(y),fibers.get(m)]}}}
   results.push({parity:b,midpointHoles:holes.size,witness});
 }
 // Rank inequalities cannot distinguish the legal even support from full zonotope
 // if all rank maxima coincide (checked, not assumed).
 const max=(set,mask)=>Math.max(...set.map(x=>vec(x).reduce((s,n,i)=>s+((mask>>i&1)?n:0),0)));
 const all=[...fibers.keys()],rankGaps=[];
 for(let b=0;b<2;b++){const sector=all.filter(x=>fibers.get(x)[b]);let gaps=[];for(let m=0;m<64;m++){const a=max(all,m),v=max(sector,m);if(a!==v)gaps.push({mask:m,unrestricted:a,sector:v})}rankGaps.push(gaps)}
 return {results,rankGaps};
}
function auditRankBlindness(){
 const labels=["DL","BL","FL","UL","DB","DF","UB","UF","DR","BR","FR","UR"],colors="URFDLB",p=Array.from({length:6},(_,i)=>5**i),vec=x=>p.map(q=>Math.floor(x/q)%5);
 let vertices=[0,0],best=null;
 for(let m=0;m<4096;m++){let x=0,b=0;const adj=Array.from({length:6},()=>[]),deg=Array(6).fill(0);for(let i=0;i<12;i++){const f=m>>i&1,u=colors.indexOf(labels[i][f]),v=colors.indexOf(labels[i][1-f]);x+=p[u];b^=f;adj[v].push(u);deg[u]++}const queue=deg.flatMap((d,i)=>d===0?[i]:[]),order=[];for(let i=0;i<queue.length;i++){let v=queue[i];order.push(v);for(const u of adj[v])if(--deg[u]===0)queue.push(u)}
 if(order.length!==6)continue;vertices[b]++;if(b===1&&!best){const w=Array(6);order.forEach((v,i)=>w[v]=i);best={histogram:vec(x),weights:w,orientationMask:m,score:vec(x).reduce((s,v,i)=>s+v*w[i],0)}}}
 const scores=[-1,-1];for(let m=0;m<4096;m++){let x=0,b=0;for(let i=0;i<12;i++){const f=m>>i&1;x+=p[colors.indexOf(labels[i][f])];b^=f}scores[b]=Math.max(scores[b],vec(x).reduce((s,v,i)=>s+v*best.weights[i],0))}
 if(scores[1]!==best.score||scores[0]>=scores[1])throw Error("weighted objective not separated");
 return {vertices,weightedWitness:best,sectorMaxima:scores}
}
function auditParitySupportFunction(){
 const labels=["DL","BL","FL","UL","DB","DF","UB","UF","DR","BR","FR","UR"],colors="URFDLB",edges=labels.map(l=>[colors.indexOf(l[0]),colors.indexOf(l[1])]),p=Array.from({length:6},(_,i)=>5**i);
 const masks=Array.from({length:4096},(_,m)=>{let h=0,b=0,adj=Array.from({length:6},()=>[]),deg=Array(6).fill(0);for(let i=0;i<12;i++){const f=m>>i&1,u=edges[i][f],v=edges[i][1-f];h+=p[u];b^=f;adj[v].push(u);deg[u]++}let q=deg.flatMap((v,i)=>v===0?[i]:[]);for(let i=0;i<q.length;i++)for(const j of adj[q[i]])if(--deg[j]===0)q.push(j);return {h,b,acyclic:q.length===6}});
 const fibers=new Map();for(const {h,b,acyclic} of masks){const a=fibers.get(h)||{count:[0,0],vertex:false};a.count[b]++;a.vertex||=acyclic;fibers.set(h,a)}
 let exclusiveNonvertex=[0,0],vertices=[0,0];for(const {count,vertex} of fibers.values()){if(vertex&&count[0]+count[1]!==1)throw Error("vertex fiber");if(vertex)vertices[count[1]?1:0]++;if(!vertex&&!(count[0]&&count[1]))exclusiveNonvertex[count[1]?1:0]++}
 let checks=0;
 for(let code=0;code<3**6;code++){let w=Array.from({length:6},(_,i)=>Math.floor(code/3**i)%3-1);let best=0,b=0,gap=Infinity;for(const [u,v] of edges){best+=Math.max(w[u],w[v]);b^=+(w[v]>w[u]);gap=Math.min(gap,Math.abs(w[u]-w[v]))}const expected=[best-(b===0?0:gap),best-(b===1?0:gap)],actual=[-Infinity,-Infinity];for(const {h,b:k} of masks){let score=0;for(let i=0;i<6;i++)score+=w[i]*(Math.floor(h/p[i])%5);actual[k]=Math.max(actual[k],score)}if(expected.some((x,i)=>x!==actual[i]))throw Error("support function mismatch");checks++}
 if(vertices[0]!==210||vertices[1]!==216||exclusiveNonvertex[0]!==12||exclusiveNonvertex[1]!==0)throw Error("vertex classification");
 return {vertices,exclusiveNonvertex,weightVectors:checks};
}
function auditParityExchanges(){
 const labels=["DL","BL","FL","UL","DB","DF","UB","UF","DR","BR","FR","UR"],colors="URFDLB",p=Array.from({length:6},(_,i)=>5**i),vec=x=>p.map(q=>Math.floor(x/q)%5),orient=[],sets=[new Set(),new Set()];
 for(let m=0;m<4096;m++){let x=0,b=0,adj=Array.from({length:6},()=>[]);for(let i=0;i<12;i++){const f=m>>i&1,u=colors.indexOf(labels[i][f]),v=colors.indexOf(labels[i][1-f]);x+=p[u];b^=f;adj[v].push([u,1<<i])}sets[b].add(x);orient.push({m,x,b,adj})}
 let tests=0,exactPositive=0,liftFP=0,liftFN=0,evenPathFN=0,liftFPWitness=null,liftFNWitness=null,pathFNWitness=null;
 for(const {m,x,b,adj} of orient){
   const counts=vec(x),oddCycles=new Set();
   for(let s=0;s<6;s++){function visit(v,seen,used,len){for(const [u,edge] of adj[v]){if(u===s&&len>=2&&(len+1)%2===1)oddCycles.add(used|edge);else if(!(seen>>u&1))visit(u,seen|1<<u,used|edge,len+1)}}visit(s,1<<s,0,0)}
   for(let j=0;j<6;j++)for(let i=0;i<6;i++)if(i!==j&&counts[i]>0&&counts[j]<4){
      let hasEvenPath=false,hasCorrectedPath=false;
      function path(v,seen,used,len){if(v===i){if(len%2===0)hasEvenPath=true;else if([...oddCycles].some(c=>!(c&used)))hasCorrectedPath=true;return}for(const [u,e] of adj[v])if(!(seen>>u&1))path(u,seen|1<<u,used|e,len+1)}
      path(j,1<<j,0,0);
      const reach=new Set([2*j]),queue=[2*j];for(let k=0;k<queue.length;k++){const s=queue[k];for(const [u] of adj[s>>1]){let t=2*u+((s&1)^1);if(!reach.has(t)){reach.add(t);queue.push(t)}}}
      const lift=reach.has(2*i),actual=sets[b].has(x-p[i]+p[j]),pred=hasEvenPath||hasCorrectedPath;tests++;if(actual)exactPositive++;if(pred!==actual)throw Error(JSON.stringify({m,i,j,b,actual,pred}));
      const witness={orientationMask:m,parity:b,from:colors[i],to:colors[j],histogram:counts,target:vec(x-p[i]+p[j]),adj:adj.map(a=>a.map(([u,e])=>[colors[u],Math.log2(e)]))};
      if(lift&&!actual){liftFP++;liftFPWitness??=witness}if(!lift&&actual){liftFN++;liftFNWitness??=witness}if(!hasEvenPath&&actual){evenPathFN++;pathFNWitness??=witness}
   }
 }
 if(tests!==108384||exactPositive!==93156||!liftFP||!liftFN)throw Error("exchange census");
 return {tests,exactPositive,liftFP,liftFN,evenPathFN,liftFPWitness,liftFNWitness,pathFNWitness};
}
function auditGraphParityClassification(){
 const tally={},examples={};let graphCount=0,sectorCount=0;
 for(let n=2;n<=5;n++){
  const edges=[];for(let i=0;i<n;i++)for(let j=i+1;j<n;j++)edges.push([i,j]);const base=n,p=Array.from({length:n},(_,i)=>base**i);
  for(let mask=1;mask<2**edges.length;mask++){
   const es=edges.filter((_,i)=>mask>>i&1),m=es.length,sets=[new Set(),new Set()];
   for(let o=0;o<2**m;o++){let x=0,b=0;for(let i=0;i<m;i++){let k=o>>i&1;x+=p[es[i][k]];b^=k}sets[b].add(x)}
   function exchange(set){let rows=[...set].map(x=>[x,p.map(q=>Math.floor(x/q)%base)]);for(const [x,a] of rows)for(const [,b] of rows)for(let i=0;i<n;i++)if(a[i]>b[i]&&!a.some((v,j)=>v<b[j]&&set.has(x-p[i]+p[j])))return false;return true}
   let valid=sets.map(exchange),num=valid.filter(Boolean).length;
   const touching=m===2&&es[0].some(v=>es[1].includes(v));const expected=m===1?2:touching?1:0;
   if(num!==expected)throw Error(JSON.stringify({n,es,valid,expected}));
   const key=m===1?"oneEdge":m===2?(touching?"twoAdjacent":"twoDisjoint"):"threeOrMore";tally[key]=(tally[key]||0)+1;examples[key]??={n,es,valid};graphCount++;sectorCount+=2;
  }
 }
 return {graphCount,sectorCount,tally,examples};
}
function auditBoundedExchange(){
  const colors="URFDLB",pow=Array.from({length:6},(_,i)=>5**i),vec=x=>pow.map(p=>Math.floor(x/p)%5);
  const families=[{name:"edge",pieces:["DL","BL","FL","UL","DB","DF","UB","UF","DR","BR","FR","UR"],mod:2},{name:"corner",pieces:["UFR","URB","ULF","UBL","DRF","DBR","DFL","DLB"],mod:3}];
  const results=[];
  for(const {name,pieces,mod} of families){
    const counts=new Map();
    function gen(i,key,charge){if(i===pieces.length){let a=counts.get(key)||Array(mod).fill(0);a[charge]++;counts.set(key,a);return;}
      for(let j=0;j<mod;j++)gen(i+1,key+pow[colors.indexOf(pieces[i][j])],(charge+j)%mod);}
    gen(0,0,0);
    const sectors=[];
    for(let b=0;b<mod;b++){
      const keys=[...counts].filter(([,a])=>a[b]).map(([k])=>k),set=new Set(keys),rows=keys.map(k=>({k,v:vec(k)})),steps=Array(mod+1).fill(0),witnesses={};
      let obligations=0;
      for(const {k:x,v:a} of rows)for(const {k:y,v:c} of rows){
        if(x===y)continue;
        let plus=[],minus=[],delta=a.map((v,i)=>v-c[i]);for(let i=0;i<6;i++){if(delta[i]>0)plus.push(i);if(delta[i]<0)minus.push(i)}
        for(const i of plus){
          obligations++;
          function rec(depth,limit,d,initial){
            if(depth>0&&set.has(x+d)&&set.has(y-d))return d;
            if(depth===limit)return null;
            for(const u of initial?[i]:plus)if(delta[u]>0)for(const v of minus)if(delta[v]<0){
              delta[u]--;delta[v]++;const ans=rec(depth+1,limit,d-pow[u]+pow[v],false);delta[u]++;delta[v]--;if(ans!==null)return ans;
            }return null;
          }
          let found=false;
          for(let lim=1;lim<=mod;lim++){const d=rec(0,lim,0,true);if(d!==null){steps[lim]++;witnesses[lim]??={x:a,y:c,excess:colors[i],xNext:vec(x+d),yNext:vec(y-d)};found=true;break}}
          if(!found)throw Error(`bounded exchange failed ${name} ${b} ${x} ${y} ${i}`);
        }
      }sectors.push({parity:b,support:keys.length,obligations,minTransfers:steps.slice(1),witnesses});
    }let hist={};for(const a of counts.values()){const k=a.map(n=>+(n>0)).join("");hist[k]=(hist[k]||0)+1}
    results.push({name,unrestricted:counts.size,sectorSupport:hist,sectors});
  }
  return results;
}
function auditSignCertificates(){
 const types=[["edge",["DL","BL","FL","UL","DB","DF","UB","UF","DR","BR","FR","UR"],2],["corner",["UFR","URB","ULF","UBL","DRF","DBR","DFL","DLB"],3]];
 const out=[];
 for(const [name,labels,m] of types){
   const n=labels.length;for(let d=1;d<m;d++){const unique=new Set();for(const l of labels)for(let j=0;j<m;j++){const key=l[j]+l[(j+d)%m];if(unique.has(key))throw Error("two colors not unique");unique.add(key);}}
   let hist={},min=2*n,example=null,checked=0,certCount=0;
   for(let blank=-1;blank<n;blank++){
     const used=new Set(blank<0?[]:labels[blank]);const singles=[];
     function run(i){
       if(i===n){
         const cost=2*n-singles.length-(blank>=0?2:0);
         const remaining=[...singles.map(([p])=>p),...(blank<0?[]:[blank])].sort((a,b)=>a-b);
         const req=new Map(singles);
         function oddCompletion(k,used,parity,twist){
           if(k===remaining.length)return parity===1&&twist===0;
           const pos=remaining[k];for(let j=0;j<remaining.length;j++)if(!(used>>j&1)){let lab=remaining[j],side=req.get(pos);
             for(let t=0;t<m;t++)if(side===undefined||labels[lab][(side+t)%m]===labels[pos][side]){
               let q=0;for(let z=j+1;z<remaining.length;z++)q^=used>>z&1;
               if(oddCompletion(k+1,used|1<<j,parity^q,(twist+t)%m))return true;
             }
           }return false;
         }
         checked++;let a=hist[cost]??[0,0];if(!oddCompletion(0,0,0,0)){a[1]++;certCount++;if(cost<min||!example){min=cost;example={blank,singles:singles.map(([i,s])=>({piece:labels[i],side:s,color:labels[i][s]})),full:labels.filter((_,i)=>i!==blank&&!req.has(i))}}}else a[0]++;hist[cost]=a;
         return;
       }
       if(i===blank){run(i+1);return;}
       run(i+1);
       for(let j=0;j<m;j++){const c=labels[i][j];if(used.has(c))continue;used.add(c);singles.push([i,j]);run(i+1);singles.pop();used.delete(c);}
     }run(0)
   }
   out.push({name,min,example,checked,certCount,hist});
 }
 if(out[0].min!==18||out[1].min!==11||out[1].hist[10][1]!==0)throw Error("certificate minima");
 return out;
}
function auditCornerSignMinimax(){
 const labels=["UFR","URB","ULF","UBL","DRF","DBR","DFL","DLB"],colors="URFDLB";
 const pos=labels.map(l=>Array.from(colors,c=>l.indexOf(c))),cm=Array.from(colors,(_,c)=>labels.reduce((a,l,i)=>a|(pos[i][c]>=0?1<<i:0),0));
 const pop=Array.from({length:256},(_,x)=>{let n=0;while(x){x&=x-1;n++}return n});
 const signCache=new Map(),depthCache=new Map();
 const key=(rows,mask,r)=>`${rows.join("")}:${mask}:${r}`;
 const swap=s=>((s&1)<<1)|((s&2)>>1);
 function signs(rows,mask,r){
  const k=key(rows,mask,r);if(signCache.has(k))return signCache.get(k);
  let s=0;
  if(!rows.length){const b=pop[mask];s=b>=2?3:b===1||r===0?1:0;}
  else{let j=mask&cm[rows[0]];while(j){const bit=j&-j;j^=bit;const l=31-Math.clz32(bit),child=signs(rows.slice(1),mask^bit,(r-pos[l][rows[0]]+3)%3);s|=pop[mask&(bit-1)]%2?swap(child):child;if(s===3)break;}}
  signCache.set(k,s);return s;
 }
 let calls=0;
 function depth(rows,mask,r){
  const k=key(rows,mask,r);if(depthCache.has(k))return depthCache.get(k);
  const s=signs(rows,mask,r);if(s!==3)return 0;
  calls++;
  let best=Infinity; const blanks=pop[mask]-rows.length;
  if(blanks){for(let j=0;j<3;j++){let worst=0;for(let c=0;c<6;c++){const next=[...rows,c].sort((a,b)=>a-b),nr=(r+j)%3;if(signs(next,mask,nr))worst=Math.max(worst,depth(next,mask,nr));if(worst+1>=best)break;}best=Math.min(best,worst+1);}}
  for(let i=0;i<rows.length;i++){
   if(i&&rows[i]===rows[i-1])continue;
   let j=mask&cm[rows[i]],worst=0;const rest=rows.slice(0,i).concat(rows.slice(i+1));
   while(j){const bit=j&-j;j^=bit;const l=31-Math.clz32(bit),nr=(r-pos[l][rows[i]]+3)%3;if(signs(rest,mask^bit,nr))worst=Math.max(worst,depth(rest,mask^bit,nr));if(worst+1>=best)break;}
   best=Math.min(best,worst+1);
  }
  if(!Number.isFinite(best))throw Error("no distinguishing action");depthCache.set(k,best);return best;
 }
 const result=depth([],255,0);
 const rootChoices=Array.from({length:3},(_,j)=>({side:j,cost:1+Math.max(...Array.from({length:6},(_,c)=>depth([c],255,j)))}));
 const scanMemo=new Map();
 function scan(rows,mask){const k=key(rows,mask,0);if(scanMemo.has(k))return scanMemo.get(k);if(signs(rows,mask,0)!==3)return 0;
  let best=Infinity;for(let i=0;i<rows.length;i++){if(i&&rows[i]===rows[i-1])continue;const rest=rows.slice(0,i).concat(rows.slice(i+1));let j=mask&cm[rows[i]],worst=0;while(j){const bit=j&-j;j^=bit;if(signs(rest,mask^bit,0))worst=Math.max(worst,scan(rest,mask^bit));}best=Math.min(best,1+worst);}scanMemo.set(k,best);return best;
 }
 let hist={},roots=0;function prefix(rows,min){if(rows.length===7){if(signs(rows,255,0)){let d=scan(rows,255);hist[d]=(hist[d]||0)+1;roots++;}return;}for(let c=min;c<6;c++)prefix([...rows,c],c);}prefix([],0);
 if(result!==13||rootChoices.some(x=>x.cost!==13)||roots!==642||hist[6]!==462)throw Error("sign minimax regression");
 return {result,rootChoices,calls,signCache:signCache.size,depthCache:depthCache.size,sevenPrefix:{roots,hist},scanCache:scanMemo.size};
}
function auditCornerGoals(){
 const labels=["UFR","URB","ULF","UBL","DRF","DBR","DFL","DLB"],colors="URFDLB";
 const index=labels.map(s=>Array.from(colors,c=>s.indexOf(c)));
 const pop=Array.from({length:256},(_,x)=>{let n=0;while(x){x&=x-1;n++}return n});
 const counts=new Map(),memo=new Map(),key=(a,m,r)=>`${a.join("")}:${m}:${r}`, cap=x=>Math.min(x,2);
 function count(a,m,r){
   const k=key(a,m,r);if(counts.has(k))return counts.get(k);let out=[0,0];
   if(!a.length){const b=pop[m];out=b>=2?[2,2]:b===1||r===0?[1,0]:[0,0];}
   else{for(let l=0;l<8;l++)if((m>>l&1)&&index[l][a[0]]>=0){
     const c=count(a.slice(1),m^(1<<l),(r-index[l][a[0]]+3)%3),p=pop[m&((1<<l)-1)]%2;
     out[0]=cap(out[0]+c[p]);out[1]=cap(out[1]+c[p^1]);}}
   counts.set(k,out);return out;
 }
 function actions(a,m,r){
   let out=[];
   if(pop[m]>a.length)for(let j=0;j<3;j++){const children=[];for(let c=0;c<6;c++){let b=[...a,c].sort((x,y)=>x-y),s=(r+j)%3;if(count(b,m,s).some(Boolean))children.push([b,m,s]);}out.push(children)}
   for(let i=0;i<a.length;i++)if(i===0||a[i]!==a[i-1]){const children=[],b=a.slice(0,i).concat(a.slice(i+1));for(let l=0;l<8;l++)if((m>>l&1)&&index[l][a[i]]>=0){let n=m^(1<<l),s=(r-index[l][a[i]]+3)%3;if(count(b,n,s).some(Boolean))children.push([b,n,s]);}out.push(children)}
   return out;
 }
 function depths(a,m,r){
   const k=key(a,m,r);if(memo.has(k))return memo.get(k);
   const c=count(a,m,r);if(c[0]+c[1]<=1)return [0,0,0];
   // sign, complete, complete with terminal (not early) sign
   let best=[c.every(Boolean)?Infinity:0,Infinity,c.every(x=>x<=1)?0:Infinity];
   for(const ch of actions(a,m,r)){
     const worst=[0,0,0];for(const s of ch){const d=depths(...s);for(let i=0;i<3;i++)worst[i]=Math.max(worst[i],d[i]+1);}
     for(let i=0;i<3;i++)best[i]=Math.min(best[i],worst[i]);
   }
   if(best.some(x=>!Number.isFinite(x)))throw Error("unresolved");
   memo.set(k,best);return best;
 }
 const root=depths([],255,0),hist={},examples={};
 for(const [k,d] of memo){const h=`${d[1]-d[0]},${d[1]-d[2]}`;hist[h]=(hist[h]||0)+1;examples[h]??={state:k,depths:d};}
 const feasibility=new Map();
 function feasible(a,m,r,h,t){
   const c=count(a,m,r),d=depths(a,m,r);
   if(c[0]+c[1]<=1)return true;
   if(d[0]>Math.max(h,0)||d[1]>t)return false;
   if(!c.every(Boolean))return d[1]<=t;
   const k=`${key(a,m,r)}:${h}:${t}`;if(feasibility.has(k))return feasibility.get(k);
   const ans=actions(a,m,r).some(ch=>ch.every(s=>feasible(...s,h-1,t-1)));feasibility.set(k,ans);return ans;
 }
 const deadlines=[];for(let h=root[0];h<=root[1];h++){let t=root[1];while(t<=16&&!feasible([],255,0,h,t))t++;deadlines.push({signBy:h,fullBy:t});}
 if(root.join(",")!=="13,13,12"||deadlines[0].fullBy!==13)throw Error("corner goal regression");
 return {root,deadlines,counts:counts.size,depths:memo.size,feasibility:feasibility.size,depthGapHistogram:hist,examples};
}
function auditEarlyCornerSign(){
 const labels=["UFR","URB","ULF","UBL","DRF","DBR","DFL","DLB"],colors="URFDLB",index=labels.map(s=>Array.from(colors,c=>s.indexOf(c)));
 const pop=Array.from({length:256},(_,x)=>{let n=0;while(x){x&=x-1;n++}return n});
 const counts=new Map(),memo=new Map(),key=(a,m,r)=>`${a.join("")}:${m}:${r}`;
 function count(a,m,r){const k=key(a,m,r);if(counts.has(k))return counts.get(k);let o=[0,0];if(!a.length){const b=pop[m];o=b>=2?[2,2]:b===1||r===0?[1,0]:[0,0]}else for(let l=0;l<8;l++)if(m>>l&1&&index[l][a[0]]>=0){const v=count(a.slice(1),m^(1<<l),(r-index[l][a[0]]+3)%3),p=pop[m&((1<<l)-1)]%2;for(let s=0;s<2;s++)o[s]=Math.min(2,o[s]+v[s^p])}counts.set(k,o);return o}
 function depth(a,m,r,s){if(count(a,m,r)[s]<=1)return 0;const k=key(a,m,r)+":"+s;if(memo.has(k))return memo.get(k);let best=Infinity;
  if(pop[m]>a.length)for(let j=0;j<3;j++){let worst=0;for(let c=0;c<6;c++){const b=[...a,c].sort((x,y)=>x-y),t=s^(a.filter(x=>x>c).length%2),nr=(r+j)%3;if(count(b,m,nr)[t])worst=Math.max(worst,1+depth(b,m,nr,t));}best=Math.min(best,worst)}
  for(let i=0;i<a.length;i++){if(i&&a[i]===a[i-1])continue;let worst=0,b=a.slice(0,i).concat(a.slice(i+1));for(let l=0;l<8;l++)if(m>>l&1&&index[l][a[i]]>=0){const nm=m^(1<<l),nr=(r-index[l][a[i]]+3)%3,t=s^((i+pop[m&((1<<l)-1)])%2);if(count(b,nm,nr)[t])worst=Math.max(worst,1+depth(b,nm,nr,t));}best=Math.min(best,worst)}
  if(!Number.isFinite(best))throw Error("unresolved");memo.set(k,best);return best;
 }
 const root=[depth([],255,0,0),depth([],255,0,1)];
 if(root.some(d=>d!==12))throw Error("early sign regression");
 return {root,countStates:counts.size,depthStates:memo.size};
}
function auditChargedCycleCertificates(){
 const types=[["edge",["DL","BL","FL","UL","DB","DF","UB","UF","DR","BR","FR","UR"],2],["corner",["UFR","URB","ULF","UBL","DRF","DBR","DFL","DLB"],3]],out=[];
 for(const [name,labels,m] of types){
  const n=labels.length, hist={},cyclesUsed={},witnesses={};let checked=0,min=2*n;
  for(let blank=-1;blank<n;blank++){
   const colors=new Set(blank<0?[]:labels[blank]),singles=[];
   function test(){
    const rows=[...singles.map(x=>x[0]),...(blank<0?[]:[blank])].sort((a,b)=>a-b),k=rows.length,req=new Map(singles),edges=rows.map((i)=>rows.map(j=>Array.from({length:m},(_,t)=>t).filter(t=>!req.has(i)||labels[j][(req.get(i)+t)%m]===labels[i][req.get(i)])));
    const byStart=Array.from({length:k},()=>[]); 
    for(let s=0;s<k;s++){
     const found=new Map();
     function walk(v,mask,len,r){
      for(let j=s;j<k;j++)for(const t of edges[v][j]){
       const nr=(r+t)%m;
       if(j===s){if(len===1&&nr===0)continue;const p=(len-1)%2,charge=p*m+nr,id=mask*2*m+charge;if(charge!==0&&!found.has(id))found.set(id,{mask,p,r:nr});}
       else if(!(mask>>j&1))walk(j,mask|1<<j,len+1,nr);
      }
     }walk(s,1<<s,1,0);byStart[s]=[...found.values()];
    }
    const memo=new Map();
    function target(mask,p,r){
     if(p===0&&r===0)return 0;
     if(!mask)return Infinity;
     const key=mask*2*m+p*m+r;if(memo.has(key))return memo.get(key);
     const bit=mask&-mask,s=31-Math.clz32(bit);let best=target(mask^bit,p,r);
     for(const c of byStart[s])if((mask&c.mask)===c.mask)best=Math.min(best,1+target(mask^c.mask,p^c.p,(r-c.r+m)%m));
     memo.set(key,best);return best;
    }
    const d=target((1<<k)-1,1,0);
    function brute(i,used,p,r){if(i===k)return p===1&&r===0;for(let j=0;j<k;j++)if(!(used>>j&1)){let q=0;for(let l=j+1;l<k;l++)q^=used>>l&1;for(const t of edges[i][j])if(brute(i+1,used|1<<j,p^q,(r+t)%m))return true;}return false}
    if(Number.isFinite(d)!==brute(0,0,0,0))throw Error("cycle mismatch");
    checked++;const cost=2*n-singles.length-(blank>=0?2:0),v=hist[cost]??[0,0];v[Number(!Number.isFinite(d))]++;hist[cost]=v;
    if(Number.isFinite(d)){cyclesUsed[d]=(cyclesUsed[d]||0)+1;witnesses[d]??={blank,singles:singles.map(([i,s])=>[labels[i],s,labels[i][s]])};}else min=Math.min(min,cost);
   }
   function gen(i){if(i===n){test();return;}if(i===blank){gen(i+1);return;}gen(i+1);for(let s=0;s<m;s++){let c=labels[i][s];if(colors.has(c))continue;colors.add(c);singles.push([i,s]);gen(i+1);singles.pop();colors.delete(c);}}gen(0);
  }
  out.push({name,checked,min,hist,cyclesUsed,witnesses});
 }
 if(out[0].checked!==14891||out[1].checked!==5873||out[0].cyclesUsed[1]!==782||out[1].cyclesUsed[2]!==312)throw Error("charged cycle regression");
 return out;
}
function auditGraphSignCertificateFormula(){
 let graphs=0,patterns=0,certificates=0,examples={};
 for(let v=2;v<=5;v++){
  const possible=[];for(let u=0;u<v;u++)for(let w=u+1;w<v;w++)possible.push([u,w]);
  for(let mask=1;mask<1<<possible.length;mask++){
   const E=possible.filter((_,i)=>mask>>i&1),n=E.length;
   const adj=Array.from({length:v},()=>[]);E.forEach(([u,w])=>{adj[u].push(w);adj[w].push(u)});
   const active=adj.filter(a=>a.length).length,side=Array(v).fill(-1);let bip=0;
   for(let u=0;u<v;u++)if(adj[u].length&&side[u]<0){let ok=true,q=[u];side[u]=0;for(let i=0;i<q.length;i++)for(const w of adj[q[i]]){if(side[w]<0){side[w]=side[q[i]]^1;q.push(w)}else if(side[w]===side[q[i]])ok=false;}if(ok)bip++;}
   const expected=2*n-active+Math.max(0,bip-1);let min=2*n;
   for(let blank=-1;blank<n;blank++){
    const used=new Set(blank<0?[]:E[blank]),singles=[];
    function inspect(){
     patterns++;
     const rows=[...singles.map(x=>x[0]),...(blank<0?[]:[blank])].sort((a,b)=>a-b),req=new Map(singles),k=rows.length;
     function odd(i,mask,p,r){if(i===k)return p===1&&r===0;for(let j=0;j<k;j++)if(!(mask>>j&1)){let q=0;for(let l=j+1;l<k;l++)q^=mask>>l&1;for(let t=0;t<2;t++)if(!req.has(rows[i])||E[rows[j]][(req.get(rows[i])+t)%2]===E[rows[i]][req.get(rows[i])])if(odd(i+1,mask|1<<j,p^q,r^t))return true;}return false}
     const next=Array(v).fill(-1);
     for(const [i,s] of singles)next[E[i][s]]=E[i][s^1];
     let evenCycle=false;
     for(let u=0;u<v;u++){let seen=new Map(),w=u,t=0;while(w>=0&&next[w]>=0&&!seen.has(w)){seen.set(w,t++);w=next[w]}if(seen.has(w)&&(t-seen.get(w))%2===0)evenCycle=true;}
     const ambiguous=odd(0,0,0,0);
     if(ambiguous!==evenCycle)throw Error(JSON.stringify({E,blank,singles,ambiguous,evenCycle}));
     if(!ambiguous){certificates++;min=Math.min(min,2*n-singles.length-(blank<0?0:2));}
    }
    function gen(i){if(i===n){inspect();return}if(i===blank){gen(i+1);return}gen(i+1);for(let s=0;s<2;s++){const c=E[i][s];if(used.has(c))continue;used.add(c);singles.push([i,s]);gen(i+1);singles.pop();used.delete(c)}}gen(0);
   }
   if(min!==expected)throw Error(JSON.stringify({E,expected,min,bip,active}));
   graphs++;examples[bip]??={E,n,active,bip,min};
  }
 }
 if(graphs!==1094||patterns!==312453||certificates!==306669)throw Error("graph census");
 return {graphs,patterns,certificates,examples};
}
function auditFullGraphCertificates(){
 let graphs=0,patterns=0,certs=0,gaps={};
 for(let v=2;v<=5;v++){
  const all=[];for(let u=0;u<v;u++)for(let w=u+1;w<v;w++)all.push([u,w]);
  for(let m=1;m<1<<all.length;m++){
   const E=all.filter((_,i)=>m>>i&1),n=E.length,adj=Array.from({length:v},()=>[]);
   for(const [u,w] of E){adj[u].push(w);adj[w].push(u)}
   let c=0,b=0,active=adj.filter(x=>x.length).length,side=Array(v).fill(-1);
   for(let u=0;u<v;u++)if(adj[u].length&&side[u]<0){c++;let q=[u],ok=true;side[u]=0;for(let i=0;i<q.length;i++)for(let w of adj[q[i]]){if(side[w]<0){side[w]=side[q[i]]^1;q.push(w)}else if(side[w]===side[q[i]])ok=false;}b+=+ok}
   let best=2*n;
   for(let blank=-1;blank<n;blank++){
    let used=new Set(blank<0?[]:E[blank]),single=[];
    function inspect(){
     patterns++;
     const next=Array(v).fill(-1);for(const [i,s] of single)next[E[i][s]]=E[i][s^1];
     let done=new Set(),even=0,odd=0;for(let u=0;u<v;u++){if(done.has(u))continue;let seen=new Map(),w=u,t=0;while(w>=0&&next[w]>=0&&!done.has(w)&&!seen.has(w)){seen.set(w,t++);w=next[w]}if(seen.has(w)){if((t-seen.get(w))%2)odd++;else even++}for(const x of seen.keys())done.add(x)}
     const pred=even===0&&odd<=(blank<0?1:0);
     let rows=[...single.map(x=>x[0]),...(blank<0?[]:[blank])].sort((a,b)=>a-b),req=new Map(single),k=rows.length,count=0;
     function direct(i,mask,r){if(count>=2)return;if(i===k){if(r===0)count++;return}for(let j=0;j<k;j++)if(!(mask>>j&1))for(let t=0;t<2;t++)if(!req.has(rows[i])||E[rows[j]][(req.get(rows[i])+t)%2]===E[rows[i]][req.get(rows[i])])direct(i+1,mask|1<<j,r^t)}
     direct(0,0,0);if(pred!==(count===1))throw Error("full cycle criterion");
     if(pred){certs++;best=Math.min(best,2*n-single.length-(blank<0?0:2))}
    }
    function gen(i){if(i===n){inspect();return}if(i===blank){gen(i+1);return}gen(i+1);for(let s=0;s<2;s++){let u=E[i][s];if(used.has(u))continue;used.add(u);single.push([i,s]);gen(i+1);single.pop();used.delete(u)}}gen(0)
   }
   const expected=2*n-active+c-1,sign=2*n-active+Math.max(0,b-1);if(best!==expected)throw Error(JSON.stringify({E,best,expected}));gaps[best-sign]=(gaps[best-sign]||0)+1;graphs++;
  }
 }
 if(graphs!==1094||patterns!==312453)throw Error("census");
 return {graphs,patterns,certs,gaps};
}
function solveGraphObservation(E,v){
 const n=E.length,N=1<<n,all=N-1,pop=new Uint8Array(N),cm=new Int32Array(v),side=Array.from({length:v},()=>new Uint8Array(n)),deg=new Uint8Array(v);
 if(n<1||n>12||v<2||v>7)throw Error("audit domain");
 for(let i=0;i<n;i++)for(let s=0;s<2;s++){const c=E[i][s];cm[c]|=1<<i;side[c][i]=s;deg[c]++}
 const gp=new Int32Array(v);let H=1;for(let c=0;c<v;c++){gp[c]=H;H*=deg[c]+1}
 const digits=new Uint8Array(H*v),sum=new Uint8Array(H);for(let h=0;h<H;h++)for(let c=0;c<v;c++){const q=Math.floor(h/gp[c])%(deg[c]+1);digits[h*v+c]=q;sum[h]+=q}
 const strides=new Int32Array(N*v),caps=new Uint8Array(N*v),off=new Int32Array(N+1);for(let m=0;m<N;m++){pop[m]=m?pop[m&(m-1)]+1:0;let p=1;for(let c=0;c<v;c++){let d=pop[m&cm[c]];caps[m*v+c]=d;strides[m*v+c]=p;p*=d+1;}off[m+1]=off[m]+p;}
 const C=new Uint8Array(2*off[N]),D=new Uint16Array(2*off[N]);let countStates=0,depthStates=0;
 function key(h,m,r){let z=off[m];for(let c=0;c<v;c++){let d=digits[h*v+c];if(d>caps[m*v+c])return -1;z+=d*strides[m*v+c]}return z*2+r;}
 function count(h,m,r){
  const b=pop[m]-sum[h];if(b<0)return 0;if(b>0)r=0;const k=key(h,m,r);if(k<0)return 0;if(C[k])return C[k]-1;
  countStates++;let a=0,d=0;
  if(!h){if(b>=2)a=d=2;else if(b===1||r===0)a=1;}
  else{let c=0;while(!digits[h*v+c])c++;for(let j=m&cm[c];j;){const bit=j&-j;j^=bit;const l=31-Math.clz32(bit),z=count(h-gp[c],m^bit,r^side[c][l]),p=pop[m&(bit-1)]&1;let x=z%3,y=Math.floor(z/3);if(p)[x,y]=[y,x];a=Math.min(2,a+x);d=Math.min(2,d+y);if(a===2&&d===2)break;}}
  C[k]=1+a+3*d;return a+3*d;
 }
 function depth(h,m,r){
  const b=pop[m]-sum[h];if(b>0)r=0;const z=count(h,m,r),a=z%3,d=Math.floor(z/3);if(a+d<=1)return 0;
  const k=key(h,m,r);if(D[k])return D[k]-1;depthStates++;const best=[a&&d?31:0,31,Math.max(a,d)<=1?0:31];
  function consider(ch){const w=[0,0,0];for(const [x,l,t] of ch)if(count(x,l,t)){const q=depth(x,l,t);for(let i=0;i<3;i++)w[i]=Math.max(w[i],1+((q>>(5*i))&31));}for(let i=0;i<3;i++)best[i]=Math.min(best[i],w[i]);}
  if(b>0)for(let s=0;s<(b===1?2:1);s++){const ch=[];for(let c=0;c<v;c++)if(digits[h*v+c]<caps[m*v+c])ch.push([h+gp[c],m,r^s]);consider(ch)}
  for(let c=0;c<v;c++)if(digits[h*v+c]){const ch=[];for(let j=m&cm[c];j;){let bit=j&-j;j^=bit;ch.push([h-gp[c],m^bit,r^side[c][31-Math.clz32(bit)]]);}consider(ch)}
  if(best.some(x=>x>=31))throw Error("unresolved");const q=best[0]|best[1]<<5|best[2]<<10;D[k]=q+1;return q;
 }
 const q=depth(0,all,0),depths=[q&31,(q>>5)&31,(q>>10)&31];
 let cover=99,strong=99;for(let s=0;s<1<<v;s++)if(E.every(([i,j])=>(s>>i&1)||(s>>j&1))){const k=s.toString(2).replace(/0/g,"").length;cover=Math.min(cover,k);if(E.some(([i,j])=>(s>>i&1)&&(s>>j&1)))strong=Math.min(strong,k)}
 const lower=Math.max(0,2*n-cover-1,2*n-strong);if(depths[0]<lower||depths[1]<depths[0])throw Error("cover lower violated");
 return {depths,cover,strong,lower,countStates,depthStates,tableBytes:C.byteLength+D.byteLength};
}
function auditGraphAdaptiveObjectives(){
 let graphs=0,gaps={};for(let v=2;v<=4;v++){const all=[];for(let i=0;i<v;i++)for(let j=i+1;j<v;j++)all.push([i,j]);for(let m=1;m<1<<all.length;m++){const E=all.filter((_,i)=>m>>i&1),r=solveGraphObservation(E,v),g=r.depths[0]-r.lower;gaps[g]=(gaps[g]||0)+1;graphs++;}}
 const families=[["star6",[[0,1],[0,2],[0,3],[0,4],[0,5],[0,6]]],["cycle6",[[0,1],[1,2],[2,3],[3,4],[4,5],[5,0]]],["path6",[[0,1],[1,2],[2,3],[3,4],[4,5],[5,6]]],["twoTriangles",[[0,1],[1,2],[2,0],[3,4],[4,5],[5,3]]],["matching3",[[0,1],[2,3],[4,5]]],["K23",[[0,2],[0,3],[0,4],[1,2],[1,3],[1,4]]]];
 const controls=families.map(([name,E])=>({name,...solveGraphObservation(E,1+Math.max(...E.flat()))}));
 const colors="URFDLB",labels=["DL","BL","FL","UL","DB","DF","UB","UF","DR","BR","FR","UR"],cube=solveGraphObservation(labels.map(l=>[...l].map(c=>colors.indexOf(c))),6);
 if(graphs!==71||gaps[0]!==71||cube.depths.join(",")!=="20,20,19")throw Error("adaptive census");
 return {graphs,gaps,controls,cube};
}
function auditK5Orbit(){
 const v=5,E=[];for(let i=0;i<v;i++)for(let j=i+1;j<v;j++)E.push([i,j]);const n=E.length,N=1<<n,all=N-1;
 const pop=Array.from({length:N},(_,x)=>{let p=0;while(x){x&=x-1;p++}return p});
 const cm=Array.from({length:v},(_,c)=>E.reduce((a,e,i)=>a|(e.includes(c)?1<<i:0),0)),pairs=new Map(E.map((e,i)=>[e.join(""),i]));
 const perms=[];function gen(a){if(a.length===v){let to=E.map(([u,w])=>pairs.get([a[u],a[w]].sort().join(""))),rev=E.map(([u,w])=>+(a[u]>a[w])),masks=new Int16Array(N),par=new Uint8Array(N);for(let m=1;m<N;m++){let b=m&-m,i=31-Math.clz32(b);masks[m]=masks[m^b]|1<<to[i];par[m]=par[m^b]^rev[i]}perms.push({a,masks,par});return}for(let c=0;c<v;c++)if(!a.includes(c))gen([...a,c])}gen([]);
 const key=(a,m,r)=>`${a}:${m}:${r}`,M=new Map(),C=new Map();let evaluated=0,oracleCalls=0;
 function counts(a,m,r){
  const b=pop[m]-a.length;if(b<0)return [0,0];if(b)r=0;const k=key(a,m,r);if(C.has(k))return C.get(k);oracleCalls++;let out=[0,0];
  function rec(i,left,p,t){if(out[0]===2&&out[1]===2)return;if(i===a.length){if(b>=2){out=[2,2];return}if(b===1||t===0)out[p]=Math.min(2,out[p]+1);return}
   for(let j=left&cm[+a[i]];j;){let bit=j&-j;j^=bit;let l=31-Math.clz32(bit);rec(i+1,left^bit,p^(pop[left&(bit-1)]&1),t^E[l].indexOf(+a[i]));}
  }rec(0,m,0,r);C.set(k,out);return out;
 }
 function depth(a,m,r){
  const b=pop[m]-a.length;if(b)r=0;const k=key(a,m,r);if(M.has(k))return M.get(k);const c=counts(a,m,r);if(c[0]+c[1]<=1)return [0,0,0];evaluated++;let best=[c.every(Boolean)?99:0,99,c.every(x=>x<=1)?0:99];
  function consider(children){const w=[0,0,0];for(const [aa,mm,rr] of children)if(counts(aa,mm,rr).some(Boolean)){const d=depth(aa,mm,rr);for(let i=0;i<3;i++)w[i]=Math.max(w[i],d[i]+1)}for(let i=0;i<3;i++)best[i]=Math.min(best[i],w[i]);}
  if(b)for(let s=0;s<(b===1?2:1);s++)consider(Array.from({length:v},(_,c)=>[[...a,String(c)].sort().join(""),m,r^s]));
  for(let i=0;i<a.length;i++)if(!i||a[i]!==a[i-1]){let ch=[];for(let j=m&cm[+a[i]];j;){let bit=j&-j;j^=bit;let l=31-Math.clz32(bit);ch.push([a.slice(0,i)+a.slice(i+1),m^bit,r^E[l].indexOf(+a[i])]);}consider(ch);}
  if(best.some(x=>x>=99))throw Error("unresolved");
  for(const {a:p,masks,par} of perms){const aa=[...a].map(x=>p[+x]).sort().join(""),kk=key(aa,masks[m],b?0:r^par[m]);if(M.has(kk)&&M.get(kk).join()!==best.join())throw Error("orbit mismatch");M.set(kk,best);}
  return best;
 }
 const result=depth("",all,0);if(result.join()!=="17,17,16"||evaluated!==2162||M.size!==175226)throw Error("K5 regression");return {result,evaluated,orbitStates:M.size,oracleCalls,automorphisms:perms.length};
}
function auditFiveVertexCover(){
 let hist={},counterexamples=[];for(let m=1;m<1024;m++){let E=[],k=0;for(let i=0;i<5;i++)for(let j=i+1;j<5;j++,k++)if(m>>k&1)E.push([i,j]);const r=solveGraphObservation(E,5),d=r.depths[0]-r.lower,g=r.depths[1]-r.depths[0],key=d+","+g;hist[key]=(hist[key]||0)+1;if(d||g)counterexamples.push({E,...r});}
 if(hist["0,0"]!==1022||hist["1,0"]!==1||counterexamples[0].E.length!==10||counterexamples[0].depths.join()!=="17,17,16")throw Error("five-vertex census");return {hist,counterexamples};
}
function generateK5LowerCertificate(){
 const E=[];for(let i=0;i<5;i++)for(let j=i+1;j<5;j++)E.push([i,j]);const n=10,N=1024,all=N-1;
 const pop=Array.from({length:N},(_,x)=>{let p=0;while(x){x&=x-1;p++}return p});
 const cm=Array.from({length:5},(_,c)=>E.reduce((a,e,i)=>a|(e.includes(c)?1<<i:0),0)),edgeIndex=new Map(E.map((e,i)=>[e.join(""),i]));
 const perms=[];function gen(a){if(a.length===5){let to=E.map(([u,w])=>edgeIndex.get([a[u],a[w]].sort().join(""))),rev=E.map(([u,w])=>+(a[u]>a[w])),masks=new Int16Array(N),par=new Uint8Array(N);for(let m=1;m<N;m++){let b=m&-m,i=31-Math.clz32(b);masks[m]=masks[m^b]|1<<to[i];par[m]=par[m^b]^rev[i]}perms.push({a,masks,par});return}for(let c=0;c<5;c++)if(!a.includes(c))gen([...a,c])}gen([]);
 const key=(a,m,r)=>`${a}:${m}:${r}`,cache=new Map(),normCache=new Map();
 function norm(a,m,r){const blank=pop[m]-a.length;if(blank>0)r=0;const k=key(a,m,r);if(normCache.has(k))return normCache.get(k);let best=k;
  for(const {a:p,masks,par} of perms){const kk=key([...a].map(x=>p[+x]).sort().join(""),masks[m],blank?0:r^par[m]);if(kk<best)best=kk;}normCache.set(k,best);return best}
 function decode(k){const [a,m,r]=k.split(":");return [a,+m,+r]}
 function actions(a,m,r){const b=pop[m]-a.length,out=[];
  if(b>0)for(let s=0;s<(b===1?2:1);s++)out.push(Array.from({length:5},(_,c)=>({reply:c,state:[[...a,String(c)].sort().join(""),m,r^s]})));
  for(let i=0;i<a.length;i++)if(!i||a[i]!==a[i-1]){let ch=[];for(let j=m&cm[+a[i]];j;){let bit=j&-j;j^=bit;let l=31-Math.clz32(bit);ch.push({reply:l,state:[a.slice(0,i)+a.slice(i+1),m^bit,r^E[l].indexOf(+a[i])]})}out.push(ch)}
  return out;
 }
 function witness(a,m,r){let result=[null,null],q=pop[m],labels=[],twists=[];
  function dfs(i,left,p,t){if(result[0]&&result[1])return;if(i===q){if(t===r&&!result[p])result[p]=[labels.join(""),twists.join("")];return}
   for(let j=left;j;){let bit=j&-j;j^=bit;let l=31-Math.clz32(bit);for(let f=0;f<2;f++)if(i>=a.length||E[l][f]===+a[i]){labels.push(l);twists.push(f);dfs(i+1,left^bit,p^(pop[left&(bit-1)]&1),t^f);labels.pop();twists.pop();}}
  }dfs(0,m,0,0);return result.every(Boolean)?result:null;
 }
 let searched=0;
 function lose(k){if(cache.has(k))return cache.get(k);searched++;const [a,m,r]=decode(k),remaining=2*pop[m]-a.length,blank=pop[m]-a.length;
  if(blank<0){cache.set(k,null);return null;}
  if(remaining===4){const w=witness(a,m,r),node=w?{leaf:w}:null;cache.set(k,node);return node;}
  const replies=[];for(const children of actions(a,m,r)){let chosen=null;for(const {reply,state} of children){const child=norm(...state);if(lose(child)){chosen=[reply,child];break}}if(!chosen){cache.set(k,null);return null;}replies.push(chosen)}
  const node=replies.length?{replies}:null;cache.set(k,node);return node;
 }
 const root=norm("",all,0);if(!lose(root))throw Error("no lower certificate");
 const cert=new Map();function collect(k){if(cert.has(k))return;const node=cache.get(k);if(!node)throw Error("missing node");cert.set(k,node);if(node.replies)for(const r of node.replies)collect(r[1])}collect(root);
 const ids=new Map([...cert.keys()].map((k,i)=>[k,i]));
 return [...cert].map(([k,node])=>[k,node.leaf?node.leaf:node.replies.map(([reply,child])=>[reply,ids.get(child)])]);
}
function verifyK5LowerCertificate(certificate){
 const E=[];for(let u=0;u<5;u++)for(let v=u+1;v<5;v++)E.push([u,v]);
 const perms=[];function perm(p){if(p.length===5)perms.push(p);else for(let i=0;i<5;i++)if(!p.includes(i))perm([...p,i])}perm([]);
 const parse=s=>{if(!/^[0-4]*:\d+:[01]$/.test(s))throw Error("state syntax");const [a,m,r]=s.split(":");const labels=E.map((_,i)=>i).filter(i=>(+m>>i)&1);if(+m>=1024||a!==[...a].sort().join("")||a.length>labels.length||labels.length>a.length&&+r!==0)throw Error("state invariant");return {a:[...a].map(Number),labels,r:+r,cap:2*labels.length-a.length};};
 const states=certificate.map(x=>parse(x[0])),visited=new Set();let leaves=0,arcs=0;const leafTypes={};
 if(certificate[0][0]!==":1023:0"||new Set(certificate.map(x=>x[0])).size!==certificate.length)throw Error("root or duplicate");
 function equivalent(a,labels,r,s){if(a.length!==s.a.length||labels.length!==s.labels.length)return false;
  return perms.some(p=>{const cs=a.map(c=>p[c]).sort((x,y)=>x-y);if(cs.some((c,i)=>c!==s.a[i]))return false;let parity=r;
   const es=labels.map(l=>{const [x,y]=E[l].map(c=>p[c]);if(x>y)parity^=1;return E.findIndex(([u,v])=>u===Math.min(x,y)&&v===Math.max(x,y));}).sort((x,y)=>x-y);
   return es.every((e,i)=>e===s.labels[i])&&(labels.length>a.length||parity===s.r);
  });
 }
 function leafSign(s,w){if(!Array.isArray(w)||w.length!==2||!w.every(x=>typeof x==="string"&&/^\d*$/.test(x))||w[0].length!==s.labels.length||w[1].length!==s.labels.length)throw Error("leaf shape");
  const l=[...w[0]].map(Number),t=[...w[1]].map(Number);if([...l].sort((x,y)=>x-y).join()!==s.labels.join()||t.some(x=>x!==0&&x!==1)||t.reduce((x,y)=>x^y,0)!==s.r||s.a.some((c,i)=>E[l[i]][t[i]]!==c))throw Error("leaf constraint");
  let p=0;for(let i=0;i<l.length;i++)for(let j=i+1;j<l.length;j++)p^=+(l[i]>l[j]);return p;
 }
 function visit(id){if(!Number.isInteger(id)||id<0||id>=states.length)throw Error("child index");if(visited.has(id))return;visited.add(id);const s=states[id],data=certificate[id][1],b=s.labels.length-s.a.length;
  if(s.cap===4){if(!Array.isArray(data)||data.length!==2||leafSign(s,data[0])===leafSign(s,data[1]))throw Error("leaf signs");leaves++;const k=`blank${b}:single${s.a.length}`;leafTypes[k]=(leafTypes[k]||0)+1;return}
  if(s.cap<4)throw Error("budget");const required=[];
  if(b)for(let side=0;side<(b===1?2:1);side++)required.push(reply=>{if(!Number.isInteger(reply)||reply<0||reply>4)throw Error("first reply");return [[...s.a,reply],s.labels,s.r^side]});
  for(const c of new Set(s.a))required.push(reply=>{if(!s.labels.includes(reply)||!E[reply].includes(c))throw Error("second reply");let a=[...s.a];a.splice(a.indexOf(c),1);return [a,s.labels.filter(l=>l!==reply),s.r^E[reply].indexOf(c)]});
  if(!Array.isArray(data)||!required.length||data.length!==required.length)throw Error("action coverage");
  for(let i=0;i<required.length;i++){if(!Array.isArray(data[i])||data[i].length!==2)throw Error("arc shape");const [reply,child]=data[i];if(!Number.isInteger(child)||!states[child]||states[child].cap!==s.cap-1||!equivalent(...required[i](reply),states[child]))throw Error("arc transition");arcs++;visit(child);}
 }visit(0);if(visited.size!==certificate.length)throw Error("unreachable nodes");
 return {nodes:visited.size,leaves,arcs,leafTypes};
}
const K5_LOWER_CERTIFICATE=[[":1023:0",[[0,1]]],["0:1023:0",[[0,2],[0,636]]],["00:1023:0",[[0,3],[0,632]]],["000:1023:0",[[1,4],[0,538]]],["0001:1023:0",[[1,5],[0,516],[4,531]]],["00011:1023:0",[[2,6],[0,481],[4,496]]],["000112:1023:0",[[2,7],[0,381],[5,430],[7,473]]],["0001122:1023:0",[[3,8],[0,344],[5,375],[7,375]]],["00011223:1023:0",[[3,9],[0,184],[6,298],[8,298],[9,337]]],["000112233:1023:0",[[1,10],[1,10],[0,73],[6,158],[8,158],[9,158]]],["0001112233:1023:0",[[2,11],[4,11],[8,63],[9,63]]],["000112233:1007:0",[[2,12],[6,31],[8,31],[9,57]]],["00112233:1003:0",[[3,13],[6,13],[8,13],[9,13]]],["0011223:382:0",[[3,14],[6,14],[8,23],[2,27]]],["001123:221:1",[[3,15],[6,15],[4,19],[2,19]]],["00123:157:1",[[3,16],[0,17],[4,18],[2,17]]],["0123:149:1",[["0472","0001"],["2047","0111"]]],["0012:153:0",[["0347","0000"],["3047","0000"]]],["0012:139:1",[["1307","0010"],["3107","0010"]]],["00112:203:1",[[1,20],[0,21],[7,22]]],["0012:198:0",[["1267","0000"],["2167","0000"]]],["0012:197:0",[["0267","0000"],["2067","0000"]]],["0011:101:0",[["0256","0000"],["0265","0000"]]],["001123:126:0",[[3,15],[6,15],[1,24],[2,24]]],["00112:118:1",[[1,25],[5,17],[4,26]]],["0012:141:1",[["2307","0010"],["3207","0010"]]],["0011:102:0",[["1256","0000"],["1265","0000"]]],["001122:189:0",[[2,19],[0,28],[4,30]]],["00112:188:0",[[2,20],[4,29],[7,26]]],["0012:172:0",[["2357","0000"],["3257","0000"]]],["00112:173:1",[[2,21],[0,29],[7,22]]],["00011223:383:0",[[0,13],[6,32],[8,52],[2,55]]],["0001123:223:1",[[1,14],[6,33],[4,40],[2,47]]],["000123:159:1",[[1,15],[0,34],[4,38],[2,34]]],["00012:155:0",[[0,35],[4,36],[7,37]]],["0012:154:0",[["1347","0000"],["3147","0000"]]],["0001:29:0",[["0234","0000"],["0324","0000"]]],["0001:23:0",[["0124","0000"],["0214","0000"]]],["00012:143:1",[[1,25],[0,37],[7,39]]],["0001:15:1",[["1320","0001"],["1230","0001"]]],["000112:207:1",[[1,41],[0,43],[7,45]]],["00112:205:1",[[2,20],[0,42],[7,22]]],["0012:204:0",[["2367","0000"],["3267","0000"]]],["00012:205:0",[[0,42],[6,44],[7,37]]],["0001:30:0",[["1234","0000"],["1324","0000"]]],["00011:31:1",[[1,46],[0,44]]],["0011:29:1",[["2304","0010"],["2340","0001"]]],["000112:219:0",[[0,48],[4,50],[7,51]]],["00112:218:0",[[1,21],[4,21],[7,49]]],["0011:108:0",[["2356","0000"],["2365","0000"]]],["00012:199:0",[[0,20],[6,37],[7,36]]],["00011:109:0",[[0,49],[5,37]]],["0001123:127:0",[[0,23],[6,33],[1,53],[2,53]]],["000112:119:1",[[0,24],[5,34],[4,54]]],["00011:103:0",[[0,26],[5,36]]],["0001122:247:1",[[0,27],[5,47],[4,56]]],["000112:231:0",[[0,28],[5,50],[7,54]]],["00011223:495:0",[[2,13],[6,32],[8,32],[5,58]]],["0001122:239:1",[[0,59],[5,40],[1,62]]],["001122:238:1",[[2,60],[5,41],[1,61]]],["00112:220:0",[[2,21],[4,42],[7,26]]],["00112:236:0",[[2,42],[5,42],[7,49]]],["000112:237:0",[[0,61],[5,43],[7,51]]],["000111223:511:0",[[2,31],[4,57],[8,64],[5,70]]],["00011123:255:0",[[2,32],[4,32],[1,65],[5,65]]],["0001112:223:1",[[1,66],[0,67],[7,69]]],["000112:235:0",[[0,60],[5,50],[7,54]]],["000112:222:0",[[1,60],[4,43],[7,68]]],["00011:110:0",[[1,49],[5,44]]],["000111:111:1",[[1,51],[0,68]]],["00011122:447:1",[[1,71],[0,72],[7,65]]],["0001122:487:0",[[0,59],[5,66],[7,66]]],["0001122:253:1",[[0,59],[5,67],[4,62]]],["00112233:1007:0",[[0,11],[3,11],[3,74],[6,142],[8,142],[9,74]]],["0011223:495:0",[[0,57],[3,75],[3,92],[6,126],[8,126],[2,138]]],["00112233:495:1",[[3,76],[6,86],[8,86],[2,13]]],["0011223:254:0",[[3,77],[6,77],[7,23],[2,85]]],["001123:187:0",[[3,78],[4,15],[1,81],[5,83]]],["00123:151:1",[[1,16],[0,79],[4,80],[2,79]]],["0012:147:0",[["0147","0000"],["1047","0000"]]],["0012:135:1",[["1207","0010"],["2107","0010"]]],["00112:185:0",[[0,20],[4,82],[7,46]]],["0012:169:0",[["0357","0000"],["3057","0000"]]],["00112:155:1",[[1,84],[0,35],[7,22]]],["0012:195:0",[["0167","0000"],["1067","0000"]]],["001122:221:0",[[2,81],[0,60],[4,41]]],["0011223:223:0",[[3,77],[6,87],[1,14],[2,90]]],["001123:119:0",[[0,15],[6,78],[1,88],[2,88]]],["00112:115:1",[[0,89],[5,79],[4,46]]],["0012:29:0",[["2304","0011"],["3204","0011"]]],["001122:187:0",[[1,19],[0,81],[4,91]]],["00112:171:1",[[1,21],[0,82],[7,46]]],["001123:254:0",[[2,76],[3,76],[3,93],[6,93],[1,116],[2,116]]],["00123:187:0",[[1,77],[2,77],[3,94],[0,105],[1,105],[5,113]]],["0123:151:0",[[2,78],[0,78],[0,95],[0,100],[1,101],[2,100]]],["012:135:0",[[2,96],[0,80],[2,97],[0,98],[7,99]]],["0012:150:0",[["1247","0000"],["2147","0000"]]],["01:100:0",[["256","000"],["265","000"]]],["01:19:0",[["140","000"],["041","000"]]],["01:11:0",[["301","011"],["103","011"]]],["012:147:0",[[0,79],[1,79],[0,99],[0,99],[7,98]]],["012:149:0",[[0,102],[1,103],[2,104],[0,97],[7,104]]],["0012:149:0",[["0247","0000"],["2047","0000"]]],["0012:163:0",[["0157","0000"],["1057","0000"]]],["01:21:0",[["240","000"],["042","000"]]],["0012:185:0",[[1,81],[2,106],[0,107],[5,109],[7,111]]],["00112:186:0",[[1,20],[4,82],[7,26]]],["012:184:0",[[1,20],[2,20],[3,98],[5,108],[7,108]]],["01:28:0",[["342","000"],["243","000"]]],["001:102:0",[[1,26],[3,17],[1,97],[5,110]]],["00:137:0",[["037","000"],["307","000"]]],["001:57:0",[[1,46],[2,35],[0,108],[4,112]]],["00:131:0",[["017","000"],["107","000"]]],["0012:155:0",[[0,34],[1,83],[0,114],[0,111],[7,115]]],["012:139:0",[[2,35],[0,18],[3,97],[0,104],[7,99]]],["001:23:0",[[0,37],[1,22],[0,97],[0,112]]],["00112:222:0",[[0,67],[2,85],[2,117],[4,120],[7,123]]],["0012:213:0",[[1,91],[2,48],[0,118],[6,119],[7,111]]],["012:169:0",[[0,82],[1,21],[3,97],[5,108],[7,104]]],["001:108:0",[[1,49],[3,102],[2,97],[5,112]]],["0012:205:0",[[0,43],[1,41],[2,107],[6,121],[7,115]]],["001:30:0",[[0,44],[2,89],[1,108],[4,122]]],["00:11:0",[["013","000"],["031","000"]]],["0011:110:0",[[0,68],[2,124],[1,119],[5,121]]],["00112:110:1",[[2,125],[5,25],[1,49]]],["0012:156:0",[["2347","0000"],["3247","0000"]]],["001123:223:0",[[2,86],[0,32],[3,93],[6,127],[1,131],[2,136]]],["00123:159:0",[[2,87],[0,33],[3,94],[0,113],[1,128],[2,113]]],["0012:171:0",[[0,129],[1,91],[0,118],[5,130],[7,130]]],["00012:171:0",[[0,82],[5,36],[7,36]]],["001:29:0",[[0,36],[1,46],[0,108],[0,110]]],["00112:221:0",[[0,132],[1,66],[2,133],[0,134],[7,135]]],["000112:221:0",[[0,60],[4,43],[7,54]]],["0012:199:0",[[0,50],[1,81],[0,107],[6,115],[7,130]]],["0012:220:0",[[1,60],[2,60],[2,118],[6,109],[7,109]]],["0011:103:0",[[0,54],[1,54],[0,109],[0,109]]],["00112:219:0",[[0,47],[1,47],[0,117],[0,117],[7,137]]],["0011:109:0",[[0,51],[1,51],[0,119],[0,119]]],["001122:254:0",[[2,71],[0,139],[2,131],[5,131],[1,141]]],["0001122:254:1",[[1,59],[5,132],[4,140]]],["000112:238:0",[[1,61],[5,43],[7,68]]],["00112:238:0",[[0,140],[2,59],[2,134],[5,120],[7,123]]],["0011223:383:0",[[0,31],[1,31],[3,126],[6,126],[8,143],[2,151]]],["001123:127:0",[[0,52],[1,52],[3,127],[6,127],[1,144],[2,144]]],["00112:119:0",[[1,145],[0,53],[0,146],[5,113],[1,150]]],["000112:63:1",[[0,24],[4,38],[1,54]]],["0012:157:0",[[0,147],[1,148],[2,149],[0,109],[7,130]]],["00012:157:0",[[0,125],[4,44],[7,36]]],["00112:157:1",[[2,84],[0,125],[7,46]]],["012:153:0",[[0,17],[1,84],[3,104],[0,108],[7,104]]],["0011:115:0",[[1,45],[2,88],[0,121],[4,111]]],["001122:191:0",[[0,152],[0,152],[2,136],[0,156],[1,156]]],["0001122:191:0",[[1,27],[0,153],[4,155]]],["000112:189:0",[[0,28],[4,154],[7,54]]],["00012:173:0",[[0,29],[5,44],[7,37]]],["000112:175:1",[[1,30],[0,154],[7,45]]],["00112:189:0",[[0,153],[1,56],[2,133],[0,157],[7,135]]],["0012:188:0",[[1,28],[2,28],[2,107],[5,109],[7,109]]],["00011223:511:0",[[1,63],[1,63],[0,74],[6,159],[8,159],[2,179]]],["0001123:255:0",[[1,64],[1,64],[0,92],[6,160],[1,168],[2,168]]],["000123:191:0",[[1,161],[1,161],[0,93],[0,165],[1,165],[2,165]]],["0001123:191:0",[[2,77],[4,33],[1,162],[5,163]]],["000112:187:0",[[0,106],[4,129],[7,54]]],["000112:159:1",[[1,148],[0,164],[7,45]]],["00012:158:0",[[1,125],[4,37],[7,44]]],["00012:187:0",[[1,162],[2,162],[0,105],[5,166],[7,166]]],["0001:103:0",[[1,54],[3,34],[0,109],[5,167]]],["000:139:0",[[2,36],[3,44],[0,112]]],["000112:251:0",[[1,65],[2,169],[0,116],[5,171],[7,178]]],["0001122:251:1",[[0,85],[5,170],[4,66]]],["000112:215:0",[[0,106],[4,50],[7,54]]],["00012:215:0",[[1,170],[2,47],[0,172],[6,174],[7,166]]],["0012:214:0",[[1,106],[2,19],[1,118],[6,173],[7,109]]],["001:101:0",[[1,22],[3,79],[0,97],[5,112]]],["0001:109:0",[[1,51],[3,175],[0,119],[5,176]]],["00012:151:0",[[0,96],[4,37],[7,37]]],["000:135:0",[[2,37],[3,37],[0,177]]],["00:134:0",[["127","000"],["217","000"]]],["00011:119:0",[[1,69],[2,53],[0,123],[4,166]]],["0001122:503:0",[[1,70],[2,70],[0,180],[5,168],[7,168]]],["001122:239:0",[[1,72],[0,58],[2,116],[5,181],[1,183]]],["00112:207:0",[[2,182],[0,40],[2,172],[0,120],[7,150]]],["001122:207:0",[[2,106],[0,41],[1,41]]],["00112:237:0",[[0,62],[1,62],[2,120],[5,120],[7,137]]],["0011223:1007:0",[[3,73],[3,185],[6,258],[8,258],[9,289]]],["001123:510:0",[[2,74],[3,186],[6,186],[8,238],[2,254]]],["00123:251:0",[[1,126],[3,187],[6,215],[1,227],[5,234]]],["0123:119:0",[[1,127],[0,188],[6,194],[1,205],[2,205]]],["012:171:0",[[0,128],[0,189],[0,193],[1,193]]],["01:202:0",[[2,118],[3,190],[6,192]]],["0:152:0",[[2,108],[3,191]]],[":10:0",[["13","00"],["31","00"]]],["0:131:0",[[0,112],[0,191]]],["01:153:0",[[2,149],[3,192],[0,190]]],["012:167:0",[[0,195],[0,200],[0,203],[1,203]]],["0012:167:0",[[0,196],[1,198],[0,199],[5,115],[7,115]]],["00012:167:0",[[0,197],[5,37],[7,37]]],["0012:165:0",[["0257","0000"],["2057","0000"]]],["00112:167:1",[[1,197],[0,197],[7,22]]],["012:165:0",[[0,197],[1,197],[2,97],[5,97],[7,98]]],["01:150:0",[[2,95],[1,201],[4,202]]],["0:100:0",[[1,97],[2,191]]],["0:134:0",[[0,177],[1,191]]],["01:147:0",[[2,100],[0,204],[0,204]]],["0:146:0",[[2,99],[1,191]]],["012:115:0",[[1,206],[0,208],[5,203],[1,211]]],["0012:31:0",[[0,207],[0,207],[2,100],[0,130],[1,130]]],["00012:31:0",[[1,89],[0,36],[4,39]]],["01:29:0",[[0,130],[0,190],[0,209]]],["0:137:0",[[0,110],[0,210]]],[":129:0",[["07","00"],["70","00"]]],["01:113:0",[[1,212],[0,214],[4,204]]],["001:15:0",[[2,213],[0,39],[1,99],[0,122]]],["0012:15:0",[["2301","0011"],["3201","0011"]]],["0:11:0",[[0,122],[0,191]]],["0012:189:0",[[0,216],[0,219],[0,222],[4,225]]],["00012:189:0",[[1,153],[2,217],[0,157],[5,218],[7,166]]],["000112:190:0",[[1,28],[4,154],[7,68]]],["0001:110:0",[[1,68],[3,147],[1,119],[5,167]]],["012:188:0",[[0,157],[2,220],[4,221],[4,221]]],["01:201:0",[[2,107],[3,209],[6,209]]],["01:154:0",[[2,114],[3,204],[4,192]]],["001:186:0",[[2,105],[1,223],[4,224]]],["01:184:0",[[2,107],[3,202],[4,190]]],["00:102:0",[[1,109],[1,201]]],["001:155:0",[[2,113],[0,221],[0,226]]],["00:154:0",[[2,111],[1,190]]],["0012:249:0",[[1,181],[0,228],[5,230],[4,233]]],["012:205:0",[[0,120],[2,223],[0,189],[7,229]]],["01:101:0",[[0,173],[0,192],[0,201]]],["001:214:0",[[2,172],[1,231],[6,232]]],["01:156:0",[[3,118],[3,201],[4,192]]],["00:101:0",[[1,173],[0,201]]],["001:217:0",[[2,172],[0,189],[6,224]]],["0012:215:0",[[0,171],[0,235],[0,233],[1,236]]],["012:185:0",[[0,105],[0,220],[0,223],[4,193]]],["001:213:0",[[2,117],[0,231],[6,237]]],["00:108:0",[[1,119],[2,201]]],["00112:254:0",[[0,239],[1,245],[4,245],[1,250]]],["000112:254:0",[[1,240],[2,139],[1,141],[5,242],[7,243]]],["0001112:254:0",[[1,140],[4,140],[7,241]]],["000111:126:0",[[1,68],[4,68]]],["00012:221:0",[[1,132],[2,67],[0,134],[6,218],[7,166]]],["00011:126:0",[[1,241],[2,244],[1,123],[4,218]]],["000112:126:1",[[1,124],[5,147],[4,68]]],["0012:238:0",[[1,141],[2,246],[5,247],[1,249]]],["012:220:0",[[0,134],[2,193],[4,189],[4,189]]],["001:203:0",[[2,133],[0,189],[6,248]]],["00:139:0",[[0,167],[0,192]]],["001:218:0",[[2,117],[1,189],[6,226]]],["0011:222:0",[[2,116],[1,251],[4,252]]],["001:220:0",[[2,134],[2,189],[6,224]]],["001:206:0",[[2,120],[1,189],[6,253]]],["00:135:0",[[0,176],[0,202]]],["00112:446:0",[[2,180],[2,227],[4,255],[7,250]]],["0012:237:0",[[1,183],[2,228],[5,252],[7,256]]],["001:109:0",[[0,174],[0,257],[0,237]]],["01:108:0",[[0,119],[2,192],[5,192]]],["001123:479:0",[[2,142],[3,186],[6,259],[8,273],[2,283]]],["00123:127:0",[[1,143],[3,187],[6,260],[1,268],[2,268]]],["0012:175:0",[[0,261],[0,267],[0,225],[1,225]]],["00012:175:0",[[0,262],[1,155],[0,265],[5,266],[7,266]]],["000012:175:0",[[0,154],[5,263],[7,263]]],["00001:31:0",[[0,44],[4,264]]],["0000:15:0",[["0123","0000"],["0132","0000"]]],["0012:173:0",[[0,154],[1,30],[2,118],[5,121],[7,115]]],["0001:31:0",[[0,263],[1,45],[0,121],[0,167]]],["012:173:0",[[0,265],[2,189],[0,221],[7,229]]],["0012:119:0",[[1,144],[0,269],[5,225],[1,272]]],["012:118:0",[[1,146],[1,270],[5,193],[1,271]]],["01:139:0",[[2,114],[3,201],[0,192]]],["01:114:0",[[1,121],[1,214],[4,190]]],["001:115:0",[[1,150],[0,271],[4,226]]],["00112:239:0",[[0,274],[0,281],[0,245],[1,282]]],["000112:239:0",[[0,275],[1,278],[0,141],[5,279],[7,280]]],["0000112:239:0",[[0,140],[5,276],[7,277]]],["000012:207:0",[[0,43],[6,263],[7,263]]],["000011:111:0",[[0,68],[5,263]]],["0001112:239:1",[[1,62],[0,140],[7,69]]],["00012:207:0",[[0,276],[1,40],[0,120],[6,266],[7,266]]],["00011:111:0",[[0,277],[1,69],[0,123],[0,218]]],["0012:252:0",[[1,141],[2,228],[5,251],[4,249]]],["0011:219:0",[[2,136],[0,249],[0,249]]],["00112:439:0",[[2,151],[0,284],[0,284],[7,282]]],["0012:245:0",[[1,285],[0,267],[5,249],[4,287]]],["00112:175:0",[[2,286],[0,155],[2,117],[0,265],[7,150]]],["001122:175:0",[[2,48],[0,30],[1,30]]],["001:211:0",[[2,288],[0,221],[6,232]]],["0012:211:0",[[1,83],[2,83],[0,114],[6,173],[7,173]]],["001122:495:0",[[0,290],[0,296],[0,297],[1,297]]],["0001122:495:0",[[0,291],[1,294],[0,295],[5,274],[7,274]]],["00001122:495:0",[[0,292],[5,275],[7,275]]],["0001122:493:0",[[0,293],[5,140],[7,62]]],["001122:492:0",[[2,61],[5,61],[7,61]]],["00011122:495:1",[[1,292],[0,292],[7,278]]],["001122:493:0",[[0,292],[1,292],[2,141],[5,141],[7,183]]],["00112:494:0",[[2,295],[2,281],[5,255],[7,250]]],["00112:493:0",[[2,295],[2,245],[5,245],[7,282]]],["0001123:511:0",[[2,158],[0,185],[6,299],[8,323],[2,336]]],["000123:255:0",[[1,159],[0,300],[6,311],[1,319],[2,319]]],["00123:254:0",[[1,92],[3,301],[6,308],[1,310],[2,310]]],["0123:187:0",[[0,93],[3,302],[0,235],[1,235],[5,307]]],["012:151:0",[[0,303],[0,305],[0,229],[1,306]]],["0012:151:0",[[0,175],[1,304],[0,95],[0,173],[7,115]]],["00112:151:1",[[1,103],[0,96],[7,22]]],["01:135:0",[[2,95],[1,201],[0,202]]],["01:149:0",[[2,101],[0,201],[0,201]]],["012:155:0",[[0,113],[0,270],[0,208],[1,193]]],["0012:187:0",[[0,165],[0,235],[0,309],[1,309]]],["001:185:0",[[2,105],[0,223],[4,224]]],["0012:250:0",[[1,116],[1,228],[5,236],[4,251]]],["00012:191:0",[[0,312],[0,215],[0,317],[1,317]]],["000012:191:0",[[1,313],[2,313],[0,216],[5,314],[7,314]]],["0000112:191:0",[[0,217],[4,262],[7,277]]],["00001:111:0",[[1,277],[3,315],[0,218],[5,316]]],["000012:159:0",[[0,164],[4,263],[7,263]]],["0000:143:0",[[2,263],[3,263],[0,176]]],["0001:187:0",[[2,165],[0,222],[4,318]]],["000:110:0",[[1,218],[1,237]]],["00012:251:0",[[1,168],[0,310],[5,320],[4,322]]],["0001:215:0",[[2,171],[0,230],[6,321]]],["000:109:0",[[1,174],[0,237]]],["0001:221:0",[[2,242],[0,251],[6,318]]],["000112:255:0",[[0,324],[0,238],[0,332],[1,335]]],["0000112:255:0",[[1,325],[2,327],[0,239],[5,329],[7,330]]],["00001112:255:0",[[0,240],[4,275],[7,326]]],["0000111:127:0",[[0,241],[4,277]]],["00001122:255:1",[[0,139],[5,328],[4,275]]],["0000112:223:0",[[0,67],[4,276],[7,277]]],["000012:223:0",[[1,328],[2,328],[0,242],[6,314],[7,314]]],["000011:127:0",[[1,326],[2,331],[0,243],[4,314]]],["0000112:127:1",[[0,244],[5,315],[4,277]]],["00012:254:0",[[1,239],[1,281],[5,322],[4,333]]],["0001:222:0",[[2,242],[1,251],[6,334]]],["000:103:0",[[1,166],[0,224]]],["00011:251:0",[[2,168],[0,250],[4,322]]],["000112:503:0",[[2,179],[0,254],[5,319],[7,335]]],["0001122:511:0",[[0,338],[0,289],[0,343],[1,343]]],["00001122:511:0",[[1,339],[2,339],[0,341],[5,324],[7,324]]],["000011122:511:0",[[0,340],[4,291],[7,325]]],["00011122:510:0",[[1,292],[4,292],[7,240]]],["0001122:509:0",[[1,294],[2,340],[0,295],[5,239],[7,342]]],["000112:253:0",[[1,278],[2,72],[0,141],[5,242],[7,178]]],["000112:509:0",[[2,341],[0,296],[5,332],[7,335]]],["001122:1007:0",[[3,184],[2,345],[5,369],[7,369]]],["00112:766:0",[[3,185],[3,346],[6,346],[1,365]]],["0012:701:0",[[3,186],[3,347],[0,358],[4,362]]],["012:679:0",[[3,187],[0,348],[0,355],[1,355]]],["01:406:0",[[2,349],[1,352],[4,354]]],["012:117:0",[[1,350],[0,270],[5,221],[4,229]]],["0012:143:0",[[2,351],[0,38],[2,114],[0,115],[7,212]]],["00112:117:1",[[0,25],[5,35],[4,22]]],["0:209:0",[[1,270],[0,353]]],[":100:0",[[0,201]]],["0:101:0",[[0,232],[0,353]]],["01:403:0",[[2,205],[0,356],[0,356]]],["0:113:0",[[1,211],[0,357]]],[":112:0",[[1,214]]],["001:442:0",[[2,227],[1,359],[4,361]]],["01:426:0",[[2,228],[1,360],[5,354]]],["0:212:0",[[1,231],[2,353]]],["00:214:0",[[1,230],[1,360]]],["001:407:0",[[2,268],[0,348],[0,363]]],["00:115:0",[[1,272],[0,364]]],["0:114:0",[[1,271],[1,357]]],["0011:446:0",[[2,254],[2,358],[4,366]]],["001:430:0",[[2,255],[2,359],[5,367]]],["00:109:0",[[0,321],[0,368]]],["0:108:0",[[0,237],[2,353]]],["00112:751:0",[[3,258],[3,346],[6,370],[1,371]]],["0012:687:0",[[3,259],[3,347],[0,362],[1,362]]],["0011:439:0",[[2,283],[0,372],[0,372]]],["001:438:0",[[2,284],[1,373],[4,374]]],["01:422:0",[[2,267],[1,352],[5,354]]],["00:211:0",[[1,287],[0,352]]],["000112:767:0",[[3,298],[0,345],[6,376],[1,380]]],["00012:703:0",[[3,299],[0,346],[0,377],[1,377]]],["0001:443:0",[[2,319],[0,358],[4,378]]],["000:221:0",[[1,322],[0,379]]],["00:220:0",[[1,251],[2,360]]],["00011:503:0",[[2,336],[0,365],[5,377]]],["00112:1022:0",[[2,344],[2,382],[5,382],[7,424]]],["0012:765:0",[[1,369],[3,383],[5,395],[4,406]]],["012:687:0",[[0,370],[3,384],[0,387],[1,387]]],["01:438:0",[[0,372],[1,385],[4,385]]],["0:211:0",[[0,374],[0,386]]],[":114:0",[[0,364]]],["01:407:0",[[0,362],[0,388],[0,394]]],["0:241:0",[[1,389],[0,393]]],["01:143:0",[[0,390],[1,352],[0,391]]],["001:143:0",[[2,350],[1,270],[0,253]]],["0:135:0",[[0,253],[0,392]]],[":134:0",[[0,202]]],[":101:0",[[0,354]]],["0:115:0",[[0,363],[0,386]]],["001:494:0",[[1,396],[2,399],[5,404]]],["0011:494:0",[[2,296],[2,397],[5,366]]],["001:444:0",[[2,281],[2,359],[4,398]]],["00:213:0",[[1,236],[0,360]]],["01:444:0",[[0,397],[2,400],[4,403]]],["0:214:0",[[0,361],[1,401]]],[":102:0",[[0,402]]],["0:102:0",[[0,224],[1,353]]],["0:213:0",[[0,398],[0,401]]],["00:215:0",[[0,405],[0,400]]],["000:215:0",[[1,320],[0,361]]],["001:439:0",[[0,407],[0,384],[0,414]]],["0001:439:0",[[2,408],[0,372],[4,405]]],["00012:247:0",[[1,409],[0,412],[5,413],[4,320]]],["000112:247:0",[[1,410],[2,55],[0,411],[5,171],[7,178]]],["0001112:191:1",[[1,56],[0,217],[7,69]]],["00112:190:0",[[0,217],[2,27],[2,172],[4,265],[7,123]]],["0012:246:0",[[1,411],[1,267],[5,233],[4,230]]],["0001:219:0",[[2,171],[0,249],[6,334]]],["00:243:0",[[1,415],[0,423]]],["001:243:0",[[1,416],[0,422],[4,398]]],["0011:159:0",[[2,417],[1,236],[0,421]]],["00112:159:0",[[2,418],[0,163],[2,288],[0,419],[7,150]]],["001122:119:0",[[0,148],[5,83],[1,351]]],["0012:158:0",[[0,164],[2,420],[2,114],[4,115],[7,121]]],["00112:103:1",[[0,125],[5,18],[1,22]]],["001:158:0",[[2,419],[1,231],[4,253]]],["01:158:0",[[0,421],[1,360],[4,391]]],["0:242:0",[[1,422],[1,393]]],["0011:510:0",[[0,425],[1,395],[4,395]]],["00011:510:0",[[2,426],[1,396],[5,429]]],["000112:510:0",[[2,341],[1,296],[5,427],[7,428]]],["00012:253:0",[[1,342],[0,281],[5,333],[4,413]]],["00011:254:0",[[2,239],[1,250],[4,333]]],["0001:446:0",[[2,427],[1,397],[4,405]]],["00012:767:0",[[1,375],[0,431],[5,455],[1,468]]],["0012:766:0",[[1,345],[3,432],[5,438],[1,446]]],["012:701:0",[[0,346],[2,433],[0,437],[4,387]]],["01:429:0",[[0,434],[2,436],[0,403]]],["001:429:0",[[2,245],[2,435],[0,398]]],["01:425:0",[[2,246],[0,360],[0,360]]],["0:220:0",[[0,379],[2,401]]],["01:442:0",[[0,358],[1,400],[4,400]]],["001:487:0",[[1,439],[0,399],[5,445]]],["0011:445:0",[[2,440],[2,444],[0,397]]],["00112:445:0",[[2,138],[2,441],[0,281],[7,443]]],["0012:235:0",[[1,131],[0,246],[5,442],[1,233]]],["001:199:0",[[2,133],[0,223],[6,253]]],["0011:221:0",[[2,131],[0,251],[0,251]]],["001:427:0",[[2,441],[0,359],[0,361]]],["00:221:0",[[0,378],[0,436]]],["001:502:0",[[1,365],[1,447],[5,452]]],["01:430:0",[[0,366],[2,448],[5,450]]],["0:248:0",[[1,449],[3,393]]],["01:206:0",[[0,252],[1,360],[6,391]]],["0:109:0",[[0,367],[0,451]]],[":108:0",[[0,368]]],["00:249:0",[[1,453],[0,448]]],["001:249:0",[[1,454],[0,449],[4,361]]],["0011:207:0",[[2,181],[1,233],[0,252]]],["0001:495:0",[[1,456],[0,395],[5,464]]],["00011:495:0",[[2,457],[0,396],[5,463]]],["000112:495:0",[[2,290],[0,296],[5,458],[7,461]]],["00012:239:0",[[1,274],[0,245],[5,459],[1,413]]],["0001:207:0",[[2,279],[0,252],[6,460]]],["000:143:0",[[0,316],[0,253]]],["00011:223:0",[[2,462],[0,250],[0,333]]],["000112:223:0",[[0,328],[1,65],[0,116],[0,242],[7,280]]],["0001:431:0",[[2,458],[0,366],[0,405]]],["000:223:0",[[0,465],[0,445]]],["0000:223:0",[[1,466],[0,378]]],["00001:223:0",[[2,329],[0,333],[6,467]]],["0000:111:0",[[1,314],[0,318]]],["0001:503:0",[[1,380],[0,446],[5,469]]],["000:251:0",[[1,470],[0,472]]],["0001:251:0",[[1,335],[0,471],[4,378]]],["001:250:0",[[1,250],[1,449],[4,379]]],["00:250:0",[[1,471],[1,448]]],["00011:511:0",[[0,474],[0,424],[0,479]]],["000011:511:0",[[2,475],[0,425],[5,478]]],["0000112:511:0",[[2,338],[0,426],[5,476],[7,477]]],["000012:255:0",[[1,324],[0,332],[5,466],[4,466]]],["000011:255:0",[[2,324],[0,428],[4,466]]],["00001:447:0",[[2,476],[0,429],[4,465]]],["0001:510:0",[[1,425],[1,480],[5,469]]],["001:508:0",[[1,396],[2,447],[5,472]]],["0011:1022:0",[[2,381],[1,482],[4,482]]],["001:1006:0",[[3,382],[1,483],[5,488]]],["01:1004:0",[[3,383],[2,484],[5,484]]],["0:243:0",[[0,414],[0,485]]],[":103:0",[[0,486]]],["0:103:0",[[0,487],[0,401]]],["00:103:0",[[0,334],[0,402]]],["00:247:0",[[0,489],[0,495]]],["000:247:0",[[1,490],[0,494]]],["0001:247:0",[[1,491],[0,493],[4,405]]],["00011:247:0",[[2,409],[0,492],[4,320]]],["0011:190:0",[[2,411],[1,230],[4,421]]],["001:246:0",[[1,492],[1,422],[4,361]]],["00:246:0",[[1,493],[1,423]]],["0:246:0",[[0,494],[1,485]]],["0001:1007:0",[[3,430],[0,482],[0,497]]],["000:1005:0",[[3,468],[0,498]]],["00:1004:0",[[3,499],[2,514]]],["001:499:0",[[1,500],[0,513],[5,414]]],["0011:415:0",[[2,501],[2,511],[0,512]]],["00112:415:0",[[2,502],[2,508],[0,510],[7,416]]],["001122:127:0",[[0,503],[1,503],[2,417],[5,417],[1,506]]],["0001122:127:0",[[0,504],[5,163],[1,505]]],["001122:126:0",[[2,148],[5,148],[1,124]]],["000112:125:1",[[0,124],[5,164],[4,51]]],["00112:111:0",[[1,505],[0,507],[2,419],[5,350],[1,137]]],["000112:111:1",[[0,124],[5,38],[1,51]]],["0012:243:0",[[1,417],[0,509],[5,287],[4,236]]],["012:103:0",[[1,419],[0,231],[5,270],[1,229]]],["0012:125:0",[[1,506],[2,349],[5,421],[4,256]]],["001:435:0",[[2,508],[0,348],[4,398]]],["001:414:0",[[2,510],[2,348],[4,367]]],["01:414:0",[[0,512],[2,388],[4,450]]],["0:1000:0",[[3,513],[3,515]]],[":109:0",[[0,450]]],["001:1022:0",[[1,481],[1,517],[4,530]]],["01:1006:0",[[0,482],[1,518],[5,520]]],["0:1004:0",[[0,498],[2,519]]],[":1000:0",[[0,514]]],["0:247:0",[[0,488],[0,521]]],[":187:0",[[0,522]]],["0:187:0",[[0,523],[0,529]]],["00:187:0",[[0,524],[0,527]]],["000:187:0",[[1,317],[0,525]]],["00:185:0",[[1,309],[0,526]]],["0:184:0",[[1,223],[3,392]]],["0:185:0",[[0,525],[0,528]]],[":184:0",[[0,526]]],[":185:0",[[0,527]]],["00:1005:0",[[0,497],[0,518]]],["000:1007:0",[[0,532],[0,530]]],["0000:1007:0",[[3,533],[0,497]]],["00001:511:0",[[1,474],[0,479],[5,534]]],["0000:255:0",[[1,535],[0,537]]],["00001:255:0",[[1,477],[0,536],[4,465]]],["0001:254:0",[[1,428],[1,471],[4,378]]],["000:254:0",[[1,536],[1,472]]],["00:1015:0",[[1,539],[0,583]]],["001:1015:0",[[1,540],[0,517],[4,579]]],["0011:1007:0",[[2,541],[1,550],[0,482]]],["00112:1007:0",[[2,344],[2,431],[5,542],[7,544]]],["0012:751:0",[[1,369],[3,432],[5,543],[1,406]]],["001:431:0",[[0,463],[0,447],[0,404]]],["0011:447:0",[[0,545],[0,446],[0,549]]],["00011:447:0",[[2,546],[0,365],[0,429]]],["000112:447:0",[[2,547],[0,254],[0,427],[7,461]]],["0001122:255:0",[[1,548],[0,327],[0,138],[5,462],[1,342]]],["00011122:255:0",[[1,58],[0,139],[4,278]]],["001:446:0",[[0,429],[1,399],[4,404]]],["001:1005:0",[[3,551],[0,483],[0,498]]],["0012:759:0",[[1,552],[0,432],[5,577],[1,499]]],["00112:703:0",[[3,553],[3,575],[0,346],[1,576]]],["001123:447:0",[[2,554],[3,564],[0,186],[8,571],[2,574]]],["0011223:255:0",[[0,555],[0,556],[3,558],[6,558],[1,126],[2,563]]],["00011223:255:0",[[0,76],[6,161],[7,52],[2,169]]],["00011223:255:1",[[2,86],[6,161],[4,32],[5,557]]],["0001122:223:0",[[1,85],[0,132],[4,40]]],["001123:191:0",[[0,161],[0,161],[3,559],[0,93],[1,562],[2,562]]],["00123:183:0",[[1,560],[1,560],[0,94],[0,561],[1,561],[2,561]]],["001123:183:0",[[2,78],[4,78],[1,304],[5,304]]],["0012:179:0",[[1,304],[2,304],[0,95],[5,173],[7,173]]],["00112:187:0",[[0,162],[1,170],[0,172],[0,105],[7,135]]],["001122:223:0",[[0,557],[0,557],[2,562],[0,131],[1,131]]],["00123:247:0",[[1,558],[0,301],[6,565],[1,508],[2,508]]],["0012:183:0",[[0,566],[0,194],[0,570],[1,570]]],["00012:183:0",[[1,567],[2,567],[0,569],[5,174],[7,174]]],["000112:183:0",[[0,568],[4,196],[7,51]]],["00112:182:0",[[1,197],[4,197],[7,49]]],["0012:181:0",[[1,198],[2,568],[0,199],[5,119],[7,173]]],["001:179:0",[[2,561],[0,200],[4,237]]],["00112:191:0",[[0,572],[0,412],[0,215],[1,573]]],["000112:191:0",[[0,313],[1,410],[0,411],[0,216],[7,280]]],["0011:187:0",[[2,562],[0,230],[0,222]]],["00112:443:0",[[2,563],[0,227],[0,227],[7,573]]],["0012:695:0",[[3,564],[0,347],[0,511],[1,511]]],["0011:443:0",[[2,574],[0,358],[0,358]]],["001:493:0",[[1,578],[2,433],[5,445]]],["0011:493:0",[[2,297],[2,434],[5,434]]],["00:1003:0",[[0,580],[0,582]]],["000:1003:0",[[3,479],[0,581]]],["00:1001:0",[[3,446],[0,514]]],["0:1001:0",[[0,581],[0,519]]],["0:1011:0",[[1,584],[0,626]]],["01:1011:0",[[1,585],[0,520],[4,623]]],["001:927:0",[[2,586],[2,622],[0,488]]],["0012:639:0",[[1,587],[2,616],[5,543],[1,620]]],["00112:639:0",[[3,588],[2,603],[5,603],[1,612]]],["001123:383:0",[[2,142],[3,589],[6,589],[8,595],[2,571]]],["00123:223:0",[[1,126],[3,301],[6,590],[1,441],[2,234]]],["0012:159:0",[[0,591],[0,509],[0,592],[1,594]]],["00012:159:0",[[0,315],[1,163],[0,419],[0,166],[7,266]]],["001:103:0",[[0,166],[0,593],[0,224]]],["01:102:0",[[0,109],[1,192],[5,209]]],["001:157:0",[[2,146],[0,231],[0,224]]],["00112:127:0",[[0,596],[0,599],[0,599],[1,601]]],["000112:127:0",[[1,597],[0,331],[0,598],[5,591],[1,178]]],["0001112:127:0",[[1,507],[0,244],[4,69]]],["00112:126:0",[[2,504],[0,244],[2,146],[5,146],[1,123]]],["0012:126:0",[[1,598],[2,269],[5,594],[1,600]]],["001:118:0",[[1,123],[1,271],[4,224]]],["0011:111:0",[[0,280],[0,600],[0,602]]],["001:110:0",[[0,218],[1,257],[5,248]]],["0012:575:0",[[3,589],[3,604],[0,444],[1,609]]],["012:567:0",[[3,301],[0,605],[0,605],[1,606]]],["01:405:0",[[2,269],[0,352],[0,364]]],["01:155:0",[[0,225],[0,352],[0,607]]],["0:154:0",[[0,226],[1,608]]],[":137:0",[[0,209]]],["001:215:0",[[0,320],[0,610],[0,361]]],["01:186:0",[[0,222],[1,611],[4,402]]],["0:198:0",[[1,223],[1,608]]],["0011:191:0",[[0,613],[0,493],[0,615]]],["00011:191:0",[[2,572],[0,492],[0,614]]],["0001:190:0",[[2,216],[1,222],[4,334]]],["001:190:0",[[0,614],[1,610],[4,487]]],["012:575:0",[[0,603],[2,433],[0,617],[1,618]]],["01:427:0",[[0,444],[0,448],[0,400]]],["01:187:0",[[0,619],[0,400],[0,527]]],["001:187:0",[[0,317],[0,610],[0,525]]],["001:247:0",[[0,490],[0,621],[0,494]]],["01:190:0",[[0,615],[1,400],[4,486]]],["01:1001:0",[[3,432],[0,484],[0,514]]],["0:508:0",[[0,624],[2,521]]],["00:508:0",[[1,480],[2,625]]],["0:500:0",[[1,447],[2,515]]],[":1009:0",[[1,627]]],["0:191:0",[[0,628],[0,521]]],["00:191:0",[[0,629],[0,522]]],["000:191:0",[[0,630],[0,523]]],["0000:191:0",[[1,631],[0,524]]],["00001:191:0",[[2,312],[0,614],[4,467]]],["0:1015:0",[[0,538],[0,633]]],[":1005:0",[[0,634]]],["0:1005:0",[[0,530],[0,635]]],[":1004:0",[[0,518]]],[":1007:0",[[0,637]]],["0:1007:0",[[0,638],[0,633]]],["00:1007:0",[[0,531],[0,634]]]];
function auditK5LowerReceipt(){const r=verifyK5LowerCertificate(K5_LOWER_CERTIFICATE);if(r.nodes!==639||r.leaves!==40||r.arcs!==2003)throw Error('K5 receipt');let rejected=0;for(let i=0;i<3;i++){const bad=JSON.parse(JSON.stringify(K5_LOWER_CERTIFICATE));if(i===0)bad[0][1]=[];if(i===1)bad[0][1][0][1]=0;if(i===2){const l=bad.find(x=>x[1].length===2&&typeof x[1][0][0]==='string');l[1][1]=l[1][0]}try{verifyK5LowerCertificate(bad)}catch{rejected++}}if(rejected!==3)throw Error('K5 negative controls');return {...r,rejected};}
function auditCornerHallPlans(){
 const labels=["UFR","URB","ULF","UBL","DRF","DBR","DFL","DLB"],colors="URFDLB";
 const plans=[["0000112","",48],["0000113","",24],["0000114","",24],["0000123","",24],["0000124","",24],["0000133","",24],["0000134","",12],["0000333","",6],["0001112","",24],["0001113","",24],["0001122","",24],["0001123","112",48],["0001124","0002",48],["0001125","00011",24],["0001133","11",24],["0001134","114",24],["0001144","000",12],["0001233","12",24],["0001234","124",24],["0001245","00014",6],["0001333","1",12],["0001334","14",12],["0011223","1122",24],["0011233","112",24],["0011234","0023",24],["0011235","1125",24],["0011334","114",12],["0012334","124",12],["0012345","1245",6]];
 const opposite=[[0,3],[1,4],[2,5]],sym=[];for(let a=0;a<3;a++)for(let b=0;b<3;b++)if(a!==b)for(let mask=0;mask<8;mask++){const p=[];for(let i=0;i<3;i++)for(let j=0;j<2;j++)p[opposite[i][j]]=opposite[[a,b,3-a-b][i]][j^(mask>>i&1)];sym.push(p)}
 const all=labels.map((_,i)=>i),planMap=new Map(plans.map(([a,p,n])=>[a,{p,n,count:0}]));
 // Direct injections, deliberately not Hall subset enumeration or minimax.
 function assignments(a,l,visit){const pick=[];function walk(i,left){if(i===a.length){visit(pick,left[0]);return}for(const j of left)if(labels[j].includes(colors[+a[i]])){pick.push(j);walk(i+1,left.filter(x=>x!==j));pick.pop()}}walk(0,l)}
 function support(a,l){const blanks=new Set();let total=0;assignments(a,l,(_,b)=>{blanks.add(b);total++});return {total,blanks}}
 let roots=0,injections=0,branchChecks=0,maxPlan=0,planHistogram={},actualSecondReadHistogram={},terminalSignChecks=0,terminalCounts={};
 function verifyPlan(a,p){let witnesses=0;assignments(a,all,(matching,blank)=>{witnesses++;let rows=[...a],remaining=[...all],assigned=[...matching],q=0;
  while(true){let s=support(rows,remaining);branchChecks++;if(!s.total)throw Error("actual matching lost");if(s.blanks.size<remaining.length){
   // Find a tight set independently, then simulate resolving all but one in that set.
   let tight=null;for(let k=1;k<(1<<rows.length)&&!tight;k++){let ii=rows.map((_,i)=>i).filter(i=>k>>i&1),neighbors=remaining.filter(j=>ii.some(i=>labels[j].includes(colors[+rows[i]])));if(ii.length===neighbors.length)tight={ii,neighbors};}
   if(!tight)throw Error("coloop without tight set");
   const skip=tight.ii[0];if(!tight.neighbors.includes(assigned[skip]))throw Error("tight witness");const left=tight.neighbors.filter(x=>!tight.ii.slice(1).some(i=>assigned[i]===x));if(left.length!==1||left[0]!==assigned[skip])throw Error("saved read");const cost=q+rows.length-1;if(cost!==6)throw Error("budget");
   // Two omissions are safe with a terminal sign oracle: either both in a tight
   // set of size >=2, or one forced tight singleton and one arbitrary other row.
   if(rows.length<2)throw Error("too late for terminal oracle");
   const omit=tight.ii.length>=2?tight.ii.slice(0,2):[skip,rows.findIndex((_,i)=>i!==skip)];
   const kept=rows.map((_,i)=>i).filter(i=>!omit.includes(i));
   const unknown=remaining.filter(l=>!kept.some(i=>assigned[i]===l));
   const target=[...assigned,blank],parity=x=>{let b=0;for(let i=0;i<x.length;i++)for(let j=i+1;j<x.length;j++)b^=+(x[i]>x[j]);return b;};
   const signs=[0,0];assignments(omit.map(i=>rows[i]),unknown,(pair,last)=>{const candidate=[...target];for(let j=0;j<2;j++)candidate[omit[j]]=pair[j];candidate[candidate.length-1]=last;signs[parity(candidate)]++;});
   if(signs.some(x=>x>1)||signs[parity(target)]!==1||q+rows.length-2!==5)throw Error("terminal oracle");
   terminalSignChecks++;const key=signs[0]+signs[1];terminalCounts[key]=(terminalCounts[key]||0)+1;
actualSecondReadHistogram[q]=(actualSecondReadHistogram[q]||0)+1;break;
  }
  if(q>=p.length)throw Error("plan exhausted "+a);const i=rows.indexOf(p[q]);if(i<0)throw Error("bad schedule");remaining=remaining.filter(x=>x!==assigned[i]);rows.splice(i,1);assigned.splice(i,1);q++;
 }});injections+=witnesses;if(!witnesses)throw Error("infeasible rep");return witnesses}
 for(const [a,p,n] of plans){verifyPlan(a,p);maxPlan=Math.max(maxPlan,p.length);planHistogram[p.length]=(planHistogram[p.length]||0)+n}
 function gen(a,c){if(a.length===7){if(!support(a,all).total)return;roots++;const k=sym.map(p=>[...a].map(c=>p[+c]).sort().join("")).sort()[0],row=planMap.get(k);if(!row)throw Error("uncovered root");row.count++;return}for(let i=c;i<6;i++)gen(a+i,i)}gen("",0);
 if(roots!==642||plans.length!==29||maxPlan!==5||[...planMap.values()].some(r=>r.count!==r.n))throw Error("coverage");
 // Mutation must fail: shorten one of the hardest schedules.
 const receipt={roots,orbitCount:plans.length,maxPlan,planHistogram,injections,branchChecks,actualSecondReadHistogram:{...actualSecondReadHistogram},terminalSignChecks,terminalCounts:{...terminalCounts}};
 let rejected=false;try{verifyPlan("0001125","0001")}catch{rejected=true}if(!rejected)throw Error("negative control");
 return {...receipt,negativeControl:rejected};
}
function auditHallBlockPacking(){
 const labels=["UFR","URB","ULF","UBL","DRF","DBR","DFL","DLB"],colors="URFDLB";
 const masks=Array.from(colors,c=>labels.reduce((m,l,i)=>m|(l.includes(c)?1<<i:0),0)),pop=Array.from({length:256},(_,x)=>x.toString(2).replace(/0/g,"").length);
 let checked=0,hist={},examples={};const memo=new Map();
 function inspect(a,m){
  const n=a.length;if(pop[m]!==n+1)return;
  let tight=[];for(let s=1;s<1<<n;s++){let N=0;for(let i=0;i<n;i++)if(s>>i&1)N|=m&masks[+a[i]];if(pop[N]<pop[s])return;if(pop[N]===pop[s])tight.push(s)}
  let match=[],blank=-1;function assign(i,left){if(i===n){blank=31-Math.clz32(left);return true}for(let q=left&masks[+a[i]];q;){let b=q&-q;q^=b;match.push(31-Math.clz32(b));if(assign(i+1,left^b))return true;match.pop()}return false}
  if(!assign(0,m))throw Error("Hall mismatch");
  const reach=Array.from({length:n+1},(_,i)=>1<<i);for(let i=0;i<n;i++){for(let j=0;j<n;j++)if(masks[+a[i]]>>match[j]&1)reach[i]|=1<<j;if(masks[+a[i]]>>blank&1)reach[i]|=1<<n}
  for(let j=0;j<=n;j++)for(let i=0;i<=n;i++)if(reach[i]>>j&1)reach[i]|=reach[j];
  let sinks=0,seen=0;for(let i=0;i<n;i++)if(!(seen>>i&1)){let component=0;for(let j=0;j<=n;j++)if((reach[i]>>j&1)&&(reach[j]>>i&1))component|=1<<j;seen|=component;if(reach[i]===component)sinks++}
  let pack=Array(1<<n).fill(0);for(let s=1;s<1<<n;s++)for(const t of tight)if((s&t)===t)pack[s]=Math.max(pack[s],1+pack[s^t]);if(sinks!==pack[(1<<n)-1])throw Error("packing mismatch");
  checked++;hist[sinks]=(hist[sinks]||0)+1;examples[sinks]??={a,m,matching:match,blank};
 }
 for(let m=1;m<256;m++){let n=pop[m]-1;function gen(a,c){if(a.length===n){inspect(a,m);return}for(let j=c;j<6;j++)gen(a+j,j)}gen("",0)}
 return {checked,hist,examples};
}
function auditEdgeTerminalStructure(){
 const L=["DL","BL","FL","UL","DB","DF","UB","UF","DR","BR","FR","UR"],colors="URFDLB",n=L.length;
 let hist={},checks=0,examples={};const reasons={};
 function inspect(ids,blank,sides){
  const singles=ids.filter(i=>i!==blank),obs=singles.map((i,j)=>colors.indexOf(L[i][sides[j]])),f=Array(6).fill(0);for(const c of obs)f[c]++;
  const F=f.reduce((p,k)=>p*(k>=3?6:k===2?2:1),1);
  const edges=singles.map((i,j)=>[obs[j],colors.indexOf(L[i][sides[j]^1])]);
  const cycles=new Map();for(let start=0;start<6;start++){
   function walk(v,seen,mask,len){for(let j=0;j<edges.length;j++)if(edges[j][0]===v){const w=edges[j][1];if(w===start&&len+1>=2)cycles.set(mask|1<<j,len+1);else if(!(seen>>w&1))walk(w,seen|1<<w,mask|1<<j,len+1);}}
   walk(start,1<<start,0,0)
  }
  const even=[...cycles].filter(([_,l])=>l%2===0),odd=[...cycles].filter(([_,l])=>l%2===1);
  let predicted=false,reason="";
  if(F>2)reason="multiplicity";
  else if(blank<0){
   if(F===2){predicted=even.length===0&&!odd.some(([a],i)=>odd.slice(i+1).some(([b])=>!(a&b)));reason=predicted?"duplicate-unique-flip":"duplicate-flip-cycle";}
   else{predicted=even.length<=1&&odd.length<=1;reason=predicted?"distinct-cycle-limit":"distinct-cycle-excess";}
  }else{
   const hits=[...L[blank]].map(c=>colors.indexOf(c)).filter(c=>f[c]>0);
   if(F===2){predicted=hits.length===0&&cycles.size===0;reason=predicted?"duplicate-unique-blank":"duplicate-blank-or-cycle";}
   else if(hits.length===0){predicted=cycles.size===0||(cycles.size===1&&even.length===1);reason=predicted?"blank-isolated":"blank-isolated-cycles";}
   else if(hits.length===1){const j=edges.findIndex(e=>e[0]===hits[0]);predicted=f[edges[j][1]]===0&&cycles.size===0;reason=predicted?"one-blank-swap":"blank-path-or-cycle";}
   else reason="two-blank-swaps";
  }
  let c=[0,0];const req=new Map(singles.map((i,j)=>[i,sides[j]]));
  function rec(i,used,p,r){if(c[0]>=2&&c[1]>=2)return;if(i===ids.length){if(r===0)c[p]=Math.min(2,c[p]+1);return}const row=ids[i];for(let j=0;j<ids.length;j++)if(!(used>>j&1)){let q=0;for(let k=j+1;k<ids.length;k++)q^=used>>k&1;for(let t=0;t<2;t++)if(!req.has(row)||L[ids[j]][req.get(row)^t]===L[row][req.get(row)])rec(i+1,used|1<<j,p^q,r^t)}}
  rec(0,0,0,0);if(predicted!==c.every(x=>x<=1))throw Error(JSON.stringify({ids,blank,sides,c,predicted,reason,edges,cycles:[...cycles]}));
  const key=(blank<0?"noBlank":"oneBlank")+":"+ids.length;hist[key]??=[0,0];hist[key][+predicted]++;checks++;reasons[reason]=(reasons[reason]||0)+1;examples[reason]??={ids:ids.map(i=>L[i]),blank:blank<0?null:L[blank],sides,c};
 }
 for(let mask=1;mask<1<<n;mask++){const ids=L.map((_,i)=>i).filter(i=>mask>>i&1);if(ids.length>6)continue;for(const b of [-1,...ids]){let k=ids.length-(b<0?0:1);for(let s=0;s<1<<k;s++)inspect(ids,b,Array.from({length:k},(_,j)=>s>>j&1));}}
 if(checks!==353972||hist["noBlank:5"][1]!==16536||hist["oneBlank:4"][1]!==8904)throw Error("terminal structure regression");
 return {checks,hist,reasons,examples};
}
function edgeTerminalStructure(edges,blank){
 const colors=[...new Set([...edges.flat(),...blank??[]])],f=new Map();for(const [u] of edges)f.set(u,(f.get(u)||0)+1);
 const dup=[...f.values()].filter(x=>x===2).length;if(dup>1||[...f.values()].some(x=>x>=3))return [false,"multiplicity"];
 const cycles=new Map();for(const start of colors){function walk(v,seen,mask,len){for(let j=0;j<edges.length;j++)if(edges[j][0]===v){const w=edges[j][1];if(w===start&&len+1>=2)cycles.set(mask|1<<j,len+1);else if(!seen.includes(w))walk(w,[...seen,w],mask|1<<j,len+1)}}walk(start,[start],0,0)}
 const even=[...cycles].filter(([_,l])=>l%2===0),odd=[...cycles].filter(([_,l])=>l%2===1);
 if(!blank){if(dup)return [even.length===0&&!odd.some(([a],i)=>odd.slice(i+1).some(([b])=>!(a&b))),"duplicate/no-blank"];return [even.length<=1&&odd.length<=1,"distinct/no-blank"]}
 const hits=blank.filter(c=>f.has(c));if(dup)return [hits.length===0&&cycles.size===0,"duplicate/blank"];
 if(!hits.length)return [cycles.size===0||cycles.size===1&&even.length===1,"distinct/isolated-blank"];
 if(hits.length===1)return [!f.has(edges.find(e=>e[0]===hits[0])[1])&&cycles.size===0,"distinct/one-swap"];
 return [false,"distinct/two-swaps"];
}
function edgeTerminalReference(record,labels){
 const remain=[],used=new Set();let flip=0;
 for(const [i,[a,b]] of record.entries())if(a&&b){const j=labels.findIndex(l=>l===a+b||l===b+a);if(j<0||used.has(j))throw Error("invalid full record");used.add(j);flip^=+(labels[j]!==a+b)}else remain.push(i);
 let edges=[],blank=null;
 function search(k,r){if(k===remain.length)return r===0;const [a,b]=record[remain[k]];for(let j=0;j<labels.length;j++)if(!used.has(j))for(let t=0;t<2;t++){const l=labels[j],u=l[t],v=l[t^1];if(a&&a!==u||b&&b!==v)continue;used.add(j);if(!a&&!b){if(blank)throw Error("two blanks");blank=[u,v]}else edges.push(a?[u,v]:[v,u]);if(search(k+1,r^t))return true;if(!a&&!b)blank=null;else edges.pop();used.delete(j)}return false}
 if(!search(0,flip))throw Error("infeasible leaf");
 return edgeTerminalStructure(edges,blank);
}
function auditPinnedStructuralTerminals(cert){
 const labels=["DL","BL","FL","UL","DB","DF","UB","UF","DR","BR","FR","UR"];let leaves=0,nodes=0,hist={};
 for(const e of cert.representatives){const rec=[...e.prefix].map(c=>[c,null]);rec.push([null,null]);function visit(i){nodes++;const node=e.nodes[i];if(node[0]==="leaf"){leaves++;const [ok,reason]=edgeTerminalReference(rec,labels);if(!ok)throw Error("structural leaf "+i);hist[reason]=(hist[reason]||0)+1;return}if(node[0]==="repeat"){visit(node[1]);return}const q=node[1],r=q<11?q:11,c=q===11?0:1,old=rec[r][c];for(const [v,j] of Object.entries(node[2])){rec[r][c]=v;visit(j)}rec[r][c]=old}visit(0)}
 if(leaves!==73962||nodes!==141097)throw Error("pinned counts");return {leaves,nodes,hist};
}
function auditEdgeCoordinateTransport(states,syms,E,roots){
 const parity=a=>{let p=0;for(let i=0;i<a.length;i++)for(let j=i+1;j<a.length;j++)p^=+(a[i]>a[j]);return p;};
 const index=(a,b)=>E.findIndex(e=>e.includes(a)&&e.includes(b));
 const all=4095;
 function gauge(pi){
  let r=0;for(const e of E){let u=pi[e[0]],v=pi[e[1]],l=index(u,v);if(l<0)throw Error("color automorphism");r^=E[l].indexOf(u);}
  return r;
 }
 function normalize(rec,pi){
  let r=gauge(pi),m=all,rows=[],blank=-1;
  for(let i=0;i<12;i++){
   const [a,b]=rec[i],u=a<0?-1:pi[a],v=b<0?-1:pi[b];
   if(u>=0&&v>=0){const l=index(u,v);if(l<0||!(m>>l&1))throw Error("resolved label");m^=1<<l;r^=E[l].indexOf(u);}
   else if(u>=0||v>=0){rows.push({c:u>=0?u:v,i,side:u>=0?0:1});r^=+(u<0);}
   else {if(blank>=0)throw Error("multiple blanks");blank=i;}
  }
  rows.sort((a,b)=>a.c-b.c||a.i-b.i);
  return {a:rows.map(x=>x.c).join(""),m,r:blank>=0?0:r,rawR:r,rows,blank};
 }
 function decode(rec,sign){
  let matches=[],p=[],t=[];
  function visit(i,mask,flip){
   if(i===12){if(!flip&&parity(p)===sign)matches.push([p.join(","),t.join("")]);return;}
   for(let l=0;l<12;l++)if(!(mask>>l&1))for(let s=0;s<2;s++){
    if(rec[i].some((c,j)=>c>=0&&c!==E[l][s^j]))continue;
    p.push(l);t.push(s);visit(i+1,mask|1<<l,flip^s);p.pop();t.pop();
   }
  }visit(0,0,0);return matches;
 }
 let runs=0,transitions=0,blankReads=0,nonzeroBlank=0,sideOneSingletons=0,mutantRejected=0,signs=[0,0],hist={},seenRoots=new Set(),seenHist=new Set(),seenStates=new Set();
 function run(p,t){
  const rec=Array.from({length:12},(_,i)=>[i<11?E[p[i]][t[i]]:-1,-1]);
  const raw=rec.slice(0,11).map(x=>x[0]).sort((a,b)=>a-b).join("");
  const variants=syms.map(pi=>({pi,a:rec.slice(0,11).map(x=>pi[x[0]]).sort((a,b)=>a-b).join("")})).sort((a,b)=>a.a.localeCompare(b.a));
  const {pi,a}=variants[0];if(!roots.has(a))throw Error("root");
  seenRoots.add(a);seenHist.add(raw);let d=8;
  while(true){
   const s=normalize(rec,pi),k=s.a+":"+s.m+":"+s.r+":"+d,q=states.get(k);seenStates.add(k);
   if(!q)throw Error("policy lookup "+k);
   if(q==="leaf"){
    const sign=parity(p),matches=decode(rec,sign);if(matches.length!==1||matches[0][0]!==p.join(",")||matches[0][1]!==t.join(""))throw Error("raw decode");
    signs[sign]++;hist[19-d]=(hist[19-d]||0)+1;runs++;return;
   }
   if(d<=0)throw Error("budget");
   let i,side,expectedA,expectedM=s.m,expectedR;
   if(q[0]==="b"){
    i=s.blank;if(i<0)throw Error("no blank");side=+q[1]^s.rawR;const c=pi[E[p[i]][t[i]^side]];
    expectedA=[...s.a,String(c)].sort().join("");expectedR=+q[1];
    blankReads++;if(s.rawR){nonzeroBlank++;const other=pi[E[p[i]][t[i]^+q[1]]];if(other===c)throw Error("distinct endpoints");mutantRejected++;}
   }else{
    const row=s.rows.find(x=>x.c===+q[1]);if(!row)throw Error("singleton");i=row.i;side=row.side^1;sideOneSingletons+=row.side;
    const l=index(pi[E[p[i]][0]],pi[E[p[i]][1]]);expectedM^=1<<l;const j=s.a.indexOf(String(row.c));expectedA=s.a.slice(0,j)+s.a.slice(j+1);expectedR=s.blank>=0?0:s.r^E[l].indexOf(row.c);
   }
   if(rec[i][side]>=0)throw Error("repeat");rec[i][side]=E[p[i]][t[i]^side];d--;transitions++;
   const u=normalize(rec,pi);if(u.a!==expectedA||u.m!==expectedM||u.r!==expectedR)throw Error("transport transition "+JSON.stringify({s,q,u,expectedA,expectedM,expectedR}));
  }
 }
 // Construct a real raw arrangement for every feasible first-color histogram.
 let feasible=0;function gen(a,c){if(a.length===11){let p=[],t=[];function assign(i,mask,r){if(i===11){let l=31-Math.clz32(all^mask);p.push(l);t.push(r);return true;}for(let l=0;l<12;l++)if(!(mask>>l&1)&&E[l].includes(+a[i])){let s=E[l].indexOf(+a[i]);p.push(l);t.push(s);if(assign(i+1,mask|1<<l,r^s))return true;p.pop();t.pop();}return false;}if(assign(0,0,0)){feasible++;run(p,t);}return;}for(let j=c;j<6;j++)gen(a+j,j);}gen("",0);
 let seed=0x6a09e667;function next(n){seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return (seed>>>0)%n;}
 for(let k=0;k<12000;k++){let p=E.map((_,i)=>i);for(let i=11;i>0;i--){let j=next(i+1);[p[i],p[j]]=[p[j],p[i]];}let t=Array.from({length:11},()=>next(2));t.push(t.reduce((a,b)=>a^b,0));run(p,t);}
 if(feasible!==1362||seenRoots.size!==52||seenHist.size!==1362||runs!==13362||!nonzeroBlank||!signs.every(Boolean))throw Error("transport coverage");
 return {runs,feasibleHistograms:feasible,representatives:seenRoots.size,visitedDagStates:seenStates.size,transitions,blankReads,nonzeroBlank,sideOneSingletons,mutantRejected,signs,readHistogram:hist};
}
function buildStructuralEdgePolicy(checkTransport=false,checkExpected=false){
 const labels=["DL","BL","FL","UL","DB","DF","UB","UF","DR","BR","FR","UR"],colors="URFDLB",E=labels.map(l=>[...l].map(c=>colors.indexOf(c))),N=4096,all=N-1,pop=Array.from({length:N},(_,m)=>m.toString(2).replace(/0/g,"").length),cm=Array.from({length:6},(_,c)=>E.reduce((a,l,i)=>a|(l.includes(c)?1<<i:0),0));
 const groups=[[0,3],[1,4],[2,5]],syms=[];for(let i=0;i<3;i++)for(let j=0;j<3;j++)if(i!==j)for(let f=0;f<8;f++){let p=[];for(let k=0;k<3;k++)for(let t=0;t<2;t++)p[groups[k][t]]=groups[[i,j,3-i-j][k]][t^(f>>k&1)];syms.push(p)}
 function terminal(edges,blank){
  let f=Array(6).fill(0);for(const [u] of edges)f[u]++;
  let dup=f.filter(x=>x===2).length;if(dup>1||f.some(x=>x>=3))return false;
  const cycles=new Map();for(let s=0;s<6;s++){function walk(v,seen,mask,len){for(let j=0;j<edges.length;j++)if(edges[j][0]===v){let w=edges[j][1];if(w===s&&len+1>=2)cycles.set(mask|1<<j,len+1);else if(!(seen>>w&1))walk(w,seen|1<<w,mask|1<<j,len+1)}}walk(s,1<<s,0,0)}
  let even=[...cycles].filter(([_,l])=>l%2===0),odd=[...cycles].filter(([_,l])=>l%2===1);
  if(!blank)return dup?even.length===0&&!odd.some(([a],i)=>odd.slice(i+1).some(([b])=>!(a&b))):even.length<=1&&odd.length<=1;
  let hits=blank.filter(c=>f[c]);if(dup)return !hits.length&&!cycles.size;
  if(!hits.length)return !cycles.size||cycles.size===1&&even.length===1;
  if(hits.length===1)return !f[edges.find(e=>e[0]===hits[0])[1]]&&!cycles.size;
  return false;
 }
 const status=new Map(),memo=new Map();let searchCalls=0;
 const norm=(a,m,r)=>pop[m]>a.length?0:r;
 const key=(a,m,r)=>a+":"+m+":"+norm(a,m,r);
 function classify(a,m,r){
  r=norm(a,m,r);const k=key(a,m,r);if(status.has(k))return status.get(k);const blank=pop[m]-a.length;let edges=[],b=null;
  function ref(i,left,t){if(i===a.length){if(blank){if(pop[left]!==1)return false;b=E[31-Math.clz32(left)];return true;}return !left&&t===r}
   let c=+a[i];for(let q=left&cm[c];q;){let bit=q&-q;q^=bit;let l=31-Math.clz32(bit),s=E[l].indexOf(c);edges.push([c,E[l][s^1]]);if(ref(i+1,left^bit,t^s))return true;edges.pop()}return false
  }
  let out=ref(0,m,0)?terminal(edges,b)?2:1:0;status.set(k,out);return out;
 }
 function actions(a,m,r){r=norm(a,m,r);let arr=[],blank=pop[m]>a.length;
  for(let i=0;i<a.length;i++)if(!i||a[i]!==a[i-1]){let c=+a[i],ch=[],b=a.slice(0,i)+a.slice(i+1);for(let q=m&cm[c];q;){let bit=q&-q;q^=bit;let l=31-Math.clz32(bit),rr=norm(b,m^bit,r^E[l].indexOf(c));if(classify(b,m^bit,rr))ch.push([l,b,m^bit,rr]);}
   arr.push({q:"s"+c,ch,priority:10*[...a].filter(x=>+x===c).length-ch.length})}
  if(blank)for(let s=0;s<2;s++){let ch=[];for(let c=0;c<6;c++){let b=[...a,String(c)].sort().join(""),rr=r^s;if(classify(b,m,rr))ch.push([c,b,m,rr])}arr.push({q:"b"+s,ch,priority:15-ch.length})}
  return arr.sort((x,y)=>y.priority-x.priority||x.q.localeCompare(y.q))
 }
 function win(a,m,r,d){
  r=norm(a,m,r);let s=classify(a,m,r);if(!s)return true;if(s===2)return true;if(!d)return false;let k=key(a,m,r)+":"+d;if(memo.has(k))return memo.get(k)!==null;
  searchCalls++;let acts=actions(a,m,r);for(const act of acts)if(act.ch.every(([,b,mm,rr])=>win(b,mm,rr,d-1))){memo.set(k,act.q);return true}memo.set(k,null);return false
 }
 const roots=new Set();function gen(a,c){if(a.length===11){if(classify(a,all,0)){let b=syms.map(p=>[...a].map(x=>p[+x]).sort().join("")).sort()[0];roots.add(b)}return}for(let j=c;j<6;j++)gen(a+j,j)}gen("",0);
 let lost=[];for(const a of roots)if(!win(a,all,0,8))lost.push(a);
 if(lost.length)return {roots:roots.size,lost,searchCalls,status:status.size};
 let states=new Map(),arcs=0,leaves=0,hist={},treeNodes=0;
 function collect(a,m,r,d){r=norm(a,m,r);let k=key(a,m,r)+":"+d;if(states.has(k))return;let s=classify(a,m,r);hist[d]=(hist[d]||0)+1;if(s===2){states.set(k,"leaf");leaves++;return}const q=memo.get(k),act=actions(a,m,r).find(x=>x.q===q);if(!act)throw Error("policy "+k+" "+q);states.set(k,q);arcs+=act.ch.length;for(const [,b,mm,rr] of act.ch)collect(b,mm,rr,d-1)}
 for(const a of roots)collect(a,all,0,8);
 function tree(a,m,r,d){r=norm(a,m,r);let s=classify(a,m,r);if(s===2)return 1;let k=key(a,m,r)+":"+d,act=actions(a,m,r).find(x=>x.q===memo.get(k));return 1+act.ch.reduce((s,[,b,mm,rr])=>s+tree(b,mm,rr,d-1),0)}
 for(const a of roots)treeNodes+=tree(a,all,0,8);
 // Independent capped sign-count recurrence; no graph terminal predicate.
 const C=new Map();
 function counts(a,m,r){r=norm(a,m,r);const k=key(a,m,r);if(C.has(k))return C.get(k);const blank=pop[m]-a.length;let out=[0,0];
  if(blank<0||blank>1)return out;
  if(!a.length){if(blank===1||!m&&r===0)out=[1,0]}
  else{const c=+a[0];for(let q=m&cm[c];q;){const bit=q&-q;q^=bit;const l=31-Math.clz32(bit),ch=counts(a.slice(1),m^bit,r^E[l].indexOf(c)),p=pop[m&(bit-1)]&1;for(let s=0;s<2;s++)out[s]=Math.min(2,out[s]+ch[s^p]);}}
  C.set(k,out);return out;
 }
 const keys=[...states.keys()];let checkedArcs=0,checkedLeaves=0,rootMass=0;
 function verify(){
  const seen=new Set();let vArcs=0,vLeaves=0;
  function visit(k){if(seen.has(k))return;seen.add(k);const [a,ms,rs,ds]=k.split(":"),m=+ms,r=+rs,d=+ds,q=states.get(k),z=counts(a,m,r);
   if(!z.some(Boolean)||q===undefined)throw Error("uncovered/infeasible");
   if(q==="leaf"){if(z.some(x=>x>1))throw Error("wrong terminal");vLeaves++;return}
   if(d<=0)throw Error("budget");let expected=[];
   if(q[0]==="b"){if(pop[m]!==a.length+1||!["b0","b1"].includes(q))throw Error("blank action");for(let c=0;c<6;c++){let aa=[...a,String(c)].sort().join(""),rr=r^+q[1];if(counts(aa,m,rr).some(Boolean))expected.push(key(aa,m,rr)+":"+(d-1));}}
   else if(q[0]==="s"){const c=+q[1],i=a.indexOf(String(c));if(i<0)throw Error("singleton action");const aa=a.slice(0,i)+a.slice(i+1);for(let l=0;l<12;l++)if((m>>l&1)&&E[l].includes(c)){const mm=m^(1<<l),rr=r^E[l].indexOf(c);if(counts(aa,mm,rr).some(Boolean))expected.push(key(aa,mm,rr)+":"+(d-1));}}
   else throw Error("action type");
   const actual=actions(a,m,r).find(x=>x.q===q).ch.map(([,aa,mm,rr])=>key(aa,mm,rr)+":"+(d-1));
   if(!expected.length||expected.sort().join("|")!==actual.sort().join("|"))throw Error("reply coverage");
   for(const child of expected){vArcs++;visit(child)}
  }
  for(const a of roots)visit(key(a,all,0)+":8");if(seen.size!==states.size)throw Error("unreachable records");return [vArcs,vLeaves];
 }
 [checkedArcs,checkedLeaves]=verify();
 function checkRoots(a,c){if(a.length===11){let feasible=counts(a,all,0).some(Boolean);if(feasible!==Boolean(classify(a,all,0)))throw Error("root feasibility");if(feasible){rootMass++;let b=syms.map(p=>[...a].map(x=>p[+x]).sort().join("")).sort()[0];if(!roots.has(b))throw Error("root coverage");}return}for(let j=c;j<6;j++)checkRoots(a+j,j)}checkRoots("",0);
 const rootKey=key([...roots][0],all,0)+":8",saved=states.get(rootKey);states.set(rootKey,"leaf");let rejected=false;try{verify()}catch{rejected=true}states.set(rootKey,saved);
 if(!rejected||rootMass!==1362||checkedArcs!==arcs||checkedLeaves!==leaves)throw Error("verification regression");

 // Optional exact uniform-state expectation under the fixed eleven-first,
 // at-most-eight continuation grammar. No sampling or floating probabilities.
 const expectedCost=checkExpected?(()=>{
  const M=new Map(),V=new Map(),B=new Map(),chosen=new Map();
  function mass(a,m,r){
   r=norm(a,m,r);const k=key(a,m,r);if(M.has(k))return M.get(k);let z=0;
   if(!a.length)z=pop[m]===1||!m&&!r?1:0;
   else{const c=+a[0];for(let q=m&cm[c];q;){const bit=q&-q;q^=bit;z+=mass(a.slice(1),m^bit,r^E[31-Math.clz32(bit)].indexOf(c))}}
   M.set(k,z);return z;
  }
  function dist(a,m,r,d,opt){
   r=norm(a,m,r);const k=key(a,m,r)+":"+d,cache=opt?V:B;
   if(cache.has(k))return cache.get(k);const z=mass(a,m,r),s=classify(a,m,r);
   if(!z||!s)throw Error("mass feasibility");
   if(s===2){if(z>2||counts(a,m,r).some(x=>x>1))throw Error("terminal sign mass");const out=[z];cache.set(k,out);if(opt)chosen.set(k,"leaf");return out}
   if(!d)throw Error("budget");
   let best=null,bestCost=Infinity,bestQ=null;
   for(const act of actions(a,m,r)){
    if(opt?!act.ch.every(([,b,mm,rr])=>win(b,mm,rr,d-1)):act.q!==memo.get(k))continue;
    const out=Array(d+1).fill(0);
    for(const [,b,mm,rr] of act.ch){const ch=dist(b,mm,rr,d-1,opt);for(let i=0;i<ch.length;i++)out[i+1]+=ch[i]}
    if(out.reduce((a,b)=>a+b,0)!==z)throw Error("branch mass");
    const cost=out.reduce((s,n,i)=>s+n*i,0);
    if(cost<bestCost){best=out;bestCost=cost;bestQ=act.q}
   }
   if(!best)throw Error("missing policy");
   cache.set(k,best);if(opt)chosen.set(k,bestQ);return best;
  }
  const fact=n=>n<2?1:n*fact(n-1);
  const base=Array(20).fill(0),optimal=Array(20).fill(0);
  let rootMassExact=0,representativeMass=0,improvedRoots=0;
  for(const a of roots){
   const h=Array(6).fill(0);for(const c of a)h[+c]++;
   const orbit=new Set(syms.map(p=>[...a].map(c=>p[+c]).sort().join(""))).size;
   const w=orbit*fact(11)/h.reduce((s,n)=>s*fact(n),1);
   const b=dist(a,all,0,8,false),v=dist(a,all,0,8,true),z=mass(a,all,0);
   if(b.reduce((s,n,i)=>s+n*i,0)>v.reduce((s,n,i)=>s+n*i,0))improvedRoots++;
   rootMassExact+=w*z;representativeMass+=z;
   for(let i=0;i<b.length;i++)base[11+i]+=w*b[i];
   for(let i=0;i<v.length;i++)optimal[11+i]+=w*v[i];
  }
  const total=fact(12)*2048;
  if(rootMassExact!==total||representativeMass!==144736||base.reduce((a,b)=>a+b,0)!==total||optimal.reduce((a,b)=>a+b,0)!==total)throw Error("weighted mass");
  // Replay the selected policy using the independent capped sign counter
  // to generate all feasible replies, not the structural search predicate.
  const replay=new Map();let replayArcs=0;
  function visit(a,m,r,d){
   r=norm(a,m,r);const k=key(a,m,r)+":"+d;if(replay.has(k))return replay.get(k);
   const q=chosen.get(k),z=mass(a,m,r),s=counts(a,m,r);let out;
   if(!z||!s.some(Boolean)||q===undefined)throw Error("optimized replay state");
   if(q==="leaf"){if(s.some(x=>x>1))throw Error("optimized replay leaf");out=[z]}
   else{
    if(!d)throw Error("optimized replay budget");const ch=[];
    if(q[0]==="b"){if(pop[m]!==a.length+1||!["b0","b1"].includes(q))throw Error("blank");for(let c=0;c<6;c++){let aa=[...a,String(c)].sort().join(""),rr=r^+q[1];if(counts(aa,m,rr).some(Boolean))ch.push([aa,m,rr])}}
    else if(q[0]==="s"){const c=+q[1],i=a.indexOf(String(c));if(i<0)throw Error("singleton");const aa=a.slice(0,i)+a.slice(i+1);for(let l=0;l<12;l++)if((m>>l&1)&&E[l].includes(c)){let mm=m^(1<<l),rr=r^E[l].indexOf(c);if(counts(aa,mm,rr).some(Boolean))ch.push([aa,mm,rr])}}
    else throw Error("action");
    out=Array(d+1).fill(0);for(const [aa,mm,rr] of ch){replayArcs++;const v=visit(aa,mm,rr,d-1);for(let i=0;i<v.length;i++)out[i+1]+=v[i]}
   }
   if(out.reduce((a,b)=>a+b,0)!==z||out.join(",")!==V.get(k).join(","))throw Error("optimized replay mass");
   replay.set(k,out);return out;
  }
  for(const a of roots)visit(a,all,0,8);
  const summarize=h=>({hist:Object.fromEntries(h.map((n,i)=>[i,n]).filter(x=>x[1])),totalCost:h.reduce((s,n,i)=>s+n*i,0),mean:h.reduce((s,n,i)=>s+n*i,0)/total});
  return {total,representativeMass,improvedRoots,baseline:summarize(base),optimal:summarize(optimal),massStates:M.size,baselineStates:B.size,optimalStates:V.size,replayStates:replay.size,replayArcs,rawTransport:auditEdgeCoordinateTransport(chosen,syms,E,roots)};
 })():null;

 const transport=checkTransport?auditEdgeCoordinateTransport(states,syms,E,roots):null;
 return {roots:roots.size,rootMass,searchCalls,status:status.size,dagNodes:states.size,arcs,leaves,hist,treeNodes,checkedArcs,checkedLeaves,negativeControl:rejected,countStates:C.size,decisionTableChars:JSON.stringify([...states]).length,transport,expectedCost};
}
function auditOppositeSignCoverWitness(){
 const E0=["DL","BL","FL","UL","DB","DF","UB","UF","DR","BR","FR","UR"].map(l=>[...l].map(c=>"URFDLB".indexOf(c)));
 let records=0,graphs=0,cube=0,minimum=Infinity,coverCases=0,types={};
 function check(E,v,isCube=false){
  const n=E.length;if(n<3)return;graphs++;
  for(let S=1;S<1<<v;S++){
   const internal=E.map((e,i)=>e.every(c=>S>>c&1)?i:-1).filter(i=>i>=0);
   if(!internal.length||E.some(e=>e.every(c=>!(S>>c&1))))continue;
   const k=S.toString(2).replace(/0/g,"").length;
   if(isCube&&k!==4)continue;coverCases++;
   for(const blank of [-1,...internal]){
    const count=k+(blank<0?2:0);if(count>n-(blank>=0?1:0))continue;
    const rows=[],sides=[];
    function verify(){
     let witnesses=0;
     function swap(i,j){
      // Reference identity, zero orientation. Compute orientations after exchanging two labels.
      const newFlip=[];
      for(const [row,l] of [[i,j],[j,i]]){
       const t=rows.indexOf(row);if(t<0){newFlip.push(null);continue;}
       const side=sides[t],c=E[row][side],p=E[l].indexOf(c);if(p<0)return;
       newFlip.push(p^side);
      }
      if(newFlip.includes(null))newFlip[newFlip.indexOf(null)]=newFlip.find(x=>x!==null);
      if(newFlip[0]!==newFlip[1])return;
      for(let z=0;z<2;z++){let row=[i,j][z],l=[j,i][z],t=rows.indexOf(row);if(t>=0&&E[l][sides[t]^newFlip[z]]!==E[row][sides[t]])throw Error("swap witness");}
      witnesses++;
     }
     for(let i=0;i<rows.length;i++){for(let j=i+1;j<rows.length;j++)swap(rows[i],rows[j]);if(blank>=0)swap(rows[i],blank);}
     if(witnesses<2)throw Error(JSON.stringify({E,S,blank,rows,sides,witnesses}));
     minimum=Math.min(minimum,witnesses);records++;if(isCube)cube++;const key=(isCube?"cube":"small")+":"+(blank<0?"noBlank":"oneBlank");types[key]=(types[key]||0)+1;
    }
    function gen(i){if(rows.length===count){verify();return}if(i===n||n-i<count-rows.length)return;if(i===blank){gen(i+1);return}gen(i+1);for(let s=0;s<2;s++)if(S>>E[i][s]&1){rows.push(i);sides.push(s);gen(i+1);sides.pop();rows.pop()}}
    gen(0);
   }
  }
 }
 for(let v=2;v<=4;v++){let E=[];for(let i=0;i<v;i++)for(let j=i+1;j<v;j++)E.push([i,j]);for(let m=1;m<1<<E.length;m++)check(E.filter((_,i)=>m>>i&1),v)}
 check(E0,6,true);
 return {graphs,coverCases,records,cube,minimum,types};
}
function auditRepresentativeMass(){
 const labels=["DL","BL","FL","UL","DB","DF","UB","UF","DR","BR","FR","UR"],colors="URFDLB",pairs=[[0,3],[1,4],[2,5]],syms=[];
 for(let i=0;i<3;i++)for(let j=0;j<3;j++)if(i!==j)for(let f=0;f<8;f++){let p=[];for(let k=0;k<3;k++)for(let t=0;t<2;t++)p[pairs[k][t]]=pairs[[i,j,3-i-j][k]][t^(f>>k&1)];syms.push(p)}
 const pop=Array.from({length:4096},(_,i)=>i.toString(2).replace(/0/g,"").length),M=[...colors].map(c=>labels.reduce((m,l,i)=>m|(l.includes(c)?1<<i:0),0));
 const fact=n=>{let r=1;for(let i=2;i<=n;i++)r*=i;return r};
 function count(a){const memo=new Map();function go(i,m){if(i===11)return [1,0];if(memo.has(m))return memo.get(m);let out=[0,0];for(let q=m&M[a[i]];q;){const b=q&-q;q^=b;const p=pop[m&(b-1)]&1,z=go(i+1,m^b);out[0]+=z[p];out[1]+=z[p^1]}memo.set(m,out);return out}return go(0,4095)}
 const roots=new Map();let total=0,even=0,odd=0,feasible=0,rawWords=0;
 function gen(h,k){if(h.length===5){h=[...h,k];const a=h.flatMap((n,i)=>Array(n).fill(i)),z=count(a);if(!z[0]&&!z[1])return;feasible++;if(z[0]!==z[1])throw Error("unbalanced");const mult=fact(11)/h.reduce((p,n)=>p*fact(n),1);rawWords+=mult;even+=mult*z[0];odd+=mult*z[1];const orbit=new Set(syms.map(p=>p.map(i=>h[i]).join(","))),key=[...orbit].sort()[0];if(h.join(",")===key){roots.set(key,{size:orbit.size,weight:mult,candidates:z[0]+z[1],perSign:z[0]});total+=z[0]+z[1]}return}for(let i=0;i<=k;i++)gen([...h,i],k-i)}
 gen([],11);const weighted=[...roots.values()].reduce((s,r)=>s+r.size*r.weight*r.candidates,0),vals=[...roots.values()].map(r=>r.candidates).sort((a,b)=>a-b);
 if(roots.size!==52||feasible!==1362||total!==144736||weighted!==fact(12)*2048||even!==odd||even+odd!==weighted||rawWords!==297297000)throw Error("mass conservation");
 return {roots:roots.size,feasible,rawOrderedPrefixes:rawWords,unweightedRepresentativeCandidates:total,weighted,even,odd,min:vals[0],max:vals.at(-1),median:(vals[25]+vals[26])/2,byRepresentative:[...roots]};
}

function solveGraphClockMean(E,v,cap,release,trace=false){
 const n=E.length,N=1<<n,all=N-1,pop=new Uint8Array(N),cm=new Int32Array(v),side=Array.from({length:v},()=>new Uint8Array(n)),deg=new Uint8Array(v);
 for(let i=0;i<n;i++)for(let s=0;s<2;s++){const c=E[i][s];cm[c]|=1<<i;side[c][i]=s;deg[c]++}
 const gp=new Int32Array(v);let H=1;for(let c=0;c<v;c++){gp[c]=H;H*=deg[c]+1}
 const digits=new Uint8Array(H*v),sum=new Uint8Array(H),less=new Uint8Array(H*v),greater=new Uint8Array(H*v),dup=new Uint8Array(H);
 for(let h=0;h<H;h++){for(let c=0;c<v;c++){let q=Math.floor(h/gp[c])%(deg[c]+1);digits[h*v+c]=q;less[h*v+c]=sum[h];sum[h]+=q;if(q>=2)dup[h]=1}for(let c=0;c<v;c++)greater[h*v+c]=sum[h]-less[h*v+c]-digits[h*v+c]}
 const strides=new Int32Array(N*v),caps=new Uint8Array(N*v),off=new Int32Array(N+1);
 for(let m=0;m<N;m++){pop[m]=m?pop[m&(m-1)]+1:0;let p=1;for(let c=0;c<v;c++){let d=pop[m&cm[c]];caps[m*v+c]=d;strides[m*v+c]=p;p*=d+1}off[m+1]=off[m]+p}
 const M=new Float64Array(4*off[N]),C=new Float64Array(4*off[N]),U=release?new Float64Array(2*off[N]):null;
 const fact=n=>n<2?1:n*fact(n-1);let mc=0,cc=0,uc=0,losers=0;
 function key(h,m,r,p){let z=off[m];for(let c=0;c<v;c++){let d=digits[h*v+c];if(d>caps[m*v+c])return -1;z+=d*strides[m*v+c]}return 4*z+2*r+p}
 function mass(h,m,r,p){let b=pop[m]-sum[h];if(b<0)return 0;if(b>0)r=0;if(b>=2||dup[h])p=0;let k=key(h,m,r,p);if(k<0)return 0;if(M[k])return M[k]-1;mc++;let z=0;
  if(!h){if(b>=2)z=fact(b)*2**(b-2);else if(!p&&(b===1||!r))z=1}
  else{let c=0;while(!digits[h*v+c])c++;for(let q=m&cm[c];q;){let bit=q&-q;q^=bit;let l=31-Math.clz32(bit);z+=mass(h-gp[c],m^bit,r^side[c][l],p^(pop[m&(bit-1)]&1))}}
  M[k]=z+1;return z}
 function actions(h,m,r,known,visit){
  const b=pop[m]-sum[h];
  // Even permutations preserve the sector, odd permutations exchange sectors.
  // If two identical rows are available, distinguish their index parities.
  if(b>0)for(let j=0;j<(known&&b>=2?2:1);j++)for(let s=0;s<(b===1?2:1);s++){let ch=[];for(let c=0;c<v;c++)if(digits[h*v+c]<caps[m*v+c])ch.push([h+gp[c],m,r^s,(greater[h*v+c]+j)&1]);visit(ch)}
  for(let c=0;c<v;c++)if(digits[h*v+c])for(let j=0;j<(known&&digits[h*v+c]>=2?2:1);j++){let ch=[];for(let q=m&cm[c];q;){let bit=q&-q;q^=bit;let l=31-Math.clz32(bit);ch.push([h-gp[c],m^bit,r^side[c][l],(less[h*v+c]+j+pop[m&(bit-1)])&1])}visit(ch)}
 }
 function cost(h,m,r,p){let b=pop[m]-sum[h];if(b>0)r=0;if(b>=2||dup[h])p=0;let z=mass(h,m,r,p);if(z<=1)return 0;let d=cap-(2*n-2*pop[m]+sum[h]);if(d<=0)return Infinity;let k=key(h,m,r,p);if(C[k])return C[k]-1;cc++;let best=Infinity;
  actions(h,m,r,true,ch=>{let tot=z,ms=0;for(const [x,l,t,s] of ch){let w=mass(x,l,t,p^s);ms+=w;if(w)tot+=cost(x,l,t,p^s)}if(ms!==z)throw Error("known mass "+[h,m,r,p,z,ms]);best=Math.min(best,tot)});
  if(!Number.isFinite(best))losers++;C[k]=best+1;return best}
 function unknown(h,m,r){if(pop[m]>sum[h])r=0;let z0=mass(h,m,r,0),z1=mass(h,m,r,1),z=z0+z1;if(z<=1)return 0;
  let t=2*n-2*pop[m]+sum[h];if(t>=release||!z0||!z1)return cost(h,m,r,0)+cost(h,m,r,1);
  if(t>=cap)return Infinity;let k=key(h,m,r,0)/2;if(U[k])return U[k]-1;uc++;let best=Infinity;
  actions(h,m,r,false,ch=>{let tot=z,ms=0;for(const [x,l,t] of ch){let w=mass(x,l,t,0)+mass(x,l,t,1);ms+=w;if(w)tot+=unknown(x,l,t)}if(ms!==z)throw Error("unknown mass");best=Math.min(best,tot)});
  U[k]=best+1;return best}
 let z=[mass(0,all,0,0),mass(0,all,0,1)],costs=[cost(0,all,0,0),cost(0,all,0,1)],clock=release?unknown(0,all,0):costs[0]+costs[1];


 const symmetryAudit=trace==="symmetry"?(()=>{
  // Every ordered prefix with the same histogram has the same known-sign
  // continuation cost (sum over signs); multiply by its multinomial weight.
  let total=0,prefixCost=0,feasible=0,failed=0,balanced=0;
  for(let h=0;h<H;h++)if(sum[h]===n-1){
   let z0=mass(h,all,0,0),z1=mass(h,all,0,1),z=z0+z1;if(!z)continue;feasible++;
   if(z0===z1)balanced++;
   let w=fact(n-1);for(let c=0;c<v;c++)w/=fact(digits[h*v+c]);
   if(!Number.isInteger(w))throw Error("prefix weight");
   total+=w*z;let k=cost(h,all,0,0)+cost(h,all,0,1);
   if(!Number.isFinite(k))failed++;
   prefixCost+=w*(z*(n-1)+k);
  }
  if(total!==z[0]+z[1])throw Error("prefix mass");
  const stats={},witnesses=[];
  for(const t of [14,15,16])for(let blanks=0;blanks<=2;blanks++){
   const singles=2*n-t-2*blanks,k=singles+blanks;if(singles<0||k>n)continue;
   const st=stats[t+":"+blanks]={feasible:0,protected:0,finite:0,exception:0,forced:0,forcedMass:0,bothTerminal:0,oneTerminal:0};
   for(let m=0;m<N;m++)if(pop[m]===k){
    function gen(c,h,rem,groups){
     if(c===v){if(rem)return;let z0=mass(h,m,0,0),z1=mass(h,m,0,1);if(!z0||!z1)return;st.feasible++;
      // The known-sign group has an odd element fixing every single-row
      // action if a class has size >=3 or two classes have size >=2.
      let sizes=[blanks,...groups].sort((a,b)=>b-a),safe=sizes[0]>=3||sizes[1]>=2;
      if(safe)st.protected++;
      let early=cost(h,m,0,0)+cost(h,m,0,1);if(!Number.isFinite(early))return;st.finite++;
      if(safe){if(z0<=1||z1<=1)throw Error("protected terminal");return}
      st.exception++;if(z0===1&&z1===1)st.bothTerminal++;else if(z0===1||z1===1)st.oneTerminal++;
      let best=Infinity,opts=[],i=0;actions(h,m,0,false,ch=>{
       let c=z0+z1;for(const [x,l,t,s] of ch)c+=cost(x,l,t,0)+cost(x,l,t,1);
       best=Math.min(best,c);opts.push([i++,Number.isFinite(c)?c:null]);
      });
      if(best<early)throw Error("negative delta");
      if(best>early){st.forced++;st.forcedMass+=z0+z1;if(witnesses.length<6)witnesses.push({t,blanks,groups,remaining:E.filter((_,i)=>m>>i&1),mass:[z0,z1],early,best,opts})}
      return;
     }
     for(let d=0;d<=Math.min(rem,caps[m*v+c]);d++)gen(c+1,h+d*gp[c],rem-d,[...groups,d])
    }
    gen(0,0,singles,[]);
   }
  }
  return {prefix:{total,prefixCost,feasible,failed,balanced,mean:prefixCost/total,equalsUnrestricted:prefixCost===costs[0]+costs[1]},stats,witnesses};
 })():null;

 const regretTrace=trace===true&&release&&Number.isFinite(clock)?(()=>{
  const knownSum=(h,m,r)=>cost(h,m,r,0)+cost(h,m,r,1);
  const canonical=(h,m,r)=>[h,m,pop[m]>sum[h]?0:r];
  let layer=new Map([["0:"+all+":0",{s:[0,all,0],multiplicity:1}]]),totalRegret=0;
  const layers=[],examples=[];
  for(let t=0;t<release;t++){
   const next=new Map();let regret=0,positiveMass=0,positiveNodes=0,forcedNodes=0,visited=0;
   for(const {s:[h,m,r],multiplicity:k} of layer.values()){
    const z0=mass(h,m,r,0),z1=mass(h,m,r,1),z=z0+z1;
    if(!z0||!z1||z<=1)continue;
    visited++;
    const early=knownSum(h,m,r),target=unknown(h,m,r);
    let best=null,minDelta=Infinity,options=[],idx=0;
    actions(h,m,r,false,ch=>{
     let c=z,e=z,branches=[];
     for(const [x,l,t] of ch)if(mass(x,l,t,0)+mass(x,l,t,1)){
      c+=unknown(x,l,t);e+=knownSum(x,l,t);branches.push(canonical(x,l,t))
     }
     const delta=e-early;if(delta<0)throw Error("negative local regret");
     minDelta=Math.min(minDelta,delta);options.push({idx:idx++,delta,clock:c});
     if(c===target&&(!best||delta<best.delta))best={delta,branches};
    });
    if(!best||!Number.isFinite(best.delta))throw Error("no optimal clock action");
    if(best.delta){positiveNodes++;positiveMass+=k*z;regret+=k*best.delta;if(minDelta>0)forcedNodes++;
     if(examples.length<12)examples.push({t,colors:Array.from({length:v},(_,c)=>digits[h*v+c]),remainingLabels:E.filter((_,i)=>m>>i&1),flip:r,sectorMass:[z0,z1],early,chosenDelta:best.delta,minDelta,options,multiplicity:k})}
    for(const s of best.branches){const q=s.join(":");if(!next.has(q))next.set(q,{s,multiplicity:0});next.get(q).multiplicity+=k;}
   }
   if(visited)layers.push({t,visited,positiveNodes,forcedNodes,positiveMass,regret});
   totalRegret+=regret;layer=next;
  }
  if(totalRegret!==clock-costs[0]-costs[1])throw Error("regret telescoping");
  return {totalRegret,layers,examples};
 })():null;

 if(z[0]+z[1]!==fact(n)*2**(n-1)||n>=2&&(z[0]!==z[1]||costs[0]!==costs[1]))throw Error("root sign symmetry");
 return {n,v,cap,release,z,costs,means:costs.map((c,i)=>z[i]?c/z[i]:null),clock,clockMean:clock/(z[0]+z[1]),regretTrace,symmetryAudit,mc,cc,uc,losers,tableBytes:M.byteLength+C.byteLength+(U?.byteLength||0)}
}

 // Independent raw-coordinate check of the first genuine local conflict:
 // 18 explicitly enumerated residual arrangements, no quotient/gauge cache.
function auditRawClockConflict(){
 const E=[[3,4],[5,4],[2,4],[0,4],[3,2],[0,5],[3,1]],a=[1,2,3,4,4,5],n=E.length,states=[],p=[],tw=[];
 function gen(i,m,flip,parity){
  if(i===n){if(!flip)states.push({parity,stickers:p.flatMap((l,j)=>[E[l][tw[j]],E[l][tw[j]^1]])});return;}
  for(let l=0;l<n;l++)if(!(m>>l&1))for(let s=0;s<2;s++)if(i===a.length||E[l][s]===a[i]){
   let sign=0;for(let j=l+1;j<n;j++)sign^=m>>j&1;
   p.push(l);tw.push(s);gen(i+1,m|1<<l,flip^s,parity^sign);p.pop();tw.pop()
  }
 }
 gen(0,0,0,0);
 const init=a.reduce((m,_,i)=>m|1<<(2*i),0),memo=new Map();
 function evaluate(B,used,d){
  if(B.length<=1)return 0;if(!d)return Infinity;let k=B.join(",")+":"+used+":"+d;if(memo.has(k))return memo.get(k);
  let best=Infinity;for(let q=0;q<2*n;q++)if(!(used>>q&1))best=Math.min(best,first(B,used,d,q));memo.set(k,best);return best
 }
 function first(B,used,d,q){
  let g=new Map();for(const i of B){let v=states[i].stickers[q];if(!g.has(v))g.set(v,[]);g.get(v).push(i)}
  let z=B.length;for(const b of g.values())z+=evaluate(b,used|1<<q,d-1);return z
 }
 let B=[0,1].map(s=>states.map((x,i)=>x.parity===s?i:-1).filter(i=>i>=0)),cost=B.map(b=>evaluate(b,init,3)),actions=[];
 for(let q=0;q<2*n;q++)if(!(init>>q&1)){let c=B.map(b=>first(b,init,3,q));actions.push({row:q>>1,side:q&1,color:a[q>>1]??null,costs:c,combined:c[0]+c[1]})}
 let minimum=Math.min(...actions.map(x=>x.combined));if(B.some(b=>b.length!==9)||cost.join(",")!=="16,16"||minimum!==34)throw Error("raw conflict");
 return {counts:B.map(b=>b.length),cost,actions,minimum,memoStates:memo.size}
}

function auditRawGraphClock(E,cap,release){
 const n=E.length,states=[],p=[];
 function gen(m){if(!m){let s=0;for(let i=0;i<n;i++)for(let j=i+1;j<n;j++)s^=+(p[i]>p[j]);for(let t=0;t<1<<n;t++){let r=0;for(let i=0;i<n;i++)r^=t>>i&1;if(!r)states.push({s,a:p.flatMap((l,i)=>[E[l][t>>i&1],E[l][1^(t>>i&1)]])})}return}
  for(let q=m;q;){let bit=q&-q;q^=bit;p.push(31-Math.clz32(bit));gen(m^bit);p.pop()}}
 gen((1<<n)-1);const memo=new Map(),all=states.map((_,i)=>i);
 function cost(B,used,known){if(B.length<=1)return 0;let t=used.toString(2).replace(/0/g,"").length;if(!known&&t>=release)return cost(B.filter(i=>!states[i].s),used,true)+cost(B.filter(i=>states[i].s),used,true);if(t>=cap)return Infinity;
  const k=B.join(",")+":"+used+":"+known;if(memo.has(k))return memo.get(k);let best=Infinity;
  for(let q=0;q<2*n;q++)if(!(used>>q&1)){let g=new Map();for(const i of B){let a=states[i].a[q];if(!g.has(a))g.set(a,[]);g.get(a).push(i)}let c=B.length;for(const b of g.values())c+=cost(b,used|1<<q,known);best=Math.min(best,c)}
  memo.set(k,best);return best}
 const costs=[0,1].map(s=>cost(all.filter(i=>states[i].s===s),0,true));return {costs,clock:cost(all,0,false),states:states.length,memo:memo.size}
}
function auditGraphClockControls(){
 let controls=0;
 for(const E of [[[0,1]],[[0,1],[0,2]],[[0,1],[0,2],[1,2]],[[0,1],[1,2],[2,3]],[[0,1],[1,2],[2,3],[3,0]]]){
  const n=E.length,v=1+Math.max(...E.flat());
  for(let cap=0;cap<=2*n;cap++)for(const r of new Set([0,Math.min(2,cap),cap])){
   const q=solveGraphClockMean(E,v,cap,r),raw=auditRawGraphClock(E,cap,r);
   if(q.costs.join(",")!==raw.costs.join(",")||q.clock!==raw.clock)throw Error("raw clock mismatch "+JSON.stringify({E,q,raw}));
   controls++
  }
 }
 return {rawControls:controls}
}
function auditGraphClockMean(release=14,trace=false){
 const E=["DL","BL","FL","UL","DB","DF","UB","UF","DR","BR","FR","UR"].map(l=>[...l].map(c=>"URFDLB".indexOf(c)));
 return solveGraphClockMean(E,6,19,release,trace)
}


function starClockFormula(n,cap,r){
 const fact=n=>n<2?1:n*fact(n-1),binom=(n,k)=>fact(n)/(fact(k)*fact(n-k));
 const total=fact(n)*2**(n-1),base=fact(n);
 let cost=0,worst=0;
 for(let x=0;x<n;x++){
  let d=n-1+Math.max(0,x-1);if(x>0&&d<r)d++;
  cost+=base*binom(n-1,x)*d;worst=Math.max(worst,d)
 }
 return {cost:worst<=cap?cost:Infinity,worst,total,mean:worst<=cap?cost/total:null}
}
function auditStarClockFormula(){
 let cases=0,finite=0,summary=[];
 for(let n=2;n<=7;n++){
  const E=Array.from({length:n},(_,i)=>[0,i+1]);
  for(let cap=2*n-4;cap<=2*n-1;cap++)for(let r=0;r<=2*n;r++){
   const a=starClockFormula(n,cap,r),b=solveGraphClockMean(E,n+1,cap,r);
   if(a.cost!==b.clock)throw Error("star formula mismatch "+JSON.stringify({n,cap,r,a,b}));
   cases++;if(Number.isFinite(a.cost))finite++
  }
  summary.push({n,early:starClockFormula(n,2*n-2,0).mean,latestLossless:n-1,unknown:starClockFormula(n,2*n-2,2*n).mean,profile:Array.from({length:2*n+1},(_,r)=>starClockFormula(n,2*n-2,r).mean)})
 }
 if(cases!==240||finite!==162)throw Error("star census");
 return {cases,finite,summary}
}

if (process.argv.includes('--star-clock')) console.log(JSON.stringify(auditStarClockFormula(), null, 2));
else if (process.argv.includes('--graph-clock-controls')) console.log(JSON.stringify(auditGraphClockControls(), null, 2));
else if (process.argv.includes('--graph-clock-conflict')) console.log(JSON.stringify(auditRawClockConflict(), null, 2));
else if (process.argv.includes('--graph-clock-symmetry')) console.log(JSON.stringify(auditGraphClockMean(0,"symmetry"), null, 2));
else if (process.argv.includes('--graph-clock-regret')) console.log(JSON.stringify(auditGraphClockMean(Number(process.argv[process.argv.indexOf('--graph-clock-regret')+1]??17),true), null, 2));
else if (process.argv.includes('--graph-clock-mean')) console.log(JSON.stringify(auditGraphClockMean(Number(process.argv[process.argv.indexOf('--graph-clock-mean')+1]??14)), null, 2));
else if (process.argv.includes('--five-vertex-cover')) console.log(JSON.stringify(auditFiveVertexCover(), null, 2));
else if (process.argv.includes('--k5-lower')) console.log(JSON.stringify(auditK5LowerReceipt(), null, 2));
else if (process.argv.includes('--regenerate-k5-lower')) console.log(JSON.stringify(generateK5LowerCertificate()));
else if (process.argv.includes('--corner-hall')) console.log(JSON.stringify(auditCornerHallPlans(), null, 2));
else if (process.argv.includes('--edge-terminal-structure')) console.log(JSON.stringify(auditEdgeTerminalStructure(), null, 2));
else if (process.argv.includes('--pinned-structural-terminals')) console.log(JSON.stringify(auditPinnedStructuralTerminals(loadPinnedCertificate()), null, 2));
else if (process.argv.includes('--structural-edge-policy')) console.log(JSON.stringify(buildStructuralEdgePolicy(), null, 2));
else if (process.argv.includes('--edge-expected-cost')) console.log(JSON.stringify(buildStructuralEdgePolicy(false,true), null, 2));
else if (process.argv.includes('--edge-coordinate-transport')) console.log(JSON.stringify(buildStructuralEdgePolicy(true), null, 2));
else if (process.argv.includes('--opposite-sign-cover')) console.log(JSON.stringify(auditOppositeSignCoverWitness(), null, 2));
else if (process.argv.includes('--representative-mass')) console.log(JSON.stringify(auditRepresentativeMass(), null, 2));
else console.log(JSON.stringify({...audit(),clock:auditClock(),structure:auditStructure(),parityCycles:auditParityCycles(),orientedCharacters:auditOrientedCharacters(),prefixPolymatroid:auditPrefixPolymatroid(),parityPolytope:auditParityPolytope(),parityHoles:auditParityHoles(),rankBlindness:auditRankBlindness(),paritySupportFunction:auditParitySupportFunction(),parityExchanges:auditParityExchanges(),graphParityClassification:auditGraphParityClassification(),boundedExchange:auditBoundedExchange(),signCertificates:auditSignCertificates(),cornerSignMinimax:auditCornerSignMinimax(),cornerGoals:auditCornerGoals(),earlyCornerSign:auditEarlyCornerSign(),chargedCycleCertificates:auditChargedCycleCertificates(),graphSignCertificates:auditGraphSignCertificateFormula(),fullGraphCertificates:auditFullGraphCertificates(),graphAdaptiveObjectives:auditGraphAdaptiveObjectives(),k5Orbit:auditK5Orbit(),k5LowerReceipt:auditK5LowerReceipt(),cornerHallPlans:auditCornerHallPlans(),hallBlockPacking:auditHallBlockPacking(),frozenLeaves:auditFrozenLeaves(loadPinnedCertificate())}, null, 2));
