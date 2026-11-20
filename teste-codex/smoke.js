// Teste rápido da cópia isolada: node teste-codex/smoke.js [URL]  (padrão http://localhost:8790/audit.html)
// Confere: faixa de teste, save de teste carregado, nada gravado na chave oficial, sem service worker, abre uma fase da Arena.
const {chromium}=require('playwright');
const URL=process.argv[2]||'http://localhost:8790/audit.html';
(async()=>{const br=await chromium.launch();const pg=await br.newPage({viewport:{width:375,height:667},deviceScaleFactor:2});
 const erros=[],rede=[];pg.on('pageerror',e=>erros.push(e.message));pg.on('request',r=>{if(/script\.google|supabase\.co/.test(r.url()))rede.push(r.url());});
 await pg.goto(URL+(URL.includes('?')?'&':'?')+'reset=1',{waitUntil:'domcontentloaded',timeout:120000});
 for(let i=0;i<120;i++){await pg.waitForTimeout(1000);if(await pg.evaluate(()=>window.__GM&&__GM()==='title').catch(()=>0))break;}
 // tela inicial: toca CONTINUAR (carrega o save de teste)
 for(let i=0;i<60;i++){const ok=await pg.evaluate(()=>__X("(()=>{const u=ui[ui.length-1];if(u&&u.cfg&&u.cfg.title&&Array.isArray(u.opts)&&u.opts[0]==='CONTINUAR'){ui.pop();u.res(0);return 1;}return 0;})()")).catch(()=>0);if(ok)break;await pg.waitForTimeout(500);}
 for(let i=0;i<60;i++){await pg.waitForTimeout(1000);if(await pg.evaluate(()=>__X("G.mode==='world'&&party.length>0")).catch(()=>0))break;}
 await pg.waitForTimeout(2000);
 const r=await pg.evaluate(()=>({teste:window.CV_TESTE,party:__X('party.length'),chavesReais:(()=>{const o=[];for(let i=0;i<window.localStorage.length;i++)o.push(localStorage.key(i));return o.length;})(),
   brutoOficial:Object.getOwnPropertyDescriptor(Storage.prototype,'length')?null:null,sw:navigator.serviceWorker?navigator.serviceWorker.controller==null:true}));
 const cru=await pg.evaluate(()=>{const raw=[];for(const n in window.localStorage)raw.push(n);return raw.filter(n=>!n.startsWith('TESTE_CODEX::')&&!/^(length|key|getItem|setItem|removeItem|clear)$/.test(n));});
 await pg.evaluate(()=>__X("(ui.forEach(u=>{try{u.res&&u.res(0)}catch(e){}}),ui.length=0,STG={mode:'arena',i:0,bio:BIOMES[0],mult:.85},arenaStage(),1)"));
 await pg.waitForTimeout(4000);await pg.screenshot({path:'teste-codex/smoke_arena.png'});
 console.log(JSON.stringify({...r,chavesForaDoPrefixo:cru,redeReal:rede.length,modo:await pg.evaluate(()=>__X('G.mode')),erros:erros.slice(0,5)},null,1));await br.close();})();
