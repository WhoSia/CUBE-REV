// CUBE-REV 0.25 P0-R6I-P8 proof-carrying IMMUTABLE goal batches.
// Real original WCA 54-sticker + 18 HTM physical geometry inherited.
// SHA-256 canonical sorted 128-bit whole CP/CO/EP/EO goal images.
// Hex digest is a computational COMMITMENT, not a Lean equality axiom.
// Physical proof certificates are checked separately in independent Go.
#define CUBEREV_P0R6E_AS_LIBRARY
#include "../p0_r6e_packed_projected_two_turn_cpp/main.cpp"
#undef CUBEREV_P0R6E_AS_LIBRARY
#include <openssl/sha.h>
#include <fstream>
#include <iomanip>
#include <algorithm>
#include <memory>
#include <chrono>
#include <sys/resource.h>

static uint64_t p8Weight(int last,int remaining){
 std::array<uint64_t,18> before{};
 uint64_t sum=uint64_t(remaining+1);
 for(int depth=1;depth<=remaining;depth++){
  std::array<uint64_t,18> now{};
  if(depth==1){
   for(int a=0;a<18;a++)if(canonical(last,a))now[a]=1;
  }else{
   for(int b=0;b<18;b++)for(int a=0;a<18;a++)
     if(canonical(b,a))now[a]+=before[b];
  }
  before=now;uint64_t layer=0;for(auto x:now)layer+=x;
  sum+=uint64_t(remaining-depth+1)*layer;
 }
 return sum;
}
static void putLE64(unsigned char* out,uint64_t n){
 for(int i=0;i<8;i++)out[i]=static_cast<unsigned char>(n>>(8*i));
}
static std::string goalHeader(int radius,size_t count){
 return "CUBE-REV-025-P8:FULL-CP-CO-EP-EO:LE64x2:v1;radius="+
   std::to_string(radius)+";count="+std::to_string(count)+"\n";
}
static std::string goalDigest(const GlobalCourt&court,int radius,
                              const std::string&binarySnapshot){
 std::vector<FullKey> sorted;
 sorted.reserve(court.goal.size());
 for(const auto &k:court.goal)sorted.push_back(k);
 std::sort(sorted.begin(),sorted.end(),[](const FullKey&a,const FullKey&b){
   return a.c<b.c||(a.c==b.c&&a.e<b.e);
 });
 for(size_t i=1;i<sorted.size();i++)
  if(sorted[i].c==sorted[i-1].c&&sorted[i].e==sorted[i-1].e)
   throw std::runtime_error("goal fingerprint serialization duplicate cubie");
 std::ofstream out;
 if(!binarySnapshot.empty()){
  out.open(binarySnapshot,std::ios::binary|std::ios::trunc);
  if(!out)throw std::runtime_error("cannot write canonical sorted goal snapshot");
 }
 SHA256_CTX hash;
 if(SHA256_Init(&hash)!=1)throw std::runtime_error("OpenSSL SHA256_Init fails");
 const auto header=goalHeader(radius,sorted.size());
 if(SHA256_Update(&hash,header.data(),header.size())!=1)
  throw std::runtime_error("SHA256 header");
 for(const auto&k:sorted){
  unsigned char b[16];
  putLE64(b,k.c);putLE64(b+8,k.e);
  if(SHA256_Update(&hash,b,sizeof b)!=1)throw std::runtime_error("SHA256 row");
  if(out)out.write(reinterpret_cast<const char*>(b),16);
 }
 if(out){out.close();if(!out)throw std::runtime_error("goal snapshot write truncated");}
 unsigned char digest[SHA256_DIGEST_LENGTH];
 if(SHA256_Final(digest,&hash)!=1)throw std::runtime_error("SHA256 final");
 std::ostringstream os;os<<std::hex<<std::setfill('0');
 for(unsigned char b:digest)os<<std::setw(2)<<unsigned(b);
 return os.str();
}
static long rssKiB(){
 struct rusage v{};if(getrusage(RUSAGE_SELF,&v))return -1;return v.ru_maxrss;
}
static std::vector<std::vector<int>> frontier43(){
 std::vector<std::vector<int>> all;
 for(int a=0;a<18;a++){
  if(a==0||a==9){for(int b=0;b<18;b++)if(canonical(a,b))all.push_back({a,b});}
  else all.push_back({a});
 }
 if(all.size()!=43)throw std::runtime_error("original source DFA not 43 leaf");
 return all;
}
#ifndef CUBEREV_P8_AS_LIBRARY
int main(int argc,char**argv){
 try{
  const std::string mode=argc>1?argv[1]:"smoke";
  const std::string snapshot=argc>2?argv[2]:"/tmp/p8-goal.bin";
  const int timeLimit=argc>3?std::stoi(argv[3]):200;
  const int rg=mode=="smoke"?3:6;
  const int rs=mode=="smoke"?3:mode=="b7"?7:10;
  if((mode!="smoke"&&mode!="b7"&&mode!="b10sample")||timeLimit<1||
     snapshot.empty())throw std::runtime_error("mode smoke/b7/b10sample snapshot seconds");
  const auto wall=std::chrono::steady_clock::now();
  initTurns();
  const auto scr=parse("R' B' F2 D2 F2 L2 R2 U' F2 L2 D2 B2 D F L' R2 B U2 F2 R2");
  const auto sol=parse("F U F D' R' F' L' F' D' L B L2 F2 U2 L2 U F' R2");
  const Cube source=cubeAfter(scr);
  Stickers orig=solvedStickers();
  for(int a:scr)physicalTurn(orig,names[a]);
  if(!(exactKey(source)==exactKey(fromStickers(orig)))||
    sol.size()!=18||!physicalSolves(scr,sol)||
    physicallyAuditFastProjection()!=4608)
    throw std::runtime_error("original 54-sticker / 18HTM whole cubie witness failure");
  PackedOrderedCourt court;
  court.court.started=Clock::now();court.court.secondsBudget=timeLimit;
  if(!court.court.build(rg)){std::cout<<"P8_HOLD_GOAL\n";return 2;}
  court.project();court.prepareEdges();
  if(court.court.goal.size()!=size_t(rg==6?8240087:3502)||
     (rg==6&&(court.c6.size()!=1405068||court.edge6.size()!=7672278)))
   throw std::runtime_error("actual complete goal B6/B3 cardinalities drift");
  auto setup=std::chrono::steady_clock::now();
  const auto target=goalDigest(court.court,rg,snapshot);
  std::cout<<"P8_GOAL_COMMIT MODE "<<mode<<" SHA256 "<<target
    <<" RADIUS "<<rg<<" STATES "<<court.court.goal.size()
    <<" C "<<court.c6.size()<<" E "<<court.edge6.size()
    <<" SNAPSHOT_BYTES "<<court.court.goal.size()*16ULL
    <<" PHYSICAL_TURNS_CHECKED 4608 PEAK_RSS_KIB "<<rssKiB()<<"\n"<<std::flush;
  const bool full=mode!="b10sample";
  const auto prefixes=full?frontier43():
    std::vector<std::vector<int>>{{0,3},{9,3}};
  uint64_t internal=0,visited=0,skipped=0,total=0;
  // Real full-cubie membership for ALL three strict internal nodes.
  if(full){
   const std::vector<std::vector<int>> roots={{},{0},{9}};
   for(auto const&p:roots){
    Cube x=source;for(int a:p)x=composeCube(x,turn[a]);
    if(court.court.goal.count(exactKey(x))){
     std::cout<<"P8_TRUE_INTERNAL_CUBIE_MEET HOLD\n";return 3;
    }
    const uint64_t wt=uint64_t(rs-p.size()+1);
    internal+=wt;
    std::cout<<"P8_INTERNAL MODE "<<mode
      <<" FIRST "<<(p.empty()?-1:p[0])<<" DEPTH "<<p.size()
      <<" REPEATED_CALLS "<<wt<<" WHOLE_CUBIE_MEETS 0 GOAL_SHA256 "<<target
      <<"\n"<<std::flush;
   }
  }
  total=internal;visited=internal;
  int count=0;
  for(auto const&p:prefixes){
   Cube x=source;for(int a:p)x=composeCube(x,turn[a]);
   court.visits=0;court.skippedChildren=0;court.orderedPairChecks=0;
   court.edgePackedChecks=0;court.fullQueries=0;court.fullHits=0;
   court.cut=false;court.path=p;
   auto t=std::chrono::steady_clock::now();
   for(int depth=int(p.size());depth<=rs;depth++){
    court.path=p;
    if(court.fastVisit(x,int(p.size()),depth,p.back())){
     std::cout<<"P8_TRUE_LEAF_CUBIE_MEET NO_NEGATIVE_CERT\n";return 3;
    }
    if(court.cut||court.court.expired()){
     std::cout<<"P8_RESOURCE_HOLD_LEAF NO_NEGATIVE_CERT\n";return 2;
    }
   }
   const double duration=std::chrono::duration<double,std::milli>(
      std::chrono::steady_clock::now()-t).count();
   auto expected=p8Weight(p.back(),rs-int(p.size()));
   if(court.visits+court.skippedChildren!=expected||court.fullHits){
    std::cout<<"P8_LEAF_ACCOUNTING_HOLD FIRST "<<p[0]<<" SECOND "<<(p.size()==2?p[1]:-1)
      <<" DEPTH "<<p.size()<<" EXPECTED "<<expected<<" VISITED "<<court.visits
      <<" OMITTED "<<court.skippedChildren<<" FULL_HITS "<<court.fullHits
      <<" EXPIRED "<<court.court.expired()<<" CUT "<<court.cut<<"\n"<<std::flush;
    throw std::runtime_error("original canonical source leaf not entirely ruled out");
   }
   count++;total+=expected;visited+=court.visits;skipped+=court.skippedChildren;
   const FullKey key=exactKey(x);
   std::cout<<"P8_LEAF MODE "<<mode<<" INDEX "<<count
     <<" FIRST "<<p[0]<<" SECOND "<<(p.size()==2?p[1]:-1)
     <<" PREFIX_DEPTH "<<p.size()<<" SOURCE_KEY_C "<<key.c
     <<" SOURCE_KEY_E "<<key.e
     <<" WORD_CALLS "<<expected<<" VISITED "<<court.visits
     <<" OMITTED "<<court.skippedChildren
     <<" PAIRS "<<court.orderedPairChecks
     <<" EDGES "<<court.edgePackedChecks<<" FULL_QUERIES "<<court.fullQueries
     <<" WALL_MS "<<std::fixed<<std::setprecision(3)<<duration
     <<" FULL_CUBIE_MEETS 0 COMPLETE 1 GOAL_SHA256 "<<target<<"\n"<<std::flush;
  }
  const auto after=goalDigest(court.court,rg,"");
  if(after!=target)throw std::runtime_error("IMMUTABILITY_BROKEN_GOAL_SHA256_CHANGED");
  const uint64_t baseline=full?canonicalBaselineVisits(rs):0;
  if(full&&(total!=baseline||visited+skipped!=baseline||count!=43))
   throw std::runtime_error("43 actual original source physical cylinders not completely composed");
  const auto millis=std::chrono::duration<double,std::milli>(
    std::chrono::steady_clock::now()-wall).count();
  std::cout<<"P8_BATCH_CERT MODE "<<mode<<" GOAL_SHA256 "<<target
    <<" POST_SEARCH_SHA256 "<<after<<" IMMUTABLE 1"
    <<" ORIGINAL_PHYSICS_4608 1 SOURCE_RADIUS "<<rs
    <<" GOAL_RADIUS "<<rg<<" INTERNAL_CALLS "<<internal
    <<" LEAVES "<<count<<" BASELINE "<<baseline<<" WEIGHT_TOTAL "<<total
    <<" VISITED "<<visited<<" OMITTED "<<skipped
    <<" FULL_CUBIE_GOAL_MEETS 0"
    <<" SOURCE_GLOBAL_COMPLETE "<<(full?1:0)
    <<" LOWER17_CLAIMED 0"
    <<" ELAPSED_MS "<<std::fixed<<std::setprecision(3)<<millis
    <<" PEAK_RSS_KIB "<<rssKiB()<<"\n"<<std::flush;
  return 0;
 }catch(const std::exception&e){
  std::cerr<<"P8_ERROR "<<e.what()<<"\n";return 4;
 }
}
#endif // CUBEREV_P8_AS_LIBRARY
