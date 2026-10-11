"""Cross-check raw recorded observations; no inference or model grading."""
import sys,json,collections
from pathlib import Path
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'src'))
from oracle import loads,valid
read=lambda x:json.loads((R/x).read_text())
s=read('results/summary.json');cases={c['id']:c for c in read('data/cases.json')};rows=read('results/transports.json')
assert len(rows)==len(cases)==8207
for r in rows:
 c=cases[r['id']];assert valid(loads(c['schema']),loads(c['value']))
 assert r['sdk']['out']==r['native']
 assert loads(r['lossless']['out'])==loads(c['value'])
 for method in ['payload_guard','joint_guard','library_guard']:
  if 'out' in r[method]:assert loads(r[method]['out'])==loads(c['value'])
for r in read('results/schema_witnesses.json'):
 assert not valid(loads(r['schema']),loads(r['value']))
 assert r['native_accepts'] and r['payload_guard_accepts'] and not r['joint_guard_accepts']
demo=read('results/demo.json');assert len(demo)==162
for mode in ['native','guard','string']:
 d=[r for r in demo if r['mode']==mode];assert len(d)==54
 if mode=='native':assert sum(not r['correct'] for r in d)==25
 elif mode=='guard':assert all(r['correct'] or r['rejected'] for r in d) and sum(r['rejected'] for r in d)==25
 else:assert all(r['correct'] for r in d)
prop=read('results/property_summary.json');assert prop['tests']==15265 and prop['guard_false_accepts']==prop['guard_false_rejects']==prop['lossless_changes']==0
print('Verified raw stress outputs, source-invalid schema witnesses, 162 local tool calls, and 15,265 differential checks.')
