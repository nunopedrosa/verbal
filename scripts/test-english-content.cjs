'use strict';
const assert=require('assert'),fs=require('fs'),vm=require('vm'),cp=require('child_process'),crypto=require('crypto');
const E=require('../public/english.js');
const context={};vm.runInNewContext(fs.readFileSync('public/english.js','utf8'),context);assert(context.VerbalEnglish);
assert.deepStrictEqual(Object.keys(E.themes),['food','nature','objects','animals','plants','places']);
for(let n=4;n<=8;n++){
 const guesses=new Set(E.guesses[n]);assert(guesses.size>2000);assert.strictEqual(guesses.size,E.guesses[n].length);
 for(const w of guesses)assert(new RegExp('^[A-Z]{'+n+'}$').test(w),w);
 assert(E.banks[n].length>=40);assert.strictEqual(new Set(E.banks[n]).size,E.banks[n].length);
 for(const w of E.banks[n])assert(guesses.has(w),w);
 for(const theme of Object.values(E.themes)){assert(theme[n].length>=5);assert.strictEqual(new Set(theme[n]).size,theme[n].length);for(const w of theme[n])assert(guesses.has(w),w);}
 assert(E.ladders[n].length>=1);
 for(const route of E.ladders[n]){
  assert(route.length>=4&&route.length<=13);assert.strictEqual(new Set(route).size,route.length);
  assert(E.banks[n].includes(route[0])&&E.banks[n].includes(route[route.length-1]));
  route.forEach((w,i)=>{assert(guesses.has(w),w);if(i)assert.strictEqual([...w].filter((c,j)=>c!==route[i-1][j]).length,1);});
 }
}
for(const w of ['COLOUR','COLOR','CENTRE','CENTER','ORGANISE','ORGANIZE','THEATRE','THEATER'])assert(E.guesses[w.length].includes(w),w);
const revision=fs.readFileSync('vendor/english/REVISION','utf8');assert(revision.includes('4f1df64b2e8e14751aa7c2205d170ca016071315'));
for(const line of revision.split('\n')){const m=line.match(/^([a-f0-9]{64})  (.+)$/);if(m)assert.strictEqual(crypto.createHash('sha256').update(fs.readFileSync('vendor/english/'+m[2])).digest('hex'),m[1]);}
// Verify editorial answers against the original source dictionaries, independent of
// generated guesses (which deliberately also include editorial/theme selections).
const editorialWords=[].concat(...Object.values(E.banks));
const sourceAccepted=new Set();
for(const dialect of ['en_GB','en_US']){
 const checked=cp.execFileSync('hunspell',['-d',require('path').resolve('vendor/english/'+dialect),'-i','UTF-8','-G'],{input:editorialWords.map(w=>w.toLowerCase()).join('\n')+'\n',encoding:'utf8'});
 checked.trim().split('\n').forEach(w=>sourceAccepted.add(w.toUpperCase()));
}
for(const word of editorialWords)assert(sourceAccepted.has(word),'Editorial answer rejected as lowercase by both source dictionaries: '+word);
assert(!E.banks[8].includes('DECEMBER')&&!E.banks[8].includes('NOVEMBER'));
const before=fs.readFileSync('public/english.js');cp.execFileSync('python3',['scripts/build-english.py']);assert(before.equals(fs.readFileSync('public/english.js')),'reproducible English build');
assert(fs.readFileSync('public/english-license.txt','utf8').includes('Kevin Atkinson'));
console.log('English content: editorial banks, accepted guesses, six themes, verified ladders, source hashes and reproducibility passed.');
