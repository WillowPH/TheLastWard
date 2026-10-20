"""Transparent caption overlays, native art fit and actual supply affordances."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];checks=[];errors=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);q=b.new_page(viewport={'width':1672,'height':941},service_workers='block');q.on('pageerror',lambda e:errors.append(str(e)));q.goto('http://127.0.0.1:8010');q.get_by_role('button',name='BEGIN INVESTIGATION').click();q.evaluate('nextIntro();nextIntro();nextIntro();S.f.phoneRinging=false;S.enemyActors.forEach(a=>a.hp=0);WardWinter.enemies.project();S.pursuer.active=false;render()')
 for w,h in [(1672,941),(1000,800),(390,844)]:
  q.set_viewport_size({'width':w,'height':h});q.wait_for_function('WardWinter.roomViewRenderer()?.loaded&&!WardWinter.orbit.busy');q.wait_for_timeout(120)
  for selector in ['.narrative-focus','.story-caption','.narration-block','.scene-thought']:
   assert q.locator(selector).evaluate('(n)=>getComputedStyle(n).backgroundColor')=='rgba(0, 0, 0, 0)',selector
  assert q.evaluate('(()=>{const n=document.querySelector("#captionText");return n.scrollHeight<=n.clientHeight+1;})()')
  assert not q.locator('.mouse-look-edge').count()
  if w>700:
   assert q.evaluate('(()=>{const r=document.querySelector(".room-view-frame").getBoundingClientRect(),c=document.querySelector(".narrative-focus").getBoundingClientRect();return c.top>=r.top&&c.bottom<=r.bottom&&c.left>=r.left&&c.right<=r.right;})()')
   assert q.locator('.narration-block').evaluate('(n)=>getComputedStyle(n).pointerEvents')=='none'
 checks.append('captions have no backing fill, retain readable fitted text and overlay native artwork on desktop/tablet; no view arrows')
 q.set_viewport_size({'width':1672,'height':941});q.evaluate('S.room="ward";S.roomView="rear";S.roomViewRoom="ward";render()');q.wait_for_function('WardWinter.roomViewRenderer()?.loaded')
 assert q.locator('[data-supply=ammo]').count()>0
 q.evaluate('S.ob.pistolRounds="done";renderScene()');q.wait_for_function('WardWinter.roomViewRenderer()?.loaded');assert not q.locator('[data-fixture=rearMedicine][data-supply=ammo]').count()
 checks.append('a remaining ammunition container has etched supply brackets which retire once its ammunition is taken')
 assert not errors,errors;b.close()
(ROOT/'tests/results/caption_v8.json').write_text(json.dumps({'checks':checks,'javascript_errors':errors},indent=2)+'\n');print('\n'.join('PASS '+s for s in checks))
