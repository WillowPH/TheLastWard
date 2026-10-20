"""Integrated surveillance, sprinkler recovery and living-patient regressions."""
from pathlib import Path
import json
import sys
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
URL = sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:8010'
checks, errors = [], []
with sync_playwright() as p:
    browser = p.chromium.launch(executable_path='/usr/bin/chromium', args=['--no-sandbox'])
    page = browser.new_page(viewport={'width': 1672, 'height': 941}, service_workers='block')
    page.on('pageerror', lambda error: errors.append(str(error)))
    page.goto(URL)
    page.get_by_role('button', name='BEGIN INVESTIGATION', exact=True).click()
    page.evaluate('nextIntro();nextIntro();nextIntro()')

    def ready():
        page.wait_for_function('WardWinter.roomViewRenderer()?.loaded&&!WardWinter.orbit.busy')

    def room(name, view='front'):
        page.evaluate('''([name,view])=>{closeModal();wardCloseFocus();S.room=name;S.prev=null;S.roomView=view;S.roomViewRoom=name;S.sceneDisturbance=null;S.pursuer.active=false;S.enemyActors.forEach(a=>a.hp=0);WardWinter.enemies.project();render();}''', [name, view])
        ready()
        page.wait_for_function('WardWinter.roomViewEffects.data.security?.front?.screens.length===6')

    ready()
    # Six different real source images must make it all the way into the game
    # canvas. Bright noise alone cannot pass this correlation check.
    room('security')
    page.evaluate('WardScene.options.flashes=false;WardScene.options.motion=false;renderScene()')
    ready()
    page.wait_for_timeout(500)
    for power, outage in [(0, 0), (1, 0), (1, 1)]:
        page.evaluate('''([power,outage])=>{S.f.power=power;S.f.powerOut=outage;WardWinter.roomViewEffects.draw(0);}''', [power, outage])
        feeds = page.evaluate('''async()=>{
          const fx=WardWinter.roomViewEffects,c=fx.screenCanvas,ctx=c.getContext('2d'),out=[];
          for(const screen of fx.data.security.front.screens){
            const [cx,cy,rw,rh]=screen.rect,x=(cx-rw/2)*c.width/100,y=(cy-rh/2)*c.height/100,w=rw*c.width/100,h=rh*c.height/100;
            const image=new Image();image.src=WardWinter.asset(WardWinter.roomViewAsset(screen.feed,'front'));await image.decode();
            const ref=document.createElement('canvas');ref.width=c.width;ref.height=c.height;const rc=ref.getContext('2d');
            rc.filter='grayscale(1)';rc.drawImage(image,x,y,w,h);
            const actual=ctx.getImageData(0,0,c.width,c.height).data,expected=rc.getImageData(0,0,c.width,c.height).data,A=[],B=[];
            for(let py=Math.ceil(y+3);py<y+h*.75;py+=2)for(let px=Math.ceil(x+3);px<x+w-3;px+=2){const i=(py*c.width+px)*4;A.push(actual[i]);B.push(expected[i]);}
            const am=A.reduce((a,b)=>a+b)/A.length,bm=B.reduce((a,b)=>a+b)/B.length;
            let aa=0,bb=0,ab=0;for(let i=0;i<A.length;i++){const a=A[i]-am,b=B[i]-bm;aa+=a*a;bb+=b*b;ab+=a*b;}
            const game=document.querySelector('.room-view-canvas'),gc=game.getContext('2d'),at=gc.getImageData(Math.round(cx*game.width/100),Math.round(cy*game.height/100),1,1).data;
            out.push({feed:screen.feed,correlation:ab/Math.sqrt(aa*bb),mean:am,visible:at[0]+at[1]+at[2]});
          }return out;
        }''')
        assert len(feeds) == 6 and len({f['feed'] for f in feeds}) == 6, feeds
        assert all(f['correlation'] > .9 and f['mean'] > 35 and f['visible'] > 40 for f in feeds), feeds
    page.screenshot(path=str(ROOT / 'tests/results/effects-six-camera-feeds.png'))
    checks.append('all six distinct room feeds reach the visible CRTs on backup, generator power and temporary outage')
    assert page.evaluate('''()=>{S.f.lobbyShutters=1;const p=WardWinter.roomViewAsset('lobby','front');S.f.lobbyShutters=0;return p;}''') == 'assets/room_views/lobby_shutters_front.webp'
    checks.append('camera sources follow authored room-state artwork rather than stale base images')

    # Trigger and stop water through the same native fixture as a mouse player.
    room('eastcorridor')
    page.evaluate('S.f.sprinklerTriggered=0;S.f.sprinklerStopped=0;S.vis.room12=1;chapterArrival("ward","eastcorridor")')
    assert page.evaluate('S.f.sprinklerTriggered&&!S.f.sprinklerStopped&&S.f.wet')
    page.get_by_role('button', name='Reach for the shutoff', exact=True).click()
    page.locator('[data-fixture="valve"]').click()
    page.locator('button[onclick="wardFixtureAction(\'staffSprinkler\')"]').click()
    ready()
    page.evaluate('wardCloseFocus()')
    frost = page.evaluate('''()=>{const host=interactiveScene,frame=host.querySelector('.room-view-frame'),old=getComputedStyle(host,':after'),local=getComputedStyle(frame,':after');return {water:S.f.sprinklerStopped,wet:S.f.wet,shiver:S.f.shivering,oldContent:old.content,oldDisplay:old.display,shadow:local.boxShadow,focusHidden:sceneFocusOverlay.classList.contains('hid'),canvasFilter:getComputedStyle(host.querySelector('canvas')).filter};}''')
    assert frost['water'] and frost['wet'] and frost['shiver'], frost
    assert frost['oldContent'] == 'none' and frost['oldDisplay'] == 'none' and frost['focusHidden'] and frost['canvasFilter'] == 'none', frost
    assert '212, 212, 212' in frost['shadow'], frost
    page.screenshot(path=str(ROOT / 'tests/results/effects-water-stopped.png'))
    checks.append('real valve action stops rain, preserves wet/cold consequences, and leaves no full-scene green overlay')

    # A saved vision does not restart its fade on every render and cannot
    # compete with the scripted sprinkler incident.
    page.evaluate('S.roomView="rear";S.sceneDisturbance={room:S.room,kind:"hanged",deadline:Date.now()+7000};renderScene()')
    ready()
    delay = page.locator('[data-sanity-vision]').evaluate('(n)=>parseFloat(n.style.animationDelay)')
    assert delay < -7
    page.evaluate('S.f.sprinklerStopped=0;renderScene()')
    assert not page.locator('[data-sanity-vision]').count()
    page.evaluate('S.f.sprinklerStopped=1;S.sceneDisturbance=null;renderScene()')
    checks.append('sanity visions retain elapsed fade time and are suppressed during active sprinkler water')

    room('isoward')
    page.evaluate('S.f.beggingPatientChoice=null;WardScene.options.motion=true;renderScene()')
    ready()
    page.wait_for_timeout(200)
    before = page.evaluate('WardWinter.roomViewEffects.patientFrame')
    page.wait_for_timeout(450)
    after = page.evaluate('WardWinter.roomViewEffects.patientFrame')
    assert before and after and abs(before['rise'] - after['rise']) > .1, (before, after)
    bounded = page.evaluate('''()=>{const c=WardWinter.roomViewEffects.canvas,d=c.getContext('2d').getImageData(0,0,c.width,c.height).data;let pixels=0,outside=0;for(let y=0;y<c.height;y++)for(let x=0;x<c.width;x++)if(d[(y*c.width+x)*4+3]){pixels++;if(x<734||x>990||y<373||y>501)outside++;}return {pixels,outside};}''')
    assert bounded['pixels'] > 1000 and bounded['outside'] == 0, bounded
    page.get_by_role('button', name='Pause game', exact=True).click()
    frozen = page.evaluate('WardWinter.roomViewEffects.patientFrame')
    page.wait_for_timeout(300)
    assert page.evaluate('WardWinter.roomViewEffects.patientFrame') == frozen
    page.get_by_role('button', name='Resume game', exact=True).click()
    page.evaluate('WardScene.options.motion=false;renderScene()')
    ready()
    assert page.evaluate('WardWinter.roomViewEffects.patientFrame') is None
    page.evaluate('WardScene.options.motion=true;S.f.beggingPatientChoice="killed";renderScene()')
    ready()
    assert page.evaluate('WardWinter.roomViewEffects.patientFrame') is None
    assert page.evaluate('WardWinter.roomViewAsset("isoward","front")') == 'assets/states/isoward_after.webp'
    checks.append('Mercer breathes in a chest-only native patch; Pause, reduced motion and covered death stop it without moving the bed')
    assert not errors, errors
    browser.close()

(ROOT / 'tests/results/effects_review.json').write_text(json.dumps({'checks': checks, 'javascript_errors': errors}, indent=2) + '\n')
for check in checks:
    print('PASS', check)
