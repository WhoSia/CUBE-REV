// CUBE-REV P0-R6I-P8: independently aggregate FOUR external worker
// artifacts from genuinely separate GitHub Actions VMs into a complete
// original WCA physical source-B7 43-canonical-prefix refutation.
// SHA256 binds all four targets; each Go shard audit has already checked
// the 8,240,087 canonical sorted real CP/CO/EP/EO cubie records locally.
// Hash equality is a cryptographic provenance commitment, NOT a Lean axiom.
package main
import("fmt";"os";"path/filepath";"strconv";"strings")
func die(x string){fmt.Fprintln(os.Stderr,"P8_GLOBAL_MERGE_FAIL",x);os.Exit(2)}
func field(s,k string)string{
 w:=strings.Fields(s);for i:=0;i+1<len(w);i++{if w[i]==k{return w[i+1]}}
 die("missing "+k);return ""
}
func n(s,k string)uint64{
 v,e:=strconv.ParseUint(field(s,k),10,64);if e!=nil{die("invalid number "+k)};return v
}
func si(s,k string)int{
 v,e:=strconv.Atoi(field(s,k));if e!=nil{die("invalid signed field "+k)};return v
}
func legal(last,a int)bool{
 if last<0{return true}
 f,g:=last/3,a/3
 if f==g{return false}
 op:=(f==0&&g==3)||(f==3&&g==0)||(f==1&&g==4)||(f==4&&g==1)||(f==2&&g==5)||(f==5&&g==2)
 return !op||g>=f
}
func expectedWeight(last,remain int)uint64{
 var old [18]uint64
 sum:=uint64(remain+1)
 for d:=1;d<=remain;d++{
  var cur [18]uint64
  if d==1{
   for a:=0;a<18;a++{if legal(last,a){cur[a]=1}}
  }else{
   for b,v:=range old{for a:=0;a<18;a++{if legal(b,a){cur[a]+=v}}}
  }
  old=cur
  var layer uint64;for _,v:=range cur{layer+=v}
  sum+=uint64(remain-d+1)*layer
 }
 return sum
}
func complete43()[][2]int{
 var all [][2]int
 for first:=0;first<18;first++{
  if first==0||first==9{
   for next:=0;next<18;next++{if legal(first,next){all=append(all,[2]int{first,next})}}
  }else{all=append(all,[2]int{first,-1})}
 }
 if len(all)!=43{die("independent 18HTM grammar has wrong 43 source first-action cylinders")}
 return all
}
func main(){
 if len(os.Args)!=3{die("usage: downloaded_shard_artifact_dir github_run_id")}
 base,runID:=os.Args[1],os.Args[2]
 golden:="82fe545bcad3537c989ec22afce9d286926ddce5f4ef9428c0307951ec2d0979"
 expected:=complete43()
 seen:=make([]bool,len(expected))
 var allCalls,allVisits,allOmitted uint64
 totalLeaves,totalInternals:=0,0
 for shard:=0;shard<4;shard++{
  root:=filepath.Join(base,fmt.Sprintf("p8-shard-%d-%s",shard,runID))
  raw,e:=os.ReadFile(filepath.Join(root,fmt.Sprintf("p8-shard-%d.log",shard)))
  if e!=nil{die("missing original native physical worker receipt artifact")}
  audited,e:=os.ReadFile(filepath.Join(root,fmt.Sprintf("p8-shard-%d-audit.log",shard)))
  if e!=nil{die("missing independently cryptographically audited worker receipt")}
  required:=fmt.Sprintf("P8_SHARD_INDEPENDENT_GO_PASS SHARD %d TARGET_SHA256 %s ",shard,golden)
  if !strings.Contains(string(audited),required){
   die("worker source receipt lacks independent full physical 8.24M goal + DFA audit")
  }
  loggedGoal,loggedEnd:=false,false
  var shardCalls,shardVisits,shardOmitted uint64
  leafCount,internalCount:=0,0
  for _,line:=range strings.Split(string(raw),"\n"){
   line=strings.TrimSpace(line)
   if strings.HasPrefix(line,"P8_SHARD_GOAL "){
    if loggedGoal||n(line,"SHARD")!=uint64(shard)||n(line,"TOTAL_SHARDS")!=4||
      field(line,"SHA256")!=golden||n(line,"GOAL_STATES")!=8240087||
      n(line,"GOAL_RADIUS")!=6||n(line,"SOURCE_RADIUS")!=7||
      n(line,"PHYSICS_4608")!=1{die("mismatched original goal 54-sticker provenance")}
    loggedGoal=true
   }else if strings.HasPrefix(line,"P8_SHARD_INTERNAL "){
    if !loggedGoal||shard!=0||internalCount>=3||
      field(line,"SHA256")!=golden||n(line,"FULL_GOAL_MEETS")!=0||
      n(line,"INDEX")!=uint64(internalCount+1){die("wrong physical root/first-U/first-D target check")}
    depth,wantFirst:=0,-1
    if internalCount==1{depth=1;wantFirst=0}
    if internalCount==2{depth=1;wantFirst=9}
    wt:=uint64(8-depth)
    if n(line,"DEPTH")!=uint64(depth)||si(line,"FIRST")!=wantFirst||n(line,"REPEATED_CALLS")!=wt{
     die("invalid canonical grammar internal target proof")
    }
    internalCount++;shardCalls+=wt;shardVisits+=wt
   }else if strings.HasPrefix(line,"P8_SHARD_LEAF "){
    if !loggedGoal||loggedEnd||n(line,"SHARD")!=uint64(shard)||
      field(line,"SHA256")!=golden||n(line,"COMPLETE")!=1||
      n(line,"FULL_CUBIE_MEETS")!=0{die("target mismatched or incomplete source physical leaf")}
    i:=int(n(line,"GLOBAL_INDEX"))-1
    if i<0||i>=43||i%4!=shard||seen[i]||
      n(line,"LOCAL_INDEX")!=uint64(leafCount+1){die("duplicated, missing or wrongly assigned original canonical prefix")}
    a,b:=si(line,"FIRST"),si(line,"SECOND")
    if a!=expected[i][0]||b!=expected[i][1]{die("actual source shard prefix is not the canonical 18HTM partition")}
    depth,last:=1,a
    if b>=0{depth=2;last=b}
    if n(line,"DEPTH")!=uint64(depth){die("inconsistent source prefix remaining horizon")}
    wt:=expectedWeight(last,7-depth)
    visits,omitted:=n(line,"VISITED"),n(line,"OMITTED")
    if n(line,"WORD_CALLS")!=wt||visits+omitted!=wt||n(line,"EDGES")>n(line,"PAIRS"){
      die("incomplete genuine physical whole-cube source proof within worker leaf")
    }
    seen[i]=true;leafCount++;shardCalls+=wt;shardVisits+=visits;shardOmitted+=omitted
   }else if strings.HasPrefix(line,"P8_SHARD_DONE "){
    if !loggedGoal||loggedEnd||n(line,"SHARD")!=uint64(shard)||
      field(line,"GOAL_SHA256")!=golden||field(line,"AFTER_SHA256")!=golden||
      n(line,"GLOBAL_SOURCE_COMPLETE")!=0||n(line,"LOCAL_CERT_COMPLETE")!=1||
      n(line,"WORD_CALLS")!=shardCalls||n(line,"VISITED")!=shardVisits||
      n(line,"OMITTED")!=shardOmitted||n(line,"FULL_CUBIE_GOAL_MEETS")!=0{
      die("individual source worker attempted unsound total/global proof")
    }
    loggedEnd=true
   }
  }
  expectedLeafs:=11;if shard==3{expectedLeafs=10}
  expectedInternals:=0;if shard==0{expectedInternals=3}
  if !loggedEnd||leafCount!=expectedLeafs||internalCount!=expectedInternals||shardVisits+shardOmitted!=shardCalls{
    die("one genuine source worker batch not complete")
  }
  allCalls+=shardCalls;allVisits+=shardVisits;allOmitted+=shardOmitted
  totalLeaves+=leafCount;totalInternals+=internalCount
  fmt.Printf("P8_MERGE_WORKER_VERIFIED SHARD %d GOAL_SHA256 %s LEAVES %d INTERNALS %d WORD_CALLS %d VISITS %d OMITTED %d REAL_WHOLE_CUBIE_MEETS 0\n",shard,golden,leafCount,internalCount,shardCalls,shardVisits,shardOmitted)
 }
 for _,yes:=range seen{if !yes{die("missing one complete first-generator source-normal-form cylinder")}}
 if totalLeaves!=43||totalInternals!=3||
   allCalls!=120213368||allVisits!=674769||allOmitted!=119538599||
   allVisits+allOmitted!=allCalls{die("four independently audited source workers do not compose to exact original B7 full grammatical coverage")}
 fmt.Printf("P8_FOUR_WORKER_COMPLETE_ORIGINAL_B7_PROOF_PASS GOAL_SHA256 %s INDEPENDENT_ACTION_WORKERS 4 WHOLE_GOAL_CUBIES 8240087 REAL_ORIGINAL_18HTM 1 LEAVES 43 INTERNALS 3 ALL_CANONICAL_SOURCE_CALLS 120213368 PHYSICAL_VISITS 674769 SOUNDLY_OMITTED 119538599 TRUE_FULL_CUBIE_INTERSECTIONS 0 SOURCE_RADIUS 7 GOAL_RADIUS 6 GLOBAL_LOWER17_NOT_CLAIMED 1\n",golden)
}
