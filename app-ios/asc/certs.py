# Limpa os certificados de DESENVOLVIMENTO que cada build na nuvem cria (a Apple tem limite e o build trava).
# Não mexe nos de distribuição (os que mandam o app pra loja/TestFlight).
import os, time, jwt, requests
def tok():
    k=os.environ['ASC_KEY_P8'];return jwt.encode({'iss':os.environ['ASC_ISSUER_ID'],'iat':int(time.time()),'exp':int(time.time())+1100,'aud':'appstoreconnect-v1'},k,algorithm='ES256',headers={'kid':os.environ['ASC_KEY_ID'],'typ':'JWT'})
H={'Authorization':'Bearer '+tok()}
r=requests.get('https://api.appstoreconnect.apple.com/v1/certificates?limit=200',headers=H);r.raise_for_status()
C=r.json()['data']
for c in C:
    a=c['attributes'];print('cert',a.get('certificateType'),a.get('name'),a.get('displayName'),a.get('expirationDate'))
dev=[c for c in C if c['attributes'].get('certificateType') in ('DEVELOPMENT','IOS_DEVELOPMENT')]
for c in dev:
    d=requests.delete('https://api.appstoreconnect.apple.com/v1/certificates/'+c['id'],headers=H)
    print('revogado' if d.status_code in (200,204) else 'falhou '+str(d.status_code)+' '+d.text[:200],c['attributes'].get('name'))
print('dev revogados:',len(dev),'de',len(C))
