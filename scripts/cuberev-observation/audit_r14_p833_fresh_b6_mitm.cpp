// CUBE-REV R14-P8.33: fresh executable reconstruction of the B6 41-target
// length-12 exclusion using independently generated 48-sticker factor data.
// No import of the historic verify_b6_41_mitm_p48.cpp acceptance routine.
// Inputs: generated b6_factor_table.hpp and targets41.txt. Output: 41 verdicts.
// This proves >=13 only for the supplied 41 candidate goal representatives.
// Source-bytes generation, 41-class completeness, and the word-normal-form
// argument remain separate proof dependencies.
#include <array>
#include <cstdint>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <unordered_set>
#include <vector>
#include "b6_factor_table.hpp"
using namespace std;
struct State {
 uint64_t edges=0,corners=0;
 bool operator==(const State& z) const noexcept {
  return edges==z.edges&&corners==z.corners;
 }
};
struct StateHash {
 size_t operator()(const State& s) const noexcept {
  uint64_t h=s.edges*0x9e3779b97f4a7c15ull ^ s.corners;
  h^=h>>30;h*=0xbf58476d1ce4e5b9ull;
  h^=h>>27;h*=0x94d049bb133111ebull;
  return (size_t)(h^(h>>31));
 }
};
State pack(const array<int,20>& a){
 State s;
 for(int i=0;i<12;i++)s.edges|=uint64_t(a[i])<<(5*i);
 for(int i=0;i<8;i++)s.corners|=uint64_t(a[12+i])<<(5*i);
 return s;
}
State turn(State a,int m){
 State z;
 for(int i=0;i<12;i++)
  z.edges|=uint64_t(TABLE[m][i][(a.edges>>(5*i))&31])<<(5*i);
 for(int i=0;i<8;i++)
  z.corners|=uint64_t(TABLE[m][i+12][(a.corners>>(5*i))&31])<<(5*i);
 return z;
}
bool admissible(int a,int prior){
 if(prior<0)return true;
 int f=a/3;
 return f!=prior && !(abs(f-prior)==3&&f<prior);
}
unordered_set<State,StateHash> ball;
uint64_t expanded=0,probes=0;
void grow(State s,int d,int prior){
 ++expanded;ball.insert(s);
 if(d==6)return;
 for(int a=0;a<18;a++)if(admissible(a,prior))grow(turn(s,a),d+1,a/3);
}
bool intersects(State s,int d,int prior){
 ++probes;
 if(ball.count(s))return true;
 if(d==6)return false;
 for(int a=0;a<18;a++)if(admissible(a,prior))
  if(intersects(turn(s,a),d+1,a/3))return true;
 return false;
}
int main(int argc,char**argv){
 if(argc!=2){cerr<<"usage: audit_b6_41_fresh_mitm targets41.txt\n";return 2;}
 // The 18 local actions must form six inverse/half-turn triples on all
 // twenty 24-valued original-cubie factors. This detects column corruption.
 for(int a=0;a<18;a++)for(int i=0;i<20;i++){
  array<bool,24> seen{};
  for(int x=0;x<24;x++){int v=TABLE[a][i][x];
   if(v<0||v>=24||seen[v])return 11;seen[v]=true;}
 }
 for(int f=0;f<6;f++)for(int i=0;i<20;i++)for(int x=0;x<24;x++){
  int q=TABLE[3*f][i][x];
  if(TABLE[3*f][i][TABLE[3*f+1][i][x]]!=x)return 12;
  if(TABLE[3*f][i][q]!=TABLE[3*f+2][i][x])return 13;
 }
 ifstream input(argv[1]);if(!input)return 14;
 vector<State> targets;string line;int expected=0;
 while(getline(input,line)){
  if(line.empty()||line.front()=='#')continue;
  istringstream ss(line);int id;ss>>id;if(!ss||id!=expected++)return 15;
  array<int,20> vals;
  for(int& x:vals){ss>>x;if(!ss||x<0||x>=24)return 16;}
  string extra;if(ss>>extra)return 17;
  targets.push_back(pack(vals));
 }
 if(targets.size()!=41)return 18;
 array<int,20> init;for(int i=0;i<20;i++)init[i]=START[i];
 State solved=pack(init);
 ball.max_load_factor(.78f);ball.reserve(8500000);
 grow(solved,0,-1);
 cout<<"FRESH_B6_BALL generated="<<expanded
     <<" unique="<<ball.size()<<"\n"<<flush;
 if(expanded!=8331112||ball.size()!=8240087)return 19;
 if(!ball.count(solved))return 20;
 for(int m=0;m<18;m++)if(!ball.count(turn(solved,m)))return 21;
 int passed=0;
 for(int id=0;id<41;id++){
  if(targets[id]==solved)return 22;
  probes=0;bool found=intersects(targets[id],0,-1);
  cout<<"FRESH_TARGET "<<id<<" collision="<<(found?1:0)
      <<" probes="<<probes<<"\n"<<flush;
  if(found||probes!=8331112)return 23;
  passed++;
 }
 cout<<"FRESH_REPLAY_ALL_41_PASS "<<passed<<"\n"<<flush;
 return 0;
}
