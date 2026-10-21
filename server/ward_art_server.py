#!/usr/bin/env python3
"""Optional AI-art website backend. Offline game doesn't use this module.

Run from the The_Last_Ward_Project directory:
  WARD_ART_UPSTREAM_URL=https://provider.example/generate \
  WARD_ART_UPSTREAM_KEY=secret python server/ward_art_server.py

Upstream is a configurable image-generation gateway. It receives JSON containing
'prompt', 'room', 'seed' and 'size'. Return {"image_base64":"..."} or
{"data":[{"b64_json":"..."}]} or {"image_url":"https://..."}.
Never put a provider API key into HTML or frontend JS. Rate-limit and authenticate
this endpoint before exposing it to public traffic.
"""
import base64, hashlib, http.server, json, mimetypes, os, pathlib, re, socketserver, tempfile, threading, urllib.request, urllib.parse
ROOT=pathlib.Path(__file__).resolve().parents[1]
GENERATED=ROOT/'generated'
GENERATED.mkdir(exist_ok=True)
HOST=os.environ.get('WARD_HOST','127.0.0.1')
PORT=int(os.environ.get('WARD_PORT','8787'))
UPSTREAM=os.environ.get('WARD_ART_UPSTREAM_URL','')
KEY=os.environ.get('WARD_ART_UPSTREAM_KEY','')
VALID_ROOMS={x.stem for x in (ROOT/'assets'/'rooms').glob('*.webp')}
_CACHE_LOCKS={}
_CACHE_LOCKS_GUARD=threading.Lock()
def _cache_lock(key):
 # Hold the same lock from the cache check through publication, even across tabs.
 with _CACHE_LOCKS_GUARD:
  return _CACHE_LOCKS.setdefault(key,threading.Lock())
def _publish_image(path,img):
 # Readers see either no cache entry or a complete image, never a partial write.
 pending=None
 try:
  with tempfile.NamedTemporaryFile(dir=path.parent,prefix='.'+path.stem+'-',suffix='.tmp',delete=False) as output:
   pending=pathlib.Path(output.name)
   output.write(img)
  os.replace(pending,path)
 finally:
  if pending is not None:pending.unlink(missing_ok=True)
class Handler(http.server.SimpleHTTPRequestHandler):
 def __init__(self,*args,**kwargs):super().__init__(*args,directory=str(ROOT),**kwargs)
 def do_GET(self):
  if urllib.parse.urlsplit(self.path).path=='/data/art_service.json':
   return self.response(200,{'available':bool(UPSTREAM),'endpoint':'/api/ward-art' if UPSTREAM else None})
  return super().do_GET()
 def response(self,status,body):
  data=json.dumps(body).encode();self.send_response(status);self.send_header('Content-Type','application/json');self.send_header('Cache-Control','no-store');self.send_header('Content-Length',str(len(data)));self.end_headers();self.wfile.write(data)
 def do_POST(self):
  if self.path!='/api/ward-art':return self.response(404,{'error':'No such service'})
  if not UPSTREAM:return self.response(503,{'error':'No image provider configured; bundled room artwork remains available.'})
  try:
   length=int(self.headers.get('Content-Length','0'))
   if not 0<length<8192:return self.response(413,{'error':'Invalid request size'})
   payload=json.loads(self.rfile.read(length));room=str(payload.get('room',''))
   if room not in VALID_ROOMS:return self.response(400,{'error':'Unknown room'})
   seed=str(payload.get('seed',''))[:100]
   if not re.fullmatch(r'[A-Za-z0-9_-]{1,100}',seed):return self.response(400,{'error':'Invalid seed'})
   phase='electrified, old fluorescent lights' if bool(payload.get('powered')) else 'emergency lighting, moody darkness'
   prompt=(f'Original 1998-era survival-horror abstract atmospheric dust-and-light texture for the room {room!r} '
    f'in Blackridge Medical Complex. A nonfigurative texture of dust, mist and {phase}. '
    'Monolith Pharmaceuticals industrial-medical aesthetic. NO text, UI, characters, architecture, doors or objects. '
    'The room layout and all doors and puzzle objects are defined by the separately-rendered base art; '
    'this generated image is used only as an atmospheric overlay. Landscape image.')
   h=hashlib.sha256((room+'|'+seed+'|'+str(phase)).encode()).hexdigest()[:32]
   fn=GENERATED/(h+'.png')
   with _cache_lock(h):
    if not fn.exists():
     post=json.dumps({'room':room,'seed':seed,'size':'1536x1024','prompt':prompt}).encode()
     req=urllib.request.Request(UPSTREAM,data=post,headers={'Content-Type':'application/json',**({'Authorization':'Bearer '+KEY} if KEY else {})},method='POST')
     with urllib.request.urlopen(req,timeout=75) as res: content=res.read(10_000_000)
     result=json.loads(content)
     b64=result.get('image_base64') or (result.get('data') or [{}])[0].get('b64_json')
     if b64:img=base64.b64decode(b64,validate=True)
     else:
      u=result.get('image_url') or (result.get('data') or [{}])[0].get('url','')
      if not str(u).startswith('https://'):raise ValueError('Provider did not return an HTTPS image URL or base64 image')
      with urllib.request.urlopen(u,timeout=60) as res:img=res.read(9_000_000)
     if len(img)>8_000_000 or len(img)<100:raise ValueError('Invalid image size')
     if not (img.startswith(b'\x89PNG') or img.startswith(b'\xff\xd8\xff') or img.startswith(b'RIFF')):raise ValueError('Unsupported image format')
     _publish_image(fn,img)
   # serve same-origin image via this server; no provider credentials exposed
   scheme='https' if self.headers.get('X-Forwarded-Proto')=='https' else 'http'
   host=self.headers.get('Host',f'{HOST}:{PORT}')
   if not re.fullmatch(r'[A-Za-z0-9.\-:\[\]]{1,128}',host):host=f'{HOST}:{PORT}'
   return self.response(200,{'image_url':f'{scheme}://{host}/generated/{fn.name}'})
  except Exception:return self.response(502,{'error':'Image service error; local artwork still works.'})
if __name__=='__main__':
 with socketserver.ThreadingTCPServer((HOST,PORT),Handler) as httpd:
  print(f'The Last Ward online art site: http://{HOST}:{PORT}/ (provider configured: {bool(UPSTREAM)})')
  httpd.serve_forever()
