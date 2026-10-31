// CUBE-REV 0.28: certify NO pure-two-edge support at radius six.
// Generate b6_factor_table.hpp with make_b6_factor_table.py.
// Compile: g++ -O3 -std=c++17 -I . /path/to/verify_b6_no_two_edge.cpp -o verify_b6_no_two_edge
// Run: for i in $(seq 1 11); do ./verify_b6_no_two_edge "$i"; done
// Each run deletes original edge tag #0 and tag #i and checks injection
// of all B6 full physical states onto the remaining 18 complete cubie factors.
// Edge transitivity under cube rotations then excludes EVERY two-edge support.
#include <bits/stdc++.h>
#include "b6_factor_table.hpp"
using namespace std;
struct Key {uint64_t a,b; bool operator==(const Key& t)const{return a==t.a&&b==t.b;}};
struct Hash {size_t operator()(Key const& k)const{return (k.a*0x9e3779b97f4a7c15ULL)^(k.b*0xbf58476d1ce4e5b9ULL);}};
constexpr uint32_t P18[7]={1,18,324,5832,104976,1889568,34012224};
uint8_t states[7][20];uint32_t mask;
unordered_map<Key,uint32_t,Hash> seen;
bool hit=false;uint64_t nseen=0;
Key projection(int d) {
    Key k{0,0};int n=0;
    for(int i=0;i<20;i++)if((mask>>i)&1){
        uint64_t x=states[d][i];
        if(n<12)k.a|=x<<(5*n);
        else k.b|=x<<(5*(n-12));
        ++n;
    }
    assert(n==18);return k;
}
bool identical(uint32_t packed,int d) {
    int steps=packed%7;uint32_t code=packed/7;
    uint8_t s[20];for(int i=0;i<20;i++)s[i]=START[i];
    for(int j=0;j<steps;j++){
        int a=code%18;code/=18;
        for(int i=0;i<20;i++)s[i]=TABLE[a][i][s[i]];
    }
    for(int i=0;i<20;i++)if(s[i]!=states[d][i])return false;
    return true;
}
void visit(int d,int prev,uint32_t code){
    if(hit)return;
    Key k=projection(d);uint32_t packed=code*7+d;
    auto [it,added]=seen.emplace(k,packed);
    if(!added){
        if(!identical(it->second,d)){hit=true;return;}
        if(int(it->second%7)<=d)return;
        it->second=packed; // MUST revisit if a shorter route arrived later
    }else nseen++;
    if(d==6)return;
    for(int a=0;a<18;a++){
        int face=a/3;
        if(face==prev)continue;
        if(prev>=0&&abs(face-prev)==3&&face<prev)continue;
        for(int i=0;i<20;i++)states[d+1][i]=TABLE[a][i][states[d][i]];
        visit(d+1,face,code+a*P18[d]);
        if(hit)return;
    }
}
int main(int argc,char**argv){
    if(argc!=2)return 2;
    int other=atoi(argv[1]);
    if(other<1||other>11)return 2;
    mask=((1u<<20)-1)^((1u<<0)|(1u<<other));
    assert(__builtin_popcount(mask)==18);
    for(int i=0;i<20;i++)states[0][i]=START[i];
    seen.max_load_factor(.8);seen.reserve(10000000);
    visit(0,-1,0);
    cout<<"omit_edge_pair {0,"<<other<<"}: distinct projected "<<nseen
        <<", collision "<<hit<<"\n";
    if(hit||nseen!=8240087)return 1;
    return 0;
}
