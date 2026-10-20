"""A live mouse gesture survives scheduled scene/health/hallucination redraws."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];checks=[];errors=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);q=b.new_page(viewport={'width':1672,'height':941},service_workers='block',reduced_motion='reduce');q.on('pageerror',lambda e:errors.append(str(e)));q.goto('http://127.0.0.1:8010');q.get_by_role('button',name='BEGIN INVESTIGATION').click();q.evaluate('nextIntro();nextIntro();nextIntro();S.f.phoneRinging=false;S.enemyActors.forEach(a=>a.hp=0);WardWinter.enemies.project();S.pursuer.active=false;render()');q.wait_for_function('WardWinter.roomViewRenderer()?.loaded&&!WardWinter.orbit.busy')
 def frame():return q.locator('.room-view-frame').bounding_box()
 for _ in range(4):
  r=frame();x=r['x']+r['width']*.7;y=r['y']+r['height']*.12;before=q.evaluate('S.roomView');q.mouse.move(x,y);q.mouse.down();q.mouse.move(x-30,y,steps=3);q.evaluate('window.gestureFrame=document.querySelector(".room-view-frame");for(let i=0;i<5;i++)renderScene()');assert q.evaluate('WardWinter.orbit.holding&&window.gestureFrame.isConnected');q.mouse.move(x-r['width']*.4,y,steps=10);q.mouse.up();q.wait_for_function('WardWinter.roomViewRenderer()?.loaded&&!WardWinter.orbit.busy');assert q.evaluate('S.roomView')!=before;q.wait_for_timeout(420)
 checks.append('four real horizontal drags retain pointer ownership through repeated scheduled scene refreshes and change facing exactly once')
 r=frame();x=r['x']+r['width']*.65;y=r['y']+r['height']*.12;before=q.evaluate('S.roomView');q.mouse.move(x,y);q.mouse.down();q.mouse.move(x-25,y,steps=3);q.evaluate('S.f.shivering=1;renderScene()');assert not q.locator('#interactiveScene.winter-cold').count();q.mouse.up();q.wait_for_function('!WardWinter.orbit.holding&&document.querySelector("#interactiveScene.winter-cold")');assert q.evaluate('S.roomView')==before
 checks.append('a short drag does not turn the camera and replays its pending status refresh after release')
 q.wait_for_timeout(420);r=frame();q.mouse.move(r['x']+r['width']*.5,r['y']+10);q.mouse.down();q.evaluate('S.f.shivering=0;renderScene();window.dispatchEvent(new Event("blur"))');q.mouse.up();q.wait_for_function('!WardWinter.orbit.holding&&!document.querySelector("#interactiveScene.winter-cold")')
 checks.append('losing focus cancels a held pointer and releases the pending refresh instead of freezing rendering')
 assert not errors,errors;b.close()
(ROOT/'tests/results/mouse_refresh_v8.json').write_text(json.dumps({'checks':checks,'javascript_errors':errors},indent=2)+'\n');print('\n'.join('PASS '+v for v in checks))
