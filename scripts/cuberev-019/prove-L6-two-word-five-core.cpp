/** CUBE-REV 0.19 P7. Exact two-word 480-five-source impossibility gate.
 * Source input: 1192 integer masks from original 0.18 physical.json.
 * Partition input: every physical L6 output partition of rank>=5.
 * No numerical LP or heuristic. Uses bitsets over all 53528 candidates.
 */
#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <vector>
using namespace std;
int main(int argc,char**argv){
 assert(argc==3);
 ifstream source_file(argv[1]),partitions_file(argv[2]);
 assert(source_file&&partitions_file);
 vector<int> five;int m,nsource=0;
 while(source_file>>m){
  assert(m>=0&&m<4096);
  if(__builtin_popcount(m)==5)five.push_back(m);
  nsource++;
 }
 assert(nsource==1192&&five.size()==480);
 vector<uint64_t> candidates;uint64_t z;int w[6];
 while(partitions_file>>z>>w[0]>>w[1]>>w[2]>>w[3]>>w[4]>>w[5])
  candidates.push_back(z);
 size_t N=candidates.size();assert(N==53528);
 size_t blocks=(N+63)/64;
 vector<vector<uint64_t>> good(five.size(),vector<uint64_t>(blocks));
 vector<vector<int>> uncovered(N);
 for(size_t j=0;j<N;j++){
  uint8_t label[12];
  for(int p=0;p<12;p++)label[p]=(candidates[j]>>(4*p))&15;
  for(size_t r=0;r<five.size();r++){
   int src=five[r];uint16_t seen=0;bool injective=true;
   for(int p=0;p<12;p++)if(src&(1<<p)){
    uint16_t bit=uint16_t(1)<<label[p];
    if(seen&bit){injective=false;break;}
    seen|=bit;
   }
   if(injective)good[r][j/64]|=1ull<<(j%64);
   else uncovered[j].push_back((int)r);
  }
 }
 uint64_t checks=0;
 vector<uint64_t> other(blocks);
 for(size_t j=0;j<N;j++){
  fill(other.begin(),other.end(),~0ull);
  bool empty=false;
  for(int r:uncovered[j]){
   checks++;bool nonzero=false;
   for(size_t p=0;p<blocks;p++)if((other[p]&=good[r][p]))nonzero=true;
   if(!nonzero){empty=true;break;}
  }
  if(!empty){
   cerr<<"TWO_WORD_FIVE_SOURCE_COVER_POSSIBLE index="<<j<<"\n";
   return 1;
  }
 }
 assert(checks==1158155ULL);
 cout<<"CUBE_REV_019_L6_ALL_53528_PHYSICAL_RANK5_PAIR_FIVE_SOURCE_UNSAT_PASS "
     <<"candidate_partitions="<<N<<" five_sources="<<five.size()
     <<" intersected_rows="<<checks<<"\n";
}
