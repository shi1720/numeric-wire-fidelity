import {McpServer} from '@modelcontextprotocol/sdk/server/mcp.js';
import {StdioServerTransport} from '@modelcontextprotocol/sdk/server/stdio.js';
import {z} from 'zod/v3';
import {PassThrough} from 'node:stream';
import readline from 'node:readline';
import {parseGuarded} from '../src/fidelity.mjs';
const mode=process.argv[2];
const records=new Map();
for(const e of [31n,52n,53n,54n,63n,64n])for(let d=-4n;d<=4n;d++){
 const id=(2n**e+d).toString(); records.set(id,'record:'+id);
 const alias=Number(id).toString();records.set(alias,'record:'+alias);
}
const server=new McpServer({name:'local-fidelity-experiment',version:'1.0.0'});
server.registerTool('read_record',{description:'Read a local fixture record by identifier',
 inputSchema:{record_id:mode==='string'?z.string().regex(/^\d+$/):z.number().int()}},
 async({record_id})=>({content:[{type:'text',text:records.get(String(record_id))??'missing'}]}));
let input=process.stdin;
if(mode==='guard'){
 input=new PassThrough();
 const lines=readline.createInterface({input:process.stdin});
 lines.on('line',line=>{try{parseGuarded(line);input.write(line+'\n')}catch(e){
  const id=JSON.parse(line).id;
  process.stdout.write(JSON.stringify({jsonrpc:'2.0',id,error:{code:-32602,message:'Pre-parse fidelity rejection'}})+'\n');
 }});
}
await server.connect(new StdioServerTransport(input,process.stdout));
