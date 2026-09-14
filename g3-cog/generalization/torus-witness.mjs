import {execFileSync} from 'node:child_process';
const out=execFileSync(process.execPath,['g3-cog/generalization/rstp-suite.mjs'],{encoding:'utf8'});
const suite=JSON.parse(out);
console.log(JSON.stringify(suite,null,2));
if(suite.result!=='PASS')process.exit(1);
