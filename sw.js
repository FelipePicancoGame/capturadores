/* Capturadores do Vale — guarda os arquivos do jogo no aparelho pra abrir rápido e funcionar sem internet */
const CACHE='cv-v517';
/* 03/nov: artes e sons ficam numa caixa separada que NÃO é apagada quando sai versão nova (senão o jogo baixado pra jogar offline sumia a cada versão).
   blobs/ têm nome único por conteúdo: nunca mudam. assets/ podem mudar: na versão nova o jogo pergunta ao servidor se mudou (resposta curta 304 se não mudou). */
const ART='cv-arte-1';
self.addEventListener('install',e=>{self.skipWaiting();e.waitUntil(caches.open(CACHE).then(c=>c.addAll(['./','./index.html','./manifest.webmanifest'])).catch(()=>{}));});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==CACHE&&k!==ART).map(k=>caches.delete(k)))).then(()=>self.clients.claim()));});
async function artFresh(r,c,m){const h={};const et=m.headers.get('etag'),lm=m.headers.get('last-modified');if(et)h['If-None-Match']=et;if(lm)h['If-Modified-Since']=lm;
  const res=await fetch(r.url,{headers:h,cache:'no-store'});if(res.status===304){await c.put(r.url,await artTag(m));return;}if(res.ok)await c.put(r.url,await artTag(res));}
async function artTag(res){const hd=new Headers(res.headers);hd.set('x-cv',CACHE);const bd=await res.blob();return new Response(bd,{status:200,statusText:'OK',headers:hd});}
async function artGet(r,isA,ev){const c=await caches.open(ART);const m=await c.match(r.url);
  if(m&&(!isA||m.headers.get('x-cv')===CACHE))return m;
  /* 12/nov (Felipe: 'no celular da Gabi as telas do Buchecha aparecem direto, no meu aparecem as telas velhas por baixo'): depois de cada versão nova o jogo
     esperava o servidor conferir CADA arte antes de mostrar — quem atualiza sempre via a tela antiga enquanto isso. Agora mostra na hora a arte guardada
     e confere com o servidor por trás (se mudou, a nova aparece na próxima vez). */
  if(m&&isA&&ev){ev.waitUntil(artFresh(r,c,m.clone()).catch(()=>{}));return m;}
  try{const h={};if(m){const et=m.headers.get('etag'),lm=m.headers.get('last-modified');if(et)h['If-None-Match']=et;if(lm)h['If-Modified-Since']=lm;}
    const res=await fetch(r.url,{headers:h,cache:'no-store'});
    if(res.status===304&&m){const nr=await artTag(m);await c.put(r.url,nr.clone());return nr;}
    if(res.ok){const nr=await artTag(res);try{await c.put(r.url,nr.clone());}catch(e){}return nr;}
    return m||res;}catch(e){if(m)return m;throw e;}}
async function swRange(r){try{let m=null;for(const k of [ART,CACHE]){const c=await caches.open(k);m=await c.match(r.url,{ignoreVary:true});if(m)break;}
  if(!m){return fetch(r);}const buf=await m.arrayBuffer(),n=buf.byteLength,mm=/bytes=(\d*)-(\d*)/.exec(r.headers.get('range')||'');if(!mm)return fetch(r);
  let s0=mm[1]===''?Math.max(0,n-(+mm[2]||0)):+mm[1],e0=(mm[1]!==''&&mm[2]!=='')?Math.min(+mm[2],n-1):n-1;if(s0>=n)return new Response(null,{status:416,headers:{'Content-Range':'bytes */'+n}});
  return new Response(buf.slice(s0,e0+1),{status:206,statusText:'Partial Content',headers:{'Content-Type':m.headers.get('content-type')||'audio/mpeg','Content-Range':'bytes '+s0+'-'+e0+'/'+n,'Content-Length':String(e0-s0+1),'Accept-Ranges':'bytes'}});}
  catch(e){return fetch(r);}}
self.addEventListener('fetch',e=>{const r=e.request;if(r.method!=='GET'||new URL(r.url).origin!==location.origin)return;const pn=new URL(r.url).pathname;if(pn.endsWith('/version.json'))return;
  const isPage=r.mode==='navigate'||r.url.endsWith('/index.html');
  if(isPage){/* 29/out: busca a página sempre no servidor (sem cópia guardada do navegador), pra versão nova chegar na hora */e.respondWith(fetch(r,{cache:'no-cache'}).then(res=>{const cp=res.clone();caches.open(CACHE).then(c=>c.put(r,cp));return res;}).catch(()=>caches.match(r).then(m=>m||caches.match('./index.html'))));return;}
  if(!r.headers.has('range')&&(pn.includes('/blobs/')||pn.includes('/assets/'))){e.respondWith(artGet(r,pn.includes('/assets/'),e));return;}
  /* SOMIOS13NOV (Felipe: 'no celular os áudios não entram, no Tesla entram na hora'): o iPhone toca som pedindo PEDAÇOS do arquivo (Range) e só aceita resposta 206;
     a cópia guardada voltava o arquivo inteiro (200) e o Safari travava/cancelava a voz. O Chrome do Tesla aceita os dois. Agora devolve o pedaço certo (206). */
  if(r.headers.has('range')){e.respondWith(swRange(r));return;}
  e.respondWith(caches.match(r).then(m=>m||fetch(r).then(res=>{if(res.ok){const cp=res.clone();caches.open(CACHE).then(c=>c.put(r,cp));}return res;})));});
