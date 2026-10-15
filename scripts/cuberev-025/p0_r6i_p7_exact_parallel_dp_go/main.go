// CUBE-REV 0.25 P0-R6I-P7.
// EXACT Bellman dynamic programme for optimally scheduling the ORIGINAL
// 18 unsplit first-generator cylinder tasks on 4 or 8 identical workers,
// under a declared deterministic TWO-TYPE cost model (9 low, 9 high).
// LPT evaluation of the 43-leaf mixed-depth cutset is an upper bound,
// NOT a proven 43-leaf optimal schedule or real measured B10 runtime.
package main
import (
 "fmt"
 "math/big"
 "sort"
)
const lowCentis=71150
const highCentis=56199
const R=10
const sourceCalls uint64=285921738920
func fail(x string){panic("P0R6I_P7_SCHEDULE_FAIL "+x)}
type K struct {p,lo,hi int}
type Ans struct {cost int;choiceLow,choiceHigh int;found bool}
var cache map[K]Ans
func optimal(p,lo,hi int)Ans{
 if lo<0||hi<0||p<1{fail("invalid DP domain")}
 k:=K{p,lo,hi}
 if x,ok:=cache[k];ok{return x}
 if p==1{
  x:=Ans{cost:lo*lowCentis+hi*highCentis,choiceLow:lo,choiceHigh:hi,found:true}
  cache[k]=x;return x
 }
 best:=Ans{cost:int(^uint(0)>>1)}
 for l:=0;l<=lo;l++{for h:=0;h<=hi;h++{
  rest:=optimal(p-1,lo-l,hi-h)
  local:=l*lowCentis+h*highCentis
  score:=local
  if rest.cost>score{score=rest.cost}
  if score<best.cost{
   best=Ans{cost:score,choiceLow:l,choiceHigh:h,found:true}
  }
 }}
 cache[k]=best;return best
}
func reconstruct(p,lo,hi int)[][2]int{
 var worker [][2]int
 for p>1{
  x:=optimal(p,lo,hi)
  if !x.found{fail("missing exact DP witness")}
  worker=append(worker,[2]int{x.choiceLow,x.choiceHigh})
  lo-=x.choiceLow;hi-=x.choiceHigh;p--
 }
 worker=append(worker,[2]int{lo,hi})
 return worker
}
// Independent YES/NO bounded-load DP, not invoking or trusting optimal().
func feasible(p,lo,hi,cap int,memo map[[3]int]bool,seen map[[3]int]bool)bool{
 if p==1{return lo*lowCentis+hi*highCentis<=cap}
 k:=[3]int{p,lo,hi}
 if seen[k]{return memo[k]}
 seen[k]=true
 for l:=0;l<=lo;l++{for h:=0;h<=hi;h++{
  if l*lowCentis+h*highCentis>cap{continue}
  if feasible(p-1,lo-l,hi-h,cap,memo,seen){
   memo[k]=true;return true
  }
 }}
 memo[k]=false;return false
}
func load(w [2]int)int{return w[0]*lowCentis+w[1]*highCentis}
func checkExact(p int){
 cache=map[K]Ans{}
 res:=optimal(p,9,9)
 if !res.found{fail("no schedule")}
 witness:=reconstruct(p,9,9)
 low,high,maximum:=0,0,0
 for _,w:=range witness{
  low+=w[0];high+=w[1]
  if load(w)>maximum{maximum=load(w)}
 }
 if low!=9||high!=9||maximum!=res.cost{fail("bad exact worker assignment")}
 if !feasible(p,9,9,res.cost,map[[3]int]bool{},map[[3]int]bool{}){
  fail("optimal makespan not feasible under independent threshold DP")
 }
 if feasible(p,9,9,res.cost-1,map[[3]int]bool{},map[[3]int]bool{}){
  fail("strictly smaller makespan feasible: Bellman DP unsound")
 }
 fmt.Printf("P0R6I_P7_EXACT_18_WORKER_DP_PASS WORKERS %d LOW_JOBS 9 HIGH_JOBS 9 COST_UNIT_CENTISECONDS 1 EXACT_MAKESPAN_CENTIS %d EXACT_MAKESPAN_SECONDS %.2f INDEPENDENT_THRESHOLD_AT_OPT_PASS 1 INDEPENDENT_THRESHOLD_BELOW_OPT_REJECTED 1 STATES %d\n",p,res.cost,float64(res.cost)/100,len(cache))
 for i,w:=range witness{
  fmt.Printf("P0R6I_P7_WORKER_CERT WORKERS %d WORKER %d LOW %d HIGH %d LOAD_CENTIS %d\n",p,i,w[0],w[1],load(w))
 }
}
func legal(last,action int)bool{
 if last<0{return true}
 f,g:=last/3,action/3
 if f==g{return false}
 opposite:=(f==0&&g==3)||(f==3&&g==0)||(f==1&&g==4)||(f==4&&g==1)||(f==2&&g==5)||(f==5&&g==2)
 return !opposite||g>=f
}
func wordWeight(last,remaining int)uint64{
 var prior [18]uint64
 total:=uint64(remaining+1)
 for d:=1;d<=remaining;d++{
  var cur [18]uint64
  if d==1{for a:=0;a<18;a++{if legal(last,a){cur[a]=1}}}else{
   for b,v:=range prior{for a:=0;a<18;a++{if legal(b,a){cur[a]+=v}}}
  }
  prior=cur
  var layer uint64;for _,v:=range cur{layer+=v}
  total+=uint64(remaining-d+1)*layer
 }
 return total
}
func ceilDiv(x,y *big.Int)*big.Int{
 return new(big.Int).Div(new(big.Int).Add(x,new(big.Int).Sub(y,big.NewInt(1))),y)
}
func leafPrice(first int,weight uint64,setupCentis uint64)uint64{
 firstWeight:=wordWeight(first,R-1)
 observed:=uint64(highCentis)
 if first<9{observed=lowCentis}
 if setupCentis>=observed{fail("invalid physical setup")}
 n:=new(big.Int).Mul(new(big.Int).SetUint64(observed-setupCentis),new(big.Int).SetUint64(weight))
 n.Mul(n,big.NewInt(10000000)) // 1 centisecond = 10,000,000ns
 d:=new(big.Int).SetUint64(firstWeight)
 c:=new(big.Int).Add(new(big.Int).SetUint64(setupCentis*10000000),ceilDiv(n,d))
 if !c.IsUint64(){fail("ns overflow")}
 return c.Uint64()
}
func mixed43(workers int,setupCentis uint64){
 var jobs []uint64
 var internal uint64=uint64(R+1)
 for first:=0;first<18;first++{
  if first==0||first==9{
   internal+=R
   for next:=0;next<18;next++{if legal(first,next){
    w:=wordWeight(next,R-2)
    jobs=append(jobs,leafPrice(first,w,setupCentis))
   }}
  }else{
   jobs=append(jobs,leafPrice(first,wordWeight(first,R-1),setupCentis))
  }
 }
 if len(jobs)!=43{fail("mixed cutset is not exactly 43")}
 var totalCalls uint64=internal
 for first:=0;first<18;first++{
  if first==0||first==9{
   for next:=0;next<18;next++{if legal(first,next){
    totalCalls+=wordWeight(next,R-2)
   }}
  }else{totalCalls+=wordWeight(first,R-1)}
 }
 if totalCalls!=sourceCalls{fail("true canonical source cylinder union not exact")}
 sort.Slice(jobs,func(i,j int)bool{return jobs[i]>jobs[j]})
 var total uint64
 loads:=make([]uint64,workers)
 for _,v:=range jobs{
  total+=v
  best:=0
  for i:=1;i<workers;i++{if loads[i]<loads[best]{best=i}}
  loads[best]+=v
 }
 var largest uint64=jobs[0]
 for _,v:=range loads{if v>largest{largest=v}}
 lower:=(total+uint64(workers)-1)/uint64(workers)
 if jobs[0]>lower{lower=jobs[0]}
 // LPT is a constructive schedule upper bound and average/max
 // constitute a mathematical lower bound on ANY nonpreemptive schedule.
 fmt.Printf("P0R6I_P7_MIXED_43_SCHEDULE_BOUNDS WORKERS %d MODEL_SETUP_CENTIS %d EXACT_GRAMMAR_CALLS %d ACTUAL_LEAF_CYLINDERS 43 TOTAL_MODEL_RUNNER_SECONDS %.6f PROVEN_MODEL_MAKESPAN_LOWER_SECONDS %.6f LPT_CONSTRUCTIVE_UPPER_SECONDS %.6f EXACT_MIXED_43_MAKESPAN_NOT_CLAIMED 1 PHYSICAL_B10_UNRUN 1\n",workers,setupCentis,totalCalls,float64(total)/1e9,float64(lower)/1e9,float64(largest)/1e9)
}
func main(){
 if wordWeight(-1,R)!=sourceCalls||wordWeight(0,R-1)!=17489205559||wordWeight(9,R-1)!=14279876542{
  fail("old original canonical B10 source calibration drift")
 }
 for _,p:=range []int{4,8}{
  checkExact(p)
  for _,setup:=range []uint64{2000,1449,1371}{mixed43(p,setup)}
 }
 fmt.Println("P0R6I_P7_SCHEDULING_COMPLETE_EXACT_18_AND_BOUNDED_MIXED43_PASS MODEL_COSTS_NOT_VERIFIED_B10_SOURCE_PRICES 1")
}
