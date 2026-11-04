// Independent P48 B6 41-target exact 18-HTM MITM distance verifier.
// The included factor table is generated from original 48 labeled stickers;
// neither the 54-facelet archive nor its B6-positive verdict is an input.
// Compile: g++ -std=c++17 -O3 -I OUT verify_b6_41_mitm_p48.cpp -o mitm_p48
// Usage:   mitm_p48 OUT/targets41.txt START END  (0<=START<END<=41)
// Validates each target's distance >=13 only; not exact equality to 13.
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
  bool operator==(State const& x)const noexcept {
    return edges==x.edges&&corners==x.corners;
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
static inline State pack(uint8_t const s[20]) {
  State z{0,0};
  for(int i=0;i<12;i++)z.edges|=uint64_t(s[i])<<(5*i);
  for(int i=12;i<20;i++)z.corners|=uint64_t(s[i])<<(5*(i-12));
  return z;
}
static inline State move(State s,int a) {
  State z{0,0};
  for(int i=0;i<12;i++)
    z.edges|=uint64_t(TABLE[a][i][(s.edges>>(5*i))&31])<<(5*i);
  for(int i=12;i<20;i++)
    z.corners|=uint64_t(TABLE[a][i][(s.corners>>(5*(i-12)))&31])<<(5*(i-12));
  return z;
}
static unordered_set<State,Hash> ball;
static uint64_t generated=0,probed=0;
static bool intersection=false;
// HTM normal form: same-face adjacent moves combine or cancel.
// Opposite-face moves commute and are written in increasing face order.
// Every HTM word has such a representative with no increased length.
static void build(State s,int depth,int prev) {
  ++generated;ball.insert(s);
  if(depth==6)return;
  for(int a=0;a<18;a++) {
    int f=a/3;
    if(f==prev||(prev>=0&&abs(f-prev)==3&&f<prev))continue;
    build(move(s,a),depth+1,f);
  }
}
static void query(State s,int depth,int prev) {
  if(intersection)return;
  ++probed;
  if(ball.find(s)!=ball.end()){intersection=true;return;}
  if(depth==6)return;
  for(int a=0;a<18;a++) {
    int f=a/3;
    if(f==prev||(prev>=0&&abs(f-prev)==3&&f<prev))continue;
    query(move(s,a),depth+1,f);
    if(intersection)return;
  }
}
int main(int argc,char**argv) {
  if(argc!=4){cerr<<"usage: mitm_p48 targets41.txt START END\n";return 2;}
  const int first=atoi(argv[2]),last=atoi(argv[3]);
  if(first<0||last>41||first>=last){cerr<<"bad target range\n";return 2;}
  ifstream in(argv[1]);
  if(!in){cerr<<"missing target list\n";return 2;}
  ball.max_load_factor(.82);
  ball.reserve(8241000);
  State solved=pack(START);
  build(solved,0,-1);
  cout<<"P48_B6 generated="<<generated<<" unique="<<ball.size()<<'\n'<<flush;
  if(generated!=8331112||ball.size()!=8240087){
    cerr<<"P48 ball mismatch\n";return 3;
  }
  if(!ball.count(move(solved,0))){
    cerr<<"one-move positive control failed\n";return 3;
  }
  string line;int expected=0,count=0;uint64_t total=0;
  while(getline(in,line)) {
    if(line.empty()||line[0]=='#')continue;
    istringstream ss(line);int id;ss>>id;
    if(!ss||id!=expected++){cerr<<"wrong goal ID\n";return 4;}
    uint8_t values[20];
    for(auto &v:values) {
      int x;ss>>x;
      if(!ss||x<0||x>=24){cerr<<"bad factor\n";return 4;}
      v=uint8_t(x);
    }
    string extra;if(ss>>extra){cerr<<"unexpected goal data\n";return 4;}
    if(id<first||id>=last)continue;
    State goal=pack(values);
    if(goal==solved){cerr<<"identity target\n";return 4;}
    intersection=false;probed=0;
    query(goal,0,-1);
    if(intersection){cerr<<"FAIL: target="<<id<<" distance <=12\n";return 5;}
    if(probed!=8331112){cerr<<"incomplete target search\n";return 6;}
    cout<<"P48_PASS target="<<id<<" probes="<<probed<<" intersection=0\n"<<flush;
    total+=probed;count++;
    if(count==last-first) {
      cout<<"P48_CERTIFIED range="<<first<<":"<<last
          <<" targets="<<count<<" probes="<<total<<'\n'<<flush;
      return 0;
    }
  }
  cerr<<"incomplete target manifest\n";return 7;
}
