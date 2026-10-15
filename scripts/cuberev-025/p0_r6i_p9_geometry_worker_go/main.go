// P0-R6I-P9 conditional proof-carrying B10 worker allocation.
// Trusts ONLY actual P9 original physical, whole-B6 and separately audited
// complete C6/C7/E6 provenance for two newly sampled OPEN-first-action
// depth-two canonical B10 leaf obligations. This is a finite workload
// scheduling MODEL and NOT a global first-action B10 no-meet certificate.
package main
import("fmt";"math";"os";"strconv";"strings")
const goal="82fe545bcad3537c989ec22afce9d286926ddce5f4ef9428c0307951ec2d0979"
var proj=map[string]string{
 "C6":"409d46f47d29852f1ced2ed1726aba0ce1085472def92591ecbb6a2346cc1ffc",
 "C7":"2fd2a3692147e81cc8bf970bcbbbdde061551065268e207d60aec4354ccd67e6",
 "E6":"40de5296f586037e8c5710b6a843263c4370c5faedb8bcf99516a4ae08a070f9",
}
func bad(s string){fmt.Fprintln(os.Stderr,"P9_GEOMETRY_WORKER_PLAN_FAIL",s);os.Exit(2)}
func k(s,name string)string{v:=strings.Fields(s);for i:=0;i+1<len(v);i++{if v[i]==name{return v[i+1]}};bad("missing "+name);return ""}
func n(s,name string)uint64{v,e:=strconv.ParseUint(k(s,name),10,64);if e!=nil{bad("invalid int "+name)};return v}
func ms(s,name string)float64{v,e:=strconv.ParseFloat(k(s,name),64);if e!=nil||math.IsNaN(v)||math.IsInf(v,0)||v<0{bad("invalid elapsed "+name)};return v}
type Leaf struct{ first,second int; calls,visits,skips,pairs,edges,full uint64; wall float64 }
func main(){
 if len(os.Args)!=5{bad("usage: original-native-pilot.log independently-audited-go.log ramBudgetKiB requestedWorkers")}
 native,e:=os.ReadFile(os.Args[1]);if e!=nil{bad("native physical source log missing")}
 audit,e:=os.ReadFile(os.Args[2]);if e!=nil{bad("independent full projection Go audit missing")}
 b,e:=strconv.ParseUint(os.Args[3],10,64);if e!=nil{bad("bad explicit RAM constraint")}
 workers,e:=strconv.Atoi(os.Args[4]);if e!=nil||workers<1||workers>2{bad("only 1/2 real measured B10 prefix tasks allowed")}
 verified:=string(audit)
 if !strings.Contains(verified,"P9_GO_INDEPENDENT_PROJECTION_CLOSURE_PASS GOAL_SHA256 "+goal+" ")||
  !strings.Contains(verified,"SOURCE_PILOT_LEAVES 2 B10_GLOBAL_COMPLETE 0"){
  bad("incomplete prior independent 8M full B6 plus projection C7 exact closure audit")
 }
 for label,digest:=range proj{
  if !strings.Contains(verified,"P9_GO_EXACT_PROJECTION_PASS TYPE "+label+" ")||
     !strings.Contains(verified,"SHA256 "+digest+" "){bad("missing independently proven full auxiliary projection "+label)}
 }
 var sample []Leaf
 var rss uint64
 var processMS float64
 goodSummary:=false
 for _,line:=range strings.Split(string(native),"\n"){
  if strings.HasPrefix(line,"P9_OPEN_B10_PILOT "){
   i:=len(sample)
   if i>=2||n(line,"CASE")!=uint64(i+1)||
     n(line,"WORD_CALLS")!=1310203083||n(line,"TRUE_FULL_CUBIE_HITS")!=0||
     n(line,"COMPLETE_LOCAL_B10")!=1||n(line,"GLOBAL_B10_COMPLETE")!=0||
     k(line,"GOAL_SHA256")!=goal{bad("physical original B10 sibling negative proof incomplete")}
   first,second:=n(line,"FIRST"),n(line,"SECOND")
   if (i==0&&(first!=3||second!=0))||
      (i==1&&(first!=12||second!=0)){bad("unrecognized measured original B10 open first-action leaf")}
   s:=Leaf{first:int(first),second:int(second),calls:n(line,"WORD_CALLS"),visits:n(line,"VISITED"),skips:n(line,"OMITTED"),pairs:n(line,"PAIRS"),edges:n(line,"EDGES"),full:n(line,"FULL_QUERIES"),wall:ms(line,"SEARCH_MS")}
   if s.visits+s.skips!=s.calls||s.edges>s.pairs{bad("physical leaf source accounting or edge gate invalid")}
   sample=append(sample,s)
  }else if strings.HasPrefix(line,"P9_COMPLETE MODE pilot "){
   if goodSummary||k(line,"GOAL_SHA256")!=goal||
     n(line,"TARGET_IMMUTABLE")!=1||n(line,"PILOT_PREFIXES")!=2||
     n(line,"GLOBAL_B10_COMPLETE")!=0||n(line,"LOWER17_CLAIMED")!=0{
    bad("native P9 original source10 pilot is incomplete or false global claim")
   }
   rss=n(line,"PEAK_RSS_KIB");processMS=ms(line,"WALL_MS");goodSummary=true
  }
 }
 if !goodSummary||len(sample)!=2||rss==0{bad("missing whole B10 original physical audited pilot")}
 nWorkers:=workers
 if uint64(nWorkers)*rss>b{nWorkers=int(b/rss)}
 if nWorkers==0{bad("RAM unable to hold even one immutable full original goal and all three projection images")}
 if nWorkers>2{nWorkers=2}
 sum:=sample[0].wall+sample[1].wall
 perWorkerGoalSetup:=processMS-sum
 if perWorkerGoalSetup<=0{bad("the source total exceeds actual paired native wall, setup not measurable")}
 var modeledMakespan,modelTotal float64
 if nWorkers==1{
  modeledMakespan=processMS;modelTotal=processMS
 }else{
  modeledMakespan=perWorkerGoalSetup+math.Max(sample[0].wall,sample[1].wall)
  modelTotal=2*perWorkerGoalSetup+sum
 }
 fmt.Printf("P9_REAL_PHYSICAL_TWO_OPEN_FIRST_ACTION_B10_CERT_LINK_PASS TARGET_SHA256 %s C6_SHA256 %s C7_SHA256 %s E6_SHA256 %s SOURCE_PREFIXES 2 ORIGINAL_FULL_B6_ROWS 8240087 TWO_ACTUAL_FULL_CUBIE_ZERO_MEET_LEAVES 1 GLOBAL_FIRST_ACTION_COVER_COMPLETE 0 LOWER17_CLAIMED 0\n",goal,proj["C6"],proj["C7"],proj["E6"])
 for i,s:=range sample{
  fmt.Printf("P9_GEOMETRY_COST_LEAF CASE %d FIRST %d SECOND %d CALLS %d VISITS %d SKIPS %d PAIRS %d EDGES %d FULL_QUERIES %d ACTUAL_SOURCE_WALL_MS %.3f FULL_PHYSICAL_TARGET_MEETS 0\n",i+1,s.first,s.second,s.calls,s.visits,s.skips,s.pairs,s.edges,s.full,s.wall)
 }
 fmt.Printf("P9_RAM_GATED_MODEL_FEASIBLE_NOT_ACTUAL_PARALLEL_B10 RESOURCE_LIMIT_KIB %d ACTUAL_SINGLE_WORKER_RSS_KIB %d REQUESTED_WORKERS %d ADMITTED_WORKERS %d OBSERVED_SHARED_NATIVE_PROCESS_MS %.3f OBSERVED_TWO_SEARCHES_SUM_MS %.3f RESIDUAL_SHARED_GOAL_AND_PROJECTION_SETUP_MS %.3f CONDITIONAL_MODEL_MAKESPAN_MS %.3f CONDITIONAL_MODEL_TOTAL_RUNNER_MS %.3f CROSS_RUNNER_PHYSICAL_SPEEDUP_NOT_MEASURED 1 UNMEASURED_B10_PREFIX_PRICES_NOT_INFERRED 1\n",
  b,rss,workers,nWorkers,processMS,sum,perWorkerGoalSetup,modeledMakespan,modelTotal)
}
