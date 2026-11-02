const assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm'),path=require('node:path');
const context={};vm.createContext(context);vm.runInContext(fs.readFileSync(path.join(__dirname,'../public/words.js'),'utf8')+';this.banks=BANKS;this.old=WORDS;',context);vm.runInContext(fs.readFileSync(path.join(__dirname,'../public/guesses.js'),'utf8')+';this.guesses=GUESSES;',context);
for(const n of [4,5,6,7,8]){const words=context.guesses[n];assert(words.length>context.banks[n].length*5);assert.equal(new Set(words).size,words.length);assert(words.every(w=>w.length===n&&/^[A-Z]+$/.test(w)));assert(context.banks[n].every(w=>words.includes(w)));}
assert(context.old.every(w=>context.guesses[5].includes(w)));
for(const word of ['MAES','CAES','CASAS','MACAS','LIVROS','PAPEIS','ANIMAIS','FLORES','JARDINS','CORACOES','CRIANCAS','CANTO','CANTAS','CANTAMOS'])assert(context.guesses[word.length].includes(word),word);
for(const word of ['ZZZZ','QWERT','CASASS','LIVROSS','JARDINSS'])assert(!context.guesses[word.length].includes(word),word);
console.log('PASS expanded accepted guesses, plurals, conjugations, normalized lengths and preserved answers/legacy guesses');console.log(Object.fromEntries(Object.entries(context.guesses).map(([n,ws])=>[n,ws.length])));
