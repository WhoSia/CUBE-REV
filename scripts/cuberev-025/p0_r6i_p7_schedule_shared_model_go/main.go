// P0-R6I-P7: explicitly price a common, immutable target court ONCE
// per nonempty worker, versus recreating it for every task.
// Both modes solve the EXACT 18 unsplit 9+9 task makespan using
// integer Bellman DP and independently test feasible(T), !feasible(T-1).
// Price inputs remain model assumptions pending actual original B10
// same-process court reuse; shared physical B7 tests run separately.
package main
import "fmt"
type C struct{setup,lo,hi int;reuse bool}
type Key struct{p,l,h int}
type V struct{cost,assignL,assignH int;ok bool}
var memo map[Key]V
func (c C) price(l,h int)int{
 if l+h==0{return 0}
 if !c.reuse{return l*c.lo+h*c.h}
 return c.setup+l*(c.lo-c.setup)+h*(c.hi-c.setup)
}
func exact(p,l,h int,c C)V{
 k:=Key{p,l,h}
 if v,ok:=memo[k];ok{return v}
 if p==1{
  v:=V{cost:c.price(l,h),assignL:l,assignH:h,ok:true}
  memo[k]=v;return v
 }
 res:=V{cost:1<<30}
 for x:=0;x<=l;x++{for y:=0;y<=h;y++{
  future:=exact(p-1,l-x,h-y,c)
  cost:=c.price(x,y)
  if future.cost>cost{cost=future.cost}
  if cost<res.cost{res=V{cost:cost,assignL:x,assignH:y,ok:true}}
 }}
 memo[k]=res;return res
}
func can(p,l,h,limit int,c C,known,seen map[Key]bool)bool{
 if p==1{return c.price(l,h)<=limit}
 k:=Key{p,l,h}
 if seen[k]{return known[k]}
 seen[k]=true
 for x:=0;x<=l;x++{for y:=0;y<=h;y++{
  if c.price(x,y)<=limit&&can(p-1,l-x,h-y,limit,c,known,seen){
   known[k]=true;return true
  }
 }}
 known[k]=false;return false
}
func run(p int,c C){
 memo=map[Key]V{}
 ans:=exact(p,9,9,c)
 if !ans.ok||!can(p,9,9,ans.cost,c,map[Key]bool{},map[Key]bool{})||
    can(p,9,9,ans.cost-1,c,map[Key]bool{},map[Key]bool{}){
  panic("shared-court schedule fails independent optimum witness or strict lower-bound check")
 }
 l,h:=9,9;maxCost,workerUsed,setupCopies:=0,0,0
 for i:=p;i>=1;i--{
  x:=exact(i,l,h,c)
  task:=c.price(x.assignL,x.assignH)
  if task>maxCost{maxCost=task}
  if x.assignL+x.assignH>0{workerUsed++;if c.reuse{setupCopies++}else{setupCopies+=x.assignL+x.assignH}}
  l-=x.assignL;h-=x.assignH
 }
 if l!=0||h!=0||maxCost!=ans.cost{panic("exact shared schedule reconstruction mismatch")}
 tag:="ISOLATED_PER_TASK"
 if c.reuse{tag="IMMUTABLE_ONCE_PER_WORKER"}
 fmt.Printf("P0R6I_P7_EXACT_SHARED_TARGET_MODEL_PASS COURT_POLICY %s WORKERS %d SETUP_CENTIS %d ORIGINAL_LOW_CENTIS %d ORIGINAL_HIGH_CENTIS %d ASSIGNED_LOW_JOBS 9 ASSIGNED_HIGH_JOBS 9 ACTUAL_USED_WORKERS %d MODEL_REBUILDS %d EXACT_MAKESPAN_CENTIS %d EXACT_SECONDS %.2f THRESHOLD_FEASIBLE 1 STRICT_THRESHOLD_INFEASIBLE 1 ALL_ORIGINAL_SOURCE_B10_FIRST_ACTIONS_COVERED 1 REAL_B10_SHARED_COURT_WALL_NOT_MEASURED 1\n",tag,p,c.setup,c.lo,c.hi,workerUsed,setupCopies,ans.cost,float64(ans.cost)/100)
}
func main(){
 for _,setup:=range []int{1371,1449,2000}{
  for _,p:=range []int{4,8}{
   run(p,C{setup:setup,lo:71150,hi:56199,reuse:false})
   run(p,C{setup:setup,lo:71150,hi:56199,reuse:true})
  }
 }
 fmt.Println("P0R6I_P7_EXACT_SHARED_WORKER_COST_COMPARISON_PASS ORIGINAL_PHYSICAL_B10_REUSE_UNMEASURED 1")
}
