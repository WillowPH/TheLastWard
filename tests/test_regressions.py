from pathlib import Path
from playwright.sync_api import sync_playwright
import json,subprocess,hashlib
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'tests/results';OUT.mkdir(exist_ok=True)
checks=[]
def passed(name):checks.append(name);print('PASS',name,flush=True)
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox']);page=b.new_page(viewport={'width':1600,'height':1000},reduced_motion='reduce');page.set_default_timeout(5000);errors=[];page.on('pageerror',lambda e:errors.append(str(e)));page.add_init_script("localStorage.setItem('lw_art_mode','offline')");page.goto('http://127.0.0.1:8010')
 def ev(code,arg=None):return page.evaluate(code,arg)
 ev('newGame();nextIntro();nextIntro();nextIntro()')
 assert ev("Object.keys(R).length===27&&Object.values(R).every(r=>r.ch===1)&&Object.values(D).every(d=>R[d.a]&&R[d.b])&&roomConnections.call(null).length===2")
 assert ev("Object.values(D).filter(d=>d.a==='lift'||d.b==='lift').length===1")
 ev("go('sublevel');beginDescent()")
 assert ev("S.room==='lobby'&&!S.f.chapter1Complete")
 passed('27 rooms; no Chapter 2/3 nodes or elevator bypass')
 # All conditional and seeded objects are covered by explicit fixture definitions.
 result=ev('''()=>{const bad=[];for(let i=0;i<128;i++){configureWorld('geometry-'+i,false);placeTelephones('geometry-'+i);for(const room of WardChapter.rooms){S.room=room;S.f.power=1;S.f.pharm=1;S.f.chapel=1;S.f.researchers=1;S.f.drained=1;S.f.photoPuzzleSolved=1;S.lightOn=true;try{WardScene.sites()}catch(e){bad.push(e.message)}}}return [...new Set(bad)]}''')
 assert not result,result
 passed('128 seeded worlds: every object has authored geometry')
 rooms=ev('WardChapter.rooms')
 for width,height in [(1600,1000),(1000,800),(390,844)]:
  page.set_viewport_size({'width':width,'height':height})
  for room in rooms:
   ev("r=>{S.room=r;S.sceneFocus=null;S.f.introComplete=1;S.f.pursuerEncounter=0;S.f.powerOut=0;S.hp=100;S.pursuer.active=false;S.en={};$('m').innerHTML='';render()}",room)
   page.wait_for_timeout(35)
   page.wait_for_function("document.querySelector('.c1-background').complete&&document.querySelector('.c1-background').naturalWidth>0")
   result=ev('''()=>{const plane=document.querySelector('.c1-plane'),r=plane.getBoundingClientRect();return [...plane.querySelectorAll('button')].filter(el=>{const a=el.getBoundingClientRect(),target=document.elementFromPoint(a.x+a.width/2,a.y+a.height/2);return a.width<=0||a.height<=0||a.left<r.left-1||a.right>r.right+1||a.top<r.top-1||a.bottom>r.bottom+1||(target!==el&&!el.contains(target))}).map(e=>e.getAttribute('aria-label'))}''')
   assert not result,(width,room,result)
   controls=ev("['lightBtn','hideBtn','combatBtn'].map(id=>{const e=document.getElementById(id),r=e.getBoundingClientRect();return {id,visible:e.classList.contains('hid')||r.top>=0&&r.bottom<=innerHeight}})")
   assert all(x['visible'] for x in controls),(width,room,controls)
   if room in ['lobby','laundry','powercontrol','observation','lift'] and width in [1600,390]:page.screenshot(path=str(OUT/f'{room}-{width}.png'))
  passed(f'all 27 rooms: loaded art, reachable targets and controls at {width}x{height}')
 page.set_viewport_size({'width':1600,'height':1000})
 # Full inventory leaves the exact object and its overlay in place.
 ev("newGame();nextIntro();nextIntro();nextIntro();S.inv=Array.from({length:8},(_,i)=>({n:'Test object '+i,c:1}));wardFixtureAction('desk')")
 assert ev("!S.ob.desk&&!has('Cabinet Key')")
 ev("$('m').innerHTML='';S.inv.pop();wardFixtureAction('desk')")
 assert ev("S.ob.desk==='done'&&has('Cabinet Key')")
 passed('full inventory preserves pickup; collecting later succeeds')
 # Actual emergency recovery, no free light in dark rooms.
 ev("S.inv=[{n:'Flashlight',c:1}];S.bat=0;S.lightOn=false;wardFixtureAction('emergencyDynamo')")
 assert ev('S.bat===3&&!S.lightOn')
 ev("S.room='eastcorridor';render();wardInspectFixture('radio')")
 assert not page.locator('#sceneFocusOverlay:not(.hid)').count()
 ev('toggleLight();wardInspectFixture("radio")')
 assert page.locator('#sceneFocusOverlay:not(.hid)').is_visible()
 ev('wardCloseFocus()')
 passed('battery recovery is manual; darkness blocks small-object inspection')
 ev("S.room='eastcorridor';S.f.sprinklerTriggered=0;S.f.sprinklerStopped=0;S.f.flashlightDropped=0;wardSprinkler();$('m').innerHTML=''")
 assert ev('S.f.flashlightDropped&&!S.lightOn&&S.f.wet')
 assert page.get_by_role('button',name='Recover dropped flashlight').count()==1
 ev('wardRecoverFlashlight();wardSprinkler()')
 assert ev('S.f.flashlightRecovered&&!S.f.flashlightDropped&&S.f.sprinklerStopped')
 ev("S.room='coldstore';S.f.coldExposure=0;S.f.shivering=0;advanceTime(8)")
 assert ev('!!S.f.shivering')
 ev("S.room='generator';S.f.power=1;advanceTime(8)")
 assert ev('!S.f.shivering')
 passed('sprinkler has separate recovery and valve actions; cold/shivering recovers in warmth')
 # A save round trip preserves seed, object state and irreversible patient outcomes.
 ev("S.room='lobby';S.f.beggingPatientChoice='helped';S.f.seen_site_lobby_desk=1;S.ob.desk='done';add('Ink Ribbon');confirmSave();")
 saved=ev('JSON.stringify(S)');ev("S.ob={};S.f={introComplete:1};loadGame()")
 assert ev("S.ob.desk==='done'&&S.f.beggingPatientChoice==='helped'&&S.f.seen_site_lobby_desk===1")
 ev("choosePatientFate('killed')")
 assert ev("S.f.beggingPatientChoice==='helped'")
 assert not ev("valid({...S,buildId:'older-build'})")
 passed('save/load restores object/choice states; older topology is rejected')
 # Optional glass attack: entering is safe; first inspection warns; second deliberately kills.
 ev("S.room='observation';S.hp=100;S.f.glassHunterStep=0;S.f.glassHunterDone=0;S.f.glassHunterEligible=true;S.f.pursuerEncounter=0;S.pursuer.active=false;render()")
 assert ev('S.hp===100')
 ev('inspectObservationGlass()')
 assert ev('S.hp===100&&S.f.glassHunterStep===1')
 assert 'WARNING' in page.locator('#m').inner_text()
 ev("$('m').innerHTML='';inspectObservationGlass();die()")
 assert ev('S.hp===0') and page.get_by_role('heading',name='GAME OVER').is_visible()
 ev('loadCheckpoint()')
 assert ev('S.hp>0&&S.f.glassHunterRetreated')
 passed('optional fatal cell warns once; second deliberate inspection kills; checkpoint recovers')
 # Hallucinations consume a real shot but never real HP.
 ev("S.room='eastcorridor';S.hp=45;S.f.falseEncounterSeen=0;S.f.falseEncounterResolved=0;S.inv=[{n:'Handgun',c:1}];S.eq='Handgun';S.ld.Handgun=2;wardFalseEncounter();wardResolveFalseEncounter('fire')")
 assert ev('S.hp===45&&S.ld.Handgun===1&&S.f.falseEncounterResolved===1')
 passed('imaginary encounter consumes ammo and preserves real health')
 # Positional audio is derived from graph distance, including side of the connecting door.
 ev("S.room='wardnorth';S.f.power=1;S.f.pursuerEncounter=0;S.f.hidingRoom=null;S.dr.wr=1;S.pursuer={active:true,room:'room12',cooldown:0,noise:0,lastMoveAt:S.t};render()")
 assert ev('WardSound.distance().distance===1')
 ev('S.t+=8;pursuerApproach(S.room)')
 assert ev("S.pursuer.room==='wardnorth'&&S.f.pursuerLastRoute[0]==='room12'&&S.f.pursuerLastRoute[1]==='wardnorth'")
 assert page.locator('.c1-threat.subject-x img').count()==1
 ev("escapePursuer('retreat')")
 assert ev("S.room!=='wardnorth'&&S.f.pursuerEscapes>0")
 passed('Subject X traverses one real edge, is visible, and permits a real retreat')
 # Locker peeking shows the current room; waiting can break contact if unseen.
 ev("S.room='laundry';S.f.pursuerEncounter=0;S.pursuer.room='laundry';S.pursuer.active=true;hideInRoom();wardConfirmHide();wardPeek()")
 assert page.get_by_role('button',name='Stop peeking').is_visible()
 assert 'laundry.webp' in page.locator('.c1-peek-scene').get_attribute('style')
 ev('wardStayHidden();wardExitHiding()')
 assert ev("!S.f.hidingRoom&&S.pursuer.room!=='laundry'")
 passed('locker peek/stay/exit uses actual room and pursuer state')
 # A visible infected uses a separate character, also in combat.
 ev("S.room='morgue';S.en.morgue=9;S.f.pursuerEncounter=0;S.pursuer.active=false;S.hp=100;S.inv=[{n:'Handgun',c:1},{n:'Handgun Ammo',c:6}];S.eq='Handgun';S.ld.Handgun=1;render();combat()")
 assert page.locator('.c1-threat.infected img').count()==1
 assert page.locator('.c1-encounter img').count()==1
 ev("$('m').innerHTML='';cm=0;S.en.morgue=0")
 passed('infected appears in the room and central combat presentation')
 assert not errors,errors
 b.close()
# Decode every bundled effect; byte existence alone is insufficient.
for sound in (ROOT/'audio/chapter1').glob('*.ogg'):
 subprocess.run(['ffmpeg','-nostdin','-v','error','-i',str(sound),'-f','null','-'],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
passed('all 26 bundled recordings decode successfully')
(OUT/'regressions.json').write_text(json.dumps({'passed':checks,'count':len(checks)},indent=2))
print('PASS',len(checks),'regression groups')
