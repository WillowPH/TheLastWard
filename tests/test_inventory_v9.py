"""All-item room-local discard, real reclaim controls and two-purpose lighter fuel."""
from pathlib import Path
import json, sys
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
URL=sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8010'
report={'checks':[],'javascript_errors':[]}
with sync_playwright() as p:
    browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
    context=browser.new_context(service_workers='block',viewport={'width':1672,'height':941})
    page=context.new_page();page.set_default_timeout(7000)
    page.on('pageerror',lambda error:report['javascript_errors'].append(str(error)))
    page.goto(URL);page.locator('#diff').select_option('1.3')
    page.get_by_role('button',name='BEGIN INVESTIGATION',exact=True).click()
    page.evaluate('nextIntro();nextIntro();nextIntro()')
    ev=page.evaluate
    def ready():page.wait_for_function('WardWinter.roomViewRenderer()?.loaded&&!WardWinter.orbit.busy')
    def reset():
        ev('''S.room='lobby';S.prev='lobby';S.roomViewRoom=null;S.roomView='front';
            S.m=1.3;S.hp=100;S.f.dead=0;S.f.chapter1Complete=0;S.f.power=1;S.f.powerOut=0;
            S.enemyActors.forEach(a=>a.hp=0);WardWinter.enemies.project();S.pursuer.active=false;
            S.f.pursuerEncounter=0;cm=0;S.roomDrops=[];S.discardedItems=[];S.leftItemSerial=0;
            S.inv=[];S.box=[];S.slots=8;S.eq=null;S.ld.Handgun=0;S.contextThought=null;
            $('m').innerHTML='';render()''');ready()
    def leave(name):
        page.get_by_role('button',name='Select '+name,exact=True).click()
        page.locator('#inventoryCarryActions').get_by_role('button',name='Discard',exact=True).click()
        assert 'It stays in this room.' in page.locator('#m').inner_text()
        token=page.get_by_role('button',name='Leave item here',exact=True).get_attribute('onclick')
        page.get_by_role('button',name='Leave item here',exact=True).click()
        return token
    def left_items():page.locator('#leftItemsButton').click()
    reset()
    equipment=['Flashlight','Handgun','Utility Knife','Power Fuse','Archive Key','Crank Handle','Maintenance Tools','Encrypted Drive','Photographic Negative','Developing Fluid','Lighter','Lighter Fluid']+ev('WardWinter.fuses')
    assert ev('names=>names.every(n=>WardWinter.inventoryDiscard.policy(n).allowed)',equipment)
    ev("S.inv=[{n:'Archive Key',c:1},{n:'Flashlight',c:1}];render()")
    page.get_by_role('button',name='Select Archive Key',exact=True).click()
    page.locator('#inventoryCarryActions').get_by_role('button',name='Discard',exact=True).click()
    page.get_by_role('button',name='Keep item',exact=True).click()
    assert ev('has("Archive Key")&&S.roomDrops.length===0');ev('closeModal()')
    stale=leave('Archive Key');ev(stale)
    assert ev('!has("Archive Key")&&S.roomDrops.length===1&&S.box.length===0&&S.inv.length===1')
    assert page.locator('#m .md').count()==0
    report['checks'].append('every carried item is discardable, including unused progression items; confirmation/Keep/stale tokens are safe, capacity frees and the item remains local rather than entering shared Storage')

    drop_id=ev('S.roomDrops[0].id')
    ev("S.room='security';S.roomViewRoom=null;render()");ready()
    assert not page.locator('#leftItemsButton').is_visible()
    ev('id=>wardRecoverLeftItem(id)',drop_id)
    assert ev('!has("Archive Key")&&S.roomDrops.length===1')
    ev("S.room='lobby';S.roomViewRoom=null;render()");ready()
    ev("S.inv=[{n:'Flashlight',c:1},{n:'Battery',c:1},{n:'Wire Spool',c:1},{n:'Utility Knife',c:1},{n:'Lighter',c:1},{n:'Floppy Disk',c:1},{n:'Handgun',c:1},{n:'Trauma Dressing',c:1}];render()")
    left_items();page.locator('.left-item-card').get_by_role('button',name='Take',exact=True).click()
    assert 'no room' in page.locator('#leftItemsStatus').inner_text().lower()
    assert ev('!has("Archive Key")&&S.roomDrops.length===1')
    ev('closeModal();rem("Wire Spool");render()');left_items()
    page.locator('.left-item-card').get_by_role('button',name='Take',exact=True).click()
    ev('id=>wardRecoverLeftItem(id)',drop_id)
    assert ev('cnt("Archive Key")===1&&S.roomDrops.length===0&&S.inv.length===8')
    assert not page.locator('#leftItemsButton').is_visible()
    report['checks'].append('only the original room exposes reclaim; a full pack leaves the item untouched with visible feedback, and a real Take click recovers it exactly once')

    reset();ev("S.inv=[{n:'Handgun',c:1},{n:'Handgun Ammo',c:7},{n:'Floppy Disk',c:2}];S.eq='Handgun';S.ld.Handgun=4;render()")
    leave('Handgun')
    assert ev('!has("Handgun")&&S.eq===null&&S.ld.Handgun===0&&S.roomDrops[0].loaded===4&&cnt("Handgun Ammo")===7')
    ev('confirmSave()');snapshot=ev('localStorage.getItem(K)')
    ev('S.roomDrops=[];S.ld.Handgun=0;loadGame()');ready()
    assert ev('S.roomDrops.length===1&&S.roomDrops[0].loaded===4&&!has("Handgun")')
    left_items();page.locator('.left-item-card').get_by_role('button',name='Take',exact=True).click()
    assert ev('has("Handgun")&&S.eq==="Handgun"&&S.ld.Handgun===4&&cnt("Handgun Ammo")===7&&S.roomDrops.length===0')
    report['checks'].append('leaving an equipped weapon clears its equipped slot and magazine; its four loaded rounds persist with the left weapon through an actual Terminal save/load and return exactly once without adding reserve ammunition')

    reset();ev("S.room='wardnorth';S.roomViewRoom=null;S.f.power=0;S.inv=[{n:'Flashlight',c:1}];S.lightOn=true;S.bat=60;render()");ready()
    leave('Flashlight');charge=ev('S.bat');page.wait_for_timeout(1150)
    assert ev('!has("Flashlight")&&!S.lightOn') and ev('S.bat')==charge
    left_items();page.locator('.left-item-card').get_by_role('button',name='Take',exact=True).click()
    assert ev('has("Flashlight")&&!S.lightOn') and ev('S.bat')==charge
    report['checks'].append('leaving the flashlight switches it off and stops battery use; it can be recovered from the dark room without needing light to access its reclaim control')

    reset();ev("S.inv=[{n:'Lighter',c:1},{n:'Lighter Fluid',c:1}];S.f.stoveLit=0;S.f.chapelCandles=0;S.lighterFuel=0;delete S.ob.chapelCandles;render()")
    page.get_by_role('button',name='Select Lighter',exact=True).click()
    page.locator('#inventoryCarryActions').get_by_role('button',name='Combine',exact=True).click()
    page.get_by_role('button',name='Combine with Lighter Fluid',exact=True).click()
    assert ev('S.lighterFuel===2&&WardWinter.fuel()===2&&!has("Lighter Fluid")')
    assert page.get_by_role('button',name='Select Lighter',exact=True).locator('.inventory-quantity-badge').inner_text()=='2 / 2'
    ev("S.room='laundry';S.roomViewRoom=null;act('dryingStove')");ready()
    assert ev('S.f.stoveLit&&S.lighterFuel===1&&has("Lighter")')
    ev("act('dryingStove')");assert ev('S.lighterFuel===1')
    ev("S.room='chapel';S.roomViewRoom=null;act('chapelCandles')");ready()
    assert ev('S.f.chapelCandles&&S.lighterFuel===0&&has("Lighter")')
    ev("S.m=1;render()");assert ev('!has("Lighter")&&S.discardedItems.at(-1).automatic')
    report['checks'].append('one actual carry-grid combine prepares exactly two ignitions; stove and chapel each use one, repeated interaction uses none, and Normal retires the finished lighter while Nightmare had retained it')

    for first,second,fuel,expected in [(False,False,6,2),(True,False,5,1),(False,True,5,1),(True,True,4,0),(False,False,0,0)]:
        reset();ev('v=>{S.f.stoveLit=v[0];S.f.chapelCandles=v[1];S.lighterFuel=v[2];S.inv=[{n:"Lighter",c:1},{n:"Floppy Disk",c:2}];confirmSave();loadGame()}',[first,second,fuel]);ready()
        assert ev('S.lighterFuel')==expected,(first,second,fuel,ev('S.lighterFuel'))
    report['checks'].append('actual saved legacy fuel of six/five/four normalizes to two/one/zero from the real ignition flags on load, without refilling empty fuel or resetting completed ignitions')

    reset();ev("S.inv=[{n:'Power Fuse',c:1}];render()")
    page.get_by_role('button',name='Select Power Fuse',exact=True).click()
    page.locator('#inventoryCarryActions').get_by_role('button',name='Discard',exact=True).click()
    token=page.get_by_role('button',name='Leave item here',exact=True).get_attribute('onclick')
    page.locator('#wardPauseButton').click()
    before=ev('JSON.stringify({inv:S.inv,drops:S.roomDrops,eq:S.eq,fuel:S.lighterFuel})')
    ev(token);ev('wardRecoverLeftItem(1);wardCombineLighter()')
    assert ev('JSON.stringify({inv:S.inv,drops:S.roomDrops,eq:S.eq,fuel:S.lighterFuel})')==before
    page.get_by_role('button',name='Resume game',exact=True).click()
    page.get_by_role('button',name='Leave item here',exact=True).click()
    ev('S.hp=0;S.f.dead=1;render()')
    before=ev('JSON.stringify({inv:S.inv,drops:S.roomDrops,eq:S.eq,fuel:S.lighterFuel})')
    ev('wardRecoverLeftItem(1);wardLeftItems();wardCombineLighter()')
    assert ev('JSON.stringify({inv:S.inv,drops:S.roomDrops,eq:S.eq,fuel:S.lighterFuel})')==before
    report['checks'].append('actual Pause preserves discard confirmation and blocks leave/reclaim/refill; death also blocks all new item commands')

    reset();ev("S.roomDrops=Array.from({length:9},(_,i)=>({id:i+1,n:'Power Fuse',c:1,room:S.room,time:S.t}));render()")
    for width,height in [(1672,941),(1000,800),(390,844)]:
        page.set_viewport_size({'width':width,'height':height});ev('closeModal()');left_items()
        assert page.locator('.left-item-card').count()==4
        bounds=page.locator('#m .md').evaluate('n=>({h:n.clientHeight,scroll:n.scrollHeight,b:n.getBoundingClientRect().bottom,t:n.getBoundingClientRect().top})')
        assert bounds['scroll']<=bounds['h']+1 and bounds['t']>=0 and bounds['b']<=height,bounds
        assert page.locator('#m .mb').evaluate('n=>n.scrollHeight<=n.clientHeight+1')
        page.get_by_role('button',name='Next',exact=True).click()
        assert 'Page 2 / 3' in page.locator('#m').inner_text()
        page.get_by_role('button',name='Next',exact=True).click()
        assert page.locator('.left-item-card').count()==1
    report['checks'].append('room-local reclaim uses four readable item rows and real pagination at desktop, tablet and mobile sizes without nested modal scrolling')
    assert not report['javascript_errors'],report['javascript_errors']
    browser.close()
(ROOT/'tests/results/inventory_v9.json').write_text(json.dumps(report,indent=2)+'\n')
for check in report['checks']:print('PASS',check)
