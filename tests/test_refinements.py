"""Eight focused player-facing checks, also runnable against the offline HTML."""
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image,ImageStat
import io,json,sys
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'tests/results';url=sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8010';packaged='The_Last_Ward' in url;checks=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);page=b.new_page(viewport={'width':1600,'height':1000},reduced_motion='reduce');page.set_default_timeout(6000);errors=[];page.on('pageerror',lambda e:errors.append(str(e)));page.goto(url)
 if packaged:page.context.set_offline(True)
 def ev(s,a=None):return page.evaluate(s,a)
 ev('newGame();nextIntro();nextIntro();nextIntro();WardScene.options.motion=false')
 base=ev('JSON.parse(JSON.stringify(S))')
 def setup(room):ev('''a=>{S=JSON.parse(JSON.stringify(a.base));S.room=a.room;S.prev=null;S.sceneView='front';S.sceneViewRoom=S.room;S.cameraSchema=2;S.lightOn=true;S.bat=100;S.hp=100;S.en={};S.pursuer.active=false;S.f.pursuerEncounter=0;S.sceneFocus=null;WardNavigation.until=0;$('m').innerHTML='';render()}''',{'base':base,'room':room})
 def loaded():page.wait_for_function("[...document.querySelectorAll('.c1-background')].every(i=>i.complete&&i.naturalWidth>0)")
 def clear():ev("$('m').innerHTML='';wardCloseFocus()")
 def done(text):checks.append(text);print('PASS',text,flush=True)
 # 1: no movement, rescale or image replacement from opening/closing inspections.
 for width,height in [(1600,1000),(1000,800),(390,844)]:
  page.set_viewport_size({'width':width,'height':height})
  for room,fixture in [('lobby','phone'),('security','monitors'),('room12','file')]:
   setup(room);loaded();before=page.locator('.c1-plane').bounding_box();ev('window.stableBackground=document.querySelector(".c1-background")')
   for _ in range(8):
    page.locator('[data-fixture='+fixture+']').click();assert page.locator('.c1-plane').bounding_box()==before;assert ev('stableBackground===document.querySelector(".c1-background")');page.locator('.c1-focus header button').click();assert page.locator('.c1-plane').bounding_box()==before
 done('1. Eight inspection open/close cycles per scene at three viewport sizes keep the art plane and image node unchanged')
 page.set_viewport_size({'width':1600,'height':1000})
 # 2: early setup, cancel, save roundtrip, automatic capture and deliberate empty release.
 setup('laundry');ev('S.f.power=1;render()');page.locator('[data-fixture=lever]').click();page.get_by_role('button',name='Examine',exact=True).click();page.get_by_role('button',name='Not now',exact=True).click();assert not ev('S.f.trapArmed||S.f.trapUsed')
 ev('triggerServiceTrap()');page.get_by_role('button',name='Set up trap',exact=True).click();assert ev('S.f.trapArmed&&!S.f.trapUsed');loaded();assert 'laundry_trap_armed' in page.locator('.c1-background').get_attribute('src') if not packaged else ev("document.querySelector('.c1-background').src===WardEmbeddedAssets['assets/states/laundry_trap_armed.webp']")
 ev("add('Ink Ribbon');confirmSave();$('m').innerHTML='';S.f.trapArmed=0;loadGame();$('m').innerHTML=''");assert ev('S.f.trapArmed&&!S.f.trapUsed')
 ev("S.pursuer.active=true;S.pursuer.room='laundry';advanceTime(1)");assert ev("S.f.trapUsed&&!S.f.trapArmed&&S.pursuer.room==='laundry'&&S.pursuer.cooldown>=7");loaded()
 setup('laundry');ev('triggerServiceTrap();wardConfirmTrap("arm");triggerServiceTrap()');page.get_by_role('button',name='Not now',exact=True).click();assert not ev('S.f.trapUsed');ev('triggerServiceTrap()');page.get_by_role('button',name='Release now',exact=True).click();assert ev('S.f.trapUsed&&!S.pursuer.active');loaded();page.screenshot(path=str(OUT/'refinement-trap.png'))
 done('2. Hoist cancel/arm/save/reload/capture/manual-release states work before pursuit; one-use aftermath does not teleport Subject X')
 # 3: every gated edge explains its actual requirement; both legacy keys migrate.
 setup('lobby');requirements=ev('Object.entries(D).filter(([id,d])=>d.need||d.flag).map(([id,d])=>({id,need:d.need,flag:d.flag,text:wardDoorRequirement(id)}))')
 for d in requirements:
  if d['need']:assert d['need'] in d['text'],d
  else:assert 'Requires' in d['text'],d
 ev("S.inv=[{n:'Maintenance Key',c:1}];S.box=[{n:'Tunnel Key',c:1}];render()");assert ev("has('Archive Key')&&S.box[0].n==='Boiler Key'")
 done('3. All gated doors name their key/code/power/clearance; old Archive and Boiler keys migrate in inventory and storage')
 # 4: compare actual rendered luminance with torch off/on for every room and both views.
 for room in ev('WardChapter.rooms'):
  setup(room)
  for powered in [0,1]:
   ev('v=>{S.f.power=v;S.lightOn=false;render()}',powered)
   for view in ['front','rear']:
    ev('v=>{S.sceneView=v;S.lightOn=false;renderScene()}',view);selector='.c1-reverse-plane' if view=='rear' else '.c1-plane';page.wait_for_function("[...document.querySelectorAll(S.sceneView==='rear'?'.c1-reverse-plane>img':'.c1-background')].every(i=>i.complete&&i.naturalWidth>0)");page.mouse.move(2,2)
    off=ImageStat.Stat(Image.open(io.BytesIO(page.locator(selector).screenshot())).convert('L')).mean[0];ev('toggleLight()');on=ImageStat.Stat(Image.open(io.BytesIO(page.locator(selector).screenshot())).convert('L')).mean[0];assert on+.1>=off,(room,powered,view,off,on)
 done('4. In all 27 rooms, powered/unpowered and front/rear, switching the flashlight on never reduces rendered brightness')
 # 5: recording replaces Clara without loss of evidence.
 setup('security');assert not page.locator('img.c1-npc,[data-actor=clara]').count();page.locator('[data-fixture=monitors]').click();page.locator('button[onclick="wardFixtureAction(\'clara\')"]').click();assert 'recorded message' in page.locator('#m').inner_text();assert ev('S.f.claraSpoken');clear()
 done('5. No floating Clara actor; her recording remains available at the monitors and records the evidence')
 # 6: every actionable fixture has idle guidance; all runtime item names load real icons.
 names=ev("[...new Set(Object.values(R).flatMap(r=>r.o.flatMap(o=>(o[4].give||[]).map(g=>g[0]))).concat(Object.keys(ITEM_ART)))]")
 for room in ev('WardChapter.rooms'):
  setup(room);assert page.locator('.c1-target:not(.important)').count()==0,room
 setup('lobby');ev("names=>{$('m').innerHTML='<section id=\"iconAudit\">'+names.map(n=>itemIconMarkup(n)).join('')+'</section>'}",names);assert page.locator('#iconAudit>img').count()==len(names);page.wait_for_function("[...document.querySelectorAll('#iconAudit img')].every(i=>i.complete&&i.naturalWidth>0)");clear()
 done(f'6. Every unresolved fixture has a subtle marker; all {len(names)} runtime item icons load, including previously missing tools/evidence')
 # 7: struggle hurts and preserves the enemy; retreat/return/save do not erase it.
 setup('eastcorridor');ev("S.f.power=1;S.en.eastcorridor=30;S.prev='security';S.dr.es=1;S.f.doctor_eastcorridor=1;combat()");hp=ev('S.hp');enemy=ev('S.en.eastcorridor');page.get_by_role('button',name='Struggle · risk injury',exact=True).click();assert ev('S.hp')<hp and ev('S.en.eastcorridor')==enemy;page.get_by_role('button',name='Retreat',exact=True).click();assert ev("S.room==='security'");ev('WardNavigation.until=0;go("eastcorridor")');assert ev('alive("eastcorridor")&&S.en.eastcorridor===30');ev("$('m').innerHTML='';S.room='lobby';add('Ink Ribbon');confirmSave();$('m').innerHTML='';S.en.eastcorridor=0;loadGame()");assert ev('S.en.eastcorridor===30')
 done('7. Struggle costs health without killing; infected survives retreat, return and save/load with its remaining health')
 # 8: knife pickup, patient cancel then confirmation, covered aftermath and save persistence.
 setup('isoward');ev("choosePatientFate('helped')");assert 'Trauma Dressing' in page.locator('#m').inner_text();assert not ev('S.f.beggingPatientChoice');clear()
 setup('security');page.locator('[data-fixture=cabinet]').click();page.get_by_role('button',name='Take Utility Knife',exact=True).click();assert ev("has('Utility Knife')&&S.ob.utilityKnife==='done'");assert not page.locator('[data-collectible=utilityKnife]').count();clear();ev("S.room='isoward';S.prev='wardnorth';S.lightOn=true;render();choosePatientFate('killed')");page.get_by_role('button',name='Leave him alive for now',exact=True).click();assert not ev('S.f.beggingPatientChoice');ev("choosePatientFate('killed')");page.get_by_role('button',name='Use utility knife',exact=True).click();assert ev("S.f.beggingPatientChoice==='killed'&&S.f.patientMethod==='knife'&&S.ld.Handgun===0");clear();loaded();assert page.locator('[data-fixture=patient]').count()==0;assert ev("document.querySelector('.c1-background').src.endsWith('isoward_after.webp')||document.querySelector('.c1-background').src===WardEmbeddedAssets?.['assets/states/isoward_after.webp']");ev("add('Ink Ribbon');confirmSave();$('m').innerHTML='';delete S.f.beggingPatientChoice;loadGame();$('m').innerHTML='';render()");assert ev("S.f.beggingPatientChoice==='killed'&&S.f.patientMethod==='knife'");loaded();page.screenshot(path=str(OUT/'refinement-patient.png'))
 done('8. Knife can be collected and used after confirmation; cancellation preserves life; covered aftermath and outcome survive save/load')
 assert not errors,errors;b.close()
(OUT/('refinements_packaged.json' if packaged else 'refinements.json')).write_text(json.dumps({'count':len(checks),'passed':checks},indent=2))
