const assert=require('node:assert/strict'),L=require('../public/vocabulary.js');
const fs=require('node:fs'),vm=require('node:vm'),ctx={};vm.createContext(ctx);vm.runInContext(fs.readFileSync('public/words.js','utf8')+';this.b=BANKS;',ctx);vm.runInContext(fs.readFileSync('public/guesses.js','utf8')+';this.g=GUESSES;',ctx);
const original={format:'verbal',schema:1,prefs:{language:'en',length:5,mode:'daily'},games:{},nextFree:1};assert.equal(L.validate(original,ctx.b,ctx.g),original);const bad=JSON.parse(JSON.stringify(original));bad.prefs.wordLanguage='fr';assert.throws(()=>L.validate(bad,ctx.b,ctx.g));console.log('PASS old backup and unknown word language validation');

const E=require('../public/english.js'),V=require('../public/variants.js');
const wrongPreference=JSON.parse(JSON.stringify(original));wrongPreference.prefs.challenge=V.encode('HOUSE','en');assert.throws(()=>L.validate(wrongPreference,ctx.b,ctx.g));
const value=JSON.parse(JSON.stringify(original));value.prefs.wordLanguage='en';value.prefs.englishChallenge=V.encode('HOUSE','en');value.english={games:{'daily:2026-11-02:5':{answer:E.banks[5][0],guesses:[],draft:'HO'}},variants:{},nextFree:1};
const g=V.create('double',5,'free:1',E.banks,{language:'en'});value.english.variants[V.key(g)]=g;L.validate(value,ctx.b,ctx.g);assert.deepEqual(L.validate(JSON.parse(JSON.stringify(value)),ctx.b,ctx.g),value);
for(const mutate of [v=>v.english.games['daily:2026-11-02:5'].answer='ZZZZZ',v=>v.english.variants[V.key(g)].answers=['ZZZZZ'],v=>v.english.nextFree=0,v=>v.prefs.englishChallenge=V.encode('CASA'),v=>v.english.games['daily:2026-11-02:5'].guesses=['ZZZZZ']]){const bad=JSON.parse(JSON.stringify(value));mutate(bad);assert.throws(()=>L.validate(bad,ctx.b,ctx.g));}
console.log('PASS additive English backup round-trip and corrupted/cross-language record rejection');


