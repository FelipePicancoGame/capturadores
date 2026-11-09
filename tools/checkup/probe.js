/* node probe.js <lang> <steps.json> → out/probe/<nome>.png ; steps: [[nome,codigo,espera_ms]] */
const {chromium}=require('playwright');const fs=require('fs'),path=require('path');
const LANG=process.argv[2]||'pt',STEPS=JSON.parse(fs.readFileSync(process.argv[3],'utf8'));const OUT=path.join(__dirname,'out','probe');fs.mkdirSync(OUT,{recursive:true});
let S=JSON.parse(fs.readFileSync(path.join(__dirname,'..','audit','save2.txt'),'utf8'));S.flags.nome='Enzo';S.flags.tid=12345;S.flags.tut={world:1,battle:1,wall:1,surv:1,td:1,exp:1,match:1,arena:1};S.flags.gems=200;S.flags.lang=LANG;S.flags.house=1;
if(process.env.SAVEJS)eval(process.env.SAVEJS);S=JSON.stringify(S);
(async()=>{const br=await chromium.launch();const pg=await br.newPage({deviceScaleFactor:1,viewport:{width:+(process.env.VW||390),height:+(process.env.VH||844)},hasTouch:true});const errs=[];pg.on('pageerror',e=>errs.push(String(e).slice(0,200)));pg.on('console',m=>{if(m.type()==='error'||m.text().startsWith('P:'))console.log('console',m.text().slice(0,300))});
await pg.route('https://script.google.com/**',r=>r.fulfill({status:200,contentType:'application/json',headers:{'access-control-allow-origin':'*'},body:'{"ok":1,"premios":[]}'}));
await pg.addInitScript(([s,l])=>{localStorage.setItem('capturadores-vale-v1',s);localStorage.setItem('cv.lang',l);},[S,LANG]);
await pg.goto('http://localhost:8790/audit.html#semsom');
for(let i=0;i<25;i++){await pg.waitForTimeout(700);if(await pg.evaluate(()=>window.__GM&&__GM()==='title'))break;}
const X=c=>pg.evaluate(c=>__X(c),c);
for(let i=0;i<40;i++){const ok=await X("(()=>{const u=ui[ui.length-1];if(u&&u.cfg&&u.cfg.title&&Array.isArray(u.opts)&&u.opts[0]==='CONTINUAR'){ui.pop();u.res(0);return 1;}return G.mode==='world'?2:0;})()");if(ok)break;await pg.waitForTimeout(500);}
for(let i=0;i<30;i++){await pg.waitForTimeout(500);if(await X("G.mode==='world'&&party.length>0"))break;}await pg.waitForTimeout(2000);
for(let j=0;j<8;j++){await X(`(()=>{const u=ui[ui.length-1];if(u){ui.pop();try{u.res&&u.res(-1)}catch(e){}}})()`);await pg.waitForTimeout(150);}
for(const [name,code,wait] of STEPS){let r;try{r=await X(`(()=>{try{const r=(${code});return typeof r==='object'?JSON.stringify(r).slice(0,1500):String(r).slice(0,1500);}catch(e){return 'ERR '+e}})()`);}catch(e){r='ERRX '+String(e).slice(0,200)}
  if(r&&r!=='undefined'&&r!=='1'&&r!=='true')console.log(name,'=>',r);await pg.waitForTimeout(wait||1500);if(name[0]!=='_')await pg.screenshot({path:path.join(OUT,name+'.png')});}
console.log('errs',errs);await br.close();})();
