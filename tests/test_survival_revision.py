"""Focused survival boundaries, earned horror, finite supplies and retreat arrivals."""
from pathlib import Path
import json
import sys
from playwright.sync_api import sync_playwright
from mouse_controls import turn_room

ROOT = Path(__file__).resolve().parents[1]
URL = sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:8010'
checks, errors, balance = [], [], []


def passed(label):
    checks.append(label)
    print('PASS', label, flush=True)


with sync_playwright() as p:
    browser = p.chromium.launch(executable_path='/usr/bin/chromium', args=['--no-sandbox'])
    context = browser.new_context(viewport={'width': 1600, 'height': 1000}, service_workers='block')
    page = context.new_page()
    page.set_default_timeout(8000)
    page.on('pageerror', lambda error: errors.append(str(error)))
    ev = page.evaluate

    def ready():
        page.wait_for_function('WardWinter.roomViewRenderer()?.loaded&&!WardWinter.orbit.busy')

    def fresh(mode='1'):
        page.goto(URL)
        page.locator('#diff').select_option(mode)
        page.get_by_role('button', name='BEGIN INVESTIGATION', exact=True).click()
        ev('nextIntro();nextIntro();nextIntro()')
        ready()
        # Compare difficulty on one authored run. Independent random seeds can
        # move or resize optional ammo caches and invalidate a balance comparison.
        ev('''S.seed='survival-revision-fixture';S.rngState=hashSeed(S.seed);
            S.puzzles=generatePuzzles();configureWorld(S.seed,false);placeTelephones(S.seed);
            S.enemyActors.forEach(a=>a.hp=0);WardWinter.enemies.project();
            S.pursuer.active=false;S.f.blackoutCount=2;S.slots=12;
            add('Flashlight',1);S.lightOn=false;render()''')

    def room(name, powered=False):
        ev('''v=>{$('m').innerHTML='';wardCloseFocus();S.prev=S.room;S.room=v.name;
            S.roomView='front';S.roomViewRoom=S.room;S.f.power=v.powered?1:0;
            S.f.powerOut=0;S.sceneFocus=null;S.contextThought=null;render();}''',
           {'name': name, 'powered': powered})
        ready()

    for mode in ['0.7', '1', '1.3']:
        fresh(mode)
        ammo = ev('''()=>{const sum=()=>Object.values(R).flatMap(r=>r.o).flatMap(o=>o[4].give||[])
            .filter(([n])=>n==='Handgun Ammo').reduce((s,[,n])=>s+n,0);
            const before=sum();configureWorld(S.seed,true);configureWorld(S.seed,true);
            return {before,after:sum(),actors:S.enemyActors.length};}''')
        assert ammo['before'] == ammo['after'], ammo
        room('eastcorridor')
        ev('S.hp=100;S.san=100;wardSprinkler()')
        initial = ev('({hp:S.hp,san:S.san})')
        assert 0 < initial['hp'] < 100 and initial['san'] == 94, initial
        page.get_by_role('button', name='Reach for the shutoff', exact=True).click()
        ev('wardCloseFocus();advanceTime(4)')
        exposed = ev('({hp:S.hp,san:S.san,wet:S.f.wet})')
        assert exposed['hp'] < initial['hp'] and exposed['san'] < initial['san'] and exposed['wet'], exposed
        ev('wardSprinkler();wardRecoverFlashlight()')
        room('generator', True)
        ev('advanceTime(40)')
        assert ev('!!S.f.wet'), 'Shelter must not automatically dry clothes.'
        ev('wardWarmUp()')
        assert ev('!S.f.wet&&!S.f.shivering&&S.f.coldExposure===0')
        recovered = ev('({hp:S.hp,san:S.san})')
        room('eastcorridor')
        ev('wardSprinkler()')
        assert ev('S.hp') == recovered['hp']
        assert ev('!S.f.flashlightDropped&&S.f.sprinklerStopped')
        balance.append({'mode': mode, 'ammo': ammo, 'sprinkler_initial': initial, 'after_four_exposure_turns': exposed})
    assert balance[0]['ammo']['before'] > balance[1]['ammo']['before'] > balance[2]['ammo']['before'], balance
    assert balance[0]['after_four_exposure_turns']['hp'] > balance[1]['after_four_exposure_turns']['hp'] > balance[2]['after_four_exposure_turns']['hp'], balance
    passed('Story/Normal/Nightmare have finite stable ammunition and increasing real hazard damage; wetness requires deliberate recovery')

    fresh()
    room('wardnorth')
    ev('wardOpenWindows();advanceTime(5);S.bat=70;S.lightOn=true;doc("Heller’s winter maintenance note")')
    snapshot = ev('[S.hp,S.san,S.bat,S.t,S.f.coldExposure,S.windows.exposure]')
    ev('advanceTime(20);WardWinter.advanceExposure(20);WardWinter.consumeFlashlight(20);WardWinter.survivalTick()')
    page.wait_for_timeout(1200)
    assert ev('[S.hp,S.san,S.bat,S.t,S.f.coldExposure,S.windows.exposure]') == snapshot
    ev('closeModal();wardCloseFocus();advanceTime(2)')
    assert ev('S.hp') < snapshot[0] and ev('S.bat') < snapshot[2]
    passed('an actual document pauses health, sanity, exposure, world time and battery costs; closing it resumes the hazard')

    fresh()
    room('observation', True)
    ev('add("Field Medkit",2);add("Battery",1);add("Handgun",1);S.eq="Handgun";S.ld.Handgun=3;inspectObservationGlass()')
    page.get_by_role('button', name='Step back for now', exact=True).click()
    ev('inspectObservationGlass()')
    assert ev('S.hp===0&&S.f.dead')
    terminal = ev('JSON.stringify({inv:S.inv,room:S.room,time:S.t,loaded:S.ld})')
    ev('''heal('Field Medkit');useInventoryHeal('Field Medkit');combatHeal('Field Medkit');
        useInventorySlot(S.inv.findIndex(s=>s.n==='Field Medkit'));useBat('Battery',false);
        equipWeapon('Handgun');reload();shoot();go('generator');wardOpenWindows();advanceTime(20);
        WardWinter.survivalTick();WardWinter.advanceExposure(20);WardWinter.consumeFlashlight(20);''')
    assert ev('S.hp===0&&S.f.dead')
    assert ev('JSON.stringify({inv:S.inv,room:S.room,time:S.t,loaded:S.ld})') == terminal
    ev('S.hp=30;heal("Field Medkit")')
    assert ev('S.hp===0&&S.f.dead'), 'The terminal latch must defeat a stale positive-health update.'
    ev('delete S.f.dead;S.hp=30;render()')
    assert ev('S.hp===0&&S.f.dead'), 'Old positive-health saves after the fatal glass outcome must also remain terminal.'
    ev('loadCheckpoint()')
    ready()
    assert ev('S.hp>0&&!S.f.dead&&S.f.glassHunterRetreated')
    passed('fatal glass is terminal before Continue; every stale item/combat/travel/timer path stays dead until explicit checkpoint load')

    for pursuer in [False, True]:
        fresh()
        room('laundry', True)
        ev('''S.prev='surgery';S.f.doctorWallSeen=0;S.f.doctorWallEncounterStarted=0;
            window.__arrivalCalls=[];window.__arrivalOriginal=chapterArrival;
            chapterArrival=function(...args){window.__arrivalCalls.push(args);return window.__arrivalOriginal(...args)};void 0;''')
        if pursuer:
            ev('''S.pursuer.active=true;S.pursuer.room=S.room;S.pursuer.cooldown=0;
                S.f.pursuerStarted=1;S.f.pursuerEncounter=0;pursuerEncounter()''')
            before = ev('S.t')
            page.get_by_role('button', name='Retreat through an unlocked door', exact=True).click()
        else:
            ev('''const a=S.enemyActors[0];a.hp=a.maxHp=20;a.room='laundry';a.home='laundry';a.down=false;a.dormant=false;
                WardWinter.enemies.project();combat()''')
            before = ev('S.t')
            page.get_by_role('button', name='Retreat', exact=True).click()
        assert ev('S.room') == 'surgery'
        assert ev('S.f.doctorWallEncounterStarted&&!S.f.doctorWallSeen')
        assert ev('window.__arrivalCalls') == [['laundry', 'surgery']], {'pursuer':pursuer,'calls':ev('window.__arrivalCalls')}
        assert ev('S.t') - before == 3
        assert page.get_by_role('button', name='Call his name', exact=True).count() == 1
        if pursuer:
            # The twelve-turn evasion window includes the same three-turn
            # physical doorway traversal as ordinary movement.
            assert ev('S.pursuer.evadeUntil-S.t') >= 9
            ev('''S.pursuer.room=S.room;S.pursuer.cooldown=0;S.f.pursuerEncounter=0;
                S.t=S.pursuer.evadeUntil-1;pursuerApproach(S.room);pursuerApproach(S.room);''')
            assert not ev('S.f.pursuerEncounter'), 'Successful evasion needs a real recovery interval.'
            ev('S.t+=2;pursuerApproach(S.room)')
            assert ev('S.f.pursuerEncounter'), 'The recovery interval must expire.'
            ev('''S.f.pursuerEncounter=0;S.pursuer.room='laundry';S.pursuer.evadeUntil=0;
                S.pursuer.cooldown=3;S.pursuer.approachCheckedAt=-1;
                pursuerApproach(S.room);pursuerApproach(S.room);pursuerApproach(S.room);''')
            assert ev('S.pursuer.cooldown') == 2, 'Arrival and clock must not consume cooldown three times in one turn.'
    passed('infected flee and Subject X retreat each invoke the new room’s scripted incident exactly once, with one original movement cost')
    passed('Subject X evasion buys a finite twelve-turn Normal recovery interval including travel; repeated arrival checks cannot burn it in one turn')

    fresh()
    room('archive', True)
    ev('''S.hp=88;S.san=76;S.f.doctorWallSeen=1;S.f.researcherLastRoomSeen=1;
        add('Handgun',1);S.eq='Handgun';S.ld.Handgun=6;S.pursuer.active=true;
        S.pursuer.room=S.room;WardWinter.sanityEpisode()''')
    assert not ev('S.hallCombat'), 'A hallucination must not replace a real Subject X already in this room.'
    ev('S.pursuer.active=false;WardWinter.sanityEpisode()')
    assert ev('!!S.hallCombat&&S.f.falseEncounterSeen')
    assert page.locator('.winter-actor.infected').count() == 1
    ev('''const a=S.enemyActors[0];a.hp=a.maxHp=20;a.room=a.home='wardservice';a.down=false;a.dormant=false;
        a.alert={room:'archive',expires:S.t+100};a.lastMove=S.t-4;WardWinter.enemies.project();''')
    page.get_by_role('button', name='Quick shot', exact=True).click()
    assert ev('S.ld.Handgun') == 5
    assert ev('S.enemyActors[0].room') == 'wardservice', 'A real infected waits outside an active imaginary encounter.'
    for _ in range(4):
        if ev('!!S.hallCombat'):
            page.get_by_role('button', name='Hold and observe', exact=True).click()
    assert ev('S.hp===88&&!S.hallCombat&&S.f.falseEncounterResolved')
    ev('wardFalseEncounter()')
    assert not ev('S.hallCombat')
    passed('two saved incidents earn visible imaginary combat despite partial composure recovery; it spends real ammo, never health, and cannot replay')

    fresh()
    room('archive', True)
    ev('S.san=86;S.f.doctorWallSeen=1;WardWinter.sanityEpisode()')
    assert ev('S.sceneDisturbance?.kind') == 'hanged'
    turn_room(page)
    ready()
    assert ev('S.roomView') == 'rear'
    assert page.locator('.winter-hallucinated-body').count() == 1
    page.wait_for_function('document.querySelector(".winter-hallucinated-body img")?.naturalWidth>0')
    ev('S.sceneDisturbance.deadline=0')
    page.wait_for_timeout(500)
    assert not ev('S.sceneDisturbance')
    ev('WardWinter.sanityEpisode()')
    assert not ev('S.sceneDisturbance'), 'Visual episodes need a quiet interval.'
    ev('S.t+=46;WardWinter.sanityEpisode()')
    assert ev('S.sceneDisturbance?.kind') == 'body'
    ev('S.sceneDisturbance.deadline=0')
    page.wait_for_timeout(500)
    ev('S.t+=100;WardWinter.sanityEpisode()')
    assert not ev('S.sceneDisturbance')
    passed('earned body visions are actually drawn, expire, have a cooldown, and stop after two episodes')
    assert not errors, errors
    browser.close()

(ROOT / 'tests/results').mkdir(exist_ok=True)
(ROOT / 'tests/results/survival_revision.json').write_text(json.dumps({'checks': checks, 'balance': balance, 'javascript_errors': errors}, indent=2) + '\n')
