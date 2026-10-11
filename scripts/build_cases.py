import sys, json, hashlib, collections
from pathlib import Path
from fractions import Fraction
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from oracle import loads, dumps, valid, num, decimal
ROOT = Path(__file__).resolve().parents[1]
CORPUS = Path(sys.argv[1])
KEYS = {'type','minimum','maximum','exclusiveMinimum','exclusiveMaximum','multipleOf','enum','const'}
MAPS = {'properties','patternProperties','$defs','definitions','dependentSchemas'}
SINGLE = {'additionalProperties','items','contains','not','if','then','else','propertyNames','unevaluatedProperties','unevaluatedItems','additionalItems'}
ARRAYS = {'allOf','anyOf','oneOf','prefixItems'}
def walk(x, p=''):
    if not isinstance(x, dict): return
    if x.get('type') in ('integer', 'number') and '$ref' not in x:
        q = {k:v for k,v in x.items() if k in KEYS}
        if any(isinstance(q.get(k), bool) for k in ['exclusiveMinimum','exclusiveMaximum']):
            # Translate draft-04 boolean exclusivity into draft-2020-12 local form.
            for k, bound in [('exclusiveMinimum','minimum'),('exclusiveMaximum','maximum')]:
                if isinstance(q.get(k), bool):
                    yes=q.pop(k)
                    if yes and bound in q:q[k]=q.pop(bound)
        yield p,q
    for k,v in x.items():
        esc=lambda k: k.replace('~','~0').replace('/','~1')
        if k in MAPS and isinstance(v,dict):
            for n,z in v.items():yield from walk(z,p+'/'+k+'/'+esc(n))
        elif k in SINGLE:
            if isinstance(v,list):
                for i,z in enumerate(v):yield from walk(z,p+'/'+k+'/'+str(i))
            else:yield from walk(v,p+'/'+k)
        elif k in ARRAYS and isinstance(v,list):
            for i,z in enumerate(v):yield from walk(z,p+'/'+k+'/'+str(i))

# Fixed diagnostic palette; deliberately not a model output distribution.
palette=['0','-0','1','-1','0.1','0.10000000000000001','0.3','0.30000000000000004',
'1.0000000000000001','0.99999999999999999','1e-324','5e-324','1e-323','1e309','-1e309',
'1.7976931348623157e308','1.7976931348623159e308','123456789.123456789','-0.10000000000000001']
for e in [31,32,52,53,54,63,64]:
    for delta in [-1,0,1,2,3]:
        palette += [str(2**e+delta), str(-(2**e+delta))]
palette=list(dict.fromkeys(palette))
leaves=[]; cases={}; memo={}; counts=collections.Counter(); schema_manifest=[]; errors=[]
for f in sorted(CORPUS.rglob('*.json')):
    rel=str(f.relative_to(CORPUS)); raw=f.read_bytes(); counts[f.parent.name]+=1
    schema_manifest.append({'file':rel,'sha256':hashlib.sha256(raw).hexdigest()})
    try:s=loads(raw)
    except Exception as e:errors.append([rel,type(e).__name__]);continue
    for path,q in walk(s):
        try:
            # Numeric projections intentionally do not assert full schema reachability.
            if q.get('multipleOf',1)<=0:raise ValueError('invalid divisor')
            memo_key=dumps(q)
            if memo_key in memo:
                leaves.append({'file':rel,'path':path,'group':f.parent.name,'projection':memo_key,'cases':memo[memo_key]})
                continue
            choices=list(palette)
            for k in ['minimum','maximum','exclusiveMinimum','exclusiveMaximum','const']:
                if num(q.get(k)):
                    v=Fraction(q[k]); choices.extend(decimal(v+d) for d in [-1,0,1])
            choices.extend(decimal(x) for x in q.get('enum',[]) if num(x))
            ids=[]
            for v in dict.fromkeys(choices):
                if not valid(q,loads(v)):continue
                key=dumps(q)+'\n'+v
                cid=hashlib.sha256(key.encode()).hexdigest()[:20]
                cases[cid]={'id':cid,'schema':dumps(q),'value':v}
                ids.append(cid)
            memo[memo_key]=ids
            leaves.append({'file':rel,'path':path,'group':f.parent.name,'projection':dumps(q),'cases':ids})
        except Exception as e:errors.append([rel,path,type(e).__name__])
(ROOT/'data/cases.json').write_text(json.dumps(list(cases.values()),indent=2)+'\n')
(ROOT/'data/leaves.json').write_text(json.dumps(leaves,indent=2)+'\n')
(ROOT/'data/corpus_manifest.json').write_text(json.dumps(schema_manifest,indent=2)+'\n')
(ROOT/'data/build_summary.json').write_text(json.dumps({'files':dict(counts),'leaves':len(leaves),'unique_cases':len(cases),'palette_size':len(palette),'errors':errors},indent=2)+'\n')
print((ROOT/'data/build_summary.json').read_text()[:5000])
