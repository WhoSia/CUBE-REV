// Independent 0.26 R2 matched-search receipt validator.
// Recomputes original canonical grammar, two genuine physical-source prefix
// language call budgets, and fail-closes missing rows, altered counts, SHA
// and condition mixups. Does not independently implement 54-sticker physics.
package main
import("bufio";"fmt";"os";"strconv";"strings";"math")
func fail(s string){fmt.Fprintln(os.Stderr,"R2_GO_INDEPENDENT_REJECT",s);os.Exit(2)}
const goalSHA="82fe545bcad3537c989ec22afce9d286926ddce5f4ef9428c0307951ec2d0979"
func legal(a,b int)bool {
 if a<0{return true};x,y:=a/3,b/3
 if x==y{return false}
 opposite:=(x==0&&y==3)||(x==3&&y==0)||(x==1&&y==4)||(x==4&&y==1)||(x==2&&y==5)||(x==5&&y==2)
 return !opposite||y>=x
}
func calls(last,remaining int)uint64{
 var before [18]uint64; sum:=uint64(remaining+1)
 for depth:=1;depth<=remaining;depth++{
  var now [18]uint64
  if depth==1{for a:=0;a<18;a++{if legal(last,a){now[a]=1}}}else{
   for b,v:=range before{for a:=0;a<18;a++{if legal(b,a){now[a]+=v}}}
  }
  before=now
  layer:=uint64(0);for _,v:=range now{layer+=v}
  sum+=uint64(remaining-depth+1)*layer
 }
 return sum
}
func find(w []string,k string)string{for i:=0;i+1<len(w);i++{if w[i]==k{return w[i+1]}};fail("missing "+k);return ""}
func num(w []string,k string)uint64{v,e:=strconv.ParseUint(find(w,k),10,64);if e!=nil{fail("invalid uint "+k)};return v}
func real(w []string,k string)float64{v,e:=strconv.ParseFloat(find(w,k),64);if e!=nil||math.IsNaN(v)||math.IsInf(v,0){fail("invalid finite float "+k)};return v}
type Row struct{mode string;visited,skipped,pairs,passes,full,early,candidates,pruned uint64; ms float64}
func main(){
 if len(os.Args)!=2{fail("usage: original-physical-A/B-stdout.log")}
 f,e:=os.Open(os.Args[1]);if e!=nil{fail(e.Error())};defer f.Close()
 sc:=bufio.NewScanner(f); sc.Buffer(make([]byte,64*1024),1024*1024)
 originals:=0;seen:=map[int]bool{};summaries:=map[int]bool{};var records [2][4]Row
 fixtureFirst:=[]int{15,16}
 for sc.Scan(){
  line:=sc.Text()
  if strings.HasPrefix(line,"R2_ORIGINAL_GOAL_FULL "){
   if originals!=0{fail("repeated source goal")};originals++
   w:=strings.Fields(line)
   if find(w,"VERIFIED_SHA")!=goalSHA||num(w,"ACTUAL_54_FACELET_4608")!=1||
    num(w,"GOAL_STATES")!=8240087||num(w,"C6")!=1405068||num(w,"C7")!=6807696||
    num(w,"E6")!=7672278||num(w,"GLOBAL_LOWER17_CLAIMED")!=0{fail("wrong 54-sticker source or goal")}
  }else if strings.HasPrefix(line,"R2_MATCHED_ORIGINAL_AB "){
   w:=strings.Fields(line);k:=int(num(w,"FIXTURE"));round:=int(num(w,"ROUND"))
   if originals!=1||k<0||k>1||round<0||round>3{fail("illegal fixture or round")}
   if k!=0&&!summaries[0]{fail("out-of-order fixture")}
   if seen[k*4+round]{fail("duplicate mode/fixture receipt")};seen[k*4+round]=true
   first,second:=int(num(w,"FIRST")),int(num(w,"SECOND"))
   if first!=fixtureFirst[k]||second!=0||!legal(first,second){fail("wrong actual original source prefix")}
   wantMode:="CORNER_FIRST";if round==1||round==2{wantMode="EDGE_FIRST"}
   if find(w,"MODE")!=wantMode||find(w,"SOURCE_B6_SHA")!=goalSHA||
    num(w,"WORD_CALLS")!=calls(second,8)||num(w,"ACTUAL_FULL_GOAL_HITS")!=0||
    num(w,"COMPLETE_DEPTH2_SOURCE_PREFIX")!=1||num(w,"COMPLETE_FIRST_ACTION_ROOT")!=0||
    num(w,"GLOBAL_LOWER17_CLAIMED")!=0{fail("source prefix/mode/checksum scientific scope mismatch")}
   a:=Row{mode:wantMode,visited:num(w,"VISITED"),skipped:num(w,"OMITTED"),
    pairs:num(w,"TWO_STEP_PAIR_CHECKS"),passes:num(w,"PROVEN_TWO_STEP_PASSES"),
    full:num(w,"FULL_GOAL_QUERIES"),early:num(w,"CORNER7_REJECTIONS"),
    candidates:num(w,"CANDIDATE_BRANCHES"),pruned:num(w,"PRUNED_BRANCHES"),
    ms:real(w,"WALL_MS")}
   if a.visited+a.skipped!=calls(second,8)||a.ms<=0{fail("wrong exact weighted baseline/benchmark")}
   records[k][round]=a
  }else if strings.HasPrefix(line,"R2_MATCHED_ABBA_SUMMARY "){
   w:=strings.Fields(line);k:=-1;for i,f:=range fixtureFirst{if int(num(w,"FIRST"))==f{k=i}}
   if k<0||summaries[k]||num(w,"SECOND")!=0||num(w,"ACTUAL_FIRST_ROOT_COMPLETE")!=0{fail("bad summary")}
   for j:=0;j<4;j++{if !seen[k*4+j]{fail("summary before four true measured receipt rows")}}
   ref:=records[k][0]
   for j:=1;j<4;j++{
    v:=records[k][j]
    if v.visited!=ref.visited||v.skipped!=ref.skipped||v.pairs!=ref.pairs||
     v.passes!=ref.passes||v.full!=ref.full||v.early!=ref.early||
     v.candidates!=ref.candidates||v.pruned!=ref.pruned{fail("admissible predicate changed source path correctness")}
   }
   base:=(records[k][0].ms+records[k][3].ms)/2
   alt:=(records[k][1].ms+records[k][2].ms)/2
   if math.Abs(real(w,"BASELINE_AVG_MS")-base)>0.004||
    math.Abs(real(w,"EDGE_FIRST_AVG_MS")-alt)>0.004||
    math.Abs(real(w,"EDGE_OVER_BASE_RATIO")-alt/base)>0.000001||
    num(w,"EXACT_SAME_VISITS")!=ref.visited||num(w,"EXACT_SAME_OMISSIONS")!=ref.skipped{
    fail("summary does not derive from four raw measurements")
   }
   summaries[k]=true
  }else if strings.HasPrefix(line,"R2_ORIGINAL_MATCHED_ADMISSIBLE_ORDER_ABBA_PASS "){
   w:=strings.Fields(line)
   if !summaries[0]||!summaries[1]||num(w,"SOURCE_PREFIXES")!=2||
    num(w,"PAIRED_COMPLETE_SEARCH_RUNS")!=8||
    num(w,"CHECKS_PROVEN_EQUIVALENT")!=1||
    num(w,"ORIGINAL_B6_TARGET_IMMUTABLE")!=1||
    num(w,"SAME_VISITS_AND_OMISSIONS")!=1||
    find(w,"VERIFIED_GOAL_SHA")!=goalSHA||
    num(w,"ROOTS_CURRENT_CERTIFIED")!=5||num(w,"ROOTS_OPEN")!=13||
    num(w,"NEW_FULL_FIRST_ROOT_CERTIFIED")!=0||num(w,"GLOBAL_LOWER17_CLAIMED")!=0{
    fail("final benchmark completeness or original distance overclaim")
   }
   for k:=0;k<2;k++{
    base:=(records[k][0].ms+records[k][3].ms)/2
    alt:=(records[k][1].ms+records[k][2].ms)/2
    if math.Abs(real(w,fmt.Sprintf("EDGE_OVER_BASE_RATIO_FIXTURE%d",k))-alt/base)>0.000001{
      fail("final A/B performance ratio forged")
    }
   }
   fmt.Printf("R2_GO_ABBA_REPLAY_PASS FULL_FIXTURES 2 COMPLETE_SOURCE_RUNS 8 ORIGINAL_SHA %s SAME_VISITS_AND_OMISSIONS 1 SRC_FIRST_ROOT_CERTIFIED 5 ROOTS_OPEN 13 NO_NEW_GLOBAL_DISTANCE_CLAIM 1\n",goalSHA)
   return
  }
 }
 if e:=sc.Err();e!=nil{fail(e.Error())}
 fail("original actual physical complete A/B footer missing")
}
