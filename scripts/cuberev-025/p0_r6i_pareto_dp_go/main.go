// CUBE-REV 0.25 P0-R6I-P6: exact finite depth<=2 Pareto DP.
// This is an exact optimizer of a DECLARED RATIONAL COST MODEL,
// NOT exact optimization of unknown real original Rubik search runtime.
// Verify the reduced-state DP against all 2^18 distinct first-action
// keep/split policies and the exact source DFA cylinder word counts.
package main
import(
 "fmt"
 "math/big"
 "math/bits"
 "sort"
)
const R=10
const goalSetupCentis=2000 // UNMEASURED setup assumption, 20.00 sec
const measuredLowCentis=71150 // measured whole first-U B10 physical
const measuredHighCentis=56199 // measured whole first-D B10 physical
const canonicalTotal uint64=285921738920
func reject(s string){panic("P0R6I_PARETO_DP_FAIL "+s)}
func legal(last,next int)bool{
 if last<0{return true}
 a,b:=last/3,next/3
 if a==b{return false}
 opposite:=(a==0&&b==3)||(a==3&&b==0)||
 (a==1&&b==4)||(a==4&&b==1)||
 (a==2&&b==5)||(a==5&&b==2)
 return !opposite||b>=a
}
func weight(last,k int)uint64{
 var cur [18]uint64
 total:=uint64(k+1)
 for d:=1;d<=k;d++{
  var nxt [18]uint64
  if d==1{for a:=0;a<18;a++{if legal(last,a){nxt[a]=1}}}else{
   for b,v:=range cur{for a:=0;a<18;a++{if legal(b,a){nxt[a]+=v}}}
  }
  cur=nxt
  var layer uint64
  for _,v:=range cur{layer+=v}
  total+=uint64(k-d+1)*layer
 }
 return total
}
func ceilDiv(n,d *big.Int)*big.Int{
 z:=new(big.Int).Add(n,new(big.Int).Sub(d,big.NewInt(1)))
 return z.Div(z,d)
}
// Model uses integer nanoseconds and CEIL rounding of each leaf once.
// This is an explicitly fixed discrete model that can be compared EXACTLY.
func cost(first int, w uint64)uint64{
 whole:=weight(first,R-1)
 observed:=uint64(measuredHighCentis)
 if first<9{observed=measuredLowCentis}
 if observed<=goalSetupCentis{reject("nonpositive net empirical source cost")}
 setup:=big.NewInt(goalSetupCentis*10000000)
 net:=new(big.Int).Mul(new(big.Int).SetUint64(observed-goalSetupCentis),new(big.Int).SetUint64(w))
 net.Mul(net,big.NewInt(10000000))
 q:=ceilDiv(net,new(big.Int).SetUint64(whole))
 ans:=new(big.Int).Add(setup,q)
 if !ans.IsUint64(){reject("nanosecond cost overflow")}
 return ans.Uint64()
}
type opt struct{jobs int;sum,max uint64;low,high uint16;inner uint64}
var choices [18][2]opt
func combine(a,b opt)opt{
 x:=opt{jobs:a.jobs+b.jobs,sum:a.sum+b.sum,low:a.low+b.low,high:a.high+b.high,inner:a.inner+b.inner}
 if a.max>b.max{x.max=a.max}else{x.max=b.max}
 return x
}
func branches(first int)(opt,opt){
 whole:=weight(first,R-1)
 plain:=opt{jobs:1,sum:cost(first,whole),max:cost(first,whole)}
 if first<9{plain.low=0}else{plain.high=0}
 split:=opt{inner:uint64(R),jobs:0}
 for second:=0;second<18;second++{if legal(first,second){
  w:=weight(second,R-2)
  c:=cost(first,w)
  split.jobs++;split.sum+=c
  if c>split.max{split.max=c}
 }}
 if first<9{split.low=1}else{split.high=1}
 var childTotal uint64
 for second:=0;second<18;second++{if legal(first,second){childTotal+=weight(second,R-2)}}
 if childTotal+uint64(R)!=whole{reject("physical canonical word cylinder conservation")}
 return plain,split
}
type key struct{jobs int;max uint64}
// DP keeps min sum at fixed exact (job count, max modeled job cost).
// One state dominates another with <= jobs, <= sum and <= max.
// This has optimal substructure under independent first-letter branches.
func solveDP()[]opt{
 states:=map[key]opt{{0,0}:{jobs:0,sum:0,max:0}}
 for first:=0;first<18;first++{
  next:=map[key]opt{}
  a,b:=choices[first][0],choices[first][1]
  for _,state:=range states{
   for _,choice:=range []opt{a,b}{
    x:=combine(state,choice); k:=key{x.jobs,x.max}
    prev,exists:=next[k]
    if !exists||x.sum<prev.sum{next[k]=x}
   }
  }
  states=next
 }
 ans:=make([]opt,0,len(states))
 for _,x:=range states{
  // Pareto compare all DP compressed (jobs,total,max) states.
  dominated:=false
  for _,other:=range states{
   if other.jobs<=x.jobs&&other.sum<=x.sum&&other.max<=x.max&&
      (other.jobs<x.jobs||other.sum<x.sum||other.max<x.max){
     dominated=true;break
   }
  }
  if !dominated{ans=append(ans,x)}
 }
 sort.Slice(ans,func(i,j int)bool{if ans[i].jobs!=ans[j].jobs{return ans[i].jobs<ans[j].jobs};return ans[i].sum<ans[j].sum})
 return ans
}
func evaluate(mask uint32)opt{
 out:=opt{}
 for i:=0;i<18;i++{
  a,b:=choices[i][0],choices[i][1]
  if mask&(1<<i)!=0{out=combine(out,b)}else{out=combine(out,a)}
 }
 return out
}
func solveBrute()[]opt{
 // Exhaustively cross-check all 262,144 action-labelled depth2 cutsets.
 // This is an independent enumeration of the DP's ENTIRE choice space.
 classes:=make(map[[2]uint64]opt)
 for mask:=uint32(0);mask<1<<18;mask++{
  x:=evaluate(mask)
  k:=[2]uint64{uint64(x.jobs),x.max}
  old,found:=classes[k]
  if !found||x.sum<old.sum{classes[k]=x}
 }
 var all []opt
 for _,x:=range classes{all=append(all,x)}
 var ans []opt
 for _,x:=range all{
  dom:=false
  for _,y:=range all{
   if y.jobs<=x.jobs&&y.sum<=x.sum&&y.max<=x.max&&
      (y.jobs<x.jobs||y.sum<x.sum||y.max<x.max){dom=true;break}
  }
  if !dom{ans=append(ans,x)}
 }
 sort.Slice(ans,func(i,j int)bool{if ans[i].jobs!=ans[j].jobs{return ans[i].jobs<ans[j].jobs};return ans[i].sum<ans[j].sum})
 return ans
}
func checkTotal(c opt){
 var base uint64=uint64(R+1)
 for i:=0;i<18;i++{
  if (i<9&&c.low>0)||(i>=9&&c.high>0){} // class counts alone determine exact cardinality
  base+=weight(i,R-1)
 }
 if base!=canonicalTotal{reject("original source N10 mismatch")}
 if c.jobs!=18+14*int(c.low)+11*int(c.high){reject("source action cardinality mismatch")}
 if c.inner!=uint64(R)*uint64(c.low+c.high){reject("source internal prefix call mismatch")}
}
func same(a,b []opt)bool{
 if len(a)!=len(b){return false}
 for i:=range a{if a[i].jobs!=b[i].jobs||a[i].sum!=b[i].sum||a[i].max!=b[i].max{return false}}
 return true
}
func main(){
 for i:=0;i<18;i++{a,b:=branches(i);choices[i]=[2]opt{a,b}}
 if bits.OnesCount32((1<<18)-1)!=18{reject("enumeration bit domain")}
 // Brute force 2^18 policies compared to exact DP. The only optimized
 // quantity is a *discretized separable cost* and a single-job maximum,
 // not real concurrent P-processor scheduling (NP-hard in general).
 dp:=solveDP()
 brute:=solveBrute()
 if !same(dp,brute){reject("DP Pareto frontier differs from exhaustive 2^18 labelled policies")}
 fmt.Printf("P0R6I_PARETO_MODEL POLICY_OPTIONS 262144 EXACT_DP_BRUTE_EQUAL 1 FRONTIER_STATES %d INITIAL_SETUP_CENTISECONDS %d SOURCE_B10_CANONICAL_CALLS %d ACTUAL_PARALLEL_MAKESPAN_OPTIMUM_NOT_CLAIMED 1\n",len(dp),goalSetupCentis,canonicalTotal)
 for _,x:=range dp{
  checkTotal(x)
  fmt.Printf("P0R6I_PARETO_CERT JOBS %d LOW_SPLITS %d HIGH_SPLITS %d INTERNAL_CALLS %d MODEL_SUM_SECONDS %.6f MODEL_MAX_JOB_SECONDS %.6f EXACT_RATIONAL_MODEL_NANOSECOND_CEIL 1 SOURCE_GRAMMAR_COMPLETE 1\n",
   x.jobs,x.low,x.high,uint64(R+1)+x.inner,float64(x.sum)/1e9,float64(x.max)/1e9)
 }
 // Cross-check published greedy first U and first D split, 43 jobs.
 greedy:=evaluate((1<<0)|(1<<9))
 checkTotal(greedy)
 dominated:=false
 for _,x:=range dp{
  if x.jobs<=greedy.jobs&&x.sum<=greedy.sum&&x.max<=greedy.max&&
     (x.jobs<greedy.jobs||x.sum<greedy.sum||x.max<greedy.max){dominated=true;break}
 }
 fmt.Printf("P0R6I_GREEDY_U_D_43 JOBS %d SUM_SECONDS %.6f MAX_JOB_SECONDS %.6f PARETO_DOMINATED %t NO_MEASURED_B10_43_SHARD_WALL_CLAIM 1\n",greedy.jobs,float64(greedy.sum)/1e9,float64(greedy.max)/1e9,dominated)
 fmt.Println("P0R6I_EXACT_DEPTH2_PARETO_DP_262144_BRUTE_FORCE_AUDIT_PASS PHYSICAL_B10_NOT_RUN 1")
}
