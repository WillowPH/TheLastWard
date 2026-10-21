"""Records freeze real encounter deadlines; a genuine New Game retires old checkpoints."""
from pathlib import Path
import json,sys
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
URL=sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8010'
checks=[];errors=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 q=b.new_page(viewport={'width':1672,'height':941},service_workers='block');q.set_default_timeout(6500);q.on('pageerror',lambda e:errors.append(str(e)));ev=q.evaluate
 def fresh():
  q.goto(URL);q.get_by_role('button',name='BEGIN INVESTIGATION',exact=True).click();ev('nextIntro();nextIntro();nextIntro()');q.wait_for_function('WardWinter.roomViewRenderer()?.loaded');ev('S.enemyActors.forEach(a=>a.hp=0);WardWinter.enemies.project();S.pursuer.active=false;S.f.blackoutCount=2;S.f.visualEpisodes=2;S.f.falseEncounterSeen=1')
 def open_reader():
  ev('doc("Heller’s winter maintenance note")');q.wait_for_function('WardWinter.isReadingRecord()');assert ev('WardWinter.readingClock().paused')
 def close_reader():
  q.get_by_role('button',name='Return to room',exact=True).click();assert not ev('WardWinter.isReadingRecord()');return ev('WardWinter.readingClock()')
 fresh()
 ev('''S.pursuer.staggerUntil=S.t+12;S.pursuer.staggerDeadline=Date.now()+1000;
 S.sceneDisturbance={room:S.room,view:S.roomView,kind:"body",deadline:Date.now()+1000};
 S.f.power=1;S.f.powerOut=1;S.f.powerRestoreAt=S.t+50;S.f.powerRestoreReal=Date.now()+1000;
 window.__readerTurn=S.t;window.__readerCharge=S.bat;''')
 open_reader();q.wait_for_timeout(1450)
 assert ev('WardWinter.pursuerDown()&&S.pursuer.staggerUntil>S.t&&!!S.sceneDisturbance&&S.f.powerOut&&S.t===window.__readerTurn&&S.bat===window.__readerCharge')
 close_reader();remaining=ev('({stagger:S.pursuer.staggerDeadline-Date.now(),vision:S.sceneDisturbance.deadline-Date.now(),outage:S.f.powerRestoreReal-Date.now()})')
 assert all(750<v<1250 for v in remaining.values()),remaining
 q.wait_for_function('!S.pursuer.staggerUntil&&!S.sceneDisturbance&&!S.f.powerOut',timeout=4000)
 checks.append('an actual record freezes knockdown, visual episode and blackout deadlines as well as turn/battery costs; each resumes with its remaining duration')
 fresh();ev('S.pursuer.staggerUntil=S.t+12;S.pursuer.staggerDeadline=Date.now()+1200');open_reader();q.wait_for_timeout(380)
 q.locator('#wardPauseButton').click();q.wait_for_timeout(780);q.get_by_role('button',name='Resume game',exact=True).click();q.wait_for_timeout(380)
 assert ev('WardWinter.pursuerDown()&&WardWinter.isReadingRecord()')
 close_reader();remaining=ev('S.pursuer.staggerDeadline-Date.now()');assert 950<remaining<1450,remaining
 checks.append('opening game Pause over a record neither consumes the encounter opening nor double-counts its paused duration')
 fresh();ev('S.room="ward";S.roomViewRoom=null;S.san=40;S.f.falseEncounterSeen=0;render();wardFalseEncounter();S.hallCombat.deadline=Date.now()+850');assert ev('!!S.hallCombat')
 open_reader();q.wait_for_timeout(1350);assert ev('!!S.hallCombat');close_reader();remaining=ev('S.hallCombat.deadline-Date.now()');assert 650<remaining<1100,remaining
 q.wait_for_function('!S.hallCombat',timeout=2500)
 checks.append('imaginary combat does not expire behind a record and resolves only after the preserved real deadline resumes')
 fresh();ev('''localStorage.setItem(K,JSON.stringify(S));localStorage.setItem("lw_ch1_finale_checkpoint",JSON.stringify(S));
 localStorage.setItem("lw_ch1_cinematic_glass_checkpoint",JSON.stringify(S));localStorage.setItem("lw_ch1_cinematic_pursuer_checkpoint",JSON.stringify(S));window.__checkpointSeed=S.seed;loadGame();''')
 assert ev('!!localStorage.getItem("lw_ch1_finale_checkpoint")&&S.seed===window.__checkpointSeed')
 ev('newGame()');assert ev('S.seed!==window.__checkpointSeed&&!localStorage.getItem("lw_ch1_finale_checkpoint")&&!localStorage.getItem("lw_ch1_cinematic_glass_checkpoint")&&!localStorage.getItem("lw_ch1_cinematic_pursuer_checkpoint")&&!!localStorage.getItem(K)')
 checks.append('Continue preserves its existing checkpoint; only genuine New Game clears all three old run checkpoints while retaining the manual save')
 assert not errors,errors;b.close()
(ROOT/'tests/results/reading_clock_v9.json').write_text(json.dumps({'checks':checks,'javascript_errors':errors},indent=2)+'\n')
for c in checks:print('PASS',c)
