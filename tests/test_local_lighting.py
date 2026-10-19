"""Pixel checks that local power and native state overlays obey the same light."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
checks=[];errors=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);q=b.new_page(viewport={'width':1672,'height':941},service_workers='block');q.on('pageerror',lambda e:errors.append(str(e)));q.goto('http://127.0.0.1:8010');q.get_by_role('button',name='BEGIN INVESTIGATION').click();q.evaluate('nextIntro();nextIntro();nextIntro();add("Flashlight");S.enemyActors.forEach(a=>a.hp=0);WardWinter.enemies.project();S.pursuer.active=false;S.f.blackoutCount=2;WardScene.options.flashes=false;WardScene.options.motion=false')
 def ev(s):return q.evaluate(s)
 def ready():q.wait_for_function('WardWinter.roomViewRenderer()?.loaded&&!WardWinter.orbit.busy')
 def mean():return ev('''(()=>{const c=document.querySelector('.room-view-canvas'),d=c.getContext('2d').getImageData(c.width*.4,c.height*.4,Math.floor(c.width*.2),Math.floor(c.height*.2)).data;let v=0;for(let i=0;i<d.length;i+=4)v+=d[i]+d[i+1]+d[i+2];return v/(d.length/4*3);})()''')
 ev('S.room="morgue";S.roomView="front";S.roomViewRoom="morgue";S.f.power=1;S.lightOn=false;render()');ready();ev('WardWinter.roomViewEffects.stop();WardWinter.roomViewRenderer().effects(null);WardWinter.roomViewRenderer().light({brightness:1,torch:0})');bright=mean();ev('WardWinter.fitRoomView()');dark=mean();assert ev('WardNavigation.isDark(S.room)&&!lit()');assert dark<bright*.4,(dark,bright);ev('toggleLight();WardWinter.roomViewEffects.stop();WardWinter.roomViewRenderer().effects(null);WardWinter.roomViewRenderer().light({beam:[0,0]})');assert mean()>dark*2;checks.append('generator leaves an unpowered local circuit visibly dark; the actual flashlight brightens it')
 ev('S.room="security";S.roomViewRoom=null;S.lightOn=false;S.bat=60;render()');ready();ev('toggleLight();advanceTime(3)');assert ev('S.bat===60&&!S.lightOn&&!WardNavigation.isDark(S.room)&&lit()');checks.append('a powered circuit is lit without the flashlight and does not spend its battery')
 for view in ['front','rear']:
  q.evaluate('v=>{S.room="lobby";S.roomView=v;S.roomViewRoom="lobby";S.f.lobbyShutters=1;S.lightOn=false;render()}',view);ready();ev('WardWinter.roomViewEffects.ready');q.wait_for_timeout(250);ev('WardWinter.roomViewEffects.stop();WardWinter.roomViewEffects.draw(1000);WardWinter.roomViewRenderer().light({brightness:1,torch:0})');full=mean();ev('WardWinter.roomViewRenderer().light({brightness:.25,torch:0})');dim=mean();assert dim<full*.4,(view,dim,full)
 checks.append('both full-resolution shutter overlays receive room lighting instead of bypassing darkness')
 assert not errors,errors;b.close()
(ROOT/'tests/results/local_lighting.json').write_text(json.dumps({'checks':checks,'javascript_errors':errors},indent=2)+'\n')
print('\n'.join('PASS '+s for s in checks))
