from playwright.sync_api import sync_playwright
from pathlib import Path
import json
r=Path(__file__).resolve().parents[1];fail=[];counts=0
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--enable-unsafe-swiftshader']);q=b.new_page(viewport={'width':1672,'height':941});errors=[];q.on('pageerror',lambda e:errors.append(str(e)));q.goto('http://127.0.0.1:8010');q.get_by_role('button',name='BEGIN INVESTIGATION').click();q.evaluate('nextIntro();nextIntro();nextIntro()');q.evaluate('WardScene.options.snapMotion=false;S.enemyActors.forEach(a=>a.hp=0);WardWinter.enemies.project();S.pursuer.active=false;S.f.power=1;S.f.pharm=1;S.f.chapel=1;S.f.photoPuzzleSolved=0;S.f.researchers=1;S.f.drained=1')
 for room in q.evaluate('Object.keys(R)'):
  q.evaluate('r=>{S.room=r;S.prev=r;S.panoramaRoom=null;S.sceneFocus=null;render()}',room);q.wait_for_function('WardWinter.panoramaRenderer().loaded');points=q.evaluate('WardWinter.orbit.points()')
  for point in points:
   q.get_by_role('combobox',name='Look at a point of interest').select_option(point['id']);result=q.evaluate('''p=>{const selector=p.id.startsWith('door:')?'[data-door="'+p.id.slice(5)+'"]':'[data-fixture="'+p.id.slice(8)+'"]',n=document.querySelector(selector),r=n.getBoundingClientRect(),x=r.x+r.width/2,y=r.y+r.height/2,h=document.elementFromPoint(x,y);return {wanted:p.id,hit:h?.dataset.fixture||h?.dataset.door||h?.id||h?.tagName,ok:h===n,rect:[r.x,r.y,r.width,r.height]}}''',point);counts+=1
   if not result['ok']:fail.append({'room':room,**result})
  print(room,'checked',len(points),flush=True)
 b.close()
(r/'tests/results/panorama_targets.json').write_text(json.dumps({'count':counts,'failures':fail,'errors':errors},indent=2));assert not fail,fail;assert not errors,errors;print('PASS',counts,'available target centers receive the expected ordinary mouse hit')
