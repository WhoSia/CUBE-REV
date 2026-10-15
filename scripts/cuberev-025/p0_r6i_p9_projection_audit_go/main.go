// P0-R6I-P9 independent full original C6/C7/E6 projection auditing.
// Derive C6/E6 from EVERY original 8,240,087 whole CP/CO/EP/EO B6 row;
// recompute C7 as the full one-move image closure of the entire C6 set,
// using independently implemented packed corner moves from the source
// 54-sticker-derived 18-turn table and explicit group-order checks.
// Compare every sorted U64 entry, independent domain-separated SHA256,
// and reject any mutation, omitted C7 transition, duplicate or extra row.
// Does not independently reimplement 54-facelet to cubie turn construction.
package main
import("crypto/sha256";"encoding/binary";"encoding/hex";"fmt";"io";"os";"sort";"strconv";"strings")
func bad(s string){fmt.Fprintln(os.Stderr,"P9_PROJECTION_GO_FAIL",s);os.Exit(2)}
const goldenB6="82fe545bcad3537c989ec22afce9d286926ddce5f4ef9428c0307951ec2d0979"
type Turn struct{cp,co [8]uint8}
func readTurns(p string)[18]Turn{
 data,e:=os.ReadFile(p);if e!=nil||len(data)!=288{bad("18 physical turn snapshots not exactly 288 bytes")}
 var ts [18]Turn
 for a:=0;a<18;a++{
  var seen uint16
  for i:=0;i<8;i++{
   id,tw:=data[a*16+i],data[a*16+8+i]
   if id>=8||tw>=3||seen&(1<<id)!=0{bad("invalid physical corner move")}
   seen|=1<<id;ts[a].cp[i],ts[a].co[i]=id,tw
  }
  if seen!=255{bad("nonbijective original physical corner turn")}
 }
 solved:=uint64(0)
 for i:=0;i<8;i++{solved|=uint64(i)<<(3*i)}
 for base:=0;base<18;base+=3{
  x:=solved
  for i:=1;i<=4;i++{
   x=move(x,ts[base])
   if i==2&&x!=move(solved,ts[base+2]){bad("original squared 18HTM generator action not consistent")}
   if i==3&&x!=move(solved,ts[base+1]){bad("original inverted 18HTM generator action not consistent")}
   if i==4&&x!=solved{bad("original quarter turn not order4")}
  }
 }
 return ts
}
func move(c uint64,t Turn)uint64{
 var next uint64
 for i:=0;i<8;i++{
  from:=uint(t.cp[i])
  cp:=(c>>(3*from))&7
  co:=(c>>(24+2*from))&3
  next|=cp<<(3*uint(i))
  next|=((co+uint64(t.co[i]))%3)<<(24+2*uint(i))
 }
 return next
}
func unique(a []uint64)[]uint64{
 sort.Slice(a,func(i,j int)bool{return a[i]<a[j]})
 if len(a)==0{return a}
 n:=1
 for i:=1;i<len(a);i++{if a[i]!=a[n-1]{a[n]=a[i];n++}}
 return a[:n]
}
func countAndDigest(p,label string,expected []uint64)string{
 f,e:=os.Open(p);if e!=nil{bad("missing sorted native projection "+label)};defer f.Close()
 st,e:=f.Stat();if e!=nil||st.Size()!=int64(len(expected))*8{bad("projection size mismatch "+label)}
 h:=sha256.New()
 header:=fmt.Sprintf("CUBE-REV-025-P9:PROJECTED-U64LE:v1;type=%s;goal-radius=6;count=%d\n",label,len(expected))
 h.Write([]byte(header))
 var b [8]byte
 for i,want:=range expected{
  if _,e:=io.ReadFull(f,b[:]);e!=nil{bad("truncated "+label)}
  h.Write(b[:])
  actual:=binary.LittleEndian.Uint64(b[:])
  if actual!=want{bad(fmt.Sprintf("projection %s sorted exact row mismatch index %d",label,i))}
  if i>0&&actual<=expected[i-1]{bad("non-strict projection order "+label)}
 }
 return hex.EncodeToString(h.Sum(nil))
}
func key(line,k string)string{
 parts:=strings.Fields(line)
 for i:=0;i+1<len(parts);i++{if parts[i]==k{return parts[i+1]}}
 bad("missing field "+k);return ""
}
func number(line,k string)uint64{
 n,e:=strconv.ParseUint(key(line,k),10,64);if e!=nil{bad("non-numeric "+k)};return n
}
func main(){
 if len(os.Args)!=4{bad("usage: filename_prefix actual_native.log audit|pilot")}
 prefix:=os.Args[1]
 native,e:=os.ReadFile(os.Args[2]);if e!=nil{bad("original physical native log missing")}
 mode:=os.Args[3];if mode!="audit"&&mode!="pilot"{bad("invalid native mode")}
 log:=string(native)
 if strings.Contains(log,"P9_HOLD")||strings.Contains(log,"P9_ERROR")||
  strings.Contains(log,"P9_TRUE_FULL_CUBIE_MEET"){bad("failed physical original court or source pilot")}
 var actual map[string]string=map[string]string{}
 foundGoal,foundComplete,leafs:=false,false,0
 for _,line:=range strings.Split(log,"\n"){
  line=strings.TrimSpace(line)
  if strings.HasPrefix(line,"P9_PROJECTION "){
   label:=key(line,"TYPE")
   if label!="C6"&&label!="C7"&&label!="E6"{bad("unrecognized projection type")}
   if _,ok:=actual[label];ok{bad("duplicate native projected set receipt")}
   actual[label]=key(line,"SHA256")
   if key(line,"ORIG_FULL_GOAL_SHA256")!=goldenB6{bad("native goal mismatch")}
  }else if strings.HasPrefix(line,"P9_PROJECTIONS_COMPLETE "){
   if foundGoal||key(line,"GOAL_SHA256")!=goldenB6||number(line,"MOVE_TABLE_BYTES")!=288||
    number(line,"FULL_GOAL_KEYS")!=8240087||number(line,"CORNER_C6")!=1405068||
    number(line,"CORNER_C7")!=6807696||number(line,"EDGE_E6")!=7672278||
    number(line,"SOURCE_PILOT")!=map[string]uint64{"audit":0,"pilot":1}[mode]{bad("original goal, radius and move table physical contract")}
   foundGoal=true
  }else if strings.HasPrefix(line,"P9_OPEN_B10_PILOT "){
   leafs++
   if mode!="pilot"||leafs>2||number(line,"CASE")!=uint64(leafs)||
     number(line,"TRUE_FULL_CUBIE_HITS")!=0||number(line,"COMPLETE_LOCAL_B10")!=1||
     number(line,"GLOBAL_B10_COMPLETE")!=0||key(line,"GOAL_SHA256")!=goldenB6{
     bad("partial R10 source physical certificate not typed")
   }
   a,b:=number(line,"FIRST"),number(line,"SECOND")
   if !((leafs==1&&a==3&&b==0)||(leafs==2&&a==12&&b==0)){bad("not the two original OPEN B10 first-action source cylinders")}
   if number(line,"WORD_CALLS")!=1310203083||
      number(line,"VISITED")+number(line,"OMITTED")!=1310203083||
      number(line,"EDGES")>number(line,"PAIRS"){bad("incomplete original physical B10 source leaf")}
  }else if strings.HasPrefix(line,"P9_COMPLETE "){
   if foundComplete||!foundGoal||key(line,"MODE")!=mode||
     key(line,"GOAL_SHA256")!=goldenB6||number(line,"TARGET_IMMUTABLE")!=1||
     number(line,"PILOT_PREFIXES")!=uint64(map[string]int{"audit":0,"pilot":2}[mode])||
     number(line,"GLOBAL_B10_COMPLETE")!=0||number(line,"LOWER17_CLAIMED")!=0{bad("missing immutable original end certificate")}
   foundComplete=true
  }
 }
 if !foundComplete||len(actual)!=3||leafs!=map[string]int{"audit":0,"pilot":2}[mode]{bad("physical source/projection receipt incomplete")}
 turns:=readTurns(prefix+"-turns.bin")
 whole,e:=os.Open(prefix+"-B6.bin");if e!=nil{bad("missing actual C++ whole B6 snapshot")};defer whole.Close()
 st,e:=whole.Stat();if e!=nil||st.Size()!=8240087*16{bad("wrong original whole B6 snapshot length")}
 h:=sha256.New();h.Write([]byte("CUBE-REV-025-P8:FULL-CP-CO-EP-EO:LE64x2:v1;radius=6;count=8240087\n"))
 c6:=make([]uint64,0,8240087);e6:=make([]uint64,0,8240087)
 var buf [16]byte;var cPrev,ePrev uint64
 for i:=0;i<8240087;i++{
  if _,e:=io.ReadFull(whole,buf[:]);e!=nil{bad("truncated real whole 8M goal")}
  h.Write(buf[:])
  c,edge:=binary.LittleEndian.Uint64(buf[:8]),binary.LittleEndian.Uint64(buf[8:])
  if i>0&&(c<cPrev||(c==cPrev&&edge<=ePrev)){bad("whole goal ordering regression")}
  cPrev,ePrev=c,edge
  c6=append(c6,c);e6=append(e6,edge)
 }
 if hex.EncodeToString(h.Sum(nil))!=goldenB6{bad("whole original B6 goal SHA mismatch Go independent")}
 c6=unique(c6);e6=unique(e6)
 if len(c6)!=1405068||len(e6)!=7672278{bad("entire original goal projection distinct counts not confirmed")}
 c7:=make([]uint64,0,len(c6)*19)
 c7=append(c7,c6...)
 for _,c:=range c6{
  for a:=0;a<18;a++{c7=append(c7,move(c,turns[a]))}
 }
 c7=unique(c7)
 if len(c7)!=6807696{bad("genuine C7 closure from entire original C6 is not native C7")}
 for _,item:=range []struct{label string; arr []uint64}{
  {"C6",c6},{"C7",c7},{"E6",e6},
 }{
  d:=countAndDigest(prefix+"-"+item.label+".bin",item.label,item.arr)
  if actual[item.label]!=d{bad("native/Go domain separated SHA different for "+item.label)}
  fmt.Printf("P9_GO_EXACT_PROJECTION_PASS TYPE %s COUNT %d SHA256 %s ORIGINAL_B6_SHA256 %s INDEPENDENT_ALL_ROWS_AND_C7_ONE_STEP_CLOSURE 1\n",item.label,len(item.arr),d,goldenB6)
 }
 fmt.Printf("P9_GO_INDEPENDENT_PROJECTION_CLOSURE_PASS GOAL_SHA256 %s WHOLE_GOAL_ROWS 8240087 C6 1405068 C7 6807696 E6 7672278 C7_RECOMPUTED_FROM_ALL_C6_THROUGH_ALL18_REAL_ACTIONS 1 PHYSICAL_QUARTER_TURN_ORDER_REGRESSION 1 SOURCE_PILOT_LEAVES %d B10_GLOBAL_COMPLETE 0 LOWER17_NOT_CLAIMED 1\n",goldenB6,leafs)
}
