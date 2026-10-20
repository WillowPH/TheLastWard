"""Extract and run the complete multi-file project with external requests blocked."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json,sys,zipfile,subprocess,tempfile,time,urllib.request,hashlib,struct
ROOT=Path(__file__).resolve().parents[1]
archive=Path(sys.argv[1]) if len(sys.argv)>1 else ROOT/'downloads/The_Last_Ward_Chapter_1_Project.zip'
checks=[];errors=[];failures=[]
with tempfile.TemporaryDirectory(prefix='last-ward-package-') as tmp:
 with zipfile.ZipFile(archive) as z:
  assert z.testzip() is None;z.extractall(tmp);names=z.namelist()
 project=Path(tmp)/'The_Last_Ward_Project'
 assert (project/'index.html').stat().st_size<100000
 for folder in ['js','css','assets','audio','data']:assert any((project/folder).rglob('*'))
 world=json.loads((project/'data/room_views.json').read_text());assert len(world)==27
 assert all((project/view['asset']).exists() for room in world.values() for view in room['views'].values())
 exe=(project/'START_GAME.exe').read_bytes();assert exe[:2]==b'MZ';pe=struct.unpack_from('<I',exe,0x3c)[0];assert exe[pe:pe+4]==b'PE\0\0' and struct.unpack_from('<H',exe,pe+4)[0]==0x8664
 checks.append('Windows x64 native launcher is included with valid PE headers')
 for folder in ['js','css','assets','audio','data']:
  for f in (ROOT/folder).rglob('*'):
   if f.is_file():assert hashlib.sha256(f.read_bytes()).digest()==hashlib.sha256((project/f.relative_to(ROOT)).read_bytes()).digest(),str(f)
 for name in ['README.md','VALIDATION.md','docs/REVISION_V6.md','docs/REVISION_V7.md','tools/package_visual_update.py']:assert (ROOT/name).read_bytes()==(project/name).read_bytes(),name
 checks.append('archive matches tested runtime source, assets, correction notes and packager byte for byte')
 checks.append('archive extracts with separate code, data, audio, 54 native room-facing views and launchers')
 command=([sys.argv[2],'--root',str(project)] if len(sys.argv)>2 else [sys.executable,str(project/'start_game.py')])+['--no-browser','--port','8124']
 proc=subprocess.Popen(command,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
 try:
  for _ in range(100):
   try:urllib.request.urlopen('http://127.0.0.1:8124',timeout=1);break
   except OSError:time.sleep(.1)
  with sync_playwright() as p:
   b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--enable-unsafe-swiftshader']);c=b.new_context(service_workers='block',viewport={'width':1672,'height':941});c.route('**/*',lambda r:r.continue_() if r.request.url.startswith('http://127.0.0.1:8124/') else r.abort());page=c.new_page();page.on('pageerror',lambda e:errors.append(str(e)));page.on('requestfailed',lambda r:failures.append(r.url));page.goto('http://127.0.0.1:8124');page.get_by_role('button',name='BEGIN INVESTIGATION').click();page.evaluate('nextIntro();nextIntro();nextIntro()');page.wait_for_function('!!S&&!!WardWinter.orbit');assert page.evaluate('WardChapter.BUILD')=='last-ward-ch1-chapter-review-7';assert not page.locator('.mouse-look-edge').count();checks.append(('native server' if len(sys.argv)>2 else 'Python launcher')+' starts the extracted playable game without external internet')
   page.evaluate("WardSound.play('winter_wind',{volume:.8,loop:true})");values=[]
   for _ in range(12):page.wait_for_timeout(100);values.append(page.evaluate('WardSound.energy()'))
   assert max(values)>.00001;checks.append('separate local audio produces measured output after Begin')
   page.evaluate("S.enemyActors.forEach(a=>a.hp=0);S.pursuer.active=false")
   for room in page.evaluate('Object.keys(R)'):
    page.evaluate('r=>{S.room=r;S.roomViewRoom=null;renderScene()}',room);page.wait_for_function("WardWinter.roomViewRenderer()?.loaded")
    for face in ['front','rear']:
     page.evaluate('v=>WardWinter.orbit.face(v)',face);page.wait_for_function('WardWinter.roomViewRenderer()?.loaded')
   page.evaluate('document.fonts.load("20px Caveat")');assert page.evaluate('document.fonts.check("20px Caveat")');assert not page.get_by_role('button',name='Turn around',exact=True).count();checks.append('all 54 native room-facing views and handwriting font load from the extracted package')
   assert not errors,errors;assert not failures,failures;b.close()
 finally:proc.terminate();proc.wait(timeout=5)
result={'format':'multi-file project','files':len(names),'checks':checks,'javascript_errors':errors,'failed_requests':failures,'zip_bytes':archive.stat().st_size,'zip_sha256':hashlib.sha256(archive.read_bytes()).hexdigest()}
(ROOT/'tests/results/winter_package.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
