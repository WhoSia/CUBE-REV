// CUBE-REV 0.25 P0-R6C: synchronize exact C6 and E6 projections
// under ONE AND THE SAME actual legal physical 18HTM generator.
// Research-grade source: exact full cubie B6/B7; NOT a joint exact-distance PDB.
#define CUBEREV_P0R6_AS_LIBRARY
#include "../p0_r6_one_step_descendant_cpp/main.cpp"
#undef CUBEREV_P0R6_AS_LIBRARY
#include <unordered_set>
struct JointNextActionCourt : R6 {
 std::unordered_set<U64> edge6;
 uint64_t cornerChildRejects=0,edgeChildRejects=0;
 uint64_t candidateChildren=0,fastCornerEnvelopeCuts=0,jointEmptyCuts=0;
 std::vector<int> path,foundPrefix;
 FullKey foundKey{};
 void prepareEdges(){
   edge6.reserve(court.goal.size());
   for(const auto &state:court.goal)edge6.insert(state.e);
 }
 bool jointVisit(const Cube&s,int depth,int limit,int last) {
   ++visits;
   if((visits&0xffff)==0 && court.expired()){cut=true;return false;}
   const FullKey key=exactKey(s);
   if(c6.find(key.c)!=c6.end()) {
     ++fullQueries;
     if(court.goal.find(key)!=court.goal.end()){
       ++fullHits;meet=true;foundPrefix=path;foundKey=key;return true;
     }
   }
   if(depth==limit)return false;
   if(limit-depth==1){
     if(c7.find(key.c)==c7.end()) {
       ++fastCornerEnvelopeCuts;++descendantCuts;
       for(int a=0;a<18;a++)if(canonical(last,a))++skippedChildren;
       return false;
     }
     uint64_t accepted=0;
     // Joint action test: an actual ONE move must simultaneously enter
     // the goal ball's exact corner AND edge projected sets.
     for(int a=0;a<18;a++){
       if(!canonical(last,a))continue;
       const Cube next=composeCube(s,turn[a]);
       const FullKey nextKey=exactKey(next);
       if(c6.find(nextKey.c)==c6.end()){
         ++skippedChildren;++cornerChildRejects;continue;
       }
       if(edge6.find(nextKey.e)==edge6.end()){
         ++skippedChildren;++edgeChildRejects;continue;
       }
       ++candidateChildren;++accepted;
       path.push_back(a);
       if(jointVisit(next,depth+1,limit,a))return true;
       path.pop_back();
       if(cut)return false;
     }
     if(accepted==0){++descendantCuts;++jointEmptyCuts;}
     return false;
   }
   for(int a=0;a<18;a++){
     if(!canonical(last,a))continue;
     path.push_back(a);
     if(jointVisit(composeCube(s,turn[a]),depth+1,limit,a))return true;
     path.pop_back();
     if(cut)return false;
   }
   return false;
 }
 bool jointCheck(const Cube&s,int radius){
   for(int d=0;d<=radius;d++){
     const auto old=visits,sk=skippedChildren;
     path.clear();
     const bool found=jointVisit(s,0,d,-1);
     std::cout<<"P0R6C_SOURCE_DEPTH "<<d<<" COMPLETE "<<(cut?0:1)
              <<" VISITS "<<visits-old<<" SKIPPED "<<skippedChildren-sk
              <<" INTERSECTION "<<(found?1:0)<<"\n"<<std::flush;
     if(found||cut)return found;
   }
   return false;
 }
};
int main(int argc,char**argv){
 try{
   int rg=argc>1?std::stoi(argv[1]):6;
   int rs=argc>2?std::stoi(argv[2]):7;
   int seconds=argc>3?std::stoi(argv[3]):1050;
   if(rg<0||rg>6||rs<0||rs>8||seconds<1)
     throw std::runtime_error("P0R6C radii goal<=6 source<=8");
   initTurns();
   const auto scramble=parse("R' B' F2 D2 F2 L2 R2 U' F2 L2 D2 B2 D F L' R2 B U2 F2 R2");
   const auto solvedWord=parse("F U F D' R' F' L' F' D' L B L2 F2 U2 L2 U F' R2");
   const Cube source=cubeAfter(scramble);
   Stickers original=solvedStickers();
   for(int a:scramble)physicalTurn(original,names[a]);
   if(!(exactKey(source)==exactKey(fromStickers(original)))||
      solvedWord.size()!=18||!physicalSolves(scramble,solvedWord))
     throw std::runtime_error("original 54-sticker or 18-word witness mismatch");
   JointNextActionCourt r;
   r.court.started=Clock::now();r.court.secondsBudget=seconds;
   if(!r.court.build(rg)){std::cout<<"P0R6C_RESOURCE_HOLD_GOAL\n";return 2;}
   r.project();r.prepareEdges();
   std::cout<<"P0R6C_PROJECTIONS GOAL_FULL "<<r.court.goal.size()
     <<" CORNER6 "<<r.c6.size()<<" CORNER7 "<<r.c7.size()
     <<" EDGE6 "<<r.edge6.size()<<"\n"<<std::flush;
   bool found=r.jointCheck(source,rs);
   if(r.cut||r.court.expired()){std::cout<<"P0R6C_RESOURCE_HOLD_SOURCE\n";return 2;}
   if(found){
     std::cout<<"P0R6C_TRUE_FULL_INTERSECTION SOURCE_PREFIX "
       <<join(r.foundPrefix)<<" FULL_CORNER_KEY "<<r.foundKey.c
       <<" FULL_EDGE_KEY "<<r.foundKey.e
       <<" LOWER_BOUND_NOT_CERTIFIED 1\n";
     return 3;
   }
   const uint64_t baseline=canonicalBaselineVisits(rs);
   if(r.visits+r.skippedChildren!=baseline)
     throw std::runtime_error("joint-action source complete partition FAILED");
   std::cout<<"P0R6C_EXACT_COVER BASELINE "<<baseline
     <<" VISITS "<<r.visits<<" SKIPPED "<<r.skippedChildren
     <<" CORNER_CHILD_REJECT "<<r.cornerChildRejects
     <<" EDGE_CHILD_REJECT "<<r.edgeChildRejects
     <<" FAST_ENVELOPE_CUTS "<<r.fastCornerEnvelopeCuts
     <<" JOINT_EMPTY_CUTS "<<r.jointEmptyCuts
     <<" POTENTIAL_CHILDREN "<<r.candidateChildren
     <<" FULL_QUERIES "<<r.fullQueries
     <<" FULL_HITS "<<r.fullHits<<" COMPLETE 1\n";
   if(rg==6&&(rs==7||rs==8)){
     if(r.court.goal.size()!=8240087||r.c6.size()!=1405068)
       throw std::runtime_error("original full physical baseline drift");
     const uint64_t expected=rs==7?120213368ULL:1604664504ULL;
     if(baseline!=expected)
       throw std::runtime_error("canonical source count mismatch");
     std::cout<<"P0R6C_CERTIFIED_PHYSICAL_GLOBAL_LOWER "<<(rg+rs+1)
       <<" UPPER 18 COMPLETE 1 COMMON_ACTION_SOUND 1"
       <<" NOT_A_COUPLED_DISTANCE_PDB 1\n";
   }
   return 0;
 }catch(const std::exception&e){std::cerr<<"P0R6C_ERROR "<<e.what()<<"\n";return 4;}
}
