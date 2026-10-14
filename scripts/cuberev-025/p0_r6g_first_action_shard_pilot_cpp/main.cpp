// CUBE-REV 0.25 P0-R6G: FIRST physically verified prefix shard court.
// Validation-only: source radius<=7, NOT the 18 expensive B10 proof jobs.
// Every exact original legal first action is a unique disjoint shard.
#define CUBEREV_P0R6E_AS_LIBRARY
#include "../p0_r6e_packed_projected_two_turn_cpp/main.cpp"
#undef CUBEREV_P0R6E_AS_LIBRARY

uint64_t exactCanonicalFirstMoveCalls(int first,int radius){
 std::array<uint64_t,18> count{};
 count[first]=1;
 uint64_t visits=0;
 for(int depth=1;depth<=radius;depth++){
   if(depth>1){
     std::array<uint64_t,18> next{};
     for(int a=0;a<18;a++)
       for(int b=0;b<18;b++)
         if(canonical(b,a))next[a]+=count[b];
     count=next;
   }
   uint64_t level=0;
   for(uint64_t n:count)level+=n;
   visits+=uint64_t(radius-depth+1)*level;
 }
 return visits;
}
int main(int argc,char**argv){
 try{
   const int goalR=argc>1?std::stoi(argv[1]):3;
   const int sourceR=argc>2?std::stoi(argv[2]):3;
   const int seconds=argc>3?std::stoi(argv[3]):240;
   const int selected=argc>4?std::stoi(argv[4]):-1;
   if(goalR<0||goalR>6||sourceR<1||sourceR>10||seconds<1||
      selected<-1||selected>17||(sourceR>7&&selected<0))
     throw std::runtime_error("R6G all 18 shards goal<=6 source<=7; optional single shard source<=10");
   initTurns();
   const auto scr=parse("R' B' F2 D2 F2 L2 R2 U' F2 L2 D2 B2 D F L' R2 B U2 F2 R2");
   const auto known=parse("F U F D' R' F' L' F' D' L B L2 F2 U2 L2 U F' R2");
   Cube source=cubeAfter(scr);
   Stickers original=solvedStickers();
   for(int a:scr)physicalTurn(original,names[a]);
   if(!(exactKey(source)==exactKey(fromStickers(original))) ||
      known.size()!=18 || !physicalSolves(scr,known))
     throw std::runtime_error("original official source/18turn sticker physics mismatch");
   const uint64_t physicalChecks=physicallyAuditFastProjection();
   if(physicalChecks!=4608)throw std::runtime_error("full packed legal 18HTM physics mismatch");
   PackedOrderedCourt court;
   court.court.started=Clock::now();
   court.court.secondsBudget=seconds;
   if(!court.court.build(goalR)){
     std::cout<<"P0R6G_RESOURCE_HOLD_GOAL\n";return 2;
   }
   court.project();court.prepareEdges();
   FullKey root=exactKey(source);
   if(court.court.goal.find(root)!=court.court.goal.end()){
     std::cout<<"P0R6G_ROOT_FULL_CUBIE_INTERSECTION NO_NEGATIVE_CERTIFICATE\n";
     return 3;
   }
   uint64_t totalVisited=uint64_t(sourceR+1);
   uint64_t totalSkipped=0;
   uint64_t summedBaseline=uint64_t(sourceR+1);
   int certifiedShards=0;
   std::array<bool,18> certified{};
   std::cout<<"P0R6G_GOAL_FULL "<<court.court.goal.size()
     <<" CORNER6 "<<court.c6.size()
     <<" EDGE6 "<<court.edge6.size()
     <<" ROOT_CHECKED 1 PHYSICAL_PACKED_CASES "<<physicalChecks
     <<"\n"<<std::flush;
   for(int first=0;first<18;first++){
     if(selected>=0&&first!=selected)continue;
     court.visits=0;court.skippedChildren=0;
     const Cube firstCube=composeCube(source,turn[first]);
     for(int limit=1;limit<=sourceR;limit++){
       court.path.assign(1,first);
       if(court.fastVisit(firstCube,1,limit,first)){
         std::cout<<"P0R6G_TRUE_FULL_CUBIE_MEET FIRST_ACTION "<<first
           <<" WORD "<<join(court.foundPrefix)
           <<" NO_NEGATIVE_CERTIFICATE\n";
         return 3;
       }
       if(court.cut||court.court.expired()){
         std::cout<<"P0R6G_RESOURCE_HOLD_SHARD "<<first<<"\n";return 2;
       }
     }
     const uint64_t baseline=exactCanonicalFirstMoveCalls(first,sourceR);
     if(court.visits+court.skippedChildren!=baseline)
       throw std::runtime_error("canonical first-action shard incomplete");
     std::cout<<"P0R6G_PHYSICAL_SHARD_COMPLETE ACTION_ID "<<first
       <<" BASELINE "<<baseline<<" VISITED "<<court.visits
       <<" SKIPPED "<<court.skippedChildren
       <<" GOAL_MEETS 0\n"<<std::flush;
     totalVisited+=court.visits;
     totalSkipped+=court.skippedChildren;
     summedBaseline+=baseline;
     certified[first]=true;
     certifiedShards++;
   }
   if(selected>=0){
     const uint64_t firstBaseline=exactCanonicalFirstMoveCalls(selected,sourceR);
     const uint64_t firstVisits=totalVisited-uint64_t(sourceR+1);
     if(certifiedShards!=1||!certified[selected]||
        firstVisits+totalSkipped!=firstBaseline||
        summedBaseline!=firstBaseline+uint64_t(sourceR+1))
       throw std::runtime_error("selected first-move physical proof subset incomplete");
     if(goalR==6&&sourceR==10){
       const uint64_t expected=selected<9?17489205559ULL:14279876542ULL;
       if(firstBaseline!=expected||court.court.goal.size()!=8240087ULL||
          court.c6.size()!=1405068ULL)
         throw std::runtime_error("source B10 canonical first-action / goal B6 regression failed");
     }
     std::cout<<"P0R6G_SINGLE_SHARD_COMPLETE 1 ACTION_ID "<<selected
       <<" GOAL_RADIUS "<<goalR<<" SOURCE_RADIUS "<<sourceR
       <<" ROOT_PHYSICAL_CHECKED 1"
       <<" SHARD_BASELINE "<<firstBaseline
       <<" SHARD_VISITED "<<firstVisits
       <<" SHARD_SAFE_SKIPS "<<totalSkipped
       <<" FULL_CUBIE_GOAL_MEETS 0"
       <<" CANONICAL_LAST_ACTION_CONTEXT_PRESERVED 1"
       <<" NOT_A_GLOBAL_SOURCE_COVER 1"
       <<" ORIGINAL_54_STICKER_PHYSICS_PASS 1"
       <<"\\n"<<std::flush;
     return 0;
   }
   for(bool flag:certified)if(!flag)
     throw std::runtime_error("missing first generator");
   if(certifiedShards!=18 ||
      totalVisited+totalSkipped!=summedBaseline ||
      summedBaseline!=canonicalBaselineVisits(sourceR))
     throw std::runtime_error("global 18-shard + root normal-form cover mismatch");
   if(goalR==6&&sourceR==7){
     if(summedBaseline!=120213368ULL ||
        court.court.goal.size()!=8240087ULL ||
        court.c6.size()!=1405068ULL)
       throw std::runtime_error("original full B7 physical proof regression drift");
   }
   std::cout<<"P0R6G_ALL_18_FIRST_ACTIONS_AND_ROOT_COMPLETE 1"
     <<" ROOT_CALLS "<<sourceR+1
     <<" SHARD_COUNT "<<certifiedShards
     <<" TOTAL_BASELINE "<<summedBaseline
     <<" TOTAL_ACTUAL_VISITS "<<totalVisited
     <<" TOTAL_SAFE_SKIPS "<<totalSkipped
     <<" TRUE_FULL_CUBIE_MEETS 0"
     <<" CANONICAL_UNION_EXACT 1"
     <<" ORIGINAL_54_STICKER_PHYSICS_PASS 1"
     <<"\n"<<std::flush;
   return 0;
 }catch(std::exception const&e){
   std::cerr<<"P0R6G_ERROR "<<e.what()<<"\n";return 4;
 }
}
