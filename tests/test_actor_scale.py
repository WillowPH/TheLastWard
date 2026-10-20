"""Compare displayed opaque enemy bodies with the fitted room art, not CSS boxes."""
from pathlib import Path
import json, sys
from PIL import Image
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
URL=sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8010'
SOURCES={
    'orderly':('assets/room_views/infected_orderly.png',False),
    'nurse':('assets/characters/nurse_walk.webp',True),
    'patient':('assets/characters/patient_walk.webp',True),
    'subject-x':('assets/characters/subject_walk.webp',True),
}
bounds={}
for name,(src,sheet) in SOURCES.items():
    image=Image.open(ROOT/src).convert('RGBA')
    if sheet:image=image.crop((0,0,image.width//4,image.height))
    box=image.getchannel('A').point(lambda a:255 if a>=200 else 0).getbbox()
    bounds[name]={'source':[image.width,image.height],'opaque':box}
checks=[];samples=[];errors=[]
with sync_playwright() as p:
    browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
    context=browser.new_context(viewport={'width':1672,'height':941},service_workers='block',reduced_motion='reduce')
    page=context.new_page();page.on('pageerror',lambda error:errors.append(str(error)))
    page.goto(URL);page.get_by_role('button',name='BEGIN INVESTIGATION',exact=True).click()
    page.evaluate('nextIntro();nextIntro();nextIntro()')
    page.wait_for_function('WardWinter.roomViewRenderer()?.loaded&&!WardWinter.orbit.busy')
    rooms=page.evaluate('Object.keys(WardRoomViews)')
    def stage(room,variant):
        page.evaluate('''({room,variant})=>{
            S.enemyActors=S.enemyActors.slice(0,1);S.enemyActors.forEach(a=>a.hp=0);let a=S.enemyActors[0];
            Object.assign(a,{id:'infected-'+variant,room,hp:20,maxHp:20,down:false,dormant:false});
            WardWinter.enemies.project();S.room=room;S.prev=null;
            S.roomView='front';S.roomViewRoom=room;S.sceneFocus=null;S.f.hidingRoom=null;
            S.f.sprinklerResolved=1;S.f.sprinklerStopped=1;S.f.sprinklerTriggered=1;
            S.f.windowBarricaded=1;S.f.power=1;S.f.powerOut=0;S.lightOn=false;
            S.pursuer={active:variant===3,room,cooldown:0};S.f.pursuerEncounter=0;
            $('m').innerHTML='';render();
        }''',{'room':room,'variant':variant})
        page.wait_for_function('WardWinter.roomViewRenderer()?.loaded&&!WardWinter.orbit.busy')
        return page.evaluate('''()=>{
            const actor=document.querySelector('.winter-actor'),frame=document.querySelector('.room-view-frame');
            const a=actor.getBoundingClientRect(),f=frame.getBoundingClientRect();
            return {room:S.room,variant:[...actor.classList].find(x=>x.startsWith('enemy-')).slice(6),
                actor:a.toJSON(),frame:f.toJSON(),opacity:getComputedStyle(actor).opacity};
        }''')
    def visible(sample):
        # CSS object-fit:contain letterboxing matters: a 2:3 source in an old
        # .55 box passed box-size tests while shrinking the actual person.
        source=bounds[sample['variant']];sw,sh=source['source'];x0,y0,x1,y1=source['opaque']
        a=sample['actor'];f=sample['frame']
        scale=min(a['width']/sw,a['height']/sh)
        left=a['left']+(a['width']-sw*scale)/2+x0*scale
        top=a['top']+(a['height']-sh*scale)/2+y0*scale
        right=left+(x1-x0)*scale;bottom=top+(y1-y0)*scale
        return {'height':(bottom-top)/f['height'],'foot':(bottom-f['top'])/f['height'],
            'left':(left-f['left'])/f['width'],'right':(right-f['left'])/f['width'],
            'top':(top-f['top'])/f['height']}
    for room in rooms:
        for variant in range(4):
            sample=stage(room,variant);body=visible(sample);sample['visible']=body;samples.append(sample)
            minimum=.82 if variant==3 else .69
            assert body['height']>=minimum,(room,variant,'miniature opaque body',body)
            assert .94<=body['foot']<=.995,(room,variant,'boots off foreground floor',body)
            assert body['top']>=.035,(room,variant,'head clipped',body)
            assert -.025<=body['left'] and body['right']<=1.025,(room,variant,'body clipped',body)
            assert sample['opacity']=='1',(room,variant,'transparent enemy')
    checks.append('all 27 room paintings fit three infected bodies and larger Subject X at full opacity, with visible boots on the foreground floor and no clipped head/body')
    normal=[s for s in samples if s['variant']=='orderly'];large=[s for s in samples if s['variant']=='subject-x']
    assert all(b['visible']['height']>a['visible']['height']+0.09 for a,b in zip(normal,large))
    generator=next(s for s in normal if s['room']=='generator')
    foot_x=(generator['actor']['x']+generator['actor']['width']/2-generator['frame']['x'])/generator['frame']['width']
    assert foot_x>.79,'Generator actor must occupy the right aisle rather than the central engine base'
    checks.append('Subject X remains at least 9% of room height larger than infected; generator foreground anchor is in the right aisle')
    for size in [{'width':1000,'height':720},{'width':390,'height':844}]:
        page.set_viewport_size(size)
        for room in ['eastcorridor','generator','wardnorth']:
            for variant in [0,2,3]:
                sample=stage(room,variant);body=visible(sample)
                assert body['height']>=(.82 if variant==3 else .69),(size,sample)
                assert body['top']>=.035 and body['foot']<=.995,(size,sample)
    checks.append('visible scale and floor contact survive tablet and narrow mobile layouts')
    stage('tunnel',0)
    page.evaluate("add('Flashlight',1);S.lightOn=false;S.f.flashlightDropped=0;S.bat=90;renderScene()")
    dark_filter=page.locator('.winter-actor').evaluate('(actor)=>getComputedStyle(actor).filter')
    page.evaluate('S.lightOn=true;renderScene()')
    torch_filter=page.locator('.winter-actor').evaluate('(actor)=>getComputedStyle(actor).filter')
    assert 'brightness(0.22)' in dark_filter and 'brightness(0.68)' in torch_filter,(dark_filter,torch_filter)
    assert page.locator('.winter-actor').evaluate('(actor)=>getComputedStyle(actor).opacity')=='1'
    checks.append('unlit enemy art follows room darkness and flashlight availability without turning a real body translucent or self-lit')
    page.set_viewport_size({'width':1672,'height':941})
    for room,variant in [('eastcorridor',0),('generator',0),('wardnorth',3)]:
        stage(room,variant)
        page.screenshot(path=str(ROOT/'tests/results'/('actor_scale_'+room+'.png')))
    stage('eastcorridor',0)
    page.evaluate("add('Staff Access Card',1)")
    before=page.locator('.winter-actor').evaluate('''actor=>({left:actor.style.left,bottom:actor.style.bottom,
        height:actor.style.height,aspect:actor.style.aspectRatio,source:actor.querySelector('img')?.src,
        hp:S.hp,enemy:WardWinter.enemies.actorAt().hp})''')
    page.locator('.winter-actor-hit').click()
    page.get_by_role('button',name='Struggle · risk injury',exact=True).click()
    fallen=page.locator('.winter-falling-enemy')
    assert fallen.count()==1
    after=fallen.evaluate('''actor=>({left:actor.style.left,bottom:actor.style.bottom,
        height:actor.style.height,aspect:actor.style.aspectRatio,source:actor.querySelector('img')?.src,
        hp:S.hp,enemy:S.enemyActors[0].hp,down:S.enemyActors[0].down})''')
    assert all(before[k]==after[k] for k in ['left','bottom','height','aspect','source']),(before,after)
    assert after['hp']<before['hp'] and after['enemy']==before['enemy'] and after['down']
    page.screenshot(path=str(ROOT/'tests/results/actor_scale_struggle.png'))
    page.evaluate("go('lobby',true)")
    page.wait_for_function("S.room==='lobby'&&WardWinter.roomViewRenderer()?.loaded")
    page.evaluate("go('eastcorridor',true)")
    page.wait_for_function("S.room==='eastcorridor'&&WardWinter.roomViewRenderer()?.loaded")
    assert page.locator('.winter-actor.infected').count()==1
    checks.append('actual Struggle click keeps the same actor art, full size and floor anchor during its fall, costs health and restores the living enemy after reentry')
    assert not errors,errors
    browser.close()
(ROOT/'tests/results').mkdir(exist_ok=True)
(ROOT/'tests/results/actor_scale.json').write_text(json.dumps({'checks':checks,'native_opaque_bounds':bounds,'samples':samples,'javascript_errors':errors},indent=2)+'\n')
for check in checks:print('PASS',check)
