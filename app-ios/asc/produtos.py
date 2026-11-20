# Cria (ou completa) as compras do jogo no App Store Connect pela API.
# Segredos: ASC_KEY_ID, ASC_ISSUER_ID, ASC_KEY_P8. Uso: python produtos.py
import os, time, json, jwt, requests
APP_BUNDLE='com.capturadoresdovale.app'; P=APP_BUNDLE+'.'
PRODS=[  # id, tipo, preço US$, nome PT, descrição PT, nome EN, descrição EN
 ('cristais100','CONSUMABLE','0.99','Punhado de Cristais','100 cristais','Handful of Crystals','100 crystals'),
 ('cristais550','CONSUMABLE','4.99','Saco de Cristais','550 cristais','Bag of Crystals','550 crystals'),
 ('cristais1200','CONSUMABLE','9.99','Baú de Cristais','1.200 cristais','Chest of Crystals','1,200 crystals'),
 ('energia','CONSUMABLE','0.99','Energia Cheia','Energia cheia + 30','Full Energy','Full energy + 30'),
 ('monstrinhoraro','CONSUMABLE','9.99','Monstrinho Raro','Um monstrinho raro + 100 cristais','Rare Monster','A rare monster + 100 crystals'),
 ('moedas5000','CONSUMABLE','0.99','5.000 Moedas','Pacote de 5.000 moedas','5,000 Coins','Pack of 5,000 coins'),
 ('moedas12000','CONSUMABLE','1.99','12.000 Moedas','Pacote de 12.000 moedas','12,000 Coins','Pack of 12,000 coins'),
 ('moedas30000','CONSUMABLE','4.99','30.000 Moedas','Pacote de 30.000 moedas','30,000 Coins','Pack of 30,000 coins'),
 ('moedas70000','CONSUMABLE','9.99','70.000 Moedas','Pacote de 70.000 moedas','70,000 Coins','Pack of 70,000 coins'),
 ('moedas150000','CONSUMABLE','19.99','150.000 Moedas','Pacote de 150.000 moedas','150,000 Coins','Pack of 150,000 coins'),
 ('moedas400000','CONSUMABLE','49.99','400.000 Moedas','Pacote de 400.000 moedas','400,000 Coins','Pack of 400,000 coins'),
 ('dobro','NON_CONSUMABLE','4.99','2x Pra Sempre','Velocidade 2x em todos os modos','2x Forever','2x speed in every mode'),
 ('automatico','NON_CONSUMABLE','4.99','Automático Pra Sempre','Modo automático em todos os modos','Auto Forever','Auto mode in every mode'),
 ('semanuncios','NON_CONSUMABLE','4.99','Sem Anúncios','Sem anúncios e prêmios a 140%','No Ads','No ads and 140% prizes'),
 ('monstronovo','CONSUMABLE','4.99','Monstrinho Novo','O monstrinho novo da vez','New Monster','The newest monster'),
 ('passe30','NON_RENEWING_SUBSCRIPTION','4.99','Passe do Mês','50 cristais por dia por 30 dias','Month Pass','50 crystals a day for 30 days'),
]
B='https://api.appstoreconnect.apple.com'
def tok():
    k=os.environ['ASC_KEY_P8'];return jwt.encode({'iss':os.environ['ASC_ISSUER_ID'],'iat':int(time.time()),'exp':int(time.time())+1100,'aud':'appstoreconnect-v1'},k,algorithm='ES256',headers={'kid':os.environ['ASC_KEY_ID'],'typ':'JWT'})
H=lambda:{'Authorization':'Bearer '+tok(),'Content-Type':'application/json'}
def req(m,u,body=None):
    r=requests.request(m,B+u,headers=H(),data=json.dumps(body) if body else None)
    if r.status_code>=300: print('ERRO',m,u,r.status_code,r.text[:500]);return None
    return r.json() if r.text else {}
app=req('GET',f'/v1/apps?filter[bundleId]={APP_BUNDLE}')['data'][0];AID=app['id'];print('app',AID)
have={}
u=f'/v1/apps/{AID}/inAppPurchasesV2?limit=200'
d=req('GET',u)
for x in (d or {}).get('data',[]):have[x['attributes']['productId']]=x['id']
for pid,typ,price,npt,dpt,nen,den in PRODS:
    full=P+pid
    if full in have: iid=have[full];print('existe',full)
    else:
        r=req('POST','/v2/inAppPurchases',{'data':{'type':'inAppPurchases','attributes':{'name':npt,'productId':full,'inAppPurchaseType':typ,'familySharable':False},'relationships':{'app':{'data':{'type':'apps','id':AID}}}}})
        if not r: continue
        iid=r['data']['id'];print('criado',full)
    locs=req('GET',f'/v2/inAppPurchases/{iid}/inAppPurchaseLocalizations') or {'data':[]}
    lh={x['attributes']['locale'] for x in locs['data']}
    for loc,n,dd in (('pt-BR',npt,dpt),('en-US',nen,den)):
        if loc not in lh:
            req('POST','/v1/inAppPurchaseLocalizations',{'data':{'type':'inAppPurchaseLocalizations','attributes':{'locale':loc,'name':n,'description':dd},'relationships':{'inAppPurchaseV2':{'data':{'type':'inAppPurchases','id':iid}}}}})
    pp=req('GET',f'/v2/inAppPurchases/{iid}/pricePoints?filter[territory]=USA&limit=800') or {'data':[]}
    pt=[x for x in pp['data'] if x['attributes']['customerPrice']==price]
    if not pt: print('sem preço',full,price);continue
    req('POST','/v1/inAppPurchasePriceSchedules',{'data':{'type':'inAppPurchasePriceSchedules','relationships':{'inAppPurchase':{'data':{'type':'inAppPurchases','id':iid}},'baseTerritory':{'data':{'type':'territories','id':'USA'}},'manualPrices':{'data':[{'type':'inAppPurchasePrices','id':'${p0}'}]}}},'included':[{'type':'inAppPurchasePrices','id':'${p0}','attributes':{'startDate':None},'relationships':{'inAppPurchasePricePoint':{'data':{'type':'inAppPurchasePricePoints','id':pt[0]['id']}}}}]})
    req('POST','/v1/inAppPurchaseAvailabilities',{'data':{'type':'inAppPurchaseAvailabilities','attributes':{'availableInNewTerritories':True},'relationships':{'inAppPurchase':{'data':{'type':'inAppPurchases','id':iid}},'availableTerritories':{'data':[]}}}})
    print('ok',full,price)
print('FIM')
