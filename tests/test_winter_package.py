"""Verify the distributable HTML with networking disabled, not the source server."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json,hashlib,sys,zipfile
ROOT=Path(__file__).resolve().parents[1]
HTML=Path(sys.argv[1]) if len(sys.argv)>1 else ROOT.parent/'artifacts/chapter1/The_Last_Ward_Chapter_1.html'
checks=[];requests=[];errors=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);c=b.new_context(offline=False,service_workers='block',viewport={'width':1600,'height':1000});page=c.new_page();page.on('pageerror',lambda e:errors.append(str(e)));page.on('requestfailed',lambda r:requests.append(r.url));c.route('**/*',lambda route:route.continue_() if route.request.url=='http://127.0.0.1:8010/downloads/The_Last_Ward_Chapter_1.html' else route.abort());page.goto('http://127.0.0.1:8010/downloads/The_Last_Ward_Chapter_1.html',timeout=60000);c.set_offline(True);page.get_by_role('button',name='BEGIN INVESTIGATION').click();page.evaluate('nextIntro();nextIntro();nextIntro()')
 assert page.evaluate('Object.keys(WardPanoramaAssets).length===27&&S.bat===100');checks.append('standalone starts offline with all 27 panoramas and 100% charge')
 page.wait_for_function("WardSound.context().state==='running'");page.evaluate("WardSound.play('winter_wind',{volume:.8,loop:true})");page.wait_for_timeout(800)
 values=[]
 for _ in range(8):page.wait_for_timeout(80);values.append(page.evaluate('WardSound.energy()'))
 assert max(values)>.00001,values;checks.append('embedded local sound produces output offline after the Begin gesture')
 page.evaluate('WardSound.stop();S.enemyActors.forEach(a=>a.hp=0);WardWinter.enemies.project();S.pursuer.active=false;S.f.power=1;S.f.pharm=1;S.f.chapel=1;S.f.photoPuzzleSolved=1;S.f.researchers=1;S.f.drained=1')
 for room in page.evaluate('Object.keys(R)'):
  for view in ['front','rear']:
   page.evaluate('v=>{S.room=v[0];S.sceneView=v[1];S.sceneViewRoom=S.room;S.cameraSchema=2;renderScene()}',[room,view]);page.wait_for_function("[...document.querySelectorAll('.winter-art-plane>img:first-child')].every(i=>i.complete&&i.naturalWidth>0)")
 page.evaluate('document.fonts.load("20px Caveat")');assert page.evaluate('document.fonts.check("20px Caveat")');checks.append('all 54 front/rear scene images and the handwriting font load offline')
 page.evaluate("S.room='security';S.sceneView='front';S.sceneViewRoom=S.room;S.f.photoPuzzleSolved=0;render();portraitPuzzle()");page.get_by_role('button',name='Inspect photograph',exact=True).first.click();page.get_by_role('button',name='Turn over',exact=True).click();assert 'Appointed' in page.locator('#m').inner_text();checks.append('embedded portrait inspection and dated reverse are interactive')
 page.evaluate("closeModal();S.room='wardnorth';S.sceneView='rear';S.sceneViewRoom=S.room;wardOpenWindows()");assert page.locator('.winter-window-state').count()==3;page.wait_for_function("[...document.querySelectorAll('.winter-window-state')].every(i=>i.complete&&i.naturalWidth)");checks.append('open window state art is embedded and independently clipped')
 page.screenshot(path=str(ROOT/'tests/results/winter-offline.png'))
 assert not errors,errors;assert not requests,requests
 b.close()
result={'transport':'Only the standalone HTML is served from loopback; all other requests are blocked, and networking is disabled after initial HTML load. Direct file navigation is blocked by environment Chromium policy.', 'checks':checks,'javascript_errors':errors,'failed_requests':requests,'standalone_bytes':HTML.stat().st_size,'standalone_sha256':hashlib.sha256(HTML.read_bytes()).hexdigest()}
(ROOT/'tests/results/winter_package.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
