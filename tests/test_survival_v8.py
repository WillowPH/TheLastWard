"""Earned incident scheduling and consequential, recoverable v8 hazards.

These are focused scenarios, not a whole-route resource balance claim. Story
flags are earned by the same incident choices a player uses; only fixture room,
condition and equipment are set up to isolate their effects.
"""
from pathlib import Path
import json, sys
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
URL = sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:8010'
checks, errors, hazard = [], [], []

def passed(label):
    checks.append(label)
    print('PASS', label, flush=True)

with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/usr/bin/chromium', args=['--no-sandbox'])
    q = b.new_page(viewport={'width': 1672, 'height': 941}, service_workers='block')
    q.set_default_timeout(8000)
    q.on('pageerror', lambda e: errors.append(str(e)))
    ev = q.evaluate

    def ready():
        q.wait_for_function('WardWinter.roomViewRenderer()?.loaded&&!WardWinter.orbit.busy')

    def fresh(mode='1'):
        q.goto(URL)
        q.locator('#diff').select_option(mode)
        q.get_by_role('button', name='BEGIN INVESTIGATION', exact=True).click()
        ev('nextIntro();nextIntro();nextIntro();S.enemyActors.forEach(a=>a.hp=0);WardWinter.enemies.project();S.pursuer.active=false;S.f.blackoutCount=2;S.slots=12;add("Flashlight");S.lightOn=false;render()')
        ready()

    def room(name, power=False):
        ev('''([name,power])=>{closeModal();wardCloseFocus();S.prev=S.room;S.room=name;
          S.roomView='front';S.roomViewRoom=name;S.f.power=power?1:0;S.f.powerOut=0;
          S.sceneFocus=null;render();}''', [name,power])
        ready()

    for mode in ['0.7', '1', '1.3']:
        fresh(mode)
        room('eastcorridor')
        ev('wardSprinkler()')
        shock = ev('({hp:S.hp,san:S.san,wet:S.f.wet,dropped:S.f.flashlightDropped})')
        assert shock['hp'] == {'0.7':92, '1':86, '1.3':82}[mode], shock
        assert shock['wet'] and shock['dropped']
        q.get_by_role('button', name='Reach for the shutoff', exact=True).click()
        ev('WardWinter.advanceExposure(10)')
        exposed = ev('[S.hp,S.san,S.f.coldExposure]')
        assert exposed[0] <= shock['hp']-8 and exposed[1] < shock['san'], (mode,shock,exposed)
        ev('doc("Night Attendant Journal")')
        freeze = ev('[S.hp,S.san,S.t,S.bat,S.f.coldExposure]')
        ev('advanceTime(10);WardWinter.advanceExposure(10);WardWinter.survivalTick()')
        q.wait_for_timeout(800)
        assert ev('[S.hp,S.san,S.t,S.bat,S.f.coldExposure]') == freeze
        q.get_by_role('button', name='Pause game', exact=True).click()
        ev('WardWinter.advanceExposure(10);wardSprinkler();wardRecoverFlashlight()')
        assert ev('[S.hp,S.san,S.t,S.bat,S.f.coldExposure]') == freeze
        q.get_by_role('button', name='Resume game', exact=True).click()
        q.get_by_role('button', name='Return to room', exact=True).click()
        ev('wardSprinkler();wardRecoverFlashlight()')
        stopped = ev('[S.hp,S.san]')
        assert ev('S.f.sprinklerStopped&&S.f.wet&&!S.f.flashlightDropped')
        room('wardservice')
        ev('WardWinter.advanceExposure(5)')
        assert ev('S.hp') < stopped[0]
        room('generator', True)
        dry_before = ev('S.hp')
        ev('WardWinter.advanceExposure(20)')
        assert ev('S.f.wet') and ev('S.hp') == dry_before
        q.get_by_role('button', name='Dry off and warm up', exact=True).click()
        assert ev('!S.f.wet&&!S.f.shivering&&S.f.coldExposure===0')
        hp = ev('S.hp')
        room('eastcorridor')
        ev('wardSprinkler()')
        assert ev('S.hp') == hp and not ev('S.f.wet')
        hazard.append({'mode':mode,'shock':shock,'ten_spray_turns':exposed,'recovered_hp':hp})
    assert hazard[0]['ten_spray_turns'][0] > hazard[1]['ten_spray_turns'][0] > hazard[2]['ten_spray_turns'][0]
    passed('three difficulties: once-only sprinkler shock, real sustained HP/sanity loss, ongoing wet travel cost, explicit recovery; reading and Pause freeze costs')

    fresh()
    room('wardnorth')
    ev('wardOpenWindows()')
    q.wait_for_timeout(50)
    assert ev('S.hp<=96&&S.san===97&&S.windows.closed.every(v=>!v)')
    ev('WardWinter.advanceExposure(7)')
    cold = ev('[S.hp,S.san,S.f.coldExposure]')
    assert cold[0] < 90 and cold[1] < 97 and ev('S.f.shivering')
    for i in range(3):
        ev('i=>wardCloseColdWindow(i)', i)
    assert ev('S.windows.resolved&&S.windows.closed.every(Boolean)')
    closed_hp = ev('S.hp')
    ev('wardOpenWindows()')
    assert ev('S.windows.closed.every(Boolean)&&S.hp') == closed_hp
    room('generator', True)
    q.get_by_role('button', name='Dry off and warm up', exact=True).click()
    assert ev('!S.f.shivering&&S.f.coldExposure===0')
    passed('one optional purge opens three dangerous windows; closing all catches and warming deliberately resolves local exposure')

    fresh()
    room('archive')
    ev('S.san=74;WardWinter.sanityEpisode()')
    assert ev('WardWinter.incidentStress()===0&&!S.sceneDisturbance&&!S.hallCombat')
    assert not q.locator('[data-sanity-vision]').count()
    passed('low composure without witnessed incident trauma cannot produce a vision or imaginary encounter')

    fresh()
    room('surgery')
    # This focused scenario begins already distressed; the actual fourteen-point
    # Kessler choice reaches the visual threshold without mutating his outcome.
    ev('S.san=88;doctorAtWall()')
    q.get_by_role('button', name='Call his name', exact=True).click()
    q.wait_for_timeout(950)
    assert ev('S.f.doctorWallSeen&&S.san===74&&S.f.pendingSanityEpisode&&!S.sceneDisturbance&&!S.hallCombat')
    q.get_by_role('button', name='Step back', exact=True).click()
    q.wait_for_function('!!S.sceneDisturbance', timeout=3000)
    assert ev('S.sceneDisturbance.room==="surgery"&&S.sceneDisturbance.view==="front"&&S.f.visualEpisodes===1')
    # The pending episode is visible in the facing the player already has.
    assert q.locator('[data-sanity-vision]').count() == 1
    q.wait_for_function('document.querySelector("[data-sanity-vision] img")?.complete&&document.querySelector("[data-sanity-vision] img")?.naturalWidth>0')
    memory = q.locator('[data-sanity-vision]').evaluate('''n=>({className:n.className,source:n.querySelector('img').dataset.solidSource,before:getComputedStyle(n,':before').content,transform:getComputedStyle(n).transform})''')
    assert 'sanity-memory' in memory['className'] and 'infected_patient.png' in memory['source'], memory
    assert memory['before'] == 'none' and memory['transform'] == 'none', memory
    assert ev('S.roomView') == 'front'
    ev('window.__visionPause=[];document.addEventListener("ward:pause",e=>window.__visionPause.push({paused:e.detail.paused,now:Date.now(),deadline:S.sceneDisturbance?.deadline}))')
    q.get_by_role('button', name='Pause game', exact=True).click()
    q.wait_for_timeout(900)
    q.get_by_role('button', name='Resume game', exact=True).click()
    pause_clock = ev('window.__visionPause')
    assert len(pause_clock) == 2 and pause_clock[0]['paused'] and not pause_clock[1]['paused'], pause_clock
    remaining = [v['deadline']-v['now'] for v in pause_clock]
    assert abs(remaining[1]-remaining[0]) < 100, pause_clock
    assert pause_clock[1]['deadline']-pause_clock[0]['deadline'] >= 850, pause_clock
    # Let the authored fifteen-second vision expire on its real clock.
    q.wait_for_function('!S.sceneDisturbance', timeout=18000)
    before = ev('[S.san,S.f.visualEpisodes]')
    ev('doctorAtWall()')
    assert ev('[S.san,S.f.visualEpisodes]') == before
    passed('an actual Kessler choice while pre-distressed records pending trauma during its modal, then shows a decoded grounded infected memory in the current facing; Pause preserves its fifteen-second life and the event cannot repeat')

    room('isoward')
    ev('add("Utility Knife");add("Handgun");S.eq="Handgun";S.ld.Handgun=6;beggingPatient()')
    q.get_by_role('button', name='End his suffering', exact=True).click()
    q.get_by_role('button', name='Use utility knife', exact=True).click()
    assert ev('S.f.beggingPatientChoice==="killed"&&S.f.patientMethod==="knife"')
    q.get_by_role('button', name='Step away', exact=True).click()
    ev('advanceTime(22)')
    q.wait_for_function('!!S.hallCombat', timeout=3000)
    assert ev('S.f.falseEncounterSeen&&WardWinter.incidentStress()===31')
    hp = ev('S.hp');ammo = ev('S.ld.Handgun')
    q.get_by_role('button', name='Quick shot', exact=True).click()
    assert ev('S.ld.Handgun') == ammo-1
    for _ in range(4):
        if ev('!!S.hallCombat'):
            q.get_by_role('button', name='Hold and observe', exact=True).click()
    assert ev('!S.hallCombat&&S.f.falseEncounterResolved&&S.hp') == hp
    before = ev('[S.san,S.f.patientMethod,S.f.beggingPatientChoice]')
    ev('choosePatientFate("left");wardConfirmPatient("knife");wardFalseEncounter()')
    assert ev('[S.san,S.f.patientMethod,S.f.beggingPatientChoice]') == before
    assert not ev('S.hallCombat')
    passed('actual Kessler plus irreversible Mercer knife decision earn imaginary combat after a cooldown; firing spends real ammunition, observing resolves it without injury, and it cannot replay')

    room('records')
    ev('researcherLastRoom()')
    q.get_by_role('button', name='Read the annotation', exact=True).click()
    assert ev('S.docs.includes("Final Research Entry")&&S.docs.includes("Rourke’s final annotation")')
    snapshot = ev('[S.san,S.t,S.f.visualEpisodes]')
    ev('advanceTime(40);WardWinter.sanityEpisode()')
    q.wait_for_timeout(900)
    assert ev('[S.san,S.t,S.f.visualEpisodes]') == snapshot
    q.get_by_role('button', name='Return to room', exact=True).click()
    before = ev('S.san');ev('researcherLastRoom()');assert ev('S.san') == before
    room('observation')
    ev('plexiIncident()')
    q.get_by_role('button', name='Back away', exact=True).click()
    ev('advanceTime(32)')
    q.wait_for_function('S.f.visualEpisodes===2&&!!S.sceneDisturbance', timeout=3000)
    assert ev('S.sceneDisturbance.view==="front"&&S.sceneDisturbance.kind==="body"')
    q.wait_for_function('!S.sceneDisturbance', timeout=18000)
    ev('advanceTime(100);for(let i=0;i<10;i++)WardWinter.sanityEpisode()')
    assert ev('S.f.visualEpisodes===2&&S.f.falseEncounterSeen&&!S.hallCombat&&!S.sceneDisturbance')
    before = ev('S.san');ev('plexiIncident()');assert ev('S.san') == before
    passed('Rourke evidence and scientist incident remain once-only; records suppress episodes, later trauma produces the second visible vision, and two visions plus one false fight is the per-run cap')
    assert not errors, errors
    b.close()

(ROOT/'tests/results/survival_v8.json').write_text(json.dumps({'checks':checks,'hazard':hazard,'javascript_errors':errors},indent=2)+'\n')
