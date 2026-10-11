import fs from 'node:fs';
import Ajv from 'ajv';
import {parse, stringify, isSafeNumber} from 'lossless-json';
import {parseGuarded, parseSafeIntegers} from '../src/fidelity.mjs';
import {deserializeMessage, serializeMessage} from '@modelcontextprotocol/sdk/shared/stdio.js';
const cases=JSON.parse(fs.readFileSync('data/cases.json','utf8'));
const ajv=new Ajv({strict:false,validateSchema:false,strictNumbers:true});
const cache=new Map();
const attempt=fn=>{try{return {out:fn()}}catch(e){return {reject:e.name}}};
const rows=cases.map(c=>{
 const x=JSON.parse(c.value), s=JSON.parse(c.schema);
 let validator=cache.get(c.schema);
 if(!validator){try{validator=ajv.compile(s)}catch(e){validator=()=>null}cache.set(c.schema,validator)}
 const msg='{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"fidelity_probe","arguments":{"value":'+c.value+'}}}';
 const schemaMsg='{"jsonrpc":"2.0","id":1,"result":{"tools":[{"name":"fidelity_probe","inputSchema":'+c.schema+'}]}}';
 return {id:c.id, native:JSON.stringify(x), native_schema:JSON.stringify(s), ajv_valid:validator(x),
  sdk:attempt(()=>JSON.stringify(deserializeMessage(msg).params.arguments.value)),
  sdk_schema:attempt(()=>JSON.stringify(deserializeMessage(schemaMsg).result.tools[0].inputSchema)),
  safe:attempt(()=>JSON.stringify(parseSafeIntegers(c.value))),
  payload_guard:attempt(()=>JSON.stringify(parseGuarded(c.value))),
  joint_guard:attempt(()=>{parseGuarded(c.schema);return JSON.stringify(parseGuarded(c.value))}),
  lossless:attempt(()=>stringify(parse(c.value))),
  library_guard:attempt(()=>{if(!isSafeNumber(c.value))throw new RangeError('loss');return JSON.stringify(JSON.parse(c.value))})};
});
fs.writeFileSync('results/transports.json',JSON.stringify(rows,null,2)+'\n');
fs.writeFileSync('results/environment.json',JSON.stringify({node:process.version,platform:process.platform,arch:process.arch,packages:JSON.parse(fs.readFileSync('package.json','utf8')).dependencies},null,2)+'\n');
console.log({cases:rows.length,projections:cache.size});
