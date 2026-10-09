/** CUBE-REV 0.15 P3D — exact noisy finite-fiber experiments.
 * Pure synthetic 24-coordinate cube automaton, not human or cryptographic data.
 * Noise: independent BSC(epsilon) on each read; actual actions are exact.
 */
import {ACTIONS} from '../cuberev-013/cross4-pdb.mjs';
export const sensorBit=(x,sensor)=>sensor==='orientation'?Number(x%2===0):
  sensor==='completion'?Number(x===0):(()=>{throw Error('UNKNOWN_SENSOR');})();
export function noisyCodewords(fiber,word,moves,sensor){
 if(fiber.length!==16||new Set(fiber).size!==16)throw Error('FIBER_SIZE');
 const states=[...fiber],bits=states.map(x=>sensorBit(x,sensor));
 for(let i=0;i<word.length;i++){
  const ai=ACTIONS.indexOf(word[i]);if(ai<0||i>=21)throw Error('ACTION_OR_LENGTH');
  for(let j=0;j<16;j++){
   states[j]=moves[ai][states[j]];
   bits[j]|=sensorBit(states[j],sensor)<<(i+1);
  }
 }
 return {signatures:bits,readCount:word.length+1};
}
export function exactBscMap(signatures,readCount,epsilon){
 if(signatures.length!==16||readCount<1||readCount>22||
   !Number.isFinite(epsilon)||epsilon<0||epsilon>0.5)throw Error('BAD_BSC');
 const N=2**readCount,all=(1<<readCount)-1;
 if(new Set(signatures).size!==16)throw Error('NOT_NOISELESSLY_SEPARATING');
 const counts=Array(readCount+1).fill(0);
 for(let y=0;y<N;y++){
  let closest=readCount;
  for(const c of signatures){
   let v=(y^c)&all,dist=0;
   while(v){dist++;v&=v-1;}
   closest=Math.min(closest,dist);
  }
  counts[closest]++;
 }
 let accuracy=0;
 for(let d=0;d<counts.length;d++)
  accuracy+=counts[d]*epsilon**d*(1-epsilon)**(readCount-d)/16;
 return {accuracy,risk:1-accuracy,nearestDistanceHistogram:counts};
}
export function majorityBitError(epsilon,repeats){
 if(!Number.isFinite(epsilon)||epsilon<0||epsilon>0.5||
   !Number.isInteger(repeats)||repeats<1||repeats%2!==1)throw Error('ODD_REPEATS_REQUIRED');
 let total=0,coef=1;
 for(let k=0;k<=repeats;k++){
  if(k>0)coef=coef*(repeats-k+1)/k;
  if(k>repeats/2)total+=coef*epsilon**k*(1-epsilon)**(repeats-k);
 }
 return total;
}
export function uniformFiberGuarantee(epsilon,repeats,readCheckpoints=8,moveCost=1,sensorReadCost=0.1){
 const flip=majorityBitError(epsilon,repeats);
 return {logicalError:flip,maxFailureUpper:Math.min(1,readCheckpoints*flip),
    successLower:Math.max(0,1-readCheckpoints*flip),
    maxPhysicalReads:readCheckpoints*repeats,
    maxTotalCost:7*moveCost+readCheckpoints*repeats*sensorReadCost};
}
export function exactAdaptiveBayes(fiber,moves,sensor,epsilon,horizon){
 if(fiber.length!==16||!Number.isInteger(horizon)||horizon<0||horizon>3||
   epsilon<0||epsilon>0.5)throw Error('BAD_BAYES_INPUT');
 const recurse=(positions,weights,remaining)=>{
  if(!remaining)return Math.max(...weights);
  let best=0;
  for(let a=0;a<18;a++){
   const next=positions.map(x=>moves[a][x]);
   let score=0;
   for(let bit=0;bit<=1;bit++){
    const updated=next.map((x,i)=>weights[i]*(sensorBit(x,sensor)===bit?1-epsilon:epsilon));
    score+=recurse(next,updated,remaining-1);
   }
   best=Math.max(best,score);
  }
  return best;
 };
 let accuracy=0;
 for(let bit=0;bit<=1;bit++)
  accuracy+=recurse(fiber,fiber.map(x=>(sensorBit(x,sensor)===bit?1-epsilon:epsilon)/16),horizon);
 return accuracy;
}
