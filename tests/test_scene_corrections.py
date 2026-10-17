"""Regressions for reported item, phone, cover, orientation and travel defects."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];checks=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);page=b.new_page(viewport={'width':1600,'height':1000});errors=[];page.on('pageerror',lambda e:errors.append(str(e)));page.goto('http://127.0.0.1:8010');page.evaluate('newGame();nextIntro();nextIntro();nextIntro()')
 def ev(x,arg=None):return page.evaluate(x,arg)
 # Reject every nonadjacent pair through every public navigation entry point.
 result=ev('''()=>{const bad=[];let tested=0;S.pursuer.active=false;for(const from of WardChapter.rooms)for(const to of WardChapter.rooms){if(from===to||WardNavigation.edge(from,to))continue;S.room=from;S.prev=null;const before=JSON.stringify({room:S.room,prev:S.prev,t:S.t,f:S.f});for(const fn of [go,mapTravel,sceneDoorTravel]){fn(to);tested++;if(before!==JSON.stringify({room:S.room,prev:S.prev,t:S.t,f:S.f}))bad.push([from,to]);}}return {bad,tested}}''');assert not result['bad'],result
 checks.append(f"{result['tested']} nonadjacent travel attempts rejected without state/time changes")
 ev("S.room='lobby';S.prev=null;WardNavigation.until=0;sceneDoorTravel('eastcorridor',{detail:1});sceneDoorTravel('ward',{detail:1})");assert ev("S.room==='eastcorridor'")
 checks.append('rapid consecutive door activations cross only one room')
 ev("S.room='laundry';S.prev='wardservice';S.f.power=1;S.f.powerOut=0;S.f.pursuerEncounter=0;S.pursuer.active=false;S.lightOn=true;render()")
 page.locator('[data-fixture=locker]').click();assert not ev('S.f.hidingRoom');assert ev('S.lightOn');page.get_by_role('button',name='Stay in the room',exact=True).click();assert not ev('S.f.hidingRoom')
 page.locator('[data-fixture=locker]').click();page.get_by_role('button',name='Hide here',exact=True).click();assert ev("S.f.hidingRoom==='laundry'&&!S.lightOn");assert 'CONCEALED' in page.locator('#lightBtn').inner_text();assert page.locator('#lightBtn').is_disabled()
 assert page.locator('.c1-peek-scene').evaluate('(e)=>getComputedStyle(e).visibility')=='hidden';ev('toggleLight()');assert not ev('S.lightOn')
 ev("go('wardservice')");assert ev("S.room==='laundry'")
 page.get_by_role('button',name='Peek',exact=True).click();assert page.locator('.c1-peek-scene').evaluate('(e)=>getComputedStyle(e).visibility')=='visible'
 clip=page.locator('.c1-peek-scene').evaluate('(e)=>getComputedStyle(e).clipPath');assert '35%' in clip and '53%' in clip,clip
 page.get_by_role('button',name='Stop peeking',exact=True).click();assert page.locator('.c1-peek-scene').evaluate('(e)=>getComputedStyle(e).visibility')=='hidden'
 page.screenshot(path=str(ROOT/'tests/results/hidden-corrected.png'));page.get_by_role('button',name='Exit',exact=True).click()
 checks.append('cover requires consent; cancel preserves position/light; hidden view black; peek narrow; torch and travel blocked while hidden')
 ev("S.room='lobby';S.prev=null;S.lightOn=false;render()")
 before=page.locator('.c1-background').bounding_box();page.locator('[data-fixture=phone]').click();assert not page.locator('.c1-closeup').count();assert before==page.locator('.c1-background').bounding_box();assert page.locator('#sceneFocusOverlay').evaluate('(e)=>getComputedStyle(e).backgroundColor')=='rgba(0, 0, 0, 0)';assert page.get_by_role('button',name='Use telephone',exact=True).is_visible();page.screenshot(path=str(ROOT/'tests/results/phone-corrected.png'));ev('wardCloseFocus()')
 checks.append('phone opens contextual actions without enlarging or moving room artwork')
 ev("S.room='security';S.prev='lobby';S.f.power=0;S.f.powerOut=0;render()")
 assert page.locator('.c1-plane [data-destination=lobby]').count()==0
 assert 'Behind you' in page.locator('.c1-return-route [data-destination=lobby]').inner_text()
 page.get_by_role('button',name='Turn around',exact=True).click();assert page.locator('.c1-rear-travel[data-destination=lobby]').count()==1;ev('wardCloseFocus()')
 # Each edge has a declared destination-light state, including the former entry.
 ev("S.room='lobby';S.prev='security';S.f.power=0;render()")
 assert page.locator('[data-door-light=dark]').count()>=1
 assert ev("WardNavigation.isDark('eastcorridor')")
 ev('S.f.power=1;render()');assert not ev("WardNavigation.isDark('eastcorridor')")
 checks.append('entry route is behind player; turn-around view uses closed door; doorway shading follows destination circuit')
 for room in ev('WardChapter.rooms'):
  ev('r=>{S.room=r;render()}',room)
  assert not page.locator('.c1-item-overlay,.c1-physical:not(img)').count(),room
  page.wait_for_function("[...document.querySelectorAll('img.c1-physical')].every(i=>i.complete&&i.naturalWidth>0)")
 checks.append('all rooms omit CSS prop boxes and pasted inventory-thumbnail badges')
 assert not errors,errors
 b.close()
(ROOT/'tests/results/scene_corrections.json').write_text(json.dumps({'passed':checks,'count':len(checks)},indent=2))
for c in checks:print('PASS',c)
