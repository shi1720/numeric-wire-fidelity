import fs from 'node:fs';import {performance} from 'node:perf_hooks';import {parse,stringify} from 'lossless-json';import {parseGuarded} from '../src/fidelity.mjs';
const fns={native:s=>JSON.stringify(JSON.parse(s)),guard:s=>JSON.stringify(parseGuarded(s)),lossless:s=>stringify(parse(s))};
let sink=0;const rows=[];
for(const target of [1024,16384,65536]){
 const n=Math.floor(target/40);const raw=JSON.stringify({arguments:Array.from({length:n},(_,i)=>({id:i,amount:0.1,label:'record'}))});
 for(const fn of Object.values(fns))for(let i=0;i<100;i++)sink+=fn(raw).length;
 // Rotating order controls some systematic order/warmup effects.
 for(let repeat=0;repeat<9;repeat++){
  const names=Object.keys(fns);names.push(...names.splice(0,repeat%3));
  for(const method of names){const t=performance.now();for(let i=0;i<500;i++)sink+=fns[method](raw).length;
   rows.push({target,bytes:Buffer.byteLength(raw),repeat,method,us:(performance.now()-t)*1000/500});}
 }
}
fs.writeFileSync('results/timing.json',JSON.stringify({warmup:100,iterations:500,repeats:9,sink,rows},null,2)+'\n');
for(const t of [1024,16384,65536])for(const method of Object.keys(fns)){
 const a=rows.filter(x=>x.target===t&&x.method===method).map(x=>x.us).sort((a,b)=>a-b);console.log({bytes:rows.find(x=>x.target===t).bytes,method,median_us:a[4],min:a[0],max:a[8]});
}
