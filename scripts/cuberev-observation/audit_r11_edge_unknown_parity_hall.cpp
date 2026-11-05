// CUBE-REV 0.28 R11: fully unknown edge permutation parity,
// universal 18-frame edge-only feedback leaf-count obstruction.
// Same Hall-relaxed recursion as independently certified R7 H=17;
// this uses H=18 and correctly compares with BOTH edge parity classes.
// A known corner state would collapse this threshold to only 12!*2^10.
#include <array>
#include <vector>
#include <string>
#include <iostream>
#include <algorithm>
#include <cassert>
#include <cstdint>
using namespace std;
constexpr int K=15625,MASKS=4096,H=18;
int a[12],b[12],cnt[MASKS][6],pop[MASKS],neighbors[64];
unsigned char cap[MASKS][64],need[K][64],digits[K][6],sumd[K];
int pw[6]={1,5,25,125,625,3125};
vector<int64_t> memo;
long long visited=0;
int64_t solve(int mask,int code){
 int key=mask*K+code; auto &r=memo[key];
 if(r>=0)return r;
 ++visited;
 int paired=pop[mask],pending=sumd[code];
 int read=pending+2*paired;
 if(read>H || pending+paired>12)return r=0;
 for(int c=0;c<6;c++)
   if(cnt[mask][c]+digits[code][c]>4)return r=0;
 for(int s=1;s<64;s++)
   if(need[code][s]>cap[mask][s])return r=0;
 if(read==H)return r=1;
 int64_t best=0;
 if(paired+pending<12){
   int64_t v=0;
   for(int c=0;c<6;c++)
     if(cnt[mask][c]+digits[code][c]<4)
       v+=solve(mask,code+pw[c]);
   best=max(best,v);
 }
 for(int c=0;c<6;c++)if(digits[code][c]){
   int64_t v=0;
   for(int j=0;j<12;j++)
     if(!(mask&(1<<j)) && (a[j]==c||b[j]==c)){
       int d=(a[j]==c)?b[j]:a[j];
       if(cnt[mask][d]+digits[code][d]<4)
         v+=solve(mask|(1<<j),code-pw[c]);
     }
   best=max(best,v);
 }
 return r=max<int64_t>(1,best);
}
int main(){
 string colors="URFDLB";
 string names[12]={"UR","UF","UL","UB","DR","DF",
                   "DL","DB","FR","FL","BL","BR"};
 for(int j=0;j<12;j++){
   a[j]=int(colors.find(names[j][0]));
   b[j]=int(colors.find(names[j][1]));
 }
 for(int m=0;m<MASKS;m++){
   pop[m]=__builtin_popcount(unsigned(m));
   for(int j=0;j<12;j++)if(m&(1<<j)){
     cnt[m][a[j]]++;
     cnt[m][b[j]]++;
   }
 }
 for(int s=1;s<64;s++)
   for(int j=0;j<12;j++)
     if((s&(1<<a[j]))||(s&(1<<b[j])))neighbors[s]|=1<<j;
 for(int m=0;m<MASKS;m++)
   for(int s=1;s<64;s++)
     cap[m][s]=__builtin_popcount(unsigned(neighbors[s]&(~m)));
 for(int code=0;code<K;code++){
   int x=code;
   for(int c=0;c<6;c++){
     digits[code][c]=x%5;
     sumd[code]+=digits[code][c];
     x/=5;
   }
   for(int s=1;s<64;s++)
     for(int c=0;c<6;c++)
       if(s&(1<<c))need[code][s]+=digits[code][c];
 }
 memo.assign(size_t(MASKS)*K,-1);
 auto n=solve(0,0);
 constexpr int64_t all_edge_states=980995276800LL; // 12!*2^11
 assert(n==947446315200LL);
 assert(n<all_edge_states);
 cout<<"R11_EDGE_ONLY_HALL_LOWER_19_PASS "<<n<<" "
     <<all_edge_states<<" visited "<<visited<<"\n";
 cout<<"R11_BOUND unknown corner parity: edge-only adaptive >=19;"
     <<" full two-color joint cube remains 18..21\n";
}