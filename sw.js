/* Capturadores do Vale — guarda os arquivos do jogo no aparelho pra abrir rápido e funcionar sem internet */
const CACHE='cv-v194';
/* 03/nov: artes e sons ficam numa caixa separada que NÃO é apagada quando sai versão nova (senão o jogo baixado pra jogar offline sumia a cada versão).
   blobs/ têm nome único por conteúdo: nunca mudam. assets/ podem mudar: na versão nova o jogo pergunta ao servidor se mudou (resposta curta 304 se não mudou). */
const ART='cv-arte-1';
self.addEventListener('install',e=>{self.skipWaiting();e.waitUntil(caches.open(CACHE).then(c=>c.addAll(['./','./index.html','./manifest.webmanifest'])).catch(()=>{}));});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==CACHE&&k!==ART).map(k=>caches.delete(k)))).then(()=>self.clients.claim()));});
async function artTag(res){const hd=new Headers(res.headers);hd.set('x-cv',CACHE);const bd=await res.blob();return new Response(bd,{status:200,statusText:'OK',headers:hd});}
async function artGet(r,isA){const c=await caches.open(ART);const m=await c.match(r.url);
  if(m&&(!isA||m.headers.get('x-cv')===CACHE))return m;
  try{const h={};if(m){const et=m.headers.get('etag'),lm=m.headers.get('last-modified');if(et)h['If-None-Match']=et;if(lm)h['If-Modified-Since']=lm;}
    const res=await fetch(r.url,{headers:h,cache:'no-store'});
    if(res.status===304&&m){const nr=await artTag(m);await c.put(r.url,nr.clone());return nr;}
    if(res.ok){const nr=await artTag(res);try{await c.put(r.url,nr.clone());}catch(e){}return nr;}
    return m||res;}catch(e){if(m)return m;throw e;}}
self.addEventListener('fetch',e=>{const r=e.request;if(r.method!=='GET'||new URL(r.url).origin!==location.origin)return;const pn=new URL(r.url).pathname;if(pn.endsWith('/version.json'))return;
  const isPage=r.mode==='navigate'||r.url.endsWith('/index.html');
  if(isPage){/* 29/out: busca a página sempre no servidor (sem cópia guardada do navegador), pra versão nova chegar na hora */e.respondWith(fetch(r,{cache:'no-cache'}).then(res=>{const cp=res.clone();caches.open(CACHE).then(c=>c.put(r,cp));return res;}).catch(()=>caches.match(r).then(m=>m||caches.match('./index.html'))));return;}
  if(!r.headers.has('range')&&(pn.includes('/blobs/')||pn.includes('/assets/'))){e.respondWith(artGet(r,pn.includes('/assets/')));return;}
  e.respondWith(caches.match(r).then(m=>m||fetch(r).then(res=>{if(res.ok){const cp=res.clone();caches.open(CACHE).then(c=>c.put(r,cp));}return res;})));});
