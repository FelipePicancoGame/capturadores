"""Gera o Livro dos Monstrinhos (HTML) e a lista de problemas a partir do dump.json.
Uso: python3 tools/livro/gen.py <pasta_do_dump> <versao> <data>
Saídas na pasta do dump: livro-monstrinhos.html e problemas.json (só os automáticos)."""
import base64, html, json, os, sys
from collections import Counter
D = sys.argv[1]; VER = sys.argv[2] if len(sys.argv) > 2 else '?'; DATA = sys.argv[3] if len(sys.argv) > 3 else ''
HERE = os.path.dirname(os.path.abspath(__file__))
d = json.load(open(D + '/dump.json'))
SP, MV, EVO, ULT, AR, ENC = d['SP'], d['MOVES'], d['EVO'], d['ULTNAME'], d['ARAB'], d['ENC']
TN, TC, prev, C, EN = d['TYPES'], d['TYPECOL'], d['EVOPREV'], d['CHART'], d.get('EN', {})
esc = lambda s: html.escape(str(s))
dex = set(d['DEXLIST'])
names = lambda ks: ', '.join(SP[k]['name'] for k in ks)

# ---------- linhas de evolução ----------
roots = [k for k in SP if k not in prev]
chains = []
for r in roots:
    c = [r]; x = r
    while x in EVO and EVO[x] and EVO[x][0] in SP and EVO[x][0] not in c:
        c.append(EVO[x][0]); x = EVO[x][0]
    chains.append(c)

# ---------- conferência automática ----------
P = []
def add(sev, t, sub=''): P.append({'sev': sev, 'rot': 'Automático', 't': t, 'sub': sub})
fora = [k for k in SP if k not in dex]
if fora: add('b', f'{len(fora)} monstrinho(s) fora da Coleção: {names(fora)}.', f'A Coleção conta /{len(dex)}, o jogo tem {len(SP)}.')
sem_img = [k for k in SP if not d['IMG'].get(k)]
if sem_img: add('b', f'Sem arte carregando: {names(sem_img)}.')
falta_mv = sorted({m for v in SP.values() for _, m in v['learn'] if m not in MV})
if falta_mv: add('b', f'Golpes que não existem na lista: {", ".join(falta_mv)}.')
for a, A in d['ARENAS'].items():
    if A.get('t') not in TN.values(): add('b', f'Líder {A["n"]} é "tipo {A["t"]}", que não existe no jogo.')
sem_ult = [k for k in SP if not ULT.get(k) or ULT[k].startswith('Especial')]
if sem_ult: add('w', f'Sem especial próprio na Muralha: {names(sem_ult)}.')
sem_ar = [k for k in SP if k not in AR]
if sem_ar: add('w', f'Sem poder na Arena: {names(sem_ar)}.')
parado = [k for k in roots if max(l for l, _ in SP[k]['learn']) < 20]
if parado: add('w', f'Não aprendem golpe novo depois do nível 20: {names(parado)}.')
dup = [k for k in roots if any(n > 1 for n in Counter(l for l, _ in SP[k]['learn'] if l > 1).values())]
if dup: add('w', f'Aprendem 2 golpes no mesmo nível: {names(dup)}.')
usados = {m for v in SP.values() for _, m in v['learn']}
sobra = [MV[m]['name'] for m in MV if m not in usados]
if sobra: add('w', f'Golpes que ninguém aprende: {", ".join(sobra)}.')
T = list(TN)
sem_fraq = [TN[t] for t in T if not any(C.get(a, {}).get(t, 1) > 1 for a in T)]
if sem_fraq: add('w', f'Tipos sem nenhuma fraqueza: {", ".join(sem_fraq)}.')
sem_en = sorted(n for n, e in EN.items() if e == n and any('a' <= ch <= 'z' for ch in n.lower()) and n not in ('Normal', 'Avalanche'))
if sem_en: add('w', f'Sem tradução em inglês: {", ".join(sem_en[:12])}{" …" if len(sem_en) > 12 else ""}.')
peq = [k for k in SP if d['IMG'].get(k) and max(d['IMG'][k]) < 150]
if peq: add('a', f'Arte pequena (pode borrar em tela grande): {names(peq)}.', 'Medido no arquivo original da imagem.')
sem_lan = [k for k in SP if k not in json.load(open(HERE + '/lancar.json'))]
if sem_lan: add('w', f'Sem descrição de como lança o poder: {names(sem_lan)}.')
if d.get('ERRS'): add('b', 'Erros ao abrir o jogo: ' + ' | '.join(d['ERRS'][:3]))
json.dump(P, open(D + '/problemas.json', 'w'), ensure_ascii=False, indent=1)

notas = json.load(open(HERE + '/arte_notas.json'))
LAN = json.load(open(HERE + '/lancar.json'))
LBL = {'b': 'Erro', 'w': 'Falta', 'a': 'Arte'}
def li(p):
    rot = p.get('rot', 'Automático')
    sub = (f'<small>{esc(rot)}' + (f' · {esc(p["sub"])}' if p.get('sub') else '') + '</small>')
    return f'<li><span class="sev {p["sev"]}">{esc(LBL.get(p["sev"], "Nota") if rot == "Automático" else rot)}</span><div><b>{esc(p["t"])}</b>{sub}</div></li>'
issues = ''.join(li(p) for p in P) + ''.join(li(p) for p in notas)
okline = 'Conferência automática: tudo certo.' if not P else f'Conferência automática: {len(P)} item(ns).'

# ---------- onde aparece ----------
AREA = {'route': 'Rota 1', 'town': 'Vila', 'route2': 'Rota 2', 'floresta': 'Floresta', 'lago': 'Lago', 'brisa': 'Porto Brisa', 'bosque': 'Bosque', 'serra': 'Serra', 'dunas': 'Dunas', 'mirante': 'Mirante', 'gruta': 'Gruta', 'mare': 'Maré', 'farol': 'Farol', 'pico': 'Pico', 'cratera': 'Cratera', 'geleira': 'Geleira', 'lunaria': 'Lunária', 'templo': 'Templo'}
where = {}
for a, v in ENC.items():
    for L in v.values():
        for e in L:
            s = f"{AREA.get(a, a)} (nv {e[1]}–{e[2]})"
            if s not in where.setdefault(e[0], []): where[e[0]].append(s)

def img(k):
    p = f'{D}/img/{k}.webp'
    return 'data:image/webp;base64,' + base64.b64encode(open(p, 'rb').read()).decode() if os.path.exists(p) else ''

def lan(k):
    L = LAN.get(k)
    if not L: return '<em>falta</em>'
    tag = '<span class=ok>aprovado</span>' if L.get('ok') else '<span class=prop>proposta</span>'
    return f"<b>{esc(L['de'])}</b> {tag}<br>{esc(L['como'])}"

cards = []
for c in chains:
    parts = []
    for i, k in enumerate(c):
        s = SP[k]; b = s['base']
        lv = '' if i == 0 else f"forma {i+1} · nv {EVO[c[i-1]][1]}"
        mv = ''.join(f"<li><span class=lv>{l}</span>{esc(MV[m]['name'])} <i class='t t-{MV[m]['type']}'>{esc(TN[MV[m]['type']])}</i> <b>{MV[m]['pow'] or '—'}</b></li>" for l, m in sorted(s['learn'], key=lambda x: x[0]) if m in MV)
        ult, ar = ULT.get(k), AR.get(k)
        flags = []
        if k not in dex: flags.append('Fora da Coleção')
        if not ult or ult.startswith('Especial'): flags.append('Sem especial próprio')
        if not ar: flags.append('Sem poder na Arena')
        fl = ''.join(f"<span class=flag>{f}</span>" for f in flags)
        w = where.get(k)
        parts.append(f"""<article class=mon data-t="{s['type']}" data-q="{esc((s['name']+' '+k).lower())}"><div class=pic><img src="{img(k)}" alt="{esc(s['name'])}" loading=lazy></div><div class=info><div class=nm><h3>{esc(s['name'])}</h3><span class="t t-{s['type']}">{esc(TN[s['type']])}</span>{f"<span class=evo>{lv}</span>" if lv else ''}</div><div class=stats><span>Vida <b>{b[0]}</b></span><span>Ataque <b>{b[1]}</b></span><span>Defesa <b>{b[2]}</b></span><span>Velocidade <b>{b[3]}</b></span></div><p class=desc>{esc(s.get('desc',''))}</p><dl><dt>Golpes</dt><dd><ul class=mv>{mv}</ul></dd><dt>Lança o poder pelo(a)</dt><dd>{lan(k)}</dd><dt>Especial (Muralha)</dt><dd>{esc(ult) if ult else '<em>nenhum</em>'}</dd><dt>Poder (Arena)</dt><dd>{(esc(ar['n'])+' — '+esc(ar['d'])) if ar else '<em>nenhum</em>'}</dd><dt>Onde aparece</dt><dd>{esc(', '.join(w[:4])+(' …' if len(w)>4 else '')) if w else 'só por evolução'}</dd></dl><div class=flags>{fl}<span class=id>id: {k}</span></div></div></article>""")
    cards.append(f"<section class=line><h2>Linha {esc(SP[c[0]]['name'])} <small>{len(c)} forma{'s' if len(c)>1 else ''}</small></h2><div class=forms>{''.join(parts)}</div></section>")

def cell(a, b):
    v = C.get(a, {}).get(b, 1)
    return f"<td class='{'x2' if v>1 else 'x5' if v<1 else ''}'>{'2×' if v>1 else '½' if v<1 else ''}</td>"
rows = ''.join(f"<tr><th><span class='t t-{a}'>{TN[a]}</span></th>" + ''.join(cell(a, b) for b in T) + '</tr>' for a in T)
head = ''.join(f"<th><span class='t t-{b}'>{TN[b]}</span></th>" for b in T)
chart = f"<div class=tbl><table><thead><tr><th>Ataca ↓ / Defende →</th>{head}</tr></thead><tbody>{rows}</tbody></table></div>"
tcss = ''.join(f".t-{t}{{--tc:{TC[t]}}}" for t in T)
filt = ''.join(f"<button class='chip t-{t}' data-f='{t}' type=button aria-pressed=false>{TN[t]}</button>" for t in T)
out = (open(HERE + '/tpl.html', encoding='utf8').read()
       .replace('%%ISSUES%%', issues).replace('%%OKLINE%%', okline).replace('%%CARDS%%', ''.join(cards)).replace('%%CHART%%', chart)
       .replace('%%TCSS%%', tcss).replace('%%FILT%%', filt).replace('%%N%%', str(len(SP))).replace('%%NL%%', str(len(chains)))
       .replace('%%NDEX%%', str(len(dex))).replace('%%VER%%', VER).replace('%%DATA%%', DATA))
open(D + '/livro-monstrinhos.html', 'w', encoding='utf8').write(out)
print(len(P), 'problemas automáticos;', len(SP), 'monstrinhos;', len(chains), 'linhas')
