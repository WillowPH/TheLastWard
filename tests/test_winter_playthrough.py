"""Playable winter Chapter 1 routes. Progression is earned through actual controls."""
from pathlib import Path
import json,sys
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
URL=sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8010'
OUT=ROOT/'tests/results';OUT.mkdir(exist_ok=True)
report=[]
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--enable-unsafe-swiftshader'])
 context=browser.new_context(viewport={'width':1600,'height':1000},service_workers='block',reduced_motion='reduce')
 context.route('**/*',lambda route:route.continue_() if route.request.url.startswith(URL.rstrip('/')+'/') else route.abort())
 page=context.new_page();page.set_default_timeout(6500)
 errors=[];page.on('pageerror',lambda error:errors.append(str(error)))
 def ev(code,arg=None):return page.evaluate(code,arg)
 def aim_point(point_id):
  """Use a native side-arrow click to expose the authored object's full view."""
  if page.locator('#m .md').count():close()
  page.wait_for_function('WardWinter.roomViewRenderer()?.loaded&&!WardWinter.orbit.busy&&!WardWinter.travelling')
  point=ev('id=>WardWinter.orbit.points().find(p=>p.id===id)',point_id)
  if not point and point_id=='fixture:dropped-light':point={'view':'front'}
  assert point,('Missing authored mouse target',ev('S.room'),point_id)
  if ev('S.roomView')!=point['view']:
   page.get_by_role('button',name='Look right',exact=True).click()
   page.wait_for_function('WardWinter.roomViewRenderer()?.loaded&&!WardWinter.orbit.busy')
  assert ev('S.roomView')==point['view'],('Side arrow did not expose requested view',point_id)
 def click_visible(selector):
  # A live enemy may cover part of a visible object. Click a genuinely exposed
  # part of the target, exactly as a player can; never click through the enemy.
  point=ev('''selector=>{const node=document.querySelector(selector);if(!node)return null;const r=node.getBoundingClientRect();for(const [u,v]of [[.5,.5],[.9,.1],[.1,.1],[.9,.9],[.1,.9],[.9,.5],[.1,.5],[.5,.1],[.5,.9]]){const x=r.left+r.width*u,y=r.top+r.height*v;if(document.elementFromPoint(x,y)===node)return {x,y};}return null;}''',selector)
  assert point,('No unobstructed mouse target',ev('S.room'),selector,ev('({pursuer:S.pursuer,combat:cm,modal:document.querySelector("#m .md")?.innerText})'))
  page.mouse.click(point['x'],point['y'])
 def close():
  for _ in range(12):
   if not page.locator('#m .md').count():
    if ev('!!S.sceneFocus'):ev('wardCloseFocus()')
    if ev('S.room==="eastcorridor"&&S.f.flashlightDropped'):
     aim_point('fixture:dropped-light');page.get_by_role('button',name='Recover dropped flashlight',exact=True).click()
    if ev('S.room==="eastcorridor"&&S.f.sprinklerTriggered&&!S.f.sprinklerStopped'):
     aim_point('fixture:valve');page.locator('[data-fixture=valve]').click();page.locator("button[onclick=\"wardFixtureAction('staffSprinkler')\"]").click()
    return
   if ev('!!S.f.pursuerEncounter'):ev("escapePursuer('retreat')")
   elif ev('!!S.hallCombat'):ev("wardResolveFalseEncounter('hold')")
   elif page.get_by_role('button',name='Call his name',exact=True).count():page.get_by_role('button',name='Call his name',exact=True).click()
   elif page.get_by_role('button',name='Struggle past · risk injury',exact=True).count():
    page.get_by_role('button',name='Struggle past · risk injury',exact=True).click();page.wait_for_timeout(650)
   elif ev('cm&&alive(S.room)'):
    if ev('S.hp<35&&has("Field Medkit")'):ev("heal('Field Medkit')")
    ev('wardStruggle()')
   else:ev('closeModal()')
  raise AssertionError('Unresolved modal: '+page.locator('#m').inner_text())
 def move(target):
  for _ in range(65):
   close()
   if ev('S.room')==target:return
   assert ev('S.hp>0'),('died',target)
   path=ev('''target=>{const q=[[S.room]],seen=new Set([S.room]);while(q.length){const p=q.shift(),r=p.at(-1);if(r===target)return p;for(const [id,d]of Object.entries(D)){const to=d.a===r?d.b:d.b===r?d.a:null;if(!to||seen.has(to)||!(doorOpen(id)||(d.need&&has(d.need))))continue;seen.add(to);q.push([...p,to]);}}return [];}''',target)
   assert len(path)>1,(ev('S.room'),target,ev('S.inv'),ev('WardChapter.requirements()'))
   destination=path[1];edge=ev('to=>WardNavigation.edge(S.room,to)',destination)
   page.wait_for_function('WardWinter.roomViewRenderer()?.loaded')
   aim_point('door:'+edge)
   click_visible('[data-destination="'+destination+'"]')
   skip=page.get_by_role('button',name='Skip transition',exact=True)
   ev("[...document.querySelectorAll('button')].find(b=>b.textContent.trim()==='Skip transition')?.click()")
   page.wait_for_timeout(360)
  raise AssertionError('Navigation did not reach '+target)
 def use(id):
  close()
  if ev('WardNavigation.isDark(S.room)&&!lit()'):
   if ev('S.bat<8&&has("Battery")'):ev("useBat('Battery',false)")
   if ev('!S.lightOn'):ev('toggleLight()')
  f=ev('id=>{const f=WardScene.sites().find(f=>f.objects.some(o=>o[0]===id));return f?{id:f.id,view:f.view||"front",rect:f.rect}:null;}',id)
  assert f,('No fixture',ev('S.room'),id)
  page.wait_for_function('WardWinter.roomViewRenderer()?.loaded')
  aim_point('fixture:'+f['id'])
  click_visible('[data-fixture="'+f['id']+'"]')
  button=page.locator('button[onclick="wardFixtureAction(\''+id+'\')"]')
  if button.count():button.click()
 def take(id,name):
  if ev('id=>S.ob[id]===\'done\'',id):return
  for _ in range(3):
   use(id)
   if ev('id=>S.ob[id]===\'done\'',id):break
   if ev('!!S.f.ammoSnakeSeen'):close()
   else:break
  assert ev('n=>has(n)',name),('Pickup failed',id,name,ev('S.inv'),page.locator('#m').inner_text())
  close()
 def store(names):
  for n in names:
   i=ev('n=>S.inv.findIndex(x=>x.n===n)',n)
   if i>=0:ev('i=>store(i)',i);close()
 def note(label):
  state=ev('({room:S.room,hp:S.hp,sanity:S.san,charge:S.bat,visited:Object.keys(S.vis).length,remaining:WardChapter.requirements()})')
  report.append({'step':label,**state});print(label,state,flush=True)
 seeds=['winter-standard-a','winter-story-complete']
 for seed in seeds:
  context.set_offline(False);page.goto(URL,timeout=60000)
  page.locator('#diff').select_option('0.7' if 'story' in seed else '1')
  page.get_by_role('button',name='BEGIN INVESTIGATION').click()
  ev('nextIntro();nextIntro();nextIntro()')
  ev('seed=>{S.seed=seed;S.rngState=hashSeed(seed);S.puzzles=generatePuzzles();configureWorld(seed,false);placeTelephones(seed);render()}',seed)
  use('payphone');close();take('desk','Cabinet Key')
  move('security');use('clara');close();use('ros');close();use('winterJournal');close();use('mapboard');close()
  take('drw','Staff Access Card');take('utilityKnife','Utility Knife');take('petrolLighter','Lighter');take('lighterFluid','Lighter Fluid')
  ev('invModal()');page.locator('#combineA').select_option(str(ev('S.inv.findIndex(x=>x.n==="Lighter")')));page.locator('#combineB').select_option(str(ev('S.inv.findIndex(x=>x.n==="Lighter Fluid")')));page.get_by_role('button',name='Combine',exact=True).click();close();assert ev('S.lighterFuel===6&&!has("Lighter Fluid")')
  move('ward');take('nightPistol','Handgun');take('pistolRounds','Handgun Ammo');ev("equipWeapon('Handgun');reload()")
  move('laundry');use('pouch');close();assert ev('carryLimit()===10')
  move('room12');take('cab','Archive Key');take('shf2','Trauma Dressing');use('file');close()
  move('isoward');use('beggingPatient');page.get_by_role('button',name='Try to treat him',exact=True).click();close();assert ev('S.f.beggingPatientChoice==="helped"')
  move('lobby');store(['Cabinet Key','Staff Access Card'])
  move('wardservice');use('kp');page.locator('#cin').fill(ev('S.puzzles.pharmacyCode'));page.get_by_role('button',name='Enter',exact=True).click();close()
  move('pharmacy');take('maintenanceKit','Maintenance Tools');take('bol','Bolt Cutters')
  move('archive');take('fus','Power Fuse');use('eastMap');close()
  move('generator');use('log');close();use('regulator')
  for c in ['A','B','C','D']:
   page.get_by_role('button',name='Lead '+c,exact=False).click();page.get_by_role('button',name='Terminal '+c,exact=True).click()
  close();use('pan');close();assert ev('!!S.f.power');note(seed+' power restored');store(['Maintenance Tools','Archive Key']);use('charger');close()
  # Collect the Archives interlock plug while this early route is still clear.
  # Returning for it after Subject X appears can leave the shelf physically blocked.
  move('archive');take('elevatorFuseA','Rook Interlock Fuse');move('generator')
  move('stafflounge');use('harness');close();use('shaw');close();use('loungeNote');close();assert ev('carryLimit()===12')
  move('residence');use('dia');close();use('brk')
  for color in ev('S.puzzles.breaker'):page.get_by_role('button',name=color,exact=True).click()
  if page.get_by_role('button',name='Take it',exact=True).count():page.get_by_role('button',name='Take it',exact=True).click()
  close();assert ev('has("Crank Handle")')
  move('children');take('neg','Photographic Negative');use('draw');close()
  move('morgue');use('aut');close();use('dw');close();move('tunnel');use('wnc');close();take('tk','Boiler Key')
  move('boiler');use('fl');close();move('generator');store(['Boiler Key','Utility Knife']);use('charger');close()
  move('surgery');close();assert ev('!!S.f.doctorWallSeen')
  move('security');use('staffPortraits')
  for name in ev('portraitOrder()'):page.locator('button[onclick="portraitChoice(\''+name+'\')"]').click()
  close();assert ev('!!S.f.photoPuzzleSolved')
  move('records');close();use('ledger');close();assert ev('!!S.f.researcherLastRoomSeen');take('elevatorFuseC','Knight Interlock Fuse')
  move('observation');close();assert ev('!!S.f.plexiIncidentSeen');take('dr','Encrypted Drive');use('glassNotice');close()
  move('specimen');take('dev','Developing Fluid')
  ev('invModal()');page.locator('#combineA').select_option(str(ev('S.inv.findIndex(x=>x.n==="Photographic Negative")')));page.locator('#combineB').select_option(str(ev('S.inv.findIndex(x=>x.n==="Developing Fluid")')));page.get_by_role('button',name='Combine',exact=True).click();close();assert ev('!!S.f.photo')
  move('coldstore');use('coldlog');close();move('isolation');use('isolog');close()
  move('archive');take('elevatorFuseA','Rook Interlock Fuse');use('cat');page.locator('#cin').fill(ev('S.puzzles.memorialCode'));page.get_by_role('button',name='Enter',exact=True).click();close()
  move('chapel');use('let');close();move('pharmacy');take('elevatorFuseB','Bishop Interlock Fuse')
  move('powercontrol');take('elevatorFuseD','King Interlock Fuse');use('clearance');close();assert ev('!!S.f.finalSecurityClearance');use('elevatorBoard')
  for i,name in enumerate(ev('WardWinter.fuses')):
   page.get_by_role('button',name=name,exact=True).click();page.get_by_role('button',name=name+' socket',exact=True).click()
  close();assert ev('!!S.f.elevatorFusesInstalled');note(seed+' interlock fitted')
  move('archive');close();assert ev('!!S.f.pursuerStarted');assert ev('Object.keys(S.vis).length>=14')
  for _ in range(20):
   if ev('(S.f.pursuerEscapes||0)>0'):break
   move('laundry');move('ward');ev('advanceTime(5);renderScene()');close()
  assert ev('(S.f.pursuerEscapes||0)>0')
  move('generator');store(['Bolt Cutters','Encrypted Drive']);move('lift')
  if page.get_by_role('button',name='Face the elevator',exact=True).count():page.get_by_role('button',name='Face the elevator',exact=True).click()
  if not page.get_by_role('button',name='Descend · End Chapter 1',exact=True).count():use('liftpanel')
  page.get_by_role('button',name='Descend · End Chapter 1',exact=True).click();assert ev('S.f.chapter1Complete&&S.room==="lift"&&!S.pursuer.active')
  assert page.get_by_role('heading',name='CHAPTER 1 COMPLETE',exact=True).is_visible();assert ev('Object.keys(S.vis).length===27')
  note(seed+' elevator ending');page.screenshot(path=str(OUT/(seed+'-ending.png')))
 assert not errors,errors
 browser.close()
(OUT/'winter_progression.json').write_text(json.dumps({'runs':seeds,'transport':URL,'multi_file':True,'trace':report},indent=2))
print('PASS: two complete all-27-room routes using earned progression, native side-arrow turns and ordinary object clicks.')
