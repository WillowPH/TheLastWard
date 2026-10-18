"""Build the multi-file project archive and reproducible offline cache."""
from pathlib import Path
import hashlib,json,sys,zipfile
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
# The requested deliverable preserves all source and assets as separate files.
archive=OUT/'The_Last_Ward_Chapter_1_Project.zip'
count=0
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
 for p in sorted(ROOT.rglob('*')):
  rel=p.relative_to(ROOT)
  if not p.is_file() or any(part in ['.git','__pycache__','downloads'] for part in rel.parts) or p.suffix=='.pyc':continue
  if rel.parts[:2]==('docs','review') and p.suffix.lower() in ['.png','.jpg','.jpeg','.webp']:continue # historical review captures are not game assets
  if rel.parts[:2]==('tests','results') and (p.suffix!='.json' or p.name in ['winter_package.json','visual_update.json']):continue # package hash report lives outside its own archive
  z.write(p,'The_Last_Ward_Project/'+rel.as_posix());count+=1
print(json.dumps({'cache':cache,'runtime_files':len(runtime),'project_zip':str(archive),'project_zip_bytes':archive.stat().st_size,'project_files':count,'format':'multi-file source and assets; no embedded standalone generated'},indent=2))
