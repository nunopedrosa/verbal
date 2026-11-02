/* Additive schema1 vocabulary validation; missing language retains Portuguese identities. */
(function(root){'use strict';
var C=typeof module==='object'&&module.exports?require('./core.js'):root.VerbalCore,V=typeof module==='object'&&module.exports?require('./variants.js'):root.VerbalVariants;
function validate(value,banks,guesses){return C.validate(value,banks,function(data,b){
 if(data.prefs.wordLanguage!==undefined&&['pt','en'].indexOf(data.prefs.wordLanguage)<0)throw Error('word language');
 V.validateCollection(data,b,guesses);
 if(data.english===undefined)return;
 var en=data.english;if(!en||typeof en!=='object'||Array.isArray(en)||Object.keys(en).some(function(k){return ['games','variants','nextFree'].indexOf(k)<0;}))throw Error('english collection');
 var E=typeof module==='object'&&module.exports?require('./english.js'):root.VerbalEnglish,prefs=Object.assign({},data.prefs);delete prefs.challenge;
 C.validate({format:'verbal',schema:1,prefs:prefs,games:en.games,variants:en.variants,nextFree:en.nextFree},E.banks,function(nested,eb){V.validateCollection(nested,eb,E.guesses,'en');});
 Object.keys(en.games).forEach(function(k){var g=en.games[k],n=Number(k.slice(-1));g.guesses.forEach(function(w){if(!V.allowed(E.guesses[n],w))throw Error('english guess');});});
 if(Object.keys(data.games).length+Object.keys(data.variants||{}).length+Object.keys(en.games).length+Object.keys(en.variants||{}).length>10000)throw Error('limit');
 });}
var api={validate:validate};if(typeof module==='object'&&module.exports)module.exports=api;else root.VerbalVocabulary=api;
})(this);
