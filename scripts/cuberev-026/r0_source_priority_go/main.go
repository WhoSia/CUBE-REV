// Independent normal-form grammar audit for 0.26 R0.
// Does not claim independent 54-facelet physics: it checks the exact
// canonical language count against a separate C++ physical source log.
package main
import("fmt";"os";"strconv";"strings")
func fail(s string){fmt.Fprintln(os.Stderr,"R0_GO_REJECT",s);os.Exit(2)}
func legal(last,a int)bool{
 if last<0{return true}
 x,y:=last/3,a/3
 if x==y{return false}
 opposite:=(x==0&&y==3)||(x==3&&y==0)||(x==1&&y==4)||(x==4&&y==1)||(x==2&&y==5)||(x==5&&y==2)
 return !opposite||y>=x
}
func weight(last,remaining int)uint64{
 var prev [18]uint64
 total:=uint64(remaining+1)
 for d:=1;d<=remaining;d++{
  var next [18]uint64
  if d==1{for a:=0;a<18;a++{if legal(last,a){next[a]=1}}}else{
   for b,v:=range prev{for a:=0;a<18;a++{if legal(b,a){next[a]+=v}}}
  }
  prev=next
  layer:=uint64(0);for _,v:=range next{layer+=v}
  total+=uint64(remaining-d+1)*layer
 }
 return total
}
func field(words []string,k string)string{
 for i:=0;i+1<len(words);i++{if words[i]==k{return words[i+1]}}
 fail("missing "+k);return ""
}
func uintField(words []string,k string)uint64{
 n,e:=strconv.ParseUint(field(words,k),10,64)
 if e!=nil{fail("invalid "+k)}
 return n
}
func main(){
 if len(os.Args)!=2{fail("usage: source-cpp-native-receipt.log")}
 raw,e:=os.ReadFile(os.Args[1]);if e!=nil{fail(e.Error())}
 rows:=strings.Split(string(raw),"\n");seen:=make(map[int]bool)
 certified:=map[int]bool{0:true,3:true,9:true,12:true}
 cheap,expensive,open,proven:=0,0,0,0
 done:=0
 for _,line:=range rows{
  if strings.HasPrefix(line,"R0_SOURCE_ROOT "){
   w:=strings.Fields(line);a:=int(uintField(w,"FIRST"))
   if a<0||a>=18||seen[a]{fail("root missing/duplicate/out of bounds")}
   seen[a]=true
   action:=string("URFDLB"[a/3])+[]string{"","'","2"}[a%3]
   if field(w,"MOVE")!=action{fail("wrong original face action name")}
   children:=0;v:=uint64(10)
   for b:=0;b<18;b++{if legal(a,b){children++;v+=weight(b,8)}}
   if uintField(w,"SECOND_CHILDREN")!=uint64(children)||uintField(w,"EXACT_VIRTUAL_IDDFS_CALLS")!=v{
    fail(fmt.Sprintf("source canonical workload not independently reproduced for action %d",a))
   }
   if (uintField(w,"FULL_ABSENCE_CERTIFIED")==1)!=certified[a]{fail("historic per-root proof classification changed")}
   if uintField(w,"UNVERIFIED_GOAL_INTERSECTION")!=1{fail("unexpected new native proof claim")}
   if children==12{cheap++}else if children==15{expensive++}else{fail("illegal child count")}
   if certified[a]{proven++}else{open++}
  }else if strings.HasPrefix(line,"R0_SOURCE_STABILIZER_AUDIT_PASS "){
   if done!=0{fail("two final source audit verdicts")};done++
   w:=strings.Fields(line)
   if field(w,"VERSION")!="0.26"||uintField(w,"PHYSICAL_PROPER_ROTATIONS")!=24||
    uintField(w,"IDENTITY_FIXED")!=1||uintField(w,"CHEAP_12_CHILD_ROOTS")!=9||
    uintField(w,"EXPENSIVE_15_CHILD_ROOTS")!=9||
    uintField(w,"PREVIOUS_CERTIFIED_ROOTS")!=4||uintField(w,"OPEN_ROOTS")!=14||
    uintField(w,"GLOBAL_LOWER17_CLAIMED")!=0||uintField(w,"ROOT_CERTIFICATE_UPGRADE")!=0{
     fail("physical source status or author claims drift")
   }
  }
 }
 if len(seen)!=18||cheap!=9||expensive!=9||proven!=4||open!=14||done!=1{fail("full canonical source action set was not audited")}
 fmt.Printf("R0_INDEPENDENT_GO_ALL_18_SOURCE_GRAMMAR_PASS ROOTS 18 CHEAP 9 EXPENSIVE 9 PREVIOUS_CERTIFIED 4 OPEN 14 NO_NEW_DISTANCE_PROOF 1\n")
}
