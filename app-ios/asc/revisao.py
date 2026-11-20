# Manda a foto de revisão de cada compra (App Store Connect). Página 0 da loja = cristais/energia/passe/raro/2x/auto; página 1 = moedas, sem anúncios, monstrinho novo.
# Segredos: ASC_KEY_ID, ASC_ISSUER_ID, ASC_KEY_P8. Pula compra que já tem foto.
import os,time,json,hashlib,jwt,requests
APP_BUNDLE='com.capturadoresdovale.app';P=APP_BUNDLE+'.';B='https://api.appstoreconnect.apple.com'
DIR=os.path.join(os.path.dirname(__file__),'revisao')
PG0='cristais100 cristais550 cristais1200 energia passe30 monstrinhoraro dobro automatico'.split()
def tok():return jwt.encode({'iss':os.environ['ASC_ISSUER_ID'],'iat':int(time.time()),'exp':int(time.time())+1100,'aud':'appstoreconnect-v1'},os.environ['ASC_KEY_P8'],algorithm='ES256',headers={'kid':os.environ['ASC_KEY_ID'],'typ':'JWT'})
H=lambda:{'Authorization':'Bearer '+tok(),'Content-Type':'application/json'}
def req(m,u,body=None):
    r=requests.request(m,B+u,headers=H(),data=json.dumps(body) if body else None)
    if r.status_code>=300:print('ERRO',m,u,r.status_code,r.text[:400]);return None
    return r.json() if r.text else {}
AID=req('GET',f'/v1/apps?filter[bundleId]={APP_BUNDLE}')['data'][0]['id']
d=req('GET',f'/v1/apps/{AID}/inAppPurchasesV2?limit=200') or {'data':[]}
for x in d['data']:
    pid=x['attributes']['productId'];iid=x['id'];short=pid.replace(P,'')
    cur=req('GET',f'/v2/inAppPurchases/{iid}/appStoreReviewScreenshot')
    if cur and cur.get('data') and (cur['data']['attributes'].get('assetDeliveryState') or {}).get('state') in ('COMPLETE','UPLOAD_COMPLETE'):print('já tem',short);continue
    f=os.path.join(DIR,'pagina0.png' if short in PG0 else 'pagina1.png');raw=open(f,'rb').read()
    r=req('POST','/v1/inAppPurchaseAppStoreReviewScreenshots',{'data':{'type':'inAppPurchaseAppStoreReviewScreenshots','attributes':{'fileName':short+'.png','fileSize':len(raw)},'relationships':{'inAppPurchaseV2':{'data':{'type':'inAppPurchases','id':iid}}}}})
    if not r:continue
    sid=r['data']['id']
    for op in r['data']['attributes']['uploadOperations']:
        hd={h['name']:h['value'] for h in op.get('requestHeaders',[])}
        rr=requests.request(op['method'],op['url'],headers=hd,data=raw[op['offset']:op['offset']+op['length']])
        if rr.status_code>=300:print('ERRO upload',short,rr.status_code)
    req('PATCH',f'/v1/inAppPurchaseAppStoreReviewScreenshots/{sid}',{'data':{'type':'inAppPurchaseAppStoreReviewScreenshots','id':sid,'attributes':{'uploaded':True,'sourceFileChecksum':hashlib.md5(raw).hexdigest()}}})
    print('foto ok',short)
print('FIM')
