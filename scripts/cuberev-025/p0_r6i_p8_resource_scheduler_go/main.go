// CUBE-REV P0-R6I-P8: memory-constrained, receipt-linked worker batching.
// Input MUST have already passed independent P8 Go SHA256+physical DFA audit.
// This computes a feasible LPT worker assignment and universal model bound
// from real source-B7 geometry-conditioned wall/probe counters.
// It is NOT an exact 43-task scheduling optimum nor measured parallel B10.
package main
import("fmt";"math";"os";"sort";"strconv";"strings")
func fail(x string){panic("P8_RESOURCE_SCHEDULER_FAIL "+x)}
func field(s,k string)string{
 w:=strings.Fields(s)
 for i:=0;i+1<len(w);i++{if w[i]==k{return w[i+1]}}
 fail("missing "+k);return ""
}
func nat(s,k string)uint64{
 v,e:=strconv.ParseUint(field(s,k),10,64)
 if e!=nil{fail("invalid uint "+k)};return v
}
func number(s,k string)float64{
 x,e:=strconv.ParseFloat(field(s,k),64)
 if e!=nil||math.IsNaN(x)||math.IsInf(x,0)||x<0{fail("invalid nonnegative "+k)}
 return x
}
type Task struct{
 first,second int
 words,visits,pairs,edges,full uint64
 micros uint64
}
type Worker struct{
 tasks []Task
 micros uint64
}
func main(){
 if len(os.Args)!=6{fail("usage: original-native-B7.log audited-B7.log RAM_budget_KiB requested_workers setup_ms")}
 memBudget,e:=strconv.ParseUint(os.Args[3],10,64);if e!=nil{fail("RAM budget")}
 requested,e:=strconv.Atoi(os.Args[4]);if e!=nil||requested<1||requested>64{fail("worker cap")}
 setupMS,e:=strconv.ParseUint(os.Args[5],10,64);if e!=nil||setupMS>100000{fail("model setup estimate")}
 raw,e:=os.ReadFile(os.Args[1]);if e!=nil{fail("missing actual B7 native source log")}
 audit,e:=os.ReadFile(os.Args[2]);if e!=nil{fail("missing independently audited SHA256 / source-court proof")}
 var goalSHA string
 var tasks []Task
 var peak uint64
 correctBatch:=false
 for _,line:=range strings.Split(string(raw),"\n"){
  line=strings.TrimSpace(line)
  if strings.HasPrefix(line,"P8_GOAL_COMMIT "){
   if goalSHA!=""||field(line,"MODE")!="b7"||nat(line,"STATES")!=8240087{fail("unverified whole original B6 source batch")}
   goalSHA=field(line,"SHA256")
  }else if strings.HasPrefix(line,"P8_LEAF "){
   if goalSHA==""||field(line,"GOAL_SHA256")!=goalSHA||field(line,"MODE")!="b7"||nat(line,"COMPLETE")!=1||nat(line,"FULL_CUBIE_MEETS")!=0{
    fail("leaf without identical immutable target and complete physical proof")
   }
   micros:=uint64(math.Ceil(number(line,"WALL_MS")*1000))
   t:=Task{first:int(nat(line,"FIRST")),second:-1,words:nat(line,"WORD_CALLS"),visits:nat(line,"VISITED"),pairs:nat(line,"PAIRS"),edges:nat(line,"EDGES"),full:nat(line,"FULL_QUERIES"),micros:micros}
   b:=field(line,"SECOND")
   signedSecond,e:=strconv.Atoi(b);if e!=nil{fail("invalid second")}
   t.second=signedSecond
   if t.edges>t.pairs||t.visits>t.words{fail("physical screening inconsistency")}
   tasks=append(tasks,t)
  }else if strings.HasPrefix(line,"P8_BATCH_CERT "){
   if correctBatch||field(line,"MODE")!="b7"||field(line,"GOAL_SHA256")!=goalSHA||
      field(line,"POST_SEARCH_SHA256")!=goalSHA||nat(line,"SOURCE_GLOBAL_COMPLETE")!=1||
      nat(line,"LEAVES")!=43||nat(line,"BASELINE")!=120213368{fail("not a complete original source B7 certificate")}
   peak=nat(line,"PEAK_RSS_KIB")
   correctBatch=true
  }
 }
 proofTag:="P8_GO_INDEPENDENT_SHA256_AND_PHYSICAL_DFA_BATCH_PASS MODE b7 GOAL_SHA256 "+goalSHA+" "
 if !strings.Contains(string(audit),proofTag){fail("independent Go crypto+physical-language audit absent")}
 if !correctBatch||len(tasks)!=43||peak==0||len(goalSHA)!=64{fail("no complete audited physical 43-prefix source proof")}
 maxWorkers:=int(memBudget/peak)
 if maxWorkers>requested{maxWorkers=requested}
 if maxWorkers>len(tasks){maxWorkers=len(tasks)}
 if maxWorkers==0{fail("insufficient requested RAM for even ONE audited physical goal court")}
 workers:=make([]Worker,maxWorkers)
 sort.Slice(tasks,func(i,j int)bool{
  if tasks[i].micros!=tasks[j].micros{return tasks[i].micros>tasks[j].micros}
  if tasks[i].first!=tasks[j].first{return tasks[i].first<tasks[j].first}
  return tasks[i].second<tasks[j].second
 })
 var total,biggest,allPairs,allEdges,allQueries uint64
 for _,t:=range tasks{
  id:=0
  for i:=1;i<len(workers);i++{if workers[i].micros<workers[id].micros{id=i}}
  workers[id].tasks=append(workers[id].tasks,t)
  workers[id].micros+=t.micros
  total+=t.micros;allPairs+=t.pairs;allEdges+=t.edges;allQueries+=t.full
  if t.micros>biggest{biggest=t.micros}
 }
 // Simulated target court setup is paid ONCE on every occupied worker.
 setupMicros:=setupMS*1000
 universalLB:=uint64(math.Ceil(float64(total)/float64(maxWorkers)))
 if biggest>universalLB{universalLB=biggest}
 universalLB+=setupMicros
 var feasibleMax uint64
 for _,w:=range workers{
  if len(w.tasks)==0{fail("unused worker in greedy minimax plan")}
  if w.micros+setupMicros>feasibleMax{feasibleMax=w.micros+setupMicros}
 }
 if feasibleMax<universalLB{fail("impossible LPT schedule below universal time lower bound")}
 if uint64(maxWorkers)*peak>memBudget{fail("memory cap improperly enforced")}
 fmt.Printf("P8_RESOURCE_CONSTRAINED_LPT_FEASIBLE_NOT_EXACT_OPT MODEL_SOURCE_R7_SINGLE_SAMPLE 1 GOAL_SHA256 %s VERIFIED_ORIGINAL_B7_CUTSET_43 1 RAM_BUDGET_KIB %d AUDITED_SINGLE_COURT_PEAK_KIB %d REQUESTED_WORKERS %d ADMITTED_WORKERS %d MODEL_SETUP_PER_WORKER_MS %d OBSERVED_SOURCE_SUM_MS %.3f MODEL_MAKESPAN_LOWER_MS %.3f LPT_CONSTRUCTIVE_UPPER_MS %.3f ALL_PAIR_TESTS %d ALL_PACKED_EDGE_TESTS %d ALL_FULL_CUBIE_QUERIES %d UNSUPPORTED_B10_COST_TRANSFER_NOT_CLAIMED 1\n",
  goalSHA,memBudget,peak,requested,maxWorkers,setupMS,float64(total)/1000,float64(universalLB)/1000,float64(feasibleMax)/1000,allPairs,allEdges,allQueries)
 for i,w:=range workers{
  fmt.Printf("P8_WORKER_BATCH_CERT WORKER %d TARGET_SHA256 %s PREFIXES %d SOURCE_MS %.3f SHARED_ONE_SETUP_MS %d BATCH_MODEL_MS %.3f PEAK_RSS_BUDGET_KIB %d\n",
   i,goalSHA,len(w.tasks),float64(w.micros)/1000,setupMS,float64(w.micros+setupMicros)/1000,peak)
  for _,t:=range w.tasks{
   fmt.Printf("P8_WORKER_LEAF_LINK WORKER %d FIRST %d SECOND %d GOAL_SHA256 %s WORD_CALLS %d VISITS %d PAIRS %d EDGES %d FULL_QUERIES %d OBSERVED_SOURCE_MS %.3f\n",
    i,t.first,t.second,goalSHA,t.words,t.visits,t.pairs,t.edges,t.full,float64(t.micros)/1000)
  }
 }
}
