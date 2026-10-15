// CUBE-REV P0-R6I-P7: original physical WCA shared-target experiment.
// Hold the exact 54-facelet-derived cubie/packed search logic fixed.
// Compare SIX prefix searches after one immutable B6 target court against
// SIX independent reconstructed courts. The B10 sibling source prefixes are a
// calibration sample, not a complete source B10 lower17 proof.
#define CUBEREV_P0R6E_AS_LIBRARY
#include "../p0_r6e_packed_projected_two_turn_cpp/main.cpp"
#undef CUBEREV_P0R6E_AS_LIBRARY
#include <memory>
#include <chrono>
#include <iomanip>
#include <sys/resource.h>
using WallClock=std::chrono::steady_clock;
static double ms(WallClock::time_point begin){return std::chrono::duration<double,std::milli>(WallClock::now()-begin).count();}
static uint64_t exactSuffixCalls(int last,int remaining){
 std::array<uint64_t,18> prev{};
 uint64_t ans=uint64_t(remaining+1);
 for(int depth=1;depth<=remaining;depth++){
  std::array<uint64_t,18> next{};
  if(depth==1){for(int a=0;a<18;a++)if(canonical(last,a))next[a]=1;}
  else for(int a=0;a<18;a++)for(int b=0;b<18;b++)if(canonical(b,a))next[a]+=prev[b];
  prev=next;
  uint64_t level=0;for(auto c:prev)level+=c;
  ans+=uint64_t(remaining-depth+1)*level;
 }
 return ans;
}
static long rssPeak(){
 rusage r{};if(getrusage(RUSAGE_SELF,&r))return -1;
 return r.ru_maxrss;
}
int main(int argc,char**argv){
 try{
  const std::string mode=argc>1?argv[1]:"shared";
  const int g=argc>2?std::stoi(argv[2]):6;
  const int r=argc>3?std::stoi(argv[3]):10;
  const int seconds=argc>4?std::stoi(argv[4]):300;
  if((mode!="shared"&&mode!="isolated")||
   !(g==6&&r==10)||seconds<1)
    throw std::runtime_error("mode shared/isolated; only original B6/B10 two-prefix physically complete pilot");
  auto processStarted=WallClock::now();
  initTurns();
  auto scramble=parse("R' B' F2 D2 F2 L2 R2 U' F2 L2 D2 B2 D F L' R2 B U2 F2 R2");
  auto known=parse("F U F D' R' F' L' F' D' L B L2 F2 U2 L2 U F' R2");
  Cube source=cubeAfter(scramble);
  Stickers physical=solvedStickers();
  for(int a:scramble)physicalTurn(physical,names[a]);
  if(!(exactKey(source)==exactKey(fromStickers(physical)))||
    known.size()!=18||!physicalSolves(scramble,known)||
    physicallyAuditFastProjection()!=4608)
   throw std::runtime_error("original 54-sticker source and physical packed projection regression failed");
  const std::vector<std::vector<int>> prefixes={{0,3},{9,3}};
  std::unique_ptr<PackedOrderedCourt> sharedCourt;
  int builds=0;
  double totalSetup=0,totalSearch=0;
  for(size_t i=0;i<prefixes.size();i++){
   std::unique_ptr<PackedOrderedCourt> isolatedCourt;
   if(mode=="shared"&&!sharedCourt)sharedCourt=std::make_unique<PackedOrderedCourt>();
   if(mode=="isolated")isolatedCourt=std::make_unique<PackedOrderedCourt>();
   PackedOrderedCourt& court=mode=="shared"?*sharedCourt:*isolatedCourt;
   if(mode=="isolated"||i==0){
    court.court.started=Clock::now();
    court.court.secondsBudget=seconds;
    const auto start=WallClock::now();
    if(!court.court.build(g)){std::cout<<"P0R6I_P7_B10_B10_TARGET_HOLD\n";return 2;}
    court.project();
    court.prepareEdges();
    double delta=ms(start);
    totalSetup+=delta;builds++;
    const uint64_t expected=g==6?8240087ULL:3502ULL;
    if(court.court.goal.size()!=expected||
       (g==6&&(court.c6.size()!=1405068||court.edge6.size()!=7672278)))
     throw std::runtime_error("physically wrong original whole-cubie target/projected sets");
    std::cout<<std::fixed<<std::setprecision(3)
      <<"P0R6I_P7_B10_GOAL_BUILD MODE "<<mode
      <<" BUILD "<<builds<<" FULL_GOAL "<<court.court.goal.size()
      <<" CORNER "<<court.c6.size()<<" EDGE "<<court.edge6.size()
      <<" TARGET_SETUP_MS "<<delta<<" RSS_PEAK_KIB "<<rssPeak()
      <<" ORIGINAL_REAL_54_FACELET_CHECKS 4608\n"<<std::flush;
   }
   const auto &p=prefixes[i];
   for(size_t j=1;j<p.size();j++)if(!canonical(p[j-1],p[j]))
    throw std::runtime_error("profiled physical prefix illegally normalized");
   Cube x=source;for(int a:p)x=composeCube(x,turn[a]);
   court.visits=0;court.skippedChildren=0;
   court.orderedPairChecks=0;court.edgePackedChecks=0;court.fullQueries=0;
   court.fullHits=0;court.cut=false;
   auto start=WallClock::now();
   for(int lim=int(p.size());lim<=r;lim++){
    court.path=p;
    if(court.fastVisit(x,int(p.size()),lim,p.back())){
      std::cout<<"P0R6I_P7_B10_TRUE_PHYSICAL_INTERSECTION NO_NEGATIVE_CERT\n";return 3;
    }
    if(court.cut||court.court.expired()){
      std::cout<<"P0R6I_P7_B10_RESOURCE_HOLD NO_NEGATIVE_CERT\n";return 2;
    }
   }
   const double duration=ms(start);
   const uint64_t expected=exactSuffixCalls(p.back(),r-int(p.size()));
   if(court.visits+court.skippedChildren!=expected||court.fullHits)
    throw std::runtime_error("source prefix not fully covered by physical true cube");
   totalSearch+=duration;
   std::cout<<std::fixed<<std::setprecision(3)
    <<"P0R6I_P7_B10_PREFIX MODE "<<mode
    <<" CASE "<<(i+1)<<" FIRST "<<p.front()
    <<" SECOND "<<(p.size()==2?p[1]:-1)
    <<" WORD_CALLS "<<expected
    <<" VISITED "<<court.visits<<" SAFELY_SKIPPED "<<court.skippedChildren
    <<" ORDERED_PAIR_CHECKS "<<court.orderedPairChecks
    <<" PACKED_EDGE_CHECKS "<<court.edgePackedChecks
    <<" FULL_QUERIES "<<court.fullQueries
    <<" SOURCE_MS "<<duration
    <<" FULL_CUBIE_GOAL_MEETS 0\n"<<std::flush;
   // In isolated mode, the court is destroyed after this iteration,
   // so its original CP/CO/EP/EO and projection sets cannot be reused.
  }
  if(builds!=(mode=="shared"?1:2))
   throw std::runtime_error("incorrect number of independent target builds");
  std::cout<<std::fixed<<std::setprecision(3)
   <<"P0R6I_P7_B10_MODE_COMPLETE MODE "<<mode
   <<" GOAL_RADIUS "<<g<<" SOURCE_RADIUS "<<r
   <<" TARGET_BUILDS "<<builds<<" PREFIXES 2"
   <<" TOTAL_GOAL_SETUP_MS "<<totalSetup
   <<" TOTAL_PHYSICAL_SEARCH_MS "<<totalSearch
   <<" FULL_PROCESS_MS "<<ms(processStarted)
   <<" PEAK_RSS_KIB "<<rssPeak()
   <<" ORIGINAL_54_STICKER_PHYSICS_PASS 1"
   <<" ALL_SAMPLED_FULL_CUBIE_MEETS 0"
   <<" NOT_GLOBAL_B10 1\n"<<std::flush;
  return 0;
 }catch(std::exception const&e){
  std::cerr<<"P0R6I_P7_B10_ERROR "<<e.what()<<"\n";return 4;
 }
}
