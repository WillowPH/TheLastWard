'use strict';
const assert=require('node:assert/strict'),vm=require('node:vm'),fs=require('node:fs');
const code=fs.readFileSync('js/launch_guard.js','utf8');
for(const protocol of ['file:','http:']){
 let callback,help;
 const document={addEventListener:(event,cb)=>{assert.equal(event,'DOMContentLoaded');callback=cb;},createElement:()=>({setAttribute(){},style:{}}),body:{append:n=>{help=n;}}};
 vm.runInNewContext(code,{document,location:{protocol}});
 if(protocol==='file:'){assert(callback);callback();assert(help.innerHTML.includes('START_GAME.exe'));assert(help.innerHTML.includes('whole ZIP'));assert(help.innerHTML.includes('no Python'));}
 else assert.equal(callback,undefined);
}
console.log('PASS direct HTML launch shows actionable instructions; local-server launch is unaffected');
