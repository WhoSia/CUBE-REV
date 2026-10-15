// CUBE-REV P0-R6I-P7 independent original physical Go audit.
// Compare the same six real 54-sticker source prefixes under
// shared-once versus rebuilt-per-prefix complete CP/CO/EP/EO target.
package main
import("fmt";"math";"os";"strconv";"strings")
func bad(s string){fmt.Fprintln(os.Stderr,"P0R6I_P7_GO_AUDIT_FAIL",s);os.Exit(2)}
func field(line,key string)string{
 w:=strings.Fields(line)
 for i:=0;i+1<len(w);i++{if w[i]==key{return w[i+1]}}
 bad("missing "+key);return ""
}
func n(line,key string)uint64{
 x,e:=strconv.ParseUint(field(line,key),10,64)
 if e!=nil{bad("invalid uint "+key)};return x
}
func si(line,key string)int{
 x,e:=strconv.Atoi(field(line,key))
 if e!=nil{bad("invalid signed int "+key)};return x
}
func number(line,key string)float64{
 x,e:=strconv.ParseFloat(field(line,key),64)
 if e!=nil||math.IsNaN(x)||math.IsInf(x,0)||x<0{bad("nonfinite actual time "+key)}
 return x
}
func legal(last,act int)bool{
 a,b:=last/3,act/3
 if a==b{return false}
 opposite:=(a==0&&b==3)||(a==3&&b==0)||(a==1&&b==4)||(a==4&&b==1)||(a==2&&b==5)||(a==5&&b==2)
 return !opposite||b>=a
}
func budget(last,k int)uint64{
 var prev [18]uint64
 total:=uint64(k+1)
 for d:=1;d<=k;d++{
  var nxt [18]uint64
  if d==1{for a:=0;a<18;a++{if legal(last,a){nxt[a]=1}}}else{
   for b,v:=range prev{for a:=0;a<18;a++{if legal(b,a){nxt[a]+=v}}}
  }
  prev=nxt
  var level uint64
  for _,v:=range nxt{level+=v}
  total+=uint64(k-d+1)*level
 }
 return total
}
type Sample struct{words,visits,skips,pairs,edges,queries uint64;wall float64}
type Receipt struct{mode string;builds int;setup,source,wall float64;samples []Sample;peak uint64}
var paths=[6][2]int{{0,-1},{9,-1},{0,3},{0,9},{9,3},{9,12}}
func inspect(path,mode string,g,r int)Receipt{
 data,e:=os.ReadFile(path);if e!=nil{bad("cannot read genuine native log "+path)}
 s:=string(data)
 if strings.Contains(s,"P0R6I_P7_RESOURCE_HOLD")||strings.Contains(s,"P0R6I_P7_TRUE_PHYSICAL_INTERSECTION")||strings.Contains(s,"P0R6I_P7_ERROR"){bad("HOLD, true physical meet or error")}
 receipt:=Receipt{mode:mode}
 setupLines:=0
 var measuredSetup,measuredSource float64
 for _,line:=range strings.Split(s,"\n"){
  line=strings.TrimSpace(line)
  if strings.HasPrefix(line,"P0R6I_P7_GOAL_BUILD "){
   if field(line,"MODE")!=mode{bad("wrong mode in target setup")}
   setupLines++
   if int(n(line,"BUILD"))!=setupLines{bad("missing/duplicate real target build")}
   expected:=uint64(3502);if g==6{expected=8240087}
   if n(line,"FULL_GOAL")!=expected||n(line,"CORNER")==0||n(line,"EDGE")==0||
      n(line,"RSS_PEAK_KIB")==0||n(line,"ORIGINAL_REAL_54_FACELET_CHECKS")!=4608{
    bad("bad original whole-cubie/projection build receipt")
   }
   if g==6&&(n(line,"CORNER")!=1405068||n(line,"EDGE")!=7672278){bad("not original projected B6 targets")}
   duration:=number(line,"TARGET_SETUP_MS")
   if duration<=0{bad("nonpositive target rebuild time")}
   measuredSetup+=duration
  }else if strings.HasPrefix(line,"P0R6I_P7_PREFIX "){
   if field(line,"MODE")!=mode{bad("wrong physical mode in prefix")}
   j:=len(receipt.samples)
   if j>=6||n(line,"CASE")!=uint64(j+1){bad("missing/duplicate sample")}
   id:=paths[j]
   first,second:=si(line,"FIRST"),si(line,"SECOND")
   if first!=id[0]||second!=id[1]{bad("unexpected original legal prefix ID")}
   last,depth:=first,1
   if second>=0{
    if !legal(first,second){bad("illegal source-prefix grammar")}
    last=second;depth=2
   }
   exact:=budget(last,r-depth)
   vis,skip:=n(line,"VISITED"),n(line,"SAFELY_SKIPPED")
   if exact!=n(line,"WORD_CALLS")||vis+skip!=exact||
     n(line,"FULL_CUBIE_GOAL_MEETS")!=0{
     bad("incomplete or colliding original source sample")
   }
   pair,edge:=n(line,"ORDERED_PAIR_CHECKS"),n(line,"PACKED_EDGE_CHECKS")
   if edge>pair{bad("edge gate exceeds ordered pair candidates")}
   wall:=number(line,"SOURCE_MS")
   measuredSource+=wall
   receipt.samples=append(receipt.samples,Sample{exact,vis,skip,pair,edge,n(line,"FULL_QUERIES"),wall})
  }else if strings.HasPrefix(line,"P0R6I_P7_MODE_COMPLETE "){
   if receipt.builds!=0{bad("duplicated summary receipt")}
   if field(line,"MODE")!=mode||n(line,"GOAL_RADIUS")!=uint64(g)||
      n(line,"SOURCE_RADIUS")!=uint64(r)||n(line,"PREFIXES")!=6||
      n(line,"ORIGINAL_54_STICKER_PHYSICS_PASS")!=1||
      n(line,"ALL_SAMPLED_FULL_CUBIE_MEETS")!=0||
      n(line,"NOT_GLOBAL_B10")!=1{
    bad("invalid complete actual physical summary")
   }
   receipt.builds=int(n(line,"TARGET_BUILDS"))
   receipt.setup=number(line,"TOTAL_GOAL_SETUP_MS")
   receipt.source=number(line,"TOTAL_PHYSICAL_SEARCH_MS")
   receipt.wall=number(line,"FULL_PROCESS_MS")
   receipt.peak=n(line,"PEAK_RSS_KIB")
  }
 }
 expectedBuilds:=1;if mode=="isolated"{expectedBuilds=6}
 if receipt.builds!=expectedBuilds||setupLines!=expectedBuilds||len(receipt.samples)!=6||receipt.peak==0{bad("missing original target builds, six physical prefixes or process RSS")}
 if math.Abs(receipt.setup-measuredSetup)>0.01||math.Abs(receipt.source-measuredSource)>0.01{bad("per-phase summed actual cost mismatches")}
 if receipt.wall+5.0<receipt.setup+receipt.source{bad("process wall too short for actual physical work")}
 return receipt
}
func main(){
 if len(os.Args)!=5{bad("usage: shared.log isolated.log goalR sourceR")}
 g,e:=strconv.Atoi(os.Args[3]);if e!=nil{bad("goalR")}
 r,e:=strconv.Atoi(os.Args[4]);if e!=nil{bad("sourceR")}
 if !(g==3&&r==3)&&!(g==6&&r==7){bad("unsupported original physical calibration horizons")}
 a,b:=inspect(os.Args[1],"shared",g,r),inspect(os.Args[2],"isolated",g,r)
 for i:=0;i<6;i++{
  x,y:=a.samples[i],b.samples[i]
  if x.words!=y.words||x.visits!=y.visits||x.skips!=y.skips||x.pairs!=y.pairs||
     x.edges!=y.edges||x.queries!=y.queries{
     bad(fmt.Sprintf("the physical source semantics or pruning differs at prefix %d",i+1))
  }
 }
 ratio:=b.setup/a.setup
 fmt.Printf("P0R6I_P7_GO_INDEPENDENT_PAIRED_PASS GOAL_RADIUS %d SOURCE_RADIUS %d PREFIXES 6 SHARED_TARGET_BUILDS %d ISOLATED_TARGET_BUILDS %d SHARED_SETUP_MS %.3f ISOLATED_SETUP_MS %.3f SHARED_PREFIX_SOURCE_MS %.3f ISOLATED_PREFIX_SOURCE_MS %.3f SHARED_PROCESS_WALL_MS %.3f ISOLATED_PROCESS_WALL_MS %.3f SHARED_PEAK_RSS_KIB %d ISOLATED_PEAK_RSS_KIB %d SETUP_RATIO_ISOLATED_VS_SHARED %.5f WHOLE_CUBIE_SOURCE_AND_GATE_COUNTERS_IDENTICAL 1 FULL_CUBIE_GOAL_MEETS 0 GLOBAL_LOWER17_NOT_CLAIMED 1\n",
    g,r,a.builds,b.builds,a.setup,b.setup,a.source,b.source,a.wall,b.wall,a.peak,b.peak,ratio)
 for i,x:=range a.samples{
  fmt.Printf("P0R6I_P7_PHYSICAL_PREFIX_PARITY CASE %d WORDS %d VISITS %d SKIPS %d ORDERED_PAIR_CHECKS %d EDGE_CHECKS %d FULL_QUERIES %d SAME_SOURCE_PRUNING 1\n",
  i+1,x.words,x.visits,x.skips,x.pairs,x.edges,x.queries)
 }
}
