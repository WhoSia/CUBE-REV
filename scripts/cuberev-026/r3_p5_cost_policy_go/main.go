package main
import("fmt";"os";"sort";"strconv";"strings";"math")
func legal(a,b int)bool{x,y:=a/3,b/3;if x==y{return false};opp:=(x==0&&y==3)||(x==3&&y==0)||(x==1&&y==4)||(x==4&&y==1)||(x==2&&y==5)||(x==5&&y==2);return !opp||y>=x}
func mass(last,rem int)uint64{var dp [18]uint64;v:=uint64(rem+1);for d:=1;d<=rem;d++{var n [18]uint64;if d==1{for a:=0;a<18;a++{if legal(last,a){n[a]=1}}}else{for b,c:=range dp{for a:=0;a<18;a++{if legal(b,a){n[a]+=c}}}};dp=n;var sum uint64;for _,c:=range n{sum+=c};v+=uint64(rem-d+1)*sum};return v}
type Candidate struct{Root,Children int;Mass uint64;CostLow,CostHigh,GainLow,GainHigh float64;Status string;Score float64}
func main(){if len(os.Args)!=2{panic("usage: output.csv")};cert:=map[int]bool{0:true,3:true,9:true,12:true,15:true,16:true}
 // Three genuine 12-child completed source-root costs: prior a12 631.73s,
 // a15 580.74s, a16 C8 433.66s. These are historical runner-sums,
 // NOT independent draws from a stationary distribution.
 historical:=[]float64{631.73,580.74,433.66};sort.Float64s(historical)
 // Wide envelope, bounded empirical scenario, NOT frequentist confidence.
 low:=historical[0]*0.75;high:=historical[len(historical)-1]*1.6
 const cheapMass uint64=14279876542;const costlyMass uint64=17489205559
 var all []Candidate
 for a:=0;a<18;a++{kids:=0;for b:=0;b<18;b++{if legal(a,b){kids++}}
  m:=mass(a,9);if kids!=12&&kids!=15{panic("grammar degree drift")}
  if (kids==12&&m!=cheapMass)||(kids==15&&m!=costlyMass){panic("grammar mass drift")}
  state:="OPEN";if cert[a]{state="CERTIFIED"}
  factor:=float64(m)/float64(cheapMass)
  c:=Candidate{Root:a,Children:kids,Mass:m,CostLow:low*factor,CostHigh:high*factor,GainLow:0,GainHigh:1,Status:state}
  // Bound on new completed root coverage (0..1), not estimated probability.
  // Lexicographic priority: cheap worst-case first; avoid pretending this
  // predicts source physics. Exploration rotates to highest-cost once/3 picks.
  c.Score=1/c.CostHigh
  all=append(all,c)
 }
 var opens []Candidate;for _,c:=range all{if c.Status=="OPEN"{opens=append(opens,c)}}
 sort.Slice(opens,func(i,j int)bool{if opens[i].CostHigh==opens[j].CostHigh{return opens[i].Root<opens[j].Root};return opens[i].CostHigh<opens[j].CostHigh})
 if len(opens)!=12{panic("wrong proof state")}
 // Non-greedy bounded policy: take 2 cheap roots then 1 representative
 // expensive root; no candidate receives CERTIFIED by this policy.
 picks:=[]int{opens[0].Root,opens[1].Root}
 expensive:=[]Candidate{};for _,c:=range opens{if c.Children==15{expensive=append(expensive,c)}}
 if len(expensive)==0{panic("no costly exploration candidate")};picks=append(picks,expensive[0].Root)
 out:="root,proof_state,legal_second_children,exact_virtual_calls,cost_scenario_low_runner_seconds,cost_scenario_high_runner_seconds,certificate_gain_lower,certificate_gain_upper,policy_score\n"
 for _,c:=range all{out+=fmt.Sprintf("%d,%s,%d,%d,%.3f,%.3f,%.0f,%.0f,%.9f\n",c.Root,c.Status,c.Children,c.Mass,c.CostLow,c.CostHigh,c.GainLow,c.GainHigh,c.Score)}
 out+=fmt.Sprintf("# POLICY_NEXT_CHEAP_ROOT %d\n# POLICY_SECOND_CHEAP_ROOT %d\n# POLICY_EXPLORATION_EXPENSIVE_ROOT %d\n# CERTIFIED 6 OPEN 12 LOWER17_PROVEN 0\n",picks[0],picks[1],picks[2])
 if err:=os.WriteFile(os.Args[1],[]byte(out),0644);err!=nil{panic(err)}
 // Reparse and independently enforce no spurious certification in saved policy.
 saved,err:=os.ReadFile(os.Args[1]);if err!=nil{panic(err)};lines:=strings.Split(string(saved),"\n");counts:=map[string]int{}
 for _,s:=range lines[1:]{if s==""||strings.HasPrefix(s,"#"){continue};fields:=strings.Split(s,",");if len(fields)!=9{panic("incorrect row")};a,err:=strconv.Atoi(fields[0]);if err!=nil||a<0||a>=18{panic("invalid root")};counts[fields[1]]++;cost,err:=strconv.ParseFloat(fields[5],64);if err!=nil||math.IsNaN(cost)||cost<=0{panic("invalid cost scenario")}}
 if counts["CERTIFIED"]!=6||counts["OPEN"]!=12{panic("proof status changed by scheduling")}
 fmt.Printf("R3_P5_COST_AWARE_PROOF_SELECTION_PASS ROOTS 18 CERTIFIED 6 OPEN 12 CHEAP_FIRST %d CHEAP_SECOND %d EXPLORATORY_EXPENSIVE %d SOURCE_GRAMMAR_EXACT 1 COST_NOT_PROOF 1 NO_LOWER17 1\n",picks[0],picks[1],picks[2])
}
