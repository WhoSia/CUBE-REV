// CUBE-REV 0.26 R3: independent packed-corner group C8-from-C7 GO witness
// and exact original 18HTM grammar/physical source prefix receipt verifier.
// No external modules. Does NOT independently rebuild full 54-sticker B6.
package main
import(
 "crypto/sha256";"encoding/binary";"encoding/hex";"fmt";"math";"math/bits";"os";"strconv";"strings"
)
const c7n=6807696
const domain=40320*2187
const originalC7="2fd2a3692147e81cc8bf970bcbbbdde061551065268e207d60aec4354ccd67e6"
const originalGoal="82fe545bcad3537c989ec22afce9d286926ddce5f4ef9428c0307951ec2d0979"
const c7header="CUBE-REV-025-P9:PROJECTED-U64LE:v1;type=C7;goal-radius=6;count=6807696\n"
const c8header="CUBE-REV-026-R3:C8-DENSE-BITSET:v1;domain=88179840;source=ORIGINAL-P9-C7\n"
func fail(s string){fmt.Fprintln(os.Stderr,"R3_GO_REJECT",s);os.Exit(2)}
func canonical(prev,a int)bool{
 if prev<0{return true}
 f,g:=prev/3,a/3
 if f==g{return false}
 opp:=(f==0&&g==3)||(f==3&&g==0)||(f==1&&g==4)||(f==4&&g==1)||(f==2&&g==5)||(f==5&&g==2)
 return !opp||g>=f
}
func mass(last,rem int)uint64{
 var dp [18]uint64
 n:=uint64(rem+1)
 for d:=1;d<=rem;d++{
  var next [18]uint64
  if d==1{for a:=0;a<18;a++{if canonical(last,a){next[a]=1}}}else{
   for b,x:=range dp{for a:=0;a<18;a++{if canonical(b,a){next[a]+=x}}}
  }
  dp=next;var sum uint64;for _,x:=range dp{sum+=x}
  n+=uint64(rem-d+1)*sum
 }
 return n
}
func rank(x uint64)uint32{
 mask:=uint16(255);p,co,mul,charge:=uint32(0),uint32(0),uint32(1),uint32(0)
 for i:=0;i<8;i++{
  v:=uint16((x>>uint(3*i))&7);o:=uint32((x>>uint(24+2*i))&3)
  if o>=3||mask&(1<<v)==0{fail("invalid physical corner key CP or CO")}
  p=p*uint32(8-i)+uint32(bits.OnesCount16(mask&((1<<v)-1)))
  mask^=1<<v;charge+=o
  if i<7{co+=o*mul;mul*=3}
 }
 if mask!=0||charge%3!=0||p>=40320||co>=2187{fail("illegal corner orientation/perm rank")}
 return p*2187+co
}
func packTurn(c uint64,actions []byte,a int)uint64{
 row:=actions[a*16:(a+1)*16]
 var n uint64
 for i:=0;i<8;i++{
  prev:=uint(row[i]);if prev>=8{fail("bad actual CP turn array")}
  p:=(c>>(3*prev))&7
  o:=(c>>(24+2*prev))&3
  shift:=uint64(row[8+i])
  if shift>=3{fail("bad CO action")}
  n|=p<<uint(3*i);n|=((o+shift)%3)<<uint(24+2*i)
 }
 return n
}
func get(w []string,k string)string{
 for i:=0;i+1<len(w);i++{if w[i]==k{return w[i+1]}}
 fail("missing "+k);return ""
}
func integer(w []string,k string)uint64{
 v,e:=strconv.ParseUint(get(w,k),10,64)
 if e!=nil{fail("invalid integer "+k)}
 return v
}
func num(w []string,k string)float64{
 v,e:=strconv.ParseFloat(get(w,k),64)
 if e!=nil||math.IsNaN(v)||math.IsInf(v,0){fail("invalid numeric "+k)}
 return v
}
type Record struct{visit,omit,pairs,full,guard,extra uint64;time float64}
func main(){
 if len(os.Args)!=4{fail("usage: exact native C7.bin original physical corner turns.bin raw-native-log")}
 src,e:=os.ReadFile(os.Args[1]);if e!=nil{fail(e.Error())}
 actions,e:=os.ReadFile(os.Args[2]);if e!=nil{fail(e.Error())}
 log,e:=os.ReadFile(os.Args[3]);if e!=nil{fail(e.Error())}
 if len(src)!=c7n*8||len(actions)!=18*16{fail("C7/physical action byte size drift")}
 h:=sha256.New();h.Write([]byte(c7header));h.Write(src)
 if hex.EncodeToString(h.Sum(nil))!=originalC7{fail("immutable original C7 independent SHA invalid")}
 table:=make([]uint64,(domain+63)/64);var last uint64
 for i:=0;i<c7n;i++{
  c:=binary.LittleEndian.Uint64(src[i*8:])
  if i>0&&c<=last{fail("C7 original key not strictly sorted")}
  last=c
  k:=rank(c);table[k/64]|=1<<uint(k%64)
  for a:=0;a<18;a++{
   next:=packTurn(c,actions,a);idx:=rank(next);table[idx/64]|=1<<uint(idx%64)
  }
 }
 var c8count uint64
 h=sha256.New();h.Write([]byte(c8header));var buf[8]byte
 for _,v:=range table{
  c8count+=uint64(bits.OnesCount64(v))
  binary.LittleEndian.PutUint64(buf[:],v);h.Write(buf[:])
 }
 c8sha:=hex.EncodeToString(h.Sum(nil))
 if c8count<c7n||c8count>domain{fail("constructed C8 impossible cardinality")}
 lines:=strings.Split(string(log),"\n")
 var build,finish int;var rows [2][2]Record;seen:=[2][2]bool{};pairs:=[2]bool{}
 for _,line:=range lines{
  if strings.HasPrefix(line,"R3_C8_BUILD_PASS "){
   if build!=0{fail("multiple original physical C8 builds")};build++
   w:=strings.Fields(line)
   if integer(w,"C7_COUNT")!=c7n||integer(w,"C8_COUNT")!=c8count||
    integer(w,"DOMAIN")!=domain||integer(w,"BITSET_BYTES")!=domain/8||
    integer(w,"C7_ALL_CONTAINED")!=c7n||
    get(w,"C7_SHA")!=originalC7||get(w,"GOAL_SHA")!=originalGoal||
    get(w,"C8_SHA")!=c8sha||num(w,"BUILD_MS")<=0{
    fail("original C8 native witness not independently reproduced")
   }
  }else if strings.HasPrefix(line,"R3_ACTUAL_MATCHED "){
   w:=strings.Fields(line);first:=int(integer(w,"FIRST"));second:=int(integer(w,"SECOND"))
   if build!=1||second!=1||(first!=15&&first!=16)||!canonical(first,second){fail("wrong original source grammar")}
   i:=first-15;mode:=get(w,"MODE");j:=0;if mode=="C8_GUARD"{j=1}else if mode!="BASELINE"{fail("unknown original mode")}
   if seen[i][j]{fail("duplicate physical receipt")};seen[i][j]=true
   if integer(w,"WORD_CALLS")!=mass(second,8)||
    integer(w,"WHOLE_GOAL_HITS")!=0||
    integer(w,"COMPLETE_DEPTH2_SOURCE")!=1||integer(w,"NEW_FIRST_ROOT")!=0{
    fail("false original DFA coverage/goal certificate")
   }
   x:=Record{visit:integer(w,"VISITED"),omit:integer(w,"OMITTED"),pairs:integer(w,"PAIRS"),
    full:integer(w,"FULL_QUERIES"),guard:integer(w,"C8_REJECT"),
    extra:integer(w,"C8_EXTRA_OMITTED"),time:num(w,"SEARCH_MS")}
   if x.visit+x.omit!=mass(second,8)||x.time<=0{fail("incorrect actual source search mass/time")}
   if j==0&&(x.guard!=0||x.extra!=0){fail("baseline incorrectly used extra C8 pruning")}
   if j==1&&x.extra<x.guard{fail("C8 subtree accounting broken")}
   rows[i][j]=x
  }else if strings.HasPrefix(line,"R3_PAIRED_ORIGINAL "){
   w:=strings.Fields(line);first:=int(integer(w,"FIRST"));second:=integer(w,"SECOND")
   if (first!=15&&first!=16)||second!=1{fail("wrong pair")}
   i:=first-15
   if pairs[i]||!seen[i][0]||!seen[i][1]{fail("pair missing original measured rows")}
   a,b:=rows[i][0],rows[i][1]
   if b.visit>a.visit||b.omit<a.omit||b.visit+b.omit!=a.visit+a.omit{
    fail("invalid C8 monotone source-visit hypothesis")
   }
   if integer(w,"VISITS_SAVED")!=a.visit-b.visit||
    integer(w,"EXTRA_OMITTED")!=b.omit-a.omit||
    math.Abs(num(w,"C8_OVER_BASE_RATIO")-b.time/a.time)>0.000002||
    integer(w,"TRUE_GOAL_ABSENCE_BOTH")!=1||integer(w,"FIRST_ROOT_COMPLETE")!=0{
    fail("matched performance/proof-pair summary forged")
   }
   pairs[i]=true
  }else if strings.HasPrefix(line,"R3_COMPLETE_ORIGINAL_C8_DFA_PILOT_PASS "){
   if finish!=0{fail("duplicate original physical final footer")};finish++
   w:=strings.Fields(line)
   if !pairs[0]||!pairs[1]||
    integer(w,"C8_COUNT")!=c8count||get(w,"C8_SHA")!=c8sha||
    get(w,"GOAL_SHA")!=originalGoal||
    integer(w,"COMPLETE_DEPTH2_PREFIXES")!=2||
    integer(w,"ORIGINAL_FIRST16_SECOND1_NEGATIVE")!=1||
    integer(w,"FIRST_ROOTS_CERTIFIED")!=5||integer(w,"FIRST_ROOTS_OPEN")!=13||
    integer(w,"NEW_FIRST_ROOT")!=0||integer(w,"GLOBAL_LOWER17_CLAIMED")!=0{
    fail("original source certificate overclaim")
   }
  }
 }
 if build!=1||finish!=1||!pairs[0]||!pairs[1]{fail("incomplete original C8/projection/physical measurement")}
 fmt.Printf("R3_GO_TRUE_INDEPENDENT_C8_PASS CORNER_DOMAIN %d C8_COUNT %d C8_SHA %s PREFIXES 2 FIRST16_SECOND1_NEGATIVE 1 NO_NEW_FIRST_ROOT 1\n",domain,c8count,c8sha)
}
