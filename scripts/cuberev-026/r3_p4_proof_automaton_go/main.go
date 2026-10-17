// CUBE-REV 0.26 R3-P4: finite-state proof assembly with strict observation authority.
// Does not accept a declaration of a root as evidence for its own children.
package main
import("fmt";"os";"strings";"strconv";"sort")
const sha="82fe545bcad3537c989ec22afce9d286926ddce5f4ef9428c0307951ec2d0979"
type Status uint8
const(Open Status=iota;Running;Certified;Meet;Hold;Invalid)
func fail(s string){fmt.Fprintln(os.Stderr,"P4_PROOF_AUTOMATON_REJECT",s);os.Exit(2)}
func legal(a,b int)bool{
 x,y:=a/3,b/3;if x==y{return false}
 opp:=(x==0&&y==3)||(x==3&&y==0)||(x==1&&y==4)||(x==4&&y==1)||(x==2&&y==5)||(x==5&&y==2)
 return !opp||y>=x
}
func mass(last,remaining int)uint64{
 var v [18]uint64;sum:=uint64(remaining+1)
 for depth:=1;depth<=remaining;depth++{var n [18]uint64
  if depth==1{for a:=0;a<18;a++{if legal(last,a){n[a]=1}}}else{
   for b,w:=range v{for a:=0;a<18;a++{if legal(b,a){n[a]+=w}}}
  }
  v=n;var layer uint64;for _,w:=range v{layer+=w};sum+=uint64(remaining-depth+1)*layer
 }
 return sum
}
type Root struct{id int;status Status;internal bool;child map[int]Status;visits,omitted uint64;receipt string}
func newRoot(a int)*Root{r:=&Root{id:a,child:map[int]Status{}};for b:=0;b<18;b++{if legal(a,b){r.child[b]=Open}};return r}
func (r *Root)promote()bool{
 if !r.internal{return false}
 for _,s:=range r.child{if s!=Certified{return false}}
 r.status=Certified;return true
}
func certify(r *Root,b int){
 if _,ok:=r.child[b];!ok{fail("noncanonical child")}
 if r.child[b]!=Open{fail("replayed/duplicate child")}
 r.child[b]=Certified
}
func parseField(s,k string)string{w:=strings.Fields(s);for i:=0;i+1<len(w);i++{if w[i]==k{return w[i+1]}};fail("missing "+k);return ""}
func num(s,k string)uint64{v,e:=strconv.ParseUint(parseField(s,k),10,64);if e!=nil{fail("invalid "+k)};return v}
func checkedOriginalR16(file0,file1 string)*Root{
 a:=newRoot(16);seen:=map[int]bool{}
 var total,visited,omitted uint64
 for shard,p:=range []string{file0,file1}{
  raw,e:=os.ReadFile(p);if e!=nil{fail("missing root16 immutable worker receipt")}
  txt:=string(raw)
  for _,bad:=range []string{"C026_R3R16_BRANCH_RESOURCE_HOLD","C026_R3R16_BRANCH_TRUE_FULL_CUBIE_MEET","C026_R3R16_BRANCH_ERROR"}{
   if strings.Contains(txt,bad){fail("unsafe source receipt")}
  }
  hasRoot,hasGoal,hasDone:=false,false,false
  n:=0
  for _,line:=range strings.Split(txt,"\n"){
   switch{
   case strings.HasPrefix(line,"C026_R3R16_BRANCH_GOAL "):
    if hasGoal||num(line,"FIRST")!=16||num(line,"SHARD")!=uint64(shard)||num(line,"GOAL_STATES")!=8240087||parseField(line,"GOAL_SHA")!=sha||
      parseField(line,"C8_SHA")!="1591559f375779e00d8343d91a753f48a655f7455ae8c67686f101b1b4bcffa3"{fail("goal/c8 authority mismatch")}
    hasGoal=true
   case strings.HasPrefix(line,"C026_R3R16_BRANCH_ROOT "):
    if shard!=0||hasRoot||!hasGoal||num(line,"REPEATED_CALLS")!=10||num(line,"WHOLE_GOAL_HITS")!=0{fail("invalid depth1 root witness")}
    hasRoot=true;total+=10;visited+=10
   case strings.HasPrefix(line,"C026_R3R16_BRANCH_LEAF "):
    if !hasGoal||hasDone||num(line,"FIRST")!=16||num(line,"SHARD")!=uint64(shard)||num(line,"COMPLETE_LEAF")!=1||num(line,"WHOLE_GOAL_HITS")!=0||parseField(line,"GOAL_SHA")!=sha{fail("unsound leaf")}
    b:=int(num(line,"SECOND"));idx:=int(num(line,"GLOBAL_SECOND_INDEX"))
    if idx%2!=shard||seen[b]||!legal(16,b)||idx<0{fail("leaf/shard assignment")}
    expected:=make([]int,0);for a:=0;a<18;a++{if legal(16,a){expected=append(expected,a)}}
    if idx>=len(expected)||expected[idx]!=b{fail("incorrect canonical child order")}
    w:=mass(b,8);v,o:=num(line,"VISITED"),num(line,"OMITTED")
    if num(line,"WORD_CALLS")!=w||v+o!=w{fail("source IDDFS accounting invalid")}
    seen[b]=true;certify(a,b);n++;total+=w;visited+=v;omitted+=o
   case strings.HasPrefix(line,"C026_R3R16_BRANCH_SHARD_COMPLETE "):
    if !hasGoal||hasDone||num(line,"FIRST")!=16||num(line,"SHARD")!=uint64(shard)||num(line,"CHILDREN")!=6||parseField(line,"GOAL_SHA")!=sha{fail("shard completion invalid")}
    hasDone=true
   }
  }
  if n!=6||!hasDone||hasRoot!=(shard==0){fail("incomplete source physical shard")}
 }
 a.internal=true
 if len(seen)!=12||!a.promote()||total!=mass(16,9)||total!=14279876542||visited!=80147215||omitted!=14199729327{
  fail("complete source root verification failed")
 }
 a.visits=visited;a.omitted=omitted;a.receipt="39017991545"
 return a
}
func main(){
 if len(os.Args)!=4{fail("usage: shard0 shard1 policy-output-path")}
 r:=checkedOriginalR16(os.Args[1],os.Args[2])
 // A partially certified root must not be promoted.
 q:=newRoot(17);q.internal=true;certify(q,0)
 if q.promote(){fail("partial witness promoted unproved root")}
 if r.status!=Certified{fail("verified root missing status")}
 // RITHM-inspired finite observation state: no inferred status for the other
 // roots. Known five roots referenced as previously authenticated external runs,
 // not independently replayed within this small R3-P4 court.
 verified:=map[int]string{0:"P10",3:"P10",9:"P10",12:"P11",15:"39007260192",16:r.receipt}
 keys:=make([]int,0,len(verified));for k:=range verified{keys=append(keys,k)};sort.Ints(keys)
 if len(keys)!=6{fail("unexpected previously certified root count")}
 var out strings.Builder
 out.WriteString("CUBE_REV_026_R3_P4_PROOF_STATUS_V1\nSOURCE_B6_SHA "+sha+"\n")
 for a:=0;a<18;a++{
  state:="OPEN";receipt:="-";if v,ok:=verified[a];ok{state="CERTIFIED";receipt=v}
  if a==16&&!r.promote(){fail("root16 invalid")}
  fmt.Fprintf(&out,"ROOT %02d %s RECEIPT %s CHILDREN %d EXACT_GRAMMAR_MASS %d\n",a,state,receipt,len(newRoot(a).child),mass(a,9))
 }
 out.WriteString("CERTIFIED_ROOTS 6 OPEN_ROOTS 12 GLOBAL_LOWER17_PROVED 0\n")
 out.WriteString("PARTIAL_ROOT_PROMOTION_REJECTED 1 EXACT_FIRST16_REPLAYED 1\n")
 if e:=os.WriteFile(os.Args[3],[]byte(out.String()),0644);e!=nil{fail(e.Error())}
 fmt.Printf("R3_P4_FINITE_PROOF_AUTOMATON_PASS ROOT16_CERTIFIED 1 ROOTS_CERTIFIED 6 ROOTS_OPEN 12 PARTIAL_PROMOTION_REJECTED 1 FIRST16_CALLS %d NO_GLOBAL_LOWER17 1\n",r.visits+r.omitted)
}
