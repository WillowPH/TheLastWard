"""Native fallback and a mocked hosted atmosphere service through real browser UI."""
from pathlib import Path
import json,sys
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
URL=sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8010'
checks=[];errors=[]
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 def fresh(connected=False,hold=None):
  context=browser.new_context(service_workers='block',viewport={'width':1672,'height':941})
  page=context.new_page();page.set_default_timeout(7000);page.on('pageerror',lambda e:errors.append(str(e)))
  log={'posts':[],'images':0,'held':[],'capabilities':[]};control={'hold':hold,'fail':False,'foreign':False}
  def capability(route):
   log['capabilities'].append(route.request.url)
   if control['hold']=='capability':log['held'].append(route);return
   route.fulfill(status=200,content_type='application/json',body=json.dumps({'available':connected,'endpoint':'/api/ward-art' if connected else None}))
  def post(route):
   payload=route.request.post_data_json;log['posts'].append(payload)
   if control['hold']==payload['room']:log['held'].append(route);return
   if control['fail']:route.fulfill(status=503,content_type='application/json',body='{}');return
   route.fulfill(status=200,content_type='application/json',body=json.dumps({'image_url':'https://untrusted.invalid/texture.png' if control['foreign'] else URL+'/online-test/texture.png'}))
  def texture(route):
   log['images']+=1;route.fulfill(status=200,content_type='image/webp',path=str(ROOT/'assets/rooms/lobby.webp'))
  page.route('**/data/art_service.json*',capability);page.route('**/api/ward-art',post);page.route('**/online-test/texture.png',texture)
  page.goto(URL)
  return context,page,log,control
 def begin(page):
  page.get_by_role('button',name='BEGIN INVESTIGATION',exact=True).click()
  page.evaluate('nextIntro();nextIntro();nextIntro()')
  page.wait_for_function('WardWinter.roomViewRenderer()?.loaded&&!WardWinter.orbit.busy')
 def active(page):
  page.wait_for_function('WardArt.status().phase==="active"&&document.querySelector(".room-online-atmosphere")?.naturalWidth>0')
 def release(route,status=200):
  try:route.fulfill(status=status,content_type='application/json',body=json.dumps({'image_url':URL+'/online-test/texture.png'}))
  except Exception as e:
   # An explicit Offline action may have already cancelled this request.
   if 'closed' not in str(e).lower() and 'handled' not in str(e).lower():raise

 c,q,log,ctl=fresh();assert q.locator('input[name=artMode][value=online]').is_checked()
 q.wait_for_function('WardArt.status().phase==="local"');begin(q)
 assert not log['posts'];assert 'local art' in q.locator('.hud-local-art').inner_text()
 assert q.evaluate('WardArt.settings.enabled&&!WardArt.settings.available&&WardWinter.roomViewRenderer().loaded')
 q.get_by_role('button',name='Options',exact=True).click()
 q.locator('#onlineArtSetting').uncheck();assert q.evaluate('WardArt.status().phase')=='offline'
 assert 'No online artwork requests' in q.locator('#onlineArtStatus').inner_text()
 count=len(log['capabilities']);q.reload();q.wait_for_timeout(200)
 assert q.locator('input[name=artMode][value=offline]').is_checked();assert len(log['capabilities'])==count
 q.locator('input[name=artMode][value=online]').check();q.wait_for_function('WardArt.status().phase==="local"')
 c.close();checks.append('Online preferred is default, native fallback is truthful and playable, explicit Offline persists with no artwork service requests, and re-enabling updates status')

 c,q,log,ctl=fresh(True);begin(q);active(q)
 before=q.evaluate('({src:WardWinter.roomViewAsset(S.room,S.roomView),targets:[...document.querySelectorAll("[data-door],[data-fixture]")].map(n=>[n.dataset.door||n.dataset.fixture,n.style.cssText])})')
 q.evaluate('Promise.all(Array.from({length:12},()=>WardArt.prepare(S.room)))');q.wait_for_timeout(100)
 assert len(log['posts'])==1
 style=q.locator('.room-online-atmosphere').evaluate('(n)=>({events:getComputedStyle(n).pointerEvents,clip:getComputedStyle(n).clipPath,opacity:getComputedStyle(n).opacity})')
 assert style['events']=='none' and style['clip'].startswith('polygon(') and float(style['opacity'])<=.1
 assert q.evaluate('({src:WardWinter.roomViewAsset(S.room,S.roomView),targets:[...document.querySelectorAll("[data-door],[data-fixture]")].map(n=>[n.dataset.door||n.dataset.fixture,n.style.cssText])})')==before
 q.evaluate('WardArt.setMode("offline")');assert not q.locator('.room-online-atmosphere').count()
 q.evaluate('WardArt.setMode("online")');active(q);assert len(log['posts'])==1
 c.close();checks.append('mocked connected host supplies decoded same-origin imagery once per room/seed/power; ceiling clipping cannot intercept input or relocate authored art/targets, and cached mode switches do not generate again')

 c,q,log,ctl=fresh(True,'lobby');begin(q);q.wait_for_function('WardArt.settings.available');q.wait_for_timeout(100)
 assert log['held'];q.evaluate('WardArt.setMode("offline")');release(log['held'][0]);q.wait_for_timeout(250)
 assert log['images']==0 and not q.locator('.room-online-atmosphere').count()
 assert q.evaluate('WardArt.status().phase')=='offline'
 c.close();checks.append('turning Offline cancels pending generation and a late response cannot start an image download or overwrite the Offline status')

 c,q,log,ctl=fresh(True,'lobby');begin(q);q.wait_for_timeout(100);assert log['held']
 q.evaluate('S.room="security";S.roomViewRoom=null;renderScene()');active(q)
 release(log['held'][0],503);q.wait_for_timeout(200)
 assert q.evaluate('S.room==="security"&&WardArt.status().phase==="active"')
 c.close();checks.append('a late failure for a previous room cannot overwrite the active current-room artwork state')

 c,q,log,ctl=fresh(True,'capability');begin(q);q.evaluate('S.room="security";S.roomViewRoom=null;renderScene()')
 assert len(log['held'])==1;ctl['hold']=None
 log['held'][0].fulfill(status=200,content_type='application/json',body=json.dumps({'available':True,'endpoint':'/api/ward-art'}));active(q)
 assert [x['room'] for x in log['posts']]==['security']
 c.close();checks.append('room changes while capability discovery is pending do not request artwork for stale room contexts')

 for foreign in [False,True]:
  c,q,log,ctl=fresh(True);ctl['fail']=not foreign;ctl['foreign']=foreign;begin(q)
  q.wait_for_function('WardArt.status().phase==="local"');q.evaluate('Promise.all(Array.from({length:8},()=>WardArt.prepare(S.room)))')
  assert len(log['posts'])==1 and log['images']==0 and not q.locator('.room-online-atmosphere').count()
  assert q.evaluate('WardWinter.roomViewRenderer().loaded')
  c.close()
 checks.append('unavailable service and cross-origin image responses retain complete local art without retry storms or external image requests')
 assert not errors,errors;browser.close()

result={'checks':checks,'javascript_errors':errors,'hosted_service':'Local browser mock only; no live provider is configured or claimed.'}
(ROOT/'tests/results/online_art_v9.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
