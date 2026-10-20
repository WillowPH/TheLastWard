"""Discard lifecycle, confirmation, capacity, save persistence and practical Thoughts."""
from pathlib import Path
import json
import sys
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
URL = sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:8010'
checks = []
errors = []

def passed(label):
    checks.append(label)
    print('PASS', label, flush=True)

with sync_playwright() as p:
    browser = p.chromium.launch(executable_path='/usr/bin/chromium', args=['--no-sandbox', '--enable-unsafe-swiftshader'])
    context = browser.new_context(service_workers='block', viewport={'width':1672, 'height':941})
    page = context.new_page()
    page.on('pageerror', lambda error: errors.append(str(error)))
    page.goto(URL)
    if not page.evaluate('!!WardWinter.inventoryDiscard'):
        page.add_script_tag(url=URL.rstrip('/')+'/js/inventory_discard.js')
    # Normal now retires spent progression tools automatically. This suite
    # verifies the explicitly manual Nightmare lifecycle and confirmations.
    page.locator('#diff').select_option('1.3')
    page.get_by_role('button', name='BEGIN INVESTIGATION', exact=True).click()
    page.evaluate('nextIntro();nextIntro();nextIntro()')
    page.wait_for_function('WardWinter.roomViewRenderer()?.loaded')
    ev = page.evaluate
    protected = ['Flashlight', 'Cabinet Key', 'Staff Access Card', 'Archive Key', 'Boiler Key', 'Bolt Cutters', 'Crank Handle', 'Maintenance Tools', 'Encrypted Drive', 'Power Fuse', 'Photographic Negative', 'Developing Fluid', 'Developed Photograph', 'Lighter', 'Lighter Fluid'] + ev('WardWinter.fuses')
    assert ev('names=>names.every(n=>!WardWinter.inventoryDiscard.policy(n).allowed)', protected)
    assert not ev('WardWinter.inventoryDiscard.policy("Unrecognized evidence").allowed')
    passed('all initial access items, evidence, elevator plugs, first lighter refill and unknown equipment are protected')

    ev('S.dr.ew=1')
    assert not ev('WardWinter.inventoryDiscard.policy("Staff Access Card").allowed')
    ev('S.dr.wr=1')
    assert ev('WardWinter.inventoryDiscard.policy("Staff Access Card").spent')
    ev('S.ob.nightPistol="done"')
    assert not ev('WardWinter.inventoryDiscard.policy("Cabinet Key").allowed')
    ev('S.ob.cab="done";S.dr.wa=1;S.dr.mb=1;S.dr.gm=1')
    for name in ['Cabinet Key', 'Archive Key', 'Boiler Key', 'Bolt Cutters']:
        assert ev('n=>WardWinter.inventoryDiscard.policy(n).spent', name), name
    ev('S.dr.mt=1')
    assert not ev('WardWinter.inventoryDiscard.policy("Crank Handle").allowed')
    ev('S.ob.wnc="done";S.f.maintenancePrepared=1;S.dr.os=1')
    assert ev('WardWinter.inventoryDiscard.policy("Crank Handle").spent')
    assert ev('WardWinter.inventoryDiscard.policy("Maintenance Tools").spent')
    assert not ev('WardWinter.inventoryDiscard.policy("Encrypted Drive").allowed')
    ev('S.f.finalSecurityClearance=1')
    assert ev('WardWinter.inventoryDiscard.policy("Encrypted Drive").spent')
    ev('S.f.stoveLit=1')
    assert not ev('WardWinter.inventoryDiscard.policy("Lighter").allowed')
    ev('S.f.chapelCandles=1')
    assert ev('WardWinter.inventoryDiscard.policy("Lighter").spent')
    passed('shared keys stay protected until every matching lock is open; tools and drive retain their additional task guards')

    ev('''S.inv=[{n:'Flashlight',c:1},{n:'Cabinet Key',c:1},{n:'Archive Key',c:1},{n:'Battery',c:2},{n:'Handgun Ammo',c:6},{n:'Floppy Disk',c:2},{n:'Utility Knife',c:1},{n:'Power Fuse',c:1}];S.slots=8;render()''')
    assert not ev('add("Trauma Dressing",1)')
    page.get_by_role('button', name='Manage carried items', exact=True).click()
    row = page.locator('#m .inventory-item-row').filter(has_text='Cabinet Key')
    assert 'Spent' in row.inner_text()
    row.get_by_role('button', name='Inspect / manage', exact=True).click()
    page.get_by_role('button', name='Discard', exact=True).click()
    page.get_by_role('button', name='Keep item', exact=True).click()
    assert ev('has("Cabinet Key")&&S.inv.length===8')
    page.get_by_role('button', name='Discard', exact=True).click()
    token = page.get_by_role('button', name='Discard permanently', exact=True).get_attribute('onclick')
    page.get_by_role('button', name='Discard permanently', exact=True).click()
    assert ev('!has("Cabinet Key")&&S.inv.length===7&&S.discardedItems.length===1')
    ev(token)
    assert ev('S.inv.length===7&&S.discardedItems.length===1')
    assert ev('add("Trauma Dressing",1)')
    assert ev('S.inv.length===8')
    passed('mouse-only Manage → Inspect → Discard requires confirmation; Keep cancels; one confirmed discard frees exactly one slot')

    ev('wardInspectInventory(S.inv.findIndex(s=>s.n==="Battery"))')
    page.get_by_role('button', name='Discard stack', exact=True).click()
    assert 'whole stack' in page.locator('#m').inner_text()
    stale = page.get_by_role('button', name='Discard permanently', exact=True).get_attribute('onclick')
    ev('closeModal()')
    ev(stale)
    assert ev('cnt("Battery")===2')
    ev('wardRequestDiscard(S.inv.findIndex(s=>s.n==="Battery"))')
    charge = ev('S.bat')
    page.get_by_role('button', name='Discard permanently', exact=True).click()
    assert ev('cnt("Battery")===0&&S.discardedItems.at(-1).c===2')
    assert ev('S.bat') == charge
    ev('wardRequestDiscard(S.inv.findIndex(s=>s.n==="Power Fuse"))')
    assert page.get_by_role('button', name='Discard permanently', exact=True).count() == 0
    assert ev('has("Power Fuse")')
    passed('supply stacks have an explicit permanent-loss warning; stale/closed confirmations and protected-item requests cannot remove items')

    ev('confirmSave()')
    # Both delivered save versions must preserve a used/discarded inventory.
    for version in ['last-ward-ch1-survival-review-5', 'last-ward-ch1-chapter-review-6', 'last-ward-ch1-chapter-review-7']:
        ev('''version=>{const saved=JSON.parse(localStorage.getItem(K));
            saved.buildId=version;localStorage.setItem(K,JSON.stringify(saved));}''', version)
        page.reload()
        assert page.evaluate('!!WardWinter.inventoryDiscard'), 'Inventory module must load through the production index'
        ev('loadGame()')
        page.wait_for_function('WardWinter.roomViewRenderer()?.loaded')
        assert ev('S.buildId===WardChapter.BUILD')
        assert ev('!has("Cabinet Key")&&!has("Battery")&&S.discardedItems.length===2&&has("Power Fuse")')
        assert ev('S.inv.length===7')
    passed('discarded inventory and freed capacity persist through actual Terminal saves and all v5/v6/v7 reload migrations')

    ev('''S.room='wardnorth';S.prev='wardnorth';S.roomViewRoom=null;S.sceneFocus=null;S.f.power=0;S.lightOn=false;S.bat=60;S.enemyActors.forEach(a=>a.hp=0);WardWinter.enemies.project();S.pursuer.active=false;S.contextThought=null;$('m').innerHTML='';render()''')
    page.wait_for_function('WardWinter.roomViewRenderer()?.loaded&&!WardWinter.orbit.busy')
    caption = page.locator('#captionText').get_attribute('data-full-text')
    ev('wardInspectFixture("notice")')
    assert 'flashlight' in page.locator('#thoughtCaptionText').inner_text().lower()
    assert page.locator('#captionText').get_attribute('data-full-text') == caption
    assert page.locator('#m .md').count() == 0
    assert ev('S.sceneFocus===null')
    assert page.locator('[data-fixture=notice]').count() == 1
    ev('render()')
    assert 'flashlight' in page.locator('#thoughtCaptionText').inner_text().lower()
    page.get_by_role('button', name='Toggle flashlight', exact=True).click()
    assert ev('S.lightOn&&!S.contextThought')
    ev('wardInspectFixture("notice")')
    assert ev('S.sceneFocus==="notice"')
    passed('a dark search writes its hint to Thoughts without a modal or narration replacement; its target remains usable after lighting')

    ev('wardCloseFocus();S.lightOn=false;S.bat=0;render();toggleLight()')
    assert 'charge' in page.locator('#thoughtCaptionText').inner_text().lower()
    assert page.locator('#t').inner_text() == ''
    assert page.locator('#m .md').count() == 0
    ev('S.room="security";S.roomViewRoom=null;render()')
    assert ev('!S.contextThought')
    ev('S.room="generator";S.roomViewRoom=null;render();rechargeAtGenerator()')
    assert ev('S.contextThought?.requirement==="power"')
    assert 'generator' in page.locator('#thoughtCaptionText').inner_text().lower()
    ev('S.f.power=1;render()')
    assert ev('!S.contextThought')
    ev('interaction("The drawer is empty.")')
    assert 'The drawer is empty.' in page.locator('#captionText').inner_text()
    passed('empty battery and unpowered charger feedback use Thoughts and clear when resolved; ordinary observations retain narration')

    ev('''S.room='wardservice';S.prev=S.room;S.roomViewRoom=null;delete S.dr.wa;rem('Archive Key',cnt('Archive Key'));$('m').innerHTML='';render();go('archive')''')
    assert ev('S.room==="wardservice"&&S.msg===null')
    assert page.locator('#m .md').count() == 0
    assert 'Archive Key' in page.locator('#thoughtCaptionText').inner_text()
    assert ev('wardDoorRequirement("wa")') == 'Requires Archive Key'
    ev('add("Archive Key");render()')
    assert ev('!S.contextThought')
    ev('''S.room='generator';S.prev=S.room;S.roomViewRoom=null;S.f.power=0;S.f.maintenancePrepared=0;S.lightOn=true;S.bat=70;render();act('regulator')''')
    assert ev('S.contextThought?.requirement==="item:Maintenance Tools"')
    assert page.locator('#m .md').count() == 0
    ev('add("Maintenance Tools");S.f.maintenancePrepared=1;render();act("pan")')
    assert ev('S.f.power&&!has("Power Fuse")')
    assert page.get_by_role('heading', name='Generator power restored', exact=True).count() == 1
    ev('closeModal()')
    passed('missing named keys/tools use Thoughts while door labels remain specific; successful generator restoration keeps its story scene')

    ev('rem("Floppy Disk",cnt("Floppy Disk"));saveGame()')
    assert ev('S.contextThought?.requirement==="item:Floppy Disk"')
    assert page.locator('#m .md').count() == 0
    ev('add("Floppy Disk");render();saveGame()')
    assert page.get_by_role('heading', name='Terminal', exact=True).count() == 1
    ev('closeModal()')
    passed('missing save supplies use Thoughts; acquiring them clears the hint and preserves the normal save confirmation')
    assert not errors, errors
    browser.close()

(ROOT/'tests/results').mkdir(exist_ok=True)
(ROOT/'tests/results/inventory_discard.json').write_text(json.dumps({'checks':checks,'javascript_errors':errors}, indent=2)+'\n')
