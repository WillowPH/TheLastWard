"""Finite encounter budgets, costly melee and an earned final pursuit opening."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];checks=[];errors=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 q=b.new_page(viewport={'width':1600,'height':1000},service_workers='block',reduced_motion='reduce');q.set_default_timeout(6000);q.on('pageerror',lambda e:errors.append(str(e)));ev=q.evaluate
 def fresh(mode='1'):
  q.goto('http://127.0.0.1:8010');q.locator('#diff').select_option(mode);q.get_by_role('button',name='BEGIN INVESTIGATION',exact=True).click();ev('nextIntro();nextIntro();nextIntro();S.f.phoneRinging=false;S.f.blackoutCount=2;S.pursuer.active=false');q.wait_for_function('WardWinter.roomViewRenderer()?.loaded')
 totals=[]
 for mode,count in [('0.7',5),('1',9),('1.3',11)]:
  fresh(mode);assert ev('S.enemyActors.filter(a=>!a.dormant).length')==count
  assert not ev('S.enemyActors.some(a=>!a.dormant&&["lobby","security","ward","generator","chapel"].includes(a.home))')
  before=ev('WardWinter.balance8.ammoBudget()');ev('configureWorld(S.seed,true);configureWorld(S.seed,true)');assert ev('WardWinter.balance8.ammoBudget()')==before
  assert ev('S.enemyActors.filter(a=>!a.dormant).length')==count;totals.append(before)
 assert totals[0]>totals[1]>totals[2],totals;checks.append('Story/Normal/Nightmare have5/9/11finite authored infected, safe first firearm access and nonstacking finite ammunition budgets')
 fresh();ev('S.enemyActors.forEach(a=>a.hp=0);let a=S.enemyActors[0];Object.assign(a,{room:"wardnorth",home:"wardnorth",hp:13,maxHp:13,down:false});S.room="wardnorth";S.prev="ward";S.roomViewRoom=null;S.f.power=1;S.hp=100;add("Utility Knife");window.savedRng=rnd;rnd=()=>.5;WardWinter.enemies.project();render();knifeAttack();knifeAttack()')
 assert ev('WardWinter.enemies.actorAt().hp')==7
 assert ev('S.hp')<=88
 assert ev('S.f.knifeCuts')==2
 checks.append('two actual knife attacks cannot kill a fresh infected and permit its close-range counterattacks')
 ev('rnd=window.savedRng;const a=WardWinter.enemies.actorAt();S.hp=100;wardStruggle()')
 assert ev('S.hp')==86 and ev('S.enemyActors[0].down&&S.enemyActors[0].hp===7')
 ev('S.room="ward";WardWinter.enemies.project();S.room="wardnorth";WardWinter.enemies.project()')
 assert ev('!S.enemyActors[0].down&&S.enemyActors[0].hp===7')
 checks.append('struggling costs14HP against a fresh Normal infected, knocks it down without killing and preserves its return')
 fresh();ev('S.enemyActors.forEach(a=>a.hp=0);let a=S.enemyActors[0];Object.assign(a,{room:"wardnorth",hp:12,maxHp:12,down:false});S.room="wardnorth";S.roomViewRoom=null;S.f.power=1;S.hp=100;add("Handgun");add("Handgun Ammo",12);S.eq="Handgun";S.ld.Handgun=6;window.savedRng=rnd;rnd=()=>.5;WardWinter.enemies.project();render();combat()')
 for _ in range(3):
  q.get_by_role('button',name='Steady aim · takes time',exact=True).click()
 assert ev('S.enemyActors[0].hp')==0 and ev('S.ld.Handgun')==3 and ev('S.hp')==100
 ev('rnd=window.savedRng;const number=S.enemyActors.length;noise();advanceTime(30);render();window.afterNoiseCount=S.enemyActors.length')
 assert ev('window.afterNoiseCount')==10
 checks.append('three deliberate handgun shots spend earned round capacity and interrupt an approach; gunfire and elapsed time never spawn extra infected')
 for difficulty,handgun_hits,shell_hits in [('0.7',2,1),('1',3,2),('1.3',4,2)]:
  for weapon,hits in [('Handgun',handgun_hits),('Shotgun',shell_hits)]:
   fresh(difficulty)
   ev('weapon=>{S.enemyActors.forEach(a=>a.hp=0);WardWinter.enemies.project();S.room="eastcorridor";S.roomViewRoom=null;S.f.power=1;S.f.sprinklerTriggered=1;S.f.sprinklerStopped=1;S.f.wet=0;S.f.coldExposure=0;S.hp=100;add(weapon);S.eq=weapon;S.ld[weapon]=W[weapon].mag;S.pursuer={active:true,room:S.room,cooldown:0,noise:0,posture:0};S.f.pursuerStarted=1;S.f.pursuerEncounter=0;$("m").innerHTML="";render();pursuerEncounter();}',weapon)
   initial=ev('S.ld[S.eq]')
   for shot in range(hits):
    q.get_by_role('button',name='Shoot Subject X',exact=True).click()
    assert ev('WardWinter.pursuerDown()')==(shot==hits-1),(difficulty,weapon,shot)
   assert ev('S.ld[S.eq]')==initial-hits
   expected_cost=round((3 if float(difficulty)<1 else 4)*float(difficulty))*(hits-1)
   assert abs(ev('S.hp')-(100-expected_cost))<.01,(difficulty,weapon,ev('S.hp'))
 checks.append('real Subject X shots require2/3/4 handgun hits or1/2/2 heavy shells onStory/Normal/Nightmare, with2/4/5HP nonstagger counters')
 fresh();ev('S.enemyActors[0].hp=0;S.vis.wardnorth=1;S.enemyActors=S.enemyActors.slice(0,3);S.balanceVersion=7;window.oldEnemyId=S.enemyActors[0].id;WardWinter.enemies.project();configureWorld(S.seed,true)')
 assert ev('S.enemyActors.find(a=>a.id===window.oldEnemyId).hp')==0
 assert ev('S.enemyActors.filter(a=>a.home==="wardnorth").length')==1
 assert ev('S.enemyActors.filter(a=>a.id!=="window-breach").length')<=9
 checks.append('legacy continued saves retain dead IDs and never repopulate cleared or visited homes')
 fresh();ev('S.enemyActors.forEach(a=>a.hp=0);WardWinter.enemies.project();S.f.power=1;S.f.photoPuzzleSolved=1;S.f.plexiIncidentSeen=1;S.f.researcherLastRoomSeen=1;S.f.doctorWallSeen=1;S.f.finalSecurityClearance=1;S.f.elevatorFusesInstalled=1;S.f.drained=1;S.f.transferBusReady=1;S.f.pursuerStarted=1;S.f.pursuerEscapes=2;S.f.pursuerStaggers=0;S.room="generator";S.prev="archive";S.roomViewRoom=null;S.pursuer.active=true;S.pursuer.room="records";S.hp=100;add("Handgun");S.eq="Handgun";S.ld.Handgun=6;$("m").innerHTML="";render()')
 q.wait_for_function('S.f.finalPursuitActive&&S.f.pursuerEncounter')
 assert ev('S.room')=='generator';assert ev('WardChapter.requirements().includes("create a safe opening past Subject X")')
 assert not ev('SAFE_FROM_PURSUER.has("generator")')
 
 for _ in range(3):q.get_by_role('button',name='Shoot Subject X',exact=True).click()
 assert ev('WardWinter.balance8.strategy()&&WardWinter.pursuerDown()')
 ev('go("lift",true)')
 assert ev('S.room')=='lift' and ev('S.ld.Handgun')==3
 assert ev('!S.f.finalPursuitActive&&SAFE_FROM_PURSUER.has("generator")')
 checks.append('plain retreat counters cannot clear the final gate: Subject X breaches the shelter and three real handgun shots create the optional-shotgun opening')

 ev('S.room="generator";S.prev="archive";S.roomViewRoom=null;S.f.pursuerEscapes=0;S.f.pursuerStaggers=0;S.f.finalPursuitActive=0;S.f.pursuerEncounter=0;S.pursuer.room="records";delete S.pursuer.staggerUntil;delete S.pursuer.staggerDeadline;S.ld.Handgun=6;$("m").innerHTML="";render()')
 q.wait_for_function('S.f.finalPursuitActive&&S.f.pursuerEncounter')
 
 for _ in range(3):q.get_by_role('button',name='Shoot Subject X',exact=True).click()
 assert ev('!WardChapter.requirements().includes("escape Subject X")')
 ev('go("lift",true)');assert ev('S.room')=='lift' and ev('S.f.pursuerEscapes')==1
 checks.append('a first-ever final knockdown can enter the lift and records exactly one real escape, avoiding a circular escape gate')

 assert not errors,errors;b.close()
(ROOT/'tests/results/balance_v8.json').write_text(json.dumps({'checks':checks,'ammo_totals':totals,'javascript_errors':errors},indent=2)+'\n');print('\n'.join('PASS '+v for v in checks))
