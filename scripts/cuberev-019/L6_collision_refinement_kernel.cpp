/** CUBE-REV 0.19 P6: sound collision-edge refinement kernel.
 * INPUT: subset of physically replayed 6-HTM partitions with q=3..5
 * flip actions and rank>=5, each row "12-slot partition signature; six move ids".
 * This is NOT an all-physical-L6 UNSAT proof: lower-rank words and other q
 * classes must be shown redundant before claiming exact k3 infeasibility.
 * A word f dominates word g if B(f) ⊆ B(g), where B is its graph of
 * equal-observation initial position pairs. Checkable independent of source R.
 */
#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <tuple>
#include <vector>
using namespace std;
struct Candidate {
 uint64_t collision_lo, collision_hi, partition;
 int collision_edges;
 array<int,6> moves;
};
int main(int argc,char**argv){
 if(argc!=4){cerr<<"usage: P6-collision-kernel candidates.tsv retained.tsv witnesses.tsv\n";return 2;}
 ifstream input(argv[1]);assert(input);
 int pair_id[12][12]={},pair_index=0;
 for(int i=0;i<12;i++)for(int j=i+1;j<12;j++)pair_id[i][j]=pair_index++;
 assert(pair_index==66);
 vector<Candidate> words;
 uint64_t partition;array<int,6> moves;
 while(input>>partition>>moves[0]>>moves[1]>>moves[2]>>moves[3]>>moves[4]>>moves[5]){
  int label[12];
  for(int i=0;i<12;i++)label[i]=(partition>>(4*i))&15;
  uint64_t lo=0,hi=0;
  for(int i=0;i<12;i++)for(int j=i+1;j<12;j++)
   if(label[i]==label[j]){
    auto e=pair_id[i][j];if(e<64)lo|=uint64_t(1)<<e;else hi|=uint64_t(1)<<(e-64);
   }
  words.push_back({lo,hi,partition,__builtin_popcountll(lo)+__builtin_popcountll(hi),moves});
 }
 assert(words.size()==53528);
 sort(words.begin(),words.end(),[](const auto &a,const auto &b){
  return make_tuple(a.collision_edges,a.collision_lo,a.collision_hi)
       < make_tuple(b.collision_edges,b.collision_lo,b.collision_hi);
 });
 vector<Candidate> keep;vector<pair<uint64_t,uint64_t>> witnesses;map<int,pair<int,int>> counts;
 for(const auto &word:words){
  bool dominated=false;uint64_t parent=word.partition;
  for(const auto &retained:keep){
   if(retained.collision_edges>word.collision_edges)break;
   if((retained.collision_lo & ~word.collision_lo)==0
      && (retained.collision_hi & ~word.collision_hi)==0){
    dominated=true;parent=retained.partition;break;
   }
  }
  witnesses.push_back({word.partition,parent});
  counts[word.collision_edges].first++;
  if(!dominated){keep.push_back(word);counts[word.collision_edges].second++;}
 }
 assert(keep.size()==18813);
 ofstream output(argv[2]);assert(output);
 for(auto &c:keep){output<<c.partition;for(int a:c.moves)output<<" "<<a;output<<"\n";}
 ofstream cert(argv[3]);assert(cert);
 for(auto [source,parent]:witnesses)cert<<source<<" "<<parent<<"\n";
 cout<<"CUBE_REV_019_L6_COLLISION_EDGE_REFINEMENT_53528_TO_18813_PASS\n";
 for(auto [degree,ct]:counts)
  cout<<"collisionEdges="<<degree<<" source="<<ct.first<<" retained="<<ct.second<<"\n";
}
