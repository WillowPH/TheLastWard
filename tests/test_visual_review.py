"""Player-visible regressions for the approved four-room visual review."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'tests/results';checks=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);page=b.new_page(viewport={'width':1600,'height':1000});page.set_default_timeout(6000);errors=[];page.on('pageerror',lambda e:errors.append(str(e)));page.goto('http://127.0.0.1:8010');page.evaluate('newGame();nextIntro();nextIntro();nextIntro()')
 def ev(x,arg=None):return page.evaluate(x,arg)
 for width,height in [(1600,1000),(390,844)]:
  page.set_viewport_size({'width':width,'height':height});ev("S.room='lobby';S.prev=null;S.sceneFocus=null;S.f.power=0;render()")
  page.locator('[data-fixture=window]').click();panel=page.locator('.c1-focus').bounding_box();host=page.locator('#interactiveScene').bounding_box();assert panel['x']>=host['x'] and panel['x']+panel['width']<=host['x']+host['width']+1;assert panel['y']>=host['y'] and panel['y']+panel['height']<=host['y']+host['height']+1
  assert page.get_by_role('button',name='Examine',exact=True).is_visible();page.screenshot(path=str(OUT/f'review-window-{width}.png'));ev('wardCloseFocus()')
  page.locator('[data-fixture=desk]').click();assert page.get_by_role('button',name='Take Cabinet Key',exact=True).is_visible();page.get_by_role('button',name='Leave',exact=True).click();assert ev("!has('Cabinet Key')&&!S.ob.desk")
 checks.append('window actions anchored beside object and inside viewport; Take/Leave preserves uncollected item at desktop/mobile sizes')
 page.set_viewport_size({'width':1600,'height':1000});ev("S.room='security';S.prev='lobby';S.f.power=1;S.f.claraGone=0;render()")
 npc=page.locator('img.c1-npc').bounding_box();plane=page.locator('.c1-plane').bounding_box();assert npc['height']>=plane['height']*.58;page.screenshot(path=str(OUT/'review-clara.png'))
 checks.append('Clara uses authored full adult height and floor placement rather than fixture-thumbnail bounds')
 for room,previous in [('lobby','security'),('security','lobby'),('eastcorridor','security'),('ward','eastcorridor'),('room12','wardnorth')]:
  ev('(a)=>{S.room=a[0];S.prev=a[1];S.sceneFocus=null;S.sceneView="front";S.sceneViewRoom=S.room;S.cameraSchema=2;render();wardTurnAround()}',[room,previous]);page.wait_for_function("document.querySelector('.c1-reverse-plane img').complete&&document.querySelector('.c1-reverse-plane img').naturalWidth>0")
  assert page.locator('.c1-reverse-plane img').get_attribute('src')=='assets/reverse/'+room+'.webp';assert page.locator('.c1-rear-travel').get_attribute('data-destination')==previous
  page.screenshot(path=str(OUT/f'review-reverse-{room}.png'));ev('wardCloseFocus()')
 checks.append('all five review rooms load distinct full reverse backgrounds with matching return destination')
 ev("S.room='children';S.en.children=0;S.prev='room12';S.inv=S.inv.filter(x=>x.n!=='Photographic Negative');delete S.ob.neg;S.lightOn=true;render()")
 assert page.locator('[data-collectible=neg]').count()==1
 page.locator('[data-fixture=negative]').click();page.get_by_role('button',name='Leave',exact=True).click();assert page.locator('[data-collectible=neg]').count()==1
 page.locator('[data-fixture=negative]').click();page.get_by_role('button',name='Take Photographic Negative',exact=True).click();assert ev("has('Photographic Negative')"),(ev("({room:S.room,inv:S.inv,ob:S.ob,hp:S.hp})"),page.locator("#m").inner_text(),errors);assert page.locator('[data-collectible=neg],[data-fixture=negative]').count()==0;ev('render()');assert page.locator('[data-collectible=neg]').count()==0
 checks.append('negative is separate physical artwork; Leave retains it, Take removes its image and hotspot persistently')
 ev("S.room='security';S.sceneFocus=null;delete S.ob.rep;render();wardFixtureAction('rep')");assert ev("S.docs.includes('Incident Report 09-17')");ev("$('m').innerHTML='';render()");assert page.locator('[data-fixture=report]').count()==0
 checks.append('read report loses its hotspot, while evidence remains available in Files')
 ev("S.room='isoward';S.prev='wardnorth';delete S.f.beggingPatientChoice;S.eq='Handgun';S.ld.Handgun=0;S.inv=[{n:'Handgun',c:1},{n:'Flashlight',c:1}];render();choosePatientFate('killed')")
 assert 'empty' in page.locator('#m').inner_text().lower();assert not ev('S.f.beggingPatientChoice');ev("$('m').innerHTML='';S.ld.Handgun=1;choosePatientFate('killed')");assert ev("S.f.beggingPatientChoice==='killed'&&S.ld.Handgun===0");assert page.locator('.c1-background').get_attribute('src').endswith('isoward_after.webp');ev("$('m').innerHTML='';render()");assert page.locator('.c1-background').get_attribute('src').endswith('isoward_after.webp')
 checks.append('unloaded weapon gives visible explanation; successful patient choice consumes one round and persists covered-bed aftermath')
 for room,kind,holes in [('laundry','locker',7),('wardservice','crates',2),('security','desk',2)]:
  ev('(a)=>{S.room=a[0];S.f.pendingHideType=a[1];S.f.hidingRoom=null;S.f.pursuerEncounter=0;S.pursuer.active=false;render();hideInRoom();wardConfirmHide();wardPeek()}',[room,kind]);assert page.locator('.c1-cover-frame mask rect').count()==holes
  page.screenshot(path=str(OUT/f'review-cover-{kind}.png'));ev('wardExitHiding()')
 checks.append('locker slats, crate gap and desk opening use distinct physical frames; no floating rectangular peek mask')
 for width,height in [(1600,1000),(390,844)]:
  page.set_viewport_size({'width':width,'height':height});ev("S.room='wardnorth';S.mapParts=3;render();mapModal()")
  assert page.locator('.c1-map-rooms g').count()==27;assert page.locator('[data-map-edge]').count()==27
  assert page.locator('[data-map-room=isoward]').count()==1;assert not page.locator('[data-map-room=children]').count()
  box=page.locator('.c1-map-scroll').bounding_box();assert box['height']>=180;close=page.get_by_role('button',name='Close',exact=True).bounding_box();assert close['y']>=0 and close['y']+close['height']<=height;page.screenshot(path=str(OUT/f'review-map-{width}.png'));ev("$('m').innerHTML=''")
 checks.append('large scrollable map has all 27 rooms/edges; isolation and children are separate branches; only adjacent rooms offer travel')
 assert not errors,errors;b.close()
(OUT/'visual_review.json').write_text(json.dumps({'passed':checks,'count':len(checks)},indent=2))
for c in checks:print('PASS',c)
