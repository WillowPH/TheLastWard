"""Visible fitted-room weather, environmental motion and stop/resume contracts."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json, sys

ROOT=Path(__file__).resolve().parents[1]
URL=sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8010'
checks=[]; errors=[]; samples=[]
with sync_playwright() as p:
    browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
    page=browser.new_page(viewport={'width':1672,'height':941},service_workers='block',reduced_motion='no-preference')
    page.on('pageerror',lambda error:errors.append(str(error)))
    page.goto(URL);page.get_by_role('button',name='BEGIN INVESTIGATION',exact=True).click()
    page.evaluate('nextIntro();nextIntro();nextIntro()')
    page.wait_for_function('WardWinter.roomViewRenderer()?.loaded&&!!WardWinter.roomViewEffects.data.lobby')
    page.evaluate('window.originalFlicker=WardWinter.flicker;WardWinter.flicker=()=>0;wardSetAccess("motion",true);WardScene.options.flashes=false')

    def room(name,view='front'):
        page.evaluate('''([name,view])=>{closeModal();wardCloseFocus();S.room=name;S.prev=null;S.roomView=view;S.roomViewRoom=name;S.sceneDisturbance=null;S.pursuer.active=false;S.enemyActors.forEach(a=>a.hp=0);S.f.power=1;S.f.powerOut=0;S.f.lobbyShutters=0;S.f.sprinklerTriggered=0;S.f.stoveLit=0;WardWinter.enemies.project();render();}''',[name,view])
        page.wait_for_function('WardWinter.roomViewRenderer()?.loaded&&!WardWinter.orbit.busy')
        page.evaluate('WardWinter.roomViewEffects.stop()')

    def digest(canvas='canvas'):
        return page.evaluate('''key=>{const c=key==='visible'?document.querySelector('.room-view-canvas'):WardWinter.roomViewEffects[key],d=c.getContext('2d').getImageData(0,0,c.width,c.height).data;let h=2166136261,painted=0;for(let i=0;i<d.length;i++){h=Math.imul(h^d[i],16777619);if(i%4===3&&d[i])painted++;}return {hash:h>>>0,painted,width:c.width,height:c.height};}''',canvas)

    # At each fitted size the moving flakes must change actual displayed pixels,
    # not merely exist in an invisible subpixel native overlay.
    exterior=[(r,v) for r,views in json.loads((ROOT/'data/room_view_effects.json').read_text()).items() for v,spec in views.items() if spec['glass']]
    assert len(exterior)==8
    for width,height in [(1672,941),(1000,800),(390,844)]:
        page.set_viewport_size({'width':width,'height':height})
        for name,view in exterior:
            room(name,view)
            page.evaluate('WardWinter.roomViewEffects.draw(1000)')
            before=digest('visible'); page.evaluate('WardWinter.roomViewEffects.draw(1700)');after=digest('visible')
            native=digest('snowCanvas')
            assert before['hash']!=after['hash'],(width,name,view,before,after)
            assert native['painted']>20,(width,name,view,native)
            samples.append({'width':width,'room':name,'view':view,'visible_changes':True,'snow_pixels':native['painted']})
    checks.append('all eight exterior views visibly animate in the fitted game canvas at desktop, tablet and mobile sizes')

    page.set_viewport_size({'width':1672,'height':941});room('lobby')
    page.evaluate('WardWinter.roomViewEffects.draw(1700)')
    main=page.evaluate('''()=>{const c=WardWinter.roomViewEffects.snowCanvas,d=c.getContext('2d').getImageData(0,0,c.width,c.height).data;let n=0;for(let y=Math.floor(c.height*.15);y<c.height*.29;y++)for(let x=0;x<c.width*.33;x++)if(d[(y*c.width+x)*4+3])n++;return n;}''')
    assert main>80,main
    checks.append('the unobstructed main Lobby panes receive visible snowfall as well as the high transoms')

    # Let the real RAF run, then use the actual left-menu Pause control.
    page.evaluate('WardWinter.roomViewEffects.mount()');page.wait_for_timeout(220);a=digest('snowCanvas')
    page.wait_for_timeout(350);b=digest('snowCanvas');assert a['hash']!=b['hash']
    page.get_by_role('button',name='Pause game',exact=True).click();frozen=digest();n=page.evaluate('WardWinter.roomViewEffects.frames')
    page.evaluate('WardWinter.roomViewEffects.draw(999999)');page.wait_for_timeout(250)
    assert digest()==frozen and page.evaluate('WardWinter.roomViewEffects.frames')==n
    page.get_by_role('button',name='Resume game',exact=True).click();page.wait_for_timeout(250)
    assert digest()['hash']!=frozen['hash']
    checks.append('real-time snow advances by itself; Pause freezes both RAF and incidental redraws, and Resume restarts it')

    page.evaluate('wardSetAccess("motion",false)');page.wait_for_timeout(90);still=digest();frames=page.evaluate('WardWinter.roomViewEffects.frames')
    page.wait_for_timeout(220);assert digest()==still and page.evaluate('WardWinter.roomViewEffects.frames')==frames
    page.emulate_media(reduced_motion='reduce');page.evaluate('WardScene.options.motion=true;WardScene.options.motionOverride=false;renderScene()')
    page.wait_for_timeout(120);frames=page.evaluate('WardWinter.roomViewEffects.frames');page.wait_for_timeout(220)
    assert page.evaluate('WardWinter.roomViewEffects.frames')==frames
    page.emulate_media(reduced_motion='no-preference');page.wait_for_timeout(220)
    assert page.evaluate('WardWinter.roomViewEffects.frames')>frames
    page.evaluate('wardSetAccess("motion",true)')
    checks.append('scene-animation Off and OS reduced motion give stable winter stills; changing the OS preference restarts a stopped animation without a room change')

    for face in ['front','rear']:
        room('lobby',face);page.evaluate('S.f.lobbyShutters=1;renderScene()')
        page.wait_for_function('WardWinter.roomViewRenderer()?.loaded&&!WardWinter.orbit.busy')
        page.evaluate('WardWinter.roomViewEffects.stop();WardWinter.roomViewEffects.draw(1700)')
        assert digest('snowCanvas')['painted']==0
        assert page.evaluate('WardWinter.roomViewEffects.weatherFrame') is None
    checks.append('both painted closed-shutter states remove exterior snowfall completely')

    # These generated plates cover only window openings. Distinct indoor image
    # pixels cannot change when the storm plate finishes loading.
    for name in ['room12','isolation']:
        room(name);page.evaluate('WardWinter.roomViewEffects.draw(1000)');page.wait_for_timeout(180)
        plate=page.evaluate('''async name=>{const f=WardWinter.roomViewEffects,s=f.data[name].front,im=new Image();im.src=WardWinter.asset(s.winterExterior.asset);await im.decode();f.stop();f.draw(1000);const c=f.canvas,d=c.getContext('2d').getImageData(0,0,c.width,c.height).data;let opening=new Path2D();for(const poly of s.winterExterior.masks){opening.moveTo(poly[0][0]/100*c.width,poly[0][1]/100*c.height);for(const [x,y]of poly.slice(1))opening.lineTo(x/100*c.width,y/100*c.height);opening.closePath();}const x=c.getContext('2d');let opaque=0,outside=0;for(let y=0;y<c.height;y++)for(let px=0;px<c.width;px++){const a=d[(y*c.width+px)*4+3];if(a>245){opaque++;if(![[.5,.5],[-1,0],[1,0],[0,-1],[0,1]].some(([dx,dy])=>x.isPointInPath(opening,px+dx,y+dy)))outside++;}}return {asset:s.winterExterior.asset,width:im.naturalWidth,height:im.naturalHeight,opaque,outside};}''',name)
        assert plate['width']==1448 and plate['height']==1086 and plate['opaque']>1500 and plate['outside']==0,plate
        page.screenshot(path=str(ROOT/f'tests/results/weather-v9-{name}.png'))
    checks.append('moon-free overcast winter plates load at native resolution and alter only authored window openings, leaving indoor room geometry untouched')

    # Control the presentation clock only for deterministic effect phase probes.
    page.evaluate('window.originalPresentationTime=WardWinter.presentationTime;WardWinter.presentationTime=t=>t')
    room('eastcorridor');page.evaluate('S.f.sprinklerTriggered=1;S.f.sprinklerStopped=0;WardWinter.roomViewEffects.draw(1000)');a=digest()
    page.evaluate('WardWinter.roomViewEffects.draw(1600)');b=digest();assert a['hash']!=b['hash'] and a['painted']>100
    page.evaluate('S.f.sprinklerStopped=1;WardWinter.roomViewEffects.draw(1600)');assert digest()['painted']==0
    checks.append('sprinkler jets visibly move while active and clear immediately when the real stopped state is set')
    room('laundry','rear');page.evaluate('S.f.stoveLit=1;WardWinter.roomViewEffects.draw(1000)');a=digest()
    page.evaluate('WardWinter.roomViewEffects.draw(1700)');b=digest();assert a['hash']!=b['hash'] and a['painted']>100
    checks.append('the lit physical stove animates its firebox instead of an unrelated full-room tint')

    room('security');page.evaluate('WardWinter.roomViewEffects.draw(1000)');page.wait_for_timeout(220);page.evaluate('WardWinter.roomViewEffects.stop();WardWinter.roomViewEffects.draw(1000)');a=digest('screenCanvas')
    page.evaluate('WardWinter.roomViewEffects.draw(1700)');b=digest('screenCanvas');assert a['hash']!=b['hash'] and a['painted']>100
    checks.append('security CRT feeds retain moving static/scan effects in their dedicated screen compositor')

    room('lobby');page.evaluate('()=>{WardScene.options.flashes=true;WardWinter.flicker=originalFlicker;}')
    flicker=page.evaluate('''()=>{const f=WardWinter.roomViewEffects,h=hashSeed(S.room),period=16+h%7,t=(period-h%13+.1)%period;f.draw((t+.8)*1000);const c=document.querySelector('.room-view-canvas'),x=Math.round(c.width*.5),y=Math.round(c.height*.4),ctx=c.getContext('2d'),normal=Array.from(ctx.getImageData(x,y,1,1).data).slice(0,3);f.draw(t*1000);const dip=Array.from(ctx.getImageData(x,y,1,1).data).slice(0,3);return {normal,dip};}''')
    assert sum(flicker['dip'])<sum(flicker['normal'])*.7,flicker
    page.evaluate('WardScene.options.flashes=false');page.evaluate('WardWinter.roomViewEffects.draw(1000)');a=digest('visible');page.evaluate('WardWinter.roomViewEffects.draw(1800)')
    assert digest('visible')['hash']!=a['hash']
    checks.append('occasional interior light dips reach rendered pixels, and disabling flashes still permits exterior snow motion')
    assert not errors,errors
    browser.close()

(ROOT/'tests/results/weather_v9.json').write_text(json.dumps({'checks':checks,'fitted_views':samples,'javascript_errors':errors},indent=2)+'\n')
for check in checks:print('PASS',check)
