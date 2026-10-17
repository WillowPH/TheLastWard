"""Persistent aftermath and drainage views retain the fixed doorway layout."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json,sys
ROOT=Path(__file__).resolve().parents[1];url=sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8010';packaged='The_Last_Ward' in url;checks=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);page=b.new_page();page.goto(url)
 if packaged:page.context.set_offline(True)
 page.evaluate('newGame();nextIntro();nextIntro();nextIntro()')
 for room,flag,value,image in [('surgery','doctorWallSeen',1,'surgery_after'),('isoward','beggingPatientChoice','killed','isoward_after'),('tunnel','drained',1,'tunnel_drained')]:
  page.evaluate("a=>{S.room=a[0];S.f[a[1]]=a[2];S.sceneView='front';S.sceneViewRoom=S.room;S.cameraSchema=2;renderScene()}",[room,flag,value]);page.wait_for_function("document.querySelector('.c1-background').complete&&document.querySelector('.c1-background').naturalWidth>0")
  assert page.evaluate("n=>document.querySelector('.c1-background').src.endsWith(n+'.webp')||document.querySelector('.c1-background').src===WardEmbeddedAssets?.['assets/states/'+n+'.webp']",image)
  assert page.locator('.c1-plane [data-door]').count()==0
  if room=='surgery':assert page.evaluate("WardScene.sites().find(f=>f.id==='kessler').rect[1]===51")
  page.get_by_role('button',name='Turn around',exact=True).click();page.wait_for_function("document.querySelector('.c1-reverse-plane>img').complete&&document.querySelector('.c1-reverse-plane>img').naturalWidth>0")
  assert page.locator('.c1-reverse-plane [data-door]').count()==1
  if room=='tunnel':
   assert page.evaluate("document.querySelector('.c1-reverse-plane>img').src.endsWith('tunnel_rear_drained.webp')||document.querySelector('.c1-reverse-plane>img').src===WardEmbeddedAssets?.['assets/states/tunnel_rear_drained.webp']")
  checks.append(room+' persistent front/rear state images load; fixed rear portal retained')
 b.close()
(ROOT/'tests/results'/('state_layers_packaged.json' if packaged else 'state_layers.json')).write_text(json.dumps({'passed':checks,'count':len(checks)},indent=2))
for c in checks:print('PASS',c)
