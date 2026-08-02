from __future__ import annotations
from pathlib import Path

js_path=Path('js/participant-cognitive-mode-0.8.13.js')
html_path=Path('participant-cognitive-mode-0.8.13.html')
test_path=Path('tests/native_multi_window_0.8.13.spec.js')

js=js_path.read_text(encoding='utf-8')
needle="""function exportSnapshot(x){
  const snapshot=scientificSnapshot(x);
  return collectorEnvelopeFromSnapshot(snapshot,{immutable_snapshot_integrity_fnv1a32:x.submission_snapshot_hash});
}
"""
replacement=needle+"""function collectorWorkingCopy(x){
  const canonical=exportSnapshot(x);
  const copy=JSON.parse(JSON.stringify(canonical));
  const same=copy.session_id===canonical.session_id&&
    copy.original_scientific_session_id===canonical.original_scientific_session_id&&
    copy.transport_session_policy===canonical.transport_session_policy&&
    copy.data_submission&&canonical.data_submission&&
    copy.data_submission.transport_session_id===canonical.data_submission.transport_session_id&&
    copy.data_submission.original_scientific_session_id===canonical.data_submission.original_scientific_session_id&&
    copy.cognitive_snapshot&&canonical.cognitive_snapshot&&
    copy.cognitive_snapshot.session_id===canonical.cognitive_snapshot.session_id;
  if(!same)throw new Error('COLLECTOR_WORKING_COPY_IDENTITY');
  if(Object.isFrozen(copy))throw new Error('COLLECTOR_WORKING_COPY_FROZEN');
  return copy;
}
"""
if js.count(needle)!=1:
    raise SystemExit(f'JS_EXPORT_TARGET_COUNT:{js.count(needle)}')
js=js.replace(needle,replacement,1)
api_old='transportSessionIdentity,deepFreeze,collectorEnvelopeFromSnapshot,exportSnapshot,emptySubmissionControl'
api_new='transportSessionIdentity,deepFreeze,collectorEnvelopeFromSnapshot,exportSnapshot,collectorWorkingCopy,emptySubmissionControl'
if js.count(api_old)!=1:
    raise SystemExit(f'JS_API_TARGET_COUNT:{js.count(api_old)}')
js=js.replace(api_old,api_new,1)
js_path.write_text(js,encoding='utf-8')

html=html_path.read_text(encoding='utf-8')
old='exportSession:()=>envelope'
new='exportSession:()=>CUBE_REV_COGNITIVE_MODE_0813.collectorWorkingCopy(state)'
if html.count(old)!=1:
    raise SystemExit(f'HTML_EXPORT_TARGET_COUNT:{html.count(old)}')
html=html.replace(old,new,1)
hook_old="exportSnapshot:()=>CUBE_REV_COGNITIVE_MODE_0813.exportSnapshot(state),transportIdentity:()=>{"
hook_new="exportSnapshot:()=>CUBE_REV_COGNITIVE_MODE_0813.exportSnapshot(state),collectorWorkingCopy:()=>CUBE_REV_COGNITIVE_MODE_0813.collectorWorkingCopy(state),transportIdentity:()=>{"
if html.count(hook_old)!=1:
    raise SystemExit(f'HTML_HOOK_TARGET_COUNT:{html.count(hook_old)}')
html=html.replace(hook_old,hook_new,1)
html_path.write_text(html,encoding='utf-8')

test=test_path.read_text(encoding='utf-8')
anchor="""  const snapshotHash=sealed1.submission_snapshot_hash,retryId=sealed1.submission_control.retry_id;
"""
insert="""  const copyIsolation=await a.evaluate(()=>{
    const h=CUBE_REV_0813_TEST_HOOKS,canonical=h.exportSnapshot(),working=h.collectorWorkingCopy();
    const before=canonical.session_id;
    working.session_id='CR-20000101000000-000000000000';
    return {canonical_frozen:Object.isFrozen(canonical),working_frozen:Object.isFrozen(working),canonical_session_id:canonical.session_id,before};
  });
  expect(copyIsolation.canonical_frozen).toBe(true);
  expect(copyIsolation.working_frozen).toBe(false);
  expect(copyIsolation.canonical_session_id).toBe(copyIsolation.before);
"""+anchor
if test.count(anchor)!=1:
    raise SystemExit(f'TEST_ANCHOR_COUNT:{test.count(anchor)}')
test=test.replace(anchor,insert,1)
test_path.write_text(test,encoding='utf-8')
print('CR0813_COLLECTOR_WORKING_COPY_PATCH_PASS')
