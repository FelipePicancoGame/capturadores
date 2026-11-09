/* CHECK-UP GERAL: node checkup.js <pt|en> <grupo>  → fotos em checkup/out/<lang>/ e textos em checkup/out/<lang>_<grupo>.json */
const {chromium}=require('playwright');const fs=require('fs'),path=require('path');
const LANG=process.argv[2]||'pt',GRP=process.argv[3]||'menus';const STEPS=JSON.parse(fs.readFileSync(path.join(__dirname,'steps.json'),'utf8'))[GRP];
const OUT=path.join(__dirname,'out',LANG);fs.mkdirSync(OUT,{recursive:true});
let S=JSON.parse(fs.readFileSync(path.join(__dirname,'..','audit','save2.txt'),'utf8'));S.flags.nome='Enzo';S.flags.tid=12345;S.flags.tut={world:1,battle:1,wall:1,surv:1,td:1,exp:1,match:1,arena:1};S.flags.gems=200;S.flags.lang=LANG;S.flags.house=1;S=JSON.stringify(S);
(async()=>{const br=await chromium.launch();const pg=await br.newPage({deviceScaleFactor:1,viewport:{width:390,height:844},hasTouch:true});const errs=[];pg.on('pageerror',e=>errs.push(String(e).slice(0,200)));
await pg.route('https://script.google.com/**',r=>r.fulfill({status:200,contentType:'application/json',headers:{'access-control-allow-origin':'*'},body:'{"ok":1,"premios":[]}'}));
await pg.addInitScript(([s,l])=>{localStorage.setItem('capturadores-vale-v1',s);localStorage.setItem('cv.lang',l);window.__TX=new Set();const F=CanvasRenderingContext2D.prototype.fillText;CanvasRenderingContext2D.prototype.fillText=function(t,...a){try{if(this.canvas&&this.canvas.width>60)window.__TX.add(String(t))}catch(e){}return F.call(this,t,...a)};},[S,LANG]);
await pg.goto('http://localhost:8790/audit.html#semsom');
for(let i=0;i<25;i++){await pg.waitForTimeout(700);if(await pg.evaluate(()=>window.__GM&&__GM()==='title'))break;}
await pg.waitForTimeout(1500);await pg.screenshot({path:path.join(OUT,'00_titulo.png')});
const X=c=>pg.evaluate(c=>__X(c),c);
const grab=async()=>pg.evaluate(()=>{const o=[...window.__TX];window.__TX.clear();const d=[];document.querySelectorAll('body *').forEach(e=>{const cs=getComputedStyle(e);if(cs.display==='none'||cs.visibility==='hidden')return;if(e.offsetParent===null&&cs.position!=='fixed')return;for(const c of e.childNodes)if(c.nodeType===3&&c.nodeValue.trim())d.push(c.nodeValue.trim());});return [...new Set(o.concat(d))];});
const out={_title:await grab()};
for(let i=0;i<40;i++){const ok=await X("(()=>{const u=ui[ui.length-1];if(u&&u.cfg&&u.cfg.title&&Array.isArray(u.opts)&&u.opts[0]==='CONTINUAR'){ui.pop();u.res(0);return 1;}return G.mode==='world'?2:0;})()");if(ok)break;await pg.waitForTimeout(500);}
for(let i=0;i<30;i++){await pg.waitForTimeout(500);if(await X("G.mode==='world'&&party.length>0"))break;}await pg.waitForTimeout(2500);
const pop=async()=>{for(let j=0;j<8;j++){await X(`(()=>{const u=ui[ui.length-1];if(u){ui.pop();try{u.res&&u.res(-1)}catch(e){}}try{if(typeof AR!=='undefined'&&AR&&AR.pick)AR.pick({k:'x'})}catch(e){}})()`);await pg.waitForTimeout(200);}try{await X("(()=>{const h=document.getElementById('arHub');if(h)h.remove();document.querySelectorAll('.say,#sayBox').forEach(e=>e.click&&e.click());})()");}catch(e){}};
await pop();await grab();
for(const [name,code,wait] of STEPS){try{await X(`setTimeout(()=>{try{const r=(${code});if(r&&r.catch)r.catch(e=>console.warn('step',e));}catch(e){window.__STEPERR=String(e)}},0);1`);}catch(e){out[name]=['ERRO '+String(e).slice(0,140)];continue;}
  await pg.waitForTimeout(wait||2500);await pg.screenshot({path:path.join(OUT,name+'.png')});out[name]=await grab();const se=await X('window.__STEPERR||""');if(se){out[name].unshift('ERRO '+se);await X('window.__STEPERR="";1');}
  if(!GRP.startsWith('play_')){await pop();await pg.waitForTimeout(600);}else{for(let j=0;j<3;j++){await X(`(()=>{const u=ui[ui.length-1];if(u&&u.cfg&&(u.cfg.say||u.cfg.text||u.cfg.tut||u.cfg.cadAsk||u.cfg.noCancel)){ui.pop();try{u.res&&u.res(0)}catch(e){}}})()`);await pg.waitForTimeout(150);}}}
out._errs=errs;fs.writeFileSync(path.join(__dirname,'out',LANG+'_'+GRP+'.json'),JSON.stringify(out,null,1));console.log('ok',LANG,GRP,Object.keys(out).length,'errs',errs.length);await br.close();})();
