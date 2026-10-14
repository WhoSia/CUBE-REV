// P0-R6G independent human-owned Go receipt verification for actual original
// physical B3/B3 or B6/B7 FIRST-MOVE-SHARDED complete-cubie proof.
package main
import (
 "fmt"
 "os"
 "strconv"
 "strings"
)
func fail(s string){fmt.Fprintln(os.Stderr,"P0R6G_AUDIT_FAIL",s);os.Exit(2)}
func number(s string)uint64{v,e:=strconv.ParseUint(s,10,64);if e!=nil{fail("bad integer "+s)};return v}
func val(tokens []string,key string)string{
 for i:=0;i+1<len(tokens);i++{if tokens[i]==key{return tokens[i+1]}}
 fail("missing field "+key);return ""
}
func permitted(last,next int)bool {
 if last/3==next/3{return false}
 a,b:=last/3,next/3
 opposite:=(a==0&&b==3)||(a==3&&b==0)||
 (a==1&&b==4)||(a==4&&b==1)||
 (a==2&&b==5)||(a==5&&b==2)
 return !opposite||b>=a
}
func shardExpected(first,radius int)uint64 {
 var cur [18]uint64
 cur[first]=1
 var calls uint64
 for depth:=1;depth<=radius;depth++ {
  if depth>1 {
   var next [18]uint64
   for a:=0;a<18;a++{for b,v:=range cur{
    if permitted(b,a){next[a]+=v}
   }}
   cur=next
  }
  var layer uint64
  for _,x:=range cur{layer+=x}
  calls+=uint64(radius-depth+1)*layer
 }
 return calls
}

func auditSingle(path string,action,radius int){
 if action<0||action>=18||!(radius==3||radius==10){
  fail("single shard only action0..17 source radius3 or10")
 }
 b,err:=os.ReadFile(path)
 if err!=nil{fail("cannot read single original physical shard log")}
 lines:=strings.Split(string(b),"\n")
 goal:=uint64(3502)
 if radius==10{goal=8240087}
 var shard,final,goalline,resource string
 var n int
 for _,l:=range lines{
  l=strings.TrimSpace(l)
  if strings.HasPrefix(l,"P0R6G_GOAL_FULL "){goalline=l}
  if strings.HasPrefix(l,"P0R6G_PHYSICAL_SHARD_COMPLETE "){shard=l;n++}
  if strings.HasPrefix(l,"P0R6G_SINGLE_SHARD_COMPLETE "){final=l}
  if strings.HasPrefix(l,"R6G_SINGLE_B10_WALL_SECONDS "){resource=l}
 }
 if n!=1||goalline==""||final==""{fail("missing or duplicate selected physical shard result")}
 gw:=strings.Fields(goalline);sw:=strings.Fields(shard);fw:=strings.Fields(final)
 if number(val(gw,"P0R6G_GOAL_FULL"))!=goal||
    number(val(gw,"PHYSICAL_PACKED_CASES"))!=4608||
    val(gw,"ROOT_CHECKED")!="1"||
    int(number(val(sw,"ACTION_ID")))!=action||
    int(number(val(fw,"ACTION_ID")))!=action||
    number(val(fw,"P0R6G_SINGLE_SHARD_COMPLETE"))!=1||
    number(val(fw,"SOURCE_RADIUS"))!=uint64(radius)||
    val(fw,"NOT_A_GLOBAL_SOURCE_COVER")!="1"||
    val(fw,"ORIGINAL_54_STICKER_PHYSICS_PASS")!="1"{
    fail("original goal, selected action, certified root, radius, physics or no-global-claim invalid")
 }
 expected:=shardExpected(action,radius)
 v:=number(val(sw,"VISITED"));skip:=number(val(sw,"SKIPPED"))
 if number(val(sw,"BASELINE"))!=expected||
  v+skip!=expected||
  number(val(fw,"SHARD_BASELINE"))!=expected||
  number(val(fw,"SHARD_VISITED"))!=v||
  number(val(fw,"SHARD_SAFE_SKIPS"))!=skip||
  val(sw,"GOAL_MEETS")!="0"||
  val(fw,"FULL_CUBIE_GOAL_MEETS")!="0"||
  val(fw,"CANONICAL_LAST_ACTION_CONTEXT_PRESERVED")!="1"{
   fail("source normal form, physical full cubie or safe prefix account missing")
 }
 if radius==10 {
  if resource==""{fail("B10 full physical wall time/RSS missing")}
  rw:=strings.Fields(resource)
  if _,e:=strconv.ParseFloat(val(rw,"R6G_SINGLE_B10_WALL_SECONDS"),64);e!=nil{
    fail("invalid B10 wall time")
  }
  if number(val(rw,"PEAK_RSS_KIB"))==0{fail("invalid B10 peak RSS")}
 }
 fmt.Printf("P0R6G_SINGLE_SHARD_GO_AUDIT_PASS SOURCE_RADIUS %d FIRST_ACTION %d SHARD_EXPECTED %d ACTUAL_VISITS %d SAFE_SKIPS %d ORIGINAL_COMPLETE_GOAL %d FULL_GOAL_MEETS 0 NOT_GLOBAL_LOWER17 1\n",radius,action,expected,v,skip,goal)
}

func main() {
 if len(os.Args)==5 && os.Args[1]=="--single" {
  a,e1:=strconv.Atoi(os.Args[3]); r,e2:=strconv.Atoi(os.Args[4]);
  if e1!=nil||e2!=nil{fail("invalid first-action/radius arguments")}
  auditSingle(os.Args[2],a,r);return
 }
 if len(os.Args)!=4{fail("usage: log-file goalRadius sourceRadius")}
 data,err:=os.ReadFile(os.Args[1]);if err!=nil{fail("read log failed")}
 goal,_:=strconv.Atoi(os.Args[2])
 radius,_:=strconv.Atoi(os.Args[3])
 if !(goal==3&&radius==3)&&!(goal==6&&radius==7){fail("only certified B3/B3 or B6/B7 pilot")}
 expectedTotal:=uint64(3784)
 expectedGoal:=uint64(3502)
 if radius==7{expectedTotal=120213368;expectedGoal=8240087}
 seen:=make(map[int]bool)
 var visited,skipped,summed uint64
 var certified bool
 for _,l:=range strings.Split(string(data),"\n"){
  w:=strings.Fields(strings.TrimSpace(l))
  if len(w)==0{continue}
  if w[0]=="P0R6G_GOAL_FULL"{
   if number(val(w,"P0R6G_GOAL_FULL"))!=expectedGoal||
      val(w,"ROOT_CHECKED")!="1"||number(val(w,"PHYSICAL_PACKED_CASES"))!=4608{fail("original goal/root/packed physical mismatch")}
   certified=true
  }
  if w[0]!="P0R6G_PHYSICAL_SHARD_COMPLETE"{continue}
  id:=int(number(val(w,"ACTION_ID")))
  if id<0||id>17||seen[id]{fail("missing/duplicated exact first-action ID")}
  seen[id]=true
  baseline:=number(val(w,"BASELINE"))
  n:=number(val(w,"VISITED"))
  skippedCalls:=number(val(w,"SKIPPED"))
  if baseline!=shardExpected(id,radius)||n+skippedCalls!=baseline||val(w,"GOAL_MEETS")!="0" {
   fail(fmt.Sprintf("incomplete or colliding physical shard %d",id))
  }
  visited+=n;skipped+=skippedCalls;summed+=baseline
 }
 if !certified||len(seen)!=18 {fail("missing original goal or one of the 18 physical proof shards")}
 root:=uint64(radius+1)
 all:=strings.Fields(strings.TrimSpace(func()string{
  for _,v:=range strings.Split(string(data),"\n"){
   if strings.HasPrefix(strings.TrimSpace(v),"P0R6G_ALL_18_FIRST_ACTIONS_AND_ROOT_COMPLETE "){return v}
  }
  fail("missing global exact source proof cover");return ""
 }()))
 if val(all,"P0R6G_ALL_18_FIRST_ACTIONS_AND_ROOT_COMPLETE")!="1" ||
   number(val(all,"ROOT_CALLS"))!=root||
   number(val(all,"SHARD_COUNT"))!=18||
   number(val(all,"TOTAL_BASELINE"))!=expectedTotal||
   number(val(all,"TOTAL_ACTUAL_VISITS"))!=visited+root||
   number(val(all,"TOTAL_SAFE_SKIPS"))!=skipped||
   val(all,"TRUE_FULL_CUBIE_MEETS")!="0"||
   val(all,"CANONICAL_UNION_EXACT")!="1"||
   val(all,"ORIGINAL_54_STICKER_PHYSICS_PASS")!="1"||
   summed+root!=expectedTotal||
   visited+skipped+root!=expectedTotal{
  fail("original root+18-shard canonical word partition or physical receipt invalid")
 }
 fmt.Printf("P0R6G_INDEPENDENT_GO_SHARD_AUDIT_PASS GOAL_RADIUS %d SOURCE_RADIUS %d SHARDS 18 ROOT_CALLS %d TOTAL_BASELINE %d ACTUAL_VISITS_WITH_ROOT %d SAFE_SKIPS %d FULL_CUBIE_MEETS 0 EXACT_18_ACTION_LANGUAGE_COVER 1\n",
  goal,radius,root,expectedTotal,visited+root,skipped)
}
