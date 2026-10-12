// Full local commuting-opposite-faces + same-face group-product closure.
// This is an EXACT FINITE closure for the two relations in this contract;
// it is NOT the full Rubik's cube relation group or global HTM distance.
// Every rewrite has equality of the actual physical full-cubie element.
struct TraceResult{bool success=false,exhausted=true;size_t states=0;vector<int>word;};
bool genuineOppositeFaces(int a,int b){
 const int x=a/3,y=b/3;
 return (x==0&&y==3)||(x==3&&y==0)||(x==1&&y==4)||(x==4&&y==1)||(x==2&&y==5)||(x==5&&y==2);
}
string traceKey(const vector<int>&w){string k;k.reserve(w.size());for(int x:w)k.push_back(char(1+x));return k;}
TraceResult traceRewrite(const vector<int>&original,int goal=18,int maxStates=30000){
 TraceResult report;queue<vector<int>> q;unordered_set<string>seen;
 q.push(original);seen.insert(traceKey(original));
 while(!q.empty()){
  auto word=std::move(q.front());q.pop();++report.states;
  if(int(word.size())<=goal){report.success=true;report.word=word;return report;}
  if(int(report.states)>maxStates){report.exhausted=false;return report;}
  for(int j=1;j<int(word.size());j++){
   if(word[j]/3==word[j-1]/3){
      auto candidate=word;
      auto power=[](int t){return t%3==0?1:t%3==1?3:2;};
      const int sum=(power(candidate[j-1])+power(candidate[j]))%4,face=candidate[j]/3;
      candidate.erase(candidate.begin()+j-1,candidate.begin()+j+1);
      if(sum)candidate.insert(candidate.begin()+j-1,face*3+(sum==1?0:sum==2?2:1));
      if(seen.insert(traceKey(candidate)).second)q.push(std::move(candidate));
   }else if(genuineOppositeFaces(word[j-1],word[j])){
      auto candidate=word;swap(candidate[j-1],candidate[j]);
      if(seen.insert(traceKey(candidate)).second)q.push(std::move(candidate));
   }
  }
 }
 return report;
}