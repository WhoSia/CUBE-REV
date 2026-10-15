// CUBE-REV P0-R6I independent Go verifier of physical 43-cylinder
// mixed-depth ORIGINAL source B3/B3 and B6/B7 court receipts.
package main
import("fmt";"os";"strings";"strconv")
func fail(s string){fmt.Fprintln(os.Stderr,"P0R6I_PHYSICAL_GO_AUDIT_FAIL",s);os.Exit(2)}
func get(l,k string)uint64{
 w:=strings.Fields(l)
 for i:=0;i+1<len(w);i++{if w[i]==k{
  v,e:=strconv.ParseUint(w[i+1],10,64);if e==nil{return v}
 }}
 fail("missing/bad integer "+k);return 0
}
func signed(l,k string)int{
 w:=strings.Fields(l)
 for i:=0;i+1<len(w);i++{if w[i]==k{
  v,e:=strconv.Atoi(w[i+1]);if e==nil{return v}
 }}
 fail("missing signed field "+k);return 0
}
func legal(last,a int)bool{
 if last<0{return true}
 x,y:=last/3,a/3
 if x==y{return false}
 opposite:=(x==0&&y==3)||(x==3&&y==0)||
 (x==1&&y==4)||(x==4&&y==1)||
 (x==2&&y==5)||(x==5&&y==2)
 return !opposite||y>=x
}
func weight(last,k int)uint64{
 var prior [18]uint64
 total:=uint64(k+1)
 for d:=1;d<=k;d++{
  var now [18]uint64
  if d==1{
   for a:=0;a<18;a++{if legal(last,a){now[a]=1}}
  }else{
   for b,c:=range prior{for a:=0;a<18;a++{
    if legal(b,a){now[a]+=c}
   }}
  }
  prior=now
  var layer uint64
  for _,c:=range now{layer+=c}
  total+=uint64(k-d+1)*layer
 }
 return total
}
func main(){
 if len(os.Args)!=4{fail("usage: original-job.log goalRadius sourceRadius")}
 goal,e:=strconv.Atoi(os.Args[2]);if e!=nil{fail("goal bad")}
 source,e:=strconv.Atoi(os.Args[3]);if e!=nil{fail("source bad")}
 if !(goal==3&&source==3)&&!(goal==6&&source==7){fail("only B3/B3 or B6/B7 official original physical court")}
 b,e:=os.ReadFile(os.Args[1]);if e!=nil{fail("missing actual Actions job log")}
 content:=string(b)
 goalSize:=uint64(3502);totalExpected:=uint64(3784)
 if source==7{goalSize=8240087;totalExpected=120213368}
 count:=0;gotGoal:=false;gotFinal:=false
 internal:=uint64(source+1+2*source)
 visited,skipped,weighted:=internal,uint64(0),internal
 seen:=make(map[string]bool)
 for _,line:=range strings.Split(content,"\n"){
  line=strings.TrimSpace(line)
  if strings.HasPrefix(line,"P0R6I_ORIGINAL_GOAL_FULL "){
   if gotGoal||get(line,"P0R6I_ORIGINAL_GOAL_FULL")!=goalSize||
     get(line,"ORIGINAL_PACKED_PHYSICAL_CASES")!=4608||
     get(line,"INTERNAL_ROOT_AND_PREFIX_CHECKS")!=3{fail("whole cubie goal/physics incorrect")}
   gotGoal=true
  }else if strings.HasPrefix(line,"P0R6I_PHYSICAL_CYLINDER_COMPLETE "){
   first:=signed(line,"FIRST");second:=signed(line,"SECOND")
   depth:=int(get(line,"DEPTH"))
   if first<0||first>17||!(depth==1||depth==2)||
     ((first==0||first==9)!=(depth==2)){fail("illegal exact mixed-depth prefix")}
   if depth==2 && (second<0||second>17||!legal(first,second)){fail("invalid canonical child")}
   if depth==1 && second!=-1{fail("first-action leaf wrongly has a second action")}
   id:=fmt.Sprintf("%d,%d",first,second)
   if seen[id]{fail("duplicate source cylinder")}
   seen[id]=true
   last:=first;if depth==2{last=second}
   base:=weight(last,source-depth)
   v:=get(line,"VISITED");sk:=get(line,"SKIPPED")
   if get(line,"WEIGHT")!=base||v+sk!=base||
      get(line,"COMPLETE_CUBIE_HITS")!=0{fail("physical source cylinder incomplete")}
   count++;visited+=v;skipped+=sk;weighted+=base
  }else if strings.HasPrefix(line,"P0R6I_ORIGINAL_43_MIXED_DEPTH_CUTSET_CERT "){
   if gotFinal||get(line,"COMPLETE")!=1||
     get(line,"LEAF_CYLINDERS")!=43||
     get(line,"INTERNAL_NODES")!=3||
     get(line,"INTERNAL_CALLS")!=internal||
     get(line,"TOTAL_BASELINE")!=totalExpected||
     get(line,"COMPLETE_CUBIE_HITS")!=0||
     get(line,"ORIGINAL_PHYSICAL_SOURCE_COMPLETE")!=1{fail("final global source condition broken")}
   gotFinal=true
   if get(line,"VISITED_INCLUDING_INTERNAL")!=visited||
     get(line,"SAFELY_SKIPPED")!=skipped{fail("C++ self-accounting diverges")}
  }
 }
 if !gotGoal||!gotFinal||count!=43||weighted!=totalExpected||
  visited+skipped!=totalExpected{fail("43 mixed-depth source grammar not fully covered")}
 for a:=0;a<18;a++{
  if a==0||a==9{
   for b:=0;b<18;b++{if legal(a,b){
    if !seen[fmt.Sprintf("%d,%d",a,b)]{fail("one legal child cylinder missing")}
   }}
  }else if !seen[fmt.Sprintf("%d,-1",a)]{fail("one first-action cylinder missing")}
 }
 fmt.Printf("P0R6I_GO_INDEPENDENT_ORIGINAL_43_CUTSET_PASS GOAL_RADIUS %d SOURCE_RADIUS %d EXACT_CYLINDERS 43 INTERNAL_CALLS %d FULL_SOURCE_BASELINE %d ACTUAL_VISITS %d SAFE_OMISSIONS %d WHOLE_CUBIE_HITS 0 REAL_ORIGINAL_PHYSICS_4608 1 LOWER17_NOT_CLAIMED 1\n",
   goal,source,internal,totalExpected,visited,skipped)
}
