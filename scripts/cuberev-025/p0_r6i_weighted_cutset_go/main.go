// CUBE-REV 0.25 P0-R6I — exact costed variable-length canonical
// prefix cutsets. This tool proves FINITE GRAMMAR COVERAGE, never a
// physical 54-sticker B10 no-intersection or a time-speedup claim.
package main
import(
 "fmt"
 "os"
 "strconv"
 "sort"
 "strings"
)
const radius=10
const fullBudget uint64=285921738920
const goalSetupSeconds=20.0 // explicitly UNMEASURED illustrative per-job overhead
const highReferenceSeconds=561.99 // externally measured source first D, R10
const lowReferenceSeconds=711.50  // externally measured source first U, R10
const highWeight=14279876542.0
const lowWeight=17489205559.0
func fail(msg string){fmt.Fprintln(os.Stderr,"P0R6I_FAIL",msg);os.Exit(2)}
func legal(last,next int)bool{
 if last<0{return true}
 fa,fb:=last/3,next/3
 if fa==fb{return false}
 opposite:=(fa==0&&fb==3)||(fa==3&&fb==0)||
 (fa==1&&fb==4)||(fa==4&&fb==1)||
 (fa==2&&fb==5)||(fa==5&&fb==2)
 return !opposite||fb>=fa
}
func nextMoves(last int)[]int {
 out:=make([]int,0,18)
 for a:=0;a<18;a++ {if legal(last,a){out=append(out,a)}}
 return out
}
type index struct {last,remaining int}
var memo=map[index]uint64{}
// Exact repeated iterative DFS CALL count from a prefix with
// 'remaining' source length and DFA context 'last'.
// Parent itself appears 'remaining+1' times.
func weight(last,remaining int)uint64 {
 if remaining==0{return 1}
 key:=index{last,remaining}
 if w,ok:=memo[key];ok{return w}
 n:=uint64(remaining+1)
 for _,a:=range nextMoves(last){n+=weight(a,remaining-1)}
 memo[key]=n
 return n
}
// Independent iterative exact 18-action DFA dynamic programming for
// the same weighted cylinder; verifies the tree recurrence method.
func layerWeight(last,remaining int)uint64{
 var counts [18]uint64
 var total uint64=uint64(remaining+1)
 for d:=1;d<=remaining;d++{
  var newer [18]uint64
  if d==1 {
   for a:=0;a<18;a++{if legal(last,a){newer[a]=1}}
  }else{
   for a:=0;a<18;a++{for b,n:=range counts{
    if legal(b,a){newer[a]+=n}
   }}
  }
  counts=newer
  var layer uint64
  for _,n:=range counts{layer+=n}
  total+=uint64(remaining-d+1)*layer
 }
 return total
}
type node struct {prefix []int;kids []*node}
func (n *node) last()int{
 if len(n.prefix)==0{return -1}
 return n.prefix[len(n.prefix)-1]
}
func (n *node) calls()uint64{return weight(n.last(),radius-len(n.prefix))}
func children(n *node)[]*node{
 var ans []*node
 if len(n.prefix)==radius{return ans}
 for _,a:=range nextMoves(n.last()){
  p:=append(append([]int(nil),n.prefix...),a)
  ans=append(ans,&node{prefix:p})
 }
 return ans
}
func split(n *node){if len(n.kids)>0||len(n.prefix)>=radius{fail("invalid split")};n.kids=children(n)}
func getLeaves(n *node)[]*node{
 if len(n.kids)==0{return []*node{n}}
 var out []*node
 for _,c:=range n.kids{out=append(out,getLeaves(c)...)}
 return out
}
func encodePrefix(p []int)string{
 if len(p)==0{return "ROOT"}
 var parts []string
 for _,a:=range p{parts=append(parts,strconv.Itoa(a))}
 return strings.Join(parts,".")
}
type verified struct{whole,interior,leafWeight uint64; leaves,internal,maxDepth int}
func verify(n *node)verified{
 depth:=len(n.prefix)
 remaining:=radius-depth
 expected:=n.calls()
 if expected!=layerWeight(n.last(),remaining){
  fail("18-symbol layer DP disagrees with recursive cylinder count at "+encodePrefix(n.prefix))
 }
 if len(n.kids)==0{return verified{whole:expected,leafWeight:expected,leaves:1,maxDepth:depth}}
 valid:=nextMoves(n.last())
 if len(n.kids)!=len(valid){fail("nonexhaustive grammar split at "+encodePrefix(n.prefix))}
 result:=verified{whole:uint64(remaining+1),interior:uint64(remaining+1),internal:1,maxDepth:depth}
 var expectedChildren map[int]bool=map[int]bool{}
 for _,a:=range valid{expectedChildren[a]=true}
 for _,c:=range n.kids{
  if len(c.prefix)!=depth+1 {fail("incorrect child depth")}
  for i,a:=range n.prefix{if c.prefix[i]!=a{fail("child prefix not in parent cylinder")}}
  a:=c.prefix[depth]
  if !expectedChildren[a]{fail("duplicate or illegal child "+encodePrefix(c.prefix))}
  delete(expectedChildren,a)
  part:=verify(c)
  result.whole+=part.whole
  result.interior+=part.interior
  result.leafWeight+=part.leafWeight
  result.leaves+=part.leaves
  result.internal+=part.internal
  if part.maxDepth>result.maxDepth{result.maxDepth=part.maxDepth}
 }
 if len(expectedChildren)!=0{fail("missing legal child")}
 if result.whole!=expected{fail("weighted cylinder splitting did not conserve exact population")}
 return result
}
func predictedCost(n *node)float64{
 if len(n.prefix)==0{fail("root has no individual physical source class")}
 rate:=(highReferenceSeconds-goalSetupSeconds)/highWeight
 if n.prefix[0]<9{rate=(lowReferenceSeconds-goalSetupSeconds)/lowWeight}
 return goalSetupSeconds+float64(n.calls())*rate
}
type report struct{max,runner,makespan float64;largest int;res verified}
func evaluate(root *node,workers int,verbose bool) report {
 check:=verify(root)
 if check.whole!=fullBudget||check.interior+check.leafWeight!=fullBudget {
  fail("root, interior and all leaf source call populations not exhaustive")
 }
 if len(root.kids)==0{fail("no split root")}
 leaves:=getLeaves(root)
 times:=make([]float64,len(leaves))
 for i,n:=range leaves{times[i]=predictedCost(n)}
 sort.Sort(sort.Reverse(sort.Float64Slice(times)))
 loads:=make([]float64,workers)
 var total float64
 for _,t:=range times{
  index:=0
  for i:=1;i<workers;i++{if loads[i]<loads[index]{index=i}}
  loads[index]+=t
  total+=t
 }
 var maxLoad float64
 for _,v:=range loads{if v>maxLoad{maxLoad=v}}
 if verbose {
  fmt.Printf("P0R6I_CUT_CERT VERIFIED 1 SOURCE_RADIUS %d FRONTIER_LEAVES %d INNER_NODES %d MAX_PREFIX_DEPTH %d INTERNAL_CALLS %d LEAF_CALLS %d TOTAL_CALLS %d PROVEN_CYLINDER_PARTITION 1 ESTIMATED_RUNNER_SECONDS %.3f ESTIMATED_LARGEST_SHARD_SECONDS %.3f ESTIMATED_%d_WORKER_BATCH_MAKESPAN_SECONDS %.3f COST_MODEL_UNMEASURED_DESCENDANT_RATE 1\n",radius,check.leaves,check.internal,check.maxDepth,check.interior,check.leafWeight,check.whole,total,times[0],workers,maxLoad)
 }
 return report{times[0],total,maxLoad,len(leaves),check}
}
func schedule(maxShards,workers int)report{
 root:=&node{}
 split(root) // never assign the physical source root as a shard job
 for{
  leaves:=getLeaves(root)
  var target *node
  best:=-1.0
  for _,n:=range leaves{
   if len(n.prefix)>=radius{continue}
   growth:=len(nextMoves(n.last()))-1
   if len(leaves)+growth>maxShards{continue}
   c:=predictedCost(n)
   if c>best{best=c;target=n}
  }
  if target==nil{break}
  // Pure minimax longest-job heuristic: guaranteed exact coverage,
  // NOT a proven globally optimal cost-aware partition policy.
  split(target)
 }
 r:=evaluate(root,workers,true)
 if r.largest>maxShards{fail("prefix budget exceeded")}
 return r
}
func main(){
 workerCount:=4
 if len(os.Args)>1{
  n,e:=strconv.Atoi(os.Args[1])
  if e!=nil||n<1||n>64{fail("workers must be 1..64")}
  workerCount=n
 }
 fmt.Printf("P0R6I_COST_MODEL INPUT_HIGH_D_WALL_SECONDS %.2f INPUT_LOW_U_WALL_SECONDS %.2f ASSUMED_PER_JOB_GOAL_SETUP_SECONDS %.2f EMPIRICALLY_VALIDATED_DEEPER_PREFIX_RATE 0 CURRENT_GLOBAL_LOWER16_ONLY 1\n",highReferenceSeconds,lowReferenceSeconds,goalSetupSeconds)
 plans:=[]int{18,30,45,60,80,120}
 for _,limit:=range plans{
  r:=schedule(limit,workerCount)
  fmt.Printf("P0R6I_PLAN MAX_SHARDS %d ACTUAL_SHARDS %d EXACT_TOTAL_WORD_CALLS %d PROVISIONAL_TOTAL_RUNNER_HOURS %.4f PROVISIONAL_%d_WORKER_HOURS %.4f NOT_A_PHYSICAL_ABSENCE_CERTIFICATE 1\n",limit,r.largest,r.res.whole,r.runner/3600,workerCount,r.makespan/3600)
 }
 // Strong invariant: for every selected frontier, literal 18-generator
 // DFA suffix enumeration equals recursive count for EVERY subtree, and
 // weighted internal + weighted frontier counts equal original B10.
 if weight(-1,radius)!=fullBudget||layerWeight(-1,radius)!=fullBudget||
  weight(0,9)!=17489205559||weight(9,9)!=14279876542{
  fail("legacy full B10 source proof and first-action weights changed")
 }
 fmt.Printf("P0R6I_ALL_PLANS_EXACT_CUTSET_COVER_PASS FULL_SOURCE_B10 %d CONSERVATION_FOR_ALL_PREFIXES 1 PHYSICAL_SOURCE_SEARCH_NOT_PERFORMED 1 GLOBAL_LOWER_16 1\n",fullBudget)
}
