from pathlib import Path
from playwright.sync_api import sync_playwright
import functools,http.server,threading,zipfile,json
ROOT=Path(__file__).resolve().parents[1]
ARTIFACTS=ROOT.parent/'artifacts/chapter1'
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*_):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ARTIFACTS)))
threading.Thread(target=server.serve_forever,daemon=True).start()
checks=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
 page=b.new_page(viewport={'width':1600,'height':1000});errors=[];requests=[]
 page.on('pageerror',lambda e:errors.append(str(e)));page.on('request',lambda r:requests.append(r.url) if r.url.startswith(('http:','https:')) else None)
 page.add_init_script("localStorage.setItem('lw_art_mode','offline')")
 page.goto(f'http://127.0.0.1:{server.server_port}/The_Last_Ward_Chapter_1.html')
 page.context.set_offline(True)
 page.evaluate('newGame();nextIntro();nextIntro();nextIntro()')
 for room in page.evaluate('WardChapter.rooms'):
  page.evaluate("r=>{S.room=r;S.f.power=1;S.f.powerOut=0;S.lightOn=true;S.sceneFocus=null;render()}",room)
  page.wait_for_function("document.querySelector('.c1-background').complete&&document.querySelector('.c1-background').naturalWidth>0")
  assert page.locator('.c1-background').get_attribute('src').startswith('data:')
 assert len(requests)==1,requests
 assert not errors,errors
 checks.append('single-file HTML: all 27 room backgrounds load after network is disabled; one HTTP document request')
 # Important new characters and audio are embedded, not merely the base room files.
 assert page.evaluate("['subject_x','infected_patient','infected_nurse','nurse_shaw','operator_clara'].every(x=>WardEmbeddedAssets['assets/characters/'+x+'.png'])")
 assert page.evaluate("Object.keys(WardEmbeddedAssets).filter(x=>x.startsWith('audio/chapter1/')).length===26")
 assert page.evaluate("['telephone','dynamo','terminal','negative'].every(x=>WardEmbeddedAssets['assets/props/'+x+'.png'])")
 assert page.evaluate("WardChapter.rooms.every(x=>WardEmbeddedAssets['assets/reverse/'+x+'.webp'])")
 checks.append('all five characters, four physical props, 27 reverse scenes and 26 recordings embedded')
 page.evaluate("S.room='security';S.prev='lobby';S.sceneFocus=null;S.sceneView='front';S.sceneViewRoom=S.room;S.cameraSchema=2;S.f.claraGone=0;S.f.power=1;render()")
 page.get_by_role('button',name='Turn around',exact=True).click();page.get_by_role('button',name='Face the room',exact=True).click();assert not page.locator('.c1-rear-view').count()
 assert not page.locator('img.c1-npc').count();page.locator('[data-fixture=monitors]').click();page.locator('button[onclick="wardFixtureAction(\'clara\')"]').click();assert 'recorded message' in page.locator('#m').inner_text()
 checks.append('standalone offline edition accepts reverse controls and Clara recording inspection')
 page.close()
 context=b.new_context();page=context.new_page();page.add_init_script("localStorage.setItem('lw_art_mode','offline')");page.goto('http://127.0.0.1:8010');page.evaluate('navigator.serviceWorker.ready');page.reload();page.wait_for_function('navigator.serviceWorker.controller!==null');context.set_offline(True);page.reload();page.evaluate('newGame();nextIntro();nextIntro();nextIntro()');page.wait_for_function("document.querySelector('.c1-background').complete&&document.querySelector('.c1-background').naturalWidth>0");assert page.locator('#lightBtn').is_visible()
 checks.append('hosted PWA installs current cache and reloads the game offline')
 context.close()
 # An unavailable image backend does not block the scene or alter target geometry.
 context=b.new_context();page=context.new_page();page.route('**/api/ward-art',lambda route:route.fulfill(status=503,content_type='application/json',body='{"error":"not configured"}'));page.goto('http://127.0.0.1:8010');page.evaluate('newGame();nextIntro();nextIntro();nextIntro()');page.wait_for_timeout(200);assert page.locator('[data-fixture=desk]').is_visible();assert page.locator('.c1-background').get_attribute('src')=='assets/rooms/lobby.webp';checks.append('optional image-provider failure preserves local scene and targets')
 b.close()
server.shutdown()
with zipfile.ZipFile(ARTIFACTS/'The_Last_Ward_Chapter_1_Source.zip') as z:
 assert z.testzip() is None
 assert not any('/downloads/' in name for name in z.namelist())
 assert len([name for name in z.namelist() if '/assets/rooms/' in name and name.endswith('.webp')])==27
checks.append('source ZIP integrity; 27 room images; no recursively bundled downloads')
(ROOT/'tests/results/delivery.json').write_text(json.dumps({'passed':checks,'count':len(checks)},indent=2))
for check in checks:print('PASS',check)
