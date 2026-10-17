"""Actual pointer acceptance checks for the reported five-room failures."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'tests/results';OUT.mkdir(exist_ok=True)
ROOMS=['lobby','security','eastcorridor','ward','room12'];checks=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);page=b.new_page(viewport={'width':1600,'height':1000},reduced_motion='no-preference');page.set_default_timeout(6000);errors=[];page.on('pageerror',lambda e:errors.append(str(e)));page.goto('http://127.0.0.1:8010');page.get_by_role('button',name='BEGIN INVESTIGATION',exact=True).click()
 for _ in range(3):page.locator('#m button[onclick="nextIntro()"]').click()
 def ev(x,arg=None):return page.evaluate(x,arg)
 def setup(room,previous=None):
  ev('(a)=>{S.room=a[0];S.prev=a[1];S.sceneFocus=null;S.sceneFocusRoom=S.room;S.sceneView="front";S.sceneViewRoom=S.room;S.hp=100;S.en={};S.pursuer.active=false;S.f.pursuerEncounter=0;S.f.hidingRoom=null;S.lightOn=true;S.bat=30;WardNavigation.until=0;$("m").innerHTML="";render()}',[room,previous])
 def click_art(rect,plane='.c1-plane'):
  r=page.locator(plane).bounding_box();page.mouse.click(r['x']+r['width']*rect[0]/100,r['y']+r['height']*rect[1]/100)
 # One real click on each visible physical doorway, including the room of entry.
 total=0
 for room in ROOMS:
  doors=ev('r=>Object.entries(WardScenes[r].doors)',room)
  for id,rect in doors:
   destination=ev('a=>D[a[0]].a===a[1]?D[a[0]].b:D[a[0]].a',[id,room]);setup(room,destination);ev('id=>{S.dr[id]=1;S.f["doctor_"+S.room]=1}',id);click_art(rect);assert ev('S.room')==destination,(room,id,destination,ev('S.room'));total+=1
 checks.append(f'{total} actual doorway-coordinate clicks traverse the matching edge, including entry doors')
 setup('eastcorridor','security');ev("delete S.dr.ew;S.inv=S.inv.filter(x=>x.n!=='Staff Access Card')");click_art(ev('WardScenes.eastcorridor.doors.ew'));assert ev("S.room==='eastcorridor'");assert 'Staff Access Card' in page.locator('#m').inner_text();page.get_by_role('button',name='Stay here',exact=True).click()
 checks.append('locked doorway click gives a visible requirement dialog rather than silently failing')
 setup('security','lobby');ev('S.f.claraGone=0;render()')
 for x,y in [(55,32),(53,52),(61,70)]:
  r=page.locator('img.c1-npc').bounding_box();page.mouse.click(r['x']+r['width']*x/100,r['y']+r['height']*y/100);assert 'Clara Whitmore' in page.locator('#m').inner_text();page.get_by_role('button',name='Leave her to the monitors',exact=True).click()
 checks.append('clicking Clara at chest, waist and leg opens her conversation')
 for width,height in [(1600,1000),(390,844)]:
  page.set_viewport_size({'width':width,'height':height})
  for room in ROOMS:
   prev=ev('r=>{const d=Object.values(D).find(d=>d.a===r||d.b===r);return d.a===r?d.b:d.a}',room);setup(room,prev);ev('S.sceneView="front";render()');page.get_by_role('button',name='Turn around',exact=True).click();door=page.locator('.c1-rear-travel');assert door.evaluate('(e)=>getComputedStyle(e).position')=='absolute';page.get_by_role('button',name='Face the room',exact=True).click();assert not page.locator('.c1-rear-view').count()
   page.get_by_role('button',name='Turn around',exact=True).click();page.locator('#lightBtn').click();assert page.locator('.c1-rear-view').count()==1;page.keyboard.press('Escape');assert not page.locator('.c1-rear-view').count()
   page.get_by_role('button',name='Turn around',exact=True).click();ev('p=>{S.dr[WardNavigation.edge(S.room,p)]=1;WardNavigation.until=0}',prev);r=door.bounding_box();page.mouse.click(r['x']+r['width']/2,r['y']+r['height']/2);assert ev('S.room')==prev,(width,room,prev)
 checks.append('all five reverse views support actual door clicks, Face the room and Escape at desktop/mobile sizes; flashlight preserves the view')
 page.set_viewport_size({'width':1600,'height':1000});setup('security','lobby');page.locator('[data-fixture=cabinet]').click();assert page.locator('.c1-finding').count()==1;page.get_by_role('button',name='Examine',exact=True).click();assert ev("S.ob.rev==='read'")
 setup('room12','wardnorth');ev("S.inv=[{n:'Cabinet Key',c:1},{n:'Flashlight',c:1}];delete S.ob.shf;delete S.ob.shf2;render()");page.locator('[data-fixture=shelf]').click();page.get_by_role('button',name='Take Trauma Dressing',exact=True).click();assert page.locator('.c1-focus').count()==1;assert page.get_by_role('button',name='Examine',exact=True).is_visible();page.get_by_role('button',name='Examine',exact=True).click()
 checks.append('equipment cabinet has one inspection; multi-item shelf stays open for its remaining action after a pickup')
 item_count=0
 for room in ROOMS:
  setup(room);ev("S.inv=[{n:'Cabinet Key',c:1},{n:'Flashlight',c:1}];S.slots=12;S.ob={};S.f.ammoSnakeSeen=1;render()")
  entries=ev('r=>WardScenes[r].fixtures.flatMap(f=>(f.collectibles||[]).map(c=>({fixture:f.id,...c})))',room)
  for item in entries:
   if page.locator('.c1-focus').count():page.locator('.c1-focus header button').click()
   assert page.locator('[data-collectible="'+item['id']+'"]').count()==1
   click_art(item['rect']);button=page.locator('button[onclick="wardFixtureAction(\''+item['id']+'\')"]');assert button.count()==1
   if item['id']!='mapboard':page.get_by_role('button',name='Leave',exact=True).click();assert page.locator('[data-collectible="'+item['id']+'"]').count()==1;click_art(item['rect']);button=page.locator('button[onclick="wardFixtureAction(\''+item['id']+'\')"]')
   button.click();assert ev('id=>S.ob[id]===\'done\'',item['id']);assert not page.locator('[data-collectible="'+item['id']+'"]').count();ev('render()');assert not page.locator('[data-collectible="'+item['id']+'"]').count();item_count+=1
 ev("add('Ink Ribbon');confirmSave();$('m').innerHTML='';S.ob={};loadGame()")
 assert ev("S.ob.cab==='done'&&S.ob.shf2==='done'&&S.ob.drw12==='done'")
 assert not page.locator('[data-collectible=cab],[data-collectible=shf2],[data-collectible=drw12]').count()
 checks.append(f'all {item_count} authored five-room collectibles remain when left and disappear when taken, including after re-render')
 # Compare actual drawn frame pixels, not only the presence of CSS animation names.
 for room in ROOMS:
  setup(room);ev('WardScene.options.motion=true;WardScene.options.motionOverride=true;render()');page.wait_for_timeout(150);first=page.locator('.c1-motion-canvas').evaluate('(c)=>c.toDataURL()');page.wait_for_timeout(450);second=page.locator('.c1-motion-canvas').evaluate('(c)=>c.toDataURL()');assert first!=second,room;page.get_by_role('button',name='Motion · on',exact=True).click();assert not page.locator('.c1-motion-canvas').count();page.get_by_role('button',name='Motion · off',exact=True).click();assert page.locator('.c1-motion-canvas').count()==1
 checks.append('all five rooms produce changing animation pixels; on/off control works')
 assert not errors,errors;page.screenshot(path=str(OUT/'five-room-input-final.png'));b.close()
(OUT/'five_room_input.json').write_text(json.dumps({'passed':checks,'count':len(checks)},indent=2))
for check in checks:print('PASS',check)
