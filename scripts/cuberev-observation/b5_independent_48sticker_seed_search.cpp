// Independent B5 physical 18-HTM state explorer for CUBE-REV 0.28.
// 48 individually labelled moving stickers, no historical cube library.
// BFS to B5; for each of 13 rotation-orbit representatives, find a pair
// differing only in the specified three ORIGINAL oriented edge cubies.
// The separate Python physical engine MUST replay and approve the JSON words.
// Build: g++ -std=c++17 -O3 b5_independent_48sticker_seed_search.cpp -o b5search
// Run: ./b5search (expects 621649 states and 13 FOUND word pairs).
#include <bits/stdc++.h>
using namespace std;
using V = array<int,3>;
using Bytes = array<uint8_t,48>;
struct Sticker { V p,n; };
struct State { Bytes original_to_slot; uint32_t parent; uint8_t move,depth; };
const string faces="URFDLB";
V normal(char f) {
  if(f=='U')return {0,1,0}; if(f=='R')return {1,0,0};
  if(f=='F')return {0,0,1}; if(f=='D')return {0,-1,0};
  if(f=='L')return {-1,0,0}; return {0,0,-1};
}
V rotate(V v,int axis,int k) {
  k=(k%4+4)%4;
  for(int t=0;t<k;t++) {
    int x=v[0],y=v[1],z=v[2];
    if(axis==0)v={x,-z,y};
    else if(axis==1)v={z,y,-x};
    else v={-y,x,z};
  }
  return v;
}
struct Hash {
  size_t operator()(Bytes const& b) const noexcept {
    uint64_t h=1469598103934665603ULL;
    for(uint8_t x:b){h^=x;h*=1099511628211ULL;}
    return h;
  }
};
int main() {
  vector<Sticker> stickers;
  map<array<int,6>,int> slot;
  for(int x=-1;x<=1;x++)for(int y=-1;y<=1;y++)for(int z=-1;z<=1;z++) {
    V p={x,y,z};
    int n=(x!=0)+(y!=0)+(z!=0);
    if(n!=2&&n!=3)continue;
    for(char f:faces) {
      V v=normal(f);
      if(inner_product(p.begin(),p.end(),v.begin(),0)!=1)continue;
      int i=(int)stickers.size();
      stickers.push_back({p,v});
      slot[{x,y,z,v[0],v[1],v[2]}]=i;
    }
  }
  if(stickers.size()!=48)throw runtime_error("bad sticker count");
  array<Bytes,18> moves;
  for(int f=0;f<6;f++) {
    V n=normal(faces[f]);
    int axis=0; while(n[axis]==0)axis++;
    int layer=n[axis];
    int sgn=(f==0||f==3||f==4||f==5)?1:-1; // U+,R-,F-,D+,L+,B+; matches independent physical oracle
    for(int kind=0;kind<3;kind++) {
      int pow=(kind==0)?1:(kind==1)?3:2;
      for(int i=0;i<48;i++) {
        V p=stickers[i].p, v=stickers[i].n;
        if(p[axis]==layer) {
          p=rotate(p,axis,pow*sgn);
          v=rotate(v,axis,pow*sgn);
        }
        moves[f*3+kind][i]=slot.at({
          p[0],p[1],p[2],v[0],v[1],v[2]
        });
      }
    }
  }
  State init{};
  iota(init.original_to_slot.begin(),init.original_to_slot.end(),0);
  init.parent=0; init.move=255; init.depth=0;
  vector<State> states;
  states.reserve(630000);
  states.push_back(init);
  unordered_map<Bytes,uint32_t,Hash> visited;
  visited.reserve(750000);
  visited.emplace(init.original_to_slot,0);
  array<size_t,6> level{};level[0]=1;
  for(size_t i=0;i<states.size();i++) {
    State a=states[i];
    if(a.depth==5)continue;
    for(int m=0;m<18;m++) {
      int f=m/3,prev=(a.move==255)?-1:a.move/3;
      if(prev==f)continue;
      // Opposite faces commute; retain one canonical ordering.
      if((prev==0&&f==3)||(prev==1&&f==4)||(prev==2&&f==5))
        continue;
      State b{};
      b.parent=(uint32_t)i;b.move=m;b.depth=a.depth+1;
      for(int j=0;j<48;j++)
        b.original_to_slot[j]=moves[m][a.original_to_slot[j]];
      if(visited.emplace(b.original_to_slot,(uint32_t)states.size()).second) {
        states.push_back(b);level[b.depth]++;
      }
    }
  }
  if(states.size()!=621649 || level!=array<size_t,6>{1,18,243,3240,43239,574908})
    throw runtime_error("wrong physical B5 state census");
  cerr<<"B5_BALL_PASS 621649\n";
  map<string,string> alias={
    {"DB","DB"},{"DL","DL"},{"FD","DF"},{"FL","FL"},
    {"LB","BL"},{"RB","BR"},{"RD","DR"},{"RF","FR"},
    {"UB","UB"},{"UF","UF"},{"UL","UL"},{"UR","UR"}
  };
  map<string,vector<int>> edge_original_stickers;
  for(int i=0;i<48;i++) {
    V p=stickers[i].p;
    if((p[0]!=0)+(p[1]!=0)+(p[2]!=0)!=2)continue;
    string raw;
    for(char f:faces) {
      V n=normal(f);
      if(inner_product(p.begin(),p.end(),n.begin(),0)==1)raw+=f;
    }
    edge_original_stickers[alias.at(raw)].push_back(i);
  }
  vector<string> edges={"UR","UF","UL","UB","DR","DF",
                        "DL","DB","FR","FL","BL","BR"};
  for(auto& e:edges)
    if(edge_original_stickers.at(e).size()!=2)
      throw runtime_error("incorrect original edge tag");
  map<V,int> to_edge;
  for(int i=0;i<12;i++) {
    V a=normal(edges[i][0]),b=normal(edges[i][1]);
    to_edge[{a[0]+b[0],a[1]+b[1],a[2]+b[2]}]=i;
  }
  vector<function<V(V)>> rotations;
  array<int,3> p={0,1,2};
  do {
    int inv=(p[0]>p[1])+(p[0]>p[2])+(p[1]>p[2]);
    for(int a:{-1,1})for(int b:{-1,1})for(int c:{-1,1})
      if(((inv%2)?-1:1)*a*b*c==1)
        rotations.push_back([p,a,b,c](V x)->V {
          return {a*x[p[0]],b*x[p[1]],c*x[p[2]]};
        });
  }while(next_permutation(p.begin(),p.end()));
  if(rotations.size()!=24)throw runtime_error("not 24 cube rotations");
  set<array<int,3>> unseen;
  for(int a=0;a<12;a++)for(int b=a+1;b<12;b++)for(int c=b+1;c<12;c++)
    unseen.insert({a,b,c});
  vector<pair<array<int,3>,size_t>> orbits;
  while(!unseen.empty()) {
    auto seed=*unseen.begin();
    set<array<int,3>> orbit;
    for(auto& rot:rotations) {
      array<int,3> transformed;
      for(int j=0;j<3;j++) {
        V a=normal(edges[seed[j]][0]),b=normal(edges[seed[j]][1]);
        transformed[j]=to_edge.at(rot({
          a[0]+b[0],a[1]+b[1],a[2]+b[2]
        }));
      }
      sort(transformed.begin(),transformed.end());
      orbit.insert(transformed);
    }
    for(auto triple:orbit)unseen.erase(triple);
    orbits.push_back({seed,orbit.size()});
  }
  if(orbits.size()!=13)throw runtime_error("wrong B5 edge orbit count");
  auto reconstruct=[&](uint32_t i) {
    vector<int> seq;
    while(i) {
      State s=states[i];seq.push_back(s.move);i=s.parent;
    }
    reverse(seq.begin(),seq.end());
    string result;
    for(int m:seq) {
      if(!result.empty())result+=" ";
      result+=faces[m/3];
      if(m%3==1)result+="'";
      if(m%3==2)result+="2";
    }
    return result;
  };
  for(size_t i=0;i<orbits.size();i++) {
    auto [triple,count]=orbits[i];
    array<bool,48> omit{};
    for(int e:triple)
      for(int sticker:edge_original_stickers.at(edges[e]))omit[sticker]=true;
    unordered_map<Bytes,uint32_t,Hash> signatures;
    signatures.reserve(750000);
    int first=-1,second=-1;
    for(uint32_t k=0;k<states.size();k++) {
      Bytes sig=states[k].original_to_slot;
      for(int j=0;j<48;j++)if(omit[j])sig[j]=255;
      auto [it,inserted]=signatures.emplace(sig,k);
      if(!inserted){first=(int)it->second;second=(int)k;break;}
    }
    if(first<0)throw runtime_error("physical B5 witness not found");
    cout<<"ORBIT "<<i<<" size="<<count<<" triple="
        <<edges[triple[0]]<<","<<edges[triple[1]]<<","<<edges[triple[2]]
        <<" FOUND left=\""<<reconstruct(first)
        <<"\" right=\""<<reconstruct(second)<<"\"\n";
  }
}
