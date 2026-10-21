"""Rendered Subject X poses use independent anatomy and retain ground contact."""
from pathlib import Path
import json,sys
import hashlib
from PIL import Image
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
URL=sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8010'
checks=[];errors=[];samples=[]
bounds={}
for pose in ['standing','kneeling']:
    path=ROOT/f'assets/characters/subject_x_{pose}.webp'
    im=Image.open(path).convert('RGBA')
    box=im.getchannel('A').point(lambda a:255 if a>=200 else 0).getbbox()
    bounds[pose]={'size':im.size,'opaque':box,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
assert bounds['standing']['opaque'][1]<40
assert bounds['kneeling']['opaque'][1]>300
assert bounds['standing']['sha256']!=bounds['kneeling']['sha256']
with sync_playwright() as p:
    browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
    page=browser.new_page(viewport={'width':1672,'height':941},service_workers='block',reduced_motion='reduce')
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.goto(URL);page.get_by_role('button',name='BEGIN INVESTIGATION',exact=True).click()
    page.evaluate('nextIntro();nextIntro();nextIntro()')
    ev=page.evaluate
    def ready():
        page.wait_for_function('WardWinter.roomViewRenderer()?.loaded&&!WardWinter.orbit.busy')
        page.wait_for_function('(()=>{const i=document.querySelector(".winter-actor.subject-x [data-solid-source]");return i?.complete&&i.naturalWidth>0;})()')
    def stage():
        ev('''()=>{S.room='wardnorth';S.prev='ward';S.roomView='front';S.roomViewRoom='wardnorth';
            S.enemyActors.forEach(a=>a.hp=0);WardWinter.enemies.project();
            S.hp=100;S.f.dead=0;S.f.power=1;S.f.powerOut=0;S.f.blackoutCount=2;
            S.f.wet=0;S.f.coldExposure=0;S.f.hidingRoom=null;S.hallCombat=null;
            S.sceneDisturbance=null;S.sceneFocus=null;S.f.pursuerEncounter=0;
            S.pursuer={active:true,room:S.room,cooldown:0,lastMoveAt:S.t};
            if(!has('Handgun'))add('Handgun',1);S.eq='Handgun';S.ld.Handgun=6;
            $('m').innerHTML='';render();}''');ready()
    def sample(pose):
        value=ev('''()=>{const a=document.querySelector('.winter-actor.subject-x'),
            body=a.querySelector('img'),f=document.querySelector('.room-view-frame'),
            r=a.getBoundingClientRect(),frame=f.getBoundingClientRect(),style=getComputedStyle(a);
            return {pose:a.dataset.pose,source:body.dataset.solidSource,rect:r.toJSON(),
                frame:frame.toJSON(),fit:getComputedStyle(body).objectFit,
                transform:style.transform,opacity:style.opacity};}''')
        sw,sh=bounds[pose]['size'];x0,y0,x1,y1=bounds[pose]['opaque'];r=value['rect'];f=value['frame']
        scale=min(r['width']/sw,r['height']/sh)
        top=r['top']+(r['height']-sh*scale)/2+y0*scale
        bottom=top+(y1-y0)*scale
        value['body_height']=(bottom-top)/f['height']
        value['body_foot']=(bottom-f['top'])/f['height']
        assert value['pose']==pose and value['source'].endswith(f'subject_x_{pose}.webp'),value
        assert value['fit']=='contain' and value['opacity']=='1',value
        assert abs(r['width']/r['height']-2/3)<.003,value
        assert .95<=value['body_foot']<=.995,value
        assert value['transform'].startswith('matrix(1, 0, 0, 1,'),value
        samples.append(value);return value
    stage();upright=sample('standing')
    assert upright['body_height']>=.84
    page.screenshot(path=str(ROOT/'tests/results/subject-x-v9-standing.png'))
    ev('pursuerEncounter()')
    for _ in range(3):page.get_by_role('button',name='Shoot Subject X',exact=True).click()
    ready();assert ev('WardWinter.pursuerDown()')
    kneel=sample('kneeling')
    assert .58<=kneel['body_height']<=.66,kneel
    assert .65<kneel['body_height']/upright['body_height']<.75
    assert abs(kneel['rect']['height']/upright['rect']['height']-1)<.04
    assert not page.locator('.winter-actor.subject-x .winter-walk-sheet').count()
    checks.append('three real firearm clicks switch from an upright brute to a separately authored bent-knee pose, without rotating, compressing or stretching the standing art')
    checks.append('both opaque bodies keep their natural source proportions, consistent canvas scale and foreground boot/knee contact')
    page.screenshot(path=str(ROOT/'tests/results/subject-x-v9-kneeling.png'))
    page.get_by_role('button',name='Pause game',exact=True).click()
    deadline=ev('S.pursuer.staggerDeadline');page.wait_for_timeout(600)
    assert page.locator('.winter-actor.subject-x').get_attribute('data-pose')=='kneeling'
    page.get_by_role('button',name='Resume game',exact=True).click()
    assert ev('S.pursuer.staggerDeadline')>=deadline+400
    ev('S.pursuer.staggerUntil=S.t-1;S.pursuer.staggerDeadline=Date.now()-1;WardWinter.updatePursuerRecovery()')
    ready();recovered=sample('standing')
    assert abs(recovered['body_height']-upright['body_height'])<.002
    assert not ev('WardWinter.pursuerDown()')
    page.screenshot(path=str(ROOT/'tests/results/subject-x-v9-recovered.png'))
    checks.append('Pause preserves the kneeling deadline, and real recovery restores the full upright pose and its original height')
    for width,height in [(1000,800),(390,844)]:
        page.set_viewport_size({'width':width,'height':height});ready()
        sample('standing');ev('S.pursuer.staggerUntil=S.t+12;S.pursuer.staggerDeadline=Date.now()+30000;renderScene()');ready()
        sample('kneeling');ev('S.pursuer.staggerUntil=0;S.pursuer.staggerDeadline=0;renderScene()');ready()
    checks.append('upright and kneeling bodies remain grounded and undistorted at desktop, tablet and mobile widths')
    assert not errors,errors
    browser.close()
(ROOT/'tests/results/actor_poses_v9.json').write_text(json.dumps({'checks':checks,'bounds':bounds,'samples':samples,'javascript_errors':errors},indent=2)+'\n')
print('\n'.join('PASS '+v for v in checks))
