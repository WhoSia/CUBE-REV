// CUBE-REV 0.26 — continuous 0.25 P12-P5 original 54-sticker physical proper rotation lift.
// A bounded native experiment, NOT a Lean proof of the entire global cube group.
// Correctly distinguishes proper spatial rotations (24) from all Q3 graph automorphisms (48).
#define main cuberev024_existing_solver_main_not_executed
#include "../../cuberev-024/p1_r3_true_54_facelet_multiaxis_dr_cpp/main.cpp"
#undef main
#include <fstream>
#include <unordered_map>
#include <unordered_set>
#include <sstream>
#include <set>
#include <random>
#include <iomanip>
struct Rot3{
 array<int,3> ix,sign;
 bool operator==(Rot3 const& r)const{return ix==r.ix&&sign==r.sign;}
};
int parity3(array<int,3> p){int inv=0;for(int i=0;i<3;i++)for(int j=i+1;j<3;j++)inv+=p[i]>p[j];return inv%2?-1:1;}
Vec apply(Rot3 r,Vec v){int a[3]={v.x,v.y,v.z};return {r.sign[0]*a[r.ix[0]],r.sign[1]*a[r.ix[1]],r.sign[2]*a[r.ix[2]]};}
vector<Rot3> properRotations(){
 vector<Rot3> out;array<int,3> p={0,1,2};
 do{for(int sx:{-1,1})for(int sy:{-1,1})for(int sz:{-1,1}){
  if(parity3(p)*sx*sy*sz==1)out.push_back({p,{sx,sy,sz}});
 }}while(next_permutation(p.begin(),p.end()));
 if(out.size()!=24)throw runtime_error("proper rotation group cardinality not24");
 return out;
}
Stickers frameTransform(Stickers s,Rot3 r){
 for(auto &st:s){
  const Vec origNorm=norm(st.c);
  st.p=apply(r,st.p);st.n=apply(r,st.n);
  st.c=faceOfNormal(apply(r,origNorm));
 }
 return s;
}
bool equalCube(Cube const&a,Cube const&b){return a.cp==b.cp&&a.co==b.co&&a.ep==b.ep&&a.eo==b.eo;}
Stickers cubieToStickers(Cube const&c){
 Stickers s=solvedStickers();
 auto change=[&](Vec p,Vec n,char val){
  int found=0;
  for(auto& st:s)if(st.p==p && st.n==n){st.c=val;found++;}
  if(found!=1)throw runtime_error("inverse facelet coordinate ambiguous");
 };
 for(int p=0;p<8;p++){
  int cub=c.cp[p],ori=c.co[p];
  if(cub>=8||ori>=3)throw runtime_error("invalid corner cubie");
  Vec pos={0,0,0};for(Vec n:cornerN[p])pos=plusv(pos,n);
  for(int i=0;i<3;i++){
   char col=cornerC[cub][(i-ori+3)%3];
   change(pos,cornerN[p][i],col);
  }
 }
 for(int p=0;p<12;p++){
  int cub=c.ep[p],ori=c.eo[p];
  if(cub>=12||ori>=2)throw runtime_error("invalid edge cubie");
  Vec pos=plusv(edgeN[p][0],edgeN[p][1]);
  for(int i=0;i<2;i++)change(pos,edgeN[p][i],edgeC[cub][i^ori]);
 }
 if(!equalCube(fromStickers(s),c))throw runtime_error("cubie-to-stickers inverse check failed");
 return s;
}
Cube transformCube(Cube c,Rot3 r){return fromStickers(frameTransform(cubieToStickers(c),r));}
int remapAction(int a,Rot3 r){
 auto old=names[a];
 const char nextFace=faceOfNormal(apply(r,norm(old[0])));
 string renamed=string(1,nextFace)+old.substr(1);
 return fromName(renamed);
}
uint64_t packCorner(Cube const &c){
 uint64_t v=0;
 for(int i=0;i<8;i++){v|=uint64_t(c.cp[i])<<(3*i);v|=uint64_t(c.co[i])<<(24+2*i);}
 return v;
}
uint64_t packEdge(Cube const &c){
 uint64_t v=0;
 for(int i=0;i<12;i++){v|=uint64_t(c.ep[i])<<(4*i);v|=uint64_t(c.eo[i])<<(48+i);}
 return v;
}
Cube unpack(uint64_t ck,uint64_t ek){
 Cube c;
 for(int i=0;i<8;i++){c.cp[i]=(ck>>(3*i))&7;c.co[i]=(ck>>(24+2*i))&3;}
 for(int i=0;i<12;i++){c.ep[i]=(ek>>(4*i))&15;c.eo[i]=(ek>>(48+i))&1;}
 return c;
}
uint64_t le64(const unsigned char* p){
 uint64_t v=0;for(int i=0;i<8;i++)v|=uint64_t(p[i])<<(8*i);return v;
}
struct PairC {uint64_t a,b;int fiber;};
uint64_t pairHash(uint64_t a,uint64_t b){ // only for lookup? NEVER used for equality
 return a^(b*0x9e3779b97f4a7c15ULL);
}
using PKey=pair<uint64_t,uint64_t>;
vector<PairC> readTwinPairs(const string& path){
 ifstream f(path);if(!f)throw runtime_error("twin pair file inaccessible");
 string line;getline(f,line);
 if(line!="corner1_u64\tcorner2_u64\tfiber_size\tcp_cycle\trelative_cp_perm\tcp_mask_hex\tco_mask_hex\tco_overlap_hex\tplus\tminus")
  throw runtime_error("wrong exact twin ledger format");
 vector<PairC> v;
 while(getline(f,line)){
  if(line.empty())throw runtime_error("blank twin row");
  istringstream in(line);string a,b,k;
  getline(in,a,'\t');getline(in,b,'\t');getline(in,k,'\t');
  if(a.empty()||b.empty()||k.empty())throw runtime_error("bad twin row");
  uint64_t c1=stoull(a),c2=stoull(b);
  int fs=stoi(k);
  if(c1>=c2||!(fs==1||fs==4))throw runtime_error("twin pair orientation not sorted or bad fiber size");
  v.push_back({c1,c2,fs});
 }
 if(v.size()!=576)throw runtime_error("original exact 576 pair ledger changed");
 return v;
}
int main(int argc,char**argv){
 try{
  if(argc!=4)throw runtime_error("usage: P9-original-turns.bin P9-original-B6.bin P12P3-original-576.tsv");
  initTurns();
  auto rots=properRotations();
  ifstream turnsFile(argv[1],ios::binary);vector<unsigned char> table((istreambuf_iterator<char>(turnsFile)),{});
  if(table.size()!=288)throw runtime_error("original generator 288 byte file missing");
  for(int a=0;a<18;a++){
   for(int i=0;i<8;i++)if(table[a*16+i]!=turn[a].cp[i]||table[a*16+8+i]!=turn[a].co[i])
    throw runtime_error("P9 source 18 corner moves disagree with actual original CPP");
  }
  auto z=solved();auto pairs=readTwinPairs(argv[3]);
  uint64_t generatorCases=0,middleCases=0;
  for(auto r:rots){
   if(!equalCube(transformCube(z,r),z))throw runtime_error("proper full cubie rotation fails to fix solved");
   for(int a=0;a<18;a++){
    int next=remapAction(a,r);
    Cube hturn=transformCube(turn[a],r);
    if(!equalCube(hturn,turn[next]))throw runtime_error("18HTM generator conjugacy failure");
    generatorCases++;
   }
   uint32_t rng=0xc0be0265;
   Cube cur=z;
   for(int it=0;it<48;it++){
    rng^=rng<<13;rng^=rng>>17;rng^=rng<<5;
    cur=composeCube(cur,turn[rng%18]);
    if(!equalCube(fromStickers(cubieToStickers(cur)),cur))
     throw runtime_error("full cubie sticker roundtrip mismatch");
    auto hs=transformCube(cur,r);
    for(int a=0;a<18;a++){
      Cube lhs=transformCube(composeCube(cur,turn[a]),r);
      Cube rhs=composeCube(hs,turn[remapAction(a,r)]);
      if(!equalCube(lhs,rhs))throw runtime_error("full CP CO EP EO intermediate equivariance failure");
      middleCases++;
    }
   }
  }
  // Pair receipt uses the original edge fibers, not a derived E class hash.
  set<PKey> twinSet;
  unordered_map<uint64_t,vector<uint64_t>> edgeSupport;
  for(auto p:pairs){
   twinSet.insert({p.a,p.b});
   edgeSupport[p.a];edgeSupport[p.b];
  }
  if(twinSet.size()!=576||edgeSupport.size()!=1152)throw runtime_error("duplicate corner pairs/vertices");
  ifstream f(argv[2],ios::binary);if(!f)throw runtime_error("original whole B6 missing");
  unsigned char buf[16];uint64_t rows=0;
  while(f.read((char*)buf,16)){
   uint64_t c=le64(buf),e=le64(buf+8);
   auto it=edgeSupport.find(c);if(it!=edgeSupport.end())it->second.push_back(e);
   rows++;
  }
  if(!f.eof()||f.gcount()!=0||rows!=8240087ULL)throw runtime_error("original B6 row count or trailing length mismatch");
  for(auto p:pairs){
   auto &a=edgeSupport[p.a],&b=edgeSupport[p.b];
   if(a!=b||int(a.size())!=p.fiber)throw runtime_error("actual full edge fiber equality mismatch");
  }
  set<PKey> mappedPairs;uint64_t pairTransport=0,edgeTransport=0;
  map<PKey,set<PKey>> orbitImages;
  for(auto r:rots){
   for(auto p:pairs){
    auto &support=edgeSupport.at(p.a);
    vector<uint64_t> imageE;
    uint64_t ca=0,cb=0;bool first=true;
    for(auto edge:support){
      Cube A=transformCube(unpack(p.a,edge),r);
      Cube B=transformCube(unpack(p.b,edge),r);
      if(first){ca=packCorner(A);cb=packCorner(B);first=false;}
      if(packCorner(A)!=ca||packCorner(B)!=cb||packEdge(A)!=packEdge(B))
       throw runtime_error("corner/edge transformed fibers do not factor");
      imageE.push_back(packEdge(A));
      edgeTransport++;
    }
    if(ca==cb)throw runtime_error("rotation merged distinct corners");
    if(ca>cb)swap(ca,cb);
    if(!twinSet.count({ca,cb}))throw runtime_error("true physical 24-rotation fails twin-pair closure");
    auto target=edgeSupport.at(ca);
    sort(imageE.begin(),imageE.end());
    if(imageE!=target)throw runtime_error("physical rotation did not transport WHOLE literal edge support");
    mappedPairs.insert({ca,cb});
    orbitImages[{p.a,p.b}].insert({ca,cb});
    pairTransport++;
   }
  }
  if(mappedPairs.size()!=576||pairTransport!=24ULL*576||edgeTransport!=24ULL*1728)
    throw runtime_error("whole original fiber orbit cover not complete");

  // Refine the physical group lift into action orbits on the 576
  // actual unordered equal-edge-fiber PAIR OBJECTS (not just CP labels).
  // A stabilizer calculation uses all 24 maps for every pair, not
  // the observed 48-element graph isometry label conjugacy alone.
  map<PKey,PairC> pairByKey;
  for(auto p:pairs)pairByKey[{p.a,p.b}]=p;
  set<PKey> unused;
  for(auto p:pairs)unused.insert({p.a,p.b});
  map<int,int> actualOrbitHistogram;
  map<string,int> typedOrbitHistogram;
  auto profileOf=[&](PairC p)->string{
   int inv[8];for(int i=0;i<8;i++)inv[(p.a>>(3*i))&7]=i;
   int D[4]={0,0,0,0};
   for(int i=0;i<8;i++){
    int pi=inv[(p.b>>(3*i))&7];
    auto cornerPoint=[](int id){Vec v={0,0,0};for(Vec n:cornerN[id])v=plusv(v,n);return v;};
    Vec v=cornerPoint(i),w=cornerPoint(pi);
    int dist=(v.x!=w.x)+(v.y!=w.y)+(v.z!=w.z);
    if(dist<0||dist>3)throw runtime_error("invalid Q3 graph metric distance");
    D[dist]++;
   }
   ostringstream out;for(int k=0;k<4;k++)out<<(k?",":"")<<D[k];
   return out.str();
  };
  while(!unused.empty()){
   PKey representative=*unused.begin();
   const auto &orb=orbitImages.at(representative);
   if(orb.empty()||24%orb.size()!=0)
    throw runtime_error("proper rotation action orbit size not divisor24");
   const string profile=profileOf(pairByKey.at(representative));
   for(auto other:orb){
    if(!unused.count(other)||profileOf(pairByKey.at(other))!=profile)
     throw runtime_error("physical pair orbit overlap or metric non-covariance");
    if(orbitImages.at(other)!=orb)
     throw runtime_error("24 actual physical rotation maps fail group orbit closure");
   }
   for(auto other:orb)unused.erase(other);
   actualOrbitHistogram[(int)orb.size()]++;
   typedOrbitHistogram[profile+"/"+to_string(orb.size())]++;
  }
  int nPhysicalOrbits=0;
  for(auto [size,count]:actualOrbitHistogram){
   nPhysicalOrbits+=count;
   cout<<"P12_P5_TRUE_PAIR_ORBIT ORBIT_SIZE "<<size
       <<" ORBIT_COUNT "<<count
       <<" ORIGINAL_PAIR_COUNT "<<size*count<<"\n";
  }
  for(auto [signature,count]:typedOrbitHistogram)
   cout<<"P12_P5_Q3_METRIC_PAIR_ORBIT PROFILE_AND_SIZE "<<signature
       <<" ORBIT_COUNT "<<count<<"\n";
  cout<<"P12_P5_TRUE_54_FACELET_24_ROTATION_CUBIE_LIFT_PASS"
      <<" PROPER_ROTATIONS 24 REFLECTIONS_CLAIMED 0"
      <<" GENERATOR_EQUIVARIANCE_CASES "<<generatorCases
      <<" WHOLE_CUBIE_EO_CO_TEST_CASES "<<middleCases
      <<" FULL_B6_STATE_ROWS "<<rows
      <<" SOURCE_576_FIBER_PAIRS "<<pairs.size()
      <<" FULL_PAIR_TRANSPORT_CHECKS "<<pairTransport
      <<" EDGE_SUPPORT_TRANSPORT_CHECKS "<<edgeTransport
      <<" MAPPED_PAIR_COVER "<<mappedPairs.size()
      <<" TRUE_PHYSICAL_PAIR_ORBITS "<<nPhysicalOrbits
      <<" FULL_48_AUTOMORPHISM_PROVEN 0"
      <<" NUMERICAL_MULTIPLICITY_LAW_EXPLAINED 0"
      <<" ORIGINAL_SCRAMBLE_SOURCE_FIXED_PROVEN 0"
      <<" GLOBAL_LOWER17_CLAIMED 0\n";
  return 0;
 }catch(exception const&e){cerr<<"P12_P5_FAIL "<<e.what()<<"\n";return 3;}
}
