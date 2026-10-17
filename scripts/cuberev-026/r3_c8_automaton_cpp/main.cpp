// CUBE-REV 0.26 R3: source-preserving projected C8 DFA vs original P9 baseline.
// Exact identical admissible bound: C6 AND E6 after each canonical second turn.
// Baseline is inherited CORNER-first P9, candidate EDGE-first reorders the same
// two mathematically necessary predicates. No stronger novel heuristic presumed.
#define CUBEREV_P9_AS_LIBRARY
#include "../../cuberev-025/p0_r6i_p9_projection_cpp/main.cpp"
#undef CUBEREV_P9_AS_LIBRARY
#include <array>
#include <vector>
#include <algorithm>
#include <numeric>
#include <limits>
#include <cmath>
#include <cstring>
// CUBE-REV 0.26 R3: bounded projected-C8 DFA source B10 verifier.
// C8 corner projection computed from immutable original C7 with all 18
// actual physical CP/CO transitions; dense 8!*3^7 bitset.
static constexpr uint32_t C8_DOMAIN=40320u*2187u;
static constexpr char C8_HEADER[]="CUBE-REV-026-R3:C8-DENSE-BITSET:v1;domain=88179840;source=ORIGINAL-P9-C7\n";
static uint32_t c8Rank(Key64 c){
 uint32_t avail=255,perm=0,ori=0,mul=1,charge=0;
 for(int i=0;i<8;i++){
  uint32_t v=(c>>(3*i))&7u,o=(c>>(24+2*i))&3u;
  if(o>=3||!(avail&(1u<<v)))throw std::runtime_error("invalid packed corner");
  perm=perm*(8-i)+__builtin_popcount(avail&((1u<<v)-1u));
  avail^=1u<<v;charge+=o;
  if(i<7){ori+=o*mul;mul*=3;}
 }
 if(avail||charge%3||perm>=40320||ori>=2187)throw std::runtime_error("illegal corner group");
 return perm*2187+ori;
}
struct DenseC8{
 std::vector<uint64_t> bits=std::vector<uint64_t>((C8_DOMAIN+63)/64,0);
 uint64_t queries=0;
 void put(Key64 c){auto i=c8Rank(c);bits[i/64]|=1ull<<(i%64);}
 bool has(Key64 c){queries++;auto i=c8Rank(c);return (bits[i/64]>>(i%64))&1ull;}
 uint64_t count()const{uint64_t n=0;for(auto x:bits)n+=__builtin_popcountll(x);return n;}
 std::string sha()const{
  SHA256_CTX h;SHA256_Init(&h);SHA256_Update(&h,C8_HEADER,strlen(C8_HEADER));
  unsigned char b[8];for(auto v:bits){putLE64(b,v);SHA256_Update(&h,b,8);}
  unsigned char d[32];SHA256_Final(d,&h);
  std::ostringstream ss;ss<<std::hex<<std::setfill('0');
  for(auto v:d)ss<<std::setw(2)<<unsigned(v);
  return ss.str();
 }
};


struct EdgeFirstCourt:PackedOrderedCourt{
 DenseC8 c8;
 uint64_t c8Reject=0,c8Descendants=0;
 bool guardedVisit(Cube const&s,int depth,int limit,int last){
  if(limit-depth==1)return jointVisit(s,depth,limit,last);
  ++visits;if((visits&0xffff)==0&&court.expired()){cut=true;return false;}
  FullKey key=exactKey(s);
  if(c6.find(key.c)!=c6.end()){
   ++fullQueries;if(court.goal.find(key)!=court.goal.end()){
    ++fullHits;meet=true;foundPrefix=path;foundKey=key;return true;
   }
  }
  if(depth==limit)return false;
  if(limit-depth==2){
   if(!c8.has(key.c)){
    ++c8Reject;
    for(int a=0;a<18;a++)if(canonical(last,a)){
     uint64_t n=canonicalSubtreeOne(a);skippedChildren+=n;c8Descendants+=n;
    }
    return false;
   }
   ++orderedPairParents;
   for(int a=0;a<18;a++)if(canonical(last,a)){
    const Cube next=composeCube(s,turn[a]);FullKey n=exactKey(next);
    bool one=c6.find(n.c)!=c6.end()&&edge6.find(n.e)!=edge6.end(),two=false;
    if(c7.find(n.c)==c7.end())++earlyCorner7Rejections;
    else if(!one){
     for(int b=0;b<18;b++)if(canonical(a,b)){
      ++orderedPairChecks;++cornerPackedChecks;++secondFullCubeMovesAvoided;
      auto c=cornerTurnPacked(n.c,b);
      if(c6.find(c)==c6.end())continue;
      ++edgePackedChecks;
      if(edge6.find(edgeTurnPacked(n.e,b))==edge6.end())continue;
      ++orderedPairPasses;two=true;break;
     }
    }
    if(!one&&!two){++twoStepRejectedBranches;
     uint64_t nskip=canonicalSubtreeOne(a);
     skippedChildren+=nskip;twoStepRejectedCalls+=nskip;continue;
    }
    ++twoStepCandidateParents;
    path.push_back(a);if(jointVisit(next,depth+1,limit,a))return true;
    path.pop_back();if(cut)return false;
   }
   return false;
  }
  for(int a=0;a<18;a++)if(canonical(last,a)){
   path.push_back(a);
   if(guardedVisit(composeCube(s,turn[a]),depth+1,limit,a))return true;
   path.pop_back();if(cut)return false;
  }
  return false;
 }
 void clear(){
  visits=0;skippedChildren=0;fullHits=0;fullQueries=0;
  orderedPairChecks=0;edgePackedChecks=0;cornerPackedChecks=0;
  secondFullCubeMovesAvoided=0;earlyCorner7Rejections=0;
  twoStepRejectedBranches=0;twoStepRejectedCalls=0;
  twoStepCandidateParents=0;orderedPairParents=0;orderedPairPasses=0;
  c8Reject=0;c8Descendants=0;c8.queries=0;
  cut=false;meet=false;foundPrefix.clear();path.clear();
 }
};

struct Snapshot{
 uint64_t visited=0,omitted=0,pairs=0,passes=0,full=0,early=0,candidates=0,pruned=0,corner=0,edge=0;
 double durationMs=0;
};

#ifndef CUBEREV_R3_AS_LIBRARY
int main(int argc,char**argv){
 try{
  if(argc!=3)throw std::runtime_error("usage: output-prefix time-budget-seconds");
  std::string prefix=argv[1];int budget=std::stoi(argv[2]);
  if(prefix.empty()||budget<180||budget>950)throw std::runtime_error("invalid output prefix/budget");
  auto beginning=Clock::now();
  initTurns();
  auto scr=parse("R' B' F2 D2 F2 L2 R2 U' F2 L2 D2 B2 D F L' R2 B U2 F2 R2");
  auto sol=parse("F U F D' R' F' L' F' D' L B L2 F2 U2 L2 U F' R2");
  Cube src=cubeAfter(scr);Stickers st=solvedStickers();
  for(int a:scr)physicalTurn(st,names[a]);
  if(!(exactKey(fromStickers(st))==exactKey(src))||sol.size()!=18||
     !physicalSolves(scr,sol)||physicallyAuditFastProjection()!=4608)
   throw std::runtime_error("original physical whole source mismatch");
  EdgeFirstCourt r;r.court.started=Clock::now();r.court.secondsBudget=budget;
  if(!r.court.build(6)){std::cout<<"R3_BUILD_HOLD\n";return 2;}
  r.project();r.prepareEdges();
  if(r.court.goal.size()!=8240087||r.c6.size()!=1405068||
    r.c7.size()!=6807696||r.edge6.size()!=7672278)
    throw std::runtime_error("original whole B6 projected size mismatch");
  auto goal=goalDigest(r.court,6,"");
  if(goal!="82fe545bcad3537c989ec22afce9d286926ddce5f4ef9428c0307951ec2d0979")
   throw std::runtime_error("original whole B6 SHA changed");
  auto c7sha=projectionDigest(r.c7,"C7",prefix+"-C7.bin");
  if(c7sha!="2fd2a3692147e81cc8bf970bcbbbdde061551065268e207d60aec4354ccd67e6")
   throw std::runtime_error("original C7 projected SHA changed");
  writeTurns(prefix+"-turns.bin");
  std::cout<<"R3_C8_BUILD_START SOURCE_C7 "<<r.c7.size()<<" GENERATORS 18\n"<<std::flush;
  auto bt=Clock::now();
  for(const auto c:r.c7){
   r.c8.put(c);
   for(int a=0;a<18;a++)r.c8.put(cornerTurnPacked(c,a));
  }
  double buildMs=std::chrono::duration<double,std::milli>(Clock::now()-bt).count();
  uint64_t c8count=r.c8.count(),inside=0;
  for(const auto c:r.c7)if(r.c8.has(c))inside++;
  if(c8count<r.c7.size()||c8count>C8_DOMAIN||inside!=r.c7.size())
   throw std::runtime_error("C8 original membership/count unsound");
  auto c8sha=r.c8.sha();
  std::cout<<"R3_C8_BUILD_PASS C7_COUNT "<<r.c7.size()
   <<" C8_COUNT "<<c8count<<" DOMAIN "<<C8_DOMAIN
   <<" BITSET_BYTES "<<r.c8.bits.size()*8<<" C7_ALL_CONTAINED "<<inside
   <<" C8_SHA "<<c8sha<<" C7_SHA "<<c7sha<<" GOAL_SHA "<<goal
   <<" BUILD_MS "<<std::fixed<<std::setprecision(3)<<buildMs
   <<" PEAK_RSS_KIB "<<rssKiB()<<"\n"<<std::flush;
  const std::array<std::array<int,2>,2> fixtures={{{15,1},{16,1}}};
  for(int i=0;i<2;i++){
   const int first=fixtures[i][0],second=fixtures[i][1];
   if(!canonical(first,second))throw std::runtime_error("bad source grammar");
   Cube node=composeCube(composeCube(src,turn[first]),turn[second]);
   uint64_t mass=p8Weight(second,8);
   struct Record{uint64_t visit=0,omit=0,pairs=0,full=0,guard=0,extra=0;double ms=0;};
   Record results[2];
   for(int mode=0;mode<2;mode++){
    r.clear();auto t=Clock::now();
    for(int limit=2;limit<=10;limit++){
     r.path={first,second};
     const bool meet=mode==0?r.fastVisit(node,2,limit,second):r.guardedVisit(node,2,limit,second);
     if(meet){std::cout<<"R3_ACTUAL_FULL_MEET_HOLD FIRST "<<first<<" SECOND "<<second
       <<" MODE "<<mode<<" PATH "<<join(r.foundPrefix)<<"\n";return 3;}
     if(r.cut||r.court.expired()){std::cout<<"R3_RESOURCE_HOLD FIRST "<<first
       <<" SECOND "<<second<<" MODE "<<mode<<" LIMIT "<<limit<<"\n";return 2;}
    }
    if(r.visits+r.skippedChildren!=mass||r.fullHits)
     throw std::runtime_error("source canonical weighted calls incomplete or false goal");
    Record rec;rec.visit=r.visits;rec.omit=r.skippedChildren;rec.pairs=r.orderedPairChecks;
    rec.full=r.fullQueries;rec.guard=r.c8Reject;rec.extra=r.c8Descendants;
    rec.ms=std::chrono::duration<double,std::milli>(Clock::now()-t).count();
    results[mode]=rec;
    std::cout<<"R3_ACTUAL_MATCHED FIRST "<<first<<" SECOND "<<second
      <<" MODE "<<(mode==0?"BASELINE":"C8_GUARD")
      <<" WORD_CALLS "<<mass<<" VISITED "<<rec.visit<<" OMITTED "<<rec.omit
      <<" PAIRS "<<rec.pairs<<" FULL_QUERIES "<<rec.full
      <<" C8_REJECT "<<rec.guard<<" C8_EXTRA_OMITTED "<<rec.extra
      <<" SEARCH_MS "<<std::fixed<<std::setprecision(3)<<rec.ms
      <<" WHOLE_GOAL_HITS 0 COMPLETE_DEPTH2_SOURCE 1 NEW_FIRST_ROOT 0\n"<<std::flush;
   }
   const Record a=results[0],b=results[1];
   if(b.visit>a.visit||b.omit<a.omit||b.visit+b.omit!=a.visit+a.omit)
    throw std::runtime_error("C8 guard violated source-language accounting");
   std::cout<<"R3_PAIRED_ORIGINAL FIRST "<<first<<" SECOND "<<second
    <<" VISITS_SAVED "<<(a.visit-b.visit)
    <<" EXTRA_OMITTED "<<(b.omit-a.omit)
    <<" C8_OVER_BASE_RATIO "<<std::fixed<<std::setprecision(7)<<b.ms/a.ms
    <<" TRUE_GOAL_ABSENCE_BOTH 1 FIRST_ROOT_COMPLETE 0\n"<<std::flush;
  }
  if(goalDigest(r.court,6,"")!=goal)throw std::runtime_error("goal mutated");
  std::cout<<"R3_COMPLETE_ORIGINAL_C8_DFA_PILOT_PASS C8_COUNT "<<c8count
   <<" C8_SHA "<<c8sha<<" GOAL_SHA "<<goal<<" COMPLETE_DEPTH2_PREFIXES 2"
   <<" ORIGINAL_FIRST16_SECOND1_NEGATIVE 1 FIRST_ROOTS_CERTIFIED 5"
   <<" FIRST_ROOTS_OPEN 13 NEW_FIRST_ROOT 0 GLOBAL_LOWER17_CLAIMED 0"
   <<" PEAK_RSS_KIB "<<rssKiB()<<" TOTAL_MS "<<std::fixed<<std::setprecision(3)
   <<std::chrono::duration<double,std::milli>(Clock::now()-beginning).count()<<"\n";
  return 0;
 }catch(std::exception const& e){std::cerr<<"R3_PHYSICAL_ERROR "<<e.what()<<"\n";return 4;}
}
#endif // CUBEREV_R3_AS_LIBRARY
