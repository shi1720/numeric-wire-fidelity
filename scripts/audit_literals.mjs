import fs from 'node:fs';
import path from 'node:path';
import {parse,isLosslessNumber} from 'lossless-json';
import {decimalKey} from '../src/fidelity.mjs';
const root=process.argv[2]; const rows=[];let files=0,numbers=0,failures=[];
for(const f of fs.readdirSync(root,{recursive:true}).filter(f=>f.endsWith('.json')).sort()){
 const raw=fs.readFileSync(path.join(root,f),'utf8');files++;
 try{
 const exact=parse(raw),native=JSON.parse(raw);
 const walk=(a,b,p)=>{
  if(isLosslessNumber(a)){
   numbers++;const to=JSON.stringify(b);
   if(to==='null'||decimalKey(a.toString())!==decimalKey(to)) rows.push({file:f,path:p,from:a.toString(),to});
  }else if(a && typeof a==='object') for(const [k,v]of Object.entries(a))walk(v,b[k],p+'/'+k.replaceAll('~','~0').replaceAll('/','~1'));
 };walk(exact,native,'');
 }catch(e){failures.push({file:f,error:e.message})}
}
fs.writeFileSync('results/literal_audit.json',JSON.stringify({files,numbers,changed:rows.length,affected_files:new Set(rows.map(r=>r.file)).size,failures,rows},null,2)+'\n');
console.log({files,numbers,changed:rows.length,affected_files:new Set(rows.map(r=>r.file)).size,failures:failures.length});
