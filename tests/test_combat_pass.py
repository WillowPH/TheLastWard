"""Subject X travel gates, finite firearm knockdowns and distinct solid enemies."""
from pathlib import Path
import hashlib, json, sys
from playwright.sync_api import sync_playwright
ROOT = Path(__file__).resolve().parents[1]
URL = sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8010'
checks, errors = [], []
with sync_playwright() as p:
    browser = p.chromium.launch(executable_path='/usr/bin/chromium', args=['--no-sandbox'])
    context = browser.new_context(viewport={'width':1600,'height':1000},service_workers='block', reduced_motion='reduce')
    page=context.new_page(); page.set_default_timeout(7000)
    page.on('pageerror',lambda e:errors.append(str(e)))
    ev=page.evaluate
    def ready():
        page.wait_for_function('WardWinter.roomViewRenderer()?.loaded&&!WardWinter.orbit.busy')
    def fresh(mode='1'):
        page.goto(URL);page.locator('#diff').select_option(mode)
        page.get_by_role('button',name='BEGIN INVESTIGATION',exact=True).click()
        ev('nextIntro();nextIntro();nextIntro()');ready()
        assert ev('!!WardWinter.pursuerBlocksExit'), 'Combat pass must be included in index.html'
        ev("""S.enemyActors.forEach(a=>a.hp=0);WardWinter.enemies.project();
            S.slots=12;S.f.blackoutCount=2;S.f.power=1;S.room='eastcorridor';S.prev='security';
            S.roomView='front';S.roomViewRoom=S.room;S.f.sprinklerTriggered=1;
            S.f.sprinklerStopped=1;S.f.sprinklerResolved=1;S.f.windowBarricaded=1;
            S.f.wet=0;S.f.coldExposure=0;S.hp=100;S.lightOn=false;
            add('Staff Access Card',1);add('Handgun',1);add('Handgun Ammo',20);S.eq='Handgun';S.ld.Handgun=6;
            S.pursuer={active:true,room:S.room,cooldown:0,noise:0};S.f.pursuerStarted=1;
            S.f.pursuerEncounter=0;S.f.securityServiceRelease=1;S.dr.es=1;$('m').innerHTML='';render();""")
        ready()
    for command in ["go('ward')","go('ward',true)","sceneDoorTravel('ward')","mapTravel('ward')","flee()","sneak()"]:
        fresh();ev(command)
        assert ev('S.room')=='eastcorridor',command
        assert ev('!!S.f.pursuerEncounter'),command
        assert not ev('!!WardWinter.travelling'),command
        assert page.get_by_role('button',name='Shoot Subject X',exact=True).count()==1,command
    checks.append('door, confirmed movement, map, flee and sneak all stop before animation when Subject X blocks the room')
    fresh();ev("go('ward')")
    hp=ev('S.hp');ammo=ev('S.ld.Handgun')
    page.get_by_role('button',name='Shoot Subject X',exact=True).click()
    assert ev('S.ld.Handgun')==ammo-1
    assert ev('S.hp')<hp and not ev('WardWinter.pursuerDown()')
    page.get_by_role('button',name='Shoot Subject X',exact=True).click()
    assert ev('S.ld.Handgun')==ammo-2 and not ev('WardWinter.pursuerDown()')
    page.get_by_role('button',name='Shoot Subject X',exact=True).click()
    ready()
    assert ev('S.ld.Handgun')==ammo-3 and ev('WardWinter.pursuerDown()')
    assert ev('S.pursuer.active&&S.pursuer.room===S.room&&!S.f.pursuerEncounter')
    assert page.locator('.winter-actor.subject-x.knocked-down').count()==1
    ev("go('ward',true)")
    assert ev('S.room')=='ward'
    assert ev('S.f.pursuerEscapes>0&&S.f.pursuerChaseComplete')
    checks.append('three actual Normal handgun clicks spend three rounds, risk two close counters and knock Subject X down long enough to pass; it remains alive')
    fresh();ev("add('Shotgun',1);S.eq='Shotgun';S.ld.Shotgun=2;pursuerEncounter()")
    page.get_by_role('button',name='Shoot Subject X',exact=True).click();ready()
    assert ev('S.ld.Shotgun===1&&!WardWinter.pursuerDown()')
    page.get_by_role('button',name='Shoot Subject X',exact=True).click();ready()
    assert ev('S.ld.Shotgun===0&&WardWinter.pursuerDown()')
    ev('S.pursuer.staggerDeadline=Date.now()-1;WardWinter.updatePursuerRecovery()')
    assert not ev('WardWinter.pursuerDown()')
    ev("sceneDoorTravel('ward')")
    assert ev('S.room')=='eastcorridor' and ev('S.f.pursuerEncounter')
    checks.append('two Normal heavy shells stagger; the real recovery deadline expires and the same exits become blocked again')
    fresh();ev('pursuerEncounter()')
    page.get_by_role('button',name='Retreat through an unlocked door',exact=True).click();ready()
    assert ev('S.room')=='security' and ev('S.f.pursuerEscapes')==1
    fresh();ev("S.prev='ward';S.f.power=0;S.dr={};pursuerEncounter()")
    # If the back route is unavailable, choosing retreat never teleports elsewhere.
    ev("const edge=WardNavigation.edge(S.room,S.prev);window.__doorOpen=doorOpen;doorOpen=id=>id===edge?false:window.__doorOpen(id);escapePursuer('retreat')")
    assert ev('S.room')=='eastcorridor'
    assert 'way behind me is locked' in page.locator('#m').inner_text()
    checks.append('retreat uses the actual unlocked entry doorway and runs arrival once; a locked rear route cannot select an unrelated forward exit')
    fresh();ev('pursuerEncounter()')
    ev("window.__pauseFlag=true;const original=WardWinter.isPaused;WardWinter.isPaused=()=>window.__pauseFlag||!!original?.();void 0")
    state=ev('JSON.stringify({room:S.room,hp:S.hp,ld:S.ld,t:S.t,p:S.pursuer})')
    ev("shoot();reload();go('ward',true);escapePursuer('push');WardWinter.updatePursuerRecovery()")
    assert ev('JSON.stringify({room:S.room,hp:S.hp,ld:S.ld,t:S.t,p:S.pursuer})')==state
    ev('window.__pauseFlag=false')
    checks.append('pause blocks all combat and pursuer movement mutations')
    fresh();ev('S.pursuer.active=false')
    variants=[]
    for i in range(3):
        ev("""i=>{S.enemyActors.forEach(a=>a.hp=0);let a=S.enemyActors[0];
            Object.assign(a,{id:'infected-'+i,room:S.room,hp:20,maxHp:20,down:false,dormant:false});
            WardWinter.enemies.project();render();}""",i)
        ready();page.wait_for_timeout(100)
        variants.append(ev("({variant:document.querySelector('.winter-actor').className,art:document.querySelector('.winter-enemy-still')?.src||document.querySelector('.winter-walk-sheet')?.style.backgroundImage,opacity:getComputedStyle(document.querySelector('.winter-actor')).opacity})"))
    assert len({v['art'] for v in variants})==3,variants
    assert all(v['opacity']=='1' for v in variants),variants
    checks.append('three finite infected identities use three distinct art assets and retain full actor opacity')
    totals=[]
    for mode in ['0.7','1','1.3']:
        fresh(mode)
        ev("S.seed='combat-ammo-balance';configureWorld(S.seed,false)")
        totals.append(ev("""()=>{const sum=()=>Object.values(R).flatMap(r=>r.o).flatMap(o=>o[4].give||[]).filter(x=>x[0]==='Handgun Ammo').reduce((n,x)=>n+x[1],0);const a=sum();configureWorld(S.seed,true);configureWorld(S.seed,true);return [a,sum()]}"""))
    assert all(a==b for a,b in totals),totals
    assert totals[0][0]>totals[1][0]>totals[2][0],totals
    checks.append('finite authored ammo covers new stagger costs, scales by difficulty and never grows on reconfigure')
    assert not errors,errors
    browser.close()
(ROOT/'tests/results').mkdir(exist_ok=True)
# The assertions above compare actual rendered sources. Keep their identities in
# the report without embedding several megabytes of runtime-generated PNG data.
reported_variants=[{k:v for k,v in variant.items() if k!='art'} | {
    'art_source_sha256':hashlib.sha256(variant['art'].encode()).hexdigest(),
    'art_source_characters':len(variant['art'])
} for variant in variants]
(ROOT/'tests/results/combat_pass.json').write_text(json.dumps({'checks':checks,'ammo_totals':totals,'enemy_variants':reported_variants,'javascript_errors':errors},indent=2)+'\n')
for check in checks:print('PASS',check)
