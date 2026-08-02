from pathlib import Path
p=Path('tests/native_multi_window_0.8.13.spec.js')
s=p.read_text(encoding='utf-8')
old="""  await a.evaluate(()=>CUBE_REV_0813_TEST_HOOKS.savePostTask('lease-expiry-network-ambiguity'));
  await expect.poll(()=>evidence.posts.length,{timeout:10000}).toBe(1);
"""
new="""  await a.evaluate(()=>CUBE_REV_0813_TEST_HOOKS.savePostTask('lease-expiry-network-ambiguity'));
  await b.evaluate(()=>{CUBE_REV_0813_TEST_HOOKS.send();return true});
  await expect.poll(()=>evidence.posts.length,{timeout:10000}).toBe(1);
"""
if s.count(old)!=1: raise SystemExit(f'TARGET_COUNT:{s.count(old)}')
p.write_text(s.replace(old,new,1),encoding='utf-8')
print('CR0813_NATIVE_SUBMISSION_DRIVER_PATCH_PASS')
