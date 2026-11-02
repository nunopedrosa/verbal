'use strict';
const assert=require('assert'),fs=require('fs'),C=require('../public/core.js'),P=require('../public/paper.js'),E=require('../public/english.js');
const score=(g,a)=>C.score(g,a).map(s=>({correct:'=',present:'~',absent:'x'})[s]).join('');
assert.equal(P.englishData.length,1671);assert.deepStrictEqual(P.englishData.slice(0,200),JSON.parse(fs.readFileSync(__dirname+'/fixtures/paper-en-200.json')));assert.equal(new Set(P.englishData.map(p=>p.answer)).size,P.englishData.length);
assert.deepStrictEqual(P.data.slice(0,60),JSON.parse(fs.readFileSync(__dirname+'/fixtures/paper-v1.json')));
const codes=new Set();
P.englishData.forEach(p=>{
 assert.equal(P.get(p.id),p);assert.equal(P.vocabulary(p),'en');assert(/^[EF][4-8]-\d{3}$/.test(P.code(p)));assert(!codes.has(P.code(p)));codes.add(P.code(p));
 assert(E.banks[p.length].includes(p.answer));assert(p.bank.length<=12);assert(p.clues.length<=3);assert.equal(new Set(p.bank).size,p.bank.length);
 p.bank.concat(p.clues.map(c=>c.word)).forEach(w=>{assert(new RegExp('^[A-Z]{'+p.length+'}$').test(w));assert(E.guesses[p.length].includes(w));});
 p.clues.forEach(c=>assert.equal(c.score,score(c.word,p.answer)));
 assert.deepStrictEqual(p.bank.filter(w=>p.clues.every(c=>score(c.word,w)===c.score)),[p.answer]);
 p.clues.forEach((_,omit)=>assert(p.bank.filter(w=>p.clues.every((c,i)=>i===omit||score(c.word,w)===c.score)).length>1));
 // Exercise actual layout and PDF byte generation for every record in a valid pack.
 const pack=[p].concat(P.englishData.filter(q=>q.id!==p.id).slice(0,3));
 for(const lang of ['pt','en']){
  const html=P.html(pack,lang,true),pdf=Buffer.from(P.pdf(pack,lang,true)).toString('latin1');
  assert(html.includes(lang==='pt'?'Palavras inglesas':'English words'));assert(pdf.startsWith('%PDF-1.4'));assert(pdf.includes('/Count 2'));assert(pdf.includes(p.answer));assert(pdf.includes(P.code(p)));
 }
});
for(let n=4;n<=8;n++){
 assert(P.englishData.filter(p=>p.length===n).length>=40);
 assert.equal(P.choose(n,'stable').id,P.choose(n,'stable','pt').id);assert.equal(P.vocabulary(P.choose(n,'stable','en')),'en');const original=JSON.parse(fs.readFileSync(__dirname+'/fixtures/paper-en-200.json')).filter(p=>p.length===n);assert.deepStrictEqual(P.choose(n,'stable','en'),original[require('../public/variants.js').hash('stable:deduction:'+n)%original.length]);
 const pool=P.englishData.filter(p=>p.length===n),ids=pool.map(p=>p.id);
 assert.throws(()=>P.pack('exhausted',4,n,ids,'en'),/exhausted/);
 const last=P.pack('last',4,n,ids.slice(0,-4),'en');assert.deepStrictEqual(last.map(p=>p.id).sort(),ids.slice(-4).sort());
}
const en=P.pack('history',12,0,[],'en'),pt=P.pack('history',12,0);
assert.deepStrictEqual(en,P.pack('history',12,0,[],'en'));
assert.throws(()=>P.validPack([en[0],pt[0],en[1],en[2]]),/mixed/);
assert.throws(()=>P.choose(4,'x','fr'),/language/);assert.throws(()=>P.pack('x',4,4,[],'fr'),/language/);
const h=P.record(P.record({},pt,'pdf',1),en,'print',2);P.validateHistory(h);assert.equal(Object.keys(h).length,24);
assert(P.pack('skip',12,0,en.map(p=>p.id),'en').every(p=>!h[p.id]));
for(const lang of ['pt','en'])for(const wordLang of ['pt','en'])for(const count of [4,12])for(const solutions of [false,true]){
 const pack=P.pack('export',count,0,[],wordLang),pdf=Buffer.from(P.pdf(pack,lang,solutions)).toString('latin1'),html=P.html(pack,lang,solutions),pages=count/4+(solutions?1:0);
 const xref=Number(pdf.match(/startxref\n(\d+)/)[1]);assert.equal(pdf.slice(xref,xref+4),'xref');
 const entries=pdf.slice(xref).split('\n').slice(3).filter(line=>/^\d{10} 00000 n /.test(line));entries.forEach((entry,i)=>assert(pdf.slice(Number(entry.slice(0,10))).startsWith((i+1)+' 0 obj')));
 assert(pdf.includes('/Count '+pages));assert.equal((html.match(/class="paper-page"/g)||[]).length,pages);
 assert(pdf.includes(wordLang==='en'?(lang==='pt'?'Palavras inglesas':'English words'):(lang==='pt'?'Palavras portuguesas':'Portuguese words')));
}
console.log('PASS English paper: catalogue scoring, essential clues, immutable PT, bilingual exports, history and exhaustion');

const used=[];while(P.englishData.length-used.length>=4){const batch=P.pack('exhaust-all:'+used.length,4,0,used,'en');assert(batch.every(p=>!used.includes(p.id)));used.push(...batch.map(p=>p.id));}assert.equal(used.length,1668);assert.throws(()=>P.pack('last-three',4,0,used,'en'),/exhausted/);assert(P.pack('repeat',4,0,[],'en').length===4);
const originals=JSON.parse(fs.readFileSync(__dirname+'/fixtures/paper-en-200.json'));const newPack=P.pack('new-print',12,0,originals.map(p=>p.id),'en');assert(newPack.every(p=>p.id.startsWith('paper-en-print-v2-')));P.validateHistory(P.record({},newPack,'pdf',Date.now()));console.log('PASS full English catalogue exhaustion, explicit repeat and print-only selection');
