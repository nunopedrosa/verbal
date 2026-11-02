const assert=require('node:assert/strict'),V=require('../public/variants.js');
const token=V.encode('HOUSE','en');assert(token.startsWith('2.en.'));assert.equal(V.tokenLanguage(token),'en');assert.equal(V.decode(token),'HOUSE');assert.equal(V.tokenLanguage(V.encode('CASA')),'pt');assert.throws(()=>V.decode(token.replace('2.en.','2.pt.')));console.log('PASS language-bound challenge tokens and legacy tokens');

const E=require('../public/english.js'),P=require('../public/paper.js');
for(const n of [4,5,6,7,8])for(const kind of ['strict','double','theme','progressive','ladder','clue','deduction','friend']){
 const options={language:'en',theme:'nature',token:V.encode(E.banks[n][0],'en')},g=V.create(kind,n,'daily:2026-11-02',E.banks,options);
 assert.deepEqual(g,V.create(kind,n,'daily:2026-11-02',E.banks,options));
 if(kind==='ladder'){const routes=E.ladders[n],path=routes.find(p=>p[0]===g.start&&p[p.length-1]===g.answers[0]);for(const w of path.slice(1))assert.equal(V.submit(g,w,E.guesses[n]),null);}
 else if(kind==='progressive'){for(let size=4;size<=8;size++){assert.equal(V.submit(g,V.answers(g)[0],E.guesses[size]),null);if(size<8)assert(V.advance(g));}}
 else for(const answer of g.answers)assert.equal(V.submit(g,answer,E.guesses[n]),null);
 assert.equal(V.status(g),'win');const data={prefs:{},games:{},variants:{[V.key(g)]:g}};V.validateCollection(data,E.banks,E.guesses,'en');
 if(kind==='deduction')assert(P.vocabulary(P.get(g.puzzleId))==='en');
}
assert.throws(()=>V.create('friend',5,'free:1',E.banks,{language:'en',token:V.encode('CASA')}));
console.log('PASS every English mode at every length, canonical backups, deterministic puzzles and language-bound links');
