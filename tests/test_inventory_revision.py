"""Reported inventory regressions, exercised through the right HUD with mouse clicks."""
from pathlib import Path
import json
import sys
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
URL = sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:8010'
checks, errors = [], []

def passed(label):
    checks.append(label)
    print('PASS', label, flush=True)

with sync_playwright() as p:
    browser = p.chromium.launch(executable_path='/usr/bin/chromium', args=['--no-sandbox'])
    page = browser.new_page(viewport={'width':1672,'height':941}, service_workers='block')
    page.on('pageerror', lambda error: errors.append(str(error)))
    page.goto(URL)
    page.get_by_role('button', name='BEGIN INVESTIGATION', exact=True).click()
    ev = page.evaluate
    ev('''nextIntro();nextIntro();nextIntro();S.f.power=1;S.room='security';S.roomViewRoom=null;S.enemyActors.forEach(a=>a.hp=0);WardWinter.enemies.project();S.pursuer.active=false;render()''')
    page.wait_for_function('WardWinter.roomViewRenderer()?.loaded&&!WardWinter.orbit.busy')
    panel = page.locator('#inventoryCarryActions')

    def inventory(items, extra=''):
        ev("items=>{S.inv=items;S.slots=8;S.f.dead=0;S.hp=100;S.f.chapter1Complete=0;cm=0;$('m').innerHTML='';render()}", items)
        if extra:
            ev(extra)

    def select(name, count=1):
        page.get_by_role('button', name='Select '+name+(f' × {count}' if count>1 else ''), exact=True).click()

    def combine(a, b, ac=1, bc=1):
        select(a, ac)
        panel.get_by_role('button', name='Combine', exact=True).click()
        page.get_by_role('button', name='Combine with '+b+(f' × {bc}' if bc>1 else ''), exact=True).click()

    inventory([{'n':'Battery','c':2},{'n':'Wire Spool','c':1},{'n':'Flashlight','c':1}])
    combine('Wire Spool','Battery',bc=2)
    assert ev('cnt("Battery")===1&&!has("Wire Spool")&&cnt("Reinforced Battery")===1')
    assert page.locator('#m .md').count()==0
    assert panel.is_hidden()
    assert 'longer charge' in ev('S.contextThought.text')
    passed('Battery + Wire combines from the right HUD, consumes one of each and returns to the scene without Manage or a dropdown')

    inventory([{'n':'Lighter','c':1},{'n':'Lighter Fluid','c':1}], 'S.lighterFuel=0')
    combine('Lighter','Lighter Fluid')
    assert ev('has("Lighter")&&!has("Lighter Fluid")&&WardWinter.fuel()===6')
    assert page.locator('#m .md').count()==0
    passed('Lighter + fluid refills the reusable lighter directly from the HUD')

    inventory([{'n':'Handgun','c':1},{'n':'Handgun Ammo','c':8}], 'S.ld.Handgun=0;S.eq="Handgun"')
    combine('Handgun','Handgun Ammo',bc=8)
    assert ev('S.ld.Handgun===Math.min(8,W.Handgun.mag)&&cnt("Handgun Ammo")===Math.max(0,8-W.Handgun.mag)')
    assert page.locator('#m .md').count()==0
    passed('Weapon + its ammunition loads the selected weapon without opening inventory')

    inventory([{'n':'Handgun','c':1},{'n':'Stabilizer Part','c':1}], 'S.up.Handgun=0;S.eq="Handgun"')
    combine('Stabilizer Part','Handgun')
    assert ev('S.up.Handgun===1&&!has("Stabilizer Part")')
    assert page.locator('#m .md').count()==0
    passed('A stabilizer can be applied to a selected firearm directly; the old inventory modal stays closed')

    inventory([{'n':'Battery','c':1},{'n':'Lighter Fluid','c':1}])
    before = ev('JSON.stringify(S.inv)')
    combine('Battery','Lighter Fluid')
    assert ev('JSON.stringify(S.inv)')==before
    assert ev('WardWinter.inventoryDirect.selection().combining')
    panel.get_by_role('button', name='Cancel combine', exact=True).click()
    assert panel.is_hidden()
    passed('An incompatible pair never consumes resources and has an explicit cancel action')

    full = [{'n':'Battery','c':2},{'n':'Wire Spool','c':2},{'n':'Flashlight','c':1},{'n':'Cabinet Key','c':1},{'n':'Archive Key','c':1},{'n':'Boiler Key','c':1},{'n':'Lighter','c':1},{'n':'Staff Access Card','c':1}]
    inventory(full)
    before = ev('JSON.stringify(S.inv)')
    combine('Wire Spool','Battery',ac=2,bc=2)
    assert ev('JSON.stringify(S.inv)')==before
    assert not ev('has("Reinforced Battery")')
    assert ev('S.contextThought.requirement')=='space'
    passed('A full pack rolls both ingredient counts back when neither stack frees an output slot')

    inventory([{'n':'Archive Key','c':1},{'n':'Flashlight','c':1}], 'for(const [id,d]of Object.entries(D))if(d.need==="Archive Key")delete S.dr[id]')
    select('Archive Key')
    assert panel.get_by_role('button', name='Discard', exact=True).count()==0
    ev('wardRequestDiscard(0)')
    assert page.get_by_role('button', name='Discard permanently', exact=True).count()==0
    ev('for(const [id,d]of Object.entries(D))if(d.need==="Archive Key")S.dr[id]=1;render()')
    select('Archive Key')
    assert 'Spent' in panel.inner_text()
    panel.get_by_role('button', name='Discard', exact=True).click()
    page.get_by_role('button', name='Discard permanently', exact=True).click()
    assert not ev('has("Archive Key")')
    assert page.locator('#m .md').count()==0
    assert panel.is_hidden()
    passed('A key remains protected while a matching lock is unfinished; discarding the spent key closes confirmation and stays in the room')

    inventory([{'n':'Field Medkit','c':1},{'n':'Battery','c':1},{'n':'Wire Spool','c':1},{'n':'Lighter','c':1},{'n':'Lighter Fluid','c':1}], 'S.hp=0;S.f.dead=1;S.bat=0;S.lighterFuel=0;render()')
    before = ev('JSON.stringify({hp:S.hp,inv:S.inv,bat:S.bat,fuel:S.lighterFuel})')
    ev('wardSelectInventory(0);wardUseManagedItem(0);useInventorySlot(0);wardCombineInventory(1,2);wardCombineInventory(3,4);wardRequestDiscard(0)')
    assert ev('JSON.stringify({hp:S.hp,inv:S.inv,bat:S.bat,fuel:S.lighterFuel})')==before
    assert page.get_by_role('button', name='Discard permanently', exact=True).count()==0
    ev('S.hp=30')
    ev('wardUseManagedItem(0);useInventorySlot(0);wardCombineInventory(1,2);wardRequestDiscard(0)')
    assert ev('S.hp===0&&S.f.dead&&cnt("Field Medkit")===1&&cnt("Battery")===1&&cnt("Wire Spool")===1')
    passed('Dead players cannot heal, recharge, craft, refill or discard through any inventory entrypoint, even if another caller changes HP')

    inventory([{'n':'Battery','c':1}], 'delete S.f.wireCombineExplained;add("Wire Spool");render()')
    page.wait_for_function('S.contextThought?.text.includes("reinforce a flashlight battery")')
    assert 'Combine' in page.locator('#thoughtCaptionText').get_attribute('data-full-text') if page.locator('#thoughtCaptionText').get_attribute('data-full-text') else 'Combine' in ev('S.contextThought.text')
    passed('First Wire Spool acquisition explains its battery use in Thoughts')

    inventory([{'n':'Battery','c':1},{'n':'Flashlight','c':1}], 'S.bat=0')
    select('Battery')
    panel.get_by_role('button', name='Recharge', exact=True).click()
    assert ev('S.bat>0&&!has("Battery")')
    assert page.locator('#m .md').count()==0
    passed('A direct Recharge action uses the selected supply and leaves the room visible')

    inventory([{'n':'Battery','c':1}], 'S.box=[]')
    for room,fixture in [('stafflounge','harness'),('pharmacy','returns'),('records','cabinet')]:
        ev('''([room,fixture])=>{S.room=room;S.prev=room;S.roomViewRoom=room;S.roomView=WardRoomViews[room].fixtures[fixture].view;S.sceneFocus=null;S.contextThought=null;S.f.power=1;for(const o of R[room].o)if(o[4].act!=='box')S.ob[o[0]]=o[4].doc?'read':'done';render()}''', [room,fixture])
        page.wait_for_function('WardWinter.roomViewRenderer()?.loaded&&!WardWinter.orbit.busy')
        assert not ev('R[S.room].safe')
        page.locator('[data-fixture='+fixture+']').click()
        page.locator('#sceneFocusOverlay').get_by_role('button',name='Interact',exact=True).click()
        assert page.get_by_role('heading',name='Storage box',exact=True).is_visible()
        if room=='stafflounge':
            page.get_by_role('button',name='Carrying (1/8)',exact=True).click()
            page.locator('.storage-card').filter(has_text='Battery').get_by_role('button',name='Store',exact=True).click()
            assert ev('!has("Battery")&&S.box.some(s=>s.n==="Battery")')
        elif room=='records':
            page.get_by_role('button',name='Stored (1/16)',exact=True).click()
            page.locator('.storage-card').filter(has_text='Battery').get_by_role('button',name='Take',exact=True).click()
            assert ev('has("Battery")&&S.box.length===0')
        ev('closeModal();wardCloseFocus()')
    passed('Three added painted Storage boxes open in non-safe rooms and share stored equipment across the route')

    inventory([{'n':'Lighter','c':1},{'n':'Lighter Fluid','c':1}])
    for width,height in [(1672,941),(1000,800),(390,844)]:
        page.set_viewport_size({'width':width,'height':height})
        select('Lighter')
        rect = panel.bounding_box()
        assert rect and rect['x']>=0 and rect['x']+rect['width']<=width+1, (width,rect)
        assert ev('document.querySelector("#inventoryCarryActions").scrollWidth<=document.querySelector("#inventoryCarryActions").clientWidth+1')
        panel.get_by_role('button', name='Cancel item selection', exact=True).click()
    passed('Selected item names and controls fit desktop, tablet and narrow mouse/touch HUD widths without icon/text overlap')

    assert not errors, errors
    browser.close()

(ROOT/'tests/results').mkdir(exist_ok=True)
(ROOT/'tests/results/inventory_revision.json').write_text(json.dumps({'checks':checks,'javascript_errors':errors},indent=2)+'\n')
