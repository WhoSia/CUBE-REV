// CUBE-REV 0.24 P1-R4: exact genuine 3x3 group-word rewrites over Cartier-Foata trace class.
// No local rewrite within these scopes is NOT a global optimality certificate.
// Uses genuine original C++ facelet/cubie turn group, not an abstract sequence toy.
#define main previous_p1r3_main
#include "../p1_r3_true_54_facelet_multiaxis_dr_cpp/main.cpp"
#undef main
struct Key{array<uint8_t,40>x;bool operator==(const Key&b)const{return x==b.x;}};
Key K(const Cube&s){Key k;int j=0;for(uint8_t a:s.cp)k.x[j++]=a;for(uint8_t a:s.co)k.x[j++]=a;for(uint8_t a:s.ep)k.x[j++]=a;for(uint8_t a:s.eo)k.x[j++]=a;return k;}
struct KeyHash{size_t operator()(const Key&s)const noexcept{uint64_t h=1469598103934665603ULL;for(uint8_t b:s.x){h^=b;h*=1099511628211ULL;}return h;}};
struct Node {Cube s;int parent;uint8_t action,depth;};
vector<Node> goalNodes;unordered_map<Key,int,KeyHash> goalIndex;
vector<int> inverseword(vector<int>w){reverse(w.begin(),w.end());for(int &a:w){int face=a/3,t=a%3;a=face*3+(t==0?1:t==1?0:2);}return w;}
void constructGoal(){goalNodes.reserve(635000);goalIndex.reserve(800000);goalNodes.push_back({solved(),-1,255,0});goalIndex.emplace(K(solved()),0);for(size_t i=0;i<goalNodes.size();i++){
 Node n=goalNodes[i];if(n.depth>=5)continue;
 for(int a=0;a<18;a++){Cube v=composeCube(n.s,turn[a]);Key k=K(v);if(goalIndex.count(k))continue;int pos=goalNodes.size();goalNodes.push_back({v,int(i),uint8_t(a),uint8_t(n.depth+1)});goalIndex.emplace(k,pos);}
 }if(goalNodes.size()!=621649)throw runtime_error("goal B5 cardinality bad");}
vector<int>goalTo(int i){vector<int>w;while(goalNodes[i].parent>=0){w.push_back(goalNodes[i].action);i=goalNodes[i].parent;}reverse(w.begin(),w.end());return w;}
struct ResultL{int examined=0,expanded=0,matched=0,shortestDistance=-1,sourceWindow=-1,windowSize=-1;vector<int>replacement;};
ResultL tryWindows(const vector<int>& base,int maxWindow=11,int maxExpanded=8500000){
 ResultL info; int n=base.size();
 for(int size=4;size<=min(n,maxWindow);size++)for(int begin=0;begin+size<=n;begin++){
  info.examined++;vector<int>window(base.begin()+begin,base.begin()+begin+size);
  Cube segment=cubeAfter(window);
  int required=max(0,size-1-5);
  unordered_set<Key,KeyHash>seen;seen.reserve(required==5?660000:55000);
  struct Fringe{Cube s;vector<int>path;int last;};
  vector<Fringe>front{{segment,{},-1}},next;
  seen.emplace(K(segment));
  for(int depth=0;depth<=required;depth++){
    next.clear();
    for(const Fringe&e:front){info.expanded++;if(info.expanded>maxExpanded)return info;
      auto jt=goalIndex.find(K(e.s));
      if(jt!=goalIndex.end()){
       vector<int>goalToMeet=goalTo(jt->second),solution=e.path;
       auto inverseGoal=inverseword(goalToMeet);
       solution.insert(solution.end(),inverseGoal.begin(),inverseGoal.end());
       if((int)solution.size()<size){
        vector<int>replacement=inverseword(solution);
        if(cubeAfter(replacement).cp!=segment.cp||cubeAfter(replacement).co!=segment.co||cubeAfter(replacement).ep!=segment.ep||cubeAfter(replacement).eo!=segment.eo)throw runtime_error("rewrite group equality mismatch");
        vector<int>candidate(base.begin(),base.begin()+begin);candidate.insert(candidate.end(),replacement.begin(),replacement.end());candidate.insert(candidate.end(),base.begin()+begin+size,base.end());candidate=normalizeLegalHTM(candidate);
        if(!physicalSolves(parse("R' B' F2 D2 F2 L2 R2 U' F2 L2 D2 B2 D F L' R2 B U2 F2 R2"),candidate))throw runtime_error("full original 54 stickers did not solve");
        info.matched++;info.shortestDistance=solution.size();info.sourceWindow=begin;info.windowSize=size;info.replacement=candidate;return info;
       }
      }
      if(depth==required)continue;
      for(int a=0;a<18;a++){if(!canonical(e.last,a))continue;Cube c=composeCube(e.s,turn[a]);Key k=K(c);if(seen.insert(k).second){auto p=e.path;p.push_back(a);next.push_back({c,std::move(p),a});}}
    }
    front.swap(next);
  }
 }
 return info;
}
int main(int argc,char**argv){try{initTurns();auto scramble=parse("R' B' F2 D2 F2 L2 R2 U' F2 L2 D2 B2 D F L' R2 B U2 F2 R2");auto base=inverseword(scramble);if(!physicalSolves(scramble,base))throw runtime_error("inverse baseline illegal");auto t=Clock::now();constructGoal();cerr<<"GOAL_BALL_RADIUS5 "<<goalNodes.size()<<" BUILD_SEC "<<chrono::duration<double>(Clock::now()-t).count()<<"\n";int maxW=argc>1?stoi(argv[1]):10,maxEx=argc>2?stoi(argv[2]):10000000;
 // Conway/Cartier-Foata trace class: all exact reorders of disjoint-face
 // generators. These commute as TRUE physical rotations, not syntactic guess.
 queue<vector<int>>q;q.push(base);
 set<vector<int>>seen;seen.insert(base);
 while(!q.empty()){
  auto cur=q.front();q.pop();
  for(size_t j=1;j<cur.size();j++){
   int fa=cur[j-1]/3,fb=cur[j]/3;
   bool opposite=(fa==0&&fb==3)||(fa==3&&fb==0)||(fa==1&&fb==4)||(fa==4&&fb==1)||(fa==2&&fb==5)||(fa==5&&fb==2);
   if(!opposite)continue;
   auto nxt=cur;swap(nxt[j-1],nxt[j]);
   if(!physicalSolves(scramble,nxt))throw runtime_error("disjoint turn swap did not preserve actual original cube");
   if(seen.insert(nxt).second)q.push(nxt);
  }
 }
 int checked=0,nodes=0,windows=0;cerr<<"EXACT_COMMUTATION_TRACE_CLASS "<<seen.size()<<"\n";
 for(const auto& representative:seen){
  checked++;
  auto r=tryWindows(representative,maxW,maxEx);
  windows+=r.examined;nodes+=r.expanded;
  if(r.matched){
   cout<<"CONWAY_TRACE_LOCAL_REWRITE_FOUND "<<r.matched<<" TRACE_CLASS "<<seen.size()<<" WINDOW "<<r.sourceWindow<<" SIZE "<<r.windowSize<<" NEW "<<r.shortestDistance<<"\n";
   cout<<"WHOLE_REWRITE_LEN "<<r.replacement.size()<<" WORD "<<join(r.replacement)<<"\n";
   return 0;
  }
 }
 cout<<"CONWAY_COMMUTATION_TRACE_CLASS "<<seen.size()<<" REPRESENTATIVES_EXAMINED "<<checked<<" LOCAL_WINDOWS "<<windows<<" EXACT_BIDIR_NODES "<<nodes<<" REWRITE_FOUND 0\n";
 cout<<"LOCAL_REWRITE_HOLD_NOT_GLOBAL_OPTIMALITY\n";}
catch(exception&e){cerr<<"ERROR "<<e.what()<<"\n";return 1;}}