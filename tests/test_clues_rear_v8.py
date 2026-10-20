"""Collected evidence, real rear pickups and spent ignition equipment."""
from pathlib import Path
import json, sys
from playwright.sync_api import sync_playwright
from mouse_controls import turn_room
ROOT=Path(__file__).resolve().parents[1]
URL=sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8010'
checks=[];errors=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 q=b.new_page(viewport={'width':1672,'height':941},service_workers='block',reduced_motion='reduce');q.set_default_timeout(8000);q.on('pageerror',lambda e:errors.append(str(e)));q.goto(URL);q.get_by_role('button',name='BEGIN INVESTIGATION',exact=True).click();q.evaluate('nextIntro();nextIntro();nextIntro();S.f.falseEncounterSeen=1;S.f.visualEpisodes=2;S.f.blackoutCount=2;S.pursuer.active=false;add("Flashlight");S.bat=100;S.slots=12;S.enemyActors.forEach(a=>a.hp=0);WardWinter.enemies.project();render()')
 def ev(s,a=None):return q.evaluate(s,a)
 def ready():q.wait_for_function('WardWinter.roomViewRenderer()?.loaded&&!WardWinter.orbit.busy&&!WardWinter.travelling')
 def room(r):
  ev('r=>{closeModal();wardCloseFocus();S.room=r;S.prev=null;S.roomViewRoom=null;S.f.power=1;S.f.powerOut=0;S.f.pursuerEncounter=0;S.pursuer.active=false;S.hp=100;S.f.wet=0;S.f.coldExposure=0;S.enemyActors.forEach(a=>a.hp=0);WardWinter.enemies.project();render();if(WardNavigation.isDark(S.room)&&!lit())toggleLight()}',r);ready()
 def action(i):
  ready();f=ev('id=>WardScene.sites().find(f=>f.objects.some(o=>o[0]===id))',i);assert f,(ev('S.room'),i)
  if ev('S.roomView')!=f.get('view','front'):turn_room(q)
  q.locator('[data-fixture="'+f['id']+'"]').click()
  select=q.locator('button[onclick="wardSelectFinding(\''+i+'\')"]')
  if select.count():select.click()
  q.locator('button[onclick="wardFixtureAction(\''+i+'\')"]').click()
 room('surgery');ev('S.f.photoPuzzleSolved=0;S.inv=S.inv.filter(v=>v.n!=="Shotgun");render()');ready()
 assert not ev('WardScene.sites().some(f=>f.objects.some(o=>o[0]==="restrictedShotgun"))')
 ev('act("restrictedShotgun")');assert not ev('has("Shotgun")')
 ev('S.f.photoPuzzleSolved=1;render()');action('restrictedShotgun');assert ev('has("Shotgun")&&S.ob.restrictedShotgun==="done"&&S.roomView==="rear"');ev('wardCloseFocus();configureWorld(S.seed,true);render()');assert ev('has("Shotgun")&&S.ob.restrictedShotgun==="done"');assert not ev('WardScene.sites().find(f=>f.id==="rearSupply")?.objects.some(o=>o[0]==="restrictedShotgun"&&S.ob[o[0]]!=="done")');checks.append('the optional shotgun is absent before executive authorization, obtainable by a real rear drawer click after it, and cannot be collected again on reconfiguration')
 for r,i,item in [('wardservice','serviceAmmo','Handgun Ammo'),('records','recordsAmmo','Handgun Ammo'),('observation','dr','Encrypted Drive')]:
  room(r);before=ev('n=>cnt(n)',item);expected=ev('id=>WardWinter.find(id)[4].give[0][1]',i);action(i);assert ev('S.roomView')=='rear';assert ev('n=>cnt(n)',item)==before+expected;assert ev('id=>S.ob[id]==="done"',i);ev('wardCloseFocus()')
 checks.append('rear service/Records ammunition and the Observation transfer drive use actual authored targets and preserve finite pickup flags')
 room('security');ev('S.docs=[];S.f.power=0;render()');action('ammoIssueLog');assert ev('S.docs.includes("Security ammunition issue log")');ev('closeModal();evidenceModal()');q.get_by_role('searchbox',name='Find a record').fill('ammunition');assert q.locator('[data-file-objective="preparation"]').count()==1;assert 'Patrol pistol rounds' in q.locator('.file-clue-excerpt').inner_text();q.get_by_role('button',name='Read Security ammunition issue log',exact=True).click();assert ev('WardWinter.reader().title')=='Security ammunition issue log';q.get_by_role('button',name='Return to Files',exact=True).click();assert q.locator('.file-browser').is_visible();ev('closeModal()');checks.append('actually reading the Security issue sheet creates a Preparation clue card with its real excerpt and a working Read/return link')
 room('tunnel');action('dvn');ev('closeModal();evidenceModal()');q.get_by_role('searchbox',name='Find a record').fill('Lift-pit');card=q.locator('[data-file-objective="pit"]');assert card.count()==1;assert 'Diver Note' in card.inner_text();assert not q.locator('[data-file="Power Control Memo"]').count();q.get_by_role('button',name='Read Diver Note',exact=True).click();assert ev('WardWinter.reader().text.includes("PRIME")');q.get_by_role('button',name='Return to Files',exact=True).click();ev('closeModal();S.f.drained=1;evidenceModal();WardWinter.fileSearch("Lift-pit")');assert not q.locator('[data-file-objective="pit"]').count();q.get_by_role('button',name='All records',exact=True).click();q.get_by_role('searchbox',name='Find a record').fill('Diver');assert q.get_by_role('button',name='Read Diver Note',exact=True).count()==1;ev('closeModal()');checks.append('Progression displays only collected relevant evidence, removes a completed goal and retains its clue in All records')
 room('security');action('attendantDiary1');story_title=ev('WardWinter.reader().title');ev('closeModal();evidenceModal()');q.get_by_role('button',name='Story',exact=True).click();q.get_by_role('searchbox',name='Find a record').fill('Attendant');assert q.get_by_role('button',name='Read '+story_title,exact=True).count()==1;ev('closeModal()');checks.append('personal journal evidence is kept in Story rather than disappearing from a progression-only filter')
 # Layout uses a representative collected dossier, not fabricated solutions.
 ev('S.docs=["Maintenance Log","Duty Roster","Resident Diary","Continuity Calibration Note","Diver Note","Power Control Memo","Rourke’s final annotation","Archive component transfer","Heller’s winter maintenance note","Memorial Ledger","Security ammunition issue log","Night Attendant Journal"];S.f.drained=0;S.f.transferBusReady=0;S.f.elevatorFusesInstalled=0;S.f.finalSecurityClearance=0;S.f.chapel=0;S.f.pharm=0;S.f.power=0;delete S.ob.brk;Object.keys(R).forEach(r=>S.vis[r]=1)')
 for w,h in [(1672,941),(1000,800),(390,844)]:
  q.set_viewport_size({'width':w,'height':h});ev('evidenceModal();WardWinter.fileTab("leads")')
  for _ in range(12):
   assert ev('(()=>{const n=document.querySelector("#recordFileList");return n.scrollHeight<=n.clientHeight+1})()'),(w,'Files overflow')
   for button in q.locator('#m button[data-file]').all():
    assert button.is_visible();assert button.evaluate('(b)=>{const r=b.getBoundingClientRect();return r.top>=0&&r.bottom<=innerHeight&&b.contains(document.elementFromPoint(r.x+r.width/2,r.y+r.height/2))}'),(w,button.inner_text())
   if q.get_by_role('button',name='Next Files page',exact=True).is_disabled():break
   q.get_by_role('button',name='Next Files page',exact=True).click()
  ev('closeModal()')
 checks.append('every Progression page keeps its real clue Read buttons visible and clickable without dialog scrolling at desktop, tablet and mobile sizes')
 for difficulty in [1,1.3]:
  ev('m=>{S.m=m;S.f.stoveLit=0;S.f.chapelCandles=0;delete S.ob.chapelCandles;S.inv=[{n:"Flashlight",c:1},{n:"Lighter",c:1},{n:"Lighter Fluid",c:1}];S.lighterFuel=0;render()}',difficulty);ev('wardCombineLighter()');assert ev('S.lighterFuel===6&&has("Lighter")&&!has("Lighter Fluid")')
  room('laundry');action('dryingStove');assert ev('S.f.stoveLit&&has("Lighter")&&!S.f.chapelCandles');ev('closeModal();wardCloseFocus()');room('chapel');action('chapelCandles');assert ev('S.f.stoveLit&&S.f.chapelCandles')
  assert ev('has("Lighter")')==(difficulty>1),(difficulty,ev('S.inv'))
  if difficulty>1:assert ev('WardWinter.inventoryDiscard.policy("Lighter").spent')
  ev('closeModal();wardCloseFocus()')
 checks.append('actual filled-lighter use protects it after the first ignition, auto-discards it only after both on Normal, and leaves spent manual discard on Nightmare')
 assert not errors,errors;b.close()
(ROOT/'tests/results/clues_rear_v8.json').write_text(json.dumps({'checks':checks,'javascript_errors':errors},indent=2)+'\n');print('\n'.join('PASS '+v for v in checks))
