import sys,random,json,subprocess,os
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from oracle import loads
R=Path(__file__).resolve().parents[1];rng=random.Random(1720406)
values=[]
for e in range(0,81):
 for d in range(-32,33):values.append(str(2**e+d))
for _ in range(10000):
 k=rng.randint(1,60); c=str(rng.randint(1,9))+''.join(str(rng.randrange(10)) for _ in range(k-1))
 values.append(('-' if rng.randrange(2) else '')+c+'e'+str(rng.randint(-400,400)))
(R/'data/property_values.json').write_text(json.dumps(values)+'\n')
script="""import fs from 'node:fs';import {parseGuarded} from './src/fidelity.mjs';import {parse,stringify} from 'lossless-json';
const v=JSON.parse(fs.readFileSync('data/property_values.json','utf8'));
const a=v.map(s=>{let guard;try{guard=JSON.stringify(parseGuarded(s))}catch{guard=null}return [JSON.stringify(JSON.parse(s)),guard,stringify(parse(s))]});
fs.writeFileSync('results/property_outputs.json',JSON.stringify(a)+'\\n');"""
subprocess.run([os.environ.get('NODE','node'),'--input-type=module','-e',script],cwd=R,check=True)
rows=json.loads((R/'results/property_outputs.json').read_text());changed=0
for source,(native,guard,lossless) in zip(values,rows):
 exact=loads(source);same=loads(native)==exact
 assert (guard is not None)==same,(source,native,guard)
 assert loads(lossless)==exact
 if guard is not None:assert loads(guard)==exact
 changed+=int(not same)
summary={'seed':1720406,'tests':len(values),'native_changed':changed,'guard_false_accepts':0,'guard_false_rejects':0,'lossless_changes':0}
(R/'results/property_summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(summary)
