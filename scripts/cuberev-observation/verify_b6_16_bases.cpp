// CUBE-REV 0.28: exhaustive B6 factor-injectivity search, 27 orbit representatives.
// Generate headers using make_b6_factor_table.py on the provenance-checked B1-B5 ZIP.
// Compile: g++ -O3 -std=c++17 verify_b6_16_bases.cpp -o verify_b6_16_bases
// Execute: ./verify_b6_16_bases 0 [through 26]. No claim of remote CI.
#include <bits/stdc++.h>
#include "b6_factor_table.hpp"
#include "b6_candidate_reps.hpp"
using namespace std;
struct Key {
    uint64_t lo,hi;
    bool operator==(Key const& o) const {return lo==o.lo && hi==o.hi;}
};
struct Hash {
    size_t operator()(Key const& k) const {
        return (k.lo*0x9e3779b97f4a7c15ULL)^(k.hi*0xbf58476d1ce4e5b9ULL);
    }
};
static constexpr uint32_t P18[7]={1,18,324,5832,104976,1889568,34012224};
uint8_t states[7][20];
uint32_t mask;
unordered_map<Key,uint32_t,Hash> observed;
uint64_t nseen=0;
bool collision=false;
int representative=0;

Key projection(int depth) {
    Key key{0,0}; int n=0;
    for(int i=0;i<20;i++) if((mask>>i)&1) {
        uint64_t v=states[depth][i];
        if(n<12)key.lo|=v<<(5*n);
        else key.hi|=v<<(5*(n-12));
        n++;
    }
    assert(n==16);
    return key;
}
bool same_full_state(uint32_t stored,int depth) {
    int k=stored%7;
    uint32_t word=stored/7;
    uint8_t factors[20];
    for(int i=0;i<20;i++) factors[i]=START[i];
    for(int j=0;j<k;j++) {
        int action=word%18;word/=18;
        for(int i=0;i<20;i++)factors[i]=TABLE[action][i][factors[i]];
    }
    for(int i=0;i<20;i++) if(factors[i]!=states[depth][i])return false;
    return true;
}
void print_word(uint32_t packed) {
    int depth=packed%7;
    uint32_t word=packed/7;
    for(int i=0;i<depth;i++) {
        int a=word%18;word/=18;
        cerr<<' '<<"URFDLB"[a/3];
        if(a%3==1)cerr<<"'";
        if(a%3==2)cerr<<'2';
    }
}
void search(int d,int previous_face,uint32_t code) {
    if(collision)return;
    Key k=projection(d);
    uint32_t packed=code*7+d;
    auto [it,inserted]=observed.emplace(k,packed);
    if(!inserted) {
        if(!same_full_state(it->second,d)) {
            cerr<<"COLLISION rep "<<representative<<" words:";
            print_word(it->second);
            cerr<<" ||";print_word(packed);cerr<<"\n";
            collision=true;return;
        }
        // A depth-first walk can see a longer word before a shorter one.
        // Only prune if the prior occurrence is AT MOST as deep.
        if(int(it->second%7)<=d)return;
        it->second=packed;
    } else nseen++;
    if(d==6)return;
    for(int a=0;a<18;a++) {
        int face=a/3;
        if(face==previous_face)continue;
        // Opposite faces commute: retain canonical order to reduce search.
        if(previous_face>=0 && abs(face-previous_face)==3 && face<previous_face)continue;
        for(int i=0;i<20;i++)
            states[d+1][i]=TABLE[a][i][states[d][i]];
        search(d+1,face,code+a*P18[d]);
        if(collision)return;
    }
}
int main(int argc,char**argv) {
    if(argc!=2) {cerr<<"Usage: verify_b6_16_bases ORBIT_INDEX_0_TO_26\n";return 2;}
    representative=atoi(argv[1]);
    if(representative<0||representative>=27)return 2;
    mask=REPS[representative];
    assert(__builtin_popcount(mask)==16);
    for(int i=0;i<20;i++)states[0][i]=START[i];
    observed.max_load_factor(0.8);
    observed.reserve(10000000);
    search(0,-1,0);
    cout<<"rep "<<representative<<" unique projected "<<nseen
        <<" fail "<<(collision?1:0)<<" orbit_size "<<int(ORBIT_SIZES[representative])<<"\n";
    if(!collision && nseen!=8240087) {
        cerr<<"INCOMPLETE: expected 8240087 HTM states (OEIS A080583)\n";
        return 3;
    }
    return 0;
}
