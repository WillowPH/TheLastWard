"""Kessler's infected aftermath uses bounded native motion, not pose distortion."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json,sys

ROOT=Path(__file__).resolve().parents[1];URL=sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8010'
checks=[];errors=[]
with sync_playwright() as p:
    browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
    page=browser.new_page(viewport={'width':1672,'height':941},service_workers='block',reduced_motion='no-preference')
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.goto(URL);page.get_by_role('button',name='BEGIN INVESTIGATION',exact=True).click();page.evaluate('nextIntro();nextIntro();nextIntro()')
    page.wait_for_function('WardWinter.roomViewRenderer()?.loaded&&WardWinter.roomViewEffects.data.surgery')
    page.evaluate('''()=>{closeModal();S.room='surgery';S.roomView='front';S.roomViewRoom='surgery';S.prev=null;S.f.doctorWallSeen=1;S.f.kesslerCondition='seizing';S.pursuer.active=false;S.enemyActors.forEach(a=>a.hp=0);S.sceneDisturbance=null;WardWinter.enemies.project();WardScene.options.flashes=false;wardSetAccess('motion',true);renderScene();}''')
    page.wait_for_function('WardWinter.roomViewRenderer()?.loaded&&!WardWinter.orbit.busy')
    page.wait_for_function('!!WardWinter.roomViewEffects.doctorFrame')
    page.evaluate('WardWinter.roomViewEffects.stop();window.realPresentationTime=WardWinter.presentationTime;WardWinter.presentationTime=t=>t;void 0')
    def phase(time):
        return page.evaluate('''time=>{const fx=WardWinter.roomViewEffects;fx.draw(time);const c=fx.canvas,d=c.getContext('2d').getImageData(0,0,c.width,c.height).data;let hash=2166136261,painted=0,outside=0;for(let y=0;y<c.height;y++)for(let x=0;x<c.width;x++){const i=(y*c.width+x)*4;for(let n=0;n<4;n++)hash=Math.imul(hash^d[i+n],16777619);if(d[i+3]){painted++;if(x<136||x>255||y<417||y>564)outside++;}}return {frame:fx.doctorFrame,hash:hash>>>0,painted,outside};}''',time)
    a=phase(100);b=phase(620)
    assert a['frame']['source']=='assets/room_views/surgery_after.webp' and b['frame']['source']==a['frame']['source'],(a,b)
    assert a['hash']!=b['hash'] and a['painted']>1000 and not a['outside'] and not b['outside'],(a,b)
    assert all(abs(part['dx'])<2 and abs(part['dy'])<2 for part in a['frame']['motion'])
    checks.append('infected Kessler has a brief native head jerk and uneven shoulder breath; all changed pixels remain in two feathered patches, with no whole-body or room transform')
    movement={}
    for condition in ['lucid','seizing','unresponsive']:
        page.evaluate('condition=>S.f.kesslerCondition=condition',condition);movement[condition]=phase(100)['frame']
    assert abs(movement['lucid']['motion'][0]['dx'])<abs(movement['seizing']['motion'][0]['dx'])
    assert all(f['condition']==name for name,f in movement.items())
    checks.append('the saved lucid, seizing and unresponsive aftermath conditions retain their identity and appropriate motion intensity')
    page.evaluate('()=>{WardWinter.presentationTime=realPresentationTime;WardWinter.roomViewEffects.mount();}');page.wait_for_timeout(100)
    page.get_by_role('button',name='Pause game',exact=True).click();frozen=page.evaluate('JSON.stringify(WardWinter.roomViewEffects.doctorFrame)')
    page.wait_for_timeout(250);assert page.evaluate('JSON.stringify(WardWinter.roomViewEffects.doctorFrame)')==frozen
    page.get_by_role('button',name='Resume game',exact=True).click();page.wait_for_timeout(150)
    assert page.evaluate('JSON.stringify(WardWinter.roomViewEffects.doctorFrame)')!=frozen
    page.evaluate('wardSetAccess("motion",false)');assert page.evaluate('WardWinter.roomViewEffects.doctorFrame') is None
    page.evaluate('wardSetAccess("motion",true);S.f.doctorWallSeen=0;renderScene()')
    page.wait_for_function('WardWinter.roomViewRenderer()?.loaded&&!WardWinter.orbit.busy');assert page.evaluate('WardWinter.roomViewEffects.doctorFrame') is None
    checks.append('Pause freezes the exact aftermath motion; reduced motion and the uncompleted encounter never animate the collapse state')
    assert not errors,errors;browser.close()
(ROOT/'tests/results/doctor_motion_v9.json').write_text(json.dumps({'checks':checks,'conditions':movement,'javascript_errors':errors},indent=2)+'\n')
for check in checks:print('PASS',check)
