"""Story evidence, legacy save-item migration and one-use purge reward regressions."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
URL = sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:8010'
checks, errors = [], []
with sync_playwright() as p:
    browser = p.chromium.launch(executable_path='/usr/bin/chromium', args=['--no-sandbox'])
    page = browser.new_page(viewport={'width': 1672, 'height': 941}, service_workers='block', reduced_motion='reduce')
    page.on('pageerror', lambda error: errors.append(str(error)))
    page.goto(URL)
    page.get_by_role('button', name='BEGIN INVESTIGATION', exact=True).click()
    page.evaluate('nextIntro();nextIntro();nextIntro()')
    ev = page.evaluate

    def ready():
        page.wait_for_function('WardWinter.roomViewRenderer()?.loaded&&!WardWinter.orbit.busy')

    def action(object_id):
        ready()
        f = ev('id=>WardScene.sites().find(f=>f.objects.some(o=>o[0]===id))', object_id)
        assert f, ('Missing authored object', object_id)
        if ev('S.roomView') != f.get('view', 'front'):
            page.get_by_role('button', name='Look right', exact=True).click()
            ready()
        page.locator('[data-fixture="' + f['id'] + '"]').click()
        choice = page.locator('button[onclick="wardSelectFinding(\'' + object_id + '\')"]')
        if choice.count():
            choice.click()
        page.locator('button[onclick="wardFixtureAction(\'' + object_id + '\')"]').click()

    assert not ev('has("Flashlight")')
    action('coat')
    assert ev('has("Flashlight")&&S.ob.coat==="done"')
    assert not page.locator('[data-collectible="coat"]').count()
    ev('wardCloseFocus()')
    checks.append('intro leaves hands empty; coat pickup grants and removes the actual flashlight')

    # Simulate a previously saved inventory using the old item name. Loading is
    # the production migration entry point; the next save must use a new disk.
    ev('''const old=structuredClone(S);old.inv=[{n:"Flashlight",c:1},{n:"Ink Ribbon",c:2}];old.box=[{n:"Ink Ribbon",c:1}];localStorage.setItem(K,JSON.stringify(old));loadGame();''')
    assert ev('cnt("Floppy Disk")===2&&cnt("Ink Ribbon")===2&&S.box[0].n==="Floppy Disk"&&S.box[0].c===1')
    ev('saveGame()')
    assert page.get_by_role('heading', name='Terminal', exact=True).is_visible()
    assert 'Floppy Disk' in page.locator('#m').inner_text() and 'Ink Ribbon' not in page.locator('#m').inner_text()
    page.get_by_role('button', name='Save record', exact=True).click()
    ev('loadGame()')
    assert ev('cnt("Floppy Disk")===1&&S.box[0].c===1&&S.saves===1')
    assert ev('JSON.parse(localStorage.getItem(K)).inv.every(s=>s.n!=="Ink Ribbon")')
    checks.append('legacy ribbons migrate to stackable Floppy Disks; an actual Terminal save consumes exactly one disk')

    assert ev('Object.values(WardScenes).every(bp=>bp.fixtures.every(f=>!/[Nn]urse/.test(f.actor||"")))')
    assert ev('WardWinter.find("shawHandover")[4].doc==="Evelyn Shaw’s handover"&&WardWinter.find("judithRecord")[4].doc==="Judith Price’s medication record"')
    ev('infectedDoctor("ward")')
    assert not page.locator('#m .md').count()
    assert not ev('Object.values(R).flatMap(r=>r.o).some(o=>["shaw","judith"].includes(o[4].act))')
    assert ev('!/(?:DDMM|DAY then MONTH|Enter four digits)/i.test(docText("Memorial Ledger"))')
    assert ev('!/(?:archive|dedication date)/i.test(docText("Chaplain Letter"))')
    checks.append('nurses exist as evidence; invisible doctor pop-ups and solved-chapel instruction text are retired')

    ev('S.room="wardnorth";S.prev="ward";S.roomViewRoom=null;S.f.power=1;S.enemyActors.forEach(a=>a.hp=0);WardWinter.enemies.project();S.pursuer.active=false;render()')
    assert not ev('availableRoomObjects().some(o=>o[0]==="purgeSupplies")')
    action('windowLever')
    page.get_by_role('button', name='Pull the handle', exact=True).click()
    for i in range(3):
        action('coldWindow' + str(i))
    ev('wardCloseFocus()')
    assert ev('S.windows.resolved&&availableRoomObjects().some(o=>o[0]==="purgeSupplies")')
    before = ev('({ammo:cnt("Handgun Ammo"),battery:cnt("Battery")})')
    expected = ev('WardWinter.find("purgeSupplies")[4].give')
    action('purgeSupplies')
    assert ev('S.ob.purgeSupplies==="done"')
    assert ev('cnt("Handgun Ammo")') == before['ammo'] + expected[0][1]
    assert ev('cnt("Battery")') == before['battery'] + 1
    snapshot = ev('JSON.stringify(S.windows)')
    ev('wardOpenWindows();act("purgeSupplies")')
    assert ev('JSON.stringify(S.windows)') == snapshot
    assert ev('cnt("Battery")') == before['battery'] + 1
    checks.append('optional purge supplies unlock only after all catches close and cannot be farmed or reopened')

    ev('S.room="lobby";S.bat=0;S.f.lastDynamo=S.t-60;S.f.power=0;S.f.powerOut=0')
    assert ev('WardWinter.chargerStatus("emergencyDynamo").available')
    ev('act("emergencyDynamo")')
    assert ev('S.bat===12&&!WardWinter.chargerStatus("emergencyDynamo").available')
    ev('S.room="generator";S.f.power=1;S.bat=0;S.f.generatorChargeUses=2')
    assert ev('!WardWinter.chargerStatus("charger").available&&WardWinter.chargerStatus("charger").label.includes("empty")')
    assert ev('Object.values(R).flatMap(r=>r.o).filter(o=>o[4].act==="box").length>=7')
    checks.append('emergency charger availability tracks reserve and cooldown; exhausted generator charger is marked empty; storage locations increased')
    assert not errors, errors
    browser.close()
(ROOT / 'tests/results/story_review.json').write_text(json.dumps({'checks': checks, 'javascript_errors': errors}, indent=2) + '\n')
for check in checks:
    print('PASS', check)
