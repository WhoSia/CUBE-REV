// CUBE-REV 0.20: independently enumerate real five-turn observation partitions.
// Requires original frozen sticker-derived 18x24 oriented-edge move table; NO invented maps.
// Build: c++ -std=c++20 -O3 -Wall -Wextra -pedantic scripts/cuberev-020/census-L5-transport-cuts.cpp -o /tmp/cube020-census
// Run: /tmp/cube020-census ORIGINAL_MOVE_MAPS.txt [canonical_partition_keys.txt]
// Then independently compare against original_L5_partitions.tsv with verify-L5-census-source.py.
#include <array>
#include <algorithm>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <set>
#include <stdexcept>
#include <string>
constexpr int N=12, A=18, L=5;
using Maps=std::array<std::array<unsigned char,24>,A>;
struct Stats {
 uint64_t words=0, ge5=0, ge7=0; int max_rank=0;
 std::array<uint64_t,13> rank_count{};
 std::set<uint64_t> partitions, rank7_partitions;
};
Maps load(const std::string& file) {
 std::ifstream in(file); if(!in)throw std::runtime_error("Missing physical 18x24 map file");
 Maps m{};
 for(int a=0;a<A;a++) {
  std::array<bool,24> seen{};
  for(int v=0;v<24;v++) {
   int x=-1; if(!(in>>x)||x<0||x>=24||seen[x])throw std::runtime_error("Invalid bijection");
   seen[x]=true; m[a][v]=x;
  }
  for(int p=0;p<N;p++){
   int even=m[a][p*2], odd=m[a][p*2+1];
   if(even/2!=odd/2 || (even%2)==(odd%2))throw std::runtime_error("Orientation contract violated");
  }
 }
 int extra; if(in>>extra)throw std::runtime_error("Unexpected map entries");
 return m;
}
uint64_t key_of(const std::array<uint16_t,N>& history,int& rank){
 std::array<uint16_t,N> encountered{}; rank=0; uint64_t key=0;
 for(int s=0;s<N;s++) {
  int label=0;
  for(;label<rank;label++)if(encountered[label]==history[s])break;
  if(label==rank)encountered[rank++]=history[s];
  key|=uint64_t(label) << (4*s);
 }
 return key;
}
struct Census {
 const Maps& maps; std::array<Stats,L+1> stats{}; std::set<uint64_t> all{};
 void visit(int depth,int q,std::array<unsigned char,N> pos,std::array<uint16_t,N> history){
  if(depth==L){
   int rank;uint64_t key=key_of(history,rank);auto& t=stats[q];
   t.words++;t.max_rank=std::max(t.max_rank,rank);t.rank_count[rank]++;
   t.ge5+=rank>=5;t.ge7+=rank>=7;t.partitions.insert(key);
   if(rank==7)t.rank7_partitions.insert(key);
   all.insert(key);return;
  }
  for(int a=0;a<A;a++) {
   auto p=pos;auto h=history;
   for(int s=0;s<N;s++){
    p[s]=maps[a][p[s]];
    h[s]=static_cast<uint16_t>((h[s]<<1) | (p[s]&1));
   }
   bool flips=false;
   for(int j=0;j<N;j++)if(maps[a][j*2]&1){flips=true;break;}
   visit(depth+1,q+flips,p,h);
  }
 }
 void run(){std::array<unsigned char,N> pos{};std::array<uint16_t,N> histories{};
  for(int i=0;i<N;i++) {
   pos[i]=2*i;
  }
  visit(0,0,pos,histories);
 }
};
int main(int argc,char** argv){
 try {
  if(argc!=2 && argc!=3)throw std::runtime_error("Usage: census maps.txt [partition_keys.txt]");
  Maps maps=load(argv[1]);Census z{maps};z.run();
  if(argc==3){std::ofstream o(argv[2]);if(!o)throw std::runtime_error("Cannot write output");
   for(auto key:z.all)o<<key<<'\n';}
  uint64_t sum=0;size_t overlap=0;
  for(auto key:z.stats[3].rank7_partitions)overlap+=z.stats[4].rank7_partitions.count(key);
  std::cout<<"{\n  \"schema\": \"cube-rev.020.L5-action-transport-census-v1\",\n";
  std::cout<<"  \"evidence\": \"independent physical map enumeration, compare with P13 TSV separately\",\n";
  std::cout<<"  \"source_sha256_expected\": \"9f2119738f92f56485897c1894d2cb721a3d6b0498c5aa14832c71f18b20e2f1\",\n";
  std::cout<<"  \"unique_partitions_all\": "<<z.all.size()<<",\n";
  std::cout<<"  \"by_informative_action_count\": [\n";
  for(int q=0;q<=L;q++){
   const auto& t=z.stats[q];sum+=t.words;
   std::cout<<"    {\"q\": "<<q<<", \"words\": "<<t.words
    <<", \"max_rank\": "<<t.max_rank<<", \"rank_at_least_five\": "<<t.ge5
    <<", \"rank_seven\": "<<t.ge7<<", \"distinct_partitions\": "<<t.partitions.size()
    <<", \"rank7_unique_partitions\": "<<t.rank7_partitions.size()<<", \"rank_histogram\": [";
   for(int r=0;r<=N;r++){if(r)std::cout<<", ";std::cout<<t.rank_count[r];}
   std::cout<<"]}"<<(q==L?"\n":",\n");
  }
  std::cout<<"  ],\n  \"rank7_partition_overlap_q3_q4\": "<<overlap
   <<",\n  \"physical_words_enumerated\": "<<sum<<"\n}\n";
  if(sum!=1889568 || z.all.size()!=14938 || z.stats[3].rank7_partitions.size()!=16
   || z.stats[4].rank7_partitions.size()!=16 || overlap!=0)return 2;
 }catch(const std::exception& e){std::cerr<<e.what()<<'\n';return 1;}
}
