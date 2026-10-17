// P0-R6I-P11: independent Go complete real physical first-action R10
// source cylinder proof merger of TWO native Actions workers.
// Neither worker alone ever claims entire initial action15, and the
// merged a=15 proof NEVER claims globally empty R10 across all 18 actions.
package main
import("fmt";"os";"strconv";"strings")
func fail(s string){fmt.Fprintln(os.Stderr,"C026_R1_FIRST_ACTION15_GO_FAIL",s);os.Exit(2)}
const target="82fe545bcad3537c989ec22afce9d286926ddce5f4ef9428c0307951ec2d0979"
var proj=map[string]string{"C6_SHA":"409d46f47d29852f1ced2ed1726aba0ce1085472def92591ecbb6a2346cc1ffc",
"C7_SHA":"2fd2a3692147e81cc8bf970bcbbbdde061551065268e207d60aec4354ccd67e6",
"E6_SHA":"40de5296f586037e8c5710b6a843263c4370c5faedb8bcf99516a4ae08a070f9"}
func f(s,key string)string{
 w:=strings.Fields(s)
 for i:=0;i+1<len(w);i++{if w[i]==key{return w[i+1]}}
 fail("missing "+key);return ""
}
func u(s,key string)uint64{
 v,e:=strconv.ParseUint(f(s,key),10,64);if e!=nil{fail("invalid int "+key)};return v
}
func legal(last,a int)bool{
 if last<0{return true}
 x,y:=last/3,a/3
 if x==y{return false}
 opposite:=(x==0&&y==3)||(x==3&&y==0)||(x==1&&y==4)||(x==4&&y==1)||(x==2&&y==5)||(x==5&&y==2)
 return !opposite||y>=x
}
func weighted(last,remaining int)uint64{
 var prev [18]uint64
 total:=uint64(remaining+1)
 for d:=1;d<=remaining;d++{
  var next [18]uint64
  if d==1{for a:=0;a<18;a++{if legal(last,a){next[a]=1}}}else{
   for b,v:=range prev{for a:=0;a<18;a++{if legal(b,a){next[a]+=v}}}
  }
  prev=next;var layer uint64
  for _,n:=range next{layer+=n}
  total+=uint64(remaining-d+1)*layer
 }
 return total
}
func main(){
 if len(os.Args)!=3{fail("usage: shard0-real-native.log shard1-real-native.log")}
 actions:=make([]int,0)
 for b:=0;b<18;b++{if legal(15,b){actions=append(actions,b)}}
 if len(actions)!=12{fail("independent legal second action count inconsistent")}
 seen:=make([]bool,18)
 var total,visits,skips,allPairs,allEdges,fullQueries uint64
 rootCount,totalLeaves:=0,0
 for shard:=0;shard<2;shard++{
  dat,e:=os.ReadFile(os.Args[shard+1]);if e!=nil{fail("missing original native shard logfile")}
  raw:=string(dat)
  for _,bad:=range []string{"C026_R1_BRANCH_ERROR","C026_R1_BRANCH_RESOURCE_HOLD","C026_R1_BRANCH_TRUE_FULL_CUBIE_MEET","C026_R1_BRANCH_GOAL_HOLD","C026_R1_BRANCH_ROOT_TRUE_MEET"}{
   if strings.Contains(raw,bad){fail("unsafe physical meet/hold found in claimed negative shard")}
  }
  goalSeen,done:=false,false
  leafCount,internal:=0,0
  var shardW,shardV,shardO uint64
  for _,line:=range strings.Split(raw,"\n"){
   if strings.HasPrefix(line,"C026_R1_BRANCH_GOAL "){
    if goalSeen||u(line,"FIRST")!=15||u(line,"SHARD")!=uint64(shard)||
      u(line,"SHARDS")!=2||u(line,"GOAL_STATES")!=8240087||
      u(line,"REAL_54_FACELET_4608")!=1||u(line,"SOURCE_RADIUS")!=10||
      u(line,"SOURCE_WHOLE_GLOBAL_COMPLETE")!=0||
      f(line,"GOAL_SHA")!=target{fail("not same physical pinned complete B6 source court")}
    for k,v:=range proj{if f(line,k)!=v{fail("target corner/edge auxiliary projection not independently P9 anchored")}}
    goalSeen=true
   }else if strings.HasPrefix(line,"C026_R1_BRANCH_ROOT "){
    if !goalSeen||shard!=0||internal!=0||u(line,"FIRST")!=15||
      u(line,"SHARD")!=0||u(line,"DEPTH")!=1||
      u(line,"REPEATED_CALLS")!=10||u(line,"WHOLE_GOAL_HITS")!=0||
      f(line,"GOAL_SHA")!=target{fail("source first-action15 physical internal check absent or forged")}
    internal++;shardW+=10;shardV+=10
   }else if strings.HasPrefix(line,"C026_R1_BRANCH_LEAF "){
    if !goalSeen||done||u(line,"FIRST")!=15||
      u(line,"SHARD")!=uint64(shard)||u(line,"COMPLETE_LEAF")!=1||
      u(line,"WHOLE_GOAL_HITS")!=0||u(line,"FIRST_ACTION_CERT_COMPLETE")!=0||
      u(line,"SOURCE_WHOLE_GLOBAL_COMPLETE")!=0||f(line,"GOAL_SHA")!=target{
     fail("source leaf incomplete or absent real goal provenance")
    }
    i:=int(u(line,"GLOBAL_SECOND_INDEX"))
    if i<0||i>=len(actions)||i%2!=shard||int(u(line,"SECOND"))!=actions[i]||
      seen[actions[i]]{fail("child wrong canonical order, assigned wrong shard, or duplicate")}
    if u(line,"SOURCE_C")==0||u(line,"SOURCE_E")==0{
     // Require actual source coordinates to be present; zero may be legal for
     // certain cubie encodings but fixed scramble/prefix is nonzero here.
     fail("missing original cubie state source key")
    }
    expected:=weighted(actions[i],8)
    v,o:=u(line,"VISITED"),u(line,"OMITTED")
    if u(line,"WORD_CALLS")!=expected||v+o!=expected||
      u(line,"EDGES")>u(line,"PAIRS"){fail("not complete original physical B10 source canonical child refutation")}
    seen[actions[i]]=true;leafCount++;totalLeaves++
    shardW+=expected;shardV+=v;shardO+=o
    allPairs+=u(line,"PAIRS");allEdges+=u(line,"EDGES");fullQueries+=u(line,"FULL_QUERIES")
   }else if strings.HasPrefix(line,"C026_R1_BRANCH_SHARD_COMPLETE "){
    if done||!goalSeen||u(line,"FIRST")!=15||
      u(line,"SHARD")!=uint64(shard)||u(line,"CHILDREN")!=uint64(leafCount)||
      u(line,"INTERNAL_CHECKS")!=uint64(internal)||
      u(line,"WEIGHT")!=shardW||u(line,"VISITED")!=shardV||
      u(line,"OMITTED")!=shardO||u(line,"TARGET_IMMUTABLE")!=1||
      f(line,"GOAL_SHA")!=target||u(line,"FIRST_ACTION_CERT_COMPLETE")!=0||
      u(line,"SOURCE_WHOLE_GLOBAL_COMPLETE")!=0{fail("partial worker claims invalid actual original source coverage")}
    done=true
   }
  }
  need:=6
  if !goalSeen||!done||leafCount!=need||internal!=1-shard||shardV+shardO!=shardW{
   fail("source physical worker missing assigned full original B10 children")
  }
  rootCount+=internal;total+=shardW;visits+=shardV;skips+=shardO
  fmt.Printf("C026_R1_FIRST_ACTION15_SHARD_GO_AUDITED SHARD %d CHILDREN %d SOURCE_CALLS %d VISITED %d OMITTED %d IMMUTABLE_GOAL_SHA256 %s\n",
   shard,leafCount,shardW,shardV,shardO,target)
 }
 for _,b:=range actions{if !seen[b]{fail("missing unproved canonical second-action child")}}
 expected:=weighted(15,9)
 if totalLeaves!=12||rootCount!=1||total!=expected||visits+skips!=expected{
  fail("full first-action15 source B10 cylinder not accounted with canonical word exactness")
 }
 fmt.Printf("C026_R1_FIRST_ACTION15_COMPLETE_REAL_PHYSICAL_B10_PROOF_PASS FIRST_ACTION 15 GOAL_SHA256 %s C6_SHA256 %s C7_SHA256 %s E6_SHA256 %s SOURCE_RADIUS 10 GOAL_RADIUS 6 LEGAL_DEPTH2_CHILDREN 12 PHYSICAL_FIRST_ACTION_INTERNAL_CHECKS 1 FIRST_ACTION_CANONICAL_WORD_CALLS %d PHYSICAL_DFS_VISITED %d SOUNDLY_OMITTED %d REAL_ORDERED_PAIR_CHECKS %d PACKED_EDGE_CHECKS %d EXACT_FULL_CUBIE_GOAL_QUERIES %d ALL_TRUE_PHYSICAL_GOAL_HITS 0 ORIGINAL_FIRST_ACTION15_REFUTED 1 ORIGINAL_FULL_18_ACTION_SOURCE_COMPLETE 0 GLOBAL_LOWER17_CLAIMED 0\n",
  target,proj["C6_SHA"],proj["C7_SHA"],proj["E6_SHA"],expected,visits,skips,allPairs,allEdges,fullQueries)
}
