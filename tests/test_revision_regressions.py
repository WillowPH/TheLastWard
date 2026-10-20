"""Browser regressions for the reported survival, reading and inventory failures.

World setup is isolated per scenario; the feature itself is exercised through its
normal mouse control. No complete-run progress is claimed by these focused checks.
"""
from pathlib import Path
import json
import re
import sys
from playwright.sync_api import sync_playwright
from mouse_controls import turn_room

ROOT = Path(__file__).resolve().parents[1]
URL = sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:8010'
OUT = ROOT / 'tests/results'
checks, errors = [], []


def passed(label):
    checks.append(label)
    print('PASS', label, flush=True)


with sync_playwright() as playwright:
    browser = playwright.chromium.launch(executable_path='/usr/bin/chromium', args=['--no-sandbox'])
    context = browser.new_context(viewport={'width': 1672, 'height': 941}, service_workers='block', reduced_motion='reduce')
    page = context.new_page()
    page.set_default_timeout(6500)
    page.on('pageerror', lambda error: errors.append(str(error)))
    ev = page.evaluate

    def ready():
        page.wait_for_function('WardWinter.roomViewRenderer()?.loaded&&!WardWinter.orbit.busy&&!WardWinter.travelling')

    def fresh():
        page.goto(URL)
        page.locator('#diff').select_option('1')
        page.get_by_role('button', name='BEGIN INVESTIGATION', exact=True).click()
        ev('nextIntro();nextIntro();nextIntro()')
        ready()
        ev('S.enemyActors.forEach(a=>a.hp=0);WardWinter.enemies.project();S.pursuer.active=false;S.f.blackoutCount=2;render()')

    def room(name, power=False, view=None):
        ev('''args=>{closeModal();wardCloseFocus();S.room=args.name;S.prev=args.name;S.roomViewRoom=null;
            S.f.power=args.power?1:0;S.f.powerOut=0;S.pursuer.active=false;S.contextThought=null;render();
            if(args.view&&S.roomView!==args.view){S.roomView=args.view;renderScene();}}''',
           {'name': name, 'power': power, 'view': view})
        ready()

    def target(object_id):
        fixture = ev('id=>WardScene.sites().find(f=>f.objects.some(o=>o[0]===id))?.id', object_id)
        assert fixture, ('Missing authored fixture', ev('S.room'), object_id)
        point = ev('id=>WardWinter.orbit.points().find(p=>p.id==="fixture:"+id)', fixture)
        assert point, ('Missing facing point', object_id)
        if ev('S.roomView') != point['view']:
            turn_room(page)
            ready()
        page.locator('[data-fixture="' + fixture + '"]').click()
        if page.locator('.finding-choices button').count():
            ev('id=>wardSelectFinding(id)', object_id)
        return fixture

    def action(object_id):
        target(object_id)
        button = page.locator('button[onclick="wardFixtureAction(\'' + object_id + '\')"]')
        if button.count():
            button.click()

    def no_scroll(selector):
        result = ev('''selector=>{const n=document.querySelector(selector),r=n?.getBoundingClientRect();
            return n?{height:n.clientHeight,scroll:n.scrollHeight,top:r.top,bottom:r.bottom,viewport:innerHeight}:null;}''', selector)
        assert result and result['scroll'] <= result['height'] + 2, (selector, result)
        assert result['top'] >= -1 and result['bottom'] <= result['viewport'] + 1, (selector, result)

    fresh()
    assert not ev('has("Flashlight")'), 'The intro must not place the flashlight into inventory.'
    pickup = ev('R.lobby.o.find(o=>o[4].give?.some(g=>g[0]==="Flashlight"))?.[0]')
    assert pickup, 'Opening room needs a physical flashlight pickup.'
    action(pickup)
    assert ev('has("Flashlight")&&S.ob[R.lobby.o.find(o=>o[4].give?.some(g=>g[0]==="Flashlight"))[0]]==="done"')
    passed('flashlight starts in the room and is obtained through its actual mouse pickup')

    named_actors = ev('''Object.entries(WardScenes).flatMap(([room,bp])=>bp.fixtures
        .filter(f=>f.actor&&/judith|shaw|evelyn/i.test(f.id+" "+f.label+" "+f.actor)).map(f=>room+"/"+f.id))''')
    assert not named_actors, named_actors
    for name in ['pharmacy', 'stafflounge']:
        room(name, power=True, view='front')
        assert page.locator('.c1-npc').count() == 0, name
    ev('infectedDoctor("ward")')
    assert not page.get_by_role('button', name='Leave quietly', exact=True).count()
    passed('named nurses have no living scene actors; invisible clipboard-doctor modal no longer appears')

    room('security', power=True, view='front')
    diary_fixture = target('attendantDiary1')
    assert page.locator('.c1-finding,.winter-drawer-item').count() == 1
    assert page.locator('.finding-choices button').count() == 0
    no_scroll('.reading-focus')
    page.get_by_role('button', name='Read', exact=True).click()
    assert ev('WardWinter.isReadingRecord()')
    no_scroll('#m .md')
    no_scroll('.winter-document')
    assert 'NIGHT ATTENDANT' in page.locator('#m').inner_text()
    ev('closeModal();wardCloseFocus()')
    note_fixture = target('winterJournal')
    assert note_fixture != diary_fixture, 'Heller’s note belongs to separate rear furniture.'
    assert page.locator('.c1-finding,.winter-drawer-item').count() == 1
    ev('wardCloseFocus()')
    target('cam')
    assert page.locator('.c1-finding,.winter-drawer-item').count() == 1
    no_scroll('.reading-focus')
    passed('journal/note and camera/recording fixtures show one selected finding without stacked scroll panels')

    room('wardnorth', power=False)
    ev('S.bat=70;S.lightOn=false;toggleLight();doc("Heller’s winter maintenance note")')
    charge, turn = ev('[S.bat,S.t]')
    assert ev('WardWinter.isReadingRecord()')
    ev('advanceTime(12)')
    page.wait_for_timeout(2200)
    assert ev('[S.bat,S.t]') == [charge, turn], ev('[S.bat,S.t]')
    no_scroll('#m .md')
    no_scroll('.winter-document')
    ev('closeModal();wardCloseFocus();advanceTime(2)')
    assert ev('S.bat') < charge
    passed('document reading pauses real-time and action-time battery costs; exploration resumes draining afterward')

    room('ward', power=True)
    ev('S.lightOn=false;S.bat=60;toggleLight();advanceTime(5)')
    assert not ev('S.lightOn'), 'Powered-room flashlight should stay off.'
    assert ev('S.bat') == 60
    room('wardnorth', power=False)
    ev('S.lightOn=false;wardInspectFixture("notice")')
    assert 'too dark to see' in page.locator('#interactiveScene').inner_text().lower()
    assert 'flashlight' in page.locator('#thoughtCaptionText').inner_text().lower()
    passed('powered-room flashlight does not run; dark examination gives a visible scene warning and practical thought')

    room('lobby', power=False)
    ev('S.bat=80;render()')
    assert not ev('WardWinter.chargerStatus("emergencyDynamo").available')
    assert not page.locator('[data-fixture="dynamo"]').count()
    ev('S.bat=0;render()')
    assert ev('WardWinter.chargerStatus("emergencyDynamo").available')
    assert page.locator('[data-fixture="dynamo"]').count() == 1
    passed('emergency battery charger is named and becomes interactive only when a nearly empty flashlight can use it')

    ev('S.docs=["Telephone record 1","Attendant Journal — Page I","Duty Roster","Memorial Ledger"];S.f.c_kp=0;S.f.c_cat=0;S.f.pharm=0')
    room('wardservice', power=False)
    ev('S.lightOn=true;evidenceModal()')
    text = page.locator('#m').inner_text()
    assert 'Duty Roster' in text
    assert 'DDMM' not in ev('docText("Memorial Ledger")')
    # The relevant record should be accessible without paging through unrelated lore.
    catalogue = ev('WardWinter.fileCatalogue()')
    roster = next(v for v in catalogue if v['title'] == 'Duty Roster')
    assert roster['lead'] and roster['topic'] == 'Pharmacy lock'
    page.locator('button[data-file="Duty Roster"]').click()
    assert 'WARD ROTATION' in page.locator('#m').inner_text()
    ev('closeModal()')
    passed('collected puzzle evidence remains directly accessible in Files and memorial record omits DDMM solution format')

    ev('S.bat=70;S.lightOn=true;render()')
    action('kp')
    page.locator('#cin').fill('12')
    page.get_by_role('button', name='Read Duty Roster', exact=True).click()
    assert 'WARD ROTATION' in page.locator('#m').inner_text()
    page.get_by_role('button', name='Return to puzzle', exact=True).click()
    assert page.locator('#cin').input_value() == ''
    assert not ev('S.f.c_kp||S.f.pharm')
    ev('closeModal();wardCloseFocus()')
    passed('a lock opens only its collected clue and returns to the unsolved puzzle without filling in the answer')

    # Pagination is allowed on the document, never an inner scrolling sheet.
    for viewport in [{'width': 1672, 'height': 941}, {'width': 390, 'height': 844}]:
        page.set_viewport_size(viewport)
        ev('doc("Heller’s winter maintenance note")')
        page.wait_for_timeout(150)
        no_scroll('#m .md')
        no_scroll('.winter-document')
        no_scroll('.winter-paper-text')
        state = ev('({pages:WardWinter.reader().pages.slice(),page:WardWinter.reader().page,text:WardWinter.reader().text})')
        assert state['pages'] and ''.join(state['pages']).strip()
        assert ' '.join(' '.join(state['pages']).split()) == ' '.join(state['text'].split())
        # The full text remains reachable and readable through mouse page buttons.
        for index in range(1, len(state['pages'])):
            page.get_by_role('button', name='Next document page', exact=True).click()
            assert ev('WardWinter.reader().page') == index
            no_scroll('.winter-paper-text')
        assert page.get_by_role('button', name='Next document page', exact=True).is_disabled()
        ev('closeModal();evidenceModal()')
        no_scroll('#m .md')
        page.get_by_role('searchbox').fill('Roster')
        assert page.locator('#recordFileList .file-entry').count() == 1
        page.locator('button[data-file="Duty Roster"]').click()
        page.get_by_role('button', name='Return to Files', exact=True).click()
        no_scroll('#m .md')
        page.get_by_role('searchbox').fill('')
        ev('closeModal()')
    page.set_viewport_size({'width': 1672, 'height': 941})
    ev('WardWinter.think("A very long thought. ".repeat(80));render()')
    assert page.locator('#thoughtCaptionControls').inner_text().strip() == 'Read in Journal'
    assert not page.get_by_role('button', name='Next thought page', exact=True).count()
    page.get_by_role('button', name='Read in Journal', exact=True).click()
    assert ev('WardWinter.reader().text') == ('A very long thought. ' * 80).strip()
    ev('closeModal()')
    passed('long handwritten records fit desktop and mobile, mouse pagination reaches all pages, Thoughts have no numbered pages')

    rear_pickups = ev('''Object.entries(R).flatMap(([room,r])=>r.o.filter(o=>o[4].give).flatMap(o=>{
        const fixture=WardScenes[room]?.fixtures.find(f=>f.ids?.includes(o[0]));
        return fixture&&WardRoomViews[room]?.fixtures[fixture.id]?.view==='rear'?[{room,id:o[0],item:o[4].give[0][0],free:!o[4].need&&!o[4].after&&!o[4].code&&!o[4].seq}]:[];}))''')
    assert len({v['room'] for v in rear_pickups}) >= 4, rear_pickups
    pickup = next(v for v in rear_pickups if v['free'] and not ev('id=>S.ob[id]==="done"', v['id']))
    room(pickup['room'], power=True, view='front')
    ev('S.inv=[{n:"Flashlight",c:1}];S.slots=12;S.lightOn=WardNavigation.isDark(S.room);S.bat=80;render()')
    action(pickup['id'])
    assert ev('S.roomView') == 'rear'
    assert ev('id=>S.ob[id]==="done"', pickup['id'])
    assert ev('name=>has(name)', pickup['item'])
    passed('useful pickups occupy rear views in several rooms and can be reached, examined and taken using mouse facing controls')

    room('wardnorth', power=False)
    ev('S.hp=100;S.san=100;S.lightOn=false;delete S.windows;S.f.wet=0;S.f.coldExposure=0')
    action('windowLever')
    page.get_by_role('button', name='Pull the handle', exact=True).click()
    ready()
    assert ev('S.windows.triggered&&S.windows.closed.every(v=>!v)')
    assert ev('S.roomView') == 'rear'
    ev('wardCloseFocus();advanceTime(8)')
    assert ev('S.hp') < 100, ev('({hp:S.hp,windows:S.windows,cold:S.f.coldExposure})')
    assert ev('S.san') < 100
    for index in range(3):
        action('coldWindow' + str(index))
        ready()
    assert ev('S.windows.resolved&&S.windows.closed.every(Boolean)')
    health = ev('S.hp')
    ev('wardCloseFocus();advanceTime(2)')
    assert ev('S.hp') == health, 'Closed dry windows must stop damaging the player.'
    ev('wardOpenWindows()')
    assert ev('S.windows.resolved&&S.windows.closed.every(Boolean)')
    passed('purge handle opens the actual rear windows, unclosed exposure hurts health/sanity, three catches resolve it once')

    room('eastcorridor', power=False)
    ev('S.hp=100;S.f.sprinklerTriggered=0;S.f.sprinklerStopped=0;S.f.wet=0;S.f.coldExposure=0;wardSprinkler()')
    assert ev('S.hp') < 100
    page.get_by_role('button', name='Reach for the shutoff', exact=True).click()
    ev('wardSprinkler();wardRecoverFlashlight();wardCloseFocus();advanceTime(8)')
    assert ev('S.f.wet&&S.hp<93')
    room('generator', power=True)
    ev('advanceTime(40)')
    assert ev('!!S.f.wet'), 'Walking or simply waiting in warmth must not erase wet clothing.'
    ev('wardWarmUp()')
    assert not ev('S.f.wet||S.f.shivering||S.f.coldExposure')
    passed('sprinkler causes injury, wet clothing persists, and deliberate warming recovers the local hazard')

    fresh()
    room('observation', power=True)
    ev('S.slots=12;add("Field Medkit",2);S.f.glassHunterEligible=true;render();inspectObservationGlass()')
    assert 'WARNING' in page.locator('#m').inner_text()
    page.get_by_role('button', name='Step back for now', exact=True).click()
    ev('inspectObservationGlass()')
    assert ev('S.hp') == 0
    page.get_by_role('button', name='Continue', exact=True).click()
    assert page.get_by_role('heading', name=re.compile(r'^(YOU DIED|GAME OVER)$')).count()
    count = ev('cnt("Field Medkit")')
    # Cover all stale action paths, including the exact heal exploit, without
    # relying on a disabled DOM button as the only death-state protection.
    ev('heal("Field Medkit");combatHeal();useInventorySlot(S.inv.findIndex(s=>s.n==="Field Medkit"));useBat("Battery",false);go("generator");advanceTime(10)')
    assert ev('S.hp') == 0
    assert ev('cnt("Field Medkit")') == count
    assert ev('S.room') == 'observation'
    assert page.get_by_role('heading', name=re.compile(r'^(YOU DIED|GAME OVER)$')).count()
    page.get_by_role('button', name='Observation checkpoint', exact=True).click()
    ready()
    assert ev('S.hp>0&&!S.f.dead&&S.f.glassHunterRetreated')
    passed('warned fatal glass encounter cannot be healed or escaped through stale actions; explicit checkpoint restores a live run')

    assert not errors, errors
    browser.close()

OUT.mkdir(exist_ok=True)
(OUT / 'revision_regressions.json').write_text(json.dumps({'transport': URL, 'checks': checks, 'javascript_errors': errors}, indent=2) + '\n')
