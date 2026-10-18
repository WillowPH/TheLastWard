"""Build the source archive, reproducible offline cache and self-contained HTML."""
from pathlib import Path
import base64,hashlib,json,mimetypes,re,sys,zipfile
ROOT=Path(__file__).resolve().parents[1]
OUT=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else ROOT.parent/'artifacts/chapter1'
OUT.mkdir(parents=True,exist_ok=True)
# Only actual runtime files are cached. No legacy/deleted rooms, tests or downloads.
runtime=[ROOT/'index.html']+[p for folder in ['js','css','assets','audio'] for p in (ROOT/folder).rglob('*') if p.is_file() and p.suffix.lower() in ['.js','.css','.png','.webp','.svg','.ogg','.ttf']]
cache_hash=hashlib.sha256()
for p in sorted(runtime):cache_hash.update(p.relative_to(ROOT).as_posix().encode()+p.read_bytes())
cache='last-ward-ch1-'+cache_hash.hexdigest()[:14]
urls=['./']+['./'+p.relative_to(ROOT).as_posix() for p in sorted(runtime)]
(ROOT/'sw.js').write_text("const CACHE="+json.dumps(cache)+";\nconst ESSENTIAL="+json.dumps(urls)+";\n"+'''
self.addEventListener('install',e=>e.waitUntil(caches.open(CACHE).then(c=>c.addAll(ESSENTIAL)).then(()=>self.skipWaiting())));
self.addEventListener('activate',e=>e.waitUntil(caches.keys().then(keys=>Promise.all(keys.filter(k=>k.startsWith('last-ward-')&&k!==CACHE).map(k=>caches.delete(k)))).then(()=>self.clients.claim())));
self.addEventListener('fetch',e=>{if(e.request.method!=='GET'||new URL(e.request.url).origin!==location.origin)return;e.respondWith(caches.match(e.request).then(cached=>cached||fetch(e.request).then(response=>{if(response.ok){const copy=response.clone();caches.open(CACHE).then(c=>c.put(e.request,copy));}return response;}).catch(()=>new Response('This optional resource is not available offline.',{status:503}))));});
''')
def data(path):
 return 'data:'+(mimetypes.guess_type(path.name)[0] or 'application/octet-stream')+';base64,'+base64.b64encode(path.read_bytes()).decode()
assets={p.relative_to(ROOT).as_posix():data(p) for p in runtime if p.suffix.lower() in ['.png','.webp','.svg','.ogg','.ttf']}
html=(ROOT/'index.html').read_text()
def css(m):
 p=ROOT/m[1]
 def url(v):
  value=v[1].strip('"\'')
  if value.startswith(('data:','http:','https:','#')):return v[0]
  target=(p.parent/value).resolve()
  if not target.is_file():raise FileNotFoundError('Missing CSS asset: '+str(target))
  return 'url("'+data(target)+'")'
 return '<style>'+re.sub(r'url\(([^)]+)\)',url,p.read_text())+'</style>'
html=re.sub(r'<link rel="stylesheet" href="([^"]+)">',css,html)
licenses={str(p.relative_to(ROOT)):p.read_text() for p in [ROOT/'assets/fonts/OFL.txt',ROOT/'assets/fonts/Caveat-OFL.txt',ROOT/'audio/CC0-LICENSE.txt']}
boot='<script>window.WardEmbeddedAssets='+json.dumps(assets,separators=(',',':'))+';</script><script type="application/json" id="bundled-asset-licenses">'+json.dumps(licenses).replace('</','<\\/')+'</script>'
html=html.replace('<script src="js/bootstrap.js">',boot+'<script src="js/bootstrap.js">')
html=re.sub(r'<script src="([^"]+)"></script>',lambda m:'<script>\n'+(ROOT/m[1]).read_text().replace('</script','<\\/script')+'\n</script>',html)
html=re.sub(r'<script>if\(location.protocol.startsWith\("http"\).*?</script>','',html)
standalone=OUT/'The_Last_Ward_Chapter_1.html';standalone.write_text(html)
# A separate player ZIP contains the actual standalone, not just source files.
player_archive=OUT/'The_Last_Ward_Chapter_1_Play.zip'
with zipfile.ZipFile(player_archive,'w',zipfile.ZIP_DEFLATED) as z:
 z.write(standalone,standalone.name)
 z.writestr('START_HERE.txt','THE LAST WARD — CHAPTER 1\n\nExtract this ZIP completely. Open The_Last_Ward_Chapter_1.html in Chrome or Edge.\nStart a NEW GAME and press Begin Investigation to enable sound.\nThe HTML contains all artwork, fonts, audio and code. No server or internet is required.\nKeep saves in the same browser; export a terminal record before moving browsers.\n')
# A source ZIP avoids recursively including previous generated builds.
archive=OUT/'The_Last_Ward_Chapter_1_Source.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
 for p in sorted(ROOT.rglob('*')):
  rel=p.relative_to(ROOT)
  if not p.is_file() or any(part in ['.git','__pycache__','downloads'] for part in rel.parts) or p.suffix=='.pyc':continue
  if rel.parts[:2]==('tests','results') and p.suffix!='.json':continue
  z.write(p,'The_Last_Ward_Project/'+rel.as_posix())
print(json.dumps({'cache':cache,'runtime_files':len(runtime),'standalone':str(standalone),'standalone_bytes':standalone.stat().st_size,'source_zip':str(archive),'source_zip_bytes':archive.stat().st_size,'play_zip':str(player_archive),'play_zip_bytes':player_archive.stat().st_size},indent=2))
