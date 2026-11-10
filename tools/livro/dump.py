"""Lê os dados do jogo (index.html) no Chrome headless e salva dump.json + img/<monstrinho>.webp.
Uso: python3 tools/livro/dump.py <pasta_saida>   (rodar na raiz do repositório)
Precisa: playwright + google-chrome. Não altera o jogo: monta _livro.html (apagado no fim)."""
import asyncio, base64, json, os, sys, subprocess, time
from playwright.async_api import async_playwright

OUT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else 'out_livro')
os.makedirs(OUT + '/img', exist_ok=True)
src = open('index.html', encoding='utf8').read()
HOOK = ("window.__D=()=>({SP,MOVES,EVO,TYPES,TYPECOL,CHART,ULTNAME,ULTDESC,EVOSTG,EVOBASE,EVOPREV,ARAB,ENC,ARENAS,DEXLIST});"
        "window.__MI=()=>MONIMG;window.__TR=(x)=>{const o=window.CVLANG;window.CVLANG='en';try{return x.map(s=>tr(s));}finally{window.CVLANG=o;}};")
assert 'window.__T={MONANIM,' in src, 'gancho window.__T não encontrado'
open('_livro.html', 'w', encoding='utf8').write(src.replace('window.__T={MONANIM,', HOOK + 'window.__T={MONANIM,', 1))
srv = subprocess.Popen([sys.executable, '-m', 'http.server', '8799'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1)

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=os.environ.get('CHROME', '/usr/bin/google-chrome'), args=['--no-sandbox'])
        pg = await b.new_page(viewport={'width': 430, 'height': 900})
        errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)[:300]))
        await pg.add_init_script("try{localStorage.setItem('cv.lang','pt')}catch(e){}")
        await pg.goto('http://localhost:8799/_livro.html#semsom', wait_until='load', timeout=180000)
        await pg.wait_for_timeout(9000)
        d = await pg.evaluate("()=>JSON.parse(JSON.stringify(window.__D(),(k,v)=>typeof v==='function'?'[fn]':v))")
        names = sorted({v['name'] for v in d['MOVES'].values()} | {v for v in d['ULTNAME'].values()})
        en = await pg.evaluate("x=>window.__TR(x)", names)
        import re as _re
        d['EN'] = {n: (e if e != n or not (_re.search(r"['\"]" + _re.escape(n) + r"['\"]\s*:\s*['\"]", src)) else n + ' (dicionário)') for n, e in zip(names, en)}
        d['ERRS'] = errs
        imgs = await pg.evaluate('''async()=>{const M=window.__MI(),out={};for(const k of Object.keys(window.__D().SP)){const I=M[k];if(!I){out[k]=null;continue;}
          if(!I.complete)await new Promise(r=>{I.onload=r;I.onerror=r;setTimeout(r,5000)});if(!I.naturalWidth){out[k]=null;continue;}
          const c=document.createElement('canvas'),sc=Math.min(1,256/Math.max(I.naturalWidth,I.naturalHeight));c.width=Math.round(I.naturalWidth*sc);c.height=Math.round(I.naturalHeight*sc);
          c.getContext('2d').drawImage(I,0,0,c.width,c.height);out[k]={w:I.naturalWidth,h:I.naturalHeight,u:c.toDataURL('image/webp',.9)};}return out;}''')
        d['IMG'] = {}
        for k, v in imgs.items():
            if not v:
                d['IMG'][k] = None; continue
            open(f'{OUT}/img/{k}.webp', 'wb').write(base64.b64decode(v['u'].split(',')[1]))
            d['IMG'][k] = [v['w'], v['h']]
        json.dump(d, open(OUT + '/dump.json', 'w'), ensure_ascii=False)
        await b.close()
try:
    asyncio.run(main())
finally:
    srv.terminate(); os.remove('_livro.html')
print('ok', OUT)
