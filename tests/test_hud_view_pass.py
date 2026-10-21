"""Regressions for physical PEEK, clinical colour, local CRT light and mouse HUD."""
from pathlib import Path
from playwright.sync_api import sync_playwright
from mouse_controls import turn_room
import json,sys
ROOT=Path(__file__).resolve().parents[1]
URL=sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8010'
OUT=ROOT/'tests/results';OUT.mkdir(exist_ok=True)
report={'checks':[],'errors':[]}
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 page=browser.new_page(viewport={'width':1672,'height':941},service_workers='block')
 page.on('pageerror',lambda error:report['errors'].append(str(error)))
 page.goto(URL);page.get_by_role('button',name='BEGIN INVESTIGATION').click();page.evaluate('nextIntro();nextIntro();nextIntro()')
 def ready():page.wait_for_function('WardWinter.roomViewRenderer()?.loaded&&!WardWinter.orbit.busy')
 ready();page.wait_for_function('!!WardWinter.playDoorTransition')
 def clean_captions():
  result=page.evaluate('''()=>{const hidden=id=>{const n=document.getElementById(id),r=n.getBoundingClientRect();return r.width===0&&r.height===0;};return {cards:document.querySelector('.story-caption').children.length,legacyInCards:!!document.querySelector('.narrative-focus .message-stream'),sourceHidden:getComputedStyle(hudFeedbackSources).display==='none'&&hudFeedbackSources.inert&&hudFeedbackSources.contains(document.querySelector('.message-stream')),legacyHidden:['feedbackBox','ev','sceneDrawer'].every(hidden),narration:getComputedStyle(document.querySelector('.narration-block')).backgroundColor,thoughts:getComputedStyle(sceneThought).backgroundColor};}''')
  assert result=={'cards':2,'legacyInCards':False,'sourceHidden':True,'legacyHidden':True,'narration':'rgba(0, 0, 0, 0)','thoughts':'rgba(0, 0, 0, 0)'},result
 clean_captions()
 for health,label,color in [(90,'FINE','rgb(131, 183, 154)'),(50,'CAUTION','rgb(210, 170, 99)'),(15,'DANGER','rgb(216, 102, 92)')]:
  value=page.evaluate('''hp=>{S.hp=hp;WardWinter.updateStatus();return {label:conditionLabel.textContent,line:getComputedStyle(heartLine).color,text:getComputedStyle(conditionLabel).color};}''',health)
  assert value=={'label':label,'line':color,'text':color},value
 report['checks'].append('Physical FINE, CAUTION and DANGER trace and label use matching green, amber and red.')
 page.evaluate('S.hp=100;WardWinter.updateStatus()')
 page.get_by_role('button',name='Options',exact=True).click()
 assert not page.locator('#m button[onclick*="saveMenu"]').count()
 assert page.locator('select[aria-label="Interaction hints"]').input_value()=='subtle'
 page.evaluate('closeModal()');assert page.get_by_role('button',name='Save',exact=True).is_visible()
 report['checks'].append('Subtle is default; save controls are separate from Options and available from the Save navigation action.')
 # Current front and rear bearings must differ by exactly 180 degrees; the mini
 # map refreshes without requiring a travel or another click on the map.
 page.evaluate('S.mapParts=3;render()');ready();before=page.locator('.floorplan-player-arrow').first.get_attribute('transform')
 turn_room(page);ready();after=page.locator('.floorplan-player-arrow').first.get_attribute('transform')
 assert before!=after,(before,after)
 a,b=[int(x.removeprefix('rotate(').removesuffix(')')) for x in (before,after)];assert (b-a)%360==180
 report['checks'].append('A mouse facing change immediately rotates the map arrow by 180 degrees.')
 # PEEK must have an actually transparent parent. Pixel comparison samples the
 # transparent slits against the room canvas; closed cover remains truly dark.
 page.evaluate("S.room='security';S.prev='lobby';S.roomView='front';S.roomViewRoom=S.room;S.f.hidingRoom='security';S.f.hidingType='locker';S.f.lockerPeeking=false;render()");ready()
 assert page.locator('.hiding-physical.closed').is_visible()
 closed=page.locator('.panorama-hiding-mask path').first.get_attribute('d')
 assert closed=='M0 0H100V100H0Z '
 page.get_by_role('button',name='Peek',exact=True).click()
 assert page.locator('.hiding-physical.peeking').is_visible()
 masked=page.evaluate('''()=>({background:getComputedStyle(sceneFocusOverlay).backgroundColor,holes:document.querySelector('.panorama-hiding-mask path').getAttribute('d'),canvas:WardWinter.roomViewRenderer().loaded})''')
 assert masked['background']=='rgba(0, 0, 0, 0)' and masked['holes'].count('M')==4 and masked['canvas'],masked
 page.screenshot(path=str(OUT/'hud-peek-locker.png'))
 page.get_by_role('button',name='Exit',exact=True).click();ready()
 report['checks'].append('Closed hiding is opaque black; PEEK has three usable physical slots showing the live room through a transparent parent.')
 # Local emissive CRT pixels exist only in the authored screen rectangles and
 # retain legible room images even while overhead circuits are not powered.
 page.evaluate('S.f.power=0;S.f.powerOut=0;render()');ready();page.wait_for_timeout(800)
 pixels=page.evaluate('''()=>{const fx=WardWinter.roomViewEffects,c=fx.screenCanvas,ctx=c.getContext('2d'),im=ctx.getImageData(0,0,c.width,c.height).data,screens=fx.data.security.front.screens;let opaque=0,bad=0,bright=0;for(let y=0;y<c.height;y++)for(let x=0;x<c.width;x++){const at=(y*c.width+x)*4;if(!im[at+3])continue;opaque++;if(!screens.some(({rect:[cx,cy,w,h]})=>x>=Math.floor((cx-w/2)*c.width/100)-1&&x<=Math.ceil((cx+w/2)*c.width/100)+1&&y>=Math.floor((cy-h/2)*c.height/100)-1&&y<=Math.ceil((cy+h/2)*c.height/100)+1))bad++;if(im[at]>60)bright++;}return {opaque,bad,bright};}''')
 assert pixels['opaque']>1000 and pixels['bad']==0 and pixels['bright']>200,pixels
 page.screenshot(path=str(OUT/'hud-security-crt.png'))
 report['checks'].append('Standby security feeds show monochrome rooms, and all emissive pixels remain strictly inside six authored CRT rectangles.')
 page.locator('[data-fixture="monitors"]').click()
 page.get_by_role('button',name='Camera feed',exact=True).click()
 preview=page.locator('.surveillance-finding-preview')
 preview.wait_for(state='visible');page.wait_for_function("document.querySelector('.surveillance-finding-preview')?.complete&&document.querySelector('.surveillance-finding-preview')?.naturalWidth>1000")
 assert preview.get_attribute('src').endswith('assets/room_views/lobby_front.webp')
 assert 'grayscale(1)' in preview.evaluate('e=>getComputedStyle(e).filter')
 page.get_by_role('button',name='Return to room ×',exact=True).click()
 report['checks'].append('Camera feed inspection uses a clear monochrome Lobby thumbnail rather than a generic document or pouch icon.')
 page.locator('[data-fixture="cabinet"]').click()
 page.get_by_role('button',name='Folding utility knife',exact=True).click()
 page.get_by_role('button',name='Take Utility Knife',exact=True).click()
 page.get_by_role('button',name='Return to room ×',exact=True).click()
 clean=page.evaluate('''()=>({focus:S.sceneFocus,hidden:sceneFocusOverlay.classList.contains('hid'),children:sceneFocusOverlay.children.length,background:getComputedStyle(sceneFocusOverlay).backgroundColor,canvasFilter:getComputedStyle(document.querySelector('.room-view-canvas')).filter})''')
 assert clean=={'focus':None,'hidden':True,'children':0,'background':'rgba(0, 0, 0, 0)','canvasFilter':'none'},clean
 clean_captions()
 report['checks'].append('Taking the Security utility knife and returning to the room clears the contents overlay and leaves no colour filter or stale focus container.')

 # Trigger and stop the once-only sprinkler through its actual fixture card.
 page.evaluate("S.room='eastcorridor';S.prev='lobby';S.roomView='front';S.roomViewRoom=S.room;add('Flashlight',1);S.lightOn=true;render()")
 ready();page.locator('[data-fixture="valve"]').click()
 page.get_by_role('button',name='Interact',exact=True).click()
 page.get_by_role('button',name='Reach for the shutoff',exact=True).click()
 page.get_by_role('button',name='Interact',exact=True).click();ready()
 assert page.evaluate('S.f.sprinklerStopped&&S.f.wet&&S.f.shivering')
 clean_captions()
 assert page.evaluate("(()=>{const r=document.querySelector('.room-view-frame').getBoundingClientRect(),c=document.querySelector('.narrative-focus').getBoundingClientRect();return c.top>=r.top&&c.bottom<=r.bottom;})()")
 page.screenshot(path=str(OUT/'hud-after-sprinkler.png'))
 report['checks'].append('After triggering and closing the sprinkler, narration and thoughts remain two transparent cards over the artwork with no extra feedback panels beneath them.')

 # Completion is exactly once; exposure changes duration without timer drift.
 durations=page.evaluate('''()=>{S.f.wet=0;S.f.shivering=0;S.f.coldExposure=0;let a=WardWinter.playDoorTransition({from:'security',to:'lobby',duration:1000});const dry=a.duration;a.cancel();S.f.wet=1;let b=WardWinter.playDoorTransition({from:'security',to:'lobby',duration:1000});const wet=b.duration;b.cancel();S.f.wet=0;return {dry,wet};}''')
 assert durations['wet']>durations['dry']*1.5,durations
 page.evaluate("window.doorCompletions=0;WardWinter.playDoorTransition({from:'security',to:'lobby',duration:1000,onComplete:()=>doorCompletions++})")
 page.wait_for_timeout(450);assert page.locator('.ward-door-slab').is_visible();page.screenshot(path=str(OUT/'hud-door-hinge.png'))
 page.wait_for_function('doorCompletions===1');page.wait_for_timeout(100);assert page.evaluate('doorCompletions')==1
 report['checks'].append('Hinged door/latch animation completes once and takes longer with wet hands.')
 # Real door entry points share the latch. Repeated clicks, a map command and
 # room-facing inputs cannot start another transition or mutate the room.
 page.evaluate("S.room='security';S.prev='lobby';S.roomView='front';S.roomViewRoom=S.room;S.dr.es=1;render()")
 ready();box=page.locator('[data-door="es"]').bounding_box();assert box
 point={'x':box['x']+box['width']/2,'y':box['y']+box['height']/2}
 page.mouse.click(**point);assert page.evaluate('!!WardWinter.travelling')
 page.mouse.click(**point)
 page.evaluate("sceneDoorTravel('eastcorridor');mapTravel('lobby');go('lobby');WardWinter.orbit.look();invModal()")
 assert page.locator('.ward-door-passage').count()==1
 assert page.evaluate("S.room==='security'&&S.roomView==='front'&&!document.querySelector('#m .md')")
 frame=page.locator('.room-view-frame').bounding_box();assert frame
 page.mouse.move(frame['x']+frame['width']*.75,frame['y']+frame['height']*.12);page.mouse.down();page.mouse.move(frame['x']+frame['width']*.25,frame['y']+frame['height']*.12,steps=2);page.mouse.up()
 assert page.evaluate("S.roomView==='front'")
 page.wait_for_function("!WardWinter.travelling&&S.room==='eastcorridor'")
 assert page.locator('.ward-door-passage').count()==0
 report['checks'].append('Rapid real door clicks and direct map/turn/inventory commands stay locked to one native transition; room-facing drags cannot bypass it.')
 # Keep the Pause probe independent of the rapid-input probe. The native door
 # takes about one second; under browser load that whole input sequence may
 # legitimately finish before its last click reaches Pause.
 page.evaluate("S.room='security';S.prev='lobby';S.roomView='front';S.roomViewRoom=S.room;S.dr.es=1;render()")
 ready();box=page.locator('[data-door="es"]').bounding_box();assert box
 page.mouse.click(x=box['x']+box['width']/2,y=box['y']+box['height']/2)
 assert page.evaluate("WardWinter.travelling&&S.room==='security'")
 page.get_by_role('button',name='Pause game',exact=True).click()
 assert page.get_by_role('heading',name='PAUSED',exact=True).is_visible()
 page.wait_for_timeout(1250)
 state=page.evaluate("({travelling:!!WardWinter.travelling,room:S.room,paused:WardWinter.isPaused(),hp:S.hp,door:!!document.querySelector('.ward-door-passage'),modal:m.innerHTML.slice(0,200)})")
 assert state['travelling'] and state['room']=='security',state
 page.get_by_role('button',name='Resume game',exact=True).click()
 page.wait_for_function("!WardWinter.travelling&&S.room==='eastcorridor'")
 assert page.locator('.ward-door-passage').count()==0
 report['checks'].append('Pause remains available during a fresh native door transition; completion waits for Resume and removes its passage overlay.')

 assert not report['errors'],report['errors'];browser.close()
(OUT/'hud_view_pass.json').write_text(json.dumps(report,indent=2)+'\n')
for check in report['checks']:print('PASS',check)
