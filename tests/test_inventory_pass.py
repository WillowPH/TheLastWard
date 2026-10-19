"""Mouse-only carry actions stay beside the selected slot, without scrolling."""
from pathlib import Path
import json
import sys
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
URL = sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:8010'
report = {'checks': [], 'javascript_errors': [], 'layouts': []}

with sync_playwright() as p:
    browser = p.chromium.launch(executable_path='/usr/bin/chromium', args=['--no-sandbox'])
    context = browser.new_context(service_workers='block', viewport={'width': 1672, 'height': 941})
    page = context.new_page()
    page.set_default_timeout(10000)
    page.on('pageerror', lambda error: report['javascript_errors'].append(str(error)))
    page.goto(URL)
    page.get_by_role('button', name='BEGIN INVESTIGATION', exact=True).click()
    page.evaluate('nextIntro();nextIntro();nextIntro()')
    page.wait_for_function('WardWinter.roomViewRenderer()?.loaded&&!WardWinter.orbit.busy')
    page.evaluate('''S.room='lobby';S.roomView='front';S.roomViewRoom=null;
        S.enemyActors.forEach(a=>a.hp=0);WardWinter.enemies.project();S.pursuer.active=false;
        S.f.pursuerEncounter=0;cm=0;$('m').innerHTML='';render()''')

    for width, height in [(1672, 941), (1000, 800), (390, 844)]:
        page.set_viewport_size({'width': width, 'height': height})
        page.evaluate('''S.inv=[{n:'Flashlight',c:1},{n:'Battery',c:3},{n:'Wire Spool',c:1},
            {n:'Handgun',c:1},{n:'Handgun Ammo',c:10},{n:'Trauma Dressing',c:1},
            {n:'Floppy Disk',c:2},{n:'Lighter',c:1}];S.hp=60;S.bat=10;S.ld.Handgun=0;
            S.eq='Handgun';S.slots=8;render()''')
        page.wait_for_timeout(120)
        battery = page.get_by_role('button', name='Select Battery × 3', exact=True)
        assert battery.locator('.inventory-quantity-badge').inner_text() == '×3'
        assert page.get_by_role('button', name='Select Handgun Ammo × 10', exact=True).locator('.inventory-quantity-badge').inner_text() == '10'
        assert page.get_by_role('button', name='Select Handgun', exact=True).locator('.inventory-quantity-badge').inner_text() == '0 / 10'
        before = page.locator('.right-rail').evaluate('n=>n.scrollTop')
        battery.click()
        panel = page.locator('#inventoryCarryActions')
        bounds = panel.evaluate('''n=>{const r=n.getBoundingClientRect();return {left:r.left,top:r.top,right:r.right,bottom:r.bottom,height:n.clientHeight,scrollHeight:n.scrollHeight,parent:n.parentElement.tagName}}''')
        assert bounds['parent'] == 'BODY', bounds
        assert bounds['left'] >= 0 and bounds['top'] >= 0 and bounds['right'] <= width and bounds['bottom'] <= height, bounds
        assert bounds['scrollHeight'] <= bounds['height'] + 1, bounds
        assert page.locator('.right-rail').evaluate('n=>n.scrollTop') == before
        assert page.locator('#m .md').count() == 0
        panel.get_by_role('button', name='Combine', exact=True).click()
        wire = page.get_by_role('button', name='Combine with Wire Spool', exact=True)
        assert 'combine-compatible' in wire.get_attribute('class')
        hits = page.locator('#inventorySlots .inventory-cell.filled').evaluate_all('''cells=>cells.map(cell=>{const r=cell.getBoundingClientRect(),hit=document.elementFromPoint(r.x+r.width/2,r.y+r.height/2);return {name:cell.getAttribute('aria-label'),y:r.y,bottom:r.bottom,hit:hit?.outerHTML.slice(0,140),clear:hit?.closest('.inventory-cell')===cell}})''')
        assert all(hit['clear'] for hit in hits), (width, hits)
        wire.click()
        assert page.evaluate('cnt("Battery")===2&&!has("Wire Spool")&&cnt("Reinforced Battery")===1')
        assert page.locator('#m .md').count() == 0
        assert not panel.is_visible()
        page.get_by_role('button', name='Select Reinforced Battery', exact=True).click()
        if width == 1000:
            panel.get_by_role('button', name='Combine', exact=True).click()
            page.get_by_role('button', name='Combine with Flashlight', exact=True).click()
        else:
            panel.get_by_role('button', name='Recharge', exact=True).click()
        assert page.evaluate('!has("Reinforced Battery")&&S.bat>70')
        assert page.locator('#m .md').count() == 0
        page.get_by_role('button', name='Select Trauma Dressing', exact=True).click()
        panel.get_by_role('button', name='Use', exact=True).click()
        assert page.evaluate('!has("Trauma Dressing")&&S.hp>60')
        assert page.locator('#m .md').count() == 0
        report['layouts'].append({'width': width, 'height': height, 'popover': bounds})
    report['checks'].append('At 1672, 1000 and 390 pixels: select, combine and use work through actual mouse clicks; actions remain in the viewport without scrolling or opening the inventory modal. Supply and ammo badges show exact counts.')

    # Reusing the shared access card is protected until both authored locks open.
    page.evaluate('''S.m=1;S.inv=[{n:'Staff Access Card',c:1},{n:'Lighter',c:1},
        {n:'Battery',c:2},{n:'Handgun',c:1}];delete S.dr.ew;delete S.dr.wr;render()''')
    assert page.evaluate('has("Staff Access Card")')
    page.evaluate('S.dr.ew=1;render()')
    assert page.evaluate('has("Staff Access Card")')
    page.evaluate('S.dr.wr=1;render()')
    assert page.evaluate('!has("Staff Access Card")&&has("Lighter")&&cnt("Battery")===2&&has("Handgun")&&S.discardedItems.at(-1).automatic')
    page.evaluate('S.m=1.3;S.inv.push({n:"Staff Access Card",c:1});render()')
    assert page.evaluate('has("Staff Access Card")&&WardWinter.inventoryDiscard.policy("Staff Access Card").spent')
    page.get_by_role('button', name='Select Staff Access Card', exact=True).click()
    page.locator('#inventoryCarryActions').get_by_role('button', name='Discard', exact=True).click()
    page.get_by_role('button', name='Discard permanently', exact=True).click()
    assert page.evaluate('!has("Staff Access Card")')
    assert page.locator('#m .md').count() == 0
    assert not page.locator('#inventoryCarryActions').is_visible()
    report['checks'].append('Normal automatically removes the access card only after both matching locks open, preserving useful supplies, lighter and weapon. Nightmare retains the spent card until confirmed manual discard; discard returns to the room.')

    # The pause contract is checked at the carry command boundary, not just by an overlay.
    page.evaluate('''window.inventoryPauseOriginal=WardWinter.isPaused;WardWinter.isPaused=()=>true;
        S.inv=[{n:'Battery',c:3},{n:'Wire Spool',c:1},{n:'Trauma Dressing',c:1}];S.bat=10;S.hp=40;
        window.inventoryPauseBefore=JSON.stringify({inv:S.inv,bat:S.bat,hp:S.hp});
        wardSelectInventory(0);wardCombineInventory(0,1);wardUseManagedItem(2);useInventorySlot(0);store(0);
        window.inventoryPauseAfter=JSON.stringify({inv:S.inv,bat:S.bat,hp:S.hp});
        WardWinter.isPaused=window.inventoryPauseOriginal;''')
    assert page.evaluate('inventoryPauseBefore===inventoryPauseAfter')
    report['checks'].append('Paused carry, combine, heal, recharge and storage commands do not mutate inventory, battery or condition.')
    assert not report['javascript_errors'], report['javascript_errors']
    browser.close()

(ROOT/'tests/results').mkdir(exist_ok=True)
(ROOT/'tests/results/inventory_pass.json').write_text(json.dumps(report, indent=2)+'\n')
for check in report['checks']:
    print('PASS', check)
