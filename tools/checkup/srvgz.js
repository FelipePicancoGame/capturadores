const http=require('http'),fs=require('fs'),path=require('path'),zlib=require('zlib');const root=path.join(__dirname,'app');
const T={'.html':'text/html; charset=utf-8','.js':'application/javascript','.json':'application/json','.webp':'image/webp','.png':'image/png','.jpg':'image/jpeg','.mp3':'audio/mpeg','.woff2':'font/woff2','.webmanifest':'application/manifest+json','.svg':'image/svg+xml','.ogg':'audio/ogg','.css':'text/css'};
const gzc=new Map();
http.createServer((q,r)=>{let p=decodeURIComponent(q.url.split('?')[0]);if(p.endsWith('/'))p+='index.html';const f=path.join(root,p);if(!f.startsWith(root))return r.end();
 fs.stat(f,(e,st)=>{if(e||!st.isFile()){r.statusCode=404;return r.end();}const ext=path.extname(f),et='"'+st.size+'-'+st.mtimeMs+'"';
  if(q.headers['if-none-match']===et){r.statusCode=304;return r.end();}
  r.setHeader('Content-Type',T[ext]||'application/octet-stream');r.setHeader('ETag',et);r.setHeader('Cache-Control','max-age=600');
  if(/\.(html|js|json|svg|css|webmanifest)$/.test(ext)&&/gzip/.test(q.headers['accept-encoding']||'')){const k=f+et;let z=gzc.get(k);if(!z){z=zlib.gzipSync(fs.readFileSync(f),{level:6});gzc.set(k,z);}r.setHeader('Content-Encoding','gzip');r.setHeader('Content-Length',z.length);return r.end(z);}
  r.setHeader('Content-Length',st.size);fs.createReadStream(f).pipe(r);});}).listen(8790);
