"""Committed patient choices, visible aftermath, saved history and bounded costs."""
from pathlib import Path
import json, sys
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
URL=sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8010'
checks=[];errors=[];outcomes=[];visuals={}
with sync_playwright() as p:
    browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
    q=browser.new_page(viewport={'width':1672,'height':941},service_workers='block',reduced_motion='reduce')
    q.set_default_timeout(8000);q.on('pageerror',lambda error:errors.append(str(error)))
    ev=q.evaluate
    def ready():q.wait_for_function('WardWinter.roomViewRenderer()?.loaded&&!WardWinter.orbit.busy')
    def fresh(mode='1'):
        q.goto(URL);q.locator('#diff').select_option(mode)
        q.get_by_role('button',name='BEGIN INVESTIGATION',exact=True).click()
        ev('nextIntro();nextIntro();nextIntro()')
        assert ev('!!WardWinter.patientOutcomes'),'The real index must load the outcome module'
        ev('S.enemyActors.forEach(a=>a.hp=0);WardWinter.enemies.project();S.pursuer.active=false;S.slots=12;S.f.blackoutCount=2;add("Flashlight");S.bat=100;S.lightOn=true;render()')
        ready()
    def room(name):
        ev('name=>{closeModal();wardCloseFocus();S.prev=S.room;S.room=name;S.roomView="front";S.roomViewRoom=name;S.sceneFocus=null;render()}',name);ready()
    def travel(destination):
        # The scenario begins at the bedside; all departures and returns below
        # use the authored doorway and real navigation/arrival wrappers.
        ev('destination=>{wardCloseFocus();const edge=WardNavigation.edge(S.room,destination);WardWinter.orbit.face(Object.entries(WardRoomViews[S.room].views).find(([view,data])=>data.doors[edge])[0]);}',destination)
        ready();q.locator('[data-destination="'+destination+'"]').click()
        q.wait_for_function('destination=>S.room===destination&&!WardWinter.travelling',arg=destination);ready()
    def patient():
        q.locator('[data-fixture="patient"]').click()
        q.locator('button[onclick="wardFixtureAction(\'beggingPatient\')"]').click()
    def snapshot():return ev('({choice:S.f.beggingPatientChoice,outcome:S.f.patientOutcome,sanity:S.san,hp:S.hp,history:S.f.patientHistory,method:S.f.patientMethod,injury:S.f.patientRestraintInjury})')
    def visual(state):
        ready()
        path=ev('WardWinter.roomViewAsset("isoward")')
        assert ('isoward_after' if state=='dead' else 'isoward_'+state) in path,path
        digest=ev('''()=>{const c=document.querySelector('.room-view-canvas'),x=c.getContext('2d'),p=x.getImageData(Math.floor(c.width*.48),Math.floor(c.height*.28),Math.floor(c.width*.34),Math.floor(c.height*.3)).data;let hash=2166136261;for(let i=0;i<p.length;i+=4){hash=Math.imul(hash^p[i],16777619);hash=Math.imul(hash^p[i+1],16777619);hash=Math.imul(hash^p[i+2],16777619);}return hash>>>0;}''')
        geometry=ev('({source:WardWinter.roomViewRenderer().sourceSize,frame:document.querySelector(".room-view-frame").getBoundingClientRect().toJSON(),patient:WardRoomViews.isoward.fixtures.patient.rect})')
        assert geometry['source']=={'width':1448,'height':1086},geometry
        visuals[state]={'loaded_asset':path,'rendered_patient_pixel_digest':digest,'geometry':geometry}
    def capture(state):
        ready();q.screenshot(path=str(ROOT/f'tests/results/mercer-v9-{state}.png'))
    def saved_reload():
        room('lobby');ev('add("Floppy Disk",2);render()')
        q.locator('button[onclick="saveMenu()"]').click()
        q.get_by_role('button',name='Save record',exact=True).click()
        q.get_by_role('button',name='Save record',exact=True).click()
        expected=snapshot()
        assert ev('S.saves===1&&cnt("Floppy Disk")===1')
        q.locator('button[onclick="saveMenu()"]').click()
        q.get_by_role('button',name='Load record',exact=True).click()
        ready();assert snapshot()==expected
        assert ev('S.docs.includes(WardWinter.patientOutcomes.patientTitle)&&docText(WardWinter.patientOutcomes.patientTitle).includes("Daniel")')
        room('isoward')
        if expected['outcome']=='contained':ev('wardPatientAftermath("secure")')
        else:ev('choosePatientFate("left");choosePatientFate("helped");choosePatientFate("killed");wardConfirmPatient("knife")')
        assert snapshot()==expected
        travel('wardnorth');travel('isoward')
        assert snapshot()==expected and not q.locator('#m .md').count()
        return expected
    def passed(label):checks.append(label);print('PASS',label,flush=True)

    fresh();room('isoward');ev('add("Trauma Dressing",2);render()');patient()
    q.get_by_role('button',name='Try to treat him',exact=True).click()
    assert ev('S.f.beggingPatientChoice==="helped"&&S.f.patientOutcome==="stabilized"&&cnt("Trauma Dressing")===1&&S.san===95')
    assert 'purge' in q.locator('#m').inner_text().lower()
    q.get_by_role('button',name='Step away',exact=True).click()
    visual('stabilized');capture('stabilized')
    assert not q.locator('[data-fixture="patient"]').count()
    before=snapshot();ev('choosePatientFate("killed");wardConfirmPatient("knife");advanceTime(80)')
    assert ev('S.f.patientOutcome==="stabilized"&&!S.f.patientDeteriorationSeen')
    saved=saved_reload();room('isoward')
    assert 'Clean dressings' in ev('R.isoward.d') and not ev('S.f.patientDeteriorationSeen')
    outcomes.append(saved);passed('actual treatment consumes one dressing, preserves a lucid stable patient, gives a practical warning, retires his target and survives a real Terminal save/load')

    fresh();room('isoward');patient();q.get_by_role('button',name='Leave him alive',exact=True).click()
    q.get_by_role('button',name='Step away',exact=True).click()
    deadline=ev('S.f.patientDeterioratesAt');assert ev('S.f.patientOutcome==="untreated"&&S.san===93')
    patient();q.get_by_role('button',name='Leave him alive',exact=True).click()
    assert ev('S.f.patientDeterioratesAt')==deadline
    q.get_by_role('button',name='Step away',exact=True).click();ev('add("Trauma Dressing");render()')
    patient();q.get_by_role('button',name='Try to treat him',exact=True).click()
    assert ev('S.f.patientOutcome==="stabilized"&&S.f.patientWasLeft&&S.f.patientHistory.length===3')
    passed('leaving starts one saved deterioration window; revisiting cannot reset it, and a dressing can still help before the infection takes his lucidity')

    for mode,injury in [('0.7',6),('1',9),('1.3',12)]:
        fresh(mode);room('isoward');patient();q.get_by_role('button',name='Leave him alive',exact=True).click();q.get_by_role('button',name='Step away',exact=True).click()
        travel('wardnorth');ev('advanceTime(20)');travel('isoward')
        assert ev('S.f.patientDeteriorationSeen&&S.f.patientOutcome==="transformed"&&S.san===87')
        assert 'no longer' in q.locator('#m').inner_text()
        if mode=='1':
            visual('transformed');q.get_by_role('button',name='Close',exact=True).click();capture('transformed');patient()
        hp=ev('S.hp');q.get_by_role('button',name='Secure the loose restraint · risk injury',exact=True).click()
        assert ev('S.f.patientOutcome==="contained"&&S.f.patientRestraintInjury')==injury
        assert ev('S.hp')==hp-injury
        q.get_by_role('button',name='Step away',exact=True).click()
        if mode=='1':visual('contained');capture('contained')
        before=snapshot();ev('wardPatientAftermath("secure")');travel('wardnorth');travel('isoward')
        assert snapshot()==before and not q.locator('#m .md').count()
        assert ev('S.enemyActors.filter(a=>!a.dormant&&a.hp>0).length===0')
        if mode=='1':outcomes.append(saved_reload())
    passed('three difficulties: real departure/return door clicks cause one visible deterioration and distinct sanity cost; securing the restraint has one bounded physical cost, creates no roaming enemy and cannot repeat on another real return or after save/load')

    fresh();room('isoward');patient();q.get_by_role('button',name='Leave him alive',exact=True).click();q.get_by_role('button',name='Step away',exact=True).click()
    travel('wardnorth');ev('advanceTime(20)');travel('isoward')
    hp=ev('S.hp');sanity=ev('S.san');q.get_by_role('button',name='Keep my distance',exact=True).click()
    assert ev('S.hp')==hp
    travel('wardnorth');travel('isoward');assert ev('S.san')==sanity and not q.locator('#m .md').count()
    passed('keeping distance is a real zero-injury option, with no hidden repeat damage or repeated deterioration event')

    for method in ['knife','firearm']:
        fresh();room('isoward');ev('add("Utility Knife");add("Handgun");S.eq="Handgun";S.ld.Handgun=4;render()');patient()
        q.get_by_role('button',name='End his suffering',exact=True).click()
        q.get_by_role('button',name='Use utility knife' if method=='knife' else 'Use loaded firearm',exact=True).click()
        assert ev('S.f.beggingPatientChoice==="killed"&&S.f.patientOutcome==="dead"')
        assert ev('S.ld.Handgun')==(4 if method=='knife' else 3)
        assert bool(ev('S.f.lastNoise'))==(method=='firearm')
        q.get_by_role('button',name='Step away',exact=True).click();ready()
        assert ev('WardWinter.roomViewAsset("isoward").includes("isoward_after")')
        if method=='knife':visual('dead');capture('dead')
        before=snapshot();ev('choosePatientFate("left");wardConfirmPatient("knife");advanceTime(25)')
        assert snapshot()==before and not q.locator('[data-fixture="patient"]').count()
        outcomes.append(saved_reload())
    passed('knife and firearm mercy have different ammunition/noise costs; both permanently cover the body, preserve the bedside chronology and reject later alive/kill replays after actual save/load')

    # A later mercy decision records the earlier abandonment instead of rewriting it.
    fresh();room('isoward');ev('add("Utility Knife");render()');patient()
    q.get_by_role('button',name='Leave him alive',exact=True).click();q.get_by_role('button',name='Step away',exact=True).click()
    travel('wardnorth');ev('advanceTime(20)');travel('isoward')
    q.get_by_role('button',name='End his suffering',exact=True).click();q.get_by_role('button',name='Use utility knife',exact=True).click()
    assert ev('S.f.beggingPatientChoice==="killed"&&S.f.patientWasLeft&&S.f.patientDeteriorationSeen&&S.f.patientHistory.length===3')
    passed('mercy after abandonment retains the earlier living decision and infection aftermath in chronological evidence')

    kessler=[]
    for choice,label,sanity,injury in [('speak','Call his name',14,0),('approach','Approach carefully · risk injury',12,6),('inspect','Watch from the doorway',16,0),('leave','Back away',8,0)]:
        fresh();room('surgery');ev('doctorAtWall()')
        q.get_by_role('button',name=label,exact=True).click()
        state=ev('({choice:S.f.kesslerResponse,condition:S.f.kesslerCondition,hp:S.hp,sanity:S.san,record:docText(WardWinter.patientOutcomes.kesslerTitle)})')
        assert state['choice']==choice and state['hp']==100-injury and state['sanity']==100-sanity
        assert ev('S.f.doctorWallSeen&&R.surgery.d.includes("Dark veins")')
        assert any(word in q.locator('#m').inner_text().lower() for word in ['spasm','convulsion','twitching','veins'])
        q.get_by_role('button',name='Step back',exact=True).click();before=ev('[S.hp,S.san,S.f.kesslerResponse,S.f.kesslerRecord]')
        if choice=='inspect':
            ready();q.screenshot(path=str(ROOT/'tests/results/kessler-v9-infected.png'))
        ev('wardFinishKessler("approach");doctorAtWall()');assert ev('[S.hp,S.san,S.f.kesslerResponse,S.f.kesslerRecord]')==before
        kessler.append(state)
    passed('Kessler choices have distinct saved evidence and sanity costs; only the warned approach risks injury, and every aftermath explicitly shows infected collapse rather than an unexplained sit-down')

    fresh();room('isoward');ev('add("Trauma Dressing");render()');patient()
    q.get_by_role('button',name='Pause game',exact=True).click();before=snapshot()
    ev('choosePatientFate("helped");wardConfirmPatient("knife");wardPatientAftermath("secure")')
    assert snapshot()==before and ev('has("Trauma Dressing")')
    q.get_by_role('button',name='Resume game',exact=True).click()
    passed('Pause blocks all new patient decision and follow-up mutations without closing the pending choice')
    assert len({v['loaded_asset'] for v in visuals.values()})==4
    assert len({v['rendered_patient_pixel_digest'] for v in visuals.values()})==4
    assert len({(v['geometry']['frame']['width'],v['geometry']['frame']['height']) for v in visuals.values()})==1
    assert len({tuple(v['geometry']['patient']) for v in visuals.values()})==1
    passed('stabilized, transformed, resecured and covered-dead outcomes load four distinct authored room images and visibly different rendered patient pixels')
    assert not errors,errors
    browser.close()
(ROOT/'tests/results/patient_outcomes_v9.json').write_text(json.dumps({'checks':checks,'outcomes':outcomes,'kessler':kessler,'visuals':visuals,'javascript_errors':errors},indent=2)+'\n')
