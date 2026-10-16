// CUBE-REV P12-P4: inverse-class normalized relative corner permutations
// and true 48-automorphism corner position graph conjugation orbit court.
// Source: original full-B6 576 exact pair witness TSV and native 18HTM
// 288-byte corner turn table. NO lifted CP/CO/EP/EO symmetry is assumed.
package main

import (
 "bufio"
 "encoding/hex"
 "fmt"
 "math/bits"
 "os"
 "sort"
 "strconv"
 "strings"
)

type Perm [8]uint8
type PairSig struct { a,b uint64; fiber int; cycle string; rel Perm }
type OrbitSig struct { n,w int; cycle string; metric [4]int }
func fail(reason string) { fmt.Fprintln(os.Stderr,"P12_P4_FAIL",reason);os.Exit(2) }
func cp(c uint64,i int)uint8{return uint8((c>>uint(3*i))&7)}
func co(c uint64,i int)uint8{return uint8((c>>uint(24+2*i))&3)}
func formatPerm(p Perm) string {var b [8]byte; for i,v:=range p{b[i]='0'+v};return string(b[:])}
func inverse(p Perm)Perm{var out Perm; for i,v:=range p{out[v]=uint8(i)};return out}
func norm(p Perm)string{a,b:=formatPerm(p),formatPerm(inverse(p));if a<b{return a};return b}
func conj(p,g Perm)Perm {
 inv:=inverse(g);var out Perm
 for i:=0;i<8;i++ {out[i]=g[p[inv[i]]]}
 return out
}
func cycleName(p Perm) string{
 var seen [8]bool
 lens:=[]int{}
 for i:=0;i<8;i++{if seen[i]{continue}; j,n:=i,0
  for !seen[j]{seen[j]=true;n++;j=int(p[j])}
  if n>1{lens=append(lens,n)}
 }
 sort.Ints(lens)
 if len(lens)==2&&lens[0]==2&&lens[1]==2{return "2+2"}
 if len(lens)==2&&lens[0]==2&&lens[1]==4{return "2+4"}
 fail("unexpected relative permutation type");return ""
}
func rel(a,b uint64)Perm{
 var inv [8]uint8;var seenA,seenB [8]bool
 for i:=0;i<8;i++{x,y:=cp(a,i),cp(b,i);if seenA[x]||seenB[y]||co(a,i)>2||co(b,i)>2{fail("invalid original corner state")};seenA[x]=true;seenB[y]=true;inv[x]=uint8(i)}
 var p Perm
 for i:=0;i<8;i++{p[i]=inv[cp(b,i)]}
 return p
}
func graphFromPhysical(turns []byte)[8][8]bool {
 if len(turns)!=288{fail("original P9 physical turn table not exactly 288 bytes")}
 var faces [6]uint8
 for f:=0;f<6;f++{var seen,changed uint8
  for i:=0;i<8;i++{v:=turns[(f*3)*16+i];if v>=8||seen&(1<<v)!=0{fail("invalid face turn permutation")};seen|=1<<v;if v!=uint8(i){changed|=1<<uint(i)}}
  if seen!=255||bits.OnesCount8(changed)!=4{fail("face turn must move four corners")};faces[f]=changed
 }
 var adj [8][8]bool
 edges:=0
 for i:=0;i<8;i++{for j:=i+1;j<8;j++{n:=0;for _,f:=range faces{if f&(1<<uint(i))!=0&&f&(1<<uint(j))!=0{n++}}
   if n==2{adj[i][j]=true;adj[j][i]=true;edges++}else if n>2{fail("two vertices share more than two faces")}
 }}
 if edges!=12{fail("physical graph not 12 edges")}
 return adj
}
func allGraphAutos(adj [8][8]bool)[]Perm {
 autos:=[]Perm{}
 var p Perm
 var rec func(int,uint8)
 rec=func(i int,used uint8){
  if i==8{
   for a:=0;a<8;a++{for b:=0;b<8;b++{if adj[a][b]!=adj[p[a]][p[b]]{return}}}
   autos=append(autos,p);return
  }
  for j:=uint8(0);j<8;j++{if used&(1<<j)==0{p[i]=j;rec(i+1,used|(1<<j))}}
 }
 rec(0,0)
 if len(autos)!=48{fail("physical Q3 full graph automorphism group != 48")}
 return autos
}
// The Q3 distance histogram is invariant under vertex-isometric conjugation
// and under reversal of the unordered relative permutation label.
func graphDistance(adj [8][8]bool)[8][8]int {
 var d [8][8]int
 for i:=0;i<8;i++ {for j:=0;j<8;j++ {
  if i==j{d[i][j]=0}else if adj[i][j]{d[i][j]=1}else{d[i][j]=99}
 }}
 for k:=0;k<8;k++{for i:=0;i<8;i++{for j:=0;j<8;j++ {
  if d[i][k]+d[k][j]<d[i][j]{d[i][j]=d[i][k]+d[k][j]}
 }}}
 for i:=0;i<8;i++{for j:=0;j<8;j++{if d[i][j]>3{fail("original Q3 graph disconnected")}}}
 return d
}
func metricProfile(p Perm,d [8][8]int)[4]int {
 var profile [4]int
 for i:=0;i<8;i++{profile[d[i][p[i]]]++}
 return profile
}
func readPairs(path string)([]PairSig,map[string]int,int){
 f,e:=os.Open(path);if e!=nil{fail("open pair ledger "+e.Error())};defer f.Close()
 sc:=bufio.NewScanner(f);if !sc.Scan(){fail("empty pair ledger")}
 if sc.Text()!="corner1_u64\tcorner2_u64\tfiber_size\tcp_cycle\trelative_cp_perm\tcp_mask_hex\tco_mask_hex\tco_overlap_hex\tplus\tminus"{fail("wrong pair ledger header")}
 pairs:=[]PairSig{};counts:=make(map[string]int);oriented:=make(map[string]bool)
 observed:=make(map[[2]uint64]bool)
 coarse:=make(map[string]int)
 for sc.Scan(){parts:=strings.Split(sc.Text(),"\t");if len(parts)!=10{fail("wrong pair ledger row")}
  a,e:=strconv.ParseUint(parts[0],10,64);if e!=nil{fail("bad corner a")}
  b,e:=strconv.ParseUint(parts[1],10,64);if e!=nil{fail("bad corner b")}
  fs,e:=strconv.Atoi(parts[2]);if e!=nil{fail("bad fiber size")}
  if a==b||fs!=1&&fs!=4{fail("invalid source pair")}
  if observed[[2]uint64{a,b}]{fail("duplicate pair ledger entry")};observed[[2]uint64{a,b}]=true
  p:=rel(a,b)
  if formatPerm(p)!=parts[4]{fail("relative map mismatch to original CP packed bytes")}
  cy:=cycleName(p);if cy!=parts[3]{fail("cycle name mismatch")}
  mask:=uint8(0);coMask:=uint8(0);plus,minus:=0,0
  for i:=0;i<8;i++{if cp(a,i)!=cp(b,i){mask|=1<<uint(i)}
   d:=(int(co(b,i))-int(co(a,i))+3)%3
   if d!=0{coMask|=1<<uint(i)}
   if d==1{plus++};if d==2{minus++}
  }
  byteHex:=func(s string)uint8{raw,e:=hex.DecodeString(s);if e!=nil||len(raw)!=1{fail("invalid support mask")};return raw[0]}
  if byteHex(parts[5])!=mask||byteHex(parts[6])!=coMask||byteHex(parts[7])!=(mask&coMask){fail("changed-position mask mismatch")}
  v1,e:=strconv.Atoi(parts[8]);if e!=nil||v1!=plus{fail("plus twist mismatch")}
  v2,e:=strconv.Atoi(parts[9]);if e!=nil||v2!=minus{fail("minus twist mismatch")}
  if cy=="2+2"&&fs!=4||cy=="2+4"&&fs!=1{fail("fiber size/cycle contradiction")}
  if coMask & ^mask != 0{fail("CO support not subset of CP support")}
  if (plus+2*minus)%3!=0{fail("corner twist conservation fail")}
  if (cy=="2+2"&&bits.OnesCount8(mask)!=4)||(cy=="2+4"&&bits.OnesCount8(mask)!=6){fail("relative support does not match cycle")}
  coarse[fmt.Sprintf("%s/%d",cy,fs)]++
  key:=norm(p);counts[key]++;oriented[formatPerm(p)]=true
  pairs=append(pairs,PairSig{a,b,fs,cy,p})
 }
 if e:=sc.Err();e!=nil{fail(e.Error())}
 if len(pairs)!=576||coarse["2+2/4"]!=384||coarse["2+4/1"]!=192||len(coarse)!=2{fail("original P12 576 pair counts not reproduced")}
 return pairs,counts,len(oriented)
}
func main(){
 if len(os.Args)!=3{fail("usage: p12p4 original-P9-turns.bin original-P12P3-576-pairs.tsv")}
 turns,e:=os.ReadFile(os.Args[1]);if e!=nil{fail(e.Error())}
 adj:=graphFromPhysical(turns)
 distances:=graphDistance(adj)
 group:=allGraphAutos(adj)
 pairs,counts,oriented:=readPairs(os.Args[2])
 if oriented!=108||len(counts)!=102{fail("raw 108 or inverse-normalized 102 relative permutations changed")}
 unseen:=make(map[string]bool);for key:=range counts{unseen[key]=true}
 orbits:=[]OrbitSig{}
 for len(unseen)>0{
  seed:="";for k:=range unseen{if seed==""||k<seed{seed=k}}
  var p Perm;for i:=0;i<8;i++{p[i]=seed[i]-'0'}
  orb:=make(map[string]bool)
  for _,g:=range group{orb[norm(conj(p,g))]=true}
  freq:=counts[seed]
  ctype:=cycleName(p)
  profile:=metricProfile(p,distances)
  if profile!=metricProfile(inverse(p),distances){fail("inverse-class has different Q3 metric profile")}
  for key:=range orb{
   var q Perm;for i:=0;i<8;i++{q[i]=key[i]-'0'}
   if metricProfile(q,distances)!=profile{fail("graph-isometric conjugation changed displacement profile")}
   if counts[key]!=freq{fail(fmt.Sprintf("orbit not weight-preserving: orbitseed %s partner %s seedweight %d observed %d",seed,key,freq,counts[key]))}
   if !unseen[key]{fail("orbit overlap with already removed label")}
   delete(unseen,key)
  }
  orbits=append(orbits,OrbitSig{len(orb),freq,ctype,profile})
 }
 sort.Slice(orbits,func(i,j int)bool{if orbits[i].cycle!=orbits[j].cycle{return orbits[i].cycle<orbits[j].cycle};if orbits[i].n!=orbits[j].n{return orbits[i].n<orbits[j].n};return orbits[i].w<orbits[j].w})
 expected:=[]OrbitSig{{6,32,"2+2",[4]int{4,0,4,0}},{24,8,"2+2",[4]int{4,2,0,2}},{24,4,"2+4",[4]int{2,4,2,0}},{48,2,"2+4",[4]int{2,1,4,1}}}
 if len(orbits)!=len(expected){fail("unexpected number of inverse-class conjugation orbits")}
 nLabels,total:=0,0
 for i,o:=range orbits{
  if o!=expected[i]{fail(fmt.Sprintf("orbit expected %+v got %+v",expected[i],o))}
  nLabels+=o.n;total+=o.n*o.w
  fmt.Printf("P12_P4_ORBIT CYCLE %s DISTINCT_UNDIRECTED_REL_MAPS %d PAIRS_PER_MAP %d TOTAL_PAIRS %d GRAPH_STABILIZER_ORDER %d Q3_METRIC_PROFILE %d,%d,%d,%d\n",o.cycle,o.n,o.w,o.n*o.w,48/o.n,o.metric[0],o.metric[1],o.metric[2],o.metric[3])
 }
 if nLabels!=102||total!=576||len(pairs)!=576{fail("the four orbit totals do not exhaust 576")}
 fmt.Printf("P12_P4_INVERSE_CONJUGACY_ORBIT_PASS ORIGINAL_B6_FIBER_PAIRS 576 RAW_RELATIVE_CP_MAPS %d UNDIRECTED_INVERSE_LABELS %d Q3_AUTOMORPHISMS %d ORBITS 4 WEIGHT_UNIFORM 1 GOAL_B6_JOINT_CUBIE_AUTOMORPHISM_PROVEN 0 SOURCE_FIXED_SYMMETRY_PROVEN 0 GLOBAL_LOWER17_CLAIMED 0\n",oriented,nLabels,len(group))
}
