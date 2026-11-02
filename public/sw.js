'use strict';
var VERSION='1.3.2',CACHE='verbal-'+VERSION;
var MANIFEST_HASH='a1e99b8512c2d928054c61006c6ba8581c4e87d79c727c26032c027dc05da208';
function digest(bytes){return crypto.subtle.digest('SHA-256',bytes).then(function(hash){return Array.prototype.map.call(new Uint8Array(hash),function(b){return ('00'+b.toString(16)).slice(-2);}).join('');});}
self.addEventListener('install',function(e){
 e.waitUntil(fetch('./release.json',{cache:'no-store'}).then(function(r){
  if(!r.ok)throw Error('Release manifest unavailable');
  return r.arrayBuffer();
 }).then(function(bytes){
  return digest(bytes).then(function(hash){
   if(hash!==MANIFEST_HASH)throw Error('Release manifest mismatch');
   var manifest=JSON.parse(new TextDecoder().decode(bytes));
   if(manifest.version!==VERSION)throw Error('Release version mismatch');
   return Promise.all(Object.keys(manifest.files).map(function(name){
    return fetch('./'+name,{cache:'no-store'}).then(function(response){
     if(!response.ok)throw Error('Asset unavailable');
     return response.clone().arrayBuffer().then(function(body){
      return digest(body).then(function(actual){
       if(actual!==manifest.files[name])throw Error('Incomplete release: '+name);
       return {name:name,response:response};
      });
     });
    });
   })).then(function(assets){
    return caches.open(CACHE).then(function(cache){
     return Promise.all(assets.map(function(asset){return cache.put('./'+asset.name,asset.response.clone());})).then(function(){
      var index=assets.filter(function(a){return a.name==='index.html';})[0];
      return cache.put('./',index.response.clone());
     });
    });
   });
  });
 }));
});
// Activation is explicit. Old complete caches remain available to old windows.
self.addEventListener('message',function(e){if(e.data&&e.data.type==='ACTIVATE')self.skipWaiting();});
self.addEventListener('activate',function(e){e.waitUntil(self.clients.claim());});
self.addEventListener('fetch',function(e){if(e.request.method!=='GET'||new URL(e.request.url).origin!==self.location.origin)return;e.respondWith(caches.open(CACHE).then(function(cache){return cache.match(e.request).then(function(r){if(r)return r;if(e.request.mode==='navigate')return cache.match('./index.html');return fetch(e.request);});}));});
