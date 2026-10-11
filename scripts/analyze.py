import json,sys,collections,platform,importlib.metadata
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from oracle import loads,valid
R=Path(__file__).resolve().parents[1]; read=lambda p:json.loads((R/p).read_text())
cases={c['id']:c for c in read('data/cases.json')}; rows=read('results/transports.json'); metrics=collections.defaultdict(collections.Counter); flags={}; schemas=set()
for row in rows:
 c=cases[row['id']]; s=loads(c['schema']); v=loads(c['value']); assert valid(s,v)
 same_schema=loads(row['native_schema'])==s; schemas.add(c['schema'])
 out=loads(row['native']); changed=out!=v
 hidden=changed and row['ajv_valid'] is True
 flags[c['id']]={'changed':changed,'hidden':hidden,'schema_changed':not same_schema}
 try:row['python_native']={'out':json.dumps(json.loads(c['value']),allow_nan=False)}
 except ValueError:row['python_native']={'reject':'ValueError'}
 for method in ['python_native','native','sdk','safe','payload_guard','joint_guard','lossless','library_guard']:
  m=metrics[method]; m['total']+=1
  o={'out':row[method]} if method=='native' else row[method]
  if 'reject' in o:m['rejected']+=1;continue
  y=loads(o['out']);m['accepted']+=1
  m['changed']+=int(y!=v);m['original_invalid']+=int(not valid(s,y));m['preserved']+=int(y==v)
  if method=='sdk': assert o['out']==row['native']
  if y!=v and row['ajv_valid'] is True:m['hidden']+=1
 assert row['sdk_schema']['out']==row['native_schema']
groups=collections.defaultdict(collections.Counter)
for leaf in read('data/leaves.json'):
 g=groups[leaf['group']];g['leaves']+=1
 g['tested_leaves']+=int(bool(leaf['cases']))
 for f in ['changed','hidden','schema_changed']:
  g[f+'_leaves']+=int(any(flags[c][f] for c in leaf['cases']))
 g['pairs']+=len(leaf['cases']);g['changed_pairs']+=sum(flags[c]['changed'] for c in leaf['cases']);g['hidden_pairs']+=sum(flags[c]['hidden'] for c in leaf['cases'])
lit=read('results/literal_audit.json')
summary={'unique_projections':len(schemas),'unique_pairs':len(rows),'groups':dict(groups),'methods':dict(metrics),
'changed_schemas_in_test':len({cases[r['id']]['schema'] for r in rows if flags[r['id']]['schema_changed']}),
'changed_unique_pairs':sum(f['changed'] for f in flags.values()),'hidden_unique_pairs':sum(f['hidden'] for f in flags.values()),
'literals':{k:lit[k] for k in ['files','numbers','changed','affected_files']},
'changed_assertion_literals':sum(r['path'].split('/')[-1] in ['minimum','maximum','exclusiveMinimum','exclusiveMaximum','multipleOf','const'] for r in lit['rows']),
'python':platform.python_version(),'python_packages':{p:importlib.metadata.version(p) for p in ['jsonschema','matplotlib','numpy']}}
(R/'results/summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
