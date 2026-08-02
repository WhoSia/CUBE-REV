from __future__ import annotations
from pathlib import Path

path=Path('js/participant-cognitive-mode-0.8.13.js')
text=path.read_text(encoding='utf-8')
block="""function deepFreeze(value){
  if(!value||typeof value!=='object'||Object.isFrozen(value))return value;
  for(const child of Object.values(value))deepFreeze(child);
  return Object.freeze(value);
}
"""
count=text.count(block)
if count<1:
    raise SystemExit('DEEP_FREEZE_MISSING')
while text.count(block)>1:
    first=text.find(block)
    second=text.find(block,first+len(block))
    text=text[:second]+text[second+len(block):]
if text.count("TRANSPORT_SESSION_INTERNAL_DIVERGENCE")!=1:
    raise SystemExit('CANONICAL_ENVELOPE_GUARD_COUNT')
if "return deepFreeze(envelope);" not in text:
    raise SystemExit('CANONICAL_ENVELOPE_FREEZE_MISSING')
path.write_text(text,encoding='utf-8')
print(f'CR0813_CANONICAL_ENVELOPE_CLEANUP_PASS original_deep_freeze_count={count}')
