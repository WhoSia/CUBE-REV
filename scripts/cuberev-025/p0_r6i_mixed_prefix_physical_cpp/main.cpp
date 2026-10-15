// CUBE-REV P0-R6I: REAL 54-STICKER 18HTM MIXED-DEPTH PREFIX PILOT.
// Source R<=7 only, not original source B10 proof and not global lower17.
#define CUBEREV_P0R6E_AS_LIBRARY
#include "../p0_r6e_packed_projected_two_turn_cpp/main.cpp"
#undef CUBEREV_P0R6E_AS_LIBRARY

uint64_t cylinderBudget(int last,int remaining){
 std::array<uint64_t,18> old{};
 uint64_t total=uint64_t(remaining+1);
 for(int depth=1;depth<=remaining;depth++){
   std::array<uint64_t,18> next{};
   if(depth==1){
     for(int a=0;a<18;a++)if(canonical(last,a))next[a]=1;
   }else{
     for(int a=0;a<18;a++)for(int b=0;b<18;b++)
       if(canonical(b,a))next[a]+=old[b];
   }
   old=next;
   uint64_t layer=0;
   for(auto x:old)layer+=x;
   total+=uint64_t(remaining-depth+1)*layer;
 }
 return total;
}
std::vector<std::vector<int>> makeMixedCutset(){
 std::vector<std::vector<int>> frontier;
 for(int first=0;first<18;first++){
   if(first==0||first==9){
     for(int next=0;next<18;next++)
       if(canonical(first,next))frontier.push_back({first,next});
   }else frontier.push_back({first});
 }
 return frontier;
}
int main(int argc,char**argv){
 try{
   const int goalRadius=argc>1?std::stoi(argv[1]):3;
   const int sourceRadius=argc>2?std::stoi(argv[2]):3;
   const int seconds=argc>3?std::stoi(argv[3]):210;
   if(goalRadius<0||goalRadius>6||sourceRadius<2||
      sourceRadius>7||seconds<1)throw std::runtime_error("only original physical B3/B3 or B6/B7");
   initTurns();
   const auto scramble=parse("R' B' F2 D2 F2 L2 R2 U' F2 L2 D2 B2 D F L' R2 B U2 F2 R2");
   const auto solvedWord=parse("F U F D' R' F' L' F' D' L B L2 F2 U2 L2 U F' R2");
   Cube source=cubeAfter(scramble);
   Stickers original=solvedStickers();
   for(int a:scramble)physicalTurn(original,names[a]);
   if(!(exactKey(source)==exactKey(fromStickers(original)))||
     solvedWord.size()!=18||!physicalSolves(scramble,solvedWord))
     throw std::runtime_error("original real 54 sticker physical regression failed");
   if(physicallyAuditFastProjection()!=4608)
     throw std::runtime_error("packed physical operator 4608 regression failed");
   PackedOrderedCourt court;
   court.court.started=Clock::now();court.court.secondsBudget=seconds;
   if(!court.court.build(goalRadius)){
     std::cout<<"P0R6I_RESOURCE_HOLD_GOAL\n";return 2;
   }
   court.project();court.prepareEdges();
   const auto frontier=makeMixedCutset();
   if(frontier.size()!=43)throw std::runtime_error("unexpected actual grammar 43 prefix frontier");
   // The exact internal nodes of this cutset are [], [0], and [9].
   uint64_t internal=uint64_t(sourceRadius+1)+2*uint64_t(sourceRadius);
   for(auto p:std::vector<std::vector<int>>{{},{0},{9}}){
     Cube x=source;
     for(int a:p)x=composeCube(x,turn[a]);
     if(court.court.goal.find(exactKey(x))!=court.court.goal.end()){
       std::cout<<"P0R6I_TRUE_FULL_CUBIE_INTERNAL_MEET\n";return 3;
     }
   }
   std::cout<<"P0R6I_ORIGINAL_GOAL_FULL "<<court.court.goal.size()
     <<" CORNER6 "<<court.c6.size()<<" EDGE6 "<<court.edge6.size()
     <<" ORIGINAL_PACKED_PHYSICAL_CASES 4608"
     <<" INTERNAL_ROOT_AND_PREFIX_CHECKS 3\n"<<std::flush;
   uint64_t visits=internal,omissions=0,total=internal;
   int completed=0;
   for(const auto&p:frontier){
     const int depth=int(p.size());
     Cube from=source;
     for(int a:p)from=composeCube(from,turn[a]);
     court.visits=0;court.skippedChildren=0;
     for(int lim=depth;lim<=sourceRadius;lim++){
       court.path=p;
       if(court.fastVisit(from,depth,lim,p.back())){
         std::cout<<"P0R6I_TRUE_FULL_CUBIE_LEAF_MEET PREFIX "<<join(p)<<"\n";
         return 3;
       }
       if(court.cut||court.court.expired()){
         std::cout<<"P0R6I_HOLD_PREFIX "<<join(p)<<"\n";return 2;
       }
     }
     auto baseline=cylinderBudget(p.back(),sourceRadius-depth);
     if(court.visits+court.skippedChildren!=baseline)
       throw std::runtime_error("shard weighted original grammar calls not fully accounted");
     std::cout<<"P0R6I_PHYSICAL_CYLINDER_COMPLETE FIRST "<<p[0]
       <<" SECOND "<<(depth==2?p[1]:-1)
       <<" DEPTH "<<depth<<" WEIGHT "<<baseline
       <<" VISITED "<<court.visits<<" SKIPPED "<<court.skippedChildren
       <<" COMPLETE_CUBIE_HITS 0\n"<<std::flush;
     visits+=court.visits;omissions+=court.skippedChildren;
     total+=baseline;completed++;
   }
   const auto expected=canonicalBaselineVisits(sourceRadius);
   if(completed!=43||visits+omissions!=expected||total!=expected)
     throw std::runtime_error("mixed-depth source proof exact full cover does not add up");
   if(sourceRadius==7&&(expected!=120213368ULL||
      court.court.goal.size()!=8240087ULL||court.c6.size()!=1405068ULL))
     throw std::runtime_error("full original 54 sticker B6/B7 goal and canonical root mismatch");
   std::cout<<"P0R6I_ORIGINAL_43_MIXED_DEPTH_CUTSET_CERT COMPLETE 1"
     <<" LEAF_CYLINDERS 43 INTERNAL_NODES 3"
     <<" INTERNAL_CALLS "<<internal
     <<" TOTAL_BASELINE "<<expected
     <<" VISITED_INCLUDING_INTERNAL "<<visits
     <<" SAFELY_SKIPPED "<<omissions
     <<" COMPLETE_CUBIE_HITS 0"
     <<" ORIGINAL_PHYSICAL_SOURCE_COMPLETE 1\n"<<std::flush;
   return 0;
 }catch(const std::exception&e){
   std::cerr<<"P0R6I_ERROR "<<e.what()<<"\n";return 4;
 }
}
