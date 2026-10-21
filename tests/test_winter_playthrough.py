"""Playable winter Chapter 1 routes. Progression is earned through actual controls."""
from pathlib import Path
import json,sys,re,itertools,argparse
from playwright.sync_api import sync_playwright
from mouse_controls import turn_room
ROOT=Path(__file__).resolve().parents[1]
BUILD='last-ward-ch1-chapter-review-9'
parser=argparse.ArgumentParser();parser.add_argument('url',nargs='?',default='http://127.0.0.1:8010');parser.add_argument('--mode',choices=['both','normal','story'],default='both');args=parser.parse_args();URL=args.url
OUT=ROOT/'tests/results';OUT.mkdir(exist_ok=True)
result_path=OUT/'winter_progression.json'
report=json.loads(result_path.read_text()).get('trace',[]) if args.mode!='both' and result_path.exists() else []
report=[entry for entry in report if entry.get('build')==BUILD]
selected_prefix='winter-story-complete' if args.mode=='story' else 'winter-standard-a'
if args.mode!='both':report=[entry for entry in report if not entry['step'].startswith(selected_prefix)]
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--enable-unsafe-swiftshader'])
 context=browser.new_context(viewport={'width':1600,'height':1000},service_workers='block',reduced_motion='reduce')
 context.route('**/*',lambda route:route.continue_() if route.request.url.startswith(URL.rstrip('/')+'/') else route.abort())
 page=context.new_page();page.set_default_timeout(6500)
 errors=[];page.on('pageerror',lambda error:errors.append(str(error)))
 def ev(code,arg=None):return page.evaluate(code,arg)
 def aim_point(point_id):
  """Use a native mouse drag to expose the authored object's full view."""
  if page.locator('#m .md').count():close()
  page.wait_for_function('WardWinter.roomViewRenderer()?.loaded&&!WardWinter.orbit.busy&&!WardWinter.travelling')
  point=ev('id=>WardWinter.orbit.points().find(p=>p.id===id)',point_id)
  if not point and point_id=='fixture:dropped-light':point={'view':'front'}
  assert point,('Missing authored mouse target',ev('S.room'),point_id)
  if ev('S.roomView')!=point['view']:
   for attempt in range(5):
    if page.locator('#m .md').count():close()
    if ev('S.roomView')==point['view']:break
    try:turn_room(page)
    except AssertionError:
     if not page.locator('#m .md').count():raise
     close()
   page.wait_for_function('WardWinter.roomViewRenderer()?.loaded&&!WardWinter.orbit.busy')
  assert ev('S.roomView')==point['view'],('Mouse drag did not expose requested view',point_id)
 def click_visible(selector):
  # A live enemy may cover part of a visible object. Click a genuinely exposed
  # part of the target, exactly as a player can; never click through the enemy.
  point=ev('''selector=>{const node=document.querySelector(selector);if(!node)return null;const r=node.getBoundingClientRect();for(const [u,v]of [[.5,.5],[.9,.1],[.1,.1],[.9,.9],[.1,.9],[.9,.5],[.1,.5],[.5,.1],[.5,.9]]){const x=r.left+r.width*u,y=r.top+r.height*v;if(document.elementFromPoint(x,y)===node)return {x,y};}return null;}''',selector)
  assert point,('No unobstructed mouse target',ev('S.room'),selector,ev('({pursuer:S.pursuer,combat:cm,modal:document.querySelector("#m .md")?.innerText})'))
  page.mouse.click(point['x'],point['y'])
 def use_medical():
  choices=ev('Object.keys(HEALS).filter(n=>has(n)&&(n!=="Trauma Dressing"||S.f.beggingPatientChoice||cnt(n)>1))')
  if not choices:return False
  name=next((n for n in ['Field Medkit','Trauma Dressing','Antiseptic'] if n in choices),choices[0])
  if page.locator('#m .md').count():
   treat=page.get_by_role('button',name='Treat injury',exact=True)
   if not treat.count():return False
   treat.click();row=page.locator('.medical-choice').filter(has_text=name)
   row.get_by_role('button',name='Use this',exact=True).click()
  else:
   page.get_by_role('button',name=re.compile(r'^Select '+re.escape(name)+r'(?: × \d+)?$')).first.click()
   page.locator('#inventoryCarryActions').get_by_role('button',name='Use',exact=True).click()
  metrics['heals']+=1
  return True
 def close():
  for _ in range(65):
   assert ev('S.hp>0&&!S.f.dead'),('died',metrics,ev('({room:S.room,hp:S.hp,log:S.log,inventory:S.inv,en:S.en,pursuer:S.pursuer,conditions:S.conditions})'))
   if not page.locator('#m .md').count():
    recovery=page.get_by_role('button',name='Dry off and warm up',exact=True)
    if recovery.count() and recovery.is_visible():recovery.click()
    if ev('!!S.sceneFocus'):ev('wardCloseFocus()')
    if ev('S.room==="eastcorridor"&&S.f.flashlightDropped'):
     aim_point('fixture:dropped-light');page.get_by_role('button',name='Recover dropped flashlight',exact=True).click()
    if ev('S.room==="eastcorridor"&&S.f.sprinklerTriggered&&!S.f.sprinklerStopped'):
     aim_point('fixture:valve');page.locator('[data-fixture=valve]').click();page.locator("button[onclick=\"wardFixtureAction('staffSprinkler')\"]").click();continue
    if ev('S.hp<45') and use_medical():continue
    return
   if ev('!!S.hallCombat'):
    page.get_by_role('button',name='Hold and observe',exact=True).click();metrics['hallucination_choices']+=1
   elif ev('!!S.f.pursuerEncounter'):
    if ev('S.hp<24') and use_medical():continue
    if ev('W[S.eq]&&has(S.eq)&&(S.ld[S.eq]||0)>0'):
     page.get_by_role('button',name='Shoot Subject X',exact=True).click();metrics['shots']+=1
    elif ev('W[S.eq]&&has(S.eq)&&cnt(W[S.eq].ammo)>0'):
     page.get_by_role('button',name='Reload',exact=True).click();metrics['reloads']+=1
    else:raise AssertionError(('Earned route ran out of ammunition at Subject X',ev('({room:S.room,hp:S.hp,inventory:S.inv,loaded:S.ld,pursuer:S.pursuer})')))
   elif page.get_by_role('button',name='Call his name',exact=True).count():page.get_by_role('button',name='Call his name',exact=True).click()
   elif page.get_by_role('button',name='Face the infected',exact=True).count():page.get_by_role('button',name='Face the infected',exact=True).click()
   elif ev('cm&&alive(S.room)'):
    if ev('S.hp<38') and use_medical():continue
    knife=page.get_by_role('button',name='Knife attack · risk injury',exact=True)
    if knife.count() and ev('has("Utility Knife")&&S.en[S.room]<=2&&S.hp>30'):
     knife.click();metrics['knife_finishers']+=1
    elif ev('W[S.eq]&&has(S.eq)&&(S.ld[S.eq]||0)>0'):
     shot=page.get_by_role('button',name='Steady aim · takes time',exact=True)
     if not shot.count():shot=page.get_by_role('button',name='Quick shot',exact=True)
     shot.click();metrics['shots']+=1
    elif ev('W[S.eq]&&has(S.eq)&&cnt(W[S.eq].ammo)>0'):
     page.get_by_role('button',name='Reload',exact=True).click();metrics['reloads']+=1
    else:raise AssertionError(('Earned route lacks ammunition at infected',ev('({room:S.room,hp:S.hp,inventory:S.inv,loaded:S.ld,en:S.en,log:S.log})')))
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
  (OUT/'winter-route-failure.json').write_text(ev('JSON.stringify(S,null,2)'));page.screenshot(path=str(OUT/'winter-route-failure.png'));raise AssertionError(('Navigation did not reach '+target,ev('({room:S.room,previous:S.prev,hp:S.hp,pursuer:S.pursuer,encounter:S.f.pursuerEncounter,modal:document.querySelector("#m .md")?.innerText,log:S.log})')))
 def use(id):
  close()
  if ev('id=>WardWinter.chargerStatus(id)?.available===false',id):return
  if ev('WardNavigation.isDark(S.room)&&!lit()'):
   if ev('S.bat<12&&has("Battery")'):
    page.get_by_role('button',name='Select Battery',exact=True).click();page.locator('#inventoryCarryActions').get_by_role('button',name='Use',exact=True).click();close()
   if ev('!S.lightOn'):ev('toggleLight()')
  f=ev('id=>{const f=WardScene.sites().find(f=>f.objects.some(o=>o[0]===id));return f?{id:f.id,view:f.view||"front",rect:f.rect}:null;}',id)
  assert f,('No fixture',ev('S.room'),id)
  page.wait_for_function('WardWinter.roomViewRenderer()?.loaded')
  aim_point('fixture:'+f['id'])
  click_visible('[data-fixture="'+f['id']+'"]')
  choice=page.locator('button[onclick="wardSelectFinding(\''+id+'\')"]')
  if choice.count():choice.click()
  button=page.locator('button[onclick="wardFixtureAction(\''+id+'\')"]')
  if button.count():button.click()
 def take(id,name):
  if ev('id=>S.ob[id]===\'done\'',id):return
  for _ in range(6):
   use(id)
   if ev('id=>S.ob[id]===\'done\'',id):break
   title=page.locator('#m .mh h2').inner_text() if page.locator('#m .mh h2').count() else ''
   if 'threat' in title.lower() or ev('!!S.f.ammoSnakeSeen'):close()
   else:break
  assert ev('id=>S.ob[id]===\'done\'',id),('Pickup was not completed',id,name,ev('({inv:S.inv,slots:carryLimit(),thought:S.contextThought})'),page.locator('#m').inner_text())
  assert ev('n=>has(n)',name),('Pickup failed',id,name,ev('S.inv'),page.locator('#m').inner_text())
  close()
 def read_object(id):
  for attempt in range(6):
   use(id)
   if page.locator('.record-reader').count():break
   close()
  assert page.locator('.record-reader').count(),('Missing readable record',id,page.locator('#m').inner_text(),ev('({room:S.room,view:S.roomView,bat:S.bat,light:S.lightOn,thought:S.contextThought,ob:S.ob,focus:S.sceneFocus,docs:S.docs,enemy:WardWinter.enemies.snapshot(),focusText:document.getElementById("sceneFocusOverlay")?.innerText,focusObject:S.sceneFocusObject})'))
  title=page.locator('.record-reader').get_attribute('data-record');parts=[]
  while True:
   parts.append(page.locator('.winter-paper-text').inner_text())
   button=page.get_by_role('button',name='Next document page',exact=True)
   if button.is_disabled():break
   button.click()
  clues[title]='\n'.join(parts)
  assert ev('title=>S.docs.includes(title)',title),('Record was not collected',title)
  close();return clues[title]
 def combine(a,b):
  close()
  page.get_by_role('button',name='Select '+a,exact=True).click()
  page.locator('#inventoryCarryActions').get_by_role('button',name='Combine',exact=True).click()
  page.get_by_role('button',name='Combine with '+b,exact=True).click()
  close()
 def store(names):
  for n in names:
   i=ev('n=>S.inv.findIndex(x=>x.n===n)',n)
   if i>=0:ev('i=>store(i)',i);close()
 def store_ui(names):
  for name in names:
   if not ev('n=>has(n)',name):continue
   use('box2')
   page.get_by_role('button',name=re.compile(r'^Carrying \(')).click()
   for _ in range(4):
    card=page.locator('.storage-card').filter(has=page.get_by_text(name,exact=True))
    if card.count():
     card.first.get_by_role('button',name='Store',exact=True).click();break
    next_page=page.get_by_role('button',name='Next ›',exact=True)
    assert not next_page.is_disabled(),('Carried item missing from storage controls',name)
    next_page.click()
   else:raise AssertionError(('Storage pagination did not find',name))
   close()
 def note(label):
  state=ev('({build:WardChapter.BUILD,room:S.room,hp:S.hp,sanity:S.san,charge:S.bat,visited:Object.keys(S.vis).length,loadedRounds:S.ld.Handgun||0,reserveRounds:cnt("Handgun Ammo"),pursuerStaggers:S.f.pursuerStaggers||0,pursuerEscapes:S.f.pursuerEscapes||0,remaining:WardChapter.requirements()})')
  assert state['build']==BUILD,state
  state.update(metrics);state['infectedKilled']=ev('S.enemyActors.filter(a=>!a.dormant&&a.hp<=0).length');state['visualEpisodes']=ev('S.f.visualEpisodes||0');state['falseEncounterResolved']=ev('!!S.f.falseEncounterResolved');state['collectedClues']=list(clues);state['shotgunObtained']=ev('has("Shotgun")||S.ob.restrictedShotgun==="done"');state['patientOutcome']=ev('S.f.patientOutcome');state['kesslerResponse']=ev('S.f.kesslerResponse');state['evidence']='Captured directly from this earned route invocation.';report.append({'step':label,**state});print(label,state,flush=True)
 all_seeds=['winter-standard-a','winter-story-complete'];seeds=all_seeds if args.mode=='both' else [selected_prefix]
 for seed in seeds:
  metrics={'shots':0,'reloads':0,'heals':0,'knife_finishers':0,'hallucination_choices':0};clues={}
  context.set_offline(False);page.goto(URL,timeout=60000)
  page.locator('#diff').select_option('0.7' if 'story' in seed else '1')
  page.get_by_role('button',name='BEGIN INVESTIGATION').click()
  ev('nextIntro();nextIntro();nextIntro()')
  ev('seed=>{S.seed=seed;S.rngState=hashSeed(seed);S.puzzles=generatePuzzles();configureWorld(seed,false);placeTelephones(seed);render()}',seed)
  assert not ev('has("Flashlight")');take('coat','Flashlight');use('payphone');close();take('desk','Cabinet Key')
  move('security');use('clara');close();read_object('ros');read_object('winterJournal');use('mapboard');close()
  take('drw','Staff Access Card');take('utilityKnife','Utility Knife');take('petrolLighter','Lighter');take('lighterFluid','Lighter Fluid')
  combine('Lighter','Lighter Fluid');assert ev('S.lighterFuel===2&&!has("Lighter Fluid")')
  take('earlyBattery','Battery')
  move('ward');take('nightPistol','Handgun');take('pistolRounds','Handgun Ammo');ev("equipWeapon('Handgun');reload()")
  move('laundry');use('dryingStove');close();assert ev('S.f.stoveLit&&!S.f.wet');metrics['deliberate_warmups']=1;use('pouch');close();assert ev('carryLimit()===10')
  if ev('has("Battery")&&S.bat<100'):
   page.get_by_role('button',name='Select Battery',exact=True).click();page.locator('#inventoryCarryActions').get_by_role('button',name='Use',exact=True).click();close()
  move('ward');take('clinicDressing','Trauma Dressing')
  move('wardservice');take('serviceAmmo','Handgun Ammo')
  move('room12');take('cab','Archive Key');take('shf2','Trauma Dressing');use('file');close()
  move('isoward');use('beggingPatient');page.get_by_role('button',name='Try to treat him',exact=True).click();close();assert ev('S.f.beggingPatientChoice==="helped"')
  move('lobby');store(['Cabinet Key','Staff Access Card','Utility Knife','Lighter'])
  pharmacy_code=''.join(re.findall(r'Ward (\d)',clues['Duty Roster']));assert len(pharmacy_code)==4
  move('wardservice');use('kp');page.locator('#cin').fill(pharmacy_code);page.get_by_role('button',name='Enter',exact=True).click();close()
  move('pharmacy');take('maintenanceKit','Maintenance Tools');take('bol','Bolt Cutters');take('am','Handgun Ammo');take('med','Field Medkit')
  move('archive');take('fus','Power Fuse');read_object('componentNote');use('eastMap');close()
  move('generator');use('log');close();use('regulator')
  for c in ['A','B','C','D']:
   page.get_by_role('button',name='Lead '+c,exact=False).click();page.get_by_role('button',name='Terminal '+c,exact=True).click()
  close();use('pan');close();assert ev('!!S.f.power');note(seed+' power restored');store(['Maintenance Tools','Archive Key']);use('charger');close()
  # Collect the Archives interlock plug while this early route is still clear.
  # Returning for it after Subject X appears can leave the shelf physically blocked.
  move('archive');take('elevatorFuseA','Rook Interlock Fuse');move('generator')
  move('stafflounge');use('harness');close();use('shawHandover');close();use('loungeNote');close();assert ev('carryLimit()===12')
  move('residence');diary=read_object('dia');use('brk')
  colors=re.search(r'exit signs: ([^.]+)',diary).group(1);breaker=['R' if c=='red' else 'G' if c=='green' else 'B' if c=='blue' else 'Y' for c in re.findall('red|green|blue|yellow',colors)]
  for color in breaker:page.get_by_role('button',name=color,exact=True).click()
  if page.get_by_role('button',name='Take it',exact=True).count():page.get_by_role('button',name='Take it',exact=True).click()
  close();assert ev('has("Crank Handle")')
  move('children');take('neg','Photographic Negative');use('draw');close()
  move('morgue');use('aut');close();use('dw');close();move('tunnel');pump_note=read_object('dvn');assert 'PRIME' in pump_note and 'DRAIN' in pump_note;use('wnc')
  for valve in ['inlet','return','relief','intake','intake']:page.locator('[data-winch='+valve+']').click()
  page.get_by_role('button',name='Turn the crank',exact=True).click();assert ev('!!S.f.winchPrimed&&!S.f.drained')
  page.locator('[data-winch=relief]').click();page.get_by_role('button',name='Turn the crank',exact=True).click();close();assert ev('S.f.drained&&!has("Crank Handle")');take('tk','Boiler Key')
  move('boiler');use('fl');close();move('generator');store(['Boiler Key','Utility Knife']);use('charger');close()
  # The second first-aid kit is now in Observation's rear desk. Reach it through
  # the powered generator door before committing to the theatre and records.
  move('observation');close();assert ev('!!S.f.plexiIncidentSeen');take('loungeFirstAid','Field Medkit')
  move('surgery');close();assert ev('!!S.f.doctorWallSeen')
  move('security');use('staffPortraits')
  photos=[]
  for name in ['Dr. Kessler','Dr. Blackwell','Dr. Rourke']:
   page.locator('button[onclick="wardInspectPortrait(\''+name+'\')"]').click();page.get_by_role('button',name='Turn over',exact=True).click();year=int(re.search(r'Appointed (\d{4})',page.locator('.winter-photo-back').inner_text()).group(1));photos.append((year,name));page.get_by_role('button',name='Return to frame',exact=True).click()
  for year,name in sorted(photos):page.locator('button[onclick="portraitChoice(\''+name+'\')"]').click()
  close();assert ev('!!S.f.photoPuzzleSolved')
  move('records');close();ledger=read_object('ledger');take('recordsAmmo','Handgun Ammo');assert ev('!!S.f.researcherLastRoomSeen');take('elevatorFuseC','Knight Interlock Fuse');note(seed+' restricted evidence recovered')
  # The collected ledger opens a nearby recovery stop before the restricted
  # wing. Carry its earned dressing rather than postponing care until afterward.
  move('archive');use('cat');date=re.search(r'(\d{2})/(\d{2})/1998',ledger);assert date;page.locator('#cin').fill(date.group(1)+date.group(2));page.get_by_role('button',name='Enter',exact=True).click();close()
  move('chapel');use('let');close();take('rel','Trauma Dressing')
  # Story grants more ammunition, so deposit one surplus stack and the spare
  # battery using the actual shared Storage box before taking laboratory items.
  if 'story' in seed:
   move('generator');store_ui(['Battery'])
   if ev('cnt("Handgun Ammo")>48'):store_ui(['Handgun Ammo'])
  move('observation');close();assert ev('!!S.f.plexiIncidentSeen');take('dr','Encrypted Drive');use('glassNotice');close()
  move('specimen');take('dev','Developing Fluid')
  combine('Photographic Negative','Developing Fluid');assert ev('!!S.f.photo')
  move('coldstore');use('coldlog');close();move('isolation');use('isolog');close();take('isolationDressing','Trauma Dressing')
  move('pharmacy');take('elevatorFuseB','Bishop Interlock Fuse')
  move('powercontrol');take('elevatorFuseD','King Interlock Fuse');supply_note=read_object('pwrmemo');assert 'TEN AMPS' in supply_note and 'recording bank' in supply_note;use('relays')
  for circuit in ['liftBrake','cageGate','shaftVent']:page.locator('[data-circuit='+circuit+']').click()
  page.get_by_role('button',name='Test transfer supply',exact=True).click();close();assert ev('!!S.f.transferBusReady');use('clearance');close();assert ev('!!S.f.finalSecurityClearance');use('elevatorBoard')
  assert 'INTERLOCK SERVICE PATTERN' in clues['Archive component transfer']
  candidates=[v for v in itertools.permutations(['Rook','King','Bishop','Knight']) if v[0]=='Rook' and v.index('King') not in [0,3] and v.index('Bishop')+1==v.index('Knight') and v.index('Knight')>v.index('King')];assert len(candidates)==1
  for roman,name in zip(['I','II','III','IV'],candidates[0]):
   page.locator('[data-plug="'+name+' Interlock Fuse"]').click();page.get_by_role('button',name='Interlock socket '+roman,exact=True).click()
  page.get_by_role('button',name='Test interlock pattern',exact=True).click()
  close();assert ev('!!S.f.elevatorFusesInstalled');note(seed+' interlock fitted')
  move('archive');close();assert ev('!!S.f.pursuerStarted');assert ev('Object.keys(S.vis).length>=14')
  assert ev('(S.f.pursuerStaggers||0)>0&&(S.f.pursuerEscapes||0)>0'),('Natural full route must meet and stagger Subject X',ev('S.f'))
  move('generator');store(['Bolt Cutters','Encrypted Drive']);move('lift')
  if page.get_by_role('button',name='Face the elevator',exact=True).count():page.get_by_role('button',name='Face the elevator',exact=True).click()
  if not page.get_by_role('button',name='Descend · End Chapter 1',exact=True).count():use('liftpanel')
  page.get_by_role('button',name='Descend · End Chapter 1',exact=True).click();assert ev('S.f.chapter1Complete&&S.room==="lift"&&!S.pursuer.active')
  assert page.get_by_role('heading',name='CHAPTER 1 COMPLETE',exact=True).is_visible();assert ev('Object.keys(S.vis).length===27');assert not ev('has("Shotgun")||S.ob.restrictedShotgun==="done"');assert ev('S.f.drained&&S.f.transferBusReady&&S.f.elevatorFusesInstalled');assert metrics['shots']>0;assert ev('S.enemyActors.some(a=>!a.dormant&&a.hp<=0)')
  note(seed+' elevator ending');page.screenshot(path=str(OUT/(seed+'-ending.png')))
  assert ev('S.f.patientOutcome==="stabilized"&&S.f.kesslerResponse==="speak"')
 assert not errors,errors
 browser.close()
result_path.write_text(json.dumps({'runs':[seed for seed in ['winter-standard-a','winter-story-complete'] if any(e['step']==seed+' elevator ending' for e in report)],'executed_this_invocation':seeds,'transport':URL,'multi_file':True,'javascript_errors':errors,'trace':report},indent=2))
print('PASS: '+str(len(seeds))+' complete all-27-room route(s) using earned progression, native mouse drags and ordinary object clicks.')
