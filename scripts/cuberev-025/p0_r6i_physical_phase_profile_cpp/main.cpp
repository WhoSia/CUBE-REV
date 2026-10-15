// CUBE-REV 0.25 P0-R6I-P6: original WCA source physical
// stage-separated runtime + per-prefix pruning measurements.
// Output is profiling, NOT a standalone global source B10 proof.
#define CUBEREV_P0R6E_AS_LIBRARY
#include "../p0_r6e_packed_projected_two_turn_cpp/main.cpp"
#undef CUBEREV_P0R6E_AS_LIBRARY
#include <sys/resource.h>
#include <fstream>
#include <iomanip>

using ProfileClock=std::chrono::steady_clock;
static double ms(ProfileClock::time_point a,ProfileClock::time_point b){
 return std::chrono::duration<double,std::milli>(b-a).count();
}
static long long rssNowKiB(){
 std::ifstream f("/proc/self/status");
 std::string key;long long value=0;std::string unit;
 while(f>>key){if(key=="VmRSS:"){f>>value>>unit;return value;}
                   std::string remainder;std::getline(f,remainder);}
 return -1;
}
static long long rssPeakKiB(){
 struct rusage r{};
 if(getrusage(RUSAGE_SELF,&r)!=0)return -1;
 return (long long)r.ru_maxrss;
}
static uint64_t suffixWordBudget(int last,int remaining){
 std::array<uint64_t,18> old{};
 uint64_t total=uint64_t(remaining+1);
 for(int d=1;d<=remaining;d++){
  std::array<uint64_t,18> next{};
  if(d==1){for(int a=0;a<18;a++)if(canonical(last,a))next[a]=1;}
  else for(int b=0;b<18;b++)for(int a=0;a<18;a++)
    if(canonical(b,a))next[a]+=old[b];
  old=next;
  uint64_t layer=0;for(auto n:old)layer+=n;
  total+=uint64_t(remaining-d+1)*layer;
 }
 return total;
}
static void stage(const std::string& name,double duration){
 std::cout<<std::fixed<<std::setprecision(3)
  <<"R6I_PROFILE_STAGE NAME "<<name<<" WALL_MS "<<duration
  <<" CURRENT_RSS_KIB "<<rssNowKiB()
  <<" PROCESS_PEAK_RSS_KIB "<<rssPeakKiB()<<"\n"<<std::flush;
}
int main(int argc,char**argv){
 try{
  const int g=argc>1?std::stoi(argv[1]):3;
  const int sourceR=argc>2?std::stoi(argv[2]):3;
  const int budget=argc>3?std::stoi(argv[3]):500;
  if(!((g==3&&sourceR==3)||(g==6&&sourceR==7))||budget<1)
   throw std::runtime_error("only original B3/B3 or B6/B7 profiling");
  const auto begin=ProfileClock::now();
  initTurns();
  const auto scr=parse("R' B' F2 D2 F2 L2 R2 U' F2 L2 D2 B2 D F L' R2 B U2 F2 R2");
  const auto known=parse("F U F D' R' F' L' F' D' L B L2 F2 U2 L2 U F' R2");
  const Cube source=cubeAfter(scr);
  Stickers original=solvedStickers();
  for(int a:scr)physicalTurn(original,names[a]);
  if(!(exactKey(source)==exactKey(fromStickers(original)))||
   known.size()!=18||!physicalSolves(scr,known))
   throw std::runtime_error("source full original stickers or known solution invalid");
  if(physicallyAuditFastProjection()!=4608)
   throw std::runtime_error("packed-vs-full original move regression invalid");
  stage("ORIGINAL_PHYSICAL_PREFLIGHT",ms(begin,ProfileClock::now()));
  PackedOrderedCourt court;
  court.court.started=Clock::now();court.court.secondsBudget=budget;
  auto start=ProfileClock::now();
  if(!court.court.build(g)){std::cout<<"R6I_PROFILE_HOLD_GOAL\n";return 2;}
  stage("FULL_GOAL_BALL_BUILD",ms(start,ProfileClock::now()));
  start=ProfileClock::now();
  court.project();
  stage("CORNER_PROJECTION",ms(start,ProfileClock::now()));
  start=ProfileClock::now();
  court.prepareEdges();
  stage("EDGE_PROJECTION",ms(start,ProfileClock::now()));
  const std::vector<std::vector<int>> paths={{0},{9},{0,3},{0,9},{9,3},{9,12}};
  std::cout<<"R6I_PROFILE_GOAL_FULL "<<court.court.goal.size()
   <<" CORNER "<<court.c6.size()
   <<" EDGE "<<court.edge6.size()
   <<" PHYSICAL_CHECKS 4608 PREFIX_TRIALS "<<paths.size()
   <<"\n"<<std::flush;
  int trial=0;
  for(const auto&p:paths){
   ++trial;
   for(size_t i=1;i<p.size();i++)if(!canonical(p[i-1],p[i]))
    throw std::runtime_error("selected profile prefix is not canonical");
   Cube x=source;for(int a:p)x=composeCube(x,turn[a]);
   court.visits=0;court.skippedChildren=0;
   court.orderedPairChecks=0;court.cornerPackedChecks=0;
   court.edgePackedChecks=0;court.fullQueries=0;court.fullHits=0;
   court.cut=false;
   const auto t=ProfileClock::now();
   for(int lim=int(p.size());lim<=sourceR;lim++){
    court.path=p;
    if(court.fastVisit(x,int(p.size()),lim,p.back())){
     std::cout<<"R6I_PROFILE_TRUE_FULL_CUBIE_INTERSECTION PREFIX "<<join(p)<<"\n";return 3;
    }
    if(court.cut||court.court.expired()){
     std::cout<<"R6I_PROFILE_HOLD_PREFIX "<<join(p)<<"\n";return 2;
    }
   }
   const auto dt=ms(t,ProfileClock::now());
   const uint64_t expected=suffixWordBudget(p.back(),sourceR-int(p.size()));
   if(court.visits+court.skippedChildren!=expected||court.fullHits!=0||
      court.cornerPackedChecks!=court.orderedPairChecks)
    throw std::runtime_error("sample original source exact word-accounting / no-full-meet fails");
   std::cout<<std::fixed<<std::setprecision(3)
    <<"R6I_PROFILE_PHYSICAL_PREFIX CASE "<<trial
    <<" FIRST "<<p.front()<<" SECOND "<<(p.size()==2?p[1]:-1)
    <<" PREFIX_DEPTH "<<p.size()
    <<" WORD_CALLS "<<expected
    <<" VISITED "<<court.visits
    <<" SAFELY_SKIPPED "<<court.skippedChildren
    <<" ORDERED_PAIR_CHECKS "<<court.orderedPairChecks
    <<" PACKED_EDGE_CHECKS "<<court.edgePackedChecks
    <<" FULL_QUERIES "<<court.fullQueries
    <<" SOURCE_WALL_MS "<<dt
    <<" CURRENT_RSS_KIB "<<rssNowKiB()
    <<" PROCESS_PEAK_RSS_KIB "<<rssPeakKiB()
    <<" FULL_CUBIE_MEETS 0\n"<<std::flush;
  }
  stage("PROCESS_TOTAL_INCLUDING_SETUP_AND_SAMPLES",ms(begin,ProfileClock::now()));
  std::cout<<"R6I_PROFILE_ORIGINAL_STAGE_AND_SIX_PREFIX_PASS SOURCE_RADIUS "<<sourceR
   <<" GOAL_RADIUS "<<g
   <<" ACTUAL_PHYSICAL_SAMPLE_ONLY 1"
   <<" GLOBAL_B10_LOWER17_NOT_CLAIMED 1\n"<<std::flush;
  return 0;
 }catch(const std::exception&e){
  std::cerr<<"R6I_PROFILE_ERROR "<<e.what()<<"\n";return 4;
 }
}
