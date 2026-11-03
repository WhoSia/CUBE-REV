// Exact independent 18-HTM radius-6 meet-in-the-middle certificate.
// Build with b6_factor_table.hpp generated from sealed independent_b4.py:
// g++ -O3 -std=c++17 -I OUTPUT verify_b6_41_mitm.cpp -o mitm41
// Then: mitm41 OUTPUT/targets41.txt 0 8 ; 8 16 ; 16 24 ; 24 32 ; 32 41
// No historical B6-positive sensor oracle or selected-tag projections used.
#include <cstdint>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <unordered_set>
#include "b6_factor_table.hpp"
using namespace std;
struct State {
  uint64_t edges,corners;
  bool operator==(const State& y)const noexcept {
    return edges==y.edges && corners==y.corners;
  }
};
struct Hash {
  size_t operator()(State s)const noexcept {
    uint64_t x=s.edges^(s.corners*0x9e3779b97f4a7c15ULL);
    x^=x>>30;x*=0xbf58476d1ce4e5b9ULL;
    x^=x>>27;x*=0x94d049bb133111ebULL;
    return size_t(x^(x>>31));
  }
};
static inline State pack(const uint8_t s[20]) {
  State z{0,0};
  for(int i=0;i<12;i++)z.edges|=uint64_t(s[i])<<(5*i);
  for(int i=12;i<20;i++)z.corners|=uint64_t(s[i])<<(5*(i-12));
  return z;
}
static inline State move(State s,int a) {
  State z{0,0};
  for(int i=0;i<12;i++)z.edges|=uint64_t(TABLE[a][i][(s.edges>>(5*i))&31])<<(5*i);
  for(int i=12;i<20;i++)z.corners|=uint64_t(TABLE[a][i][(s.corners>>(5*(i-12)))&31])<<(5*(i-12));
  return z;
}
static unordered_set<State,Hash> ball;
static uint64_t generated=0,probed=0;
static bool intersection=false;
// Same-face successive turns collapse to <=1 HTM turn. Opposite-face
// turns commute and can be ordered by face index. Repeated swaps/reductions
// yield a normal-form word without increasing length. Hence the traversal
// still covers every cube state in the original 18-HTM radius-6 ball.
static void build(State s,int d,int prev) {
  generated++;
  ball.insert(s);
  if(d==6)return;
  for(int a=0;a<18;a++) {
    int f=a/3;
    if(f==prev || (prev>=0 && abs(f-prev)==3 && f<prev))continue;
    build(move(s,a),d+1,f);
  }
}
static void query(State s,int d,int prev) {
  if(intersection)return;
  probed++;
  if(ball.find(s)!=ball.end()){intersection=true;return;}
  if(d==6)return;
  for(int a=0;a<18;a++) {
    int f=a/3;
    if(f==prev || (prev>=0 && abs(f-prev)==3 && f<prev))continue;
    query(move(s,a),d+1,f);
    if(intersection)return;
  }
}
int main(int argc,char**argv) {
  if(argc!=4){cerr<<"usage: mitm41 targets41.txt START END\n";return 2;}
  const int first=atoi(argv[2]),last=atoi(argv[3]);
  if(first<0 || last>41 || first>=last){cerr<<"bad target range\n";return 2;}
  ifstream in(argv[1]);
  if(!in){cerr<<"missing target manifest\n";return 2;}
  ball.max_load_factor(.82);
  ball.reserve(8241000);
  const State solved=pack(START);
  build(solved,0,-1);
  cout<<"B6 generated="<<generated<<" unique="<<ball.size()<<'\n';
  if(generated!=8331112 || ball.size()!=8240087){
    cerr<<"cube ball size mismatch\n";return 3;
  }
  if(!ball.count(move(solved,0))){cerr<<"positive control failed\n";return 3;}
  string line;int count=0,expected_id=0;
  uint64_t total=0;
  while(getline(in,line)) {
    if(line.empty()||line[0]=='#')continue;
    istringstream ss(line);int id;ss>>id;
    if(!ss || id!=expected_id++){cerr<<"invalid target identifiers\n";return 4;}
    uint8_t v[20];
    for(int i=0;i<20;i++){
      int x;ss>>x;
      if(!ss || x<0 || x>=24){cerr<<"invalid goal factor\n";return 4;}
      v[i]=uint8_t(x);
    }
    string extra;
    if(ss>>extra){cerr<<"unexpected goal data\n";return 4;}
    if(id<first || id>=last)continue;
    const State goal=pack(v);
    if(goal==solved){cerr<<"identity is not a goal\n";return 4;}
    intersection=false;probed=0;
    query(goal,0,-1);
    if(intersection){cerr<<"FAIL goal "<<id<<" reachable <=12 HTM\n";return 5;}
    if(probed!=8331112){cerr<<"incomplete target-ball enumeration\n";return 6;}
    cout<<"PASS class="<<id<<" probes="<<probed<<" intersection=0\n";
    count++;total+=probed;
  }
  if(expected_id!=41 || count!=last-first){
    cerr<<"missing target rows\n";return 7;
  }
  cout<<"CERTIFIED range="<<first<<":"<<last<<" classes="<<count
      <<" probes="<<total<<" all distances >=13\n";
  return 0;
}
