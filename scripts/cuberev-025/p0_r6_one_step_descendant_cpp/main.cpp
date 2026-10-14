// CUBE-REV 0.25 P0-R6: exact one-step corner descendant exclusion.
// Uses the independently completed full physical B6/B7 certificate engine.
#define CUBEREV_P1R6_AS_LIBRARY
#include "../../cuberev-024/p1_r6_global_full18_bidir_cpp/main.cpp"
#undef CUBEREV_P1R6_AS_LIBRARY
#include <unordered_set>
#include <unordered_map>
#include <iomanip>
// Independent combinatorial count of ALL complete canonical source DFS entries.
// Does not inspect cubie states or depend on the pruning algorithm.
uint64_t canonicalBaselineVisits(int radius) {
  std::vector<uint64_t> byLast(18,0);
  uint64_t count=uint64_t(radius+1);
  for(int depth=1;depth<=radius;depth++) {
    std::vector<uint64_t> next(18,0);
    for(int a=0;a<18;a++) {
      if(depth==1) next[a]=canonical(-1,a)?1:0;
      else for(int last=0;last<18;last++)
        if(canonical(last,a)) next[a]+=byLast[last];
    }
    uint64_t layer=0;
    for(auto number:next)layer+=number;
    count+=layer*uint64_t(radius-depth+1);
    byLast.swap(next);
  }
  return count;
}

struct R6 {
 GlobalCourt court;
 std::unordered_set<U64> c6,c7;
 uint64_t visits=0,descendantCuts=0,skippedChildren=0,fullQueries=0,fullHits=0;
 bool cut=false,meet=false;
 void project() {
   // A cubie representative is used only to apply genuine 18HTM
   // corner transitions. Its edges do not affect corner transitions.
   std::unordered_map<U64,FullKey> representatives;
   representatives.reserve(1650000);
   for(const auto& key:court.goal) representatives.emplace(key.c,key);
   c6.reserve(representatives.size()*2);
   c7.reserve(representatives.size()*8);
   for(const auto& kv:representatives) c6.insert(kv.first);
   c7.insert(c6.begin(),c6.end());
   for(const auto& kv:representatives) {
     const Cube state=cubeFromKey(kv.second);
     for(int a=0;a<18;a++) c7.insert(exactKey(composeCube(state,turn[a])).c);
   }
 }
 bool visit(Cube const&s,int depth,int limit,int last) {
   ++visits;
   if((visits&0xffff)==0 &&court.expired()){cut=true;return false;}
   FullKey key=exactKey(s);
   if(c6.find(key.c)!=c6.end()) {
     ++fullQueries;
     if(court.goal.find(key)!=court.goal.end()){++fullHits;meet=true;return true;}
   }
   if(depth==limit)return false;
   // At exactly one available source move, any matching full state must
   // have its corners in pi_C(B6)*A. Absence excludes ALL children.
   if(limit-depth==1 && c7.find(key.c)==c7.end()){
     ++descendantCuts;
     for(int a=0;a<18;a++)if(canonical(last,a))++skippedChildren;
     return false;
   }
   for(int a=0;a<18;a++) {
     if(!canonical(last,a))continue;
     if(visit(composeCube(s,turn[a]),depth+1,limit,a))return true;
     if(cut)return false;
   }
   return false;
 }
 bool check(Cube const&source,int maxDepth) {
   for(int k=0;k<=maxDepth;k++){
     const auto v=visits,p=descendantCuts;
     const bool hit=visit(source,0,k,-1);
     std::cout<<"P0R6_DEPTH "<<k<<" COMPLETE "<<(cut?0:1)
       <<" VISITS "<<(visits-v)<<" DESCENDANT_CUTS "<<(descendantCuts-p)
       <<" FULL_HIT "<<(hit?1:0)<<"\n"<<std::flush;
     if(hit||cut)return hit;
   }
   return false;
 }
};
#ifndef CUBEREV_P0R6_AS_LIBRARY
int main(int argc,char**argv) {
 try {
   int rg=argc>1?std::stoi(argv[1]):6;
   int rs=argc>2?std::stoi(argv[2]):7;
   int seconds=argc>3?std::stoi(argv[3]):850;
   if(rg<0||rg>6||rs<0||rs>8||seconds<1)
     throw std::runtime_error("safe radii 0..6 and 0..8");
   initTurns();
   auto sourceWords=parse("R' B' F2 D2 F2 L2 R2 U' F2 L2 D2 B2 D F L' R2 B U2 F2 R2");
   auto solveWords=parse("F U F D' R' F' L' F' D' L B L2 F2 U2 L2 U F' R2");
   Cube source=cubeAfter(sourceWords);
   Stickers physical=solvedStickers();
   for(auto a:sourceWords)physicalTurn(physical,names[a]);
   if(!(exactKey(source)==exactKey(fromStickers(physical)))||!physicalSolves(sourceWords,solveWords))
     throw std::runtime_error("source or 18-word fails original 54-sticker replay");
   R6 r;
   r.court.started=Clock::now();
   r.court.secondsBudget=seconds;
   if(!r.court.build(rg)){std::cout<<"P0R6_RESOURCE_HOLD_GOAL\n";return 2;}
   r.project();
   std::cout<<"P0R6_CORNERS_GOAL "<<r.c6.size()<<" ONE_STEP_ENVELOPE "<<r.c7.size()<<"\n"<<std::flush;
   bool hit=r.check(source,rs);
   if(r.cut||r.court.expired()){std::cout<<"P0R6_RESOURCE_HOLD_SOURCE\n";return 2;}
   if(hit){std::cout<<"P0R6_INTERSECTION_FOUND LOWER_CERTIFICATE_WITHHELD\n";return 3;}
   const uint64_t baseline=canonicalBaselineVisits(rs);
   if(r.visits+r.skippedChildren!=baseline)
     throw std::runtime_error("incomplete canonical source accounting");
   std::cout<<"P0R6_CANONICAL_ACCOUNTING BASELINE "<<baseline
     <<" VISITED "<<r.visits<<" SKIPPED "<<r.skippedChildren
     <<" EXACT_EQUATION_PASS 1\n";
   std::cout<<"P0R6_COMPLETE 1 FULL_GOAL "<<r.court.goal.size()
     <<" SOURCE_VISITS "<<r.visits<<" DESCENDANT_CUTS "<<r.descendantCuts
     <<" SKIPPED_CHILDREN "<<r.skippedChildren<<" FULL_QUERIES "<<r.fullQueries
     <<" FULL_HITS "<<r.fullHits<<" SOUND_ONE_STEP_DESCENDANT_PRUNING 1\n";
   if(rg==6&&rs==7) {
     if(baseline!=120213368ULL)throw std::runtime_error("original normal form size mismatch");
     if(r.court.goal.size()!=8240087||r.c6.size()!=1405068||r.fullHits!=0)
       throw std::runtime_error("original full-cubie baseline mismatch");
     std::cout<<"P0R6_GLOBAL_LOWER 14 UPPER 18 NEW_LOWER_NOT_CLAIMED 1\n";
   }
   if(rg==6&&rs==8) {
     // This *only* executes when the entire B8 source DFS has completed
     // without a complete physical B6(goal) match or resource hold.
     if(r.court.goal.size()!=8240087||r.c6.size()!=1405068
        ||baseline!=1604664504ULL||r.fullHits!=0)
       throw std::runtime_error("14-turn global exclusion regression failed");
     std::cout<<"P0R6_GLOBAL_LOWER 15 UPPER 18"
       <<" SOURCE_B8_GOAL_B6_COMPLETE 1 ALL_14_OR_LESS_EXCLUDED 1\n";
   }
   return 0;
 } catch(const std::exception&e){std::cerr<<"P0R6_ERROR "<<e.what()<<"\n";return 4;}
}

#endif // CUBEREV_P0R6_AS_LIBRARY
