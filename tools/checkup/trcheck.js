const {chromium}=require('playwright');const fs=require('fs'),path=require('path');
(async()=>{const L=JSON.parse(fs.readFileSync(path.join(__dirname,'lits.json'),'utf8'));const br=await chromium.launch();const pg=await br.newPage();
await pg.addInitScript(()=>{localStorage.setItem('cv.lang','en')});await pg.goto('http://localhost:8790/audit.html#semsom');
for(let i=0;i<25;i++){await pg.waitForTimeout(700);if(await pg.evaluate(()=>window.__GM&&__GM()==='title'))break;}
const r=await pg.evaluate(L=>{window.CVLANG='en';const miss=[];for(const s of L){let t;try{t=window.tr(s);}catch(e){t=s;}if(t===s)miss.push(s);}return {lang:window.CVLANG,n:L.length,miss};},L);
fs.writeFileSync(path.join(__dirname,'tr_miss.json'),JSON.stringify(r.miss,null,0));console.log(r.lang,r.n,r.miss.length);await br.close();})();
