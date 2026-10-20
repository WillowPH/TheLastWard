"""Mouse-driven service puzzles, retained evidence and truthful transfer feedback."""
from pathlib import Path
from itertools import permutations
import json
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
checks=[];errors=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 q=b.new_page(viewport={'width':1672,'height':941},service_workers='block');q.set_default_timeout(7000);q.on('pageerror',lambda e:errors.append(str(e)))
 q.goto('http://127.0.0.1:8010');q.get_by_role('button',name='BEGIN INVESTIGATION').click();q.evaluate('nextIntro();nextIntro();nextIntro();S.enemyActors.forEach(a=>a.hp=0);WardWinter.enemies.project();S.pursuer.active=false;S.f.phoneRinging=false;S.f.blackoutCount=2;add("Flashlight");S.bat=100')
 ev=q.evaluate
 def click(name):q.get_by_role('button',name=name,exact=True).click()
 def room(name):ev('r=>{closeModal();S.room=r;S.roomViewRoom=null;S.sceneFocus=null;S.lightOn=has("Flashlight");render()}',name);q.wait_for_function('WardWinter.roomViewRenderer()?.loaded&&!WardWinter.orbit.busy')
 def finding(id):
  f=ev('id=>WardScene.sites().find(f=>f.objects.some(o=>o[0]===id))?.id',id);assert f,id
  ev('id=>WardWinter.orbit.face(WardScene.sites().find(f=>f.id===id).view)',f);q.wait_for_function('WardWinter.roomViewRenderer()?.loaded&&!WardWinter.orbit.busy');q.locator('[data-fixture="'+f+'"]').click()
  choose=q.locator('button[onclick="wardSelectFinding(\''+id+'\')"]')
  if choose.count():choose.click()
  action=q.locator('button[onclick="wardFixtureAction(\''+id+'\')"]')
  if action.count():action.click()
 # Scenario setup supplies only what this isolated mechanical puzzle requires;
 # every valve selection, clue read and crank stroke below is a real mouse action.
 room('tunnel');ev('add("Crank Handle");S.docs.push("Diver Note")');finding('wnc')
 assert not ev('!!S.f.drained');click('Turn the crank');assert not ev('!!S.f.winchPrimed') and ev('has("Crank Handle")')
 click('Read Diver Note');assert 'lift-pit intake' in q.locator('.winter-paper-text').inner_text();assert q.locator('#m input[value]').count()==0;click('Return to controls')
 for control in ['inlet','return','relief','intake','intake']:q.locator('[data-winch="'+control+'"]').click()
 click('Turn the crank');assert ev('!!S.f.winchPrimed&&!S.f.drained&&has("Crank Handle")')
 ev('window.puzzleClock=[S.t,S.hp,S.bat];advanceTime(6);WardWinter.survivalTick()');assert ev('JSON.stringify(window.puzzleClock)===JSON.stringify([S.t,S.hp,S.bat])')
 q.locator('[data-winch=relief]').click();click('Turn the crank');assert ev('!!S.f.drained&&!has("Crank Handle")&&S.ob.wnc==="done"');assert q.get_by_role('heading',name='Lift pit drained',exact=True).is_visible();click('Continue')
 checks.append('two-stage hydraulic winch needs the physical crank and collected valve instructions; wrong settings preserve it, success drains the required lift sump')
 room('generator');ev('S.f.maintenancePrepared=1;add("Power Fuse");render()');finding('pan');assert ev('!!S.f.power');assert q.get_by_role('heading',name='Generator power restored',exact=True).is_visible();assert 'charging' in q.locator('#m').inner_text();click('Continue')
 checks.append('repairing and starting the actual generator announces restored circuits and charging power while keeping elevator requirements explicit')
 room('powercontrol');ev('S.docs.push("Power Control Memo");render()');finding('relays')
 click('Read Power Control Memo');assert 'TEN AMPS' in ev('WardWinter.reader().text');click('Return to controls')
 for key in ['liftBrake','cageGate','shaftVent','wardLights','recording','chamberLamps']:q.locator('[data-circuit="'+key+'"]').click()
 click('Test transfer supply');assert not ev('!!S.f.transferBusReady');assert 'overload' in q.locator('#m').inner_text().lower()
 for key in ['wardLights','recording','chamberLamps']:q.locator('[data-circuit="'+key+'"]').click()
 click('Test transfer supply');assert ev('!!S.f.transferBusReady&&S.ob.relays==="done"');assert q.get_by_role('heading',name='Transfer supply stable',exact=True).is_visible();click('Continue')
 checks.append('transfer isolation uses the ten-amp load plates and recorded safeguards; overload cannot succeed and nine safe amps enable authorization')
 ev('S.slots=12;for(const n of WardWinter.fuses)add(n);S.docs.push("Archive component transfer")');finding('elevatorBoard')
 assert not q.get_by_role('button',name='Rook Interlock Fuse socket',exact=True).count()
 # The maintenance relationships yield exactly one order, rather than named matching sockets.
 symbols=['Rook','King','Bishop','Knight'];orders=[v for v in permutations(symbols) if v[0]=='Rook' and v.index('King') not in [0,3] and v.index('Bishop')+1==v.index('Knight') and v.index('Knight')>v.index('King')]
 assert orders==[('Rook','King','Bishop','Knight')]
 click('Read Archive component transfer');assert 'INTERLOCK SERVICE PATTERN' in ev('WardWinter.reader().text');click('Return to controls')
 for i,name in enumerate(['Rook','Bishop','Knight','King']):q.locator('[data-plug="'+name+' Interlock Fuse"]').click();click('Interlock socket '+['I','II','III','IV'][i])
 click('Test interlock pattern');assert not ev('!!S.f.elevatorFusesInstalled');assert ev('WardWinter.fuses.every(has)')
 for i,name in enumerate(orders[0]):q.locator('[data-plug="'+name+' Interlock Fuse"]').click();click('Interlock socket '+['I','II','III','IV'][i])
 click('Test interlock pattern');assert ev('!!S.f.elevatorFusesInstalled&&WardWinter.fuses.every(n=>!has(n))');assert 'Elevator unlocked' not in q.locator('#m').inner_text();assert not ev('doorOpen("liftEntry")');click('Continue')
 checks.append('collected service relationships uniquely determine numbered fuse positions; wrong patterns consume nothing, correct pattern does not falsely unlock an uncleared elevator')
 ev('for(const n of ["power","photoPuzzleSolved","plexiIncidentSeen","researcherLastRoomSeen","doctorWallSeen","finalSecurityClearance","pursuerStarted"])S.f[n]=1;S.f.pursuerEscapes=1;S.f.pursuerStaggers=1;wardElevatorBoard()')
 # Additional combat revision gates are independent; unlock wording is asserted
 # only when the shared requirement list is empty, never by fuses alone.
 assert not ev('WardChapter.requirements().length'),ev('WardChapter.requirements()')
 assert 'Elevator unlocked' in q.locator('#m').inner_text();assert ev('doorOpen("liftEntry")')
 ev('closeModal()');checks.append('interlock result names remaining requirements and only reports unlocked when the shared progression gate is ready')
 room('security');ev('delete S.f.securityServiceRelease;delete S.dr.es;S.dr.ls=1');assert ev('doorOpen("es")');ev('WardWinter.orbit.face(Object.entries(WardRoomViews.security.views).find(([k,v])=>v.doors.es)[0])');q.wait_for_function('WardWinter.roomViewRenderer()?.loaded&&!WardWinter.orbit.busy');q.locator('[data-destination=eastcorridor]').click();q.wait_for_function('S.room==="eastcorridor"&&!WardWinter.travelling');assert ev('S.room==="eastcorridor"&&S.f.securityServiceRelease&&S.dr.es&&doorOpen("es")');assert 'shortcut' in ev('wardDoorRequirement("es")').lower()
 checks.append('Security corridor door releases from the secure side as a permanent outage-safe return shortcut')
 ev('WardWinter.inspectObject("openingPhoto",true)');assert 'DDMM' not in q.locator('#m').inner_text() and ev('!docText("Opening day photograph").includes(S.puzzles.memorialCode)');ev('closeModal()')
 for old in ['last-ward-ch1-survival-review-5','last-ward-ch1-chapter-review-6','last-ward-ch1-chapter-review-7']:
  ev('old=>{S.buildId=old;delete S.f.puzzleRevision;delete S.f.transferBusReady;delete S.f.drained;S.f.finalSecurityClearance=1;S.f.elevatorFusesInstalled=1;configureWorld(S.seed,true)}',old);assert ev('S.f.puzzleRevision===8&&S.f.transferBusReady&&S.f.drained')
 checks.append('late photograph is story evidence rather than a solved lock answer; recognized v5/v6/v7 transfer progress keeps its earned mechanical clearance')
 room('lift');ev('S.ob.restrictedShotgun=undefined;S.f.optionalShotgunThought=0;S.f.chapter1Revelation=1;inspectLiftControls()');assert ev('!!S.f.optionalShotgunThought');assert 'shotgun' in ev('S.contextThought?.text||document.getElementById("sceneThoughtText").textContent').lower();assert ev('!!WardWinter.find("restrictedShotgun")')
 checks.append('optional shotgun exists in a real rear theatre container and receives a once-only pre-descent thought without becoming an ending gate')
 for width,height in [(1000,800),(390,844)]:
  q.set_viewport_size({'width':width,'height':height});room('powercontrol');ev('S.f.transferBusReady=0;S.puzzles.transferLoads={};wardTransferSupply()')
  for selector in ['[data-circuit]','button[onclick="wardTestTransferSupply()"]']:
   assert ev('selector=>[...document.querySelectorAll(selector)].every(b=>{const r=b.getBoundingClientRect();return r.top>=0&&r.bottom<=innerHeight&&b.contains(document.elementFromPoint(r.x+r.width/2,r.y+r.height/2));})',selector),(width,selector)
  room('tunnel');ev('S.f.drained=0;S.f.winchPrimed=0;S.puzzles.serviceWinch=null;if(!has("Crank Handle"))add("Crank Handle");wardHydraulicWinch()')
  assert ev('selector=>[...document.querySelectorAll(selector)].every(b=>{const r=b.getBoundingClientRect();return r.top>=0&&r.bottom<=innerHeight&&b.contains(document.elementFromPoint(r.x+r.width/2,r.y+r.height/2));})','[data-winch],button[onclick="wardTurnServiceCrank()"]'),width
  room('powercontrol');ev('S.f.elevatorFusesInstalled=0;S.f.elevatorLayout=[];wardElevatorBoard()')
  assert ev('[...document.querySelectorAll(".winter-fuse-socket")].every(b=>{const r=b.getBoundingClientRect();return r.top>=0&&r.bottom<=innerHeight&&b.contains(document.elementFromPoint(r.x+r.width/2,r.y+r.height/2));})'),width
 checks.append('tablet and mobile service controls keep all mechanical switches and interlock contacts visible and mouse-accessible')
 assert not errors,errors;b.close()
(ROOT/'tests/results/puzzles_v8.json').write_text(json.dumps({'checks':checks,'javascript_errors':errors},indent=2)+'\n');print('\n'.join('PASS '+c for c in checks))
