# Preenche o texto da loja (App Store Connect) pela API: nome, subtítulo, descrição, palavras-chave, categoria, idade, URLs.
# Aprovado pelo Felipe em 15/nov. Uso: python loja.py  (segredos iguais ao produtos.py)
import os, time, json, jwt, requests
APP_BUNDLE='com.capturadoresdovale.app'
B='https://api.appstoreconnect.apple.com'
def tok():
    k=os.environ['ASC_KEY_P8'];return jwt.encode({'iss':os.environ['ASC_ISSUER_ID'],'iat':int(time.time()),'exp':int(time.time())+1100,'aud':'appstoreconnect-v1'},k,algorithm='ES256',headers={'kid':os.environ['ASC_KEY_ID'],'typ':'JWT'})
H=lambda:{'Authorization':'Bearer '+tok(),'Content-Type':'application/json'}
def req(m,u,body=None):
    r=requests.request(m,B+u,headers=H(),data=json.dumps(body) if body else None)
    if r.status_code>=300: print('ERRO',m,u,r.status_code,r.text[:700]);return None
    print('ok',m,u.split('?')[0]);return r.json() if r.text else {}
SITE='https://felipepicancogame.github.io/capturadores/'
TXT={
 'en-US':dict(name='Capturadores do Vale',subtitle='7 monster games in 1',
   promo='Catch monsters, defend the wall, survive the horde and battle friends — seven games in one adventure!',
   desc="Explore the Valley, catch and train cute monsters, and live an adventure with your partner.\n\nPlay 7 games in 1:\n• Story — an adventure RPG with your first monster\n• Wall — tower defense against monster waves\n• Horde — survive and beat the boss\n• Towers — build towers and hold the path\n• Expedition — send your team on idle adventures\n• Match — match-3 puzzle that powers up your monsters\n• Arena — play with friends\n\nYour monsters level up everywhere you play. Collect them all, evolve them and complete the Valley's story.\n\nFree to play, with optional purchases and optional ads.",
   kw='monsters,catch,tower defense,rpg,idle,match 3,survival,arena,adventure,pets,evolve,valley'),
 'pt-BR':dict(name='Capturadores do Vale',subtitle='7 jogos de monstrinhos em 1',
   promo='Capture monstrinhos, defenda a muralha, sobreviva à horda e jogue com amigos — sete jogos numa aventura só!',
   desc="Explore o Vale, capture e treine monstrinhos e viva uma aventura com o seu parceiro.\n\nSão 7 jogos em 1:\n• História — uma aventura com o seu primeiro monstrinho\n• Muralha — defenda a muralha das ondas de monstrinhos\n• Horda — sobreviva e vença o chefe\n• Torres — construa torres e segure o caminho\n• Expedição — mande sua equipe em aventuras automáticas\n• Combina — quebra-cabeça de 3 iguais que fortalece seus monstrinhos\n• Arena — jogue com os amigos\n\nSeus monstrinhos sobem de nível em todos os jogos. Capture todos, evolua e complete a história do Vale.\n\nGrátis, com compras e anúncios opcionais.",
   kw='monstrinhos,capturar,tower defense,rpg,idle,3 iguais,sobrevivência,arena,aventura,evoluir,vale'),
}
app=req('GET',f'/v1/apps?filter[bundleId]={APP_BUNDLE}')['data'][0];AID=app['id'];print('app',AID,'idioma principal',app['attributes'].get('primaryLocale'))
# --- appInfo (nome, subtítulo, privacidade, categoria, idade)
infos=req('GET',f'/v1/apps/{AID}/appInfos')['data']
info=[i for i in infos if i['attributes'].get('appStoreState') not in ('READY_FOR_SALE','REPLACED_WITH_NEW_INFO')] or infos
iid=info[0]['id'];print('appInfo',iid,info[0]['attributes'])
req('PATCH',f'/v1/appInfos/{iid}',{'data':{'type':'appInfos','id':iid,'relationships':{
  'primaryCategory':{'data':{'type':'appCategories','id':'GAMES'}},
  'primarySubcategoryOne':{'data':{'type':'appCategories','id':'GAMES_ADVENTURE'}},
  'primarySubcategoryTwo':{'data':{'type':'appCategories','id':'GAMES_ROLE_PLAYING'}}}}})
locs={x['attributes']['locale']:x['id'] for x in req('GET',f'/v1/appInfos/{iid}/appInfoLocalizations')['data']}
for lc,t in TXT.items():
    a={'name':t['name'],'subtitle':t['subtitle'],'privacyPolicyUrl':SITE+'privacidade.html'}
    if lc in locs: req('PATCH',f'/v1/appInfoLocalizations/{locs[lc]}',{'data':{'type':'appInfoLocalizations','id':locs[lc],'attributes':a}})
    else: req('POST','/v1/appInfoLocalizations',{'data':{'type':'appInfoLocalizations','attributes':dict(a,locale=lc),'relationships':{'appInfo':{'data':{'type':'appInfos','id':iid}}}}})
# idade 9+: só violência leve de desenho
ar=req('GET',f'/v1/appInfos/{iid}/ageRatingDeclaration')
if ar:
    aid=ar['data']['id'];print('idade antes',ar['data']['attributes'])
    attrs={k:('NONE' if isinstance(v,str) else (False if isinstance(v,bool) else v)) for k,v in ar['data']['attributes'].items() if v is not None or k in('violenceCartoonOrFantasy',)}
    for k in list(ar['data']['attributes'].keys()):
        v=ar['data']['attributes'][k]
        if v is None:
            if k in('gambling','unrestrictedWebAccess','lootBox','messagingAndChat','userGeneratedContent','parentalControls','ageAssurance','healthOrWellnessTopics','advertising'):attrs[k]=False
            elif k in('kidsAgeBand','ageRatingOverride','ageRatingOverrideV2','koreaAgeRatingOverride'):pass
            else:attrs[k]='NONE'
    attrs['violenceCartoonOrFantasy']='INFREQUENT_OR_MILD'
    if 'advertising' in ar['data']['attributes']:attrs['advertising']=True
    for k in('kidsAgeBand','ageRatingOverride','ageRatingOverrideV2','koreaAgeRatingOverride'):attrs.pop(k,None)
    req('PATCH',f'/v1/ageRatingDeclarations/{aid}',{'data':{'type':'ageRatingDeclarations','id':aid,'attributes':attrs}})
# --- versão (descrição, palavras-chave, texto promocional, URLs, copyright)
vs=req('GET',f'/v1/apps/{AID}/appStoreVersions?filter[platform]=IOS&limit=10')['data']
v=[x for x in vs if x['attributes']['appStoreState'] in('PREPARE_FOR_SUBMISSION','DEVELOPER_REJECTED','REJECTED','METADATA_REJECTED')]
if not v:
    r=req('POST','/v1/appStoreVersions',{'data':{'type':'appStoreVersions','attributes':{'platform':'IOS','versionString':'1.0.0'},'relationships':{'app':{'data':{'type':'apps','id':AID}}}}});v=[r['data']]
vid=v[0]['id'];print('versão',vid,v[0]['attributes'].get('versionString'),v[0]['attributes'].get('appStoreState'))
req('PATCH',f'/v1/appStoreVersions/{vid}',{'data':{'type':'appStoreVersions','id':vid,'attributes':{'copyright':'2026 FPimpulse LLC'}}})
vl={x['attributes']['locale']:x['id'] for x in req('GET',f'/v1/appStoreVersions/{vid}/appStoreVersionLocalizations')['data']}
for lc,t in TXT.items():
    a={'description':t['desc'],'keywords':t['kw'],'promotionalText':t['promo'],'supportUrl':SITE+'suporte.html','marketingUrl':SITE}
    if lc in vl: req('PATCH',f'/v1/appStoreVersionLocalizations/{vl[lc]}',{'data':{'type':'appStoreVersionLocalizations','id':vl[lc],'attributes':a}})
    else: req('POST','/v1/appStoreVersionLocalizations',{'data':{'type':'appStoreVersionLocalizations','attributes':dict(a,locale=lc),'relationships':{'appStoreVersion':{'data':{'type':'appStoreVersions','id':vid}}}}})
print('FIM')
