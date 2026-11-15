// AVALIADOR DA MURALHA: todo monstrinho na Muralha tem que estar DE COSTAS (virado pra cima).
// Uso: node murav.js [especie1,especie2,...]  -> out/murav/<especie>.png + out/murav/resultado.json
const {chromium}=require('playwright');const fs=require('fs'),path=require('path');
let S=JSON.parse(fs.readFileSync(path.join(__dirname,'..','audit','save2.txt'),'utf8'));S.flags.tut={world:1,battle:1,wall:1,surv:1,td:1,exp:1,match:1,arena:1};S.flags.lang='pt';S.flags.nome='Enzo';S.flags.vinc={};for(let i=1;i<=80;i++)S.flags.vinc[i]=1;S=JSON.stringify(S);
const OUT=path.join(__dirname,'out','murav');fs.mkdirSync(OUT,{recursive:true});
(async()=>{const br=await chromium.launch();const pg=await br.newPage({viewport:{width:390,height:844}});
await pg.route('https://script.google.com/**',r=>r.fulfill({status:200,contentType:'application/json',headers:{'access-control-allow-origin':'*'},body:'{"ok":1}'}));
await pg.addInitScript(([s])=>{localStorage.setItem('capturadores-vale-v1',s);localStorage.setItem('cv.lang','pt');},[S]);
await pg.goto('http://localhost:8790/audit.html#semsom');for(let i=0;i<25;i++){await pg.waitForTimeout(700);if(await pg.evaluate(()=>window.__GM&&__GM()==='title'))break;}
const X=c=>pg.evaluate(c=>__X(c),c);await pg.waitForTimeout(3000);
const pop=async()=>{for(let j=0;j<6;j++){await X("(()=>{const u=ui[ui.length-1];if(u){ui.pop();try{u.res&&u.res(0)}catch(e){}}return 1})()");await pg.waitForTimeout(200);}};await pop();
let LIST=process.argv[2]?process.argv[2].split(','):await X("DEXLIST.filter(k=>SP[k])");
// espião: anota como cada monstrinho foi desenhado na Muralha
const spy=()=>X(`(()=>{window.__MV={};const o=murMonDraw;murMonDraw=function(d){const base=String(d.sp).replace('*','');let modo=null;const of=drawMonFx;drawMonFx=function(){modo=MONDIR==='costas'?'animacao_costas':'FRENTE';return of.apply(this,arguments)};let r;try{r=o.apply(this,arguments)}finally{drawMonFx=of}
 if(r&&!modo)modo='arte_costas(n_)';if(!r)modo='FRENTE';const S=MONANIM[base+'@costas'];__MV[base]={modo,x:d.x,y:d.y,temCostas:!!S,temN:!!MUR_ART['n_'+base]};return r};return 1})()`);await spy();
const res={};
for(let i=0;i<LIST.length;i+=4){const grp=LIST.slice(i,i+4);
  await X(`(()=>{party.length=0;for(const k of ${JSON.stringify(grp)})party.push(mk(k,12));return 1})()`);
  await X("(()=>{WL=null;stgLaunch('wall',0);return 1})()");await pg.waitForTimeout(2500);
  for(let j=0;j<8;j++){if(await X("typeof WL!=='undefined'&&!!WL"))break;await X("(()=>{const u=ui[ui.length-1];if(u){ui.pop();try{u.res&&u.res(0)}catch(e){}}return 1})()");await pg.waitForTimeout(900);}
  await pg.waitForTimeout(3500);
  const mv=await X("JSON.stringify(__MV)");const M=JSON.parse(mv);
  const cs=await X("(()=>{const c=document.querySelector('canvas');const r=c.getBoundingClientRect();return JSON.stringify({x:r.x,y:r.y,k:r.width/c.width*(c.width/W)})})()");const C=JSON.parse(cs);
  for(const k of grp){const m=M[k];res[k]=m?m.modo:'NAO_APARECEU';}
  await pg.screenshot({path:path.join(OUT,'g'+String(i/4).padStart(2,'0')+'_'+grp.join('-')+'.png'),clip:{x:0,y:560,width:390,height:130}});
  await pg.reload();for(let t=0;t<25;t++){await pg.waitForTimeout(700);if(await pg.evaluate(()=>window.__GM&&__GM()==='title'))break;}await pg.waitForTimeout(2500);await pop();await spy();await X("(()=>{__MV={};return 1})()");
  process.stdout.write(grp.map(k=>k+':'+res[k]).join('  ')+'\n');}
fs.writeFileSync(path.join(OUT,'resultado.json'),JSON.stringify(res,null,1));
const ruins=Object.entries(res).filter(([k,v])=>v!=='animacao_costas'&&v!=='arte_costas(n_)');
console.log(ruins.length?'REPROVADO: '+ruins.map(([k,v])=>k+'='+v).join(', '):'APROVADO: todos de costas');
await br.close();})();
