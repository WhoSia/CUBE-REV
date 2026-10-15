// P0-R6I-P6 independent Go verifier for actual original
// 54-sticker B3/B6 stage and physical source-prefix timings.
package main
import("fmt";"os";"strings";"strconv";"math")
func fail(s string){fmt.Fprintln(os.Stderr,"R6I_PROFILE_GO_FAIL",s);os.Exit(2)}
func field(s,k string)string{
 w:=strings.Fields(s)
 for i:=0;i+1<len(w);i++{if w[i]==k{return w[i+1]}}
 fail("missing "+k);return ""
}
func n(s,k string)uint64{
 x,e:=strconv.ParseUint(field(s,k),10,64)
 if e!=nil{fail("invalid uint "+k)}
 return x
}
func f(s,k string)float64{
 x,e:=strconv.ParseFloat(field(s,k),64)
 if e!=nil||math.IsNaN(x)||math.IsInf(x,0)||x<0{fail("invalid finite float "+k)}
 return x
}
func signed(s,k string)int{
 x,e:=strconv.Atoi(field(s,k))
 if e!=nil{fail("invalid signed int "+k)}
 return x
}
func allowed(last,next int)bool{
 if last/3==next/3{return false}
 a,b:=last/3,next/3
 opposite:=(a==0&&b==3)||(a==3&&b==0)||
 (a==1&&b==4)||(a==4&&b==1)||
 (a==2&&b==5)||(a==5&&b==2)
 return !opposite||b>=a
}
func budget(last,k int)uint64{
 var prev [18]uint64
 var total uint64=uint64(k+1)
 for d:=1;d<=k;d++{
  var cur [18]uint64
  if d==1{for a:=0;a<18;a++{if allowed(last,a){cur[a]=1}}}else{
   for b,v:=range prev{for a:=0;a<18;a++{if allowed(b,a){cur[a]+=v}}}
  }
  prev=cur
  var layer uint64
  for _,v:=range cur{layer+=v}
  total+=uint64(k-d+1)*layer
 }
 return total
}
func main(){
 if len(os.Args)!=4{fail("usage: job_log goalRadius sourceRadius")}
 g,e:=strconv.Atoi(os.Args[2]);if e!=nil{fail("goal radius")}
 r,e:=strconv.Atoi(os.Args[3]);if e!=nil{fail("source radius")}
 if !(g==3&&r==3)&&!(g==6&&r==7){fail("unexpected original court horizon")}
 raw,e:=os.ReadFile(os.Args[1]);if e!=nil{fail("missing raw Actions log")}
 wantStages:=map[string]bool{
  "ORIGINAL_PHYSICAL_PREFLIGHT":false,
  "FULL_GOAL_BALL_BUILD":false,
  "CORNER_PROJECTION":false,
  "EDGE_PROJECTION":false,
  "PROCESS_TOTAL_INCLUDING_SETUP_AND_SAMPLES":false,
 }
 type measured struct{calls,visits,skipped uint64;wall float64}
 var samples []measured
 wantPaths:=[][2]int{{0,-1},{9,-1},{0,3},{0,9},{9,3},{9,12}}
 var full,corner,edge uint64
 var setup float64
 var totalWall float64
 for _,line:=range strings.Split(string(raw),"\n"){
  line=strings.TrimSpace(line)
  if strings.HasPrefix(line,"R6I_PROFILE_STAGE "){
   name:=field(line,"NAME")
   if _,yes:=wantStages[name];!yes||wantStages[name]{fail("unexpected/duplicate physical stage")}
   wantStages[name]=true
   wall:=f(line,"WALL_MS")
   if wall<=0||n(line,"PROCESS_PEAK_RSS_KIB")==0{fail("invalid physical time/RSS")}
   if name=="FULL_GOAL_BALL_BUILD"||name=="CORNER_PROJECTION"||name=="EDGE_PROJECTION"{setup+=wall}
   if name=="PROCESS_TOTAL_INCLUDING_SETUP_AND_SAMPLES"{totalWall=wall}
  }else if strings.HasPrefix(line,"R6I_PROFILE_GOAL_FULL "){
   if full!=0{fail("duplicated physical goal receipt")}
   full=n(line,"R6I_PROFILE_GOAL_FULL")
   corner=n(line,"CORNER");edge=n(line,"EDGE")
   if n(line,"PHYSICAL_CHECKS")!=4608||n(line,"PREFIX_TRIALS")!=6{fail("original packed/full physical evidence absent")}
  }else if strings.HasPrefix(line,"R6I_PROFILE_PHYSICAL_PREFIX "){
   trial:=int(n(line,"CASE"))
   if trial!=len(samples)+1||trial>6{fail("invalid sample order")}
   p:=wantPaths[trial-1]
   first,second:=signed(line,"FIRST"),signed(line,"SECOND")
   if first!=p[0]||second!=p[1]{fail("wrong physical prefix identity")}
   depth:=1
   last:=first
   if second>=0{
    if !allowed(first,second){fail("physically illegal canonical prefix")}
    depth=2;last=second
   }
   if n(line,"PREFIX_DEPTH")!=uint64(depth){fail("wrong source depth")}
   expected:=budget(last,r-depth)
   visit,skip:=n(line,"VISITED"),n(line,"SAFELY_SKIPPED")
   if n(line,"WORD_CALLS")!=expected||visit+skip!=expected||
     n(line,"FULL_CUBIE_MEETS")!=0||
     n(line,"PROCESS_PEAK_RSS_KIB")==0{fail("original source grammatical completion incorrect")}
   if n(line,"ORDERED_PAIR_CHECKS")<n(line,"PACKED_EDGE_CHECKS"){fail("packed edge gates exceed candidate pairs")}
   samples=append(samples,measured{expected,visit,skip,f(line,"SOURCE_WALL_MS")})
  }
 }
 for name,yes:=range wantStages{if !yes{fail("missing physical stage "+name)}}
 expectedGoal:=uint64(3502)
 if g==6{expectedGoal=8240087}
 if full!=expectedGoal||corner==0||edge==0||len(samples)!=6{fail("wrong actual original source goal and complete six samples")}
 var search float64
 for _,x:=range samples{search+=x.wall}
 if setup+search>totalWall+20.0{fail("time stages exceed actual full source process wall")}
 fmt.Printf("R6I_PROFILE_GO_INDEPENDENT_PHASE_PASS GOAL_RADIUS %d SOURCE_RADIUS %d FULL_GOAL %d REAL_54_STICKER_MOVES 4608 SHARED_SETUP_WALL_MS %.3f SIX_PREFIX_SOURCE_WALL_MS %.3f TOTAL_PROCESS_WALL_MS %.3f TRIALS 6 PHYSICAL_ORIGINAL_FULL_CUBIE_NO_MEET 1 NO_GLOBAL_B10_CLAIM 1\n",g,r,full,setup,search,totalWall)
 for i,x:=range samples{
  fmt.Printf("R6I_PROFILE_GO_SOURCE_GATE_PREFIX CASE %d WORD_CALLS %d VISITS %d SKIPPED %d ACTUAL_RETAINED_FRACTION %.9f WALL_MS %.3f\n",i+1,x.calls,x.visits,x.skipped,float64(x.visits)/float64(x.calls),x.wall)
 }
}
