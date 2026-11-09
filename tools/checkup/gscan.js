const {chromium}=require('playwright');const fs=require('fs'),path=require('path');
(async()=>{const names=fs.readFileSync(path.join(__dirname,'globs.txt'),'utf8').split('\n').filter(Boolean);const br=await chromium.launch();const pg=await br.newPage();
await pg.addInitScript(()=>{localStorage.setItem('cv.lang','en')});await pg.goto('http://localhost:8790/audit.html#semsom');
for(let i=0;i<25;i++){await pg.waitForTimeout(700);if(await pg.evaluate(()=>window.__GM&&__GM()==='title'))break;}
const r=await pg.evaluate(names=>{window.CVLANG='en';const PT=/[ãõçáéíóúâêôàÃÕÇÁÉÍÓÚÂÊÔ]|\b(você|não|com|pra|para|uma|seu|sua|dos|das|toque|jogar|voltar|vida|fase|onda|ganhe|cartas?|monstrinhos?|nível|agora|todos|cada|mais|está|isso|também|ainda|já|hoje|vez|moedas|cristais|loja|novo|nova|derrote|vença|capture|jogue|use|pegue)\b/i;
 const out={};for(const n of names){let v;try{v=__X(n);}catch(e){continue;}if(!v||typeof v!=='object')continue;if(n==='CVEN'||n==='UIK'||/SRC|BLOB|URL|IMG|ANIM/.test(n))continue;const seen=new Set();const L=[];
  const walk=(o,d)=>{if(d>6||o==null)return;if(typeof o==='string'){if(o.length>2&&o.length<600&&PT.test(o)&&!/^(data:|blobs\/|assets\/|\/_blob)/.test(o)){let t;try{t=tr(o);}catch(e){t=o;}if(t===o)L.push(o);}return;}if(typeof o!=='object'||seen.has(o))return;seen.add(o);if(o instanceof HTMLElement||o instanceof Image)return;for(const k in o){try{walk(o[k],d+1);}catch(e){}}};
  walk(v,0);if(L.length)out[n]=[...new Set(L)];}return out;},names);
fs.writeFileSync(path.join(__dirname,'gscan.json'),JSON.stringify(r,null,0));for(const k in r)console.log(k,r[k].length);await br.close();})();
