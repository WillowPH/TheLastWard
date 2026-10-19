"""Physical rear-container distribution and revised story art regressions."""
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
URL = sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:8010'
checks, errors = [], []
world = json.loads((ROOT / 'data/room_views.json').read_text())
assert world['eastcorridor']['defaultView'] == 'front'
assert 'ew' in world['eastcorridor']['views']['front']['doors']
assert world['isoward']['views']['front']['asset'] == 'assets/room_views/isoward_front.webp'
for view in ['front', 'rear']:
    # Closed shutters exclude the cold exterior reflection across the wet floor.
    # This examines the authored state, not just the particle mask.
    with Image.open(ROOT / f'assets/room_views/lobby_shutters_{view}.webp') as art:
        assert art.width >= 1400 and art.height >= 1000
        pixels = art.convert('RGB').crop((0, int(art.height * .6), art.width, art.height))
        cold = sum(b > r + 12 and b > g + 5 and b > 55 for r, g, b in pixels.get_flattened_data())
        assert cold / (pixels.width * pixels.height) < .002, (view, cold)
checks.append('both native closed-shutter paintings exclude bright blue exterior floor reflections')

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

    def room(name):
        ev('''r=>{closeModal();wardCloseFocus();S.room=r;S.prev=null;S.roomViewRoom=null;S.f.power=1;S.f.powerOut=0;S.enemyActors.forEach(a=>a.hp=0);WardWinter.enemies.project();S.pursuer.active=false;S.sceneDisturbance=null;render()}''', name)
        ready()
        if ev('WardNavigation.isDark(S.room)&&!lit()'):
            ev('toggleLight()')
            ready()

    def action(object_id):
        ready()
        f = ev('id=>WardScene.sites().find(f=>f.objects.some(o=>o[0]===id))', object_id)
        assert f, object_id
        if ev('S.roomView') != f.get('view', 'front'):
            page.get_by_role('button', name='Look right', exact=True).click()
            ready()
        target = page.locator('[data-fixture="' + f['id'] + '"]')
        target.click()
        selection = page.locator('button[onclick="wardSelectFinding(\'' + object_id + '\')"]')
        if selection.count():
            selection.click()
        page.locator('button[onclick="wardFixtureAction(\'' + object_id + '\')"]').click()

    action('coat')
    ev('wardCloseFocus()')
    # Reconfiguration is the real new-game/load path. Check many authored seeds
    # so none can put the four early pickups back into the front cabinet.
    for i in range(64):
        distribution = ev('''seed=>{configureWorld(seed,false);const f=id=>WardScenes.security.fixtures.find(f=>f.id===id);return {cabinet:f('cabinet').ids,drawer:f('drawer').ids,personal:f('personalEffects').ids,journal:f('diary').ids,records:WardScenes.records.fixtures.find(f=>f.id==='journal').ids};}''', 'containers-review-' + str(i))
        assert distribution['cabinet'] == ['rev', 'utilityKnife'], distribution
        assert set(distribution['personal']) == {'drw', 'petrolLighter'}, distribution
        assert distribution['drawer'] == ['lighterFluid'], distribution
        assert distribution['journal'] == ['attendantDiary1'], distribution
        assert distribution['records'] == ['finalJournal'], distribution
    checks.append('64 run seeds keep Security cabinet small and early equipment split across reachable rear furniture')

    room('security')
    for object_id, name in [('drw', 'Staff Access Card'), ('petrolLighter', 'Lighter'), ('lighterFluid', 'Lighter Fluid')]:
        action(object_id)
        assert ev('n=>has(n)', name)
        assert ev('S.roomView') == 'rear'
        ev('wardCloseFocus()')
    action('winterJournal')
    assert 'Heller' in page.locator('#m').inner_text()
    checks.append('real rear target clicks collect access card, lighter and fluid before the hazard and open Heller’s separate notice')

    for name, fixture, object_id, item in [
        ('children', 'nightDrawer', 'childNightCell', 'Battery'),
        ('isolation', 'dressingShelf', 'isolationDressing', 'Trauma Dressing'),
        ('coldstore', 'courierCrate', 'courierCell', 'Battery')
    ]:
        room(name)
        before = ev('n=>cnt(n)', item)
        expected = ev('id=>WardWinter.find(id)[4].give[0][1]', object_id)
        action(object_id)
        assert ev('S.roomView') == 'rear'
        assert ev('n=>cnt(n)', item) == before + expected
        assert ev('id=>S.ob[id]==="done"', object_id)
        ev('wardCloseFocus();renderScene()')
        ready()
        assert not page.locator('[data-fixture="' + fixture + '"]').count()
    checks.append('three sparse rooms have useful rear supplies in painted containers and lose their pickup targets after collection')

    assert ev('WardScenes.records.fixtures.find(f=>f.id==="researchBinder").ids.includes("mimiResearch")')
    assert ev('WardScenes.residence.fixtures.find(f=>f.id==="nightDesk").ids.includes("attendantDiary3")')
    assert ev('''Object.values(DOCS).filter(t=>/Recorded name: SISTER MIMI/.test(t)).length>=2''')
    assert ev('''!/(?:laughing|betray|stab|hunt)/i.test(DOCS['Nursing personnel amendment'])''')
    checks.append('Rourke’s journal has one record; other papers are physically scattered and Sister Mimi’s early introduction remains helpful')

    room('isoward')
    ev('S.roomView="front";renderScene()')
    ready()
    assert ev('WardWinter.roomViewRenderer().sourceSize.width>=1400')
    assert ev('WardWinter.roomViewAsset("isoward","front")') == 'assets/room_views/isoward_front.webp'
    ev('S.f.beggingPatientChoice="killed";renderScene()')
    ready()
    assert ev('document.querySelector(".room-view-frame").dataset.loading') == 'false'
    checks.append('infected conscious Mercer uses sharp native art while the irreversible covered-body state still loads')
    assert not errors, errors
    browser.close()

(ROOT / 'tests/results/scene_story_pass.json').write_text(json.dumps({'checks': checks, 'javascript_errors': errors}, indent=2) + '\n')
for check in checks:
    print('PASS', check)
