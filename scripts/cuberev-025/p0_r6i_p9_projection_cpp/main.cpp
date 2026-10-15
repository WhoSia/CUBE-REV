// CUBE-REV 0.25 P0-R6I-P9 real native 54-sticker projection-evidence
// generator and calibrated source B10 OPEN-first-action pilot.
// All source semantics inherit original CP/CO/EP/EO 18HTM core.
#define CUBEREV_P8_AS_LIBRARY
#include "../p0_r6i_p8_proof_batch_cpp/main.cpp"
#undef CUBEREV_P8_AS_LIBRARY

static std::string projectionDigest(const std::unordered_set<U64>&set,
 const std::string& label,const std::string&file){
 std::vector<U64> arr(set.begin(),set.end());
 std::sort(arr.begin(),arr.end());
 std::ofstream out(file,std::ios::binary|std::ios::trunc);
 if(!out)throw std::runtime_error("projection file not writable");
 SHA256_CTX ctx;SHA256_Init(&ctx);
 const std::string header="CUBE-REV-025-P9:PROJECTED-U64LE:v1;type="+
  label+";goal-radius=6;count="+std::to_string(arr.size())+"\n";
 SHA256_Update(&ctx,header.data(),header.size());
 U64 prev=0;
 for(size_t i=0;i<arr.size();i++){
  if(i && arr[i]<=prev)throw std::runtime_error("projection sort/unique");
  prev=arr[i];unsigned char b[8];putLE64(b,arr[i]);
  SHA256_Update(&ctx,b,8);
  out.write(reinterpret_cast<const char*>(b),8);
 }
 out.close();if(!out)throw std::runtime_error("projection write failure");
 unsigned char d[SHA256_DIGEST_LENGTH];SHA256_Final(d,&ctx);
 std::ostringstream h;h<<std::hex<<std::setfill('0');
 for(unsigned char b:d)h<<std::setw(2)<<unsigned(b);
 return h.str();
}
static void writeTurns(const std::string&file){
 std::ofstream out(file,std::ios::binary|std::ios::trunc);
 if(!out)throw std::runtime_error("unable to write 18 true physical turns");
 for(int a=0;a<18;a++){
  const Cube&t=turn[a];unsigned char buf[16];
  for(int i=0;i<8;i++){buf[i]=t.cp[i];buf[8+i]=t.co[i];}
  out.write(reinterpret_cast<const char*>(buf),16);
 }
 out.close();if(!out)throw std::runtime_error("truncated turn table");
}
static void writeProjection(const std::string&label,
 const std::unordered_set<U64>&data,const std::string&prefix){
 const auto digest=projectionDigest(data,label,prefix+"-"+label+".bin");
 std::cout<<"P9_PROJECTION TYPE "<<label<<" COUNT "<<data.size()
  <<" SNAPSHOT_BYTES "<<data.size()*8ULL<<" SHA256 "<<digest
  <<" ORIG_FULL_GOAL_SHA256 82fe545bcad3537c989ec22afce9d286926ddce5f4ef9428c0307951ec2d0979\n"<<std::flush;
}
#ifndef CUBEREV_P9_AS_LIBRARY
int main(int argc,char**argv){
 try{
  if(argc!=4)throw std::runtime_error("usage: audit|pilot outputPrefix seconds");
  std::string mode=argv[1],prefix=argv[2];
  int budget=std::stoi(argv[3]);
  if((mode!="audit"&&mode!="pilot")||budget<1)throw std::runtime_error("mode audit/pilot");
  auto start=std::chrono::steady_clock::now();
  initTurns();
  const auto scr=parse("R' B' F2 D2 F2 L2 R2 U' F2 L2 D2 B2 D F L' R2 B U2 F2 R2");
  const auto solution=parse("F U F D' R' F' L' F' D' L B L2 F2 U2 L2 U F' R2");
  const Cube source=cubeAfter(scr);
  Stickers physical=solvedStickers();
  for(int a:scr)physicalTurn(physical,names[a]);
  if(!(exactKey(source)==exactKey(fromStickers(physical)))||
    solution.size()!=18||!physicalSolves(scr,solution)||
    physicallyAuditFastProjection()!=4608)throw std::runtime_error("true physical origin");
  PackedOrderedCourt court;
  court.court.started=Clock::now();court.court.secondsBudget=budget;
  if(!court.court.build(6)){std::cout<<"P9_HOLD_BUILD\n";return 2;}
  court.project();court.prepareEdges();
  if(court.court.goal.size()!=8240087||court.c6.size()!=1405068||
     court.c7.size()!=6807696||court.edge6.size()!=7672278)
   throw std::runtime_error("original B6/C6/C7/E6 state counts drift");
  const auto full=goalDigest(court.court,6,prefix+"-B6.bin");
  if(full!="82fe545bcad3537c989ec22afce9d286926ddce5f4ef9428c0307951ec2d0979")
   throw std::runtime_error("original B6 goal differs from prior P8 gold SHA");
  writeTurns(prefix+"-turns.bin");
  writeProjection("C6",court.c6,prefix);
  writeProjection("C7",court.c7,prefix);
  writeProjection("E6",court.edge6,prefix);
  std::cout<<"P9_PROJECTIONS_COMPLETE GOAL_SHA256 "<<full
    <<" MOVE_TABLE_BYTES 288 FULL_GOAL_KEYS "<<court.court.goal.size()
    <<" CORNER_C6 "<<court.c6.size()<<" CORNER_C7 "<<court.c7.size()
    <<" EDGE_E6 "<<court.edge6.size()
    <<" SOURCE_PILOT "<<(mode=="pilot"?1:0)
    <<" PEAK_RSS_KIB "<<rssKiB()<<"\n"<<std::flush;
  if(mode=="pilot"){
   // Both prefixes start at previously UNPROVED first-action B10
   // cylinders, unlike P8's already-certified first U/D.
   const std::vector<std::vector<int>> sample={{3,0},{12,0}};
   for(int i=0;i<int(sample.size());i++){
    const auto&p=sample[i];
    if(p[0]==0||p[0]==9||!canonical(p[0],p[1]))
     throw std::runtime_error("pilot overlaps previously proven first action or illegal grammar");
    Cube x=source;
    for(int a:p)x=composeCube(x,turn[a]);
    court.visits=0;court.skippedChildren=0;court.orderedPairChecks=0;
    court.edgePackedChecks=0;court.fullQueries=0;court.fullHits=0;court.cut=false;
    auto started=std::chrono::steady_clock::now();
    for(int lim=2;lim<=10;lim++){
     court.path=p;
     if(court.fastVisit(x,2,lim,p.back())){
      std::cout<<"P9_TRUE_FULL_CUBIE_MEET PREFIX "<<p[0]<<" "<<p[1]
        <<" ABSENCE_CERT_WITHHELD 1\n";return 3;
     }
     if(court.cut||court.court.expired()){
      std::cout<<"P9_RESOURCE_HOLD_PREFIX "<<p[0]<<" "<<p[1]<<"\n";return 2;
     }
    }
    auto wordMass=p8Weight(p.back(),8);
    if(court.visits+court.skippedChildren!=wordMass||court.fullHits!=0)
     throw std::runtime_error("source B10 ordered action language not fully accounted");
    const FullKey k=exactKey(x);
    double ms=std::chrono::duration<double,std::milli>(
      std::chrono::steady_clock::now()-started).count();
    std::cout<<"P9_OPEN_B10_PILOT CASE "<<i+1<<" FIRST "<<p[0]<<" SECOND "<<p[1]
      <<" SOURCE_KEY_C "<<k.c<<" SOURCE_KEY_E "<<k.e
      <<" WORD_CALLS "<<wordMass<<" VISITED "<<court.visits<<" OMITTED "<<court.skippedChildren
      <<" PAIRS "<<court.orderedPairChecks<<" EDGES "<<court.edgePackedChecks
      <<" FULL_QUERIES "<<court.fullQueries
      <<" SEARCH_MS "<<std::fixed<<std::setprecision(3)<<ms
      <<" TRUE_FULL_CUBIE_HITS 0 COMPLETE_LOCAL_B10 1"
      <<" GOAL_SHA256 "<<full<<" GLOBAL_B10_COMPLETE 0\n"<<std::flush;
   }
   if(goalDigest(court.court,6,"")!=full)throw std::runtime_error("source mutated entire original B6 goal");
  }
  double elapsed=std::chrono::duration<double,std::milli>(
    std::chrono::steady_clock::now()-start).count();
  std::cout<<"P9_COMPLETE MODE "<<mode<<" GOAL_SHA256 "<<full
    <<" TARGET_IMMUTABLE "<<(goalDigest(court.court,6,"")==full?1:0)
    <<" PILOT_PREFIXES "<<(mode=="pilot"?2:0)
    <<" GLOBAL_B10_COMPLETE 0 LOWER17_CLAIMED 0"
    <<" WALL_MS "<<std::fixed<<std::setprecision(3)<<elapsed
    <<" PEAK_RSS_KIB "<<rssKiB()<<"\n"<<std::flush;
  return 0;
 }catch(const std::exception&e){std::cerr<<"P9_ERROR "<<e.what()<<"\n";return 4;}
}
#endif // CUBEREV_P9_AS_LIBRARY
