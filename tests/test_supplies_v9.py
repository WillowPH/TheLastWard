"""Finite medical/cell/save budgets, real rear pickups and paid Terminal saves."""
from pathlib import Path
import json
import sys

from playwright.sync_api import sync_playwright
from mouse_controls import turn_room

ROOT = Path(__file__).resolve().parents[1]
URL = sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:8010'
checks, errors, budgets = [], [], []

with sync_playwright() as p:
    browser = p.chromium.launch(executable_path='/usr/bin/chromium', args=['--no-sandbox'])
    page = browser.new_page(viewport={'width': 1600, 'height': 1000}, service_workers='block', reduced_motion='reduce')
    page.set_default_timeout(8000)
    page.on('pageerror', lambda error: errors.append(str(error)))
    ev = page.evaluate

    def ready():
        page.wait_for_function('WardWinter.roomViewRenderer()?.loaded&&!WardWinter.orbit.busy&&!WardWinter.travelling')

    def fresh(mode='1'):
        page.goto(URL)
        page.locator('#diff').select_option(mode)
        page.get_by_role('button', name='BEGIN INVESTIGATION', exact=True).click()
        ev('nextIntro();nextIntro();nextIntro()')
        ready()
        assert ev('!!WardWinter.supplies9'), 'The supply module must load in index.html before Pause'
        # Isolate inventory/placement behavior from random live encounters.
        ev('S.enemyActors.forEach(a=>a.hp=0);WardWinter.enemies.project();S.pursuer.active=false;S.f.falseEncounterSeen=1;S.f.visualEpisodes=2;S.f.blackoutCount=2;S.slots=12;S.f.power=1;S.f.phoneRinging=false;S.hp=100;add("Flashlight");render()')

    def room(name):
        ev('name=>{closeModal();wardCloseFocus();S.room=name;S.prev=null;S.roomViewRoom=null;S.sceneFocus=null;S.f.power=1;S.f.powerOut=0;S.f.wet=0;S.f.coldExposure=0;S.f.pursuerEncounter=0;S.pursuer.active=false;render();if(WardNavigation.isDark(name)&&!lit())toggleLight()}', name)
        ready()

    def action(object_id):
        close = page.get_by_role('button', name='Return to room ×', exact=True)
        if close.count() and close.is_visible():
            close.click()
        ready()
        fixture = ev('id=>WardScene.sites().find(f=>f.objects.some(o=>o[0]===id))', object_id)
        assert fixture, (ev('S.room'), object_id, ev('WardScene.sites().map(f=>f.id)'))
        if ev('S.roomView') != fixture.get('view', 'front'):
            turn_room(page)
        page.locator('[data-fixture="' + fixture['id'] + '"]').click()
        select = page.locator('button[onclick="wardSelectFinding(\'' + object_id + '\')"]')
        if select.count():
            select.click()
        page.locator('button[onclick="wardFixtureAction(\'' + object_id + '\')"]').click()

    for mode, cells, disks, dressings, kits, healing in [
        ('0.7', 4, 8, 5, 3, 235), ('1', 3, 6, 4, 2, 170), ('1.3', 2, 4, 3, 2, 150)
    ]:
        fresh(mode)
        result = ev('''()=>{
            const summaries=[], ammo=[];
            for(let i=0;i<128;i++){
                S.seed='supplies9-'+i;configureWorld(S.seed,false);
                const first=JSON.stringify(WardWinter.supplies9.summary());
                const rounds=WardWinter.balance8.ammoBudget();
                configureWorld(S.seed,true);configureWorld(S.seed,true);
                if(JSON.stringify(WardWinter.supplies9.summary())!==first)throw Error('Cumulative supplies');
                if(WardWinter.balance8.ammoBudget()!==rounds)throw Error('Cumulative ammunition');
                summaries.push(WardWinter.supplies9.summary());ammo.push(rounds);
                if(WardWinter.find('purgeSupplies')[4].give.some(([n])=>n==='Battery'))throw Error('Purge bonus cell');
                if(WardWinter.find('linenBattery'))throw Error('Redundant linen cell');
            }
            return {summary:summaries[0],variants:[...new Set(summaries.map(JSON.stringify))].length,ammo:[Math.min(...ammo),Math.max(...ammo)]};
        }''')
        assert result['variants'] == 1, (mode, result)
        summary = result['summary']
        assert [summary[k] for k in ['cells', 'disks', 'dressings', 'medkits', 'healing', 'cradleCharges']] == [cells, disks, dressings, kits, healing, 1], result
        budgets.append(result)
    checks.append('128 seeds on each difficulty retain fixed cell/save/medical budgets, unchanged optional ammunition bonuses and noncumulative reconfiguration')

    fresh()
    room('lobby')
    action('term')
    assert not page.locator('#m .md').count()
    assert ev('S.contextThought.text.includes("counter behind reception")')
    assert ev('cnt("Floppy Disk")===0&&S.saves===0')
    fresh('0.7')
    ev('S.slots=8;S.inv=[{n:"Floppy Disk",c:2},{n:"Flashlight",c:1},{n:"Handgun",c:1},{n:"Utility Knife",c:1},{n:"Lighter",c:1},{n:"Wire Spool",c:1},{n:"Archive Key",c:1},{n:"Boiler Key",c:1}];render()')
    room('lobby')
    action('securityRecordDisks')
    assert ev('cnt("Floppy Disk")===2&&S.ob.securityRecordDisks!=="done"')
    ev('wardCloseFocus();rem("Boiler Key");render()')
    action('securityRecordDisks')
    assert ev('cnt("Floppy Disk")===4&&S.ob.securityRecordDisks==="done"')
    checks.append('an empty Terminal gives a concrete reception-rear Thought, and a two-disk Story package stays intact when a full pack cannot fit both disks')

    fresh()
    room('security')
    action('earlyBattery')
    assert ev('cnt("Battery")===1&&S.ob.earlyBattery==="done"')
    ev('wardCloseFocus();configureWorld(S.seed,true);S.bat=10;useBat("Battery",false)')
    assert ev('cnt("Battery")===0&&S.bat===50&&S.ob.earlyBattery==="done"')
    ev('configureWorld(S.seed,true)')
    assert ev('S.ob.earlyBattery==="done"&&!has("Battery")')
    checks.append('a real cell pickup restores exactly40% once, and reconfiguration neither respawns it nor grants another cell')

    fresh()
    disk_sources = [('lobby', 'securityRecordDisks'), ('ward', 'gur'), ('pharmacy', 'pharmacyBattery'), ('generator', 'generatorRecordDisks'), ('residence', 'residenceRecordDisks'), ('lift', 'finalRibbon')]
    for name, object_id in disk_sources:
        room(name)
        action(object_id)
        assert ev('id=>S.ob[id]==="done"', object_id), object_id
        if name != 'lift':
            assert ev('S.roomView') == 'rear', (name, object_id)
        ev('wardCloseFocus()')
    assert ev('cnt("Floppy Disk")') == 6
    room('lobby')
    action('term')
    page.get_by_role('button', name='Cancel', exact=True).click()
    assert ev('cnt("Floppy Disk")') == 6
    action('term')
    page.get_by_role('button', name='Save record', exact=True).click()
    assert ev('cnt("Floppy Disk")===5&&S.saves===1')
    saved = ev('JSON.parse(localStorage.getItem(K))')
    assert sum(slot['c'] for slot in saved['inv'] if slot['n'] == 'Floppy Disk') == 5
    ev('configureWorld(S.seed,true)')
    assert ev('cnt("Floppy Disk")') == 5
    assert all(ev('id=>S.ob[id]==="done"', object_id) for _, object_id in disk_sources)
    checks.append('six actual Normal disk pickups are distributed across the chapter, five require rear views, Cancel costs nothing and one successful Terminal save consumes exactlyone disk')

    room('generator')
    ev('S.bat=10;render()')
    action('charger')
    assert ev('S.bat===75&&S.f.generatorChargeUses===1')
    ev('wardCloseFocus();rechargeAtGenerator()')
    assert ev('S.bat===75&&S.f.generatorChargeUses===1&&!WardWinter.chargerStatus("charger").available')
    ev('S.bat=0;render()')
    action('handCharge')
    assert ev('S.bat===12&&S.f.generatorChargeUses===1')
    ev('wardCloseFocus();S.bat=0;act("handCharge")')
    assert ev('S.bat===0&&S.f.generatorChargeUses===1')
    checks.append('the actual rear cradle has one65% reserve; exhausted supply stays exhausted, while the slow12% dynamo remains a cooldown-limited emergency fallback')

    fresh()
    room('ward')
    action('clinicDressing')
    assert ev('S.roomView==="rear"&&has("Trauma Dressing")&&S.ob.clinicDressing==="done"')
    ev('wardCloseFocus();S.hp=50;heal("Trauma Dressing")')
    assert ev('S.hp===70&&!has("Trauma Dressing")')
    room('observation')
    action('loungeFirstAid')
    assert ev('S.roomView==="rear"&&has("Field Medkit")&&S.ob.loungeFirstAid==="done"')
    ev('wardCloseFocus();S.hp=30;heal("Field Medkit")')
    assert ev('S.hp===75&&!has("Field Medkit")')
    assert not ev('R.stafflounge.o.some(o=>o[0]==="loungeFirstAid")')
    checks.append('early clinic dressing and later Observation first aid are genuine rear-container pickups, heal20/45HP and are not bundled into the Staff locker')

    for name, object_id in [('eastcorridor', 'staticNote'), ('isoward', 'patientFile'), ('chapel', 'let')]:
        room(name)
        action(object_id)
        assert ev('S.roomView') == 'rear', (name, object_id)
        assert page.locator('.record-reader').is_visible()
        ev('closeModal();wardCloseFocus()')
    checks.append('the newly useful Corridor, Treatment and Chapel rear furniture has real clickable records rather than empty scenery or door-overlapping targets')

    fresh()
    ev('S.inv=[{n:"Flashlight",c:1},{n:"Battery",c:2},{n:"Floppy Disk",c:3}];S.box=[{n:"Trauma Dressing",c:1}];S.ob.earlyBattery="done";S.ob.pharmacyBattery="done";S.f.generatorChargeUses=2;window.beforeSupplies=JSON.stringify({inv:S.inv,box:S.box,ob:S.ob});configureWorld(S.seed,true)')
    assert ev('JSON.stringify({inv:S.inv,box:S.box,ob:S.ob})===window.beforeSupplies')
    assert ev('S.f.generatorChargeUses===2&&!WardWinter.chargerStatus("charger").available')
    assert ev('WardWinter.supplies9.summary().cells===3&&WardWinter.supplies9.summary().disks===6')
    checks.append('continued records retain carried/stored supplies, collected legacy IDs and already-used charger reserves; the new world budget does not refill them')

    assert not errors, errors
    browser.close()

(ROOT / 'tests/results/supplies_v9.json').write_text(json.dumps({'checks': checks, 'budgets': budgets, 'javascript_errors': errors}, indent=2) + '\n')
for check in checks:
    print('PASS', check)
