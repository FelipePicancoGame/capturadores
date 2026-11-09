import sys
f=sys.argv[1];s=open(f).read();orig=s
blk=open('reps09.js').read()
R=[
 ("d:(d)=>`${MOVES[d.mv].name} alcança 15% mais longe`","d:(d)=>`Alcance: ${MOVES[d.mv].name} acerta 15% mais longe`",1),
 ("d:(d,v)=>`${MOVES[d.mv].name} alcança ${v}% mais longe`","d:(d,v)=>`Alcance: ${MOVES[d.mv].name} acerta ${v}% mais longe`",1),
 ("ukT(o.n,x+170,y+190,26,'#2a1a10','center',300);if(o.d)ukT(o.d,x+170,y+215,17,","ukT(o.n,x+170,y+189,31,'#2a1a10','center',300);if(o.d)ukT(o.d,x+170,y+216,22,",1),
 ("lojGeneric(x,y,{n:it.n,d:ukShort(it.d,34),ic:it.ic,it:sk&&sk.k});ukT(it.tag||'',x+75,y+249,18,","lojGeneric(x,y,{n:it.n,d:ukShort(it.d,30),ic:it.ic,it:sk&&sk.k});ukT(it.tag||'',x+75,y+249,23,",1),
 ("ukT(LOJUPD[u2.k]||ukShort(it.d,34),x+170,y+209,17,","ukT(LOJUPD[u2.k]||ukShort(it.d,30),x+170,y+210,22,",1),
 ("x+20,y+228,15,'#6a5a7a','left',165)","x+20,y+229,19,'#6a5a7a','left',165)",2),
 ("ukT(lv>=5?PWD[it.t][4]:PWD[it.t][lv],x+170,y+209,17,","ukT(lv>=5?PWD[it.t][4]:PWD[it.t][lv],x+170,y+210,22,",1),
 ("if(it.who)ukT(it.who,x+170,y+20,18,","if(it.who)ukT(it.who,x+170,y+20,22,",1),
 ("const KK=()=>{const k=Math.min(W/627,H/1254);return {k,ox:(W-627*k)/2,oy:(H-1254*k)/2};};","const KK=()=>{const k=Math.min(W/627,H/1254);return {k,ox:(W-627*k)/2+(window.__MRDX||0)*k,oy:(H-1254*k)/2};};",1),
 ("b.drawImage(MRB[key],t.ox,t.oy,627*t.k,1254*t.k);b.restore();}","b.drawImage(MRB[key],t.ox,t.oy,627*t.k,1254*t.k);const dx=(window.__MRDX||0)*t.k;if(dx>0){/* R269: beirada esquerda com a pedra da própria arte (espelhada) */b.translate(t.ox,0);b.scale(-1,1);b.drawImage(MRB[key],0,0,window.__MRDX+2,1254,0,t.oy,dx+2*t.k,1254*t.k);}b.restore();}",1),
 ("if(SI)b.drawImage(SI,X(P[2]-ss*1.5+s3*ss),Y(P[3]-ss/2),ss*k,ss*k);}","if(SI)b.drawImage(SI,X(P[2]-ss*1.5+s3*ss),Y(P[3]-ss/2),ss*k,ss*k);else star(X(P[2]-ss*1.5+s3*ss+ss/2),Y(P[3]),ss*k*.42,s3<stars?'#ffd040':'#6a5a48');}",2),
 ("let f=Math.min(BH*.86,CAP?CAP*sy:BH);b.save();const fn=()=>`800 ${f}px CadBaloo","let f=/^btv_v4_/.test(n)?BH*1.3:Math.min(BH*.86,CAP?CAP*sy:BH);b.save();const fn=()=>`800 ${f}px CadBaloo",1),
 ("id==null&&bc==='#ff5a4a'?'chance_inimigo':null;if(key&&v4chip(key,txt,id,u))return;","id==null&&bc==='#ff5a4a'?'chance_inimigo':id==null&&bc==='#b8b0d8'&&V4ok()?'chance_jogador':null;if(key&&v4chip(key,txt,id,u))return;",1),
 ("mv.type==='normal'?'c_normal':null","mv.type==='normal'?'c_normal':(BTVR['c_t_'+mv.type]?'c_t_'+mv.type:null)",1),
]
for a,b2,n in R:
  c=s.count(a)
  if c!=n: print('MISS',c,a[:70]);continue
  s=s.replace(a,b2)
k='window.__T={MONANIM,'
assert s.count(k)==1
if '/* REPS09NOV' not in s: s=s.replace(k,blk+'\n'+k,1)
open(f,'w').write(s);print('ok',f,len(orig),len(s))
