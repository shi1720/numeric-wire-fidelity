import fs from 'node:fs';import Ajv from 'ajv';import {parseGuarded} from '../src/fidelity.mjs';
const fixtures=[
 ['{"type":"integer","const":9007199254740993}','9007199254740992'],
 ['{"type":"integer","minimum":9007199254740993}','9007199254740992'],
 ['{"type":"number","const":0.10000000000000001}','0.1'],
 ['{"type":"number","maximum":0.99999999999999999}','1']
];
const ajv=new Ajv();const rows=fixtures.map(([schema,value])=>{
 let payload,joint;try{parseGuarded(value);payload=true}catch{payload=false}
 try{parseGuarded(schema);parseGuarded(value);joint=true}catch{joint=false}
 return {schema,value,native_accepts:ajv.compile(JSON.parse(schema))(JSON.parse(value)),payload_guard_accepts:payload,joint_guard_accepts:joint};
});
fs.writeFileSync('results/schema_witnesses.json',JSON.stringify(rows,null,2)+'\n');console.log(rows);
