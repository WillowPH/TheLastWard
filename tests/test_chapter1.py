"""Real-browser Chapter 1 route and invariant checks. No progression flags granted.
Run: python tests/test_chapter1.py [base_url]. Requires Playwright + Chromium.
"""
from pathlib import Path
import json,sys,collections
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
BASE=next((a for a in sys.argv[1:] if a.startswith('http')), 'http://127.0.0.1:8010')
OUT=ROOT/'tests/results';OUT.mkdir(exist_ok=True)
trace=[]
runs=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
 page=b.new_page(viewport={'width':1600,'height':1000},reduced_motion='reduce');page.set_default_timeout(6000)
 errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.add_init_script("localStorage.setItem('lw_art_mode','offline')")
 page.goto(BASE)
 def ev(code,arg=None):return page.evaluate(code,arg)
 def record(step):
  state=ev('({room:S.room,hp:S.hp,difficulty:S.m,slots:S.slots,inv:S.inv.map(x=>x.n),flags:{power:S.f.power,photo:S.f.photoPuzzleSolved,clearance:S.f.finalSecurityClearance,x:S.f.pursuerStarted,escaped:S.f.pursuerEscapes}})');trace.append({'step':step,**state});print(step,state['room'],state['hp'],flush=True)
 fight_optional=False
 def fight():
  for _ in range(30):
   if not ev('alive(S.room)'):return
   assert ev('S.hp>0'),'died during optional combat'
   if ev('S.hp<35'):
    medicine=ev("Object.keys(HEALS).find(n=>has(n))")
    if medicine:ev('n=>heal(n)',medicine)
   if ev('W[S.eq]&&S.ld[S.eq]>0'):ev('shoot()')
   elif ev('W[S.eq]&&cnt(W[S.eq].ammo)>0'):ev('reload()')
   else:ev('knifeAttack()')
  raise AssertionError('combat did not resolve')
 def dismiss():
  for _ in range(5):
   if not page.locator('#m .md').count():return
   if ev('!!S.f.pursuerEncounter'):ev("escapePursuer('retreat')")
   elif ev('cm&&alive(S.room)'):
    if fight_optional:fight()
    else:ev('flee()')
   else:ev('closeModal()')
  assert not page.locator('#m .md').count(),'modal did not close'
 def current():return ev('S.room')
 def move(target):
  for attempt in range(40):
   dismiss()
   if current()==target:return
   route=ev('''target=>{const q=[[S.room]],seen=new Set([S.room]);while(q.length){const path=q.shift(),r=path.at(-1);if(r===target)return path;for(const [id,d] of Object.entries(D)){const to=d.a===r?d.b:d.b===r?d.a:null;if(!to||seen.has(to))continue;const open=doorOpen(id)||(d.need&&has(d.need));if(!open)continue;seen.add(to);q.push([...path,to])}}return []}''',target)
   assert len(route)>1,(current(),target,ev('S.inv'))
   page.locator('[data-destination="'+route[1]+'"]').click()
  raise AssertionError('Could not navigate to '+target)
 def use(id):
  dismiss()
  if ev('R[S.room].dark&&!lit()'):
   if ev('S.bat<=0'):
    before=current();move('generator');use('charger');dismiss();move(before)
   if ev('!S.lightOn'):ev('toggleLight()')
  fixture=ev("id=>WardScene.sites().find(f=>f.objects.some(o=>o[0]===id))?.id",id)
  assert fixture,('no fixture',current(),id)
  page.locator('[data-fixture="'+fixture+'"]').click()
  button=page.locator('button[onclick="wardFixtureAction(\''+id+'\')"]')
  if button.count():button.click()
 def take(id,item):
  if ev("x=>has(x[1])&&S.ob[x[0]]===\'done\'",[id,item]):return
  use(id)
  if not ev("x=>has(x)",item) and ev("!!S.f.ammoSnakeSeen"):dismiss();use(id)
  assert ev("x=>has(x)",item),('pickup failed',id,item,ev('S.inv'),page.locator('#m').inner_text());dismiss()
 def store_named(names):
  for name in names:
   i=ev("n=>S.inv.findIndex(x=>x.n===n)",name)
   if i>=0:ev('i=>store(i)',i);dismiss()
 def run(seed,optional=False,difficulty='1'):
  global fight_optional
  fight_optional=optional
  page.reload()
  page.locator('#diff').select_option(difficulty)
  ev('newGame()')
  assert ev("!has('Handgun')&&!has('Flashlight')&&!S.lightOn")
  ev('nextIntro();nextIntro();nextIntro()')
  assert ev("has('Flashlight')&&!has('Handgun')&&!S.lightOn")
  ev("seed=>{S.seed=seed;S.rngState=hashSeed(seed);S.puzzles=generatePuzzles();configureWorld(seed,false);placeTelephones(seed);render()}",seed)
  record('opening '+seed)
  use('payphone');dismiss();assert ev('S.f.phoneStep===1')
  take('desk','Cabinet Key');move('security');use('clara');dismiss();take('drw','Staff Access Card');use('ros');dismiss();use('mapboard');dismiss();assert ev('S.mapParts===1')
  ev('toggleLight()');move('ward');take('nightPistol','Handgun');take('pistolRounds','Handgun Ammo');ev("equipWeapon('Handgun');reload()");dismiss()
  move('room12');take('cab','Maintenance Key');take('shf2','Trauma Dressing');use('file');dismiss()
  move('isoward');use('beggingPatient');page.get_by_role('button',name='Try to treat him').click();dismiss();assert ev("S.f.beggingPatientChoice==='helped'")
  # Upgrade capacity before collecting maintenance equipment.
  move('laundry');use('pouch');dismiss();assert ev('carryLimit()===10');use('serviceMap');dismiss()
  move('wardservice');use('kp');page.locator('#cin').fill(ev('S.puzzles.pharmacyCode'));page.get_by_role('button',name='Enter',exact=True).click();dismiss();assert ev('!!S.f.pharm')
  move('pharmacy');take('maintenanceKit','Maintenance Tools');take('bol','Bolt Cutters');use('judith');dismiss()
  move('archive');take('fus','Power Fuse');use('eastMap');dismiss();move('generator');record('generator prerequisites')
  use('log');dismiss();use('pan');dismiss();assert ev('!S.f.power') # must repair first
  use('regulator');dismiss();assert ev('!!S.f.maintenancePrepared');use('pan');dismiss();assert ev('!!S.f.power');record('power restored')
  store_named(['Cabinet Key','Staff Access Card','Maintenance Tools']);use('charger');dismiss()
  if optional:
   # Visit and exercise the optional first-floor branches before awakening Subject X.
   move('residence');use('dia');dismiss();use('brk');sequence=ev('S.puzzles.breaker')
   for color in sequence:page.get_by_role('button',name=color,exact=True).click()
   if page.get_by_role('button',name='Take it',exact=True).count():page.get_by_role('button',name='Take it',exact=True).click()
   dismiss();assert ev("has('Crank Handle')")
   move('stafflounge');use('harness');dismiss();assert ev('carryLimit()===12');use('loungeNote');dismiss();use('shaw');dismiss()
   move('children');take('neg','Photographic Negative');use('draw');dismiss()
   move('pharmacy');take('med','Field Medkit');take('am','Handgun Ammo')
   move('morgue');use('aut');dismiss();use('dw');dismiss();move('tunnel');use('wnc');dismiss();assert ev('!!S.f.drained');take('tk','Tunnel Key')
   move('boiler');take('fur','Stabilizer Part');use('fl');dismiss();move('generator');store_named(['Tunnel Key','Stabilizer Part']);use('charger');dismiss()
   move('records');dismiss();use('ledger');dismiss();move('archive');use('cat');page.locator('#cin').fill(ev('S.puzzles.memorialCode'));page.get_by_role('button',name='Enter',exact=True).click();dismiss();move('chapel');take('rel','Trauma Dressing');use('let');dismiss()
   move('observation');dismiss();take('dr','Encrypted Drive');move('specimen');take('dev','Developing Fluid');use('specdoc');dismiss()
   ev('invModal()');page.locator('#combineA').select_option(str(ev("S.inv.findIndex(x=>x.n==='Photographic Negative')")));page.locator('#combineB').select_option(str(ev("S.inv.findIndex(x=>x.n==='Developing Fluid')")));page.get_by_role('button',name='Combine',exact=True).click();dismiss();assert ev('!!S.f.photo')
   move('coldstore');use('reel');dismiss();use('coldlog');dismiss();move('isolation');use('mirror');dismiss();move('generator');use('charger');dismiss()
   record('optional branches explored')
  move('security');use('staffPortraits');order=ev('portraitOrder()')
  for name in order:page.locator('button[onclick="portraitChoice(\''+name+'\')"]').click()
  dismiss();assert ev('!!S.f.photoPuzzleSolved')
  move('records');dismiss();assert ev('!!S.f.researcherLastRoomSeen');use('finalJournal');dismiss()
  move('observation');dismiss();assert ev('!!S.f.plexiIncidentSeen');take('dr','Encrypted Drive');use('glassNotice');dismiss()
  move('powercontrol');use('clearance');dismiss();assert ev('!!S.f.finalSecurityClearance');record('clearance')
  # Theatre event and later shotgun remain accessible after corporate clearance.
  move('surgery');dismiss();assert ev('!!S.f.doctorWallSeen');take('lateShotgun','Shotgun');take('shotShells','Shotgun Shells')
  move('archive');dismiss();assert ev('!!S.f.pursuerStarted')
  # Keep navigating the actual graph until the pursuer enters; retreat uses a real adjacent door.
  for _ in range(30):
   if ev('(S.f.pursuerEscapes||0)>0'):break
   move('laundry');move('ward');
   if ev('S.pursuer.active'):ev('advanceTime(8);renderScene()')
   dismiss()
  assert ev('(S.f.pursuerEscapes||0)>0'),'No real pursuit escape'
  record('pursuit escaped')
  move('generator');dismiss();store_named(['Maintenance Key','Bolt Cutters','Encrypted Drive']);move('lift')
  # Arrival opens the revelation; close-up actions then offer the explicit descent.
  if page.get_by_role('button',name='Face the elevator').count():page.get_by_role('button',name='Face the elevator').click()
  assert ev('!!S.f.chapter1Revelation')
  if not page.get_by_role('button',name='Descend · End Chapter 1').count():use('liftpanel')
  page.get_by_role('button',name='Descend · End Chapter 1').click()
  assert ev("S.room==='lift'&&S.f.chapter1Complete&&!S.pursuer.active")
  assert page.get_by_role('heading',name='END OF CHAPTER 1').is_visible()
  if optional:assert ev('Object.keys(S.vis).length===27'),ev('Object.keys(S.vis)')
  record('elevator ending');page.screenshot(path=str(OUT/(seed+'-ending.png')))
  assert ev("JSON.parse(localStorage.getItem('lw_ch1_completion_v1')).record.f.chapter1Complete===1")
  runs.append({'seed':seed,'difficulty':difficulty,'all_rooms':optional})
 if '--optional-only' not in sys.argv:
  for seed in ['playtest-11','playtest-15']:run(seed)
 run('playtest-11',optional=True,difficulty='0.7')
 assert not errors,errors
 (OUT/'progression.json').write_text(json.dumps({'runs':runs,'trace':trace},indent=2))
 b.close()
print(f'PASS: {len(runs)} complete Chapter 1 route(s), including an all-27-room Story route, via real inventory, puzzles, gates, pursuit and elevator ending.')
