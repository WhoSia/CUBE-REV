// CUBE-REV 0.25 P0-R5: physically exact corner prefilter for FULL cubie B6/B7.
// A sound one-sided negative membership filter; DO NOT prune descendants.
// Reuse previously externally independently certified original full-cubie physics.
#define CUBEREV_P1R6_AS_LIBRARY
#include "../../cuberev-024/p1_r6_global_full18_bidir_cpp/main.cpp"
#undef CUBEREV_P1R6_AS_LIBRARY
#include <unordered_set>
#include <iomanip>

struct P0R5Court {
 GlobalCourt goalCourt;
 std::unordered_set<U64> projectedCorner;
 uint64_t sourceVisits=0, projectedRejects=0, fullQueries=0, fullHits=0;
 bool cut=false, matched=false;
 vector<uint64_t> depthVisits, depthRejects, depthFullQueries;
 vector<int> path;
 bool visit(Cube const&s,int depth,int limit,int last) {
   ++sourceVisits; ++depthVisits[depth];
   if ((sourceVisits&0xffff)==0 && goalCourt.expired()) {cut=true;return false;}
   auto key=exactKey(s);
   // Necessary for full-cube goal-ball membership, exact no-false-negative.
   if (projectedCorner.find(key.c)==projectedCorner.end()) {
     ++projectedRejects; ++depthRejects[depth];
   } else {
     ++fullQueries; ++depthFullQueries[depth];
     if (goalCourt.goal.find(key)!=goalCourt.goal.end()) {
       ++fullHits; matched=true;
       return true;
     }
   }
   if(depth==limit)return false;
   for(int a=0;a<18;a++) {
     if(!canonical(last,a))continue;
     path.push_back(a);
     if(visit(composeCube(s,turn[a]),depth+1,limit,a))return true;
     path.pop_back();if(cut)return false;
   }
   return false;
 }
 bool check(Cube const&source,int maximum) {
   for(int k=0;k<=maximum;k++) {
     auto v=sourceVisits,rej=projectedRejects,q=fullQueries;
     depthVisits.assign(k+1,0);
     depthRejects.assign(k+1,0);
     depthFullQueries.assign(k+1,0);
     path.clear();
     bool match=visit(source,0,k,-1);
     std::cout<<"P0R5_FULL_PHYSICAL_SOURCE_BOUND "<<k<<" COMPLETED "<<(cut?0:1)
              <<" SOURCE_VISITS "<<(sourceVisits-v)
              <<" CORNER_REJECT "<<(projectedRejects-rej)
              <<" EXACT_FULL_CUBIE_QUERIES "<<(fullQueries-q)
              <<" INTERSECTIONS "<<(match?1:0)<<"\n"<<std::flush;
     if(cut||match)return match;
   }
   return false;
 }
};
int main(int argc,char**argv) {
 try {
   const int goalRadius=argc>1?std::stoi(argv[1]):6;
   const int sourceRadius=argc>2?std::stoi(argv[2]):7;
   const int budget=argc>3?std::stoi(argv[3]):480;
   if(goalRadius<0||goalRadius>6||sourceRadius<0||sourceRadius>7||budget<1)
     throw std::runtime_error("safe parameter domain: goal<=6, source<=7");
   initTurns();
   std::string original="R' B' F2 D2 F2 L2 R2 U' F2 L2 D2 B2 D F L' R2 B U2 F2 R2";
   auto tokens=parse(original),correct18=parse("F U F D' R' F' L' F' D' L B L2 F2 U2 L2 U F' R2");
   Cube source=cubeAfter(tokens);
   Stickers orig=solvedStickers();
   for(auto a:tokens)physicalTurn(orig,names[a]);
   if(!(exactKey(source)==exactKey(fromStickers(orig)))||!physicalSolves(tokens,correct18))
     throw std::runtime_error("source original 54 sticker input/witness mismatch");
   P0R5Court p;
   p.goalCourt.started=Clock::now();
   p.goalCourt.secondsBudget=budget;
   if(!p.goalCourt.build(goalRadius)) {
     std::cout<<"P0R5_RESOURCE_HOLD_GOAL\n";return 2;
   }
   p.projectedCorner.reserve(1650000);
   for(auto const&k:p.goalCourt.goal) p.projectedCorner.insert(k.c);
   std::cout<<"P0R5_GOAL_FULL_CUBIES "<<p.goalCourt.goal.size()
            <<" DISTINCT_ORIGINAL_CORNERS "<<p.projectedCorner.size()
            <<" ORIGINAL_STICKER_SOURCE_WITNESS PASS\n"<<std::flush;
   const bool match=p.check(source,sourceRadius);
   if(p.cut) {std::cout<<"P0R5_RESOURCE_HOLD_SOURCE\n";return 2;}
   if(match) {
     std::cout<<"P0R5_TRUE_FULL_CUBE_INTERSECTION_FOUND LOWER_BOUND_NOT_CERTIFIED 1\n";return 3;
   }
   if(p.projectedRejects+p.fullQueries!=p.sourceVisits)throw std::runtime_error("incomplete check partition");
   std::cout<<"P0R5_SAFE_ORIGINAL_CUBIE_PREFILTER_COMPLETE 1 GOAL_RADIUS "<<goalRadius
            <<" SOURCE_RADIUS "<<sourceRadius
            <<" FULL_GOAL_STATES "<<p.goalCourt.goal.size()
            <<" CORNER_STATES "<<p.projectedCorner.size()
            <<" SOURCE_VISITS "<<p.sourceVisits
            <<" CORNER_REJECTS "<<p.projectedRejects
            <<" EXPENSIVE_FULL_STATE_LOOKUPS "<<p.fullQueries
            <<" FULL_INTERSECTIONS "<<p.fullHits
            <<" COLLISION_FREE_STATE_EQUALITY 1 NO_DESCENDANT_PRUNING 1\n";
   if(goalRadius==6&&sourceRadius==7) {
     if(p.goalCourt.goal.size()!=8240087||p.sourceVisits!=120213368||p.fullHits!=0)
       throw std::runtime_error("P1R6 whole state baseline drift");
     std::cout<<"P0R5_FULL_PHYSICAL_GEODESIC_BOUNDS_LOWER 14 UPPER 18 OLD_CERTIFICATE_REPRODUCED 1\n";
   }
   return 0;
 } catch(std::exception const&e) {std::cerr<<"P0R5_ERROR "<<e.what()<<"\n";return 4;}
}
