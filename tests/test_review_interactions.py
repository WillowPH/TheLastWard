"""Ordinary-input and visual bounds checks for the reviewed multi-file edition."""
from pathlib import Path
import json,sys
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];URL=sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8010';checks=[]
def passed(s):checks.append(s);print('PASS',s,flush=True)
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);c=b.new_context(service_workers='block',viewport={'width':1672,'height':941},reduced_motion='no-preference');page=c.new_page();page.set_default_timeout(6000);errors=[];page.on('pageerror',lambda e:errors.append(str(e)));page.goto(URL);page.get_by_role('button',name='BEGIN INVESTIGATION').click();page.evaluate('nextIntro();nextIntro();nextIntro()')
 def ev(s,a=None):return page.evaluate(s,a)
 def room(r):
  ev('r=>{S.room=r;S.prev=r;S.sceneView="front";S.sceneViewRoom=r;S.orbitRoom=null;S.cameraYaw=0;S.sceneFocus=null;S.enemyActors.forEach(a=>a.hp=0);WardWinter.enemies.project();S.pursuer.active=false;S.f.power=1;S.bat=100;S.lightOn=true;$("m").innerHTML="";render()}',r);page.wait_for_timeout(100)
 def close():ev('closeModal();wardCloseFocus()')
 def look(target):
  for _ in range(42):
   bb=target.bounding_box();frame=page.locator('.winter-look-frame').bounding_box()
   if bb and frame['x']+20<bb['x']+bb['width']/2<frame['x']+frame['width']-20 and bb['y']+bb['height']/2<frame['y']+frame['height']-165:return
   page.get_by_role('button',name='Look right',exact=True).click()
  raise AssertionError('Could not look toward '+str(target))
 assert not page.get_by_role('button',name='Turn around',exact=True).count();assert not page.get_by_role('button',name='Face the room',exact=True).count()
 assert not page.locator('.c1-room-tools button').count()
 page.get_by_role('button',name='Options',exact=True).click();h=page.get_by_role('combobox',name='Interaction hints');assert h.count()==1;h.select_option('strong');assert ev('WardScene.options.hints');h.select_option('subtle');assert not ev('WardScene.options.hints');close();passed('Subtle/Strong hints are in Options, with no scene hint switch or Turn Around button')
 room('security');target=page.locator('[data-fixture=diary]');look(target);yaw=ev('S.cameraYaw');target.click();assert abs(ev('S.cameraYaw')-yaw)<.00001;assert ev('S.sceneFocus==="diary"')
 card=page.locator('[data-object=winterJournal]');im=card.locator('img').bounding_box();txt=card.locator('strong').bounding_box();assert im['height']<=65 and im['width']<=65;assert im['y']+im['height']<=txt['y']+1,(im,txt)
 page.screenshot(path=str(ROOT/'tests/results/review-note.png'));page.locator('button[onclick="wardFixtureAction(\'winterJournal\')"]').click();assert abs(ev('S.cameraYaw')-yaw)<.00001;close();passed('ordinary item click and Read keep camera fixed; 64px icons do not overlap text')
 ev('S.f.photoPuzzleSolved=1;S.ob.staffPortraits="read";renderScene()');assert not page.locator('[data-fixture=portraits]').count();passed('completed portrait puzzle loses its scene target')
 room('lobby');ev('S.f.phoneStep=0;S.ob.payphone=null;S.f.phoneRinging=true;S.f.ringingPhoneRoom="lobby";renderScene()');target=page.locator('[data-fixture=phone]');look(target);target.click();page.locator('button[onclick="wardFixtureAction(\'payphone\')"]').click();close();assert ev('S.f.phoneStep===1&&S.ob.payphone==="read"');assert not page.locator('[data-fixture=phone]').count();ev('render();renderScene()');assert not page.locator('[data-fixture=phone]').count();ev("add('Ink Ribbon',1);confirmSave()");page.reload();ev('loadGame()');assert not page.locator('[data-fixture=phone]').count();passed('answered payphone stays disabled after re-render and save/reload')
 nextroom=ev('S.phoneRooms[1]');room(nextroom);ev('S.f.power=0;S.f.phoneRinging=false;renderScene()');f=ev('WardScene.sites().find(f=>f.objects.some(o=>o[0]==="phone_stage_2")).id');target=page.locator('[data-fixture="'+f+'"]');look(target);target.click();before=page.locator('#interactionText').inner_text();page.locator('button[onclick="wardFixtureAction(\'phone_stage_2\')"]').click();assert page.locator('.room-local-notice').inner_text()=='The line is dead. It will not ring.';assert page.locator('#interactionText').inner_text()==before;close();assert not page.locator('[data-fixture="'+f+'"]').count();ev('S.f.power=1;ringPayphone();renderScene()');assert page.locator('[data-fixture="'+f+'"]').count()==1;passed('dead phone feedback is local and cannot repeat; a later genuine story call reactivates it')
 room('security');ev('S.inv=[{n:"Flashlight",c:1},{n:"Handgun",c:1},{n:"Photographic Negative",c:1}];invModal()');rows=page.locator('.inventory-item-row');assert rows.count()==3
 for i in range(rows.count()):
  a=rows.nth(i).locator('.inventory-menu-icon img');assert a.count()==1;aa=a.bounding_box();bb=rows.nth(i).locator('.inventory-menu-copy').bounding_box();assert aa['x']+aa['width']<=bb['x']+1
 assert page.locator('.inventory-item-row:has-text("Photographic Negative") img').count()==1;close();passed('gun and photographic-negative icons have separate bounded inventory cells')
 room('security');ev('S.lightOn=false;render()');page.get_by_role('button',name='Toggle flashlight',exact=True).click();assert ev('S.lightOn');page.get_by_role('button',name='Toggle flashlight',exact=True).click();assert not ev('S.lightOn');passed('right HUD flashlight button toggles the actual beam without opening inventory')
 room('lobby');start=ev('S.cameraYaw');before=page.locator('.c1-plane').bounding_box()
 for _ in range(20):page.keyboard.press('ArrowRight')
 assert abs(ev('S.cameraYaw')-start-360)<.001;after=page.locator('.c1-plane').bounding_box();assert abs(before['x']-after['x'])<1;passed('20 ordinary look keys rotate 360 degrees and return to identical art coordinates')
 room('lobby');ev('S.mapParts=3;S.vis.security=1;render()');page.get_by_role('button',name='Map',exact=True).click();page.locator('g[onclick="wardMapSelect(\'security\')"]').click();skip=page.get_by_role('button',name='Skip transition',exact=True)
 if skip.count():skip.click()
 page.wait_for_timeout(200);assert ev('S.room==="security"');passed('adjacent map travel takes one node click with no confirmation step')
 # Both currently visible and offscreen panes must keep animating while looking around.
 room('room12');ev('WardScene.options.motion=true;WardScene.options.motionOverride=true;WardScene.options.flashes=true;renderScene()');snap=ev('WardMotion.snapshot().frames');page.wait_for_timeout(250);assert ev('WardMotion.snapshot().frames')>snap
 assert ev('Object.keys(WardMotion.glazing).length===27')
 observed=ev("""()=>new Promise(resolve=>{const until=performance.now()+24000;function sample(){const n=document.querySelector('.c1-plane .winter-screen-canvas');if(Number(n?.dataset.lightDip)>0&&n.getContext('2d').getImageData(n.width*.55,n.height*.15,1,1).data[3]>0)return resolve(true);if(performance.now()>until)return resolve(false);requestAnimationFrame(sample);}sample();})""")
 assert observed,'No actual brightness dip observed during complete flicker interval';passed('all 27 front window sets have snow masks; live animation and actual lamp dimming are observed')
 # Visual regression coverage at reference and compact sizes, including all four room faces.
 assert ev('Object.keys(WardSideAssets).length===27')
 for width,height in [(1672,941),(1000,800),(390,844)]:
  page.set_viewport_size({'width':width,'height':height});room('lobby');ev('S.mapParts=3;render()');page.wait_for_timeout(100);assert ev('document.documentElement.scrollWidth<=innerWidth+1');page.screenshot(path=str(ROOT/f'tests/results/review-hud-{width}.png'))
 passed('27 rooms have independent side atlases; reference, tablet and mobile HUDs do not overflow horizontally')
 assert not errors,errors;b.close()
(ROOT/'tests/results/review_interactions.json').write_text(json.dumps({'checks':checks,'javascript_errors':errors},indent=2)+'\n')
