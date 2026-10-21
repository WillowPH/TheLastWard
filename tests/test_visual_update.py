"""Apply the small update to the previously delivered project and run it."""
from pathlib import Path
from playwright.sync_api import sync_playwright
from mouse_controls import turn_room
import hashlib,json,subprocess,tempfile,zipfile,urllib.request,time,sys
ROOT=Path(__file__).resolve().parents[1]
patch=ROOT/'downloads/The_Last_Ward_Visual_Update.zip';checks=[];errors=[];failed=[]
with tempfile.TemporaryDirectory(prefix='ward-visual-update-') as tmp:
 base=Path(tmp)/'base.zip'
 with base.open('wb') as f:subprocess.run(['git','show','f8e45b0758b32d00bec1b263d35c09e724ef6cce:downloads/The_Last_Ward_Chapter_1_Project.zip'],cwd=ROOT,stdout=f,check=True)
 with zipfile.ZipFile(base) as z:assert z.testzip() is None;z.extractall(tmp)
 project=Path(tmp)/'The_Last_Ward_Project'
 with zipfile.ZipFile(patch) as z:assert z.testzip() is None;z.extractall(project)
 for folder in ['js','css','assets','audio','data']:
  for f in (ROOT/folder).rglob('*'):
   if f.is_file():assert f.read_bytes()==(project/f.relative_to(ROOT)).read_bytes(),str(f)
 for name in ['index.html','START_GAME.exe','START_GAME.bat','README.md','VALIDATION.md','ONLINE_ART.md','server/ward_art_server.py','server/README.md','docs/ROOM_VIEW_SETUP.md','docs/REVISION_V6.md','docs/REVISION_V7.md','docs/REVISION_V8.md','docs/REVISION_V9.md','docs/REVISION_2026-10-19.md']:assert (ROOT/name).read_bytes()==(project/name).read_bytes()
 checks.append('applying update to the previous delivered project reproduces every current code/data/asset/audio file byte for byte')
 proc=subprocess.Popen(['/tmp/ward-launcher','--root',str(project),'--no-browser','--port','8126'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
 try:
  for _ in range(100):
   try:urllib.request.urlopen('http://127.0.0.1:8126',timeout=1);break
   except OSError:time.sleep(.1)
  with sync_playwright() as p:
   b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);c=b.new_context(service_workers='block',viewport={'width':1672,'height':941});c.route('**/*',lambda r:r.continue_() if r.request.url.startswith('http://127.0.0.1:8126/') else r.abort());q=c.new_page();q.on('pageerror',lambda e:errors.append(str(e)));q.on('response',lambda r:failed.append(str(r.status)+' '+r.url) if r.status>=400 else None);q.goto('http://127.0.0.1:8126');q.get_by_role('button',name='BEGIN INVESTIGATION').click();q.evaluate('nextIntro();nextIntro();nextIntro()');q.wait_for_function('WardWinter.roomViewRenderer()?.loaded');assert q.evaluate('WardChapter.BUILD')=='last-ward-ch1-chapter-review-9';before=q.evaluate('S.roomView');turn_room(q);q.wait_for_function('WardWinter.roomViewRenderer()?.loaded&&!WardWinter.orbit.busy');assert q.evaluate('S.roomView')!=before;assert not q.get_by_role('combobox',name='Look at a point of interest').count();assert not errors,errors;assert not failed,failed;b.close()
  checks.append('patched project launches with native server and mouse-only room views, without external internet')
 finally:proc.terminate();proc.wait(timeout=5)
result={'checks':checks,'javascript_errors':errors,'failed_resources':failed,'bytes':patch.stat().st_size,'sha256':hashlib.sha256(patch.read_bytes()).hexdigest()}
(ROOT/'tests/results/visual_update.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
