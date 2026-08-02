from pathlib import Path

path=Path('tests/native_multi_window_0.8.13.spec.js')
text=path.read_text(encoding='utf-8')
old="""  const [a,b]=await openPair(context);
  await Promise.all([a.evaluate(()=>CUBE_REV_0813_TEST_HOOKS.setLeaseTimeoutForTest(1000)),b.evaluate(()=>CUBE_REV_0813_TEST_HOOKS.setLeaseTimeoutForTest(1000))]);
"""
new="""  const [a,b]=await openPair(context);
  const browserErrors=[];
  for(const [label,page] of [['a',a],['b',b]]){
    page.on('console',msg=>{if(msg.type()==='error')browserErrors.push({label,type:'console',text:msg.text()})});
    page.on('pageerror',err=>browserErrors.push({label,type:'pageerror',text:String(err&&err.message||err)}));
  }
  await Promise.all([a.evaluate(()=>CUBE_REV_0813_TEST_HOOKS.setLeaseTimeoutForTest(1000)),b.evaluate(()=>CUBE_REV_0813_TEST_HOOKS.setLeaseTimeoutForTest(1000))]);
"""
if text.count(old)!=1: raise SystemExit(f'LISTENER_TARGET_COUNT:{text.count(old)}')
text=text.replace(old,new,1)
old2="""  await a.evaluate(()=>CUBE_REV_0813_TEST_HOOKS.savePostTask('lease-expiry-network-ambiguity'));
  await b.evaluate(()=>{CUBE_REV_0813_TEST_HOOKS.send();return true});
  await expect.poll(()=>evidence.posts.length,{timeout:10000}).toBe(1);
"""
new2="""  await a.evaluate(()=>CUBE_REV_0813_TEST_HOOKS.savePostTask('lease-expiry-network-ambiguity'));
  await expect.poll(()=>b.evaluate(()=>{const s=CUBE_REV_0813_TEST_HOOKS.getState();return `${s.status}|${s.cursor}`}),{timeout:10000}).toBe('READY_TO_SUBMIT|28');
  await b.evaluate(()=>{CUBE_REV_0813_TEST_HOOKS.send();return true});
  try{
    await expect.poll(()=>evidence.posts.length,{timeout:10000}).toBe(1);
  }catch(error){
    const [aState,bState,stored,aUi,bUi]=await Promise.all([
      a.evaluate(()=>CUBE_REV_0813_TEST_HOOKS.getState()),
      b.evaluate(()=>CUBE_REV_0813_TEST_HOOKS.getState()),
      a.evaluate(()=>CUBE_REV_0813_TEST_HOOKS.getStoredState()),
      a.evaluate(()=>({done:document.querySelector('#doneText')?.textContent||'',retryHidden:document.querySelector('#retry')?.classList.contains('hidden'),doneHidden:document.querySelector('#done')?.classList.contains('hidden')})),
      b.evaluate(()=>({done:document.querySelector('#doneText')?.textContent||'',retryHidden:document.querySelector('#retry')?.classList.contains('hidden'),doneHidden:document.querySelector('#done')?.classList.contains('hidden')}))
    ]);
    const diagnostic={schema_version:'CR0813-NATIVE-SUBMISSION-DIAGNOSTIC-1',posts:evidence.posts,polls:evidence.polls,browser_errors:browserErrors,a_state:{status:aState.status,revision:aState.revision,cursor:aState.cursor,submission_control:aState.submission_control,snapshot_sealed:!!aState.submission_snapshot},b_state:{status:bState.status,revision:bState.revision,cursor:bState.cursor,submission_control:bState.submission_control,snapshot_sealed:!!bState.submission_snapshot},stored_state:{status:stored&&stored.status,revision:stored&&stored.revision,cursor:stored&&stored.cursor,submission_control:stored&&stored.submission_control,snapshot_sealed:!!(stored&&stored.submission_snapshot)},a_ui:aUi,b_ui:bUi};
    fs.mkdirSync('artifacts/0.8.13',{recursive:true});
    fs.writeFileSync('artifacts/0.8.13/native_submission_failure.json',JSON.stringify(diagnostic,null,2));
    throw new Error(`NATIVE_SUBMISSION_NO_POST:${JSON.stringify(diagnostic)}`,{cause:error});
  }
"""
if text.count(old2)!=1: raise SystemExit(f'SUBMISSION_TARGET_COUNT:{text.count(old2)}')
text=text.replace(old2,new2,1)
path.write_text(text,encoding='utf-8')
print('CR0813_NATIVE_SUBMISSION_DIAGNOSTICS_PATCH_PASS')
