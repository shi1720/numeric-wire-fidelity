import subprocess,os,json,selectors,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
NODE=os.environ.get('NODE','node')
rows=[]
def read(p):
 s=selectors.DefaultSelector();s.register(p.stdout,selectors.EVENT_READ)
 if not s.select(10):raise TimeoutError('server response')
 return json.loads(p.stdout.readline())
for mode in ['native','guard','string']:
 p=subprocess.Popen([NODE,'scripts/demo_server.mjs',mode],cwd=ROOT,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,bufsize=1)
 def send(x):p.stdin.write(x+'\n');p.stdin.flush()
 try:
  send(json.dumps({'jsonrpc':'2.0','id':1,'method':'initialize','params':{'protocolVersion':'2025-06-18','capabilities':{},'clientInfo':{'name':'raw-exact-client','version':'1'}}}))
  init=read(p);assert 'result' in init,init
  send(json.dumps({'jsonrpc':'2.0','method':'notifications/initialized'}))
  send(json.dumps({'jsonrpc':'2.0','id':2,'method':'tools/list'}));tools=read(p)
  (ROOT/f'results/demo_schema_{mode}.json').write_text(json.dumps(tools,indent=2)+'\n')
  i=2
  for e in [31,52,53,54,63,64]:
   for d in range(-4,5):
    i+=1;n=2**e+d
    raw=json.dumps({'jsonrpc':'2.0','id':i,'method':'tools/call','params':{'name':'read_record','arguments':{'record_id':str(n) if mode=='string' else n}}},separators=(',',':'))
    send(raw); response=read(p)
    text=response.get('result',{}).get('content',[{}])[0].get('text')
    rows.append({'mode':mode,'power':e,'offset':d,'source':str(n),'request':raw,'response':response,'rejected':'error' in response,'correct':text=='record:'+str(n)})
 finally:
  p.terminate();p.wait(timeout=5)
  err=p.stderr.read()
  if err:print(err)
(ROOT/'results/demo.json').write_text(json.dumps(rows,indent=2)+'\n')
for mode in ['native','guard','string']:
 r=[x for x in rows if x['mode']==mode];print(mode,{'total':len(r),'correct':sum(x['correct'] for x in r),'rejected':sum(x['rejected'] for x in r),'wrong':sum(not x['correct'] and not x['rejected'] for x in r)})
