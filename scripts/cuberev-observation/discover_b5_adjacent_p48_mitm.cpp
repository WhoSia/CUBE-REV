// P48 B5 two-sided physical 18-HTM witness rediscovery.
// Generate b6_factor_table.hpp and b5_adjacent_candidate_goals121.txt using
// b6_independent_48sticker_goals.py and emit_b5_adjacent_p48_discovery_goals.py.
// No archived 54-facelet engine, B5 word oracle or B5 negative verdict is used.
// Exact B5 solved ball 621649; search each target to depth five.
// Print TWO actual words of length <=5, independently rechecked by Python P48.
#include <cstdint>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <unordered_map>
#include "b6_factor_table.hpp"
using namespace std;
struct State {
  uint64_t edges,corners;
  bool operator==(State const& x)const noexcept {
    return edges==x.edges&&corners==x.corners;
  }
};
struct Hash {
  size_t operator()(State s) const noexcept {
    uint64_t x=s.edges^(s.corners*0x9e3779b97f4a7c15ULL);
    x^=x>>30;x*=0xbf58476d1ce4e5b9ULL;
    x^=x>>27;x*=0x94d049bb133111ebULL;
    return size_t(x^(x>>31));
  }
};
State pack(uint8_t const s[20]){
  State z{0,0};
  for(int i=0;i<12;i++)z.edges|=uint64_t(s[i])<<(5*i);
  for(int i=12;i<20;i++)z.corners|=uint64_t(s[i])<<(5*(i-12));
  return z;
}
State move(State s,int a){
  State z{0,0};
  for(int i=0;i<12;i++)
    z.edges|=uint64_t(TABLE[a][i][(s.edges>>(5*i))&31])<<(5*i);
  for(int i=12;i<20;i++)
    z.corners|=uint64_t(TABLE[a][i][(s.corners>>(5*(i-12)))&31])<<(5*(i-12));
  return z;
}
struct Path{uint32_t encoded;uint8_t depth;};
unordered_map<State,Path,Hash> ball;
uint64_t generated=0,probed=0;
void build(State s,int depth,int previous,uint32_t w){
  ++generated;
  ball.emplace(s,Path{w,(uint8_t)depth});
  if(depth==5)return;
  for(int a=0;a<18;a++){
    int f=a/3;
    if(f==previous||(previous>=0&&abs(f-previous)==3&&f<previous))continue;
    build(move(s,a),depth+1,f,w|(uint32_t(a)<<(5*depth)));
  }
}
static const char* TOKEN[18]={
  "U","U'","U2","R","R'","R2","F","F'","F2",
  "D","D'","D2","L","L'","L2","B","B'","B2"
};
string decode(uint32_t w,int d){
  string result;
  for(int i=0;i<d;i++){
    if(i)result+=' ';
    result+=TOKEN[(w>>(5*i))&31];
  }
  return result;
}
bool query(State s,int depth,int prev,uint32_t w,string &left,string &right){
  ++probed;
  auto it=ball.find(s);
  if(it!=ball.end()){
    // Q*goal=P, so goal=Q^-1*P. Actual B5 endpoints Q and P
    // differ on precisely the goal's original oriented cubie support.
    left=decode(w,depth);
    right=decode(it->second.encoded,it->second.depth);
    return true;
  }
  if(depth==5)return false;
  for(int a=0;a<18;a++){
    int f=a/3;
    if(f==prev||(prev>=0&&abs(f-prev)==3&&f<prev))continue;
    if(query(move(s,a),depth+1,f,w|(uint32_t(a)<<(5*depth)),left,right))
      return true;
  }
  return false;
}
int main(int argc,char**argv){
  if(argc!=2){cerr<<"usage: p48_b5_discovery goals121.txt\n";return 2;}
  ball.max_load_factor(.78);
  ball.reserve(630000);
  build(pack(START),0,-1,0);
  cout<<"P48_B5_BUILD normalized="<<generated<<" unique="<<ball.size()<<'\n'<<flush;
  if(ball.size()!=621649)return 3;
  ifstream in(argv[1]);
  if(!in)return 4;
  int row=0;string line;int hits[11]={};
  while(getline(in,line)){
    if(line.empty()||line[0]=='#')continue;
    istringstream ss(line);int core;ss>>core;
    uint8_t v[20];
    for(auto &x:v){
      int n;ss>>n;
      if(!ss||n<0||n>=24)return 5;
      x=(uint8_t)n;
    }
    string extra;if(ss>>extra)return 5;
    if(core!=row/11||core<0||core>=11)return 6;
    string left,right;
    probed=0;
    bool hit=query(pack(v),0,-1,0,left,right);
    if(hit){
      ++hits[core];
      cout<<"WITNESS "<<core<<" "<<row%11<<" | "<<left
          <<" | "<<right<<" | "<<probed<<'\n'<<flush;
    }
    ++row;
  }
  if(row!=121)return 7;
  int total=0;
  for(int i=0;i<11;i++){
    cout<<"ORBIT "<<i<<" hits="<<hits[i]<<'\n';
    total+=hits[i]>0;
  }
  cout<<"DONE positive_orbits="<<total<<" of=11\n";
  return total==9?0:8;
}
