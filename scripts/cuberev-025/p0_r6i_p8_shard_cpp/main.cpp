// P0-R6I-P8 multi-worker, actually executed source B7 proof batches.
// Each worker independently builds and commits the entire original B6.
// Inside one worker, all assigned source leaves share an immutable goal.
// Only external independent Go merger may certify the GLOBAL 43-leaf cut.
#define main inherited_p8_batch_single_main
#include "../p0_r6i_p8_proof_batch_cpp/main.cpp"
#undef main

int main(int argc,char**argv){
 try{
  if(argc!=4)throw std::runtime_error("usage: shard_id_0_to_3 canonical_sorted_goal_file seconds");
  const int shard=std::stoi(argv[1]);
  const std::string file=argv[2];
  const int timeBudget=std::stoi(argv[3]);
  if(shard<0||shard>3||timeBudget<1||file.empty())
   throw std::runtime_error("only four disjoint source worker jobs are defined");
  initTurns();
  const auto scramble=parse("R' B' F2 D2 F2 L2 R2 U' F2 L2 D2 B2 D F L' R2 B U2 F2 R2");
  const auto solution=parse("F U F D' R' F' L' F' D' L B L2 F2 U2 L2 U F' R2");
  const Cube original=cubeAfter(scramble);
  Stickers whole=solvedStickers();
  for(int a:scramble)physicalTurn(whole,names[a]);
  if(!(exactKey(original)==exactKey(fromStickers(whole)))||
     solution.size()!=18||!physicalSolves(scramble,solution)||
     physicallyAuditFastProjection()!=4608)
    throw std::runtime_error("actual 54-sticker full physical initial-state regression");
  PackedOrderedCourt court;
  court.court.started=Clock::now();
  court.court.secondsBudget=timeBudget;
  if(!court.court.build(6)){std::cout<<"P8_SHARD_GOAL_HOLD\n";return 2;}
  court.project();court.prepareEdges();
  if(court.court.goal.size()!=8240087||
     court.c6.size()!=1405068||court.edge6.size()!=7672278)
    throw std::runtime_error("source physical B6 goal cardinalities drift");
  const auto goal=goalDigest(court.court,6,file);
  if(goal!="82fe545bcad3537c989ec22afce9d286926ddce5f4ef9428c0307951ec2d0979")
   throw std::runtime_error("physical original B6 SHA256 not pinned golden goal");
  std::cout<<"P8_SHARD_GOAL SHARD "<<shard<<" TOTAL_SHARDS 4 SHA256 "<<goal
   <<" GOAL_RADIUS 6 SOURCE_RADIUS 7 GOAL_STATES "<<court.court.goal.size()
   <<" C "<<court.c6.size()<<" E "<<court.edge6.size()
   <<" PHYSICS_4608 1 GOAL_IMAGE_BYTES "<<16ULL*court.court.goal.size()
   <<" PEAK_RSS_KIB "<<rssKiB()<<"\n"<<std::flush;
  uint64_t total=0,seen=0,omitted=0;
  int internals=0,leaves=0;
  if(shard==0){
   for(auto const&p:std::vector<std::vector<int>>{{},{0},{9}}){
    Cube x=original;for(int a:p)x=composeCube(x,turn[a]);
    if(court.court.goal.count(exactKey(x))){
     std::cout<<"P8_SHARD_INTERNAL_TARGET_MEET HOLD\n";return 3;
    }
    uint64_t mass=8-p.size();
    total+=mass;seen+=mass;internals++;
    std::cout<<"P8_SHARD_INTERNAL SHARD "<<shard<<" INDEX "<<internals
     <<" FIRST "<<(p.empty()?-1:p[0])<<" DEPTH "<<p.size()
     <<" REPEATED_CALLS "<<mass<<" FULL_GOAL_MEETS 0 SHA256 "<<goal<<"\n"<<std::flush;
   }
  }
  const auto prefixes=frontier43();
  for(size_t global=0;global<prefixes.size();global++){
   if(int(global%4)!=shard)continue;
   auto const&p=prefixes[global];
   Cube x=original;for(int a:p)x=composeCube(x,turn[a]);
   court.visits=0;court.skippedChildren=0;court.fullHits=0;
   court.fullQueries=0;court.orderedPairChecks=0;court.edgePackedChecks=0;
   court.cut=false;
   auto start=std::chrono::steady_clock::now();
   for(int d=int(p.size());d<=7;d++){
    court.path=p;
    if(court.fastVisit(x,int(p.size()),d,p.back())){
     std::cout<<"P8_SHARD_TRUE_LEAF_TARGET_MEET HOLD\n";return 3;
    }
    if(court.cut||court.court.expired()){
     std::cout<<"P8_SHARD_RESOURCE_HOLD_NO_CERT\n";return 2;
    }
   }
   const auto wt=p8Weight(p.back(),7-int(p.size()));
   if(court.visits+court.skippedChildren!=wt||court.fullHits)
    throw std::runtime_error("shard source exact grammar accounting failed");
   const auto elapsed=std::chrono::duration<double,std::milli>(
      std::chrono::steady_clock::now()-start).count();
   const FullKey key=exactKey(x);
   total+=wt;seen+=court.visits;omitted+=court.skippedChildren;leaves++;
   std::cout<<"P8_SHARD_LEAF SHARD "<<shard<<" GLOBAL_INDEX "<<(global+1)
    <<" LOCAL_INDEX "<<leaves<<" FIRST "<<p.front()
    <<" SECOND "<<(p.size()==2?p[1]:-1)<<" DEPTH "<<p.size()
    <<" SOURCE_KEY_C "<<key.c<<" SOURCE_KEY_E "<<key.e
    <<" WORD_CALLS "<<wt<<" VISITED "<<court.visits
    <<" OMITTED "<<court.skippedChildren
    <<" PAIRS "<<court.orderedPairChecks<<" EDGES "<<court.edgePackedChecks
    <<" FULL_QUERIES "<<court.fullQueries
    <<" WALL_MS "<<std::fixed<<std::setprecision(3)<<elapsed
    <<" FULL_CUBIE_MEETS 0 COMPLETE 1 SHA256 "<<goal<<"\n"<<std::flush;
  }
  const auto finalDigest=goalDigest(court.court,6,"");
  if(goal!=finalDigest)throw std::runtime_error("shared goal mutated during source shard");
  if(leaves!=(shard==3?10:11)||internals!=(shard==0?3:0)||
     seen+omitted!=total)
   throw std::runtime_error("shard mass, internal, leaf or visit mismatch");
  std::cout<<"P8_SHARD_DONE SHARD "<<shard<<" TOTAL_SHARDS 4"
    <<" GOAL_SHA256 "<<goal<<" AFTER_SHA256 "<<finalDigest
    <<" LOCAL_CERT_COMPLETE 1 GLOBAL_SOURCE_COMPLETE 0"
    <<" LEAVES "<<leaves<<" INTERNALS "<<internals
    <<" WORD_CALLS "<<total<<" VISITED "<<seen<<" OMITTED "<<omitted
    <<" FULL_CUBIE_GOAL_MEETS 0 PEAK_RSS_KIB "<<rssKiB()<<"\n"<<std::flush;
  return 0;
 }catch(const std::exception&e){
  std::cerr<<"P8_SHARD_ERROR "<<e.what()<<"\n";return 4;
 }
}
