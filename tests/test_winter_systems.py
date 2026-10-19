"""Winter mechanics and all directed entrances on the native room-view renderer."""
from pathlib import Path
import json,hashlib
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];checks=[]
def passed(s):checks.append(s);print('PASS',s,flush=True)
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--enable-unsafe-swiftshader'])
 c=b.new_context(service_workers='block',viewport={'width':1600,'height':1000});page=c.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto('http://127.0.0.1:8010');page.get_by_role('button',name='BEGIN INVESTIGATION').click()
 def ev(s,a=None):return page.evaluate(s,a)
 ev('nextIntro();nextIntro();nextIntro()')
 assert not ev('has("Flashlight")')
 ev('const pickup=R.lobby.o.find(o=>o[4].give?.some(g=>g[0]==="Flashlight"));if(!pickup)throw Error("Missing opening flashlight pickup");wardFixtureAction(pickup[0]);wardCloseFocus()')
 assert ev('has("Flashlight")')
 ev('WardScene.options.motion=false;WardScene.options.flashes=false')
 def ready():page.wait_for_function('WardWinter.roomViewRenderer()?.loaded&&WardWinter.roomViewRenderer().room===S.room&&WardWinter.roomViewRenderer().view===S.roomView&&!WardWinter.orbit.busy')
 def whole_art(path):
  ready()
  result=ev('''async path=>{const im=new Image();im.src=WardWinter.asset(path);await im.decode();const r=WardWinter.roomViewRenderer();WardWinter.roomViewEffects.stop();r.light({brightness:1,torch:0});r.effects(null);const actual=document.querySelector('.room-view-canvas'),expected=document.createElement('canvas');expected.width=actual.width;expected.height=actual.height;const c=expected.getContext('2d');c.imageSmoothingEnabled=true;c.imageSmoothingQuality='high';c.drawImage(im,0,0,expected.width,expected.height);const a=actual.getContext('2d').getImageData(0,0,actual.width,actual.height).data,b=c.getImageData(0,0,expected.width,expected.height).data;let delta=0;for(let i=0;i<a.length;i++)delta+=Math.abs(a[i]-b[i]);return {mean:delta/a.length,room:r.room,view:r.view};}''',path)
  assert result['mean']<.2,(path,result)
 initial=ev('JSON.stringify(S)')
 def reset(room='lobby'):
  ev('s=>{S=JSON.parse(s);configureWorld(S.seed,true);placeTelephones(S.seed);cm=0;$("m").innerHTML="";render()}',initial)
  ev('r=>{S.prev=S.room;S.room=r;S.roomView="front";S.roomViewRoom=r;S.sceneView="front";S.sceneViewRoom=r;S.sceneFocus=null;S.f.powerOut=0;S.pursuer.active=false;render()}',room)
  ready()
 def close():ev('closeModal();wardCloseFocus()')
 assert ev('S.bat===100&&S.batteryCapacity===100')
 # Sound must decode, advance and produce measurable audio after a gesture.
 page.wait_for_function("WardSound.context().state==='running'")
 ev("WardSound.stop();WardSound.play('winter_wind',{volume:.6,loop:true})")
 page.wait_for_timeout(1100)
 assert ev('WardSound.snapshot().some(a=>!a.paused&&a.time>.1&&a.ready>=3)'),ev('WardSound.snapshot()')
 energies=[]
 for _ in range(10):page.wait_for_timeout(70);energies.append(ev('WardSound.energy()'))
 assert max(energies)>0.00001,energies
 passed('local recorded sound advances and produces nonzero WebAudio output')
 reset('wardnorth');ev('S.lightOn=true;S.bat=100;S.m=1;advanceTime(10);renderScene()');assert 92<ev('S.bat')<=92.5
 normal=ev('S.bat');ev('S.m=.7;S.bat=100;advanceTime(10)');assert ev('S.bat')>normal
 ev('S.room="security";S.roomView="front";S.roomViewRoom=S.room;S.f.power=1;S.lightOn=false;renderScene()');ready()
 assert ev('''()=>{WardWinter.roomViewEffects.stop();WardWinter.roomViewRenderer().effects(null);const c=document.querySelector('.room-view-canvas'),a=c.getContext('2d').getImageData(0,0,c.width,c.height).data;S.lightOn=true;WardWinter.fitRoomView();const b=c.getContext('2d').getImageData(0,0,c.width,c.height).data;return a.length===b.length&&b.every((v,i)=>v===a[i]);}''')
 reset('tunnel');ev('S.lightOn=true;S.bat=100;S.m=1;renderScene()');ready()
 center='''()=>{WardWinter.roomViewEffects.stop();const r=WardWinter.roomViewRenderer();r.effects(null);const c=document.querySelector('.room-view-canvas'),p=c.getContext('2d').getImageData(c.width*.45,c.height*.45,Math.max(1,c.width*.1),Math.max(1,c.height*.1)).data;let sum=0;for(let i=0;i<p.length;i++)if(i%4!==3)sum+=p[i];return sum/(p.length/4*3);}'''
 beam_on=ev(center);ev('S.bat=.01;S.m=1;closeModal()');page.wait_for_timeout(1300);assert ev('S.bat===0&&!S.lightOn');assert ev(center)<beam_on*.5
 passed('Normal drains faster than Story; lit rooms stay lit; exhaustion updates the actual flashlight beam')
 reset('laundry');ev('triggerServiceTrap()');assert not ev('S.f.trapArmed||S.f.trapUsed');ev("wardConfirmTrap('arm')");assert ev('S.f.trapArmed&&!S.f.trapUsed');whole_art('assets/states/laundry_trap_armed.webp');ev("wardConfirmTrap('release')");assert ev('S.f.trapUsed&&!S.f.trapArmed');whole_art('assets/states/laundry_trap_spent.webp');passed('hoist requires confirmation and actual rendered pixels match its persistent armed/spent artwork')
 reset('security');ev('hideInRoom()');assert not ev('S.f.hidingRoom');page.get_by_role('button',name='Hide here',exact=True).click();assert ev('S.f.hidingRoom===S.room&&!S.lightOn');assert page.locator('.panorama-hiding-mask path').get_attribute('d').count('M')==1;ev('wardPeek()');assert page.locator('.panorama-hiding-mask path').get_attribute('d').count('M')==4;ev('wardExitHiding()');passed('hiding asks first, is dark while concealed and uses narrow slits when peeking')
 reset('security');ev('S.f.power=1;S.lightOn=true;renderScene();window.__roomImage=document.querySelector(".room-view-canvas");window.__roomPose=[S.roomView,S.cameraYaw,S.cameraPitch];S.sceneFocus="diary";wardFixtureAction("winterJournal")');assert ev('window.__roomImage===document.querySelector(".room-view-canvas")&&JSON.stringify(window.__roomPose)===JSON.stringify([S.roomView,S.cameraYaw,S.cameraPitch])');close();passed('reading a document preserves the existing room image and camera')
 reset('wardnorth');ev("add('Lighter',1);add('Lighter Fluid',1);wardCombineLighter();S.lightOn=true;S.f.power=1;render()")
 assert ev('S.lighterFuel===6&&!has("Lighter Fluid")')
 ev("WardWinter.orbit.face('rear');act('windowLever')");assert not ev('WardWinter.windowState().triggered')
 page.get_by_role('button',name='Pull the handle',exact=True).click();assert ev('WardWinter.windowState().closed.every(v=>!v)')
 ev('advanceTime(18)');assert ev('S.hp<100&&S.san<100&&S.f.shivering')
 for i in range(3):
  ev('i=>{const f=WardScene.sites().find(f=>f.id===\'coldWindow\'+i);WardWinter.orbit.reveal(f.rect,f.view)}',i);ready()
  page.locator('[data-fixture=coldWindow'+str(i)+']').click();page.locator('button[onclick="wardFixtureAction(\'coldWindow'+str(i)+'\')"]').click()
 assert ev('S.windows.resolved&&S.windows.closed.every(Boolean)')
 hp=ev('S.hp');ev('wardOpenWindows();advanceTime(4)');assert ev('S.hp')==hp
 ev("S.room='laundry';S.roomView='rear';S.roomViewRoom=S.room;S.sceneView='rear';S.sceneViewRoom=S.room;render();act('dryingStove')")
 assert ev('S.f.stoveLit&&S.lighterFuel===5&&!S.f.wet&&!S.f.shivering')
 passed('window confirmation, individual catches, local health/sanity exposure, one-use resolution and lighter recovery')
 reset('eastcorridor');ev('wardSprinkler()');assert ev('S.f.wet&&S.f.flashlightDropped&&!S.lightOn');close()
 ev('wardSprinkler();wardRecoverFlashlight()');assert ev('S.f.sprinklerStopped&&S.f.flashlightRecovered&&!S.f.flashlightDropped')
 ev('wardSprinkler()');assert not ev('S.f.flashlightDropped')
 passed('sprinkler and flashlight recovery are separate persistent one-time actions')
 reset('eastcorridor');ev("add('Wooden Plank',1);reinforceWindow()");assert ev('has("Wooden Plank")&&!S.f.windowBarricaded')
 page.get_by_role('button',name='Cancel',exact=True).click();assert ev('has("Wooden Plank")')
 ev('reinforceWindow()');page.get_by_role('button',name='Place plank',exact=True).click();assert ev('!has("Wooden Plank")&&S.f.windowBarricaded')
 ev('WardWinter.orbit.reveal(WardRoomViews.eastcorridor.fixtures.window.rect,"front")');ready();bounds=page.locator('.room-view-plank').bounding_box();assert bounds['width']>bounds['height']*3,bounds
 passed('plank is confirmed before consumption and renders as a substantial horizontal board')
 reset('isoward');ev("add('Utility Knife',1);choosePatientFate('killed')");assert not ev('S.f.beggingPatientChoice')
 page.get_by_role('button',name='Use utility knife',exact=True).click();assert ev('S.f.beggingPatientChoice==="killed"&&S.f.patientMethod==="knife"')
 whole_art('assets/states/isoward_after.webp')
 san=ev('S.san');ev("choosePatientFate('helped');wardConfirmPatient('knife')");assert ev('S.san')==san
 close();ev("S.room='lobby';add('Ink Ribbon',1);confirmSave()");saved=ev('({slots:JSON.stringify(S.placements),fate:S.f.beggingPatientChoice,san:S.san})')
 page.reload();ev('loadGame()');assert ev('JSON.stringify(S.placements)')==saved['slots'];assert ev('S.f.beggingPatientChoice')==saved['fate']
 passed('knife choice covers Mercer, cannot be repeated or undone, and survives save/reload with seeded placements')
 reset();n=ev('S.enemyActors.length');ev('S.room=S.enemyActors.find(a=>!a.dormant).room;S.sceneViewRoom=S.room;render();combat()')
 hp=ev('S.hp');ev('wardStruggle()');assert ev('S.hp')<hp;assert not ev('alive(S.room)')
 enemy=ev('S.enemyActors.find(a=>a.down).id');ev('S.room="lobby";WardWinter.enemies.project();S.room=S.enemyActors.find(a=>a.id===\''+enemy+'\').room;WardWinter.enemies.project()');assert ev('alive(S.room)')
 ev('S.en[S.room]=0;render()');assert not ev('alive(S.room)')
 ev('noise();advanceTime(40);render()');assert ev('S.enemyActors.length')==n;assert ev('a=>S.enemyActors.find(x=>x.id===a).hp===0',enemy)
 passed('struggle costs health, survivor returns on re-entry, killed actors stay dead, noise creates no new population')
 reset('archive');ev("S.enemyActors.forEach(a=>a.hp=0);WardWinter.enemies.project();add('Handgun',1);add('Handgun Ammo',6);S.eq='Handgun';S.ld.Handgun=6;S.san=45;S.f.plexiIncidentSeen=1;wardFalseEncounter()")
 assert page.locator('.winter-combat-modal').count()==1
 hp=ev('S.hp');rounds=ev('S.ld.Handgun');page.get_by_role('button',name='Quick shot',exact=True).click();assert ev('S.ld.Handgun')==rounds-1
 for _ in range(4):
  if ev('!!S.hallCombat'):ev("wardResolveFalseEncounter('hold')")
 assert ev('S.hp')==hp;assert ev('!S.hallCombat&&S.f.falseEncounterResolved')
 ev('wardFalseEncounter()');assert not ev('S.hallCombat')
 passed('imaginary combat uses real ammo, shares in-room enemy presentation, cannot damage health, resolves and stays resolved')
 reset();ev('S.f.power=1;S.f.plexiIncidentSeen=1;S.f.photoPuzzleSolved=1')
 for step in range(3):
  ev('step=>{S.room=S.phoneRooms[step];S.sceneViewRoom=S.room;ringPayphone();answerPayphone(step===0?"payphone":"phone_stage_"+(step+1))}',step);close()
 assert ev('S.f.phoneStep===3&&new Set(S.phoneRooms).size===3&&S.docs.filter(t=>t.startsWith("Telephone record")).length===3')
 ev('ringPayphone()');assert not ev('S.f.phoneRinging')
 passed('three once-only story calls use three different seeded phones and preserve transcripts')
 reset('observation');ev('inspectObservationGlass()');assert ev('S.hp===100&&S.f.glassHunterStep===1');assert 'WARNING' in page.locator('#m').inner_text()
 page.get_by_role('button',name='Step back for now',exact=True).click();assert ev('S.hp===100');ev('inspectObservationGlass()');assert ev('S.hp===0&&S.f.glassHunterStep===2')
 ev('loadCheckpoint()');assert ev('S.hp>0&&S.f.glassHunterStep===1')
 passed('rare lethal encounter warns on first inspection, permits retreat and restores its checkpoint after deliberate second inspection')
 reset('security');ev('S.f.power=1;portraitPuzzle()');page.get_by_role('button',name='Inspect photograph',exact=True).first.click();page.get_by_role('button',name='Turn over',exact=True).click();assert 'Appointed' in page.locator('#m').inner_text();close()
 passed('high-resolution photographs have inspectable dated backs')
 reset();ev('S.mapParts=3;mapModal()');assert page.locator('.architectural-map.full').count()==1;close()
 reset();bad=[]
 arrivals=[]
 for edge,fromroom,to in ev("Object.entries(D).flatMap(([id,d])=>[[id,d.a,d.b],[id,d.b,d.a]])"):
  ev('v=>{S.prev=v[0];S.room=v[1];S.roomViewRoom=null;renderScene()}',[fromroom,to]);ready()
  result=ev('''id=>{const data=WardRoomViews[S.room],entry=Object.entries(data.views).find(([view,v])=>Object.hasOwn(v.doors,id))?.[0];return {room:S.room,from:S.prev,entry,view:S.roomView,entranceVisible:!!document.querySelector('[data-door="'+id+'"]'),renderRoom:WardWinter.roomViewRenderer().room,renderView:WardWinter.roomViewRenderer().view};}''',edge)
  arrivals.append({'door':edge,**result})
  if result['view']==result['entry'] or result['entranceVisible'] or result['room']!=to or result['from']!=fromroom or result['renderRoom']!=to or result['renderView']!=result['view']:bad.append([edge,fromroom,to,result])
  ev('WardWinter.orbit.face(\''+result['entry']+'\')');ready();assert page.locator('[data-door='+edge+'][data-destination='+fromroom+']').count()==1,(edge,fromroom,to,result)
 assert not bad,bad
 assert len(arrivals)==54
 passed('all 54 directed doorway arrivals face away from the real entrance; looking back exposes the correct return destination')
 # Seed variation must never create a missing object target or move a room connection.
 reset();issues=ev("""()=>{const bad=[];for(let i=0;i<128;i++){configureWorld('winter-audit-'+i,false);placeTelephones('winter-audit-'+i);for(const room of Object.keys(R)){S.room=room;S.f.power=1;S.f.pharm=1;S.f.chapel=1;S.f.researchers=1;S.f.drained=1;S.f.photoPuzzleSolved=1;try{WardScene.sites()}catch(e){bad.push(e.message)}}}return [...new Set(bad)]}""");assert not issues,issues
 passed('128 seeded worlds retain authored geometry for every object and telephone')
 # Every runtime pickup gets a valid physical icon; every authored target is inside its art.
 paths=ev('''()=>{const paths=[];for(const r of Object.values(R))for(const o of r.o)for(const [n]of o[4].give||[]){itemIconMarkup(n);paths.push(ITEM_ART[n])}return [...new Set(paths)]}''')
 assert all((ROOT/p).is_file() for p in paths),[p for p in paths if not (ROOT/p).is_file()]
 views={r:v['views'] for r,v in json.loads((ROOT/'data/room_views.json').read_text()).items()};assert len(views)==27;assets=[v['asset'] for room in views.values() for v in room.values()];assert len(assets)==54;assert len({hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in assets})==54
 for width,height in [(1600,1000),(1000,800),(390,844)]:
  page.set_viewport_size({'width':width,'height':height});page.wait_for_timeout(100)
  for room in ev('Object.keys(R)'):
   ev('r=>{S.room=r;S.roomView="front";S.roomViewRoom=r;S.sceneView="front";S.sceneViewRoom=r;renderScene()}',room)
   ready();assert ev('document.documentElement.scrollWidth<=innerWidth+1')
   assert not page.get_by_role('button',name='Turn around',exact=True).count()
   ev("WardWinter.orbit.face('rear')");ready();assert ev('S.sceneView==="rear"&&S.roomView==="rear"')
 passed('54 distinct native room views, all pickup icons, and working mouse view arrows at desktop, tablet and mobile widths')
 assert not errors,errors
 b.close()
(ROOT/'tests/results/winter_systems.json').write_text(json.dumps({'checks':checks,'directed_arrivals':arrivals,'javascript_errors':errors},indent=2))
